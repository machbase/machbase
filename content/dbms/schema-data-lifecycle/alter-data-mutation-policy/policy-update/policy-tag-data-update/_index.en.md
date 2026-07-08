---
type: docs
title: 'TAG data UPDATE policy'
weight: 10
---

TAG time-series rows can be updated under explicit target conditions. The UPDATE
must be limited by tag selection and the BASETIME column, and metadata updates use
a separate syntax.

## Policy

1. The WHERE clause must include a tag selector: `name =`, `name IN`, or `name LIKE`.
2. The WHERE clause must include a BASETIME condition.
3. SET targets must be data columns.
4. `name` (PRIMARY KEY), `time` (BASETIME), and metadata columns cannot be updated
   by TAG data UPDATE.

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

Metadata columns use `UPDATE ... METADATA`.

```sql
UPDATE tag METADATA
   SET location = 'zone-2'
 WHERE name = 'TEMP-01';
```

Before large corrections, verify the target row count with the same WHERE clause.
If rollup data is queried for the corrected interval, rebuild affected rollups
with `ROLLUP_REBUILD`.
