---
type: docs
title: 'SELECT'
weight: 10
toc: true
---

`SELECT` retrieves, filters, and aggregates data from Machbase table types.

## Complete SELECT Syntax

```sql
query_stmt ::=
    [ with_clause ]
    select_stmt

select_stmt ::=
    'SELECT' [ hint_clause ] target_list
    [ 'FROM' table_reference_list ]
    [ 'WHERE' condition_expr ]
    [ 'DURATION' duration_expr ]
    [ 'GROUP BY' expr_list [ 'HAVING' condition_expr ] ]
    [ 'ORDER BY' expr_list [ 'ASC' | 'DESC' ] ]
    [ 'SERIES BY' condition_expr ]
    [ 'LIMIT' [ offset ',' ] row_count ]

-- Set operator
select_stmt 'UNION ALL' select_stmt
```

Place `DURATION` after WHERE and before GROUP BY, HAVING, ORDER BY, SERIES BY,
and LIMIT. The syntax above shows clause order, not internal execution order.

`with_clause` declares nonrecursive CTEs in Standard Edition. See
[WITH / CTE Syntax](../cte-syntax/) for complete syntax and restrictions.

### Target List (target_list)

```sql
target_list ::=
    '*'
  | target_expr ( ',' target_expr )*

target_expr ::=
    column_name [ 'AS' alias ]
  | expr [ 'AS' alias ]
  | '(' subquery ')' [ 'AS' alias ]
```

### FROM Clause

```sql
table_reference_list ::=
    table_reference ( ',' table_reference )*

table_reference ::=
    table_name [ alias ]
  | '(' subquery ')' [ alias ]
  | table_name [ alias ] join_clause
  | view_name [ alias ]

join_clause ::=
    [ 'INNER' | 'LEFT OUTER' | 'RIGHT OUTER' ] 'JOIN' table_reference 'ON' condition_expr
  | 'CROSS JOIN' table_reference
```

---

## SELECT Without FROM

Returns constants, arithmetic expressions, or simple function results as one
row without querying a table.

```sql
SELECT 1;
SELECT 'alive';
SELECT 1 + 2;
SELECT ABS(-7);
SELECT SYSDATE;
```

---

## WHERE Clause

```sql
condition_expr ::=
    expr comparison_op expr
  | expr [ 'NOT' ] 'BETWEEN' expr 'AND' expr
  | column_name [ 'NOT' ] 'IN' '(' value_list | subquery ')'
  | column_name 'RANGE' duration_spec
  | column_name [ 'NOT' ] 'SEARCH' string_literal
  | column_name 'ESEARCH' pattern_literal
  | column_name [ 'NOT' ] 'REGEXP' pattern_literal
  | expr 'IS' [ 'NOT' ] 'NULL'
  | condition_expr ( 'AND' | 'OR' ) condition_expr
  | 'NOT' condition_expr
  | '(' condition_expr ')'
  | '(' subquery ')'
```

### Main WHERE Operators

| Operator | Description |
|--------|------|
| `=`, `<>`, `<`, `<=`, `>`, `>=` | Comparison |
| `BETWEEN value1 AND value2` | Range condition |
| `IN (value_list)` | Value-list condition |
| `IN (subquery)` | Subquery IN |
| `RANGE n unit` | Time range relative to now |
| `SEARCH 'keyword'` | Keyword-index text search |
| `ESEARCH 'pattern%'` | Extended text search (% wildcard) |
| `REGEXP 'pattern'` | Regular expression search (no index) |
| `IS NULL` / `IS NOT NULL` | NULL condition |

```sql
-- BETWEEN
SELECT * FROM sensor_log WHERE value BETWEEN 10.0 AND 20.0;

-- IN
SELECT * FROM sensor_log WHERE status IN ('OK', 'WARN');

-- RANGE (Last hour relative to now)
SELECT * FROM sensor_log WHERE _arrival_time RANGE 1 HOUR;

-- SEARCH (Uses the keyword index)
SELECT * FROM log_table WHERE message SEARCH 'error';

-- ESEARCH (Wildcard pattern)
SELECT * FROM log_table WHERE message ESEARCH 'timeout%';

-- REGEXP (Regular expression)
SELECT * FROM log_table WHERE message REGEXP 'error[0-9]+';
```

---

## GROUP BY / HAVING

```sql
'GROUP BY' expr_list [ 'HAVING' condition_expr ]
```

```sql
SELECT name, AVG(value), MAX(value), COUNT(*)
  FROM sensor_log
 GROUP BY name
HAVING AVG(value) > 50.0;
```

---

## ORDER BY

```sql
'ORDER BY' expr_list [ 'ASC' | 'DESC' ]
```

```sql
SELECT name, value FROM sensor_log ORDER BY value DESC;
SELECT name, value FROM sensor_log ORDER BY name ASC, value DESC;
```

---

## LIMIT

```sql
'LIMIT' [ offset ',' ] row_count
```

```sql
-- Retrieve only the first 10 rows
SELECT * FROM sensor_log LIMIT 10;

-- Retrieve 10 rows starting with the 11th
SELECT * FROM sensor_log LIMIT 10, 10;
```

---

## DURATION

Specifies a query time range based on `_arrival_time`.

```sql
duration_expr ::=
    number time_unit [ ( 'BEFORE' | 'AFTER' ) number time_unit ]
  | 'FROM' datetime_expr 'TO' datetime_expr

time_unit ::= 'YEAR' | 'MONTH' | 'WEEK' | 'DAY' | 'HOUR' | 'MINUTE' | 'SECOND'
```

```sql
-- Data from the last hour
SELECT * FROM sensor_log DURATION 1 HOUR;

-- One-hour range starting one day ago
SELECT * FROM sensor_log DURATION 1 HOUR BEFORE 1 DAY;

-- Explicit range
SELECT * FROM sensor_log
DURATION FROM TO_DATE('2024-01-01','YYYY-MM-DD')
         TO TO_DATE('2024-01-31','YYYY-MM-DD');
```

---

## JOIN

### INNER JOIN (Comma Syntax)

```sql
SELECT t1.id, t2.name
  FROM sensor_log t1, devices t2
 WHERE t1.id = t2.device_id AND t1.value > 50;
```

### ANSI JOIN

```sql
-- INNER JOIN
SELECT t1.id, t2.name
  FROM sensor_log t1
  INNER JOIN devices t2 ON (t1.id = t2.device_id)
 WHERE t1.value > 50;

-- LEFT OUTER JOIN
SELECT t1.id, t2.location
  FROM sensor_log t1
  LEFT OUTER JOIN devices t2 ON (t1.name = t2.name);

-- RIGHT OUTER JOIN
SELECT t1.value, t2.name
  FROM sensor_log t1
  RIGHT OUTER JOIN devices t2 ON (t1.name = t2.name);
```

> FULL OUTER JOIN is not supported.

---

## SERIES BY

Extracts groups of consecutive records that satisfy a condition in sorted results.

```sql
'ORDER BY' expr 'SERIES BY' condition_expr
```

```sql
-- Retrieve consecutive record groups satisfying C2 > 1
SELECT c1, c2, SERIESNUM() AS grp
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

---

## SUBQUERY

```sql
-- FROM subquery (inline view)
SELECT a.name, a.avg_val
  FROM (SELECT name, AVG(value) AS avg_val FROM sensor_log GROUP BY name) a
 WHERE a.avg_val > 50;

-- WHERE subquery
SELECT * FROM sensor_log
 WHERE value > (SELECT AVG(value) FROM sensor_log);

-- IN subquery
SELECT * FROM sensor_log
 WHERE name IN (SELECT name FROM devices WHERE status = 'ACTIVE');
```

> Correlated subqueries (subqueries referencing outer-query columns) are not supported.

---

## CASE Expressions

```sql
-- simple CASE
CASE expr
    WHEN value1 THEN result1
    [ WHEN value2 THEN result2 ... ]
    [ ELSE default_result ]
END

-- searched CASE
CASE
    WHEN condition1 THEN result1
    [ WHEN condition2 THEN result2 ... ]
    [ ELSE default_result ]
END
```

```sql
SELECT name,
       value,
       CASE
           WHEN value >= 80 THEN 'HIGH'
           WHEN value >= 40 THEN 'MID'
           ELSE 'LOW'
       END AS level
  FROM sensor_log;
```

---

## PIVOT

Transforms aggregate results from an inline view from rows into columns.

```sql
'PIVOT' '(' aggregate_func '(' column ')' 'FOR' pivot_column 'IN' '(' value_list ')' ')'
```

```sql
SELECT *
  FROM (SELECT regtime, tagid, dvalue FROM result_d)
 PIVOT (SUM(dvalue) FOR tagid IN ('AXIS_X', 'AXIS_Y', 'AXIS_Z'));
```

---

## UNION ALL

```sql
select_stmt 'UNION ALL' select_stmt
```

Combines two SELECT results. Column counts and types must be compatible.
`UNION` (deduplication), `INTERSECT`, and `EXCEPT` are unsupported.

```sql
SELECT id, name FROM table_a
UNION ALL
SELECT id, name FROM table_b;
```

---

## SAVE DATA INTO

Saves SELECT results to a CSV file.

```sql
'SAVE DATA INTO' 'file_path'
    [ 'HEADER' ( 'ON' | 'OFF' ) ]
    [ ( 'FIELDS' | 'COLUMNS' )
        [ 'TERMINATED BY' char ]
        [ 'ENCLOSED BY' char ] ]
    [ 'ENCODED BY' encoding ]
    'AS' select_stmt
```

```sql
SAVE DATA INTO '/tmp/sensor_data.csv' HEADER ON AS SELECT * FROM sensor_log;
```

---

## Related Documentation

- [WITH / CTE Syntax](../cte-syntax/) – Nonrecursive common table expressions
- [Hint Reference](../select-hint-syntax/) – SELECT optimization hints
- [SERIES BY](../series-syntax/) – Consecutive-condition grouping
- [PIVOT](../pivot-syntax/) – Row-to-column examples
- [SEARCH/ESEARCH/REGEXP](../search-esearch-regexp-syntax/) – Text search
- [DURATION Relative Time Expressions](../../relative-time/) – Complete time-range expressions
