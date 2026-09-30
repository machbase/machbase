---
title: Backup and Mount
type: docs
weight: 61
---

## Introduction

The exponential growth of time-series data, often termed "Industrial Big Data" or associated with Smart-X initiatives, presents significant challenges for traditional data management strategies. Persistently storing vast quantities of sensor readings requires robust mechanisms for data archival, disaster recovery, and historical analysis. Conventional database backup and restore processes, while essential, often suffer from limited scope flexibility, long restoration times, and the inability to access backup contents without a full restore, which can be disruptive and resource-intensive.

Machbase addresses these challenges with **Backup** and **Mount** features tailored for time-series workloads. They support full, incremental, time-based, and table-specific backups and, critically, a **Mount** feature that provides read-only, online access to backup data without a time-consuming restore process.

## Core Concepts

- **Backup:** Creates a physical copy of database data (the entire database, or specific tables or time ranges) in an external storage location. Machbase backups are stored as a directory structure containing the necessary data and metadata files.
- **Restore:** Restores a database from a backup. It is used primarily for disaster recovery or for setting up replica environments. `machbase-neo restore` requires an empty `dbs` directory and refuses to run when existing data is present.
- **Mount:** Attaches a backup directory to a running Machbase instance as a read-only database. This provides immediate query access to the historical "fossilized" data in the backup, without a lengthy restore operation.
- **Unmount:** Detaches a mounted backup database. The backup files are not deleted.
- **Live Data:** The current, active data in the operational Machbase instance, subject to real-time reads and writes.
- **Fossilized Data:** Data contained in a backup, representing an immutable snapshot at a specific point in time (or time range). When mounted, this data is accessible for read operations only.

## Backup Operations

Machbase provides granular control over the backup process, so you can select the scope and type that fit your requirements.

### Full Backup (Database or Table)

Creates a complete copy of either the entire database or the specified table at the time of execution.

```sql
BACKUP DATABASE INTO DISK = 'path/to/backup_directory_name';

BACKUP TABLE table_name INTO DISK = 'path/to/backup_directory_name';
```

- `DATABASE`: Backs up the entire database.
- `TABLE table_name`: Backs up only the named table.
- `INTO DISK = 'path/...'`: Defines the target directory where the backup files are created. The path can be absolute or relative to the `$MACHBASE_HOME/dbs` directory. Specify a new path that the backup process can create; the directory is created if it doesn't exist.

**Considerations:**
- A full backup captures the state of the data at the moment the backup operation starts.
- The output is a directory containing multiple files and subdirectories.

### Incremental Backup (Database or Table)

Captures only the data that has changed since a previous backup (typically a full backup or a prior incremental backup). This significantly reduces backup time and storage space for subsequent backups.

```sql
BACKUP DATABASE AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';

BACKUP TABLE table_name AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';
```

- `AFTER 'path/...'`: Specifies the directory of the *immediately preceding* backup (full or incremental) in the chain. This path **must** exist and be accessible.
- `INTO DISK = 'path/...'`: Defines the target directory for the *new* incremental backup.

**Considerations:**
- Primarily applicable to Log and Tag tables, where data is typically appended.
- Lookup tables are **always** fully backed up, even during an incremental backup, because they can be modified in ways other than appending.
- Requires the previous backup directory to be present and intact.

### Time-Based Backup (Database or Table)

Backs up data within a specific time window. This is useful for archiving time-series data in manageable units such as monthly or quarterly backups.

```sql
BACKUP DATABASE
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';

BACKUP TABLE table_name
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';
```

- `FROM time_expression_start`: Defines the inclusive start time of the backup window. Example: `TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')`.
- `TO time_expression_end`: Defines the inclusive end time of the backup window.

### Disk Backup File Structure

| Path/File | Description |
|:--|:--|
| `<path>/backup.dat` | Backup status and management information. Neo identifies a backup by this file. |
| `<path>/backup.trc` | Trace file for the backup process. |
| Other generated files | Files required for restore and mount, such as data, metadata, and indexes. Keep the entire backup directory. |

## Mount Operations

The Mount feature attaches a backup directory to the running Machbase instance as a read-only database, so you can query backup data immediately without a restore.

### Mounting a Backup

```sql
MOUNT DATABASE '/path/to/backup_directory' TO mount_name;
```

- `'/path/to/backup_directory'`: The path to the directory containing the Machbase backup files (created with `BACKUP ... INTO DISK`).
- `mount_name`: A user-defined alias for the mounted database. Use it to qualify object names when querying the mounted data, in the form `mount_name.user_name.table_name`.

You can mount multiple backups at the same time by giving each one a unique `mount_name`.

### Querying Mounted Data

To access a table in a mounted backup, qualify the table name with the mount name and the original schema owner (typically `sys` for standard tables).

```sql
SELECT column_list
FROM mount_name.user_name.table_name
WHERE [conditions];
```

- `mount_name`: The alias assigned in the `MOUNT DATABASE` command.
- `user_name`: The schema owner of the original table (commonly `sys`).
- `table_name`: The name of the table in the backup.

### Mount Example

```sql
MOUNT DATABASE '/backup/jan_data' TO backup_jan;

-- Querying table 'sensor_data' (owned by 'sys') from a backup mounted as 'backup_jan'
SELECT COUNT(*) FROM backup_jan.sys.sensor_data;
SELECT * FROM backup_jan.sys.sensor_data
 WHERE time BETWEEN TO_DATE('2024-01-05') AND TO_DATE('2024-01-06');
```

### Unmounting a Backup

Detaches a mounted backup database. After unmounting, its contents can no longer be queried through the mount name. The backup files themselves remain untouched on disk.

```sql
UNMOUNT DATABASE mount_name;
```

- `mount_name`: The alias of the mounted database to detach.

## Restore Operations

`machbase-neo restore` restores a backup into the data directory of a stopped instance. It is used primarily for disaster recovery or for setting up identical instances. The target home directory must already exist. If `dbs` does not exist, the command creates it; if `dbs` is not empty, the command fails. Restore does not automatically overwrite existing data.

```bash
machbase-neo restore --data <machbase_home_dir> <path/to/backup_directory>
```

- `--data <machbase_home_dir>`: Specifies the `$MACHBASE_HOME` directory of the target Machbase instance.
- `<path/to/backup_directory>`: The path to the backup directory to restore from.
  - For a full restore, specify the full backup directory.
  - For a restore that involves incremental backups, this **must** be the **last** incremental backup directory in the chain. The restore process automatically locates and uses the preceding backups in the chain (the full backup and intermediate incremental backups).

**Considerations:**
- Restore is an offline operation. Stop the target instance before you run it.
- Confirm the target `$MACHBASE_HOME` and secure the existing data to avoid unintended data loss. Restore fails while `dbs` is not empty.
- If you need to modify backup data, a restore is required; Mount provides read-only access only.

## Advantages and Considerations of Mounting

### Advantages

- **Rapid Data Access:** Provides near-instant access to historical data in backups, without the lengthy durations of traditional restore processes (especially for multi-terabyte datasets).
- **Index Preservation:** Backups retain the original time-series index structures. Mounted databases use these indexes, so queries on historical data perform comparably to queries on live data.
- **Rollup Structure Preservation:** Rollup tables associated with the backed-up tables are also preserved in the backup and can be queried through the mount, allowing consistent statistical analysis across live and historical ("fossilized") data.
- **Online Operation:** Mounting and unmounting run while the primary database instance stays online and operational.
- **Resource Efficiency:** Avoids the significant disk I/O and CPU resources that a full restore would consume just to query historical data.

### Considerations

- **Read-Only Access:** Mounted databases are strictly read-only. `INSERT`, `UPDATE`, `DELETE`, and DDL operations are prohibited. A `RESTORE` operation is required if you need to modify the backup data.
- **Statistics Views:** Real-time statistics views (`v$...`) may not apply to statically mounted backup data. Query the data directly for counts or aggregates.
- **Filesystem Access:** The Machbase server process requires read access to the backup directory.

## Examples

This section provides practical scenarios that demonstrate the Backup and Mount workflow.

Assume two TAG tables, `EQPT_A` and `EQPT_B`, exist and contain time-series data from 2024-01-01 to 2024-06-30.

```sql
CREATE TAG TABLE IF NOT EXISTS EQPT_A (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) tag_partition_count=1;

CREATE TAG TABLE IF NOT EXISTS EQPT_B (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) tag_partition_count=1;

SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM EQPT_A;
SELECT COUNT(*) FROM EQPT_A;
```

### Example 1: Full Database Backup and Mount

```sql
-- 1. Perform a full database backup into a specified directory
-- Use a new target path and ensure Machbase has permission to create it.
BACKUP DATABASE INTO DISK = '/backup/full_db_20240630'; -- Use an appropriate path

-- 2. Mount the backup with an alias 'mount_fulldb'
MOUNT DATABASE '/backup/full_db_20240630' TO mount_fulldb;

-- 3. Query data from the mounted backup
-- Check time range in mounted EQPT_A
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_fulldb.sys.EQPT_A;
-- Check row count in mounted EQPT_A
SELECT COUNT(*) FROM mount_fulldb.sys.EQPT_A;
-- Query specific data from mounted EQPT_B
SELECT name, TO_CHAR(time), value FROM mount_fulldb.sys.EQPT_B LIMIT 5;

-- 4. Unmount the backup when access is no longer needed
UNMOUNT DATABASE mount_fulldb;
```

### Example 2: Time-Range Database Backup and Mount

```sql
-- 1. Backup data only from Jan 1st, 2024 to Mar 31st, 2024
BACKUP DATABASE
    FROM TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/db_2024Q1'; -- Use an appropriate path

-- 2. (Optional) Simulate data aging by deleting older data from the live tables
DELETE FROM EQPT_A BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
DELETE FROM EQPT_B BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
-- Verify live data count has decreased
SELECT COUNT(*) FROM EQPT_A;

-- 3. Mount the time-range backup
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;

-- 4. Query the mounted backup - it should contain the original data for Q1
SELECT COUNT(*) FROM mount_q1.sys.EQPT_A; -- Should match original Q1 count
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_q1.sys.EQPT_A; -- Should show Q1 range

-- Compare counts between live (post-delete) and mounted (pre-delete)
SELECT COUNT(*) AS live_count FROM EQPT_A;
SELECT COUNT(*) AS mounted_q1_count FROM mount_q1.sys.EQPT_A;

-- 5. Unmount the backup
UNMOUNT DATABASE mount_q1;
```

### Example 3: Table-Specific, Time-Range Backup and Mount

```sql
-- 1. Backup only table EQPT_A for the period April 1st to May 15th, 2024
BACKUP TABLE EQPT_A
    FROM TO_DATE('2024-04-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-05-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/eqpta_20240401_20240515'; -- Use an appropriate path

-- 2. Mount the table-specific backup
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;

-- 3. Query the mounted backup
-- Verify time range and count match the specified backup window
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_eqpta_partial.sys.EQPT_A;
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
-- Query raw data sample
SELECT name, TO_CHAR(time), value FROM mount_eqpta_partial.sys.EQPT_A LIMIT 5;

-- Attempting to query EQPT_B from this mount will fail (it wasn't included)
-- SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_B; -- Expected error: table not found

-- 4. Unmount the backup
UNMOUNT DATABASE mount_eqpta_partial;
```

### Example 4: Mounting Multiple Backups Concurrently

```sql
-- Assuming backups from previous examples exist:
-- '/backup/db_2024Q1' (Full DB, Q1)
-- '/backup/full_db_20240630' (Full DB, up to Jun 30)
-- '/backup/eqpta_20240401_20240515' (EQPT_A only, Apr 1 - May 15)

-- 1. Mount all three backups with unique aliases
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;
MOUNT DATABASE '/backup/full_db_20240630' TO mount_jun30;
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;

-- 2. Query data across different mounts
-- Count from EQPT_A in Q1 backup
SELECT COUNT(*) FROM mount_q1.sys.EQPT_A;
-- Count from EQPT_B in the full backup
SELECT COUNT(*) FROM mount_jun30.sys.EQPT_B;
-- Count from EQPT_A in the partial table backup
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
-- Attempt to count EQPT_B from the partial backup (will fail)
-- SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_B;

-- 3. Unmount all backups when finished
UNMOUNT DATABASE mount_q1;
UNMOUNT DATABASE mount_jun30;
UNMOUNT DATABASE mount_eqpta_partial;
```

By combining Backup and Mount in this way, you can keep live data lean while querying or comparing historical data immediately. Perform a full restore when needed, or mount backups to reference historical data quickly in read-only mode.
