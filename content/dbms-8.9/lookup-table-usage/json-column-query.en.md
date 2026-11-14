---
type: docs
title: '9.12 JSON Columns and Queries'
weight: 120
toc: true
---
This section covers LOOKUP JSON column support and JSON predicate queries.


<a id="condition-query-lookup-json"></a>

## LOOKUP JSON Predicate Queries

LOOKUP supports `JSON` for ordinary columns. Use JSON columns to store flexible attributes alongside
reference data.

```sql
CREATE LOOKUP TABLE ch9_json (
    sensor_id VARCHAR(80) PRIMARY KEY,
    location  VARCHAR(200),
    config    JSON
);

INSERT INTO ch9_json VALUES (
    'TEMP-01',
    'factory1',
    '{"unit":"celsius","level":3,"threshold":{"high":90.0}}'
);

SELECT sensor_id, config
FROM ch9_json
WHERE config->'$.unit' = 'celsius';
```

<a id="design-column-lookup-json"></a>

## Type-Specific JSON Predicates

Use type-specific JSON extraction functions to compare numeric values as numbers.

```sql
SELECT sensor_id
FROM ch9_json
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

You can also inspect the JSON structure itself.

```sql
SELECT sensor_id
FROM ch9_json
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

<a id="lookup-json-serialized-string"></a>

## PRIMARY KEY Restriction

LOOKUP can store JSON columns, but JSON cannot be a `PRIMARY KEY`. Use a stable ordinary type such
as `INTEGER`, `LONG`, or `VARCHAR` for row identifiers.

```sql
-- Expected failure: JSON cannot be a primary key.
CREATE LOOKUP TABLE ch9_json_bad (
    config JSON PRIMARY KEY,
    note   VARCHAR(80)
);
```

```sql
-- Recommended: use a separate identifier as the primary key.
CREATE LOOKUP TABLE ch9_json_ok (
    sensor_id VARCHAR(80) PRIMARY KEY,
    config    JSON,
    note      VARCHAR(80)
);
```

<a id="lookup-json-design-criteria"></a>

## Design Criteria

| Situation | Recommended approach |
|------|----------|
| Values frequently used in joins/searches | Separate columns |
| Flexible attributes that differ by device | JSON column |
| Numeric predicate queries | Extract into ordinary numeric columns |
| Primary key | Stable identifier column |
| Frequent path queries | Extract into separate columns |

Dedicated JSON path indexes are unsupported. For frequent predicates, first consider extracting the
values into separate indexed columns.

```sql
CREATE LOOKUP TABLE ch9_json_fast (
    sensor_id VARCHAR(80) PRIMARY KEY,
    unit      VARCHAR(16),
    level     INTEGER,
    config    JSON
);

CREATE INDEX ch9_json_unit_idx ON ch9_json_fast(unit);
```

<a id="lookup-json-update-delete"></a>

## UPDATE and DELETE Predicates

```sql
UPDATE ch9_json
SET location = 'factory2'
WHERE config->'$.unit' = 'celsius';

DELETE FROM ch9_json
WHERE JSON_EXTRACT_INTEGER(config, '$.level') < 2;
```

Because the target scope can be broad, check the count with the same predicate before UPDATE/DELETE.

<a id="lookup-json-limitations"></a>

Clean up the example objects as follows. `ch9_json_bad` is excluded because its creation intentionally fails.

```sql
DROP TABLE ch9_json_fast;
DROP TABLE ch9_json_ok;
DROP TABLE ch9_json;
```

## Considerations

- LOOKUP supports JSON as an ordinary column.
- JSON cannot be a primary key.
- Dedicated JSON path indexes are unsupported.
- Extract frequently searched values into ordinary LOOKUP columns.
- Consider TRANSACTION or TAG tables if JSON path indexes are required.
