---
title: Bridge - SQLite
type: docs
weight: 11
---

## Register a bridge to sqlite3

Register a bridge that connects to the SQLite.

```
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
```

SQLite supports memory only mode like below.

```
bridge add -t sqlite mem file::memory:?cache=shared
```

In the web UI, register it as follows. The settings are the same as the command above.

1. Click the <img src="/neo/bridges/img/bridge_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> icon in the left menu.

2. Click the <img src="/neo/bridges/img/bridge_add_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> icon in the `BRIDGE` header.

3. Enter `mem` in `Name`, choose `SQLite` in `Type`, and enter `file::memory:?cache=shared` in `Connection String`.

4. Click `Create`.

{{< figure src="/neo/bridges/img/sqlite-add.png" width="500" >}}

## Test the bridge's connectivity

```
machbase-neo» bridge test mem;
Test bridge mem connectivity... success 11.917µs
```

In the web UI, select the bridge in the `BRIDGE` list and click `Test`. When the connection succeeds, `success` is shown.

{{< figure src="/neo/bridges/img/sqlite-test.png" width="600" >}}

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
The standard SQL editor can execute SQL for the bridged database if there is an `-- env: bridge=<name>` comment. The *env* comment remains effective until it is cleared by `-- env: reset`.

```sql
-- env: bridge=mem
CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
-- env: reset
```

{{< figure src="/neo/bridges/img/sqlite-sql-create-table.png" width="600" >}}

## DML on the SQL Editor

```sql
-- env: bridge=mem
INSERT INTO mem_example(company, employee, created_on) 
    values('Fedel-Gaylord', 12, datetime('now'));

INSERT INTO mem_example(company, employee, created_on) 
    values('Simoni', 23, datetime('now'));

SELECT company, employee, datetime(created_on, 'localtime') from mem_example;

DELETE from mem_example;
-- env: reset
```

{{< figure src="/neo/bridges/img/sqlite-sql-dml.png" width="600" >}}

## *TQL* writing on the SQLite

```js {linenos=table,hl_lines=["8-10"],linenostart=1}
FAKE( json({
    ["COMPANY", "EMPLOYEE"],
    ["NovaWave", 10],
    ["Sunflower", 20]
}))

DROP(1) // skip header
SQL(bridge("mem"), 
    `insert into mem_example (company, employee, created_on) values(?, ?, ?)`,
    value(0), value(1), time('now'))
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
SQL(bridge('mem'), "select company, employee, created_on from mem_example")
CSV()
```

And call the endpoint with `curl` command or open the browser.

```sh
curl -o - http://127.0.0.1:5654/db/tql/sqlite.tql
```

```csv
NovaWave,10,1704866777160399000
Sunflower,20,1704866777160407000
```

## Copy data from/to SQLite

This example demonstrates how to copy data from Machbase to an SQLite bridge.

**Bridge**

Define a `sqlite` bridge with the following details:

- Type: `SQLite`
- Connection string: `file:///tmp/sqlite.db`

**SQL**

Create the `example` table in the SQLite database located at "/tmp/sqlite.db".

```sql
--env: bridge=sqlite
CREATE TABLE IF NOT EXISTS example (
    NAME TEXT,
    TIME DATETIME,
    VALUE REAL
);
-- env: reset
```

**TQL**

The TQL script below executes a `SELECT` statement using the `SQL()` function to retrieve the required data, 
and then writes the data into the SQLite database using the `INSERT()` function with `bridge("sqlite")` as the first argument.

```js
SQL(`select name, time, value from example where name = 'my-car'`)
SQL(bridge("sqlite"), 
    `insert into example values(?,?,?)`,
    value(0), value(1), value(2))
```

**SQL**

```sql
--env: bridge=sqlite
SELECT * FROM example order by TIME;
-- env: reset
```