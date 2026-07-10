---
title: '6.11 주/월/연 단위 조회와 시간대 기준'
weight: 100
toc: true
---

<a id="query-week-month-year-day-timezone-origin-rollup"></a>

## 주/월/연 단위 조회

`rollup()` 함수의 `time_unit`에 `'day'`, `'week'`, `'month'`, `'year'`를 사용하면 HOUR ROLLUP 테이블에서 데이터를 읽어 해당 단위로 묶어 반환합니다.

### 일/주/월/연 조회 예시

```sql
-- 일 단위 집계
SELECT rollup('day', 1, time) AS rt,
       MIN(value), MAX(value), AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY rt
ORDER BY rt;
```

```sql
-- 월 단위 집계
SELECT rollup('month', 1, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY rt
ORDER BY rt;
```

```sql
-- 주 단위 집계
SELECT rollup('week', 1, time) AS rt, COUNT(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

### origin 파라미터로 기준 시점 조정

기본 기준 시점은 `1970-01-01 00:00:00 UTC`입니다. 타임존이나 업무 기준을 맞추려면 `origin`을 명시합니다.

```sql
-- 한국 시간 기준 (UTC+9)으로 일 단위 집계
SELECT rollup('day', 1, time, '1970-01-01 09:00:00') AS rt,
       AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

```sql
-- 영업일 기준 (월요일 시작 주 단위)
SELECT rollup('week', 1, time, '1970-01-05 00:00:00') AS rt,
       AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
-- 1970-01-05는 월요일
```

### 주의사항

- `'day'`, `'week'`, `'month'`, `'year'`는 모두 HOUR ROLLUP을 읽으므로 HOUR 단위 ROLLUP이 존재해야 합니다.
- HOUR ROLLUP이 없으면 원시 TAG 데이터를 전체 스캔합니다.
- 월/연도는 달력상 길이가 가변적입니다. ROLLUP 결과는 UTC 기준 HOUR 버킷을 다시 묶어 계산하므로 DST(서머타임) 환경에서는 origin을 정확히 설정해야 합니다.

### DATE_TRUNC과 병행 사용

정밀한 달력 단위 집계가 필요하면 `DATE_TRUNC`와 GROUP BY를 조합합니다.

```sql
-- 월 기준으로 정렬된 집계
SELECT DATE_TRUNC('month', rollup('hour', 1, time)) AS month_rt,
       AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY month_rt
ORDER BY month_rt;
```
