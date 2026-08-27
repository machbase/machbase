---
type: docs
title: '13.8 Schema Change Checklist'
weight: 80
toc: true
---

## Index change checklist

- Confirm the query and ingestion impact before creating or dropping an index.
- Account for the initial build time on existing rows.
- When using `IF NOT EXISTS`, verify the definition of any index with the same name.

```sql
CREATE INDEX IF NOT EXISTS idx_new ON sensor_log (sensor_id);
SHOW INDEX idx_new;
```

`IF NOT EXISTS` checks the index name only. See
[INDEX syntax](/dbms/reference/sql/syntax-dictionary-sql/index-syntax/#create-index-if-not-exists)
and verify the effective table, columns, type, and properties after deployment.
