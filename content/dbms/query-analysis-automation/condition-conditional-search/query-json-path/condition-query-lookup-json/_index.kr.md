---
type: docs
title: 'LOOKUP 테이블 JSON 조회 제한'
weight: 10
---

현재 빌드에서는 LOOKUP 테이블에 `JSON` 타입 컬럼을 생성할 수 없습니다. 다음과 같이
`CREATE LOOKUP TABLE ... JSON`을 실행하면 오류가 발생합니다.

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id  VARCHAR(80) PRIMARY KEY,
    location   VARCHAR(200),
    config     JSON
);
-- [ERR-02173: Cannot create columns with data type (JSON) in VOLATILE / LOOKUP table.]
```

JSONPath 조건 조회가 필요하면 RDB 테이블이나 TAG 테이블의 JSON 컬럼을 사용합니다. LOOKUP
테이블은 참조 데이터를 빠르게 조회하는 용도로 사용하되, 구조화되지 않은 속성은 `VARCHAR` 문자열로
저장하거나 조회 조건으로 자주 쓰는 필드를 별도 컬럼으로 분리합니다.

## LOOKUP에서 JSON 문자열 저장

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id  VARCHAR(80) PRIMARY KEY,
    location   VARCHAR(200),
    config     VARCHAR(4096)
);
```

```sql
INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'factory1',
    '{"threshold": {"high": 90.0, "low": 10.0}, "unit": "celsius", "interval_sec": 30}'
);
```

문자열로 저장한 값에는 `config->'$.unit'` 같은 JSONPath 연산자를 적용할 수 없습니다.
애플리케이션에서 파싱하거나, 조건 검색이 필요한 값은 컬럼으로 분리합니다.

## 필드 분리 패턴

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id    VARCHAR(80) PRIMARY KEY,
    location     VARCHAR(200),
    unit         VARCHAR(20),
    high_limit   DOUBLE,
    low_limit    DOUBLE,
    interval_sec INTEGER,
    config_text  VARCHAR(4096)
);
```

```sql
SELECT
    t.name,
    t.time,
    t.value,
    c.unit,
    c.high_limit
FROM tag t, sensor_config c
WHERE t.name = c.sensor_id
  AND t.time >= NOW - 1800000000000
  AND t.value > c.high_limit;
```

## JSONPath가 필요한 경우

JSONPath 필드 조건과 화살표 연산자가 필요하면 RDB 테이블을 사용합니다.

```sql
CREATE RDB TABLE sensor_config_rdb (
    sensor_id  VARCHAR(80) PRIMARY KEY,
    location   VARCHAR(200),
    config     JSON
);
```

RDB 테이블에서는 `config->'$.unit'` 같은 JSONPath 조회와 조건식을 사용할 수 있습니다.

## 정리

- LOOKUP 테이블의 JSON 타입 컬럼은 현재 지원되지 않습니다.
- LOOKUP에 `VARCHAR` JSON 문자열을 저장할 수는 있지만 JSONPath 조건 조회 대상은 아닙니다.
- 조회 조건으로 쓰는 속성은 별도 컬럼으로 분리합니다.
- JSONPath 조회가 핵심이면 RDB 또는 TAG 테이블의 JSON 컬럼을 사용합니다.
