---
title: '5.11 TAG Data UPDATE and Correction'
weight: 110
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="correction-performance-bulk-considerations-tag-data-update"></a>

## TAG data UPDATE range and bulk correction performance

TAG data UPDATE can directly correct time-series rows. Keep the target range
explicit with tag selection and BASETIME conditions.

### Basic pattern

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

<a id="design-correction-tag"></a>

## TAG correction design

TAG time-series rows can be corrected with `UPDATE`. When audit history or
query-time correction logic is required, combine direct UPDATE with correction
columns or a separate correction log table.

```sql
UPDATE sensor_data
   SET raw_value = 25.3,
       is_corrected = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

The UPDATE must include a tag selector and a BASETIME condition. `name` and
`time` themselves cannot be changed. Rebuild affected rollups when corrected
intervals are served from rollup data.
