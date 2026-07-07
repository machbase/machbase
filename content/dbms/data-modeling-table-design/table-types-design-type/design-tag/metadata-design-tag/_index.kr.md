---
type: docs
title: 'METADATA 설계'
weight: 40
---

TAG 테이블은 `METADATA` 절을 사용하여 태그(센서)의 속성 정보를 함께 저장할 수 있습니다. METADATA 컬럼은 태그 이름(`PRIMARY KEY`) 기준으로 관리되며, LOOKUP 테이블처럼 UPDATE/DELETE가 가능합니다.

## METADATA 절 문법

```sql
CREATE TAG TABLE sensor_meta_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
) METADATA (
    location  VARCHAR(128),
    unit      VARCHAR(16),
    threshold DOUBLE
);
```

## METADATA 조회

```sql
-- 태그와 메타데이터 함께 조회
SELECT name, time, value, location, unit
FROM sensor_meta_data
WHERE name = 'sensor-01'
  AND time >= NOW - 3600000000000;

-- 메타데이터 조건으로 필터링
SELECT name, time, value
FROM sensor_meta_data
WHERE location = 'Building-A'
  AND time >= NOW - 86400000000000;
```

## METADATA 업데이트

```sql
-- 메타데이터 변경 (태그 속성 갱신)
UPDATE sensor_meta_data METADATA SET unit = 'Celsius' WHERE name = 'sensor-01';
UPDATE sensor_meta_data METADATA SET threshold = 80.0 WHERE location = 'Building-A';
```

## METADATA 삽입

```sql
-- 태그 데이터 삽입 시 메타데이터 함께 지정
INSERT INTO sensor_meta_data (name, time, value, location, unit, threshold)
VALUES ('sensor-01', NOW, 23.5, 'Building-A', 'Celsius', 80.0);

-- 또는 메타데이터 별도 삽입
INSERT INTO sensor_meta_data METADATA (name, location, unit, threshold)
VALUES ('sensor-02', 'Building-B', 'Celsius', 75.0);
```

## 설계 지침

- METADATA 컬럼에는 자주 변경되지 않는 태그 속성(위치, 단위, 임계값 등)을 저장합니다.
- 계측값(시간에 따라 변하는 값)은 반드시 일반 컬럼에 저장합니다.
- METADATA 컬럼 수는 10개 내외로 유지하는 것이 권장됩니다.
