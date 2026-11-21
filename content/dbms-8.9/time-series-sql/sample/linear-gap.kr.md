---
type: docs
title: '13.3.3 LINEAR와 MAX GAP'
weight: 30
toc: true
---

LINEAR는 원본 관측을 먼저 버킷별로 집계한 후 **실제 관측이 있는 두 버킷** 사이를 보간합니다. 원본 행 시각 사이를 직접 보간하는 INTERPOLATE JOIN과 구분합니다.

A의 0초=20과 2초=24 사이에는 1초=22가 만들어집니다. 2초=24와 5초=30의 간격은 3초이므로 MAX GAP 3s에서는 3초=26·4초=28을 만들고, MAX GAP 2s에서는 두 버킷을 NULL로 둡니다. 허용 간격과 같은 경계는 포함합니다.

한쪽 endpoint가 없거나 값이 NULL이면 보간하지 않으며 외삽하지 않습니다. 실제 관측 버킷의 NULL은 빈 버킷으로 바꾸어 덮어쓰지 않습니다. NULL 관측 예제는 NULL 측정값을 허용하는 LOG TS13_NULL을 사용합니다.

수치 scalar와 수치 ARRAY를 지원하며 정수·부동소수점은 DOUBLE 계열로 승격합니다. DECIMAL은 정수 자리수를 보존하는 확장 타입을 사용합니다. 고정 최대 기간에는 ns/us/ms/s/m/h/d/w 및 복합 기간을 사용하고 mo/y는 사용하지 않습니다. LINEAR의 시리즈 키는 숨은 GROUP 키를 포함해 최대 하나입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [3초 endpoint 간격을 허용](#example-1) | 정상 |
| 2 | [최대 간격 경계 포함](#example-2) | 정상 |
| 3 | [간격 초과 구간은 NULL](#example-3) | 정상 |
| 4 | [모든 비정확 버킷의 간격 초과](#example-4) | 정상 |
| 5 | [양끝 밖으로 외삽하지 않음](#example-5) | 정상 |
| 6 | [실제 관측 NULL을 덮어쓰지 않음](#example-6) | 정상 |
| 7 | [LINEAR 기간 누락](#example-7) | 오류 확인 |
| 8 | [고정 기간에 월 사용 거부](#example-8) | 오류 확인 |

## 1. 3초 endpoint 간격을 허용 {#example-1}

최대 간격은 현재 출력점에서 한쪽까지의 거리가 아니라 앞뒤 실제 관측 버킷 사이 전체 간격입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/01.json)

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


## 2. 최대 간격 경계 포함 {#example-2}

최대 간격은 현재 출력점에서 한쪽까지의 거리가 아니라 앞뒤 실제 관측 버킷 사이 전체 간격입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/02.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 3s)
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


## 3. 간격 초과 구간은 NULL {#example-3}

최대 간격은 현재 출력점에서 한쪽까지의 거리가 아니라 앞뒤 실제 관측 버킷 사이 전체 간격입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/03.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 2s)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 22 |
| A | 2 | 24 |
| A | 3 | NULL |
| A | 4 | NULL |
| A | 5 | 30 |


## 4. 모든 비정확 버킷의 간격 초과 {#example-4}

최대 간격은 현재 출력점에서 한쪽까지의 거리가 아니라 앞뒤 실제 관측 버킷 사이 전체 간격입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/04.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 1s)
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


## 5. 양끝 밖으로 외삽하지 않음 {#example-5}

왼쪽 또는 오른쪽 실제 endpoint가 없는 바깥 구간은 NULL입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/05.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729199000000000) TO FROM_TIMESTAMP(1798729207000000000) FILL(LINEAR MAX GAP 4s)
) s ORDER BY NAME,B;
```

결과 **8행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | -1 | NULL |
| A | 0 | 20 |
| A | 1 | 22 |
| A | 2 | 24 |
| A | 3 | 26 |
| A | 4 | 28 |
| A | 5 | 30 |
| A | 6 | NULL |


## 6. 실제 관측 NULL을 덮어쓰지 않음 {#example-6}

0초의 실제 NULL은 보간으로 바꾸지 않습니다. NULL endpoint를 건너뛰어 더 먼 근거를 찾지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/06.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_NULL TIMESTAMP(TIME)
WHERE NAME='N'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 4s)
) s ORDER BY NAME,B;
```

결과 **6행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| N | 0 | NULL |
| N | 1 | NULL |
| N | 2 | 24 |
| N | 3 | 26 |
| N | 4 | 28 |
| N | 5 | 30 |


## 7. LINEAR 기간 누락 {#example-7}

무제한 기본값과 세션 fallback은 없습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/07.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR)
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2369 - Specify a duration in the FILL policy, for example FILL(LINEAR MAX GAP 2s).
```


## 8. 고정 기간에 월 사용 거부 {#example-8}

달력 월과 고정 시간 한계를 구분합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/linear-gap/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/linear-gap/08.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 1mo)
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2370 - FILL(LINEAR MAX GAP) requires a positive fixed duration, such as 2s or 1m30s.
```
