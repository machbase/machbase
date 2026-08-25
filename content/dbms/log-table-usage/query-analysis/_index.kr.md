---
title: '7.5 조회와 분석'
weight: 50
toc: true
---

LOG 테이블 데이터를 SELECT, DURATION, JOIN으로 조회하는 방법을 다룹니다.


<a id="original-85-select-data"></a>

## 데이터 검색


ANSI 표준 SQL로 데이터를 검색할 수 있습니다.

아래 예제는 인덱스를 생성하지 않은 상태에서의 검색을 보여줍니다. 마지막에 입력된 데이터가 먼저 출력됩니다.

자세한 내용은 SQL Reference의 [SELECT](/dbms/reference/sql/syntax-dictionary-sql/select-syntax/) 섹션을 참조합니다.


### 기본 검색

```sql
SELECT * FROM table_name;
```

```sql
Index
Basic access
View Conditional Clause
Mach> SELECT * FROM mach_log;
DEVICE          TM                              TEMP
----------------------------------------------------------------
MSG
------------------------------------------------------------------------------------
192.168.0.1     NULL                            NULL
NULL
192.168.0.2     2014-06-15 19:50:03 484:382:010 82
error code = 20, critical warning
192.168.0.2     2014-06-15 19:50:03 484:382:008 57
error code = 20
192.168.0.1     2014-06-15 19:50:03 484:382:006 99
error code = 10, critical bug
192.168.0.1     2014-06-15 19:50:03 484:382:004 55
error code = 10
192.168.0.2     2014-06-15 19:50:03 484:382:002 31
normal state
192.168.0.1     2014-06-15 19:50:03 484:382:000 32
normal state
[7] row(s) selected.
Mach>
```


### 조건절 검색

```sql
SELECT column_name,column_name
FROM table_name
WHERE column_name operator value;
```

```sql
Mach> SELECT * FROM mach_log WHERE device = '192.168.0.1';
DEVICE          TM                              TEMP
----------------------------------------------------------------
MSG
------------------------------------------------------------------------------------
192.168.0.1     NULL                            NULL
NULL
192.168.0.1     2014-06-15 19:50:36 488:663:006 99
error code = 10, critical bug
192.168.0.1     2014-06-15 19:50:36 488:663:004 55
error code = 10
192.168.0.1     2014-06-15 19:50:36 488:663:000 32
normal state
[4] row(s) selected.

Mach> SELECT * FROM mach_log WHERE device = '192.168.0.1' AND temp > 30 AND temp < 50;
DEVICE          TM                              TEMP
----------------------------------------------------------------
MSG
------------------------------------------------------------------------------------
192.168.0.1     2014-06-15 19:50:36 488:663:000 32
normal state
[1] row(s) selected.

Mach> SELECT * FROM mach_log where device > '192.168.0.1';
DEVICE          TM                              TEMP
----------------------------------------------------------------
MSG
------------------------------------------------------------------------------------
192.168.0.2     2014-06-15 19:50:36 488:663:010 82
error code = 20, critical warning
192.168.0.2     2014-06-15 19:50:36 488:663:008 57
error code = 20
192.168.0.2     2014-06-15 19:50:36 488:663:002 31
normal state
[3] row(s) selected.

Mach> SELECT * FROM mach_log WHERE msg LIKE '%error%';
DEVICE          TM                              TEMP
----------------------------------------------------------------
MSG
------------------------------------------------------------------------------------
192.168.0.2     2014-06-15 19:50:36 488:663:010 82
error code = 20, critical warning
192.168.0.2     2014-06-15 19:50:36 488:663:008 57
error code = 20
192.168.0.1     2014-06-15 19:50:36 488:663:006 99
error code = 10, critical bug
192.168.0.1     2014-06-15 19:50:36 488:663:004 55
error code = 10
[4] row(s) selected.
```

### 힌트를 사용한 검색 방향 지정

#### 역방향

기본값이며, /*+ SCAN_BACKWARD(table_name) */ 힌트를 추가하여 검색할 수 있습니다.

```sql
Mach> SELECT * FROM LOG;
TIME
----------------------------------
2021-01-04 00:00:00 000:000:000
2021-01-03 00:00:00 000:000:000
2021-01-02 00:00:00 000:000:000
2021-01-01 00:00:00 000:000:000
[4] row(s) selected.
Elapsed time: 0.001

Mach> SELECT /*+ SCAN_BACKWARD(LOG) */ * FROM LOG;
TIME
----------------------------------
2021-01-04 00:00:00 000:000:000
2021-01-03 00:00:00 000:000:000
2021-01-02 00:00:00 000:000:000
2021-01-01 00:00:00 000:000:000
[4] row(s) selected.
Elapsed time: 0.001
```

#### 정방향

/*+ SCAN_FORWARD(table_name) */ 힌트를 사용하여 정방향으로 검색합니다.

```sql
Mach> SELECT /*+ SCAN_FORWARD(LOG) */ * FROM LOG;
TIME
----------------------------------
2021-01-01 00:00:00 000:000:000
2021-01-02 00:00:00 000:000:000
2021-01-03 00:00:00 000:000:000
2021-01-04 00:00:00 000:000:000
[4] row(s) selected.
Elapsed time: 0.001
```

#### 기본 스캔 방향을 설정하는 프로퍼티

[TABLE_SCAN_DIRECTION](/dbms/reference/configuration/dictionary-configuration/) 프로퍼티를 사용하면
SELECT 문에 힌트가 없을 때 LOG 테이블의 스캔 방향을 지정할 수 있습니다.

<a id="original-85-select-time-data"></a>

## 시계열 데이터 검색


SELECT 문의 DURATION 절은 검색할 시간 범위를 정의합니다. 검색 대상을 줄여 대량의 데이터를 검색할 때 성능을 높이기 위한 핵심 절입니다.

Machbase는 입력 시간을 기준으로 데이터를 분할하여 저장하므로, 시간 조건을 기반으로 데이터를 빠르게 검색할 수 있습니다. 입력 시간은 사용자 정의 컬럼이 아닌 자동 생성된 '_ARRIVAL_TIME' 컬럼에 저장됩니다. 추가 시간 컬럼을 지정하지 않고 내장 '_ARRIVAL_TIME' 컬럼을 사용하는 것이 가장 효율적입니다.

Machbase는 데이터를 입력 순서의 역순으로 출력합니다. 가장 최신 데이터가 먼저, 가장 오래된 데이터가 나중에 나옵니다. 모든 DURATION 조건의 출력도 최신에서 과거 순입니다. 과거에서 최신으로 역순 출력하려면 AFTER 절을 사용합니다.


### 구문

```sql
DURATION    time_expression [BEFORE time_expression];
DURATION    time_expression [AFTER time_expression];
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


### DURATION...BEFORE

BEFORE를 명시적으로 사용하거나 생략하면(자동 BEFORE 적용) 데이터가 최신에서 과거 순으로 출력됩니다.

절대 시간 값 또는 상대 시간 값으로 데이터를 쿼리할 수 있습니다.

#### 절대 시간 값 기반 검색

```sql
Mach> CREATE LOG TABLE time_table (id INTEGER);
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

#### 상대 시간 값 기반 검색

현재 시간을 기준으로 한 검색입니다.

```sql
Mach> CREATE LOG TABLE relative_table(id INTEGER);
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

### DURATION...AFTER

AFTER를 적용하면 데이터가 과거에서 최신 순으로 출력됩니다.

BEFORE는 입력 시간 기준으로 자동 역순(최신 우선) 출력이고, AFTER는 그 반대입니다.

```sql
Mach> CREATE LOG TABLE after_table (id INTEGER);
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


### DURATION...FROM/TO

두 개의 절대 시간을 기준으로 데이터를 검색할 때 "DURATION FROM A TO B" 형태를 사용합니다.

A와 B는 절대 시간이며 TO_DATE 함수로 표현합니다. A와 B의 순서에 따라 출력 방향이 달라집니다.

* A가 B보다 이전이면 AFTER와 같은 방향(과거 → 최신)으로 출력됩니다.
* B가 A보다 이전이면 BEFORE와 같은 방향(최신 → 과거)으로 출력됩니다.

```sql
Mach> CREATE LOG TABLE from_table (id INTEGER);
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

<a id="original-85-simple-join"></a>

## 간단한 Join


Log 테이블, Volatile 테이블, Lookup 테이블 및 메타 테이블을 Join으로 검색할 수 있습니다.


### 간단한 Join

```sql
Mach> CREATE LOG TABLE logtable (code INT,value INT);
Created successfully.

Mach> INSERT INTO logtable VALUES(1,20 );
1 row(s) inserted.

Mach> INSERT INTO logtable VALUES(2,10 );
1 row(s) inserted.

Mach> INSERT INTO logtable VALUES(3,15 );
1 row(s) inserted.

Mach> INSERT INTO logtable VALUES(4,20 );
1 row(s) inserted.

Mach> INSERT INTO logtable VALUES(5,10 );
1 row(s) inserted.

Mach> CREATE VOLATILE table VTABLE (code INT,name VARCHAR(32));
Created successfully.

Mach> INSERT INTO vtable VALUES(1, 'Sam');
1 row(s) inserted.

Mach> INSERT INTO vtable VALUES(3, 'Thomas');
1 row(s) inserted.

Mach> INSERT INTO vtable VALUES(5, 'Micheal');
1 row(s) inserted.

Mach> INSERT INTO vtable VALUES(7, 'Jessica');
1 row(s) inserted.

Mach> SELECT name,value FROM logtable, vtable WHERE logtable.code=vtable.code;
name                              value
-------------------------------------------------
Micheal                           10
Thomas                            15
Sam                               20
[3] row(s) selected.
```


### Alias를 사용한 Join

Join 대상 테이블에 alias를 사용할 수 있습니다.

```sql
SELECT c.name FROM m$sys_tables t, m$sys_columns c WHERE t.id = c.table_id AND t.name = 'T1'
AND c.id NOT IN(0, 65534) ORDER BY c.name;

c.name
--------------------------------------------
ADDR
ISTYPE
SRCIP
[3] row(s) selected.
```


### GROUP BY/ORDER BY

GROUP BY, ORDER BY, 집계 함수도 함께 사용할 수 있습니다.

```sql
Mach> SELECT t.name, COUNT(c.name) FROM m$sys_columns c, m$sys_tables t WHERE t.id = c.table_id GROUP BY t.name ORDER BY t.name;
t.name                                    count(c.name)
------------------------------------------------------------------
COMMON_TABLE                              5
DURATIONT                                 3
[2] row(s) selected.
```


### JOIN 절이 없는 Join

JOIN 절이 없는 조인 쿼리는 오류를 발생시킵니다. Log 테이블에는 데이터가 매우 많기 때문에 조인 조건 없이 쿼리하면 성능을 예측할 수 없습니다.

두 개의 Log 테이블 조인은 매우 느릴 수 있으므로, 데이터베이스를 설계할 때 비정규화를 고려하여 조인을 최소화하는 것이 좋습니다.

```sql
Mach> CREATE LOG TABLE log_table1(i1 INTEGER);
Created successfully.
Mach> INSERT INTO log_table1 VALUES(1);
1 row(s) inserted.
Mach> INSERT INTO log_table1 VALUES(20);
1 row(s) inserted.
Mach> INSERT INTO log_table1 VALUES(30);
1 row(s) inserted.


Mach>CREATE LOG TABLE log_table2(i1 INTEGER);
Created successfully.
Mach> INSERT INTO log_table2 VALUES(1);
1 row(s) inserted.
Mach> INSERT INTO log_table2 VALUES(30);
1 row(s) inserted.
Mach> INSERT INTO log_table2 VALUES(50);
1 row(s) inserted.

Mach> SELECT log_table1.i1 FROM log_table1, log_table2;
[ERR-02101 : Error in joining tables. Cannot join without join predicate.]

Mach> SELECT log_table1.i1 FROM log_table1, log_table2 where log_table1.i1 = 1;
[ERR-02101 : Error in joining tables. Cannot join without join predicate.]

Mach> SELECT log_table1.i1 from log_table1, log_table2 WHERE log_table1.i1 = log_table2.i1;
i1
--------------
30
1
[2] row(s) selected.
```


### Inner Join / Outer Join

ANSI 타입의 INNER, LEFT OUTER, RIGHT OUTER 조인을 사용할 수 있습니다. FULL OUTER JOIN은 지원하지 않습니다.

```sql
FROM    TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER]  JOIN    TABLE_2 ON  expression
```

```sql
SELECT t1.i1, t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

위 쿼리는 where 절의 t2.i2 = 1 조건에 의해 Inner Join으로 변경됩니다.
