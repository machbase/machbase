---
type: docs
title: '13.3.1 시간 구간별 집계'
weight: 10
toc: true
---

SAMPLE BY는 시간축을 일정한 버킷으로 묶고 AVG·MIN·MAX·SUM·COUNT 등의 집계를 계산합니다. SELECT의 지정 시각은 각 버킷의 시작 시각으로 출력됩니다. 비집계 시리즈 키는 시리즈를 분리합니다.

TS13_FILL의 A는 0·2·5초에 각각 20·24·30을 관측했습니다. 기본 1초 샘플링은 관측이 있는 3개 버킷만 반환합니다. 2초 간격이면 5초 관측이 `[4,6)` 버킷에 포함되어 4초로 출력됩니다.

## 간격

단위는 ns/us/ms/s/m/h/d/w/mo/y이며 숫자와 단위를 붙여 `1s`, `15m`, `1mo`처럼 씁니다. 간격은 양수의 단일 단위입니다. SAMPLE BY의 간격과 FILL의 최대 기간은 서로 다른 인자입니다. 월·년 간격을 고정 초 수로 해석하지 않습니다.

TAG는 BASETIME을 기본 시간축으로 사용합니다. LOG와 파생 입력은 `TIMESTAMP(TM)`으로 DATETIME 축을 지정합니다. 집계 전 WHERE를 적용하고, 집계가 끝난 뒤 FILL을 적용합니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 관측 버킷만 반환](#example-1) | 정상 |
| 2 | [COUNT로 관측 수 집계](#example-2) | 정상 |
| 3 | [2초 버킷의 집계](#example-3) | 정상 |
| 4 | [모든 관측을 10초 버킷으로 집계](#example-4) | 정상 |
| 5 | [버킷별 합계](#example-5) | 정상 |
| 6 | [다른 장치와 분리된 버킷](#example-6) | 정상 |
| 7 | [0 간격 거부](#example-7) | 오류 확인 |
| 8 | [분리한 숫자와 단위 거부](#example-8) | 오류 확인 |

## 1. 공통 데이터의 관측 버킷만 반환 {#example-1}

SAMPLE은 입력을 버킷별로 집계합니다. FILL을 생략하면 관측 없는 버킷 행을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/01.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 5 | 30 |


## 2. COUNT로 관측 수 집계 {#example-2}

SAMPLE은 입력을 버킷별로 집계합니다. FILL을 생략하면 관측 없는 버킷 행을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/02.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,COUNT(*) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 1 |
| A | 2 | 1 |
| A | 5 | 1 |


## 3. 2초 버킷의 집계 {#example-3}

SAMPLE은 입력을 버킷별로 집계합니다. FILL을 생략하면 관측 없는 버킷 행을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/03.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 2s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 4 | 30 |


## 4. 모든 관측을 10초 버킷으로 집계 {#example-4}

SAMPLE은 입력을 버킷별로 집계합니다. FILL을 생략하면 관측 없는 버킷 행을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/04.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 10s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **1행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 24.66666667 |


## 5. 버킷별 합계 {#example-5}

SAMPLE은 입력을 버킷별로 집계합니다. FILL을 생략하면 관측 없는 버킷 행을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/05.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,SUM(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 2s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 4 | 30 |


## 6. 다른 장치와 분리된 버킷 {#example-6}

SAMPLE은 입력을 버킷별로 집계합니다. FILL을 생략하면 관측 없는 버킷 행을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/06.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME IN('A','B')
SAMPLE BY 1s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **5행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 5 | 30 |
| B | 1 | 10 |
| B | 4 | 16 |


## 7. 0 간격 거부 {#example-7}

양수 간격을 지정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/07.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 0s
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2380 - SAMPLE BY requires a positive interval with one unit: ns, us, ms, s, m, h, d, w, mo, or y. Examples: 1ns, 1mo.
```


## 8. 분리한 숫자와 단위 거부 {#example-8}

숫자와 단위는 붙여 씁니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/basic/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/basic/08.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1 s
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2380 - SAMPLE BY requires a positive interval with one unit: ns, us, ms, s, m, h, d, w, mo, or y. Examples: 1ns, 1mo.
```
