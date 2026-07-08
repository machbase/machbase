---
type: docs
title: 'JSON 타입의 테이블 타입별 지원 범위'
weight: 10
---

JSON 타입 컬럼을 각 테이블 타입에서 사용할 때의 지원 범위를 정리합니다.

## 지원 범위 요약

| 테이블 타입 | JSON 컬럼 생성 | JSON path query | JSON PK | 비고 |
|------------|:-------------:|:---------------:|:-------:|------|
| TAG | O | O | X | JSON 컬럼과 JSON 함수 지원, PK는 미지원 |
| LOG | O | O | X | 완전 지원 |
| LOOKUP | X | X | X | JSON 컬럼 생성 불가 |
| VOLATILE | X | X | X | JSON 컬럼 생성 불가 |
| RDB | O | O | X | 완전 지원 |

---

## TAG 테이블

TAG 테이블은 JSON 타입 컬럼을 지원합니다. JSON 컬럼은 일반 TAG 데이터 컬럼으로 사용할 수
있지만, TAGNAME/PRIMARY KEY 컬럼으로는 사용할 수 없습니다.

```sql
CREATE TAG TABLE tag_data (
    name   VARCHAR(100) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DOUBLE SUMMARIZED,
    data   JSON
);

INSERT INTO tag_data VALUES
    ('sensor-1', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 23.5,
     '{"device":"sensor-1","status":"ok"}');

SELECT JSON_EXTRACT_STRING(data, '$.status')
  FROM tag_data
 WHERE name = 'sensor-1';
```

---

## LOG 테이블

LOG 테이블은 JSON 타입을 완전히 지원합니다. JSON 컬럼 생성, `->` 연산자를 이용한 경로 접근, `JSON_SET`/`JSON_REMOVE` 등 모든 JSON 함수를 사용할 수 있습니다.

```sql
CREATE TABLE device_log (
    ts    DATETIME,
    data  JSON
);

-- 데이터 삽입
INSERT INTO device_log VALUES
    (NOW, '{"device":"sensor-1","temp":23.5,"status":"ok"}');

-- JSON 경로 접근
SELECT ts, data -> 'temp' AS temperature
  FROM device_log
 WHERE (data -> 'status') = 'ok';

-- JSON 값 수정 후 다시 삽입
SELECT JSON_SET(data, '$.status', 'error') FROM device_log;
```

---

## LOOKUP 테이블

LOOKUP 테이블은 JSON 타입 컬럼 생성을 지원하지 않습니다.

```sql
CREATE TABLE config_lookup (
    key    VARCHAR(64) PRIMARY KEY,
    config JSON
) TABLE_TYPE=LOOKUP;
-- 오류: JSON 타입은 VOLATILE / LOOKUP 테이블에서 사용할 수 없음
```

---

## VOLATILE 테이블

VOLATILE 테이블은 JSON 타입 컬럼 생성을 지원하지 않습니다.

```sql
CREATE VOLATILE TABLE session_data (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
-- 오류: JSON 타입은 VOLATILE / LOOKUP 테이블에서 사용할 수 없음
```

---

## RDB 테이블

RDB 테이블은 JSON 타입을 완전히 지원합니다. 관계형 특성(트랜잭션, 인덱스 등)과 JSON 경로 접근을 함께 사용할 수 있습니다.

```sql
CREATE RDB TABLE metadata (
    id   INTEGER PRIMARY KEY,
    info JSON
);

INSERT INTO metadata VALUES (1, '{"category":"A","tags":["iot","sensor"]}');

SELECT id, info -> 'category' AS category
  FROM metadata
 WHERE id = 1;

-- JSON 값 갱신
UPDATE metadata
   SET info = JSON_SET(info, '$.category', 'B')
 WHERE id = 1;
```

---

## JSON 관련 함수 테이블 타입별 지원

| 함수/연산자 | TAG | LOG | LOOKUP | VOLATILE | RDB |
|-------------|:---:|:---:|:------:|:--------:|:---:|
| `->` 연산자 | O | O | X | X | O |
| `JSON_EXTRACT*` | O | O | X | X | O |
| `JSON_TYPEOF` | O | O | X | X | O |
| `JSON_IS_VALID` | O | O | O | O | O |
| `JSON_SET` | O | O | X | X | O |
| `JSON_SET_JSON` | O | O | X | X | O |
| `JSON_REMOVE` | O | O | X | X | O |
