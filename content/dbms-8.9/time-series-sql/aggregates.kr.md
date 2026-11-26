---
type: docs
title: '13.7 선택 집계와 보정 합계'
weight: 70
toc: true
---

[선택 집계·보정 합계 함수 문법](../../reference/sql/functions/aggregation/#first_not_null)에서 작성 순서와 인자 제약을 확인합니다.

값과 선택 기준을 분리하거나 큰 수의 상쇄가 있는 합계를 계산합니다.

| 함수 | 의미 |
|---|---|
| FIRST_NOT_NULL(value) | 입력 순서의 처음 NULL 아닌 값 |
| LAST_NOT_NULL(value) | 입력 순서의 마지막 NULL 아닌 값 |
| ARG_MIN(value,key) | 최소 유효 key 행의 value |
| ARG_MAX(value,key) | 최대 유효 key 행의 value |
| KSUM(value) | 보정 항을 사용하는 부동소수점 합계 |
| NSUM(value) | 크기가 다른 값의 누적을 보정하는 합계 |

FIRST_NOT_NULL/LAST_NOT_NULL은 시각을 자동 정렬하지 않습니다. 결정적인 입력 ORDER BY를 지정합니다. ARG_MIN/ARG_MAX는 key가 같으면 먼저 입력된 행을 유지합니다. 선택 행의 value가 NULL이면 그대로 NULL이며 다음 후보를 고르지 않습니다. NULL·NaN key는 제외합니다.

선택 결과는 value 타입을 보존하며 DECIMAL 정밀도·스케일과 ARRAY payload도 보존합니다. 빈 입력은 NULL입니다. ARRAY를 ARG_MIN/ARG_MAX의 비교 key로 사용할 수 없습니다.

KSUM은 Kahan, NSUM은 Neumaier 알고리즘을 사용하며 입력을 DOUBLE로 변환해 결과도 DOUBLE로 반환합니다. NULL·비유한 값은 제외합니다. 유효 입력이 없거나 누적·최종 결과가 비유한 값이면 NULL입니다.

보정 합계도 유한 정밀도의 부동소수점 계산입니다. 모든 입력에서 수학적으로 정확한 답을 보장하지 않습니다. `1e16, 1, -1e16` 사례에서 일반 SUM·KSUM·NSUM의 실제 결과를 비교합니다. 소수의 정확한 계산이 필요하면 DECIMAL 사용 여부를 별도로 결정합니다.

[공통 준비와 정리](../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [입력 순서와 극값 key로 선택](#example-1) | 정상 |
| 2 | [입력 순서를 뒤집은 동률 선택](#example-2) | 정상 |
| 3 | [NULL value를 입력에서 명시 제외](#example-3) | 정상 |
| 4 | [모든 value와 key가 NULL](#example-4) | 정상 |
| 5 | [입력이 없는 집계](#example-5) | 정상 |
| 6 | [DECIMAL payload 타입 보존](#example-6) | 정상 |
| 7 | [큰 값의 상쇄에서 KSUM과 NSUM 비교](#example-7) | 정상 |
| 8 | [일반 유효 관측의 보정 합계](#example-8) | 정상 |
| 9 | [ARRAY를 선택 key로 사용 거부](#example-9) | 오류 확인 |
| 10 | [인자 수가 맞지 않는 선택 집계](#example-10) | 오류 확인 |

## 1. 입력 순서와 극값 key로 선택 {#example-1}

ARG_MIN/MAX의 동률은 먼저 입력된 행을 유지합니다. 선택된 value가 NULL이어도 더 먼 비NULL 후보로 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/01.json)

```sql
SELECT FIRST_NOT_NULL(V),LAST_NOT_NULL(V),ARG_MIN(V,Q),ARG_MAX(V,Q) FROM (SELECT ID,K,V,Q,P FROM TS13_AGG  ORDER BY ID) s;
```

결과 **1행**입니다.

| FIRST_NOT_NULL(V) | LAST_NOT_NULL(V) | ARG_MIN(V,Q) | ARG_MAX(V,Q) |
| --- | --- | --- | --- |
| 20 | 40 | 20 | NULL |


## 2. 입력 순서를 뒤집은 동률 선택 {#example-2}

ARG_MIN/MAX의 동률은 먼저 입력된 행을 유지합니다. 선택된 value가 NULL이어도 더 먼 비NULL 후보로 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/02.json)

```sql
SELECT FIRST_NOT_NULL(V),LAST_NOT_NULL(V),ARG_MIN(V,Q),ARG_MAX(V,Q) FROM (SELECT ID,K,V,Q,P FROM TS13_AGG  ORDER BY ID DESC) s;
```

결과 **1행**입니다.

| FIRST_NOT_NULL(V) | LAST_NOT_NULL(V) | ARG_MIN(V,Q) | ARG_MAX(V,Q) |
| --- | --- | --- | --- |
| 40 | 20 | 30 | NULL |


## 3. NULL value를 입력에서 명시 제외 {#example-3}

ARG_MIN/MAX의 동률은 먼저 입력된 행을 유지합니다. 선택된 value가 NULL이어도 더 먼 비NULL 후보로 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/03.json)

```sql
SELECT FIRST_NOT_NULL(V),LAST_NOT_NULL(V),ARG_MIN(V,Q),ARG_MAX(V,Q) FROM (SELECT ID,K,V,Q,P FROM TS13_AGG WHERE V IS NOT NULL ORDER BY ID) s;
```

결과 **1행**입니다.

| FIRST_NOT_NULL(V) | LAST_NOT_NULL(V) | ARG_MIN(V,Q) | ARG_MAX(V,Q) |
| --- | --- | --- | --- |
| 20 | 40 | 20 | 20 |


## 4. 모든 value와 key가 NULL {#example-4}

ARG_MIN/MAX의 동률은 먼저 입력된 행을 유지합니다. 선택된 value가 NULL이어도 더 먼 비NULL 후보로 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/04.json)

```sql
SELECT FIRST_NOT_NULL(V),LAST_NOT_NULL(V),ARG_MIN(V,Q),ARG_MAX(V,Q) FROM (SELECT ID,K,V,Q,P FROM TS13_AGG WHERE K=2 ORDER BY ID) s;
```

결과 **1행**입니다.

| FIRST_NOT_NULL(V) | LAST_NOT_NULL(V) | ARG_MIN(V,Q) | ARG_MAX(V,Q) |
| --- | --- | --- | --- |
| NULL | NULL | NULL | NULL |


## 5. 입력이 없는 집계 {#example-5}

ARG_MIN/MAX의 동률은 먼저 입력된 행을 유지합니다. 선택된 value가 NULL이어도 더 먼 비NULL 후보로 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/05.json)

```sql
SELECT FIRST_NOT_NULL(V),LAST_NOT_NULL(V),ARG_MIN(V,Q),ARG_MAX(V,Q) FROM (SELECT ID,K,V,Q,P FROM TS13_AGG WHERE ID<0 ORDER BY ID) s;
```

결과 **1행**입니다.

| FIRST_NOT_NULL(V) | LAST_NOT_NULL(V) | ARG_MIN(V,Q) | ARG_MAX(V,Q) |
| --- | --- | --- | --- |
| NULL | NULL | NULL | NULL |


## 6. DECIMAL payload 타입 보존 {#example-6}

ARG_MIN/MAX의 동률은 먼저 입력된 행을 유지합니다. 선택된 value가 NULL이어도 더 먼 비NULL 후보로 바꾸지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/06.json)

```sql
SELECT FIRST_NOT_NULL(P),LAST_NOT_NULL(P),ARG_MIN(P,Q) FROM (SELECT ID,K,V,Q,P FROM TS13_AGG  ORDER BY ID) s;
```

결과 **1행**입니다.

| FIRST_NOT_NULL(P) | LAST_NOT_NULL(P) | ARG_MIN(P,Q) |
| --- | --- | --- |
| 20.25 | 40.25 | 20.25 |


## 7. 큰 값의 상쇄에서 KSUM과 NSUM 비교 {#example-7}

1e16,1,-1e16의 순서에서 보정 알고리즘의 차이를 봅니다. 임의 정밀도의 정확한 합계를 보장하는 함수는 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/07.json)

```sql
SELECT SUM(V),KSUM(V),NSUM(V) FROM (SELECT ID,V FROM TS13_SUM ORDER BY ID) s;
```

결과 **1행**입니다.

| SUM(V) | KSUM(V) | NSUM(V) |
| --- | --- | --- |
| 0 | 0 | 1 |


## 8. 일반 유효 관측의 보정 합계 {#example-8}

NULL·비유한 값은 제외합니다. 입력 순서가 수치 결과에 미치는 영향을 이해합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/08.json)

```sql
SELECT KSUM(V),NSUM(V) FROM TS13_AGG WHERE K=1;
```

결과 **1행**입니다.

| KSUM(V) | NSUM(V) |
| --- | --- |
| 90 | 90 |


## 9. ARRAY를 선택 key로 사용 거부 {#example-9}

value의 지원 타입과 key의 지원 타입은 다릅니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/09.json)

```sql
SELECT ARG_MIN(V,AR) FROM TS13_RAW;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2037 - Function [ARG_MIN] argument data type does not match.
```


## 10. 인자 수가 맞지 않는 선택 집계 {#example-10}

ARG_MAX는 value,key 두 인자를 받습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/aggregates/10.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/aggregates/10.json)

```sql
SELECT ARG_MAX(V) FROM TS13_AGG;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2036 - Function [ARG_MAX] has an invalid argument.
```
