---
type: docs
title: '시간축 모델링'
weight: 10
---

시간을 기준 축으로 하는 데이터 모델링 패턴입니다. 센서 계측값, 에너지 모니터링, 환경 데이터 등에 적용합니다.

## 기본 패턴: TAG 테이블

```sql
CREATE TAG TABLE power_meter (
    meter_id  VARCHAR(32) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
) METADATA (
    location  VARCHAR(64),
    phase     SHORT,
    rating_kw DOUBLE
);
```

## 시간 범위 집계

```sql
-- 1시간 단위 평균 전력 (최근 24시간)
SELECT meter_id,
       DATE_TRUNC('hour', time, 1) AS hour,
       AVG(kwh) AS avg_kwh,
       MAX(kwh) AS peak_kwh
FROM power_meter
WHERE time >= NOW - 86400000000000
GROUP BY meter_id, hour
ORDER BY meter_id, hour;
```

## 다중 해상도 저장 패턴

원시 데이터(고해상도)와 집계 데이터(저해상도)를 별도 테이블에 저장합니다.

```sql
-- 원시 데이터 (초 단위)
CREATE TAG TABLE power_raw (
    meter_id VARCHAR(32) PRIMARY KEY,
    time     DATETIME    BASETIME,
    kwh      DOUBLE
);

-- 1분 집계 (VOLATILE 또는 별도 TAG로 캐싱)
CREATE VOLATILE TABLE power_1min (
    key_id   VARCHAR(80) PRIMARY KEY,
    meter_id VARCHAR(32),
    ts       DATETIME,
    avg_kwh  DOUBLE,
    max_kwh  DOUBLE
);
```

## 시간대 처리

Machbase는 UTC 기준으로 시각을 저장합니다. 표시 시 타임존 변환을 적용합니다.

```sql
-- UTC → KST 변환 (UTC+9)
SELECT meter_id,
       time + 32400000000000 AS time_kst,
       kwh
FROM power_meter
WHERE meter_id = 'MTR-001'
  AND time >= '2024-01-01 00:00:00';
```
