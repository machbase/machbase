---
type: docs
title: 'SAMPLING hint'
weight: 10
toc: true
---

The SAMPLING hint extracts data at a specified rate.
SamplingRate is a floating-point value; 1 means 100% of the data.

## Syntax

```sql
SELECT /*+ SAMPLING(SamplingRate) */ col1, col2, ...
  FROM table_name
 WHERE ...;
```

| Parameter | Description |
|----------|------|
| `SamplingRate` | Floating-point sampling fraction |

Multiply SamplingRate by 100 to express it as a percentage.

| SamplingRate | Sampling Percentage |
|--------------|-----------|
| `1` | 100% (all data) |
| `0.01` | 1% |
| `0.0001` | 0.01% |
| `0.00001` | 0.001% |

## Examples

```sql
-- Sample 1% from a range capped at 100,000 matching rows
SELECT /*+ SAMPLING(0.01) */ t_name, time, value
  FROM tag
 WHERE t_name = 'TAG_99'
 LIMIT 100000;
```

## Notes

- SamplingRate is a sampling fraction, not a time interval or result row count.
- Row counts may vary per execution; an exact count corresponding to the rate is not guaranteed.
- Small datasets or low rates may return zero rows.
- With LIMIT as above, sampling applies within the row range capped by LIMIT.
  For example, SAMPLING(0.5) with LIMIT 1000 samples about 50% of up to 1,000 rows when enough
  matching data exists. It does not fill the sampled result to 1,000 rows.

## Related Documentation

- [SELECT Hint Syntax](../) — Complete hint list
- [ROLLUP Syntax](../../rollup-syntax/) — Exact time-unit aggregation
