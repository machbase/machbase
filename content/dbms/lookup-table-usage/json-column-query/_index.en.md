---
title: '9.12 JSON Column Constraints and Queries'
weight: 120
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="condition-query-lookup-json"></a>

## LOOKUP JSON Predicate Query

LOOKUP `JSON` columns can be used in JSON path predicates.

### Basic Query

```sql
CREATE LOOKUP TABLE sensor_config (
    sensor_id VARCHAR(80) PRIMARY KEY,
    location  VARCHAR(200),
    config    JSON
);

INSERT INTO sensor_config VALUES (
    'TEMP-01',
    'factory1',
    '{"unit":"celsius","level":3,"threshold":{"high":90.0}}'
);

SELECT sensor_id, config
FROM sensor_config
WHERE config->'$.unit' = 'celsius';
```

### Typed Extraction

Use typed JSON extraction functions when comparing numeric values as numbers.

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

### JSON Checks

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

### Notes

- Write JSON path literals with single quotes, such as `'$.unit'`; double quotes are parsed as SQL identifiers.
- Use `->` when comparing a JSON path value as a string.
- Dedicated JSON path indexes are not supported. Extract frequently searched JSON values into regular columns for large LOOKUP tables.

<a id="design-column-lookup-json"></a>

## JSON Column Limitation

LOOKUP tables do not support `JSON` columns. For flexible reference-data
attributes, split frequently queried values into regular columns, serialize
rarely queried attributes into a string, or consider JSON columns in RDB/TAG
tables.

### Design Example

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

### Query and Update

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

### Design Rules

| Situation | Recommended approach |
|-----------|----------------------|
| Frequently searched or joined value | Regular column |
| Flexible attributes per device | Serialized string or RDB/TAG JSON column |
| Numeric predicate | Regular numeric column |
| Primary key | Stable identifier column |
| High-frequency path search | Extract the value into a regular column |

### Notes

- JSON columns cannot be created in LOOKUP/VOLATILE tables.
- If JSON path predicates or JSON path indexes are required, consider RDB/TAG tables.

<a id="definition-column-lookup-json"></a>

## LOOKUP JSON Column Limitation

LOOKUP tables do not support `JSON` columns. For flexible reference-data
attributes, split frequently queried values into regular columns, serialize
rarely queried attributes into a string, or consider JSON columns in RDB/TAG
tables.

### Column Definition

```sql
-- Fails: LOOKUP tables cannot contain JSON columns.
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

### Alternative Schema and Query

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

### Update Values

```sql
UPDATE device_config
SET status = 'ACTIVE'
WHERE site = 'SEOUL';

UPDATE device_config
SET limits = '{"high":85.0,"low":5.0,"verified":1}'
WHERE device_id = 'DEV-01';
```

### Constraints

- JSON columns cannot be created in LOOKUP/VOLATILE tables.
- If JSON path predicates or JSON path indexes are required, consider RDB/TAG tables.
- Extract frequently searched values into regular LOOKUP columns.
