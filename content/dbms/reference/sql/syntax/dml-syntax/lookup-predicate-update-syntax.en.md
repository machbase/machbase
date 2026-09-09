---
type: docs
title: 'LOOKUP predicate UPDATE'
weight: 30
toc: true
---

LOOKUP UPDATE supports general WHERE predicates as well as primary key equality. Every matching row
is updated.

## Syntax

```sql
UPDATE table_name
   SET column_name = expression [, column_name = expression ...]
 WHERE predicate;
```

## Supported Predicate Examples

```sql
-- Ordinary column predicate
UPDATE device_lookup
SET status = 'ACTIVE'
WHERE site = 'SEOUL' AND status = 'READY';

-- Range and string predicates
UPDATE device_lookup
SET score = score + 10
WHERE score BETWEEN 10 AND 80
  AND note LIKE 'sensor-%';

-- JSON path predicates
UPDATE device_lookup
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

Right-hand SET expressions can reference the current row values.

```sql
UPDATE device_lookup
SET score = score + 1
WHERE group_name IN ('A', 'B');
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

## Constraints

- SET cannot change the primary key column itself.
- Multiple matching rows result in multiple updates.
- Use single quotes for JSON path strings, such as '$.key'. Double quotes denote SQL identifiers.
- For numeric JSON comparison, use typed functions such as JSON_EXTRACT_INTEGER or JSON_EXTRACT_DOUBLE.

## Related Documentation

- [LOOKUP Predicate DELETE Syntax](../lookup-predicate-delete-syntax/)
- [LOOKUP SQL/JSON Support Matrix](../../../../support-scope-constraints/lookup-sql-json/)
