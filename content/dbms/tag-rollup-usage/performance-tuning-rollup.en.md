---
type: docs
title: '6.11 ROLLUP Performance Tuning'
weight: 110
toc: true
---

<a id="tuning-rollup"></a>

## Compare Equivalent Results Before Costs

ROLLUP reduces the number of raw rows read. First verify equivalent tags, time ranges, NULL
handling, and aggregation criteria; then compare execution time, CPU, I/O, and memory. Small-example
timings do not guarantee production performance.

## Comparison Exercise

```sql
CREATE TAG TABLE ch6_perf (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_perf_ru ON ch6_perf(value) INTERVAL 1 MIN;
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_perf);
ALTER ROLLUP ch6_perf_ru FORCE;

SELECT DATE_TRUNC('minute', time) AS bucket,
       SUM(value), COUNT(value), AVG(value), MIN(value), MAX(value)
  FROM ch6_perf
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time < TO_DATE('2026-01-01 00:02:00')
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('min', 1, time) AS bucket,
       SUM(value), COUNT(value), AVG(value), MIN(value), MAX(value)
  FROM ch6_perf
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time < TO_DATE('2026-01-01 00:02:00')
 GROUP BY bucket ORDER BY bucket;

EXPLAIN SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_perf WHERE name = 'TEMP_01'
 GROUP BY bucket;
```

Both results show sum 30, count 2, average 15, minimum 10, maximum 20 at 00:00; and sum 30, count 1,
average 30, minimum 30, maximum 30 at 00:01. Inspect the source DATE_TRUNC execution plan the same
way.

## Measuring Production Load

| Metric | Conditions to record |
|---|---|
| Ingestion throughput | Tag count, input rate, row width, and concurrent writers |
| Query latency | Tag range, buckets, concurrent queries, and cold/warm cache state |
| Aggregation lag | Gap, job state, and processing time at each level |
| Storage | Source data, aggregates, indexes, compression, and replicas |
| Change impact | Ingestion/query costs before and after wakeup or hierarchy changes |

Shorter WAKEUP intervals can create partial aggregates more frequently within the same bucket.
Smaller aggregation buckets increase storage and reaggregation volume. Treat the two intervals as
distinct tuning parameters. Measure concurrent ingestion and queries as well as isolated runs.

## Meaning of Hierarchy Size

The following logical bucket counts assume one tag has data in every interval for 30 days.

| Query interval | Bucket count |
|---|---:|
| 1 second | 2,592,000 |
| 1 minute | 43,200 |
| 1 hour | 720 |
| 1 day | 30 |

These are not physical row counts. Measure actual storage with sample loading, including partial
aggregates, empty intervals, NULLs, and conditional filters. The coarsest candidate does not always
produce correct results; also check required resolution, origin, and candidate constraints.

Daily results reaggregate applicable HOUR/MIN/SEC statistics. A 24 HOUR ROLLUP is not recommended as
a substitute storage level for `rollup('day', 1, ...)`. Follow
[Query Candidate Rules](../query-syntax-rollup/) and actual EXPLAIN output.

## Distinguishing Lag from Mismatches

gap=0 means processing positions have caught up, not that source corrections have been reflected.
Before comparing performance, distinguish aggregation progress from historical correction state and
check matching definitions and filters. Do not use `rollup()` without an applicable ROLLUP to
benchmark source queries.

## Clean Up

```sql
DROP ROLLUP ch6_perf_ru;
DROP TABLE ch6_perf;
```

Choose the next adjustment using [Control and Status](../ingestion-control-rollup/),
[Hierarchy Design](../target-tag-table-design/), and
[Troubleshooting](../../troubleshooting/rollup/).
