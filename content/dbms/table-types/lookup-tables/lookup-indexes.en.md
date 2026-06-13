---
title : Creating and Managing Lookup Index
type: docs
weight: 50
---

Lookup tables support RED-BLACK indexes. If `INDEX_TYPE LSM` is specified on a
Lookup table, Machbase creates a RED-BLACK index. `KEYWORD` indexes are only
available for LOG tables.

```sql
CREATE LOOKUP TABLE lookup_table (code INTEGER PRIMARY KEY, name VARCHAR(20));
CREATE INDEX idx_lookup_name ON lookup_table(name) INDEX_TYPE REDBLACK;
```
