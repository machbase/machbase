---
type: docs
title: '5.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
aliases:
  - /dbms/troubleshooting/update-delete/
---


The UPDATE exercises require Standard Edition. Create these tables first and run
valid SQL separately from intentional failures. Do not include failure examples
in a normal script. Do not delete existing objects with conflicting names.

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

## TAG Data UPDATE WHERE Errors

WHERE must include both tag selection and BASETIME predicates. Ambiguous or
unsupported conditions cause UPDATE to fail.

{{< callout type="warning" >}}
**Required Predicates**

Specify both a tag predicate such as `WHERE name ...` and a BASETIME predicate
such as `time ...`. Full UPDATE without conditions, tag-only UPDATE, and
time-only UPDATE are not allowed.
{{< /callout >}}

### Symptom

The following UPDATE statements are rejected:

```sql
-- No time predicate
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01';

-- No tag predicate
UPDATE ch5_error_time SET value = 99.9
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Uses OR
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01'
   OR name = 'sensor-02';
```

### Cause

Conditions that cannot clearly restrict target tags and the time range are rejected.

| Predicate | Supported |
|-----------|:--------:|
| `name = 'sensor-01' AND time >= ...` | O |
| `name IN ('sensor-01', 'sensor-02') AND time BETWEEN ...` | O |
| `name LIKE 'sensor-%' AND time < ...` | O |
| Only `value > 10` | X |
| Only `name = 'sensor-01'` | X |
| Only `time >= ...` | X |
| `OR`, subqueries, aggregate predicates | X |

### Resolution

Specify both tag and time predicates.

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

### NAME or TIME Binding Rejected with `ERR-02190`

Since Machbase 8.7.0, Standard Edition supports bind parameters for NAME and
BASETIME predicate values as follows:

```sql
UPDATE ch5_error_time
   SET value = ?
 WHERE name = ?
   AND time = ?;
```

If both required predicates are present but the statement fails with
`ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)`,
check the server version. Older servers do not support NAME/TIME binding for TAG
data UPDATE. Upgrade to 8.7.0 or later. For named markers, also use an 8.7.0 SDK
that supports the named API.

The `?` example is SQL for SDK prepare/bind, not a statement to run unchanged
without values in machsql. When reusing a prepared statement, rebind all SET,
NAME, and TIME values. See
[TAG Data UPDATE Binding](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)
for marker rules.

Before a large UPDATE, run `SELECT COUNT(*)` with the same WHERE condition to
check the target row count.

<a id="column-error-tag-data-update-set"></a>

## TAG Data UPDATE SET Target Errors

SET can target only actual DATA columns. PRIMARY KEY, BASETIME, and metadata
columns raise errors as SET targets.

{{< callout type="warning" >}}
**SET Targets**

`value` and user DATA columns can be updated. `name`, `time`, and columns in the
METADATA block cannot be SET targets in TAG data UPDATE.
{{< /callout >}}

### Symptom

```sql
-- Error: attempts to update PRIMARY KEY column (name)
UPDATE ch5_error_time
   SET name = 'new-sensor'
 WHERE name = 'old-sensor'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Error: attempts to update BASETIME column (time)
UPDATE ch5_error_time
   SET time = NOW
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Error: changes metadata through data UPDATE
UPDATE ch5_error_time
   SET location = 'zone-2'
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

### UPDATE Support by Column Type

| Column type | Description | Data UPDATE |
|-----------|------|:-----------:|
| PRIMARY KEY (`name`) | Unique tag identifier | X |
| BASETIME (`time`) | Time-series timestamp | X |
| DATA (`value`, auxiliary columns) | Actual row values | O |
| `SUMMARIZED` DATA column | Column with statistics | O |
| Metadata column | Tag attribute in METADATA | X |

### Resolution

Use ordinary UPDATE for DATA values.

```sql
UPDATE ch5_error_time
   SET value = 99.9,
       status = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

Use separate syntax for metadata.

```sql
UPDATE ch5_error_time METADATA
   SET location = 'zone-2'
 WHERE name = 'sensor-01';
```

To change a tag name or time axis, insert data with the new `name`/`time`, then
delete the original data according to operational policy.

<a id="tag-stat-distance-schema-error"></a>

## BASE DISTANCE TAG STAT Column Errors

Machbase 8.7.0 exposes distance-named, numeric axis columns in BASE DISTANCE TAG
`V$<TABLE>_STAT` views. Pre-upgrade SQL referencing `MIN_TIME`, `MAX_TIME`, or
`RECENT_ROW_TIME` may fail with column-not-found errors.

### Symptoms

- Existing `*_TIME` columns cannot be queried in BASE DISTANCE statistics after upgrade.
- Older servers may interpret distances as `DATETIME`, displaying meaningless dates.
- Using Standard ordinal result mappings in Cluster may shift columns because
  `HOSTNAME` is added first.

### Diagnosis

Check both the table axis and actual statistics-view schema.

```sql
DESC ch5_error_distance;
DESC V$CH5_ERROR_DISTANCE_STAT;
```

For BASE DISTANCE, `MIN_DISTANCE`, `MAX_DISTANCE`, `MIN_VALUE_DISTANCE`,
`MAX_VALUE_DISTANCE`, and `RECENT_ROW_DISTANCE` should use the original distance
type. Cluster adds `HOSTNAME VARCHAR(64)` as the first column.

### Resolution

1. Replace old `*_TIME` SQL names with corresponding `*_DISTANCE` names.
2. Change SDK mappings from `DATETIME` to the original `DOUBLE`, `LONG`, or `ULONG`.
3. Read Cluster results by name or recheck ordinals including `HOSTNAME`.
4. Retain existing `*_TIME DATETIME` mappings for BASE TIME TAG queries.

See [Per-Tag Statistics Views](../query-analysis/#tag-stat-axis-schema) for the
complete mapping and Cluster aggregation precautions.

<a id="limitations-tag"></a>

## Constraints and Precautions

<a id="지원하지-않는-기능"></a>

### Feature Support

| Feature | Status |
|------|------|
| Time-series DATA UPDATE | Standard Edition; tag/BASETIME predicates required |
| Metadata UPDATE | Supported (`UPDATE ... METADATA`) |
| DELETE | Supported (`BEFORE`, tag/axis predicates, or full deletion) |
| Multiple PRIMARY KEY columns | Unsupported; one column only |
| BASETIME and BASEDISTANCE together | Unsupported |
| TAG DATA ordinary-column ALTER ADD/DROP | Unsupported |
| TAG METADATA ALTER ADD/DROP | Supported in Standard Edition |

### Tag Count Limits

- System settings limit the number of tags per TAG table.
- More tags increase tag-index and metadata memory use. Measure query and ingestion
  performance with production-scale data.
- Do not make tag names unique per record (an antipattern; see
  [One Table per Sensor](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create)).

<a id="시간-역삽입-제한"></a>

### Late-Arriving Data

- BASETIME accepts arbitrary past timestamps.
- Measure ingestion rates and query performance separately for workloads with
  substantial late-arriving data.

### Cluster Edition Support

Cluster Edition supports TAG tables.

However, TAG data UPDATE is Standard Edition only and is not supported in Cluster.

### Summary

```
TAG table = sensor name (PK) + time/distance axis + measurements
- INSERT/APPEND: O
- UPDATE: DATA requires Standard Edition tag/BASETIME predicates; METADATA uses separate SQL
- DELETE: O (BEFORE or tag/axis predicates)
- METADATA: O (separate attributes; UPDATE supported)
```

---

**Read Next**
- [TRANSACTION Table Design](/dbms/rdb-table-usage/)

## Clean Up the Exercise

Verify successful changes with SELECT, then remove only the exercise tables.

```sql
SELECT name, time, value, status FROM ch5_error_time ORDER BY name, time;
DROP TABLE ch5_error_time;
DROP TABLE ch5_error_distance;
```
