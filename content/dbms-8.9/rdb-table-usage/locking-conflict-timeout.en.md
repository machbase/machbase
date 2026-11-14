---
type: docs
title: '8.10 Locks, Conflicts, and Busy Timeout'
weight: 100
toc: true
---

If different rows still produce Resource busy, thinking only in terms of row locks can obscure the
cause. TRANSACTION write conflicts can occur between different rows of the same table. Distinguish
conflicts resolved by waiting from those requiring a new transaction.

<a id="transaction-locking-conflict-rdb"></a>
<a id="design-locking-conflict-rdb-busy-timeout-ddl-dml"></a>

<a id="두-연결을-준비합니다"></a>

## Example Environment

This exercise targets a Standard validation environment with default WAL settings. A and B are
separate connections to the same account and database. Execute blocks in the stated order and fully
consume SELECT results to close cursors. Do not change production journal mode for this exercise.

Prepare the table in A.

```sql
SELECT NAME, VALUE FROM V$PROPERTY WHERE NAME = 'TRANSACTION_JOURNAL_MODE';

CREATE TRANSACTION TABLE ch8_lock (id INTEGER PRIMARY KEY, val INTEGER);
INSERT INTO ch8_lock VALUES (1, 10);
INSERT INTO ch8_lock VALUES (2, 20);
```

TRANSACTION_JOURNAL_MODE=4 means WAL. With another value, check the environment before expecting the
WAL snapshot results below.

<a id="같은-테이블의-서로-다른-행도-쓰기가-충돌합니다"></a>

## Concurrent Write Conflicts

In A, begin a transaction and leave it open.

```sql
BEGIN;
UPDATE ch8_lock SET val = 11 WHERE id = 1;
```

Next query in B. Set the wait time to 0 only on the example B connection.

```sql
ALTER SESSION SET TRANSACTION_BUSY_TIMEOUT_MS = 0;
SELECT id, val FROM ch8_lock ORDER BY id;
```

B sees the previous values 10 and 20, not A's uncommitted 11. B's following UPDATE intentionally
produces Resource busy.

```sql
-- B: failure is expected; a different row still writes the same table.
UPDATE ch8_lock SET val = val + 1 WHERE id = 2;
```

COMMIT in A, then repeat the UPDATE in B.

```sql
-- A
COMMIT;
```

```sql
-- B
UPDATE ch8_lock SET val = val + 1 WHERE id = 2;
SELECT id, val FROM ch8_lock ORDER BY id;
```

Values are now 11 and 21. This demonstrates why same-table write conflicts must not be interpreted
as conventional row-level locking.

<a id="wal의-오래된-읽기-스냅샷은-대기로-해결되지-않습니다"></a>

## WAL Snapshot Conflicts

After completing the preceding steps, open a read transaction in A.

```sql
-- A
BEGIN;
SELECT val FROM ch8_lock WHERE id = 1;
```

After A reads 11, change the value in B. B has no explicit transaction active.

```sql
-- B
UPDATE ch8_lock SET val = val + 10 WHERE id = 1;
```

Switching A to a write now is expected to cause a snapshot conflict.

```sql
-- A: intentionally failing step
UPDATE ch8_lock SET val = val + 1 WHERE id = 1;
```

Another connection has already committed, so A cannot promote its stale read snapshot to a write.
Increasing busy timeout or setting it to -1 does not resolve this conflict by waiting. End A's
transaction and reassess the new state instead of repeating only UPDATE.

```sql
-- A
ROLLBACK;
BEGIN;
UPDATE ch8_lock SET val = val + 1 WHERE id = 1;
COMMIT;
SELECT id, val FROM ch8_lock ORDER BY id;
```

Final values are 22 and 21. If the next change was calculated from a value read earlier, repeat the
read and business decision in the new transaction.

<a id="timeout은-보장된-대기-시간이-아닙니다"></a>

## busy timeout

The server default TRANSACTION_BUSY_TIMEOUT_MS is 30000 ms and is copied to new sessions. Change the
current session with ALTER SESSION.

| Value | Handling of temporary lock conflicts |
|---|---|
| -1 | Wait until cancellation, disconnection, or lock release |
| 0 | Return busy without waiting |
| Positive | Wait up to that many milliseconds, then proceed or return busy |

Conflicts that retries cannot resolve, such as snapshot promotion conflicts, are exceptions to this
policy. -1 is not an infinite retry policy for every conflict. DDL_LOCK_TIMEOUT separately controls
DDL lock waits; changing it does not fix snapshot conflicts.

<a id="오류-문자열-하나로-재시도하지-마세요"></a>

## Errors and Retries

Retrying because the message contains TRANSACTION also repeats type, constraint, and permission
errors. Use driver error codes, complete diagnostics, and operation type to identify retryable lock
conflicts.

To retry an explicit transaction, close open result sets, ROLLBACK, and rerun in a new transaction
within bounded attempts and total request time. Connection loss and lost COMMIT responses are
separate cases. Repeating counter increments or order processing without checking business keys for
prior completion can apply changes twice.

<a id="실행-중인-작업을-찾아-원인을-좁힙니다"></a>

## Conflict Diagnosis

```sql
SELECT id, user_name, user_ip, transaction_busy_timeout_ms
  FROM V$SESSION WHERE closed = 0 ORDER BY id;

SELECT id, sess_id, state, query FROM V$STMT
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%';
```

This query does not directly map lock owners. V$MUTEX contains internal server mutex statistics, not
a business-row lock list. Check connection information together with application BEGIN/end records.
Do not make forced session termination the first action, because it can cancel uncommitted work.

Confirm that neither connection has an open transaction, then clean up in A.

```sql
DROP TABLE ch8_lock;
```

Closing example connections A and B removes the effect of B's session timeout. In production, moving
external API calls and long computations outside BEGIN can itself reduce waits.
