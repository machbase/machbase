---
title: '5.7 Operations and Data Lifecycle'
weight: 70
toc: true
---

Manage raw retention, corrections, duplicate inputs, and ROLLUP history as distinct concerns.
Preview destructive work and verify both surviving data and downstream query results.

<a id="original-85-deleting-data"></a>

## Delete TAG Data

| Goal | Scope |
|---|---|
| Remove all data for one tag | Tag-name equality |
| Remove one tag's time interval | Tag and BASETIME bounds |
| Remove old data across tags | Supported time predicates or BEFORE |
| Remove all DATA | TAG DELETE without WHERE |

```sql
CREATE TAG TABLE ch5_lifecycle (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO ch5_lifecycle VALUES
    ('TAG_0001', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1.0);
INSERT INTO ch5_lifecycle VALUES
    ('TAG_0001', TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2.0);
INSERT INTO ch5_lifecycle VALUES
    ('TAG_0002', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3.0);

DELETE FROM ch5_lifecycle
 WHERE name = 'TAG_0001'
   AND time < TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT name, time, value
  FROM ch5_lifecycle
 ORDER BY name, time;

DELETE FROM ch5_lifecycle;
SELECT COUNT(*) FROM ch5_lifecycle;
DROP TABLE ch5_lifecycle;
```


After the first DELETE, TAG_0001 retains its January 2 value 2.0 and TAG_0002 retains value 3.0.
After whole-table DATA deletion, COUNT is 0. DATA deletion is separate from METADATA removal;
see [Metadata](../tag-metadata/) for the latter's preconditions.

Check [DML Syntax](../../reference/sql/syntax-dictionary-sql/dml-syntax/) for exact predicates and
Edition support. Repeated expiry can use supported
[Retention Policy](../../operations-configuration-recovery/policy-data-retention/).
Raw deletion and existing ROLLUP removal are different operations. Rebuild an aggregate range if
its result must change after a correction or deletion; preserve intentionally retained aggregates
according to their own retention policy.

<a id="original-85-duplication-removal"></a>

## Automatic Duplicate Removal

TAG_DUPLICATE_CHECK_DURATION is measured in minutes. Standard Edition accepts 0–43200; zero
disables it. Cluster Edition accepts only zero, so this exercise is Standard-only.

Rows with the same tag, axis, and data values are checked within the configured server-time-based
window. Removal happens during index processing and duplicate-row cleanup. Append success counts
are therefore not counts of already deduplicated rows. Late data outside the window may not be
deduplicated as expected; this is not a business-key uniqueness constraint.

```sql
CREATE TAG TABLE ch5_dedup (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
) TAG_DUPLICATE_CHECK_DURATION = 1440;

INSERT INTO ch5_dedup VALUES ('TAG_0001', NOW, 1.0);
INSERT INTO ch5_dedup SELECT name, time, value FROM ch5_dedup;

EXEC TABLE_FLUSH(ch5_dedup);
EXEC INDEX_FLUSH(ch5_dedup);

SELECT name, time, value
  FROM ch5_dedup
 WHERE name = 'TAG_0001';

ALTER TABLE ch5_dedup SET TAG_DUPLICATE_CHECK_DURATION = 60;
DROP TABLE ch5_dedup;
```


The second INSERT copies the first row, preserving exactly the same timestamp. No concurrent
input is assumed. Wait for storage and index processing and verify that one row remains.
Do not run both flush operations after every production input row. Data already removed by
retention is no longer present as a comparison candidate.

## Operational Checks

1. Define raw and aggregate retention separately.
2. Measure arrival delays before selecting a duplicate-check duration.
3. Preview tag and time bounds before deletion or correction.
4. Verify raw results and affected ROLLUPs afterwards.
5. Monitor ingestion, storage usage, and policy completion.

See [ROLLUP Rebuild](../../tag-rollup-usage/rollup-rebuild/) and
[TAG Corrections](../tag-data-update-correction/).
