---
title: 'Custom Rollup: User-Defined Aggregation'
type: docs
weight: 62
toc: true
---

## Overview

Custom Rollup executes a user-defined `SELECT` aggregation query periodically and appends the result into a target TAG table.

It is useful for multi-column aggregation, condition-based aggregation, and hierarchical rollup pipelines.

## Differences from Standard Rollup

| Category | Standard Rollup | Custom Rollup |
|---|---|---|
| Create syntax | `CREATE ROLLUP ... ON table(column)` | `CREATE ROLLUP ... INTO (...) AS (SELECT ...)` |
| Aggregation logic | Engine-defined | User-defined `SELECT` |
| Destination | Internal rollup table | User-created TAG table |
| WHERE location | External `INTERVAL ... WHERE ...` | Internal `SELECT ... WHERE ...` |
| Query pattern | `rollup()` hint path | Query destination table with re-aggregation |
| Metadata type | `v$rollup.ext_type = 0/1` | `v$rollup.ext_type = 2` |

## Execution Model and Re-Aggregation

Custom Rollup stores data as incremental `INSERT INTO <dest> SELECT ...` results.

Multiple partial rows can exist for the same time bucket. Because of this, final queries should re-aggregate by the bucket key.

```sql
SELECT code,
       time,
       SUM(sum_price) / SUM(cnt) AS avg_price
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## Syntax

### Create Custom Rollup

```sql
CREATE ROLLUP [IF NOT EXISTS] <rollup_name>
INTO (<dest_tag_table>)
AS (
  SELECT ...
  FROM <source_tag_table>
  [WHERE ...]
  GROUP BY ...
)
INTERVAL <n> (SEC | MIN | HOUR)
[WAKEUP INTERVAL <m> (SEC | MIN | HOUR)];
```

### Control Commands

```sql
ALTER ROLLUP <rollup_name> START;
ALTER ROLLUP <rollup_name> STOP;
ALTER ROLLUP <rollup_name> WAKEUP;
ALTER ROLLUP <rollup_name> FORCE;
DROP ROLLUP <rollup_name>;
```

Note: Rollup worker threads are started automatically after creation. Calling `START` immediately can return an already-started error.

## Validation Rules and Constraints

### Source and Destination Tables

- Only one TAG table is allowed as the source.
- The destination must be a pre-created TAG table.
- Destination `DROP TABLE` is blocked while the rollup exists.

### SELECT Constraints

- The query inside `AS (...)` must be a valid `SELECT`.
- Exactly one table is allowed in `FROM`.
- `JOIN`, `FROM` subqueries, and `ON/USING` are not allowed.
- SELECT text length is limited (internal 1024-based limit).
- Result column count/types must be compatible with the destination table.

### WHERE Constraints

- Internal `WHERE` in `SELECT` is allowed.
- Direct filtering on the source BASETIME column in `WHERE` is rejected.
- External `INTERVAL ... WHERE ...` is not allowed for Custom Rollup syntax.

### Interval Constraints

- `INTERVAL` must be positive.
- If `WAKEUP INTERVAL` is omitted, it defaults to `INTERVAL`.
- `WAKEUP INTERVAL` must be `<= INTERVAL` and must divide `INTERVAL` exactly.

### DATE_BIN Origin Guidance

`DATE_BIN` origin must be a valid DATETIME value. Boundary origins may fail depending on environment/timezone behavior, so use a safe origin value.

## Basic Example

### 1) Source and Destination Tables

```sql
CREATE TAG TABLE stock_tick (
  code      VARCHAR(20) PRIMARY KEY,
  time      DATETIME BASETIME,
  price     DOUBLE,
  volume    DOUBLE,
  bid_price DOUBLE,
  ask_price DOUBLE
);

CREATE TAG TABLE stock_rollup_1m (
  code       VARCHAR(20) PRIMARY KEY,
  time       DATETIME BASETIME,
  sum_price  DOUBLE,
  sum_volume DOUBLE,
  sum_bid    DOUBLE,
  sum_ask    DOUBLE,
  cnt        INTEGER
);
```

### 2) Create Custom Rollup

```sql
CREATE ROLLUP rollup_stock_1m
INTO (stock_rollup_1m)
AS (
  SELECT code,
         DATE_TRUNC('minute', time) AS time,
         SUM(price)                 AS sum_price,
         SUM(volume)                AS sum_volume,
         SUM(bid_price)             AS sum_bid,
         SUM(ask_price)             AS sum_ask,
         COUNT(*)                   AS cnt
    FROM stock_tick
   GROUP BY code, time
)
INTERVAL 1 MIN;
```

### 3) Re-Aggregation Query

```sql
SELECT code,
       time,
       SUM(sum_price)  / SUM(cnt) AS avg_price,
       SUM(sum_volume)            AS total_volume,
       SUM(sum_bid)    / SUM(cnt) AS avg_bid,
       SUM(sum_ask)    / SUM(cnt) AS avg_ask
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## OHLCV Pattern (FIRST/LAST)

When using `FIRST/LAST`, keeping helper time columns (`firsttime`, `lasttime`) improves correctness during re-aggregation.

```sql
SELECT code,
       time,
       FIRST(firsttime, open) AS open,
       MAX(high)              AS high,
       MIN(low)               AS low,
       LAST(lasttime, close)  AS close,
       SUM(volume)            AS volume,
       SUM(cnt)               AS cnt
  FROM stock_candle_1m
 GROUP BY code, time
 ORDER BY code, time;
```

## Hierarchical Pipeline Example (1m -> 10m)

A Custom Rollup destination table can be used as the source of another rollup stage.

```sql
CREATE ROLLUP rollup_stock_candle_10m
INTO (stock_candle_10m)
AS (
  SELECT code,
         DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
         MIN(firsttime)         AS firsttime,
         MAX(lasttime)          AS lasttime,
         FIRST(firsttime, open) AS open,
         MAX(high)              AS high,
         MIN(low)               AS low,
         LAST(lasttime, close)  AS close,
         SUM(volume)            AS volume,
         SUM(cnt)               AS cnt
    FROM stock_candle_1m
   GROUP BY code, time
)
INTERVAL 10 MIN;
```

## Metadata Check

```sql
SELECT rollup_name,
       rollup_table,
       source_table,
       ext_type,
       enabled,
       interval_time,
       wakeup_interval,
       predicate
  FROM v$rollup
 WHERE rollup_name = 'ROLLUP_STOCK_1M';
```

- `ext_type = 2`: Custom Rollup
- `rollup_table`: destination TAG table for a Custom Rollup
- `interval_time` and `wakeup_interval`: interval values in milliseconds
- `predicate`: Custom `SELECT` text

## Operational Notes

- Destination `DROP TABLE` is blocked while the rollup exists.
- If corrected source data requires rebuilding destination buckets, follow [Rollup Rebuild Guide](../rollup-rebuild/).
- Recommended drop order:

```sql
ALTER ROLLUP <name> STOP;
DROP ROLLUP <name>;
DROP TABLE <dest_table>;
DROP TABLE <source_table>;
```

- `DROP TAG TABLE ... CASCADE` removes dependent rollups.
- Custom Rollup destination tables are not auto-dropped and should be removed separately when needed.

## Best Practices

- Standardize result queries as re-aggregation queries.
- Keep `firsttime`/`lasttime` helper columns for FIRST/LAST patterns.
- For destination schema changes, stop/drop/recreate the rollup.
- After correcting anomalous data, rebuild by bucket using delete followed by insert. In rollup-on-rollup pipelines, always rebuild from lower stages first.
- Configure `WAKEUP INTERVAL` explicitly to balance latency and load.

<a id="composite-key-ohlc"></a>

## OHLC reaggregation with preserved composite keys

> Composite FIRST/LAST sort keys and ordered EXTENSION ROLLUPs are supported from Machbase 8.5.13.

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
