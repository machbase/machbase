---
title: 'Tag 메타데이터'
type: docs
weight: 20
---

## 개요

Tag 메타데이터는 태그의 정적 속성을 저장하는 영역입니다. 센서 위치, 장비 상태, 설치 정보, 외부 식별자, JSON 문서형 속성을 메타데이터에 둘 수 있습니다.

이번 기능으로 다음 작업을 `TAG METADATA` 문법으로 직접 처리할 수 있습니다.

- 메타데이터 전용 조회
- 메타데이터 조건 기반 `UPDATE` / `DELETE`
- `JSON` 타입 메타데이터 컬럼 선언
- JSON path 조회와 JSON path 인덱스
- JSON 문서 일부만 수정하는 부분 갱신

사용자는 내부 저장 테이블을 직접 다룰 필요 없이 `TAG METADATA` 문법만 사용하면 됩니다.

## 메타데이터 컬럼 정의

메타데이터 컬럼은 `CREATE TAGDATA TABLE` 의 `METADATA (...)` 절에서 정의합니다.

```sql
CREATE TAGDATA TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    location VARCHAR(100),
    status VARCHAR(20),
    srcip IPV4
);
```

메타데이터 컬럼은 태그 이름별로 1행만 저장됩니다.

## 메타데이터 입력

메타데이터는 `INSERT INTO ... METADATA` 로 입력합니다.

```sql
INSERT INTO sensors METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

컬럼 목록을 지정할 수도 있습니다.

```sql
INSERT INTO sensors METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```

주의사항:

- `VALUES (...)` 의 순서는 항상 `NAME` 다음에 메타데이터 정의 순서를 따릅니다.
- 지정하지 않은 메타데이터 컬럼은 `NULL` 로 저장됩니다.
- 메타데이터 행의 식별자는 항상 `NAME` 입니다.

## 메타데이터 조회

### 메타데이터만 조회

메타데이터 전용 조회는 `FROM TAG METADATA` 를 사용합니다.

```sql
SELECT name, location, status, srcip
  FROM sensors METADATA
 ORDER BY name;
```

이 조회는 태그 이름당 1행을 반환합니다.

```sql
SELECT *
  FROM sensors METADATA
 ORDER BY name;
```

`SELECT *` 와 `table_alias.*` 는 `NAME` 과 메타데이터 컬럼만 반환합니다.

### 데이터와 함께 조회

메타데이터 조건으로 시계열 데이터를 조회할 때는 일반 `FROM TAG` 를 사용합니다.

```sql
SELECT name, status, time, value
  FROM sensors
 WHERE status = 'READY'
 ORDER BY name, time;
```

이 조회는 데이터 row 기준으로 반환되므로, 같은 tag의 메타데이터 값은 각 데이터 row마다 반복됩니다.

주의사항:

- `FROM TAG METADATA` 에서는 `TIME`, `VALUE` 같은 데이터 컬럼을 조회할 수 없습니다.
- `FROM TAG` 는 데이터 조회 모드이고, `FROM TAG METADATA` 는 메타데이터 조회 모드입니다.
- `TAG METADATA` 에서는 내부 컬럼 `_ID`, `_RID` 를 사용할 수 없습니다.

## 메타데이터 수정

메타데이터 수정은 `UPDATE TAG METADATA` 를 사용합니다.

```sql
UPDATE sensors METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

메타데이터 조건으로 여러 태그를 한 번에 수정할 수도 있습니다.

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

주의사항:

- 수정 대상은 `NAME` 과 메타데이터 컬럼입니다.
- `TIME`, `VALUE` 같은 데이터 컬럼은 `UPDATE ... METADATA` 에서 수정할 수 없습니다.
- 내부 컬럼은 수정할 수 없습니다.

## 메타데이터 삭제

메타데이터 삭제는 `DELETE FROM TAG METADATA` 를 사용합니다.

```sql
DELETE FROM sensors METADATA
 WHERE name = 'TEMP_002';
```

메타데이터 조건으로 여러 태그를 한 번에 삭제할 수도 있습니다.

```sql
DELETE FROM sensors METADATA
 WHERE status = 'STOP';
```

주의사항:

- 삭제 대상 중 하나라도 실제 데이터 row를 가지고 있으면 문장 전체가 실패합니다.
- 즉, 사용 중인 tag의 메타데이터는 삭제할 수 없습니다.

## JSON 메타데이터 컬럼

메타데이터에 `JSON` 컬럼을 선언할 수 있습니다.

```sql
CREATE TAGDATA TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);
```

JSON 메타데이터 입력 예:

```sql
INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

주의사항:

- `JSON` 메타데이터 컬럼은 길이를 지정하지 않습니다.
- 유효하지 않은 JSON 문자열은 오류가 발생합니다.
- raw JSON 컬럼 자체에는 자동 인덱스가 생성되지 않습니다.

## JSON path 조회

JSON 메타데이터는 `->` 연산자로 조회할 수 있습니다.

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ships METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

데이터 조회에서도 같은 방식으로 사용할 수 있습니다.

```sql
SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

### 경로 표기 규칙

조회와 부분 갱신에서 사용하는 path는 full JSONPath를 사용합니다.

- 일반 key: `$.name`
- 중첩 key: `$.ship.status`
- key 이름에 `.` 또는 `-` 가 포함되면 bracket 표기 사용

```sql
SELECT info->'$[''ship.owner'']'
  FROM ships METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ships METADATA;
```

## JSON path 인덱스

### 테이블 생성 시 함께 선언

자주 조회하는 JSON path는 메타데이터 정의 시 함께 인덱싱할 수 있습니다.

```sql
CREATE TAGDATA TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
);
```

`INDEX(...)` 안의 문자열은 다음 규칙으로 해석합니다.

- `'name'` 은 `$.name`
- `'ship.status'` 는 `$.ship.status`
- 특수 문자가 있는 key나 복잡한 경로는 full JSONPath를 직접 사용

```sql
INFO JSON INDEX('$[''ship.owner'']')
```

### 생성 후 인덱스 추가

테이블 생성 후에도 JSON path 인덱스를 추가할 수 있습니다.

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

### 인덱스 삭제

인덱스 이름만으로 삭제합니다.

```sql
DROP INDEX idx_ship_owner;
```

생성 시 `INFO JSON INDEX(...)` 로 자동 생성된 인덱스 이름은 `SHOW INDEX` 로 확인하는 것이 가장 안전합니다.

```sql
SHOW INDEX idx_ship_owner;
```

### 인덱스 사용 시 주의사항

현재 JSON path 인덱스는 문자열 비교 중심으로 동작합니다.

```sql
SELECT name
  FROM ships METADATA
 WHERE info->'$.status' = 'READY';
```

문자열 literal 비교는 인덱스를 사용할 수 있습니다. 반면 숫자 literal 비교는 full scan으로 처리될 수 있습니다.

예:

- `info->'$.num' = '10'` : 인덱스 사용 가능
- `info->'$.num' = 10` : full scan 가능

## JSON 부분 갱신

JSON 메타데이터는 문서 전체를 다시 쓰지 않고 일부만 갱신할 수 있습니다.

### JSON_SET

SQL scalar 값을 JSON scalar로 저장합니다.

```sql
UPDATE ships METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

### JSON_SET_JSON

입력 문자열을 JSON으로 해석해 object 또는 array를 저장합니다.

```sql
UPDATE ships METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

### JSON_REMOVE

특정 멤버 또는 하위 경로를 삭제합니다.

```sql
UPDATE ships METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```

### 부분 갱신 규칙

- `JSON_SET(..., path, NULL)` 은 JSON `null` 을 저장합니다.
- `JSON_SET_JSON(..., path, NULL)` 의 결과는 SQL `NULL` 입니다.
- JSON 문서 인자가 `NULL` 이면 함수 결과는 SQL `NULL` 입니다.
- path 가 `NULL` 이거나 빈 문자열이면 오류가 발생합니다.
- 존재하지 않는 경로에 대한 `JSON_REMOVE` 는 오류가 아니라 no-op 입니다.
- `JSON_REMOVE(..., '$')` 는 허용되지 않습니다.
- 부분 갱신은 object 경로 중심으로 지원합니다.
- array element 경로 갱신 예: `$.items[0]` 는 지원하지 않습니다.

## 전체 예제

```sql
CREATE TAGDATA TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    srcip IPV4,
    info JSON INDEX('name', 'ship.status')
);

INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '192.168.0.11',
    '{"name":"alpha","ship":{"status":"READY"}}'
);

INSERT INTO ships VALUES ('SHIP_001', '2026-04-01 00:00:00', 10.5);

SELECT name, status, info
  FROM ships METADATA;

SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY';

CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');

UPDATE ships METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';

DROP INDEX idx_ship_owner;
```

## 요약

- 메타데이터 전용 조회는 `FROM TAG METADATA`
- 데이터 조회는 `FROM TAG`
- 메타데이터 수정/삭제는 `UPDATE/DELETE ... METADATA`
- JSON 메타데이터는 `INFO JSON`
- JSON path 인덱스는 `INFO JSON INDEX(...)` 또는 `CREATE INDEX ... ON TAG METADATA (...)`
- JSON 부분 갱신은 `JSON_SET`, `JSON_SET_JSON`, `JSON_REMOVE`
