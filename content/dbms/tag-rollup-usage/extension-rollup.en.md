---
type: docs
title: '6.7 Extension ROLLUP and FIRST/LAST'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/first-last-rollup/
---

<a id="rollup-extension"></a>

## EXTENSION versus Source FIRST/LAST

EXTENSION adds first/last values and associated timestamp information to ROLLUP. Using FIRST/LAST in
an ordinary source GROUP BY differs from querying FIRST/LAST from stored ROLLUP statistics. The
latter requires an applicable extension ROLLUP.

Time-only EXTENSION stores first/last values and timestamps; ordered EXTENSION also stores candidate keys.
MIN, MAX, SUM, COUNT, and SUMSQ, the sum of
squares, are also stored in general ROLLUP. For deriving variance and standard deviation from SUMSQ,
see [SUMSQ, Variance, and Standard Deviation](../query-syntax-rollup/#query-sumsq-stddev-rollup).

## Preparation and Ingestion

```sql
CREATE TAG TABLE ch6_ext (
    code VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    price DOUBLE
);
CREATE ROLLUP ch6_ext_first
  ON ch6_ext(price) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_ext_plain
  ON ch6_ext(price) INTERVAL 1 MIN;
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:10', 'YYYY-MM-DD HH24:MI:SS'), 105);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:20', 'YYYY-MM-DD HH24:MI:SS'), 99);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30', 'YYYY-MM-DD HH24:MI:SS'), 103);
EXEC TABLE_FLUSH(ch6_ext);
ALTER ROLLUP ch6_ext_first FORCE;
ALTER ROLLUP ch6_ext_plain FORCE;
```

## Comparing Source and OHLC Results

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_ext_first) */
       rollup('min', 1, time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;
```

Both queries return Open=100, High=105, Low=99, Close=103 in the 09:00 bucket. Time-only ROLLUP
FIRST/LAST use BASETIME as the first argument and the aggregate column as the second.
Use the composite-key definitions below when equal-timestamp rows require business ordering.

## General and Extension Candidates Together

General ROLLUP does not always take priority over extension ROLLUP. Registration order affects
candidates with the same conditions and interval. This example creates extension first, but
explicitly selects it when results must depend on a particular candidate. Where only extension is
applicable, it can be selected without a hint.

The following query intentionally fails because it forces general ROLLUP.

```sql
SELECT /*+ ROLLUP_TABLE(ch6_ext_plain) */
       rollup('min', 1, time) AS bucket, FIRST(time, price)
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket;
```

For automatic extension hierarchies, use `WITH ROLLUP (SEC) EXTENSION` in a separate table's CREATE
statement. Keep the extension attribute consistent when creating a hierarchy with FROM. For Custom
OHLCV reaggregation, see [Custom Examples](../custom-rollup/).

## Clean Up

```sql
DROP ROLLUP ch6_ext_plain;
DROP ROLLUP ch6_ext_first;
DROP TABLE ch6_ext;
```

<a id="composite-first-last"></a>

## Composite FIRST/LAST and ordered ROLLUP

> Composite sort keys require an engine build that includes this feature. Check support in the deployed product version.

Public ROWID sort keys are outside the support scope of this document.

### Example data

raw_tab is a source TAG without ROLLUP; rollup_tab is the source TAG for an ordered ROLLUP.
The examples require unused object names in a separate environment. Time is the first key.
Insertion order differs from business ordering, with three records per code/time at each minute's start.

```sql
CREATE TAG TABLE raw_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 102, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 105, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 103, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 101, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 104, 1, 1);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 202, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 205, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 203, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 201, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 204, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 302, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 305, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 303, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 301, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 304, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 402, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 405, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 403, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 401, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 404, 1, 1);

EXEC TABLE_FLUSH(raw_tab);

SELECT COUNT(*) AS row_count FROM raw_tab;
```

### Source queries and ties

With time alone, FIRST for A at 09:00 can select 101/102/103 and LAST can select 104/105.
Using (time, seq) narrows FIRST to 101/102 but does not resolve equal time/seq values.
The following query adds event_id to identify the candidates.

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS first_price,
       LAST(time, price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq), price) AS first_price,
       LAST((time, seq), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

| code | bucket | first_price | last_price |
|---|---|---:|---:|
| A | 2026-10-22 09:00:00 | 101 | 105 |
| A | 2026-10-22 09:01:00 | 201 | 205 |
| B | 2026-10-22 09:00:00 | 301 | 305 |
| B | 2026-10-22 09:01:00 | 401 | 405 |

### Per-key direction

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time ASC, seq ASC, event_id DESC), price) AS first_price,
       LAST((time ASC, seq ASC, event_id DESC), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

Using DESC only for event_id produces A=102/104, 202/204 and B=302/304, 402/404.

### Ordered ROLLUP definition and query

Store the same data in rollup_tab and query with keys matching the definition.
The ROLLUP_TABLE hint explicitly selects the stored ROLLUP in this example.

```sql
CREATE TAG TABLE rollup_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO rollup_tab SELECT * FROM raw_tab;
EXEC TABLE_FLUSH(rollup_tab);

CREATE ROLLUP price_1m_ordered
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id ASC;

ALTER ROLLUP price_1m_ordered FORCE;
```

```sql
SELECT /*+ ROLLUP_TABLE(price_1m_ordered) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

The result matches the source three-key ASC query. A DESC query requires a separate definition with matching directions.

```sql
CREATE ROLLUP price_1m_desc
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id DESC;

ALTER ROLLUP price_1m_desc FORCE;

SELECT /*+ ROLLUP_TABLE(price_1m_desc) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id DESC), price) AS first_price,
       LAST((time, seq, event_id DESC), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

### Parent ROLLUP

```sql
CREATE ROLLUP price_1h_ordered
    FROM price_1m_ordered
    INTERVAL 1 HOUR EXTENSION;

ALTER ROLLUP price_1h_ordered FORCE;

SELECT /*+ ROLLUP_TABLE(price_1h_ordered) */
       code, ROLLUP('hour', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

The parent inherits the source definition and original candidate keys. Hourly results are A=101/205 and B=301/405.

### Definition matching and changes

- The first key must be the source TAG's BASETIME; secondary keys must be supported ordinary data columns.
  TAG names, metadata columns, expressions, and table-qualified references cannot appear in the definition.
- Ordered EXTENSION supports numeric targets, not combinations with JSON_PATH/JSON_SUMMARY.
- Query key counts, columns, order, directions, and types must match. Forcing a different direction produces an error.
- Existing time-only ROLLUPs lack secondary keys. Reaggregate source data using a new definition; deleted source keys cannot be recovered.
- Stored candidate keys do not broaden access to original columns in ordinary WHERE, GROUP BY, or projections.
- Definitions exceeding sort-metadata or generated-SQL length limits are rejected at creation.
- Standard rejects RENAME of referenced key columns with ERR-02686, including stopped jobs and parent dependencies.
  Drop all related parent/child ROLLUPs before renaming the column and creating new definitions.
- This feature does not add automatic reaggregation after source UPDATE.
- All Cluster brokers and warehouses must run the same feature-supporting build.

### Delete example objects

```sql
DROP ROLLUP price_1h_ordered;
DROP ROLLUP price_1m_desc;
DROP ROLLUP price_1m_ordered;
DROP TABLE rollup_tab;
DROP TABLE raw_tab;
```
