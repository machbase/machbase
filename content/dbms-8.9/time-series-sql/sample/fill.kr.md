---
type: docs
title: '13.3.2 FILL 정책 비교'
weight: 20
toc: true
---

관측이 없는 버킷을 어떤 값으로 출력할지 정합니다. 실제 관측의 집계값이 NULL인 경우와 관측 자체가 없는 버킷은 구분합니다.

| 정책 | 빈 버킷 처리 |
|---|---|
| 생략 또는 NONE | 해당 행을 생략 |
| NULL | NULL로 출력 |
| 상수 | 해당 집계 출력 타입으로 검사한 값 |
| PREV MAX AGE 2s | 원래 관측 버킷에서 2초 이내이면 이전값 |
| LINEAR MAX GAP 3s | 앞뒤 관측 버킷 간격이 3초 이내이면 선형 보간 |

단일 정책은 집계 출력 전체에 적용합니다. `AVG(VALUE), COUNT(*)`에 `FILL(NULL,0)`을 주면 빈 버킷 평균은 NULL, 건수는 0입니다. 여러 정책의 순서는 공개 집계 출력 순서이며 시각·시리즈 키는 개수에 포함하지 않습니다. NONE은 다른 정책과 섞지 않습니다.

PREV는 채운 버킷을 새 관측으로 간주하지 않습니다. 최대 나이는 원래 관측 버킷으로부터 계산하며 경계를 포함합니다. PREV에는 MAX AGE, LINEAR에는 MAX GAP의 양수 고정 기간을 반드시 지정합니다. 기간 누락은 ERR-02369, 0이나 월·년 등 유효하지 않은 고정 기간은 ERR-02370입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [빈 버킷 행 생략](#example-1) | 정상 |
| 2 | [빈 버킷을 NULL로 표현](#example-2) | 정상 |
| 3 | [상수 0으로 표현](#example-3) | 정상 |
| 4 | [원래 관측으로부터 2초까지 유지](#example-4) | 정상 |
| 5 | [채운 값으로 유효 기간을 갱신하지 않음](#example-5) | 정상 |
| 6 | [버킷 집계 사이를 선형 보간](#example-6) | 정상 |
| 7 | [집계 출력마다 다른 정책](#example-7) | 정상 |
| 8 | [PREV 기간 누락](#example-8) | 오류 확인 |
| 9 | [0인 LINEAR 최대 간격](#example-9) | 오류 확인 |

## 1. 빈 버킷 행 생략 {#example-1}

빈 버킷만 채웁니다. 실제 관측 NULL과 관측 없는 버킷을 같은 것으로 처리하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/01.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(NONE)
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 5 | 30 |


## 2. 빈 버킷을 NULL로 표현 {#example-2}

빈 버킷만 채웁니다. 실제 관측 NULL과 관측 없는 버킷을 같은 것으로 처리하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/02.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(NULL)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | NULL |
| A | 2 | 24 |
| A | 3 | NULL |
| A | 4 | NULL |
| A | 5 | 30 |


## 3. 상수 0으로 표현 {#example-3}

빈 버킷만 채웁니다. 실제 관측 NULL과 관측 없는 버킷을 같은 것으로 처리하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/03.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(0)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 0 |
| A | 2 | 24 |
| A | 3 | 0 |
| A | 4 | 0 |
| A | 5 | 30 |


## 4. 원래 관측으로부터 2초까지 유지 {#example-4}

빈 버킷만 채웁니다. 실제 관측 NULL과 관측 없는 버킷을 같은 것으로 처리하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/04.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(PREV MAX AGE 2s)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 20 |
| A | 2 | 24 |
| A | 3 | 24 |
| A | 4 | 24 |
| A | 5 | 30 |


## 5. 채운 값으로 유효 기간을 갱신하지 않음 {#example-5}

빈 버킷만 채웁니다. 실제 관측 NULL과 관측 없는 버킷을 같은 것으로 처리하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/05.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(PREV MAX AGE 1s)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 20 |
| A | 2 | 24 |
| A | 3 | 24 |
| A | 4 | NULL |
| A | 5 | 30 |


## 6. 버킷 집계 사이를 선형 보간 {#example-6}

빈 버킷만 채웁니다. 실제 관측 NULL과 관측 없는 버킷을 같은 것으로 처리하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/06.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 4s)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 22 |
| A | 2 | 24 |
| A | 3 | 26 |
| A | 4 | 28 |
| A | 5 | 30 |


## 7. 집계 출력마다 다른 정책 {#example-7}

정책 개수는 공개 집계 출력 개수와 순서입니다. 시각·시리즈 키는 포함하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/07.json)

```sql
SELECT CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V,N FROM (
 SELECT TIME AS B,AVG(VALUE) AS V,COUNT(*) AS N FROM TS13_FILL
 WHERE NAME='A' SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(NULL,0)
) s ORDER BY B;
```

결과 **6행**입니다.

| BUCKET | V | N |
| --- | --- | --- |
| 0 | 20 | 1 |
| 1 | NULL | 0 |
| 2 | 24 | 1 |
| 3 | NULL | 0 |
| 4 | NULL | 0 |
| 5 | 30 | 1 |


## 8. PREV 기간 누락 {#example-8}

PREV MAX AGE에 양수 고정 기간을 지정합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/08.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(PREV)
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2369 - Specify a duration in the FILL policy, for example FILL(PREV MAX AGE 2s).
```


## 9. 0인 LINEAR 최대 간격 {#example-9}

LINEAR MAX GAP은 양수입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/fill/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/fill/09.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 0s)
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2370 - FILL(LINEAR MAX GAP) requires a positive fixed duration, such as 2s or 1m30s.
```
