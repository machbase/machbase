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

## Sum and Valid-Count Example

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

## OHLCV and a 1-Minute → 10-Minute Custom Hierarchy

This example uses separate objects. Store the first and last source observation timestamps to support
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
examples used. For source corrections and retry/completion checks for upper-level reaggregation,
follow [Control and Status](../ingestion-control-rollup/) and the REBUILD procedure.

<a id="composite-key-ohlc"></a>

## OHLC reaggregation with preserved composite keys

> Composite FIRST/LAST sort keys and ordered EXTENSION ROLLUPs are supported from Machbase 8.7.3.
> Edition-specific restrictions are described below.

Custom creation in this example is Standard-only. Reaggregating summary rows already stored
in an ordinary TAG is a separate SELECT operation and is also supported in Cluster.
Use the same source timestamp and secondary-key columns when merging those rows.

Standard Custom ROLLUP supports composite FIRST/LAST in its SELECT.
Do not append EXTENSION ORDER BY to a Custom definition. Store the selected price and its original
timestamp and DOUBLE key together to preserve ordering when merging partial results.
The following example uses separate objects.

### Source and destination schemas

```sql
CREATE TAG TABLE custom_ticks (
    code  VARCHAR(16) PRIMARY KEY,
    time  DATETIME BASETIME,
    price INTEGER,
    gvol  DOUBLE
);

CREATE TAG TABLE custom_ticks_1s (
    code        VARCHAR(16) PRIMARY KEY,
    time        DATETIME BASETIME,
    open_price  INTEGER,
    open_time   DATETIME,
    open_gvol   DOUBLE,
    close_price INTEGER,
    close_time  DATETIME,
    close_gvol  DOUBLE,
    high_price  INTEGER,
    low_price   INTEGER
);
```

### One-second aggregation

Match output column order to the destination schema. STOP before ingestion disables automatic processing; FORCE processes the input explicitly.

```sql
CREATE ROLLUP custom_ticks_rollup_1s
INTO (custom_ticks_1s) AS (
    SELECT code,
           DATE_TRUNC('second', time) AS time,
           FIRST((time, gvol), price) AS open_price,
           FIRST((time, gvol), time)  AS open_time,
           FIRST((time, gvol), gvol)  AS open_gvol,
           LAST((time, gvol), price)  AS close_price,
           LAST((time, gvol), time)   AS close_time,
           LAST((time, gvol), gvol)   AS close_gvol,
           MAX(price) AS high_price,
           MIN(price) AS low_price
      FROM custom_ticks
     GROUP BY code, time
) INTERVAL 1 SEC;

STOP ROLLUP custom_ticks_rollup_1s;
```

### Ingestion and aggregation

Three trades share each duplicate timestamp; gvol is an ordinary DOUBLE business key.
Values at 09:01:29.999 and 09:01:30 test timestamp precedence, not monotonically increasing production volumes.

```sql
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:00', 201, 2.5);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:00', 200, 1.25);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:00', 202, 3.75);

INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:50', 205, 5.5);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:50', 198, 4.25);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:50', 206, 6.75);

INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:29.999', 204, 0.25);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:30', 203, 999.5);

EXEC TABLE_FLUSH(custom_ticks);
EXEC ROLLUP_FORCE(custom_ticks_rollup_1s);
```

### Stored original keys

```sql
SELECT code, time, open_price, open_time, open_gvol,
       close_price, close_time, close_gvol, high_price, low_price
  FROM custom_ticks_1s
 ORDER BY code, time, open_time, close_time;
```

Destination time is the one-second bucket, while open_time/close_time preserve the selected source timestamps.
A source timestamp of 09:01:29.999 belongs to bucket 09:01:29 but retains its original candidate timestamp.
Multiple partial rows may share a bucket; stored row count is not bucket count.

### Thirty-second reaggregation

Use destination time to calculate buckets and (open_time, open_gvol) and
(close_time, close_gvol) to select candidates. These ordinary DATETIME keys need not be BASETIME.

```sql
SELECT code,
       DATE_BIN('sec', 30, time) AS bucket,
       FIRST((open_time, open_gvol), open_price) AS open_price,
       LAST((close_time, close_gvol), close_price) AS close_price,
       MAX(high_price) AS high_price,
       MIN(low_price) AS low_price
  FROM custom_ticks_1s
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

| code | bucket | open_price | close_price | high_price | low_price |
|---|---|---:|---:|---:|---:|
| AAPL | 2026-10-19 09:01:00 | 200 | 204 | 204 | 200 |
| AAPL | 2026-10-19 09:01:30 | 203 | 206 | 206 | 198 |

### Comparison with source aggregation

```sql
SELECT code,
       DATE_BIN('sec', 30, time) AS bucket,
       FIRST((time, gvol), price) AS open_price,
       LAST((time, gvol), price) AS close_price,
       MAX(price) AS high_price,
       MIN(price) AS low_price
  FROM custom_ticks
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT FIRST((time, gvol), price) AS open_price,
       LAST((time, gvol), price) AS close_price
  FROM custom_ticks;
```

Direct source aggregation and reaggregation of stored results must match. The full-minute open/close values are 200/206.

### Keys for further aggregation

When storing results for another aggregation level, carry the selected original keys using the same FIRST/LAST criteria.

```sql
SELECT code,
       DATE_BIN('sec', 30, time) AS bucket,
       FIRST((open_time, open_gvol), open_price) AS open_price,
       FIRST((open_time, open_gvol), open_time) AS open_time,
       FIRST((open_time, open_gvol), open_gvol) AS open_gvol,
       LAST((close_time, close_gvol), close_price) AS close_price,
       LAST((close_time, close_gvol), close_time) AS close_time,
       LAST((close_time, close_gvol), close_gvol) AS close_gvol,
       MAX(high_price) AS high_price,
       MIN(low_price) AS low_price
  FROM custom_ticks_1s
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

Using only bucket time in FIRST(time, open_price) cannot always reconstruct source ordering across partial summaries.
Existing concatenated-string summaries are not automatically converted to typed-key summaries.
Validate a new destination and job; historical migration requires retained source data and the ability to reaggregate.
Cluster Custom creation retains its existing ERR-02837 restriction.

### Delete example objects

Use START ROLLUP custom_ticks_rollup_1s to resume automatic processing. Delete example objects in the following order.

```sql
DROP ROLLUP custom_ticks_rollup_1s;
DROP TABLE custom_ticks_1s;
DROP TABLE custom_ticks;
```
