---
type: docs
title: 'LOOKUP 테이블 JSON 조회'
weight: 10
---

LOOKUP 테이블의 컬럼을 JSON 타입으로 정의하면 센서 메타데이터나 설정 정보처럼 구조가 다양한 참조 데이터를 유연하게 저장할 수 있습니다.

## LOOKUP 테이블에 JSON 컬럼 정의

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id  VARCHAR(80) PRIMARY KEY,
    location   VARCHAR(200),
    config     JSON
);
```

## 데이터 삽입

```sql
INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'factory1',
    '{"threshold": {"high": 90.0, "low": 10.0}, "unit": "celsius", "interval_sec": 30}'
);

INSERT INTO sensor_config VALUES (
    'PRESS-01',
    'factory2',
    '{"threshold": {"high": 500.0, "low": 0.0}, "unit": "kPa", "interval_sec": 10}'
);
```

## JSON 필드 조회

```sql
-- 화살표 연산자로 특정 JSON 필드 조회
SELECT sensor_id, config->'$.unit' AS unit
FROM sensor_config;

-- 중첩 필드 조회
SELECT
    sensor_id,
    config->'$.threshold.high' AS high_limit,
    config->'$.threshold.low'  AS low_limit
FROM sensor_config
WHERE location = 'factory1';
```

## TAG 테이블과 JOIN하여 메타데이터 활용

LOOKUP 테이블의 JSON 설정 정보를 TAG 테이블 데이터와 결합하면 동적 임계값 필터링 등을 구현할 수 있습니다.

```sql
-- TAG 데이터와 LOOKUP JSON 메타데이터 JOIN
SELECT
    t.name,
    t.ts,
    t.value,
    c.config->'$.unit'            AS unit,
    c.config->'$.threshold.high'  AS high_limit
FROM tag t, sensor_config c
WHERE t.name = c.sensor_id
  AND t.ts >= DATEADD('h', -1, NOW);
```

### 임계값 초과 알람 조회

```sql
-- LOOKUP의 JSON 임계값과 실시간 값을 비교
SELECT
    t.name,
    t.ts,
    t.value,
    c.config->'$.threshold.high' AS high_limit
FROM tag t, sensor_config c
WHERE t.name = c.sensor_id
  AND t.ts >= DATEADD('m', -30, NOW)
  AND t.value > c.config->'$.threshold.high';
```

## JSON 필드 조건으로 필터링

```sql
-- 특정 단위를 사용하는 센서 목록 조회
SELECT sensor_id, location
FROM sensor_config
WHERE config->'$.unit' = 'celsius';

-- 폴링 간격이 30초 미만인 센서 조회
SELECT sensor_id, config->'$.interval_sec' AS interval
FROM sensor_config
WHERE config->'$.interval_sec' < 30;
```

## ISNOTNULL로 필드 존재 여부 확인

```sql
-- 특정 JSON 필드가 있는 행만 조회
SELECT sensor_id, config->'$.firmware_version' AS fw_ver
FROM sensor_config
WHERE config->'$.firmware_version' ISNOTNULL;
```

## 제한 사항

> LOOKUP 테이블의 JSON 필드에는 인덱스를 생성할 수 없습니다. JSON 필드 조건은 전체 스캔으로 처리됩니다. LOOKUP 테이블은 일반적으로 행 수가 적으므로 실용적인 성능을 제공하지만, 수십만 건 이상의 대용량 LOOKUP에는 주의가 필요합니다.

```sql
-- 권장: PRIMARY KEY 조건을 함께 사용하여 스캔 최소화
SELECT config->'$.threshold.high'
FROM sensor_config
WHERE sensor_id = 'TEMP-01';   -- PK 조건으로 단일 행 조회
```
