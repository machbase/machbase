---
type: docs
title: 'PIVOT'
weight: 70
toc: true
---

PIVOT converts row-oriented data into columns. Use it to rearrange GROUP BY aggregate results into
readable reports.

> PIVOT is supported from Machbase 5.6.

## Syntax

```sql
SELECT *
  FROM (inline_view)
 PIVOT (aggregate_function(value_col) FOR category_col IN ('val1', 'val2', ...))
[WHERE ...]
```

- Groups columns in inline_view that are not referenced by PIVOT.
- FOR category_col IN (...) specifies the pivot column and values to turn into output columns.
- Result column names are the string values in IN.

## Examples

### Pivoting Sensor Aggregates into Columns

```sql
-- PIVOT with an inline view
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
     WHERE regtime BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                       AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
WHERE FRONT_AXIS_TORQUE >= 40 AND REAR_AXIS_TORQUE >= 20;
```

### Concise Alternative to CASE

```sql
-- CASE without PIVOT
SELECT regtime,
       SUM(CASE WHEN tagid = 'SENSOR_A' THEN dvalue ELSE 0 END) AS sensor_a,
       SUM(CASE WHEN tagid = 'SENSOR_B' THEN dvalue ELSE 0 END) AS sensor_b
  FROM result_d
 GROUP BY regtime;

-- Concise PIVOT form
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
) PIVOT (SUM(dvalue) FOR tagid IN ('SENSOR_A', 'SENSOR_B'));
```

### PIVOT with TAG Tables

```sql
SELECT * FROM (
    SELECT name, time, value
      FROM sensor_tag
     WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                    AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    AVG(value) FOR name IN ('sensor-01', 'sensor-02', 'sensor-03')
);
```

## Constraints

- PIVOT requires an inline view (subquery).
- All inline-view columns except value_col and category_col are automatically grouped.
- IN values must be literals known at compile time; dynamic column lists are unsupported.

## Related Documentation

- [SELECT Hint Syntax](../select-hint-syntax/) — Syntax and examples for SELECT hints
