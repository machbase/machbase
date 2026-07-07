---
type: docs
title: '집계 함수와 GROUP BY'
weight: 10
---

집계 함수(Aggregate Function)는 여러 행의 값을 하나의 결과로 요약합니다. Machbase는 표준 SQL 집계 함수를 지원하며, GROUP BY와 HAVING 절을 함께 사용하여 그룹별 집계를 수행할 수 있습니다.

## 지원 집계 함수

| 함수 | 설명 |
|------|------|
| `COUNT(*)` | 전체 행 수 |
| `COUNT(col)` | NULL이 아닌 값의 수 |
| `SUM(col)` | 합계 |
| `AVG(col)` | 평균 |
| `MIN(col)` | 최솟값 |
| `MAX(col)` | 최댓값 |
| `SUMSQ(col)` | 제곱합 |
| `STDDEV(col)` | 표준편차 |
| `VARIANCE(col)` | 분산 |

## GROUP BY 기본 사용법

GROUP BY 절은 지정한 컬럼의 값이 같은 행들을 하나의 그룹으로 묶고, 각 그룹에 집계 함수를 적용합니다.

```sql
-- LOG 테이블: 장비 유형별 측정값 평균
SELECT device_type, AVG(value) AS avg_value, COUNT(*) AS cnt
FROM sensor_log
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
GROUP BY device_type;
```

```sql
-- TAG 테이블: 센서 이름별 최대·최솟값
SELECT name, MIN(value) AS min_val, MAX(value) AS max_val
FROM tag
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
GROUP BY name;
```

### HAVING 절

HAVING은 집계 결과에 조건을 적용합니다. WHERE가 행 수준 필터라면, HAVING은 그룹 수준 필터입니다.

```sql
-- 하루 평균이 50 이상인 센서만 조회
SELECT name, AVG(value) AS avg_val
FROM tag
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
GROUP BY name
HAVING AVG(value) >= 50;
```

## NULL 처리

집계 함수는 기본적으로 NULL 값을 무시합니다. `COUNT(*)`는 NULL 포함 전체 행을 세지만, `COUNT(col)`은 해당 컬럼이 NULL인 행을 제외합니다.

```sql
-- col에 NULL이 있는 경우 두 결과가 다를 수 있음
SELECT COUNT(*), COUNT(value) FROM sensor_log;
```

## 시계열 데이터에서의 주의 사항

> **주의**: TAG 테이블에서 단순 GROUP BY를 사용하면 전체 기간의 값을 하나의 그룹으로 처리합니다. 시간 축을 기준으로 일정 간격마다 집계하려면 [ROLLUP](../rollup/)을 사용하십시오. ROLLUP은 시간 해상도(초, 분, 시간 등)를 지정하여 자동으로 시간 버킷을 만들어 줍니다.

```sql
-- 잘못된 예: 전체 기간을 하나의 그룹으로 집계
SELECT name, AVG(value) FROM tag GROUP BY name;

-- 올바른 예: 1시간 단위로 집계하려면 ROLLUP 사용
SELECT name, AVG(value)
FROM tag
GROUP BY name
ROLLUP (time, 1 HOUR);
```

## LOG 테이블과 TAG 테이블 비교

LOG 테이블은 임의 컬럼을 GROUP BY 기준으로 사용할 수 있습니다. TAG 테이블은 `name` 컬럼을 그룹 기준으로 자주 사용하며, 시간 축 집계는 ROLLUP을 병행하는 것이 권장됩니다.

```sql
-- LOG 테이블: 여러 컬럼을 GROUP BY 기준으로 사용
SELECT factory, line, AVG(temperature) AS avg_temp
FROM production_log
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
GROUP BY factory, line
ORDER BY factory, line;
```
