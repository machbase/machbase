---
type: docs
title: '영속·임시 혼합 패턴'
weight: 60
---

영속 테이블(TAG, LOG, RDB, LOOKUP)과 임시 테이블(VOLATILE)을 조합하여 성능과 데이터 무결성을 동시에 달성하는 패턴입니다.

## 원본 + 집계 캐시 패턴

원본 데이터는 영속 테이블에, 집계 결과는 VOLATILE 테이블에 저장합니다.

```sql
-- 원본 데이터 (TAG, 영속)
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 집계 캐시 (VOLATILE, 임시)
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       INTEGER
);
```

## 캐시 갱신 패턴

```sql
-- 주기적 집계 갱신 (1시간마다 실행)
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name AS key_id,
       name,
       MAX(DATE_TRUNC('hour', time, 1)) AS base_ts,
       AVG(value),
       MAX(value),
       COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 최근 2시간 재계산
GROUP BY name;
```

`INSERT ... SELECT`에는 `ON DUPLICATE KEY UPDATE`를 붙이지 않습니다. 캐시를 재구성할 때는
기존 캐시를 삭제한 뒤 다시 적재합니다.

## 대시보드 조회 최적화

```sql
-- 캐시 우선 조회, 없으면 원본에서 계산
SELECT sensor_id, base_ts, avg_val, max_val
FROM sensor_recent_avg
WHERE base_ts >= NOW - 86400000000000
ORDER BY sensor_id, base_ts;
```

## 장애 복구

서버 재시작 시 VOLATILE 캐시가 소멸되면 원본 TAG 테이블에서 재계산합니다.

```sql
-- 캐시 재구성 (서버 재시작 후)
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name,
       name, MAX(DATE_TRUNC('hour', time, 1)), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 86400000000000  -- 최근 24시간 재구성
GROUP BY name;
```
