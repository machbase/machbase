---
title: Go クライアント
type: docs
weight: 100
toc: true
---

## 概要 {#overview}

`machgo` は、Machbase ネイティブプロトコルに接続する純粋な Go クライアントです。
`machcli` と同じ API スタイルを提供し、CGo に依存しません。
Go だけのツールチェーンでネイティブポートの性能を利用する場合に適しています。

### `machgo` の利点 {#why-use-machgo}

- **CGo 不要**：Go だけの環境でビルド、配布できます。
- **ネイティブプロトコル**：ネイティブポート（既定値 `5656`）で接続します。
- **`machcli` と互換の API**：接続、検索、APPEND のパターンを再利用できます。
- **本番向け**：コンテナーや複数プラットフォームへの Go の配布に適しています。

### 前提条件 {#prerequisites}

- **サーバー**：ネイティブポートで接続可能な DBMS または Neo
- **Go 1.22 以降**：新しい Go バージョンを推奨
- **ネットワーク**：ネイティブポート（既定値 `5656`）に到達可能であること

## はじめに {#getting-started}

### インストール {#install}

```sh
go get github.com/machbase/neo-client@latest
```

### インポート {#import}

API パッケージと `machgo` クライアントをインポートします。

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### 設定 {#configuration}

`machgo.Config` でホスト、ポート、同時実行数を設定します。

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // サーバーホスト
    Port:         5656,          // ネイティブポート
    MaxOpenConn:  0,             // 接続数の上限
    MaxOpenQuery: 0,             // 同時クエリー数の上限
}

// データベースインスタンスを作成
// API の使用方法は machcli と同じ
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 設定パラメーター {#configuration-parameters}

| パラメーター | 説明 | 値 |
|-----------|-------------|--------|
| `MaxOpenConn` | 最大接続数 | `< 0`：無制限<br>`0`：CPU 数 × 係数<br>`> 0`：指定値 |
| `MaxOpenConnFactor` | `MaxOpenConn` が `0` の場合の係数 | 既定値：1.5 |
| `MaxOpenQuery` | 最大同時クエリー数 | `< 0`：無制限<br>`0`：CPU 数 × 係数<br>`> 0`：指定値 |
| `MaxOpenQueryFactor` | `MaxOpenQuery` が `0` の場合の係数 | 既定値：1.5 |

#### FlowControl の動作 {#flowcontrol-behavior}

`MaxOpenConn` と `MaxOpenQuery` はフロー制御の上限です。
`-1` を指定すると、その項目の制限を無効にします。

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // 接続のフロー制御を無効化
    MaxOpenQuery: -1, // クエリーのフロー制御を無効化
}
```

### 接続の確立 {#establishing-connection}

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

### 接続ごとの調整 {#connection-level-tuning-options}

`Connect()` 時に、接続単位で設定を上書きできます。
`machgo.Config` の全体の既定値を維持しつつ、個別の接続を調整できます。

#### 繰り返し SQL 用の StatementCache {#statementcache-for-repeated-sql}

1つの接続で同じ SQL を繰り返す場合、
プリペアードステートメントの再利用で性能を改善できます。

`machgo.Config.StatementCache` を既定値とし、`api.WithStatementCache(...)` で接続ごとに上書きします。

```go {linenos=table,linenostart=1,hl_lines=[5,16]}
// 接続 A：ステートメントを積極的に再利用
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// 接続 B：この接続だけ再利用を無効化
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

#### 先読み件数 `FetchRows` {#fetchrows-pre-fetch-size}

`FetchRows` は、1回のフェッチでサーバーから先読みする最大レコード数です。
`machgo.Config.FetchRows` を既定値とし、`api.WithFetchRows(...)` で上書きします。
既定値は `1000` です。

{{< callout type="warning" >}}
実際の負荷を検証せずに、極端に大きい値や小さい値を設定しないでください。
ネットワーク遅延やクエリー特性によっては、性能が大きく低下し、メモリ使用量が増えます。
{{< /callout >}}

```go {linenos=table,linenostart=1,hl_lines=[5]}
// 接続 C：スキャン中心の処理向けに先読み件数を増やす
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
接続には必ず `Close()` を呼び、リソースを解放してください。
{{< /callout >}}

## データベース操作 {#database-operations}

### 単一行の検索（`QueryRow`） {#single-row-query-queryrow}

結果が 1行の場合は `QueryRow` を使用します。

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

### 複数行の検索（`Query`） {#multiple-row-query-query}

複数行の結果には `Query` を使用します。

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

### データの変更（`Exec`） {#data-modification-exec}

INSERT、DELETE、DDL には `Exec` を使用します。

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

## 高速な一括入力（`Appender`） {#high-performance-bulk-insert-appender}

高スループットの取り込みには、専用接続で `Appender` を使用します。

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

クライアントからサーバーへ送信するバッファーのしきい値を、次のように調整できます。

`Append()` のデータは内部バッファーに蓄積され、設定したしきい値に達すると送信されます。
バイト数、行数、遅延（バッファー内の最古と最新のレコードの時間差）を指定できます。
いずれかのしきい値を超えると、バッファー内のデータを送信します。

- `WithBatchMaxRows(rows)`：既定値 `512`、最小値 `1`
- `WithBatchMaxBytes(bytes)`：既定値 `512KB`、最小値 `4KB`
- `WithBatchMaxDelay(duration)`：既定値 `5ms`、最小値 `1ms`
- `WithBatchMaxDelay(0)`：時間によるしきい値を無効化

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MB のしきい値
    WithBatchMaxRows(2000).            // 行数のしきい値
    WithBatchMaxDelay(500 * time.Millisecond) // 遅延のしきい値
```

フラッシュの例：

`Flush()` は、プログラムから明示的にフラッシュするメソッドです。
自動フラッシュと異なり、バイト数、行数、遅延の設定にかかわらず、蓄積したデータを直ちに送信します。

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

{{< callout type="warning" >}}
有効な `Appender` を持つ接続では、通常のクエリーを実行しないでください。
APPEND には専用の接続を使用します。
{{< /callout >}}

## 完全な例 {#complete-example}

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

    result = conn.Exec(ctx, `EXEC TABLE_FLUSH(sample_data)`)
    if err := result.Err(); err != nil {
        log.Fatal(err)
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

`machcli` と同じ処理手順なので、既存コードを少ない変更で移行できます。
