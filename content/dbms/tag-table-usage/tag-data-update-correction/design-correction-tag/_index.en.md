---
type: docs
title: '5.12.2 TAG correction design'
weight: 110
---

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
