---
title : 시계열 데이터 검색
type: docs
weight: 20
---

SELECT 문의 DURATION 절은 검색할 시간 조건을 정의합니다. DURATION 절을 사용하는 주요 이유는 검색 대상을 줄여서 대량의 데이터를 검색할 때에도 성능을 향상시키기 위함입니다.

Machbase는 입력 시간을 기준으로 데이터를 분할하여 저장하기 때문에, 시간 조건을 기반으로 데이터를 쉽게 검색할 수 있습니다. 입력 시간은 사용자 정의 컬럼이 아닌 자동 생성된 '_ARRIVAL_TIME'이라는 컬럼에 저장됩니다. 따라서 Machbase를 가장 효율적으로 사용하려면 추가 시간 컬럼을 지정하지 않고 내장 '_ARRIVAL_TIME' 컬럼을 사용하는 것이 좋습니다.

Machbase는 데이터를 입력 순서의 역순으로 출력합니다. 즉, 가장 최신 데이터가 먼저 출력되고, 가장 오래된 데이터가 나중에 출력됩니다. 일반적으로 시계열 데이터를 검색할 때 가장 최근 데이터가 더 중요하고 먼저 얻어야 하는 경우가 많습니다. 또한 모든 DURATION 조건에 의해 출력되는 데이터는 최신에서 마지막 순으로 출력됩니다. 과거에서 최신으로의 역순으로 출력하려면 AFTER 절을 사용해야 합니다. 구문은 다음과 같습니다.


## 구문

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

앞서 언급했듯이, BEFORE를 명시적으로 사용하거나 정의하지 않으면(자동으로 BEFORE 적용) 데이터가 최신에서 가장 오래된 순서로 출력됩니다.

절대 시간 값 또는 상대 시간 값으로 데이터를 쿼리할 수 있습니다.

### 절대 시간 값 기반 검색

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

### 상대 시간 값 기반 검색

상대 시간 값 기반 검색은 현재 시간을 기준으로 한 검색으로 볼 수 있습니다.

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

AFTER를 적용하면 데이터가 과거에서 최신 순으로 출력됩니다.

BEFORE 명령은 과거 출력과 비교하여 입력 시간을 기준으로 데이터를 자동으로 역순으로 출력합니다.

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

사용자가 두 개의 절대 시간을 기준으로 데이터를 검색하려고 할 때, "DURATION FROM A TO B" 형태의 조건식을 사용합니다.

A와 B는 절대 시간이며 TO_DATE 함수를 사용하여 표현됩니다. A와 B는 사용자의 의도에 따라 다르게 설정할 수 있습니다. 예를 들어,

* A가 B보다 나중일 때, 검색 방향은 BEFORE에서 사용하는 것처럼 최신에서 가장 오래된 순서로 데이터를 출력합니다.
* B가 A보다 이전일 때, 검색 방향은 AFTER에서 사용하는 것처럼 가장 오래된 것에서 최신 순서로 데이터를 출력합니다.

다음 예제는 데이터가 어떻게 출력되는지 보여줍니다.

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
