---
type: docs
title: 'LOOKUP JSON Column Definition'
weight: 60
---

LOOKUP tables can use `JSON` as a regular column type. JSON columns can be
created, stored, queried, filtered, and updated.

## Column Definition

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

## Insert and Query

```sql
INSERT INTO device_config VALUES (
    'DEV-01',
    'SEOUL',
    'READY',
    '{"region":"kr","level":3,"limits":{"high":85.0,"low":5.0}}'
);

SELECT device_id, config
FROM device_config
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

## Update JSON Values

```sql
UPDATE device_config
SET config = JSON_SET(config, '$.status', 'active')
WHERE site = 'SEOUL';

UPDATE device_config
SET config = JSON_SET_JSON(config, '$.extra', '{"verified":1}')
WHERE device_id = 'DEV-01';

UPDATE device_config
SET config = JSON_REMOVE(config, '$.extra')
WHERE device_id = 'DEV-01';
```

## Constraints

- A `JSON` column can be used as a regular LOOKUP column.
- A `JSON` column cannot be declared as the primary key.
- Write JSON path literals with single quotes, such as `'$.key'`.
- Dedicated JSON path indexes are not supported. For frequently searched values, consider extracting them into regular columns.
