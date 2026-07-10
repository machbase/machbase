---
title: '9.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="too-many-lookup-predicate-update-delete-row"></a>

## LOOKUP UPDATE/DELETE Predicate Error

LOOKUP UPDATE and conditional DELETE require a primary-key equality predicate.
Non-PK, range, and JSON-path predicates return `ERR-02190`. Query the target
primary keys first and execute the DML for each key. A DELETE statement without
a WHERE clause removes all rows.

<a id="error-lookup-json-path-primary-key"></a>

## LOOKUP JSON Primary Key Error

LOOKUP tables support `JSON` columns as regular columns, but a `JSON` column
cannot be declared as the primary key.

### Symptom

```sql
CREATE LOOKUP TABLE device_config (
    config JSON PRIMARY KEY,
    note   VARCHAR(32)
);
```

This statement fails because JSON is not a valid primary-key type.

### Cause

The primary key must identify rows with a stable key type. LOOKUP JSON columns
can be stored, queried, filtered, and updated, but not used as the primary key.

### Resolution

Use a separate identifier column as the primary key and keep JSON as a regular
column.

```sql
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(64) PRIMARY KEY,
    config    JSON
);

INSERT INTO device_config VALUES (
    'DEV-001',
    '{"status":"active","version":"1.0"}'
);
```

Use JSON path predicates when filtering by values inside the JSON document.

```sql
SELECT device_id
FROM device_config
WHERE config->'$.status' = 'active';
```

Write JSON path literals with single quotes. Double quotes are parsed as SQL
identifiers and can produce a column-name error.

<a id="limitations-lookup"></a>

## LOOKUP 제한사항
