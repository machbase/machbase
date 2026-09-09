---
type: docs
title: '6.10 ROLLUP_REBUILD'
weight: 100
toc: true
aliases:
  - /dbms/tag-rollup-usage/delete-partial-rebuild-rollup/
---

ROLLUP_REBUILD recalculates aggregates after historical source-value corrections and is available
only in Standard Edition. Unlike FORCE, it deletes and recreates affected buckets. It is not a
general-purpose command for rebuilding arbitrary ROLLUP definitions.

## Check Supported Targets First

| Target | Current support path |
|---|---|
| Complete SEC→MIN→HOUR hierarchy created with WITH ROLLUP | Basic numeric, extension, and full-document JSON modes |
| Supported Custom tree linked to the source | Check 1 SEC/1 MIN/1 HOUR intervals and SELECT compatibility with rebuild boundaries |
| Manually named general ROLLUP with arbitrary intervals | Do not assume the same support as automatic hierarchies |
| Automatic MIN/HOUR-only hierarchy without SEC | Not considered a complete default hierarchy |
| Custom with other intervals, such as 10 MIN | Unsupported by the current time-boundary generation path |
| Cluster Edition | Unsupported |

Custom SELECT buckets, INTERVAL, and reference time zone must align with rebuild boundaries. First
inspect the tree for unsupported jobs. Creation support for a Custom expression or interval does not
imply rebuild support.

## Time Arguments and Bucket Boundaries

Specify timestamp strings or TO_DATE with constant strings. This path does not evaluate arbitrary
DATETIME expressions; do not use NOW arithmetic or bound parameters in examples.

The operation includes the buckets containing both endpoints and expands to entire buckets. At the
1-minute level, 00:00:30–00:01:00 recalculates the 00:00 and 00:01 buckets, namely
[00:00:00, 00:02:00). Equal start/end values recalculate the containing bucket; start later than end is an error. Upper time levels expand to wider buckets.

## Default Hierarchy and Custom Correction Exercise

### 1. Preparation and Initial Aggregation

```sql
CREATE TAG TABLE ch6_rebuild (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
CREATE TAG TABLE ch6_rebuild_dst (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, sum_value DOUBLE, cnt LONG
);
CREATE ROLLUP ch6_rebuild_custom INTO (ch6_rebuild_dst)
AS (
    SELECT name, DATE_TRUNC('minute', time) AS time, SUM(value), COUNT(value)
      FROM ch6_rebuild GROUP BY name, time
) INTERVAL 1 MIN;

INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:00:00'), 1);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:00:30'), 200);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:01:00'), 300);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:01:30'), 4);
EXEC TABLE_FLUSH(ch6_rebuild);

SELECT DISTINCT ROLLUP_NAME, INTERVAL_TIME FROM V$ROLLUP
 WHERE ROOT_TABLE = 'CH6_REBUILD' ORDER BY INTERVAL_TIME, ROLLUP_NAME;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_SEC FORCE;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_MIN FORCE;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_HOUR FORCE;
ALTER ROLLUP ch6_rebuild_custom FORCE;
SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

Verify that automatically generated names in control commands match V$ROLLUP above. Do not guess
names of other objects. Initial minute averages are 100.5 and 152.

### 2. Correct Source Data and Rebuild

```sql
UPDATE ch6_rebuild SET value = 20
 WHERE name = 'S1' AND time = TO_DATE('2026-01-01 00:00:30');
UPDATE ch6_rebuild SET value = 30
 WHERE name = 'S1' AND time = TO_DATE('2026-01-01 00:01:00');
EXEC ROLLUP_REBUILD(ch6_rebuild, 'S1',
    TO_DATE('2026-01-01 00:00:30'),
    TO_DATE('2026-01-01 00:01:00'));
```

### 3. Compare Source, General, and Custom Results

```sql
SELECT DATE_TRUNC('minute', time) AS bucket, SUM(value), COUNT(value), AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
SELECT rollup('min', 1, time) AS bucket, SUM(value), COUNT(value), AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
SELECT time, SUM(sum_value), SUM(cnt), SUM(sum_value) / SUM(cnt)
  FROM ch6_rebuild_dst WHERE name = 'S1'
 GROUP BY time ORDER BY time;
SHOW ROLLUPGAP;
```

All three results have sum 21, count 2, average 10.5 at 00:00, and sum 34, count 2, average 17 at
00:01. The value 4 at 00:01:30, after the end argument, must also be included when its bucket is
recalculated.

## Operational Impact and Failure Recovery

Related jobs catch up, stop, recalculate, and restart. Internal processing also stabilizes source
reads, so normal work does not simply continue unchanged during rebuilding. Measure acceptable
query/ingestion delays and downtime in a validation environment first.

Do not assume all stages roll back as one atomic transaction. State recovery after failure is best
effort; check actual data and V$ROLLUP. Restoring the original stopped state is not guaranteed
either. Before retrying, verify supported targets, remaining source data, and reaggregation scope.

A nonexistent tag can be a no-op when a valid rebuild target is otherwise prepared. A successful
response alone does not prove the intended tag was processed; compare actual results. Original
statistics cannot be reconstructed after the source data has been deleted.

## Clean Up

```sql
DROP ROLLUP ch6_rebuild_custom;
DROP TABLE ch6_rebuild_dst;
DROP TABLE ch6_rebuild CASCADE;
```

Remove Custom targets separately. If a general definition must change or the task is outside this
procedure's scope, prepare a supported new definition and data migration procedure. Do not
substitute arbitrary deletion of internal storage tables. For exact arguments, see the
[REBUILD Reference](../../reference/sql/syntax/rollup-rebuild-syntax/).
