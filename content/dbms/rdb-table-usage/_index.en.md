---
type: docs
title: '8. TRANSACTION Table Usage'
weight: 80
toc: true
---

Appending source logs differs from changing order status, inventory, or device information.
State-changing workloads must also check how many rows changed, what rolls back after a partial
failure, and how concurrent updates from another connection behave.

TRANSACTION tables support these relational queries and modifications in Standard Edition only. This
chapter connects schema design, updates, transactions, concurrent access, and recovery while
checking results on small samples. Although SQLite is used internally for storage, Machbase SQL
defines the public syntax and support scope. Not every SQLite or other RDBMS feature is available
unchanged.

<a id="필요한-작업부터-찾아보세요"></a>

## Chapter Contents

| Section | What to check |
|---|---|
| [8.1 Overview and Use Criteria](./overview-use-criteria/) | Roles compared with LOG, TAG, and LOOKUP |
| [8.2 Table Structure and Schema](./table-structure-schema/) | Identifiers, business keys, types, and constraints |
| [8.3 Create, Alter, and Drop](./create-alter-drop/) | DDL and existing-data checks |
| [8.4 Data Ingestion and Modification](./data-input-mutation/) | Conditional updates/deletes, copying, and Append |
| [8.5 Queries and Analysis](./query-analysis/) | Filtering, sorting, aggregation, and JSON queries |
| [8.6 Indexes and Performance](./index-performance/) | Primary key, unique, composite, and JSON path indexes |
| [8.7 Operations and Data Lifecycle](./operations-lifecycle/) | Batch cleanup and operational checks |
| [8.8 Constraints, Errors, and Troubleshooting](./constraints-errors-troubleshooting/) | Symptom diagnosis and retry decisions |
| [8.9 Transactions](./transaction/) | Statement failures, ROLLBACK, and commit guarantees |
| [8.10 Locks, Conflicts, and Busy Timeout](./locking-conflict-timeout/) | Two-connection conflicts and snapshot retries |
| [8.11 JOIN and Relational Query Design](./join-relational-query/) | Rows added or excluded by joins |
| [8.12 Backup, Restore, and Mount](./backup-restore-mount/) | Verifying actual data at the backup point |
| [8.13 INSERT ON DUPLICATE KEY UPDATE](./insert-on-duplicate-key-update/) | Insert/update branches and duplicate handling |

For common automatic-numbering syntax, see
[AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/).

<a id="실습-환경과-실행-단위를-먼저-맞춥니다"></a>

## Example Environment and Execution Scope

SQL exercises target a DBMS 8.7 Standard Edition validation environment. Each section creates and
cleans up `ch8_` objects independently. Table/index creation privileges are required; backup
exercises also require separate privileges and server paths.

Run BEGIN through COMMIT/ROLLBACK on the same connection. Follow the specified A/B sequence in
two-session exercises. Intentionally failing SQL is separated from normal flow. Complete cleanup SQL
before rerunning an exercise.

Caution: the TRANSACTION name does not mean all operations and all failure scenarios roll back
together. First check DDL, writes to other table types, and cross-table commit boundaries during
failures in [8.9 Transactions](./transaction/).
