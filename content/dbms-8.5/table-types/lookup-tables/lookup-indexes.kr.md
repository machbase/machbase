---
title : Lookup 인덱스 생성 및 관리
type: docs
weight: 50
---

Lookup 테이블은 RED-BLACK 인덱스를 지원합니다. Lookup 테이블에
`INDEX_TYPE LSM`을 지정해도 Machbase는 RED-BLACK 인덱스를 생성합니다.
`KEYWORD` 인덱스는 LOG 테이블에서만 사용할 수 있습니다.

```sql
CREATE LOOKUP TABLE lookup_table (code INTEGER PRIMARY KEY, name VARCHAR(20));
CREATE INDEX idx_lookup_name ON lookup_table(name) INDEX_TYPE REDBLACK;
```
