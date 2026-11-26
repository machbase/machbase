---
type: docs
title: '13.1.5 WINDOW JOIN: 이벤트 시간창의 집계'
weight: 50
toc: true
---

[시계열 JOIN·TIMESTAMP·TIE 전체 BNF](../../../reference/sql/syntax/time-series-join-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

이벤트마다 시간창 안의 관측을 모두 집계합니다. `RANGE BETWEEN 1m PRECEDING AND CURRENT ROW`는 `[이벤트 시각−1분, 이벤트 시각]`이며 양끝을 포함합니다.

21초 이벤트의 창에는 0·4·8·10·12·16·18초의 관측 7행이 있습니다. 평균은 `904 / 7 = 129.142857…`입니다. 같은 시각의 여러 행도 각각 집계하며 한 행을 선택하는 JOIN과 달리 창 안의 중복을 TIE로 제거하지 않습니다.

빈 창에서 COUNT(*)와 COUNT(expr)는 0이고 AVG·SUM 등은 각 함수의 빈 입력 규칙을 따릅니다. 실제 NULL 값의 행은 COUNT(*)에는 포함되고 COUNT(expr)에는 포함되지 않습니다. 오른쪽 원시 컬럼은 대표 행이 없으므로 MAX(m.TIME)처럼 집계합니다.

## 창의 경계와 이전 상태

경계에는 PRECEDING·CURRENT ROW·FOLLOWING을 사용합니다. WINDOW JOIN에서 UNBOUNDED는 지원하지 않습니다. NULL 경계는 빈 창이 되며 음수 폭은 0으로 보정됩니다. 역순 범위는 오류입니다.

기본은 EXCLUDE PREVAILING입니다. INCLUDE PREVAILING은 하한 시각에 적격 관측이 없을 때 하한 직전의 상태 한 행을 추가합니다. 창 안의 실제 행은 그대로 유지합니다. 추가할 시각에 중복이 있으면 별도의 TIE 정책이 필요합니다. ROWS 프레임의 행 개수 기준과 이 절의 시간 범위 기준은 다릅니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 과거 1분 창](#example-1) | 정상 |
| 2 | [양끝이 같은 정확 시각 창](#example-2) | 정상 |
| 3 | [3초 창의 하한 포함](#example-3) | 정상 |
| 4 | [관측 없는 창](#example-4) | 정상 |
| 5 | [하한 이전 상태를 추가](#example-5) | 정상 |
| 6 | [4초 창과 COUNT(expr)](#example-6) | 정상 |
| 7 | [WINDOW JOIN의 UNBOUNDED 경계 거부](#example-7) | 오류 확인 |
| 8 | [집계하지 않은 오른쪽 원시값 거부](#example-8) | 오류 확인 |

## 1. 공통 데이터의 과거 1분 창 {#example-1}

시간창 양끝은 포함합니다. 빈 창의 COUNT는 0이며 PREVAILING을 지정한 경우에만 하한 이전 대표를 더합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/01.json)

```sql
SELECT e.ID AS EVENT_ID,COUNT(*) AS N,AVG(m.VALUE) AS MEAN
FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE BETWEEN 60s PRECEDING AND CURRENT ROW

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | N | MEAN |
| --- | --- | --- |
| 1 | 4 | 45 |
| 2 | 7 | 129.1428571 |
| 3 | 11 | 331.6363636 |
| 4 | 14 | 529.4285714 |
| 5 | 16 | 694.5 |
| 6 | 18 | 884.2222222 |


## 2. 양끝이 같은 정확 시각 창 {#example-2}

시간창 양끝은 포함합니다. 빈 창의 COUNT는 0이며 PREVAILING을 지정한 경우에만 하한 이전 대표를 더합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/02.json)

```sql
SELECT e.ID AS EVENT_ID,COUNT(*) AS N,AVG(m.VALUE) AS MEAN
FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE BETWEEN 0s PRECEDING AND CURRENT ROW

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | N | MEAN |
| --- | --- | --- |
| 1 | 1 | 100 |
| 2 | 0 | NULL |
| 3 | 1 | 900 |
| 4 | 0 | NULL |
| 5 | 0 | NULL |
| 6 | 0 | NULL |


## 3. 3초 창의 하한 포함 {#example-3}

시간창 양끝은 포함합니다. 빈 창의 COUNT는 0이며 PREVAILING을 지정한 경우에만 하한 이전 대표를 더합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/03.json)

```sql
SELECT e.ID AS EVENT_ID,COUNT(*) AS N,AVG(m.VALUE) AS MEAN
FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE BETWEEN 3s PRECEDING AND CURRENT ROW

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | N | MEAN |
| --- | --- | --- |
| 1 | 2 | 82 |
| 2 | 1 | 324 |
| 3 | 2 | 842 |
| 4 | 1 | 1444 |
| 5 | 1 | 1936 |
| 6 | 0 | NULL |


## 4. 관측 없는 창 {#example-4}

시간창 양끝은 포함합니다. 빈 창의 COUNT는 0이며 PREVAILING을 지정한 경우에만 하한 이전 대표를 더합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/04.json)

```sql
SELECT e.ID AS EVENT_ID,COUNT(*) AS N,AVG(m.VALUE) AS MEAN
FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE BETWEEN 2s PRECEDING AND CURRENT ROW

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | N | MEAN |
| --- | --- | --- |
| 1 | 2 | 82 |
| 2 | 0 | NULL |
| 3 | 2 | 842 |
| 4 | 0 | NULL |
| 5 | 1 | 1936 |
| 6 | 0 | NULL |


## 5. 하한 이전 상태를 추가 {#example-5}

시간창 양끝은 포함합니다. 빈 창의 COUNT는 0이며 PREVAILING을 지정한 경우에만 하한 이전 대표를 더합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/05.json)

```sql
SELECT e.ID AS EVENT_ID,COUNT(*) AS N,AVG(m.VALUE) AS MEAN
FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE BETWEEN 2s PRECEDING AND CURRENT ROW
INCLUDE PREVAILING
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | N | MEAN |
| --- | --- | --- |
| 1 | 2 | 82 |
| 2 | 1 | 324 |
| 3 | 2 | 842 |
| 4 | 1 | 1444 |
| 5 | 1 | 1936 |
| 6 | 1 | 2500 |


## 6. 4초 창과 COUNT(expr) {#example-6}

시간창 양끝은 포함합니다. 빈 창의 COUNT는 0이며 PREVAILING을 지정한 경우에만 하한 이전 대표를 더합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/06.json)

```sql
SELECT e.ID AS EVENT_ID,COUNT(*) AS N,AVG(m.VALUE) AS MEAN
FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE BETWEEN 4s PRECEDING AND CURRENT ROW

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | N | MEAN |
| --- | --- | --- |
| 1 | 2 | 82 |
| 2 | 1 | 324 |
| 3 | 2 | 842 |
| 4 | 1 | 1444 |
| 5 | 2 | 1850 |
| 6 | 0 | NULL |


## 7. WINDOW JOIN의 UNBOUNDED 경계 거부 {#example-7}

시간창은 일반 ROWS 프레임과 다릅니다. 유한한 시간 경계를 지정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/07.json)

```sql
SELECT COUNT(*) FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_WINDOW_UNBOUNDED).
```


## 8. 집계하지 않은 오른쪽 원시값 거부 {#example-8}

창에는 여러 행이 있을 수 있어 오른쪽 값은 집계로 선택합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/window/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/window/08.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WINDOW JOIN TS13_MOTOR m ON e.NAME=m.NAME RANGE BETWEEN 1s PRECEDING AND CURRENT ROW;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_WINDOW_AGGREGATE).
```
