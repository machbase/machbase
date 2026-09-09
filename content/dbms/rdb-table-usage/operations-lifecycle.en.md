---
type: docs
title: '8.7 Operations and Data Lifecycle'
weight: 70
toc: true
---

Deleting old business data requires more than checking dates. Cancelled orders and orders still in
progress have different retention criteria, and cleanup can conflict with other writes. Define
business predicates and processing units before deleting.

<a id="operations-rdb-lifecycle"></a>

<a id="원본과-업무-상태의-보관-목적을-나눕니다"></a>

## Data Retention Criteria

Use TAG/LOG for source time series and TRANSACTION for mutable state or summary results. Their
retention periods need not match. TAG/LOG Retention Policy does not directly apply to TRANSACTION.
Design DELETE predicates and external scheduling for business requirements.

<a id="operations-rdb-transaction"></a>
<a id="operations-rdb-cleanup"></a>

<a id="삭제-전후를-같은-실습에서-확인합니다"></a>

## Deletion and Rollback

```sql
CREATE TRANSACTION TABLE ch8_cleanup (
    id      LONG PRIMARY KEY,
    status  VARCHAR(16),
    created DATETIME
);
INSERT INTO ch8_cleanup VALUES (1, 'CANCELLED', TO_DATE('2025-12-01', 'YYYY-MM-DD'));
INSERT INTO ch8_cleanup VALUES (2, 'PENDING', TO_DATE('2025-12-01', 'YYYY-MM-DD'));
INSERT INTO ch8_cleanup VALUES (3, 'CANCELLED', TO_DATE('2026-02-01', 'YYYY-MM-DD'));

BEGIN;
SELECT COUNT(*) AS delete_candidates FROM ch8_cleanup
 WHERE status = 'CANCELLED' AND created < TO_DATE('2026-01-01', 'YYYY-MM-DD');
DELETE FROM ch8_cleanup
 WHERE status = 'CANCELLED' AND created < TO_DATE('2026-01-01', 'YYYY-MM-DD');
SELECT id, status FROM ch8_cleanup ORDER BY id;
ROLLBACK;

SELECT COUNT(*) AS after_rollback FROM ch8_cleanup;
```

One row is targeted. Rows 2 and 3 remain during deletion; after rollback, the count is 3. The
exercise rolls back for verification. To finalize production work, choose COMMIT after business
approval and result checks. Close result cursors before ending the transaction.

Do not equate preliminary query counts with actual affected rows. Account for concurrent changes and
snapshot conflicts, and record affected counts returned during execution and final state. See
[Locks and Retries](../locking-conflict-timeout/).

<a id="큰-작업은-다시-시작할-기준을-남깁니다"></a>

## Batch Processing and Resumption

Partition deletion by date interval or unique-key range instead of one long transaction. Record
boundaries, processed counts, and commit results for each range so work can resume after an
interruption.

Also take care when copying reference data to another table before deleting the source. Do not
assume atomic cross-table commit under failure for multiple TRANSACTION tables. Design copy
verification and resumption according to [Transaction Guarantees](../transaction/). Avoid waiting
for external APIs or long file operations inside BEGIN.

<a id="operations-rdb-backup-recovery"></a>

<a id="삭제-전에-백업을-실제로-읽어-봅니다"></a>

## Backup Validation

Check business keys, row counts, totals, and indexes in the mounted backup, not merely
backup-command success. Use three-part names `mount_name.owner.table_name`. Two-part names can be
confused with production data.

Even incremental backups include a complete TRANSACTION table storage snapshot at the backup point.
Do not estimate additional space only from the changed row count. For exercises, see
[Backup, Restore, and Mount](../backup-restore-mount/).

<a id="operations-rdb-checklist"></a>

<a id="정리-후에도-조회와-공간을-따로-확인합니다"></a>

## Checks After Cleanup

Fewer rows do not necessarily reduce operating-system file size immediately or proportionally. Check
business row counts, actual file usage, and retained backup volume separately. Do not connect
directly to internal SQLite files or delete files arbitrarily to reclaim space.

```sql
DROP TABLE ch8_cleanup;
```

If cleanup fails, check the last successful range and commit result before attempting further
deletion. These records reduce omissions and duplicate processing.
