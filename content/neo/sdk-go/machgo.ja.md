---
toc: true
title: Go クライアント
type: docs
weight: 100
draft: true
---

## 概要 {#개요}

`machgo`パッケージは、Machbaseのネイティブプロトコルにアクセスするための純粋なGoクライアントです。
`machcli`と同じ形式のAPIを提供し、CGoには依存しません。
Goツールチェーンだけでネイティブポートの性能を活用するには、`machgo`が適しています。

### machgoを使用する理由 {#machgo를-사용하는-이유}

- **CGoへの依存なし**：純粋なGo環境でビルド・配布可能
- **ネイティブプロトコルへのアクセス**：Machbaseのネイティブポート（既定値`5656`）で接続
- **machcliとのAPI互換性**：同じ接続・クエリ・Appenderの方式を再利用可能
- **運用への適合性**：コンテナ環境とクロスプラットフォームのGo配布に適合

### 前提条件 {#사전-요구사항}

- **Machbase Neo Server**: 実行中のMachbase Neoサーバーインスタンス
- **Go 1.22+**: 最新のGoバージョンを推奨
- **ネットワークアクセス**：ネイティブポート（既定値`5656`）への接続が可能

## はじめに {#시작하기}

### インストール {#설치}

```sh
go get github.com/machbase/neo-client@latest
```

### Import {#import}

APIパッケージと`machgo`クライアントパッケージをインポートします。

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### 設定 {#설정}

`machgo.Config`で、ホスト・ポートおよび並行処理のオプションを設定します。

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbaseサーバーのホスト
    Port:         5656,          // Machbaseのネイティブポート
    MaxOpenConn:  0,             // 接続数の上限
    MaxOpenQuery: 0,             // 同時実行クエリ数の上限
}

// データベースインスタンスの作成
// APIの使用方法はmachcliと同じ
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 設定 パラメーター {#설정-매개변수}

| パラメーター | 説明 | 値 |
|-----------|-------------|--------|
| `MaxOpenConn` | 開いている接続の最大数 | `< 0`：無制限<br>`0`：CPU数×係数<br>`> 0`：指定した上限 |
| `MaxOpenConnFactor` | MaxOpenConnが0の場合の係数 | 既定値： 1.5 |
| `MaxOpenQuery` | 同時実行クエリの最大数 | `< 0`：無制限<br>`0`：CPU数×係数<br>`> 0`：指定した上限 |
| `MaxOpenQueryFactor` | MaxOpenQueryが0の場合の係数 | 既定値： 1.5 |

#### FlowControlの動作 {#flowcontrol-동작}

`MaxOpenConn`と`MaxOpenQuery`は、FlowControlの上限値です。
いずれかを`-1`にすると、その項目の制限が無効になります（その項目のFlowControlなし）。

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // 接続数のFlowControlを無効化
    MaxOpenQuery: -1, // クエリのFlowControlを無効化
}
```

### 接続設定 {#연결-설정}

```go
ctx := context.Background()
conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    panic(err)
}
defer conn.Close()
```

認証オプション：

- `api.WithPassword(user, password)`

### 接続ごとのチューニングオプション {#연결-단위-튜닝-옵션}

`machgo`は、`Connect()`の呼び出し時に接続ごとの設定の上書きに対応しています。
`machgo.Config`のグローバルな既定値を維持しながら、接続ごとに調整できます。

#### 繰り返すSQL用のStatementCache {#반복-sql을-위한-statementcache}

1つの接続の有効期間中に同じSQLを繰り返し実行する場合、
プリペアドステートメントの再利用で性能を向上できます。

既定のモードは`machgo.Config.StatementCache`に設定し、
接続ごとに`api.WithStatementCache(...)`で上書きできます。

```go  {linenos=table,linenostart=1,hl_lines=[5,16]}
// Connection A: ステートメントを積極的に再利用
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// Connection B: この接続だけでステートメントの再利用を無効化
connB, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheOff),
)
if err != nil {
    panic(err)
}
defer connB.Close()
```

#### FetchRowsのプリフェッチサイズ {#fetchrows-pre-fetch-크기}

`FetchRows`は、1回のフェッチでサーバーから先読みするレコードの最大数を制御します。
既定値は`machgo.Config.FetchRows`に設定し、
接続ごとに`api.WithFetchRows(...)`で上書きできます。
既定値は`1000`です。

{{< callout type="warning" >}}
ワークロードを検証せずに、`FetchRows`を極端に大きい値や小さい値に設定しないでください。
ネットワーク遅延とクエリの特性によっては、不適切な値が大幅な性能低下やメモリ消費の増加を引き起こします。
{{< /callout >}}

```go  {linenos=table,linenostart=1,hl_lines=[5]}
// Connection C: 大量スキャンのワークロード用に大きなプリフェッチを設定
connC, err := mdb.Connect(
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
リソースを解放するために、接続では必ず`Close()`を呼び出してください。
{{< /callout >}}

## データベース操作 {#데이터베이스-작업}

### 単一行クエリ (`QueryRow`) {#단일-행-쿼리-queryrow}

結果がちょうど1行の場合は、`QueryRow`を使用します。

```go
var name = "tag1"
var tm time.Time
var val float64

row := conn.QueryRow(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 1`,
    name,
)
if err := row.Err(); err != nil {
    panic(err)
}
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

fmt.Println("name:", name, "time:", tm.Local(), "value:", val)
```

### 複数行クエリ (`Query`) {#다중-행-쿼리-query}

複数行の結果を取得する場合は、`Query`を使用します。

```go
rows, err := conn.Query(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 10`,
    "tag1",
)
if err != nil {
    panic(err)
}
defer rows.Close()

for rows.Next() {
    var tm time.Time
    var val float64

    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    fmt.Println("time:", tm.Local(), "value:", val)
}
```

### データの変更 (`Exec`) {#데이터-수정-exec}

INSERT、DELETE、DDL文の実行には`Exec`を使用します。

```go
result := conn.Exec(
    ctx,
    `INSERT INTO example_table VALUES(?, ?, ?)`,
    "tag1", time.Now(), 3.14,
)
if err := result.Err(); err != nil {
    panic(err)
}

fmt.Println("RowsAffected:", result.RowsAffected())
fmt.Println("Message:", result.Message())
```

## 高性能な一括挿入 (`Appender`) {#고성능-대량-입력-appender}

高スループットの取り込みには、専用の接続と`Appender`を使用します。

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

for i := range 10_000 {
    if err := apd.Append("tag1", time.Now(), float64(i)); err != nil {
        panic(err)
    }
}
```

Appenderは、アプリケーションからの`Append()`のデータをバッファーに蓄積し、指定したしきい値に達するとサーバーに送信します。
しきい値には、バイト数、行数、バッファー内で最も古いレコードと最新レコードの到着時刻の差を設定できます。
いずれかのしきい値を超えると、バッファーをサーバーに送信します。

サーバーへの送信バッファーのしきい値は、以下のオプションで調整できます。

- `WithBatchMaxRows(rows)` : 既定値 `512`, 最小値 `1`
- `WithBatchMaxBytes(bytes)` : 既定値 `512KB`, 最小値 `4KB`
- `WithBatchMaxDelay(duration)` : 既定値 `5ms`, 最小値 `1ms`
- `WithBatchMaxDelay(0)`を指定すると、時間に基づくしきい値を使用しません。

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MBのしきい値
    WithBatchMaxRows(2000).            // 行数のしきい値
    WithBatchMaxDelay(500 * time.Millisecond) // 最大遅延のしきい値
```

Appenderのフラッシュの例：

`Flush()`は、プログラムからフラッシュを行うメソッドです。
しきい値による自動フラッシュとは異なり、バイト数・行数・遅延のしきい値に関係なく、現在のバッファーのレコードを直ちにサーバーへ送信します。

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

{{< callout type="warning" >}}
使用中のAppenderがある接続で、通常のクエリを実行しないでください。
append処理には、別の接続を使用してください。
{{< /callout >}}

## 完全な例 {#전체-예제}

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    conf := &machgo.Config{
        Host:         "127.0.0.1",
        Port:         5656,
        MaxOpenConn:  -1,
        MaxOpenQuery: -1,
    }

    mdb, err := machgo.NewDatabase(conf)
    if err != nil {
        log.Fatal(err)
    }

    ctx := context.Background()
    conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) PRIMARY KEY,
            time DATETIME BASETIME,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    for i := 0; i < 5; i++ {
        result := conn.Exec(
            ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i),
            time.Now(),
            float64(i)*1.5,
        )
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }

    rows, err := conn.Query(ctx, 
        `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var name string
        var tm time.Time
        var value float64

        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n",
            name, tm.Local().Format(time.RFC3339), value)
    }
}
```

この手順は`machcli`と同じになるように設計されており、既存コードを最小限の変更で移行できます。
