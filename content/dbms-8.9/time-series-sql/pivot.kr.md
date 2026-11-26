---
type: docs
title: '13.8 PIVOT으로 시계열 비교하기'
weight: 80
toc: true
---

[PIVOT 전체 BNF](../../reference/sql/syntax/pivot-syntax/#pivot-bnf)에서 작성 순서와 인자 제약을 확인합니다.

시리즈별 세로형 관측을 열로 펼칩니다. 같은 시간·그룹의 값을 나란히 비교하거나 복수 집계를 함께 출력할 수 있습니다.

IN 목록 순서가 결과 열 순서이며 키별로 집계식 순서를 따릅니다. 복수 집계는 `IN별칭_집계별칭`으로 열 이름을 만듭니다. 단일 집계의 별칭을 생략하면 IN 별칭만 사용합니다. 셀에 SUM(V)*2 같은 집계 결과 식도 지정할 수 있습니다.

GROUP BY를 생략하면 입력에서 FOR 키와 집계 인자를 제외한 열이 암묵적 그룹 키가 됩니다. 명시 GROUP BY는 지정한 식만 그룹으로 사용합니다. 불필요한 입력 열 때문에 그룹이 쪼개지는 경우를 비교합니다. 존재하는 그룹의 빈 COUNT 셀은 0이며, PIVOT 결과 행 전체가 OUTER JOIN에서 미매칭된 경우의 NULL과 구분합니다.

동적 IN SELECT는 한 열을 반환하며 prepare 시 결과 스키마가 결정됩니다. 같은 준비문을 재실행해도 새 키 열은 추가되지 않습니다. 새 열이 필요하면 다시 prepare합니다. IN SELECT의 ORDER BY로 열 순서를 정합니다. 이 스키마 결정 SELECT에는 바인드를 사용할 수 없습니다.

동일 키 중복은 ERR-02385입니다. 서로 다른 키가 같은 결과 열 이름을 만들거나 목록이 비었거나 여러 열을 반환하면 오류입니다. 문자열 'NULL'과 SQL NULL은 다릅니다.

[공통 준비와 정리](../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [정적 시리즈 열과 빈 셀](#example-1) | 정상 |
| 2 | [빈 셀 COUNT는 0](#example-2) | 정상 |
| 3 | [복수 집계와 출력 열 순서](#example-3) | 정상 |
| 4 | [집계 결과를 사용하는 셀 표현식](#example-4) | 정상 |
| 5 | [IN 순서가 결과 열 순서](#example-5) | 정상 |
| 6 | [prepare에서 결정하는 동적 IN](#example-6) | 정상 |
| 7 | [명시 GROUP BY로만 그룹 구성](#example-7) | 정상 |
| 8 | [중복 pivot 값 거부](#example-8) | 오류 확인 |
| 9 | [동적 IN의 다중 열 거부](#example-9) | 오류 확인 |

## 1. 정적 시리즈 열과 빈 셀 {#example-1}

PIVOT은 기존 기능의 확장입니다. 동적 IN은 실행마다 열 구성을 바꾸지 않으며 새 키는 다시 prepare합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/01.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(SUM(V) FOR K IN (1 AS K1,2 AS K2,3 AS K3));
```

결과 **1행**입니다.

| K1 | K2 | K3 |
| --- | --- | --- |
| 74 | 12 | NULL |


## 2. 빈 셀 COUNT는 0 {#example-2}

PIVOT은 기존 기능의 확장입니다. 동적 IN은 실행마다 열 구성을 바꾸지 않으며 새 키는 다시 prepare합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/02.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(COUNT(V) FOR K IN (1 AS K1,2 AS K2,3 AS K3));
```

결과 **1행**입니다.

| K1 | K2 | K3 |
| --- | --- | --- |
| 3 | 2 | 0 |


## 3. 복수 집계와 출력 열 순서 {#example-3}

PIVOT은 기존 기능의 확장입니다. 동적 IN은 실행마다 열 구성을 바꾸지 않으며 새 키는 다시 prepare합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/03.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(SUM(V) AS TOTAL,COUNT(V) AS N FOR K IN (1 AS K1,2 AS K2,3 AS K3));
```

결과 **1행**입니다.

| K1_TOTAL | K1_N | K2_TOTAL | K2_N | K3_TOTAL | K3_N |
| --- | --- | --- | --- | --- | --- |
| 74 | 3 | 12 | 2 | NULL | 0 |


## 4. 집계 결과를 사용하는 셀 표현식 {#example-4}

PIVOT은 기존 기능의 확장입니다. 동적 IN은 실행마다 열 구성을 바꾸지 않으며 새 키는 다시 prepare합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/04.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(AVG(V)+1 AS ADJUSTED FOR K IN (1 AS K1,2 AS K2));
```

결과 **1행**입니다.

| K1_ADJUSTED | K2_ADJUSTED |
| --- | --- |
| 25.66666667 | 7 |


## 5. IN 순서가 결과 열 순서 {#example-5}

PIVOT은 기존 기능의 확장입니다. 동적 IN은 실행마다 열 구성을 바꾸지 않으며 새 키는 다시 prepare합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/05.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(SUM(V) FOR K IN (2 AS K2,1 AS K1));
```

결과 **1행**입니다.

| K2 | K1 |
| --- | --- |
| 12 | 74 |


## 6. prepare에서 결정하는 동적 IN {#example-6}

PIVOT은 기존 기능의 확장입니다. 동적 IN은 실행마다 열 구성을 바꾸지 않으며 새 키는 다시 prepare합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/06.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(SUM(V) FOR K IN (SELECT DISTINCT K FROM TS13_PIVOT ORDER BY K));
```

결과 **1행**입니다.

| 1 | 2 |
| --- | --- |
| 74 | 12 |


## 7. 명시 GROUP BY로만 그룹 구성 {#example-7}

GROUP BY 생략 시 남는 입력 열이 암묵 그룹 키가 되는 것과 구분합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/07.json)

```sql
SELECT * FROM (SELECT ID,K,V FROM TS13_PIVOT) PIVOT(SUM(V) FOR K IN(1 AS K1,2 AS K2) GROUP BY ID) ORDER BY ID;
```

결과 **5행**입니다.

| ID | K1 | K2 |
| --- | --- | --- |
| 1 | 20 | NULL |
| 2 | 24 | NULL |
| 3 | 30 | NULL |
| 4 | NULL | 5 |
| 5 | NULL | 7 |


## 8. 중복 pivot 값 거부 {#example-8}

같은 typed key를 서로 다른 별칭으로 반복하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/08.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(SUM(V) FOR K IN(1 AS A,1 AS B));
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2385 - PIVOT IN values must be distinct.
```


## 9. 동적 IN의 다중 열 거부 {#example-9}

결과 스키마를 정하는 조회는 한 열이어야 합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/pivot/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/pivot/09.json)

```sql
SELECT * FROM (SELECT K,V FROM TS13_PIVOT) PIVOT(SUM(V) FOR K IN(SELECT K,V FROM TS13_PIVOT));
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_PIVOT_SCHEMA_ARITY).
```
