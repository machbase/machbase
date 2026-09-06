---
title: '6.4 ROLLUP 조회 문법'
weight: 40
toc: true
aliases:
  - /dbms/tag-rollup-usage/week-month-year-timezone-rollup/
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
| period | 1 이상의 정수 literal. 컬럼이나 bind 값은 사용할 수 없음 |
| basetime_column | 대상 TAG 테이블의 BASETIME 컬럼 이름 |
| origin | DATETIME으로 변환 가능한 기준식. 생략 시 session timezone offset을 반영한 기본 origin 사용 |

반환 타입은 `DATETIME`입니다. 지원 단위는 `SECOND`/`SEC`, `MINUTE`/`MIN`, `HOUR`,
`DAY`, `WEEK`, `MONTH`, `YEAR`이며 대소문자를 구분하지 않습니다.

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

| time_unit | 일반적으로 선택되는 가장 큰 ROLLUP 레벨 |
|-----------|------------------------------------------|
| second, sec | 초(SEC) ROLLUP |
| minute, min | 분(MIN) ROLLUP |
| hour, day, week, month, year | HOUR 우선. 적용 가능하면 MIN·SEC 후보도 선택 가능 |

> 장주기 요청은 적용 가능한 가장 큰 ROLLUP을 읽고 서버가 요청 bucket으로 재집계합니다.
> HOUR가 없더라도 MIN·SEC interval이 요청 interval을 나누면 선택될 수 있습니다.
> 요청 interval에 적용 가능한 ROLLUP이 없으면 원시 TAG scan으로 전환하지 않고 오류를
> 반환합니다.

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

엔진의 선택 기준은 다음과 같습니다.

1. `ROLLUP_TABLE` 힌트가 있으면 지정한 ROLLUP을 사용합니다. 요청과 호환되지 않으면 오류를 반환합니다.
2. 같은 주기·컬럼인 후보 중 **조건 없는 ROLLUP** 우선
3. 조건 없는 ROLLUP이 없으면 조건 ROLLUP 사용
4. 후보가 여러 개면 요청 주기의 약수 중 가장 큰 주기 → 먼저 등록된 ROLLUP 순으로 선택

<a id="query-week-month-year-day-timezone-origin-rollup"></a>

## 주·월·연 단위와 origin

`day`, `week`, `month`, `year` 요청도 적용 가능한 가장 큰 ROLLUP을 읽고 요청 bucket으로
재집계합니다.

```sql
-- 월 단위 집계
SELECT rollup('month', 1, time) AS rt, AVG(value)
  FROM tag
 WHERE name = 'SENSOR-01'
   AND time BETWEEN '2024-01-01' AND '2024-12-31'
 GROUP BY rt
 ORDER BY rt;

-- 월요일 시작 주 단위
SELECT rollup('week', 1, time, '1970-01-05 00:00:00') AS rt,
       AVG(value)
  FROM tag
 WHERE name = 'SENSOR-01'
 GROUP BY rt
 ORDER BY rt;
```

origin을 생략하면 session timezone offset을 반영한 기본값을 사용합니다. 업무일이 오전
6시에 시작하면 `2000-01-01 06:00:00`처럼 DATETIME으로 변환 가능한 origin을 명시합니다.
같은 문자열도 session timezone에 따라 다른 절대 시각이 될 수 있으므로 실제 접속 timezone에서
bucket 경계를 검증합니다.

- 월·연도는 달력상 길이가 가변적입니다.
- DST 환경에서는 timezone과 origin 전후의 표본을 확인합니다.
- 정밀한 달력 절단이 필요하면 `DATE_TRUNC()`와 `GROUP BY`를 함께 사용합니다.
