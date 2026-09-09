---
type: docs
title: '16.6.4 TAG Data UPDATE Support'
weight: 40
toc: true
---

Modify the actual time-series data in TAG tables with `UPDATE table_name SET ... WHERE ...`.
This page lists allowed WHERE predicates and SET targets for TAG data UPDATE.
Use the separate `UPDATE ... METADATA` syntax to modify metadata.

<span class="badge-since">Available since Machbase 8.7.0</span>

TAG data UPDATE is supported only on logical TAG tables in Standard Edition. Cluster Edition and
direct UPDATE on internal raw component tables are not supported.

## WHERE Predicate Support

TAG data UPDATE requires one tag selection predicate and one or more BASETIME axis predicates.

| WHERE Predicate | Support | Notes |
|-----------|:---:|------|
| `name = 'tag-01'` | O | Select one tag |
| `name = ?`, `name = :tag_name` | O | Select one tag with a positional/named bind |
| `? = name`, `:tag_name = name` | O | Reversed equality is supported; column-on-left form is recommended |
| `name IN ('tag-01', 'tag-02')` | O | Literal/bind lists supported; subquery `IN` is not supported |
| `name LIKE 'tag-%'` | O | Expand to tags matching the pattern |
| `time = t1` | O | BASETIME equality predicate |
| `time = ?`, `time = :base_time` | O | Specify base time with a positional/named bind |
| `? = time`, `:base_time = time` | O | Reversed equality supported |
| `time BETWEEN t1 AND t2` | O | Both endpoints inclusive |
| `time >= t1 AND time < t2` | O | Combinations of `>`, `>=`, `<`, and `<=` supported |
| `time >= ? AND time < ?` | O | Bind markers supported for range bounds |
| One-sided time predicate | O | For example, `time >= t1` |
| Data column predicate | O | For example, `value > 100`, combined with tag/time predicates |
| UPDATE without predicates | X | Updating all TAG data is not allowed |
| Time predicate without tag selection | X | Target tags must be specified |
| Tag predicate without a time predicate | X | A BASETIME range must be specified |
| `OR` predicate | X | Not allowed in TAG data UPDATE predicates |
| Subquery/aggregate expression | X | Cannot determine UPDATE targets |
| Tag/axis columns wrapped in functions or expressions | X | Tag selectors and BASETIME predicates must reference columns directly |

Bind parameters replace values only. They do not change the required tag and BASETIME predicates,
allowed predicate structure, or SET targets. Reexecuting a prepared statement selects targets
using the latest bind values. If no rows match, it succeeds with `0` affected rows.

## SET Target Support

| SET Target | Support | Notes |
|---------|:---:|------|
| Data column | O | User data columns such as `value` and auxiliary columns |
| `SUMMARIZED` data column | O | Updates original TAG data |
| Multiple data columns | O | Can be specified in the same UPDATE |
| `name` (PRIMARY KEY) | X | Tag names cannot be changed |
| `time` (BASETIME) | X | The time axis column cannot be changed |
| Metadata column | X | Use `UPDATE table_name METADATA SET ...` |
| Hidden/system column | X | Internal columns cannot be UPDATE targets |

SET expressions may use constants, bind variables, arithmetic, functions, `CASE`, and string
concatenation without existing row column references, and NULL if column constraints allow it.
SET right-hand expressions cannot reference existing row columns, subqueries, or aggregates.


## Canonical References

For execution syntax and parameter metadata, see
[TAG Data UPDATE](../../sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind).
For marker APIs by SDK, see
[Named Bind Parameters](../../sql/syntax/named-bind-parameter-syntax/).
For diagnosis, see
[TAG Constraints and Troubleshooting](../../../tag-table-usage/constraints-errors-troubleshooting/).
