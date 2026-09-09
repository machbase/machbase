---
type: docs
title: 'EXEC Procedures and ROLLUPGAP'
weight: 240
toc: true
---

This reference covers public Machbase table/ROLLUP control procedures and machsql status commands.

## Common EXEC Form

```text
execute_procedure_stmt ::=
    'EXEC' procedure_name [ '(' argument_list ')' ]
```

Argument counts are fixed for each procedure. Missing names, incorrect argument counts/types, or
nonexistent target objects return errors.

<a id="table-flush"></a>

## TABLE_FLUSH

```sql
EXEC TABLE_FLUSH(table_name);
```

| Item | Contract |
|---|---|
| Arguments | One table name |
| Edition | Standard, Cluster |
| Behavior | Explicitly flush pending table storage/input buffers |
| Return | Statement success or error; no ResultSet |
| Errors | Missing table, denied access, or flush failure |

Use when validation or operations require an explicit storage flush. It does not guarantee
transaction commit or query visibility. Do not call it for every input row, which increases flush
cost.

<a id="index-flush"></a>

## INDEX_FLUSH

```sql
EXEC INDEX_FLUSH(table_name);
EXEC INDEX_FLUSH(table_name, index_name);
```

With only a table name, waits for all index builds on that table to finish. With an index name,
targets only that index; an index not belonging to the table causes an error. No ResultSet is
returned.

<a id="table-refresh"></a>

## TABLE_REFRESH

```sql
EXEC TABLE_REFRESH(lookup_table_name);
```

| Item | Contract |
|---|---|
| Arguments | One LOOKUP table name |
| Edition | Standard, Cluster |
| Behavior | Reload persistent LOOKUP content into the runtime memory table |
| Name scope | Current database; owner.table allowed |
| Privileges | Table owner or authorized administrative user |
| Write restriction | Cannot run in a READ ONLY database |
| Return | Statement success or error; no ResultSet |
| Errors | Non-LOOKUP target, missing table, or write-admission failure |

Before execution, check ongoing LOOKUP changes and query impact. Afterward, query row counts and
representative keys again.

<a id="freeze-tag-index"></a>

## FREEZE_TAG_INDEX and UNFREEZE_TAG_INDEX

```sql
EXEC FREEZE_TAG_INDEX(tag_table_name);
EXEC UNFREEZE_TAG_INDEX(tag_table_name);
```

These one-argument procedures freeze or unfreeze a TAG table's tag index. Other table types are
unsupported. They directly control index-maintenance boundaries and should not be used routinely in
ordinary ingestion. After failure, always check whether UNFREEZE_TAG_INDEX was executed. Both return
statement success or error without a ResultSet.

<a id="rollup-start-stop"></a>

## ROLLUP_START and ROLLUP_STOP

```sql
EXEC ROLLUP_START;
EXEC ROLLUP_START(rollup_name);

EXEC ROLLUP_STOP;
EXEC ROLLUP_STOP(rollup_name);
```

Both procedures accept zero arguments or one ROLLUP name. A name controls that ROLLUP; omission
controls ROLLUPs within the current user scope. Unnamed SYS execution can affect all users,
requiring target checks and change approval.

A nonexistent ROLLUP, START on an already started target, or STOP on an already stopped target
causes an error. Verify the change with V$ROLLUP.RUN_STATE.

<a id="rollup-force"></a>

## ROLLUP_FORCE

```sql
EXEC ROLLUP_FORCE;
EXEC ROLLUP_FORCE(rollup_name);
```

The zero-argument form processes the current user's default SEC→MIN→HOUR hierarchy. The named form
synchronously waits to catch up to the named ROLLUP source's current END_RID. For a stopped ROLLUP,
first ensure it has been started.

After completion, check every relevant source-stage gap with V$ROLLUP and SHOW ROLLUPGAP.

<a id="rollup-rebuild"></a>

## ROLLUP_REBUILD

This Standard-only four-argument procedure accepts a tag and time range. Use
[ROLLUP_REBUILD](../rollup-rebuild-syntax/) as the authoritative contract.

<a id="show-rollupgap"></a>

## SHOW ROLLUPGAP

```sql
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP is a **machsql-only client command**, not server SQL. Do not send it to ordinary
JDBC, ODBC, or SDK SQL execution APIs.

Standard output includes source/ROLLUP tables, source END_RID, ROLLUP END_RID, GAP, state, and
wakeup time. Cluster adds HOSTNAME for per-node state. `GAP = SRC_END_RID - ROLLUP_END_RID`. Every
source→ROLLUP row in the hierarchy must be 0 before the entire hierarchy is considered caught up.

## Related Documentation

- [ROLLUP Operations and Status](/dbms/tag-rollup-usage/ingestion-control-rollup/)
- [V$ROLLUP Reference](/dbms/reference/system-catalog/vrollup/)
- [machsql Commands](/dbms/reference/command-line-tools/machsql/)
