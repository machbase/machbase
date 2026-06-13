---
title : Log 테이블의 인덱스
type: docs
weight: 50
---

Machbase Log 테이블에서는 세 가지 인덱스 타입 키워드를 사용할 수 있습니다.

자세한 내용은 SQL Reference의 DDL 페이지 CREATE INDEX 섹션을 참조하세요.

* LSM Index: 범위 조건과 동등 조건 검색에 사용합니다.
* BITMAP Index: LOG 테이블 컬럼에 생성할 수 있으며 `DESC`에서는 `LSM`으로 표시됩니다.
* KEYWORD Index: 문자열 검색에 사용되며 Varchar 및 Text 컬럼에만 생성할 수 있습니다.


##  인덱스 생성

CREATE INDEX 문을 사용하여 특정 컬럼에 인덱스를 생성합니다.

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type] [tablespace] [index_prop_list]
    index_type ::= INDEX_TYPE { LSM | BITMAP | KEYWORD }
    tablespace ::= TABLESPACE tablespace_name
    index_prop_list ::= value_pair, value_pair, ...
    value_pair ::= property_name = property_value
```

```sql
Mach> CREATE INDEX id_index ON log_data(id) INDEX_TYPE LSM MAX_LEVEL=3;
Created successfully.
```


##  인덱스 속성

인덱스 속성은 인덱스를 생성할 때 지정합니다.

```sql
CREATE BITMAP INDEX value_bitmap_idx ON log_data(value) KEY_COMPRESS=1;
```

```sql
Mach> CREATE BITMAP INDEX value_bitmap_idx ON log_data(value) KEY_COMPRESS=1;
Created successfully.
```


##  인덱스 삭제

DROP INDEX 문을 사용하여 지정된 인덱스를 삭제합니다. 단, 테이블을 검색 중인 다른 세션이 있으면 오류와 함께 실패합니다.

```sql
DROP INDEX index_name;
```

```sql
Mach> DROP INDEX id_index;
Dropped successfully.
```
