---
type: docs
title: '16.6.8 Backup/Mount Support'
weight: 80
toc: true
---

Backup saves data to files. Mount connects saved backup files to the database for querying.

## Support by Edition

| Feature | Standard | Cluster | Notes |
|------|:--------:|:-------:|------|
| Multiple logical databases | O | X | Standard Edition only |
| BACKUP DATABASE | O | O | Back up an entire database |
| BACKUP TABLE | O | O | Back up a specific table |
| MOUNT DATABASE | O | X | Not supported in Cluster Edition |
| UMOUNT DATABASE | O | X | Not supported in Cluster Edition |
| machadmin -r restore | O | X | Not supported in Cluster Edition |

`BACKUP DATABASE database_name INTO DISK` backs up one active logical database.
A full-instance image containing multiple active databases cannot be used as input to logical
`MOUNT` or `RESTORE DATABASE`. Querying a mounted database requires `USAGE` and table `SELECT`.
`USE` and writes are not supported.

## Backup Support by Table Type

| Table Type | BACKUP | Query After MOUNT | Notes |
|------------|:-----------:|:------------:|------|
| TAG tables | O | O | |
| LOG tables | O | O | |
| LOOKUP tables | O | O | |
| TRANSACTION tables | O | O | |
| VOLATILE tables | X | X | In-memory data cannot be backed up |


## Canonical References

- Syntax: [BACKUP · RESTORE · MOUNT](../../sql/syntax/backup-restore-mount-syntax/)
- Operations: [Backup, Restore, and Mount](../../../operations-configuration-recovery/backup-restore-mount/)
