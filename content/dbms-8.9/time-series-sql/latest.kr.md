---
type: docs
title: '13.2 LATEST ON: 태그별 최신값 조회'
weight: 20
toc: true
---

[LATEST ON 전체 BNF](../../reference/sql/syntax/latest-on-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

태그나 그룹마다 최신 관측 한 행을 반환합니다. `LATEST ON TIME PARTITION BY NAME`에서 TIME은 비교할 DATETIME 컬럼이며 PARTITION BY는 그룹 키입니다. TAG는 기본 시간축을 사용할 수 있고 다른 입력은 TIMESTAMP로 시간축을 지정합니다.

WHERE를 통과한 입력에서 최신값을 선택합니다. 시간 범위를 제한하면 전체 데이터의 최신값이 아니라 그 범위 안의 최신값을 반환합니다. 값 조건도 먼저 적용하므로 최신 관측이 그 조건을 만족하지 않으면 이전의 적격 관측이 선택될 수 있습니다. 입력이 없는 그룹의 행을 자동으로 만들지 않습니다.

## 키와 순서

결과 출력 순서는 바깥 ORDER BY로 정합니다. 최신 시각에 후보가 겹치면 논리 순서가 필요하며 기본 중복 정책은 오류입니다. LATEST에 지정한 컬럼은 지정 시간축과 일치해야 합니다.

복합 PARTITION BY에서 VARCHAR가 마지막이 아닌 구성은 동일 그룹의 최신 한 행으로 축약되지 않을 수 있습니다. 복합 키 예제는 **고정 길이 수치 키 K, 마지막 VARCHAR 키 REGION** 순서를 사용합니다. 문자열 키 여러 개를 조합하는 구성에는 이 예제의 동작을 일반화하지 않습니다.

[공통 준비와 정리](../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [모든 장치의 최신 행](#example-1) | 정상 |
| 2 | [지정 시간 범위 안의 최신 행](#example-2) | 정상 |
| 3 | [특정 장치 집합](#example-3) | 정상 |
| 4 | [WHERE로 입력 지역 제한](#example-4) | 정상 |
| 5 | [최신 선택 전 값 필터](#example-5) | 정상 |
| 6 | [입력이 없는 장치](#example-6) | 정상 |
| 7 | [복합 partition 키](#example-7) | 정상 |
| 8 | [DATETIME이 아닌 LATEST 축 거부](#example-8) | 오류 확인 |
| 9 | [최신 시각의 중복은 기본 오류](#example-9) | 오류 확인 |

## 1. 모든 장치의 최신 행 {#example-1}

WHERE를 통과한 입력에서 키별 최신 원본 행을 고릅니다. 삽입 순서나 전체 최댓값이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/01.json)

```sql
SELECT NAME,VALUE FROM TS13_STATUS  LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```

결과 **3행**입니다.

| NAME | VALUE |
| --- | --- |
| alpha | 5 |
| beta | 42 |
| gamma | 18 |


## 2. 지정 시간 범위 안의 최신 행 {#example-2}

WHERE를 통과한 입력에서 키별 최신 원본 행을 고릅니다. 삽입 순서나 전체 최댓값이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/02.json)

```sql
SELECT NAME,VALUE FROM TS13_STATUS WHERE TIME<FROM_TIMESTAMP(1798729210000000000) LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```

결과 **3행**입니다.

| NAME | VALUE |
| --- | --- |
| alpha | 1 |
| beta | 30 |
| gamma | 18 |


## 3. 특정 장치 집합 {#example-3}

WHERE를 통과한 입력에서 키별 최신 원본 행을 고릅니다. 삽입 순서나 전체 최댓값이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/03.json)

```sql
SELECT NAME,VALUE FROM TS13_STATUS WHERE NAME IN ('alpha','gamma') LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```

결과 **2행**입니다.

| NAME | VALUE |
| --- | --- |
| alpha | 5 |
| gamma | 18 |


## 4. WHERE로 입력 지역 제한 {#example-4}

WHERE를 통과한 입력에서 키별 최신 원본 행을 고릅니다. 삽입 순서나 전체 최댓값이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/04.json)

```sql
SELECT NAME,VALUE FROM TS13_STATUS WHERE REGION='N' LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```

결과 **2행**입니다.

| NAME | VALUE |
| --- | --- |
| alpha | 5 |
| gamma | 18 |


## 5. 최신 선택 전 값 필터 {#example-5}

WHERE를 통과한 입력에서 키별 최신 원본 행을 고릅니다. 삽입 순서나 전체 최댓값이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/05.json)

```sql
SELECT NAME,VALUE FROM TS13_STATUS WHERE VALUE<10 LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```

결과 **1행**입니다.

| NAME | VALUE |
| --- | --- |
| alpha | 5 |


## 6. 입력이 없는 장치 {#example-6}

WHERE를 통과한 입력에서 키별 최신 원본 행을 고릅니다. 삽입 순서나 전체 최댓값이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/06.json)

```sql
SELECT NAME,VALUE FROM TS13_STATUS WHERE NAME='missing' LATEST ON TIME PARTITION BY NAME ORDER BY NAME;
```

결과 **0행**입니다.

| NAME | VALUE |
| --- | --- |


## 7. 복합 partition 키 {#example-7}

숫자 장치 키를 앞에, 가변 길이 문자열 키를 마지막에 배치합니다. 본문의 현재 복합 문자열 키 제약을 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/07.json)

```sql
SELECT K,REGION,VALUE FROM TS13_KEYS TIMESTAMP(TIME) LATEST ON TIME PARTITION BY K,REGION ORDER BY K,REGION;
```

결과 **3행**입니다.

| K | REGION | VALUE |
| --- | --- | --- |
| 1 | N | 5 |
| 2 | S | 42 |
| 3 | N | 18 |


## 8. DATETIME이 아닌 LATEST 축 거부 {#example-8}

LATEST의 시각은 지정 DATETIME 시간축과 같아야 합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/08.json)

```sql
SELECT ID FROM TS13_TIES TIMESTAMP(TIME) LATEST ON ID PARTITION BY K;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_TYPE).
```


## 9. 최신 시각의 중복은 기본 오류 {#example-9}

최신 시각 동률에는 비NULL·고유한 순서 키로 TIE를 명시합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/latest/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/latest/09.json)

```sql
SELECT l.ID FROM TS13_TIES l TIMESTAMP(TIME) WHERE l.TIME<FROM_TIMESTAMP(1798729220000000000) LATEST ON TIME PARTITION BY K;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TIE_CONFLICT).
```
