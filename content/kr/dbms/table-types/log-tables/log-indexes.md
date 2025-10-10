---
title : Log 테이블의 인덱스
type: docs
weight: 50
---

Machbase Log 테이블에서는 두 가지 인덱스 타입을 생성할 수 있습니다.

자세한 내용은 SQL Reference의 DDL 페이지 CREATE INDEX 섹션을 참조하세요.

* BITMAP Index: Text, Binary 타입을 제외한 모든 컬럼에 생성할 수 있습니다.
* KEYWORD Index: Varchar 및 Text 컬럼에만 생성할 수 있으며 문자열 검색에 사용됩니다.


##  인덱스 생성

CREATE INDEX 문을 사용하여 특정 컬럼에 인덱스를 생성합니다.

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type] [tablespace] [index_prop_list]
    index_type ::= INDEX_TYPE { LSM | KEYWORD }
    tablespace ::= TABLESPACE tablesapce_name
    index_prop_list ::= value_pair, value_pair, ...
    value_pair ::= property_name = property_value
```

```sql
Mach> CREATE INDEX id_index ON log_data(id) INDEX_TYPE LSM TABLESPACE tbs_data MAX_LEVEL=3;
Created successfully.
```


##  인덱스 변경

ALTER INDEX 문을 사용하여 인덱스 속성을 변경합니다.

```sql
ALTER INDEX index_name SET KEY_COMPRESS = { 0 | 1 }
```

```sql
Mach> ALTER INDEX id_index SET KEY_COMPRESS = 1;
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
