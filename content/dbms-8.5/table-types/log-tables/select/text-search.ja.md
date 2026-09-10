---
title : テキスト検索
type: docs
weight: 30
toc: true
---

キーワードインデックスを使用するテキスト検索を説明します。

転置インデックスから文字列パターンを検索するため、一般的な DBMS の LIKE 検索より高速です。キーワードインデックスは、可変長文字列の VARCHAR 列と TEXT 列にのみ作成できます。ただし、検索文字列は完全に一致する必要があります。特殊文字に基づくキーワード処理や形態素解析は行いません。

## SEARCH {#search}

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
SEARCH  pattern;
```

```sql
Mach> CREATE TABLE search_table (id INTEGER, name VARCHAR(20));
Created successfully.

Mach> INSERT INTO search_table VALUES(1, 'time flys');
1 row(s) inserted.
 
Mach> INSERT INTO search_table VALUES(1, 'time runs');
1 row(s) inserted.

Mach> CREATE INDEX idx_SEARCH ON search_table (name) INDEX_TYPE KEYWORD;
Created successfully.
 
Mach> SELECT * FROM search_table WHERE name SEARCH 'time' OR name SEARCH 'runs2' ;
ID          NAME
-------------------------------------
1           time runs
1           time flys
[2] row(s) selected.
 
Mach> SELECT * FROM search_table WHERE name SEARCH 'time' AND name SEARCH 'runs2' ;
ID          NAME
-------------------------------------
[0] row(s) selected.
 
Mach> SELECT * FROM search_table WHERE name SEARCH 'flys' OR name SEARCH 'runs2' ;
ID          NAME
-------------------------------------
1           time flys
[1] row(s) selected.
```


## 多言語検索 {#multilingual-search}

Machbase は ASCII と UTF-8 の多言語文字列を検索できます。韓国語や日本語の文の一部を検索するには、2-gram 方式を使用します。

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
SEARCH  pattern;
```

```sql
Mach> CREATE TABLE multi_table (message varchar(100));
Created successfully.

Mach> INSERT INTO multi_table VALUES("Machbase is the combination of ideal solutions");
1 row(s) inserted.
 
Mach> INSERT INTO multi_table VALUES("Machbase is a columnar DBMS");
1 row(s) inserted.
 
Mach> INSERT INTO multi_table VALUES("Machbaseは理想的なソリューションの組み合わせです");
1 row(s) inserted.
 
Mach> INSERT INTO multi_table VALUES("Machbaseは円柱状のDBMSです");
1 row(s) inserted.

Mach> CREATE INDEX idx_multi ON multi_table(message) INDEX_TYPE KEYWORD;
Created successfully.
 
Mach>  SELECT * from multi_table WHERE message SEARCH 'Machbase DBMS';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは円柱状のDBMSです
Machbase is a columnar DBMS
[2] row(s) selected.
 
Mach> SELECT * from multi_table WHERE message SEARCH 'DBMS is';
MESSAGE
------------------------------------------------------------------------------------
Machbase is a columnar DBMS
[1] row(s) selected.
 
Mach> SELECT * from multi_table WHERE message SEARCH 'DBMS' OR message SEARCH 'ideal';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは円柱状のDBMSです
Machbase is a columnar DBMS
Machbase is the combination of ideal solutions
[3] row(s) selected.
 
Mach> SELECT * from multi_table WHERE message SEARCH '組み合わせ';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは理想的なソリューションの組み合わせです
[1] row(s) selected.
Elapsed time: 0.001
Mach> SELECT * from multi_table WHERE message SEARCH '円柱';
MESSAGE
------------------------------------------------------------------------------------
Machbaseは円柱状のDBMSです
[1] row(s) selected.
```

例えば入力が「대한민국」の場合、「대한」「한민」「민국」の 3 つの語をインデックスに記録します。「대한」または「민국」で「대한민국」を検索できます。

検索語は基本的に AND 条件で組み合わせます。韓国語の「컴퓨터 활용 가이드」（コンピューター活用ガイド）では、「컴퓨터」「활용」「가이드」の各語を AND 条件で検索します。例えば computer utilization guide を指定すると、computer、utilization、guide の 3 語を AND 条件として検索するため、少数の語でも対象を絞り込めます。

## ESEARCH {#esearch}

ESEARCH は検索キーワードを拡張します。対象のキーワードは ASCII である必要があり、% を使用できます。LIKE と同じく % で始まるパターンは全体を検索しますが、ESEARCH はキーワードインデックス内の語を対象にするため、LIKE より高速です。エラーメッセージやコードなどの英字文字列の検索に適しています。

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
ESEARCH pattern;
```

```sql
Mach> CREATE TABLE esearch_table(id INTEGER, name VARCHAR(100), data VARCHAR(40));
Created successfully.

Mach> INSERT INTO esearch_table VALUES(1, 'machbase', 'Real-time search technology');
1 row(s) inserted.
 
Mach> INSERT INTO esearch_table VALUES(2, 'mach2flux', 'Real-time data compression');
1 row(s) inserted.
 
Mach> INSERT INTO esearch_table VALUES(3, 'DB MS', 'Memory cache technology');
1 row(s) inserted.
 
Mach> INSERT INTO esearch_table VALUES(4, 'ファ ッションアドバイザー、', 'errors');
1 row(s) inserted.
 
Mach> INSERT INTO esearch_table VALUES(5, '인피 니 플럭스', 'socket232');
1 row(s) inserted.

Mach> CREATE INDEX idx1 ON esearch_table(name) INDEX_TYPE KEYWORD;
Created successfully.

Mach> CREATE INDEX idx2 ON esearch_table(data) INDEX_TYPE KEYWORD;
Created successfully.

Mach> SELECT * FROM esearch_table where name ESEARCH '%base';
ID          NAME                  DATA
--------------------------------------------------------------------------------
1           machbase            Real-time search technology
[1] row(s) selected.
Elapsed time: 0.001
Mach> SELECT * FROM esearch_table where data ESEARCH '%echn%';
ID          NAME                  DATA
--------------------------------------------------------------------------------
3           DB MS                 Memory cache technology
1           machbase            Real-time search technology
[2] row(s) selected.
 
Mach> SELECT * FROM esearch_table where name ESEARCH '%피니%럭스';
ID          NAME                  DATA
--------------------------------------------------------------------------------
[0] row(s) selected.
 
Mach> SELECT * FROM esearch_table where data ESEARCH '%232';
ID          NAME                  DATA
--------------------------------------------------------------------------------
5           인피 니 플럭스  socket232
[1] row(s) selected.
```


## REGEXP {#regexp}

REGEXP は正規表現で列のデータを検索します。インデックスを利用できないため、性能が低下する場合があります。インデックスを利用できる他の条件を AND で追加すると、検索を高速化できます。

SEARCH または ESEARCH で候補を絞ってから REGEXP を適用すると、正規表現の処理対象を減らせます。

```sql
Mach> CREATE TABLE regexp_table(id INTEGER, name VARCHAR(20), data VARCHAR(40));
Created successfully.
 
Mach> INSERT INTO regexp_table VALUES(1, 'machbase', 'Real-time search technology');
1 row(s) inserted.
 
Mach> INSERT INTO regexp_table VALUES(2, 'mach2base', 'Real-time data compression');
1 row(s) inserted.
 
Mach> INSERT INTO regexp_table VALUES(3, 'DBMS', 'Memory cache technology');
1 row(s) inserted.
 
Mach> INSERT INTO regexp_table VALUES(4, 'ファ ッショ', 'errors');
1 row(s) inserted.
 
Mach> INSERT INTO regexp_table VALUES(5, '인피니플럭스', 'socket232');
1 row(s) inserted.
 
Mach> SELECT * FROM regexp_table WHERE name REGEXP 'mach';
ID          NAME                  DATA
--------------------------------------------------------------------------------
2           mach2base           Real-time data compression
1           machbase            Real-time search technology
[2] row(s) selected.
 
Mach> SELECT * FROM regexp_table WHERE data REGEXP 'mach[1]';
ID          NAME                  DATA
--------------------------------------------------------------------------------
[0] row(s) selected.
 
Mach> SELECT * FROM regexp_table WHERE data REGEXP '[A-Za-z]';
ID          NAME                  DATA
--------------------------------------------------------------------------------
5           인피니플럭스  socket232
4           ファ ッショ      errors
3           DBMS                  Memory cache technology
2           mach2base           Real-time data compression
1           machbase            Real-time search technology
[5] row(s) selected.
```


## LIKE {#like}

SQL 標準の LIKE もサポートします。韓国語、日本語、中国語でも利用できます。

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
LIKE    pattern;
```

例：

```sql
Mach> CREATE TABLE like_table (id INTEGER, name VARCHAR(100), data VARCHAR(40));
Created successfully.
 
Mach> INSERT INTO like_table VALUES(1, 'machbase', 'Real-time search technology');
1 row(s) inserted.
 
Mach> INSERT INTO like_table VALUES(2, 'mach2base', 'Real-time data compression');
1 row(s) inserted.
 
Mach> INSERT INTO like_table VALUES(3, 'DBMS', 'Memory cache technology');
1 row(s) inserted.
 
Mach> INSERT INTO like_table VALUES(4, 'ファ ッションアドバイザー、', 'errors');
1 row(s) inserted.
 
Mach> INSERT INTO like_table VALUES(5, '인피 니 플럭스', 'socket232');
1 row(s) inserted.
 
Mach> SELECT * FROM like_table WHERE name LIKE 'mach%';
ID          NAME                  DATA
--------------------------------------------------------------------------------
2           mach2base           Real-time data compression
1           machbase            Real-time search technology
[2] row(s) selected.
 
Mach> SELECT * FROM like_table WHERE name LIKE '%니%';
ID          NAME                  DATA
--------------------------------------------------------------------------------
5           인피 니 플럭스  socket232
[1] row(s) selected.
 
Mach> SELECT * FROM like_table WHERE data LIKE '%technology';
ID          NAME                  DATA
--------------------------------------------------------------------------------
3           DBMS                  Memory cache technology
1           machbase            Real-time search technology
[2] row(s) selected.
```
