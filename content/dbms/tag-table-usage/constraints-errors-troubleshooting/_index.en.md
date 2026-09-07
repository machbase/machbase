---
title: '5.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
aliases:
  - /dbms/troubleshooting/update-delete/
---

Use Standard Edition for this page's TAG DATA UPDATE exercises. Set up independent fixtures
before running the valid and intentionally failing statements separately. Do not mix expected
errors into an unattended success-only SQL script.

```sql
CREATE TAG TABLE ch5_error_time (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    status INTEGER
) METADATA (location VARCHAR(64));
INSERT INTO ch5_error_time METADATA VALUES ('sensor-01', 'zone-1');
INSERT INTO ch5_error_time METADATA VALUES ('sensor-02', 'zone-2');
INSERT INTO ch5_error_time VALUES
    ('sensor-01', TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 0);
INSERT INTO ch5_error_time VALUES
    ('sensor-02', TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 0);
CREATE TAG TABLE ch5_error_distance (
    name VARCHAR(64) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value DOUBLE SUMMARIZED
);
```


<a id="rejected-condition-tag-data-update-where"></a>

## Missing or Unsupported WHERE Conditions

TAG DATA UPDATE requires both a tag selector and a BASETIME condition.
These examples intentionally fail:

```sql
-- Missing time condition
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01';

-- Missing tag selector
UPDATE ch5_error_time SET value = 99.9
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Unsupported OR condition
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01'
   OR name = 'sensor-02';
```


Valid selectors include name equality, IN, and LIKE combined with supported time bounds.
A value predicate alone, name alone, time alone, OR, subqueries, and aggregate predicates do not
provide the supported UPDATE form. Correct the scope as follows:

```sql
UPDATE ch5_error_time
   SET value = 99.9
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE ch5_error_time
   SET status = 1
 WHERE name IN ('sensor-01', 'sensor-02')
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```


### NAME/TIME Binding Errors

Since 8.7.0, Standard supports binding predicate values:

```sql
UPDATE ch5_error_time
   SET value = ?
 WHERE name = ?
   AND time = ?;
```


This is SQL to prepare and bind through an SDK, not an unbound machsql command. If the required
conditions are present but the server returns ERR-2190, check the server version and the SDK's
named/positional binding support. Rebind SET, NAME, and TIME values on reuse. See
[TAG UPDATE Binding](../../reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind).

<a id="column-error-tag-data-update-set"></a>

## Protected SET Targets

DATA UPDATE may change ordinary DATA columns, including supported SUMMARIZED values, but not the
tag name, BASETIME, or metadata. These attempts are intentionally invalid:

```sql
-- Expected failure: changing the tag-name column
UPDATE ch5_error_time
   SET name = 'new-sensor'
 WHERE name = 'old-sensor'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Expected failure: changing the axis column
UPDATE ch5_error_time
   SET time = NOW
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Expected failure: metadata in DATA UPDATE
UPDATE ch5_error_time
   SET location = 'zone-2'
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```


Use DATA UPDATE for values and METADATA UPDATE for attributes:

```sql
UPDATE ch5_error_time
   SET value = 99.9,
       status = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

```sql
UPDATE ch5_error_time METADATA
   SET location = 'zone-2'
 WHERE name = 'sensor-01';
```


SET expressions for TAG DATA cannot read existing row columns. Supply a calculated constant or
bound value. Changing name/axis identity requires a separately designed insert/delete transition,
not an arbitrary DATA UPDATE.

<a id="tag-stat-distance-schema-error"></a>

## Distance STAT Schema Errors

8.7.0 distance-axis statistics use numeric *_DISTANCE columns. Old SQL requesting *_TIME names
can fail. Inspect both the table and view:

```sql
DESC ch5_error_distance;
DESC V$CH5_ERROR_DISTANCE_STAT;
```


The five axis fields must be MIN_DISTANCE, MAX_DISTANCE, MIN_VALUE_DISTANCE, MAX_VALUE_DISTANCE,
and RECENT_ROW_DISTANCE, using the original DOUBLE/LONG/ULONG type. Cluster additionally prepends
HOSTNAME VARCHAR(64). Adjust positional mappings or read by name. Time-axis tables keep DATETIME
*_TIME fields. See [STAT Queries](../query-analysis/#tag-stat-axis-schema).

<a id="limitations-tag"></a>
<a id="지원하지-않는-기능"></a>

## Support Boundaries

| Feature | Scope |
|---|---|
| DATA UPDATE | Standard, logical TAG table, tag plus BASETIME predicates |
| Metadata changes | Separate METADATA SQL |
| DATA DELETE | Supported BEFORE/predicates or all rows |
| Multiple name keys or both special axes | Not supported |
| DATA column ALTER ADD/DROP | Not supported |
| Metadata ALTER ADD/DROP | Standard Edition |

A unique tag per event increases tag metadata rather than giving ordinary row-key semantics.
Measure metadata memory and ingestion/query behavior at the intended tag count.
Late time-axis observations are allowed, but large out-of-order workloads need measurement.
Do not generalize Standard-only DATA UPDATE to Cluster.

## Cleanup

Query successful changes and remove only these fixtures.

```sql
SELECT name, time, value, status FROM ch5_error_time ORDER BY name, time;
DROP TABLE ch5_error_time;
DROP TABLE ch5_error_distance;
```
