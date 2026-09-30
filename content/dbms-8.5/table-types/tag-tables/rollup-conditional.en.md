---
title: 'Conditional Rollup for Filtering Noise'
type: docs
weight: 61
---

## Overview

Real-world time-series data often contains a mix of normal values and outliers. **Conditional rollup (filtered rollup)** lets you aggregate only rows that match a predicate, so your rollup statistics stay clean and consistent.  
This page walks through an example based on a real regression test scenario: **create rollups → load data → validate results → apply in production**.

> The SQL examples in this document use the same content as `extension.tc`, which is used for regression testing.  
> See the full SQL at [extension.tc sample SQL](../rollup-conditional-extension.tc/).

## When should you use conditional rollup?

- Outliers caused by sensor or communication errors distort your aggregates (MAX, AVG, etc.)
- Only rows with a certain flag (for example, `value2=0` for normal) should be counted in reports
- You want separate rollups for monitoring vs. reporting

Compared with adding `WHERE` clauses at query time, a conditional rollup is more stable.  
Because the aggregation table is built with the condition already applied, it gives you **pre-cleaned statistics of consistent quality, quickly**.

---

## 1) Example table and column meanings

In this example, `value` is the metric to aggregate, and `value2` is a flag that separates normal values from outliers:

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

- `_tag_rollup_custom_3` is the **filtered minute rollup**, which reflects only normal data.
- The `WHERE` clause is applied to raw rows before aggregation.
- Columns used in the predicate (like `value2`) are **not stored** in the rollup table.

> `FIRST()` and `LAST()` require **EXTENSION rollups**.

---

## 3) Sample data (including outliers)

Rows with `value2=1` are mixed in so that you can see the effect of the conditional rollup. The sample data below is taken directly from `extension.tc`.

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

The outlier values are far outside the normal range, so they strongly affect the aggregation results.

---

## 4) Force rollup execution for testing

In a test environment, force rollup processing so that the timing is fixed:

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

Even if a filtered rollup exists, the optimizer automatically **prefers an unfiltered rollup** when multiple candidates match.  
That means that without a hint, your query might silently ignore the filtered rollup.

Use the hint when:

- You must verify the filtered rollup result exactly
- Multiple rollups share the same interval/value column and you need a specific one
- You use `FIRST()`/`LAST()` and must point to an **EXTENSION** rollup

Think of the hint as a **safety switch**: it guarantees the rollup you intended is actually used.

---

## 7) Example summary (raw vs. filtered)

The table below summarizes only the key per-minute statistics for the `extension.tc` data.

**Counts and min/max:**

| Minute (rollup) | Raw COUNT | Raw MIN | Raw MAX | Filtered COUNT | Filtered MIN | Filtered MAX |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 | 7 | 99 | 9900 | 6 | 99 | 130 |
| 00:01 | 6 | 92 | 2990 | 5 | 92 | 102 |
| 00:02 | 6 | 110 | 66160 | 5 | 110 | 180 |

Key takeaways:

- **Raw aggregates inflate MAX** because outliers are included.
- **Filtered rollup keeps statistics stable** by reflecting only normal data.

### FIRST/LAST examples

`FIRST()` and `LAST()` return the first and last values of each bucket, and they require an **EXTENSION rollup**.  
The table below shows actual per-minute FIRST/LAST results. Each cell lists the matching time together with the value, but the functions return only the value.

| Minute (rollup) | Raw FIRST(time, value) | Raw LAST(time, value) | Filtered FIRST(time, value) | Filtered LAST(time, value) |
|---|---|---|---|---|
| 00:00 | 00:00:00, 100 | 00:00:50, 99 | 00:00:00, 100 | 00:00:50, 99 |
| 00:01 | 00:01:00, 98 | 00:01:50, 102 | 00:01:00, 98 | 00:01:50, 102 |
| 00:02 | 00:02:00, 110 | 00:02:50, 180 | 00:02:00, 110 | 00:02:50, 180 |

In this dataset, outliers do not sit on the bucket boundaries, so FIRST/LAST stays the same.  
In real workloads, outliers can sit on the boundaries, so **a conditional rollup can change FIRST/LAST values as well**.

---

## 8) Practical deployment flow

In practice, conditional rollups are applied with the following flow.

1. **Ingest**: record a quality flag (`value2`) together with the raw data from sensors or logs.
2. **Maintain two rollups**: keep a general rollup (all data) and a filtered rollup (normal data) side by side.
3. **Dashboards**: use general rollups for fast monitoring of all data.
4. **Reports/KPIs**: use the filtered rollup, fixed with a hint.
5. **Root-cause analysis**: query the raw data directly when investigating outliers.

This gives you **fast analytics and reliable statistics** without sacrificing detail.

---

## Summary

- A conditional rollup is a practical way to **stabilize statistics when outliers are mixed in**.
- The hint is **required to reliably select** the conditional rollup.
- In production, running general and conditional rollups side by side to **separate monitoring from analysis** works well.

---

## Related Documentation

- [Rollup Tables](../rollup-tables/)
- [SELECT Hint: ROLLUP_TABLE](../../../sql-reference/select-hint/)
