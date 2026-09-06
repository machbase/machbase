---
title: '9.12 JSON Column Constraints and Queries'
weight: 120
toc: true
---
LOOKUP tables support JSON values and JSON path predicates. Use a separate scalar column for the
primary key, and extract frequently searched attributes into ordinary indexed columns when needed.


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

<a id="json-column-limitation"></a>

## JSON column design

LOOKUP tables support `JSON` as an ordinary column but not as a PRIMARY KEY. Use JSON for flexible
attributes and regular columns for values used frequently in joins or indexed predicates. The
following examples compare both designs with distinct table names.

### Design Example

```sql
-- Valid: JSON is a regular column; sensor_id is the primary key.
CREATE LOOKUP TABLE sensor_config_json (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

```sql
-- Alternative: split frequently queried attributes into regular columns.
CREATE LOOKUP TABLE sensor_config_columns (
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
FROM sensor_config_columns
WHERE site = 'SEOUL'
  AND unit = 'Celsius'
  AND level >= 3;

UPDATE sensor_config_columns
SET status = 'ACTIVE'
WHERE sensor_id = 'TEMP-01';
```

### Design Rules

| Situation | Recommended approach |
|-----------|----------------------|
| Frequently searched or joined value | Regular column |
| Flexible attributes per device | LOOKUP JSON column |
| Numeric predicate | Regular numeric column |
| Primary key | Stable identifier column |
| High-frequency path search | Extract the value into a regular column |

### Notes

- LOOKUP supports JSON columns and JSON path predicates; VOLATILE does not support JSON columns.
- Dedicated JSON path indexes are not supported on LOOKUP. Consider TRANSACTION or TAG if such
  indexes are required.

<a id="definition-column-lookup-json"></a>

<a id="lookup-json-column-limitation"></a>

## JSON and regular-column alternatives

The next examples store device settings either in a JSON column or in regular columns. A string
column can preserve an opaque payload, but a JSON column validates JSON input and supports the path
queries shown above.

### Column Definition

```sql
-- Valid JSON column definition.
CREATE LOOKUP TABLE device_config_json (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    config    JSON
);
```

### Alternative Schema and Query

```sql
CREATE LOOKUP TABLE device_config_columns (
    device_id VARCHAR(40) PRIMARY KEY,
    site      VARCHAR(32),
    status    VARCHAR(16),
    region    VARCHAR(16),
    level     INTEGER,
    limits    VARCHAR(512)
);

SELECT device_id, limits
FROM device_config_columns
WHERE region = 'kr'
  AND level >= 3;
```

### Update Values

```sql
UPDATE device_config_columns
SET status = 'ACTIVE'
WHERE site = 'SEOUL';

UPDATE device_config_columns
SET limits = '{"high":85.0,"low":5.0,"verified":1}'
WHERE device_id = 'DEV-01';
```

### Constraints

- JSON columns are supported on LOOKUP, but cannot be used as its primary key.
- Dedicated JSON path indexes require a supporting table type, such as TRANSACTION or TAG.
- Extract frequently searched values into regular LOOKUP columns.
