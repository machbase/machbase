---
type: docs
title: 'BACKUP / RESTORE / MOUNT syntax'
weight: 170
toc: true
---

Machbase backup, restore, and mount statements protect data, recover it when needed, and query
historical data.

> **Privileges**: Ordinary users need separate privileges for backup and mount.
> ```sql
> GRANT BACKUP ON DATABASE database_name TO user_name;
> GRANT MOUNT  ON DATABASE MACHBASEDB TO user_name;
> ```

---

## BACKUP

### Logical Database Backup

Standard Edition 8.7.0 supports logical backups with an explicit target catalog.

```sql
backup_logical_database_stmt ::=
    'BACKUP DATABASE' database_name
    [ 'AFTER' 'backup_path_or_lsn' ]
    'INTO DISK' '=' 'backup_path'
```

```sql
BACKUP DATABASE factory_a INTO DISK = '/backup/factory_a_20260806';
BACKUP DATABASE factory_a AFTER '/backup/factory_a_20260806'
  INTO DISK = '/backup/factory_a_inc';
```

A logical backup targets one active database catalog. A full-instance image containing multiple
active databases cannot be input to logical MOUNT or RESTORE.

### Full Backup

```sql
backup_database_stmt ::=
    'BACKUP DATABASE INTO DISK' '=' 'backup_path'
    [ 'IMPORT MODE' ]
```

Saves the entire current database to the specified path. This is an online backup that does not stop
the server.

```sql
-- Full backup to an absolute path
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- Relative path (under $MACHBASE_HOME/dbs)
BACKUP DATABASE INTO DISK = 'backup_20240101';
```

- An existing backup_path causes an error. Use a unique name, for example including a date.
- The command blocks until the backup completes.

### Incremental Backup

```sql
backup_incremental_stmt ::=
    'BACKUP DATABASE AFTER' 'backup_path_or_lsn'
    'INTO DISK' '=' 'backup_path'
```

Backs up relative to the last full or incremental backup. Distinguish storage behavior by table
type. TRANSACTION storage is included as a complete snapshot at the backup point even in incremental
images, so do not estimate it as a changed-row delta or changed-data-sized increment. Compare backup
and current data in [TRANSACTION Backup Validation](/dbms/rdb-table-usage/backup-restore-mount/).

```sql
-- Incremental backup after the full backup
BACKUP DATABASE AFTER '/backup/machbase_20240101'
INTO DISK = '/backup/incr_20240102';
```

### Time-Range Backup

```sql
backup_period_stmt ::=
    'BACKUP DATABASE'
    'FROM' datetime_expr 'TO' datetime_expr
    'INTO DISK' '=' 'backup_path'
```

Backs up only data in the specified time range.

```sql
BACKUP DATABASE
FROM TO_DATE('2024-01-01','YYYY-MM-DD')
TO   TO_DATE('2024-02-01','YYYY-MM-DD')
INTO DISK = '/backup/period_jan';
```

### Table Backup

```sql
backup_table_stmt ::=
    'BACKUP TABLE' table_name 'INTO DISK' '=' 'backup_path'
```

Selectively backs up a table instead of the entire database.

```sql
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';
```

---

## RESTORE

Existing machadmin -r recovery restores an instance offline with the server stopped. Standard
Edition 8.7.0 also supports online RESTORE DATABASE to a new logical catalog or to replace a READ
ONLY target.

```sql
restore_database_stmt ::=
    'RESTORE DATABASE' database_name 'FROM DISK' '=' 'backup_path'
    [ 'REMAP OWNER' old_owner 'TO' new_owner ]
    [ 'REPLACE' ]
```

```sql
RESTORE DATABASE factory_a_copy
  FROM DISK = '/backup/factory_a_20260806'
  REMAP OWNER APP_A TO APP_ARCHIVE;

RESTORE DATABASE factory_a
  FROM DISK = '/backup/factory_a_20260806'
  REPLACE;
```

RESTORE DATABASE is SYS-only. A REPLACE target must be READ ONLY with no active references.
Database/table privileges are not inherited automatically after restore and must be granted again.
Unsupported objects or owner conflicts in the backup image can fail the entire restore.

### Offline Instance Restore (`machadmin -r`)

Prepare and validate a backup SQL file before running the restore procedure.

```sql
-- /secure/path/pre_restore_backup.sql
BACKUP DATABASE INTO DISK = '/backup/before_restore';
```

```bash
# 1. Back up current data before restore
machsql -s 127.0.0.1 -P 5656 -u SYS \
  -f /secure/path/pre_restore_backup.sql

# 2. Stop the server
machadmin -s

# 3. Destroy the current database
machadmin -d

# 4. Restore from the backup
machadmin -r /backup/machbase_20240101

# 5. Start the server
machadmin -u
```

machadmin -d destroys the current database. Verify the recovery target, backup, and rollback plan,
and execute only after explicit approval. Restore completely replaces the current database with its
backup-time state.

### Restoring an Incremental Backup

Specify the final incremental backup path once. Incremental backups contain chain information, so
repeated application starting from the full backup is unnecessary.

```bash
machadmin -s
machadmin -d
machadmin -r /backup/incr_20240103
machadmin -u
```

### Main machadmin Options

| Option | Description |
|------|------|
| `-s` (`--shutdown`) | Shut down the server normally |
| `-k` (`--kill`) | Force server termination |
| `-u` (`--startup`) | Start the server |
| `-d` (`--destroydb`) | Destroy the current database |
| `-r path` (`--restore`) | Restore from the specified backup path |

---

## MOUNT DATABASE

```sql
mount_database_stmt ::=
    'MOUNT DATABASE' 'backup_database_path' 'TO' mount_name
```

Attaches a single-catalog backup image as a mounted database without stopping the server or
replacing an active database. Mounted databases are always READ ONLY and cannot become the current
database through USE.

- backup_database_path: backup directory created using DISK.
- mount_name: database alias used to access the mounted database.

```sql
-- Mount an absolute path
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- Relative path (under $MACHBASE_HOME/dbs)
MOUNT DATABASE 'machbase_20240101' TO backup_db;
```

### Querying Mounted Databases

Access mounted tables as mount_name.user_name.table_name. Queries require both USAGE on the mounted
database and SELECT on the target table.

```sql
-- Query a mounted database table
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-01','YYYY-MM-DD');

-- Join current and mounted database tables
SELECT a.name, a.value AS current_val, b.value AS backup_val
  FROM sensor_log a
  JOIN backup_db.sys.sensor_log b ON a.name = b.name;
```

---

## UMOUNT DATABASE

```sql
umount_database_stmt ::=
    'UMOUNT DATABASE' mount_name
```

Detaches a mounted database.

```sql
UMOUNT DATABASE backup_db;
```

Unmount fails if open cursors or running queries reference the mounted database. End the relevant
sessions and retry.

---

## Limitations and Considerations

| Item | Description |
|------|------|
| Writes to mounted databases | Unsupported; read-only |
| Mounting IBFILE backups | Unsupported; only DISK backups can be mounted |
| Version compatibility | Backup and current server metadata versions must be compatible |
| Time-range restore for TAG tables | Unsupported; use full or incremental backups |
| Cluster Edition | Multiple databases and MOUNT/UMOUNT unsupported |

---

## Related Documentation

- [Backup, Restore, and Mount Operations](/dbms/operations-configuration-recovery/backup-restore-mount/) — Detailed procedures and automation examples
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) — Backup and mount privileges
