---
type: docs
title: '9.15.2 LOOKUP Predicate DML Performance Considerations'
weight: 50
---

LOOKUP `UPDATE`/`DELETE` with a primary-key condition uses the primary-key hash
path. General-predicate `UPDATE`/`DELETE` first identifies matching rows and
then applies the change, so wide predicates can cost more than single-row
primary-key operations.

## Recommended Patterns

### 1. Use the primary key for single-row changes

```sql
UPDATE device_meta
SET status = 'ACTIVE'
WHERE device_id = 'DEV-001';

DELETE FROM device_meta
WHERE device_id = 'DEV-001';
```

### 2. Check the target range before bulk changes

```sql
SELECT COUNT(*)
FROM device_meta
WHERE location = 'Building-A'
  AND status = 'INACTIVE';

UPDATE device_meta
SET status = 'RETIRED'
WHERE location = 'Building-A'
  AND status = 'INACTIVE';
```

### 3. Use typed functions for JSON predicates

```sql
UPDATE device_meta
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

For numeric comparisons, prefer typed functions such as `JSON_EXTRACT_INTEGER`
and `JSON_EXTRACT_DOUBLE` instead of `->`.

## Summary

| DML type | Behavior | Recommended use |
|----------|----------|-----------------|
| Primary-key UPDATE/DELETE | Primary-key hash path | Single-row or clearly identified rows |
| Non-PK predicate UPDATE/DELETE | Finds matching rows and applies the change | Small or medium batch changes; count first |
| JSON path predicate DML | Includes JSON path evaluation cost | Extract frequently searched values into regular columns |

Keep LOOKUP tables small and scoped to reference-data use cases.
