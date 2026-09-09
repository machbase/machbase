---
type: docs
title: '6.6 Custom ROLLUP'
weight: 60
toc: true
---

<span class="badge-since">Standard Edition only</span>

<a id="original-85-rollup-custom"></a>
<a id="custom-rollup"></a>

## Custom and General ROLLUP

Custom ROLLUP appends incremental SELECT aggregation results to a precreated target TAG table.
General ROLLUP reads internal statistics through `rollup()`; Custom instead requires querying the
target TAG directly and merging partial aggregates again. It cannot be created in Cluster Edition.

```text
CREATE ROLLUP [IF NOT EXISTS] name
  INTO (destination_tag)
  AS (SELECT ... FROM source_tag [WHERE ...] GROUP BY ...)
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)];
```

The source must be one time-axis TAG table. JOIN and FROM subqueries are unsupported. The target
must be a precreated TAG compatible with the SELECT column order and types. WHERE inside SELECT is
allowed, but direct BASETIME predicates are not. Do not append an external WHERE after INTERVAL as
in general ROLLUP.

Match the creation interval to the time bucket calculated by SELECT. Because the job processes only
new input, one bucket can contain several result rows. Do not interpret row count as bucket count.

## 1. Sum and Valid-Count Exercise

```sql
CREATE TAG TABLE ch6_custom_src (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE ch6_custom_dst (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME,
    sum_value DOUBLE, valid_count LONG, total_count LONG
);
CREATE ROLLUP ch6_custom_ru INTO (ch6_custom_dst)
AS (
    SELECT name, DATE_TRUNC('minute', time) AS time,
           SUM(value), COUNT(value), COUNT(*)
      FROM ch6_custom_src
     GROUP BY name, time
) INTERVAL 1 MIN;
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:05', 'YYYY-MM-DD HH24:MI:SS'), 10);
EXEC TABLE_FLUSH(ch6_custom_src);
ALTER ROLLUP ch6_custom_ru FORCE;
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:10', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:15', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:20', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:25', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:35', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:40', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:45', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:55', 'YYYY-MM-DD HH24:MI:SS'), NULL);
EXEC TABLE_FLUSH(ch6_custom_src);
ALTER ROLLUP ch6_custom_ru FORCE;

SELECT name, DATE_TRUNC('minute', time) AS bucket,
       SUM(value), COUNT(value), COUNT(*), AVG(value)
  FROM ch6_custom_src
 GROUP BY name, bucket ORDER BY name, bucket;

SELECT name, time, SUM(sum_value) AS sum_value,
       SUM(valid_count) AS valid_count, SUM(total_count) AS total_count,
       CASE WHEN SUM(valid_count) = 0 THEN NULL
            ELSE SUM(sum_value) / SUM(valid_count) END AS avg_value
  FROM ch6_custom_dst
 GROUP BY name, time ORDER BY name, time;
```

The bucket has sum 180, 10 valid values, 11 total rows, and average 18. This differs from 15, the
simple average of partial averages 10 and 20. Use COUNT(value) so NULL is excluded from the average
denominator, and retain COUNT(*) separately for total rows including NULL. Define a result policy
that avoids division by zero for all-NULL buckets.

### Sample Ratio and Time-Based Availability

Matching sample count divided by total sample count is a sample ratio. Interpreting it as time-based
availability requires accounting for observation intervals, missing data, and state duration. Sum
the numerator and denominator separately; do not average partial ratios.

## 2. OHLCV and a 1-Minute → 10-Minute Custom Hierarchy

This is a separate exercise. Store the first and last source observation timestamps to support
FIRST/LAST reaggregation.

```sql
CREATE TAG TABLE ch6_ticks (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    price DOUBLE, volume DOUBLE
);
CREATE TAG TABLE ch6_candle_min (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    open_price DOUBLE, high_price DOUBLE, low_price DOUBLE, close_price DOUBLE,
    volume DOUBLE, cnt LONG, firsttime DATETIME, lasttime DATETIME
);
CREATE TAG TABLE ch6_candle_10m (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    open_price DOUBLE, high_price DOUBLE, low_price DOUBLE, close_price DOUBLE,
    volume DOUBLE, cnt LONG, firsttime DATETIME, lasttime DATETIME
);
CREATE ROLLUP ch6_candle_ru_min INTO (ch6_candle_min)
AS (
    SELECT code, DATE_TRUNC('minute', time) AS time,
           FIRST(time, price), MAX(price), MIN(price), LAST(time, price),
           SUM(volume), COUNT(*), MIN(time), MAX(time)
      FROM ch6_ticks
     GROUP BY code, time
) INTERVAL 1 MIN;

CREATE ROLLUP ch6_candle_ru_10m INTO (ch6_candle_10m)
AS (
    SELECT code, DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
           FIRST(firsttime, open_price), MAX(high_price),
           MIN(low_price), LAST(lasttime, close_price),
           SUM(volume), SUM(cnt), MIN(firsttime), MAX(lasttime)
      FROM ch6_candle_min
     GROUP BY code, time
) INTERVAL 10 MIN;

INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00'), 100, 2);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30'), 105, 3);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:01:00'), 103, 1);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:01:30'), 99, 4);
EXEC TABLE_FLUSH(ch6_ticks);
ALTER ROLLUP ch6_candle_ru_min FORCE;
EXEC TABLE_FLUSH(ch6_candle_min);
ALTER ROLLUP ch6_candle_ru_10m FORCE;

SELECT code, time,
       FIRST(firsttime, open_price), MAX(high_price),
       MIN(low_price), LAST(lasttime, close_price), SUM(volume), SUM(cnt)
  FROM ch6_candle_10m
 GROUP BY code, time ORDER BY code, time;
```

The 09:00 10-minute bucket has Open=100, High=105, Low=99, Close=99, volume=10, and cnt=4. NULL
prices or volumes require separate rules and tests for choosing row timestamps and values. If
multiple trades share a timestamp but have business ordering, design an additional identifier.

This 10-minute Custom example demonstrates creation and querying. Do not assume its interval is
supported by current Custom time-range REBUILD processing. Check
[REBUILD Limitations](../rollup-rebuild/).

## Status and Cleanup

Jobs start automatically after creation, so do not immediately repeat START. Call STOP/START and
FORCE according to job state. Dropping a target TAG is blocked while its job exists.

```sql
SELECT DISTINCT ROLLUP_NAME, ROLLUP_TABLE, ROOT_TABLE, EXT_TYPE,
       INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CUSTOM_RU';

DROP ROLLUP ch6_candle_ru_10m;
DROP ROLLUP ch6_candle_ru_min;
DROP TABLE ch6_candle_10m;
DROP TABLE ch6_candle_min;
DROP TABLE ch6_ticks;
DROP ROLLUP ch6_custom_ru;
DROP TABLE ch6_custom_dst;
DROP TABLE ch6_custom_src;
```

EXT_TYPE=2 indicates Custom; PREDICATE records the SELECT body. Clean up only objects from the
exercises you ran. For source corrections and retry/completion checks for upper-level reaggregation,
follow [Control and Status](../ingestion-control-rollup/) and the REBUILD procedure.
