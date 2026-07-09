---
type: docs
title: '5.11.3 거리축 범위 조회'
weight: 50
---

거리축(BASE DISTANCE) TAG 테이블은 시간이 아닌 거리(위치) 기준으로 데이터를 조회합니다.

## 거리축 TAG 테이블

거리축 TAG 테이블은 `BASE DISTANCE` 컬럼을 사용하여 위치 기반 데이터를 저장합니다.

```sql
CREATE TAG TABLE position_sensor (
    name     VARCHAR(20) PRIMARY KEY,
    distance DOUBLE BASE DISTANCE,
    value    DOUBLE,
    quality  INT
);
```

## 거리 범위 조회

거리축 테이블은 시간 조건 대신 거리 조건으로 범위를 지정합니다.

```sql
-- 거리 0 ~ 100 범위의 데이터
SELECT name, distance, value
FROM position_sensor
WHERE distance BETWEEN 0 AND 100;

-- 특정 태그의 거리 범위
SELECT name, distance, value
FROM position_sensor
WHERE name = 'SENSOR-A'
  AND distance >= 50 AND distance <= 200;

-- 특정 거리 이후 데이터
SELECT name, distance, value
FROM position_sensor
WHERE distance > 500
ORDER BY name, distance;
```

## 거리별 집계

```sql
-- 100m 구간별 평균
SELECT name,
       FLOOR(distance / 100) * 100 AS seg_start,
       AVG(value) AS avg_val
FROM position_sensor
GROUP BY name, seg_start
ORDER BY name, seg_start;
```

## 거리축과 시간축 비교

| 항목 | 시간축 (BASETIME) | 거리축 (BASEDISTANCE) |
|------|----------------|-------------------|
| 기준 컬럼 타입 | DATETIME | DOUBLE, LONG, ULONG |
| DURATION 키워드 | O | X |
| 범위 조회 | WHERE time BETWEEN ... | WHERE distance BETWEEN ... |
| 대표 사용처 | 시계열 센서 데이터 | 위치·거리 기반 측정 데이터 |
| ROLLUP 지원 | O (WITH ROLLUP) | X |

> 거리축 테이블에는 `WITH ROLLUP`을 사용할 수 없습니다. ROLLUP은 시간축 TAG 테이블 전용입니다.
