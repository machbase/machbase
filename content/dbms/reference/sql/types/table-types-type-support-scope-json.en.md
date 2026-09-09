---
type: docs
title: 'JSON Support by Table Type'
weight: 10
toc: true
---

Support scope for JSON columns in each table type.

## Support Summary

| Table Type | JSON Columns | JSON Path Queries | JSON PK | Notes |
|------------|:-------------:|:---------------:|:-------:|------|
| TAG | O | O | X | JSON columns and functions supported; PK not supported |
| LOG | O | O | X | JSON columns and functions supported |
| LOOKUP | O | O | X | Ordinary columns supported; JSON path indexes not supported |
| VOLATILE | X | X | X | Cannot create JSON columns |
| TRANSACTION | O | O | X | JSON columns and functions supported |

## LOOKUP Tables

LOOKUP supports JSON as an ordinary column.

```sql
CREATE LOOKUP TABLE config_lookup (
    key    VARCHAR(64) PRIMARY KEY,
    site   VARCHAR(32),
    config JSON
);

INSERT INTO config_lookup VALUES (
    'device-001',
    'SEOUL',
    '{"region":"kr","level":3,"state":"ready"}'
);

SELECT key
FROM config_lookup
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

Update JSON columns with JSON_SET, JSON_SET_JSON, JSON_REMOVE, and other JSON functions.

```sql
UPDATE config_lookup
SET config = JSON_SET(config, '$.state', 'active')
WHERE site = 'SEOUL';
```

JSON columns cannot be declared as primary keys.

```sql
-- Error
CREATE LOOKUP TABLE invalid_lookup (
    config JSON PRIMARY KEY
);
```

## VOLATILE Tables

VOLATILE does not support JSON column creation.

```sql
CREATE VOLATILE TABLE session_data (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
```

## JSON Functions by Table Type

| Function/Operator | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|-------------|:---:|:---:|:------:|:--------:|:---:|
| `->` operator | O | O | O | X | O |
| `JSON_EXTRACT*` | O | O | O | X | O |
| `JSON_TYPEOF` | O | O | O | X | O |
| `JSON_IS_VALID` | O | O | O | O | O |
| `JSON_SET` | O | O | O | X | O |
| `JSON_SET_JSON` | O | O | O | X | O |
| `JSON_REMOVE` | O | O | O | X | O |

## Usage Notes

- Write JSON paths as single-quoted strings, such as '$.key'.
- Use typed functions such as JSON_EXTRACT_INTEGER or JSON_EXTRACT_DOUBLE for numeric comparisons.
- LOOKUP does not support dedicated JSON path indexes. Extract frequently searched values into separate columns.
