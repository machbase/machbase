---
title: 'Conditional Rollup for Filtering Noise'
type: docs
weight: 61
---

## Overview

Real-world time-series data often contains a mix of normal values and outliers. **Conditional rollup (filtered rollup)** lets you aggregate only rows that match a predicate, so your rollup statistics stay clean and consistent.  
This page walks through a regression-test based example: **create rollups → load data → validate results → apply in production**.

> The SQL in this document follows the same data used in `extension.tc`.  
> See the full SQL at [extension.tc sample SQL](../rollup-conditional-extension.tc/).

## When should you use conditional rollup?

- Outliers distort your aggregates (MAX, AVG, etc.)
- Only rows with a certain flag (for example, `value2=0`) should be counted
- You want separate rollups for monitoring vs. reporting

Compared with adding `WHERE` clauses at query time, a conditional rollup gives you **pre-cleaned statistics with consistent performance**.

---

## 1) Example table and column meanings

In this example, `value` is the metric to aggregate, and `value2` is a flag:

- `value2=0` means normal
- `value2=1` means outlier

```sql
CREATE TAG TABLE tag (
    name   VARCHAR(20) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DOUBLE SUMMARIZED,
    value2 DOUBLE
);
```

---

## 2) Define a rollup chain and add a filter

We create second/minute rollups, then add a **filtered rollup** at the minute level.

```sql
CREATE ROLLUP _tag_rollup_custom_1 ON tag(value) INTERVAL 1 SEC  EXTENSION;
CREATE ROLLUP _tag_rollup_custom_2 FROM _tag_rollup_custom_1 INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP _tag_rollup_custom_3 ON tag(value) INTERVAL 1 MIN EXTENSION WHERE value2 = 0;
```

- `_tag_rollup_custom_3` is the **filtered minute rollup**.
- The `WHERE` clause is applied to raw rows before aggregation.
- Columns used in the predicate (like `value2`) are **not stored** in the rollup table.

> `FIRST()` and `LAST()` require **EXTENSION rollups**.

---

## 3) Sample data (including outliers)

The sample data below is taken directly from `extension.tc`.

```sql
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:00', 100,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:10', 101,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:11', 130,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:20', 120,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:30', 110,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:40', 9900, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:50', 99,   0);

INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:00', 98,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:10', 94,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:20', 2990, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:30', 92,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:40', 99,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:50', 102, 0);

INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:00', 110, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:10', 120, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:20', 140, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:30', 66160, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:40', 170, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:50', 180, 0);
```

---

## 4) Force rollup execution for testing

To align test timing, force rollup processing:

```sql
EXEC ROLLUP_FORCE(_tag_rollup_custom_1);
EXEC ROLLUP_FORCE(_tag_rollup_custom_2);
EXEC ROLLUP_FORCE(_tag_rollup_custom_3);
```

---

## 5) Query and compare results

### 5-1. Normal aggregation (raw data)
```sql
SELECT rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

### 5-2. Force the filtered rollup with a hint
```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_custom_3) */
       rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

---

## 6) Why the hint is required

Even if a filtered rollup exists, the optimizer **prefers an unfiltered rollup** when multiple candidates match.  
That means your query might silently use the wrong rollup unless you force it.

Use the hint when:

- You must verify the filtered rollup result
- Multiple rollups share the same interval/value column
- `FIRST()`/`LAST()` requires an **EXTENSION** rollup

Think of the hint as a **safety switch**: it guarantees the rollup you intended is actually used.

---

## 7) Example summary (raw vs. filtered)

**Counts and min/max:**

| Minute (rollup) | Raw COUNT | Raw MIN | Raw MAX | Filtered COUNT | Filtered MIN | Filtered MAX |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 | 7 | 99 | 9900 | 6 | 99 | 130 |
| 00:01 | 6 | 92 | 2990 | 5 | 92 | 102 |
| 00:02 | 6 | 110 | 66160 | 5 | 110 | 180 |

Key takeaway:

- **Raw aggregates inflate MAX** because outliers are included.
- **Filtered rollup keeps statistics stable** by excluding outliers.

### FIRST/LAST examples

`FIRST()` and `LAST()` show the boundary values per bucket:

| Minute (rollup) | Raw FIRST(time, value) | Raw LAST(time, value) | Filtered FIRST(time, value) | Filtered LAST(time, value) |
|---|---|---|---|---|
| 00:00 | 00:00:00, 100 | 00:00:50, 99 | 00:00:00, 100 | 00:00:50, 99 |
| 00:01 | 00:01:00, 98 | 00:01:50, 102 | 00:01:00, 98 | 00:01:50, 102 |
| 00:02 | 00:02:00, 110 | 00:02:50, 180 | 00:02:00, 110 | 00:02:50, 180 |

In this dataset, outliers do not sit on the boundaries, so FIRST/LAST stays the same.  
In real workloads, boundary values can change, which is another reason to apply filtered rollups.

---

## 8) Practical deployment flow

1. **Ingest** raw data with a quality flag (`value2`)
2. **Maintain two rollups**: a general rollup and a filtered rollup
3. **Dashboards** can use general rollups
4. **Reports/KPIs** should use the filtered rollup with a hint
5. **Root-cause analysis** can still rely on raw data

This gives you **fast analytics and reliable statistics** without sacrificing detail.

---

## Related Documentation

- [Rollup Tables](../rollup-tables/)
- [SELECT Hint: ROLLUP_TABLE](../../../sql-reference/select-hint/)
