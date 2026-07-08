---
type: docs
title: 'LOOKUP JSON Predicate Query'
weight: 10
---

LOOKUP `JSON` columns can be used in JSON path predicates.

## Basic Query

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

## Typed Extraction

Use typed JSON extraction functions when comparing numeric values as numbers.

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

## JSON Checks

```sql
SELECT sensor_id
FROM sensor_config
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

## Notes

- Write JSON path literals with single quotes, such as `'$.unit'`; double quotes are parsed as SQL identifiers.
- Use `->` when comparing a JSON path value as a string.
- Dedicated JSON path indexes are not supported. Extract frequently searched JSON values into regular columns for large LOOKUP tables.
