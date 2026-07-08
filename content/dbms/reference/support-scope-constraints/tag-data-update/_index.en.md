---
type: docs
title: 'TAG data UPDATE support matrix'
weight: 40
---

TAG time-series rows can be updated with `UPDATE table_name SET ... WHERE ...`.
Metadata columns are updated with the separate `UPDATE ... METADATA` syntax.

## WHERE support

TAG data UPDATE requires both a tag selector and a BASETIME condition.

| WHERE condition | Supported | Notes |
|-----------------|:---------:|-------|
| `name = 'tag-01'` | O | Single tag |
| `name IN ('tag-01', 'tag-02')` | O | Literal/bind lists only; `IN (SELECT ...)` is not supported |
| `name LIKE 'tag-%'` | O | Expands to matching tag names |
| `time = t1` | O | BASETIME equality |
| `time BETWEEN t1 AND t2` | O | Inclusive range |
| `time >= t1 AND time < t2` | O | `>`, `>=`, `<`, `<=` combinations are supported |
| One-sided time condition | O | For example, `time >= t1` |
| Data-column predicate | O | For example, `value > 100`, together with tag/time conditions |
| UPDATE without WHERE | X | Whole-table TAG data UPDATE is not allowed |
| Time condition without tag selector | X | Target tags must be selected |
| Tag selector without time condition | X | A BASETIME condition is required |
| `OR` condition | X | Not allowed in TAG data UPDATE conditions |
| Subquery, aggregate, volatile predicate | X | Not allowed when selecting the update target |

## SET target support

| SET target | Supported | Notes |
|------------|:---------:|-------|
| Data column | O | `value` and user-defined data columns |
| `SUMMARIZED` data column | O | Updates the raw TAG rows |
| Multiple data columns | O | Can be assigned in one UPDATE statement |
| `name` (PRIMARY KEY) | X | Tag names cannot be changed |
| `time` (BASETIME) | X | The time axis cannot be changed |
| Metadata column | X | Use `UPDATE table_name METADATA SET ...` |
| Hidden/system column | X | Internal columns are not update targets |

SET expressions can use constants, row-local column references, arithmetic, `CASE`,
string concatenation, and NULL values when the column definition allows them.

## Examples

```sql
UPDATE sensor_data
   SET value = value + 10,
       status = status + 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_data
   SET note = 'checked'
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 100;
```

Before a large UPDATE, run a `SELECT COUNT(*)` with the same WHERE clause. If the
updated interval is served from rollup tables, rebuild the affected rollups with
`ROLLUP_REBUILD`.
