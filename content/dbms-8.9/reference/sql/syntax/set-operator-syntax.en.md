---
type: docs
title: 'set operator'
weight: 60
toc: true
---

Set operators combine results from two or more SELECT queries or calculate intersections/differences.

> Machbase currently supports only UNION ALL. UNION (duplicate removal),
> INTERSECT, and EXCEPT are not supported.

## UNION ALL

Combines two query results without removing duplicates.

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2;
```

## Requirements

Both SELECT statements must satisfy the following.

1. **Same column count**.
2. **Matching or compatible column types**.

A violation returns an error.

### Type Compatibility

| Combination | Compatible | Result Type |
|------|-----------|-----------|
| Signed ↔ unsigned integer | X | Error |
| Integer ↔ floating-point | O | Floating-point |
| Character types of different lengths | O | Accepted |
| IPv6 ↔ IPv4 | X | Error |

- Result column names come from the left query.

## Examples

```sql
-- Combine data from two tables
SELECT id, name FROM active_devices
UNION ALL
SELECT id, name FROM inactive_devices;

-- Combine statistics from different periods
SELECT 'Q1' AS quarter, SUM(value) AS total FROM sales WHERE month BETWEEN 1 AND 3
UNION ALL
SELECT 'Q2' AS quarter, SUM(value) AS total FROM sales WHERE month BETWEEN 4 AND 6;

-- Combine three queries
SELECT name, time, value FROM sensor_a WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
UNION ALL
SELECT name, time, value FROM sensor_b WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
UNION ALL
SELECT name, time, value FROM sensor_c WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

## Notes

- UNION ALL retains duplicates. To remove them, wrap the result in a subquery and apply DISTINCT or GROUP BY.
- UNION ALL between literal SELECT statements without FROM is unsupported.
- Result order is not guaranteed. For sorting, wrap the entire operation in an inline view and apply ORDER BY outside it.

```sql
-- When sorting is required
SELECT * FROM (
    SELECT id, name, time FROM log_a
    UNION ALL
    SELECT id, name, time FROM log_b
) ORDER BY time DESC;
```

## Related Documentation

- [SELECT Syntax](../select-syntax/) — Basic SELECT syntax
- [WITH / CTE Syntax](../cte-syntax/) — UNION ALL in CTEs
- [VIEW Syntax](../view-syntax/) — Views containing UNION ALL
