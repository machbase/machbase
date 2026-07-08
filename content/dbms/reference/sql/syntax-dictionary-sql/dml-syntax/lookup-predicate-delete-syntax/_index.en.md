---
type: docs
title: 'LOOKUP predicate DELETE syntax'
weight: 40
---

LOOKUP `DELETE` supports general predicates in the `WHERE` clause, not only
primary-key equality. Every matching row is deleted.

## Syntax

```sql
DELETE FROM table_name
 WHERE predicate;
```

Without a `WHERE` clause, the statement deletes all rows in the LOOKUP table.

## Predicate Examples

```sql
DELETE FROM device_lookup
WHERE status = 'EXPIRED';

DELETE FROM device_lookup
WHERE updated_at < TO_DATE('2026-01-01 00:00:00')
   OR score < 10;

DELETE FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
```

## Supported Predicates

| Predicate | Support |
|-----------|:-------:|
| `pk_col = value` | O |
| `non_pk_col = value` | O |
| `<`, `<=`, `>`, `>=`, `<>` | O |
| `BETWEEN` | O |
| `IN`, `NOT IN` | O |
| `LIKE`, `NOT LIKE` | O |
| `AND`, `OR`, `NOT` | O |
| `IS NULL`, `IS NOT NULL` | O |
| `TO_DATE(...)` date predicates | O |
| JSON `->`, `JSON_EXTRACT_*`, `JSON_IS_VALID` | O |
| Delete all rows without `WHERE` | O |

## Operational Note

Predicate `DELETE` removes every row that matches the predicate. On production
data, check the target range first.

```sql
SELECT COUNT(*)
FROM device_lookup
WHERE status = 'EXPIRED';

DELETE FROM device_lookup
WHERE status = 'EXPIRED';
```

## Related Documents

- [LOOKUP predicate UPDATE syntax](../lookup-predicate-update-syntax/)
- [LOOKUP SQL/JSON Support](../../../../support-scope-constraints/lookup-sql-json/)
