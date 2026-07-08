---
type: docs
title: 'Large LOOKUP Predicate UPDATE/DELETE Range'
weight: 30
---

LOOKUP predicate `UPDATE` and `DELETE` are supported. Because the statement
applies to every matching row, check the target range before changing
production data.

## Symptoms

- The statement succeeds, but more rows than expected are updated or deleted.
- A wide range predicate or JSON path predicate matches many rows.

## Diagnosis

Run the same predicate with `SELECT COUNT(*)` first.

```sql
SELECT COUNT(*)
FROM equipment
WHERE location = 'Building-A'
  AND status = 'inactive';
```

If needed, inspect the target keys.

```sql
SELECT eq_id, location, status
FROM equipment
WHERE location = 'Building-A'
  AND status = 'inactive';
```

## Resolution

- Use the primary key for single-row changes.
- Narrow bulk predicates and verify row counts before and after the DML.
- Use typed JSON functions for numeric JSON predicates.

```sql
UPDATE equipment
SET status = 'retired'
WHERE location = 'Building-A'
  AND status = 'inactive'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
```
