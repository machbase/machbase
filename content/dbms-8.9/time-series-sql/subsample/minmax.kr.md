---
type: docs
title: '13.4.2 MINMAX: 구간별 극값 보존'
weight: 20
toc: true
---

시간 범위를 나누고 구간별 최솟값·최댓값 행을 선택합니다. target 4에서는 ID 0·3·4·5를 선택합니다. 마지막 7초 관측을 반드시 보존하지 않으므로 M4와 비교합니다.

구문 인자는 `minmax(value, target)`입니다. 절 형태는 지정 시각 컬럼을 SELECT에 직접 포함해야 합니다. 아래 SQL의 TIME_NS는 표시 시간대에 영향받지 않는 원본 시각 확인용입니다.

target은 2~2147483647의 정수입니다. value 기반 알고리즘의 DECIMAL 인자는 지원하지 않지만 선택된 행의 별도 DECIMAL·ARRAY·문자열 payload는 유지됩니다. LTTB·MINMAX·M4는 NULL 시각과 NULL·NaN·Inf 값을 후보에서 제외하며 UNIFORM·CADENCE는 값과 무관하게 행을 셉니다.

![원본 신호와 MINMAX 선택점 비교](/assets/dbms-8.9/time-series-sql/plots/minmax.svg)

회색 선은 원본, 색 점은 선택 관측입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [두 구간의 최소·최대](#example-1) | 정상 |
| 2 | [전체 구간의 최고·최저](#example-2) | 정상 |
| 3 | [세 구간으로 나누어 선택](#example-3) | 정상 |
| 4 | [유효하지 않은 알고리즘 인자](#example-4) | 오류 확인 |
| 5 | [선택 시각을 출력하지 않은 절 형태](#example-5) | 오류 확인 |

## 1. 두 구간의 최소·최대 {#example-1}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/minmax/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/minmax/01.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE minmax(V,4) ORDER BY TIME;
```

결과 **4행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |
| 5 | 2027-01-01 00:00:05 | 5 | 1798729205000000000 |


## 2. 전체 구간의 최고·최저 {#example-2}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/minmax/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/minmax/02.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE minmax(V,2) ORDER BY TIME;
```

결과 **2행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |


## 3. 세 구간으로 나누어 선택 {#example-3}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/minmax/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/minmax/03.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE minmax(V,6) ORDER BY TIME;
```

결과 **6행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 1 | 2027-01-01 00:00:01 | 4 | 1798729201000000000 |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |
| 5 | 2027-01-01 00:00:05 | 5 | 1798729205000000000 |
| 6 | 2027-01-01 00:00:06 | 1 | 1798729206000000000 |


## 4. 유효하지 않은 알고리즘 인자 {#example-4}

target은 2 이상, stride는 1 이상, SDT 허용 편차는 유한한 0 이상이어야 합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/minmax/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/minmax/04.json)

```sql
SELECT ID,TIME,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE minmax(V,1);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_SUBSAMPLE_TARGET).
```


## 5. 선택 시각을 출력하지 않은 절 형태 {#example-5}

절 형태는 지정 시각 컬럼을 SELECT에 직접 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/minmax/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/minmax/05.json)

```sql
SELECT ID,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE minmax(V,4);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
