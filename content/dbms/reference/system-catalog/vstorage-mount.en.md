---
type: docs
title: '16.3.4 V$STORAGE_MOUNT_DATABASES Dictionary'
weight: 50
toc: true
---

`V$STORAGE_MOUNT_DATABASES` lists backup databases mounted read-only
on the current instance.

## Columns

| Column | Type | Description |
|---|---|---|
| `NAME` | VARCHAR | Backup database name |
| `PATH` | VARCHAR | Original backup image path |
| `BACKUP_TBSID` | LONG | Backup tablespace identifier |
| `BACKUP_SCN` | LONG | backup SCN |
| `BACKUP_SCN` | LONG | Backup SCN |
| `MOUNTDB` | VARCHAR | Database alias specified for MOUNT |
| `DB_BEGIN_TIME` | VARCHAR | Start timestamp of backup data |
| `DB_END_TIME` | VARCHAR | End timestamp of backup data |
| `BACKUP_BEGIN_TIME` | VARCHAR | Backup operation start timestamp |
| `BACKUP_END_TIME` | VARCHAR | Backup operation end timestamp |

| `FLAG` | INTEGER | Internal status flags. Do not infer their meaning |

```sql
SELECT NAME, PATH, MOUNTDB,
       DB_BEGIN_TIME, DB_END_TIME,
       BACKUP_BEGIN_TIME, BACKUP_END_TIME
  FROM V$STORAGE_MOUNT_DATABASES
 ORDER BY MOUNTDB;
```

## Query

```sql
MOUNT DATABASE '/data/backup/sc15_snapshot' TO backup_check;

SELECT *
  FROM backup_check.sys.target_table
 LIMIT 10;

UMOUNT DATABASE backup_check;
```

## MOUNT and Query Example
Operands appear in this order: backup path, `TO`, and alias. Query mounted database objects
with the three-part name `mount_alias.owner.table`. For complete privileges and safety restrictions,
see [BACKUP/RESTORE/MOUNT Syntax](/dbms/reference/sql/syntax/backup-restore-mount-syntax/).
