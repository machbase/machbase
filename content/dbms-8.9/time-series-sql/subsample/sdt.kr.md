---
type: docs
title: '13.4.6 SDT: 허용 편차로 관측 압축'
weight: 60
toc: true
---

[SUBSAMPLE 절과 윈도 형태 전체 BNF](../../../reference/sql/syntax/subsample-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

compdev는 값의 단위로 표현한 유한한 0 이상의 허용 편차입니다. 8개 굴곡 신호에 편차 0을 주면 모두 남지만 정확한 직선은 양끝만 남습니다. 온도 20·21·22.25·23·24·30에 편차 0.5를 주면 ID 0·4·5를 남겨 마지막 급상승을 보존합니다.

구문 인자는 `sdt(value, compdev)`입니다. 절 형태는 지정 시각 컬럼을 SELECT에 직접 포함해야 합니다. 아래 SQL의 TIME_NS는 표시 시간대에 영향받지 않는 원본 시각 확인용입니다.

compdev는 유한한 0 이상의 수치 상수입니다. value 기반 알고리즘의 DECIMAL 인자는 지원하지 않지만 선택된 행의 별도 DECIMAL·ARRAY·문자열 payload는 유지됩니다. LTTB·MINMAX·M4는 NULL 시각과 NULL·NaN·Inf 값을 후보에서 제외하며 UNIFORM·CADENCE는 값과 무관하게 행을 셉니다.

compdev는 상수이며 바인드를 받지 않습니다. 기본 RESPECT NULLS는 무효 입력을 경계로 남기고 IGNORE NULLS는 제외합니다. 같은 수준의 JOIN·GROUP BY·SAMPLE BY·DISTINCT와 결합하려면 입력을 파생 조회로 먼저 구성합니다.

![원본 신호와 SDT 선택점 비교](/assets/dbms-8.9/time-series-sql/plots/sdt.svg)

회색 선은 원본, 색 점은 선택 관측입니다. SDT 그림은 편차 0의 굴곡 신호입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [굴곡 신호의 편차 0](#example-1) | 정상 |
| 2 | [온도 허용 편차 0.5](#example-2) | 정상 |
| 3 | [편차 0이어도 직선은 양끝만 보존](#example-3) | 정상 |
| 4 | [유효하지 않은 알고리즘 인자](#example-4) | 오류 확인 |
| 5 | [선택 시각을 출력하지 않은 절 형태](#example-5) | 오류 확인 |
| 6 | [같은 온도 입력의 허용 편차 0](#example-6) | 정상 |

## 1. 굴곡 신호의 편차 0 {#example-1}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/sdt/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/sdt/01.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE sdt(V,0) ORDER BY TIME;
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


## 2. 온도 허용 편차 0.5 {#example-2}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/sdt/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/sdt/02.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SDT TIMESTAMP(TIME) SUBSAMPLE sdt(V,0.5) ORDER BY TIME;
```

결과 **3행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 20 | 1798729200000000000 |
| 4 | 2027-01-01 00:00:04 | 24 | 1798729204000000000 |
| 5 | 2027-01-01 00:00:05 | 30 | 1798729205000000000 |


## 3. 편차 0이어도 직선은 양끝만 보존 {#example-3}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/sdt/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/sdt/03.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_LINE TIMESTAMP(TIME) SUBSAMPLE sdt(V,0) ORDER BY TIME;
```

결과 **2행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 20 | 1798729200000000000 |
| 5 | 2027-01-01 00:00:05 | 25 | 1798729205000000000 |


## 4. 유효하지 않은 알고리즘 인자 {#example-4}

target은 2 이상, stride는 1 이상, SDT 허용 편차는 유한한 0 이상이어야 합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/sdt/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/sdt/04.json)

```sql
SELECT ID,TIME,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE sdt(V,-1);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_SUBSAMPLE_COMPDEV).
```


## 5. 선택 시각을 출력하지 않은 절 형태 {#example-5}

절 형태는 지정 시각 컬럼을 SELECT에 직접 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/sdt/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/sdt/05.json)

```sql
SELECT ID,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE sdt(V,0.5);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```


## 6. 같은 온도 입력의 허용 편차 0 {#example-6}

같은 온도 입력에 허용 편차 0과 0.5를 비교합니다. 편차 0에서는 6행 모두 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/sdt/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/sdt/06.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SDT TIMESTAMP(TIME) SUBSAMPLE sdt(V,0) ORDER BY TIME;
```

결과 **6행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 20 | 1798729200000000000 |
| 1 | 2027-01-01 00:00:01 | 21 | 1798729201000000000 |
| 2 | 2027-01-01 00:00:02 | 22.25 | 1798729202000000000 |
| 3 | 2027-01-01 00:00:03 | 23 | 1798729203000000000 |
| 4 | 2027-01-01 00:00:04 | 24 | 1798729204000000000 |
| 5 | 2027-01-01 00:00:05 | 30 | 1798729205000000000 |
