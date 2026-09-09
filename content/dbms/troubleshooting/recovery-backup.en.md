---
type: docs
title: '15.5 Backup and Recovery Problems'
weight: 50
toc: true
---

<a id="failure-backup-restore"></a>

## Backup or restore fails

For backup failures, check path permissions for the server process's OS account, available
space, existing backups at the same path, and server logs.

```sql
SELECT * FROM V$STORAGE_USAGE;
```

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

Restoration is destructive: it replaces the existing physical database. Stopping the running
server alone is insufficient; restoration is rejected if the current database still exists.
The following is a conceptual checklist, not commands to copy into production.

```text
1. Verify the recovery target, backup path, version, and checksums.
2. Obtain approval for preserving the current database and defining rollback conditions.
3. Shut down the server normally.
4. Follow the approved procedure to remove the current physical database.
5. Run machadmin restore.
6. Start the server and run application validation queries.
```

`machadmin -d` destroys the current database. Do not run it without a backup and explicit
approval. For exact restoration syntax and restrictions, see
[BACKUP/RESTORE/MOUNT Syntax](/dbms/reference/sql/syntax/backup-restore-mount-syntax/).

Checking a backup image or successfully mounting it is only preliminary validation and does
not guarantee complete recoverability. Regularly restore and validate applications in a
separate environment.

<a id="failure-mount"></a>

## Mounting fails

Check current mounts, a unique alias, the backup path, and read permissions for the server process.

```sql
SELECT * FROM V$STORAGE_MOUNT_DATABASES;
```

The current syntax places the alias after the backup path.

```sql
MOUNT DATABASE '/backup/sc15_snapshot' TO backup_check;
SELECT COUNT(*) FROM backup_check.sys.target_table;
UMOUNT DATABASE backup_check;
```

Distinguish alias conflicts, unsupported editions, incompatible backups, and mounted
databases in use. Do not forcibly delete files or modify server metadata.
