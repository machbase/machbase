---
type: docs
title: 'LOOKUP SQL/JSON Support'
weight: 50
---

This page summarizes SQL and JSON support for LOOKUP tables. The examples were
verified against the prepared NFX main trunk build through port 5656.

## Support Matrix

| Feature | Support | Notes |
|---------|:-------:|-------|
| **Basic CRUD** | | |
| INSERT | O | Use regular SQL INSERT |
| SELECT | O | Primary-key and general predicates are supported |
| UPDATE with primary-key condition | O | Uses the primary-key hash path |
| DELETE with primary-key condition | O | Uses the primary-key hash path |
| UPDATE with non-primary-key predicate | O | Updates all rows that match the predicate |
| DELETE with non-primary-key predicate | O | Deletes all rows that match the predicate |
| **JSON** | | |
| JSON column | O | Can be created, stored, queried, and updated |
| JSON path query (`$.key`) | O | Supports `->`, `JSON_EXTRACT_*`, `JSON_TYPEOF`, and `JSON_IS_VALID` |
| JSON primary key | X | A JSON column cannot be declared as a primary key |
| JSON path index | X | Dedicated JSON path indexes are not supported |
| **Other** | | |
| Transaction | △ | Use LOOKUP DML as individual statements |
| Prepared Statement | O | Predicate UPDATE with bind/self-reference is supported |
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

JSON columns can be used in both predicates and update expressions.

```sql
SELECT id, status
FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;

UPDATE device_lookup
SET meta = JSON_SET(meta, '$.status', 'active')
WHERE meta->'$.region' = 'kr';
```

## Predicate UPDATE and DELETE

LOOKUP `UPDATE` and `DELETE` support primary-key equality as well as general
column predicates, range predicates, string predicates, date predicates, and
JSON path predicates.

```sql
UPDATE device_lookup
SET status = 'ACTIVE',
    score = score + 10,
    meta = JSON_SET(meta, '$.state', 'active')
WHERE site = 'SEOUL'
  AND status = 'READY'
  AND score BETWEEN 10 AND 80
  AND meta->'$.region' = 'kr';

DELETE FROM device_lookup
WHERE status = 'EXPIRED'
   OR updated_at < TO_DATE('2026-01-01 00:00:00')
   OR JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
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
| Non-PK DML | The statement applies to every matching row; check the target range first |
