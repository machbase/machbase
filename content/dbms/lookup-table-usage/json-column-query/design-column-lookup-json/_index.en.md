---
type: docs
title: 'JSON Column Limitation'
weight: 40
---

LOOKUP tables do not support `JSON` columns. For flexible reference-data
attributes, split frequently queried values into regular columns, serialize
rarely queried attributes into a string, or consider JSON columns in RDB/TAG
tables.

## Design Example

```sql
-- Fails: LOOKUP tables cannot contain JSON columns.
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

```sql
-- Alternative: split frequently queried attributes into regular columns.
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    unit      VARCHAR(16),
    level     INTEGER
);
```

## Query and Update

```sql
SELECT sensor_id
FROM sensor_config
WHERE site = 'SEOUL'
  AND unit = 'Celsius'
  AND level >= 3;

UPDATE sensor_config
SET status = 'ACTIVE'
WHERE sensor_id = 'TEMP-01';
```

## Design Rules

| Situation | Recommended approach |
|-----------|----------------------|
| Frequently searched or joined value | Regular column |
| Flexible attributes per device | Serialized string or RDB/TAG JSON column |
| Numeric predicate | Regular numeric column |
| Primary key | Stable identifier column |
| High-frequency path search | Extract the value into a regular column |

## Notes

- JSON columns cannot be created in LOOKUP/VOLATILE tables.
- If JSON path predicates or JSON path indexes are required, consider RDB/TAG tables.
