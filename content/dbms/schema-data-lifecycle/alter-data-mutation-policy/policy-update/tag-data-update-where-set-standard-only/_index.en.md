---
type: docs
title: 'TAG data UPDATE WHERE/SET support scope'
weight: 30
---

TAG data UPDATE is supported with constraints that keep the update target explicit.

## Supported form

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE tag
   SET value = value * 0.98
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

## Allowed WHERE/SET scope

- Tag selector: `name =`, `name IN (...)`, `name LIKE ...`
- Time condition: `time =`, `BETWEEN`, two-sided ranges, one-sided ranges
- Additional filters: data-column predicates
- SET targets: data columns, including `SUMMARIZED` data columns

## Not allowed

- UPDATE without a WHERE clause
- UPDATE without a tag selector
- UPDATE without a time condition
- `OR`, subqueries, and aggregate predicates
- SET targets such as `name`, `time`, or metadata columns

Metadata columns use `UPDATE tag METADATA SET ...`.
