---
type: docs
title: '13.3.4 입력 범위와 출력 범위'
weight: 40
toc: true
---

WHERE는 집계·채움에 사용할 원본 관측을 제한합니다. SAMPLE의 FROM/TO는 출력할 버킷 범위 `[FROM,TO)`를 정합니다. TO 시각은 결과에 포함하지 않습니다. WHERE의 종료 시각만 넓혀도 출력 축이 자동으로 그 시각까지 늘어나지 않습니다.

출력 첫 버킷을 보간하려면 FROM 이전 실측이 필요할 수 있습니다. 이 실측을 입력 WHERE에서 제거하지 않으면 채움 근거로 사용합니다. 반대로 WHERE로 제거한 실측은 FILL이 다시 읽지 않습니다. 입력은 넓게 받고 출력은 원하는 구간으로 좁히는 예제를 비교합니다.

FROM과 TO가 같으면 결과는 0행입니다. 역순 범위는 오류입니다. 명시 FROM/TO는 CALENDAR 정렬에서 사용하며 FIRST OBSERVATION과 함께 사용할 수 없습니다. 예제는 FROM_TIMESTAMP의 절대 나노초 시각으로 입력 문자열의 세션 해석 차이를 피합니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [WHERE만으로 출력 축이 늘어나지 않음](#example-1) | 정상 |
| 2 | [출력 TO는 제외](#example-2) | 정상 |
| 3 | [FROM 밖 실제 근거로 첫 출력 보간](#example-3) | 정상 |
| 4 | [WHERE가 endpoint를 제거하면 다시 찾지 않음](#example-4) | 정상 |
| 5 | [빈 출력 범위](#example-5) | 정상 |
| 6 | [왼쪽 바깥 출력은 PREV 근거가 없으면 NULL](#example-6) | 정상 |
| 7 | [역순 출력 범위 거부](#example-7) | 오류 확인 |
| 8 | [FIRST OBSERVATION과 명시 범위 충돌](#example-8) | 오류 확인 |

## 1. WHERE만으로 출력 축이 늘어나지 않음 {#example-1}

WHERE는 입력 관측을, FROM/TO는 출력 축을 제한합니다. 입력에서 제거한 근거를 다시 조회하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/01.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s  FILL(NONE)
) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 5 | 30 |


## 2. 출력 TO는 제외 {#example-2}

WHERE는 입력 관측을, FROM/TO는 출력 축을 제한합니다. 입력에서 제거한 근거를 다시 조회하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/02.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729205000000000) FILL(NULL)
) s ORDER BY NAME,B;
```

결과 **5행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | NULL |
| A | 2 | 24 |
| A | 3 | NULL |
| A | 4 | NULL |


## 3. FROM 밖 실제 근거로 첫 출력 보간 {#example-3}

WHERE는 입력 관측을, FROM/TO는 출력 축을 제한합니다. 입력에서 제거한 근거를 다시 조회하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/03.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729201000000000) TO FROM_TIMESTAMP(1798729205000000000) FILL(LINEAR MAX GAP 4s)
) s ORDER BY NAME,B;
```

결과 **4행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 1 | 22 |
| A | 2 | 24 |
| A | 3 | 26 |
| A | 4 | 28 |


## 4. WHERE가 endpoint를 제거하면 다시 찾지 않음 {#example-4}

WHERE는 입력 관측을, FROM/TO는 출력 축을 제한합니다. 입력에서 제거한 근거를 다시 조회하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/04.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A' AND TIME>=FROM_TIMESTAMP(1798729202000000000)
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729201000000000) TO FROM_TIMESTAMP(1798729205000000000) FILL(LINEAR MAX GAP 4s)
) s ORDER BY NAME,B;
```

결과 **4행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | 1 | NULL |
| A | 2 | 24 |
| A | 3 | 26 |
| A | 4 | 28 |


## 5. 빈 출력 범위 {#example-5}

WHERE는 입력 관측을, FROM/TO는 출력 축을 제한합니다. 입력에서 제거한 근거를 다시 조회하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/05.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729202000000000) TO FROM_TIMESTAMP(1798729202000000000) FILL(NULL)
) s ORDER BY NAME,B;
```

결과 **0행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |


## 6. 왼쪽 바깥 출력은 PREV 근거가 없으면 NULL {#example-6}

WHERE는 입력 관측을, FROM/TO는 출력 축을 제한합니다. 입력에서 제거한 근거를 다시 조회하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/06.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729199000000000) TO FROM_TIMESTAMP(1798729203000000000) FILL(PREV MAX AGE 2s)
) s ORDER BY NAME,B;
```

결과 **4행**입니다.

| NAME | BUCKET | V |
| --- | --- | --- |
| A | -1 | NULL |
| A | 0 | 20 |
| A | 1 | 20 |
| A | 2 | 24 |


## 7. 역순 출력 범위 거부 {#example-7}

FROM은 TO보다 늦을 수 없습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/07.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729206000000000) TO FROM_TIMESTAMP(1798729200000000000) FILL(NULL)
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2229 - Invalid argument value for function (SAMPLE FROM/TO).
```


## 8. FIRST OBSERVATION과 명시 범위 충돌 {#example-8}

명시 출력 범위와 FIRST OBSERVATION을 함께 사용하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/bounds/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/bounds/08.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS BUCKET,V FROM (
SELECT NAME,TIME AS B,AVG(VALUE) AS V FROM TS13_FILL
WHERE NAME='A'
SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(NULL) ALIGN TO FIRST OBSERVATION
) s ORDER BY NAME,B;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2384 - SAMPLE BY FROM/TO requires ALIGN TO CALENDAR or the default alignment.
```
