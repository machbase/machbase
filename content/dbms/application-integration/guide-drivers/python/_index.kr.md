---
type: docs
title: '11.3.3 Python'
weight: 30
---

## 개요

`machbaseapi` 패키지는 Machbase 서버에 연결하기 위한 순수 Python 구현 드라이버입니다. 네이티브 `.so`/`.dll` 파일이 필요 없으며, DB-API 2.0 스타일과 레거시 스타일 두 가지 인터페이스를 모두 제공합니다.

- PyPI 패키지명: `machbaseapi`
- Python 3.6 이상 필요
- 네이티브 라이브러리 의존성 없음
- DB-API 2.0 방식: `connect()`, `cursor()` 지원
- Append 프로토콜 지원 (대량 고속 적재)

## 설치

```bash
pip3 install machbaseapi
```

`pip3`가 PATH에 없다면 다음 명령을 사용합니다.

```bash
python3 -m pip install machbaseapi
```

### 설치 확인

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase 클래스 import:', bool(machbase))
print('connect 함수 존재:', callable(connect))
PY
```

## 빠른 시작

### DB-API 방식 (권장)

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

# 테이블 생성
cur.execute('''
    CREATE TABLE IF NOT EXISTS py_sensor (
        ts DATETIME,
        device VARCHAR(40),
        value DOUBLE
    )
''')

# 데이터 삽입
cur.execute("INSERT INTO py_sensor VALUES (NOW, 'sensor-1', 23.5)")
cur.execute("INSERT INTO py_sensor VALUES (NOW, 'sensor-2', 24.1)")

# 데이터 조회
cur.execute("SELECT to_char(ts,'YYYY-MM-DD HH24:MI:SS') as ts, device, value FROM py_sensor ORDER BY ts")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()
```

### 레거시 방식 (machbase 클래스)

```python
#!/usr/bin/env python3
import json
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    # 테이블 생성
    db.execute('DROP TABLE py_quick')
    db.result()  # 테이블이 없어도 다음 CREATE를 계속 진행
    db.execute('CREATE TABLE py_quick(ts DATETIME, device VARCHAR(40), value DOUBLE)')

    # 데이터 삽입
    for i in range(3):
        sql = (
            f"INSERT INTO py_quick VALUES ("
            f"to_date('2024-01-0{i+1}', 'YYYY-MM-DD'),"
            f"'sensor-{i}',"
            f"{20.5 + i})"
        )
        if db.execute(sql) == 0:
            raise SystemExit(db.result())

    # 데이터 조회 (스트리밍 방식)
    if db.select('SELECT * FROM py_quick ORDER BY ts') == 0:
        raise SystemExit(db.result())

    while True:
        rc, payload = db.fetch()
        if rc == 0:
            break
        print(json.loads(payload))

    db.selectClose()
finally:
    db.close()
```

## 연결 관리

### DB-API connect()

```python
from machbaseAPI import connect

# 기본 연결
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# 추가 연결 문자열 속성 지정
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER',
               conn_str='APP_NAME=my-python-app')
```

### machbase 클래스 open() / openEx()

```python
from machbaseAPI import machbase

db = machbase()

# 기본 연결
rc = db.open('127.0.0.1', 'SYS', 'MANAGER', 5656)

# 확장 연결 (추가 속성 지정)
rc = db.openEx('127.0.0.1', 'SYS', 'MANAGER', 5656, 'APP_NAME=my-app')

# 연결 상태 확인
print('isOpened:', db.isOpened())
print('isConnected:', db.isConnected())

db.close()
```

## 지원 API

### DB-API 스타일

| API | 설명 |
|-----|------|
| `connect(**kwargs)` | 연결 생성. `host`, `port`, `user`, `password` 키워드 인자 사용 |
| `cursor(dictionary=True)` | 커서 생성. `True`이면 딕셔너리, `False`이면 튜플 반환 |
| `cursor.execute(sql, params=None)` | SQL 실행 |
| `cursor.fetchone()` | 결과 한 행 조회 |
| `cursor.fetchmany(size)` | 최대 `size`건 조회 |
| `cursor.fetchall()` | 전체 결과 조회 |
| `cursor.rowcount` | 영향받은 행 수 |
| `cursor.close()` | 커서 닫기 |
| `connection.append(table, rows, types=None, times=None)` | Append 프로토콜로 행 추가 |

### machbase 클래스 스타일

| API | 반환 | 설명 |
|-----|------|------|
| `open(host, user, password, port)` | `1`/`0` | 서버 연결 |
| `openEx(host, user, password, port, conn_str)` | `1`/`0` | 확장 연결 |
| `close()` | `1`/`0` | 세션 종료 |
| `isOpened()` | `1`/`0` | 핸들 열림 여부 확인 |
| `isConnected()` | `1`/`0` | 연결 상태 확인 |
| `execute(sql)` | `1`/`0` | SQL 직접 실행 |
| `select(sql)` | `1`/`0` | 스트리밍 SELECT 실행 |
| `fetch()` | `(rc, json_str)` | 다음 행 조회 |
| `selectClose()` | `1`/`0` | 결과 커서 닫기 |
| `result()` | JSON 문자열 | 최신 결과 페이로드 반환 |
| `tables()` | `1`/`0` | 모든 테이블 메타데이터 조회 |
| `columns(table_name)` | `1`/`0` | 테이블 컬럼 메타데이터 조회 |
| `appendOpen(table_name)` | `1`/`0` | Append 세션 시작 |
| `appendData(table_name, rows)` | `1`/`0` | Append 행 전송 |
| `appendFlush()` | `1`/`0` | Pending 응답 동기화 |
| `appendClose()` | `1`/`0` | Append 세션 종료 |
| `append(table_name, rows)` | `1`/`0` | 열기·추가·닫기 한 번에 처리 |

## cursor 사용법

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# 딕셔너리 커서 (기본)
cur = conn.cursor()
cur.execute('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT 5')
for row in cur.fetchall():
    print(row['NAME'])

# 튜플 커서
cur_tuple = conn.cursor(dictionary=False)
cur_tuple.execute('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT 5')
for row in cur_tuple.fetchall():
    print(row[0])

# fetchone / fetchmany
cur.execute('SELECT NAME FROM V$TABLES ORDER BY NAME')
first = cur.fetchone()
print('first:', first)
batch = cur.fetchmany(3)
print('batch:', batch)

cur.close()
conn.close()
```

## 에러 처리

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('SELECT * FROM non_existent_table')
except Exception as e:
    print('Query error:', e)
finally:
    cur.close()
    conn.close()
```

레거시 방식에서는 반환 코드로 성공 여부를 판별합니다.

```python
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    print('Connection failed:', db.result())
    raise SystemExit(1)

if db.execute('SELECT * FROM non_existent_table') == 0:
    print('Execute failed:', db.result())

db.close()
```

## Append 프로토콜

Append는 대량 데이터를 고속으로 적재할 때 사용합니다. `INSERT`보다 훨씬 빠른 성능을 제공합니다.

### DB-API append()

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('DROP TABLE py_append_demo')
except Exception:
    pass
cur.execute('CREATE TABLE py_append_demo(ts DATETIME, device VARCHAR(32), value DOUBLE)')

rows = [
    ['2024-01-01 09:00:00', 'sensor-a', 21.5],
    ['2024-01-01 09:01:00', 'sensor-b', 22.1],
    ['2024-01-01 09:02:00', 'sensor-a', 21.8],
]

appended = conn.append('PY_APPEND_DEMO', rows)
print(f'Appended {appended} rows.')

cur.execute('SELECT COUNT(*) as cnt FROM py_append_demo')
print('Count:', cur.fetchone())

cur.close()
conn.close()
```

### Append 행 길이와 기본값

Append 입력 행은 테이블 컬럼 수와 같은 개수의 값을 가져야 합니다. 마지막 컬럼도
생략하지 말고 명시적으로 값을 전달합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('DROP TABLE py_append_defaults')
except Exception:
    pass
cur.execute(
    'CREATE TABLE py_append_defaults('
    '  ts DATETIME, name VARCHAR(20), value DOUBLE, note VARCHAR(40))'
)

# 모든 행은 4개 컬럼 값을 전달합니다.
conn.append('PY_APPEND_DEFAULTS', [
    ['2024-01-01 10:00:00', 'sensor-1', 12.3, 'auto'],
    ['2024-01-01 10:00:01', 'sensor-2', 13.4, 'manual'],
])

cur.execute('SELECT ts, name, value, note FROM py_append_defaults ORDER BY ts')
print(cur.fetchall())

cur.close()
conn.close()
```

Append에서 컬럼을 생략하면 `Append row length does not match append metadata` 오류가
발생합니다. NULL 입력이 필요한 경우에는 `INSERT`와 파라미터 바인딩을 사용하고,
컬럼 타입별 조회 표현을 확인합니다.

### 레거시 방식 Append

```python
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    db.execute('DROP TABLE py_legacy_append')
    db.result()
    db.execute('CREATE TABLE py_legacy_append(ts DATETIME, tag VARCHAR(16), reading DOUBLE)')

    # appendOpen → appendData → appendFlush → appendClose
    if db.appendOpen('PY_LEGACY_APPEND') == 0:
        raise SystemExit(db.result())

    rows = [
        ['2024-01-01 09:00:00', 'node-1', 30.0],
        ['2024-01-01 09:05:00', 'node-1', 30.5],
    ]
    if db.appendData('PY_LEGACY_APPEND', rows) == 0:
        raise SystemExit(db.result())

    db.appendFlush()
    db.appendClose()

    # 편의 함수: append() - 열기/추가/닫기 한 번에 처리
    more_rows = [
        ['2024-01-01 10:00:00', 'node-2', 40.1],
        ['2024-01-01 10:05:00', 'node-2', 40.7],
    ]
    if db.append('PY_LEGACY_APPEND', more_rows) == 0:
        raise SystemExit(db.result())

    print('Append done.')
finally:
    db.close()
```

### appendByTime() - LOG 테이블 arrival time 지정

```python
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    db.execute('DROP TABLE py_append_time')
    db.result()
    db.execute('CREATE LOG TABLE py_append_time(tag VARCHAR(16), reading DOUBLE)')

    rows = [
        ['node-2', 40.1],
        ['node-2', 40.7],
    ]
    epoch_times = [
        1704106800_000_000_000,
        1704106860_000_000_000,
    ]  # Unix epoch (나노초 단위)

    if db.appendByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
        raise SystemExit(db.result())
    print('appendByTime result:', db.result())
finally:
    db.close()
```

`aTimes`는 LOG 테이블의 `_ARRIVAL_TIME` 값으로 사용됩니다. 일반 컬럼에 저장할
시각 값은 행 데이터에 직접 포함합니다.

## TAG 테이블 Append

TAG 테이블 Append도 테이블 정의의 컬럼 순서에 맞춰 값을 전달해야 합니다. 추가 컬럼과
메타데이터 컬럼을 정의했다면 해당 값도 행 배열에 포함합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('DROP TABLE py_tag_demo')
except Exception:
    pass
cur.execute('''
    CREATE TAG TABLE py_tag_demo (
        name VARCHAR(40) PRIMARY KEY,
        time DATETIME BASETIME,
        value DOUBLE SUMMARIZED,
        status VARCHAR(20)
    ) METADATA (
        site VARCHAR(20),
        line INTEGER
    )
''')

# name, time, value, status, site, line 순서로 값을 전달
conn.append('PY_TAG_DEMO', [
    ['tag-1', '2024-01-01 10:00:00', 12.3, 'ok', 'seoul', 1],
    ['tag-2', '2024-01-01 10:01:00', 13.7, 'ok', 'busan', 2],
])

cur.execute('SELECT name, time, value, status FROM py_tag_demo ORDER BY time')
print(cur.fetchall())

cur.close()
conn.close()
```

## 스트리밍 SELECT (레거시)

대용량 결과를 처리할 때 `select()` + `fetch()` 방식으로 행을 스트리밍합니다.

```python
import json
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    if db.select('SELECT NAME FROM V$TABLES ORDER BY NAME') == 0:
        raise SystemExit(db.result())

    count = 0
    while True:
        rc, payload = db.fetch()
        if rc == 0:
            break
        row = json.loads(payload)
        print(row)
        count += 1

    db.selectClose()
    print(f'Total: {count} rows')
finally:
    db.close()
```

## 주의 사항

- `machbase` 클래스 메서드는 성공 시 `1`, 실패 시 `0`을 반환합니다. 반드시 반환 코드를 확인하세요.
- 트랜잭션은 RDB 테이블 작업에서 사용합니다. LOG/TAG 테이블 Append성 입력은 롤백 대상이 아니므로 테이블 타입별 지원 범위를 확인합니다.
- Append 행은 테이블 컬럼 수와 순서를 맞춰야 합니다. 컬럼 생략은 지원하지 않습니다.
- 커넥션 풀 옵션(`pool_name`, `pool_size`)은 현재 미지원입니다.
- `getSessionId()`, `count()`, `checkBit()` 등 기존 네이티브 기반 API는 2.3 이상 순수 Python 패키지에서 제공되지 않습니다.
