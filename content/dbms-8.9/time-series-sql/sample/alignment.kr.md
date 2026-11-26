---
type: docs
title: '13.3.5 ALIGN TO와 시간대'
weight: 50
toc: true
---

[SAMPLE·FILL·ALIGN·EXPECT KEYS 전체 BNF](../../../reference/sql/syntax/sample-fill-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

ALIGN TO는 버킷의 원점을 정합니다. 기본 CALENDAR는 세션의 UTC 오프셋을 사용합니다. 실행 환경에 관계없이 같은 경계를 얻으려면 `ALIGN TO CALENDAR TIME ZONE 'UTC'` 또는 지역 이름을 명시합니다.

TIME ZONE은 버킷 경계만 정하며 WHERE 문자열의 해석과 결과 DATETIME 표시 시간대를 바꾸지 않습니다. 서울 자정은 UTC 전날 15시, 방콕 자정은 UTC 전날 17시입니다. 일간 집계는 달라지지만 정수 시간 차이인 두 지역의 1시간 버킷 경계는 같을 수 있습니다.

`WITH OFFSET '00:30'`은 달력 경계를 30분 이동합니다. ALIGN TO FIRST OBSERVATION은 WHERE를 통과한 시리즈별 최소 관측 시각을 원점으로 사용합니다. 물리 입력 순서가 아닙니다. 이 정렬에는 명시 FROM/TO를 함께 쓰지 않습니다.

CALENDAR의 명시 FROM은 출력 원점도 정합니다. 예제에서는 1초에서 시작하는 2초 간격으로 1·3·5·7초를 만듭니다. 지역 달력의 하루는 DST 전환 때 23시간 또는 25시간일 수 있습니다. Europe/Berlin의 봄·가을 사례로 이를 확인합니다.

TIME ZONE에는 제품에 포함된 IANA 지역 이름을 사용합니다. `Asia/Seoul`, `Asia/Bangkok`, `Europe/Berlin`, `UTC`를 예제로 제공합니다. 숫자 오프셋 문자열을 지역 이름처럼 지정하지 않습니다. 고정 MAX AGE/MAX GAP의 1d는 24시간으로, 지역 달력 하루와 구분합니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [UTC 자정 기준](#example-1) | 정상 |
| 2 | [서울 자정 기준](#example-2) | 정상 |
| 3 | [방콕 자정 기준](#example-3) | 정상 |
| 4 | [OFFSET으로 자정 경계 30분 이동](#example-4) | 정상 |
| 5 | [달력 경계의 공통 2초 버킷](#example-5) | 정상 |
| 6 | [시리즈별 첫 관측의 2초 버킷](#example-6) | 정상 |
| 7 | [FROM으로 1초 원점의 2초 축 지정](#example-7) | 정상 |
| 8 | [DST 전환의 23시간 달력 하루](#example-8) | 정상 |
| 9 | [DST 전환의 25시간 달력 하루](#example-9) | 정상 |
| 10 | [숫자 offset을 TIME ZONE 이름으로 쓰지 않음](#example-10) | 오류 확인 |
| 11 | [OFFSET의 잘못된 시각 형식](#example-11) | 오류 확인 |

## 1. UTC 자정 기준 {#example-1}

TIME ZONE은 버킷 경계의 기준입니다. WHERE 문자열과 결과 DATETIME 표시 시간대를 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/01.json)

```sql
SELECT TO_TIMESTAMP(BUCKET) AS BUCKET_NS,N FROM (
 SELECT TIME AS BUCKET,COUNT(*) AS N FROM TS13_MOTOR
 WHERE NAME='edu27_main' SAMPLE BY 1d ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY BUCKET;
```

결과 **1행**입니다.

| BUCKET_NS | N |
| --- | --- |
| 1798675200000000000 | 18 |


## 2. 서울 자정 기준 {#example-2}

TIME ZONE은 버킷 경계의 기준입니다. WHERE 문자열과 결과 DATETIME 표시 시간대를 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/02.json)

```sql
SELECT TO_TIMESTAMP(BUCKET) AS BUCKET_NS,N FROM (
 SELECT TIME AS BUCKET,COUNT(*) AS N FROM TS13_MOTOR
 WHERE NAME='edu27_main' SAMPLE BY 1d ALIGN TO CALENDAR TIME ZONE 'Asia/Seoul'
) s ORDER BY BUCKET;
```

결과 **1행**입니다.

| BUCKET_NS | N |
| --- | --- |
| 1798729200000000000 | 18 |


## 3. 방콕 자정 기준 {#example-3}

TIME ZONE은 버킷 경계의 기준입니다. WHERE 문자열과 결과 DATETIME 표시 시간대를 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/03.json)

```sql
SELECT TO_TIMESTAMP(BUCKET) AS BUCKET_NS,N FROM (
 SELECT TIME AS BUCKET,COUNT(*) AS N FROM TS13_MOTOR
 WHERE NAME='edu27_main' SAMPLE BY 1d ALIGN TO CALENDAR TIME ZONE 'Asia/Bangkok'
) s ORDER BY BUCKET;
```

결과 **1행**입니다.

| BUCKET_NS | N |
| --- | --- |
| 1798650000000000000 | 18 |


## 4. OFFSET으로 자정 경계 30분 이동 {#example-4}

자정 직후의 입력은 전날 00:30에서 시작한 버킷에 들어갑니다. OFFSET은 시간대 이름이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/04.json)

```sql
SELECT TO_TIMESTAMP(BUCKET) AS BUCKET_NS,N FROM (
 SELECT TIME AS BUCKET,COUNT(*) AS N FROM TS13_MOTOR WHERE NAME='edu27_main'
 SAMPLE BY 1d ALIGN TO CALENDAR TIME ZONE 'Asia/Seoul' WITH OFFSET '00:30'
) s ORDER BY BUCKET;
```

결과 **1행**입니다.

| BUCKET_NS | N |
| --- | --- |
| 1798644600000000000 | 18 |


## 5. 달력 경계의 공통 2초 버킷 {#example-5}

FIRST OBSERVATION은 물리 삽입 순서가 아니라 WHERE 통과 후 시리즈별 최소 관측 시각입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/05.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME IN('A','B')
SAMPLE BY 2s   ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **5행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 4 | 30 |
| B | 0 | 10 |
| B | 4 | 16 |


## 6. 시리즈별 첫 관측의 2초 버킷 {#example-6}

FIRST OBSERVATION은 물리 삽입 순서가 아니라 WHERE 통과 후 시리즈별 최소 관측 시각입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/06.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME IN('A','B')
SAMPLE BY 2s   ALIGN TO FIRST OBSERVATION
) s ORDER BY NAME,B;
```

결과 **5행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 4 | 30 |
| B | 1 | 10 |
| B | 3 | 16 |


## 7. FROM으로 1초 원점의 2초 축 지정 {#example-7}

명시 FROM은 출력의 시작이자 버킷 원점입니다. [1,3) 버킷은 2초 관측을 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/07.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 2s FROM FROM_TIMESTAMP(1798729201000000000) TO FROM_TIMESTAMP(1798729207000000000) FILL(NULL) ALIGN TO CALENDAR TIME ZONE 'UTC'
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 1 | 24 |
| A | 3 | NULL |
| A | 5 | 30 |


## 8. DST 전환의 23시간 달력 하루 {#example-8}

지역 달력의 하루는 고정 24시간과 다릅니다. ns 값을 UTC 시각으로 읽으면 자정 경계의 변화가 보입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/08.json)

```sql
SELECT TO_TIMESTAMP(BUCKET) AS BUCKET_NS,N FROM (
 SELECT TIME AS BUCKET,COUNT(*) AS N FROM TS13_CAL TIMESTAMP(TIME)
 WHERE TIME>=FROM_TIMESTAMP(1711670400000000000) AND TIME<FROM_TIMESTAMP(1712016000000000000)
 SAMPLE BY 1d ALIGN TO CALENDAR TIME ZONE 'Europe/Berlin'
) s ORDER BY BUCKET;
```

결과 **3행**입니다.

| BUCKET_NS | N |
| --- | --- |
| 1711753200000000000 | 1 |
| 1711839600000000000 | 1 |
| 1711922400000000000 | 1 |


## 9. DST 전환의 25시간 달력 하루 {#example-9}

지역 달력의 하루는 고정 24시간과 다릅니다. ns 값을 UTC 시각으로 읽으면 자정 경계의 변화가 보입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/09.json)

```sql
SELECT TO_TIMESTAMP(BUCKET) AS BUCKET_NS,N FROM (
 SELECT TIME AS BUCKET,COUNT(*) AS N FROM TS13_CAL TIMESTAMP(TIME)
 WHERE TIME>=FROM_TIMESTAMP(1729814400000000000) AND TIME<FROM_TIMESTAMP(1730160000000000000)
 SAMPLE BY 1d ALIGN TO CALENDAR TIME ZONE 'Europe/Berlin'
) s ORDER BY BUCKET;
```

결과 **3행**입니다.

| BUCKET_NS | N |
| --- | --- |
| 1729893600000000000 | 1 |
| 1729980000000000000 | 1 |
| 1730070000000000000 | 1 |


## 10. 숫자 offset을 TIME ZONE 이름으로 쓰지 않음 {#example-10}

지원되는 IANA 이름 또는 UTC를 사용합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/10.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/10.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s   ALIGN TO CALENDAR TIME ZONE '+09:00'
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2229 - Invalid argument value for function (TIME ZONE).
```


## 11. OFFSET의 잘못된 시각 형식 {#example-11}

OFFSET은 유효한 HH:MI 형식의 경계 이동입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/alignment/11.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/alignment/11.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s   ALIGN TO CALENDAR WITH OFFSET '25:00'
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2229 - Invalid argument value for function (SAMPLE WITH OFFSET).
```
