---
title : Python
type : docs
weight: 30
---

## 개요

이 문서는 2.0 패키지를 기준으로 정리했습니다. PyPI 패키지명은 `machbaseapi`(소문자)이고 구현은 순수 Python입니다(네이티브 `.so/.dll/.dylib` 불필요).

기존 `machbase` 사용 흐름은 유지됩니다.

- 패키지 설치명: `machbaseapi`
- 기존과 동일하게 `import machbaseAPI` 사용
- DB-API 방식 `connect()`, `cursor()` 지원
- `append*`는 `on_ack` 콜백을 추가할 수 있어 ACK 관찰 가능
- `append()` / `appendByTime()`는 타입 리스트를 생략해도 동작합니다. 서버 메타데이터 기반으로 타입을 자동 추론합니다.
- 커넥션 풀 옵션(`pool_name`, `pool_size`, `pool_reset_session`) 미지원

아래 예제는 기존 `machbase` 클래스 기반 레거시 스크립트를 대상으로 합니다.

## 설치

### 요구 사항

- `pip`을 사용할 수 있는 Python 3.8 이상
- 접속 가능한 Machbase 서버와 계정 정보(기본 계정 `SYS/MANAGER`, 포트 `5656`)
- 2.0은 네이티브 라이브러리 의존성이 없습니다.

### PyPI에서 설치

```bash
pip3 install machbaseapi
```

`pip3`가 PATH에 없다면 `python3 -m pip install machbaseapi` 명령을 사용합니다.

### 모듈 확인

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase 클래스 import:', bool(machbase))
print('connect 함수 존재:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

위 명령이 성공하면 패키지를 정상적으로 import하고 인스턴스를 생성할 수 있음을 의미합니다.

DB-API 방식 샘플도 바로 사용할 수 있습니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()
cur.execute('SELECT * FROM m$tables LIMIT 1')
print(cur.fetchall())
conn.close()
```

## 빠르게 시작하기

아래 스니펫은 로컬 서버에 접속해 샘플 테이블을 만들고, 데이터를 삽입한 뒤 조회하고 세션을 종료하는 흐름을 보여줍니다.

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

## 결과 처리

대다수 `machbase` 메서드는 성공 시 `1`, 실패 시 `0`을 반환합니다. 호출 직후 `db.result()`를 사용하면 서버에서 반환한 JSON 형식의 페이로드를 확인할 수 있습니다. `select()` 결과를 순회할 때는 `(0, None)`가 반환될 때까지 `db.fetch()`를 반복 호출하고, 마지막에 `db.selectClose()`로 리소스를 해제합니다.

## 지원 API 매트릭스

| 클래스 | API | 설명 | 반환 |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | 기본 계정과 포트로 Machbase 서버에 연결합니다. | 성공 시 `1`, 실패 시 `0` |
| `machbase` | `openEx(host, user, password, port, conn_str)` | 추가 연결 문자열 속성을 사용해 확장 연결을 수행합니다. | `1` 또는 `0` |
| `machbase` | `close()` | 현재 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `isOpened()` | 핸들이 열려 있는지 확인합니다. | `1` 또는 `0` |
| `machbase` | `isConnected()` | 서버와의 연결 상태를 확인합니다. | `1` 또는 `0` |
| `machbase` | `execute(sql, type=0)` | `UPDATE`를 제외한 SQL 문을 실행합니다. | `1` 또는 `0` |
| `machbase` | `schema(sql)` | 스키마 관련 명령을 실행합니다. | `1` 또는 `0` |
| `machbase` | `tables()` | 모든 테이블의 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `columns(table_name)` | 특정 테이블의 컬럼 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `column(table_name)` | 저수준 카탈로그 호출로 컬럼 레이아웃을 가져옵니다. | `1` 또는 `0` |
| `machbase` | `statistics(table_name, user='SYS')` | CLI를 통해 테이블 통계를 요청합니다. | `1` 또는 `0` |
| `machbase` | `select(sql)` | 스트리밍 `SELECT` 또는 `DESC`를 실행합니다. | `1` 또는 `0` |
| `machbase` | `fetch()` | `select()` 호출 이후 다음 행을 가져옵니다. | `(rc, json_str)` |
| `machbase` | `selectClose()` | 열린 결과 집합 커서를 닫습니다. | `1` 또는 `0` |
| `machbase` | `result()` | 최신 JSON 페이로드를 반환합니다. | JSON 문자열 |
| `machbase` | `appendOpen(table_name, types)` | 컬럼 타입 코드를 지정하여 Append 프로토콜을 시작합니다. | `1` 또는 `0` |
| `machbase` | `appendData(table_name, types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | 활성 Append 세션으로 행을 추가합니다. 2.0에서는 `appendOpen()` 시 메타데이터 기반으로 열 타입이 준비된 경우 `types`를 생략하고 행을 두 번째 인자로 바로 전달할 수 있습니다. | `1` 또는 `0` |
| `machbase` | `appendDataByTime(table_name, types, values=None, format='YYYY-MM-DD HH24:MI:SS', times=None, on_ack=None)` | 명시적 타임스탬프로 행을 추가합니다. 위 항목과 동일하게 타입 생략이 가능합니다. | `1` 또는 `0` |
| `machbase` | `appendFlush()` | 버퍼링된 Append 데이터를 디스크에 플러시합니다. | `1` 또는 `0` |
| `machbase` | `appendClose()` | Append 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `append(table_name, aTypes, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | 열기·추가·닫기를 한 번에 처리하는 편의 함수입니다. 2.0에서는 `aTypes`를 생략하고 `aValues`를 두 번째 인자로 바로 전달할 수 있습니다. | `1` 또는 `0` |
| `machbase` | `appendByTime(table_name, aTypes, aValues=None, format='YYYY-MM-DD HH24:MI:SS', times=None)` | 타임스탬프 인지 Append를 위한 편의 함수입니다. 2.0에서는 `aTypes`를 생략하고 `aValues`를 두 번째 인자로 바로 전달할 수 있습니다. | `1` 또는 `0` |

## DB-API 스타일 API (2.0)

| API | 설명 | 반환 |
| -- | -- | -- |
| `connect(host, port, user, password, ...)` | DB-API 연결 생성 | `MachbaseConnection` |
| `cursor(dictionary=True)` | 커서 생성 (`True`: dict, `False`: tuple) | `MachbaseCursor` |
| `cursor.execute(sql, params=None)` | SQL 실행 | `cursor` |
| `cursor.fetchone()` | 한 건 조회 | `tuple | dict | None` |
| `cursor.fetchmany(size)` | 최대 `size`건 조회 | `list` |
| `cursor.fetchall()` | 전체 조회 | `list` |
| `cursor.close()` | 커서 종료 | `None` |
| `cursor.rowcount` | 영향 행 수 | `int` |

## 2.0 타입 리스트 생략 append (권장)

`append()`와 `appendByTime()`는 타입 리스트를 생략하고 호출할 수 있습니다.  
두 번째 인자로 행 집합을 그대로 전달하면 서버 메타데이터 기반으로 처리합니다.

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

## API 참고 및 샘플 (레거시 1.x 기준)

아래 예제는 기존 레거시 버전 기준 정리입니다. 2.0 순수 Python에서는 `getSessionId()`, `count()`, `checkBit()`와 같은 API가 제공되지 않습니다. 필요 시 2.0 DB-API 예제를 참고하세요.

각 스크립트에서 호스트·포트·계정 정보를 환경에 맞게 수정하세요. 모든 예제는 독립 실행이 가능하며 `python3 script.py` 형태로 실행할 수 있습니다.

### 연결 관리

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

### DML과 결과 버퍼

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

### 스트리밍 SELECT 도우미

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

### 스키마 도우미

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

### 메타데이터와 통계

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

### Append 프로토콜 기본기

`appendOpen()`, `appendData()`, `appendFlush()`, `appendClose()`를 조합하면 행을 효율적으로 스트리밍할 수 있습니다. 아래 예제는 `columns()` 결과에서 컬럼 타입 코드를 추출한 뒤 데이터를 적재합니다.

```python
#!/usr/bin/env python3
import json
import re
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

        if db.columns('PY_APPEND_DEMO') == 0:
            raise SystemExit(db.result())
        column_payload = db.result()
        col_specs = [json.loads(item) for item in re.findall(r'\{[^}]+\}', column_payload)]
        types = [spec.get('type') for spec in col_specs]
        print('append column types:', types)

        if db.appendOpen('PY_APPEND_DEMO', types) == 0:
            raise SystemExit(db.result())

        rows = [
            ['2024-01-01 09:00:00', 'sensor-a', 21.5],
            ['2024-01-01 09:05:00', 'sensor-b', 22.1],
        ]
        if db.appendData('PY_APPEND_DEMO', types, rows) == 0:
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

### Append 편의 함수

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

        types = ['6', '5', '20']
        values = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', types, values) == 0:
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

        types = ['6', '5', '20']
        rows = [
            ['2024-01-01 11:00:00', 'node-2', 40.1],
            ['2024-01-01 11:01:00', 'node-2', 40.7],
        ]
        epoch_times = [1704106800, 1704106860]

        if db.appendOpen('PY_APPEND_TIME', types) == 0:
            raise SystemExit(db.result())
        if db.appendDataByTime('PY_APPEND_TIME', types, rows, 'YYYY-MM-DD HH24:MI:SS', epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendDataByTime result:', db.result())
        db.appendClose()

        if db.appendByTime('PY_APPEND_TIME', types, rows, 'YYYY-MM-DD HH24:MI:SS', epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendByTime result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 진단 도우미

#### machbase.checkBit()

`checkBit()`는 기존 native 기반 버전에 있던 포인터 폭 확인용 API로, 2.0 순수 Python 패키지에서는 더 이상 제공되지 않습니다.

### 저수준 바인딩

2.0 순수 Python 패키지에서는 `get_library_path()`, `openDB()`, `execAppend*()` 또는 포인터 유틸리티 API(예: `getlAddr`, `getrAddr`)와 같은 저수준 ctypes 인터페이스를 제공하지 않습니다.
기존 C 레이어 직접 접근이 필요한 경우에는 2.0 이전 버전을 사용하세요.
