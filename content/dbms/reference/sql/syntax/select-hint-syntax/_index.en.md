---
type: docs
title: 'SELECT hint'
weight: 40
toc: true
aliases:
  - /dbms/reference/sql/hint-dictionary-select/
---

SELECT hints use /*+ ... */ comment blocks to control optimizer behavior or specify processing such
as sampling.

## Hint Syntax

```sql
SELECT /*+ hint_clause */ ...
SELECT /*+ hint1 hint2 */ ...
```

Place hints in a /*+ ... */ block immediately after SELECT.

## Main Hints

### Execution Plan Hints

| Hint | Syntax | Description |
|------|------|------|
| `PARALLEL` | `/*+ PARALLEL(table, n) */` | Set parallelism factor |
| `NOPARALLEL` | `/*+ NOPARALLEL(table) */` | Disable parallel processing |
| `FULL` | `/*+ FULL(table) */` | Force a full scan instead of an index scan |
| `NO_INDEX` | `/*+ NO_INDEX(table, index) */` | Disable a specific index |
| `ROLLUP_TABLE` | `/*+ ROLLUP_TABLE(rollup_table) */` | Force a specific ROLLUP table |
| `RID_RANGE` | `/*+ RID_RANGE(table, start, end) */` | Specify an RID range |
| `SCAN_FORWARD` | `/*+ SCAN_FORWARD(table) */` | Scan oldest records first (LOG tables) |
| `SCAN_BACKWARD` | `/*+ SCAN_BACKWARD(table) */` | Scan newest records first (LOG tables) |

### Data Processing Hints

| Hint | Syntax | Description |
|------|------|------|
| `SAMPLING` | `/*+ SAMPLING(SamplingRate) */` | Sample using a floating-point rate |

## Examples

```sql
-- Parallel processing with 8 threads
SELECT /*+ PARALLEL(sensor_log, 8) */ sensor, AVG(value)
  FROM sensor_log
 WHERE ts BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
               AND TO_DATE('2024-01-31', 'YYYY-MM-DD')
 GROUP BY sensor;

-- Disable a specific index
SELECT /*+ NO_INDEX(sensor_log, idx_ts) */ *
  FROM sensor_log
 WHERE ts > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- Force a ROLLUP table
SELECT /*+ ROLLUP_TABLE(_rollup_tag_value_min) */
       name, rollup('min', 5, time) AS t, AVG(value)
  FROM tag
 WHERE name = 'TEMP-01'
 GROUP BY name, t;

-- Sample 1% from a range capped at 100,000 matching rows
SELECT /*+ SAMPLING(0.01) */ t_name, time, value
  FROM tag
 WHERE t_name = 'TAG_99'
 LIMIT 100000;
```

## Subsections

- [SAMPLING Hint](./sampling-hint/) — Rate-based sampling details

## Related Documentation

- [Query Performance Tuning](/dbms/performance-tuning/performance-query-tuning/) — Execution plans and hint selection
