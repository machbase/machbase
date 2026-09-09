---
type: docs
title: '16.6.6 ROLLUP Support'
weight: 60
toc: true
aliases:
  - /dbms/tag-rollup-usage/support-scope-rollup/
---

<a id="support-scope-rollup-rebuild-cluster"></a>

## Edition and Table Scope

| Feature | Standard | Cluster |
|---|:---:|:---:|
| Create, query, and control ordinary, conditional, and extended ROLLUPs on time-axis TAG tables | O | O |
| Automatic creation with WITH ROLLUP | O | O |
| Supported JSON path and whole-document aggregation | O | O |
| Custom INTO...AS | O | X |
| ROLLUP_REBUILD | Supported for limited targets and arguments | X |

Time-axis ROLLUP does not apply to distance-axis TAG, LOG, TRANSACTION, VOLATILE, or LOOKUP tables.
In Cluster Edition, check status by relevant node and hierarchy level.

## Creation Types and Columns

| Type | Requirements |
|---|---|
| Ordinary numeric | Supported numeric DATA column; SUMMARIZED is not required for explicit creation |
| JSON path | JSON DATA column and a numeric path to aggregate |
| Whole JSON document | JSON SUMMARIZED column |
| WITH ROLLUP | Third SUMMARIZED column of a time-axis TAG table |
| FROM hierarchy | A larger integer-multiple interval with matching extension and mode conditions |
| Custom | One source time-axis TAG table and a precreated compatible target TAG table |

## Aggregation and Selection

Ordinary numeric ROLLUP provides MIN/MAX/SUM/COUNT/AVG/SUMSQ; extended ROLLUP also provides
FIRST/LAST. Users must reaggregate partial Custom results. Combine averages using sums and valid
counts, and preserve corresponding timestamps when combining FIRST/LAST.
Whole-document JSON COUNT is the stored aggregate count and need not equal the original COUNT(value).

Candidate selection depends on predicates, columns, paths, mode, and interval. Do not infer priority
from ordinary/extended status alone or assume a 24 HOUR ROLLUP automatically applies to daily buckets.
Check the [query rules](../../../tag-rollup-usage/query-syntax-rollup/).

## REBUILD Scope Differs from Creation Scope

REBUILD targets complete automatic SEC/MIN/HOUR hierarchies and supported Custom paths. It cannot
rebuild every configuration that can be created, such as arbitrary manual names, partial automatic
hierarchies, or 10 MIN Custom rollups.
Custom time-boundary processing currently supports 1 SEC, 1 MIN, and 1 HOUR and must match SELECT buckets.
For constant time arguments, expansion to whole buckets, state transitions, and checks after errors,
follow the [REBUILD Reference](../../sql/syntax/rollup-rebuild-syntax/).

## Privileges

Grant the operational account database access and required creation, deletion, and query privileges.
The following example grants create/drop privileges to an existing account; it does not
configure every required privilege in one script.

```sql
GRANT CREATE, DROP ON DATABASE MACHBASEDB TO rollup_user;
```

Check ownership and operation scope in
[Privilege Management](../../../security-access-control/privileges/).
