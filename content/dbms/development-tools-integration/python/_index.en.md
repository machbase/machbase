---
type: docs
title: '11.6 Python'
weight: 60
toc: true
aliases:
  - /dbms/reference/sdk-api/python/
---

## Overview

This page describes package 2.4. The PyPI package is `machbaseapi` (lowercase). Its pure
Python implementation requires no native binaries (`.so/.dll/.dylib`). The existing
`machbase` workflow remains available.

- Installation package: `machbaseapi`
- Continue using `import machbaseAPI`.
- Supports DB-API `connect()` and `cursor()`.
- Since 2.4, `cursor(prepared=True)` reuses server statements across calls.
- `append*` can accept an `on_ack` callback to observe ACKs.
- `append()`, `appendByTime()`, `appendData()`, and `appendDataByTime()` work without a type list; types are inferred from server metadata.
- Since 2.3, omitted trailing append columns are stored as `NULL` through append null bits.
- TAG input must include values through the `value` column; omitted subsequent data and metadata columns can be stored as `NULL`.
- Connection pool options (`pool_name`, `pool_size`, `pool_reset_session`) are unsupported.

## Multiple Databases

Specify the initial database with `connect(database=...)`. There is no current-catalog
getter/setter. Verify it with `SELECT CURRENT_DATABASE()` after connecting and change
it with SQL `USE`.

```python
conn = connect(
    host='127.0.0.1', port=5656,
    user='APP_A', password='secret', database='FACTORY_A',
)
cur = conn.cursor()
cur.execute('SELECT CURRENT_DATABASE()')
print(cur.fetchone())
cur.execute('USE FACTORY_B')
```

The legacy `machbase.open()` has no database argument. Use the current `connect()` API
for multi-database work. See the
[Multi-Database Operations Guide](/dbms/operations-configuration-recovery/multi-database/#94-python)
for connection pool and statement binding rules.

## Installation

### Requirements

- Python 3.6 or later with `pip`
- A reachable Machbase server and credentials (default `SYS/MANAGER`, port `5656`)
- Version 2.4 has no native library dependencies.

### Install from PyPI

```bash
pip3 install machbaseapi
```

If `pip3` is not on PATH, use `python3 -m pip install machbaseapi`.

### Offline Installation from the Distribution Package

Without internet access, install the wheel included in the Machbase distribution package.

```bash
python3 -m pip install \
  $MACHBASE_HOME/3rd-party/python3-module/machbaseapi-2.4-py3-none-any.whl
```

The source distribution `machbaseapi-2.4.tar.gz` in the same directory is also available.
Check that Python is 3.6 or later before installing.

### Verify the Module

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase class import:', bool(machbase))
print('connect function exists:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

If this command succeeds, the package imports correctly.

## Quick Start

This DB-API example creates a sample LOG table, inserts and queries data, then removes
the table and closes the connection. The password comes from an environment variable.

```python
import os
from machbaseAPI import connect

conn = connect(
    host=os.getenv('MACH_HOST', '127.0.0.1'),
    port=int(os.getenv('MACH_PORT', '5656')),
    user=os.getenv('MACH_USER', 'SYS'),
    password=os.environ['MACHBASE_PASSWORD'],
)
cur = conn.cursor()

try:
    cur.execute(
        'CREATE LOG TABLE py_sample '
        '(ts DATETIME, device VARCHAR(40), value DOUBLE)'
    )
    cur.execute(
        "INSERT INTO py_sample VALUES ("
        "TO_DATE('2026-01-01','YYYY-MM-DD'), 'sensor-1', 20.5)"
    )
    cur.execute('SELECT device, value FROM py_sample')
    print(cur.fetchall())
finally:
    cur.execute('DROP TABLE py_sample')
    cur.close()
    conn.close()
```

## Handle Results

DB-API cursors provide `execute()`, `fetchone()`, and `fetchall()`. Close the cursor and
connection when finished, and remove sample objects from production databases.

### ROWID from INSERT

After a single `INSERT ... VALUES` through a DB-API cursor in Standard Edition, read
the inserted row's ROWID from `cursor.lastrowid`.

```python
cursor.execute(
    "INSERT INTO orders(item) VALUES(%s)",
    ("pump",),
)
row_id = cursor.lastrowid
```

The value is an arbitrary-precision Python `int`, preserving unsigned 64-bit ROWIDs as
positive integers. Executions without a ROWID return `None`. `executemany()`, Append,
`INSERT ... SELECT`, and UPSERT do not return ROWIDs. Do not reuse a previous value after
an execution failure. See [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/) for
detailed conditions.

### Nullable Metadata in DB-API Results

For DB-API cursors, `null_ok` at `cursor.description[i][6]` reports SELECT result column nullability.

```python
cursor.execute(sql)

for column in cursor.description:
    name = column[0]
    null_ok = column[6]
    print(name, null_ok)
```

| `null_ok` | Meaning |
|-----------|------|
| `False` | Cannot be NULL |
| `True` | Can be NULL |
| `None` | Unknown |

`None` does not mean `NOT NULL`; handle it as potentially nullable. See
[Nullable Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)
for SQL result rules.

In Machbase SQL, `''` is SQL `NULL`, so `null_ok` is `True`. For legacy compatibility,
the Python connector may return string SQL `NULL` as the Python empty string `""`.
`null_ok` describes column nullability, not whether an individual row is NULL. To distinguish
individual rows, also query an SQL `IS NULL` predicate or a CASE expression based on it.

### PRIMARY KEY Metadata in SELECT Results

With a Machbase 8.7.0 server and matching SDK, `is_primary_key` in
`cursor.column_metadata` reports whether a direct SELECT result column is a PRIMARY KEY.

```python
cursor.execute("SELECT ID, VALUE, ID + 1 AS ID_EXPR FROM T_PK")
for column in cursor.column_metadata:
    print(column.name, column.is_primary_key)
```

The standard seventh DB-API field in `cursor.description` (`null_ok`) still reports only
nullability. Expressions, aggregates, and columns on the NULL-supplying side of outer
joins are not primary keys, so `is_primary_key` is `False`. Older servers or SDKs may
not provide the primary key flag.

### Named Bind Parameter

The Python DB-API module uses `paramstyle = "named"`. Passing mappings to
`cursor.execute()` or `cursor.executemany()` executes `:name` SQL through server prepare/bind.

```python
from decimal import Decimal
from machbaseAPI import connect

conn = connect(host="127.0.0.1", port=5656,
               user="SYS", password="MANAGER")
cur = conn.cursor(dictionary=False)

cur.execute(
    """INSERT INTO SENSOR_DATA (ID, NAME, VALUE)
       VALUES (:id, :name, :value)""",
    {
        "id": 600,
        "name": "python-client",
        "value": Decimal("52.125000"),
    },
)

cur.execute(
    """SELECT ID, NAME FROM SENSOR_DATA
       WHERE ID = :id OR PARENT_ID = :id""",
    {"id": 600},
)
```

Pass each row as a mapping to `executemany()`.

```python
cur.executemany(
    "INSERT INTO SENSOR_DATA (ID, NAME, VALUE) "
    "VALUES (:id, :name, :value)",
    [
        {"id": 601, "name": "batch-a", "value": Decimal("1.5")},
        {"id": 602, "name": "batch-b", "value": None},
    ],
)
```

Server Prepared Statement lifetime depends on the cursor type and call:

| Cursor | Call | Server statement reuse |
|--------|------|----------------------------|
| Regular cursor | `execute(sql, params)` | This call only |
| Regular cursor | `executemany(sql, rows)` | Within this call |
| Prepared cursor | `execute()` / `executemany()` | Subsequent calls using identical original SQL |

A regular cursor uses server prepare/bind for `:name` with a mapping, but closes the
statement when the call ends. Use `cursor(prepared=True)` to reuse a statement across calls.

Mapping keys omit the leading colon and are case-sensitive. A repeated name applies one
value to every matching position. Missing names, extra keys, and mixed named/positional
binding raise `ProgrammingError`. Named APIs on older servers raise `NotSupportedError`
with SQLSTATE `0A000`.

For compatibility, `%s` and `%(name)s` remain supported. On regular cursors, these use
the legacy client-side SQL literal rendering path. Prepared cursors convert `%s` to `?`
and `%(name)s` to `:name`, then use server prepare/bind.

See [Named Bind Parameter Syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)
for shared name syntax.

## Prepared Cursor (2.4)

`connection.cursor(prepared=True)` retains one server Prepared Statement and reuses it
when executing the same SQL repeatedly. Use it for repeated INSERTs, parameterized
queries, and batches of the same SQL.

```python
from machbaseAPI import connect

conn = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
)
cur = conn.cursor(dictionary=False, raw=False, prepared=True)

sql = "INSERT INTO SENSOR_DATA (ID, NAME, VALUE) VALUES (%s, %s, %s)"
cur.execute(sql, (700, "sensor-a", 21.5))
cur.execute(sql, (701, "sensor-b", 22.1))
cur.executemany(
    sql,
    [
        (702, "sensor-c", 23.0),
        (703, "sensor-d", None),
    ],
)

cur.close()
conn.close()
```

Relevant `cursor()` arguments:

- `dictionary=True`: Return results as dictionaries keyed by column name.
- `dictionary=False`: Return results as tuples.
- `raw=True`: Preserve the existing raw-result contract.
- `prepared=True`: Return the public `MachbasePreparedCursor` type.
- `prepared=False`: Return a regular cursor; this is the default.

### Parameter marker

Prepared cursors support both Python DB-API and native Machbase formats.

| Public placeholder | Server placeholder | Parameter form |
|---------------|-------------|----------------|
| `%s` | `?` | Sequence, such as tuple or list |
| `?` | `?` | Sequence, such as tuple or list |
| `%(name)s` | `:name` | Mapping, such as dictionary |
| `:name` | `:name` | Mapping, such as dictionary |

Placeholder-like text in string literals, quoted identifiers, `--` comments, and
`/* ... */` comments is not converted. Do not mix positional and named placeholders in
one SQL statement. Names start with a letter, `_`, or `$`; subsequent characters may
include digits. Named placeholders require a Machbase 8.7.0 server and matching SDK.

```python
sql = (
    "SELECT ID, NAME FROM SENSOR_DATA "
    "WHERE ID = %(target)s OR PARENT_ID = %(target)s"
)
cur.execute(sql, {"target": 700})
rows = cur.fetchall()
```

### Statement Reuse

A prepared cursor reuses its cached server statement only when the original SQL string
exactly matches the previous call. Any difference, including whitespace or comments,
releases the old statement and prepares a new one.

```python
insert_cur = conn.cursor(prepared=True)
select_cur = conn.cursor(prepared=True)
```

One cursor retains one server statement. To keep multiple SQL statements reusable,
create a prepared cursor per SQL statement as above. The statement remains after
`executemany()` and is reused by subsequent `execute()` or `executemany()` with the same
SQL. An empty parameter list returns `0` without preparing or executing a statement.

### Errors and Close

The following inputs raise `ProgrammingError`:

- Placeholders with no parameters supplied
- A mapping for positional placeholders or a sequence for named placeholders
- Mixed positional and named placeholders
- Missing or extra named parameter keys
- Nonempty parameters for SQL without placeholders

For SQL without placeholders, pass `None`, an empty sequence, or an empty mapping to
indicate no parameters. An empty mapping is normalized to `None` internally, preserving
the same meaning across protocol versions.

Parameter errors preserve the cached statement, so the same SQL can run again with
valid parameters. On older servers, named parameters raise `NotSupportedError` with
SQLSTATE `0A000` before server PREPARE. This error does not release or replace the
cached statement. Use positional placeholders on older servers.

`cursor.close()` releases the cached server statement. Closing a cursor twice is safe.
If the connection is already closed, only local state is cleaned up, without a network
request. Calling `execute()`, `executemany()`, or fetch APIs on a closed prepared cursor
raises `InterfaceError`.

Prepared cursors do not change allowed SQL operations or Python API auto-commit behavior.
See [Support Scope and Constraints](../../reference/support-scope-constraints/) for
DML support by table type.

## Supported API Matrix

| Class | API | Description | Returns |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | Connects to the Machbase server using the specified credentials and port. | `1` on success, `0` on failure |
| `machbase` | `openEx(host, user, password, port, conn_str)` | Connects with additional connection-string properties. | `1` or `0` |
| `machbase` | `close()` | Closes the current session. | `1` or `0` |
| `machbase` | `isOpened()` | Checks whether the handle is open. | `1` or `0` |
| `machbase` | `isConnected()` | Checks the server connection state. | `1` or `0` |
| `machbase` | `execute(sql)` | Executes SQL directly. Routes `SELECT`, `WITH`, `DESC`, `DESCRIBE`, and `SHOW` to `select()`; other SQL uses `exec_direct()`. | `1` or `0` |
| `machbase` | `schema(sql)` | Executes schema commands. | `1` or `0` |
| `machbase` | `tables()` | Retrieves metadata for all tables. | `1` or `0` |
| `machbase` | `columns(table_name)` | Retrieves column metadata for a table. | `1` or `0` |
| `machbase` | `column(table_name)` | Retrieves column layout through a low-level catalog call. | `1` or `0` |
| `machbase` | `statistics(table_name, user='SYS')` | Requests table statistics through CLI. | `1` or `0` |
| `machbase` | `select(sql)` | Executes a streaming `SELECT` or `DESC`. | `1` or `0` |
| `machbase` | `fetch()` | Fetches the next row after `select()`. | `(rc, json_str)` |
| `machbase` | `selectClose()` | Closes the open result cursor. | `1` or `0` |
| `machbase` | `result()` | Returns the latest JSON payload. | JSON string |
| `machbase` | `appendOpen(table_name, types=None)` | Starts Append with column type codes; if omitted, uses server metadata. | `1` or `0` |
| `machbase` | `appendOpenColumns(table_name, columns, types=None)` | Starts Append for selected columns or ARRAY elements in Machbase DBMS 8.7.0. | `1` or `0` |
| `machbase` | `appendData(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | Adds rows to an active Append session. Pass rows as the second argument to omit types. Sends data packets immediately. | `1` or `0` |
| `machbase` | `appendDataByTime(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None, on_ack=None)` | Adds rows with explicit timestamps. Pass rows as the second argument to omit types and supply timestamps through `aTimes`. Sends data packets immediately. | `1` or `0` |
| `machbase` | `appendFlush()` | Synchronizes pending server responses for already transmitted Append data. It does not flush a deferred transmission buffer. | `1` or `0` |
| `machbase` | `appendClose()` | Closes the Append session. | `1` or `0` |
| `machbase` | `append(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | Opens, appends, and closes in one call. Pass rows as the second argument to omit types. | `1` or `0` |
| `machbase` | `appendByTime(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None)` | Convenience function for timestamp-aware Append. Pass rows as the second argument to omit types and supply timestamps through `aTimes`. | `1` or `0` |

## DB-API Style APIs (2.4)

| API | Description | Returns |
| -- | -- | -- |
| `connect(**kwargs)` | Creates a DB-API connection; pass `host`, `port`, `user`, `password`, and other properties as keywords | `MachbaseConnection` |
| `cursor(dictionary=True, raw=False, prepared=False)` | Creates a regular or prepared cursor | `MachbaseCursor` or `MachbasePreparedCursor` |
| `cursor.execute(sql, params=None)` | Executes SQL | `cursor` |
| `cursor.executemany(sql, seq_of_params)` | Executes the same SQL with multiple mappings or sequences | Execution count |
| `cursor.fetchone()` | Fetches one row | `tuple` / `dict` / `None` |
| `cursor.fetchmany(size)` | Fetches up to `size` rows | `list` |
| `cursor.fetchall()` | Fetches all rows | `list` |
| `cursor.description` | Result column metadata; the seventh field is `null_ok` | `tuple` / `None` |
| `cursor.lastrowid` | ROWID of a successful single INSERT; `None` for unsupported input methods or after failure | `int` / `None` |
| `cursor.close()` | Closes the cursor | `None` |
| `cursor.rowcount` | Affected-row count | `int` |
| `connection.append(table, rows, *, types=None, times=None, date_format=..., strict=False, columns=None)` | Appends rows; `columns` specifies selected columns or ARRAY element targets | Input row count |

## Omit Append Types and Pad Trailing NULLs in 2.3 (Recommended)

Call `append()` and `appendByTime()` without a type list. Pass rows directly as the
second argument to use server metadata. Since 2.3, omitted trailing input columns are
stored as `NULL` through append null bits.

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', rows) == 0:
            raise SystemExit(db.result())
        print('append without types result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DB-API Append with Trailing NULLs

`connect().append()` uses the same trailing `NULL` padding rules. Positional input
cannot skip intermediate columns; explicitly place `None` at a position to store an
intermediate value as `NULL`.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_append_null')
except Exception:
    pass
cur.execute('create table py_append_null(ts datetime, name varchar(20), value double, note varchar(40))')

conn.append('PY_APPEND_NULL', [
    ['2024-01-01 10:00:00', 'sensor-1', 12.3],
    ['2024-01-01 10:00:01', 'sensor-2', None, 'manual null'],
])

cur.execute('select ts, name, value, note from py_append_null order by ts')
print(cur.fetchall())
conn.close()
```

The first row omits `note`, so it is stored as `NULL`. The second row explicitly passes
`None` at the `value` position, so `value` is stored as `NULL`.

### TAG Append and NULL Metadata

TAG rows must supply values through the `name`, `time`, and `value` columns. Additional
data or metadata columns defined after `value` can be omitted and are stored as `NULL`.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_tag_append_null')
except Exception:
    pass
cur.execute('''
    create tag table py_tag_append_null (
        name varchar(40) primary key,
        time datetime basetime,
        value double summarized,
        status varchar(20)
    ) metadata (
        site varchar(20),
        line integer
    )
''')

conn.append('PY_TAG_APPEND_NULL', [
    ['tag-1', '2024-01-01 10:00:00', 12.3],
])

cur.execute('select name, time, value, status, site, line from py_tag_append_null')
print(cur.fetchall())
conn.close()
```

In this example, `status`, `site`, and `line` are all stored as `NULL`. A TAG append
that omits `value` fails.

## Compatible `machbase` Class API

The `machbase` class is retained for compatibility with existing applications. Prefer
the DB-API `connect()` approach above for new code. APIs such as `getSessionId()`,
`count()`, and `checkBit()` existed in the old native package but are not provided by
the current pure-Python implementation. Use the 2.4 DB-API examples where needed.

Adjust host, port, and credentials in each script to your environment. All examples
run independently with `python3 script.py`.

### Connection Management

#### machbase.open(), machbase.isOpened(), machbase.isConnected(), machbase.close()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    print('isOpened before open:', db.isOpened())
    print('isConnected before open:', db.isConnected())

    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    print('isOpened after open:', db.isOpened())
    print('isConnected after open:', db.isConnected())

    if db.close() == 0:
        raise SystemExit(db.result())

    print('isOpened after close:', db.isOpened())
    print('isConnected after close:', db.isConnected())

if __name__ == '__main__':
    main()
```

#### machbase.openEx()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    conn_str = 'APP_NAME=python-demo'
    if db.openEx('127.0.0.1', 'SYS', 'MANAGER', 5656, conn_str) == 0:
        raise SystemExit(db.result())
    print('connected with openEx:', db.isConnected())
    if db.close() == 0:
        raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DML and Result Buffers

#### machbase.execute(), machbase.result()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_exec_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_exec_demo(id integer, note varchar(32))'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(2):
            sql = f"insert into py_exec_demo values ({idx}, 'row-{idx}')"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.execute('select * from py_exec_demo order by id') == 0:
            raise SystemExit(db.result())
        payload = db.result()
        print('select payload:', payload)
        rows = json.loads(payload)
        print('decoded rows:', rows)
        print('row count:', len(rows))
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Streaming SELECT Helpers

#### machbase.select(), machbase.fetch(), machbase.selectClose()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_select_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_select_demo(id integer, value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(5):
            sql = f"insert into py_select_demo values ({idx}, {idx * 1.5})"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.select('select id, value from py_select_demo order by id') == 0:
            raise SystemExit(db.result())

        fetched = 0
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            print('fetched row:', json.loads(payload))
            fetched += 1
        print('fetched rows:', fetched)

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Schema Helpers

#### machbase.schema()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.schema('drop table py_schema_demo')
        print('schema drop rc:', rc)
        print('schema drop result:', db.result())

        ddl = 'create table py_schema_demo(name varchar(20), created datetime)'
        if db.schema(ddl) == 0:
            raise SystemExit(db.result())
        print('schema create result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Metadata and Statistics

#### machbase.tables(), machbase.columns(), machbase.column(), machbase.statistics()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        if db.tables() == 0:
            raise SystemExit(db.result())
        print('tables metadata:', db.result())

        if db.columns('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('columns metadata:', db.result())

        if db.column('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('column metadata:', db.result())

        if db.statistics('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('statistics output:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Append Protocol Basics

Combine `appendOpen()`, `appendData()`, `appendFlush()`, and `appendClose()` to stream
rows efficiently. Since 2.1, `appendOpen()` can omit types. `appendData()` and
`appendDataByTime()` send data packets immediately. `appendFlush()` is a synchronization
point that checks pending server responses for already transmitted append data.

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_append_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_append_demo(ts datetime, device varchar(32), value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        if db.appendOpen('PY_APPEND_DEMO') == 0:
            raise SystemExit(db.result())

        rows = [
            ['2024-01-01 09:00:00', 'sensor-a', 21.5],
            ['2024-01-01 09:05:00', 'sensor-b', 22.1],
        ]
        if db.appendData('PY_APPEND_DEMO', rows) == 0:
            raise SystemExit(db.result())
        print('appendData result:', db.result())

        if db.appendFlush() == 0:
            raise SystemExit(db.result())
        print('appendFlush result:', db.result())

        if db.appendClose() == 0:
            raise SystemExit(db.result())
        print('appendClose result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Append Convenience Functions

#### machbase.append()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        values = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', values) == 0:
            raise SystemExit(db.result())
        print('append() result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### machbase.appendDataByTime(), machbase.appendByTime()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_time')
        db.result()
        ddl = 'create table py_append_time(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 11:00:00', 'node-2', 40.1],
            ['2024-01-01 11:01:00', 'node-2', 40.7],
        ]
        epoch_times = [
            1704106800 * 1_000_000_000,
            1704106860 * 1_000_000_000,
        ]

        if db.appendOpen('PY_APPEND_TIME') == 0:
            raise SystemExit(db.result())
        if db.appendDataByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendDataByTime result:', db.result())
        db.appendClose()

        if db.appendByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendByTime result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

`aTimes` is a sequence of epoch nanoseconds in the same order as the rows. Do not pass
Unix timestamps in seconds unchanged.

## ARRAY and Selected-Column Append

Machbase DBMS 8.7.0 returns ARRAY values as Python `list`; prepared input accepts
`list` or `tuple`. An element NULL is `None` within the collection; whole-array NULL
is `None` for the column value itself.

You can also pass `SparseArray` to `connection.append(table, rows)` without a column list.

```python
from machbaseAPI import SparseArray

sparse = SparseArray(4).set(1, 200).set(3, 400)
connection.append("ARRAY_APPEND_FULL_EXAMPLE", [[2, sparse]])
```

This code assumes a table with `ID LONG, A INT32[4]` and an open connection. See the
[standard input example](../data-input-load-export/array-append/#python-full-open) for
whole NULL, empty sparse arrays, and result checks. The legacy wrapper has an
[`appendOpen(table)` example](../data-input-load-export/array-append/#python-legacy-full-open).

Specify selected targets with `connection.append(..., columns=...)`. Use `SparseArray`
for positions that vary by row. Element targets and positions in `SparseArray.set()`
are 0-based.

```python
from machbaseAPI import SparseArray, connect

connection = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
)
try:
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[1, 10, 40]],
        columns=["ID", "A[0]", "A[3]"],
    )

    sparse = SparseArray(4).set(1, 200).set(3, 400)
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[2, sparse]],
        columns=["ID", "A"],
    )
finally:
    connection.close()
```

`SparseArray.clear()` resets all elements to NULL while preserving the element count.
See [Sparse ARRAY and Selected-Column Append API](../data-input-load-export/array-append/)
for NULL distinctions, validation, and legacy API examples.
