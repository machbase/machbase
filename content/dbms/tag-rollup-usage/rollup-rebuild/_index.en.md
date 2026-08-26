---
type: docs
title: '6.10 ROLLUP_REBUILD'
weight: 100
toc: true
aliases:
  - /dbms/tag-rollup-usage/delete-partial-rebuild-rollup/
---

Recalculate ROLLUP values for a corrected TAG and time range. `ROLLUP_REBUILD` is available only in
Standard Edition.

## Choose rebuild or recreation

| Situation | Start with |
|---|---|
| A bounded historical range for a few tags | `ROLLUP_REBUILD` |
| A changed ROLLUP definition | Drop and create the ROLLUP with the new definition |
| An unknown affected range | Determine raw-data and query impact first |
| Cluster Edition | Use an approved recovery procedure; rebuild is unsupported |

## Execute and verify

```sql
EXEC ROLLUP_REBUILD(
    sensor_tag,
    'sensor-01',
    TO_DATE('2026-01-01 00:00:00'),
    TO_DATE('2026-01-02 00:00:00')
);

SHOW ROLLUPGAP;
```

Compare bucket count, boundaries, `COUNT`, `MIN`, `MAX`, and `AVG` with an identical raw-data range.
If results still differ, follow [ROLLUP troubleshooting](/dbms/troubleshooting/rollup/) before
repeating the command.

Use [ROLLUP syntax](/dbms/reference/sql/syntax-dictionary-sql/rollup-syntax/) when changing interval,
condition, source, or EXTENSION attributes.
