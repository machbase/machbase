---
type: docs
title: '5.12.1 TAG data UPDATE range and bulk correction performance'
weight: 40
---

TAG data UPDATE can directly correct time-series rows. Keep the target range
explicit with tag selection and BASETIME conditions.

## Basic pattern

```sql
SELECT COUNT(*), MIN(value), MAX(value)
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2025-06-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2025-06-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_tag
   SET value = 99.5,
       corrected = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2025-06-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2025-06-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

For large corrections, split long intervals into batches, verify each batch with
`SELECT COUNT(*)`, and rebuild affected rollups with `ROLLUP_REBUILD` when rollup
queries need the corrected interval.
