---
type: docs
title: '18.8.5 LOOKUP SQL/JSON Support'
weight: 50
toc: true
---

This page summarizes SQL and JSON support for LOOKUP tables.

## Support Matrix

| Feature | Support | Notes |
|---------|:-------:|-------|
| **Basic CRUD** | | |
| INSERT | O | Use regular SQL INSERT |
| SELECT | O | Primary-key and general predicates are supported |
| UPDATE with primary-key condition | O | Uses the primary-key fast path |
| DELETE with primary-key condition | O | Uses the primary-key fast path |
| UPDATE with a general predicate | O | Collects matching primary keys and updates every target row |
| DELETE with a general predicate | O | Collects matching primary keys and deletes every target row |
| **JSON** | | |
| JSON column | O | Can be created, stored, queried, and updated |
| JSON path query (`$.key`) | O | Supports `->`, `JSON_EXTRACT_*`, `JSON_TYPEOF`, and `JSON_IS_VALID` |
| JSON primary key | X | A JSON column cannot be declared as a primary key |
| JSON path index | X | Dedicated JSON path indexes are not supported |
| **Other** | | |
| Transaction | △ | Use LOOKUP DML as individual statements |
| Prepared Statement | O | Binding is supported with primary-key and general predicates |
| Append API | △ | Regular SQL INSERT is the default; LOOKUP append follows its own duplicate-key policy |

## JSON Column Example

```sql
CREATE LOOKUP TABLE device_lookup
(
    id          VARCHAR(32) PRIMARY KEY,
    site        VARCHAR(32),
    status      VARCHAR(16),
    score       INTEGER,
    updated_at  DATETIME,
    meta        JSON
);

INSERT INTO device_lookup VALUES
(
    'dev-001',
    'SEOUL',
    'READY',
    30,
    TO_DATE('2026-06-01 10:00:00'),
    '{"region":"kr","level":3,"tags":["edge","main"]}'
);
```

JSON paths can be used in SELECT, UPDATE, and DELETE predicates.

```sql
SELECT id, status
FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;

UPDATE device_lookup
SET meta = JSON_SET(meta, '$.status', 'active')
WHERE meta->'$.region' = 'kr'
  AND status = 'READY';
```

## UPDATE and DELETE Predicates

LOOKUP UPDATE and DELETE support primary-key, non-primary-key, range, string,
date, logical, and JSON-path predicates. A DELETE statement without a WHERE
clause removes all rows.

```sql
UPDATE device_lookup
SET status = 'ACTIVE',
    score = score + 10,
    meta = JSON_SET(meta, '$.state', 'active')
WHERE site = 'SEOUL'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;

DELETE FROM device_lookup
WHERE status = 'EXPIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00');

DELETE FROM device_lookup;
```

The right side of the `SET` clause can reference the current row. The primary
key column itself cannot be updated.

## Constraints

| Item | Description |
|------|-------------|
| JSON primary key | A `JSON` column cannot be used as a primary key |
| JSON path index | Dedicated JSON path indexes are not supported |
| JSON path literal | Use single quotes (`'$.key'`); double quotes are parsed as identifiers |
| Numeric comparison | Prefer `JSON_EXTRACT_INTEGER` or `JSON_EXTRACT_DOUBLE` instead of `->` |
| General-predicate DML | Affects every matching row; check the target range before execution |
