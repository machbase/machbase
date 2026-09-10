---
title : Lookup インデックスの作成と管理
type: docs
weight: 50
toc: true
---

Lookup テーブルは RED-BLACK インデックスをサポートします。Lookup テーブルで
`INDEX_TYPE LSM` を指定すると、RED-BLACK インデックスが作成されます。
`KEYWORD` インデックスは LOG テーブルでのみ使用できます。

```sql
CREATE LOOKUP TABLE lookup_table (code INTEGER PRIMARY KEY, name VARCHAR(20));
CREATE INDEX idx_lookup_name ON lookup_table(name) INDEX_TYPE REDBLACK;
```
