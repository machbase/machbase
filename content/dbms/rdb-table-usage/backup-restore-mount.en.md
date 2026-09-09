---
type: docs
title: '8.12 TRANSACTION Backup, Restore, and Mount'
weight: 120
toc: true
---

A successful backup command does not complete recovery preparation. When production and backup
tables have the same name, querying the wrong one can look like successful validation. This exercise
changes production values after backup and verifies that the two results differ.

<a id="support-scope-backup-rdb"></a>

<a id="백업-범위와-복원-경로를-구분합니다"></a>

## Backup and Restore Support

| Operation | TRANSACTION behavior |
|---|---|
| BACKUP DATABASE | Includes persistent TRANSACTION data in the target scope |
| BACKUP TABLE | Backs up the specified table and required metadata |
| Incremental backup | Includes a complete TRANSACTION storage snapshot at that backup point |
| MOUNT DATABASE | Queries the backup read-only |
| Offline instance restore | Stop the server and use machadmin -r |
| Online logical database restore | Restore a supported logical backup with RESTORE DATABASE |

Do not treat TRANSACTION data in incremental backups as a changed-row-only delta. Use supported
backup commands instead of copying internal files. A backup containing TRANSACTION is also not a
workaround for using those tables in Cluster.

<a id="backup-rdb"></a>
<a id="design-backup-mount-rdb"></a>

<a id="운영-값과-백업-값을-다르게-만들어-확인합니다"></a>

## Backup and Mount Validation

This exercise uses SYS in a Standard validation environment. Backup/mount privileges and server file
permissions are required. Paths are server-side examples; use a new, nonexistent path for every run.
Check parent directories and free space. Do not delete existing backups merely to reuse paths.

```sql
CREATE TRANSACTION TABLE ch8_backup (
    id     LONG PRIMARY KEY,
    code   VARCHAR(32) NOT NULL,
    amount DECIMAL(18,2)
);
CREATE UNIQUE INDEX ch8_backup_code ON ch8_backup(code);
INSERT INTO ch8_backup VALUES (1, 'A', 10.25);
INSERT INTO ch8_backup VALUES (2, 'B', 20.50);

BACKUP TABLE ch8_backup INTO DISK = '/backup/ch8_table_20260907_a';

UPDATE ch8_backup SET amount = 99.00 WHERE id = 1;

MOUNT DATABASE '/backup/ch8_table_20260907_a' TO ch8_bak;

SELECT id, code, amount FROM ch8_bak.SYS.ch8_backup ORDER BY id;
SELECT id, code, amount FROM ch8_backup ORDER BY id;
```

The backup contains 10.25 and 20.50; production contains 99.00 and 20.50. Mounted queries use
three-part names `mount_name.owner.table_name`. If another account owns the example, replace SYS
with the actual owner.

Running only `SELECT ... FROM ch8_backup` is a common mistake: it queries the current connection's
production table, not the mounted backup. Also do not expect tables excluded from the backup to be
present.

A mount is read-only, not a recovery environment for UPDATE or DDL. Finish verification, close open
cursors, and unmount.

```sql
UMOUNT DATABASE ch8_bak;
DROP TABLE ch8_backup;
```

This cleanup removes only the example table and mount. The backup directory remains; manage it
separately under the retention policy.

<a id="복원-검증에서는-데이터뿐-아니라-제약도-확인합니다"></a>

## Restore Validation Checks

In an isolated restore environment, verify owners, row counts, business keys, monetary totals, and
representative JSON values. Check retained PRIMARY KEY/UNIQUE INDEX definitions, required
privileges, and application COMMIT/ROLLBACK flows. Mounted read-only validation does not establish
that restored writes work.

Online RESTORE DATABASE follows logical-backup and target-database requirements. Distinguish it from
a complete instance image containing multiple databases. Offline restore replacing an existing
instance and REPLACE are outside this exercise. Check privileges, downtime, and target-replacement
requirements in [Restore Syntax](/dbms/reference/sql/syntax/backup-restore-mount-syntax/) and
[Operational Procedures](/dbms/operations-configuration-recovery/backup-restore-mount/) before
executing them separately.

For business consistency across tables, do not rely on backup-command success alone. Define
write-pausing procedures, the business reference point, and cross-table validation criteria
together.
