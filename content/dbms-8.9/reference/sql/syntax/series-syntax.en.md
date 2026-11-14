---
type: docs
title: 'SERIES BY'
weight: 90
toc: true
---

SERIES BY extracts contiguous sequences of rows satisfying a condition from an ordered result set.
Use it to analyze interval start/end times and patterns.

## Syntax

```sql
SELECT ...
  FROM table_name
 [WHERE ...]
 ORDER BY col [ASC | DESC]
 SERIES BY condition_expr
```

- Without ORDER BY, rows are ordered by _ARRIVAL_TIME.
- Explicit ORDER BY is required with GROUP BY or on VOLATILE/LOOKUP tables without _ARRIVAL_TIME.
- Rows in one contiguous interval satisfying SERIES BY share the same SERIESNUM() value.

## Examples

### Basic Usage

```sql
CREATE LOG TABLE t1 (c1 INTEGER, c2 INTEGER);
INSERT INTO t1 VALUES (0, 1);
INSERT INTO t1 VALUES (1, 2);
INSERT INTO t1 VALUES (2, 3);
INSERT INTO t1 VALUES (3, 2);
INSERT INTO t1 VALUES (4, 1);
INSERT INTO t1 VALUES (5, 2);
INSERT INTO t1 VALUES (6, 3);
INSERT INTO t1 VALUES (7, 1);

SELECT c1, c2
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

Result:

```
C1          C2
---------------------------
1           2
2           3
3           2
5           2
6           3
```

### Identifying Intervals with SERIESNUM()

```sql
SELECT c1, c2, SERIESNUM() AS grp
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

Result:

```
C1          C2          GRP
-----------------------------------
1           2           1
2           3           1
3           2           1
5           2           2
6           3           2
```

### Contiguous Intervals in TAG Tables

Generate interval numbers in an inner query, then aggregate by interval number in the outer query.

```sql
-- Start/end timestamps and maximum for each contiguous interval above 100
SELECT MIN(time) AS start_time,
       MAX(time) AS end_time,
       MAX(value) AS peak_value,
       series_id
  FROM (
      SELECT time, value, SERIESNUM() AS series_id
        FROM tag
       WHERE name = 'PRESSURE-01'
         AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
       ORDER BY time
       SERIES BY value > 100.0
  )
 GROUP BY series_id
 ORDER BY series_id;
```

## Related Documentation

- [SELECT Hint Syntax](../select-hint-syntax/) — Syntax and examples for SELECT hints
- [Window Function / OVER Syntax](../window-function-over-syntax/) — Comparison with window-based analysis
