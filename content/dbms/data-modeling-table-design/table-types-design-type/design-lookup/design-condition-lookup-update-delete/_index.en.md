---
type: docs
title: 'UPDATE and DELETE Predicate Design'
weight: 80
---

LOOKUP tables support both primary-key and general-predicate `UPDATE`/`DELETE`.

## UPDATE

```sql
UPDATE equipment_master
SET location = 'Line-3',
    status = 'ACTIVE',
    score = score + 10,
    updated_at = NOW
WHERE site = 'SEOUL'
  AND status = 'READY';
```

JSON column predicates and updates can be used together.

```sql
UPDATE equipment_master
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

## DELETE

```sql
DELETE FROM equipment_master
WHERE status = 'RETIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

## Design Rules

1. **Use primary keys for single-row changes**: this is the clearest and fastest path.
2. **Check the target range for bulk changes**: a general predicate applies to every matching row.
3. **Extract frequently searched values**: dedicated JSON path indexes are not supported.
4. **Do not update the primary key**: primary key columns cannot be targets in the `SET` clause.

```sql
SELECT COUNT(*)
FROM equipment_master
WHERE status = 'RETIRED';
```
