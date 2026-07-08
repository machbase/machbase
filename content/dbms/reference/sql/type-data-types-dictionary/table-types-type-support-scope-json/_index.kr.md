---
type: docs
title: 'JSON 타입의 테이블 타입별 지원 범위 (LOOKUP planned: dbms-nfx#3696)'
weight: 10
---

JSON 타입 컬럼을 각 테이블 타입에서 사용할 때의 지원 범위를 정리합니다.

## 지원 범위 요약

| 테이블 타입 | JSON 컬럼 생성 | JSON path query | JSON PK | 비고 |
|------------|:-------------:|:---------------:|:-------:|------|
| TAG | X | X | X | JSON 미지원 |
| LOG | O | O | X | 완전 지원 |
| LOOKUP | O (일부) | 계획 중 | 계획 중 | dbms-nfx#3696 참고 |
| VOLATILE | O | O | X | 완전 지원 |
| RDB | O | O | X | 완전 지원 |

---

## TAG 테이블

TAG 테이블은 JSON 타입 컬럼을 지원하지 않습니다. TAG 테이블은 시계열 센서 값 저장에 최적화되어 있으며, 구조화된 수치 데이터 타입(SHORT, INTEGER, LONG, FLOAT, DOUBLE 등)을 사용해야 합니다.

```sql
-- TAG 테이블에 JSON 컬럼 추가 시 오류 발생
CREATE TAG TABLE tag_data (
    name   VARCHAR(100) PRIMARY KEY,
    time   DATETIME BASETIME,
    data   JSON   -- 오류: TAG 테이블에서 JSON 미지원
);
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

LOOKUP 테이블의 JSON 지원은 현재 일부만 제공됩니다.

- **JSON 컬럼 생성**: 지원 (단순 삽입/조회 가능)
- **JSON path query (`->` 연산자, `JSON_SET` 등)**: 계획 중 (dbms-nfx#3696)
- **JSON 컬럼을 Primary Key로 사용**: 계획 중

```sql
-- JSON 컬럼 생성은 가능
CREATE TABLE config_lookup (
    key    VARCHAR(64) PRIMARY KEY,
    config JSON
) TABLE_TYPE=LOOKUP;

-- 단순 삽입/조회는 가능
INSERT INTO config_lookup VALUES ('app1', '{"timeout":30,"retry":3}');
SELECT config FROM config_lookup WHERE key = 'app1';

-- JSON path query는 현재 미지원 (계획 중)
-- SELECT config -> 'timeout' FROM config_lookup;  -- 미지원
```

{{< callout type="info" >}}
LOOKUP 테이블의 JSON path query 기능은 **dbms-nfx#3696** 이슈에서 추적 중이며, 향후 버전에서 지원될 예정입니다.
{{< /callout >}}

---

## VOLATILE 테이블

VOLATILE 테이블은 JSON 타입을 완전히 지원합니다. 인메모리 임시 데이터 저장에 사용되며 서버 재시작 시 데이터가 소멸합니다.

```sql
CREATE VOLATILE TABLE session_data (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);

INSERT INTO session_data VALUES ('sess-001', '{"user":"admin","role":"superuser"}');

SELECT payload -> 'role' AS role
  FROM session_data
 WHERE session_id = 'sess-001';
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
| `->` 연산자 | X | O | 계획 중 | O | O |
| `JSON_SET` | X | O | 계획 중 | O | O |
| `JSON_SET_JSON` | X | O | 계획 중 | O | O |
| `JSON_REMOVE` | X | O | 계획 중 | O | O |
