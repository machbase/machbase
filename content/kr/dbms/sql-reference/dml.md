---
title : 'DML'
type: docs
weight: 30
---

## INSERT

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

특정 테이블에 값을 입력하는 구문입니다. 한 가지 특이한 점은 Column_List에서 지정되지 않은 컬럼에는 모두 NULL 값으로 채워진다는 것입니다. 이는 입력의 편의성과 저장 공간의 효율화를 위해 채택된 로그 파일의 특성을 고려한 정책입니다.

METADATA는 tag table에만 사용할 수 있습니다.

### INSERT ON DUPLICATE KEY UPDATE

마크베이스는 흔히 알려진 UPSERT 기능과 유사한 구문을 지원합니다.

기본 키가 지정된 Lookup/Volatile 테이블에 값을 입력할 때 사용할 수 있는 특수 구문으로, 기본 키 값이 중복되는 데이터가 이미 테이블에 존재하는 경우에는 기존 데이터의 값이 변경됩니다.
물론 키 값이 중복되는 데이터가 존재하지 않는 경우에는 새로운 데이터로 삽입됩니다.

이 구문을 사용하기 위해서 휘발성 테이블에 기본 키가 지정되어 있어야 합니다.

삽입되는 데이터의 컬럼 값과 갱신되는 데이터의 컬럼 값을 다르게 하고자 하는 경우, 또는 삽입되는 데이터의 컬럼 값이 아닌 다른 컬럼 값을 갱신하고자 하는 경우에는 SET 절을 추가로 입력할 수 있습니다.

* SET 절은 '컬럼=값'으로 구성되며, 각각을 콤마로 구분해야 합니다.
* SET 절에서 기본 키 값을 변경해서는 안 됩니다.

## INSERT SELECT

**insert_select_stmt:**

![insert_select_stmt](/images/sql/dml/insert_select_stmt.png)

```sql
insert_select_stmt ::= 'INSERT INTO' table_name ( '(' insert_column_list ')' )? select_stmt
```

특정 table에 대해서 SELECT 문의 수행 결과를 삽입하는 문장입니다. 기본적으로는 다른 DBMS와 유사하지만 다음의 차이점이 있습니다.

1. _ARRIVAL_TIME 컬럼 값은 select 및 INSERT 컬럼 리스트에서 지정되지 않으면 INSERT SELECT 문이 수행되는 시점의 시간 값으로 입력됩니다.
2. VARCHAR 타입의 컬럼에 대해서 삽입되는 입력값이 컬럼의 최대 길이보다 큰 경우, 오류를 발생시키지 않고 해당 컬럼의 최대 길이만큼 잘라서 입력됩니다.
3. 형 변환이 가능한 경우(숫자형->숫자형)에는 입력되는 컬럼 값에 맞게 삽입됩니다.
4. 수행 도중 오류가 발생한 경우 ROLLBACK되지 않습니다.
5. _ARRIVAL_TIME 컬럼의 값을 지정하여 삽입하는 경우, 새로 입력되는 값이 기존의 값보다 이전 시간을 갖고 있으면 입력되지 않습니다.

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

## UPDATE

* 5.5 부터 제공되는 기능입니다.

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

INSERT ON DUPLICATE KEY UPDATE를 통한 UPSERT가 아닌 UPDATE 구문도 제공합니다.

역시 기본 키(Primary Key)가 지정된 Lookup/Volatile 테이블에 값을 입력할 때 사용할 수 있습니다. WHERE 절에는 기본 키의 일치 조건식을 작성해야 합니다.

### UPDATE METADATA

TAGDATA 테이블에 한해서 메타데이터를 업데이트하고자 할 때 사용합니다.

```sql
UPDATE TAG METADATA SET ...
```
 
* TAGDATA 테이블의 메타데이터는 INSERT ON DUPLICATE KEY UPDATE를 통해 입력하거나 수정할 수 없습니다.

## DELETE

**delete_stmt:**

![delete_stmt](/images/sql/dml/delete_stmt.png)

**time_unit:**

![time_unit](/images/sql/dml/time_unit.png)

```sql
delete_stmt ::= 'DELETE FROM' table_name ( 'OLDEST' number 'ROWS' | 'EXCEPT' number ( 'ROWS' | time_unit ) | 'BEFORE' datetime_expression )? 'NO WAIT'?
time_unit ::= 'DURATION' number time_unit ( ( 'BEFORE' | 'AFTER' ) number time_unit )?
```

마크베이스에서의 DELETE BEFORE 구문은 로그 테이블, Tag 테이블, Rollup table에 대해서 수행 가능합니다. 중간의 임의 위치에 있는 데이터를 삭제할 수 없으며, 임의의 위치부터 연속적으로 마지막(가장 오래된 로그) 레코드까지 지울 수 있도록 구현되었습니다.

이는 로그 데이터의 특성을 살린 정책으로서 한 번 입력되면 수정이 없고, 공간 확보를 위해 파일을 삭제하는 행위를 DB 형식으로 표현한 것입니다.

DURATION, OLDEST, EXCEPT 구문은 TAG 및 Rollup 테이블에 대해서는 사용할 수 없습니다.

```sql
-- 모두 삭제합니다.
DELETE FROM devices;
 
-- 가장 오래된 마지막 N건을 삭제합니다.
DELETE FROM devices OLDEST N ROWS;
 
-- 최근 N건을 제외하고 모두 삭제합니다.
DELETE FROM devices EXCEPT N ROWS;
 
-- 지금부터 N일치를 남기고 모두 삭제합니다.
DELETE FROM devices EXCEPT N DAY;
 
-- 2014년 6월 1일 이전의 데이터를 모두 삭제합니다.
DELETE FROM devices BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
 
-- tag 데이터의 시간을 기준으로 삭제합니다.
DELETE FROM tag BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
 
-- tag rollup 데이터를 시간 기준으로 삭제합니다.
DELETE FROM tag ROLLUP BEFORE TO_DATE('2014-06-01', 'YYYY-MM-DD');
```

## DELETE WHERE

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

휘발성 테이블에 대해서만 수행 가능한 구문으로, WHERE 절에 작성된 조건에 일치하는 레코드만 삭제할 수 있습니다.

* 기본 키가 지정된 휘발성 테이블에 대해서만 수행 가능합니다.
* WHERE 절에는 (기본 키 컬럼) = (값) 조건만 허용되며, 다른 조건과 함께 작성할 수 없습니다.
* 기본 키 컬럼이 아닌 다른 컬럼을 조건에 사용할 수 없습니다.

**delete_from_tag_where_stmt:**

![delete_from_tag_where_stmt](/images/sql/dml/delete_from_tag_where_stmt.png)

```sql
delete_from_tag_where_stmt ::= 'DELETE FROM' table_name 'ROLLUP'? 'WHERE' tag_name '=' value ( and tag_time '<' datetime_expression  )?
```

Tag 테이블 및 Rollup 테이블은 아래와 같이 두 가지 방식의 삭제 구문이 지원됩니다.

* Tag name 기준 삭제가 가능합니다.
* Tag name과 Tag time 기준 삭제가 가능합니다.

```sql
-- tag name 기준으로 삭제하는 예시입니다.
DELETE FROM tag WHERE tag_name = 'my_tag_2021'
 
-- tag name과 tag time 기준으로 삭제하는 예시입니다.
DELETE FROM tag WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');

-- tag name 기준으로 rollup을 삭제하는 예시입니다.
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021'
 
-- tag name과 tag time 기준으로 rollup을 삭제하는 예시입니다.
DELETE FROM tag ROLLUP WHERE tag_name = 'my_tag_2021' AND tag_time < TO_DATE('2021-07-01', 'YYYY-MM-DD');
```

* 삭제 쿼리가 실행된 후에 삭제된 row가 저장 공간에서 물리적으로 삭제되기까지 걸리는 시간은 DBMS의 동작 상황에 따라서 다를 수 있습니다.

## LOAD DATA INFILE

**load_data_infile_stmt:**

![load_data_infile_stmt](/images/sql/dml/load_data_infile_stmt.png)

```sql
load_data_infile_stmt: 'LOAD DATA INFILE' file_name 'INTO TABLE' table_name ( 'TABLESPACE' tbs_name )? ( 'AUTO' ( 'BULKLOAD' | 'HEADUSE' | 'HEADUSE_ESCAPE' ) )? ( ( 'FIELDS' | 'COLUMNS' ) ( 'TERMINATED BY' char )? ( 'ENCLOSED BY' char )? )? ( 'TRIM' ( 'ON' | 'OFF' ) )? ( 'IGNORE' number ( 'LINES' | 'ROWS' ) )? ( 'MAX_LINE_LENGTH' number )? ( 'ENCODED BY' coding_name )? ( 'ON ERROR' ( 'STOP' | 'IGNORE' ) )?
```

CSV 포맷의 데이터 파일을 서버에서 직접 읽어서, 옵션에 따라 서버에서 직접 테이블 및 컬럼들을 생성하여 이를 입력하는 기능입니다.

각 옵션에 대해서 설명하면 다음과 같습니다.

|옵션|설명|
|--|--|
|AUTO mode_string<br><br>mode_string =<br><br>(BULKLOAD \| HEADUSE \| HEADUSE_ESCAPE)|해당 테이블을 생성하고 컬럼 타입(자동 생성 시 VARCHAR 타입) 및 컬럼명을 자동으로 생성합니다.<br>__BULKLOAD__: 데이터 한 개의 row를 하나의 컬럼으로 입력합니다. 컬럼으로 구분할 수 없는 데이터에 대해서 사용합니다.<br>__HEADUSE__: 데이터 파일의 첫 번째 라인에 기술되어 있는 컬럼명을 테이블의 컬럼명으로 사용하고, 그 라인에 기술된 수만큼의 컬럼을 생성합니다.<br>__HEADUSE_ESCAPE__: HEADUSE 옵션과 유사하지만, 컬럼명이 DB의 예약어와 같을 경우 발생할 수 있는 오류를 회피하기 위해 컬럼명의 앞뒤로 '_' 문자를 덧붙이고, 컬럼명에 특수문자가 존재하면 그 문자를 '_' 문자로 변경합니다.|
<br>(FIELDS\|COLUMNS) TERMINATED BY 'term_char'<br><br>ESCAPED BY 'escape_char'|데이터 라인을 파싱하기 위한 구분 문자(term_char)와 이스케이프 문자(escape_char)를 지정합니다. 일반적인 CSV 파일의 경우 구분 문자는 ,이며 이스케이프 문자는 '입니다.|
|ENCODED BY coding_name<br>coding_name =<br>{ UTF8(default) \| MS949 \| KSC5601 \| EUCJP \| SHIFTJIS \| BIG5 \| GB231280 }|데이터 파일의 인코딩 옵션을 지정합니다. 기본값은 UTF-8입니다.|
|TRIM (ON \| OFF)|컬럼의 빈 공간을 제거하거나 유지합니다. 기본값은 ON입니다.|
|IGNORE number (LINES \| ROWS)|숫자로 지정된 라인 또는 행만큼의 데이터를 무시합니다. CSV 포맷 파일의 헤더 등을 무시하거나 VCF 헤더를 무시하기 위해 사용합니다.|한 라인의 최대 길이를 지정합니다. 기본값은 512K이며, 데이터가 더 큰 경우에는 더 큰 값을 지정할 수 있습니다.|
|ON ERROR (STOP \| IGNORE)|입력 도중 에러가 발생할 경우 수행할 동작을 지정합니다. STOP인 경우 입력을 중단하고 IGNORE인 경우 에러가 발생한 라인을 건너뛰고 계속 입력합니다.<br>기본값은 IGNORE입니다.|

```sql
-- default field delimiter(,)와 field encloser(\")를 사용하여 데이터를 입력합니다.
LOAD DATA INFILE '/tmp/aaa.csv' INTO TABLE Sample_data ;
 
-- 하나의 컬럼을 갖는 NEWTABLE을 생성해서 한 라인을 한 컬럼으로 입력합니다.
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO BULKLOAD;
 
-- CSV의 첫 번째 라인을 컬럼 정보로 이용하여 NEWTABLE을 생성하고 해당 테이블에 입력합니다.
LOAD DATA INFILE '/tmp/bbb.csv' INTO TABLE NEWTABLE AUTO HEADUSE;
  
-- 첫 번째 라인은 무시하고 필드 구분자는 ;, enclosing 문자는 '로 지정해서 입력합니다.
LOAD DATA INFILE '/tmp/ccc.csv' INTO TABLE Sample_data FIELDS TERMINATED BY ';' ENCLOSED BY '\''  IGNORE 1 LINES ON ERROR IGNORE;
```

* AUTO 옵션을 사용하지 않는 경우 테이블의 모든 컬럼은 VARCHAR 또는 TEXT 타입으로 생성해야 합니다.
