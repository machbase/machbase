---
title: '8. RDB Table Usage'
weight: 80
toc: true
---

This page mirrors the Korean chapter structure. Detailed English content will be aligned after the Korean manual is finalized.

## Chapter Structure

| Section | Topic |
| --- | --- |
| [Overview and Usage Criteria](./overview-use-criteria/) | RDB table characteristics and selection criteria |
| [Table Structure and Schema](./table-structure-schema/) | Column types, primary keys, and schema design |
| [Create, Alter, and Drop](./create-alter-drop/) | `CREATE RDB TABLE`, `ALTER`, and `DROP` syntax |
| [Data Input and Mutation](./data-input-mutation/) | `INSERT`, `UPDATE`, `DELETE`, and `INSERT SELECT` |
| [Query and Analysis](./query-analysis/) | `SELECT`, aggregation, and filtering |
| [Indexes and Performance](./index-performance/) | Primary key, unique, normal, and JSON path indexes and tuning |
| [Operations and Data Lifecycle](./operations-lifecycle/) | Operational procedures and data management |
| [Constraints, Errors, and Troubleshooting](./constraints-errors-troubleshooting/) | Edition limits, feature constraints, and error handling |
| [Patterns and Scenarios](./patterns-scenarios/) | Practical RDB table usage patterns |
| [Transactions](./transaction/) | `BEGIN`, `COMMIT`, `ROLLBACK`, and batch operations |
| [Locks, Conflicts, and Busy Timeout](./locking-conflict-timeout/) | Lock checks, conflict prevention, and timeout settings |
| [JOIN and Relational Query Design](./join-relational-query/) | RDB-LOOKUP, RDB-TAG, and RDB-RDB joins |
| [RDB Backup, Restore, and Mount](./backup-restore-mount/) | Database/table backup, restore, and read-only mount |
| [INSERT ON DUPLICATE KEY UPDATE](./insert-on-duplicate-key-update/) | RDB upsert syntax and conflict handling |

See [AUTO_INCREMENT](/dbms/reference/sql/syntax-dictionary-sql/auto-increment-syntax/) for the
cross-table automatic-key syntax.
