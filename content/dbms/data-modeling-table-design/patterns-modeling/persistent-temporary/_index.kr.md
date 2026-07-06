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
CREATE VOLATILE TABLE sensor_1h_avg (
    sensor_id VARCHAR(64) PRIMARY KEY,
    hour_ts   DATETIME    PRIMARY KEY,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       INTEGER
);
```

## 캐시 갱신 패턴

```sql
-- 주기적 집계 갱신 (1시간마다 실행)
INSERT INTO sensor_1h_avg
SELECT name,
       TIME_BUCKET('1h', time) AS hour_ts,
       AVG(value),
       MAX(value),
       COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 최근 2시간 재계산
GROUP BY name, TIME_BUCKET('1h', time)
ON DUPLICATE KEY UPDATE
    avg_val = VALUES(avg_val),
    max_val = VALUES(max_val),
    cnt = VALUES(cnt);
```

## 대시보드 조회 최적화

```sql
-- 캐시 우선 조회, 없으면 원본에서 계산
SELECT sensor_id, hour_ts, avg_val, max_val
FROM sensor_1h_avg
WHERE hour_ts >= NOW - 86400000000000
ORDER BY sensor_id, hour_ts;
```

## 장애 복구

서버 재시작 시 VOLATILE 캐시가 소멸되면 원본 TAG 테이블에서 재계산합니다.

```sql
-- 캐시 재구성 (서버 재시작 후)
INSERT INTO sensor_1h_avg
SELECT name, TIME_BUCKET('1h', time), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 86400000000000  -- 최근 24시간 재구성
GROUP BY name, TIME_BUCKET('1h', time);
```
