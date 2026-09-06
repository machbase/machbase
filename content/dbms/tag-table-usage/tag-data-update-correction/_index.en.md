---
title: '5.11 TAG Data UPDATE and Correction'
weight: 110
toc: true
---

TAG corrections either change raw values or retain raw values and apply an overlay at query time.
These approaches affect ROLLUP differently. The UPDATE exercises require Machbase DBMS 8.7.0
Standard Edition.

<a id="correction-performance-bulk-considerations-tag-data-update"></a>

## Correct Raw Values

Specify a tag selector and BASETIME bounds. SET expressions cannot reference existing-row
columns, so supply constants or bound values rather than `SET value = value + 1`.
Create this independent fixture, including default ROLLUPs for the rebuild example.

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

### Preview, Update, and Verify

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

The first query returns count 2, minimum 10.0, and maximum 99.0. Afterwards both TEMP-01 rows
have value 25.0 and status 1; TEMP-02 remains 20.0. A preview COUNT does not lock the target
against concurrent ingestion. Control the cutoff and scope separately in production.

### Multiple Tags and Failures

Tag selectors support `=`, `IN`, and `LIKE`. Preview names and counts and split large corrections
into smaller ranges. Multiple tags can be processed sequentially; an error does not establish that
the whole statement was rolled back. Requery changed values and remaining targets before retrying.

Use `>= start AND < end` for adjacent ranges. Ending a day at `23:59:59` omits fractional-second
values later in that second. See [TAG UPDATE](../../reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/)
for supported predicates and binding.

### Rebuild ROLLUP

Existing aggregates do not automatically follow raw corrections. Rebuild this fixture's corrected
range, then follow [ROLLUP Rebuild](../../tag-rollup-usage/rollup-rebuild/) for progress and query checks.

```sql
EXEC ROLLUP_REBUILD(ch5_correction, 'TEMP-01',
    TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

<a id="design-correction-tag"></a>

## Preserve Raw Data and Correct to NULL

Store raw and corrected values separately when the original must remain available. A correction
can itself be NULL, so do not use `corrected_value IS NOT NULL` as the only correction flag.

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

The result retains raw_value 99.0, sets is_corrected to 1, and returns NULL for effective_value.
A flag of 0 selects the original. This model applies an expression at query time; it does not
modify raw_value. Default ROLLUPs do not automatically aggregate the CASE expression, and merely
rebuilding a raw-value aggregate does not apply the overlay. Define a query or aggregation model
for effective values.

## Audit History and Validation

Use a separate history for multiple changes, reasons, and actors.

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

TAG mutation and LOG audit insertion do not share a TRANSACTION transaction. The application must
define operation IDs, ordering, partial-failure recovery, and retries. Creating this table alone
does not automatically write an audit trail.

Check raw/effective values, affected-row counts, interval statistics, and reports. Remove only
objects created for this exercise. CASCADE also removes ch5_correction's ROLLUPs.

```sql
DROP TABLE ch5_correction CASCADE;
DROP TABLE ch5_correction_overlay;
DROP TABLE ch5_correction_log;
```
