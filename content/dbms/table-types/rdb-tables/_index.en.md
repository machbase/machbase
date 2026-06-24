---
type: docs
title: 'RDB Tables'
weight: 50
---

RDB tables are generalized disk row tables for Machbase DBMS workloads that need
`INSERT`, `UPDATE`, `DELETE`, and indexed `SELECT` beyond the single primary-key
model of Lookup tables.

## Overview

Use an RDB table when a Machbase application needs a generalized disk table next
to high-volume `TAG` or `LOG` data. Typical examples are equipment master data,
alarm rules, current alarm state, work queues, and dimension tables used in joins.
Use a Lookup table instead when the data is persistent reference data and all row
access is centered on one primary key.

RDB tables are created explicitly with `CREATE RDB TABLE`. The existing `CREATE TABLE` syntax continues to create a `LOG` table.

## Key Features

- **Generalized disk row storage**
- **Full DML support**: `INSERT`, `UPDATE`, `DELETE`, and `SELECT`
- **Optional primary key** at create time or later with `CREATE PRIMARY KEY INDEX`
- **Normal, unique, and JSON path indexes**
- **Joins with `TAG`, `LOG`, `VOLATILE`, `LOOKUP`, and `VIEW` sources**
- **Backup, restore, and mounted database read access**
- **machloader and SDK support for prepared statements and append APIs**

## Basic Syntax

```sql
CREATE RDB TABLE device_master (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(64) NOT NULL,
    site       VARCHAR(32) DEFAULT 'SEOUL',
    state      VARCHAR(16),
    info       JSON,
    updated_at DATETIME
);

INSERT INTO device_master(id, name, state, info, updated_at)
VALUES (1, 'pump-01', 'READY', '{"owner":"ops"}', NOW);

UPDATE device_master
   SET state = 'RUNNING',
       info = JSON_SET(info, '$.status', 'normal')
 WHERE id = 1;

SELECT id, name, state
  FROM device_master
 WHERE id = 1;

DELETE FROM device_master
 WHERE id = 1;
```

## Indexes

Use normal indexes for lookup predicates, unique indexes for uniqueness constraints, and primary key indexes when the table must have a primary key.

```sql
CREATE INDEX idx_device_site ON device_master(site);
CREATE UNIQUE INDEX uidx_device_name ON device_master(name);
CREATE PRIMARY KEY INDEX pk_device_id ON device_master(id);
CREATE INDEX idx_device_owner ON device_master(info->'$.owner');
```

`CREATE PRIMARY KEY INDEX` is only for RDB tables without an existing primary key. If existing rows contain `NULL` or duplicate values in the target column, the statement fails and the table remains unchanged. A primary key index cannot be dropped.

RDB index scan is currently optimized for safe equality and range predicates. Predicates that cannot be pushed down are still evaluated by the Machbase query processor so query results remain correct.

## DML and Transactions

RDB tables support:

- `INSERT` and `INSERT ... SELECT`
- `UPDATE ... SET ... WHERE ...`
- `UPDATE ... SET ...` without `WHERE`, which updates all rows
- `DELETE FROM ... WHERE ...`
- `DELETE FROM table_name` without `WHERE`, which deletes all rows
- `TRUNCATE TABLE table_name`

Plain `BEGIN`, `COMMIT`, and `ROLLBACK` can be used with RDB DML. An active RDB transaction blocks conflicting RDB DDL such as `ALTER TABLE`, `CREATE INDEX`, and `DROP TABLE` until the transaction ends.

## Supported Data Types

RDB tables support the following data types in SQL and machloader paths:

| Category | Types |
| --- | --- |
| Integer | `SHORT`, `USHORT`, `INTEGER`, `UINTEGER`, `LONG`, `ULONG` |
| Floating point | `FLOAT`, `DOUBLE` |
| Text | `VARCHAR`, `TEXT`, `CLOB` |
| Binary | `BINARY`, `BLOB` |
| Date/time | `DATETIME` |
| Network | `IPV4`, `IPV6` |
| JSON | `JSON` |

`NUMERIC` and `DECIMAL` are not supported for RDB tables.

## Altering RDB Tables

RDB tables support table and column rename, adding columns, and dropping columns.

```sql
ALTER TABLE device_master RENAME TO device_registry;
ALTER TABLE device_registry RENAME COLUMN state TO run_state;
ALTER TABLE device_registry ADD COLUMN score INTEGER DEFAULT 0;
ALTER TABLE device_registry DROP COLUMN (score);
```

RDB `ALTER TABLE DROP COLUMN` is rejected when the column is used by a primary key, unique index, normal index, or JSON path index.

## Backup, Restore, and Mount

RDB table data is stored in an RDB sidecar file. Database and table backup include the sidecar snapshot together with the Machbase catalog metadata.

- `RESTORE DATABASE` restores the RDB sidecar after catalog restore.
- `machadmin -r` also restores the RDB sidecar.
- `MOUNT DATABASE` opens RDB sidecars read-only and can query mounted RDB tables and views.
- DML, DDL, backup, and schema writes against mounted RDB objects are rejected.
- `MOUNT TABLE` for RDB tables is not supported.

## machloader and SDK Support

`machloader` can import and export RDB tables, export schema, use replace mode, match CSV headers, and write bad files for invalid input rows.

Client SDKs can use prepared or parameterized execution against RDB tables. SQLCLI, JDBC, Python, Node.js, and .NET paths are covered by the RDB regression suite. JDBC and Node.js also support append batch paths, and SQLCLI/Python/.NET support append stream paths.

## Limitations

- RDB tables are supported in standard edition. Cluster edition rejects RDB DDL, DML, SELECT, VIEW, and INDEX operations.
- Native backend SQL passthrough is not provided.
- Table-level constraints, composite primary keys, foreign keys, triggers, generated columns, partial indexes, arbitrary expression indexes, and collation options are not supported.
- `CREATE TABLE` still creates a `LOG` table. Use `CREATE RDB TABLE` for RDB tables.

## Related Documentation

- [Table Types Overview](../../core-concepts/table-types-overview/)
- [SQL Reference](../../sql-reference/)
- [Tools Reference](../../tools-reference/)
