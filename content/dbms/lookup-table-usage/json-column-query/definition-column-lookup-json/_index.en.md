---
type: docs
title: 'LOOKUP JSON Column Limitation'
weight: 60
---

LOOKUP tables do not support `JSON` columns. For flexible reference-data
attributes, split frequently queried values into regular columns, serialize
rarely queried attributes into a string, or consider JSON columns in RDB/TAG
tables.

## Column Definition

```sql
-- Fails: LOOKUP tables cannot contain JSON columns.
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

## Alternative Schema and Query

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    region    VARCHAR(16),
    level     INTEGER,
    limits    VARCHAR(512)
);

SELECT device_id, limits
FROM device_config
WHERE region = 'kr'
  AND level >= 3;
```

## Update Values

```sql
UPDATE device_config
SET status = 'ACTIVE'
WHERE site = 'SEOUL';

UPDATE device_config
SET limits = '{"high":85.0,"low":5.0,"verified":1}'
WHERE device_id = 'DEV-01';
```

## Constraints

- JSON columns cannot be created in LOOKUP/VOLATILE tables.
- If JSON path predicates or JSON path indexes are required, consider RDB/TAG tables.
- Extract frequently searched values into regular LOOKUP columns.
