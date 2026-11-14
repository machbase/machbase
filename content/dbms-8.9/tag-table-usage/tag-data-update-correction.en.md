---
type: docs
title: '5.11 TAG Data UPDATE and Correction'
weight: 110
toc: true
---

TAG DATA correction can directly replace original values or preserve originals
and apply corrected values at query time. These approaches affect ROLLUP
differently. UPDATE exercises require Machbase DBMS 8.7.0 Standard Edition.

<a id="correction-performance-bulk-considerations-tag-data-update"></a>

## Correct Values Directly

Specify both tag-name and BASETIME predicates. SET expressions cannot reference
existing-row columns; pass a precomputed value or bind parameter instead of
`SET value = value + 1`. Create the following table with a nonconflicting name.
It includes default ROLLUP to verify aggregate correction.

```sql
CREATE TAG TABLE ch5_correction (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED,
    status INTEGER
) WITH ROLLUP;
INSERT INTO ch5_correction VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 0);
INSERT INTO ch5_correction VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 99.0, 0);
INSERT INTO ch5_correction VALUES
    ('TEMP-02', TO_DATE('2026-01-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 0);
```

### Check Scope, Update, and Query Again

```sql
SELECT COUNT(*), MIN(value), MAX(value)
  FROM ch5_correction
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
UPDATE ch5_correction SET value = 25.0, status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
SELECT name, time, value, status
  FROM ch5_correction ORDER BY name, time;
```

The first query returns 2 rows, minimum 10.0, and maximum 99.0. After UPDATE,
both TEMP-01 rows have value=25.0 and status=1; TEMP-02 retains 20.0. A preceding
COUNT does not lock targets. Control the cutoff and range separately when
concurrent ingestion is possible.

### Multiple Tags and Error Handling

Tag selection supports `=`, `IN`, and `LIKE`. Check target names and counts
before broad patterns or long time ranges, and divide work into smaller ranges.
Multiple tags may be processed sequentially; do not assume a failure atomically
undoes the entire statement. Requery changed values and remaining targets before retrying.

Use `>= start AND < end` for adjacent time intervals to avoid processing boundary
rows twice. Ending a full day at `23:59:59` can miss fractional-second data
after that time. See [TAG UPDATE](../../reference/sql/syntax/dml-syntax/tag-data-update-syntax/)
for allowed predicates and binding.

### Rebuild ROLLUP

Changing source data does not automatically update previously calculated ROLLUP.
Rebuild the corrected interval as follows, then follow
[ROLLUP Rebuild](../../tag-rollup-usage/rollup-rebuild/) for progress and query validation.

```sql
EXEC ROLLUP_REBUILD(ch5_correction, 'TEMP-01',
    TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

<a id="design-correction-tag"></a>

## Preserve Originals and Correct to NULL

Store original and corrected values in separate columns to retain the initial
value. A corrected value may itself be NULL, so use a flag instead of testing
only `corrected_value IS NOT NULL`.

```sql
CREATE TAG TABLE ch5_correction_overlay (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    raw_value DOUBLE,
    corrected_value DOUBLE,
    is_corrected SHORT
);
INSERT INTO ch5_correction_overlay VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 99.0, NULL, 0);
UPDATE ch5_correction_overlay
   SET corrected_value = NULL, is_corrected = 1
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
SELECT name, raw_value, is_corrected,
       CASE WHEN is_corrected = 1 THEN corrected_value ELSE raw_value END AS effective_value
  FROM ch5_correction_overlay;
```

raw_value is 99.0, is_corrected is 1, and effective_value is NULL. A flag of 0
selects the original. This approach chooses values in a query expression without
changing raw_value. Do not assume default ROLLUP aggregates the CASE expression
automatically or that rebuilding raw_value incorporates corrections. Define a
separate query/aggregation model for effective values.

## Correction History and Validation

Record separate history to retain reasons and operators for repeated changes.

```sql
CREATE LOG TABLE ch5_correction_log (
    sensor_name VARCHAR(64),
    target_time DATETIME,
    old_value DOUBLE,
    new_value DOUBLE,
    reason VARCHAR(256),
    corrected_by VARCHAR(64)
);
```

TAG updates and LOG history writes do not share one TRANSACTION transaction.
Design ordering, partial-failure handling, and operation identifiers for retries
in the application. Creating a history table does not automatically record audits.

After correction, verify original/effective values, affected-row counts, interval
statistics, and reports. Then remove only exercise objects. The CASCADE below
also deletes the ROLLUPs of ch5_correction.

```sql
DROP TABLE ch5_correction CASCADE;
DROP TABLE ch5_correction_overlay;
DROP TABLE ch5_correction_log;
```
