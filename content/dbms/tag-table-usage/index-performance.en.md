---
type: docs
title: '5.6 Indexes and Performance'
weight: 60
toc: true
---
Start TAG queries by limiting tag names and axis ranges. Choose additional indexes only
after measuring actual predicates and execution plans.

<a id="index-tuning-tag"></a>
<a id="original-85-tag-indexes"></a>

## Basic Query Paths

TAG tables automatically manage structures for queries by `PRIMARY KEY` tag
name and `BASETIME` or `BASEDISTANCE`. Applications should not depend on
generated system-object names or storage stages.

| Query condition | Tuning direction |
| --- | --- |
| Axis range for one tag | Specify both tag name and axis range |
| Same time range for multiple tags | Limit time first and manage target tag count |
| Metadata attributes | Define TAG `METADATA` columns |
| Repeated time aggregation | Consider ROLLUP |
| Value-driven queries | Validate secondary value indexes with execution plans |

Broad queries without tag or axis limits read more data. Check `EXPLAIN` and
execution time with actual volumes instead of assuming constant speed.

## METADATA Columns

Use `METADATA` for attributes defined once per tag, such as location or device
type. Ordinary scalar METADATA columns have automatic search indexes. Raw
JSON columns do not; index required JSON paths explicitly. Numeric ARRAY
metadata supports neither automatic nor explicit indexes. See [TAG Metadata](../tag-metadata/).

Putting time-series values or frequently changing status in METADATA obscures
update semantics. Depending on the value, consider TAG DATA columns, LOOKUP,
VOLATILE, or TRANSACTION tables (Standard Edition only).

<a id="값-컬럼-secondary-index"></a>

## Secondary Indexes on Value Columns

For frequent value predicates, consider `INDEX_TYPE TAG` secondary indexes.
They increase ingestion and storage costs; compare representative queries
before and after creation.

This example uses isolated names to create value and JSON path indexes,
checks execution plans, and removes all objects. The small sample validates
syntax and results, not performance benefits. Run in a separate environment
without name conflicts.

```sql
CREATE TAG TABLE ch5_index_tag (
    name    VARCHAR(32) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   DOUBLE,
    payload JSON
) METADATA (
    location VARCHAR(64)
);

INSERT INTO ch5_index_tag METADATA VALUES ('TEMP-01', 'LINE-A');
INSERT INTO ch5_index_tag METADATA VALUES ('TEMP-02', 'LINE-B');
INSERT INTO ch5_index_tag VALUES
    ('TEMP-01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
     10.0, '{"state":"normal"}');
INSERT INTO ch5_index_tag VALUES
    ('TEMP-01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'),
     90.0, '{"state":"alarm"}');
INSERT INTO ch5_index_tag VALUES
    ('TEMP-02', TO_DATE('2026-01-01 00:02:00', 'YYYY-MM-DD HH24:MI:SS'),
     95.0, '{"state":"alarm"}');

CREATE INDEX idx_ch5_index_tag_value
    ON ch5_index_tag (value) INDEX_TYPE TAG;
CREATE INDEX idx_ch5_index_tag_json
    ON ch5_index_tag (payload->'$.state');

EXPLAIN SELECT name, time, value
  FROM ch5_index_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2026-01-01', 'YYYY-MM-DD')
                AND TO_DATE('2026-01-02', 'YYYY-MM-DD')
   AND value > 80.0;

SELECT name, value FROM ch5_index_tag
 WHERE location = 'LINE-A' AND value > 80.0
 ORDER BY name, time;
SELECT name, value FROM ch5_index_tag
 WHERE payload->'$.state' = 'alarm'
 ORDER BY name, time;

DROP INDEX idx_ch5_index_tag_json;
DROP INDEX idx_ch5_index_tag_value;
DROP TABLE ch5_index_tag;
```

The first SELECT returns TEMP-01 with 90.0; the second returns TEMP-01 with
90.0 and TEMP-02 with 95.0. Verify identical results before and after indexing.
With production-scale data, compare ingestion cost and index size as well as query time.

Match JSON path result types to comparison value types, and use `EXPLAIN`
to check whether the intended path uses an index.

## Avoid Inapplicable Tuning

- Do not create separate indexes on TAG axis columns.
- Do not apply the LOG `MINMAX_CACHE_SIZE` setting to TAG value columns.
- Consider ROLLUP for repeated broad-period aggregation instead of relying
  only on secondary indexes.

See the [SQL Syntax Reference](/dbms/reference/sql/syntax/) for index syntax
and [Query Tuning](/dbms/performance-tuning/performance-query-tuning/) for
measurement and tuning procedures.
