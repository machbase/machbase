---
type: docs
title: '13.5 샘플링 추가 활용'
weight: 50
toc: true
---

[SUBSAMPLE 절과 윈도 형태 전체 BNF](../../reference/sql/syntax/subsample-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

관측이 전혀 없는 장치도 동일한 출력 축에 포함하거나 집계 출력 사이에서 이전값을 전달할 때 사용합니다.

## EXPECT KEYS와 교차 PREV

EXPECT KEYS는 관측 키에 기대 키를 추가합니다. 기존 관측 키를 걸러내는 조건이 아닙니다. 특정 키만 출력하려면 입력 WHERE도 함께 사용합니다. 명시 FROM/TO와 하나의 시리즈 키가 필요하며 NULL 기대 키는 허용하지 않습니다. FILL(NONE)은 기대 키가 있어도 빈 행을 만들지 않습니다.

`PREV(alias) MAX AGE 기간`은 같은 SELECT의 다른 집계 별칭을 참조합니다. 원본·대상 타입이 맞아야 하며 값을 받는 출력의 정책에 기간을 지정합니다. 아래 사례는 두 출력에 서로 다른 기간을 줍니다.

## SUBSAMPLE 윈도 형태

윈도 형태는 원래 행마다 선택 여부 BOOL을 반환합니다. 바깥 SELECT에서 KEEP을 필터링합니다. OVER에는 ORDER BY가 필요합니다. lttb/minmax/m4/sdt에는 시각 인자가 추가되고 uniform/cadence는 OVER의 정렬 순서를 사용합니다. PARTITION BY는 sdt만 지원하며 별도의 ROWS/RANGE 프레임과 결합하지 않습니다.

[공통 준비와 정리](../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [미관측 장치 Z의 공통 축](#example-1) | 정상 |
| 2 | [미관측 버킷의 상수 표현](#example-2) | 정상 |
| 3 | [EXPECT KEYS라도 NONE은 빈 행을 만들지 않음](#example-3) | 정상 |
| 4 | [키별 LINEAR와 FROM/TO](#example-4) | 정상 |
| 5 | [교차 PREV와 출력별 서로 다른 기간](#example-5) | 정상 |
| 6 | [SUBSAMPLE 윈도 형태로 선택 여부 필터](#example-6) | 정상 |
| 7 | [EXPECT KEYS의 출력 범위 누락](#example-7) | 오류 확인 |
| 8 | [PREV 대상 별칭 부재](#example-8) | 오류 확인 |

## 1. 미관측 장치 Z의 공통 축 {#example-1}

기대 키는 하나의 시리즈 키와 명시 출력 범위에 사용합니다. 값이 없는 키에 가짜 관측 근거를 만들지 않습니다. 기대 키는 관측 키를 제한하는 목록이 아닙니다. 여기서는 WHERE로 입력을 A로 제한합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/01.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS SECOND,V
FROM (SELECT NAME,TIME AS B,MAX(VALUE) AS V FROM TS13_FILL
 WHERE NAME='A' SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(NULL)
 EXPECT KEYS('A','Z')) s ORDER BY NAME,B;
```

결과 **12행** 중 앞 8행입니다.

| NAME | SECOND | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | NULL |
| A | 2 | 24 |
| A | 3 | NULL |
| A | 4 | NULL |
| A | 5 | 30 |
| Z | 0 | NULL |
| Z | 1 | NULL |


## 2. 미관측 버킷의 상수 표현 {#example-2}

기대 키는 하나의 시리즈 키와 명시 출력 범위에 사용합니다. 값이 없는 키에 가짜 관측 근거를 만들지 않습니다. 기대 키는 관측 키를 제한하는 목록이 아닙니다. 여기서는 WHERE로 입력을 A로 제한합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/02.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS SECOND,V
FROM (SELECT NAME,TIME AS B,MAX(VALUE) AS V FROM TS13_FILL
 WHERE NAME='A' SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(0)
 EXPECT KEYS('A','Z')) s ORDER BY NAME,B;
```

결과 **12행** 중 앞 8행입니다.

| NAME | SECOND | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 0 |
| A | 2 | 24 |
| A | 3 | 0 |
| A | 4 | 0 |
| A | 5 | 30 |
| Z | 0 | 0 |
| Z | 1 | 0 |


## 3. EXPECT KEYS라도 NONE은 빈 행을 만들지 않음 {#example-3}

기대 키는 하나의 시리즈 키와 명시 출력 범위에 사용합니다. 값이 없는 키에 가짜 관측 근거를 만들지 않습니다. 기대 키는 관측 키를 제한하는 목록이 아닙니다. 여기서는 WHERE로 입력을 A로 제한합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/03.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS SECOND,V
FROM (SELECT NAME,TIME AS B,MAX(VALUE) AS V FROM TS13_FILL
 WHERE NAME='A' SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(NONE)
 EXPECT KEYS('A','Z')) s ORDER BY NAME,B;
```

결과 **3행**입니다.

| NAME | SECOND | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 2 | 24 |
| A | 5 | 30 |


## 4. 키별 LINEAR와 FROM/TO {#example-4}

기대 키는 하나의 시리즈 키와 명시 출력 범위에 사용합니다. 값이 없는 키에 가짜 관측 근거를 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/04.json)

```sql
SELECT NAME,CAST((TO_TIMESTAMP(B)-1798729200000000000)/1000000000 AS LONG) AS SECOND,V
FROM (SELECT NAME,TIME AS B,MAX(VALUE) AS V FROM TS13_FILL
 WHERE NAME IN('A','B') SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729206000000000) FILL(LINEAR MAX GAP 4s)
 EXPECT KEYS('A','B','Z')) s ORDER BY NAME,B;
```

결과 **18행** 중 앞 8행입니다.

| NAME | SECOND | V |
| --- | --- | --- |
| A | 0 | 20 |
| A | 1 | 22 |
| A | 2 | 24 |
| A | 3 | 26 |
| A | 4 | 28 |
| A | 5 | 30 |
| B | 0 | NULL |
| B | 1 | 10 |


## 5. 교차 PREV와 출력별 서로 다른 기간 {#example-5}

0초 버킷의 AVG는 20, MAX는 30입니다. 1초의 A는 이전 B=30, B는 이전 A=20을 받습니다. 채운 값으로 근거 시각을 갱신하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/05.json)

```sql
SELECT CAST((TO_TIMESTAMP(BUCKET)-1798729200000000000)/1000000000 AS LONG) AS SECOND,A,B
FROM (SELECT TIME AS BUCKET,AVG(V) AS A,MAX(V) AS B FROM TS13_MIX TIMESTAMP(TIME)
 SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729204000000000)
 FILL(PREV(B) MAX AGE 2s,PREV(A) MAX AGE 1s)) s ORDER BY BUCKET;
```

결과 **4행**입니다.

| SECOND | A | B |
| --- | --- | --- |
| 0 | 20 | 30 |
| 1 | 30 | 20 |
| 2 | 40 | 40 |
| 3 | 40 | 40 |


## 6. SUBSAMPLE 윈도 형태로 선택 여부 필터 {#example-6}

윈도 함수는 BOOL 선택 여부를 반환하고 바깥 WHERE로 원본 행을 고릅니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/06.json)

```sql
SELECT ID,V FROM (SELECT ID,TIME,V,lttb(TIME,V,4) OVER(ORDER BY TIME) AS KEEP FROM TS13_SUB) s WHERE KEEP ORDER BY TIME;
```

결과 **4행**입니다.

| ID | V |
| --- | --- |
| 0 | 0 |
| 3 | 7 |
| 4 | -1 |
| 7 | 3 |


## 7. EXPECT KEYS의 출력 범위 누락 {#example-7}

미관측 시리즈를 만들려면 FROM/TO와 하나의 키를 지정합니다. 기대 키는 관측 키를 제한하는 목록이 아닙니다. 여기서는 WHERE로 입력을 A로 제한합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/07.json)

```sql
SELECT NAME,TIME,MAX(VALUE) FROM TS13_FILL SAMPLE BY 1s FILL(NULL) EXPECT KEYS('A','Z');
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (EXPECT KEYS requires one key and FROM/TO).
```


## 8. PREV 대상 별칭 부재 {#example-8}

동일 SELECT에 공개된 집계 별칭을 참조합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/advanced/sampling/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/advanced/sampling/08.json)

```sql
SELECT TIME,AVG(V) AS A FROM TS13_MIX TIMESTAMP(TIME) SAMPLE BY 1s FROM FROM_TIMESTAMP(1798729200000000000) TO FROM_TIMESTAMP(1798729203000000000) FILL(PREV(MISSING) MAX AGE 2s);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2374 - Invalid FILL PREV reference (MISSING). The alias does not exist in the SELECT outputs.
```
