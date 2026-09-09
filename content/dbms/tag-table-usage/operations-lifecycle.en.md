---
type: docs
title: '5.7 Operations and Data Lifecycle'
weight: 70
toc: true
---
Manage TAG data through manual deletion, retention policies, and duplicate prevention.
This page explains operational choices and links to complete SQL references.

<a id="original-85-deleting-data"></a>

## Delete TAG Data

Limit deletion with tag identifiers and axis predicates. Common time-axis
TAG choices are:

| Purpose | Condition |
| --- | --- |
| Delete all data for one tag | Match tag `PRIMARY KEY` |
| Delete one tag's time range | Tag match + BASETIME range |
| Delete old data for all tags | BASETIME predicate or `BEFORE` |
| Delete all table data | TAG `DELETE` without predicates |

This example creates a separate test table, checks deletion scope, and cleans up.

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

After the first deletion, TAG_0001 retains value 2.0 at 2026-01-02, and
TAG_0002 retains 3.0. After full deletion, COUNT is 0. DATA and METADATA
deletion are separate. To remove tag registrations, also check
[METADATA Deletion](../tag-metadata/) requirements.

See [TAG DELETE Syntax](/dbms/reference/sql/syntax/dml-syntax/) for operators
and Edition support. Use [Retention Policies](/dbms/operations-configuration-recovery/policy-data-retention/)
when deletion must run periodically.

### Handle ROLLUP Data

Deleting raw TAG data and handling existing ROLLUP are separate operations.
If aggregates must reflect corrected or deleted source data, rebuild the
affected ROLLUP range. Do not repeatedly execute ROLLUP deletion as a
retention policy.

- [Partial ROLLUP Deletion and Rebuild](/dbms/tag-rollup-usage/rollup-rebuild/)
- [Rebuild ROLLUP After TAG Correction](../tag-data-update-correction/)

<a id="original-85-duplication-removal"></a>

## Automatic Deduplication

`TAG_DUPLICATE_CHECK_DURATION` sets the duplicate-check interval in minutes.
Standard Edition accepts 0–43200; 0 disables it. Cluster accepts only 0,
so the following enablement exercise is Standard Edition only.

Within the interval measured against server time, rows with identical tags,
axis values, and DATA values are duplicates. Detection occurs during index
processing and duplicate cleanup, so an Append success count is not an
already-deduplicated count. Late data outside the interval may not be
deduplicated as expected. This does not replace business-key uniqueness constraints.

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

The second input copies the first row, including its exact axis timestamp.
This exercise assumes no concurrent production ingestion. Wait for storage
buffers and index processing, then verify that one row remains. Do not call
both flush procedures per row in a normal collection loop.

Check full properties and restrictions against the current
[CREATE TAG TABLE Syntax](/dbms/reference/sql/syntax/ddl-syntax/). Data already
deleted by retention is no longer available for duplicate comparison.

## Operational Checklist

1. Define raw and ROLLUP retention periods separately.
2. Measure maximum arrival delay to choose a duplicate-check interval.
3. Verify target tags and time ranges with SELECT before deleting or correcting.
4. Validate ROLLUP and representative queries after bulk changes.
5. Monitor input volume, disk use, and retention execution together.
