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

> Composite FIRST/LAST sort keys and ordered EXTENSION ROLLUPs are supported from Machbase 8.7.3.
> Edition-specific restrictions are described below.

Standard 8.7.3 or later also supports an explicit ROWID secondary key. See the
[Standard-only ROWID example](#standard-rowid-key) below; Cluster does not support it.

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
- Standard also permits an explicit public ROWID secondary key as described below.
- Ordered EXTENSION supports numeric targets, not combinations with JSON_PATH/JSON_SUMMARY.
- Query key counts, columns, order, directions, and types must match the definition.
  An existing but incompatible ROLLUP named by `ROLLUP_TABLE` returns
  `ERR-02813: Invalid ROLLUP expression. (Token = ROLLUP ordering mismatch, Unit = 0)`.
  A nonexistent hint target returns `ERR-02025`. An earlier ROLLUP validation failure may take precedence.
  An unsupported key in a definition returns `ERR-02813` with `Token = EXTENSION ORDER BY`.
- Existing time-only ROLLUPs lack secondary keys. Reaggregate source data using a new definition; deleted source keys cannot be recovered.
- Stored candidate keys do not broaden access to original columns in ordinary WHERE, GROUP BY, or projections.
- An ordered ROLLUP generates an internal aggregation SQL that repeats the full key list for each key.
  If this SQL exceeds the internal length limit, creation fails with `ERR-02813`
  (`Token = ordering query exceeds supported size, Unit = 0`). The limit is reached sooner with more
  keys or longer column names; for example, a 10-key definition made of `time` and nine `seq` keys
  is rejected. Specify only the keys needed to break ties. If the sort definition itself exceeds the
  metadata length limit, the token is `EXTENSION ORDER BY`.
- Standard rejects RENAME of referenced key columns with ERR-02686, including stopped jobs and parent dependencies.
  Drop all related parent/child ROLLUPs before renaming the column and creating new definitions.
- This feature does not add automatic reaggregation after source UPDATE.
- All Cluster brokers and warehouses must run the same feature-supporting build.

### Existing EXT and automatic selection {#ordered-rollup-selection}

For ordinary aggregates that can use either kind, candidates without WHERE conditions are
considered first. Within the same condition category, nullable value columns prefer existing
ROLLUPs without a sort definition. For a confirmed NOT NULL aggregate value column, existing
and ordered candidates are treated equally. `COUNT(*)` does not infer a value column's NOT NULL
property and retains the existing-candidate preference. Eligible periods must divide the query
period; the largest eligible period wins, followed by registration order for equal periods.
Composite FIRST/LAST can use only an ordered definition with matching keys and directions.

Time-only EXT and ordered ROLLUPs handle NULL buckets differently. For a nullable price with
NULL then 10 in one minute, and 20 in the next minute, an existing EXT may omit the first
minute and produce SUM/COUNT(price) of 20/1; an ordered ROLLUP preserves that bucket and can
produce 30/2. The aggregate list, period, hint, and removal of existing objects can change the
eligible candidate. Recheck SUM/COUNT as well as FIRST/LAST when migrating.

A stored ROLLUP query using the legacy `FIRST(time, price)` / `LAST(time, price)` needs an
applicable existing time-only EXT; it cannot use an ordered ROLLUP instead. Keep the existing
EXT if these queries must continue. With only ordered ROLLUPs available, such a query returns
`ERR-02685` (`There are no applicable ROLLUP tables.`), while ordinary aggregates such as SUM and
COUNT can use the ordered ROLLUP. A conditional candidate still represents filtered input.

### Inspecting and rebuilding definitions

`V$ROLLUP.EXT_TYPE = 1` identifies EXTENSION but does not distinguish ordered from time-only
EXT or show its keys. Retain the CREATE ROLLUP SQL to manage the definition.
`WITH ROLLUP ... EXTENSION` does not accept ORDER BY; create ordered objects with CREATE ROLLUP.
For a FROM hierarchy, omitted ORDER BY inherits the lower definition. An explicit definition
must match the lower keys and directions.

Do not assume ROLLUP_REBUILD rebuilds arbitrary ordered objects. Its supported targets are
limited to the documented automatic hierarchy and Custom paths. After correcting source data,
drop dependent upper objects before lower ones, recreate the ordered hierarchy from retained
source data, and verify the results. Dropping objects cannot recover deleted source keys.

### Older binaries and rollback {#ordered-rollup-compatibility}

Opening or MOUNTing a database containing ordered ROLLUPs with a binary that lacks this
feature is unsupported. This feature does not raise the metadata version; an older binary
with the same metadata version may pass the version check and interpret an ordered object as
an existing EXT. To roll back, restore a backup taken before introducing ordered ROLLUPs and
follow the target version's recovery procedure. Dropping the ordered objects alone does not
guarantee compatibility of all catalogs and files.

When upgrading a database with ordered ROLLUPs created in 8.5.13 to 8.7, use 8.7.3 or later.
Releases 8.7.0 through 8.7.2 lack this feature and may interpret ordered objects as existing EXTs,
as described above.

### Standard public ROWID as a secondary key {#standard-rowid-key}

This optional example is for Standard 8.7.3 or later, using the `rollup_tab` created above.
Skip this section in Cluster. An explicit ROWID can be the second or a later key, including
`(time, seq, ROWID)`. ROLLUPs preserve the selected source row's ROWID, not the summary row's ID.

```sql
CREATE ROLLUP price_1m_rowid
    ON rollup_tab(price)
    INTERVAL 1 MIN EXTENSION ORDER BY time, ROWID;
ALTER ROLLUP price_1m_rowid FORCE;

SELECT code,
       FIRST((time, ROWID), price) AS first_price,
       LAST((time, ROWID), price) AS last_price
  FROM rollup_tab
 GROUP BY code
 ORDER BY code;

SELECT /*+ ROLLUP_TABLE(price_1m_rowid) */
       code, ROLLUP('hour', 1, time) AS bucket,
       FIRST((time, ROWID), price) AS first_price,
       LAST((time, ROWID), price) AS last_price
  FROM rollup_tab
 GROUP BY code, bucket
 ORDER BY code, bucket;

DROP ROLLUP price_1m_rowid;
```

For each code in this one-hour data set, the raw and ROLLUP queries must agree on FIRST/LAST.
Their values need not match the earlier business-sequence example: ROWID identifies a stored row,
not a business sequence or table-wide insertion order. Reloading a backup or recreating a table
does not guarantee the same identifiers or order. ROWID is never added implicitly.

Existing ROWID restrictions remain. A ROLLUP query cannot use ROWID directly in GROUP BY or
ORDER BY, or wrap it in BITAND to create another key. Use it as an explicit composite
FIRST/LAST secondary key; ordering by that aggregate, its alias, or its SELECT-list position
is allowed. Cluster rejects public ROWID keys (`ERR-02056` for this SELECT form,
`ERR-02813` with `Token = EXTENSION ORDER BY` for the definition).

### Delete example objects

```sql
DROP ROLLUP price_1h_ordered;
DROP ROLLUP price_1m_desc;
DROP ROLLUP price_1m_ordered;
DROP TABLE rollup_tab;
DROP TABLE raw_tab;
```
