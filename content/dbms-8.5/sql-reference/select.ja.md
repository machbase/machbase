---
title : 'SELECT'
type: docs
weight: 40
toc: true
---

## 目次 {#index}

* [SELECT 構文](#select-syntax)
* [FROM なしの SELECT](#select-without-from)
* [集合演算子](#set-operator)
* [選択リスト](#target-list)
    * [CASE 式](#case-statement)
* [FROM](#from)
    * [サブクエリー（インラインビュー）](#subqueryinline-view)
    * [保存されたビュー](#stored-view)
    * [JOIN(INNER JOIN)](#joininner-join)
    * [内部結合と外部結合](#inner-join-and-outer-join)
    * [PIVOT](#pivot)
* [WHERE](#where)
    * [サブクエリーの使用](#use-of-subquery)
    * [SEARCH](#search-statement)
    * [ESEARCH](#esearch-statement)
    * [NOT SEARCH](#not-search-statement)
    * [REGEXP](#regexp-statement)
    * [IN](#in-statement)
    * [IN とサブクエリー](#use-in-statement-and-subquery)
    * [BETWEEN](#between-statement)
    * [RANGE](#range-statement)
* [GROUP BY / HAVING](#group-by--having)
* [ORDER BY](#order-by)
* [SERIES BY](#series-by)
* [LIMIT](#limit)
* [DURATION](#duration)
* [データの保存](#save-data)


`SELECT` は、各テーブルのデータを検索、抽出、加工する構文です。

## `SELECT` 構文 {#select-syntax}

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT target_list [FROM table_list]
[WHERE condition_expr]
[GROUP BY expr] [HAVING expr]
[ORDER BY expr [DESC]] [SERIES BY expr]
[LIMIT n[,n]]
[DURATION duration_expr];
```

通常は `FROM` を使用しますが、単純な式は
`FROM` なしでも実行できます。

## `FROM` なしの `SELECT` {#select-without-from}

テーブルを読み取らず、定数、文字列リテラル、算術式、
単純な関数の結果を 1 行返します。接続確認や
簡単な計算に利用できます。

```sql
select 1;
select 'alive';
select 1 + 2;
select abs(-7);
```

各クエリーは 1 行を返します。

次の拡張形式はサポートしません。

```sql
select distinct 1;
select 1 where 1 = 1;
select 1 order by 1;
select count(*);
select *;
```

未対応の形式は、通常次のエラーになります。

```text
ERR-02362: This statement is not supported.
```

`select *;` は、次のエラーになる場合があります。

```text
ERR-02039: No table specified in the target list.
```

`FROM` なしの `SELECT` は、単一行の式だけを対象とします。集計関数、
ソート、条件、周期指定、ヒントは使用できません。

## 集合演算子 {#set-operator}

複数の `SELECT` の結果を、1 つの結果にまとめます。
Machbase は `UNION ALL` だけをサポートします。左右の `SELECT` は、
（1）同じ型または互換型、（2）同じ結果列数である
必要があります。いずれかを満たさない場合は
エラーになります。

型の互換性と変換は、次の規則に従います。
* 符号付き整数と符号なし整数は互換ではありません。
* 整数と実数は互換で、結果を実数型へ変換します。
* 長さが異なる文字列型は互換です。
* IPv4 と IPv6 は互換ではありません。
* 列名は常に左側の `SELECT` を使用します。

例

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2
```


## 選択リスト {#target-list}

`SELECT` の対象となる列やサブクエリーの一覧です。

選択リストのサブクエリーは、WHERE のスカラーサブクエリーと同様に、2 行以上または 2 列以上を返すとエラーになります。

```sql
SELECT i1, i2 ...
SELECT i1 (Select avg(c1) FROM t1), i2 ...
```

## CASE 式 {#case-statement}

```sql
CASE <simple_case_expression|searched_case_expression> [else_clause] END
 
simple_case_expression ::=
    expr WHEN comparison_expr THEN return_expr
        [WHEN comparison_expr THEN return_expr ...]
 
searched_case_expression ::=
    WHEN condtion_expr THEN return EXPR [WHEN condtion_expr THEN return EXPR ...]
 
else_clause ::=
    ELSE else_value_expr
```

一般的な IF ... THEN ... ELSE に相当します。simple_case_expression は、CASE の列や式が WHEN の comparison_expr と一致すると return_expr を返します。WHEN ... THEN は複数指定できます。

searched_case_expression は CASE の後に式を書かず、WHEN に比較条件を指定します。最初に真になる THEN の値を返します。どの条件も満たさない場合（NULL を含む）は ELSE の値を返します。

```sql
select * from t1;
I1          I2         
---------------------------
2           2          
1           1          
[2] row(s) selected.
 
select case i1 when 1 then 100 end from t1;
case i1 when 1 then 100 end
------------------------------
NULL       
100        
[2] row(s) selected.
```

単純 CASE の例では、i1 が 2 の場合に NULL を返します。

```
select case when i1 > 0 then 100 when i1 > 1 then 200 end from t1;
case when i1 > 0 then 100 when i1 > 1 then 200 end
------------------------------------------
100        
100        
[2] row(s) selected.
```

検索 CASE の例では、最初の条件が成立して 100 を返し、2 番目の条件は評価しません。


## `FROM` {#from}

`FROM` にはテーブル名またはインラインビューを指定します。結合では、対象をカンマで区切って列挙できます。

```sql
FROM table_name
```

table_name で指定したテーブルを取得します。

### サブクエリー（インラインビュー） {#subqueryinline-view}

```sql
FROM (Select statement)
```

括弧内のサブクエリーの結果を取得します。

* 相関サブクエリーは未サポートです。サブクエリーから外側のクエリーの列を参照できません。

### 保存されたビュー {#stored-view}

`FROM` には、事前に `CREATE VIEW` で作成したビューも指定できます。
インラインビューと異なり、名前付きの論理オブジェクトです。
`DESC`、`SHOW VIEWS`、`M$SYS_VIEWS` でメタデータを確認できます。

```sql
SELECT *
FROM v_customer
WHERE id = 100;
```

作成、削除、メタデータ、性能と制限、Tag/`BINARY` の例は、
[VIEW](../view) を参照してください。

### JOIN（内部結合） {#joininner-join}

```sql
JOIN(INNER JOIN)
```

table_1 と table_2 を結合します。3 つ以上のテーブルでも内部結合でき、結合条件と検索条件を WHERE に記述します。

```sql
SELECT t1.i1, t2.i1 FROM t1, t2 WHERE t1.i1 = t2.i1 AND t1.i1 > 1 AND t2.i2 = 3;
```

### 内部結合と外部結合 {#inner-join-and-outer-join}

ANSI 形式の INNER、LEFT OUTER、RIGHT OUTER JOIN をサポートします。FULL OUTER JOIN は未サポートです。

```sql
FROM TABLE_1 [INNER|LEFT OUTER|RIGHT OUTER] JOIN TABLE_2 ON expression
```

ON に結合条件を指定します。外部結合で、ON に一致しないと NULL で補われる側のテーブルに WHERE 条件を指定すると、内部結合へ変換されます。

```sql
SELECT t1.i1, t2.i1 FROM t1 LEFT OUTER JOIN t2 ON (t1.i1 = t2.i1) WHERE t2.i2 = 1;
```

上の例は、WHERE の t2.i2 = 1 により内部結合になります。

### PIVOT {#pivot}

* PIVOT は Machbase 5.6 以降でサポートされます。

**pivot_clause:**

![pivot_clause](/images/sql/select/pivot_clause.png)


GROUP BY の集計結果を、行から列へ並べ替えて表示します。

インラインビューと組み合わせ、次のように処理します。
* PIVOT で使わない列を GROUP BY し、PIVOT IN の値に対して集計関数を実行します。
* グループ化した列と集計結果を、列方向に展開します。

複数センサーのデータから、デバイスごとの値を集計する例です。
CASE で書く集計を、PIVOT で簡潔に表現できます。

```sql
-- PIVOT なし
SELECT * FROM (
    SELECT
             regtime,
             SUM(CASE WHEN tagid = 'FRONT_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS front_axis_torque,
             SUM(CASE WHEN tagid = 'REAR_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS rear_axis_torque,
             SUM(CASE WHEN tagid = 'HOIST_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS hoist_axis_torque,
             SUM(CASE WHEN tagid = 'SLIDE_AXIS_TORQUE' THEN dvalue ELSE 0 END)  AS slide_axis_torque
    FROM     result_d
    WHERE    regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
    GROUP BY regtime
) WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;
  
-- PIVOT あり
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
    WHERE  regtime BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
) PIVOT (SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE'))
WHERE front_axis_torque >= 40 AND rear_axis_torque >= 20;
 
-- 結果
regtime                         'FRONT_AXIS_TORQUE'         'REAR_AXIS_TORQUE'          'HOIST_AXIS_TORQUE'         'SLIDE_AXIS_TORQUE'       
------------------------------------------------------------------------------------------------------------------------------------------------------
2018-12-07 16:42:29 840:000:000 12158                       7244                        NULL                        NULL                      
2018-12-07 14:56:26 220:000:000 3308                        663                         NULL                        NULL                      
2018-12-07 12:20:13 844:000:000 3804                        113                         NULL                        NULL                      
2018-12-07 11:10:01 957:000:000 8729                        5384                        NULL                        NULL                      
2018-12-07 17:46:57 812:000:000 7500                        4559                        NULL                        NULL                      
2018-12-07 14:30:06 138:000:000 5080                        6817                        NULL                        -429                      
2018-12-07 13:09:20 464:000:000 5233                        1869                        -7253                       NULL                      
2018-12-07 15:43:03 539:000:000 7491                        4453                        NULL                        NULL
...
```


## WHERE {#where}

### サブクエリーの使用 {#use-of-subquery}

条件にサブクエリーを使用できます。IN 以外で複数行を返す場合や、複数列を返す場合はサポートしません。

```sql
WHERE i1 = (SELECT MAX(c2) FROM T1)
```

比較演算子の右側に、括弧で囲んで指定します。

* 相関サブクエリーは未サポートです。サブクエリーから外側の列を参照できません。

### SEARCH {#search-statement}

通常の条件に加えて、キーワードインデックスを作成すると SEARCH 演算子でテキスト検索できます。

```sql
-- drop table realdual;
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
 
create keyword index idx1 on realdual (id2);
create keyword index idx2 on realdual (id3);
 
insert into realdual values(1, 'time time2', 'series series2');
 
select * from realdual;
 
select * from realdual where id2 search 'time';
select * from realdual where id3 search 'series' ;
select * from realdual where id2 search 'time' and id3 search 'series';
```

結果：

```sql
Mach> create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
Created successfully.
 
Mach> create keyword index idx1 on realdual (id2);
Created successfully.
 
Mach> create keyword index idx2 on realdual (id3);
Created successfully.
 
Mach> insert into realdual values(1, 'time time2', 'series series2');
1 row(s) inserted.
 
Mach> select * from realdual;
ID1         ID2                   ID3                  
------------------------------------------------------------
1           time time2            series series2 
[1] row(s) selected.
 
Mach> select * from realdual where id2 search 'time';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.
 
Mach> select * from realdual where id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.
 
Mach> select * from realdual where id2 search 'time' and id3 search 'series';
ID1         ID2                   ID3
------------------------------------------------------------
1           time time2            series series2
[1] row(s) selected.
```

### ESEARCH {#esearch-statement}

ESEARCH は ASCII テキストの拡張検索です。% でパターンを指定します。LIKE で先頭に % を置くと全レコードを調べますが、ESEARCH はその場合もインデックス内の語を高速に検索できます。英語のエラーメッセージやコードの部分検索に役立ちます。

```sql
-- 例
 
select id2 from realdual where id2 esearch 'bbb%';
id2
--------------------------------------------
bbb ccc1
aaa bbb1
 
[2] row(s) selected.
 
-- bbb% の検索結果には bbb1 も含む
 
 
select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
 
-- % は先頭や末尾だけでなく途中にも使用可能
 
select id3 from realdual where id3 esearch '%cd%';
id3
--------------------------------------------
cdf def1
bcd/cdf1ad
abc, bcd1
[3] row(s) selected.
```

### NOT SEARCH {#not-search-statement}

SEARCH に一致しないレコードに対して真を返します。

NOT ESEARCH は使用できません。

```sql
create table t1 (id integer, i2 varchar(10));
create keyword index t1_i2 on t1(i2);
insert into t1 values (1, 'aaaa');
insert into t1 values (2, 'bbbb');
 
select id from t1 where i2 not search 'aaaa';
 
id
--------------------------------------------
2
[1] row(s) selected.
```

### REGEXP {#regexp-statement}

正規表現でデータを検索し、列の文字列パターンを絞り込みます。

インデックスを利用できないため、他の列にインデックス条件を付けて検索対象を減らしてください。
SEARCH/ESEARCH で先に対象を絞ってから REGEXP を適用すると、全体の効率を改善できます。

```sql
Mach>
create table realdual (id1 integer, id2 varchar(20), id3 varchar(20));
create table dual (id integer);
insert into dual values(1);
insert into realdual values(1, 'time1', 'series1 series21');
insert into realdual values(1, 'time2', 'series2 series22');
insert into realdual values(1, 'time3', 'series3 series32');
 
 
Mach> select * from realdual where id2 REGEXP 'time' ;
ID1         ID2                   ID3                  
------------------------------------------------------------
1           time3                 series3 series32
1           time2                 series2 series22
1           time1                 series1 series21
[3] row(s) selected.
 
Mach> select * from realdual where id2 REGEXP 'time[12]' ;
ID1         ID2                   ID3                  
------------------------------------------------------------
1           time2                 series2 series22
1           time1                 series1 series21
[2] row(s) selected.
 
Mach> select * from realdual where id2 REGEXP 'time[13]' ;
ID1         ID2                   ID3                  
------------------------------------------------------------
1           time3                 series3 series32
1           time1                 series1 series21
[2] row(s) selected.
 
Mach> select * from realdual where id2 regexp 'time[13]' and id3 regexp 'series[12]';
ID1         ID2                   ID3                  
------------------------------------------------------------
1           time1                 series1 series21 
[1] row(s) selected.
 
Mach> select * from realdual where id2 NOT REGEXP 'time[12]';
ID1         ID2                   ID3                  
------------------------------------------------------------
1           time3                 series3 series32
[1] row(s) selected.
 
Mach> SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' from dual;
'abcde' REGEXP 'a[bcd]{1,10}e'
---------------------------------
1          
[1] row(s) selected.
```

### IN {#in-statement}

```sql
column_name IN (value1, value2,...)
```

値がリストに含まれると真を返します。OR で連結した条件と同等です。

### IN とサブクエリー {#use-in-statement-and-subquery}

IN の右側にサブクエリーを指定し、左側の値が結果に含まれるか確認します。左側に複数の列を指定するとエラーになります。

```sql
WHERE i1 IN (Select c1 from ...)
```

* 相関サブクエリーは未サポートです。サブクエリーから外側の列を参照できません。

### BETWEEN {#between-statement}

```sql
column_name BETWEEN value1 AND value2
```

列の値が value1 から value2 の範囲内なら真を返します。

### RANGE {#range-statement}

```sql
column_name RANGE duration_spec;
 
-- duration_spec : integer (YEAR | WEEK | HOUR | MINUTE | SECOND);
```

指定列の時刻条件を簡単に記述する演算子です。特定の絶対時刻ではなく、現在時刻を基準とする範囲を対象にし、必要な期間のレコードを取得できます。

```sql
select * from test where id < 2 and c1 range 1 hour;
ID          C1                             
-----------------------------------------------
1           2014-07-25 09:28:53 706:707:001
[1] row(s) selected.
```


## GROUP BY / HAVING {#group-by--having}

GROUP BY は指定列の値が同じ行をグループにまとめ、集計関数などを適用します。後ろに HAVING を付けると、集計したグループのうち条件に一致するものだけを取得できます。

```sql
SELECT ...
GROUP BY { col_name | expr } ,...[ HAVING <search_condition> ]
 
select id1, avg(id2) from exptab where id2 group by id1 order by id1;
-- id1 でグループ化し、id2 の平均を求める。
```


## ORDER BY {#order-by}

結果を昇順または降順に並べます。ASC/`DESC` を省略すると昇順です。ORDER BY 自体を省略した場合の順序は、クエリーによって異なります。

```sql
SELECT ...
ORDER BY {col_name | expr} [ASC | DESC]
 
select id1, avg(id2) from exptab where id2 group by id1 order by id1;
-- id1 でグループ化し、id2 の平均を求める。
```


## SERIES BY {#series-by}

並べた結果を SERIES BY 条件に一致する連続した系列として抽出します。ORDER BY がなければ _ARRIVAL_TIME で並べます。GROUP BY を使用する場合や、_ARRIVAL_TIME のない Volatile/Lookup では、ORDER BY が必要です。

同じ連続条件に属する結果は、SERIESNUM() が同じ値を返します。

```sql
-- 次のデータを使用する例
 
CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
INSERT INTO T1 VALUES (0, 1);
 
INSERT INTO T1 VALUES (1, 2);
 
INSERT INTO T1 VALUES (2, 3);
 
INSERT INTO T1 VALUES (3, 2);
 
INSERT INTO T1 VALUES (4, 1);
 
INSERT INTO T1 VALUES (5, 2);
 
INSERT INTO T1 VALUES (6, 3);
 
INSERT INTO T1 VALUES (7, 1);
 
 
-- 次のクエリーは、以下の結果を返す。
 
SELECT C1,C2 FROM T1 ORDER BY C1 SERIES BY C2>1;
C1          C2         
---------------------------
1           2          
2           3          
3           2          
5           2          
6           3   
 
-- C2 が 1 より大きい区間に対応する C1 の範囲は、SERIESNUM で各レコードの系列番号を取得して確認できます。
```


## LIMIT {#limit}

出力するレコード数を制限します。整数で結果セットの開始位置と件数を指定できます。

```sql
LIMIT [offset,] row_count
 
select id1, avg(id2) from exptab where id2 group by id1 order by id1 LIMIT 10;
```


## DURATION {#duration}

`_arrival_time` を基に検索範囲を限定します。BEFORE と組み合わせて特定時刻を基準とする範囲を指定できます。対象を減らすことで性能を改善し、負荷を軽減します。詳しい使用例を示します。

```sql
DURATION Number TimeSpec [BEFORE/AFTER Number TimeSpec]
DURATION FROM expr TO expr
TimeSpec : YEAR | MONTH | WEEK |  DAY | HOUR | MINUTE | SECOND
```

`DURATION FROM expr TO expr` は、`_arrival_time` の明示的な範囲を指定します。
`expr` には `TO_DATE(value, format)` などの日時式を使用できます。

```sql
create table t8(i1 integer);
insert into t8 values(1);
insert into t8 values(2);
 
select i1 from t8;
 
-- BEFORE なし
select i1 from t8 duration 2 second;
select i1 from t8 duration 1 minute;
select i1 from t8 duration 1 hour;
select i1 from t8 duration 1 day;
select i1 from t8 duration 1 week;
select i1 from t8 duration 1 month;
select i1 from t8 duration 1 year;
 
-- 完全な DURATION 構文
select i1 from t8 duration 1 second before 1 day;
select i1 from t8 duration 1 minute before 1 day;
select i1 from t8 duration 1 hour before 1 day;
select i1 from t8 duration 1 day before 1 day;
select i1 from t8 duration 1 week before 1 day;
select i1 from t8 duration 1 month before 1 day;
select i1 from t8 duration 1 year before 1 day;

-- 明示的な範囲を使用
select i1 from t8
duration from to_date('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
       to to_date('2030-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

結果：

```sql
Mach> create table t8(i1 integer);
Created successfully.
 
Mach> insert into t8 values(1);
1 row(s) inserted.
 
Mach> insert into t8 values(2);
1 row(s) inserted.
 
Mach> select i1 from t8;
i1         
--------------
2          
1          
[2] row(s) selected.
 
#BEFORE なし
Mach> select i1 from t8 duration 2 second;
i1         
--------------
2          
1          
[2] row(s) selected.
 
Mach> select i1 from t8 duration 1 minute;
i1         
--------------
2          
1          
[2] row(s) selected.
 
Mach> select i1 from t8 duration 1 hour;
i1         
--------------
2          
1          
[2] row(s) selected.
 
Mach> select i1 from t8 duration 1 day;
i1         
--------------
2          
1          
[2] row(s) selected.
 
Mach> select i1 from t8 duration 1 week;
i1         
--------------
2          
1          
[2] row(s) selected.
 
Mach> select i1 from t8 duration 1 month;
i1         
--------------
2          
1          
[2] row(s) selected.
 
Mach> select i1 from t8 duration 1 year;
i1         
--------------
2          
1          
[2] row(s) selected.
 
-- 完全な DURATION 構文
Mach> select i1 from t8 duration 1 second before 1 day;
i1         
--------------
[0] row(s) selected.
 
Mach> select i1 from t8 duration 1 minute before 1 day;
i1         
--------------
[0] row(s) selected.
 
Mach> select i1 from t8 duration 1 hour before 1 day;
i1         
--------------
[0] row(s) selected.
 
Mach> select i1 from t8 duration 1 day before 1 day;
i1         
--------------
[0] row(s) selected.
 
Mach> select i1 from t8 duration 1 week before 1 day;
i1         
--------------
[0] row(s) selected.
 
Mach> select i1 from t8 duration 1 month before 1 day;
i1         
--------------
[0] row(s) selected.
 
Mach> select i1 from t8 duration 1 year before 1 day;
i1         
--------------
[0] row(s) selected.
```


## データの保存（SAVE DATA） {#save-data}

クエリー結果を直接 CSV に保存します。

```sql
SAVE DATA INTO 'file_name.csv' [HEADER ON|OFF] [(FIELDS | COLUMNS) [TERMINATED BY 'char'] [ENCLOSED BY 'char']] [ENCODED BY coding_name] AS select query;
```

オプション：

| オプション | 説明 |
|--|--|
|HEADER (ON\|OFF)|先頭行に列名を出力するか。既定は OFF。|
|(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br>ENCLOSED BY 'enclose_char'|出力 CSV のフィールド区切りと囲み文字を指定。|
|ENCODED BY coding_name<br>coding_name = ( UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280 )|出力ファイルの文字コード。既定は UTF8。|

```sql
SAVE DATA INTO '/tmp/aaa.csv' AS select * from t1;
-- 結果を CSV 形式で /tmp/aaa.csv に保存
  
SAVE DATA INTO '/tmp/ccc.csv' HEADER ON FIELDS TERMINATED BY ';' ENCLOSED BY '\'' ENCODED BY MS949 AS select * from t1 where i1 > 100;
-- 結果を /tmp/ccc.csv に保存。区切りと囲み文字、MS949 を指定
```
