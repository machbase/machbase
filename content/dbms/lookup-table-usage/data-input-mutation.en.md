---
type: docs
title: '9.4 Data Input and Mutation'
weight: 40
toc: true
---
This section uses one runnable example to explain LOOKUP data insertion, updates, and deletion.


<a id="original-85-inserting-data"></a>

## Prepare the Example Table

Run the following examples in order through the final cleanup statements.

<a id="insert-lookup-basic"></a>

```sql
CREATE LOOKUP TABLE ch9_mutation (
    code       VARCHAR(32) PRIMARY KEY,
    label      VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO ch9_mutation VALUES ('TEMP', 'Temperature', 'ACTIVE', NOW);
INSERT INTO ch9_mutation VALUES ('PRESS', 'Pressure', 'ACTIVE', NOW);
```

If a sequence key is needed, see [SEQUENCE](/dbms/lookup-table-usage/sequence-column/).

<a id="update-lookup-basic"></a>

## UPDATE

Use a PRIMARY KEY predicate for single-row changes.

```sql
UPDATE ch9_mutation
SET status = 'INACTIVE',
    updated_at = NOW
WHERE code = 'TEMP';
```

Before changing multiple rows, query the targets with the same `WHERE` clause. For a single-row
change, a `PRIMARY KEY` predicate is recommended because it identifies the target clearly and can
use an index.

The PRIMARY KEY column itself cannot be updated. To change a key, delete the row and insert it again
with the new key. These statements cannot be grouped into a TRANSACTION table transaction, so also
design for intermediate failures and changes to referencing data.

<a id="upsert-lookup"></a>

## Duplicate-Key Handling

Use `ON DUPLICATE KEY UPDATE` when a duplicate key in SQL INSERT should update an existing row.

```sql
INSERT INTO ch9_mutation
VALUES ('TEMP', 'Temperature sensor', 'ACTIVE', NOW)
ON DUPLICATE KEY UPDATE SET label = 'Temperature sensor', status = 'ACTIVE', updated_at = NOW;
```

When Append encounters a duplicate primary key, it can update the row according to
`LOOKUP_APPEND_UPDATE_ON_DUPKEY`. This setting controls duplicate-key handling for the LOOKUP Append
path. Check its current value before using it in production.

```sql
SELECT name, value
FROM v$property
WHERE name = 'LOOKUP_APPEND_UPDATE_ON_DUPKEY';
```

<a id="refresh-lookup-table"></a>

## TABLE_REFRESH

Run `TABLE_REFRESH` when persistently stored LOOKUP content must be reloaded into the running
in-memory table.

```sql
EXEC TABLE_REFRESH(ch9_mutation);
```

Do not run it after every ordinary SQL DML operation. Its target is a LOOKUP table in the current
database, and it cannot run in a READ ONLY database. For name resolution, permissions, and errors,
see the
[EXEC Procedure Reference](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-refresh). For
cluster procedures, see [Operations and Lifecycle](/dbms/lookup-table-usage/operations-lifecycle/).

<a id="original-85-deleting-data"></a>

## Deleting LOOKUP Data

Use a PRIMARY KEY predicate for single-row deletion.

```sql
DELETE FROM ch9_mutation
WHERE code = 'PRESS';
```

A general predicate deletes all matching rows. Omit WHERE to delete every row.

```sql
DELETE FROM ch9_mutation;
DROP TABLE ch9_mutation;
```

<a id="mutation-lookup-checklist"></a>

## Modification Checklist

- Use PRIMARY KEY predicates for single-row changes.
- Before bulk changes with general predicates, query the target scope using the same predicates.
- Check backups or reload sources before deleting all rows.
- Change PRIMARY KEY values with DELETE followed by INSERT.
- Check `LOOKUP_APPEND_UPDATE_ON_DUPKEY` for Append duplicate-key handling.
- Use `EXEC TABLE_REFRESH(table_name)` only when persistent LOOKUP content must be reloaded into runtime memory.
