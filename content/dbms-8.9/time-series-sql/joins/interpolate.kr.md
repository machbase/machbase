---
type: docs
title: '13.1.4 INTERPOLATE JOIN: 실측 사이의 선형 보간'
weight: 40
toc: true
---

기준 시각을 사이에 둔 두 실측으로 값을 계산합니다. `COLUMNS(m.VALUE)`는 보간할 오른쪽 출력을 지정합니다. 보간값은 원본 행을 선택한 값과 구분해야 합니다.

21초의 계산은 `324 + (484 - 324) × (21 - 18) / (22 - 18) = 444`입니다. `MAX GAP`은 **좌우 두 실측 사이의 전체 시간차**에 대한 한계이며 기준 시각에서 양쪽으로 각각 적용하는 반경이 아닙니다. 경계와 같은 간격은 허용합니다.

정확히 같은 시각의 실측이 있으면 그 값을 사용하며 두 번째 실측이 필요하지 않습니다. 정확 일치가 없고 한쪽 실측이 없거나 간격이 너무 크면 NULL입니다. 끝값을 연장하는 외삽은 하지 않습니다.

## 타입과 입력 범위

수치 scalar와 같은 길이의 수치 ARRAY를 보간합니다. 정수·FLOAT·DOUBLE 결과는 DOUBLE로, 수치 ARRAY는 DOUBLE ARRAY로 승격됩니다. DECIMAL은 정수 자리수를 유지하면서 보간 정밀도를 확장합니다. 문자열을 보간하지 않습니다. NULL endpoint는 해당 값을 보간할 수 없습니다.

오른쪽에서 직접 참조할 수 있는 출력은 COLUMNS 계약을 따릅니다. `m.TIME`을 최종 WHERE에 추가해 입력 범위를 제한하는 대신, 오른쪽 입력 서브쿼리 안에서 필요한 범위를 거릅니다. 아래 예제는 ARRAY·DECIMAL 보간과 빈 입력도 확인합니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

두 끝점의 ARRAY는 실제 원소 수가 같아야 합니다. 선언 상한이 같아도 실제 길이가 다르면
보간 오류를 반환합니다. 길이가 같은 배열은 원소별로 보간하며 NULL 원소의 위치를 보존합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 원본 관측 보간](#example-1) | 정상 |
| 2 | [MAX GAP과 같은 간격 허용](#example-2) | 정상 |
| 3 | [최대 간격을 넘는 보간은 NULL](#example-3) | 정상 |
| 4 | [정확 일치는 다른 endpoint 없이 반환](#example-4) | 정상 |
| 5 | [ARRAY와 DECIMAL의 원소별 보간](#example-5) | 정상 |
| 6 | [빈 오른쪽 입력에서도 왼쪽 유지](#example-6) | 정상 |
| 7 | [0인 MAX GAP 거부](#example-7) | 오류 확인 |
| 8 | [COLUMNS 밖의 오른쪽 상태 직접 선택 거부](#example-8) | 오류 확인 |

## 1. 공통 데이터의 원본 관측 보간 {#example-1}

양끝 원본 시각의 전체 간격을 검사합니다. 21초는 18초=324와 22초=484에서 444가 됩니다. 60초는 외삽하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/01.json)

```sql
SELECT e.ID AS EVENT_ID,CAST((TO_TIMESTAMP(e.TIME)-1798729200000000000)/1000000000 AS LONG) AS EVENT_S,m.VALUE AS INTERPOLATED_VALUE
FROM TS13_EVENT e WITH SOURCE(ID(ID))
INTERPOLATE JOIN TS13_MOTOR m WITH SOURCE(ID(ID))
ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 120s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | EVENT_S | INTERPOLATED_VALUE |
| --- | --- | --- |
| 1 | 10 | 100 |
| 2 | 21 | 444 |
| 3 | 30 | 900 |
| 4 | 41 | 1684 |
| 5 | 46 | 2120 |
| 6 | 60 | NULL |


## 2. MAX GAP과 같은 간격 허용 {#example-2}

양끝 원본 시각의 전체 간격을 검사합니다. 21초는 18초=324와 22초=484에서 444가 됩니다. 60초는 외삽하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/02.json)

```sql
SELECT e.ID AS EVENT_ID,m.VALUE AS INTERPOLATED_VALUE
FROM TS13_EVENT e WITH SOURCE(ID(ID))
INTERPOLATE JOIN TS13_MOTOR m WITH SOURCE(ID(ID))
ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 4s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | INTERPOLATED_VALUE |
| --- | --- |
| 1 | 100 |
| 2 | 444 |
| 3 | 900 |
| 4 | 1684 |
| 5 | 2120 |
| 6 | NULL |


## 3. 최대 간격을 넘는 보간은 NULL {#example-3}

양끝 원본 시각의 전체 간격을 검사합니다. 21초는 18초=324와 22초=484에서 444가 됩니다. 60초는 외삽하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/03.json)

```sql
SELECT e.ID AS EVENT_ID,m.VALUE AS INTERPOLATED_VALUE
FROM TS13_EVENT e WITH SOURCE(ID(ID))
INTERPOLATE JOIN TS13_MOTOR m WITH SOURCE(ID(ID))
ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 3s
WHERE e.NAME='edu27_main' ORDER BY e.ID;
```

결과 **6행**입니다.

| EVENT_ID | INTERPOLATED_VALUE |
| --- | --- |
| 1 | 100 |
| 2 | NULL |
| 3 | 900 |
| 4 | NULL |
| 5 | NULL |
| 6 | NULL |


## 4. 정확 일치는 다른 endpoint 없이 반환 {#example-4}

정확한 10초 실측이 있으므로 1ns보다 먼 두 번째 관측이 필요하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/04.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e INTERPOLATE JOIN TS13_MOTOR m ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 1ns WHERE e.ID=1;
```

결과 **1행**입니다.

| ID | VALUE |
| --- | --- |
| 1 | 100 |


## 5. ARRAY와 DECIMAL의 원소별 보간 {#example-5}

정수와 ARRAY는 DOUBLE 계열로, DECIMAL은 정밀도를 보존한 확장 타입으로 반환합니다. 키가 다르거나 한쪽 endpoint가 없으면 NULL입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/05.json)

```sql
SELECT l.ID,r.V,r.AR,r.D FROM TS13_REF l TIMESTAMP(TIME) WITH SOURCE(ID(ID)) INTERPOLATE JOIN TS13_RAW r TIMESTAMP(TIME) WITH SOURCE(ID(ID)) ON l.K=r.K COLUMNS(r.V,r.AR,r.D) MAX GAP 4s ORDER BY l.ID;
```

결과 **4행**입니다.

| ID | V | AR | D |
| --- | --- | --- | --- |
| 1 | 22 | [1.0, 11.0] | 22.500000000000000 |
| 2 | 26 | [3.0, 13.0] | 26.500000000000000 |
| 3 | NULL | NULL | NULL |
| 4 | NULL | NULL | NULL |


## 6. 빈 오른쪽 입력에서도 왼쪽 유지 {#example-6}

빈 입력을 0이나 임의의 이전 값으로 대체하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/06.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e INTERPOLATE JOIN (SELECT NAME,TIME,ID,VALUE FROM TS13_MOTOR WHERE ID<0) m TIMESTAMP(TIME) ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 4s WHERE e.ID=2;
```

결과 **1행**입니다.

| ID | VALUE |
| --- | --- |
| 2 | NULL |


## 7. 0인 MAX GAP 거부 {#example-7}

최대 간격은 양수 고정 기간이어야 합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/07.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e INTERPOLATE JOIN TS13_MOTOR m ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 0s;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2379 - INTERPOLATE JOIN MAX GAP requires a positive fixed duration, such as 5m, or a positive integer nanosecond expression in parentheses.
```


## 8. COLUMNS 밖의 오른쪽 상태 직접 선택 거부 {#example-8}

보간하지 않는 ID·상태를 암묵적으로 가져오지 않습니다. 이산 상태는 별도 ASOF/LT로 조회합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/interpolate/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/interpolate/08.json)

```sql
SELECT e.ID,m.ID,m.VALUE FROM TS13_EVENT e INTERPOLATE JOIN TS13_MOTOR m ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 4s;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2378 - Column (m.ID) is unavailable after INTERPOLATE JOIN. Use an output column from COLUMNS or a supported join key.
```
