---
type: docs
title: '6.8 JSON SUMMARIZED ROLLUP'
weight: 80
toc: true
---

<a id="json-summarized-rollup"></a>

## JSON Path and Full-Document Aggregation

JSON path ROLLUP aggregates numeric values at a specified path. Full-document ROLLUP maintains
statistics for numeric paths in a JSON SUMMARIZED column. Do not treat missing paths, JSON null, SQL
NULL, and arrays as equivalent samples.

## Preparation

```sql
CREATE TAG TABLE ch6_json (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value JSON SUMMARIZED
);
CREATE ROLLUP ch6_json_metric ON ch6_json(value.metric) INTERVAL 1 MIN;
CREATE ROLLUP ch6_json_whole ON ch6_json(value) INTERVAL 1 MIN;
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:00'),
    '{"metric":10,"nested":{"x":2},"status":"OK","items":[1,2]}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:10'),
    '{"metric":20,"nested":{"x":4},"status":"WARN","items":[3,4]}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:20'),
    '{"metric":null,"status":false}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:30'), NULL);
EXEC TABLE_FLUSH(ch6_json);
ALTER ROLLUP ch6_json_metric FORCE;
ALTER ROLLUP ch6_json_whole FORCE;
```

## Comparing Path Aggregates

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       COUNT(JSON_EXTRACT_DOUBLE(value, '$.metric')),
       AVG(JSON_EXTRACT_DOUBLE(value, '$.metric'))
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_json_metric) */
       rollup('min', 1, time) AS bucket,
       COUNT(value.metric), AVG(value.metric)
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_json_metric) */
       rollup('min', 1, time) AS bucket, AVG(value->'$.metric')
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

metric has two valid numeric samples with average 15. Dot and arrow syntax express the same path.
Specifying an array element in a path is different from full-document aggregation automatically
expanding arrays. `value.items[0]."metric-id"` is an example path declaration, but first verify that
the JSON structure and numeric samples actually exist.

## Full-Document Aggregation and COUNT

```sql
SELECT COUNT(*) AS raw_rows, COUNT(value) AS raw_documents FROM ch6_json;

SELECT /*+ ROLLUP_TABLE(ch6_json_whole) */
       rollup('min', 1, time) AS bucket,
       COUNT(value), AVG(value), MIN(value), MAX(value), SUM(value)
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

Source COUNT(*) is 4 and COUNT(value) is 3. Full-document ROLLUP COUNT(value) sums stored document
aggregate counts. Currently those counts are built from source COUNT(*), so this bucket containing
both numeric-path documents and SQL NULL returns 4. Do not apply the ordinary source COUNT(value)
NULL-exclusion rule unchanged.

AVG returns metric=15 and nested.x=3, calculated from the valid numeric samples at each path.
Strings, booleans, JSON null, and arrays are excluded from numeric aggregation; nonnumeric paths can
appear as null or be omitted. Do not compare serialized JSON as fixed strings based on key order.
Test separate samples for documents with no numeric paths and intervals containing only SQL NULL.

JSON path and full-document aggregation use different candidate modes. Do not assume forcing a
ROLLUP from another mode with a hint gives equivalent results. Invalid JSON causes an ingestion
error.

## Clean Up

```sql
DROP ROLLUP ch6_json_whole;
DROP ROLLUP ch6_json_metric;
DROP TABLE ch6_json;
```
