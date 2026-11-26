---
type: docs
title: '13.4.1 LTTB: 곡선의 굴곡 보존'
weight: 10
toc: true
---

[SUBSAMPLE 절과 윈도 형태 전체 BNF](../../../reference/sql/syntax/subsample-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

이전 선택점·현재 후보·다음 구간 평균점의 삼각형 면적으로 굴곡을 선택합니다. target 4에서 ID 0·3·4·7이 남습니다. 양끝과 3초 최고점·4초 최저점을 함께 보존합니다. 선택점은 원래 관측값입니다.

구문 인자는 `lttb(value, target[, gap])`입니다. 절 형태는 지정 시각 컬럼을 SELECT에 직접 포함해야 합니다. 아래 SQL의 TIME_NS는 표시 시간대에 영향받지 않는 원본 시각 확인용입니다.

target은 2~2147483647의 정수입니다. value 기반 알고리즘의 DECIMAL 인자는 지원하지 않지만 선택된 행의 별도 DECIMAL·ARRAY·문자열 payload는 유지됩니다. LTTB·MINMAX·M4는 NULL 시각과 NULL·NaN·Inf 값을 후보에서 제외하며 UNIFORM·CADENCE는 값과 무관하게 행을 셉니다.

선택 인자 gap은 '2s'처럼 양수 정수에 s/m/h/d 한 글자 단위를 붙인 문자열입니다. ms/us/ns는 사용할 수 없습니다. 해당 간격을 넘으면 구간을 나누고 양끝을 보존하므로 최종 행 수가 target을 넘을 수 있습니다.

![원본 신호와 LTTB 선택점 비교](/assets/dbms-8.9/time-series-sql/plots/lttb.svg)

회색 선은 원본, 색 점은 선택 관측입니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [공통 데이터의 target=4](#example-1) | 정상 |
| 2 | [양끝 2개만 선택](#example-2) | 정상 |
| 3 | [입력보다 큰 target](#example-3) | 정상 |
| 4 | [유효하지 않은 알고리즘 인자](#example-4) | 오류 확인 |
| 5 | [선택 시각을 출력하지 않은 절 형태](#example-5) | 오류 확인 |
| 6 | [목표 개수와 선택 위치 변경](#example-6) | 정상 |
| 7 | [간격 경계에서 원본 구간 분리](#example-7) | 정상 |
| 8 | [gap의 밀리초 문자열은 허용하지 않음](#example-8) | 오류 확인 |

## 1. 공통 데이터의 target=4 {#example-1}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/01.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,4) ORDER BY TIME;
```

결과 **4행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 4 | 2027-01-01 00:00:04 | -1 | 1798729204000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 2. 양끝 2개만 선택 {#example-2}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/02.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,2) ORDER BY TIME;
```

결과 **2행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 3. 입력보다 큰 target {#example-3}

원본 행을 선택합니다. 반환 ID·값을 원래 관측과 대조하며 보간값을 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/03.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,12) ORDER BY TIME;
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

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/04.json)

```sql
SELECT ID,TIME,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,1);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_SUBSAMPLE_TARGET).
```


## 5. 선택 시각을 출력하지 않은 절 형태 {#example-5}

절 형태는 지정 시각 컬럼을 SELECT에 직접 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/05.json)

```sql
SELECT ID,V FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,4);
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```


## 6. 목표 개수와 선택 위치 변경 {#example-6}

target를 3으로 줄이면 4초 최저점이 빠지고 양끝과 3초 최고점이 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/06.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,3) ORDER BY TIME;
```

결과 **3행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 3 | 2027-01-01 00:00:03 | 7 | 1798729203000000000 |
| 7 | 2027-01-01 00:00:07 | 3 | 1798729207000000000 |


## 7. 간격 경계에서 원본 구간 분리 {#example-7}

같은 값을 2초 간격의 시각에 배치합니다. gap 1s를 넘는 각 구간의 끝점을 보존하므로 target 4보다 많은 8행이 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/07.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM (SELECT ID,FROM_TIMESTAMP(1798729200000000000+ID*2000000000) AS TIME,V FROM TS13_SUB) S TIMESTAMP(TIME) SUBSAMPLE lttb(V,4,'1s') ORDER BY TIME;
```

결과 **8행**입니다.

| ID | TIME | V | TIME_NS |
| --- | --- | --- | --- |
| 0 | 2027-01-01 00:00:00 | 0 | 1798729200000000000 |
| 1 | 2027-01-01 00:00:02 | 4 | 1798729202000000000 |
| 2 | 2027-01-01 00:00:04 | 2 | 1798729204000000000 |
| 3 | 2027-01-01 00:00:06 | 7 | 1798729206000000000 |
| 4 | 2027-01-01 00:00:08 | -1 | 1798729208000000000 |
| 5 | 2027-01-01 00:00:10 | 5 | 1798729210000000000 |
| 6 | 2027-01-01 00:00:12 | 1 | 1798729212000000000 |
| 7 | 2027-01-01 00:00:14 | 3 | 1798729214000000000 |


## 8. gap의 밀리초 문자열은 허용하지 않음 {#example-8}

LTTB gap 문자열은 양수 정수와 s/m/h/d 한 글자 단위를 사용합니다. SAMPLE 간격의 단위 지원 범위와 다릅니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/subsample/lttb/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/subsample/lttb/08.json)

```sql
SELECT ID,TIME,V,TO_TIMESTAMP(TIME) AS TIME_NS FROM TS13_SUB TIMESTAMP(TIME) SUBSAMPLE lttb(V,4,'500ms') ORDER BY TIME;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_SUBSAMPLE_TARGET).
```
