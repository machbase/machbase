---
type: docs
title: '9.13.1 LOOKUP Predicate DELETE'
weight: 10
---

LOOKUP tables can be deleted with general predicates, not only primary-key
conditions. Every matching row is deleted.

## Example

```sql
DELETE FROM alarm_threshold
WHERE active = 0
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

JSON column predicates are supported.

```sql
DELETE FROM device_config
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') < 2;
```

## Policy

- The `WHERE` clause can use regular columns, ranges, strings, dates, and JSON path predicates.
- Without a `WHERE` clause, the statement deletes every row in the LOOKUP table.
- On production data, check the target range first with the same predicate.

```sql
SELECT COUNT(*)
FROM alarm_threshold
WHERE active = 0;
```
