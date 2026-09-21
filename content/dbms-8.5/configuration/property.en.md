---
layout : post
title : Property
type : docs
weight: 0
---

Properties are the settings used by the Machbase server, stored as key-value pairs in the `$MACHBASE_HOME/conf/machbase.conf` file.

These values are set when the Machbase server starts and are used continuously at runtime. To change them for performance tuning, you must understand what each value means and set it carefully.

## Index

- [Index](#index)
- [CPU_AFFINITY_BEGIN_ID](#cpu_affinity_begin_id)
- [CPU_AFFINITY_COUNT](#cpu_affinity_count)
- [CPU_COUNT](#cpu_count)
- [CPU_PARALLEL](#cpu_parallel)
- [DBS_PATH](#dbs_path)
- [DEFAULT_LSM_MAX_LEVEL](#default_lsm_max_level)
- [DISK_BUFFER_COUNT](#disk_buffer_count)
- [DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC](#disk_columnar_index_checkpoint_interval_sec)
- [DISK_COLUMNAR_INDEX_FDCACHE_COUNT](#disk_columnar_index_fdcache_count)
- [DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH](#disk_columnar_index_shutdown_build_finish)
- [DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE](#disk_columnar_page_cache_max_size)
- [DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC](#disk_columnar_table_checkpoint_interval_sec)
- [DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT](#disk_columnar_table_column_fdcache_count)
- [DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE](#disk_columnar_table_column_minmax_cache_size)
- [DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE](#disk_columnar_table_column_part_flush_mode)
- [DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC](#disk_columnar_table_column_part_io_interval_min_sec)
- [DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE](#disk_columnar_table_time_inversion_mode)
- [DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE](#disk_columnar_tablespace_dwfile_ext_size)
- [DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE](#disk_columnar_tablespace_dwfile_int_size)
- [DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE](#disk_columnar_tablespace_memory_ext_size)
- [DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE](#disk_columnar_tablespace_memory_max_size)
- [DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE](#disk_columnar_tablespace_memory_min_size)
- [DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT](#disk_columnar_tablespace_memory_slowdown_high_limit_pct)
- [DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC](#disk_columnar_tablespace_memory_slowdown_msec)
- [DISK_IO_THREAD_COUNT](#disk_io_thread_count)
- [DISK_TABLESPACE_DIRECT_IO_FSYNC](#disk_tablespace_direct_io_fsync)
- [DISK_TABLESPACE_DIRECT_IO_READ](#disk_tablespace_direct_io_read)
- [DISK_TABLESPACE_DIRECT_IO_WRITE](#disk_tablespace_direct_io_write)
- [DISK_TABLESPACE_SYNCHRONOUS](#disk_tablespace_synchronous)
- [DUMP_APPEND_ERROR](#dump_append_error)
- [DUMP_TRACE_INFO](#dump_trace_info)
- [DURATION_BEGIN](#duration_begin)
- [DURATION_GAP](#duration_gap)
- [ENABLE_CASE_SENSITIVE_PASSWORD](#enable_case_sensitive_password)
- [FEEDBACK_APPEND_ERROR](#feedback_append_error)
- [GEN_CALLSTACK_FOR_ABORT_ERROR](#gen_callstack_for_abort_error)
- [GEN_CORE_FILE](#gen_core_file)
- [GRANT_REMOTE_ACCESS](#grant_remote_access)
- [BIND_IP_ADDRESS](#bind_ip_address)
- [HTTP_AUTH](#http_auth)
- [HTTP_ENABLE](#http_enable)
- [HTTP_MAX_MEM](#http_max_mem)
- [HTTP_PORT_NO](#http_port_no)
- [HTTP_THREAD_COUNT](#http_thread_count)
- [INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD](#index_build_max_row_count_per_thread)
- [INDEX_BUILD_THREAD_COUNT](#index_build_thread_count)
- [INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX](#index_flush_max_request_count_per_index)
- [INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT](#index_level_partition_ager_thread_count)
- [INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT](#index_level_partition_build_memory_high_limit_pct)
- [INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT](#index_level_partition_build_thread_count)
- [LIN_HASH_BIT_SIZE](#lin_hash_bit_size)
- [LOOKUP_APPEND_UPDATE_ON_DUPKEY](#lookup_append_update_on_dupkey)
- [MAX_QPX_MEM](#max_qpx_mem)
- [MAX_SESSION_COUNT](#max_session_count)
- [MAX_STMT_COUNT_PER_SESSION](#max_stmt_count_per_session)
- [SESSION_IDLE_TIMEOUT_SEC](#session_idle_timeout_sec)
- [SESSION_QUERY_TIMEOUT_SEC](#session_query_timeout_sec)
- [MEMORY_ROW_TEMP_TABLE_PAGESIZE](#memory_row_temp_table_pagesize)
- [PID_PATH](#pid_path)
- [PORT_NO](#port_no)
- [PROCESS_MAX_SIZE](#process_max_size)
- [PVO_CACHE_ENABLE](#pvo_cache_enable)
- [PVO_CACHE_SHARD_COUNT](#pvo_cache_shard_count)
- [PVO_CACHE_MAX_MEMORY_SIZE](#pvo_cache_max_memory_size)
- [PVO_CACHE_MAX_PLANS_PER_SQL](#pvo_cache_max_plans_per_sql)
- [PVO_CACHE_MAX_SQL_ENTRIES](#pvo_cache_max_sql_entries)
- [QUERY_PARALLEL_FACTOR](#query_parallel_factor)
- [ROLLUP_FETCH_COUNT_LIMIT](#rollup_fetch_count_limit)
- [RS_CACHE_APPROXIMATE_RESULT_ENABLE](#rs_cache_approximate_result_enable)
- [RS_CACHE_ENABLE](#rs_cache_enable)
- [RS_CACHE_MAX_MEMORY_PER_QUERY](#rs_cache_max_memory_per_query)
- [RS_CACHE_MAX_MEMORY_SIZE](#rs_cache_max_memory_size)
- [RS_CACHE_MAX_RECORD_PER_QUERY](#rs_cache_max_record_per_query)
- [RS_CACHE_TIME_BOUND_MSEC](#rs_cache_time_bound_msec)
- [SHOW_HIDDEN_COLS](#show_hidden_cols)
- [TABLE_SCAN_DIRECTION](#table_scan_direction)
- [TAG_CACHE_ENABLE](#tag_cache_enable)
- [TAG_CACHE_MAX_MEMORY_SIZE](#tag_cache_max_memory_size)
- [TAG_CACHE_POOL_COUNT](#tag_cache_pool_count)
- [TAG_MEMORY_INDEX_TYPE](#tag_memory_index_type)
- [TAG_MEMORY_INDEX_PANOUT](#tag_memory_index_panout)
- [TAGDATA_AUTO_META_INSERT](#tagdata_auto_meta_insert)
- [TAG_TABLE_META_MAX_SIZE](#tag_table_meta_max_size)
- [TAG_PARTITION_COUNT](#tag_partition_count)
- [TAG_DATA_PART_SIZE](#tag_data_part_size)
- [TRACE_LOGFILE_COUNT](#trace_logfile_count)
- [TRACE_LOGFILE_PATH](#trace_logfile_path)
- [TRACE_LOGFILE_SIZE](#trace_logfile_size)
- [TRACE_LOG_LEVEL](#trace_log_level)
- [UNIX_PATH](#unix_path)
- [VOLATILE_TABLESPACE_MEMORY_MAX_SIZE](#volatile_tablespace_memory_max_size)

## CPU_AFFINITY_BEGIN_ID

The starting number of the CPUs used by the Machbase server. It is used to control the CPU usage of the Machbase server.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|0|

## CPU_AFFINITY_COUNT

The number of CPUs that the Machbase server uses. If set to 0, the Machbase server uses all CPUs.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|0|

## CPU_COUNT

Specifies the number of CPUs set in the system. Machbase determines the number of threads based on this value. If set to 0, all CPUs in the system are used.

||Value|
|---|---|
|Minimum|0 (auto-detects the number of CPUs physically installed in the system)|
|Maximum|2^32 - 1|
|Default|1|

## CPU_PARALLEL

Specifies the number of threads to create per CPU. If this value is 2 and the number of CPUs is 2, two parallel threads are created per CPU, so the number of parallel processing threads is four. If this value is too large, memory can be consumed quickly.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|1|

## DBS_PATH

Specifies the path where the basic data of the Machbase server is stored. The default is `?/dbs`, which means `$MACHBASE_HOME/dbs`.

||Value|
|---|---|
|Default|?/dbs|

## DEFAULT_LSM_MAX_LEVEL

Sets the default level of the LSM index. If you do not specify a `MAX_LEVEL` value when creating an index, this value applies.

||Value|
|---|---|
|Minimum|0|
|Maximum|3|
|Default|2|

## DISK_BUFFER_COUNT

Specifies the number of buffers for disk I/O.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|16|

## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

Sets the checkpoint interval for indexes. If set too long, errors may occur during index builds.

||Value|
|---|---|
|Minimum|1 (sec)|
|Maximum|2^32 - 1 (sec)|
|Default|120 (sec)|

## DISK_COLUMNAR_INDEX_FDCACHE_COUNT

Specifies the number of open index partition file descriptors.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|0|

## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH

Sets whether to write all index information to disk when the Machbase server shuts down. If set to 1, the server writes all index information to disk before it shuts down, so shutdown can take longer.

||Value|
|---|---|
|Minimum|0 (False)|
|Maximum|1 (True)|
|Default|0 (False)|

## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE

Sets the maximum size of the page cache.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|32 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

Sets the checkpoint interval for table data. If this value is too large, recovery at restart takes much longer. If it is too small, I/O occurs frequently and overall performance may degrade.

||Value|
|---|---|
|Minimum|1 (sec)|
|Maximum|2^32 - 1 (sec)|
|Default|120 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT

Specifies the maximum number of open file descriptors for column data in tables.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|0|

## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE

Sets the size of the default MINMAX cache set on the `_ARRIVAL_TIME` column.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|100 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

Sets whether column partitions are flushed only when they are full.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

Sets the interval at which partition files are written to disk. When more data is input than the configured number of partitions, it is written to disk regardless of this interval.

||Value|
|---|---|
|Minimum|0 (sec)|
|Maximum|2^32 - 1 (sec)|
|Default|3 (sec)|

## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE

If set to 1, input is allowed even if the value of the `_ARRIVAL_TIME` column decreases. If set to 0, a value smaller than the maximum value of the `_ARRIVAL_TIME` column is treated as an error.

||Value|
|---|---|
|Minimum|0 (False)|
|Maximum|1 (True)|
|Default|1 (True)|

## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE

Specifies how much the double write file used for recovery at startup grows at a time.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^32 - 1|
|Default|1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE

Specifies the amount of space the double write file reserves when it is created.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^32 - 1|
|Default|2 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE

Specifies the block size of the memory reserved for column partitions.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^64 - 1|
|Default|2 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

Specifies the maximum amount of memory allocated by log tables. If the server allocates more memory than this value, memory allocation waits until memory usage drops below this value, so performance degrades. It is recommended to set this value to 50~80% of physical memory.

||Value|
|---|---|
|Minimum|256 * 1024 * 1024|
|Maximum|2^64 - 1|
|Default|8 * 1024 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

When the Machbase server starts, it pre-allocates this amount of memory to prevent performance degradation caused by memory allocation. Since this memory is used only as a data input buffer, it is recommended to use it only when memory is sufficient.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^64 - 1|
|Default|100 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT

When data is input to log tables, input performance is throttled if the memory usage for column data files exceeds the limit calculated with this value as follows.

```c
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE * (DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT / 100)
```

||Value|
|---|---|
|Minimum|0|
|Maximum|100|
|Default|80|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC

Sets the wait time applied to each record input when the memory usage for column data files exceeds the limit.

||Value|
|---|---|
|Minimum|0 (msec)|
|Maximum|2^32 - 1 (msec)|
|Default|1 (msec)|

## DISK_IO_THREAD_COUNT

Sets the number of I/O threads that write data to disk.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|3|

## DISK_TABLESPACE_DIRECT_IO_FSYNC

When Direct I/O is used, fsync is unnecessary for data files. Disabling fsync while using Direct I/O (set to 0) improves data I/O performance.
Without fsync, no data is lost in normal situations, but you must enable fsync if failures such as a power outage can occur.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## DISK_TABLESPACE_DIRECT_IO_READ

Sets whether to use Direct I/O for data read operations.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## DISK_TABLESPACE_DIRECT_IO_WRITE

Sets whether to use Direct I/O for data write operations. If the file system does not support Direct I/O (for example, ZFS), it must be set to 0.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|1|

## DISK_TABLESPACE_SYNCHRONOUS

Sets the synchronization policy for disk tablespace files.

|Value|Mode|Description|
|---|---|---|
|0|OFF|No synchronization|
|1|NORMAL|Synchronize on double write file writes and backup|
|2|FULL|Synchronize on disk file close and end-RID adjustment, including NORMAL|
|3|EXTRA|Synchronize on every write, including FULL|

||Value|
|---|---|
|Minimum|0|
|Maximum|3|
|Default|1|

## DUMP_APPEND_ERROR

If this value is set to 1, errors are recorded in the `$MACHBASE_HOME/trc/machbase.trc` file when the Append API fails.
In this case, append performance can drop significantly, so it is recommended to use this only for testing.

To check for errors in a user application, it is helpful to use the `SQLAppendSetErrorCallback` API.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## DUMP_TRACE_INFO

Sets the interval at which the server periodically records DBMS system status information in the `machbase.trc` file.
If set to 0, the information is not recorded.

||Value|
|---|---|
|Minimum|0 (sec)|
|Maximum|2^32 - 1 (sec)|
|Default|300 (sec)|

## DURATION_BEGIN

Sets the start point of the default duration applied to `SELECT` statements that do not specify a `DURATION` clause: how many seconds before the current time the newer end of the search range is placed.
If set to 60, the newer end of the search range is 60 seconds before the current time.

The default is 0. If both `DURATION_BEGIN` and `DURATION_GAP` are 0, no default time range is applied and all data is retrieved.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|0|

## DURATION_GAP

Sets the period of the default duration applied to `SELECT` statements that do not specify a `DURATION` clause: the length, in seconds, of the search range going back from its newer end.

* If `DURATION_BEGIN` is 0 and `DURATION_GAP` is 60, data from 60 seconds ago up to the current time is retrieved.
* If both values are 60, data from 120 seconds ago up to 60 seconds ago is retrieved.

The default is 0. If both values are 0, all data is retrieved. To set a time range, specify a positive `DURATION_GAP`.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^31 - 1|
|Default|0|

## ENABLE_CASE_SENSITIVE_PASSWORD

Determines whether passwords are case-sensitive.

* 0: Case-insensitive. Passwords are converted to uppercase when a user is created or altered and during authentication.
* 1: Case-sensitive.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## FEEDBACK_APPEND_ERROR

Sets whether to send error data to the client when an Append API error occurs. If 0, no error data is sent to the client. If 1, error information is sent to the client.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|1|

## GEN_CALLSTACK_FOR_ABORT_ERROR

Sets whether to record call stacks after an abnormal server shutdown.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## GEN_CORE_FILE

Sets whether to record core files after an abnormal server shutdown.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|1|

## GRANT_REMOTE_ACCESS

Determines whether the database can be accessed remotely. If 0, remote connections are blocked.

||Value|
|---|---|
|Minimum|0 (False)|
|Maximum|1 (True)|
|Default|1 (True)|

## BIND_IP_ADDRESS

Specifies the bind IP address for INET/HTTP listeners. The native INET listener uses this address only when `GRANT_REMOTE_ACCESS=1`; when `GRANT_REMOTE_ACCESS=0`, the native INET listener binds to loopback. The HTTP listener always uses `BIND_IP_ADDRESS`, so set this value to `127.0.0.1` if HTTP must be limited to loopback. `0.0.0.0` means all interfaces.

||Value|
|---|---|
|Default|0.0.0.0|

## HTTP_AUTH

Sets whether Basic Authentication is enabled for the REST API service.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## HTTP_ENABLE

Sets whether the REST API service is enabled.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|1|

## HTTP_MAX_MEM

Sets the maximum memory per web session.

||Value|
|---|---|
|Minimum|1 * 1024 * 1024|
|Maximum|2^64 - 1|
|Default|536870912 (512MB)|

## HTTP_PORT_NO

Sets the REST API port number.

||Value|
|---|---|
|Minimum|1024|
|Maximum|65535|
|Default|5657|

## HTTP_THREAD_COUNT

Sets the number of threads used by the Machbase web server.

||Value|
|---|---|
|Minimum|0|
|Maximum|1024|
|Default|2|

## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD

When the number of records not yet indexed reaches this value, the index build thread starts adding them to the index.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|100000|

## INDEX_BUILD_THREAD_COUNT

Specifies the number of index build threads. If set to 0, no index is built.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|3|

## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX

Specifies the maximum number of flush requests per index.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|3|

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT

Specifies the number of threads that delete index files that are no longer needed when LSM indexes are built.

||Value|
|---|---|
|Minimum|1|
|Maximum|1024|
|Default|1|

## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT

Sets the maximum memory usage for LSM index builds as a percentage. The percentage is relative to the maximum memory usage of Machbase. If memory usage exceeds the limit, LSM partition merges are stopped.

||Value|
|---|---|
|Minimum|0|
|Maximum|100|
|Default|70|

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT

Determines the number of threads that perform merge operations for LSM index builds.

||Value|
|---|---|
|Minimum|1|
|Maximum|1024|
|Default|3|

## LIN_HASH_BIT_SIZE

Controls the initial bucket bit width used by the internal linear hash. The type is `UINT32`. Adjusting this value can change the internal scan order of hash-based operations, so the output order of queries without an explicit `ORDER BY` may differ from previous releases.

||Value|
|---|---|
|Minimum|1|
|Maximum|31|
|Default|7|

### Verification SQL

```sql
SELECT name, value, type, min_value, max_value
  FROM v$property
 WHERE name = 'LIN_HASH_BIT_SIZE';
```

## LOOKUP_APPEND_UPDATE_ON_DUPKEY

Specifies how to handle a duplicate primary key when appending to a lookup table.

* 0: Append fails.
* 1: The row for the corresponding primary key is updated.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## MAX_QPX_MEM

Sets the maximum amount of memory the query processor uses to execute `GROUP BY`, `DISTINCT`, and `ORDER BY` clauses.
If a query uses more memory than this value, the query is canceled. An error message is then sent to the client, and the details are recorded in the `machbase.trc` file.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^64 - 1|
|Default|1024 * 1024 * 1024|

## MAX_SESSION_COUNT

Sets the maximum number of concurrent sessions. When exceeded, new sessions are rejected.

||Value|
|---|---|
|Minimum|64|
|Maximum|2^64 - 1|
|Default|4096|

## MAX_STMT_COUNT_PER_SESSION

Sets the maximum number of statements allowed per session. Statement creation fails when the limit is exceeded.

||Value|
|---|---|
|Minimum|512|
|Maximum|2^32 - 1|
|Default|1024|

## SESSION_IDLE_TIMEOUT_SEC

Sets the maximum idle time for a session in seconds. If the idle time exceeds this value, the connection is closed. 0 disables the idle timeout.

||Value|
|---|---|
|Minimum|0 (sec)|
|Maximum|2^64 - 1 (sec)|
|Default|0 (sec)|

## SESSION_QUERY_TIMEOUT_SEC

Sets the maximum query execution time in seconds. If the query time exceeds this value, the query is canceled. 0 disables the query timeout.

||Value|
|---|---|
|Minimum|0 (sec)|
|Maximum|2^64 - 1 (sec)|
|Default|0 (sec)|

## MEMORY_ROW_TEMP_TABLE_PAGESIZE

Sets the page size of the temporary tablespace for volatile tables and lookup tables. Because records of volatile and lookup tables are stored in these pages, the value must be larger than the maximum record size of volatile tables.
To store N records in one page, set this value to the maximum record size * N.

||Value|
|---|---|
|Minimum|8 * 1024|
|Maximum|2^32 - 1|
|Default|32 * 1024|

## PID_PATH

Specifies the location where the PID file of the Machbase server process is written. The default is `?/conf`, which means `$MACHBASE_HOME/conf`.

||Value|
|---|---|
|Default|?/conf|

|PID_PATH Value|PID File Location Path|
|---|---|
|Not Specified|$MACHBASE_HOME/conf/machbase.pid|
|?/test|$MACHBASE_HOME/test/machbase.pid|
|/tmp|/tmp/machbase.pid|

## PORT_NO

Specifies the TCP/IP port that the Machbase server process uses to communicate with clients. The default is 5656.

||Value|
|---|---|
|Minimum|1024|
|Maximum|65535|
|Default|5656|

## PROCESS_MAX_SIZE

Specifies the maximum memory size used by `machbased`, the Machbase server process. If the server tries to use more memory than this limit, it reduces memory usage as follows.

* Stops data input or treats it as an error.
* Slows down index builds.

In this case, performance degrades greatly, so find and fix the cause of the excessive memory usage.

||Value|
|---|---|
|Minimum|32 * 1024 * 1024|
|Maximum|2^64 - 1|
|Default|8 * 1024 * 1024 * 1024|

## PVO_CACHE_ENABLE

Turns the global PVO statement cache on or off. Available only in the Standard edition.

||Value|
|---|---|
|Minimum|0 (Disabled)|
|Maximum|1 (Enabled)|
|Default|1|

## PVO_CACHE_SHARD_COUNT

Sets the number of shards for the PVO statement cache. It is applied only at initialization, so changing it requires a server restart; it cannot be changed at runtime.

||Value|
|---|---|
|Minimum|1|
|Maximum|256|
|Default|16|

## PVO_CACHE_MAX_MEMORY_SIZE

Sets the total memory budget (bytes) for the PVO statement cache. The value is distributed evenly across shards. It can be changed at runtime.

||Value|
|---|---|
|Minimum|32768|
|Maximum|2^64 - 1|
|Default|268435456|

## PVO_CACHE_MAX_PLANS_PER_SQL

Sets the maximum number of cached plans (handles) per SQL statement. It can be changed at runtime.

||Value|
|---|---|
|Minimum|1|
|Maximum|512|
|Default|512|

## PVO_CACHE_MAX_SQL_ENTRIES

Limits the number of SQL entries stored in the PVO statement cache; 0 means unlimited. The value is distributed across shards, and it can be changed at runtime.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|0|

## QUERY_PARALLEL_FACTOR

Specifies the number of execution threads of the parallel query executor.
The default is 0 for Standard builds and 4 for Cluster builds.

||Value|
|---|---|
|Minimum|0|
|Maximum|100|
|Default|0|

## ROLLUP_FETCH_COUNT_LIMIT

Limits the amount of data the rollup thread fetches at one time.

If set to 0, there is no limit.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|3000000|

## RS_CACHE_APPROXIMATE_RESULT_ENABLE

Determines whether to use the approximate result mode of the result cache. If this value is 1, approximate values are returned when the result cache is used (very fast, but the data may be inaccurate). If it is 0, exact values are returned.

||Value|
|---|---|
|Minimum|0 (False)|
|Maximum|1 (True)|
|Default|0 (False)|

## RS_CACHE_ENABLE

Determines whether to use the result cache.

||Value|
|---|---|
|Minimum|0 (False)|
|Maximum|1 (True)|
|Default|1 (True)|

## RS_CACHE_MAX_MEMORY_PER_QUERY

Sets the amount of result cache memory that the result of a single query can use. If the memory usage of a query result exceeds this value, that result is not stored in the result cache.

||Value|
|---|---|
|Minimum|1024|
|Maximum|2^64 - 1|
|Default|16 * 1024 * 1024|

## RS_CACHE_MAX_MEMORY_SIZE

Specifies the maximum memory usage of the result cache.

||Value|
|---|---|
|Minimum|32 * 1024|
|Maximum|2^64 - 1|
|Default|512 * 1024 * 1024|

## RS_CACHE_MAX_RECORD_PER_QUERY

The maximum number of records stored in the result cache. If a query returns more records than this value, its result is not stored in the cache.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^64 - 1|
|Default|10000|

## RS_CACHE_TIME_BOUND_MSEC

Results of queries that run very quickly are better left out of the result cache, because this reduces memory usage.

This value determines how fast a query must run for its result not to be cached. When set to 0, all query results are stored in the result cache.

||Value|
|---|---|
|Minimum|0 (msec)|
|Maximum|2^64 - 1 (msec)|
|Default|1000 (msec)|

## SHOW_HIDDEN_COLS

With the default value 0, the `_ARRIVAL_TIME` column is not displayed by a `SELECT * FROM` query. If this value is set to 1, the column is displayed.

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|0|

## TABLE_SCAN_DIRECTION

Sets the scan direction of tag tables. The value is one of -1, 0, and 1, and the default is 0.

* -1: Reverse scan
* 0: Tag Table (forward scan), Log Table (reverse scan)
* 1: Forward scan

||Value|
|---|---|
|Minimum|-1|
|Maximum|1|
|Default|0|

## TAG_CACHE_ENABLE

Enables the key-value (TAG) table cache by bitwise OR flags.

* 0: Disable cache
* 1: TAG map cache
* 2: Row data cache
* 4: Data file cache
* 8: External VARCHAR file cache
* 16: Delete vector cache

||Value|
|---|---|
|Minimum|0|
|Maximum|31|
|Default|31|

## TAG_CACHE_MAX_MEMORY_SIZE

Sets the maximum memory size (bytes) per TAG cache pool. The total cache limit is `TAG_CACHE_MAX_MEMORY_SIZE * TAG_CACHE_POOL_COUNT`.

||Value|
|---|---|
|Minimum|32 * 1024|
|Maximum|2^64 - 1|
|Default|512 * 1024 * 1024|

## TAG_CACHE_POOL_COUNT

Sets the number of TAG cache pools.

||Value|
|---|---|
|Minimum|1|
|Maximum|128|
|Default|1|

## TAG_MEMORY_INDEX_TYPE

Selects the memory index type for TAG tables.

* 0: RBTree
* 1: BTree

||Value|
|---|---|
|Minimum|0|
|Maximum|1|
|Default|1|

## TAG_MEMORY_INDEX_PANOUT

Sets the B-Tree order (fanout) for the TAG memory index. Effective when `TAG_MEMORY_INDEX_TYPE=1`.

||Value|
|---|---|
|Minimum|127|
|Maximum|65536|
|Default|255|

## TAGDATA_AUTO_META_INSERT

{{< callout type="info" >}}
In version 5.5, this property was named `TAGDATA_AUTO_NAME_INSERT` and supported only 0 or 1.
In version 5.7 and earlier, the default value was 1.
{{< /callout >}}

Specifies how to handle data input through APPEND/INSERT into the TAGDATA table when there is no matching TAG_NAME.

* 0: Input fails.
* 1: The TAG_NAME value is inserted. If there are additional metadata columns, their values are all entered as NULL.
* 2: The TAG_NAME value is inserted together with the additional metadata column values.
    * This setting is valid only for APPEND. INSERT works like 1 because it cannot enter additional metadata column values.
    * With this setting, APPEND must always use APPEND parameters that include the metadata column values.

||Value|
|---|---|
|Minimum|0|
|Maximum|2|
|Default|2|

## TAG_TABLE_META_MAX_SIZE

Sets the maximum size of memory used to store the metadata area when a TAGDATA table is created.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^32 - 1|
|Default|524288000|

## TAG_PARTITION_COUNT

Specifies the number of key-value tables that make up a tag table.

||Value|
|---|---|
|Minimum|1|
|Maximum|1024|
|Default|4|

## TAG_DATA_PART_SIZE

Determines the partition size of tag data storage.

||Value|
|---|---|
|Minimum|1048576 (1MB)|
|Maximum|1073741824 (1GB)|
|Default|16777216 (16MB)|

## TRACE_LOGFILE_COUNT

Specifies the maximum number of log trace files created in `TRACE_LOGFILE_PATH`. To save disk space, the oldest log file is deleted when more log files than the maximum are created.

When the oldest file is deleted because the maximum number is exceeded, the name of the deleted file is reused for the newest log file.

||Value|
|---|---|
|Minimum|1|
|Maximum|2^32 - 1|
|Default|1000|

## TRACE_LOGFILE_PATH

Sets the path of the log trace files (`machbase.trc`, `machadmin.trc`, `machsql.trc`).
These files continuously record internal information when Machbase starts, stops, and runs. The default `?/trc` means `$MACHBASE_HOME/trc`.

||Value|
|---|---|
|Default|?/trc|

|TRACE_LOGFILE_PATH Value|trc Directory Location|
|---|---|
|Not Specified|$MACHBASE_HOME/trc/|
|?/test|$MACHBASE_HOME/test/|
|/tmp|/tmp/|

## TRACE_LOGFILE_SIZE

Sets the maximum size of a log trace file. If more data than this size needs to be recorded, a new log file is created.

||Value|
|---|---|
|Minimum|1024 * 1024|
|Maximum|2^32 - 1|
|Default|10 * 1024 * 1024|

## TRACE_LOG_LEVEL

Sets the trace log detail level. Higher values write more detailed logs.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^32 - 1|
|Default|277|

## UNIX_PATH

Sets the Unix domain socket name.

||Value|
|---|---|
|Default|machbase-unix|

## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE

Sets the limit on the total memory usage of all volatile and lookup tables in the system.

||Value|
|---|---|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|2 * 1024 * 1024 * 1024|
