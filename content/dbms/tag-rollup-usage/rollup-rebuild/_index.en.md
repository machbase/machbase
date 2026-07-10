---
title: '6.15 ROLLUP_REBUILD'
weight: 140
toc: true
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="validation-policy-tag-data-update-stat-index-rollup"></a>

## TAG data UPDATE impact on statistics, indexes, and rollups

TAG data UPDATE changes the raw TAG rows. Statistics and data indexes are handled
for the updated rows, but materialized rollup rows may need an explicit rebuild.

### Affected structures

#### Raw TAG rows

`UPDATE tag SET value = ... WHERE name ... AND time ...` updates data columns in
the raw rows that match the WHERE clause.

#### Statistics and indexes

`SUMMARIZED` data columns and data-partition indexes are maintained for the
updated rows. For large updates, narrow the target with tag and time conditions.

#### Rollups

When rollup rows already exist for the corrected interval, rebuild the affected
rollup with `ROLLUP_REBUILD` before relying on rollup-query results.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, 'TEMP-01',
    TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

### Verification flow

1. Check the target row count with the same WHERE clause.
2. Run the UPDATE.
3. Verify the corrected values from the raw TAG table.
4. Rebuild affected rollups if rollup queries cover the corrected interval.

<a id="original-85-rollup-rebuild"></a>

## ROLLUP Rebuild

English structure placeholder. Korean content is authoritative for this restructuring pass.

<a id="correction-abnormal-data-rollup-rebuild"></a>

## 이상 데이터 정정 후 ROLLUP Rebuild
