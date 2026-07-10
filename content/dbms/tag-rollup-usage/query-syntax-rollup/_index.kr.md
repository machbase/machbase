---
title: '6.5 ROLLUP 조회 문법'
weight: 40
toc: true
---

<a id="query-syntax-rollup"></a>

## ROLLUP 조회 문법

ROLLUP 테이블 데이터는 `rollup()` 함수를 SELECT 절에 사용해 조회합니다.

### rollup() 함수

```text
rollup(time_unit, period, basetime_column [, origin])
```

| 파라미터 | 설명 |
|----------|------|
| time_unit | 시간 단위 문자열: `'sec'`, `'min'`, `'hour'`, `'day'`, `'week'`, `'month'`, `'year'` |
| period | 묶을 구간 수 (예: 5분이면 `'min'`, 5) |
| basetime_column | BASETIME 컬럼 이름 |
| origin | 구간 기준 시작 시각 (기본값: `'1970-01-01 00:00:00'`) |

### 기본 조회

```sql
-- 1분 단위 집계
SELECT rollup('min', 1, time) AS rt,
       MIN(value), MAX(value), AVG(value), COUNT(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 12:00:00'
GROUP BY rt
ORDER BY rt;
```

```sql
-- 5분 단위 집계
SELECT rollup('min', 5, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

```sql
-- 1시간 단위 집계
SELECT rollup('hour', 1, time) AS rt, SUM(value), COUNT(value)
FROM   tag
WHERE  name IN ('S1', 'S2', 'S3')
  AND  time BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY rt
ORDER BY rt;
```

### 지원 집계 함수

ROLLUP 조회에서 사용할 수 있는 집계 함수는 롤업 테이블에 저장된 값에 한정됩니다.

| 함수 | 일반 ROLLUP | 확장 ROLLUP |
|------|-------------|-------------|
| MIN | O | O |
| MAX | O | O |
| SUM | O | O |
| COUNT | O | O |
| AVG | O | O |
| SUMSQ | O | O |
| FIRST | X | O |
| LAST | X | O |

### 시간 단위와 조회 대상 ROLLUP 테이블

| time_unit | 조회하는 ROLLUP 레벨 |
|-----------|---------------------|
| nsec, usec, msec, sec | 초(SEC) ROLLUP |
| min | 분(MIN) ROLLUP |
| hour, day, week, month, year | 시(HOUR) ROLLUP |

> time_unit이 `'day'`, `'week'`, `'month'`, `'year'`여도 HOUR ROLLUP에서 읽습니다. 원하는 단위로 클라이언트에서 추가 집계하거나, `DATE_TRUNC` 함수를 함께 사용하십시오.

### 힌트: 특정 ROLLUP 강제 사용

여러 ROLLUP이 있을 때 특정 ROLLUP을 명시합니다.

```sql
SELECT /*+ ROLLUP_TABLE(_tag_ru_cond_1m) */
       rollup('min', 1, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

### ROLLUP 자동 선택 우선순위

힌트가 없을 때 엔진의 선택 기준:
1. `ROLLUP_TABLE` 힌트가 있으면 무조건 그 ROLLUP 사용
2. 같은 주기·컬럼인 후보 중 **조건 없는 ROLLUP** 우선
3. 조건 없는 ROLLUP이 없으면 조건 ROLLUP 사용
4. 후보가 여러 개면 요청 주기의 약수 중 가장 큰 주기 → 먼저 등록된 ROLLUP 순으로 선택
