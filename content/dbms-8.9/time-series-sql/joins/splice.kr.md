---
type: docs
title: '13.1.8 SPLICE JOIN: 양쪽 관측의 변화 시점'
weight: 80
toc: true
---

[시계열 JOIN·TIMESTAMP·TIE 전체 BNF](../../../reference/sql/syntax/time-series-join-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

양쪽 입력 시각의 합집합에서 상태를 출력합니다. 한쪽에 새 관측이 오면 반대쪽의 직전 상태를 유지합니다. 같은 시각의 사건은 합쳐지며, 출력 컬럼의 시각은 각 원본 관측의 시각입니다.

21초 사건은 event 21초·motor 18초 상태를, 22초 사건은 event 21초·motor 22초 상태를 출력합니다. 따라서 같은 event 시각이 여러 결과 행에 나타날 수 있습니다.

공통 데이터의 전체 사건 축은 22행입니다. 첫 event 이전 motor 사건에서 event는 NULL입니다. 최종 WHERE에 event의 NAME·TIME 조건을 적용하면 앞의 3행이 빠져 공통 데이터의 19행이 됩니다. **19행은 필터를 적용한 결과이며 SPLICE의 고정 행 수가 아닙니다.** 마지막 60초 사건은 motor 50초의 상태를 유지합니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [전체 사건 시간축 22행](#example-1) | 정상 |
| 2 | [공통 데이터의 event 존재 조건 19행](#example-2) | 정상 |
| 3 | [21초 이벤트가 carry되는 구간](#example-3) | 정상 |
| 4 | [오른쪽 없는 사건 확인](#example-4) | 정상 |
| 5 | [첫 event 이전 motor 사건](#example-5) | 정상 |
| 6 | [마지막 이벤트와 직전 motor 상태](#example-6) | 정상 |
| 7 | [동등 관계가 아닌 ON 키 거부](#example-7) | 오류 확인 |
| 8 | [명시 시간축 없는 입력 거부](#example-8) | 오류 확인 |

## 1. 전체 사건 시간축 22행 {#example-1}

양쪽 사건 시각에서 상대쪽 최신 상태를 이어 붙입니다. 19행은 event가 존재하는 결과만 남긴 조건의 결과이며 전체 합집합은 22행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/01.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.NAME=m.NAME
 ORDER BY CASE WHEN e.ID IS NULL THEN 0 ELSE e.ID END,m.ID;
```

결과 **22행** 중 앞 8행입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| NULL | 101 | 0 |
| NULL | 102 | 16 |
| NULL | 103 | 64 |
| 1 | 104 | 100 |
| 1 | 105 | 144 |
| 1 | 106 | 256 |
| 1 | 107 | 324 |
| 2 | 107 | 324 |


## 2. 공통 데이터의 event 존재 조건 19행 {#example-2}

양쪽 사건 시각에서 상대쪽 최신 상태를 이어 붙입니다. 19행은 event가 존재하는 결과만 남긴 조건의 결과이며 전체 합집합은 22행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/02.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.ID IS NOT NULL ORDER BY CASE WHEN e.ID IS NULL THEN 0 ELSE e.ID END,m.ID;
```

결과 **19행** 중 앞 8행입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 1 | 104 | 100 |
| 1 | 105 | 144 |
| 1 | 106 | 256 |
| 1 | 107 | 324 |
| 2 | 107 | 324 |
| 2 | 108 | 484 |
| 2 | 109 | 576 |
| 2 | 110 | 784 |


## 3. 21초 이벤트가 carry되는 구간 {#example-3}

양쪽 사건 시각에서 상대쪽 최신 상태를 이어 붙입니다. 19행은 event가 존재하는 결과만 남긴 조건의 결과이며 전체 합집합은 22행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/03.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.ID=2 ORDER BY CASE WHEN e.ID IS NULL THEN 0 ELSE e.ID END,m.ID;
```

결과 **4행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 2 | 107 | 324 |
| 2 | 108 | 484 |
| 2 | 109 | 576 |
| 2 | 110 | 784 |


## 4. 오른쪽 없는 사건 확인 {#example-4}

양쪽 사건 시각에서 상대쪽 최신 상태를 이어 붙입니다. 19행은 event가 존재하는 결과만 남긴 조건의 결과이며 전체 합집합은 22행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/04.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE m.ID IS NULL ORDER BY CASE WHEN e.ID IS NULL THEN 0 ELSE e.ID END,m.ID;
```

결과 **0행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |


## 5. 첫 event 이전 motor 사건 {#example-5}

양쪽 사건 시각에서 상대쪽 최신 상태를 이어 붙입니다. 19행은 event가 존재하는 결과만 남긴 조건의 결과이며 전체 합집합은 22행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/05.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.ID IS NULL ORDER BY CASE WHEN e.ID IS NULL THEN 0 ELSE e.ID END,m.ID;
```

결과 **3행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| NULL | 101 | 0 |
| NULL | 102 | 16 |
| NULL | 103 | 64 |


## 6. 마지막 이벤트와 직전 motor 상태 {#example-6}

양쪽 사건 시각에서 상대쪽 최신 상태를 이어 붙입니다. 19행은 event가 존재하는 결과만 남긴 조건의 결과이며 전체 합집합은 22행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/06.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID,m.VALUE AS MOTOR_VALUE
FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.NAME=m.NAME
WHERE e.ID=6 ORDER BY CASE WHEN e.ID IS NULL THEN 0 ELSE e.ID END,m.ID;
```

결과 **1행**입니다.

| EVENT_ID | MOTOR_ID | MOTOR_VALUE |
| --- | --- | --- |
| 6 | 118 | 2500 |


## 7. 동등 관계가 아닌 ON 키 거부 {#example-7}

SPLICE는 양측의 동등 키로 연결합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/07.json)

```sql
SELECT e.ID FROM TS13_EVENT e SPLICE JOIN TS13_MOTOR m ON e.VALUE>m.VALUE;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_JOIN_ON_OP).
```


## 8. 명시 시간축 없는 입력 거부 {#example-8}

LOG의 시간축을 TIMESTAMP로 지정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/splice/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/splice/08.json)

```sql
SELECT l.ID FROM TS13_L l SPLICE JOIN TS13_R r ON l.K=r.K;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
