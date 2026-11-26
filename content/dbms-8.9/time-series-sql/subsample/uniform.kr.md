---
type: docs
title: '13.4.4 UNIFORM: 행 위치의 균등 선택'
weight: 40
toc: true
---

[SUBSAMPLE 절과 윈도 형태 전체 BNF](../../../reference/sql/syntax/subsample-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

값의 크기와 관계없이 행 위치를 고르게 선택합니다. target 4에서 ID 0·2·5·7이 남아 최고점과 최저점은 빠집니다. 입력이 target 이하이면 전체를 반환합니다. 불규칙한 관측에서는 균등한 시간 간격을 보장하지 않습니다.

구문 인자는 `uniform(target)`입니다. 절 형태는 지정 시각 컬럼을 SELECT에 직접 포함해야 합니다. 아래 SQL의 TIME_NS는 표시 시간대에 영향받지 않는 원본 시각 확인용입니다.

target은 2~2147483647의 정수입니다. value 기반 알고리즘의 DECIMAL 인자는 지원하지 않지만 선택된 행의 별도 DECIMAL·ARRAY·문자열 payload는 유지됩니다. LTTB·MINMAX·M4는 NULL 시각과 NULL·NaN·Inf 값을 후보에서 제외하며 UNIFORM·CADENCE는 값과 무관하게 행을 셉니다.

![원본 신호와 UNIFORM 선택점 비교](/assets/dbms-8.9/time-series-sql/plots/uniform.svg)

회색 선은 원본, 색 점은 선택 관측입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 균등 위치 4행](#example-1) | 정상 |
| 2 | [양끝 포함](#example-2) | 정상 |
| 3 | [입력 수 이하에서 전체 보존](#example-3) | 정상 |
| 4 | [유효하지 않은 알고리즘 인자](#example-4) | 오류 확인 |
| 5 | [선택 시각을 출력하지 않은 절 형태](#example-5) | 오류 확인 |

## 1. 공통 데이터의 균등 위치 4행 {#example-1}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/uniform/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/uniform/01.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE uniform(4) ORDER BY TIME;
```

결과 **4행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 2 | 2027-01-01 00:00:02 | 2 | 1798729202000000000 |
| 5 | 2027-01-01 00:00:05 | 5 | 1798729205000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 2. 양끝 포함 {#example-2}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/uniform/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/uniform/02.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE uniform(2) ORDER BY TIME;
```

결과 **2행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 3. 입력 수 이하에서 전체 보존 {#example-3}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/uniform/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/uniform/03.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE uniform(12) ORDER BY TIME;
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

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/uniform/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/uniform/04.json)

```sql
SELECT ID,TIME,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE uniform(1);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_SUBSAMPLE_TARGET).
```


## 5. 선택 시각을 출력하지 않은 절 형태 {#example-5}

절 형태는 지정 시각 컬럼을 SELECT에 직접 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/uniform/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/uniform/05.json)

```sql
SELECT ID,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE uniform(4);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
