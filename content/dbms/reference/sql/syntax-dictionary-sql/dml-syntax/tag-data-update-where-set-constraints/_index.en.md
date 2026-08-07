---
type: docs
title: '18.1.1.10.2 TAG data UPDATE WHERE/SET constraints'
weight: 20
toc: true
---

TAG data UPDATE must have a clear target range. The WHERE clause requires both a
tag selector and a BASETIME condition, and the SET clause can target data columns
only.

## SET constraints

| Column role | SET allowed | Notes |
|-------------|:-----------:|-------|
| Data column | O | `value` and user-defined data columns |
| `SUMMARIZED` data column | O | Updates the raw TAG rows |
| BASETIME column | X | The time axis cannot be changed |
| PRIMARY KEY column (`name`) | X | Tag names cannot be changed |
| Metadata column | X | Use `UPDATE ... METADATA` |
| Hidden/system column | X | Internal columns are not SET targets |

SET expressions can use constants, row-local column values, arithmetic, string
expressions, `CASE`, and supported conversion functions. Subqueries and aggregate
expressions are not allowed on the SET right-hand side.

## WHERE constraints

| WHERE condition | Supported |
|-----------------|:---------:|
| `name = '...'` | O |
| `name IN ('...', '...')` | O |
| `name LIKE '...'` | O |
| `time = t1` | O |
| `time BETWEEN t1 AND t2` | O |
| `time >= t1 AND time < t2` | O |
| One-sided time condition | O |
| Data-column predicate | O |
| No tag selector | X |
| No time condition | X |
| `OR` condition | X |
| `IN (SELECT ...)` | X |

Metadata UPDATE uses `UPDATE table_name METADATA SET ...` and modifies tag
attributes, not time-series rows.
