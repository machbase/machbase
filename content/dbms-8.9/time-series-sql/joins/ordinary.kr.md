---
type: docs
title: '13.1.7 일반 JOIN과 시계열 JOIN 비교'
weight: 70
toc: true
---

[시계열 JOIN·TIMESTAMP·TIE 전체 BNF](../../../reference/sql/syntax/time-series-join-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

일반 JOIN은 ON 조건을 만족하는 모든 행 조합을 반환합니다. 키만 같다고 연결하면 직전 관측이나 최근접 한 행을 선택하지 않습니다. event 6행과 motor 18행은 같은 NAME이므로 108행이 됩니다.

INNER는 일치 조합만, LEFT는 왼쪽 미매칭 행도, RIGHT는 오른쪽 미매칭 행도 보존합니다. 공통 데이터는 모든 행의 NAME이 같아 세 방식 모두 108행입니다. 차이를 확인할 수 있도록 추가 TS13_L·TS13_R 데이터에는 미매칭 키와 NULL 키를 넣었습니다.

ON에서 오른쪽 값을 제한하면 미매칭 왼쪽 행을 보존할 수 있습니다. LEFT JOIN 뒤 WHERE에서 오른쪽 값을 요구하면 NULL 확장 행은 제거됩니다. RIGHT JOIN도 최종 WHERE가 왼쪽 컬럼의 일치를 요구하면 오른쪽 미매칭 행이 제거됩니다. NULL 키끼리는 일반 동등 비교로 일치하지 않습니다.

[공통 준비와 정리](../../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [INNER의 전체 조합과 미매칭](#example-1) | 정상 |
| 2 | [INNER의 ON에서 후보 값 제한](#example-2) | 정상 |
| 3 | [INNER 뒤 WHERE가 NULL 확장을 제거](#example-3) | 정상 |
| 4 | [INNER 공통 데이터의 108행](#example-4) | 정상 |
| 5 | [LEFT의 전체 조합과 미매칭](#example-5) | 정상 |
| 6 | [LEFT의 ON에서 후보 값 제한](#example-6) | 정상 |
| 7 | [LEFT 뒤 WHERE가 NULL 확장을 제거](#example-7) | 정상 |
| 8 | [LEFT 공통 데이터의 108행](#example-8) | 정상 |
| 9 | [RIGHT의 전체 조합과 미매칭](#example-9) | 정상 |
| 10 | [RIGHT의 ON에서 후보 값 제한](#example-10) | 정상 |
| 11 | [RIGHT 뒤 WHERE가 NULL 확장을 제거](#example-11) | 정상 |
| 12 | [RIGHT 공통 데이터의 108행](#example-12) | 정상 |

## 1. INNER의 전체 조합과 미매칭 {#example-1}

일반 JOIN은 적격한 모든 조합을 반환합니다. NULL 키끼리는 일반 등호로 매칭되지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/01.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l INNER JOIN TS13_R r ON l.K=r.K ORDER BY l.ID,r.ID;
```

결과 **2행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |


## 2. INNER의 ON에서 후보 값 제한 {#example-2}

ON의 조건은 매칭을 제한하며 보존 측의 미매칭 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/02.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l INNER JOIN TS13_R r ON l.K=r.K AND r.V>5 ORDER BY l.ID,r.ID;
```

결과 **1행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 102 |


## 3. INNER 뒤 WHERE가 NULL 확장을 제거 {#example-3}

WHERE는 완성된 JOIN 결과를 필터합니다. NULL 확장 행이 제거될 수 있습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/03.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l INNER JOIN TS13_R r ON l.K=r.K WHERE l.ID IS NOT NULL AND r.ID IS NOT NULL ORDER BY l.ID,r.ID;
```

결과 **2행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |


## 4. INNER 공통 데이터의 108행 {#example-4}

이 데이터는 모든 이벤트에 같은 NAME의 motor 18행이 매칭됩니다. 시간 JOIN의 6행과 달리 6×18=108행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/04.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID FROM TS13_EVENT e INNER JOIN TS13_MOTOR m ON e.NAME=m.NAME WHERE e.NAME='edu27_main' ORDER BY e.ID,m.ID;
```

결과 **108행** 중 앞 8행입니다.

| EVENT_ID | MOTOR_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |
| 1 | 103 |
| 1 | 104 |
| 1 | 105 |
| 1 | 106 |
| 1 | 107 |
| 1 | 108 |


## 5. LEFT의 전체 조합과 미매칭 {#example-5}

일반 JOIN은 적격한 모든 조합을 반환합니다. NULL 키끼리는 일반 등호로 매칭되지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/05.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l LEFT JOIN TS13_R r ON l.K=r.K ORDER BY l.ID,r.ID;
```

결과 **4행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |
| 2 | NULL |
| 3 | NULL |


## 6. LEFT의 ON에서 후보 값 제한 {#example-6}

ON의 조건은 매칭을 제한하며 보존 측의 미매칭 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/06.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l LEFT JOIN TS13_R r ON l.K=r.K AND r.V>5 ORDER BY l.ID,r.ID;
```

결과 **3행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 102 |
| 2 | NULL |
| 3 | NULL |


## 7. LEFT 뒤 WHERE가 NULL 확장을 제거 {#example-7}

WHERE는 완성된 JOIN 결과를 필터합니다. NULL 확장 행이 제거될 수 있습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/07.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l LEFT JOIN TS13_R r ON l.K=r.K WHERE l.ID IS NOT NULL AND r.ID IS NOT NULL ORDER BY l.ID,r.ID;
```

결과 **2행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |


## 8. LEFT 공통 데이터의 108행 {#example-8}

이 데이터는 모든 이벤트에 같은 NAME의 motor 18행이 매칭됩니다. 시간 JOIN의 6행과 달리 6×18=108행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/08.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID FROM TS13_EVENT e LEFT JOIN TS13_MOTOR m ON e.NAME=m.NAME WHERE e.NAME='edu27_main' ORDER BY e.ID,m.ID;
```

결과 **108행** 중 앞 8행입니다.

| EVENT_ID | MOTOR_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |
| 1 | 103 |
| 1 | 104 |
| 1 | 105 |
| 1 | 106 |
| 1 | 107 |
| 1 | 108 |


## 9. RIGHT의 전체 조합과 미매칭 {#example-9}

일반 JOIN은 적격한 모든 조합을 반환합니다. NULL 키끼리는 일반 등호로 매칭되지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/09.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/09.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l RIGHT JOIN TS13_R r ON l.K=r.K ORDER BY l.ID,r.ID;
```

결과 **4행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| NULL | 103 |
| NULL | 104 |
| 1 | 101 |
| 1 | 102 |


## 10. RIGHT의 ON에서 후보 값 제한 {#example-10}

ON의 조건은 매칭을 제한하며 보존 측의 미매칭 행은 남습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/10.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/10.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l RIGHT JOIN TS13_R r ON l.K=r.K AND r.V>5 ORDER BY l.ID,r.ID;
```

결과 **4행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| NULL | 101 |
| NULL | 103 |
| NULL | 104 |
| 1 | 102 |


## 11. RIGHT 뒤 WHERE가 NULL 확장을 제거 {#example-11}

WHERE는 완성된 JOIN 결과를 필터합니다. NULL 확장 행이 제거될 수 있습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/11.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/11.json)

```sql
SELECT l.ID AS LEFT_ID,r.ID AS RIGHT_ID FROM TS13_L l RIGHT JOIN TS13_R r ON l.K=r.K WHERE l.ID IS NOT NULL AND r.ID IS NOT NULL ORDER BY l.ID,r.ID;
```

결과 **2행**입니다.

| LEFT_ID | RIGHT_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |


## 12. RIGHT 공통 데이터의 108행 {#example-12}

이 데이터는 모든 이벤트에 같은 NAME의 motor 18행이 매칭됩니다. 시간 JOIN의 6행과 달리 6×18=108행입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/joins/ordinary/12.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/joins/ordinary/12.json)

```sql
SELECT e.ID AS EVENT_ID,m.ID AS MOTOR_ID FROM TS13_EVENT e RIGHT JOIN TS13_MOTOR m ON e.NAME=m.NAME WHERE e.NAME='edu27_main' ORDER BY e.ID,m.ID;
```

결과 **108행** 중 앞 8행입니다.

| EVENT_ID | MOTOR_ID |
| --- | --- |
| 1 | 101 |
| 1 | 102 |
| 1 | 103 |
| 1 | 104 |
| 1 | 105 |
| 1 | 106 |
| 1 | 107 |
| 1 | 108 |
