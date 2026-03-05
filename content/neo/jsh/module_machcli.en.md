---
title: "machcli"
type: docs
weight: 9
---

{{< neo_since ver="8.0.73" />}}

The `machcli` module provides a Machbase client API for JSH applications.

## Client

Creates a database client.

<h6>Syntax</h6>

```js
new Client(config)
```

<h6>Configuration fields</h6>

- `host` (default: `127.0.0.1`)
- `port` (default: `5656`)
- `user` (default: `sys`)
- `password` (default: `manager`)
- `alternativeHost` (optional)
- `alternativePort` (optional)

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
```

**Client.connect()**

Opens a connection and returns a `Connection` object.

<h6>Syntax</h6>

```js
connect()
```

**Client.close()**

Closes the underlying database client.

<h6>Syntax</h6>

```js
close()
```

**Client.user()**

Returns the configured user name (uppercase).

<h6>Syntax</h6>

```js
user()
```

**Client.normalizeTableName()**

Normalizes a table name into `[database, user, table]` format.

<h6>Syntax</h6>

```js
normalizeTableName(tableName)
```

## Connection

Connection object returned by `Client.connect()`.

**Connection.query()**

Executes a SELECT query and returns a `Rows` object.

<h6>Syntax</h6>

```js
query(sql[, ...params])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[12]}
const { Client } = require('machcli');
var db, conn, rows;
const conf = {
  host: '127.0.0.1',
  port: 5656,
  user: 'sys',
  password: 'manager' 
};
try {
  db = new Client(conf);
  conn = db.connect();
  rows = conn.query('SELECT NAME, TIME, VALUE FROM TAG LIMIT ?', 1);
  for (const row of rows) {
    console.println(row.NAME, row.TIME, row.VALUE);
  }
} catch( e ) {
  console.println("ERROR", e.message);
}
rows && rows.close();
conn && conn.close();
db && db.close();
```

**Connection.queryRow()**

Executes a query and returns a single row object.

Returned object includes `_ROWNUM` and each column as a property.

<h6>Syntax</h6>

```js
queryRow(sql[, ...params])
```

**Connection.exec()**

Executes DDL/DML and returns result object.

Returned fields:

- `rowsAffected`
- `message`

<h6>Syntax</h6>

```js
exec(sql[, ...params])
```

**Connection.explain()**

Returns an execution plan string.

<h6>Syntax</h6>

```js
explain(sql[, ...params])
```

**Connection.append()**

Creates an appender object for bulk inserts.

The returned appender supports methods such as `append()`, `flush()`, `close()`.

<h6>Syntax</h6>

```js
append(tableName)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,6]}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
const conn = db.connect();
const appender = conn.append('TAG');
appender.append('sensor-1', new Date(), 12.34);
appender.flush();
const result = appender.close();
console.println(result);
conn.close();
db.close();
```

**Connection.close()**

Closes the connection.

<h6>Syntax</h6>

```js
close()
```

## Rows

Result set object returned by `Connection.query()`.

**Rows.message**

Message from query execution.

**Rows.isFetchable()**

Returns whether the result set can fetch rows.

<h6>Syntax</h6>

```js
isFetchable()
```

**Rows.next()**

Returns an iterator result object.

- `{ value: Row, done: false }` while rows remain
- `{ done: true }` when completed

<h6>Syntax</h6>

```js
next()
```

**Rows.close()**

Closes the result set.

<h6>Syntax</h6>

```js
close()
```

## Row

Represents a fetched row object.

- Each column is available as `row.COLUMN_NAME`.
- `for...of` iteration is supported.

## queryDatabaseId()

Returns backup tablespace ID for a mounted database.

- Returns `-1` for default database (`''` or `MACHBASEDB`).
- Throws an error when the database is not found.

<h6>Syntax</h6>

```js
queryDatabaseId(conn, dbName)
```

## queryTableType()

Returns table type code by normalized table name tokens.

<h6>Syntax</h6>

```js
queryTableType(conn, names)
```

## TableType

**stringTableType()**

Table type constants and string converter.

<h6>TableType values</h6>

- `Log`, `Fixed`, `Volatile`, `Lookup`, `KeyValue`, `Tag`

<h6>Syntax</h6>

```js
stringTableType(type)
```

## TableFlag

**stringTableFlag()**

Table flag constants and string converter.

<h6>TableFlag values</h6>

- `None`, `Data`, `Rollup`, `Meta`, `Stat`

<h6>Syntax</h6>

```js
stringTableFlag(flag)
```

**stringTableDescription()**

Returns combined table description with type and flag text.

<h6>Syntax</h6>

```js
stringTableDescription(type, flag)
```

## ColumnType

**stringColumnType()**

Column type constants and string converter.

<h6>Main ColumnType values</h6>

- `Short`, `UShort`, `Integer`, `UInteger`, `Long`, `ULong`
- `Float`, `Double`, `Varchar`, `Text`, `Clob`, `Blob`, `Binary`
- `Datetime`, `IPv4`, `IPv6`, `JSON`

<h6>Syntax</h6>

```js
stringColumnType(columnType)
```

**columnWidth()**

Returns default display width for a column type.

<h6>Syntax</h6>

```js
columnWidth(columnType, length)
```

## ColumnFlag

**stringColumnFlag()**

Column flag constants and string converter.

<h6>ColumnFlag values</h6>

- `TagName`
- `Basetime`
- `Summarized`
- `MetaColumn`

<h6>Syntax</h6>

```js
stringColumnFlag(flag)
```
