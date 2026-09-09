---
type: docs
title: 'WITH / CTE'
weight: 20
toc: true
---

A Common Table Expression (CTE) names a `SELECT` result within one SQL statement.
Use it to split complex inline views into stages or join aggregate results
to other tables.

Machbase 8.7.0 Standard Edition supports nonrecursive SELECT CTEs. A CTE exists
only within its SQL statement and is not stored as a database object.

## Support Scope

| Feature | Supported | Description |
|---|:---:|---|
| Single nonrecursive CTE | O | CTE body and main query are `SELECT` |
| Multiple CTEs | O | Comma-separated; later CTEs can reference earlier ones |
| Explicit result column names | O | Column list follows the CTE name |
| Nested CTEs | O | Outer CTEs are visible to nested `SELECT` queries |
| `INSERT SELECT` | O | Uses `INSERT INTO ... WITH ... SELECT` |
| VIEW definitions | O | Uses `CREATE VIEW ... AS WITH ... SELECT` |
| Prepared statements | O | `?` or `:name` in CTE bodies and the main `SELECT` |
| EXPLAIN | O | `EXPLAIN`, `EXPLAIN FULL`, `EXPLAIN TRACE` |
| `UNION ALL`, PIVOT | O | Existing `SELECT` scope and restrictions apply |
| Table types | O | Queries LOG, TAG, LOOKUP, VOLATILE, and TRANSACTION |
| Recursive CTEs | X | No `WITH RECURSIVE`, self-reference, or mutual recursion |
| Materialization control | X | No `MATERIALIZED` or `NOT MATERIALIZED` |
| Data-modifying CTEs | X | No DML or DDL in CTE bodies |

CTE bodies support JOIN, aggregates, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`,
`UNION ALL`, and PIVOT under existing SELECT rules. LOG `DURATION`, `SERIES BY`,
window functions, and TAG ROLLUP also retain their existing rules.

See [Named Bind Parameter Syntax](../named-bind-parameter-syntax/) for parameter
name rules and SDK binding methods.

## Basic Syntax

### SELECT

```sql
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

### INSERT SELECT

```sql
INSERT INTO target_table [(target_column [, ...])]
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

For `INSERT SELECT`, place `WITH` after the target table and column list.
The leading `WITH ... INSERT INTO ...` form used by other DBMSs is unsupported.

### VIEW

```sql
CREATE [OR REPLACE] VIEW view_name AS
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

### EXPLAIN

```sql
EXPLAIN [FULL | TRACE]
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

## Basic Usage

The examples assume the current user owns these tables:

| Table | Type | Columns used |
|---|---|---|
| `sensor_data` | LOG | `name`, `device_id`, `time`, `value` |
| `device_info` | TRANSACTION | `device_id`, `device_name` |
| `device_summary` | LOG | `device_id`, `sample_count`, `avg_value` |

### Name a Query Result

```sql
WITH recent_data AS (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 10m
)
SELECT name, time, value
FROM recent_data
ORDER BY time DESC;
```

Specify `ORDER BY` in the main SELECT to guarantee final ordering. An
`ORDER BY` inside the CTE alone does not guarantee outer-result order.

### Join Aggregate Results

```sql
WITH top_devices AS (
    SELECT device_id,
           AVG(value) AS avg_value
    FROM sensor_data
    WHERE time >= NOW - 1h
    GROUP BY device_id
    ORDER BY avg_value DESC
    LIMIT 10
)
SELECT d.device_id,
       d.device_name,
       t.avg_value
FROM device_info d
JOIN top_devices t
  ON d.device_id = t.device_id
ORDER BY t.avg_value DESC;
```

Use this to aggregate large time-series datasets and reduce result counts
before joining reference data.

### Chain Multiple CTEs

```sql
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 30m
),
device_avg AS (
    SELECT device_id, AVG(value) AS avg_value
    FROM recent_data
    GROUP BY device_id
)
SELECT device_id, avg_value
FROM device_avg
WHERE avg_value >= 80;
```

`device_avg` can reference the earlier `recent_data`. An earlier CTE
cannot reference a later one; forward references are unsupported.

### Specify Result Column Names

```sql
WITH device_stat (id, sample_count, average_value) AS (
    SELECT device_id, COUNT(*), AVG(value)
    FROM sensor_data
    GROUP BY device_id
)
SELECT id, sample_count, average_value
FROM device_stat;
```

The explicit column count must match the CTE result count, and names must
be unique. Without a list, SELECT aliases and inline-view column naming
rules apply.

## Supported SQL Contexts

### Nested SELECT

```sql
WITH active_devices AS (
    SELECT device_id
    FROM sensor_data
    WHERE time >= NOW - 1m
)
SELECT d.device_id, d.device_name
FROM device_info d
WHERE d.device_id IN (
    SELECT device_id
    FROM active_devices
);
```

A CTE declared in an outer SELECT is visible in scalar subqueries,
`IN (subquery)`, inline views, and other nested SELECTs. Existing restrictions
on scalar subqueries and `IN (subquery)` in JOIN ON conditions still apply.

### INSERT SELECT

```sql
INSERT INTO device_summary
WITH hourly_summary AS (
    SELECT device_id,
           COUNT(*) AS sample_count,
           AVG(value) AS avg_value
    FROM sensor_data
    WHERE time >= NOW - 1h
    GROUP BY device_id
)
SELECT device_id, sample_count, avg_value
FROM hourly_summary;
```

A CTE produces result rows; target-table `INSERT SELECT` rules determine
allowed input and duplicate-key handling. CTEs do not change target
constraints or atomicity scope.

### VIEW Definitions

```sql
CREATE VIEW active_device_summary AS
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 10m
)
SELECT device_id,
       COUNT(*) AS sample_count,
       AVG(value) AS avg_value
FROM recent_data
GROUP BY device_id;
```

A VIEW stores the SELECT definition, including the CTE, and interprets
it again when queried. The same syntax applies to `CREATE OR REPLACE VIEW`.

VIEW definitions cannot use bind parameters (`?`). Put conditions that
vary per execution in the SELECT querying the VIEW.

### EXPLAIN

```sql
EXPLAIN FULL
WITH recent_data AS (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 5m
)
SELECT *
FROM recent_data
WHERE name = 'sensor-01';
```

Use `EXPLAIN`, `EXPLAIN FULL`, or `EXPLAIN TRACE` to inspect scans, filters,
and joins on actual tables after CTE expansion.

### Prepared statement

Bind parameters (`?`) are allowed in CTE bodies and the main SELECT.

```sql
WITH selected_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE device_id = ?
)
SELECT device_id, time, value
FROM selected_data
WHERE value >= ?;
```

Parameters in unreferenced CTEs are still registered and require values.
Referencing a CTE multiple times does not multiply its original parameter count.

## Names and Scope

### Declaration Order

Later CTEs can reference earlier CTEs. Forward references, self-references,
and mutual references are unsupported.

### Names Shared with Real Tables

When an unqualified name matches both a CTE and a real TABLE or VIEW,
the CTE in the current scope takes precedence.

```sql
WITH device_info AS (
    SELECT device_id
    FROM sensor_data
)
SELECT *
FROM device_info;
```

Qualify a real table with its owner, such as `user_name.device_info`.
Owner-qualified names resolve to actual TABLEs or VIEWs, not CTEs.

### Nested Scope

Inner SELECTs can reference outer CTEs. An inner CTE is not visible
outside its SELECT. If its name matches an outer CTE, the inner one takes precedence.

## Execution and Performance

Machbase plans CTE references by expanding them into existing inline-view
forms. It does not guarantee materialization into temporary tables or
single evaluation.

Multiple references to one CTE may be planned and executed independently.

```sql
WITH recent_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE time >= NOW - 1d
)
SELECT a.device_id, a.value, b.value
FROM recent_data a
JOIN recent_data b
  ON a.device_id = b.device_id
 AND a.time = b.time;
```

Use these performance guidelines:

- Avoid repeated references to CTEs that read large tables.
- Apply selective time, tag-name, and key predicates as early as possible in CTE bodies.
- Do not predict performance assuming filter pushdown or automatic result reuse.
- For repeated references, consider separate queries or persisted objects.
- Inspect the actual plan for each reference with `EXPLAIN`.

Because `MATERIALIZED` and `NOT MATERIALIZED` are unsupported, users cannot
force a CTE evaluation strategy.

### CTE Expansion Limit

CTE expansion can generate at most 1,024 SELECT units per SQL statement.
This is the total after expanding repeated and chained references, not
the number of declared CTE names.

Exceeding the limit raises this error:

```text
CTE expansion limit exceeded
```

Reduce repeated-reference chains or separate intermediate results into
another table or VIEW.

## Limitations

The following are unsupported:

- `WITH RECURSIVE` and recursive CTEs
- Self-reference or mutual recursion even without `RECURSIVE`
- Forward references
- `MATERIALIZED`, `NOT MATERIALIZED`
- Recursive syntax `SEARCH DEPTH FIRST`, `SEARCH BREADTH FIRST`, `CYCLE`
- Leading `WITH ... INSERT`, `WITH ... UPDATE`, `WITH ... DELETE`, `WITH ... MERGE`
- INSERT, UPDATE, DELETE, MERGE, or DDL inside a CTE
- `UNION`, `INTERSECT`, `EXCEPT`
- `UNION ALL` between literal SELECTs without FROM
- `EXISTS` expressions
- `FREQUENCY` inside a CTE
- CTEs in custom `CREATE ROLLUP ... AS (...)` queries

CTEs do not expand table-type DML support. Queries and inserts on LOG, TAG,
LOOKUP, VOLATILE, and TRANSACTION follow their existing rules.

## Diagnose Errors

| Condition | Check |
|---|---|
| Duplicate CTE name | Declare each name once per WITH clause. |
| Column-count mismatch | Match explicit columns to SELECT result columns. |
| Duplicate column name | Remove duplicates from the explicit list. |
| Forward reference | Declare the referenced CTE first. |
| Self-reference | Remove recursion or use fixed-depth SQL/application iteration. |
| Table not found | Check whether a qualified name resolves to a real TABLE/VIEW instead of a CTE. |
| Expansion limit exceeded | Reduce reference chains or separate intermediate objects. |
| VIEW bind error | Remove `?` from VIEW/CTE definitions and apply predicates when querying. |
| Syntax error | Check for unsupported recursion, materialization, or leading WITH/DML forms. |

## Migrate from Other DBMSs

| Source feature | Machbase approach |
|---|---|
| PostgreSQL/MySQL `WITH RECURSIVE` | Use fixed-depth SQL or application iteration. |
| PostgreSQL/SQLite `MATERIALIZED` | Remove the keyword; do not assume single evaluation. |
| PostgreSQL/SQLite `NOT MATERIALIZED` | Remove the keyword and inspect EXPLAIN. |
| Oracle recursive subquery factoring | Migrate only nonrecursive CTEs without self-reference. |
| SQL Server `WITH ... UPDATE/DELETE/MERGE` | Separate CTE and DML; follow table-specific rules. |
| Recursive `SEARCH` or `CYCLE` | Handle paths and cycle detection in applications or stored columns. |

## Related Documentation

- [SELECT Syntax](../select-syntax/)
- [DML Syntax](../dml-syntax/)
- [VIEW Syntax](../view-syntax/)
- [Set Operators](../set-operator-syntax/)
- [PIVOT Syntax](../pivot-syntax/)
- [Window Functions and OVER](../window-function-over-syntax/)
- [Query Analysis and EXPLAIN](/dbms/performance-tuning/performance-query-tuning/)
