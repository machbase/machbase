---
toc: true
title: CGo クライアント
type: docs
weight: 150
draft: true
---

## 概要 {#개요}

`machcli`パッケージは、MachbaseのネイティブCクライアントライブラリのGoラッパーです。GoからMachbaseデータベースへの高性能なアクセスを提供します。Cライブラリの性能と効率を活用しながら、標準のdatabase/sqlの方式に沿った使い慣れたGo APIを利用できます。

### 前提条件 {#사전-요구사항}

- **CGo環境**：Cライブラリのラッパーのため、CGoを有効にしたGo環境が必要
- **Machbase Neo Server**: 実行中のMachbase Neoサーバーインスタンス
- **Go 1.24+**: 互換性を確保するための新しいGoバージョン

## はじめに {#시작하기}

### Import {#import}

まず、必要なパッケージをインポートします。`machcli`パッケージは、MachbaseのCクライアントライブラリのGoラッパーを提供します。

```go
import (
    "context"
    "fmt"
    "time"
    
    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machcli"
)
```

{{< callout type="info" >}}
**CGoの要件**：`machcli`はCライブラリをラップするため、ビルド環境がCGoに対応している必要があります。`CGO_ENABLED=1`であることを確認してください。
{{< /callout >}}

### 設定 {#설정}

`Config`構造体で、データベースの接続パラメーターを設定します。接続の動作と性能を調整できます。

```go
conf := &machcli.Config{
    Host:         "127.0.0.1",    // Machbaseサーバーのホスト
    Port:         5656,           // Machbaseサーバーのポート
    MaxOpenConn:  0,              // 接続数の上限
    MaxOpenQuery: 0,              // 同時実行クエリ数の上限
}

// 設定からデータベースインスタンスを作成
db, err := machcli.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 設定 パラメーター {#설정-매개변수}

| パラメーター | 説明 | 値 |
|---------|------|---|
| `MaxOpenConn` | 開いている接続の最大数 | `< 0`：無制限<br>`0`：CPU数×係数<br>`> 0`：指定した上限 |
| `MaxOpenConnFactor` | MaxOpenConnが0の場合の係数 | 既定値： 1.5 |
| `MaxOpenQuery` | 同時実行クエリの最大数 | `< 0`：無制限<br>`0`：CPU数×係数<br>`> 0`：指定した上限 |
| `MaxOpenQueryFactor` | MaxOpenQueryが0の場合の係数 | 既定値： 1.5 |

{{< callout type="tip" >}}
**性能のヒント**：高スループットのアプリケーションでは、システムリソースと想定する負荷に基づき、明示的な上限を設定することを検討してください。
{{< /callout >}}

### 接続設定 {#연결-설정}

設定したデータベースインスタンスから、Machbaseサーバーへの接続を作成します。

```go
ctx := context.Background()
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close() // 処理の完了時に必ず接続を閉じます
```

接続はパスワード認証に対応しています。
- `api.WithPassword(user, password)`

{{< callout type="warning" >}}
**接続管理**：接続を確実に解放するために、必ず`defer conn.Close()`を使用してください。
{{< /callout >}}

## データベース操作 {#데이터베이스-작업}

### 単一行クエリ (QueryRow) {#단일-행-쿼리-queryrow}

結果がちょうど1行の場合は、`QueryRow`を使用します。単一行のクエリに最適化されており、自動的にリソースを解放します。

```go
var name = "tag1"
var tm time.Time
var val float64

// 単一行を返すクエリを実行
row := conn.QueryRow(ctx, 
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY TIME DESC LIMIT 1`, 
    name)

// クエリの実行エラーを確認
if err := row.Err(); err != nil {
    panic(err)
}

// 結果を変数にスキャン
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

// 表示用にローカルタイムゾーンに変換
tm = tm.In(time.Local)
fmt.Println("name:", name, "time:", tm, "value:", val)
```

**要点：**
- SQLインジェクションを防ぐため、`?`プレースホルダーを使ったパラメーター化クエリを使用
- スキャン前に必ず`row.Err()`を確認
- `Scan()`は、データベースとGoの型変換を自動処理

### 複数行クエリ (Query) {#다중-행-쿼리-query}

複数行を取得するには、`Query`を使用します。反復処理できる`Rows`オブジェクトを返します。

```go
var name = "tag1"
var tm time.Time
var val float64

// 複数行を返すクエリを実行
rows, err := conn.Query(ctx, 
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY TIME DESC LIMIT 10`, 
    name)
if err != nil {
    panic(err)
}
defer rows.Close() // 重要：リソースを解放するため、必ずrowsを閉じます

// 返されたすべての行を反復処理
for rows.Next() {
    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    tm = tm.In(time.Local)
    fmt.Println("name:", name, "time:", tm, "value:", val)
}
```

**注意事項：**
- リソースリークを防ぐため、必ず`defer rows.Close()`を使用
- `rows.Next()`を使う、Go開発者に馴染みのあるイテレーター方式

### データの変更 (Exec) {#데이터-수정-exec}

INSERT、DELETE、DDL文には`Exec`を使用します。実行情報を含む結果オブジェクトを返します。

```go
var name = "tag1"
var tm = time.Now()
var val = 3.14

// INSERT文を実行
result := conn.Exec(ctx, 
    `INSERT INTO example_table VALUES(?, ?, ?)`, 
    name, tm, val)

// 実行エラーを確認
if err := result.Err(); err != nil {
    panic(err)
}

// 実行結果を取得
fmt.Println("RowsAffected:", result.RowsAffected()) 
fmt.Println("Message:", result.Message())
```

**使用例：**
- **INSERT**: テーブルへの新規レコードの追加
- **DELETE**: レコードの削除
- **DDL**: テーブルとインデックスの作成・変更

### 高性能な一括挿入 (Appender) {#고성능-대량-삽입-appender}

高スループットのデータ挿入には、`Appender`インターフェースを使用します。時系列データの取り込みに最適な性能を提供します。

```go
// 重要：Appender専用の接続を使用
// 使用中のAppenderがある接続を他の処理に使用しないでください
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close()

// 対象テーブルのAppenderを作成
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close() // 残りのデータをフラッシュするため、必ずAppenderを閉じます

// 高速な一括挿入
for i := range 10_000 {
    err := apd.Append("tag1", time.Now(), 1.23*float64(i))
    if err != nil {
        panic(err)
    }
}
```

**Appenderのフラッシュ**

クライアントのバッファーに残るデータを、ネットワーク経由でサーバーにフラッシュします。

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

**Appenderの推奨事項：**

{{< callout type="warning" >}}
**接続の分離**：使用中のAppenderがある接続を、他のデータベース操作に使用しないでください。append専用の接続を作成してください。
{{< /callout >}}

{{< callout type="tip" >}}
**性能**：Appenderは時系列ワークロード向けに設計されており、適切なバッチ処理により毎秒数百万件の挿入を達成できます。
{{< /callout >}}

- **バッチサイズ**：Appenderは内部でバッチ処理を自動的に実行
- **エラー処理**：重要なアプリケーションでは、各`Append()`呼び出しのエラーを確認
- **リソースの解放**：データを確実にフラッシュするため、Appenderで必ず`Close()`を実行

## 完全な例 {#완전한-예제}

すべての概念を示す完全な例です。

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machcli"
)

func main() {
    // データベースの接続設定
    conf := &machcli.Config{
        Host: "127.0.0.1",
        Port: 5656,
        MaxOpenConn: 10,
        MaxOpenQuery: 5,
    }
    
    db, err := machcli.NewDatabase(conf)
    if err != nil {
        panic(err)
    }
    ctx := context.Background()
    
    // データベースに接続
    conn, err := db.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()
    
    // サンプルテーブルの作成
    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) primary key,
            time DATETIME basetime,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }
    
    // サンプルデータの挿入
    for i := 0; i < 5; i++ {
        result := conn.Exec(ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i), time.Now(), float64(i)*1.5)
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }
    
    // データの検索
    rows, err := conn.Query(ctx, `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()
    
    fmt.Println("Retrieved data:")
    for rows.Next() {
        var name string
        var tm time.Time
        var value float64
        
        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        tm = tm.Local()
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n", 
            name, tm.Format(time.RFC3339), value)
    }
}
```

この例は、接続設定からデータ操作までの一連の手順を示し、Machbaseを使用するGo開発者に`machcli`の機能と使いやすさを示します。
