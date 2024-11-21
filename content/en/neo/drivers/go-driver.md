---
title: Go Driver
type: docs
weight: 200
---

The driver is provided for Go developers.

## Import

```go
import "github.com/machbase/neo-server/v8/api/machrpc"
import "database/sql"
```

## Register Driver

```go
serverAddr := "tcp://127.0.0.1:5655"
datasourceName := "neo"

sql.Register(datasourceName, &machrpc.Driver{
    ServerAddr: serverAddr,
    User:       "sys",
    Password:   "manager",
})
```

## QueryRow

```go
db, err := sql.Open(datasourceName, "")
if err != nil {
    panic(err)
}
defer db.Close()

row := db.QueryRow("select count(*) from M$SYS_TABLES where name = 'EXAMPLE'")
if row.Err() != nil {
    panic(row.Err())
}

var count int
err = row.Scan(&count)
if err != nil {
    panic(err)
}
```

## Query

```go
rows, err := db.Query("select name, time, value, id from EXAMPLE where time >= ? order by time", ts)
if err != nil {
    panic(err)
}
pass := 0
for rows.Next() {
    var name string
    var ts time.Time
    var value float64
    var id string
    err := rows.Scan(&name, &ts, &value, &id)
    if err != nil {
        panic("ERR> %v", err.Error())
        break
    }
    pass++
    fmt.Printf("==> %v %v %v %v\n", name, ts, value, id)
}
rows.Close()
```