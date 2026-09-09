---
type: docs
title: '12.5 Query and Analysis Tuning'
weight: 50
toc: true
aliases:
  - /dbms/performance-tuning/query-analysis/
---

Improve query performance by reducing rows and partitions read and sorting and aggregation
work while preserving correct results. Compare execution time and result counts before and
after changes using the same data, predicates, and concurrency.

## Key principles

1. First restrict TAG and LOG queries to the required time range.
2. Select only the needed columns and avoid unbounded `SELECT *`.
3. Consider indexes for frequent equality and range predicates and JOIN keys.
4. Use ROLLUP for repeated long-range TAG aggregates.
5. Inspect the plan with `EXPLAIN` before changing hints or configuration.
6. Record latency distributions, rows read, CPU, I/O, and concurrent query effects, not just averages.

## Reproducible example

This example creates a LOG table and index, checks the execution plan and results, then cleans up.

```sql
CREATE LOG TABLE perf_event_demo (
    device_id VARCHAR(32),
    level     VARCHAR(16),
    code      INTEGER,
    message   VARCHAR(100)
);

CREATE INDEX idx_perf_event_code
ON perf_event_demo(code) INDEX_TYPE LSM;

INSERT INTO perf_event_demo VALUES ('DEV-01', 'WARN', 1001, 'temperature high');
INSERT INTO perf_event_demo VALUES ('DEV-02', 'INFO', 1000, 'started');
EXEC TABLE_FLUSH(perf_event_demo);

EXPLAIN
SELECT device_id, level, message
FROM perf_event_demo
WHERE code = 1001
  AND _ARRIVAL_TIME >= NOW - 60000000000;

SELECT device_id, level, message
FROM perf_event_demo
WHERE code = 1001
  AND _ARRIVAL_TIME >= NOW - 60000000000;

DROP TABLE perf_event_demo;
```

Do not conclude from a small sample that an index scan is always faster. Compare before and
after index creation with production-like data distribution and predicate selectivity.

<a id="performance-tuning-select"></a>
<a id="select-join-optimizer"></a>

## SELECT and JOIN

- First reduce large source tables with time and key predicates.
- Match data types and lengths on both sides of JOIN predicates.
- Check whether functions around WHERE columns prevent index-range access.
- Before replacing an outer JOIN with an inner JOIN, check whether NULL-extended rows disappear.
- Specify `ORDER BY` when result order matters.
- For pagination, consider keyset pagination using business keys and timestamps instead of large OFFSETs.

Do not assume the optimizer follows table order as written in SQL. Hints that force join
order can become counterproductive as statistics and data distribution change. Verify both
the execution plan and results.

## Use EXPLAIN

`EXPLAIN` shows the execution plan without running the query. `EXPLAIN FULL` may execute the
query, so use it only in a controlled environment without production load.

Check these plan elements:

| Element | Question |
|------|------|
| Target tables | Are the intended tables and views selected? |
| Scan type | Does the access path match the predicates and indexes? |
| Time range | Is the TAG or LOG partition range restricted? |
| JOIN | Are unnecessary joins processing large inputs? |
| Sorting and aggregation | Are large intermediate results sorted or materialized? |

Do not hardcode internal object IDs or complete plan strings in automated checks; they can
change across versions. Check stable semantic elements such as table names, scan types, and
key predicates.

<a id="performance-cte"></a>

## CTE

CTEs improve readability but do not automatically improve performance. Inspect the plan for
repeated CTE evaluation, filter pushdown into the CTE, and large intermediate results. Machbase
8.7.0 Standard Edition supports non-recursive SELECT CTEs. Recursive CTEs are not supported.

For syntax and examples, see [CTE](/dbms/reference/sql/syntax/cte-syntax/).

<a id="performance-operators-tuning"></a>

## Search operators

| Predicate | Check |
|------|------|
| Equality and range comparisons | Column type and index type compatibility |
| `LIKE 'prefix%'` | Prefix search support and string index usage |
| Leading wildcard | Whether a full scan is affordable |
| `SEARCH` and `ESEARCH` | KEYWORD index and syntax compatibility |
| `REGEXP` | Whether time and other indexed predicates first reduce candidate rows |
| JSON path | Supported table types and JSON indexes |
| IP range | IPV4/IPV6 types and index support |

For exact predicate semantics and index requirements, see
[SEARCH, ESEARCH, and REGEXP](/dbms/reference/sql/syntax/search-esearch-regexp-syntax/) and
[JSON Operators](/dbms/reference/sql/functions/operators-json/).

<a id="performance-window-functions-considerations-pivot"></a>

<a id="window-function과-pivot"></a>

## Window functions and PIVOT

Large window partitions or wide ordering keys can increase sorting and memory costs. First
reduce input with time and business-key predicates, and check for duplicate window calculations.
For PIVOT, limit output categories and define how unexpected categories are handled.

For syntax, see [Window Functions](/dbms/reference/sql/syntax/window-function-over-syntax/)
and [PIVOT](/dbms/reference/sql/syntax/pivot-syntax/).

## Before-and-after checklist

- Are result row counts and NULL distributions unchanged?
- Are the time range and time zone the same?
- Have cold and warm caches been measured separately?
- Have you compared concurrent queries as well as individual executions?
- Are there adverse effects on ingestion throughput or memory usage?
- Have you recorded rollback DDL, configuration values, and baseline measurements?

<a id="관련-sql-정본"></a>

## Related SQL documentation

| Topic | Details |
|---|---|
| SELECT and time predicates | [SELECT Syntax](/dbms/reference/sql/syntax/select-syntax/) |
| VIEW, CTE, and set operations | [SQL Syntax Reference](/dbms/reference/sql/syntax/) |
| Hints | [SELECT Hints](/dbms/reference/sql/syntax/select-hint-syntax/) |
| Functions and aggregates | [Function Reference](/dbms/reference/sql/functions/) |
