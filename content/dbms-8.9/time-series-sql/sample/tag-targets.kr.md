---
type: docs
title: '13.3.6 태그 집합의 특정 시각 조회'
weight: 60
toc: true
---

METADATA에서 조회 대상 태그 집합을 만들고 목표 DATETIME을 지정하면, 태그마다 해당 시각의 실제 관측 또는 보간값을 얻을 수 있습니다. 관측이 없거나 허용 범위를 벗어나도 왼쪽 대상 태그 행을 유지합니다.

최근접 실제값에는 NEAREST JOIN과 TOLERANCE를 사용합니다. 추정값에는 INTERPOLATE JOIN의 COLUMNS와 MAX GAP을 사용합니다. 동일 목표 시각을 모든 태그에 적용하거나 태그별 DATETIME을 목표 시각으로 만들 수 있습니다.

파생 입력의 목표 컬럼은 `TIMESTAMP(TARGET_TIME)`으로 지정해야 합니다. 문자열 컬럼 자체를 시간축으로 지정하지 않습니다. 아래 예제는 태그 집합·정확 일치·동률·허용 범위 밖·보간을 비교합니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [태그 집합의 기준 시각에 최근접 관측](#example-1) | 정상 |
| 2 | [동일 거리의 과거 관측 선택](#example-2) | 정상 |
| 3 | [허용차 밖이면 태그 행 유지](#example-3) | 정상 |
| 4 | [정확 시각만 허용](#example-4) | 정상 |
| 5 | [정확 시각이 없으면 NULL](#example-5) | 정상 |
| 6 | [태그 집합의 기준 시각에 원본 보간](#example-6) | 정상 |
| 7 | [DATETIME 목표 컬럼을 지정하지 않음](#example-7) | 오류 확인 |
| 8 | [문자열을 지정 시간축으로 사용 거부](#example-8) | 오류 확인 |

## 1. 태그 집합의 기준 시각에 최근접 관측 {#example-1}

metadata로 얻은 태그마다 실제 DATETIME 목표 컬럼을 만듭니다. placeholder나 단위 없는 허용차를 사용하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/01.json)

```sql
SELECT t.NAME,t.TARGET_TIME,m.VALUE AS MOTOR_VALUE
FROM (
 SELECT NAME,FROM_TIMESTAMP(1798729221000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA
 WHERE NAME='edu27_main'
) t TIMESTAMP(TARGET_TIME)
NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME TOLERANCE 5s;
```

결과 **1행**입니다.

| NAME | TARGET_TIME | MOTOR_VALUE |
| --- | --- | --- |
| edu27_main | 2027-01-01 00:00:21 | 484 |


## 2. 동일 거리의 과거 관측 선택 {#example-2}

metadata로 얻은 태그마다 실제 DATETIME 목표 컬럼을 만듭니다. placeholder나 단위 없는 허용차를 사용하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/02.json)

```sql
SELECT t.NAME,t.TARGET_TIME,m.VALUE AS MOTOR_VALUE
FROM (
 SELECT NAME,FROM_TIMESTAMP(1798729246000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA
 WHERE NAME='edu27_main'
) t TIMESTAMP(TARGET_TIME)
NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME TOLERANCE 5s;
```

결과 **1행**입니다.

| NAME | TARGET_TIME | MOTOR_VALUE |
| --- | --- | --- |
| edu27_main | 2027-01-01 00:00:46 | 1936 |


## 3. 허용차 밖이면 태그 행 유지 {#example-3}

metadata로 얻은 태그마다 실제 DATETIME 목표 컬럼을 만듭니다. placeholder나 단위 없는 허용차를 사용하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/03.json)

```sql
SELECT t.NAME,t.TARGET_TIME,m.VALUE AS MOTOR_VALUE
FROM (
 SELECT NAME,FROM_TIMESTAMP(1798729260000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA
 WHERE NAME='edu27_main'
) t TIMESTAMP(TARGET_TIME)
NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME TOLERANCE 5s;
```

결과 **1행**입니다.

| NAME | TARGET_TIME | MOTOR_VALUE |
| --- | --- | --- |
| edu27_main | 2027-01-01 00:01:00 | NULL |


## 4. 정확 시각만 허용 {#example-4}

metadata로 얻은 태그마다 실제 DATETIME 목표 컬럼을 만듭니다. placeholder나 단위 없는 허용차를 사용하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/04.json)

```sql
SELECT t.NAME,t.TARGET_TIME,m.VALUE AS MOTOR_VALUE
FROM (
 SELECT NAME,FROM_TIMESTAMP(1798729210000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA
 WHERE NAME='edu27_main'
) t TIMESTAMP(TARGET_TIME)
NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME TOLERANCE 0s;
```

결과 **1행**입니다.

| NAME | TARGET_TIME | MOTOR_VALUE |
| --- | --- | --- |
| edu27_main | 2027-01-01 00:00:10 | 100 |


## 5. 정확 시각이 없으면 NULL {#example-5}

metadata로 얻은 태그마다 실제 DATETIME 목표 컬럼을 만듭니다. placeholder나 단위 없는 허용차를 사용하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/05.json)

```sql
SELECT t.NAME,t.TARGET_TIME,m.VALUE AS MOTOR_VALUE
FROM (
 SELECT NAME,FROM_TIMESTAMP(1798729221000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA
 WHERE NAME='edu27_main'
) t TIMESTAMP(TARGET_TIME)
NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME TOLERANCE 0s;
```

결과 **1행**입니다.

| NAME | TARGET_TIME | MOTOR_VALUE |
| --- | --- | --- |
| edu27_main | 2027-01-01 00:00:21 | NULL |


## 6. 태그 집합의 기준 시각에 원본 보간 {#example-6}

목표 시각의 앞뒤 원본 관측을 보간합니다. SAMPLE 버킷의 평균을 보간하는 연산이 아닙니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/06.json)

```sql
SELECT t.NAME,m.VALUE AS INTERPOLATED_VALUE
FROM (SELECT NAME,FROM_TIMESTAMP(1798729221000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA
 WHERE NAME='edu27_main') t TIMESTAMP(TARGET_TIME)
INTERPOLATE JOIN TS13_MOTOR m ON t.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 4s;
```

결과 **1행**입니다.

| NAME | INTERPOLATED_VALUE |
| --- | --- |
| edu27_main | 444 |


## 7. DATETIME 목표 컬럼을 지정하지 않음 {#example-7}

metadata 파생 입력의 이름만으로 시간축을 추론하지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/07.json)

```sql
SELECT t.NAME FROM (SELECT NAME,FROM_TIMESTAMP(1798729221000000000) AS TARGET_TIME FROM TS13_MOTOR METADATA) t NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```


## 8. 문자열을 지정 시간축으로 사용 거부 {#example-8}

시각 문자열이 아니라 DATETIME 컬럼을 노출합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/sample/tag-targets/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/sample/tag-targets/08.json)

```sql
SELECT t.NAME FROM (SELECT NAME,'2027-01-01' AS TARGET_TIME FROM TS13_MOTOR METADATA) t TIMESTAMP(TARGET_TIME) NEAREST JOIN TS13_MOTOR m ON t.NAME=m.NAME;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_TS_REQUIRED).
```
