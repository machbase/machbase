---
title : '단순 Join'
type: docs
weight: 40
---

로그 테이블, 휘발성 테이블, 참조 테이블과 메타 테이블은 Join 하여 검색할 수 있다.

## 단순 Join

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

## Alias 를 이용한 Join

Join을 사용할 때, join 대상 테이블에 alias를 사용할 수 있다.

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

## GROUP BY/ORDER BY 사용

GROUP BY, ORDER BY 와 집계 함수도 사용 가능하다.

```sql
Mach> SELECT t.name, COUNT(c.name) FROM m$sys_columns c, m$sys_tables t WHERE t.id = c.table_id GROUP BY t.name ORDER BY t.name;
t.name                                    count(c.name)
------------------------------------------------------------------
COMMON_TABLE                              5
DURATIONT                                 3
[2] row(s) selected.
```

## 조건절 없는 Join

JOIN 조건절이 없는 join 질의는 에러를 발생시킨다. 로그 테이블에 너무나 많은 데이터가 있기 때문에, join 조건절이 없는 질의의 속도는 예측할 수 없을 정도로 느리기 때문이다.

또한, 두개의 로그 테이블 join은 매우 성능이 느릴 수 있다. 그래서 데이터베이스를 설계할 때, 역정규화(denormalization)를 고려하여 join이 발생하지 않도록 설계하는 것이 좋다.

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

ANSI 타입의 INNER, LEFT OUTER, RIGHT OUTER join을 사용할 수 있으나 FULL OUTER JOIN은 사용할 수 없다.

```sql
FROM    TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER]  JOIN    TABLE_2 ON  expression
```
```sql
SELECT t1.i1 t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```
위 질의는 where절의 t2.i2 = 1 조건에 의해서 Inner Join 으로 변경되어 실행된다.

