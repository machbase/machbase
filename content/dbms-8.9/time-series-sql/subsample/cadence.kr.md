---
type: docs
title: '13.4.5 CADENCE: 일정 행 간격으로 선택'
weight: 50
toc: true
---

[SUBSAMPLE 절과 윈도 형태 전체 BNF](../../../reference/sql/syntax/subsample-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

stride 3은 ID 0·3·6·7을 선택합니다. 마지막 행 보존 때문에 단순히 stride의 배수 행만 반환하는 것은 아닙니다. seed를 생략하면 offset은 0이며 정수 seed는 같은 입력에 재현 가능한 선택을 만듭니다. stride 1은 모든 행, stride가 입력 수보다 크면 첫 행을 선택합니다.

구문 인자는 `cadence(stride[, seed])`입니다. 절 형태는 지정 시각 컬럼을 SELECT에 직접 포함해야 합니다. 아래 SQL의 TIME_NS는 표시 시간대에 영향받지 않는 원본 시각 확인용입니다.

stride는 1~2147483647의 정수입니다. value 기반 알고리즘의 DECIMAL 인자는 지원하지 않지만 선택된 행의 별도 DECIMAL·ARRAY·문자열 payload는 유지됩니다. LTTB·MINMAX·M4는 NULL 시각과 NULL·NaN·Inf 값을 후보에서 제외하며 UNIFORM·CADENCE는 값과 무관하게 행을 셉니다.

![원본 신호와 CADENCE 선택점 비교](/assets/dbms-8.9/time-series-sql/plots/cadence.svg)

회색 선은 원본, 색 점은 선택 관측입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [세 행 간격과 마지막 행](#example-1) | 정상 |
| 2 | [명시 seed 0과 두 행 간격](#example-2) | 정상 |
| 3 | [stride 1은 모든 행](#example-3) | 정상 |
| 4 | [유효하지 않은 알고리즘 인자](#example-4) | 오류 확인 |
| 5 | [선택 시각을 출력하지 않은 절 형태](#example-5) | 오류 확인 |
| 6 | [stride 3과 명시 seed 1](#example-6) | 정상 |

## 1. 세 행 간격과 마지막 행 {#example-1}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/cadence/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/cadence/01.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE cadence(3) ORDER BY TIME;
```

결과 **4행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 6 | 2027-01-01 00:00:06 | 1 | 1798729206000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 2. 명시 seed 0과 두 행 간격 {#example-2}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/cadence/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/cadence/02.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE cadence(2,0) ORDER BY TIME;
```

결과 **5행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 2 | 2027-01-01 00:00:02 | 2 | 1798729202000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |
| 6 | 2027-01-01 00:00:06 | 1 | 1798729206000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 3. stride 1은 모든 행 {#example-3}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/cadence/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/cadence/03.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE cadence(1) ORDER BY TIME;
```

결과 **8행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 1 | 2027-01-01 00:00:01 | 4 | 1798729201000000000 |
| 2 | 2027-01-01 00:00:02 | 2 | 1798729202000000000 |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |
| 5 | 2027-01-01 00:00:05 | 5 | 1798729205000000000 |
| 6 | 2027-01-01 00:00:06 | 1 | 1798729206000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 4. 유효하지 않은 알고리즘 인자 {#example-4}

target은 2 이상, stride는 1 이상, SDT 허용 편차는 유한한 0 이상이어야 합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/cadence/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/cadence/04.json)

```sql
SELECT ID,TIME,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE cadence(0);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_SUBSAMPLE_TARGET).
```


## 5. 선택 시각을 출력하지 않은 절 형태 {#example-5}

절 형태는 지정 시각 컬럼을 SELECT에 직접 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/cadence/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/cadence/05.json)

```sql
SELECT ID,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE cadence(3);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```


## 6. stride 3과 명시 seed 1 {#example-6}

동일 입력에서 명시 seed 1의 선택 위치를 확인합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/cadence/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/cadence/06.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE cadence(3,1) ORDER BY TIME;
```

결과 **3행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |
