---
type: docs
title: '6.2 Target TAG Table Design for ROLLUP'
weight: 20
toc: true
---

<a id="design-rollup-on"></a>

## ON and FROM

`ON source(column)` aggregates a column of a source time-axis TAG table. `FROM rollup_name` combines
statistics from an existing general/extension ROLLUP into larger intervals. A Custom target is also
a TAG table, but the next Custom stage uses INTO...AS with a SELECT from that target TAG.

## Hierarchy Exercise

```sql
CREATE TAG TABLE ch6_design (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_design_sec ON ch6_design(value) INTERVAL 1 SEC;
CREATE ROLLUP ch6_design_min FROM ch6_design_sec INTERVAL 1 MIN;
CREATE ROLLUP ch6_design_hour FROM ch6_design_min INTERVAL 1 HOUR;
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_design);
ALTER ROLLUP ch6_design_sec FORCE;
ALTER ROLLUP ch6_design_min FORCE;
ALTER ROLLUP ch6_design_hour FORCE;

SELECT name, rollup('hour', 1, time) AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_design
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01 has sum 60, count 3, and average 20; TEMP_02 has 100, 1, and 100. FORCE lower levels first
so upper levels can process newly generated lower-level results.

### Hierarchy Constraints

- The upper interval must be larger than the source interval and an integer multiple of it. Equal intervals are not allowed.
- FROM cannot convert general ROLLUP to extension ROLLUP or vice versa. Keep EXTENSION consistent throughout the hierarchy.
- JSON path/full-document modes must also match the source.
- Coarse statistics cannot reconstruct source detail finer than the smallest supported query interval.

Each creation example below intentionally fails.

```sql
CREATE ROLLUP ch6_design_bad_same FROM ch6_design_min INTERVAL 1 MIN;
CREATE ROLLUP ch6_design_bad_divisor FROM ch6_design_min INTERVAL 90 SEC;
CREATE ROLLUP ch6_design_bad_ext FROM ch6_design_sec INTERVAL 1 MIN EXTENSION;
```

## Choosing Intervals and Storage Capacity

Assuming every tag has values in every interval, the approximate logical bucket count is
`(retention time / bucket interval) × tag count`. Retaining 1-second buckets for 10,000 tags for 365
days gives about 315.4 billion buckets. Actual row counts depend on partial aggregates, empty
intervals, and column counts. Measure disk usage including compression and storage overhead.

If second-level observations are queried only by minute, assess whether every second-level hierarchy
is needed. Creation intervals use SEC/MIN/HOUR; DAY/WEEK/MONTH/YEAR are query bucket units. In
particular, do not assume a 24 HOUR storage interval works directly for daily queries; check
[Candidate Selection Rules](../query-syntax-rollup/).

A new ROLLUP initially aggregates existing data still present in its source. Check initial workload
and gaps. FORCE does not rewind processing after source corrections. Follow
[REBUILD Support Scope](../rollup-rebuild/).

## Clean Up

```sql
DROP ROLLUP ch6_design_hour;
DROP ROLLUP ch6_design_min;
DROP ROLLUP ch6_design_sec;
DROP TABLE ch6_design;
```
