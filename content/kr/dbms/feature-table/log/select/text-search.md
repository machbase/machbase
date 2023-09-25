---
title : '텍스트 검색'
type: docs
weight: 30
---

이 문서는 키워드 인덱스를 이용한 텍스트 검색을 다룬다.

텍스트 검색은 "reverse index"라는 특수한 종류의 인덱스를 탐색하여 원하는 문자열 패턴을 검색하기 때문에, 일반적인 DBMS의 LIKE검색과 비교할 수 없을 정도로 빠른 성능을 낸다.

키워드 인덱스는 가변길이 문자형 칼럼인 varchar 타입과 text 타입 칼럼에 대해서만 생성할 수 있다. 단, 검색 대상 문자열이 반드시 정확히 일치해야 한다.

마크베이스는 특수문자를 기반한 키워드나, 형태소 분석등을 수행하지는 않는다.


## SEARCH

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
SEARCH  pattern;
```
```sql
Mach> CREATE TABLE search_table (id INTEGER, name VARCHAR(20));
Created successfully.
 
Mach> CREATE INDEX idx_SEARCH ON SEARCH_table (name) INDEX_TYPE KEYWORD;
Created successfully.
 
Mach> INSERT INTO search_table VALUES(1, 'time flys');
1 row(s) inserted.
 
Mach> INSERT INTO search_table VALUES(1, 'time runs');
1 row(s) inserted.
 
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

## 다중 언어 검색

마크베이스는 ASCII와 UTF-8로 저장된 여러 가지 종류의 언어의 가변길이 문자열에 대한 검색이 가능하다. 한국어나 일본어와 같은 언어의 문장에서 일부분만을 검색하기 위해서, 2-gram 기법을 이용한다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
SEARCH  pattern;
```
```sql
Mach> CREATE TABLE multi_table (message varchar(100));
Created successfully.
 
Mach> CREATE INDEX idx_multi ON multi_table(message)INDEX_TYPE KEYWORD;
Created successfully.
 
Mach> INSERT INTO multi_table VALUES("Machbase is the combination of ideal solutions");
1 row(s) inserted.
 
Mach> INSERT INTO multi_table VALUES("Machbase is a columnar DBMS");
1 row(s) inserted.
 
Mach> INSERT INTO multi_table VALUES("Machbaseは理想的なソリューションの組み合わせです");
1 row(s) inserted.
 
Mach> INSERT INTO multi_table VALUES("Machbaseは円柱状のDBMSです");
1 row(s) inserted.
 
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

입력된 데이터가 "대한민국" 인 경우,  "대한", "한민", "민국"의 세 단어가 인덱스에 기록된다.  그러므로 "대한" 또는 "민국" 키워드로도 "대한민국"을 검색할 수 있다.

기본적으로 search문에서 입력받은 키워드들은 AND조건으로 검색되므로, 세 단어만 입력하더라도 결과는 매우 정확하게 표시된다. 예를 들어, 검색 대상 키워드가 "computer utilization guide"인 경우, 세 단어 "computer", "utilization", "guide"가 AND 조건으로 설정되므로 세 단어가 한 데이터에서 모두 사용된 칼럼값만 표시된다.

## ESEARCH

ESEARCH 연산자는 검색 대상 키워드를 확장하여 검색하기 위해 사용된다. 검색 대상 키워드는 반드시 ASCII여야 한다. 검색 키워드를 %문자를 이용하여 설정할 수 있다.

LIKE조건절처럼 %문자로 시작되는 키워드를 이용하면, 모든 레코드를 검색해야 하지만 키워드 색인 내의 단어들에 대해서 이 조건을 검색하기 때문에, LIKE보다 빠르게 검색할 수 있다. 

이 기능은 알파벳 문자열(에러 문장 또는 코드등)을 빠르게 검색할 경우에 유용하다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
ESEARCH pattern;
```
```sql
Mach> CREATE TABLE esearch_table(id INTEGER, name VARCHAR(20), data VARCHAR(40));
Created successfully.
 
Mach> CREATE INDEX idx1 ON esearch_table(name) INDEX_TYPE KEYWORD;
Created successfully.
 
Mach> CREATE INDEX idx2 ON esearch_table(data) INDEX_TYPE KEYWORD;
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
 
Mach> SELECT * FROM esearch_table WHERE name ESEARCH '%mach%';
ID          NAME                  DATA                                     
--------------------------------------------------------------------------------
2           mach2flux             Real-time data compression               
1           machbase              Real-time search technology      
 
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

## REGEXP

REGEXP 연산자는 정규표현식을 통하여 데이터에 대한 텍스트 검색을 수행하기 위해서 사용된다. REGEXP 연산자는 대상 칼럼에 정규표현식을 수행하여 실행되며, 색인을 사용할 수 없기 때문에, 검색 성능이 저하될 수 있다. 

따라서 검색 속도를 향상시키기 위해 색인을 사용할 수 있는 다른 검색 조건을 AND 연산자로 추가하여 사용하는 것이 좋다.

특정한 정규표현식 패턴으로 검색하기 전에 인덱스를 사용할 수 있는 SEARCH 또는 ESEARCH 연산자를 먼저 적용하고, 결과집합을 축소시킨 다음 REGEXP를 사용하는 것이 검색 성능을 향상시킬 수 있는 방법이다.

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

## LIKE

마크베이스는 SQL표준의 LIKE연산자도 지원한다. 

LIKE연산자에 한국어, 일본어, 중국어도 사용 가능하다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
LIKE    pattern;
```

Example:
```sql
Mach> CREATE TABLE like_table (id INTEGER, name VARCHAR(20), data VARCHAR(40));
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
