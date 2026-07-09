---
type: docs
title: '17.1.1.10.3 LOOKUP predicate UPDATE syntax'
weight: 30
---

LOOKUP `UPDATE` supports general predicates in the `WHERE` clause, not only
primary-key equality. Every matching row is updated.

## Syntax

```sql
UPDATE table_name
   SET column_name = expression [, column_name = expression ...]
 WHERE predicate;
```

## Predicate Examples

```sql
UPDATE device_lookup
SET status = 'ACTIVE'
WHERE site = 'SEOUL' AND status = 'READY';

UPDATE device_lookup
SET score = score + 10
WHERE score BETWEEN 10 AND 80
  AND note LIKE 'sensor-%';

UPDATE device_lookup
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

The right side of the `SET` clause can reference the current row.

```sql
UPDATE device_lookup
SET score = score + 1
WHERE group_name IN ('A', 'B');
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

## Constraints

- The primary key column itself cannot be updated in the `SET` clause.
- If multiple rows match the predicate, multiple rows are updated.
- Use single quotes for JSON path literals, such as `'$.key'`; double quotes are parsed as SQL identifiers.
- For numeric JSON comparisons, prefer typed functions such as `JSON_EXTRACT_INTEGER` and `JSON_EXTRACT_DOUBLE`.

## Related Documents

- [LOOKUP predicate DELETE syntax](../lookup-predicate-delete-syntax/)
- [LOOKUP SQL/JSON Support](../../../../support-scope-constraints/lookup-sql-json/)
