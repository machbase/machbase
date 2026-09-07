---
type: docs
title: '17.1.1.8 window function / OVER syntax'
weight: 80
toc: true
---

Machbase `LAG()` and `LEAD()` access values in the preceding or following rows of a query result.
For example, you can compare sensor readings in time order and calculate the change from the
previous reading. Unlike `GROUP BY` aggregation, these functions do not collapse multiple rows.

## Syntax

```sql
LAG(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)

LEAD(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)
```

| Element | Description |
|---------|-------------|
| `value_expression` | Value to retrieve from the preceding or following row |
| `offset` | Distance in rows from the current row; specify an integer of at least 1 |
| `PARTITION BY` | One expression that groups rows for comparison; omission treats the result as one group |
| `ORDER BY` | One expression that determines the comparison order within each group |

`OVER` is required. Its `PARTITION BY` and `ORDER BY` clauses are optional.
For chronological comparisons, specify a criterion such as `ORDER BY time`. That expression
alone cannot distinguish the order of rows with equal values. To order the final output,
also specify `ORDER BY` at the end of the SELECT statement.

## Supported window functions

| Function | Description |
|----------|-------------|
| `LAG(value, n)` | Value n rows before the current row within the same group |
| `LEAD(value, n)` | Value n rows after the current row within the same group |

If the referenced row does not exist, the function returns NULL. `offset` counts rows, not elapsed
time. With irregular measurements, the previous row is not necessarily one second or one minute old.

### Differences from other DBMS window syntax

Machbase's `LAG`/`LEAD` syntax does not support the following forms:

- `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `FIRST_VALUE()`, or `LAST_VALUE()`.
- Aggregate window functions such as `SUM(...) OVER (...)` or `AVG(...) OVER (...)`.
- `ROWS`/`RANGE` frames or frame boundaries such as `UNBOUNDED PRECEDING` and `CURRENT ROW`.
- Multiple expressions in either `PARTITION BY` or `ORDER BY` inside `OVER`, or `ASC`/`DESC`
  after its `ORDER BY` expression.

For `ROWNUM()`, which numbers result rows, and `SERIESNUM()`, which identifies contiguous series,
see [the function reference](../../dictionary/functions-full/).

## Examples

### LAG / LEAD: compare preceding and following values

This example assumes a `sensor_tag` table with `name`, `time`, and `value` columns.

```sql
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value,
       LEAD(value, 1) OVER (PARTITION BY name ORDER BY time) AS next_value,
       value - LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS delta
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
 ORDER BY name, time;
```

`prev_value` and `next_value` refer to values within the selected range. The first row's
`prev_value` and the last row's `next_value` are NULL. Earlier rows excluded by `WHERE` do not
participate in the comparison. Extend the range backward if you also need the first row's change.

### Compare preceding aggregate values

You can first aggregate readings into time buckets, then compare the resulting values.
This example assumes that hourly ROLLUP queries are available for `sensor_tag`.

```sql
SELECT name, bucket, avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg
  FROM (
      SELECT name,
             rollup('hour', 1, time) AS bucket,
             AVG(value)              AS avg_val
        FROM sensor_tag
       WHERE time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                      AND TO_DATE('2024-07-01', 'YYYY-MM-DD')
       GROUP BY name, bucket
  ) t
 ORDER BY name, bucket;
```

This query compares each bucket's average with the preceding bucket's average. It does not
calculate a moving average or cumulative sum. Buckets with no data are not filled automatically.

## Performance considerations

Window calculations require grouping, ordering, and retaining values from preceding or following
rows. Limit the input with time and tag predicates. For long-term comparisons, applying the
functions to aggregate results can reduce the number of rows processed.

Use `LAG`/`LEAD` in SELECT result expressions. Do not call them directly in `WHERE`, `HAVING`,
`GROUP BY`, `ORDER BY`, or a JOIN's `ON` condition. To filter a calculated value, expose it as an
inline-view result column and reference that column from the outer SELECT.

## Related documentation

- [Function reference](../../dictionary/functions-full/) — `ROWNUM()` and `SERIESNUM()`
- [PIVOT syntax](../pivot-syntax/) — turn rows into columns
- [SERIES BY syntax](../series-syntax/) — identify contiguous series
