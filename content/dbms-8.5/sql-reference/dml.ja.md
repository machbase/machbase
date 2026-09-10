---
title : 'DML'
type: docs
weight: 30
toc: true
---

## INSERT {#insert}

**insert_stmt:**

![insert_stmt](/images/sql/dml/insert_stmt.png)

**insert_column_list:**

![insert_column_list](/images/sql/dml/insert_column_list.png)

**value_list:**

![value_list](/images/sql/dml/value_list.png)

**set_list:**

![set_list](/images/sql/dml/set_list.png)

```sql
insert_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? 'METADATA'? 'VALUES' '(' value_list ')' ( 'ON DUPLICATE KEY UPDATE' ( 'SET' set_list )? )?
insert_column_list ::= column_name ( ',' column_name )*
value_list ::= value ( ',' value )*
set_list ::= column_name '=' value ( ',' column_name '=' value )*
```

```sql
create table test (number int,name varchar(20));
Created successfully.
insert into test values (1,"test");
1 row(s) inserted.
insert into test(name,number) values ("test",2);
1 row(s) inserted.
```

指定したテーブルに値を挿入します。Column_List にない列には NULL が格納されます。ログの特性に合わせ、入力の簡便さとストレージ効率を優先した方式です。
METADATA は Tag テーブルでのみ使用できます。

### INSERT ON DUPLICATE KEY UPDATE {#insert-on-duplicate-key-update}

一般的な UPSERT に相当する構文です。

主キーを持つ Lookup/Volatile テーブルで使用します。主キーが重複した場合、既存の値を更新します。
重複がなければ、新しいデータとして挿入します。

Volatile テーブルでは、主キーを定義する必要があります。

挿入用の値とは異なる値や列を更新する場合は、SET 句を追加します。

* SET 句には column `=` value をカンマで区切って指定します。
* SET 句で主キーの値は変更できません。


## INSERT SELECT {#insert-select}

insert_select_stmt:

![insert_select_stmt](/images/sql/dml/insert_select_stmt.png)

```sql
insert_select_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? select_stmt
```

SELECT の結果を指定したテーブルに挿入します。他の DBMS と基本は同じですが、次の違いがあります。
1. SELECT と INSERT の列リストに _ARRIVAL_TIME がなければ、INSERT SELECT 実行時の時刻を格納します。
2. VARCHAR の最大長を超える入力は、エラーにせず最大長に切り詰めます。
3. 型変換が可能な場合（数値から数値など）は、対象の列型に変換して挿入します。
4. 実行中にエラーが発生しても ROLLBACK されません。
5. _ARRIVAL_TIME を指定する場合、既存データより前の時刻は挿入されません。

```sql
create table t1 (i1 integer, i2 varchar(60), i3 varchar(5));
Created successfully.
 
insert into t1 values (1, 'a', 'ddd' );
1 row(s) inserted.
insert into t1 values (2, 'kkkkkkkkkkkkkkkkkkkkk', 'c');
1 row(s) inserted.
 
insert into t1 select * from t1;
2 row(s) inserted.
create table t2 (i1 integer, i2 varchar(60), i3 varchar(5));
 
insert into t2 (_arrival_time, i1, i2, i3) select _arrival_time, * from t1;
4 row(s) inserted.
```


## UPDATE {#update}

* バージョン 5.5 以降で使用できます。

**update_stmt:**

![update_stmt](/images/sql/dml/update_stmt.png)


**update_expr_list:**

![update_expr_list](/images/sql/dml/update_expr_list.png)


**update_expr:**

![update_expr](/images/sql/dml/update_expr.png)

```sql
update_stmt ::= 'UPDATE' table_name ( 'METADATA' )? 'SET' update_expr_list 'WHERE' primary_key_column '=' value
update_expr_list ::= update_expr ( ',' update_expr)*
update_expr ::= column '=' value
```

主キーによる更新に加え、INSERT ON DUPLICATE KEY UPDATE も使用できます。
主キーを持つ Lookup/Volatile テーブルの値を更新します。`WHERE` 句には主キーの等価条件を指定する必要があります。

### UPDATE METADATA {#update-metadata}

TAGDATA テーブルのメタデータを更新する場合に使用します。

```sql
UPDATE TAG METADATA SET ...
```
 
* TAGDATA のメタデータは INSERT ON DUPLICATE KEY UPDATE では挿入、更新できません。
* `TAG METADATA` は、`WHERE NAME = ...` に加え、メタデータの条件も指定できます。
* `TIME`、`VALUE` などのデータ列は `UPDATE ... METADATA` では更新できません。
* 更新できるのは `NAME` とメタデータ列だけです。

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```


## DELETE {#delete}

**delete_stmt:**

![delete_stmt](/images/sql/dml/delete_stmt.png)


**time_unit:**

![time_unit](/images/sql/dml/time_unit.png)

```sql
delete_stmt ::= 'DELETE FROM' table_name ( 'OLDEST' number 'ROWS' | 'EXCEPT' number ( 'ROWS' | time_unit ) | 'BEFORE' datetime_expression )? 'NO WAIT'?
time_unit ::= 'DURATION' number time_unit ( ( 'BEFORE' | 'AFTER' ) number time_unit )?
```

`DELETE BEFORE` は Log、Tag、ロールアップテーブルで使用できます。Log テーブルの DELETE は、途中の任意のレコードだけを削除できません。指定位置から最古のレコードまでを連続して削除します。

これはログの特性に合わせた方式で、記録済みのファイルを削除して空き領域を確保する操作に相当します。

DURATION、OLDEST、EXCEPT は Tag/ロールアップテーブルでは使用できません。

```sql
-- 全件削除
DELETE FROM devices;
 
-- 最も古い N 行を削除
DELETE FROM devices OLDEST N ROWS;
 
-- 最新 N 行以外を削除
DELETE FROM devices EXCEPT N ROWS;
 
-- 現在から N の期間を残して削除
DELETE FROM devices EXCEPT N DAY;
 
-- 2014 年 6 月 1 日より前を削除
DELETE FROM devices BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
 
-- 2014 年 6 月 1 日より前の Tag データを削除
DELETE FROM tag BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
 
-- 2014 年 6 月 1 日より前のロールアップを削除
DELETE FROM tag ROLLUP BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
```


## DELETE `WHERE` {#delete-where}

**delete_where_stmt:**

![delete_where_stmt](/images/sql/dml/delete_where_stmt.png)

```sql
delete_where_stmt ::= 'DELETE FROM' table_name 'WHERE' column_name '=' value
```

```sql
create volatile table t1 (i1 int primary key, i2 int);
Created successfully.
insert into t1 values (2,2);
1 row(s) inserted.
delete from t1 where i1 = 2;
1 row(s) deleted.
```

* Volatile/Lookup の `WHERE` 条件に一致するレコードを削除します。
* テーブルには主キーの定義が必要です。
* 条件は「主キー列 `=` 値」だけを指定でき、他の条件と組み合わせられません。
* 主キー以外の列は条件に使用できません。

### `DELETE FROM TAG METADATA` {#delete-from-tag-metadata}

`DELETE FROM TAG METADATA` で TAGDATA のメタデータを削除できます。
`WHERE` を省略すると、すべてのメタデータ行を削除します。

```sql
DELETE FROM tag METADATA;
DELETE FROM tag METADATA WHERE name = 'tag-1';
DELETE FROM tag METADATA WHERE status = 'STOP';
```

注意事項：

- `WHERE NAME = ...` に加え、メタデータの条件も指定できます。
- 対象タグのいずれかにデータ行が残っている場合、文全体が失敗します。
- 使用中のタグのメタデータは削除できません。
- 全メタデータの削除でも、使用中の対象タグが 1 つでもあれば全体が失敗し、
  一部のメタデータだけが削除されることはありません。
- タグ名の列が `name` 以外の名前でも、同じ構文を使用できます。

**delete_from_tag_where_stmt:**

![delete_from_tag_where_stmt](/images/sql/dml/delete_from_tag_where_stmt.png)

```sql
delete_from_tag_where_stmt ::= 'DELETE FROM' table_name 'ROLLUP'? 'WHERE' predicate
```

Tag/ロールアップテーブルは、タグ名、タグ名と時刻、または時刻だけによる制限付き DELETE 条件をサポートします。

時刻条件には `=`、`<`、`<=`、`BETWEEN` を使用できます。

```sql
-- タグ名で削除
DELETE FROM tag WHERE tag_name = 'my_tag_2021';
 
-- タグ名と時刻で削除
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');

-- 時刻だけで削除
DELETE FROM tag WHERE tag_time <= TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- タグ名でロールアップを削除
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021';
 
-- タグ名と時刻でロールアップを削除
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- 時刻だけでロールアップを削除
DELETE FROM tag ROLLUP WHERE tag_time BETWEEN TO_DATE('2021-07-01', 'YYYY-MM-DD') AND TO_DATE('2021-07-02', 'YYYY-MM-DD');
```

* DELETE 実行後にストレージから物理的に削除されるまでの時間は、DBMS の状態によって異なります。


## LOAD DATA INFILE {#load-data-infile}

**load_data_infile_stmt:**

![load_data_infile_stmt](/images/sql/dml/load_data_infile_stmt.png)

```sql
load_data_infile_stmt: 'LOAD DATA INFILE' file_name 'INTO TABLE' table_name ( 'TABLESPACE' tbs_name )? ( 'AUTO' ( 'BULKLOAD' | 'HEADUSE' | 'HEADUSE_ESCAPE' ) )? ( ( 'FIELDS' | 'COLUMNS' ) ( 'TERMINATED BY' char )? ( 'ENCLOSED BY' char )? )? ( 'TRIM' ( 'ON' | 'OFF' ) )? ( 'IGNORE' number ( 'LINES' | 'ROWS' ) )? ( 'MAX_LINE_LENGTH' number )? ( 'ENCODED BY' coding_name )? ( 'ON ERROR' ( 'STOP' | 'IGNORE' ) )?
```

サーバーが CSV ファイルを直接読み込みます。オプションに応じてテーブルと列を作成し、データを入力します。
オプションを示します。

| オプション | 説明 |
|--|--|
|AUTO mode_string<br>mode_string `=` (BULKLOAD \| HEADUSE \| HEADUSE_ESCAPE)|テーブル、列名、列型（自動作成時は VARCHAR）を作成。<br>BULKLOAD：1 行を 1 列として入力。列に分割できないデータ向け。<br>HEADUSE：先頭行の列名と列数を使用。<br>HEADUSE_ESCAPE：予約語との衝突を避けるため、列名の前後に _ を付加。列名の特殊文字も _ に置換。|
|(FIELDS\|COLUMNS) TERMINATED BY '`term_char`'<br>ENCLOSED BY '`enclose_char`'|フィールド区切りと囲み文字を指定。通常の CSV では区切りは `,`、囲みは `"`。|
|ENCODED BY coding_name<br>{ UTF8 \| MS949 \| KSC5601 \| EUCJP \| SHIFTJIS \| BIG5 \| GB231280 }|文字コードを指定。既定値は UTF-8。|
|TRIM (ON \| OFF)|列の空白を除去するか保持するかを指定。既定は ON。|
|IGNORE number (LINES \| ROWS)|指定行数を読み飛ばす。CSV や VCF のヘッダー除外などに使用。|
|MAX_LINE_LENGTH|1 行の最大長。既定値 512K。必要に応じて増やせる。|
|ON ERROR (STOP \| IGNORE)|入力エラー時の動作。STOP は停止、IGNORE は該当行を飛ばして続行。既定は IGNORE。|

```sql
-- 既定の区切りカンマと囲み文字の二重引用符を使用
LOAD DATA INFILE '/tmp/aaa.csv' INTO TABLE Sample_data ;
 
-- 1 列の NEWTABLE を作成し、1 行を 1 列として入力
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO BULKLOAD;
 
-- CSV の先頭行を列情報にして NEWTABLE を作成、入力
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO HEADUSE;
  
-- 先頭行を除外し、区切りにセミコロン、囲みに単一引用符を指定
LOAD DATA INFILE '/tmp/ccc.csv' INTO TABLE Sample_data FIELDS TERMINATED BY ';' ENCLOSED BY '\'' IGNORE 1 LINES ON ERROR IGNORE;
```

* AUTO を使わない場合、テーブルの全列を VARCHAR または TEXT にしてください。
