---
title: Bridge
type: docs
weight: 70
---

Bridges make machbase-neo enabled to inter-work external systems.
For example, machbase-neo can execute DDL and DML SQL statements via bridges to other dbms system.
And receive messages from an external MQTT broker.

## Register a bridge to sqlite3

Register a bridge that connects to the SQLite.

```
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
```

SQLite supports memory only mode like below.


```
bridge add -t sqlite mem file::memory:?cache=shared
```

## Test the bridge's connecitivity

```
machbase-neo» bridge test mem;
Test bridge mem connectivity... success 11.917µs
```

## Create table

Open machbase-neo shell and execute the command below which creates a `mem_example` table via the `mem` bridge.

```sh
bridge exec mem CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
```

## *TQL* writing on the SQLite

```js
BYTES(payload() ?? `{
  "company": "acme",
  "employee": 10
}`)
SCRIPT({
  // get current time
  times := import("times")
  ts := times.now()
  // parse json from the payload
  ctx := import("context")
  val := ctx.value()
  // parse json
  json := import("json")
  msg := json.decode(val[0])
  ctx.yield(msg.company, msg.employee, ts)
})
INSERT(bridge("mem"), table("mem_example"), "company", "employee", "created_on")
```

```
machbase-neo» bridge query mem select * from mem_example;
╭────┬─────────┬──────────┬──────────┬───────┬───────┬──────┬──────────────────────────────────────╮
│ ID │ COMPANY │ EMPLOYEE │ DISCOUNT │ CODE  │ VALID │ MEMO │ CREATED_ON                           │
├────┼─────────┼──────────┼──────────┼───────┼───────┼──────┼──────────────────────────────────────┤
│  1 │ acme    │       10 │ <nil>    │ <nil> │ <nil> │ []   │ 2023-08-10 14:33:08.667491 +0900 KST │
╰────┴─────────┴──────────┴──────────┴───────┴───────┴──────┴──────────────────────────────────────╯
```

## *TQL* reading from the SQLite

Save the code below as `sqlite.tql`.

```js
SQL(bridge('mem'), "select * from mem_example")
CSV()
```

And call `curl -o - http://127.0.0.126:5654/db/tql/sqlite.tql`

```sh
curl -o - http://127.0.0.1:5654/db/tql/sqlite.tql
1,acme,10,,,,,1691647672291731000
```