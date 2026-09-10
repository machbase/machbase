---
type: docs
title: '11.9 Go'
weight: 90
toc: true
aliases:
  - /dbms/reference/sdk-api/go/
---


## neo-clientの概要

`neo-client`はMachbase Neo用のGoクライアントモジュールです。v2から標準の`database/sql`
ドライバーを中心に再構成され、旧バージョン（v1）のネイティブ`machgo`パッケージは提供されなくなりました。
v1のコードはv2と互換性がないため、`machgo.Config`や`mdb.Connect()`を使用する既存コードは、
以下を参照して`database/sql`ベースに移行してください。

`neo-client`は次のパッケージを提供します。

- `client`（モジュールルート、インポートパス`github.com/machbase/neo-client/v2`）:
  標準`database/sql`ドライバー、`Appender`、構造体スキャン・名前付きパラメーターヘルパー
- `api`: Machbase専用のデータ型とオプション定義
- `machnet`: `client`が内部で使用する低レベルのプロトコル・転送実装。アプリケーションコードで
  直接インポートする必要はほとんどありません。

### 前提条件

- **Machbaseサーバー**: ネイティブポート（デフォルト`5656`）にアクセス可能な稼働中のDBMSまたはNeoサーバー
- **Go 1.22以降**
- **アカウント情報**: 有効なMachbaseユーザーアカウント（ローカル開発環境では`sys` / `manager`など）

## はじめに

### インストール

```sh
go get github.com/machbase/neo-client/v2
```

### インポート

ドライバーパッケージはブランク識別子でインポートします。ドライバー名`machbase`で自動登録されるため、
別途`sql.Register()`を呼び出す必要はありません。

```go
import (
    "context"
    "database/sql"
    "fmt"

    _ "github.com/machbase/neo-client/v2"
)
```

## 接続

### DSN形式

`neo-client`は次のDSN形式をサポートします。

- サーバー値のみ: `host`または`host:port`
- URL形式: `tcp://user:password@host:port/database?as=proxy&fetch_rows=100`
- セミコロンで区切った`key=value`リスト: `key=value;key=value;...`
  （例: `user=sys;password=manager;server=127.0.0.1:5656`）

`key=value`形式は次の規則に従います。

- 値は`"..."`または`'...'`で引用できます。
- 引用された値内の`;`はリテラル文字として扱います。
- 引用された値内ではバックスラッシュエスケープを使用できます。二重引用符の値では`\"`、
  単一引用符の値では`\'`、および`\\`を使用できます。
- 引用符が閉じていない、または対応しない場合は解析エラーになります。

例:

```text
user="sys as demo";password="12;34";server=127.0.0.1:5656;
password="a\"b";server=127.0.0.1:5656;
```

サポートするDSNキーは次のとおりです。

| キー | 説明 |
|----|------|
| `server` | `tcp://user:password@127.0.0.1:5656`形式のサーバーURL |
| `host`, `port` | サーバーホストとポートを個別指定（デフォルトポート: `5656`） |
| `user`, `uid` | ログインユーザー |
| `password`, `pwd` | ログインパスワード |
| `database`, `db` | 初期データベース |
| `auth_mode` | 認証方式: `password`または`challenge` |
| `auth_key_file`, `auth_key_pem` | `auth_mode=challenge`の秘密鍵ファイルパスまたはインラインPEM |
| `auth_sig_scheme` | チャレンジ認証の署名方式 |
| `fetch_rows`, `fetchrows` | 1回のフェッチで取得する最大行数（デフォルト`1000`） |
| `statement_cache`, `statementcache` | 文キャッシュモード: `auto`、`on`、`off`（デフォルト`auto`） |
| `io_metrics`, `iometrics` | I/Oメトリクスの有効化: `true`、`false` |
| `alternative_servers` | `127.0.0.2:5656,backup.example.com:5657`のようなカンマ区切りの代替サーバー一覧 |

`auth_key_file`または`auth_key_pem`を指定し、`auth_mode`を省略するとチャレンジ認証になります。
URLクエリパラメーターも同じオプション名を使用します。

```text
tcp://sys:manager@127.0.0.1:5656/DATABASE_A?statement_cache=on&io_metrics=true
```

不明なキーは`key=value`のDSNではエラーですが、URLクエリ文字列では無視されます。
URLパスは初期データベースも指定します（`tcp://sys:manager@127.0.0.1:5656/DATABASE_A`）。
物理接続ごとに指定データベースが選択され、アプリケーションが直接`USE`を実行した場合は、
その接続がプールで再利用される前に指定データベースへ復元されます。

## 検索例

次の例は標準の`database/sql`パッケージでシステムテーブル`M$SYS_TABLES`を検索します。

```go
package main

import (
	"context"
	"database/sql"
	"fmt"

	_ "github.com/machbase/neo-client/v2"
)

func main() {
	db, err := sql.Open("machbase", "server=tcp://sys:manager@127.0.0.1:5656")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()
	rows, err := db.QueryContext(ctx, `SELECT NAME, ID, TYPE FROM M$SYS_TABLES ORDER BY NAME`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	for rows.Next() {
		var (
			name string
			id   int64
			typ  int
		)
		if err := rows.Scan(&name, &id, &typ); err != nil {
			panic(err)
		}
		fmt.Println(name, id, typ)
	}

	if err := rows.Err(); err != nil {
		panic(err)
	}
}
```

## テーブルの作成と入力

次の例は`database/sql`でTagテーブルを作成し、`ExecContext`で行を入力します。

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name VARCHAR(100) PRIMARY KEY,
	time DATETIME BASE TIME,
    value DOUBLE
);
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	_ "github.com/machbase/neo-client/v2"
)

func main() {
	dsn := "server=tcp://sys:manager@127.0.0.1:5656"

	db, err := sql.Open("machbase", dsn)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()

	_, err = db.ExecContext(ctx, `CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
		NAME   VARCHAR(100)  PRIMARY KEY,
		TIME   DATETIME      BASE TIME,
		VALUE  DOUBLE
	)`)
	if err != nil {
		panic(err)
	}

	ts := time.Now()
	for i := 0; i < 10; i++ {
		rec := []any{
			"example-client",
			ts.Add(time.Duration(i) * time.Second),
			3.14 * float64(i),
		}
		result, err := db.ExecContext(ctx, `INSERT INTO EXAMPLE VALUES (?, ?, ?)`, rec...)
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

ROWID対応のStandard Editionで単一の`INSERT ... VALUES`が成功すると、`Result.LastInsertId()`で
入力行のROWIDを確認できます。戻り値の型は`int64`のため、ROWIDの64ビット値を保持するには`uint64`に
変換します。バッチ、Appender、`INSERT ... SELECT`、UPSERTはROWIDを返しません。詳細な条件は
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

## トランザクション

Machbaseは`CREATE TABLE`で作成した通常のテーブル（TRANSACTIONテーブル）で
`BEGIN`/`COMMIT`/`ROLLBACK`をサポートします。TAG/LOGテーブルはトランザクションをサポートせず、
トランザクション内でTAG/LOGテーブルにDMLを実行すると`MACHCLI-ERR-2362`になります。

標準の`database/sql`トランザクションAPIをそのまま使用できます。

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
	panic(err)
}
if _, err := tx.ExecContext(ctx, `INSERT INTO EXAMPLE_TX VALUES (?, ?, ?)`, name, ts, value); err != nil {
	tx.Rollback()
	panic(err)
}
if err := tx.Commit(); err != nil {
	panic(err)
}
```

繰り返す準備コードを減らすには`client.Tx`/`client.TxConn`のクロージャーヘルパーを使用します。
関数が`nil`を返すとコミットし、エラーを返すとロールバックしてそのエラーをそのまま返します。
panicが発生するとロールバック後に再度panicします。

```go
import client "github.com/machbase/neo-client/v2"

err := client.Tx(ctx, db, func(tx *sql.Tx) error {
	if _, err := tx.ExecContext(ctx, `INSERT INTO EXAMPLE_TX VALUES (?, ?, ?)`, name, ts, value); err != nil {
		return err // 自動ROLLBACK
	}
	return nil // 自動COMMIT
})

// TxConnはdb.Conn(ctx)で取得した特定の接続でトランザクションを実行します。
conn, _ := db.Conn(ctx)
defer conn.Close()
err = client.TxConn(ctx, conn, func(tx *sql.Tx) error {
	// ...
	return nil
})
```

クロージャーのエラーはそのまま返されるため、`errors.Is`/`errors.As`を引き続き使用できます。
強制ロールバックにはセンチネルエラーを返す方法が一般的です。Machbaseはトランザクションオプション
（分離レベル、読み取り専用）をサポートしないため、ドライバーが拒否します。

## 高性能な大量入力（`Appender`）

大量の時系列入力には、行単位の`INSERT`の代わりに`client.Appender`を使用します。
Appenderはクライアントでレコードをバッファリングし、専用チャネルでサーバーにストリーミングするため、
個別のINSERT文より大幅に高速です。

```go
import client "github.com/machbase/neo-client/v2"

appender := &client.Appender{}
// 一部の列のみ指定: 以下のAppend()はこの3値だけを送信し、残りの列はNULLになります。
if err := appender.Connect(ctx, dsn, "EXAMPLE", "NAME", "TIME", "VALUE"); err != nil {
	panic(err)
}
defer func() {
	successCount, failCount, err := appender.Close() // 残りのバッファをフラッシュ
	if err != nil {
		panic(err)
	}
	fmt.Println("Append finished. Success:", successCount, "Fail:", failCount)
}()

for _, rec := range records {
	// Connectに渡した列と同じ順序で値を1つずつ渡します。
	if err := appender.Append(rec.Name, rec.Time, rec.Value); err != nil {
		panic(err)
	}
}
```

主なポイント:

- **列選択**: `Connect`（または`WithInputColumns`）に渡す列リストが、各`Append`呼び出しで
  順番に提供する列を正確に決めます。リストにない列はNULLとして入力されます。
- **列リストを省略**すると（例: `appender.Connect(ctx, dsn, "EXAMPLE")`）、Appenderはテーブルの
  **全列**を対象とし、各`Append`は`nil`を含めて全列の値を提供する必要があります。
  そうしないと値の数のエラーになります。
- `Append`は行をバッファリングします。即時送信は`Flush()`を呼び出します。`Close()`はフラッシュとともに
  セッション単位の成功・失敗件数を返します。
- バッファリングは`WithBatchMaxRows`、`WithBatchMaxBytes`、`WithBatchMaxDelay`で調整できます。
  - `WithBatchMaxRows(rows)`: デフォルト`512`、最小`1`
  - `WithBatchMaxBytes(bytes)`: デフォルト`512KB`、最小`4KB`
  - `WithBatchMaxDelay(duration)`: デフォルト`5ms`、最小`1ms`。`0`は時間ベースの閾値を使用しません。
- AppenderはTAG、LOG、TRANSACTIONテーブルで動作しますが、SQLを迂回するため、Appendはいずれの
  トランザクションにも含まれません。

```go
appender := &client.Appender{}
if err := appender.Connect(ctx, dsn, "EXAMPLE", "NAME", "TIME", "VALUE"); err != nil {
	panic(err)
}
defer appender.Close()

appender.
	WithBatchMaxBytes(1024 * 1024).           // 1 MBの閾値
	WithBatchMaxRows(2000).                   // 行数の閾値
	WithBatchMaxDelay(500 * time.Millisecond) // 最大遅延の閾値
```

{{< callout type="warning" >}}
有効なAppenderを使用する接続で通常のクエリを併用しないでください。
Appendのワークロードには別接続を使用してください。
{{< /callout >}}

### ARRAYと選択列Append

通常の`appender.Connect(ctx, dsn, table)`で列引数を省略し、ARRAY列の値に`api.NewSparseArray()`で
作成したオブジェクトを渡せます。固定要素の選択とは異なります。

```go
if err := appender.Connect(ctx, dsn, "ARRAY_APPEND_FULL_EXAMPLE"); err != nil {
    return err
}
```

`ID LONG, A INT32[4]`テーブルの入力順序、スパース値の構成、エラー時のClose、検索確認は
[通常Connectの例](../data-input-load-export/array-append/#go-full-open)を参照してください。

```go
func appendSelected(ctx context.Context, dsn string) error {
    appender := &client.Appender{}
    if err := appender.Connect(
        ctx,
        dsn,
        "ARRAY_APPEND_EXAMPLE",
        "ID",
        "A[0]",
        "A[3]",
    ); err != nil {
        return err
    }
    if err := appender.Append(int64(1), int32(10), int32(40)); err != nil {
        _, _, _ = appender.Close()
        return err
    }
    success, failed, err := appender.Close()
    if err != nil {
        return err
    }
    if failed != 0 {
        return fmt.Errorf(
            "append result: success=%d failed=%d",
            success,
            failed,
        )
    }
    return nil
}
```

上記は`context`、`fmt`、`client "github.com/machbase/neo-client/v2"`のインポートを前提とします。

行ごとに異なる位置を入力する場合は`api.NewSparseArray()`を使用します。`Array.Set()`、`Get()`、
`Entries()`、および要素位置を指定したAppend対象の位置は0始まりです。
APIとバージョン制限は
[Sparse ARRAYと選択列Append API](../data-input-load-export/array-append/)を参照してください。

## 結果を構造体にスキャン

列順に全対象を列挙する代わりに、`db`タグで列を構造体フィールドにマッピングできます。
ヘルパーは取得済みの`*sql.Rows`をそのまま受け取るため、標準`database/sql` APIと併用できます。

```go
import client "github.com/machbase/neo-client/v2"

type TagRecord struct {
	Name  string    `db:"NAME"`
	Time  time.Time `db:"TIME"`
	Value float64   `db:"VALUE"`

	cached string // 非公開またはタグなしのフィールドは無視
}

records, err := client.Select[TagRecord](ctx, db,
	`SELECT NAME, TIME, VALUE FROM EXAMPLE WHERE NAME = ? ORDER BY TIME LIMIT 100`, "sensor-1")
```

提供するヘルパー:

| 関数 | 用途 |
| --- | --- |
| `Select[T](ctx, q, query, args...)` | クエリを実行し、全行を`[]T`にスキャン |
| `Get[T](ctx, q, query, args...)` | クエリを実行し、最初の行をスキャン。結果がなければ`sql.ErrNoRows` |
| `ScanAll[T](rows)` / `ScanOne[T](rows)` | 呼び出し側がすでに開いたrowsに同じ操作を実行 |
| `ScanEach[T](rows, fn)` | メモリ使用量を一定に保ちながら1行ずつストリーミング |
| `NewCursor[T](rows)` | 明示的な`Next`/`Value`/`Err`イテレーター |
| `ScanStruct(rows, &dest)` | `rows.Next()`を呼ばずに現在の行をスキャン |
| `ScanRow(rows, &dest)` / `ScanRows(rows, &slice)` | ジェネリクスを使用しない形式 |

`T`は構造体、構造体ポインター、単一列クエリのスカラー、`map[string]any`のいずれかです。

マッピング規則:

- タグキーは`db`で、既存DTOをそのまま使用できるように`json`タグを代替として使用します。
- 列名は大文字・小文字を区別せずに一致するため、`db:"id"`は`ID`列と一致します。
- `db:"-"`はフィールドを除外し、**タグなしフィールドも除外**されます。タグなしフィールドを名前で
  マッピングするには`WithNameMapper(client.NameMapperIdentity())`を呼び出してください。
- 埋め込み構造体は平坦化され、名前のあるネスト構造体は`parent.child`で指定します。
- NULL列は`nil`になる`*T`フィールド、または`sql.Null[T]`で受け取れます。

デフォルトのマッピングは厳密です。一致するフィールドがない列と、一致する列がないフィールドは
どちらもエラーとなり、変更された`SELECT *`が値を黙って欠落させることを防ぎます。
呼び出しごとに`WithLaxColumns()`または`WithLaxFields()`で緩和できます。

DATETIME列を`string`、`int64`、`time.Time`フィールドにスキャンする際は、machbase-neo HTTP APIの
`timeformat`/`tz`クエリパラメーターと名前を合わせた追加の`db`タグオプションを使用できます。

```go
type Row struct {
	Time  string    `db:"TIME,timeformat=2006-01-02 15:04:05,tz=Local"` // カスタムレイアウト + 表示タイムゾーン
	Epoch int64     `db:"TIME,timeformat=ms"`                           // ミリ秒単位のエポック
	At    time.Time `db:"TIME,tz=UTC"`                                  // フィールド別にタイムゾーンを上書き
}
```

- `timeformat=<Go time layout>`: `string`/`*string`フィールドのGo時刻レイアウト
  （またはエポックを数値文字列で表す`ns`/`us`/`ms`/`s`）
- `timeformat=ns|us|ms|s`: `int64`/`*int64`フィールドのエポック単位
- `tz=<IANA name>|Local|UTC`: `string`/`time.Time`フィールド（およびポインター形式）のタイムゾーン

このオプションはタグがなくても適用されます。DATETIME列に一致する`string`、`int64`、`time.Time`の
フィールドは、デフォルトとして`WithDateTime(timeformat, tz)`を使用します。`WithDateTime`も未設定なら
`timeformat="2006-01-02 15:04:05.999"`と`tz="Local"`を使用します。
フィールド自体のタグは常に`WithDateTime`より優先されます。

`Select`、`ScanAll`、`ScanRows`は結果全体をメモリに読み込むため、`WithMaxRows`（デフォルト1000）を
超えると`ErrScanTooManyRows`で中断します。`WithMaxRows(n)`で上限を増やすか、`WithMaxRows(0)`で
制限を解除できます。制限のない`ScanEach`や`NewCursor`でストリーミングすることもできます。

```go
rows, err := db.QueryContext(ctx, `SELECT NAME, TIME, VALUE FROM EXAMPLE`)
if err != nil {
	panic(err)
}
defer rows.Close() // ヘルパーは受け取ったrowsを閉じない

var total float64
err = client.ScanEach(rows, func(rec TagRecord) error {
	total += rec.Value
	return nil
})
```

## 名前付きパラメーター

`NamedArgs`は構造体または`map[string]any`を、同じ`db`タグで`sql.Named`引数に変換します。
SQLテキストを検査・書き換えず、`:name`プレースホルダーはサーバーが直接解釈します。

```go
type condition struct {
	Name string    `db:"name"`
	From time.Time `db:"from"`
	To   time.Time `db:"to"`
}

args, err := client.NamedArgs(condition{Name: "sensor-1", From: begin, To: end})
if err != nil {
	panic(err)
}

records, err := client.Select[TagRecord](ctx, db, `
	SELECT NAME, TIME, VALUE FROM EXAMPLE
	 WHERE NAME = :name AND TIME BETWEEN :from AND :to`, args...)
```

名前付きパラメーターには、パラメーター名メタデータを報告するサーバー（Machbase v8.7.0以降）が
必要です。`client.SupportsNamedParameters(ctx, db)`で確認します。非サポートの場合、クエリは
`client.ErrNamedParamsUnsupported`で失敗するため、位置指定プレースホルダー`?`を使用する必要があります。
一般的なSQL機能とSDK別の違いは
[Named Bind Parameter syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。


## Machbase 8.7: DECIMALと名前付きパラメーター

Machbase 8.7は正確なDECIMAL値、NULL許容列情報、名前付きパラメーターを提供します。

```go
import "database/sql"
import client "github.com/machbase/neo-client/v2"

amount, err := client.ParseDecimal("1234567890.125", 30, 3)
if err != nil {
	panic(err)
}
result, err := conn.ExecContext(ctx,
	"INSERT INTO payments(id, amount) VALUES (:id, :amount)",
	sql.Named("id", int32(1)),
	sql.Named("amount", amount),
)
if err != nil {
	panic(err)
}
```

`database/sql`ドライバーは`sql.Named`を受け取り、DECIMALの検索値を正確な文字列で返します。
パラメーター名は大文字・小文字を区別せずに一致し、繰り返すプレースホルダーには1回渡した値を適用します。
名前付き引数と位置指定引数は混用できません。`client.NamedArgs`は構造体またはmapから
`sql.Named`リストを作成します。

Machbase 8.5.xに接続する場合は、そのサーバーバージョンがサポートするテーブル・データ型と、
位置指定パラメーター`?`を使用してください。名前付きパラメーターとMachbase 8.7のデータ型は使用できず、
NULL許容列情報が不明な場合（`ColumnType.Nullable()`が`ok=false`を返す場合）があります。

### プリペアドステートメントと文キャッシュ

`db.PrepareContext`で作成した文は複数回実行できます。ドライバーの文キャッシュは接続単位で動作し、
DSNキー`statement_cache=auto|on|off`で設定します。テーブルを削除して再作成した場合や結果列の型が
変わった場合は、キャッシュしたメタデータを更新するため文を再準備します。`USE`でセッションの
データベースを変えた後も、既存の準備済み文やカーソルを別データベースの操作に再利用せず、
新しく準備またはオープンする必要があります。

## 付属サンプルの実行

実行可能なサンプルはneo-clientリポジトリの`_example/`に含まれています。

```sh
go run ./_example/query.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/append.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/insert.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/scanbytag.go -s 127.0.0.1:5656 -u sys -p manager
```

## 補足と制限事項

- 位置指定と名前付きプレースホルダーの両方を使用できますが、1つの文で混用できません。
  名前付きAPIは`sql.Named()`を使用します。共通SQL機能とSDK別の違いは
  [Named Bind Parameter syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。
- `database/sql`の接続プールは通常の`sql.DB`の方式で動作します。DSNに`database`/`db`を指定すると、
  物理接続ごとに指定データベースを選択します。アプリケーションが直接`USE`を実行したセッションは、
  プールへの返却前に設定済みデータベースへ復元されます。
- ROWID対応のStandard Editionでは、単一INSERT結果で`Result.LastInsertId()`を呼び出せます。
  返された`int64`を`uint64`に変換してROWIDのビットパターンを保持します。詳細は
  [ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。
- 使用後の`Rows`、`Stmt`、`sql.Conn`、`sql.DB`は必ず閉じてください。
  構造体スキャンヘルパーは受け取ったrowsを閉じません。
- `Appender.Close()`はAppendセッションの成功・失敗件数を返します。
- パラメーター型はドライバー実装に従います。一般的なSQL型、`time.Time`、`[]byte`、`net.IP`、
  `api.Decimal`をサポートしますが、`bool`パラメーターはサポートしません。
