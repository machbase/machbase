---
type: docs
title: '13.6 ROWS 윈도 프레임'
weight: 60
toc: true
---

[OVER·ROWS 전체 BNF](../../reference/sql/syntax/window-function-over-syntax/#rows-bnf)에서 작성 순서와 인자 제약을 확인합니다.

현재 행을 기준으로 앞뒤 N행을 집계합니다. 시간 길이를 지정하는 WINDOW JOIN과 달리 **정렬된 행의 개수**가 기준입니다. PARTITION BY는 장치별 계산을 분리하며 프레임은 파티션 경계에서 잘립니다.

ROWS BETWEEN 2 PRECEDING AND CURRENT ROW는 현재 행과 앞 두 행의 이동 통계입니다. UNBOUNDED PRECEDING부터 현재까지는 누적 통계입니다. FOLLOWING을 사용하면 미래 행을 포함합니다. ROWS 2 PRECEDING은 현재 행까지의 축약형입니다.

양끝을 포함하며 폭은 0 이상의 정수형 문장 상수나 정수 바인드입니다. NULL·음수·비정수·입력 행에 의존하는 폭은 허용하지 않습니다. 프레임이 파티션 밖에 있으면 빈 프레임이며 COUNT는 0, 다른 집계는 빈 입력 규칙을 따릅니다.

윈도 내부 ORDER BY 조합은 행을 유일하게 구분해야 합니다. 같은 시각이 있으면 ID 같은 보조 키를 **OVER 안에** 추가합니다. 최종 ORDER BY를 추가하는 것만으로 내부 동률을 해결할 수 없습니다. SAMPLE 결과에 적용하면 FILL이 만든 버킷도 논리 행으로 계산합니다.

[공통 준비와 정리](../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [앞 2행과 현재의 이동 합계](#example-1) | 정상 |
| 2 | [처음부터 현재까지 누적 합계](#example-2) | 정상 |
| 3 | [앞뒤 1행의 이동 평균](#example-3) | 정상 |
| 4 | [빈 프레임의 COUNT=0](#example-4) | 정상 |
| 5 | [축약된 ROWS 표현](#example-5) | 정상 |
| 6 | [현재부터 끝까지 합계](#example-6) | 정상 |
| 7 | [윈도 내부의 모호한 정렬 순서](#example-7) | 오류 확인 |
| 8 | [음수 프레임 폭](#example-8) | 오류 확인 |
| 9 | [장치별 프레임은 서로 넘나들지 않음](#example-9) | 정상 |

## 1. 앞 2행과 현재의 이동 합계 {#example-1}

행 개수 프레임이며 시간창 WINDOW JOIN과 다릅니다. 파티션 경계에서 잘리고 내부 정렬에 유일한 보조 키를 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/01.json)

```sql
SELECT ID,SUM(VALUE) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS RESULT
FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID;
```

결과 **18행** 중 앞 8행입니다.

| ID | RESULT |
| --- | --- |
| 101 | 0 |
| 102 | 16 |
| 103 | 80 |
| 104 | 180 |
| 105 | 308 |
| 106 | 500 |
| 107 | 724 |
| 108 | 1064 |


## 2. 처음부터 현재까지 누적 합계 {#example-2}

행 개수 프레임이며 시간창 WINDOW JOIN과 다릅니다. 파티션 경계에서 잘리고 내부 정렬에 유일한 보조 키를 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/02.json)

```sql
SELECT ID,SUM(VALUE) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS RESULT
FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID;
```

결과 **18행** 중 앞 8행입니다.

| ID | RESULT |
| --- | --- |
| 101 | 0 |
| 102 | 16 |
| 103 | 80 |
| 104 | 180 |
| 105 | 324 |
| 106 | 580 |
| 107 | 904 |
| 108 | 1388 |


## 3. 앞뒤 1행의 이동 평균 {#example-3}

행 개수 프레임이며 시간창 WINDOW JOIN과 다릅니다. 파티션 경계에서 잘리고 내부 정렬에 유일한 보조 키를 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/03.json)

```sql
SELECT ID,AVG(VALUE) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS RESULT
FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID;
```

결과 **18행** 중 앞 8행입니다.

| ID | RESULT |
| --- | --- |
| 101 | 8 |
| 102 | 26.66666667 |
| 103 | 60 |
| 104 | 102.6666667 |
| 105 | 166.6666667 |
| 106 | 241.3333333 |
| 107 | 354.6666667 |
| 108 | 461.3333333 |


## 4. 빈 프레임의 COUNT=0 {#example-4}

행 개수 프레임이며 시간창 WINDOW JOIN과 다릅니다. 파티션 경계에서 잘리고 내부 정렬에 유일한 보조 키를 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/04.json)

```sql
SELECT ID,COUNT(*) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS BETWEEN 2 FOLLOWING AND 2 FOLLOWING) AS RESULT
FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID;
```

결과 **18행** 중 앞 8행입니다.

| ID | RESULT |
| --- | --- |
| 101 | 1 |
| 102 | 1 |
| 103 | 1 |
| 104 | 1 |
| 105 | 1 |
| 106 | 1 |
| 107 | 1 |
| 108 | 1 |


## 5. 축약된 ROWS 표현 {#example-5}

행 개수 프레임이며 시간창 WINDOW JOIN과 다릅니다. 파티션 경계에서 잘리고 내부 정렬에 유일한 보조 키를 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/05.json)

```sql
SELECT ID,SUM(VALUE) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS 2 PRECEDING) AS RESULT
FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID;
```

결과 **18행** 중 앞 8행입니다.

| ID | RESULT |
| --- | --- |
| 101 | 0 |
| 102 | 16 |
| 103 | 80 |
| 104 | 180 |
| 105 | 308 |
| 106 | 500 |
| 107 | 724 |
| 108 | 1064 |


## 6. 현재부터 끝까지 합계 {#example-6}

행 개수 프레임이며 시간창 WINDOW JOIN과 다릅니다. 파티션 경계에서 잘리고 내부 정렬에 유일한 보조 키를 포함합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/06.json)

```sql
SELECT ID,SUM(VALUE) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS RESULT
FROM TS13_MOTOR WHERE NAME='edu27_main' ORDER BY ID;
```

결과 **18행** 중 앞 8행입니다.

| ID | RESULT |
| --- | --- |
| 101 | 15916 |
| 102 | 15916 |
| 103 | 15900 |
| 104 | 15836 |
| 105 | 15736 |
| 106 | 15592 |
| 107 | 15336 |
| 108 | 15012 |


## 7. 윈도 내부의 모호한 정렬 순서 {#example-7}

바깥 ORDER BY가 아니라 OVER 안의 보조 키로 동률을 해소합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/07.json)

```sql
SELECT ID,SUM(VALUE) OVER(ORDER BY TIME ROWS 1 PRECEDING) FROM TS13_TIES;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
Function [E_TIE_CONFLICT] argument data type does not match.
```


## 8. 음수 프레임 폭 {#example-8}

프레임 폭은 0 이상의 정수 문장상수 또는 지원되는 bind입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/08.json)

```sql
SELECT ID,SUM(VALUE) OVER(ORDER BY TIME,ID ROWS BETWEEN -1 PRECEDING AND CURRENT ROW) FROM TS13_MOTOR;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_ROWS_BOUND).
```


## 9. 장치별 프레임은 서로 넘나들지 않음 {#example-9}

장치 B의 첫 행은 앞선 장치 A의 마지막 값을 포함하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/rows/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/rows/09.json)

```sql
SELECT NAME,ID,SUM(VALUE) OVER(PARTITION BY NAME ORDER BY TIME,ID ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS RESULT
FROM TS13_FILL ORDER BY NAME,TIME,ID;
```

결과 **5행**입니다.

| NAME | ID | RESULT |
| --- | --- | --- |
| A | 201 | 20 |
| A | 202 | 44 |
| A | 203 | 54 |
| B | 204 | 10 |
| B | 205 | 26 |
