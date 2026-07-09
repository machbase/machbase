---
title: '9.13 Predicate UPDATE/DELETE'
weight: 130
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="condition-lookup-delete"></a>

## LOOKUP Predicate DELETE

LOOKUP tables can be deleted with general predicates, not only primary-key
conditions. Every matching row is deleted.

### Example

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

### Policy

- The `WHERE` clause can use regular columns, ranges, strings, dates, and JSON path predicates.
- Without a `WHERE` clause, the statement deletes every row in the LOOKUP table.
- On production data, check the target range first with the same predicate.

```sql
SELECT COUNT(*)
FROM alarm_threshold
WHERE active = 0;
```

<a id="condition-lookup-update"></a>

## LOOKUP Predicate UPDATE

LOOKUP tables can be updated with general predicates, not only primary-key
conditions. Every matching row is updated.

### Example

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

### Policy

- The `WHERE` clause can use regular columns, ranges, strings, dates, and JSON path predicates.
- The right side of the `SET` clause can reference current row values.
- The primary key column itself cannot be updated.
- Before a large update, run `SELECT COUNT(*)` with the same predicate to check the affected range.

<a id="design-condition-lookup-update-delete"></a>

## UPDATE and DELETE Predicate Design

LOOKUP tables support both primary-key and general-predicate `UPDATE`/`DELETE`.

### UPDATE

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

### DELETE

```sql
DELETE FROM equipment_master
WHERE status = 'RETIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');
```

### Design Rules

1. **Use primary keys for single-row changes**: this is the clearest and fastest path.
2. **Check the target range for bulk changes**: a general predicate applies to every matching row.
3. **Extract frequently searched values**: dedicated JSON path indexes are not supported.
4. **Do not update the primary key**: primary key columns cannot be targets in the `SET` clause.

```sql
SELECT COUNT(*)
FROM equipment_master
WHERE status = 'RETIRED';
```
