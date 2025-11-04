---
title : 텍스트 검색
type: docs
weight: 30
---

이 문서는 키워드 인덱스를 사용한 텍스트 검색을 다룹니다.

텍스트 검색은 원하는 문자열 패턴을 검색하기 위해 "역인덱스"라고 하는 특별한 종류의 인덱스를 검색하기 때문에 비교 가능한 DBMS의 LIKE 검색보다 빠릅니다. 키워드 인덱스는 가변 길이 문자 컬럼인 varchar 및 text 타입 컬럼에만 생성할 수 있습니다. 그러나 검색 대상 문자열은 정확히 일치해야 합니다. Machbase는 특수 문자나 형태소 분석 기반의 키워드를 수행하지 않습니다.

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


## 다국어 검색

Machbase는 ASCII 및 UTF-8로 저장된 다양한 종류의 언어의 가변 길이 문자열을 검색할 수 있습니다. 한국어나 일본어와 같은 언어에서 문장의 일부만 검색하기 위해 2-gram 기법을 사용합니다.

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

입력 데이터가 "대한민국"일 때, "대한," "한민," "민국" 세 단어가 인덱스에 기록됩니다. 따라서 "대한" 또는 "민국" 키워드로 "대한민국"을 검색할 수 있습니다.

기본적으로 검색 문에 입력된 키워드는 AND 조건으로 검색되므로 세 단어만 입력해도 결과가 매우 정확하게 표시됩니다. 예를 들어, 검색 대상 키워드가 "컴퓨터 활용 가이드"인 경우 "컴퓨터", "활용", "가이드" 세 단어가 AND 조건으로 설정됩니다.

## ESEARCH

ESEARCH 연산자는 검색 대상 키워드를 확장하는 데 사용됩니다. 검색 대상 키워드는 ASCII여야 합니다. % 문자를 사용하여 검색 키워드를 설정할 수 있습니다. LIKE 조건과 같이 % 문자로 시작하는 키워드를 사용하면 모든 레코드를 검색하지만, 키워드 인덱스의 단어에 대해 이 조건을 검색하므로 LIKE보다 검색이 빠릅니다. 이 기능은 알파벳 문자열(오류 문 또는 코드 등)을 빠르게 검색하는 데 유용합니다.

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
 
Mach> SELECT * FROM esearch_table where name ESEARCH '%mach';
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


## REGEXP

REGEXP 연산자는 정규 표현식을 통해 데이터에 대한 텍스트 검색을 수행하는 데 사용됩니다. REGEXP 연산자는 대상 컬럼에 대해 정규 표현식을 수행하여 실행되며, 인덱스를 사용할 수 없기 때문에 검색 성능이 저하될 수 있습니다. 따라서 인덱스를 사용할 수 있는 다른 검색 조건을 AND 연산자로 추가하여 검색 속도를 향상시키는 것이 좋습니다.

특정 정규 표현식 패턴을 검색하기 전에 인덱스를 사용할 수 있는 SEARCH 또는 ESEARCH 연산자를 적용하는 것은 먼저 결과 집합을 줄인 다음 REGEXP를 사용하여 검색 성능을 향상시키는 좋은 방법입니다.

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

Machbase는 SQL 표준 LIKE 연산자도 지원합니다. LIKE 연산자는 한국어, 일본어 및 중국어에서 사용할 수 있습니다.

```sql
SELECT  column_name(s)
FROM    table_name
WHERE   column_name
LIKE    pattern;
```

예제:

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
