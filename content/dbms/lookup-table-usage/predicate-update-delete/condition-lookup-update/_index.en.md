---
type: docs
title: '9.13.2 LOOKUP Predicate UPDATE'
weight: 50
---

LOOKUP tables can be updated with general predicates, not only primary-key
conditions. Every matching row is updated.

## Example

```sql
UPDATE alarm_threshold
SET high_limit = high_limit + 5.0,
    updated_at = NOW
WHERE device_type = 'MOTOR'
  AND active = 1;
```

JSON columns can also be used in predicates and update expressions.

```sql
UPDATE device_config
SET config = JSON_SET(config, '$.status', 'active')
WHERE site = 'SEOUL'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

## Policy

- The `WHERE` clause can use regular columns, ranges, strings, dates, and JSON path predicates.
- The right side of the `SET` clause can reference current row values.
- The primary key column itself cannot be updated.
- Before a large update, run `SELECT COUNT(*)` with the same predicate to check the affected range.
