---
type: docs
title: '17.1.1.19 ROLLUP_REBUILD syntax'
weight: 190
toc: true
---

`ROLLUP_REBUILD` recalculates rollup data for a tag and time range after the raw
TAG data has been corrected.

> This procedure is supported in Standard Edition. Cluster Edition does not
> support `ROLLUP_REBUILD`.

## Syntax

```sql
EXEC ROLLUP_REBUILD(table_name, tag_name, start_time, end_time)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `table_name` | identifier | Source TAG table |
| `tag_name` | string | Tag name to rebuild |
| `start_time` | DATETIME expression | Rebuild start time |
| `end_time` | DATETIME expression | Rebuild end time |

## Example

```sql
UPDATE sensor_tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS');

EXEC ROLLUP_REBUILD(
    sensor_tag,
    'TEMP-01',
    TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
);
```

Use the minimum necessary time range. Rebuild can take longer for wide intervals.
