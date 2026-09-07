---
title: '6.4 ROLLUP 조회 문법'
weight: 40
toc: true
aliases:
  - /dbms/tag-rollup-usage/week-month-year-timezone-rollup/
---

<a id="query-syntax-rollup"></a>

## 명시적인 ROLLUP 조회

```text
rollup(time_unit, period, basetime_column [, origin])
```

| 인자 | 계약 |
|---|---|
| time_unit | SECOND/SEC, MINUTE/MIN, HOUR, DAY, WEEK, MONTH, YEAR; 대소문자 무관 |
| period | 양의 정수 리터럴; 컬럼이나 매개변수 자리표시자가 아님 |
| basetime_column | 원본 시간축 TAG의 BASETIME 컬럼 |
| origin | 생략 시 시간대 오프셋을 반영한 기본 기준점; 명시 시 단위별 제약 확인 |

반환값은 DATETIME 버킷입니다. 저장된 집계의 최소 간격보다 세밀한 결과를 복원할 수는
없습니다. 적용 가능한 ROLLUP이 없으면 원시 스캔으로 자동 전환하지 않고 오류가 발생합니다.
원본 집계가 필요하면 별도의 DATE_TRUNC/DATE_BIN + GROUP BY 쿼리를 작성합니다.

## 준비와 기본 조회

```sql
CREATE TAG TABLE ch6_query (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_query_sec ON ch6_query(value) INTERVAL 1 SEC;
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_query);
ALTER ROLLUP ch6_query_sec FORCE;

SELECT name, rollup('min', 1, time) AS bucket,
       COUNT(value), SUM(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_query
 WHERE time >= TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 00:02:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01의 00:00은 COUNT=2, SUM=30, AVG=15이고 00:01은 1, 30, 30입니다.
TEMP_02는 00:00의 1, 100, 100입니다. SELECT에서 name을 반환한다면 GROUP BY에도
name을 넣습니다. name을 빼면 여러 태그를 합친 집계이므로 단위가 다른 센서를 섞지 않습니다.

## 후보 선택과 힌트

1. ROLLUP_TABLE 힌트가 있으면 해당 후보의 호환성을 검사합니다.
2. 자동 선택은 집계 컬럼·JSON 경로·모드와 요청 간격이 맞는 후보를 찾습니다.
3. 조건 없는 후보를 먼저 찾고, 없을 때 조건 후보를 포함해 탐색합니다.
4. 적용 가능한 가장 큰 간격을 선택하며 같은 간격에서는 먼저 등록된 후보가 유지됩니다.

일반/확장 여부만으로 “일반이 항상 우선”이라고 단정하지 않습니다.
조건 ROLLUP만 있을 때는 필터된 데이터가 자동 선택될 수 있으므로 결과가 나타내는
표본 집합을 확인합니다. 반드시 특정 집계를 사용해야 하면 힌트를 명시합니다.

```sql
SELECT /*+ ROLLUP_TABLE(ch6_query_sec) */
       rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

### 저장 후보의 간격과 조회 버킷

현재 후보 간격 검사는 SEC 요청을 period초, MIN 요청을 period분으로 계산합니다.
HOUR와 DAY/WEEK/MONTH/YEAR 요청은 후보 선택 단계에서 period시간을 기준으로 검사하고,
선택된 통계를 요청한 달력·시간 버킷으로 다시 합칩니다.

따라서 `rollup('day', 1, time)`을 위해 24 HOUR ROLLUP을 만들면 자동으로 사용할 수
있다고 가정하면 안 됩니다. 해당 요청은 1시간 기준에 맞는 HOUR/MIN/SEC 후보를 검토합니다.
생성 INTERVAL과 결과 버킷의 의미를 구분하고 실제 실행 계획을 확인합니다.

## 집계 함수와 표본

일반 숫자 ROLLUP은 MIN, MAX, SUM, COUNT, AVG, SUMSQ를 지원합니다.
ROLLUP 조회의 FIRST/LAST에는 EXTENSION이 필요합니다. Custom 결과는 일반 TAG에
저장되므로 [Custom 재집계](../custom-rollup/)의 합계·건수 규칙을 사용합니다.
JSON 문서 전체 집계의 COUNT도 [JSON 절](../json-summarized-rollup/)에서 별도로 설명합니다.

<a id="query-week-month-year-day-timezone-origin-rollup"></a>

## 달력 단위와 origin

같은 준비 데이터를 사용해 월 단위 결과와 월요일 기준 주 단위를 확인합니다.

```sql
SELECT rollup('month', 1, time, '2000-01-01 00:00:00') AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('week', 1, time, '1970-01-05 00:00:00') AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

월 조회는 2026-01-01 버킷에 SUM=60, COUNT=3, AVG=20을 반환합니다.
월·년 origin은 시간대 해석 후 월의 1일이어야 하며 결과는 해당 월 경계의 자정입니다.
임의 날짜나 시각 오프셋으로 월간 업무 시작 시각을 옮기는 기능으로 해석하지 않습니다.
일·주 같은 고정 간격의 origin과 월·년의 달력 계산을 구분합니다.

문자열의 의미는 접속 시간대와 함께 확인합니다. DST를 자동으로 원하는 업무 달력에
맞춰 준다고 가정하지 말고 경계 전후의 원본 DATE_BIN 집계와 비교합니다. 저장 집계를
쪼개야 하는 origin이나 조회 경계에는 원본과 동일한 결과를 기대할 수 있는지 검증합니다.

## 정리

```sql
DROP ROLLUP ch6_query_sec;
DROP TABLE ch6_query;
```
