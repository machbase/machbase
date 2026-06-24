---
title : Creating and Managing Lookup Index
type: docs
weight: 50
---

Lookup tables use a single memory index on the primary key. Design lookup queries,
updates, and deletes around the primary-key predicate. `KEYWORD` indexes are only
available for LOG tables; use RDB tables when a persistent row table needs multiple
secondary indexes or JSON path indexes.

```sql
CREATE LOOKUP TABLE lookup_table (code INTEGER PRIMARY KEY, name VARCHAR(20));

SELECT name FROM lookup_table WHERE code = 100;
UPDATE lookup_table SET name = 'sensor-a' WHERE code = 100;
```
