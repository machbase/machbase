---
type: docs
title: 'Aggregate Functions'
weight: 10
toc: true
---

Aggregate functions combine values from multiple rows into one result. With GROUP BY, they return
results per group. NULL values are ignored, except by COUNT(*).

## Quick Reference

| Function | Syntax | Description |
|------|------|------|
| COUNT | `COUNT(*) / COUNT(col)` | All rows or non-NULL rows |
| SUM | `SUM(col)` | Sum |
| AVG | `AVG(col)` | Average |
| MIN | `MIN(col)` | Minimum |
| MAX | `MAX(col)` | Maximum |
| STDDEV | `STDDEV(col)` | Sample standard deviation |
| STDDEV_POP | `STDDEV_POP(col)` | Population standard deviation |
| VARIANCE | `VARIANCE(col)` | Sample variance |
| VAR_POP | `VAR_POP(col)` | Population variance |
| FIRST | `FIRST(sort_expr, return_expr)` | Value from the first row by the sort expression |
| LAST | `LAST(sort_expr, return_expr)` | Value from the last row by the sort expression |
| SUMSQ | `SUMSQ(col)` | Sum of squares |
| MEDIAN | `MEDIAN(col)` | Median |
| MODE | `MODE(col)` | Most frequent value |
| AREA | `AREA(y, x)` | Area under the curve (trapezoidal integration) |
| SLOPE | `SLOPE(y, x)` | Linear regression slope |
| GROUP_CONCAT | `GROUP_CONCAT(col ...)` | Concatenate values within a group |
| TS_CHANGE_COUNT | `TS_CHANGE_COUNT(col)` | Number of value changes |
| TOP_K | `TOP_K(col, k)` | k most frequent values |
| PERCENTILE_CONT | `PERCENTILE_CONT(col, ratio)` | Continuous percentile |
| PERCENTILE_DISC | `PERCENTILE_DISC(col, ratio)` | Discrete percentile |
| APPROX_PERCENTILE | `APPROX_PERCENTILE(col, ratio)` | Approximate percentile |
| CUME_DIST | `CUME_DIST(value, threshold)` | Cumulative distribution ratio |

---

## COUNT

Counts records. `COUNT(*)` returns all rows, including NULLs; `COUNT(col)` returns the count of
non-NULL rows.

```sql
COUNT(*)
COUNT(column_name)
```

```sql
Mach> CREATE LOG TABLE count_table (id1 INTEGER, id2 INTEGER);
Mach> INSERT INTO count_table VALUES(1, 1);
Mach> INSERT INTO count_table VALUES(2, 2);
Mach> INSERT INTO count_table VALUES(null, 4);

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
---------
3

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------
2
```

---

## SUM

Returns the sum of a numeric column.

```sql
SUM(column_name)
```

```sql
Mach> SELECT c1, SUM(c2) FROM sum_table GROUP BY c1;
c1          SUM(c2)
--------------------
1           6
2           6
3           4
```

---

## AVG

Returns the average of a numeric column.

```sql
AVG(column_name)
```

```sql
Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
---------------------
1           2
2           2
NULL        4
```

---

## MIN

Returns the minimum of the specified numeric column.

```sql
MIN(column_name)
```

```sql
Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------
1
```

---

## MAX

Returns the maximum of the specified numeric column.

```sql
MAX(column_name)
```

```sql
Mach> SELECT MAX(c) FROM max_table;
MAX(c)
-------
30
```

---

## STDDEV / STDDEV_POP

Returns the sample standard deviation (STDDEV) or population standard deviation (STDDEV_POP) of a column.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2          STDDEV(c1)
-----------------------
1           0.707107
2           0.707107

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2          STDDEV_POP(c1)
---------------------------
1           0.5
2           0.5
```

---

## VARIANCE / VAR_POP

Returns sample variance (VARIANCE) or population variance (VAR_POP).

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
--------------
0.333333

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
-------------
0.25
```

---

## FIRST / LAST

Returns `return_expr` from the first (FIRST) or last (LAST) row in each group ordered by
`sort_expr`. Useful for retrieving values at specific points in a time series.

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> SELECT group_no, FIRST(id, name) FROM firstlast_table GROUP BY group_no;
group_no    first(id, name)
----------------------------
0           John
1           Grey

Mach> SELECT group_no, LAST(id, name) FROM firstlast_table GROUP BY group_no;
group_no    last(id, name)
---------------------------
0           Ryan
1           Kyle
```

---

## SUMSQ

Returns the sum of squared numeric values.

```sql
SUMSQ(value)
```

```sql
Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
----------------------
1           14
2           41
```

---

## MEDIAN

Returns the exact median of a numeric expression.

```sql
MEDIAN(value)
```

```sql
SELECT MEDIAN(temp_c) FROM sensor_log;
```

---

## MODE

Returns the most frequent numeric value. If multiple values tie, returns the smallest.

```sql
MODE(value)
```

```sql
SELECT MODE(alarm_code) FROM event_log;
```

---

## AREA

Calculates the area under a curve of numeric `(x, y)` points using trapezoidal integration. Returns
NULL with fewer than two valid points.

```sql
AREA(y, x)
```

```sql
SELECT AREA(power_kw, sample_sec) FROM power_log;
```

---

## SLOPE

Calculates the slope of the linear regression line for numeric `(x, y)` points. Returns NULL if x
has zero variance or there are insufficient valid data.

```sql
SLOPE(y, x)
```

```sql
SELECT SLOPE(temp_c, sample_sec) FROM sensor_log;
```

---

## GROUP_CONCAT

Concatenates column values within a group into a string.

{{< callout type="warning" >}}
Unavailable in Cluster Edition.
{{< /callout >}}

```sql
GROUP_CONCAT(
    [DISTINCT] column
    [ORDER BY column [ASC | DESC] [, ...]]
    [SEPARATOR str_val]
)
```

```sql
Mach> SELECT GROUP_CONCAT(name) FROM concat_table GROUP BY id2;
G_NAMES
---------
Jack,Jack,Ram
Jill,Zara,John

Mach> SELECT GROUP_CONCAT(DISTINCT name SEPARATOR '.') FROM concat_table GROUP BY id2;
G_NAMES
---------
Jack.Ram
Jill.Zara.John
```

---

## TS_CHANGE_COUNT

Returns the number of changes in time-ordered column values. VARCHAR is not supported.

{{< callout type="warning" >}}
Unavailable in Cluster Edition.
{{< /callout >}}

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> SELECT id, TS_CHANGE_COUNT(ip) FROM ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
--------------------------------
1           4
2           2
```

---

## TOP_K

Returns the k most frequent numeric values as a `value:count` string, ordered by descending
frequency and ascending value for ties.

```sql
TOP_K(value, k)
```

```sql
SELECT TOP_K(alarm_code, 3) FROM event_log;
-- Example result: 101:532,205:317,301:90
```

---

## PERCENTILE_CONT / PERCENTILE_DISC

Aggregate functions that calculate exact percentiles. `ratio` must be a constant from 0.0 through 1.0.

- `PERCENTILE_CONT`: Interpolates between adjacent sorted values.
- `PERCENTILE_DISC`: Selects an observed value.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

Shorthand functions `P05`, `P10`, `P90`, and `P95` are also available.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS p95,
       PERCENTILE_DISC(latency_ms, 0.50) AS p50
FROM api_log;

-- Shorthand
SELECT P05(response_ms), P95(response_ms) FROM web_log;
```

---

## APPROX_PERCENTILE

Approximate percentile function, useful for very large datasets when a small error is acceptable.
Shorthands include APPROX_MEDIAN, APPROX_P05, APPROX_P10, APPROX_P90, and APPROX_P95.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P95(value)
```

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms)            AS amedian
FROM api_log;
```

---

## CUME_DIST

Returns the cumulative fraction of rows whose `value` is at most `threshold` (0.0–1.0). This is an
aggregate function, not a window function.

```sql
CUME_DIST(value, threshold)
```

```sql
SELECT CUME_DIST(latency_ms, 100) FROM api_log;
```
