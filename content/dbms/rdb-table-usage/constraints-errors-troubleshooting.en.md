---
type: docs
title: '8.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
---

When migrating SQL from another RDBMS, similar names can suggest equivalent features incorrectly.
First check Edition and public syntax, then examine data constraints separately from concurrency
issues.

<a id="limitations-rdb-edition"></a>

<a id="지원-범위부터-확인합니다"></a>

## Feature Support

TRANSACTION is Standard Edition only. Cluster rejects CREATE TABLE, CREATE TRANSACTION TABLE, and
CREATE TXN TABLE. Specify CREATE LOG TABLE explicitly for LOG.

| Requirement | Support or alternative |
|---|---|
| General SELECT/INSERT/UPDATE/DELETE | Supported; changes without WHERE target all rows |
| Single-column PRIMARY KEY | Supported; one per table |
| Single/composite UNIQUE INDEX | Supported; create separately after the table |
| Column UNIQUE or table-level PRIMARY KEY | These creation forms are unsupported |
| FOREIGN KEY, Trigger, Stored Procedure | Unsupported |
| BEGIN/COMMIT/ROLLBACK | Supported; nested BEGIN and SAVEPOINT unsupported |
| ADD/DROP/RENAME COLUMN, RENAME TO | Check supported conditions |
| MODIFY COLUMN | Unsupported |
| Append | Check SDK public paths and batch boundaries |
| TAG METADATA/BASETIME/BASEDISTANCE | Not applicable to TRANSACTION |

LOOKUP can support small reference-data changes in Cluster, but is not a complete replacement for
explicit relational transactions. Separate requirements appropriately, such as LOG/TAG for source
events and another RDBMS for relational transactions.

<a id="오류별로-확인-대상을-좁힙니다"></a>

## Diagnosis by Error

| Symptom | What to check | Next action |
|---|---|---|
| ERR-01418 uniqueness violation | Primary/unique keys and existing data | Correct input or review UPSERT rules |
| NOT NULL violation | Omitted values, NULL, empty strings, and DEFAULT | Check input and constraints |
| UPDATE affects 0 rows | Key and current-state predicates | Distinguish missing/already-processed targets |
| Resource busy | Other writers, stale read snapshots, and open cursors | Wait, restart the transaction, or close cursors as appropriate |
| COMMIT/ROLLBACK is busy | Open result sets on the same connection | Close result sets and retry termination |
| Subsequent SQL is rejected after an error | Rollback-only state | ROLLBACK and start a new operation |
| DDL fails | Referencing indexes/views and active transactions | Adjust dependencies and timing |
| Mounted values differ from expectations | Mount, owner, and table names | Distinguish production from backup data |

Resource busy errors require different retry strategies. See the two-connection exercises in
[Locks and Busy Timeout](../locking-conflict-timeout/). Do not retry solely because the error text
contains TRANSACTION.

<a id="작은-표본에서-제약과-상태-보존을-확인합니다"></a>

## Constraint Errors and Data Preservation

```sql
CREATE TRANSACTION TABLE ch8_error (
    id    LONG PRIMARY KEY,
    code  VARCHAR(32) NOT NULL,
    value INTEGER
);
CREATE UNIQUE INDEX ch8_error_code ON ch8_error(code);
INSERT INTO ch8_error VALUES (1, 'A', 10);
```

Each optional example below intentionally fails. Run only the statement being checked, separately
from normal SQL.

```sql
-- Duplicate PRIMARY KEY
INSERT INTO ch8_error VALUES (1, 'B', 20);
-- Duplicate UNIQUE key
INSERT INTO ch8_error VALUES (2, 'A', 20);
-- Required-value violation
INSERT INTO ch8_error VALUES (3, NULL, 30);
-- Unsupported schema change
ALTER TABLE ch8_error MODIFY COLUMN (code VARCHAR(64));
```

```sql
SELECT id, code, value FROM ch8_error ORDER BY id;
DROP TABLE ch8_error;
```

The final query contains only (1, A, 10). Distinguish a failed statement preserving state from
automatic cancellation of earlier successful statements inside BEGIN; the latter does not follow.
See the comparison in [Transactions](../transaction/).

<a id="진단-정보는-민감한-값을-가리고-공유하세요"></a>

## Collecting Diagnostic Information

Collect server version/Edition, DDL and indexes, executed SQL, error code and full message, and
actual affected row counts. For connection failures, also record COMMIT request/response times and
business keys. Redact passwords, personal information, and sensitive business values; share only a
minimal reproducer.

Do not repair by editing internal storage files or recreating production tables. Establish the cause
and whether changes were applied first to reduce data loss.
