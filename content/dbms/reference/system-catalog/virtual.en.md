---
type: docs
title: '16.3.2 Virtual Table Dictionary'
weight: 20
toc: true
---

Virtual tables (dynamic views) use the `V$` prefix and expose current Machbase server status as
tables. They are read-only and return the latest state on each query.

## Virtual Tables

| Category | Table | Description |
|---------|------------|------|
| Session/System | `V$VERSION` | Server version information |
| Session/System | `V$SESSION` | Connected sessions |
| Database | `V$DATABASES` | Active/mounted database status |
| Database | `V$DATABASE_OPERATIONS` | Database lifecycle operation history |
| Session/System | `V$STMT` | Running SQL statements |
| Session/System | `V$PROPERTY` | Current server settings |
| Session/System | `V$SYSMEM` | System memory usage |
| Session/System | `V$SYSSTAT` | System statistics |
| Session/System | `V$SYSTIME` | System time statistics |
| Storage | `V$STORAGE` | Storage file size summary |
| Storage | `V$STORAGE_USAGE` | Disk usage and usage limit ratio |
| Storage | `V$STORAGE_TABLES` | Storage usage per table |
| Storage | `V$STORAGE_MOUNT_DATABASES` | Mounted backup databases |
| Tag Rollup | `V$ROLLUP` | Rollup job status |
| TAG Table | `V$<TABLE>_STAT` | Per-table tag and axis statistics. The actual name is generated from the TAG table name |
| License | `V$LICENSE_INFO` | License information |
| Locking | `V$MUTEX` | Lock status |

`V$<TABLE>_STAT` is generated dynamically for each TAG table and is separate from the fixed list
of global virtual tables. For column names and types by time and distance axis, see
[Per-tag Statistics Views](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema).

## V$VERSION

Returns server version information.

| Column | Description |
|----------|------|
| `BINARY_SIGNATURE` | Server version string |

```sql
SELECT binary_signature FROM v$version;
```

## V$DATABASES

Returns the status of logical and mounted databases. `DATABASE_ID` identifies a logical
catalog and differs from `TABLESPACE_ID`.

| Column | Description |
|------|------|
| `DATABASE_ID` | Logical database identifier |
| `SOURCE_DATABASE_ID` | Source database identifier of a mounted backup |
| `NAME` | Database name or mount alias |
| `KIND` | `ACTIVE` or `MOUNTED` |
| `ACCESS_MODE` | `READ_WRITE` or `READ_ONLY` |
| `CAN_USE` | Whether the database can be selected with `USE` |
| `STATE` | Lifecycle state |
| `IS_DEFAULT` | Whether this is the default `MACHBASEDB` |

```sql
SELECT database_id, name, kind, access_mode, can_use, state, is_default
  FROM v$databases
 ORDER BY database_id;
```

## V$DATABASE_OPERATIONS

Returns status and errors for `CREATE`, `ALTER`, `DROP`, `BACKUP`, `RESTORE`, `MOUNT`, and `UMOUNT`
operations. For `FAILED_NEEDS_ACTION`, also inspect the actual `V$DATABASES` state and
server log.

| Column | Description |
|------|------|
| `OPERATION_ID` | Operation identifier |
| `DATABASE_ID` | Target logical database identifier |
| `DATABASE_NAME` | Target database name |
| `STATE` | Operation state |
| `LAST_ERROR` | Failure cause |
| `CREATED_AT` | Creation timestamp |
| `UPDATED_AT` | Last update timestamp |

```sql
SELECT operation_id, database_name, state, last_error
  FROM v$database_operations
 ORDER BY operation_id DESC;
```

## V$SESSION

Lists connected sessions and their status.

| Column | Description |
|----------|------|
| `ID` | Session identifier |
| `CLOSED` | Whether the connection is closed (0: active) |
| `USER_ID` | User identifier |
| `LOGIN_TIME` | Connection timestamp |
| `CLIENT_TYPE` | Connected client type |
| `USER_NAME` | Username |
| `USER_IP` | User IP address |
| `SQL_LOGGING` | Whether trace logging is enabled for the session |
| `IDLE_TIMEOUT` | Idle session termination timeout in seconds |
| `QUERY_TIMEOUT` | Query response timeout |

```sql
-- List currently active sessions
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

## V$STMT

Displays information about SQL statements that are running or waiting.

| Column | Description |
|----------|------|
| `ID` | Query identifier |
| `SESS_ID` | Identifier of the session executing the query |
| `STATE` | Query state |
| `RECORD_SIZE` | SELECT result record size |
| `QUERY` | Query text |

```sql
-- Check running queries
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

## V$PROPERTY

Returns all server property values.

| Column | Description |
|----------|------|
| `NAME` | Property name |
| `VALUE` | Current value |
| `TYPE` | Data type |
| `DEFLT` | Default value |
| `MIN` | Minimum value |
| `MAX` | Maximum value |

```sql
-- Check specific settings
SELECT name, value, deflt
  FROM v$property
 WHERE name IN ('PORT_NO', 'TRACE_LOG_LEVEL', 'MAX_SESSION_COUNT');

-- Query settings that differ from defaults
SELECT name, value, deflt
  FROM v$property
 WHERE value != deflt
 ORDER BY name;
```

## V$STORAGE_USAGE

Displays storage system disk usage.

| Column | Description |
|----------|------|
| `TOTAL_SPACE` | Total capacity of the storage containing the data directory |
| `USED_SPACE` | Used capacity |
| `USED_RATIO` | Usage ratio (%) |
| `RATIO_CAP` | Usage limit (ingestion stops when exceeded) |

```sql
SELECT total_space, used_space, used_ratio, ratio_cap
  FROM v$storage_usage;
```

## V$SYSMEM

Returns system memory usage.

| Column | Description |
|----------|------|
| `ID` | Memory manager identifier |
| `NAME` | Memory manager name |
| `USAGE` | Current usage |
| `MAX_USAGE` | Recorded peak usage |

```sql
SELECT name, usage, max_usage
  FROM v$sysmem
 ORDER BY usage DESC;
```

## V$LICENSE_INFO

Returns server license information.

| Column | Description |
|----------|------|
| `ID` | License ID |
| `ISSUE_DATE` | Issue date |
| `TYPE` | License type |
| `CUSTOMER` | Customer name |
| `PROJECT` | Project name |
| `INSTALL_DATE` | Installation date |
| `VIOLATE_STATUS` | License violation status |
| `VIOLATE_MSG` | License violation message |

```sql
SELECT id, type, customer, issue_date,
       install_date, violate_status, violate_msg
  FROM v$license_info;
```

## Listing All Virtual Tables

```sql
-- List all V$ virtual tables available on the current server
SELECT name
  FROM v$tables
 WHERE name LIKE 'V$%'
 ORDER BY name;
```

> Virtual tables are read-only. Tables available only in Cluster Edition, such as V$NODE_STATUS and V$REPLICATION, cannot be queried in Standard Edition.
