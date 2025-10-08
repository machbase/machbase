---
title : Python (KR)
type : docs
weight: 30
---

## 개요

Machbase는 데이터베이스에서 배포되는 네이티브 CLI 클라이언트를 감싼 CPython 확장 모듈 `machbaseAPI`를 제공합니다. 패키지는 다음 두 클래스를 노출합니다.

- `machbaseAPI.machbaseAPI`: 네이티브 공유 라이브러리에 대한 얇은 ctypes 바인딩.
- `machbaseAPI.machbase`: 연결 관리, SQL 실행, 메타데이터 조회, Append 프로토콜 헬퍼를 제공하는 상위 레벨 헬퍼.

이 문서의 예제는 애플리케이션 개발자의 진입점인 `machbase` 클래스를 기준으로 설명합니다.

## 설치

### 요구 사항

- `pip`이 포함된 Python 3.8 이상.
- 접근 가능한 Machbase 서버와 자격 증명(기본값은 포트 `5656`의 `SYS/MANAGER`).
- 휠 패키지에 포함된 Machbase 공유 라이브러리(또는 소스 설치 시 번들된 라이브러리).

### PyPI에서 설치

```bash
pip3 install machbaseAPI
```

`pip3`가 PATH에 없다면 `python3 -m pip install machbaseAPI`를 사용하세요.

### 모듈 확인

```bash
python3 - <<'PY'
from machbaseAPI.machbaseAPI import machbase
print('machbaseAPI import ok')
cli = machbase()
print('isConnected():', cli.isConnected())
PY
```

정상적으로 실행되면 모듈 임포트와 인스턴스 생성을 확인할 수 있습니다.

## 빠른 시작

아래 스니펫은 로컬 서버에 연결하고, 샘플 테이블을 생성하고, 데이터를 삽입한 뒤 조회 후 세션을 종료합니다.

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

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

        print('rows available:', db.count())
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

대부분의 `machbase` 메서드는 성공 시 `1`, 실패 시 `0`을 반환합니다. 호출 직후 `db.result()`를 사용해 서버가 전달한 JSON 형식 페이로드를 읽어야 합니다. `db.count()`는 현재 결과 집합에 버퍼링된 행 개수를 알려줍니다. `select()` 후에는 `db.fetch()`를 반환값 `(0, '')`가 나올 때까지 반복 호출하고, 이후 `db.selectClose()`로 리소스를 해제합니다.

## 지원 API 매트릭스

| 클래스 | API | 설명 | 반환 |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | 기본 자격 증명과 포트로 Machbase 서버에 연결합니다. | 성공 시 `1`, 실패 시 `0` |
| `machbase` | `openEx(host, user, password, port, conn_str)` | 추가 연결 문자열 속성을 지정해 확장 연결을 수행합니다. | `1` 또는 `0` |
| `machbase` | `close()` | 현재 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `isOpened()` | 핸들이 열려 있는지 확인합니다. | `1` 또는 `0` |
| `machbase` | `isConnected()` | 서버 연결 상태를 확인합니다. | `1` 또는 `0` |
| `machbase` | `getSessionId()` | 서버가 부여한 세션 식별자를 반환합니다. | 세션 ID 정수 |
| `machbase` | `execute(sql, type=0)` | `UPDATE`를 제외한 SQL 문을 실행합니다. | `1` 또는 `0` |
| `machbase` | `schema(sql)` | 스키마 관련 문장을 실행합니다. | `1` 또는 `0` |
| `machbase` | `tables()` | 모든 테이블 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `columns(table_name)` | 특정 테이블의 컬럼 정보를 조회합니다. | `1` 또는 `0` |
| `machbase` | `column(table_name)` | 로우 레벨 카탈로그 호출을 통해 컬럼 레이아웃을 가져옵니다. | `1` 또는 `0` |
| `machbase` | `statistics(table_name, user='SYS')` | 테이블 통계를 요청합니다. | `1` 또는 `0` |
| `machbase` | `select(sql)` | `SELECT` 또는 `DESC` 문을 스트리밍 방식으로 실행합니다. | `1` 또는 `0` |
| `machbase` | `fetch()` | `select()` 이후 다음 행을 가져옵니다. | `(rc, json_str)` |
| `machbase` | `selectClose()` | 열린 결과 집합 커서를 닫습니다. | `1` 또는 `0` |
| `machbase` | `result()` | 최신 JSON 페이로드를 반환합니다. | JSON 문자열 |
| `machbase` | `count()` | 현재 버퍼에 있는 행 수를 반환합니다. | 정수 |
| `machbase` | `checkBit()` | 포인터 폭(32 또는 64비트)을 보고합니다. | `32` 또는 `64` |
| `machbase` | `appendOpen(table_name, types)` | 컬럼 타입 코드를 사용해 Append 프로토콜을 시작합니다. | `1` 또는 `0` |
| `machbase` | `appendData(table_name, types, values, format)` | 활성화된 Append 세션으로 행을 추가합니다. | `1` 또는 `0` |
| `machbase` | `appendDataByTime(table_name, types, values, format, times)` | 에포크 타임스탬프를 명시해 행을 추가합니다. | `1` 또는 `0` |
| `machbase` | `appendFlush()` | Append 버퍼를 디스크로 플러시합니다. | `1` 또는 `0` |
| `machbase` | `appendClose()` | Append 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `append(table_name, types, values, format)` | Open → Append → Close를 한번에 수행하는 편의 함수입니다. | `1` 또는 `0` |
| `machbase` | `appendByTime(table_name, types, values, format, times)` | 타임스탬프 기반 Append 편의 함수입니다. | `1` 또는 `0` |
| `machbaseAPI` | `get_library_path()` | 번들된 네이티브 클라이언트의 경로를 확인합니다. | 문자열 경로 |
| `machbaseAPI` | `machbaseAPI.openDB(...)` | 로우 레벨 연결 함수(`machbase.open`과 동일). | 포인터 또는 `None` |
| `machbaseAPI` | `machbaseAPI.openDBEx(...)` | 로우 레벨 확장 연결 함수. | 포인터 또는 `None` |
| `machbaseAPI` | `machbaseAPI.closeDB(handle)` | 로우 핸들을 닫습니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execDirect(handle, sql)` | 분류 없이 SQL을 실행합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execSelect(handle, sql, type)` | SQL을 실행하고 결과 버퍼를 준비합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execSchema(handle, sql)` | 스키마 문장을 실행합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execStatistics(handle, table, user)` | 테이블 통계를 요청합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execAppendOpen(...)` | Append 프로토콜을 시작합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execAppendData(...)` | Append 데이터 행을 전달합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execAppendDataByTime(...)` | 타임스탬프와 함께 Append를 실행합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execAppendFlush(handle)` | Append 버퍼를 플러시합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.execAppendClose(handle)` | Append 세션을 종료합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.getColumns(handle, table)` | 컬럼 메타데이터를 조회합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.getIsConnected(handle)` | 연결 상태 플래그를 확인합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.getDataCount(handle)` | 버퍼링된 행 수를 반환합니다. | 부호 없는 정수 |
| `machbaseAPI` | `machbaseAPI.getData(handle)` | JSON 버퍼 포인터를 반환합니다. | `ctypes.c_char_p` |
| `machbaseAPI` | `machbaseAPI.getlAddr(handle)` | 결과 포인터의 하위 워드를 반환합니다(64비트). | 정수 |
| `machbaseAPI` | `machbaseAPI.getrAddr(handle)` | 결과 포인터의 상위 워드를 반환합니다(64비트). | 정수 |
| `machbaseAPI` | `machbaseAPI.getSessionId(handle)` | 서버 세션 ID를 반환합니다. | 부호 없는 정수 |
| `machbaseAPI` | `machbaseAPI.fetchRow(handle)` | 결과 집합 커서를 전진합니다. | 정수 상태값 |
| `machbaseAPI` | `machbaseAPI.selectClose(handle)` | select 커서를 닫습니다. | 정수 상태값 |

## API 참조 및 샘플

필요에 따라 호스트, 포트, 사용자 이름, 암호 값을 조정하세요. 모든 스니펫은 독립 실행 가능하며 `python3 script.py` 형태로 실행할 수 있습니다.

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

### 스트리밍 SELECT 헬퍼

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

### 스키마 헬퍼

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

`appendOpen()`, `appendData()`, `appendFlush()`, `appendClose()`는 행을 효율적으로 스트리밍합니다. 아래 예시는 `columns()` 결과로부터 컬럼 타입 코드를 추출한 뒤 데이터를 적재합니다.

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

### 진단 도구

#### machbase.checkBit()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    print('client pointer width:', db.checkBit())

if __name__ == '__main__':
    main()
```

### 로우 레벨 바인딩

하위 레벨 `machbaseAPI` 클래스는 원시 ctypes 바인딩과 `get_library_path()` 헬퍼를 제공합니다.

```python
#!/usr/bin/env python3
from machbaseAPI import machbaseAPI
from machbaseAPI.machbaseAPI import get_library_path

def main():
    print('native library path:', get_library_path())
    api = machbaseAPI.machbaseAPI()
    print('openDB argtypes:', api.clib.openDB.argtypes)

if __name__ == '__main__':
    main()
```

일상적인 데이터베이스 작업은 `machbase` 헬퍼가 대부분을 처리하므로, C 레이어에 직접 접근해야 할 때만 로우 레벨 인터페이스를 사용하세요.
