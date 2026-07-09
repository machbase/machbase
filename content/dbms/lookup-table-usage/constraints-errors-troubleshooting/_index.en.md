---
title: '9.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="too-many-lookup-predicate-update-delete-row"></a>

## Large LOOKUP Predicate UPDATE/DELETE Range

LOOKUP predicate `UPDATE` and `DELETE` are supported. Because the statement
applies to every matching row, check the target range before changing
production data.

### Symptoms

- The statement succeeds, but more rows than expected are updated or deleted.
- A wide range predicate or JSON path predicate matches many rows.

### Diagnosis

Run the same predicate with `SELECT COUNT(*)` first.

```sql
SELECT COUNT(*)
FROM equipment
WHERE location = 'Building-A'
  AND status = 'inactive';
```

If needed, inspect the target keys.

```sql
SELECT eq_id, location, status
FROM equipment
WHERE location = 'Building-A'
  AND status = 'inactive';
```

### Resolution

- Use the primary key for single-row changes.
- Narrow bulk predicates and verify row counts before and after the DML.
- Use typed JSON functions for numeric JSON predicates.

```sql
UPDATE equipment
SET status = 'retired'
WHERE location = 'Building-A'
  AND status = 'inactive'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
```

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
