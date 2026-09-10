---
title: Go SQL ドライバー
type: docs
weight: 110
toc: true
---

## 概要 {#overview}
`github.com/machbase/neo-client` は、Machbase 用の標準 Go `database/sql` ドライバーを提供します。
ネイティブ TCP クライアントを基盤とし、ネイティブポート（既定値 `5656`）を使用します。

アプリケーションやフレームワークが `database/sql` インターフェースを使用する場合に選択してください。
`database/sql` が不要な新規コードでは、通常は `machgo` が適しています。

### 前提条件 {#prerequisites}

- **Machbase サーバー**：ネイティブポートで接続可能な DBMS または Neo のインスタンス
- **Go 1.22 以降**：`github.com/machbase/neo-client` の要件
- **認証情報**：有効な Machbase ユーザーアカウント

## はじめに {#getting-started}

### インストール {#install}

```sh
go get github.com/machbase/neo-client@latest
```

### インポート {#import}

ブランク識別子を使用してドライバーパッケージをインポートします。
ドライバーは `machbase` という名前で自動登録されるため、別途 `sql.Register()` を呼び出す必要はありません。

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## 接続 {#connection}

### DSN 形式 {#dsn-format}

最も簡単な DSN は `server` キーを使用します。

```text
server=tcp://sys:manager@127.0.0.1:5656
```

セミコロン区切りのキーと値の組み合わせで、追加オプションを指定できます。

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### サポートする DSN キー {#supported-dsn-keys}

| キー | 説明 |
|-----|-------------|
| `server` | サーバー URL。例：`tcp://user:password@127.0.0.1:5656` |
| `host`, `port` | サーバーホストとポートを個別に指定 |
| `user` | ログインユーザー |
| `password` | ログインパスワード |
| `fetch_rows` | 1 回の通信で取得する行数 |
| `statement_cache` | ステートメントキャッシュ：`auto`、`on`、`off` |
| `io_metrics` | I/O メトリクスを有効にするか：`true`、`false` |
| `alternative_servers` | 代替サーバー。例：`127.0.0.2:5656` |
| `alternative_host`, `alternative_port` | 代替ホストとポートを個別に指定 |

## 検索の例 {#query-example}

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
		"io_metrics=true",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()

	rows, err := db.QueryContext(ctx, `SELECT * FROM M$SYS_TABLES ORDER BY NAME`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		panic(err)
	}
	fmt.Println("Columns:", columns)

	var (
		name        string
		typ         int
		dbID        int64
		id          int64
		userID      int
		columnCount int
		flag        int
	)

	for rows.Next() {
		if err := rows.Scan(&name, &typ, &dbID, &id, &userID, &columnCount, &flag); err != nil {
			panic(err)
		}
		fmt.Println(name, typ, dbID, id, userID, columnCount, flag)
	}

	if err := rows.Err(); err != nil {
		panic(err)
	}
}
```

## 挿入の例 {#insert-example}

`EXAMPLE` という Tag テーブルへ行を挿入する例を示します。

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()
	ts := time.Now()

	for i := 0; i < 10; i++ {
		result, err := db.ExecContext(
			ctx,
			`INSERT INTO EXAMPLE VALUES (?, ?, ?)`,
			"example-client",
			ts.Add(time.Second*time.Duration(i)),
			3.14*float64(i),
		)
		if err != nil {
			panic(err)
		}

		affected, err := result.RowsAffected()
		if err != nil {
			panic(err)
		}
		fmt.Println("Rows affected:", affected)
	}
}
```

## 注意事項と制限 {#notes-and-limitations}

- `?` のような位置パラメーターを使用します。名前付きパラメーターは未サポートです。
- 通常どおり `sql.DB` によるコネクションプールを利用できます。
- 明示的トランザクションは未サポートで、`Begin` と `BeginTx` はエラーを返します。
- `LastInsertId()` はサポートされません。
- パラメーター型はドライバーの実装に従います。一般的な SQL 型、`time.Time`、`[]byte`、`net.IP` をサポートしますが、`bool` パラメーターは未サポートです。
