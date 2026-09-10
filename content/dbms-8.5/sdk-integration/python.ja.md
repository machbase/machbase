---
title : Python
type : docs
weight: 30
toc: true
---

## 概要 {#overview}

本ガイドはパッケージ 2.3 を対象とします。インストール名は小文字の `machbaseapi` で、純粋な Python 実装になりました。ネイティブの `.so/.dll/.dylib` は不要です。

`import machbaseAPI` と既存の `machbase` の呼び出し方を引き続き使用できます。

- PyPI のパッケージ名：`machbaseapi`
- インポート：`import machbaseAPI`
- DB-API 形式の `connect()` と `cursor()` を利用可能
- APPEND API の任意引数 `on_ack` で応答コールバックを取得可能
- `append()`、`appendByTime()`、`appendData()`、`appendDataByTime()` は列型コードを省略でき、メタデータから型を推論します。
- 2.3 では、APPEND 行の省略した末尾列を null-bit メタデータにより `NULL` として保存します。
- TAG テーブルでは `value` 列までの値が必須です。その後の追加列やメタデータ列は省略でき、`NULL` で保存します。
- 2.3 では接続プール設定（`pool_name`、`pool_size`、`pool_reset_session`）はサポートしません。

以下は、従来形式のスクリプトの入口である `machbase` クラスを使用します。

## インストール {#installation}

### 要件 {#requirements}

- `pip` を利用できる Python 3.6 以降。
- 接続可能なサーバーと認証情報（既定はポート `5656` の `SYS/MANAGER`）。
- 2.3 ではネイティブの Machbase 共有ライブラリーは不要です。

### PyPI からのインストール {#install-from-pypi}

```bash
pip3 install machbaseapi
```

`pip3` が PATH にない場合は `python3 -m pip install machbaseapi` を使用します。

### モジュールの確認 {#verify-the-module}

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase class import ok:', bool(machbase))
print('connect function exists:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

成功すれば、インポートとインスタンス作成が可能であることを確認できます。

`connect()` による DB-API の例も実行できます。

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()
cur.execute('SELECT * FROM m$tables LIMIT 1')
print(cur.fetchall())
conn.close()
```

## クイックスタート {#quick-start}

ローカルサーバーに接続し、テーブルを作成して挿入、検索し、セッションを閉じる例です。

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

## 結果の処理 {#result-handling}

`machbase` の多くのメソッドは、成功時 `1`、失敗時 `0` を返します。各呼び出し後に `db.result()` で JSON 形式の結果を取得します。`select()` の結果は、`db.fetch()` が `(0, None)` を返すまで繰り返し取得し、`db.selectClose()` で解放します。

## 対応 API {#supported-api-matrix}

| クラス | API | 説明 | 戻り値 |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | サーバーに接続。既定の認証情報とポートを使用可能。 | 成功時 `1`、失敗時 `0` |
| `machbase` | `openEx(host, user, password, port, conn_str)` | 追加の接続文字列属性を指定して接続。 | `1` または `0` |
| `machbase` | `close()` | 現在のセッションを終了。 | `1` または `0` |
| `machbase` | `isOpened()` | ハンドルが開いているか確認。 | `1` または `0` |
| `machbase` | `isConnected()` | サーバーへの接続状態を確認。 | `1` または `0` |
| `machbase` | `execute(sql)` | SQL を直接実行。`SELECT`、`WITH`、`DESC`、`DESCRIBE`、`SHOW` は `select()`、それ以外は `exec_direct()` を使用。 | `1` または `0` |
| `machbase` | `schema(sql)` | スキーマ関連の文を実行。 | `1` または `0` |
| `machbase` | `tables()` | すべてのテーブルのメタデータを取得。 | `1` または `0` |
| `machbase` | `columns(table_name)` | 指定テーブルの列メタデータを取得。 | `1` または `0` |
| `machbase` | `column(table_name)` | 低水準のカタログ呼び出しで列構成を取得。 | `1` または `0` |
| `machbase` | `statistics(table_name, user='SYS')` | CLI 経由でテーブル統計を取得。 | `1` または `0` |
| `machbase` | `select(sql)` | ストリーミング `SELECT` または `DESC` を実行。 | `1` または `0` |
| `machbase` | `fetch()` | `select()` 後に次の行を取得。 | `(rc, json_str)` |
| `machbase` | `selectClose()` | 結果セットのカーソルを閉じる。 | `1` または `0` |
| `machbase` | `result()` | 最新の JSON ペイロードを返す。 | JSON 文字列 |
| `machbase` | `appendOpen(table_name, types=None)` | 列型コードを指定して APPEND を開始。省略時はサーバーのスキーマを取得可能。 | `1` または `0` |
| `machbase` | `appendData(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | 有効な APPEND セッションで行を入力。型を省略する場合は第 2 引数に行を指定。呼び出し時に直ちに送信。 | `1` または `0` |
| `machbase` | `appendDataByTime(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None, on_ack=None)` | エポック時刻を指定して入力。型を省略する場合は第 2 引数に行、`aTimes` に時刻を指定。呼び出し時に直ちに送信。 | `1` または `0` |
| `machbase` | `appendFlush()` | 送信済み APPEND の保留応答を確認する同期ポイント。遅延送信バッファーのフラッシュ API ではない。 | `1` または `0` |
| `machbase` | `appendClose()` | APPEND セッションを閉じる。 | `1` または `0` |
| `machbase` | `append(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | 開始、入力、終了をまとめて行う。型を省略する場合は第 2 引数に行を指定。 | `1` または `0` |
| `machbase` | `appendByTime(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None)` | 時刻付き APPEND のラッパー。型を省略する場合は第 2 引数に行、`aTimes` に時刻を指定。 | `1` または `0` |

## DB-API 形式の API（2.3） {#db-api-style-api-23}

| API | 説明 | 戻り値 |
| -- | -- | -- |
| `connect(**kwargs)` | DB-API 接続を作成。`host`、`port`、`user`、`password` などをキーワード引数で指定。 | `MachbaseConnection` |
| `cursor(dictionary=True)` | カーソルを作成（`True`：辞書の行、`False`：タプルの行）。 | `MachbaseCursor` |
| `cursor.execute(sql, params=None)` | SQL 文を実行。 | `cursor` |
| `cursor.fetchone()` | 1行を取得。 | `tuple \| dict \| None` |
| `cursor.fetchmany(size)` | 最大 `size` 行を取得。 | `list` |
| `cursor.fetchall()` | すべての行を取得。 | `list` |
| `cursor.close()` | カーソルを閉じる。 | `None` |
| `cursor.rowcount` | 影響を受けた行数。 | `int` |
| `connection.append(table, rows, types=None, times=None, strict=False)` | Append プロトコルで行を入力。2.3 以降では省略した末尾列を `NULL` で補完。 | 入力行数 |

## 2.3：列型の省略と末尾列の `NULL` 補完（推奨） {#23-append-without-explicit-column-types-and-trailing-null-padding-recommended}

`append()` と `appendByTime()` は、型のリストを省略できます。
第 2 引数に行を渡し、サーバーのメタデータで型を処理します。
2.3 以降では末尾の列を省略でき、null-bit メタデータによって `NULL` として保存します。

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

### DB-API で末尾列を `NULL` にする例 {#db-api-append-trailing-null-example}

`connect().append()` も同じ規則です。位置指定の入力では途中の列を飛ばせないため、途中を `NULL` にする場合は `None` を明示します。

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

1行目は `note` を省略するので `NULL` になります。2 行目は `value` に `None` を渡すので、`value` が `NULL` になります。

### TAG テーブルの APPEND とメタデータの `NULL` {#tag-table-append-and-metadata-null-example}

TAG テーブルでは `name`、`time`、`value` が必須です。`value` より後の追加列とメタデータ列は省略でき、`NULL` になります。

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

この例では `status`、`site`、`line` が `NULL` になります。`value` を省略した TAG APPEND は失敗します。

## API と使用例（従来形式の `machbase` クラス） {#api-reference-and-samples-legacy-style-machbase-class}

以下は 2.3 でも利用できる従来形式の `machbase` クラスの例です。
古いネイティブ版にあった `getSessionId()`、`count()`、`checkBit()` は、
現在の純粋な Python 実装では提供しません。必要に応じて、2.3のDB-APIの例を参照してください。

各例のホスト、ポート、ユーザー、パスワードを環境に合わせて変更します。各スクリプトは独立して `python3 script.py` で実行できます。

### 接続管理 {#connection-management}

#### machbase.open(), machbase.isOpened(), machbase.isConnected(), machbase.close() {#machbaseopen-machbaseisopened-machbaseisconnected-machbaseclose}

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

#### machbase.openEx() {#machbaseopenex}

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

### DML と結果バッファー {#dml-and-result-buffers}

#### machbase.execute(), machbase.result() {#machbaseexecute-machbaseresult}

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

### ストリーミング `SELECT` {#streaming-select-helpers}

#### machbase.select(), machbase.fetch(), machbase.selectClose() {#machbaseselect-machbasefetch-machbaseselectclose}

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

### スキーマ操作 {#schema-helpers}

#### machbase.schema() {#machbaseschema}

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

### メタデータと統計 {#metadata-and-statistics}

#### machbase.tables(), machbase.columns(), machbase.column(), machbase.statistics() {#machbasetables-machbasecolumns-machbasecolumn-machbasestatistics}

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

### Append プロトコルの基本操作 {#append-protocol-primitives}

`appendOpen()`、`appendData()`、`appendFlush()`、`appendClose()` で効率よく行を入力できます。
2.1以降では、列型を省略して`appendOpen()`を開始でき、サーバーのメタデータを自動的に使用します。
`appendData()` と `appendDataByTime()` は呼び出し時に直ちにデータを送信します。`appendFlush()` は、送信済みデータの保留応答を確認する同期ポイントです。

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

### APPEND の便利なラッパー {#convenience-append-helpers}

#### machbase.append() {#machbaseappend}

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

#### machbase.appendDataByTime(), machbase.appendByTime() {#machbaseappenddatabytime-machbaseappendbytime}

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

### 診断 {#diagnostics}

#### machbase.checkBit() {#machbasecheckbit}

`checkBit()` は旧版でネイティブのポインターサイズを確認するもので、2.3 の純粋な Python 版にはありません。

### 低水準バインディング {#low-level-bindings}

2.3 では、従来の ctypes ヘルパーである
`get_library_path()`、`openDB()`、`execAppend*()`、`getlAddr`や`getrAddr`などのポインター操作APIは提供しません。
低水準の C 層にアクセスする場合は、2.0 より前のパッケージを引き続き使用してください。
