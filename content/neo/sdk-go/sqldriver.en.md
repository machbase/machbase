---
title: SQL driver
type: docs
weight: 300
---

## Overview
The `machrpc` package, built on gRPC, provides compatibility with Go's `database/sql` package.

For setup instructions, see the **gRPC client** section for details on installation, TLS configuration, and certificate generation.

## Usage

```go
package main

import (
	"database/sql"
	"fmt"
	"time"

	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	// Configure server address and TLS certificates
	serverAddr := "127.0.0.1:5655"
	serverCert := "/path/to/server-cert.pem"
	clientKey := "/path/to/client-key.pem"
	clientCert := "/path/to/client-cert.pem"
	
    // register machbase-neo data source
	sql.Register("neo", &machrpc.Driver{})

	db, err := sql.Open("neo",
	fmt.Sprintf("server=%s; user=sys; password=manager; server-cert=%s; client-key=%s; client-cert=%s",
		serverAddr, serverCert, clientKey, clientCert))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	// INSERT with Exec
	tag := "tag01"
	var result sql.Result
	result, err = db.Exec("INSERT INTO EXAMPLE(name, time, value) VALUES(?, ?, ?)", tag, time.Now(), 1.234)
	if err != nil {
		panic(err)
	}
	fmt.Println("INSERT: ", result)

	// QueryRow
	row := db.QueryRow("SELECT count(*) FROM EXAMPLE WHERE name = ?", tag)
	if row.Err() != nil {
		panic(row.Err())
	}
	var count int
	if err = row.Scan(&count); err != nil {
		panic(err)
	}
	fmt.Println("count:", count)

	// Query
	rows, err := db.Query("SELECT name, time, value FROM EXAMPLE WHERE name = ? ORDER BY TIME DESC", tag)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	for rows.Next() {
		var name string
		var ts time.Time
		var value float64
		rows.Scan(&name, &ts, &value)
		fmt.Println("name:", name, "time:", ts.Local().String(), "value:", value)
	}
}
```
