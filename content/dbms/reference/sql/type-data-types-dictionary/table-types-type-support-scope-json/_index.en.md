---
type: docs
title: '17.1.2.1 JSON Type Support by Table Type'
weight: 10
toc: true
---

This page summarizes JSON type support by table type.

| Table type | JSON column | JSON path query | JSON primary key | Notes |
|------------|:-----------:|:---------------:|:----------------:|-------|
| TAG | O | O | X | JSON can be used as a value/metadata column according to TAG rules |
| LOG | O | O | X | Use regular JSON functions and operators |
| LOOKUP | O | O | X | JSON is supported as a regular column; no JSON path index |
| VOLATILE | X | X | X | JSON columns are not supported |
| RDB | O | O | X | Use regular JSON functions and operators |

For LOOKUP tables, write JSON path literals with single quotes and use typed
extraction functions for numeric comparisons.

```sql
SELECT id
FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```
