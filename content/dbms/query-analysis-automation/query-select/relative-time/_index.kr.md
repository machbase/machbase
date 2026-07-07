---
type: docs
title: '상대 시간 표현'
weight: 40
---

Machbase에서 현재 시각 기준의 상대 시간을 계산하는 함수와 표현식을 정리합니다.

## NOW

현재 서버 시각을 반환합니다. INSERT 및 WHERE 조건에 모두 사용할 수 있습니다.

```sql
-- 현재 시각 조회
SELECT NOW;

-- INSERT에서 현재 시각 삽입
INSERT INTO sensor_log VALUES ('TEMP-01', NOW, 25.3);

-- WHERE에서 현재 시각 비교
SELECT * FROM sensor_log WHERE ts < NOW;
```

## DATEADD

날짜에 특정 기간을 더하거나 빼는 함수입니다.

```sql
DATEADD(unit, n, datetime_expr)
-- unit: 'y'(년), 'mm'(월), 'w'(주), 'd'(일), 'h'(시), 'mi'(분), 's'(초)
```

```sql
-- 현재 기준 1시간 전
SELECT DATEADD('h', -1, NOW);

-- 현재 기준 30일 후
SELECT DATEADD('d', 30, NOW);

-- 최근 24시간 데이터 조회
SELECT * FROM sensor_log
WHERE ts >= DATEADD('h', -24, NOW);

-- 최근 7일 TAG 데이터
SELECT name, time, value FROM tag
WHERE time >= DATEADD('d', -7, NOW)
ORDER BY name, time;
```

## TO_DATE

문자열을 DATETIME으로 변환합니다.

```sql
TO_DATE(str, format)
```

```sql
SELECT * FROM sensor_log
WHERE ts >= TO_DATE('2024-01-15', 'YYYY-MM-DD');

SELECT * FROM sensor_log
WHERE ts BETWEEN TO_DATE('2024-01-15 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
             AND TO_DATE('2024-01-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

## DATE_TRUNC

날짜를 특정 단위로 잘라냅니다. 시간 단위 집계에 유용합니다.

```sql
DATE_TRUNC(unit, datetime_expr)
-- unit: 'year', 'month', 'week', 'day', 'hour', 'minute', 'second'
```

```sql
-- 시간별 평균
SELECT DATE_TRUNC('hour', time) AS h, AVG(value)
FROM tag
WHERE name = 'TEMP-01'
GROUP BY h
ORDER BY h;

-- 일별 최댓값
SELECT DATE_TRUNC('day', time) AS d, name, MAX(value)
FROM tag
GROUP BY d, name
ORDER BY d, name;
```

## TO_CHAR

DATETIME을 문자열로 변환합니다.

```sql
TO_CHAR(datetime_expr, format)
```

```sql
SELECT TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') AS time_str, value
FROM tag WHERE name = 'TEMP-01';
```
