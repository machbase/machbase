---
title : '로그 인덱스 생성 및 관리'
type: docs
weight: 50
---

마크베이스의 로그테이블에는 2가지 인덱스 타입을 생성할 수 있다. 

자세한 내용은 SQL 레퍼런스의 DDL 페이지의 CREATE INDEX 문단을 참조하면 된다.

* BITMAP 인덱스 : BITMAP인덱스는 Text, Binary 타입을 제외한 모든 컬럼에 생성할 수 있다.
* KEYWORD 인덱스 : Varchar, Text 컬럼에만 생성 가능하며 문자열을 검색할 때 사용한다.

## 인덱스 생성

CREATE INDEX 구문을 이용하여 특정 컬럼에 대해서 인덱스를 생성한다.

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type] [tablespace] [index_prop_list]
    index_type ::= INDEX_TYPE { BITMAP | KEYWORD }
    tablespace ::= TABLESPACE tablesapce_name
    index_prop_list ::= value_pair, value_pair, ...
    value_pair ::= property_name = property_value
Mach> CREATE INDEX id_index ON log_data(id) INDEX_TYPE BITMAP TABLESPACE tbs_data MAX_LEVEL=3;
Created successfully.
```

## 인덱스 변경

ALTER INDEX 구문을 이용하여 인덱스 속성을 변경한다.

```sql
ALTER INDEX index_name SET KEY_COMPRESS = { 0 | 1 }
Mach> ALTER INDEX id_index SET KEY_COMPRESS = 1;
```

## 인덱스 삭제

DROP INDEX 구문을 이용하여 지정된 인덱스를 삭제한다. 단, 해당 테이블을 검색 중인 다른 세션이 존재할 경우에는 에러를 내면서 실패한다.

```sql
DROP INDEX index_name;
Mach> DROP INDEX id_index;
Dropped successfully.
```
