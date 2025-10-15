---
title : 간단한 Join
type: docs
weight: 40
---

Log 테이블, Volatile 테이블, Lookup 테이블 및 메타 테이블을 Join으로 검색할 수 있습니다.


## 간단한 Join

```sql
Mach> CREATE TABLE logtable (code INT,value INT);
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


## Alias를 사용한 Join

Join을 사용할 때 조인 대상 테이블에 대해 alias를 사용할 수 있습니다.

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


## GROUP BY/ORDER BY 

GROUP BY, ORDER BY 및 집계 함수도 사용할 수 있습니다.

```sql
Mach> SELECT t.name, COUNT(c.name) FROM m$sys_columns c, m$sys_tables t WHERE t.id = c.table_id GROUP BY t.name ORDER BY t.name;
t.name                                    count(c.name)
------------------------------------------------------------------
COMMON_TABLE                              5
DURATIONT                                 3
[2] row(s) selected.
```


## JOIN 절이 없는 Join 

JOIN 절이 없는 조인 쿼리는 오류를 발생시킵니다. Log 테이블에는 데이터가 매우 많기 때문에 조인 조건 없이 쿼리하는 속도는 예측할 수 없을 정도로 느립니다.

또한 두 개의 Log 테이블 조인은 매우 느릴 수 있습니다. 따라서 데이터베이스를 설계할 때는 비정규화를 고려하여 조인이 발생하지 않도록 설계하는 것이 좋습니다.

```sql
Mach> CREATE TABLE log_table1(i1 INTEGER);
Created successfully.
Mach> INSERT INTO log_table1 VALUES(1);
1 row(s) inserted.
Mach> INSERT INTO log_table1 VALUES(20);
1 row(s) inserted.
Mach> INSERT INTO log_table1 VALUES(30);
1 row(s) inserted.
 
 
Mach>CREATE TABLE log_table2(i1 INTEGER);
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


## Inner Join / Outer Join

ANSI 타입의 INNER, LEFT OUTER 또는 RIGHT OUTER 조인을 사용할 수 있지만, FULL OUTER JOIN은 사용할 수 없습니다.

```sql
FROM    TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER]  JOIN    TABLE_2 ON  expression
```

```sql
SELECT t1.i1 t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

위 쿼리는 where 절의 t2.i2 = 1 조건에 의해 Inner Join으로 변경됩니다.
