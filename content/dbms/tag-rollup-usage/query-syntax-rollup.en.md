---
type: docs
title: '6.4 ROLLUP Query Syntax'
weight: 40
toc: true
aliases:
  - /dbms/tag-rollup-usage/week-month-year-timezone-rollup/
---

<a id="query-syntax-rollup"></a>

## Explicit ROLLUP Queries

```text
rollup(time_unit, period, basetime_column [, origin])
```

| Argument | Requirements |
|---|---|
| time_unit | SECOND/SEC, MINUTE/MIN, HOUR, DAY, WEEK, MONTH, YEAR; case-insensitive |
| period | Positive integer literal; not a column or parameter placeholder |
| basetime_column | BASETIME column of the source time-axis TAG |
| origin | If omitted, uses the default reference point adjusted for the time-zone offset; explicit values have unit-specific restrictions |

The result is a DATETIME bucket. Finer detail than the minimum stored aggregation interval cannot be
reconstructed. If no applicable ROLLUP exists, the query fails instead of automatically falling back
to a raw scan. Write a separate DATE_TRUNC/DATE_BIN + GROUP BY query for source aggregation.

## Preparation and Basic Queries

```sql
CREATE TAG TABLE ch6_query (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_query_sec ON ch6_query(value) INTERVAL 1 SEC;
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_query);
ALTER ROLLUP ch6_query_sec FORCE;

SELECT name, rollup('min', 1, time) AS bucket,
       COUNT(value), SUM(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_query
 WHERE time >= TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 00:02:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01 at 00:00 has COUNT=2, SUM=30, AVG=15; at 00:01 it has 1, 30, 30. TEMP_02 at 00:00 has 1,
100, 100. If SELECT returns name, also include name in GROUP BY. Omitting name combines tags; do not
mix sensors with different units.

## Candidate Selection and Hints

1. If a ROLLUP_TABLE hint is present, check the named candidate for compatibility.
2. Automatic selection finds candidates matching the aggregate column, JSON path, mode, and requested interval.
3. Search unconditional candidates first; if none exist, include conditional candidates.
4. Select the largest applicable interval. For equal intervals, retain the first registered candidate.

Do not assume general ROLLUP always takes priority over extension ROLLUP. If only conditional
ROLLUPs exist, filtered data can be selected automatically. Check which sample set the result
represents. Specify a hint when a particular aggregate must be used.

```sql
SELECT /*+ ROLLUP_TABLE(ch6_query_sec) */
       rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

### Stored Candidate Intervals and Query Buckets

Current candidate-interval validation calculates SEC requests as period seconds and MIN requests as
period minutes. HOUR and DAY/WEEK/MONTH/YEAR requests are checked against period hours during
candidate selection. Selected statistics are then merged into the requested calendar/time buckets.

Do not assume a 24 HOUR ROLLUP automatically serves `rollup('day', 1, time)`. That request considers
HOUR/MIN/SEC candidates compatible with a 1-hour basis. Distinguish creation INTERVAL from result
buckets and inspect the actual execution plan.

## Aggregate Functions and Samples

General numeric ROLLUP supports MIN, MAX, SUM, COUNT, AVG, and SUMSQ. FIRST/LAST in a ROLLUP query
require EXTENSION. Custom results are stored in ordinary TAG tables; use the sum/count rules in
[Custom Reaggregation](../custom-rollup/). COUNT for full-document JSON aggregation is covered
separately in [JSON](../json-summarized-rollup/).

<a id="query-sumsq-stddev-rollup"></a>

### SUMSQ, Variance, and Standard Deviation

ROLLUP queries do not directly support STDDEV, STDDEV_POP, VARIANCE, or VAR_POP. Using them in a
`rollup()` query causes
`ERR-02816: Only rollup column with aggregate function can be referenced in ROLLUP SELECT query.`
Variances and standard deviations cannot be added across intervals. Averaging two interval standard
deviations does not give the standard deviation of the combined interval.

Instead, ROLLUP stores SUMSQ, the sum of squared values, alongside COUNT and SUM. All three are
additive and remain valid when merged into buckets larger than the storage interval. Variance and
standard deviation can then be calculated at query time. SUMSQ is included in both general and
EXTENSION ROLLUP.

| Value | Formula |
|---|---|
| Population variance | `SUMSQ/N - (SUM/N)^2` |
| Population standard deviation | Square root of population variance |
| Sample variance | `(SUMSQ - SUM^2/N) / (N-1)` |
| Sample standard deviation | Square root of sample variance |

N is `COUNT(value)`, the number of valid, non-NULL values.

Keep only supported aggregates in the ROLLUP query block, and calculate variance and standard
deviation outside the inline view. This reads COUNT, SUM, and SUMSQ once and separates derived
calculations, allowing formulas to change without changing the ROLLUP query.

```sql
SELECT bucket, n, s, sq,
       sq/n - POWER(s/n, 2)       AS var_pop,
       SQRT(sq/n - POWER(s/n, 2)) AS stddev_pop
  FROM (
      SELECT rollup('min', 1, time) AS bucket,
             COUNT(value)           AS n,
             SUM(value)             AS s,
             SUMSQ(value)           AS sq
        FROM ch6_query WHERE name = 'TEMP_01'
       GROUP BY bucket
  ) t
 ORDER BY bucket;
```

The 00:00 bucket contains 10 and 20, so n=2, s=30, sq=500, population variance=25, and population
standard deviation=5. The 00:01 bucket has one value, so both population measures are 0.

Sample variance divides by `N-1`, so handle single-value buckets first, also outside the inline
view. Explicit `ELSE NULL` causes `ERR-02042`; omit ELSE.

```sql
SELECT bucket, n,
       CASE WHEN n > 1
            THEN (sq - POWER(s, 2)/n) / (n - 1)
            END AS var_samp
  FROM (
      SELECT rollup('min', 1, time) AS bucket,
             COUNT(value)           AS n,
             SUM(value)             AS s,
             SUMSQ(value)           AS sq
        FROM ch6_query WHERE name = 'TEMP_01'
       GROUP BY bucket
  ) t
 ORDER BY bucket;
```

The 00:00 sample variance is 50; the single-value 00:01 bucket returns NULL. To omit single-value
intervals, use `WHERE n > 1` outside the inline view. Source-table `VARIANCE` and `STDDEV` return 0
rather than NULL for these intervals, so align display policies when combining results.

For the example values, results match direct `VAR_POP`, `STDDEV_POP`, `VARIANCE`, and `STDDEV` on
the source table. However, both formulas lose precision when the mean is large relative to the
spread. For values near 100000 varying only in fractional digits, `SUMSQ/N` and `(SUM/N)^2` are
nearly equal, reducing significant digits after subtraction. If floating-point error yields a small
negative variance, SQRT is also invalid. When precision matters, compare with source-table STDDEV
and VAR_POP to establish an acceptable range.

<a id="query-week-month-year-day-timezone-origin-rollup"></a>

## Calendar Units and origin

Use the same data to check monthly results and weeks starting on Monday.

```sql
SELECT rollup('month', 1, time, '2000-01-01 00:00:00') AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('week', 1, time, '1970-01-05 00:00:00') AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

The monthly query returns SUM=60, COUNT=3, AVG=20 in the 2026-01-01 bucket. Monthly/yearly origin
values must be on the first day of a month after time-zone interpretation, and results fall at
midnight on the corresponding month boundary. This does not shift monthly business start times by
arbitrary dates or time offsets. Distinguish fixed-interval origins, such as day/week, from
month/year calendar calculations.

Check string interpretation together with the connection time zone. Do not assume DST automatically
matches the desired business calendar. Compare against source DATE_BIN aggregation around
boundaries. Validate equivalence to source results for origins or query boundaries that would split
stored aggregates.

## Clean Up

```sql
DROP ROLLUP ch6_query_sec;
DROP TABLE ch6_query;
```
