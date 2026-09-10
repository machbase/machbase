---
toc: true
title: Goクライアントのチュートリアル
type: docs
weight: 300
---

## 概要 {#개요}

`machgo`パッケージは、Machbaseのネイティブプロトコルにアクセスする純粋なGoクライアントです。
CGoに依存せず、高性能なデータ処理アプリケーションを実装するために設計されています。
接続管理、クエリ、Appenderを含む、使い慣れた形式のAPIを提供します。

### machgoを使用する理由 {#machgo를-사용하는-이유는}

- **CGoへの依存なし**：純粋なGoツールチェーンでビルド・配布可能
- **ネイティブプロトコルへのアクセス**：Machbaseのネイティブポート（既定値`5656`）で接続
- **Goに適したAPI**：Go標準のdatabase/sqlに似た開発方法
- **運用への適合性**：コンテナやクロスプラットフォームでの配布に適合

### 前提条件 {#사전-요구사항}

- **Machbase Neo Server**: 実行中のMachbase Neoサーバーインスタンス
- **Go 1.24+**: 互換性を確保するための新しいGoバージョン

### インストール {#설치}

```sh
go get github.com/machbase/neo-server/v8
```

## はじめに {#시작하기}

### Import {#import}

まず、必要なパッケージをインポートします。`machgo`パッケージは、Machbase用のGoネイティブクライアントを提供します。

```go
import (
    "context"
    "fmt"
    "time"
    
    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machgo"
)
```

### 設定 {#설정}

`Config`構造体で、データベースの接続パラメーターを設定します。接続の動作と性能を調整できます。

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",    // Machbaseサーバーのホスト
    Port:         5656,           // Machbaseサーバーのポート
    MaxOpenConn:  -1,             // 接続数の上限, -1: 無制限
    MaxOpenQuery: -1,             // 同時実行クエリ数の上限
    StatementCache: api.StatementCacheAuto,
}

// 設定からデータベースインスタンスを作成
db, err := machgo.NewDatabase(conf)
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

接続ごとのオプション`api.WithStatementCache(...)`と`api.WithFetchRows(...)`を使って、
ワークロードに合わせたチューニングもできます。

#### ステートメントキャッシュと性能改善 {#statement-cache와-성능-개선-포인트}

`StatementCache`は、同じ接続で繰り返し実行するSQLのプリペアドステートメントを再利用します。
SQLを繰り返し実行する割合が高いワークロードでは、準備処理のオーバーヘッドを減らし、スループットとレイテンシを
ともに改善できます。

代表的な使用方法：

- **`api.StatementCacheAuto`**: 繰り返しクエリの多い一般的な検索サービスに推奨
- **`api.StatementCacheOn`**: 繰り返しクエリとINSERTが多い場合
- **`api.StatementCacheOff`**: SQLテキストが頻繁に変わり、再利用率が低い場合

```go
// 繰り返すSQLが多い接続：ステートメントキャッシュを有効化
connA, err := db.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// 動的SQLが多い接続：この接続だけでキャッシュを無効化
connB, err := db.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheOff),
)
if err != nil {
    panic(err)
}
defer connB.Close()
```

{{< callout type="tip" >}}
**性能のヒント**：ワーカーが同じSQLを高頻度で繰り返し呼び出す構成では、
`StatementCacheAuto`だけでもCPU使用量と応答遅延を大きく改善できる場合があります。
{{< /callout >}}

#### FetchRowsと検索性能 {#fetchrows와-조회-성능}

`FetchRows`は、1回のフェッチでサーバーから先読みするレコード数を制御します。
大量スキャンを行うクエリで、ネットワークの往復回数とスループットに直接影響します。

- `FetchRows`を大きくする：往復回数が減り、広範囲のスキャンのスループット改善に有利
- `FetchRows`を小さくする：フェッチごとのメモリ使用量が減り、短いクエリのレイテンシ安定化に有利

既定値は通常`1000`です。実際のワークロードで検証して調整してください。

```go
// 大量スキャンのワークロード用にプリフェッチサイズを増やす
connC, err := db.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithFetchRows(5000),
)
if err != nil {
    panic(err)
}
defer connC.Close()
```

{{< callout type="warning" >}}
検証せずに極端に大きい値や小さい値を設定しないでください。クエリの形式やネットワーク遅延によって、
メモリ使用量の増加や性能低下が発生する可能性があります。
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

#### Appenderのバッチオプションとチューニング {#appender-batch-옵션과-튜닝}

Appenderは、データをメモリバッファーに蓄積し、しきい値に達するとサーバーに送信します。
しきい値は、以下のオプションで制御できます。

- `WithBatchMaxRows(rows)`
- `WithBatchMaxBytes(bytes)`
- `WithBatchMaxDelay(duration)`

既定値と最小値：

- `WithBatchMaxBytes`: 既定値`512KB`、最小値`4KB`
- `WithBatchMaxRows`: 既定値`512`、最小値`1`
- `WithBatchMaxDelay`: 既定値`5ms`、最小値`1ms`
- `WithBatchMaxDelay(0)`: 時間に基づくしきい値を無効化

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).          // 1MB
    WithBatchMaxRows(2000).                  // 行数のしきい値
    WithBatchMaxDelay(500 * time.Millisecond) // 遅延のしきい値
```

これらのオプションは、性能チューニングの要点です。

- しきい値を大きくすると、ネットワークの往復が減り、スループット改善に有利
- しきい値を小さくすると、レコードごとの遅延とメモリ使用量の抑制に有利

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
    "github.com/machbase/neo-server/v8/api/machgo"
)

func main() {
    // データベースの接続設定
    conf := &machgo.Config{
        Host: "127.0.0.1",
        Port: 5656,
        MaxOpenConn: 10,
        MaxOpenQuery: 5,
    }
    
    db, err := machgo.NewDatabase(conf)
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

この例は、接続設定からデータ操作までの一連の手順と、Machbaseを使用するGo開発者向けの推奨パッケージ`machgo`の使用方法を示します。

関連情報：[Goネイティブクライアントリファレンス](/dbms/development-tools-integration/go/)
