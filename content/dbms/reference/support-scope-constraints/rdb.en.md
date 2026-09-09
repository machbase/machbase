---
type: docs
title: '16.6.3 TRANSACTION Feature Support'
weight: 30
toc: true
---

Machbase TRANSACTION tables store general relational data that requires transactions. Access them
through Machbase SQL and supported drivers such as JDBC/ODBC.

> **Note**: TRANSACTION tables are supported **only in Standard Edition**. They cannot be created or used in Cluster Edition.

Unqualified `CREATE TABLE`, `CREATE TRANSACTION TABLE`, and `CREATE TXN TABLE` all create
TRANSACTION tables. Cluster Edition therefore rejects all three forms. Use
`CREATE LOG TABLE` to create LOG tables in Cluster Edition.

## SQL Feature Support

| Feature | Support | Notes |
|------|:---------:|------|
| **Basic DML** | | |
| SELECT | O | |
| INSERT | O | |
| UPDATE | O | |
| DELETE | O | |
| INSERT ... ON DUPLICATE KEY UPDATE | O | Update an existing row on a PRIMARY KEY or UNIQUE INDEX conflict |
| **Transactions** | | |
| Transaction (COMMIT/ROLLBACK) | O | plain `BEGIN`, `COMMIT`, `ROLLBACK` |
| ROLLBACK of TRANSACTION TRUNCATE | O | Treated as deletion of all rows within an explicit transaction |
| Savepoint | X | Not supported |
| **Queries** | | |
| Prepared Statement | O | |
| Parameter binding | O | |
| JOIN | O | Can join other table types |
| Subquery | O | |
| VIEW | O | |
| **Objects** | | |
| SEQUENCE | O | `CREATE SEQUENCE` |
| PRIMARY KEY / UNIQUE INDEX | O | Single-column PRIMARY KEY and single-/multiple-column UNIQUE INDEX |
| Secondary INDEX | O | Single-/multiple-column BTREE indexes |
| JSON path INDEX | O | `json_column->'$.path'` |
| AUTO_INCREMENT | O | Column-level PRIMARY KEY on a `LONG`/`INT64` column |
| ALTER ADD/DROP COLUMN | O | Parentheses required around column definitions |
| ALTER RENAME COLUMN / RENAME TO | O | Rename columns and tables |
| ALTER MODIFY COLUMN | X | Not supported |
| Trigger | X | Not supported |
| Stored Procedure | X | Not supported |
| Foreign Key | X | Not supported |

For `AUTO_INCREMENT`, see [AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/); for
upsert, see
[INSERT ON DUPLICATE KEY UPDATE](/dbms/rdb-table-usage/insert-on-duplicate-key-update/).
Append paths differ by client. Use the
[SDK Append matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix)
as the canonical reference.


## Transaction and Concurrent Access Boundaries

SELECT on other table types and mixed-type JOINs are allowed during an active transaction.
However, LOG, TAG, LOOKUP, and VOLATILE writes cannot be included in the same TRANSACTION transaction.
Allowed queries do not guarantee a shared snapshot across all table types.

For ordinary constraint errors, distinguish a failed statement from the entire transaction.
ROLLBACK is required to undo earlier successful changes. End a rollback-only transaction rather
than continuing work. Open TRANSACTION cursors can block COMMIT and ROLLBACK.


Currently, commits across TRANSACTION tables are applied sequentially to each table's storage handle.
Support for normal multi-table COMMIT/ROLLBACK does not guarantee multi-table atomicity
when a failure occurs during commit. After an error or a lost response, verify persisted state
using a business key.

A WAL conflict when upgrading an obsolete read snapshot to a write cannot be resolved by waiting,
even with TRANSACTION_BUSY_TIMEOUT_MS=-1.
See the [transaction exercise](../../../rdb-table-usage/transaction/) and
[two-connection conflict exercise](../../../rdb-table-usage/locking-conflict-timeout/).

## Related Documentation

- [Using TRANSACTION Tables](../../../rdb-table-usage/)
- [TRANSACTION DDL and DML](../../sql/syntax/)
- [SDK Feature Support](../../../development-tools-integration/sdk-support-scope/)
