---
type: docs
title: '6.1 ROLLUP Overview and Use Criteria'
weight: 10
toc: true
---

ROLLUP reduces the cost of repeatedly aggregating raw rows. It is neither a source-retention policy
nor a cache for arbitrary query results, and it cannot reconstruct source information absent from
the aggregates.

<a id="original-85-rollup-tables"></a>
<a id="rollup"></a>

## Use Criteria

| Requirement | Approach to consider |
|---|---|
| Repeated interval statistics for one numeric column | General ROLLUP |
| Aggregate only samples meeting quality conditions | Conditional ROLLUP |
| First and last values within an interval | EXTENSION ROLLUP |
| Store multiple aggregate expressions in a separate TAG | Custom ROLLUP (Standard Edition only) |
| Aggregate numeric values in JSON paths or documents | JSON path or full-document ROLLUP |
| Distance-axis TAG | Ordinary numeric interval aggregation; ROLLUP unsupported |

SUMMARIZED is not required when explicitly creating a ROLLUP on an ordinary numeric column. WITH
ROLLUP automatic creation and full-document JSON aggregation have separate SUMMARIZED requirements.
See [Creation Syntax](../create-delete-rollup/).

## Basic Exercise

### 1. Create and Insert

```sql
CREATE TAG TABLE ch6_basic (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_basic_ru ON ch6_basic(value) INTERVAL 1 MIN;
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
```

### 2. Check the Completed Aggregation Range

```sql
EXEC TABLE_FLUSH(ch6_basic);
ALTER ROLLUP ch6_basic_ru FORCE;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP is a machsql command. SDKs should use supported SQL queries such as V$ROLLUP.
TABLE_FLUSH processes storage buffers; FORCE catches up the named ROLLUP's processing range. It does
not complete processing for future arrivals during continuous ingestion.

### 3. Compare with Source Data

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       COUNT(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_basic
 WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('min', 1, time) AS bucket,
       COUNT(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_basic
 WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

| Bucket | COUNT(value) | MIN | MAX | AVG |
|---|---:|---:|---:|---:|
| 2026-01-01 00:00:00 | 2 | 10 | 20 | 15 |
| 2026-01-01 00:01:00 | 1 | 30 | 30 | 30 |

Both queries should return the same results. A DATE_TRUNC aggregation on source data does not
automatically switch simply because a ROLLUP exists. Specify `rollup()` explicitly in ROLLUP
queries.

### 4. Clean Up

```sql
DROP ROLLUP ch6_basic_ru;
DROP TABLE ch6_basic;
```

## Before Adoption

Define representative tag counts, ingestion volume, query frequency, and acceptable aggregation lag.
Determine the finest required interval and source retention first, then continue to
[Hierarchy Design](../target-tag-table-design/). Measure long-period performance with
production-like data rather than extrapolating from this small sample.
