---
title : Python
type : docs
weight: 30
---

## Overview

This guide is updated for the 2.1 package: install name is lowercase `machbaseapi`, and the package is now implemented in pure Python (no native `.so/.dll/.dylib` dependency).

You can continue using `import machbaseAPI` and existing `machbase` call patterns.

- `machbaseAPI` package name on PyPI: `machbaseapi`
- Module import pattern: `import machbaseAPI`
- DB-API style: `connect()` and `cursor()` are available
- `append*` callbacks can be observed through optional `on_ack` in append APIs.
- `append()`, `appendByTime()`, `appendData()`, and `appendDataByTime()` can be called without explicit column type codes; Machbase metadata is used for type inference.
- Connection-pool options are intentionally unsupported in 2.1 (`pool_name`, `pool_size`, `pool_reset_session`)

The examples below target the `machbase` class, which remains the main entry point for legacy-style scripts.

## Installation

### Requirements

- Python 3.8 or later with `pip`.
- A reachable Machbase server and credentials (default `SYS/MANAGER` on port `5656`).
- No native Machbase shared library installation is required in 2.1.

### Install from PyPI

```bash
pip3 install machbaseapi
```

If `pip3` is not on your PATH, use `python3 -m pip install machbaseapi`.

### Verify the module

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase class import ok:', bool(machbase))
print('connect function exists:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

A successful run confirms that the package can be imported and instantiated.

You can also run 2.1-style DB-API samples with `connect()`.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()
cur.execute('SELECT * FROM m$tables LIMIT 1')
print(cur.fetchall())
conn.close()
```

## Quick Start

The snippet below connects to a local server, creates a sample table, inserts rows, reads them back, and closes the session.

```python
#!/usr/bin/env python3
import json
from machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_sample')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = (
            "create table py_sample ("
            "ts datetime,"
            "device varchar(40),"
            "value double"
            ")"
        )
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for seq in range(3):
            sql = (
                "insert into py_sample values ("
                f"to_date('2024-01-0{seq+1}','YYYY-MM-DD'),"
                f"'sensor-{seq}',"
                f"{20.5 + seq}"
                ")"
            )
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.select('select * from py_sample order by ts') == 0:
            raise SystemExit(db.result())

        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            row = json.loads(payload)
            print('row:', row)

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

## Result Handling

Most `machbase` methods return `1` on success and `0` on failure. After each call, use `db.result()` to read the JSON-formatted payload emitted by the server. When iterating over `select()` results, call `db.fetch()` repeatedly until it returns `(0, None)`, then release resources with `db.selectClose()`.

## Supported API Matrix

| Class | API | Description | Return |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | Connect to a Machbase server with default credentials and port. | `1` on success, `0` on failure |
| `machbase` | `openEx(host, user, password, port, conn_str)` | Extended connect with additional connection string attributes. | `1` or `0` |
| `machbase` | `close()` | Terminate the current session. | `1` or `0` |
| `machbase` | `isOpened()` | Check whether a handle has been opened. | `1` or `0` |
| `machbase` | `isConnected()` | Verify that the handle is connected to the server. | `1` or `0` |
| `machbase` | `execute(sql, type=0)` | Run a SQL statement (all statements except `UPDATE`). | `1` or `0` |
| `machbase` | `schema(sql)` | Execute schema-related statements. | `1` or `0` |
| `machbase` | `tables()` | Fetch metadata for all tables. | `1` or `0` |
| `machbase` | `columns(table_name)` | Fetch column metadata for a specific table. | `1` or `0` |
| `machbase` | `column(table_name)` | Retrieve column layout using the low-level catalog call. | `1` or `0` |
| `machbase` | `statistics(table_name, user='SYS')` | Request table statistics via the CLI. | `1` or `0` |
| `machbase` | `select(sql)` | Execute a streaming `SELECT` or `DESC`. | `1` or `0` |
| `machbase` | `fetch()` | Pull the next row after `select()`. | `(rc, json_str)` |
| `machbase` | `selectClose()` | Close an open result set cursor. | `1` or `0` |
| `machbase` | `result()` | Return the latest JSON payload. | JSON string |
| `machbase` | `appendOpen(table_name, types=None)` | Begin append protocol with column type codes. When omitted, metadata can be loaded from server-side schema. | `1` or `0` |
| `machbase` | `appendData(table_name, aTypes=None, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | Append rows using the active append session. `aTypes` can be omitted and rows can be passed directly as the second argument. | `1` or `0` |
| `machbase` | `appendDataByTime(table_name, aTypes=None, values=None, format='YYYY-MM-DD HH24:MI:SS', times=None, on_ack=None)` | Append rows with explicit epoch timestamps. `aTypes` can also be omitted and rows can be passed directly as the second argument. | `1` or `0` |
| `machbase` | `appendFlush()` | Flush buffered append rows to disk. | `1` or `0` |
| `machbase` | `appendClose()` | Close the append session. | `1` or `0` |
| `machbase` | `append(table_name, aTypes=None, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | Convenience wrapper that opens, appends, and closes. `aTypes` can be omitted and `aValues` can be passed directly as second argument. | `1` or `0` |
| `machbase` | `appendByTime(table_name, aTypes=None, aValues=None, format='YYYY-MM-DD HH24:MI:SS', times=None)` | Convenience wrapper for time-aware append. `aTypes` can be omitted and `aValues` can be passed directly as second argument. | `1` or `0` |

## DB-API style API (2.1)

| API | Description | Return |
| -- | -- | -- |
| `connect(host, port, user, password, ...)` | Create DB-API connection | `MachbaseConnection` |
| `cursor(dictionary=True)` | Create a cursor (`True`: dict rows, `False`: tuple rows) | `MachbaseCursor` |
| `cursor.execute(sql, params=None)` | Execute SQL statement | `cursor` |
| `cursor.fetchone()` | Fetch one row | `tuple | dict | None` |
| `cursor.fetchmany(size)` | Fetch up to `size` rows | `list` |
| `cursor.fetchall()` | Fetch all rows | `list` |
| `cursor.close()` | Close cursor | `None` |
| `cursor.rowcount` | Number of affected rows | `int` |

## 2.1 append without explicit column types (recommended)

`append()` and `appendByTime()` can be called without a type list.  
Pass rows as the second argument and let the server metadata drive type handling.

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

## API Reference and Samples (Legacy 1.x behavior)

The examples below are mainly compatibility references from legacy releases. In the current 2.1 package, methods such as `getSessionId()`, `count()`, and `checkBit()` are not provided.

Update host, port, username, and password values as needed in each script. Every snippet is standalone and can be executed with `python3 script.py`.

### Connection management

#### machbase.open(), machbase.isOpened(), machbase.isConnected(), machbase.getSessionId(), machbase.close()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    print('isOpened before open:', db.isOpened())
    print('isConnected before open:', db.isConnected())

    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    print('session id:', db.getSessionId())
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
    print('connected with openEx, session id:', db.getSessionId())
    if db.close() == 0:
        raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DML and result buffers

#### machbase.execute(), machbase.result(), machbase.count()

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
        print('row count via count():', db.count())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Streaming SELECT helpers

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

        print('buffered rows:', db.count())
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            print('fetched row:', json.loads(payload))

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Schema helpers

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

### Metadata and statistics

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

### Append protocol primitives

`appendOpen()`, `appendData()`, `appendFlush()`, and `appendClose()` stream rows efficiently.
In 2.1 you can omit column types; server metadata is used automatically.

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

### Convenience append helpers

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
        epoch_times = [1704106800, 1704106860]

        if db.appendOpen('PY_APPEND_TIME') == 0:
            raise SystemExit(db.result())
        if db.appendDataByTime('PY_APPEND_TIME', rows, 'YYYY-MM-DD HH24:MI:SS', epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendDataByTime result:', db.result())
        db.appendClose()

        if db.appendByTime('PY_APPEND_TIME', rows, 'YYYY-MM-DD HH24:MI:SS', epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendByTime result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Diagnostics

#### machbase.checkBit()

`checkBit()` was used for native pointer-size checks in legacy releases and is not available in the 2.1 pure-Python package.

### Low-level bindings

The 2.1 package does not provide legacy ctypes helpers such as
`get_library_path()`, `openDB()`, `execAppend*()`, or pointer utility APIs.
For low-level C-layer access, please keep using the pre-2.0 package.
