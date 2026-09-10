---
toc: true
title: SQLドライバー
type: docs
weight: 110
draft: true
---

## 概要 {#개요}
`github.com/machbase/neo-client`パッケージは、Machbase Neo用の標準Go `database/sql`ドライバーを提供します。
このドライバーはネイティブTCPクライアントに基づき、ネイティブポート（既定値`5656`）を使用します。

アプリケーションやフレームワークがGoの`database/sql`インターフェースを必要とする場合は、このドライバーを使用してください。
`database/sql`との互換性が不要な新規コードには、通常は`machgo`が適しています。

### 前提条件 {#사전-요구사항}

- **Machbase Neo Server**: ネイティブポートでアクセスできる実行中のサーバー
- **Go 1.22+**: `github.com/machbase/neo-client`の要件
- **アカウント情報**：有効なMachbaseユーザーアカウント

## はじめに {#시작하기}

### インストール {#설치}

```sh
go get github.com/machbase/neo-client@latest
```

### Import {#import}

ドライバーパッケージをブランク識別子でインポートします。
ドライバー名`machbase`で自動登録されるため、別途`sql.Register()`を呼び出す必要はありません。

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## 接続 {#연결}

### DSN形式 {#dsn-형식}

最も簡単なDSNは、`server`キーを使用する形式です。

```text
server=tcp://sys:manager@127.0.0.1:5656
```

セミコロンで区切ったオプションを追加できます。

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### 対応するDSNキー {#지원되는-dsn-키}

| キー | 説明 |
|----|------|
| `server`       | `tcp://user:password@127.0.0.1:5656`形式のサーバーURL |
| `host`, `port` | サーバーのホストとポートを個別に指定 |
| `user`         | ログインユーザー |
| `password`     | ログインパスワード |
| `fetch_rows`   | 1回のラウンドトリップで取得する行数 |
| `statement_cache` | ステートメントキャッシュのモード：`auto`、`on`、`off` |
| `io_metrics`   | I/Oメトリクスを有効にするかどうか：`true`、`false` |
| `alternative_servers` | `127.0.0.2:5656`形式の代替サーバーアドレス |
| `alternative_host`, `alternative_port` | 代替サーバーのホストとポートを個別に指定 |

## 検索 例 {#조회-예제}

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

## 挿入の例 {#입력-예제}

次の例は、`EXAMPLE`というタグテーブルに行を挿入します。

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

## 注意事項と制限 {#참고-사항-및-제한-사항}

- パラメーターには`?`形式の位置プレースホルダーを使用します。名前付きパラメーターには対応していません。
- `database/sql`の接続プールは、通常の`sql.DB`の方式で動作します。
- 明示的なトランザクションには対応していないため、`Begin`と`BeginTx`はエラーを返します。
- `LastInsertId()`には対応していません。
- パラメーターの型はドライバーの実装に従います。一般的なSQL型、`time.Time`、`[]byte`、`net.IP`に対応していますが、`bool`パラメーターには対応していません。
