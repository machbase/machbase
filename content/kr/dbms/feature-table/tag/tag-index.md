---
type: docs
title : '태그 테이블 인덱스 생성 및 관리'
weight: 60
---

마크베이스의 태그테이블에는 추가 칼럼에 대한 TAG 인덱스 타입을 생성할 수 있다.

자세한 내용은 SQL 레퍼런스의 DDL 페이지의 CREATE INDEX 문단을 참조하면 된다.

TAG 인덱스: 기본칼럼(time, name)등을 제외한 추가 칼럼에 대한 인덱스

## 인덱스 생성

CREATE INDEX 구문을 이용하여 특정 컬럼에 대해서 인덱스를 생성한다.

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type]
    index_type ::= INDEX_TYPE { TAG }
```

```sql
Mach> CREATE INDEX id_index ON tag (id) INDEX_TYPE TAG;
Created successfully.
```

7.5 버전부터 tag table에 한해 json 타입의 칼럼에 대해서 json path 별로 인덱스를 생성할 수 있다.

기존의 인덱스 생성 구문에 json path를 operator와 연결하면 된다.

json operator의 return 타입이 varchar이므로, varchar 비교 시 인덱스를 사용할 수 있다.

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, jval JSON);
Executed successfully.
 
Mach> CREATE INDEX idx_jval_value1 ON tag (jval->'$.value1');
Created successfully.
 
Mach> CREATE INDEX idx_jval_value2 ON tag (jval->'$.value2');
Created successfully.
 
Mach> EXPLAIN SELECT * FROM tag WHERE jval->'$.value1' = '10';
PLAN                                                                             
------------------------------------------------------------------------------------
 PROJECT                                                                         
  TAG READ (RAW)                                                                 
   KEYVALUE INDEX SCAN (_TAG_DATA_0)                                             
    [KEY RANGE]                                                                  
     * jval->'$.value1' = '10'                                                   
   VOLATILE FULL SCAN (_TAG_META)                                                
[6] row(s) selected.
```

## 인덱스 삭제

DROP INDEX 구문을 이용하여 지정된 인덱스를 삭제한다. 단, 해당 테이블을 검색 중인 다른 세션이 존재할 경우에는 에러를 내면서 실패한다.

```sql
DROP INDEX index_name;
```

```sql
Mach> DROP INDEX id_index;
Dropped successfully.
```
