---
type: docs
title: '11.9 Go'
weight: 90
toc: true
aliases:
  - /dbms/reference/sdk-api/go/
---


## neo-client Overview

`neo-client` is the Go client module for Machbase Neo. Version 2 centers on the standard
`database/sql` driver and no longer provides the native `machgo` package from v1. Code
written for v1 is incompatible with v2. Migrate existing `machgo.Config` or `mdb.Connect()`
code to `database/sql` as described below.

`neo-client` provides these packages:

- `client` (module root, import `github.com/machbase/neo-client/v2`): Standard
  `database/sql` driver, `Appender`, struct scanning, and named parameter helpers
- `api`: Machbase-specific data types and options
- `machnet`: Low-level protocol/transport implementation used internally by `client`;
  application code rarely needs to import it directly

### Prerequisites

- **Machbase server:** A running DBMS or Neo server reachable on its native port
  (default `5656`)
- **Go 1.22 or later**
- **Credentials:** A valid Machbase account (for example, `sys` / `manager` for local development)

## Getting Started

### Installation

```sh
go get github.com/machbase/neo-client/v2
```

### Import

Import the driver package with the blank identifier. It registers automatically as
`machbase`; no explicit `sql.Register()` call is needed.

```go
import (
    "context"
    "database/sql"
    "fmt"

    _ "github.com/machbase/neo-client/v2"
)
```

## Connections

### DSN Formats

`neo-client` supports these DSN formats:

- Server only: `host` or `host:port`
- URL: `tcp://user:password@host:port/database?as=proxy&fetch_rows=100`
- Semicolon-separated `key=value` pairs: `key=value;key=value;...`
  (for example, `user=sys;password=manager;server=127.0.0.1:5656`)

Rules for `key=value` DSNs:

- Values may be quoted with `"..."` or `'...'`.
- Semicolons inside quoted values are literal characters.
- Quoted values support backslash escapes: `\"` in double-quoted values,
  `\'` in single-quoted values, and `\\`.
- Unclosed or mismatched quotes cause a parse error.

Example:

```text
user="sys as demo";password="12;34";server=127.0.0.1:5656;
password="a\"b";server=127.0.0.1:5656;
```

Supported DSN keys:

| Key | Description |
|----|------|
| `server` | Server URL such as `tcp://user:password@127.0.0.1:5656` |
| `host`, `port` | Separate server host and port (default port: `5656`) |
| `user`, `uid` | Login user |
| `password`, `pwd` | Login password |
| `database`, `db` | Initial database |
| `auth_mode` | Authentication mode: `password` or `challenge` |
| `auth_key_file`, `auth_key_pem` | Private key file path or inline PEM for `auth_mode=challenge` |
| `auth_sig_scheme` | Challenge authentication signature scheme |
| `fetch_rows`, `fetchrows` | Maximum rows per fetch (default `1000`) |
| `statement_cache`, `statementcache` | Statement cache mode: `auto`, `on`, `off` (default `auto`) |
| `io_metrics`, `iometrics` | Enable I/O metrics: `true`, `false` |
| `alternative_servers` | Comma-separated alternatives such as `127.0.0.2:5656,backup.example.com:5657` |

If `auth_key_file` or `auth_key_pem` is set without `auth_mode`, challenge authentication
is selected. URL query parameters use the same option names.

```text
tcp://sys:manager@127.0.0.1:5656/DATABASE_A?statement_cache=on&io_metrics=true
```

Unknown keys cause errors in `key=value` DSNs but are ignored in URL query strings. The
URL path also selects the initial database
(`tcp://sys:manager@127.0.0.1:5656/DATABASE_A`). Every physical connection selects the
configured database. If application code executes `USE`, the connection is restored
to that database before pool reuse.

## Query Example

This example queries the `M$SYS_TABLES` system table through standard `database/sql`.

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

## Create a Table and Insert Data

This example creates a TAG table through `database/sql` and inserts rows with `ExecContext`.

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

After a successful single `INSERT ... VALUES` on Standard Edition with ROWID support,
`Result.LastInsertId()` returns the inserted row's ROWID. Its type is `int64`; convert
to `uint64` to preserve the ROWID's 64-bit value. Batches, Appender, `INSERT ... SELECT`,
and UPSERT do not return ROWIDs. See [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/)
for detailed conditions.

## Transactions

Machbase supports `BEGIN`/`COMMIT`/`ROLLBACK` on ordinary tables (TRANSACTION tables)
created with `CREATE TABLE`. TAG/LOG tables do not support transactions; DML on TAG/LOG
tables inside a transaction raises `MACHCLI-ERR-2362`.

Use the standard `database/sql` transaction API:

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

Use the `client.Tx`/`client.TxConn` closure helpers to reduce setup code. A `nil` return
commits. An error rolls back and is returned unchanged. A panic rolls back and then
panics again.

```go
import client "github.com/machbase/neo-client/v2"

err := client.Tx(ctx, db, func(tx *sql.Tx) error {
	if _, err := tx.ExecContext(ctx, `INSERT INTO EXAMPLE_TX VALUES (?, ?, ?)`, name, ts, value); err != nil {
		return err // Automatic ROLLBACK
	}
	return nil // Automatic COMMIT
})

// TxConn runs a transaction on a specific connection obtained with db.Conn(ctx).
conn, _ := db.Conn(ctx)
defer conn.Close()
err = client.TxConn(ctx, conn, func(tx *sql.Tx) error {
	// ...
	return nil
})
```

Errors returned by the closure remain unchanged, so `errors.Is`/`errors.As` still work.
Returning a sentinel error is the idiomatic way to force rollback. Machbase does not
support transaction options (isolation level or read-only), so the driver rejects them.

## High-Performance Bulk Ingestion (`Appender`)

Use `client.Appender` for bulk time-series ingestion instead of individual `INSERT`
statements. The appender buffers records on the client and streams them through a
dedicated channel, making it much faster than individual INSERTs.

```go
import client "github.com/machbase/neo-client/v2"

appender := &client.Appender{}
// Select columns: Append() sends these three values; remaining columns receive NULL.
if err := appender.Connect(ctx, dsn, "EXAMPLE", "NAME", "TIME", "VALUE"); err != nil {
	panic(err)
}
defer func() {
	successCount, failCount, err := appender.Close() // Flush remaining buffers
	if err != nil {
		panic(err)
	}
	fmt.Println("Append finished. Success:", successCount, "Fail:", failCount)
}()

for _, rec := range records {
	// Pass individual values in the column order supplied to Connect.
	if err := appender.Append(rec.Name, rec.Time, rec.Value); err != nil {
		panic(err)
	}
}
```

Key points:

- **Column selection:** The columns passed to `Connect` (or `WithInputColumns`) define
  exactly which values each `Append` must supply and in what order. Unlisted columns
  receive NULL.
- **Omitting the column list** (for example, `appender.Connect(ctx, dsn, "EXAMPLE")`)
  targets **all** table columns. Each `Append` must supply every value, including
  `nil`; otherwise, a value-count error occurs.
- `Append` buffers rows. Call `Flush()` to send immediately. `Close()` flushes and
  returns session success/failure counts.
- Configure buffering with `WithBatchMaxRows`, `WithBatchMaxBytes`, and `WithBatchMaxDelay`.
  - `WithBatchMaxRows(rows)`: Default `512`, minimum `1`
  - `WithBatchMaxBytes(bytes)`: Default `512KB`, minimum `4KB`
  - `WithBatchMaxDelay(duration)`: Default `5ms`, minimum `1ms`; `0` disables the time threshold
- The appender works with TAG, LOG, and TRANSACTION tables, but bypasses SQL, so append
  is never part of a transaction.

```go
appender := &client.Appender{}
if err := appender.Connect(ctx, dsn, "EXAMPLE", "NAME", "TIME", "VALUE"); err != nil {
	panic(err)
}
defer appender.Close()

appender.
	WithBatchMaxBytes(1024 * 1024).           // 1 MB threshold
	WithBatchMaxRows(2000).                   // Row-count threshold
	WithBatchMaxDelay(500 * time.Millisecond) // Maximum delay threshold
```

{{< callout type="warning" >}}
Do not run ordinary queries on a connection with an active appender.
Use a separate connection for append workloads.
{{< /callout >}}

### ARRAY and Selected-Column Append

Omit column arguments from standard `appender.Connect(ctx, dsn, table)` and pass an
object created by `api.NewSparseArray()` as the ARRAY column value. This differs from
selecting fixed elements.

```go
if err := appender.Connect(ctx, dsn, "ARRAY_APPEND_FULL_EXAMPLE"); err != nil {
    return err
}
```

See the [standard Connect example](../data-input-load-export/array-append/#go-full-open)
for the input order of `ID LONG, A INT32[4]`, sparse values, Close on errors, and query checks.

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

This example assumes imports of `context`, `fmt`, and
`client "github.com/machbase/neo-client/v2"`.

Use `api.NewSparseArray()` when positions vary by row. `Array.Set()`, `Get()`,
`Entries()`, and element-position Append targets use 0-based positions. See
[Sparse ARRAY and Selected-Column Append API](../data-input-load-export/array-append/)
for APIs and version restrictions.

## Scan Results into Structs

Map columns to struct fields with `db` tags instead of listing destinations in column
order. Helpers accept an existing `*sql.Rows`, so they work with standard `database/sql` APIs.

```go
import client "github.com/machbase/neo-client/v2"

type TagRecord struct {
	Name  string    `db:"NAME"`
	Time  time.Time `db:"TIME"`
	Value float64   `db:"VALUE"`

	cached string // Unexported or untagged fields are ignored
}

records, err := client.Select[TagRecord](ctx, db,
	`SELECT NAME, TIME, VALUE FROM EXAMPLE WHERE NAME = ? ORDER BY TIME LIMIT 100`, "sensor-1")
```

Available helpers:

| Function | Purpose |
| --- | --- |
| `Select[T](ctx, q, query, args...)` | Executes a query and scans all rows into `[]T` |
| `Get[T](ctx, q, query, args...)` | Executes a query and scans the first row; returns `sql.ErrNoRows` if empty |
| `ScanAll[T](rows)` / `ScanOne[T](rows)` | Equivalent operations on rows opened by the caller |
| `ScanEach[T](rows, fn)` | Streams one row at a time with constant memory |
| `NewCursor[T](rows)` | Explicit `Next`/`Value`/`Err` iterator |
| `ScanStruct(rows, &dest)` | Scans the current row without calling `rows.Next()` |
| `ScanRow(rows, &dest)` / `ScanRows(rows, &slice)` | Non-generic variants |

`T` can be a struct, pointer to a struct, scalar for a single-column query, or `map[string]any`.

Mapping rules:

- The tag key is `db`, with `json` as a fallback for existing DTOs.
- Column names match case-insensitively; `db:"id"` matches `ID`.
- `db:"-"` excludes a field; **untagged fields are also excluded**. To map untagged fields
  by name, call `WithNameMapper(client.NameMapperIdentity())`.
- Embedded structs are flattened; named nested structs use `parent.child`.
- NULL columns can be scanned into `*T` fields that become `nil`, or into `sql.Null[T]`.

Mapping is strict by default: columns without matching fields and fields without
matching columns are errors. This prevents changed `SELECT *` results from silently
omitting values. Relax each call with `WithLaxColumns()` or `WithLaxFields()`.

When scanning DATETIME into `string`, `int64`, or `time.Time` fields, additional `db`
tag options use the same names as the machbase-neo HTTP API `timeformat`/`tz` query parameters.

```go
type Row struct {
	Time  string    `db:"TIME,timeformat=2006-01-02 15:04:05,tz=Local"` // Custom layout and display time zone
	Epoch int64     `db:"TIME,timeformat=ms"`                           // Epoch milliseconds
	At    time.Time `db:"TIME,tz=UTC"`                                  // Per-field time zone override
}
```

- `timeformat=<Go time layout>`: Go time layout for `string`/`*string` fields (or
  `ns`/`us`/`ms`/`s` for an epoch represented as a numeric string)
- `timeformat=ns|us|ms|s`: Epoch unit for `int64`/`*int64` fields
- `tz=<IANA name>|Local|UTC`: Time zone for `string`/`time.Time` fields and their pointer variants

These options also apply without tags. Fields of type `string`, `int64`, or `time.Time`
matching DATETIME columns use `WithDateTime(timeformat, tz)` as the default. Without
`WithDateTime`, defaults are `timeformat="2006-01-02 15:04:05.999"` and `tz="Local"`.
Field tags always override `WithDateTime`.

`Select`, `ScanAll`, and `ScanRows` load all results into memory and stop with
`ErrScanTooManyRows` if `WithMaxRows` (default 1000) is exceeded. Raise it with
`WithMaxRows(n)` or remove it with `WithMaxRows(0)`. Alternatively, stream with unlimited
`ScanEach` or `NewCursor`.

```go
rows, err := db.QueryContext(ctx, `SELECT NAME, TIME, VALUE FROM EXAMPLE`)
if err != nil {
	panic(err)
}
defer rows.Close() // Helpers do not close supplied rows

var total float64
err = client.ScanEach(rows, func(rec TagRecord) error {
	total += rec.Value
	return nil
})
```

## Named Parameters

`NamedArgs` converts a struct or `map[string]any` into `sql.Named` arguments using the
same `db` tags. It does not inspect or rewrite SQL text; the server parses `:name` placeholders.

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

Named parameters require a server that reports parameter-name metadata (Machbase
v8.7.0 or later). Check `client.SupportsNamedParameters(ctx, db)`. Unsupported queries
fail with `client.ErrNamedParamsUnsupported`; use positional `?` placeholders instead.
See [Named Bind Parameter Syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)
for shared SQL behavior and SDK differences.


## Machbase 8.7: DECIMAL and Named Parameters

Machbase 8.7 provides exact DECIMAL values, column nullability metadata, and named parameters.

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

The `database/sql` driver accepts `sql.Named` and returns DECIMAL values as exact
strings. Parameter names match case-insensitively; one supplied value binds all repeated
occurrences. Do not mix named and positional arguments. `client.NamedArgs` creates
`sql.Named` lists from structs or maps.

When connecting to Machbase 8.5.x, use positional `?` parameters with table and data
types supported by that server. Named parameters and Machbase 8.7 data types are
unavailable. Column nullability may be unknown (`ColumnType.Nullable()` returns `ok=false`).

### Prepared Statements and Statement Cache

Statements created with `db.PrepareContext` can run repeatedly. The driver caches
statements per connection, configured by DSN `statement_cache=auto|on|off`. Reprepare
after dropping and recreating a table or changing result column types to refresh
cached metadata. After changing the session database with `USE`, prepare new statements
or open new cursors for the other database instead of reusing existing ones.

## Run the Included Examples

Runnable examples are included under `_example/` in the neo-client repository.

```sh
go run ./_example/query.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/append.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/insert.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/scanbytag.go -s 127.0.0.1:5656 -u sys -p manager
```

## Notes and Limitations

- Both positional and named placeholders are supported, but cannot be mixed in one
  statement. Use `sql.Named()` for named input. See
  [Named Bind Parameter Syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)
  for shared SQL behavior and SDK differences.
- Pooling follows ordinary `sql.DB` behavior. With `database`/`db` in the DSN, every
  physical connection selects that database. Sessions changed with explicit `USE`
  are restored to the configured database before returning to the pool.
- On Standard Edition with ROWID support, call `Result.LastInsertId()` after a single
  INSERT. Convert the returned `int64` to `uint64` to preserve its bit pattern. See
  [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/).
- Always close `Rows`, `Stmt`, `sql.Conn`, and `sql.DB` after use. Struct scanning
  helpers do not close caller-supplied rows.
- `Appender.Close()` returns append session success/failure counts.
- Parameter types follow the driver implementation. Common SQL types, `time.Time`,
  `[]byte`, `net.IP`, and `api.Decimal` are supported; `bool` parameters are not.
