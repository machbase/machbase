---
type: docs
title: 'WHERE / ORDER BY / LIMIT'
weight: 20
---

## WHERE 절

일반적인 비교 연산자를 모두 사용할 수 있습니다.

```sql
SELECT * FROM sensor_log
WHERE value > 25.0 AND sensor_id = 'TEMP-01';

-- BETWEEN
SELECT * FROM sensor_log
WHERE value BETWEEN 20.0 AND 30.0;

-- IN
SELECT * FROM sensor_log
WHERE sensor_id IN ('TEMP-01', 'TEMP-02', 'PRESS-01');

-- IS NULL / IS NOT NULL
SELECT * FROM sensor_log WHERE status IS NULL;
SELECT * FROM sensor_log WHERE status IS NOT NULL;
```

## ORDER BY

```sql
-- 오름차순 (기본)
SELECT * FROM sensor_log ORDER BY ts;

-- 내림차순
SELECT * FROM sensor_log ORDER BY ts DESC;

-- 다중 컬럼 정렬
SELECT * FROM sensor_log ORDER BY sensor_id, ts DESC;
```

TAG/LOG 테이블은 최신 데이터가 먼저 반환되는 경향이 있습니다. 명시적 정렬이 필요하면 ORDER BY를 지정하세요.

## LIMIT

결과 행 수를 제한합니다.

```sql
-- 최근 100건
SELECT * FROM sensor_log ORDER BY ts DESC LIMIT 100;

-- offset, count (100번째부터 50건)
SELECT * FROM sensor_log ORDER BY ts LIMIT 100, 50;
```

## HAVING

GROUP BY와 함께 사용하여 집계 결과에 조건을 적용합니다.

```sql
SELECT sensor_id, AVG(value) AS avg_val
FROM sensor_log
GROUP BY sensor_id
HAVING AVG(value) > 30.0;
```

## RANGE 연산자

현재 시각 기준으로 일정 기간 내의 데이터를 조회합니다.

```sql
-- 현재 기준 최근 1시간 데이터
SELECT * FROM sensor_log WHERE ts RANGE 1 HOUR;

-- 최근 30분
SELECT * FROM sensor_log WHERE ts RANGE 30 MINUTE;
```

`RANGE`는 `_ARRIVAL_TIME` 외의 DATETIME 컬럼에도 사용할 수 있습니다.
