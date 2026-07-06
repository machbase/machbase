---
type: docs
title: '고빈도 LOOKUP 조회'
weight: 10
---

## 문제

LOOKUP 테이블을 초고빈도 시계열 데이터 조회에 사용하는 패턴입니다. LOOKUP 테이블은 소규모 참조 데이터에 최적화되어 있으며, 대량 시계열 데이터의 고속 조회에는 부적합합니다.

## 안티패턴 예시

```sql
-- 잘못된 설계: 센서 계측값을 LOOKUP 테이블에 저장
CREATE LOOKUP TABLE sensor_data_wrong (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    ts         DATETIME
);

-- LOOKUP은 한 센서당 한 행만 저장 가능 (PK 중복 불가)
-- 시계열 이력 저장 불가
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.3, NOW);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.5, NOW);  -- PK 중복 오류
```

## 올바른 패턴

시계열 계측값은 TAG 테이블에 저장합니다. 최신 값만 필요하면 VOLATILE 테이블을 캐시로 사용합니다.

```sql
-- 올바른 설계: 이력은 TAG 테이블
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 최신값 캐시는 VOLATILE 테이블
CREATE VOLATILE TABLE sensor_latest (
    sensor_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE,
    updated_at DATETIME
);
```

## 결과

| | 안티패턴 (LOOKUP) | 올바른 설계 (TAG) |
|-|-----------------|-----------------|
| 이력 저장 | X (PK 중복 불가) | O |
| 고속 입력 | 느림 | 빠름 (Append API) |
| 시간 범위 조회 | 불가 | O |
