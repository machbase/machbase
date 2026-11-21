---
type: docs
title: '13.1.1 ASOF JOIN: 이벤트 시점의 직전 상태'
weight: 10
toc: true
---

이벤트가 발생한 순간에 유효했던 최신 상태를 조회합니다. 같은 키에서 오른쪽 시각이 왼쪽 시각 이하인 후보 중 가장 늦은 관측 한 행을 선택합니다. 같은 시각도 포함합니다.

`TOLERANCE 5s`는 선택 관측과 이벤트의 차이가 5초 이하인 경우만 허용합니다. 생략하면 과거 방향의 시간차에 제한이 없습니다. 후보가 없거나 허용 시간을 넘으면 왼쪽 이벤트를 유지하고 오른쪽을 NULL로 반환합니다.

21초 이벤트는 18초의 값 324를 선택합니다. 22초 관측은 미래이므로 제외합니다. 60초 이벤트에서는 마지막 관측인 50초와 10초 차이가 나므로 5초 허용차를 만족하지 않습니다.

## 중복과 필터 위치

동일 키·시각의 후보가 여러 개이면 기본 `TIE ERROR`는 오류를 반환합니다. `TIE FIRST BY m.SEQ` 또는 `TIE LAST BY m.SEQ`로 논리적 순서를 지정합니다. 순서 키가 NULL이거나 끝까지 동률이면 선택하지 않고 오류를 반환합니다. 물리 저장 순서에 의존하지 않습니다.

오른쪽 입력의 서브쿼리 WHERE는 후보를 먼저 제한합니다. 최종 WHERE는 이미 선택된 결과를 거릅니다. 최종 WHERE가 선택 관측을 제거해도 그다음 후보를 다시 선택하지 않습니다. 여러 시간 JOIN을 연결할 때의 기준 시각은 최초 왼쪽 행의 시각입니다.

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

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/01.json)

```sql
SELECT e.ID AS EVENT_ID,CAST((TO_TIMESTAMP(e.TIME)-1798729200000000000)/1000000000 AS LONG) AS EVENT_S,
 m.ID AS MOTOR_ID,CAST((TO_TIMESTAMP(m.TIME)-1798729200000000000)/1000000000 AS LONG) AS MOTOR_S,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 5s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | EVENT_S | MOTOR_ID | MOTOR_S | MOTOR_VALUE |
| --- | --- | --- | --- | --- |
| 1 | 10 | 104 | 10 | 100 |
| 2 | 21 | 107 | 18 | 324 |
| 3 | 30 | 111 | 30 | 900 |
| 4 | 41 | 114 | 38 | 1444 |
| 5 | 46 | 116 | 44 | 1936 |
| 6 | 60 | NULL | NULL | NULL |


## 2. 정확 시각과 0초 허용차 {#example-2}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/02.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m ON e.NAME=m.NAME
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

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/03.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m ON e.NAME=m.NAME
TOLERANCE 2s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 104 | 100 |
| 2 | NULL | NULL |
| 3 | 111 | 900 |
| 4 | NULL | NULL |
| 5 | 116 | 1936 |
| 6 | NULL | NULL |


## 4. 허용차를 생략한 조회 {#example-4}

왼쪽 이벤트를 유지하고 선택된 관측 또는 NULL을 반환합니다. 행 ID로 원래 시각과 값을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/04.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m ON e.NAME=m.NAME

WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 104 | 100 |
| 2 | 107 | 324 |
| 3 | 111 | 900 |
| 4 | 114 | 1444 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 5. 최종 WHERE로 선택 결과 제한 {#example-5}

최종 WHERE는 선택 후 필터입니다. 더 오래되거나 다른 후보를 다시 찾지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/05.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.NAME='edu27_main' AND m.VALUE>500 ORDER BY e.ID;
```

결과 **4행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 3 | 111 | 900 |
| 4 | 114 | 1444 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 6. 오른쪽 입력을 먼저 필터링 {#example-6}

오른쪽 파생 조회는 후보 집합을 먼저 제한합니다. 최종 WHERE와 NULL·행 수가 다를 수 있습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/06.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e ASOF JOIN (
 SELECT NAME,TIME,ID,VALUE FROM TS13_MOTOR WHERE VALUE>500
) m TIMESTAMP(TIME) ON e.NAME=m.NAME
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | NULL | NULL |
| 2 | NULL | NULL |
| 3 | 111 | 900 |
| 4 | 114 | 1444 |
| 5 | 116 | 1936 |
| 6 | 118 | 2500 |


## 7. 동일 시각은 논리 순서로 FIRST 선택 {#example-7}

선택된 시각 그룹 안에서 비NULL·고유한 SEQ로 순서를 정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/07.json)

```sql
SELECT e.ID AS EVENT_ID,r.VALUE AS READING
FROM TS13_EVENT e ASOF JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME
TOLERANCE 5s TIE FIRST BY r.SEQ WHERE e.ID=2;
```

결과 **1행**입니다.

| EVENT_ID | READING |
| --- | --- |
| 2 | 324 |


## 8. 동일 시각은 논리 순서로 LAST 선택 {#example-8}

순서 키는 값 크기나 삽입 순서가 아니라 원본 논리 순서를 뜻합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/08.json)

```sql
SELECT e.ID AS EVENT_ID,r.VALUE AS READING
FROM TS13_EVENT e ASOF JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME
TOLERANCE 5s TIE LAST BY r.SEQ WHERE e.ID=2;
```

결과 **1행**입니다.

| EVENT_ID | READING |
| --- | --- |
| 2 | 325 |


## 9. 기본 TIE ERROR의 중복 진단 {#example-9}

선택할 시각 그룹의 중복을 FIRST/LAST와 고유한 순서 키로 해결합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/09.json)

```sql
SELECT r.VALUE FROM TS13_EVENT e ASOF JOIN (SELECT * FROM TS13_TIES WHERE TIME<FROM_TIMESTAMP(1798729220000000000)) r TIMESTAMP(TIME) ON e.NAME=r.NAME WHERE e.ID=2;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
Function [E_TIE_CONFLICT] argument data type does not match.
```


## 10. 시간축 없는 LOG 입력 거부 {#example-10}

LOG는 TIME이라는 컬럼이 있어도 자동 시간축이 아닙니다. TIMESTAMP(TIME)을 선언합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/asof/10.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/asof/10.json)

```sql
SELECT e.ID,r.VALUE FROM TS13_EVENT e ASOF JOIN TS13_TIES r ON e.NAME=r.NAME;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
