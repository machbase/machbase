---
type: docs
title: '8.9 Transactions'
weight: 90
toc: true
---

When a statement fails midway through several SQL operations, earlier changes do not necessarily
disappear. Ordinary constraint errors distinguish the failing statement from the entire transaction.
This section first checks COMMIT/ROLLBACK boundaries using changes within one table.

<a id="design-transaction-rdb"></a>

<a id="begin부터-종료까지-같은-연결을-사용합니다"></a>

## Executing Transactions

```sql
CREATE TRANSACTION TABLE ch8_tx (
    item_id LONG PRIMARY KEY,
    qty     INTEGER NOT NULL
);
INSERT INTO ch8_tx VALUES (1, 10);
INSERT INTO ch8_tx VALUES (2, 20);

BEGIN;
UPDATE ch8_tx SET qty = qty - 3 WHERE item_id = 1 AND qty >= 3;
UPDATE ch8_tx SET qty = qty + 3 WHERE item_id = 2;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
ROLLBACK;

SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

Inside the transaction, values are 7 and 23; after ROLLBACK, they are 10 and 20. The application
must verify that each UPDATE affected the expected one row. Updating 0 rows because a predicate does
not match is not an SQL error, so the database does not automatically identify business failure.

The following successful exercise commits the same changes.

```sql
BEGIN;
UPDATE ch8_tx SET qty = qty - 3 WHERE item_id = 1 AND qty >= 3;
UPDATE ch8_tx SET qty = qty + 3 WHERE item_id = 2;
COMMIT;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

Committed values are 7 and 23. The public syntax is BEGIN; BEGIN TRANSACTION, nested BEGIN, and
SAVEPOINT are unsupported. Without an explicit transaction, TRANSACTION DML is processed statement
by statement. Check driver autocommit and transaction APIs separately.

<a id="문장-오류-뒤에도-앞선-변경은-남아-있을-수-있습니다"></a>

## Statement Errors and Rollback

This exercise demonstrates error handling. The duplicate INSERT intentionally fails. If the SQL tool
stops on error, ensure ROLLBACK is executed on the same connection.

```sql
BEGIN;
UPDATE ch8_tx SET qty = 100 WHERE item_id = 1;
```

```sql
-- Expected failure: duplicate item_id
INSERT INTO ch8_tx VALUES (1, 999);
```

```sql
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
ROLLBACK;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

The first query shows 100 and 23; after ROLLBACK, 7 and 23. An ordinary constraint error rolls back
the failing statement, but earlier successful statements remain in the transaction. The application
must choose ROLLBACK to cancel the whole business operation. Continuing is not possible after every
error: a rollback-only state entered during recovery must be ended with ROLLBACK.

<a id="truncate도-테이블-타입에-따라-다릅니다"></a>

## TRUNCATE and Rollback

```sql
BEGIN;
TRUNCATE TABLE ch8_tx;
SELECT COUNT(*) AS during_truncate FROM ch8_tx;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM ch8_tx;
```

Results are 0 and 2. Current TRANSACTION TRUNCATE deletes all rows as part of an explicit
transaction. Distinguish this from LOG/TAG cleanup and schema changes such as CREATE/ALTER/DROP.
Perform schema operations outside business transactions.

<a id="다른-테이블-조회와-쓰기의-경계가-다릅니다"></a>

## Transaction Scope by Table Type

Queries and mixed joins involving LOG, TAG, LOOKUP, and VOLATILE are allowed during an active
TRANSACTION transaction. Writes to those types cannot be grouped into the same transaction.
Permitted reads do not give those types the same snapshot/rollback guarantees as TRANSACTION. Design
consistency between source ingestion and business-state changes separately.

TRANSACTION reads use snapshots that exclude other sessions' uncommitted changes. Do not assume
BEGIN fixes one common read point across every table at once. Read-to-write conflicts are covered in
[Locks and Retries](../locking-conflict-timeout/).

<a id="여러-테이블과-장애-시-커밋을-구분하세요"></a>

## Multitable Commit and Failures

DML on multiple TRANSACTION tables can be grouped with BEGIN and normally committed or rolled back.
However, storage currently uses per-table handles, and COMMIT processes those handles sequentially.
Do not interpret this as guaranteed atomic commit across all tables if a failure occurs during
commit.

Review this limitation first for workloads requiring indivisible multitable processing. After commit
failure or a lost response, sending ROLLBACK does not prove every table was restored. Check applied
state by business key. This is also why the basic exercise uses two rows in one table.

<a id="열린-결과-집합을-닫고-종료합니다"></a>

## Cursors and Transaction Termination

Open TRANSACTION cursors can cause COMMIT/ROLLBACK to fail with Resource busy. Close SDK result
sets/statements, then retry the termination command. Disconnecting rolls back uncommitted changes,
but the client must separately establish whether the server had already committed before the
connection was lost.

```sql
DROP TABLE ch8_tx;
```

Do not wait for external APIs or long computations inside BEGIN. Keep transactions short and
distinguish retrying an operation from first checking its result to make operational decisions
clearer.
