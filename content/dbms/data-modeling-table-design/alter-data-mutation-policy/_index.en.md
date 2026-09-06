---
type: docs
title: '4.3 Data Mutation Policy'
weight: 30
toc: true
---

Define not just whether a value can change, but which rows may change, which operations must commit
together, and how failures are handled. Current-state updates, measurement corrections, schema
changes, and retention deletion are different operations.

## Mutation support by table type

| Table | UPDATE | DELETE | TRUNCATE |
|---|---|---|---|
| TAG | Standard DATA correction with tag and BASETIME predicates | BEFORE, tag/axis predicates, or all rows | No |
| LOG | No | BEFORE, OLDEST, EXCEPT, or all rows | Yes |
| TRANSACTION | General predicates | General predicates or all rows | Yes |
| VOLATILE | Primary-key equality | Primary-key equality or all rows | No |
| LOOKUP | General predicates; primary key immutable | General predicates or all rows | No |

## Change boundaries and failure handling

| Operation | Model decision |
|---|---|
| Update current settings | Key, valid values, and concurrent writers |
| Correct measurements | Tag/time range, reason, and affected rollups |
| Correct a LOG event | Whether a new correction event should reference the original |
| Replace a reference key | Order of dependent changes and recovery from partial failure |
| Delete expired data | Time basis, deletion scope, and required backups |

Multiple TRANSACTION DML statements can share an explicit transaction. Do not assume LOOKUP or
VOLATILE changes and LOG/TAG input join it. If history is stored but its cache update fails, the
history can remain; the application needs a cache rebuild or retry path. Append transaction scope
depends on the API and target table; consult [SDK support](../../development-tools-integration/sdk-support-scope/).

Before changing many rows, query the count and sample rows with the same predicate. This preview
does not lock the target or freeze it against concurrent input. Control the work period and scope,
then check affected-row counts and resulting values too.


<a id="policy-update"></a>

## UPDATE policy

TRANSACTION supports general relational UPDATE and explicit transactions. VOLATILE identifies
the target by primary-key equality. LOOKUP allows general WHERE predicates but requires WHERE and
does not allow updating its key. A LOOKUP/VOLATILE key replacement requires separate DELETE and
INSERT statements, so retain the old value and plan reference changes and partial failures.

See [LOOKUP UPDATE](../../reference/sql/syntax-dictionary-sql/dml-syntax/lookup-predicate-update-syntax/)
for supported predicates and expressions. LOG does not support UPDATE.

<a id="policy-update-policy-tag-data-update"></a>

### TAG data UPDATE policy

TAG time-series rows can be updated under explicit target conditions. The UPDATE
must be limited by tag selection and the BASETIME column, and metadata updates use
a separate syntax.

TAG data UPDATE is supported only on logical TAG tables in Standard Edition. It is not supported
in Cluster Edition.

#### Policy

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

<a id="policy-update-distinction-tag-data-update-metadata"></a>

### Distinguish DATA and METADATA updates

DATA correction changes stored observations. METADATA update changes tag attributes and uses the
separate syntax above. To retain a complete correction history, store old/new values and a reason
in a separate history model rather than only overwriting the latest value.

<a id="policy-update-tag-data-update-where-set-standard-only"></a>

### TAG data UPDATE WHERE/SET support scope

TAG data UPDATE is supported with constraints that keep the update target explicit.

#### Supported form

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

#### Allowed WHERE/SET scope

- Tag selector: `name =`, `name IN (...)`, `name LIKE ...`
- Time condition: `time =`, `BETWEEN`, two-sided ranges, one-sided ranges
- Additional filters: data-column predicates
- SET targets: data columns, including `SUMMARIZED` data columns

#### Not allowed

- UPDATE without a WHERE clause
- UPDATE without a tag selector
- UPDATE without a time condition
- `OR`, subqueries, and aggregate predicates
- SET targets such as `name`, `time`, or metadata columns

The SET expression cannot reference existing-row columns. For example, `SET value = value + 1`
is not supported for TAG DATA. Supply a calculated constant or bound value, and restrict its target
range. Constant expressions that do not reference row columns have their own supported rules.

Metadata columns use `UPDATE tag METADATA SET ...`.

<a id="policy-delete"></a>

## DELETE policy

TRANSACTION supports general WHERE predicates. VOLATILE supports primary-key equality for a
specific row or omission of WHERE for all rows. LOOKUP supports general predicates and whole-table
DELETE. LOG uses BEFORE, OLDEST, EXCEPT, or whole-table deletion instead of arbitrary WHERE
predicates. See [LOG lifecycle](../../log-table-usage/operations-lifecycle/) for exact syntax.

<a id="policy-delete-delete-tag-metadata"></a>

### TAG Metadata Delete

Use `DELETE FROM table_name METADATA`. If any target tag still has data, the entire statement
fails. See [TAG metadata](../../tag-table-usage/tag-metadata/) before removing tag definitions.

<a id="condition-tag-kv-delete-before"></a>

## TAG/KV deletion and BEFORE

TAG/KV can remove older data with BEFORE or select data with tag and axis predicates. A BEFORE
timestamp must be in the past. Consult [TAG mutation](../../tag-table-usage/data-input-mutation/) for
exact forms. If periodic expiry is the goal, use a supported
[Retention Policy](../../operations-configuration-recovery/policy-data-retention/).

<a id="policy-truncate"></a>

## TRUNCATE policy

TRUNCATE TABLE is supported for LOG and TRANSACTION, preserving schema and index definitions while
removing all rows. It does not accept WHERE. TRANSACTION DELETE and TRUNCATE can be rolled back
within an explicit transaction; this does not make LOG deletion rollbackable. Committed changes
cannot be undone by a later ROLLBACK.

For VOLATILE or LOOKUP, omit WHERE from DELETE to empty the table. Use supported TAG deletion
forms for TAG. Check backups and re-ingestion before deletion. Row deletion and physical disk-space
reclamation need not complete at the same instant; inspect storage usage and table cleanup status.
