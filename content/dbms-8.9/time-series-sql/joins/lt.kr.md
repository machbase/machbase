---
type: docs
title: '13.1.2 LT JOIN: 같은 시각을 제외한 직전 상태'
weight: 20
toc: true
---

[시계열 JOIN·TIMESTAMP·TIE 전체 BNF](../../../reference/sql/syntax/time-series-join-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

이벤트 직전의 상태만 필요할 때 사용합니다. ASOF와 달리 오른쪽 시각이 이벤트 시각보다 **엄격히 이전**이어야 합니다.

10초 이벤트에서 ASOF는 10초의 값 100을, LT는 8초의 값 64를 선택합니다. 30초 이벤트도 30초 관측을 제외하고 28초의 값 784를 선택합니다. `TOLERANCE 0s`이면 엄격히 이전이면서 차이가 0인 관측은 존재할 수 없어 모두 미매칭입니다.

허용 시간의 경계는 포함합니다. 후보 부재·시간차 초과 시 왼쪽을 유지하고 오른쪽을 NULL로 반환합니다. 같은 후보 시각의 중복과 입력·출력 필터의 차이는 ASOF와 같습니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 5초 허용차](#example-1) | 정상 |
| 2 | [정확 시각과 0초 허용차](#example-2) | 정상 |
| 3 | [허용차 2초의 포함 경계](#example-3) | 정상 |
| 4 | [허용차를 생략한 조회](#example-4) | 정상 |
| 5 | [최종 WHERE로 선택 결과 제한](#example-5) | 정상 |
| 6 | [오른쪽 입력을 먼저 필터링](#example-6) | 정상 |
| 7 | [동일 시각은 논리 순서로 FIRST 선택](#example-7) | 정상 |
| 8 | [동일 시각은 논리 순서로 LAST 선택](#example-8) | 정상 |
| 9 | [기본 TIE ERROR의 중복 진단](#example-9) | 오류 확인 |
| 10 | [시간축 없는 LOG 입력 거부](#example-10) | 오류 확인 |

## 1. 공통 데이터의 5초 허용차 {#example-1}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/01.json)

```sql
SELECT e.ID AS EVENT_ID,CAST((TO_TIMESTAMP(e.TIME)-1798729200000000000)/1000000000 AS LONG) AS EVENT_S,
 m.ID AS MOTOR_ID,CAST((TO_TIMESTAMP(m.TIME)-1798729200000000000)/1000000000 AS LONG) AS MOTOR_S,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e LT JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 5s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | EVENT_S | MOTOR_ID | MOTOR_S | MOTOR_VALUE |
| --- | --- | --- | --- | --- |
| 1 | 10 | 103 | 8 | 64 |
| 2 | 21 | 107 | 18 | 324 |
| 3 | 30 | 110 | 28 | 784 |
| 4 | 41 | 114 | 38 | 1444 |
| 5 | 46 | 116 | 44 | 1936 |
| 6 | 60 | NULL | NULL | NULL |


## 2. 정확 시각과 0초 허용차 {#example-2}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/02.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e LT JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 0s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | NULL | NULL |
| 2 | NULL | NULL |
| 3 | NULL | NULL |
| 4 | NULL | NULL |
| 5 | NULL | NULL |
| 6 | NULL | NULL |


## 3. 허용차 2초의 포함 경계 {#example-3}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/03.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e LT JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 2s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 103 | 64 |
| 2 | NULL | NULL |
| 3 | 110 | 784 |
| 4 | NULL | NULL |
| 5 | 116 | 1936 |
| 6 | NULL | NULL |


## 4. 허용차를 생략한 조회 {#example-4}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/04.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e LT JOIN TS13_MOTOR m ON e.NAME=m.NAME

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 103 | 64 |
| 2 | 107 | 324 |
| 3 | 110 | 784 |
| 4 | 114 | 1444 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 5. 최종 WHERE로 선택 결과 제한 {#example-5}

최종 WHERE는 선택 후 필터입니다. 더 오래되거나 다른 후보를 다시 찾지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/05.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e LT JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.NAME='edu27_main' AND m.VALUE>500 ORDER BY e.ID;
```

결과 **4행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 3 | 110 | 784 |
| 4 | 114 | 1444 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 6. 오른쪽 입력을 먼저 필터링 {#example-6}

오른쪽 파생 조회는 후보 집합을 먼저 제한합니다. 최종 WHERE와 NULL·행 수가 다를 수 있습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/06.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e LT JOIN (
 SELECT NAME,TIME,ID,VALUE FROM TS13_MOTOR WHERE VALUE>500
) m TIMESTAMP(TIME) ON e.NAME=m.NAME
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | NULL | NULL |
| 2 | NULL | NULL |
| 3 | 110 | 784 |
| 4 | 114 | 1444 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 7. 동일 시각은 논리 순서로 FIRST 선택 {#example-7}

선택된 시각 그룹 안에서 비NULL·고유한 SEQ로 순서를 정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/07.json)

```sql
SELECT e.ID AS EVENT_ID,r.VALUE AS READING
FROM TS13_EVENT e LT JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME
TOLERANCE 5s TIE FIRST BY r.SEQ WHERE e.ID=2;
```

결과 **1행**입니다.

| EVENT_ID | READING |
| --- | --- |
| 2 | 324 |


## 8. 동일 시각은 논리 순서로 LAST 선택 {#example-8}

순서 키는 값 크기나 삽입 순서가 아니라 원본 논리 순서를 뜻합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/08.json)

```sql
SELECT e.ID AS EVENT_ID,r.VALUE AS READING
FROM TS13_EVENT e LT JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME
TOLERANCE 5s TIE LAST BY r.SEQ WHERE e.ID=2;
```

결과 **1행**입니다.

| EVENT_ID | READING |
| --- | --- |
| 2 | 325 |


## 9. 기본 TIE ERROR의 중복 진단 {#example-9}

선택할 시각 그룹의 중복을 FIRST/LAST와 고유한 순서 키로 해결합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/09.json)

```sql
SELECT r.VALUE FROM TS13_EVENT e LT JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME WHERE e.ID=2;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
Function [E_TIE_CONFLICT] argument data type does not match.
```


## 10. 시간축 없는 LOG 입력 거부 {#example-10}

LOG는 TIME이라는 컬럼이 있어도 자동 시간축이 아닙니다. TIMESTAMP(TIME)을 선언합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/lt/10.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/lt/10.json)

```sql
SELECT e.ID,r.VALUE FROM TS13_EVENT e LT JOIN TS13_TIES r ON e.NAME=r.NAME;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
