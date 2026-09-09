---
type: docs
title: 'ROLLUP'
weight: 180
toc: true
---

ROLLUP stores and queries recurring aggregates for time-axis TAG tables. Query ordinary, conditional,
and extended ROLLUPs with the public rollup() function; reaggregate user target TAG tables for
Custom rollups.

<a id="create-rollup"></a>

## Creation

The following is syntax notation; do not execute brackets or braces literally.

```text
CREATE ROLLUP [IF NOT EXISTS] name
    ON source_tag [(column_name | json_path_expression)]
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    FROM source_rollup
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }]
    [EXTENSION]
    [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
    INTO (destination_tag)
    AS (SELECT ...)
    INTERVAL n { SEC | MIN | HOUR }
    [WAKEUP INTERVAL m { SEC | MIN | HOUR }];
```

- EXTENSION is a standalone keyword; do not append an extension_name.
- CREATE uses SEC/MIN/HOUR. Distinguish these from query units such as DAY.
- Ordinary numeric columns can be specified without SUMMARIZED. JSON path aggregation differs from
  whole-document aggregation; whole-document and automatic WITH ROLLUP creation require SUMMARIZED.
- FROM intervals must be larger integer multiples of the source interval, with matching extension attributes and aggregation modes.
- WAKEUP must be positive, no greater than the aggregation interval, and divide it evenly.
- Custom is Standard-only and requires one source TAG and a precreated target TAG.
  Put WHERE inside SELECT. Direct BASETIME predicates, JOIN, and FROM subqueries are disallowed.
- IF NOT EXISTS skips creation for an existing name; it does not modify, compare, or reconcile
  definitions. It does not bypass all syntax and source validation.

<a id="drop-rollup"></a>

## Deletion

```sql
DROP ROLLUP rollup_name;
```

Drop higher-level ROLLUPs that reference others first. Dropping a Custom target TAG is rejected
while related jobs remain. Before using CASCADE on the source TAG, check which related ROLLUPs
will be removed. Manage user Custom target tables with their own lifecycle.

<a id="alter-rollup"></a>

## Control

```sql
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name WAKEUP;
ALTER ROLLUP rollup_name FORCE;
ALTER ROLLUP rollup_name SET WAKEUP INTERVAL 10 SEC;
```

These commands require existing jobs and valid interval conditions.
Jobs start automatically at creation. Repeating an already-started/stopped state may cause an error.
WAKEUP returns without waiting for completion; FORCE waits for the target to catch up with its
source processing range.
For historical source corrections, check [REBUILD's separate support scope](../rollup-rebuild-syntax/).

## Queries and Candidate Selection

```text
rollup(time_unit, period, basetime_column [, origin])
```

Return type: DATETIME. period must be a positive integer literal. Do not assume an ordinary
DATE_TRUNC + GROUP BY query switches automatically merely because a ROLLUP exists. Specify
rollup() for ROLLUP queries; use a separate source-data query if no candidate applies.

Automatic selection first looks for unconditional candidates matching column, path, and mode,
then selects the largest usable interval. Equal intervals are affected by registration order.
Do not infer priority from ordinary/extended status alone. Use ROLLUP_TABLE to fix the dataset.

SEC/MIN candidate intervals are checked against period seconds/minutes. HOUR, DAY, WEEK, MONTH,
and YEAR use period hours during candidate selection. This rule is separate from calendar
calculation of result buckets. For month/year origins, check the first-day-of-month requirement.

For per-tag aggregation returning name, also include name in GROUP BY.
Match time range, origin, NULL handling, and candidate predicates before comparing source results.
Ordinary numeric ROLLUP supports MIN/MAX/SUM/COUNT/AVG/SUMSQ; extended ROLLUP adds FIRST/LAST.
Distinguish source-data FIRST/LAST usage from stored ROLLUP extension requirements.
Whole-document JSON COUNT and per-path counts have separate contracts.

For runnable creation, query, and error examples, see [Chapter 6: Using ROLLUP](/dbms/tag-rollup-usage/)
and [Query Syntax](/dbms/tag-rollup-usage/query-syntax-rollup/).
