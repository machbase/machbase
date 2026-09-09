---
type: docs
title: '13.8 Backup, Restore, and Mount'
weight: 90
toc: true
---

Verify backups by mounting or restoring them in an isolated environment and running sample
queries, as well as checking successful creation. Manage paths, permissions, storage, retention,
encryption, and access control together. For complete SQL and options, see
[Backup, Restore, and Mount Syntax](/dbms/reference/sql/syntax/backup-restore-mount-syntax/).

<a id="backup"></a>

## Choose a backup method

| Purpose | Method |
|------|------|
| Full recovery baseline for an instance | Full database backup |
| Move or preserve a specific table | Table backup |
| Changes since a previous backup | Incremental backup |
| Archive a specific time range | Period backup |
| Query a backup while the server runs | Read-only mount |
| Replace instance data | Offline restore |

Before choosing a backup type, check support in the current release for the edition, table
types, incremental chains, mounting, and restoration.

<a id="backup-full"></a>

## Full backup

Keep a full backup as an independent recovery baseline.

- The server process accesses the backup path.
- Check free space and quotas on the destination file system.
- Record start and end times, errors, and output size.
- Do not keep the only backup in the same failure domain as the source data.
- Regularly restore to an isolated server and verify key tables.

<a id="backup-table"></a>

<a id="table-백업"></a>

## Table backup

Check supported table types and which indexes and metadata a table backup includes. To recover
one table, preferably validate it in a new database or mount, then transfer it through an explicit
INSERT or export/import procedure. Do not immediately replace an existing production table.

<a id="backup-incremental-after"></a>

<a id="incremental-backup과-after"></a>

## Incremental backup and AFTER

An incremental backup stores changes since a previous backup. Manage the baseline and all
required incremental backups as one recovery chain.

- Record each backup's baseline and creation order.
- Check recoverability if an intermediate file is missing.
- Do not retain only the final incremental backup.
- Create a new full backup baseline when the chain becomes long.
- For offline restore, pass the final incremental backup path to `machadmin -r` once.
  Do not apply each backup separately starting with the full backup. Preserve the entire required
  chain and verify that the data is restored to the final backup point.

<a id="backup-period"></a>

## Period backup

A period backup specifies start and end times with `BACKUP DATABASE FROM ... TO ...`. Do not
confuse this syntax with a query's `WHERE` clause. Compare minimum and maximum timestamps and
row counts with the source, including the selected time zone and boundary records.

<a id="sql-backup"></a>

## SQL BACKUP

The account running BACKUP needs the required database and table privileges and access to the
server path. In production automation, do not hardcode passwords on the command line. Check
both exit codes and job status.

Checks before and after execution:

1. Verify the target database or table and backup type.
2. Confirm that the destination is a unique path that does not yet exist.
3. Check free space and expected growth.
4. Check backup completion and errors.
5. Verify output files, sizes, and checksums or storage integrity.
6. Validate samples through a mount or restore.

<a id="offline-restore-machadmin-r"></a>

<a id="offline-restore"></a>

## Offline restore

An offline restore with `machadmin -r` replaces the current instance data. Restoration is rejected
if a database already exists. First preserve the current data and verify the recovery target,
then stop the server and remove the existing database using a validated procedure. Online
restoration of a logical database in 8.7.0 Standard Edition uses the separate SQL statement
`RESTORE DATABASE`. Distinguish the targets and prerequisites of the two methods.

- Plan to stop the service and all clients and Collectors.
- Secure a separate backup of current data and a rollback path.
- Verify the exact backup and chain to restore.
- Check compatibility of the release, edition, and configuration.
- Have two recovery operators cross-check the target instance and paths.
- Use production runbooks only after successful isolated recovery drills.
- After restoration, verify schemas, row counts, time ranges, and application queries.

<a id="database-mount"></a>

## Mount a database

Mounting attaches a backup as a read-only database for investigation and selective recovery.

```text
MOUNT DATABASE '/absolute/backup/path' TO mount_name;
UMOUNT DATABASE mount_name;
```

Use a mount name that does not conflict with an active production database. Mount paths and
permissions are evaluated for the server process.

<a id="query-database-mount"></a>

<a id="mounted-database-조회"></a>

## Query a mounted database

```text
SELECT *
FROM mount_name.SYS.table_name
WHERE _ARRIVAL_TIME >= TO_DATE('2026-01-01', 'YYYY-MM-DD');
```

First inspect the table list and schemas, then verify time ranges, row counts, and sample
values. Before selectively transferring data, check the current schema and duplicate handling policy.

<a id="mounted-db-read-only-refcount-active-same-name"></a>

<a id="read-only와-사용-중-mount"></a>

## Read-only access and mounts in use

Do not execute DDL or DML on a mounted database. Open cursors or statements may prevent
unmounting; close all references before retrying. First check for name conflicts with active
databases or other mounts.

<a id="unsupported-support-scope-mount-table-umount"></a>

## Unsupported paths

Do not depend on `MOUNT TABLE` or `UMOUNT TABLE`, which are not public operational APIs, even
if internal syntax appears to succeed. Use the public `MOUNT DATABASE` and `UMOUNT DATABASE` commands.

<a id="table-types-type-backup-mount"></a>

<a id="table-type과-edition-범위"></a>

## Scope by table type and edition

Backup and mount behavior differs among LOG, TAG, TRANSACTION, LOOKUP, and VOLATILE tables.
VOLATILE is an in-memory table whose data does not survive a server restart. Check
[Backup and Mount Support](/dbms/reference/support-scope-constraints/backup-mount/) for table
and edition restrictions.

## Recovery validation checklist

- Database, owner, and table counts
- Key table schemas and indexes
- Row counts and minimum and maximum timestamps
- Sample NULL, string, and numeric values
- Users, privileges, and application connections
- ROLLUP, retention policies, and job status
- Handling of data received after the backup point
- Rollback feasibility and actual recovery duration
