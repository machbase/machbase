---
type: docs
title: '11.7 Node.js / TypeScript'
weight: 70
toc: true
aliases:
  - /dbms/reference/sdk-api/node-js-typescript/
---

## Overview

The Machbase TypeScript client (`@machbase/ts-client`) connects to Machbase Standard
Edition without native bindings. Node.js applications can execute SQL, retrieve results,
use Prepared Statements, and append log data.

This document covers installation, core APIs, examples, testing, and behavior.

## Multiple Databases

Set `database` in the connection configuration or URL to select the initial database.
There is no catalog getter; use SQL `CURRENT_DATABASE()` and `USE` to inspect and change it.

```typescript
const conn = createConnection({
  host: '127.0.0.1', port: 5656,
  user: 'APP_A', password: 'secret', database: 'FACTORY_A',
});
await conn.connect();
const [rows] = await conn.query('SELECT CURRENT_DATABASE()');
console.table(rows);
```

Appenders and prepared statements remain bound to the database selected at open/prepare
time. See the
[Multi-Database Operations Guide](/dbms/operations-configuration-recovery/multi-database/#95-nodejs)
for details.

## Installation

### Requirements

- Node.js 18 or later (LTS recommended)
- A reachable Machbase server (Standard Edition)

### Install from npm

Install with a package manager:

```bash
npm install @machbase/ts-client
# or
yarn add @machbase/ts-client
# or
pnpm add @machbase/ts-client
```

### Offline Installation

If Machbase supplied a `.tgz` package:

```bash
# example file name; your version may differ
npm install ./machbase-ts-client-<version>.tgz
```

### Verify Installation

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'ts-client import ok' : 'ts-client import failed')"
```

> **Note:** This client uses TCP sockets in Node.js. It does not provide a browser library
> with WebSocket transport.
> The NFX `cce422d2972` source tree reports `@machbase/ts-client` 1.0.1 in `package.json`.
> Some named binding, nullable, PK, ROWID, and TRANSACTION features were added after the
> public 1.0.1 release while retaining that version string. Check artifact commit
> provenance or build from this NFX source instead of assuming parity from the npm version.
>
> The default `SYS`/`MANAGER` credentials in this document are for local tests. Use
> dedicated credentials in production.

## Quick Start

This example connects to a local server, queries a system table, and closes the session.

```typescript
// src/example.ts
import { createConnection } from '@machbase/ts-client';

const conn = createConnection({
  host: process.env.MACH_HOST ?? '127.0.0.1',
  port: +(process.env.MACH_PORT ?? 5656),
  user: process.env.MACH_USER ?? 'SYS',
  password: process.env.MACH_PASS ?? 'MANAGER',
});

await conn.connect();
const [rows] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
console.log(rows);
await conn.end();
```

> **Transactions:** The server supports plain `BEGIN`, `COMMIT`, and `ROLLBACK` SQL for
> TRANSACTION tables. This client does not implement `beginTransaction`, `commit`, or
> `rollback` convenience methods; execute the SQL directly through `execute()`.

## Common Problems

- **ECONNREFUSED** – Check server status (`machadmin -e`), host and port, and firewall
  access to the listener. The default SQL port is 5656.
- **Authentication failed** – Check credentials and account connection privileges.

## API Reference

### Connection Management

#### createConnection(config)

Connects to the Machbase listener and creates a database session.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | string | `127.0.0.1` | Server IP address or host name |
| `port` | number | `5656` | Listener port |
| `user` | string | – | Database user (default `SYS`) |
| `password` | string | – | Password (default `MANAGER`) |
| `database` | string | `data` | Database name |
| `clientId` | string | `NPM` | Client ID shown in server logs |
| `showHiddenColumns` | boolean | `false` | Include hidden columns in metadata |
| `timezone` | string | Empty | Optional time zone identifier |
| `connectTimeout` | number | 5000 | Socket connection timeout (ms) |
| `queryTimeout` | number | 60000 | Per-command timeout (ms) |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

The promise rejects on socket connection failure, authentication error, or invalid
handshake response.

#### connect()

Opens the server connection.

```javascript
await conn.connect();
```

#### end()

Closes the socket connection. Further operations after `end()` raise an error.

```javascript
await conn.end();
```

### Execute SQL

#### execute(sql, values?)

Executes commands that may not return a result set. Use for DDL (`CREATE`, `ALTER`,
`DROP`) or DML (`INSERT`, `UPDATE`, `DELETE`).

```javascript
const [create] = await conn.execute('CREATE TRANSACTION TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // -> 0 for DDL

await conn.execute('BEGIN');
const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1
await conn.execute('COMMIT');
```

After a successful single `INSERT ... VALUES` in Standard Edition, the execution result
includes the ROWID in `rowId`. Use `bigint`, not `number`, to preserve 64-bit precision.

```javascript
const [result] = await conn.execute(
  'INSERT INTO sensor_log(message) VALUES(?)',
  ['started']
);

if (result.rowId !== undefined) {
  const rowId = result.rowId; // bigint
}
```

Executions without a ROWID have `rowId` set to `undefined`. See
[ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/) for batches, Append,
`INSERT ... SELECT`, and UPSERT.

#### query(sql, values?)

Executes a query that returns rows. Returns a two-element tuple, `[rows, fields]`.

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

#### Named Bind Parameter

For `execute()`, `query()`, and Prepared Statement `execute()`, arrays provide positional
input and plain objects provide named input.

```typescript
export type MachbaseNamedBindInput =
  Record<string, MachbaseBindInput>;
export type MachbaseExecuteInput =
  MachbaseBindInput[] | MachbaseNamedBindInput;
```

```javascript
await conn.execute(
  'INSERT INTO demo (ID, NAME) VALUES (:id, :name)',
  { id: 1, name: 'node-client' },
);

const [rows] = await conn.query(
  'SELECT ID, NAME FROM demo WHERE ID = :id OR PARENT_ID = :id',
  { id: 1 },
);
```

Pass an object to Prepared Statements as well:

```javascript
const stmt = await conn.prepare(
  'SELECT ID, NAME FROM demo WHERE ID = :id'
);
try {
  const [rows] = await stmt.execute({ id: 1 });
} finally {
  await stmt.close();
}
```

Object keys omit the leading colon and are case-sensitive. Repeated names receive the
same value. Object input with `?` placeholders, missing required keys, or keys absent
from SQL raises an error.

| Error code | Condition |
|---|---|
| `ERR_MACHBASE_BIND_MISSING` | Required name missing |
| `ERR_MACHBASE_BIND_EXTRA` | Name absent from SQL supplied |
| `ERR_MACHBASE_BIND_MIXED` | Mixed named and anonymous placeholders |
| `ERR_MACHBASE_NAMED_BIND_UNSUPPORTED` | Server does not support named binding |

Each `ColumnMeta` object in `fields` provides a `nullable` property.

```typescript
import { ColumnNullable } from '@machbase/ts-client';

const [rows, fields] = await conn.query(
  'SELECT ID, NAME, ID + 1 AS EXPR_VALUE FROM demo ORDER BY ID'
);

for (const field of fields) {
  if (field.nullable === ColumnNullable.NoNulls) {
    console.log(field.name, 'NO_NULLS');
  } else {
    console.log(field.name, 'NULL handling required');
  }
}
```

| Enum | Numeric value | Meaning |
|--------|:------:|------|
| `ColumnNullable.NoNulls` | `0` | Cannot be NULL |
| `ColumnNullable.Nullable` | `1` | Can be NULL |
| `ColumnNullable.Unknown` | `2` | Unknown |

`ColumnNullable.Unknown` does not mean `NOT NULL`; handle it as potentially nullable.
See
[Nullable Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)
for SQL result rules.

In Machbase SQL, `''` is SQL `NULL`: `field.nullable` is
`ColumnNullable.Nullable`, and the row value is JavaScript `null`. The literal `''''`
is one single quote character, returning `ColumnNullable.NoNulls` and the string `'`.

### PRIMARY KEY Metadata in SELECT Results

With a Machbase 8.7.0 server and matching SDK, `isPrimaryKey` in the `fields` array
returned by `query()` or `execute()` reports primary key membership for direct columns.

```ts
const [rows, fields] = await conn.query(
  'SELECT ID, VALUE, ID + 1 AS ID_EXPR FROM T_PK'
);
for (const field of fields) {
  console.log(field.name, field.isPrimaryKey);
}
```

Expressions, aggregates, and columns on the NULL-supplying side of outer joins report
`false`. Older servers or SDKs may not provide the primary key flag.

### Use Prepared Statements

#### prepare(sql)

Creates a Prepared Statement on the server.

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

The returned object provides these methods:

- `execute(parameters?)` – Executes the statement and returns `[rowsOrPacket, fields]`.
- `getColumns()` – Returns cached column metadata.
- `getLastMessage()` – Returns the latest server message.
- `getStatementId()` – Returns the internal Statement ID.
- `close()` – Releases server resources; repeated calls are safe.

`ColumnMeta` returned by `getColumns()` includes the same `nullable` values.

```typescript
const stmt = await conn.prepare('SELECT ID, NAME FROM demo WHERE ID = ?');
for (const column of stmt.getColumns()) {
  console.log(column.name, ColumnNullable[column.nullable]);
}
```

#### Prepared Statement Examples

**Reuse a Prepared SELECT:**

```javascript
const select = await conn.prepare('SELECT DEVICE_ID, SENSOR_VALUE FROM sensors WHERE DEVICE_ID = ?');
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
await select.close();
```

**Prepared Upsert:**

```javascript
const upsert = await conn.prepare(
  'INSERT INTO devices (DEVICE_ID, SENSOR_VALUE) VALUES (?, ?) ' +
  'ON DUPLICATE KEY UPDATE SET SENSOR_VALUE = ?',
);
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**Typed Arguments and NULL Handling:**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

Runnable example scripts are usually generated under `dist/examples/` after
`npm run build`. Examples typically resolve credentials in this order:
`MACHBASE_EXAMPLE_*`, `MACHBASE_SMOKE_*`, then `SYS/MANAGER@127.0.0.1`.

### Append API

#### appendBatch(table, columns, rows, options?)

Use `appendBatch()` to add multiple rows to a **LOG table**. Supply only user-visible
columns; LOG tables automatically include `_arrival_time` and `_rid`.

```javascript
const appendResult = await conn.appendBatch(
  'sensor_log',
  [
    { name: 'ID', type: 'int32' },
    { name: 'NAME', type: 'varchar' },
    { name: 'VALUE', type: 'float64' },
  ],
  [
    [1, 'alpha', 0.5],
    { values: [2, 'bravo', 1.25], arrivalTime: BigInt(Date.now()) * 1_000_000n },
  ],
);
console.log('Appended rows:', appendResult.rowsAppended);
```

Supported column types: `int32`, `int64`, `float64`, `varchar`.

- `rows` accepts arrays of values or `{ values, arrivalTime }` objects. `null` is
  automatically encoded as a Machbase sentinel.
- `options` accepts `arrivalTime` (one default) or `arrivalTimes` (one value per row).
- Convert to `bigint` before calculating epoch nanoseconds. Multiplication with `number`
  exceeds the safe integer range.

Returns `{ table, rowsAppended, rowsFailed, message }`.

> **Tip:** A column-count mismatch error occurs if the target is not a LOG table or
> column order does not match the schema. Use `appendOpen()` for TAG tables.

#### appendOpen(table, columns, options?)

Opens a lightweight Append session. By default, it uses native APPEND open/data/close.
Successful native writes do not return per-chunk responses.

```javascript
const stream = await conn.appendOpen('sensor_log', [
  { name: 'ID', type: 'int32' },
  { name: 'NAME', type: 'varchar' },
  { name: 'VALUE', type: 'float64' },
]);

await stream.append([
  [1, 'alpha', 0.5],
  [2, 'bravo', 1.25],
]);

await stream.append({ values: [3, 'charlie', 2.5] });
await stream.close();
```

Set `MACHBASE_NATIVE_APPEND=0` to disable native Append and force Prepared Statements.
If the server does not support native Append for a table type or session, the facade
automatically falls back to Prepared Statements.

Pass `Date` objects or `bigint` epoch values to DATETIME columns in TAG tables.

Pass sparse ARRAY values through `appendOpen()`. The current `@machbase/ts-client`
requires `columns`, so define all input columns in order even for full-row input.
Automatic inference from `appendOpen(table)` or an empty column list is unsupported.
If `ID` and `A` below are all the table input columns, this is full-row input. Each
row's `SparseArray` chooses positions within the ARRAY.

See the [all-column definition example](../data-input-load-export/array-append/#node-full-columns)
for connection, four-row ingestion, Close, and queries.

For selected-column Append in Machbase DBMS 8.7.0, set `name` to an ordinary column or
`ARRAY_COLUMN[position]`. To vary positions by row, pass `SparseArray` to a whole-array
target. Element targets and `SparseArray.set()` positions are 0-based.

```javascript
const { SparseArray } = require('@machbase/ts-client');

const stream = await conn.appendOpen('array_append_example', [
  { name: 'ID', type: 'int64' },
  { name: 'A', type: 'int32-array' },
]);
const sparse = new SparseArray(4).set(1, 200).set(3, 400);
await stream.append([[2n, sparse]]);
await stream.close();
```

Even when `MACHBASE_NATIVE_APPEND=0` forces the prepared fallback, `SparseArray` is
treated as an ARRAY-compatible value. See
[Sparse ARRAY and Selected-Column Append API](../data-input-load-export/array-append/)
for complete examples and NULL distinctions.

#### append(rows) on an append stream

Sends one or more rows to an open Append stream.

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

Native mode omits success responses for maximum throughput; only errors return failure packets.

### Helper Methods

#### ping()

Checks the connection with `SELECT 1 FROM V$TABLES`.

```javascript
await conn.ping();
```

#### promise()

Provides a familiar `.promise()`-style wrapper.

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format

Utilities for constructing SQL strings safely.

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## Testing and Diagnosis

### Scripts

- `npm run build` – Compiles TypeScript
- `npm run lint` – Runs ESLint on `src/`
- `npm run smoke` – Optional smoke tests (skipped without environment variables)
- `npm test` – Integration suite (requires a live server)
  1. Creates a LOG table
  2. Inserts and queries sample data
  3. Demonstrates prepared positional binding
  4. Runs append load tests (default: 5 batches × 200 rows) and verifies counts
  5. Checks direct SQL `BEGIN`/`ROLLBACK`/`COMMIT` on TRANSACTION tables
  6. Verifies the Machbase facade and `UPDATE` restrictions

Sample output:

```text
TRANSACTION transaction commit returned 1 row.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

## Tutorials

### Quick Start (LOG Table)

```javascript
// quickstart-log.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    await conn.execute(`INSERT INTO "${table}" VALUES (1, 'A', 0.5)`);
    const [rows] = await conn.query(`SELECT * FROM "${table}" ORDER BY ID`);
    console.table(rows);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### Reuse Prepared Statements

```javascript
// prepared-reuse.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_VOL_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE VOLATILE TABLE "${table}" (ID INTEGER PRIMARY KEY, NAME VARCHAR(64))`);
    for (let i = 1; i <= 3; i++) await conn.execute(`INSERT INTO "${table}" VALUES (${i}, 'N${i}')`);
    const stmt = await conn.prepare(`SELECT NAME FROM "${table}" WHERE ID = ?`);
    try {
      for (const id of [1, 2, 3]) {
        const [rows] = await stmt.execute([id]);
        console.log(id, rows[0]?.NAME);
      }
    } finally {
      await stmt.close();
    }
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### Batch Append to a LOG Table

```javascript
// append-batch.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOGAPP_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    const result = await conn.appendBatch(
      table,
      [
        { name: 'ID', type: 'int32' },
        { name: 'NAME', type: 'varchar' },
        { name: 'VALUE', type: 'float64' },
      ],
      [[1, 'X', 0.5], [2, 'Y', 1.25]],
    );
    console.log(result);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### Streaming Append to a TAG Table

```javascript
// append-tag-stream.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_TAG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE TAG TABLE "${table}" (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)`);
    const stream = await conn.appendOpen(table, [
      { name: 'NAME', type: 'varchar' },
      { name: 'TIME', type: 'int64' },
      { name: 'VALUE', type: 'float64' },
    ]);
    const now = Date.now();
    await stream.append([
      ['T-0001', new Date(now), 1.0],
      ['T-0002', new Date(now + 1), 2.0],
    ]);
    await stream.close();
    const [rows] = await conn.query(`SELECT COUNT(*) AS CNT FROM "${table}"`);
    console.log('count', rows[0]?.CNT);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

> Native mode is enabled by default. Set `MACHBASE_NATIVE_APPEND=0` to disable it.
> Successful chunks have no response; only errors return failure responses.

### Promise Wrapper and Ping

```javascript
// promise-and-ping.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const p = conn.promise();
    await p.ping(); // SELECT 1 FROM V$TABLES
    const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
    console.log(rows.map(r => r.NAME));
  } finally {
    await conn.end();
  }
})();
```

## Behavior and Limitations

### Transactions

Server SQL transactions work on TRANSACTION tables, but facade transaction convenience
methods are not implemented. Execute SQL directly on the same connection.

```javascript
await conn.execute('BEGIN');
await conn.execute('UPDATE orders SET status = ? WHERE order_id = ?', ['DONE', 1001]);
await conn.execute('COMMIT');
```

### Result Buffering and Pagination

The wrapper `query` method buffers the entire result set before returning it. For large
tables, paginate explicitly with `ORDER BY … LIMIT` or primary key ranges.

### Parameter Binding

Arrays bind to positional `?` placeholders; objects bind to `:name` placeholders.
Supported types include common scalar types such as `int32`, `int64`, `float64`, and
`varchar`. Supply an explicit type when passing `null`.

```javascript
{ value: null, type: 'varchar' }
```

See [Named Bind Parameter Syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)
for name rules and the maximum parameter count.

### Append API

Use `appendBatch` for LOG tables and `appendOpen`/`append` for incremental input. If
a table type, such as TAG, does not support the ingestion path, it automatically falls
back to repeated prepared execution. In production, split data into chunks and check `rowsFailed`.

### Error Handling

Errors are passed as standard `Error` objects (`QueryError` with the wrapper). Inspect
`error.message` or the `code` and `sql` fields of `QueryError` for diagnosis. Integration
tests deliberately query nonexistent tables and attempt unsupported `UPDATE` operations
to check that error messages are informative.

### SQL Considerations by Table Type

- **LOG tables** do not support `UPDATE`.
- **TAG table** data UPDATE is supported only in Standard Edition. It requires tag
  selection and BASETIME predicates. Tag names, the time axis, and metadata columns
  cannot be SET targets. SET expressions cannot reference existing-row columns.
- **VOLATILE table** UPDATE/DELETE uses primary key predicates. **LOOKUP tables** support
  both primary key predicates and general conditions; primary key predicates are
  efficient for single-row changes.

## Best Practices

1. **Always close connections:** Use `try...finally` to ensure `conn.end()` runs.
2. **Reuse Prepared Statements:** Prepare once and execute repeatedly for better performance.
3. **Use batch ingestion:** Use `appendBatch` or `appendOpen` for bulk loading.
4. **Handle errors:** Wrap database operations in `try...catch` and log appropriately.
5. **Use connection pools:** Introduce pooling in production to handle concurrent requests reliably.
6. **Parameterize queries:** Use binding (`?` placeholders) instead of concatenation to prevent SQL injection.
