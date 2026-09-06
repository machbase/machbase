---
title: '5.6 Indexes and Performance'
weight: 60
toc: true
---

Start TAG queries with tag identity and axis bounds. Choose additional indexes by comparing the
actual access plan and workload rather than assuming that every predicate needs an index.

<a id="index-tuning-tag"></a>
<a id="original-85-tag-indexes"></a>

## Built-In Access and Metadata

TAG manages access by name and time/distance axis. Applications should not depend on generated
storage object names. Metadata attributes select tags; DATA columns filter observations.
Ordinary scalar metadata columns have automatic search indexes. JSON metadata needs indexes
on relevant paths; numeric ARRAY metadata supports neither automatic nor explicit indexing.

Frequent per-observation changes belong in DATA or an appropriate state table rather than being
silently treated as historical metadata snapshots.

## Value and JSON Path Indexes

The following independent fixture inserts actual values, creates indexes, inspects a plan, queries
results, and removes its objects. A three-row sample validates syntax and semantics, not speed.

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


The first SELECT returns TEMP-01 with value 90.0. The second returns TEMP-01/90.0 and TEMP-02/95.0.
Keep JSON path result types and comparison literals compatible. Verify results before and after
index creation; then measure query time, ingestion overhead, and index size at representative scale.

Do not create another axis index, apply LOG MINMAX_CACHE_SIZE to TAG values, or expect a secondary
index alone to replace repeated long-range ROLLUP aggregation. See
[Metadata](../tag-metadata/), [Index SQL](../../reference/sql/syntax-dictionary-sql/index-syntax/),
and [Query Tuning](../../performance-tuning/performance-query-tuning/).
