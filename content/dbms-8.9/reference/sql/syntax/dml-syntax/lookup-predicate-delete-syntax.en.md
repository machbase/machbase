---
type: docs
title: 'LOOKUP predicate DELETE'
weight: 40
toc: true
---

LOOKUP DELETE supports general WHERE predicates as well as primary key equality. Every matching row
is deleted.

## Syntax

```sql
DELETE FROM table_name
 WHERE predicate;
```

Omitting WHERE deletes all rows in the LOOKUP table.

## Supported Predicate Examples

```sql
-- Ordinary column predicate
DELETE FROM device_lookup
WHERE status = 'EXPIRED';

-- Date and range predicates
DELETE FROM device_lookup
WHERE updated_at < TO_DATE('2026-01-01 00:00:00')
   OR score < 10;

-- JSON path predicates
DELETE FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
```

## Supported Predicates

| Predicate | Supported |
|------|:---:|
| `pk_col = value` | Yes |
| `non_pk_col = value` | Yes |
| `<`, `<=`, `>`, `>=`, `<>` | Yes |
| BETWEEN | Yes |
| IN, NOT IN | Yes |
| LIKE, NOT LIKE | Yes |
| AND, OR, NOT | Yes |
| IS NULL, IS NOT NULL | Yes |
| TO_DATE(...) date predicates | Yes |
| JSON ->, JSON_EXTRACT_*, JSON_IS_VALID | Yes |
| Delete all rows without WHERE | Yes |

## Operational Considerations

General-predicate DELETE removes every matching row. For production data, verify the target scope
with the same predicate before execution.

```sql
SELECT COUNT(*)
FROM device_lookup
WHERE status = 'EXPIRED';

DELETE FROM device_lookup
WHERE status = 'EXPIRED';
```

## Related Documentation

- [LOOKUP Predicate UPDATE Syntax](../lookup-predicate-update-syntax/)
- [LOOKUP SQL/JSON Support Matrix](../../../../support-scope-constraints/lookup-sql-json/)
