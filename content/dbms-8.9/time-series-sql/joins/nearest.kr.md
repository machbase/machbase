---
type: docs
title: '13.1.3 NEAREST JOIN: 가장 가까운 관측값'
weight: 30
toc: true
---

이벤트 전후에서 절대 시간차가 가장 작은 실측 한 행을 선택합니다. 미래 관측도 사용할 수 있는 사후 분석에 적합합니다.

21초 이벤트는 과거 18초보다 가까운 미래 22초의 값 484를 선택합니다. 46초에서는 44초와 48초가 모두 2초 차이이므로 과거 44초의 값 1936을 선택합니다. 이 과거 우선 규칙과 동일 시각에 여러 행이 있는 경우의 TIE 정책은 별개입니다.

`TOLERANCE 5s`는 양쪽 방향에서 각각 5초 이내를 허용합니다. 생략 시 시간차 제한 없이 가장 가까운 관측을 선택합니다. 결과값이 NULL인 실제 관측과 후보가 없는 미매칭은 출처 정보로 구분할 수 있습니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 5초 허용차](#example-1) | 정상 |
| 2 | [정확 시각과 0초 허용차](#example-2) | 정상 |
| 3 | [허용차 2초의 포함 경계](#example-3) | 정상 |
| 4 | [허용차를 생략한 조회](#example-4) | 정상 |
| 5 | [최종 WHERE로 선택 결과 제한](#example-5) | 정상 |
| 6 | [같은 거리이면 과거 관측 선택](#example-6) | 정상 |
| 7 | [동일 시각은 논리 순서로 FIRST 선택](#example-7) | 정상 |
| 8 | [동일 시각은 논리 순서로 LAST 선택](#example-8) | 정상 |
| 9 | [기본 TIE ERROR의 중복 진단](#example-9) | 오류 확인 |
| 10 | [시간축 없는 LOG 입력 거부](#example-10) | 오류 확인 |

## 1. 공통 데이터의 5초 허용차 {#example-1}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/01.json)

```sql
SELECT e.ID AS EVENT_ID,CAST((TO_TIMESTAMP(e.TIME)-1798729200000000000)/1000000000 AS LONG) AS EVENT_S,
 m.ID AS MOTOR_ID,CAST((TO_TIMESTAMP(m.TIME)-1798729200000000000)/1000000000 AS LONG) AS MOTOR_S,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e NEAREST JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 5s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | EVENT_S | MOTOR_ID | MOTOR_S | MOTOR_VALUE |
| --- | --- | --- | --- | --- |
| 1 | 10 | 104 | 10 | 100 |
| 2 | 21 | 108 | 22 | 484 |
| 3 | 30 | 111 | 30 | 900 |
| 4 | 41 | 115 | 42 | 1764 |
| 5 | 46 | 116 | 44 | 1936 |
| 6 | 60 | NULL | NULL | NULL |


## 2. 정확 시각과 0초 허용차 {#example-2}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/02.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e NEAREST JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 0s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 104 | 100 |
| 2 | NULL | NULL |
| 3 | 111 | 900 |
| 4 | NULL | NULL |
| 5 | NULL | NULL |
| 6 | NULL | NULL |


## 3. 허용차 2초의 포함 경계 {#example-3}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/03.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e NEAREST JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 2s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 104 | 100 |
| 2 | 108 | 484 |
| 3 | 111 | 900 |
| 4 | 115 | 1764 |
| 5 | 116 | 1936 |
| 6 | NULL | NULL |


## 4. 허용차를 생략한 조회 {#example-4}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/04.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e NEAREST JOIN TS13_MOTOR m ON e.NAME=m.NAME

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 104 | 100 |
| 2 | 108 | 484 |
| 3 | 111 | 900 |
| 4 | 115 | 1764 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 5. 최종 WHERE로 선택 결과 제한 {#example-5}

최종 WHERE는 선택 후 필터입니다. 더 오래되거나 다른 후보를 다시 찾지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/05.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e NEAREST JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.NAME='edu27_main' AND m.VALUE>500 ORDER BY e.ID;
```

결과 **4행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 3 | 111 | 900 |
| 4 | 115 | 1764 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 6. 같은 거리이면 과거 관측 선택 {#example-6}

46초에서 44초와 48초의 거리는 같습니다. 과거 44초 관측을 선택합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/06.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE FROM TS13_EVENT e NEAREST JOIN TS13_MOTOR m ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=5 ORDER BY e.ID;
```

결과 **1행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 5 | 116 | 1936 |


## 7. 동일 시각은 논리 순서로 FIRST 선택 {#example-7}

선택된 시각 그룹 안에서 비NULL·고유한 SEQ로 순서를 정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/07.json)

```sql
SELECT e.ID AS EVENT_ID,r.VALUE AS READING
FROM TS13_EVENT e NEAREST JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME
TOLERANCE 5s TIE FIRST BY r.SEQ WHERE e.ID=2;
```

결과 **1행**입니다.

| EVENT_ID | READING |
| --- | --- |
| 2 | 324 |


## 8. 동일 시각은 논리 순서로 LAST 선택 {#example-8}

순서 키는 값 크기나 삽입 순서가 아니라 원본 논리 순서를 뜻합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/08.json)

```sql
SELECT e.ID AS EVENT_ID,r.VALUE AS READING
FROM TS13_EVENT e NEAREST JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME
TOLERANCE 5s TIE LAST BY r.SEQ WHERE e.ID=2;
```

결과 **1행**입니다.

| EVENT_ID | READING |
| --- | --- |
| 2 | 325 |


## 9. 기본 TIE ERROR의 중복 진단 {#example-9}

선택할 시각 그룹의 중복을 FIRST/LAST와 고유한 순서 키로 해결합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/09.json)

```sql
SELECT r.VALUE FROM TS13_EVENT e NEAREST JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME WHERE e.ID=2;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
Function [E_TIE_CONFLICT] argument data type does not match.
```


## 10. 시간축 없는 LOG 입력 거부 {#example-10}

LOG는 TIME이라는 컬럼이 있어도 자동 시간축이 아닙니다. TIMESTAMP(TIME)을 선언합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/nearest/10.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/nearest/10.json)

```sql
SELECT e.ID,r.VALUE FROM TS13_EVENT e NEAREST JOIN TS13_TIES r ON e.NAME=r.NAME;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
