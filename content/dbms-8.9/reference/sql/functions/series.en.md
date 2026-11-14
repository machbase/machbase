---
type: docs
title: 'Window/Series Functions'
weight: 20
toc: true
---

This page describes `ROWNUM()`, which numbers result rows, and `SERIESNUM()`, which identifies
contiguous intervals. `SERIES BY` analyzes intervals in ordered data where a condition holds
continuously. For functions such as `LAG()` and `LEAD()` that use `OVER`, see
[Window Function Syntax](../../syntax/window-function-over-syntax/).

## Quick Reference

| Function | Syntax | Description |
|------|------|------|
| ROWNUM | `ROWNUM()` | Number SELECT result rows |
| SERIESNUM | `SERIESNUM()` | Number of the contiguous interval containing the row; rows in the same interval share a number |

---

## ROWNUM

Assigns sequential numbers to `SELECT` result rows. It can be used in subqueries and inline views.
Assign an alias in an inline view's select list so the outer query can reference it.

```sql
ROWNUM()
```

### Allowed Clauses

| Allowed | Not Allowed |
|-----------|----------|
| SELECT Target List, GROUP BY, ORDER BY | WHERE, HAVING |

To filter by row number in WHERE/HAVING, calculate `ROWNUM()` in an inline view and reference it
from the outer query.

```sql
-- Select only the first two rows
Mach> SELECT INNER_RANK, c3 AS NAME
        FROM (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
       WHERE INNER_RANK < 3;
INNER_RANK           NAME
--------------------------
1                    Fourth Row
2                    Third Row
```

### Using ORDER BY

Place the query with `ORDER BY` in an inline view and call `ROWNUM()` in the outer SELECT to number
rows in sorted order.

```sql
Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
        FROM (SELECT * FROM rownum_table ORDER BY c3);
ROWNUM()    SORT    NAME
--------------------------
1           1       NULL
2           2       John
3           4.3     Micheal
4           3.3     Sarah
```

---

## SERIESNUM

Returns the series number for each record grouped by `SERIES BY`. Without `SERIES BY`, it always
returns 1. The return type is `BIGINT`.

```sql
SERIESNUM()
```

```sql
Mach> CREATE LOG TABLE T1 (C1 INTEGER, C2 INTEGER);
Mach> INSERT INTO T1 VALUES (0, 1);
Mach> INSERT INTO T1 VALUES (1, 2);
Mach> INSERT INTO T1 VALUES (2, 3);
Mach> INSERT INTO T1 VALUES (3, 2);
Mach> INSERT INTO T1 VALUES (4, 1);
Mach> INSERT INTO T1 VALUES (5, 2);
Mach> INSERT INTO T1 VALUES (6, 3);
Mach> INSERT INTO T1 VALUES (7, 1);

-- Split contiguous intervals satisfying C2 > 1 into series
Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM()  C1  C2
--------------------
1            1   2
1            2   3
1            3   2
2            5   2
2            6   3
[5] row(s) selected.
```

- `C1=1,2,3` (contiguous interval satisfying C2>1) → Series 1
- `C1=4` (C2=1, condition false) → Series boundary
- `C1=5,6` (contiguous interval satisfying C2>1) → Series 2

---

## SERIES BY Overview

`SERIES BY` works with `ORDER BY` to group consecutive rows satisfying a condition into a series.
Use `SERIESNUM()` to identify each series and aggregate functions to calculate interval statistics.

For interval statistics, generate series numbers in an inner query and aggregate in the outer query.
Replace `threshold` in the example below with the threshold to compare.

```sql
SELECT series_id, COUNT(*), AVG(value)
  FROM (
      SELECT value, SERIESNUM() AS series_id
        FROM sensor_log
       ORDER BY ts
       SERIES BY value > threshold
  )
 GROUP BY series_id
 ORDER BY series_id;
```
