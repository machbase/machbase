---
type: docs
title: 'JSON Column Design'
weight: 40
---

LOOKUP tables can store flexible reference-data attributes in `JSON` columns.
Use regular columns for values that are searched frequently, and JSON columns
for attributes that vary by device or item.

## Design Example

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

```sql
INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'SEOUL',
    'READY',
    '{"unit":"Celsius","range":{"min":-40,"max":150},"level":3}'
);
```

## Query and Update

```sql
SELECT sensor_id
FROM sensor_config
WHERE site = 'SEOUL'
  AND config->'$.unit' = 'Celsius'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;

UPDATE sensor_config
SET config = JSON_SET(config, '$.status', 'active')
WHERE sensor_id = 'TEMP-01';
```

## Design Rules

| Situation | Recommended approach |
|-----------|----------------------|
| Frequently searched or joined value | Regular column |
| Flexible attributes per device | JSON column |
| Numeric JSON predicate | `JSON_EXTRACT_INTEGER` or `JSON_EXTRACT_DOUBLE` |
| Primary key | Stable non-JSON identifier column |
| High-frequency path search | Extract the value into a regular column |

## Notes

- A JSON column can be used as a regular column, but not as the primary key.
- Dedicated JSON path indexes are not supported.
- Write JSON path literals with single quotes, such as `'$.key'`.
