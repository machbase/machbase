---
type: docs
title: '16.2.1 Configuration Property Dictionary'
weight: 10
toc: true
---

This dictionary lists the main Standard Edition properties configured in
`$MACHBASE_HOME/conf/machbase.conf`. A server restart is required unless otherwise stated.

## Basic Server Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `PORT_NO` | 5656 | 1024~65535 | Client TCP/IP connection port |
| `BIND_IP_ADDRESS` | 0.0.0.0 | - | Client listener bind IP. `0.0.0.0` means all interfaces |
| `GRANT_REMOTE_ACCESS` | 1 | 0~1 | Allows remote access. 0 allows local access only |
| `MAX_SESSION_COUNT` | 4096 | 64~2^64-1 | Maximum concurrent sessions |
| `MAX_STMT_COUNT_PER_SESSION` | 1024 | 512~2^32-1 | Maximum statements per session |
| `SESSION_IDLE_TIMEOUT_SEC` | 0 | 0~2^64-1 | Session idle timeout in seconds. 0 disables it |
| `SESSION_QUERY_TIMEOUT_SEC` | 0 | 0~2^64-1 | Query execution timeout in seconds. 0 disables it |
| `UNIX_PATH` | machbase-unix | - | Unix domain socket filename |
| `DBS_PATH` | ?/dbs | - | Database file directory (`?` means `$MACHBASE_HOME`) |
| `PID_PATH` | ?/conf | - | PID file directory |

## CPU and Thread Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `CPU_COUNT` | 1 | 0~2^32-1 | CPUs to use. 0 uses all CPUs |
| `CPU_PARALLEL` | 1 | 1~2^32-1 | Parallel threads per CPU |
| `CPU_AFFINITY_BEGIN_ID` | 0 | 0~2^32-1 | Starting CPU affinity ID |
| `CPU_AFFINITY_COUNT` | 0 | 0~2^32-1 | CPUs used for affinity. 0 means all |
| `DISK_IO_THREAD_COUNT` | 3 | 1~2^32-1 | Disk I/O threads |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 0~2^32-1 | Index build threads. 0 disables index creation |
| `INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT` | 3 | 1~1024 | LSM index merge threads |
| `INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT` | 1 | 1~1024 | Threads that delete obsolete LSM index files |
| `QUERY_PARALLEL_FACTOR` | 0 | 0~100 | Parallel query execution threads. Default: 0 for Standard, 4 for Cluster |

## Memory Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `PROCESS_MAX_SIZE` | 8GB | 1GB~2^64-1 | Maximum server process memory in bytes. Distribution samples may specify `16GB` |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 256MB~2^64-1 | Log table ingestion buffer limit. Adjust within the total memory budget |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE` | 100MB | 1MB~2^64-1 | Memory preallocated at server startup |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE` | 2MB | 1MB~2^64-1 | Column partition memory block size |
| `DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE` | 2MB | 1MB~2^32-1 | Initial doublewrite file size for data consistency and recovery |
| `DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE` | 1MB | 1MB~2^32-1 | Doublewrite file growth increment |
| `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` | 2GB | 0~2^64-1 | Maximum page cache size in bytes |
| `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` | 2GB | 0~2^64-1 | Total memory limit for Volatile/Lookup tables |
| `MAX_QPX_MEM` | 1GB | 1MB~2^64-1 | Maximum query processor memory for GROUP BY, ORDER BY, and similar operations |
| `MEMORY_ROW_TEMP_TABLE_PAGESIZE` | 32768 | 8KB~2^32-1 | Volatile/Lookup temporary table page size in bytes |

## Disk I/O Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `DISK_BUFFER_COUNT` | 16 | 1~2^32-1 | Disk I/O buffers |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 0~1 | Enables direct I/O for writes. Set to 0 for unsupported filesystems such as ZFS |
| `DISK_TABLESPACE_DIRECT_IO_READ` | 0 | 0~1 | Enables direct I/O for reads |
| `DISK_TABLESPACE_DIRECT_IO_FSYNC` | 0 | 0~1 | Enables fsync with direct I/O |
| `DISK_TABLESPACE_SYNCHRONOUS` | 1 | 0~3 | Synchronization policy. 0=OFF, 1=NORMAL, 2=FULL, 3=EXTRA |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | 0~2^32-1 | Partition file disk write interval in seconds |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE` | 0 | 0~1 | Whether to flush column partitions only when full |
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 1~2^32-1 | Table checkpoint interval in seconds |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 1~2^32-1 | Index checkpoint interval in seconds |
| `DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE` | 1 | 0~1 | For reversed LOG timestamps: 1=adjust to previous timestamp+1ns, 0=reject ingestion |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT` | 80 | 0~100 | Memory usage threshold (%). Ingestion slows above this threshold |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC` | 1 | 0~2^32-1 | Wait per record in ms above the threshold |

For LOG tables, `DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE=1` does not mean an explicitly supplied
past timestamp is stored unchanged.
Values earlier than the preceding `_ARRIVAL_TIME` are adjusted. Equal timestamps do not satisfy
this reversal condition, so this setting does not make every row's timestamp unique.
During migration, also check ordering and target state in the
[time model](/dbms/log-table-usage/arrival-time-model/).

## Index Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `DEFAULT_LSM_MAX_LEVEL` | 2 | 0~3 | Default maximum LSM index level |
| `INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD` | 100000 | 1~2^32-1 | Unindexed record count that triggers an index build |
| `INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX` | 3 | 1~2^32-1 | Maximum flush requests per index |
| `INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT` | 70 | 0~100 | Maximum memory usage percentage for LSM index builds |
| `DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH` | 0 | 0~1 | Whether to flush all indexes to disk at shutdown |
| `DISK_COLUMNAR_INDEX_FDCACHE_COUNT` | 0 | 0~2^32-1 | Open index partition file descriptors |
| `DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT` | 0 | 0~2^32-1 | Open column file descriptors |
| `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` | 100MB | 0~2^64-1 | `_ARRIVAL_TIME` column MINMAX cache size in bytes |

## TAG Table Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `TAG_CACHE_ENABLE` | 31 | 0~31 | TAG cache scope (bitwise OR). 0=disabled, 1=map, 2=row, 4=data file, 8=varchar file, 16=delete vector |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 512MB | 32KB~2^64-1 | Maximum memory per TAG cache pool in bytes |
| `TAG_CACHE_POOL_COUNT` | 1 | 1~128 | TAG cache pools. Total limit = `TAG_CACHE_MAX_MEMORY_SIZE × TAG_CACHE_POOL_COUNT` |
| `TAG_MEMORY_INDEX_TYPE` | 1 | 0~1 | Memory index type. 0=RBTree, 1=BTree |
| `TAG_MEMORY_INDEX_PANOUT` | 255 | 127~65536 | B-tree index fanout. Applies when `TAG_MEMORY_INDEX_TYPE=1` |
| `TAGDATA_AUTO_META_INSERT` | 2 | 0~2 | Action when TAG_NAME is missing. 0=fail, 1=insert name only, 2=insert with metadata |
| `TAG_TABLE_META_MAX_SIZE` | 524288000 | 1MB~2^32-1 | Maximum TAGDATA table metadata memory in bytes |
| `TAG_PARTITION_COUNT` | 4 | 1~1024 | Tag table key-value partitions |
| `TAG_DATA_PART_SIZE` | 16MB | 1MB~1GB | Tag data partition size in bytes |
| `ROLLUP_FETCH_COUNT_LIMIT` | 3000000 | 0~2^32-1 | Rows fetched per rollup thread iteration. 0=unlimited |

## Security Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `ENABLE_CASE_SENSITIVE_PASSWORD` | 0 | 0~1 | Case-sensitive passwords. 0 converts passwords to uppercase |

## Session and Query Settings

`TABLE_SCAN_DIRECTION` is not exclusive to TAG tables. It can also affect queries that use scan
direction on LOG and other tables, and does not guarantee final result ordering.
Use ORDER BY to specify output order and EXPLAIN to check the actual access path.

| Property | Default | Range | Description |
|----------|--------|------|------|
| `TABLE_SCAN_DIRECTION` | 0 | -1~1 | -1=reverse, 0=table type default, 1=forward |
| `DDL_LOCK_TIMEOUT` | 0 | 0~1000000 | Standard Edition DDL lock wait in seconds. 0 returns an error immediately |
| `SHOW_HIDDEN_COLS` | 0 | 0~1 | Whether `SELECT *` includes `_ARRIVAL_TIME` |
| `DURATION_BEGIN` | 0 | 0~2^32-1 | Default start offset in seconds for SELECT without `DURATION` |
| `DURATION_GAP` | 0 | 0~2^31-1 | Default duration in seconds for SELECT without `DURATION` |
| `LOOKUP_APPEND_UPDATE_ON_DUPKEY` | 0 | 0~1 | Duplicate key handling for Lookup table Append. 0=fail, 1=UPDATE |
| `LIN_HASH_BIT_SIZE` | 7 | 1~31 | Initial bucket bits for internal linear hashing |

After a server restart, `DDL_LOCK_TIMEOUT` in `machbase.conf` is copied to new sessions. Change the
current session value with `ALTER SESSION SET DDL_LOCK_TIMEOUT = seconds` and check it in `V$SESSION`.
Cluster Edition does not provide this property.

## TRANSACTION Settings

| Property | Default | Range | Description |
|----------|--------|------|------|
| `TRANSACTION_BUSY_TIMEOUT_MS` | 30000 | -1~2147483647 | Wait in ms for retryable TRANSACTION lock conflicts. -1 waits until cancellation or release; 0 returns immediately |
| `TRANSACTION_SYNCHRONOUS` | 2 | 1~2 | TRANSACTION table transaction durability. 1=NORMAL, 2=FULL |
| `TRANSACTION_JOURNAL_MODE` | 4 | 0~4 | TRANSACTION journal mode. 0=DELETE, 4=WAL |

New sessions copy the server's TRANSACTION_BUSY_TIMEOUT_MS. Use ALTER SESSION to change it for
the current connection. This value does not guarantee a minimum wait for every busy error.
In WAL mode, upgrading an obsolete read snapshot to a write can fail immediately even with -1.
In that case, do not repeat the same statement: ROLLBACK and repeat the reads and decisions in
a new transaction. The [two-connection exercise](/dbms/rdb-table-usage/locking-conflict-timeout/)
compares temporary write locks with snapshot conflicts.

## Logging and Diagnostics

| Property | Default | Range | Description |
|----------|--------|------|------|
| `TRACE_LOG_LEVEL` | 277 | 0~2^32-1 | Trace log verbosity. Higher values provide more detail |
| `TRACE_LOGFILE_PATH` | ?/trc | - | Trace log directory |
| `TRACE_LOGFILE_SIZE` | 10MB | 1MB~2^32-1 | Maximum trace log file size in bytes |
| `TRACE_LOGFILE_COUNT` | 1000 | 1~2^32-1 | Maximum trace log files |
| `DUMP_TRACE_INFO` | 300 | 0~2^32-1 | Interval in seconds for writing DBMS status to trc. 0 disables it |
| `DUMP_APPEND_ERROR` | 0 | 0~1 | Logs Append API errors to trc. Recommended for testing only |
| `FEEDBACK_APPEND_ERROR` | 1 | 0~1 | Sends Append error data to the client |
| `GEN_CORE_FILE` | 1 | 0~1 | Generates a core file on abnormal termination |
| `GEN_CALLSTACK_FOR_ABORT_ERROR` | 0 | 0~1 | Records a call stack on abnormal termination |

## Property Query Examples

```sql
-- Query all current property values
SELECT name, value, type FROM v$property ORDER BY name;

-- Query details for a specific property
SELECT name, value, min, max
  FROM v$property
 WHERE name = 'MAX_SESSION_COUNT';
```

Dynamically configurable properties can be changed with `ALTER SYSTEM SET` without a server restart.

```sql
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET SESSION_QUERY_TIMEOUT_SEC = 30;
```
