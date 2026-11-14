---
type: docs
title: 'window function / OVER'
weight: 80
toc: true
---

Machbase `LAG()` and `LEAD()` reference earlier or later row values in query
results. For example, compare sensor measurements in time order to calculate
changes from the previous reading. Unlike GROUP BY aggregates, they do
not collapse multiple rows into one.

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
|------|------|
| `value_expression` | Value from an earlier or later row |
| `offset` | Row distance from the current row; integer at least 1 |
| `PARTITION BY` | One expression grouping rows; omitted means one group for all results |
| `ORDER BY` | One expression ordering comparisons within each group |

OVER is required, but PARTITION BY and ORDER BY inside it are optional.
Specify an order such as `ORDER BY time` for chronological comparisons.
That expression alone does not order ties. To guarantee final output
order, also put ORDER BY at the end of SELECT.

## Supported Window Functions

<a id="이동-참조-함수"></a>

| Function | Description |
|------|------|
| `LAG(value, n)` | Value n rows before the current row in the same group |
| `LEAD(value, n)` | Value n rows after the current row in the same group |

Returns NULL if the referenced row does not exist. `offset` counts rows,
not elapsed time. With irregular samples, the previous row is not
necessarily one second or one minute earlier.

<a id="순위-함수"></a>
<a id="집계-윈도우-함수"></a>

### Differences from Other DBMS Window Syntax

Do not confuse the following syntax with Machbase LAG/LEAD:

- `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `FIRST_VALUE()`, and `LAST_VALUE()` are unsupported.
- Aggregate windows such as `SUM(...) OVER (...)` and `AVG(...) OVER (...)` are unsupported.
- ROWS/RANGE frames and boundaries such as UNBOUNDED PRECEDING and CURRENT ROW are unsupported.
- PARTITION BY and ORDER BY within OVER each accept only one expression.
  ASC/DESC after ORDER BY is also unsupported.

See [Window/Series Functions](../../functions/series/) for `ROWNUM()`, which
numbers result rows, and `SERIESNUM()`, which numbers consecutive groups.

## Examples

### LAG / LEAD: Compare Previous and Next Values

This example uses `sensor_tag` with `name`, `time`, and `value` columns.

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

`prev_value` and `next_value` are previous/next values within the query
range. The first prev_value and last next_value are NULL. Rows excluded
by WHERE are not comparison candidates; extend the range earlier if
you need the first row's change as well.

<a id="순위-함수-1"></a>
<a id="이동-평균"></a>
<a id="누적-합계"></a>

### Compare Previous Aggregate Values

Aggregate tag time intervals first, then compare aggregate changes.
This example assumes `sensor_tag` has an hourly ROLLUP available.

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

This compares each interval average to the preceding interval average.
It does not calculate a moving average or cumulative total. Empty
intervals are not filled automatically.

## Performance Considerations

Window calculations require grouping, sorting, and retaining previous/next
values. Reduce target rows with time/tag predicates. For long-term trends,
apply comparisons to aggregates to process fewer rows.

Use LAG/LEAD in SELECT result expressions. Do not call them directly in
WHERE, HAVING, GROUP BY, ORDER BY, or JOIN ON. To filter computed values,
reference inline-view result columns from an outer SELECT.

## Related Documentation

- [Window/Series Functions](../../functions/series/) — `ROWNUM()` and `SERIESNUM()`
- [PIVOT Syntax](../pivot-syntax/) — Convert rows to columns
- [SERIES BY Syntax](../series-syntax/) — Extract consecutive groups
