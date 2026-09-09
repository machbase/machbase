---
type: docs
title: '6.5 Conditional ROLLUP'
weight: 50
toc: true
---

<a id="original-85-rollup-conditional"></a>

## Filter Source Rows Before Aggregation

Conditional ROLLUP maintains statistics for source rows meeting quality or state conditions. This
differs from removing bad samples from an already computed average. The quality column used by the
predicate is not itself retained in the aggregate result.

## 1. Prepare the Table and Two ROLLUPs

```sql
CREATE TAG TABLE ch6_condition (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_condition_all
  ON ch6_condition(value) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_condition_good
  ON ch6_condition(value) INTERVAL 1 MIN EXTENSION WHERE quality = 1;
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
INSERT INTO ch6_condition VALUES
    ('TEMP_01', TO_DATE('2026-01-01 00:00:50', 'YYYY-MM-DD HH24:MI:SS'), 90.0, 0);
EXEC TABLE_FLUSH(ch6_condition);
ALTER ROLLUP ch6_condition_all FORCE;
ALTER ROLLUP ch6_condition_good FORCE;
```

## 2. Compare the Source Predicate and ROLLUP

```sql
SELECT DATE_TRUNC('minute', time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition
 WHERE name = 'TEMP_01' AND quality = 1
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_condition_good) */
       rollup('min', 1, time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_condition_all) */
       rollup('min', 1, time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

| Bucket and set | COUNT | AVG | MIN | MAX | FIRST | LAST |
|---|---:|---:|---:|---:|---:|---:|
| 00:00, all rows | 3 | 40 | 10 | 90 | 10 | 90 |
| 00:00, quality=1 | 2 | 15 | 10 | 20 | 10 | 20 |
| 00:01, both sets | 1 | 30 | 30 | 30 | 30 | 30 |

The bad sample is last in its interval, so LAST also differs. FIRST/LAST return the selected value,
not a timestamp/value pair.

## Explicit Candidate Selection

This example uses hints to fix the result sets for all samples and valid samples. Automatic
selection favors unconditional candidates, but can select filtered statistics when only conditional
candidates exist. Do not interpret this as conditional ROLLUP always being ignored or EXTENSION
always requiring a hint.

<a id="rollup-conditional-extension-tc"></a>
<a id="original-85-rollup-conditional-extension"></a>
<a id="condition-conditional-rollup"></a>

## Syntax and Constraints

For general ROLLUP, place the filter in WHERE after INTERVAL and EXTENSION. Comparisons, BETWEEN,
IN, LIKE, logical operations, and supported scalar functions are allowed. Subqueries, aggregate
functions, and predicates on the tag-name PRIMARY KEY are unsupported. Custom uses WHERE inside
SELECT; do not mix these syntax forms.

## Check Status and Clean Up

```sql
SELECT DISTINCT ROLLUP_NAME, PREDICATE, ENABLED
  FROM V$ROLLUP WHERE ROOT_TABLE = 'CH6_CONDITION';
DROP ROLLUP ch6_condition_good;
DROP ROLLUP ch6_condition_all;
DROP TABLE ch6_condition;
```

When business quality criteria change, update both the predicate and reaggregation plan. Existing
aggregates do not automatically adopt the new predicate. See [Control](../ingestion-control-rollup/)
and [Rebuild Scope](../rollup-rebuild/).
