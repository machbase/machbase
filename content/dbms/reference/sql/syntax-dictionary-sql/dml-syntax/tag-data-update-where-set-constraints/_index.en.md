---
type: docs
title: '17.1.1.10.2 TAG data UPDATE WHERE/SET constraints'
weight: 20
toc: true
---

TAG data UPDATE must have a clear target range. The WHERE clause requires both a
tag selector and a BASETIME condition, and the SET clause can target data columns
only.

<span class="badge-since">Supported since Machbase 8.7.0</span>

TAG data UPDATE is supported only for logical TAG tables in Standard Edition.

## SET constraints

| Column role | SET allowed | Notes |
|-------------|:-----------:|-------|
| Data column | O | `value` and user-defined data columns |
| `SUMMARIZED` data column | O | Updates the raw TAG rows |
| BASETIME column | X | The time axis cannot be changed |
| PRIMARY KEY column (`name`) | X | Tag names cannot be changed |
| Metadata column | X | Use `UPDATE ... METADATA` |
| Hidden/system column | X | Internal columns are not SET targets |

SET expressions can use constants, bind parameters, arithmetic, string expressions,
`CASE`, and supported conversion functions when they do not reference an existing row
column. Row-column references, subqueries, and aggregate expressions are not allowed on
the SET right-hand side.

## WHERE constraints

| WHERE condition | Supported |
|-----------------|:---------:|
| `name = '...'` | O |
| `name = ?`, `name = :tag_name` | O |
| `? = name`, `:tag_name = name` | O |
| `name IN ('...', '...')` | O |
| `name LIKE '...'` | O |
| `time = t1` | O |
| `time = ?`, `time = :base_time` | O |
| `? = time`, `:base_time = time` | O |
| `time BETWEEN t1 AND t2` | O |
| `time >= t1 AND time < t2` | O |
| `time >= ? AND time < ?` | O |
| One-sided time condition | O |
| Data-column predicate | O |
| No tag selector | X |
| No time condition | X |
| `OR` condition | X |
| `IN (SELECT ...)` | X |

Bind markers replace condition values only. They cannot replace the tag-name or
BASETIME column, and both required condition classes remain mandatory. Reexecuting a
prepared statement selects rows with the latest bind values. A no-match execution
succeeds with affected rows `0`.

See [TAG data UPDATE predicate binds](../tag-data-update-syntax/#tag-data-update-predicate-bind)
and [Named bind parameters](../../named-bind-parameter-syntax/) for parameter metadata
and SDK APIs.

Metadata UPDATE uses `UPDATE table_name METADATA SET ...` and modifies tag
attributes, not time-series rows.

## Related

- [TAG data UPDATE syntax](../tag-data-update-syntax/)
- [Named bind parameters](../../named-bind-parameter-syntax/)
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/)
