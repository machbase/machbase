---
type: docs
title: '17.7.6 Go'
weight: 60
toc: true
---


## machgo


## Overview

The `machgo` package is a pure Go client for Machbase native protocol access.
It provides the same API style as `machcli`, but without depending on CGo.
If you need native-port performance with a fully Go toolchain, `machgo` is a good choice.

### Why use machgo?

- **No CGo dependency**: Build and deploy with a pure Go environment
- **Native protocol access**: Connect through the Machbase native port (default `5656`)
- **API compatibility with machcli**: Reuse the same connection/query/appender patterns
- **Production-friendly**: Good fit for containerized and cross-platform Go deployments

### Prerequisites

- **Machbase server**: A running DBMS or Neo server instance reachable on the native port
- **Go 1.22+**: Recent Go version recommended
- **Network access**: Reachable native port (`5656` by default)

## Getting Started

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

Import the API package and `machgo` client package:

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### Configuration

Use `machgo.Config` to configure host/port and concurrency options:

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase server host
    Port:         5656,          // Machbase native port
    MaxOpenConn:  0,             // Max Connection threshold
    MaxOpenQuery: 0,             // Max Query concurrency limit
}

// Create a database instance
// API usage is the same as machcli
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### Configuration Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `MaxOpenConn` | Maximum open connections | `< 0`: unlimited<br>`0`: CPU count × factor<br>`> 0`: specified limit |
| `MaxOpenConnFactor` | Multiplier when MaxOpenConn is 0 | Default: 1.5 |
| `MaxOpenQuery` | Maximum concurrent queries | `< 0`: unlimited<br>`0`: CPU count × factor<br>`> 0`: specified limit |
| `MaxOpenQueryFactor` | Multiplier when MaxOpenQuery is 0 | Default: 1.5 |

#### FlowControl behavior

`MaxOpenConn` and `MaxOpenQuery` are flow-control limits.
If you set either value to `-1`, that limit is disabled (no FlowControl on that dimension).

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // disable connection FlowControl
    MaxOpenQuery: -1, // disable query FlowControl
}
```

### Establishing Connection

```go
ctx := context.Background()
conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    panic(err)
}
defer conn.Close()
```

Authentication options:

- `api.WithPassword(user, password)`

### Connection-level tuning options

`machgo` supports per-connection overrides at `Connect()` time.
This lets you keep global defaults in `machgo.Config`, while tuning each connection differently.

#### StatementCache for repeated SQL

For the same SQL used repeatedly during a single connection lifetime,
statement reuse can improve performance by reusing prepared statements.

You can set a default mode in `machgo.Config.StatementCache`, and override per connection with `api.WithStatementCache(...)`.

```go {linenos=table,linenostart=1,hl_lines=[5,16]}
// Connection A: aggressive statement reuse
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// Connection B: disable statement reuse for this connection only
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

#### FetchRows pre-fetch size

`FetchRows` controls the maximum number of records pre-fetched from server in one fetch round.
Set `machgo.Config.FetchRows` as the default, and override per connection via `api.WithFetchRows(...)`.
The default value is `1000`.

{{< callout type="warning" >}}
Avoid setting `FetchRows` to excessively large or small values without workload validation.
Depending on network latency and query characteristics, an improper value can cause significant performance degradation and increased memory consumption.
{{< /callout >}}

```go {linenos=table,linenostart=1,hl_lines=[5]}
// Connection C: larger pre-fetch for scan-heavy workloads
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
Always call `Close()` on connections to release resources.
{{< /callout >}}

## Database Operations

### Single Row Query (`QueryRow`)

Use `QueryRow` when exactly one row is expected.

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

### Multiple Row Query (`Query`)

Use `Query` for multi-row results.

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

### Data Modification (`Exec`)

Use `Exec` for INSERT, DELETE, and DDL statements.

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

## High-Performance Bulk Insert (`Appender`)

For high-throughput ingestion, use `Appender` with a dedicated connection.

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

You can tune the client-side transfer buffer threshold to server with:

The appender accumulates data from `Append()` calls in an internal buffer and sends it to the server only when configured thresholds are reached.
You can configure thresholds by byte size, row count, and delay (the time gap between the oldest buffered record and the newest one).
If any one of these thresholds is exceeded, the buffered data is sent to the server.

- `WithBatchMaxRows(rows)` : default `512`, minimum `1`
- `WithBatchMaxBytes(bytes)`: default `512KB`, minimum `4KB`
- `WithBatchMaxDelay(duration)` : default `5ms`, minimum `1ms`
- `WithBatchMaxDelay(0)` disables the time-based threshold

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MB threshold
    WithBatchMaxRows(2000).            // row-count threshold
    WithBatchMaxDelay(500 * time.Millisecond) // max delay threshold
```

Appender flush example:

`Flush()` is a programmatic flush method.
Unlike threshold-based auto flush behavior, it forces buffered records to be sent immediately regardless of configured byte/row/delay thresholds.

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

{{< callout type="warning" >}}
Do not run regular queries on a connection that currently owns an active appender.
Use a separate connection for append workloads.
{{< /callout >}}

## Complete Example

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

This workflow is intentionally identical to `machcli` so existing code can be migrated with minimal changes.


## Go database/sql Driver


## Overview
The `github.com/machbase/neo-client` package provides a standard Go `database/sql` driver for Machbase.
It is built on top of the native TCP client and uses the native port (default `5656`).

Use this driver when your application or framework already depends on Go's `database/sql` interfaces.
For new code that does not require `database/sql`, `machgo` is usually the better choice.

### Prerequisites

- **Machbase server**: A running DBMS or Neo server instance reachable on the native port
- **Go 1.22+**: Required by `github.com/machbase/neo-client`
- **Credentials**: A valid Machbase user account

## Getting Started

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

Import the driver package with a blank identifier.
The driver registers itself automatically with the name `machbase`.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## Connection

### DSN format

The simplest DSN uses the `server` key:

```text
server=tcp://sys:manager@127.0.0.1:5656
```

You can also combine additional options as semicolon-separated key/value pairs:

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### Supported DSN keys

| Key | Description |
|-----|-------------|
| `server` | Server URL such as `tcp://user:password@127.0.0.1:5656` |
| `host`, `port` | Server host and port provided separately |
| `user` | Login user |
| `password` | Login password |
| `fetch_rows` | Number of rows fetched per round trip |
| `statement_cache` | Statement cache mode: `auto`, `on`, or `off` |
| `io_metrics` | Enable I/O metrics: `true` or `false` |
| `alternative_servers` | Alternate server address such as `127.0.0.2:5656` |
| `alternative_host`, `alternative_port` | Alternate server host and port provided separately |

## Query Example

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

## Insert Example

The following example inserts rows into a tag table named `EXAMPLE`.

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

## Notes and Limitations

- Use positional placeholders like `?`; named parameters are not supported.
- `database/sql` connection pooling works through `sql.DB` as usual.
- Explicit transactions are not supported, so `Begin` and `BeginTx` return an error.
- `LastInsertId()` is not supported.
- Parameter type support follows the driver implementation. Common SQL types, `time.Time`, `[]byte`, and `net.IP` are supported, but `bool` parameters are not.
