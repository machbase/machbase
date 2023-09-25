---
title : '시계열 데이터 조회'
type: docs
weight: 20
---

SELECT문의 DURATION절은 검색 대상 시간 조건절을 정의한다. DURATION절을 이용하는 가장 큰 이유는 검색 대상을 줄여서 대량의 데이터를 검색하더라도 성능을 향상시키기 위함이다.

마크베이스는 입력 시간을 기준으로 데이터를 파티션하여 저장하므로, 시간 조건으로 데이터를 쉽게 검색하도록 하였다. 입력 시간은 사용자가 정의한 칼럼이 아니라 '_ARRIVAL_TIME'이라는 자동 생성 칼럼에 저장된다. 그러므로 마크베이스를 가장 효율적으로 사용하기 위해서는 추가로 시간 칼럼을 지정하지 않고 내장된 '_ARRIVAL_TIME' 칼럼을 이용하는 것이 좋다.

마크베이스는 입력된 순서의 역순으로 데이터를 출력한다. 즉, 최근 데이터가 먼저, 오래전 데이터가 나중에 출력되는 것이다. 일반적으로 시계열 데이터를 검색할 때, 최근 데이터가 더 중요하고 먼저 얻어야 하는 경우가 많으므로 이와 같은 순서로 출력한다. 또한 모든 DURATION조건절에 의한 데이터 출력은 최근에서 과거 순으로 출력된다. 과거에서 최근 순으로 출력하려면 AFTER 절을 이용하여야 한다. 문법은 다음과 같다.

## 문법

```sql
DURATION    time_expression [BEFORE time_expression | TO_DATE(time) ];
DURATION    time_expression [AFTER TO_DATE(time)]; 
time_expression
 -  ALL
 -  n   year
 -  n   month
 -  n   week
 -  n   day
 -  n   hour   
 -  n   minute 
 -  n   second
 ```

## DURATION...BEFORE

앞서 말한 것 처럼, BEFORE를 명시적 이용하거나 정의되지 않은 경우(자동으로 BEFORE를 적용)에는 최근에서 과거 순으로 데이터를 출력한다.

절대 시간 값 또는 상대 시간 값을 기준으로 데이터를 조회할 수 있다.

### 절대 시간 값 기준 검색

```sql
Mach> CREATE TABLE time_table (id INTEGER);
Created successfully.
 
Mach> INSERT INTO time_table(_arrival_time, id) VALUES(TO_DATE('2014-6-12 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1);
1 row(s) inserted.
 
Mach> INSERT INTO time_table(_arrival_time, id) VALUES(TO_DATE('2014-6-12 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2);
1 row(s) inserted.
 
Mach> INSERT INTO time_table(_arrival_time, id) VALUES(TO_DATE('2014-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3);
1 row(s) inserted.
 
Mach> INSERT INTO time_table(_arrival_time, id) VALUES(TO_DATE('2014-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4);
1 row(s) inserted.
 
Mach> INSERT INTO time_table VALUES(5);
1 row(s) inserted.
 
Mach> SELECT _arrival_time, * FROM time_table DURATION 1 MINUTE;
_arrival_time                   ID
-----------------------------------------------
2017-02-16 12:17:01 880:937:028 5
[1] row(s) selected.
 
Mach> SELECT _arrival_time, * FROM time_table DURATION 1 DAY BEFORE TO_DATE('2014-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2014-06-12 12:00:00 000:000:000 3
2014-06-12 11:00:00 000:000:000 2
2014-06-12 10:00:00 000:000:000 1
[3] row(s) selected.
```

### 상대 시간 값 기준 검색

상대 시간 값을 기준으로 한 검색은, 바로 현재를 기준으로 한 검색으로 볼 수 있다.

```sql
Mach> CREATE TABLE relative_table(id INTEGER);
Created successfully.
 
Mach> INSERT INTO relative_table values(1);
1 row(s) inserted.
 
------ WAIT for 30 SECONDS before the second value ------
 
Mach> INSERT INTO relative_table values(2);
1 row(s) inserted.
 
Mach> SELECT _arrival_time, * FROM relative_table;
_arrival_time                   ID
-----------------------------------------------
2017-02-16 12:35:34 476:055:014 2
2017-02-16 12:35:04 430:802:356 1
[2] row(s) selected.
 
Mach> SELECT id FROM relative_table DURATION 30 second ;
id
--------------
2
[1] row(s) selected.
 
Mach> SELECT id FROM relative_table DURATION 60 second ;
id
--------------
2
1
[2] row(s) selected.
 
Mach> SELECT id FROM relative_table DURATION 30 second BEFORE 30 second;
id
--------------
1
[1] row(s) selected.
```

## DURATION...AFTER

AFTER를 적용한 경우, 데이터는 과거에서 최근순으로 출력된다.

BEFORE명령은, 최근에서 과거로 출력하는것에 비교하면 데이터가 입력 시간을 기준으로 자동으로 역순으로 출력된다.

```sql
Mach> CREATE TABLE after_table (id INTEGER);
Created successfully.
 
Mach> INSERT INTO after_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1);
1 row(s) inserted.
 
Mach> INSERT INTO after_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2);
 
Mach> INSERT INTO after_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3);
1 row(s) inserted.
 
Mach> INSERT INTO after_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4);
1 row(s) inserted.
 
Mach> INSERT INTO after_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 5);
1 row(s) inserted.
 
Mach> select _arrival_time, * from after_table duration ALL after TO_DATE('2016-6-12 11:00:00', 'YYYY-MM-DD HH24:MI:SS');
 
_arrival_time                   ID
-----------------------------------------------
2016-06-12 11:00:00 000:000:000 2
2016-06-12 12:00:00 000:000:000 3
2016-06-12 13:00:00 000:000:000 4
2016-06-12 14:00:00 000:000:000 5
[4] row(s) selected.
 
Mach> select _arrival_time, * from after_table duration ALL before TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 13:00:00 000:000:000 4
2016-06-12 12:00:00 000:000:000 3
2016-06-12 11:00:00 000:000:000 2
2016-06-12 10:00:00 000:000:000 1
[4] row(s) selected.
```

## DURATION...FROM/TO
사용자가 두개의 절대 시간을 기준으로 데이터를 검색하려고 할 때, "DURATION FROM A TO B" 형태의 조건절을 이용한다.

A와 B는 절대적 시간이며 TO_DATE함수를 이용하여 표현된다. A와 B는 사용자의 의도에 따라 다르게 설정될 수 있다. 예를 들어,

* <span style='color:blue'>A가 B보다 이후의 시간일 경우</span> BEFORE를 사용한 것과 같이, 검색 방향은 최근에서 과거 순으로 데이터를 출력한다.
* <span style='color:red'>B가 A보다 과거인 경우</span> AFTER를 사용한 것과 같이, 검색 방향은 과거에서 최근 순으로 데이터를 출력한다.
아래의 예제를 보면 데이터의 출력 방식을 쉽게 이해할 수 있다.

```sql
Mach> CREATE TABLE from_table (id INTEGER);
Created successfully.
 
Mach> INSERT INTO from_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1);
1 row(s) inserted.
 
Mach> INSERT INTO from_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2);
1 row(s) inserted.
 
Mach> INSERT INTO from_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3);
1 row(s) inserted.
 
Mach> INSERT INTO from_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4);
1 row(s) inserted.
 
Mach> INSERT INTO from_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 5);
1 row(s) inserted.
 
Mach> INSERT INTO from_table(_arrival_time, id) VALUES(TO_DATE('2016-6-12 15:00:00', 'YYYY-MM-DD HH24:MI:SS'), 6);
1 row(s) inserted.
 
Mach> SELECT _arrival_time, * FROM from_table DURATION FROM TO_DATE('2016-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 14:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 12:00:00 000:000:000 3
2016-06-12 13:00:00 000:000:000 4
2016-06-12 14:00:00 000:000:000 5
[3] row(s) selected.
 
Mach> SELECT _arrival_time, * FROM from_table limit 2 DURATION FROM TO_DATE('2016-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 15:00:00',
'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 12:00:00 000:000:000 3
2016-06-12 13:00:00 000:000:000 4
[2] row(s) selected.
 
Mach> SELECT _arrival_time, * FROM from_table DURATION FROM TO_DATE('2016-6-12 15:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 15:00:00 000:000:000 6
2016-06-12 14:00:00 000:000:000 5
2016-06-12 13:00:00 000:000:000 4
2016-06-12 12:00:00 000:000:000 3
[4] row(s) selected.
 
Mach> SELECT _arrival_time, * FROM from_table LIMIT 2 duration FROM TO_DATE('2016-6-12 15:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 12:00:00',
'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 15:00:00 000:000:000 6
2016-06-12 14:00:00 000:000:000 5
[2] row(s) selected.
 
Mach> SELECT _arrival_time, * from from_table duration FROM TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 13:00:00 000:000:000 4
[1] row(s) selected.
 
Mach> SELECT _arrival_time, * from from_table duration FROM TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 20:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 13:00:00 000:000:000 4
2016-06-12 14:00:00 000:000:000 5
2016-06-12 15:00:00 000:000:000 6
[3] row(s) selected.
 
Mach> SELECT _arrival_time, * from from_table duration FROM TO_DATE('2016-6-12 20:00:00', 'YYYY-MM-DD HH24:MI:SS') TO TO_DATE('2016-6-12 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
_arrival_time                   ID
-----------------------------------------------
2016-06-12 15:00:00 000:000:000 6
2016-06-12 14:00:00 000:000:000 5
2016-06-12 13:00:00 000:000:000 4
[3] row(s) selected.
```