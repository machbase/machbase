---
type: docs
title: '4.3 Data Mutation Policy'
weight: 30
toc: true
---

Support for `UPDATE`, `DELETE`, and `TRUNCATE` differs by table type. This page summarizes
policies relevant to data model selection. Use the linked SQL references for exact syntax
and restrictions.

A mutation policy defines who may change which data and what can be rolled back on failure,
not just whether a value is editable. Treat current-state updates, raw measurement corrections,
schema changes, and retention-based deletion as separate operations.

## Data mutation support by table type

| Table type | UPDATE | DELETE | TRUNCATE |
|------------|--------|--------|----------|
| TAG | DATA correction in Standard: requires tag selection and BASETIME predicates | `BEFORE`, tag/axis predicates, or all rows | No |
| LOG | No | `BEFORE`, `OLDEST`, `EXCEPT`, or all rows | Yes |
| TRANSACTION | Yes | Yes | Yes |
| VOLATILE | Primary-key predicate | Primary-key predicate or all rows | No |
| LOOKUP | General predicates; cannot change the PK | General predicates or all rows | No |

LOG tables are designed to preserve ingested events without updating them. Store frequently
modified state or configuration in VOLATILE, LOOKUP, or TRANSACTION tables.

## Mutation units and failure handling

| Operation | Design decision |
|---|---|
| Update current settings | Key, allowed values, and concurrent-writer handling |
| Correct inaccurate measurements | Tag/time range, reason, and ROLLUP recalculation |
| Correct a LOG event | Whether to retain the original and link a correction event |
| Replace a reference key | Reference migration order and intermediate failure handling |
| Delete a period | Retention cutoff, deletion scope, and required backups |

Multiple TRANSACTION DML statements can share an explicit transaction. Do not assume LOOKUP
or VOLATILE changes or LOG or TAG ingestion participate in that transaction. For example,
TAG history may remain after a subsequent VOLATILE cache update fails. Prepare cache rebuilding
or retry procedures. Append transaction participation depends on the API and target type;
check [SDK Support Scope](/dbms/development-tools-integration/sdk-support-scope/).

Before changing multiple rows, query the count and representative rows with the same
predicates. This precheck does not lock rows or fix the later mutation scope. With concurrent
ingestion or updates, also control the operation window and target range. Verify the affected
row count and resulting values afterward.

<a id="policy-update"></a>

## UPDATE policy

### TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION supports general relational `UPDATE` and transactions.
- VOLATILE selects targets through primary-key equality predicates.
- LOOKUP supports general predicates, but its primary-key column cannot be changed.

LOOKUP UPDATE requires a WHERE clause. Changing a LOOKUP or VOLATILE primary key requires
separate delete and insert statements. First define how to preserve the original and switch
references. If both statements must be rolled back together, consider TRANSACTION.

For supported LOOKUP predicates and expressions, see
[LOOKUP Predicate UPDATE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-update-syntax/).

<a id="policy-update-policy-tag-data-update"></a>
<a id="policy-update-distinction-tag-data-update-metadata"></a>
<a id="policy-update-tag-data-update-where-set-standard-only"></a>

### TAG data UPDATE

TAG time-series data and metadata use different update syntax.

| Target | Syntax | Key restriction |
|------|------|-----------|
| Time-series data | `UPDATE tag_table SET ... WHERE ...` | Requires both tag selection and BASETIME predicates |
| Metadata | `UPDATE tag_table METADATA SET ...` | Uses TAG-specific metadata syntax |

TAG data UPDATE is supported on logical TAG tables in Standard Edition. Tag names, BASETIME,
and metadata columns cannot be SET targets. If materialized rollups cover the changed range,
regenerate them with `ROLLUP_REBUILD`.

The right-hand side of TAG DATA `SET` cannot reference existing row columns. Do not apply
corrections with expressions such as `SET value = value + 1`. Pass calculated values as
constants or parameters and limit the affected range. If correction history is required,
store before/after values and reasons separately rather than only overwriting the current value.

The following references define syntax and allowed expressions:

- [TAG Data UPDATE](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/)
- [TAG Data UPDATE WHERE/SET Constraints](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-where-set-constraints/)
- [TAG Metadata](/dbms/tag-table-usage/tag-metadata/)

LOG tables do not support `UPDATE`.

<a id="policy-delete"></a>

## DELETE policy

### TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION supports deletion with general `WHERE` predicates.
- VOLATILE supports primary-key deletion or deletion of all rows without a predicate.
- LOOKUP supports general predicates or deletion of all rows without `WHERE`.

For supported LOOKUP predicates, see
[LOOKUP Predicate DELETE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-delete-syntax/).

### LOG

LOG uses retention-oriented deletion syntax instead of arbitrary `WHERE` predicates. Choose
`OLDEST`, `EXCEPT`, `BEFORE`, or deletion of all rows according to the purpose. For exact syntax
and examples, see [LOG Data Lifecycle](/dbms/log-table-usage/operations-lifecycle/).

<a id="condition-tag-kv-delete-before"></a>

### TAG/KV

TAG/KV can remove old data with `BEFORE` or select targets through tag names and axis predicates.
The `BEFORE` timestamp must be earlier than the current time. For syntax, see
[TAG Data Mutation](/dbms/tag-table-usage/data-input-mutation/).

For recurring retention-based deletion, use a
[Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/).

<a id="delete-tag-metadata"></a>
<a id="policy-delete-delete-tag-metadata"></a>

### TAG metadata

Delete TAG metadata with `DELETE FROM table_name METADATA`. If any selected tag still has
actual data, the entire statement fails.

For detailed conditions, see [TAG Metadata](/dbms/tag-table-usage/tag-metadata/).

<a id="policy-truncate"></a>

## TRUNCATE policy

`TRUNCATE TABLE` is supported only for LOG and TRANSACTION. It removes all rows while
retaining the schema and index definitions.

| Item | TRUNCATE | DELETE |
|------|----------|--------|
| Target | Entire table | All rows or selected rows, depending on type |
| `WHERE` | Not allowed | Allowed within the supported scope |
| TRANSACTION rollback | Possible in an explicit transaction | Possible in an explicit transaction |

Before deletion, check backups and reingestion paths. For TAG, use supported `BEFORE` or
tag/axis predicates. To clear VOLATILE or LOOKUP, use `DELETE` without predicates.

Do not apply TRANSACTION rollback guarantees to LOG deletion. Later ROLLBACK cannot undo
committed changes. Logical deletion and physical disk reclamation may occur at different
times; check storage usage and the table's reclamation state.
