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

EXTENSION adds only first/last values and timestamps. MIN, MAX, SUM, COUNT, and SUMSQ, the sum of
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

Both queries return Open=100, High=105, Low=99, Close=103 in the 09:00 bucket. ROLLUP FIRST/LAST use
BASETIME as the first argument and the aggregate column as the second. Design separately for
equal-timestamp values when additional business ordering is required.

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
