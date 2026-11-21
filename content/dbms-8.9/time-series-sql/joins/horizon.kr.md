---
type: docs
title: '13.1.6 HORIZON JOIN: 여러 오프셋 시각의 조회'
weight: 60
toc: true
---

각 이벤트에 여러 시간 오프셋을 더한 뒤 각 시각에서 ASOF를 수행합니다. `LIST(-1m, 0, 1m) AS h`는 이벤트별로 세 행을 만듭니다. `h.offset`은 나노초 정수이며 원래 이벤트 시각은 유지됩니다.

21초 이벤트의 조회 시각은 −39·21·81초입니다. 허용차를 생략하면 각각 NULL·18초·50초 관측을 선택합니다. 미래 오프셋의 조회도 그 조회 시각 이전 상태를 선택하는 ASOF입니다. 공통 데이터에서는 이벤트 6개 × 오프셋 3개로 18행이 됩니다.

LIST는 증가하는 오프셋을 지정합니다. RANGE는 FROM·TO·STEP으로 생성하며 TO 이하의 마지막 오프셋까지 출력합니다. HORIZON 오프셋에는 ns/us/ms/s/m/h/d를 사용하며 월·년·주 단위와 복합 오프셋은 지원하지 않습니다. 시간대를 바꾸는 연산으로 사용하지 않습니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 전·현재·후 조회](#example-1) | 정상 |
| 2 | [RANGE의 마지막 TO 이하 offset](#example-2) | 정상 |
| 3 | [현재 시각 한 점](#example-3) | 정상 |
| 4 | [초 단위 전후 상태](#example-4) | 정상 |
| 5 | [FROM과 TO가 같은 한 점](#example-5) | 정상 |
| 6 | [양끝을 포함하는 일정 간격](#example-6) | 정상 |
| 7 | [역순 LIST 거부](#example-7) | 오류 확인 |
| 8 | [HORIZON의 월 단위 거부](#example-8) | 오류 확인 |

## 1. 공통 데이터의 전·현재·후 조회 {#example-1}

이벤트마다 offset 행을 생성하고 이벤트 시각+offset에서 ASOF를 수행합니다. 후보가 없어도 offset 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/01.json)

```sql
SELECT e.ID AS EVENT_ID,CAST((TO_TIMESTAMP(e.TIME)-1798729200000000000)/1000000000 AS LONG) AS EVENT_S,
 h.offset AS OFFSET_NS,CAST((TO_TIMESTAMP(h.timestamp)-1798729200000000000)/1000000000 AS LONG) AS QUERY_S,
 CAST((TO_TIMESTAMP(m.TIME)-1798729200000000000)/1000000000 AS LONG) AS MOTOR_S,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME
LIST(-1m,0,1m) AS h WHERE e.NAME='edu27_main' ORDER BY e.ID,h.offset;
```

결과 **18행** 중 앞 8행입니다.

| EVENT_ID | EVENT_S | OFFSET_NS | QUERY_S | MOTOR_S | MOTOR_VALUE |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | -60000000000 | -50 | NULL | NULL |
| 1 | 10 | 0 | 10 | 10 | 100 |
| 1 | 10 | 60000000000 | 70 | 50 | 2500 |
| 2 | 21 | -60000000000 | -39 | NULL | NULL |
| 2 | 21 | 0 | 21 | 18 | 324 |
| 2 | 21 | 60000000000 | 81 | 50 | 2500 |
| 3 | 30 | -60000000000 | -30 | NULL | NULL |
| 3 | 30 | 0 | 30 | 30 | 900 |


## 2. RANGE의 마지막 TO 이하 offset {#example-2}

이벤트마다 offset 행을 생성하고 이벤트 시각+offset에서 ASOF를 수행합니다. 후보가 없어도 offset 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/02.json)

```sql
SELECT e.ID AS EVENT_ID,h.offset AS OFFSET_NS,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE FROM -1s TO 4s STEP 2s AS h WHERE e.NAME='edu27_main' ORDER BY e.ID,h.offset;
```

결과 **18행** 중 앞 8행입니다.

| EVENT_ID | OFFSET_NS | MOTOR_VALUE |
| --- | --- | --- |
| 1 | -1000000000 | 64 |
| 1 | 1000000000 | 100 |
| 1 | 3000000000 | 144 |
| 2 | -1000000000 | 324 |
| 2 | 1000000000 | 484 |
| 2 | 3000000000 | 576 |
| 3 | -1000000000 | 784 |
| 3 | 1000000000 | 900 |


## 3. 현재 시각 한 점 {#example-3}

이벤트마다 offset 행을 생성하고 이벤트 시각+offset에서 ASOF를 수행합니다. 후보가 없어도 offset 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/03.json)

```sql
SELECT e.ID AS EVENT_ID,h.offset AS OFFSET_NS,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME
LIST(0) AS h WHERE e.NAME='edu27_main' ORDER BY e.ID,h.offset;
```

결과 **6행**입니다.

| EVENT_ID | OFFSET_NS | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 0 | 100 |
| 2 | 0 | 324 |
| 3 | 0 | 900 |
| 4 | 0 | 1444 |
| 5 | 0 | 1936 |
| 6 | 0 | 2500 |


## 4. 초 단위 전후 상태 {#example-4}

이벤트마다 offset 행을 생성하고 이벤트 시각+offset에서 ASOF를 수행합니다. 후보가 없어도 offset 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/04.json)

```sql
SELECT e.ID AS EVENT_ID,h.offset AS OFFSET_NS,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME
LIST(-1s,0,1s) AS h WHERE e.NAME='edu27_main' ORDER BY e.ID,h.offset;
```

결과 **18행** 중 앞 8행입니다.

| EVENT_ID | OFFSET_NS | MOTOR_VALUE |
| --- | --- | --- |
| 1 | -1000000000 | 64 |
| 1 | 0 | 100 |
| 1 | 1000000000 | 100 |
| 2 | -1000000000 | 324 |
| 2 | 0 | 324 |
| 2 | 1000000000 | 484 |
| 3 | -1000000000 | 784 |
| 3 | 0 | 900 |


## 5. FROM과 TO가 같은 한 점 {#example-5}

이벤트마다 offset 행을 생성하고 이벤트 시각+offset에서 ASOF를 수행합니다. 후보가 없어도 offset 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/05.json)

```sql
SELECT e.ID AS EVENT_ID,h.offset AS OFFSET_NS,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE FROM 1s TO 1s STEP 1s AS h WHERE e.NAME='edu27_main' ORDER BY e.ID,h.offset;
```

결과 **6행**입니다.

| EVENT_ID | OFFSET_NS | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 1000000000 | 100 |
| 2 | 1000000000 | 484 |
| 3 | 1000000000 | 900 |
| 4 | 1000000000 | 1764 |
| 5 | 1000000000 | 1936 |
| 6 | 1000000000 | 2500 |


## 6. 양끝을 포함하는 일정 간격 {#example-6}

이벤트마다 offset 행을 생성하고 이벤트 시각+offset에서 ASOF를 수행합니다. 후보가 없어도 offset 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/06.json)

```sql
SELECT e.ID AS EVENT_ID,h.offset AS OFFSET_NS,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME
RANGE FROM -2s TO 2s STEP 2s AS h WHERE e.NAME='edu27_main' ORDER BY e.ID,h.offset;
```

결과 **18행** 중 앞 8행입니다.

| EVENT_ID | OFFSET_NS | MOTOR_VALUE |
| --- | --- | --- |
| 1 | -2000000000 | 64 |
| 1 | 0 | 100 |
| 1 | 2000000000 | 144 |
| 2 | -2000000000 | 324 |
| 2 | 0 | 324 |
| 2 | 2000000000 | 484 |
| 3 | -2000000000 | 784 |
| 3 | 0 | 900 |


## 7. 역순 LIST 거부 {#example-7}

LIST는 중복 없이 오름차순으로 지정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/07.json)

```sql
SELECT e.ID FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME LIST(1s,0) AS h;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_HORIZON_ORDER).
```


## 8. HORIZON의 월 단위 거부 {#example-8}

offset은 ns/us/ms/s/m/h/d의 단일 고정 단위를 사용합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/horizon/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/horizon/08.json)

```sql
SELECT e.ID FROM TS13_EVENT e HORIZON JOIN TS13_MOTOR m ON e.NAME=m.NAME LIST(1mo) AS h;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2382 - Invalid HORIZON offset. Use a signed literal with one unit (ns, us, ms, s, m, h, d), or 0 without a unit.
```
