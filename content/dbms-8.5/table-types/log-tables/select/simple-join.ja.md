---
title : 単純な JOIN
type: docs
weight: 40
toc: true
---

Log、Volatile、Lookup、メタテーブルを結合して検索できます。


## 単純な JOIN {#simple-join}

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


## 別名を使用した JOIN {#join-using-alias}

結合するテーブルには別名を指定できます。

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


## GROUP BY/ORDER BY {#group-byorder-by}

GROUP BY、ORDER BY、集計関数も使用できます。

```sql
Mach> SELECT t.name, COUNT(c.name) FROM m$sys_columns c, m$sys_tables t WHERE t.id = c.table_id GROUP BY t.name ORDER BY t.name;
t.name                                    count(c.name)
------------------------------------------------------------------
COMMON_TABLE                              5
DURATIONT                                 3
[2] row(s) selected.
```


## 結合条件のない JOIN {#join-without-join-clause}

結合条件のないクエリーはエラーになります。Log テーブルは大量のデータを持つため、条件なしの結合は処理時間を予測できないほど遅くなる可能性があります。

2 つの Log テーブルの結合も非常に遅くなる場合があります。設計時には非正規化を検討し、結合を避ける構成を推奨します。

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


## 内部結合と外部結合 {#inner-join--outer-join}

ANSI 形式の INNER、LEFT OUTER、RIGHT OUTER JOIN を使用できます。FULL OUTER JOIN は使用できません。

```sql
FROM    TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER]  JOIN    TABLE_2 ON  expression
```

```sql
SELECT t1.i1, t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

上のクエリーは、WHERE 句の t2.i2 = 1 により内部結合として動作します。
