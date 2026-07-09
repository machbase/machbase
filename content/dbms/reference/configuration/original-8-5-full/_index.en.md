---
type: docs
title: '17.2.6 Complete Configuration Reference'
weight: 95
tocSort: true
---


## property


The properties are the settings used by the Machbase server and stored as key-value pairs in the $MACHBASE_HOME/conf/machbase.conf file.
These values are set when the Machbase server starts and are used continuously during runtime. To change this value for performance tuning, you must understand the meaning of these values and set them carefully.

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

This is the start number of the CPU used by the Machbase server. It is used to control the CPU usage of the Machbase server.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## CPU_AFFINITY_COUNT

This is the number of CPUs that the Machbase server will use. If set to 0, the Machbase server uses all CPUs.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## CPU_COUNT

Specifies the number of CPUs set in the system. Based on this value, the Machbase Thread determines the number. If set to 0, all CPUs in the system are used.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0(auto detect the physically installed count of CPU on  the system)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

## CPU_PARALLEL

Specifies the number of threads to spawn per CPU. If this value is 2 and the number of CPUs is 2, then two parallel threads are created per CPU, so the number of parallel processing threads is four. If this value is too large, memory can be consumed quickly.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## DBS_PATH

Specifies the path where the basic data of the Machbase server will be stored. The default is "? Dbs",  which means $MACHBASE_HOME/dbs.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Default</td>
      <td>?/dbs</td>
    </tr>
  </tbody>
</table>


## DEFAULT_LSM_MAX_LEVEL

Sets the base level of the LSM index. If you do not enter a MAX_LEVEL value when creating an index, this value applies.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>3</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## DISK_BUFFER_COUNT

Specifies the number of buffers for disk I/O.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

Sets the checkpoint interval for the index. If set too long, errors may occur during index creation.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1 (sec)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 -1 (sec)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>120 (sec)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_INDEX_FDCACHE_COUNT

Specifies the number of opened index partition file descriptors.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH

Sets whether or not to reflect index information on the disk when the Machbase server is shutdown. If this value is set to '1', all index information is reflected on the disk and ends, so waiting times may be long.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0 (False)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE

Sets the maximum size of the page cache.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>32 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

Sets checkpoint period of table data. If this value is too large, the recovery time will be longer at restart. If this value is too small, I/O will frequently occur and the overall performance may be degraded.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1 (sec)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1 (sec)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>120 (sec)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT

Specifies the maximum number of open file descriptors for column data in the table.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE
Sets the size of the default MINMAX cache set in the _ARRIVAL_TIME column.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2 ^ 64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>100 *1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

Sets whether column partitions are flushed only when full.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC
Sets the frequency with which the partition file is reflected on the disk. When more data is input than the number of partitions set, it is reflected on the disk regardless of this period.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (sec)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32-1 (sec)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>3 (sec)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE

If set to 1, the input is allowed even if the value of the _ARRIVAL_TIME column is reduced. If it is 0, a value smaller than the Maximum of the _ARRIVAL_TIME column value is entered as an error.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (False)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1 (True)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE

Specifies the size at which the double write file used for recovery at startup increases at one time.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE
Specifies the amount of space secured by the double write file when the file is created.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>2 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE

Specifies the block size of the memory to reserve for the column partition.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>2 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

Specifies the maximum amount of memory allocated by the log table. If the server allocates more than this amount of memory, the memory allocation will wait until the memory usage drops below this value. It is recommended to set this value to 50 ~ 80% of physical memory.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>256 * 1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>8 * 1024 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

When the Machbase server starts, it pre-allocates memory by this value to prevent performance degradation due to memory allocation. Since this memory is used only as a data input buffer, it is recommended to use it only when memory is sufficient.

Table 24. Range of values


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>100 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT

Limits the performance when the memory usage exceeds the set value when data is input to the log table.

```c
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE * (DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT / 100)
```

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>100</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>80</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC

Sets the next wait time for each record entry if the memory usage for the column data file exceeds the criterion.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (msec)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1 (msec)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1 (msec)</td>
    </tr>
  </tbody>
</table>


## DISK_IO_THREAD_COUNT

Sets the number of I/O threads that write data to disk.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>3</td>
    </tr>
  </tbody>
</table>


## DISK_TABLESPACE_DIRECT_IO_FSYNC

When running Direct I/O, fsync is unnecessary for data files. Disable fsync when using Direct I/O to improve data I/O performance (Set to 0).
Although fsync is unncessary, fsync must be set to perform in case of failure situations such as a power outage because in a normal situation there is no data loss,

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_TABLESPACE_DIRECT_IO_READ

Sets whether to use DIRECT I/O for data read operation.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_TABLESPACE_DIRECT_IO_WRITE

Sets whether to use DIRECT I/O for data write operation. If DIRECT I/O is not supported on the file system (ex: ZFS), it must be set to 0.

||Value|
|-|----|
|Minimum|    0|
|Maximum|    1|
|Default|    1|


## DISK_TABLESPACE_SYNCHRONOUS

Sets the synchronization policy for disk tablespace files.

|Value|Mode|Description|
|--|--|--|
|0|OFF|No synchronization|
|1|NORMAL|Synchronize on double-write file writes and backup|
|2|FULL|Synchronize on disk file close and end-RID adjustment, including NORMAL|
|3|EXTRA|Synchronize on every write, including FULL|

||Value|
|-|----|
|Minimum| 0|
|Maximum| 3|
|Default| 1|


## DUMP_APPEND_ERROR
If this value is set to 1, the $MACHBASE_HOME/trc/machbase.trc file will record the error if the Append API fails.
In this situation, the append performance is very low, so it is recommended to use for testing purposes only.

If you want to check for errors in the user application,  it is helpful to use the SQLAppendSetErrorCallback API.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DUMP_TRACE_INFO

The server periodically records the DBMS system status information in the machbase.trc file at regular intervals, and sets this period.
If it is set to 0, it is not recorded.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (sec)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1 (sec)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>300 (sec)</td>
    </tr>
  </tbody>
</table>


## DURATION_BEGIN

Sets the start time of the duration value that sets the default for the SELECT statements that do not specify the DURATION clause.
If set to 60, data will be retrieved 60 seconds before the current time.

The default is 0 to retrieve all data.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DURATION_GAP
Sets the start time of the duration value that sets the default for the SELECT statements that do not specify the DURATION clause.

* If set to 60, data will be retrieved for 60 seconds from the current time.
* If the DURATION_BEGIN value is 60, the data is retrieved from 60 seconds before to 60 seconds from the current time.

The default is 0 to retrieve all data.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^31 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## ENABLE_CASE_SENSITIVE_PASSWORD

Determines whether passwords are case-sensitive.

* 0: Case-insensitive. Passwords are converted to uppercase on create/alter/auth.
* 1: Case-sensitive.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## FEEDBACK_APPEND_ERROR

Sets whether to send error data to the client when an Append API error occurs. If 0, no error data is sent to the client. If it is 1, error information is sent to the client.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

## GEN_CALLSTACK_FOR_ABORT_ERROR

Sets whether to record call stacks after an abnormal server shutdown.

||Value|
|-|----|
|Minimum| 0|
|Maximum| 1|
|Default| 0|


## GEN_CORE_FILE

Sets whether to record core files after an abnormal server shutdown.

||Value|
|-|----|
|Minimum| 0|
|Maximum| 1|
|Default| 1|


## GRANT_REMOTE_ACCESS

Determines whether the database can be accessed remotely. If 0, the remote connection is blocked.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (False)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1 (True)</td>
    </tr>
  </tbody>
</table>


## BIND_IP_ADDRESS

Specifies the bind IP address for INET/HTTP listeners. The native INET listener uses this address only when `GRANT_REMOTE_ACCESS=1`; when `GRANT_REMOTE_ACCESS=0`, the native INET listener binds to loopback. The HTTP listener always uses `BIND_IP_ADDRESS`, so set this value to `127.0.0.1` if HTTP must be limited to loopback.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Default</td>
      <td>0.0.0.0</td>
    </tr>
  </tbody>
</table>


## HTTP_AUTH

Sets whether Basic Authentication is enabled for the REST API service.

||Value|
|-|----|
|Minimum| 0|
|Maximum| 1|
|Default| 0|


## HTTP_ENABLE

Sets whether the REST API service is enabled.

||Value|
|-|----|
|Minimum| 0|
|Maximum| 1|
|Default| 1|


## HTTP_MAX_MEM

Sets the maximum memory per web session.

||Value|
|-|----|
|Minimum| 1 * 1024 * 1024|
|Maximum| 2^64 - 1|
|Default| 536870912 (512MB)|


## HTTP_PORT_NO

Sets the REST API port number.

||Value|
|-|----|
|Minimum| 1024|
|Maximum| 65535|
|Default| 5657|


## HTTP_THREAD_COUNT

Set the number of threads to be used by the Machbase web server.

||Value|
|-|----|
|Minimum| 0|
|Maximum| 1024|
|Default| 2|


## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD
If the number of records not indexed is greater than this value, the index build thread begins to add indexes.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>100000</td>
    </tr>
  </tbody>
</table>


## INDEX_BUILD_THREAD_COUNT
Specifies the number of index creation threads. If set to 0, no index is created.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>3</td>
    </tr>
  </tbody>
</table>


## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX
Specifies the maximum number of flush requests per index.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT
Specifies the number of threads to delete index files that are not needed when creating LSM indexes.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT
Sets the maximum memory usage for LSM index creation as a percent. This percent is set based on the maximum memory usage used by Machbase. If the memory usage exceeds the limit, the LSM partition merge is stopped.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>100</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>70</td>
    </tr>
  </tbody>
</table>

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT
Determines the number of threads performing the merge operation for the creation of the LSM index.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

## LIN_HASH_BIT_SIZE
Controls the initial bucket bit width used by the internal linear hash. Type: UINT32. Adjusting this value can change the internal scan order of hash-based operations, so the output order of queries without an explicit `ORDER BY` may differ from previous releases.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>31</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>7</td>
    </tr>
  </tbody>
</table>

```sql
SELECT name, value, type, min_value, max_value
  FROM v$property
 WHERE name = 'LIN_HASH_BIT_SIZE';
```


## LOOKUP_APPEND_UPDATE_ON_DUPKEY
When appending to the lookup table, it specifies how to handle duplicate primary keys.

* 0 : Append fail
* 1 : Update Row for the corresponding Primary Key.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## MAX_QPX_MEM

Sets the maximum amount of memory used by the query processor to perform the GROUP BY, DISTINCT, and ORDER BY clauses.
If one query uses memory with a larger value, the query is canceled. At this time, an error message is sent to the client, and the relevant content is recorded in the machbase.trc file.

||Value|
|--|----|
|Minimum|    1024 * 1024|
|Maximum|    2^64 - 1|
|Default|    1024 * 1024 * 1024|


## MAX_SESSION_COUNT

Sets the maximum number of concurrent sessions. When exceeded, new sessions are rejected.

||Value|
|--|----|
|Minimum|    64|
|Maximum|    2^64 - 1|
|Default|    4096|


## MAX_STMT_COUNT_PER_SESSION

Sets the maximum number of statements allowed per session. Statement creation fails when the limit is exceeded.

||Value|
|--|----|
|Minimum|    512|
|Maximum|    2^32 - 1|
|Default|    1024|


## SESSION_IDLE_TIMEOUT_SEC

Sets the maximum idle time for a session in seconds. If the idle time exceeds this value, the connection is closed. 0 disables the idle timeout.

||Value|
|--|----|
|Minimum|    0 (sec)|
|Maximum|    2^64 - 1 (sec)|
|Default|    0 (sec)|


## SESSION_QUERY_TIMEOUT_SEC

Sets the maximum query execution time in seconds. If the query time exceeds this value, the query is canceled. 0 disables the query timeout.

||Value|
|--|----|
|Minimum|    0 (sec)|
|Maximum|    2^64 - 1 (sec)|
|Default|    0 (sec)|


## MEMORY_ROW_TEMP_TABLE_PAGESIZE
Sets the page size of the temporary tablespace for volatile tables and lookup tables. Because this page stores volatile tables and lookup table records, it should be larger than the maximum record size for volatile tables.
If you want to enter N records into the page, you should set this value to the maximum record size * N.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>8 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>32 * 1024</td>
    </tr>
  </tbody>
</table>


## PID_PATH
Specifies the location where the PID file of the Machbase server process is to be written. The default is "?/Conf", which means $MACHBASE_HOME/conf.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Default</td>
      <td>?/conf</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <th>PID_PATH Value</th>
    <th>PID File Location Path</th>
  </thead>
  <tbody>
    <tr>
      <td>Not Specified</td>
      <td>$MACHBASE_HOME/conf/machbase.pid</td>
    </tr>
    <tr>
      <td>?/test</td>
      <td>$MACHBASE_HOME/test/machbase.pid</td>
    </tr>
    <tr>
      <td>/tmp</td>
      <td>/tmp/machbase.pid</td>
    </tr>
  </tbody>
</table>


## PORT_NO
Specifies the TCP/IP port for the Machbase server process to communicate with the client. The Default is 5656.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>65535</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>5656</td>
    </tr>
  </tbody>
</table>


## PROCESS_MAX_SIZE
Specifies the maximum memory size used by machbased programs that are Machbase server processes. If you try to use more memory than the set limit, the server operates as follows to reduce the memory usage.

* Stops data insert or treats it as an error
* Decreased index creation speed

In this case, the performance is greatly degraded, so the cause of overuse of the memory must be found and solved.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>32 * 1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>8 * 1024 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_ENABLE
Turns the global PVO statement cache on or off. Available only in the Standard edition.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (Disabled)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (Enabled)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_SHARD_COUNT
Sets the number of shards for the PVO statement cache. Applied only at initialization; changing it requires a server restart (runtime change is not supported).

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>256</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>16</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_MAX_MEMORY_SIZE
Sets the total memory budget (bytes) for the PVO statement cache. The value is distributed across shards. Runtime change is allowed.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>32768</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>268435456</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_MAX_PLANS_PER_SQL
Sets the maximum number of cached plans (handles) per SQL statement. Runtime change is allowed.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>512</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>512</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_MAX_SQL_ENTRIES
Limits the number of SQL entries stored in the PVO statement cache; 0 means unlimited. The budget is distributed across shards. Runtime change is allowed.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## QUERY_PARALLEL_FACTOR
Specifies the number of execution threads of the parallel query executor.
The standard build default is 0. The cluster build default is 4.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>100</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## ROLLUP_FETCH_COUNT_LIMIT
Limits the amount of data the rollup thread can fetch at one time.

If set to 0, there is no limit.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>3000000</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_APPROXIMATE_RESULT_ENABLE
Determines whether to use the approximate result mode of the result cache. If this value is 1, the speculative value is obtained (very fast but the data may be inaccurate) when using the result cache, and if it is 0, the correct value is obtained.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0 (False)</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_ENABLE
Determines whether to use the result cache.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1 (True)</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_MAX_MEMORY_PER_QUERY
Sets the amount of memory the result cache will use. If the memory usage of a particular query result exceeds this value, the result of the query is not stored in the result cache.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>16 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_MAX_MEMORY_SIZE
Specifies the maximum memory usage of the result cache.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>32 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>512 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_MAX_RECORD_PER_QUERY
The maximum number of records to be stored in the result cache. If the number of records resulting from the query is greater than this value, the query result is not stored in the cache.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_TIME_BOUND_MSEC
If a particular query is executed very quickly, it is better not to store it in the result cache because it can reduce memory usage.
This value determines how fast the query executed should not be stored in the cache. When set to 0, all query results are stored in the result cache.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (msec)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1 (msec)</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>1000 (msec)</td>
    </tr>
  </tbody>
</table>


## SHOW_HIDDEN_COLS
If set to the Default of 0, the _ARRIVAL_TIME column is not displayed by the SELECT * FROM query. If this value is set to 1, the corresponding column is displayed.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## TABLE_SCAN_DIRECTION
You can set the scan direction of the tag table. The property value is one of -1, 0, and 1, and the default value is 0.

* -1 : Reverse scan
* 0  : Tag Table(Forward scan), Log Table(Reverse scan)
* 1  : Forward scan

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>-1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## TAG_CACHE_ENABLE

Enables the key-value (TAG) cache by bitwise OR flags.

* 0: Disable cache
* 1: TAG map cache
* 2: Row data cache
* 4: Data file cache
* 8: External VARCHAR file cache
* 16: Delete vector cache

||Value|
|--|----|
|Minimum|    0|
|Maximum|    31|
|Default|    31|


## TAG_CACHE_MAX_MEMORY_SIZE

Sets the maximum memory size (bytes) per TAG cache pool. The total reserved cache memory is `TAG_CACHE_MAX_MEMORY_SIZE * TAG_CACHE_POOL_COUNT`.

||Value|
|--|----|
|Minimum|    32 * 1024|
|Maximum|    2^64 - 1|
|Default|    512 * 1024 * 1024|


## TAG_CACHE_POOL_COUNT

Sets the number of TAG cache pools.

||Value|
|--|----|
|Minimum|    1|
|Maximum|    128|
|Default|    1|


## TAG_MEMORY_INDEX_TYPE

Selects the memory index type for TAG tables.

* 0: RBTree
* 1: BTree

||Value|
|--|----|
|Minimum|    0|
|Maximum|    1|
|Default|    1|


## TAG_MEMORY_INDEX_PANOUT

Sets the B-Tree order (fanout) for the TAG memory index. Effective when `TAG_MEMORY_INDEX_TYPE=1`.

||Value|
|--|----|
|Minimum|    127|
|Maximum|    65536|
|Default|    255|


## TAGDATA_AUTO_META_INSERT
{{<callout type="info">}}
In version 5.5, this property name was TAGDATA_AUTO_NAME_INSERT and supported
only 0 or 1. In versions earlier than 5.7, the default value was 1.
{{</callout>}}

When entering data through APPEND / INSERT into the TAGDATA table, specify how to handle it if there is no matching TAG_NAME.

* 0: Input fails.
* 1: Input TAG_NAME value to input. If there are additional metadata columns, the values of all columns are entered as NULL.
* 2: Enter the additional metadata column value along with the TAG_NAME value you want to enter.
    * This setting is valid only in APPEND. INSERT works like 1 because you cannot enter additional metadata column values.
    * After this setting, the APPEND parameter must include the metadata column value in APPEND.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## TAG_TABLE_META_MAX_SIZE

When creating the TAGDATA table, set the maximum size of memory to store the metadata area.

||Value|
|-|----|
|Minimum|    1024*1024|
|Maximum|    2^32-1|
|Default|    524288000|


## TAG_PARTITION_COUNT

Specify the number of Key Value tables that consist the tag table.

||Value|
|--|--|
|Minimum| 1|
|Maximum| 1024|
|Default| 4 |

## TAG_DATA_PART_SIZE

Determines the partition size in tag data storage.

||Value|
|--|--|
|Minimum| 1048576 (1MB)|
|Maximum| 1073741824 (1GB)|
|Default| 16777216 (16MB) |

## TRACE_LOGFILE_COUNT

Specifies the maximum number of log trace files generated in TRACE_LOGFILE_PATH. To save disk space, delete the oldest log file if more than the maximum number of log files are created.

If more than the maximum number of log trace files is created and the oldest file is deleted, the name of the deleted file is saved as the newest log file.

||Value|
|-|----|
|Minimum|    1|
|Maximum|    2^32 - 1|
|Default|    1000|


## TRACE_LOGFILE_PATH
Set the path of the log trace files (machbase.trc, machadmin.trc, machsql.trc).
These files continuously record internal information at the start, end, and run of Machbase. The default ?/trc  means $MACHBASE_HOME/trc.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Default</td>
      <td>?/trc</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <th>TRACE_LOGFILE_PATH </th>
    <th>trc direction location</th>
  </thead>
  <tbody>
    <tr>
      <td>Not Specified</td>
      <td>$MACHBASE_HOME/trc/</td>
    </tr>
    <tr>
      <td>?/test</td>
      <td>$MACHBASE_HOME/test/</td>
    </tr>
    <tr>
      <td>/tmp</td>
      <td>/tmp/</td>
    </tr>
  </tbody>
</table>


## TRACE_LOGFILE_SIZE
Sets the maximum size of the log trace file. If it is necessary to record more data than the size, a new log file is created.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32-1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>10 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## TRACE_LOG_LEVEL

Sets the trace log detail level. Higher values write more detailed logs.

||Value|
|-|----|
|Minimum| 0|
|Maximum| 2^32 - 1|
|Default| 277|


## UNIX_PATH
Sets the Unix domain socket name.

<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Default</td>
      <td>machbase-unix</td>
    </tr>
  </tbody>
</table>


## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE
Sets the total amount of memory usage for all volatile and lookup tables in the system.


<table>
  <thead>
    <th> </th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td>Default</td>
      <td>2 * 1024 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>

## property-cl



Separate from [Property](../property), Property (Cluster) organizes the Property only available in Cluster Edition.

# Index

- [Index](#index)
  - [CLUSTER_LINK_ACCEPT_TIMEOUT](#cluster_link_accept_timeout)
  - [CLUSTER_LINK_BUFFER_SIZE](#cluster_link_buffer_size)
  - [CLUSTER_LINK_CHECK_INTERVAL](#cluster_link_check_interval)
  - [CLUSTER_LINK_CONNECT_RETRY_TIMEOUT](#cluster_link_connect_retry_timeout)
  - [CLUSTER_LINK_CONNECT_TIMEOUT](#cluster_link_connect_timeout)
  - [CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST](#cluster_link_error_add_origin_host)
  - [CLUSTER_LINK_HANDSHAKE_TIMEOUT](#cluster_link_handshake_timeout)
  - [CLUSTER_LINK_SEND_RETRY_COUNT](#cluster_link_send_retry_count)
  - [CLUSTER_LINK_HOST](#cluster_link_host)
  - [CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL](#cluster_link_long_term_callback_interval)
  - [CLUSTER_LINK_LONG_WAIT_INTERVAL](#cluster_link_long_wait_interval)
  - [CLUSTER_LINK_MAX_LISTEN](#cluster_link_max_listen)
  - [CLUSTER_LINK_MAX_POLL](#cluster_link_max_poll)
  - [CLUSTER_LINK_PORT_NO](#cluster_link_port_no)
  - [CLUSTER_LINK_RECEIVE_TIMEOUT](#cluster_link_receive_timeout)
  - [CLUSTER_LINK_REQUEST_TIMEOUT](#cluster_link_request_timeout)
  - [CLUSTER_LINK_SEND_TIMEOUT](#cluster_link_send_timeout)
  - [CLUSTER_LINK_SESSION_TIMEOUT](#cluster_link_session_timeout)
  - [CLUSTER_LINK_THREAD_COUNT](#cluster_link_thread_count)
  - [CLUSTER_QUERY_STAT_LOG_ENABLE](#cluster_query_stat_log_enable)
  - [CLUSTER_REPLICATION_BLOCK_SIZE](#cluster_replication_block_size)
  - [CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE](#cluster_warehouse_direct_dml_enable)
  - [COORDINATOR_DBS_PATH](#coordinator_dbs_path)
  - [COORDINATOR_DDL_REQUEST_TIMEOUT](#coordinator_ddl_request_timeout)
  - [COORDINATOR_DDL_TIMEOUT](#coordinator_ddl_timeout)
  - [COORDINATOR_DECISION_DELAY](#coordinator_decision_delay)
  - [COORDINATOR_DECISION_INTERVAL](#coordinator_decision_interval)
  - [COORDINATOR_HOST_RESOURCE_ENABLE](#coordinator_host_resource_enable)
  - [COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL](#coordinator_host_resource_collect_interval)
  - [COORDINATOR_HOST_RESOURCE_INTERVAL](#coordinator_host_resource_interval)
  - [COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT](#coordinator_host_resource_request_timeout)
  - [COORDINATOR_NODE_REQUEST_TIMEOUT](#coordinator_node_request_timeout)
  - [COORDINATOR_NODE_TIMEOUT](#coordinator_node_timeout)
  - [COORDINATOR_STARTUP_DELAY](#coordinator_startup_delay)
  - [COORDINATOR_STATUS_NODE_INTERVAL](#coordinator_status_node_interval)
  - [COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT](#coordinator_status_node_request_timeout)
  - [COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO](#coordinator_disk_full_upper_bound_ratio)
  - [COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO](#coordinator_disk_full_lower_bound_ratio)
  - [DEPLOYER_DBS_PATH](#deployer_dbs_path)
  - [EXECUTION_STAGE_MEMORY_MAX](#execution_stage_memory_max)
  - [HTTP_ADMIN_PORT](#http_admin_port)
  - [HTTP_CONNECT_TIMEOUT](#http_connect_timeout)
  - [HTTP_RECEIVE_TIMEOUT](#http_receive_timeout)
  - [HTTP_SEND_TIMEOUT](#http_send_timeout)
  - [INSERT_BULK_DATA_MAX_SIZE](#insert_bulk_data_max_size)
  - [INSERT_RECORD_COUNT_PER_NODE](#insert_record_count_per_node)
  - [LOOKUPNODE_COMMAND_RETRY_MAX_COUNT](#lookupnode_command_retry_max_count)
  - [STAGE_RESULT_BLOCK_SIZE](#stage_result_block_size)



## CLUSTER_LINK_ACCEPT_TIMEOUT
Timeout until receiving Handshake message after Accept when connecting to a specific Node.

Failure to receive within the timeout will cause the connection to fail.

The default value is 5 seconds.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>5000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_BUFFER_SIZE

The size of the request/receive buffer.

If this size is insufficient, it will try again until the buffer is empty during transmission.

|(byte)|    Value|
|------|---------|
|Minimum|    1024768|
|Maximum|    2^32 - 1|
|Default|    33554432 (32M)|


## CLUSTER_LINK_CHECK_INTERVAL
Check interval of the Timeout Thread that checks the Sockets connected to a specific Node.

There is a Timeout Thread that checks RECEIVE_TIMEOUT and SESSION_TIMEOUT.

The shorter the cycle is, the more frequently it is checked but the Timeout determination is made according to the following values.

The default value is 1 second.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT
Timeout to repeat reconnect attempt after connection failure with a specific Node.

If it is not connected within the timeout, it is determined to be completely disconnected.

The default value is 1 minute.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>60000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_CONNECT_TIMEOUT
Time to wait when trying to connect to a specific Node.

If it does not connect within the Timeout, it will try to reconnect until CLUSTER_LINK_CONNECT_RETRY_TIMEOUT has passed.

The default value is 5 seconds.



<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>5000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST
You can choose whether to add an errored host name to error messages that occur during communication between the Cluster.

If you want to display a detailed error message, set the property to 1.

The default value is 1, which means the host name is displayed.


<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_HANDSHAKE_TIMEOUT
Timeout until receiving a Handshake message while connected to a specific Node and Cluster Socket.

Two Nodes that have just finished connecting exchange small size Handshake messages to check the connection status.

The Accept Node sends the Handshake message first, and the time to wait for the response is set here.

The default value is 5 seconds.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>5000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_SEND_RETRY_COUNT
Number of times to retry sending until the send buffer is empty.

Every retry will take 1ms off. If you retry beyond this number, you will be disconnected.

The default value is 5000 (msec).


<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_HOST

Host name of the current Node to connect to a specific Node and Cluster Socket

|(string)|  Value|
|--|--|
|Default|    localhost|


## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL
If the execution time of Receive Callback to process a message received on Cluster Socket exceeds the set value, it is recognized as Long-Term Callback.

Since the number of receive Threads is limited, Receive Callback should not process messages for a long time.

If Receive Callback processes the message after this time, it recognizes it as Long-Term Callback and records it in Trace Log.

The default value is 1 second.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_LONG_WAIT_INTERVAL
If the time until the arrival of a message received on Cluster Socket exceeds the set value, it is recognized as Long-Wait Message.

If the time from receiving start to receiving end is long, it can be regarded as a problem of the network environment.

If the received message does not arrive after this time, it is recognized as a Long-Wait Message and recorded in the Trace Log.

The default value is 1 second.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_MAX_LISTEN
The maximum number of Socket's Accept Queue when connecting to a specific Node.

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^31-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>512</td>
    </tr>
  </tbody>
</table>



## CLUSTER_LINK_MAX_POLL
The maximum number of Events that can be retrieved at a time by Poll when communicating with a specific node.

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^31-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>4096</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_PORT_NO
The port number of the current Node for connecting the specific Node to the Cluster Socket

<table>
  <thead>
    <th style="background-color: lightyellow;">(port)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>65535</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>3868</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_RECEIVE_TIMEOUT
Timeout until the Timeout Thread determines that the connection has been disconnected since the last reception.

Connections that exist in the 'Linked List' should be continuously receiving because the connection between Cluster Nodes is terminated when the reception is complete.

If the last received time is not updated after the set time has elapsed, the Timeout Thread records its contents in the Trace Log and closes the Socket.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_REQUEST_TIMEOUT
Timeout from when a request message is sent from the Cluster Socket to when a response to the request is received.

For specific messages, specify the time to wait for a response after the request.

If the response message does not arrive at this time, write log to the Trace Log and close the Socket.

The default value is 60 seconds, Timeout is long enough because it is not known what kind of message and receive processing will happen.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>60000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_SEND_TIMEOUT
Timeout to set when sending messages through Cluster Socket.

Set the corresponding timeout when transmitting.

If transmission is not completed until Timeout, it is recorded in the Trace Log.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_SESSION_TIMEOUT
Timeout until the Timeout thread determines that the connection has been disconnected since the last receive in a specific session.

Cluster connection manages the session of all messages internally, which is a necessary property in case the session can suddenly not be fixed.

If the last receive time for the session is not updated after this time, the Timeout Thread writes to the Trace Log and closes the session.

The default value is 1 hour.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>3600000000</td>
    </tr>
  </tbody>
</table>


## CLUSTER_LINK_THREAD_COUNT
The number of Threads to process the received messages when communicating with a specific Node.

If the size of the Cluster grows or the number of operations to be processed increases, you can increase the number of receive threads.

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>4096</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## CLUSTER_QUERY_STAT_LOG_ENABLE
Outputs statistical information about the executed query to the trace log.


<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## CLUSTER_REPLICATION_BLOCK_SIZE
The size of the data to be sent at once when the Replication for adding Node is performed in the Cluster Edition.

The Property must be applied directly to the warehouse (=Transmitting Warehouse) that becomes the Replication Active.

The default value is 640 KB.


<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>64 * 1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>100 * 1024 * 1024</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>640 * 1024 (655360)</td>
    </tr>
  </tbody>
</table>


## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE
It is made possible to connect directly to the Warehouse to perform DML in Cluster Edition.

* 1: Executable
* 0: Not executable. An error is returned.

When directly performing the DML in Warehouse, there are performance advantages over Brokers but there is an issue where the DML is not propagated to the same Group.

Therefore, it is used only for emergency recovery due to data discrepancies, or if the data discrepancies of the Group can be taken into account.

You must apply Properties directly to the specific Warehouse you want.

The default value is 0.

{{<callout type="info">}}
The Coordinator does not check for data discrepancies, even if there is a data difference between the Warehouses in the Group with the corresponding Property turned on.
{{</callout>}}

<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DBS_PATH
Specifies the directory where the Coordinator data file will be created.

The default value is set to ?/dbs, and ? is replaced with the $ MACHBASE_COORDINATOR_HOME environment variable.

This is an environment variable $MACHBASE_COORDINATOR_HOME/dbs directory.

It must be applied to the Coordinator, and it has no effect on other Nodes.


<table>
  <thead>
    <th style="background-color: lightyellow;">(path)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>?/dbs</td>
    </tr>
  </tbody>
</table>

## COORDINATOR_DDL_REQUEST_TIMEOUT
Timeout until the Coordinator waits after requesting the Node to execute DDL.

This value refers to the time the Coordinator waits after requesting each Node to perform DDL.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>300000000</td>
    </tr>
  </tbody>
</table>

## COORDINATOR_DDL_TIMEOUT

Timeout until the broker waits after requesting the coordinator to perform DDL.

This value means the time it takes to wait after the broker requests the coordinator to perform DDL for the entire cluster nodes.

|(usec)|Value|
|--|--|
|Minimum|0|
|Maximum|2^64 - 1|
|Default|300000000|

## COORDINATOR_DECISION_DELAY
Timeout until the Coordinator requests the status change and effectively reflects it.

If the status does not actually change over this time, disable the cluster status.

If the status of the Warehouse Active is not changed but the connected Standby exists, the Fail-Over operation starts.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DECISION_INTERVAL
Time to determine how often the Coordinator changes status.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_ENABLE
Whether the Coordinator collects Host Resources for Cluster Nodes.

<table>
  <thead>
    <th style="background-color: lightyellow;">(boolean)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>1 (true)</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>0 (false)</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL
Interval at which Cluster Nodes collect Host Resources.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_INTERVAL
Interval at which the Coordinator exchanges Host Resources with Nodes.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT
Time that the Coordinator waits after requesting the Host Resource information from the Nodes.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>10000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_NODE_REQUEST_TIMEOUT
Timeout until the Coordinator waits after requesting the Node to execute the command.

Because the Add/Remove-node and Add/Remove-Package includes the Node command execution, if it is caught in a short time, the command processing may not be completed.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>600000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_NODE_TIMEOUT
Time the Coordinator waits before determining that the Node has failed.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>



## COORDINATOR_STARTUP_DELAY
Grace time until activating the Decision Thread immediately after Coordinator startup.

If it takes a long time to run the entire Cluster, you can start the Node control of Coordinator later by setting a larger value.

If the Decision Thread runs before the entire drive, there is a high likelihood that the Coordinator will be misplaced.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>3000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_STATUS_NODE_INTERVAL
Interval in which the Coordinator exchanges status inquiry messages with the Nodes.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT
Time the Coordinator waits after requesting status inquiries from Nodes.

If there is no status inquiry response during that time, the Coordinator proceeds without updating the status of the corresponding Node.

If the network situation is not good and you need to update the state, you could consider increasing the value.

Instead, if there is no status query response, the Coordinator will wait for as much as the value was increased.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>15000000</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO
If the disk usage of some servers configured in the cluster exceeds the property value, the group to which the warehouse belongs will enter the DISKFULL state.

Input is restricted for the group in the DISKFULL state, and only inquiry and deletion are possible.

If the property value is 0, the function is disabled.

<table>
  <thead>
    <th style="background-color: lightyellow;">(percent)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>99</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO
If the disk usage of the server operating in the DISKFULL state falls below the property value, the group state transitions to the normal.

If the property value is 0, the function is disabled.

<table>
  <thead>
    <th style="background-color: lightyellow;">(percent)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>99</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>0</td>
    </tr>
  </tbody>
</table>

## DEPLOYER_DBS_PATH
Specifies the directory where the Deployer's data files will be created.

The default value is set to?/dbs, and ? is replaced with the $ MACHBASE_DEPLOYER_HOME environment variable.

This is an environment variable $MACHBASE_DEPLOYER_HOME /dbs directory.

It must be applied to Deployer, and it has no effect on other Nodes.

<table>
  <thead>
    <th style="background-color: lightyellow;">(path)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>?/dbs</td>
    </tr>
  </tbody>
</table>


## EXECUTION_STAGE_MEMORY_MAX
The maximum amount of Memory used by the Stage Thread performing the SELECT query in Cluster Edition.

Because it is the maximum size of each Stage, the complexity of the SELECT query with an increase in the number of Stages can lead to a larger memory requirement.

If there is a Stage that exceeds the maximum size, the Stage is canceled and the Query is canceled with an error.

You must apply Properties directly to the specific Warehouse you want.

The default value is 1GB.

<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1024 *1024 * 1024</td>
    </tr>
  </tbody>
</table>


## HTTP_ADMIN_PORT
Port number to receive requests from MWA or machcoordinatoradmin.

<table>
  <thead>
    <th style="background-color: lightyellow;">(port)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>65535</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>5779</td>
    </tr>
  </tbody>
</table>


## HTTP_CONNECT_TIMEOUT
Timeout used when connecting to machcoordinatoradmin.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>30000000</td>
    </tr>
  </tbody>
</table>


## HTTP_RECEIVE_TIMEOUT
Timeout used when communicating with machcoordinatoradmin.


<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>3600000000</td>
    </tr>
  </tbody>
</table>


## HTTP_SEND_TIMEOUT
Timeout used when communicating with machcoordinatoradmin.

<table>
  <thead>
    <th style="background-color: lightyellow;">(usec)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>60000000</td>
    </tr>
  </tbody>
</table>



## INSERT_BULK_DATA_MAX_SIZE
Maximum size of input data block when executing Append or INSERT-SELECT.


<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>10 * 1024 * 1024</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1024 * 1024</td>
    </tr>
  </tbody>
</table>


## INSERT_RECORD_COUNT_PER_NODE
Number of data inputs that lead to the warehouse group conversion when performing the input.


<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1000</td>
    </tr>
  </tbody>
</table>


## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT
Number of retry when command and connection to Lookup node fails

<table>
  <thead>
    <th style="background-color: lightyellow;">(count)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>3600</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>30</td>
    </tr>
  </tbody>
</table>


## STAGE_RESULT_BLOCK_SIZE
Maximum block size created in one stage.

<table>
  <thead>
    <th style="background-color: lightyellow;">(size)</th>
    <th>Value</th>
  </thead>
  <tbody>
    <tr>
      <td>Minimum</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>Maximum</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td style="background-color: #F0FFFF;">Default</td>
      <td>1024 * 1024</td>
    </tr>
  </tbody>
</table>

## meta-table


## Index

- [Index](#index)
- [User Objects](#user-objects)
  - [M$SYS\_TABLES](#msys_tables)
  - [M$SYS\_TABLE\_PROPERTY](#msys_table_property)
  - [M$SYS\_COLUMNS](#msys_columns)
  - [M$SYS\_INDEXES](#msys_indexes)
  - [M$SYS\_INDEX\_COLUMNS](#msys_index_columns)
  - [M$SYS\_TABLESPACES](#msys_tablespaces)
  - [M$SYS\_TABLESPACE\_DISKS](#msys_tablespace_disks)
  - [M$SYS\_USERS](#msys_users)
  - [M$SYS\_VIEWS](#msys_views)
  - [M$SYS\_USER\_ACCESS](#msys_user_access)
  - [M$RETENTION](#mretention)
- [Others](#others)
  - [M$TABLES](#mtables)
  - [M$COLUMNS](#mcolumns)


The Meta Tables are tables that present the schema information of Machbase. The table names begin with "M$".

These tables hold the table name, column information,  and index information, and reflect the creation, modification and deletion information resulting from the DDL statement.
The Meta Tables can not be added, deleted, or changed by the user.


## User Objects

### M$SYS_TABLES
---

Displays the table created by the user.

|Column Name|Description|
|--|--|
|NAME|Table name|
|TYPE|Table type<br> - 0: Log<br> - 1: Fixed<br> - 3: Volatile<br> - 4: Lookup<br> - 5: Key Value<br> - 6: Tag|
|DATABASE_ID|Database identifier|
|ID|Table identifier|
|USER_ID|User of created table|
|COLCOUNT|Number of columns|
|FLAG|classification Table Type<br> - 1 : Tag Data Table<br> - 2 : Rollup Table<br> - 4 : Tag Meta Table<br> - 8 : Tag Stat Table|

### M$SYS_TABLE_PROPERTY
---

Displays table property information applied to each table.

|Column Name|Description|
|--|--|
|ID|Table identifier|
|NAME|Property Name|
|VALUE|Property Value|


### M$SYS_COLUMNS
---

Displays the column information of the user table displayed in M$SYS_TABLES.

|Column Name|Description|
|--|--|
|NAME|Column name|
|TYPE|Column type|
|DATABASE_ID|Database identifier|
|ID|Column identifier|
|LENGTH|Column length|
|TABLE_ID|Table identifier of column|
|FLAG|(Information for internal use of the server)|
|PART_PAGE_COUNT|Pages per partition|
|PAGE_VALUE_COUNT|Number of data per page|
|MINMAX_CACHE_SIZE|Size of MIN-MAX cache|
|MAX_CACHE_PART_COUNT|Maximum number of partition caches|
|NEXTVAL|Next sequence value for columns that use sequence metadata|


### M$SYS_INDEXES
---

Displays the index information generated by the user.

|Column Name|Description|
|--|--|
|NAME|Index name|
|TYPE|Index type|
|DATABASE_ID|Database identifier|
|ID|Index identifier|
|TABLE_ID|Table of index identifier|
|COLCOUNT|Number of columns of created index|
|PART_VALUE_COUNT|Number of data per partition of index table|
|KEY_COMPRESS|Compression status of key values|
|MAX_LEVEL|Maximum level of index (LSM only)|
|PAGE_SIZE|Page size|
|MAX_KEYWORD_SIZE|Maximum keyword length (keyword only)|
|BITMAP_ENCODE|Bitmap encoding type (RANGE / EQUAL)|


### M$SYS_INDEX_COLUMNS
---

Displays the column information of the user index shown in M$SYS_INDEXES.

|Column Name|Description|
|--|--|
|INDEX_ID|Index identifier|
|INDEX_TYPE|Index type|
|NAME|Column name|
|COL_ID|Column identifier|
|DATABASE_ID|Database identifier|
|TABLE_ID|Table identifier|
|TYPE|Data type of column|


### M$SYS_TABLESPACES
---

Displays the table space information created by the user.

|Column Name|Description|
|--|--|
|NAME|Tablespace name|
|ID|Tablespace identifier|
|DISK_COUNT|Number of disks in tablespace|


### M$SYS_TABLESPACE_DISKS
---

Maintains the disk information used by the tablespace.

|Column Name|Description|
|--|--|
|NAME|Disk name|
|ID|Disk identifier|
|TABLESPACE_ID|Disk tablespace identifier|
|PATH|Disk path|
|IO_THREAD_COUNT|Number of IO threads allocated to this disk|
|VIRTUAL_DISK_COUNT|Number of Virtual Disk units assigned to this disk|


### M$SYS_USERS
---

Maintain user information registered in Machbase.

|Column Name|Description|
|--|--|
|USER_ID|User identifier|
|NAME|User name|
|PWD_POLICY_LEVEL|Password policy level|
|VALID_BEFORE|Password validity end date|

### M$SYS_VIEWS
---

Displays view definitions.

|Column Name|Description|
|--|--|
|USER_NAME|Owner user name|
|DB_NAME|Database name|
|VIEW_NAME|View name|
|VIEW_SQL|View definition SQL text|

### M$SYS_USER_ACCESS
---

Displays user privileges granted on tables.

|Column Name|Description|
|--|--|
|USER_NAME|User name|
|TABLE_NAME|Table name|
|PRIV|Privilege name|

### M$RETENTION
---

Displays the RETENTION POLICY information.

|Column Name|Description|
|-------------|----------------|
| USER_ID     | User ID      |
| POLICY_NAME | policy name    |
| DURATION    | retention period(sec) |
| INTERVAL    | update cycle(sec) |

## Others

### M$TABLES
---

Display all meta tables beginning with M$.

|Column Name|Description|
|--|--|
|NAME|Meta table name|
|TYPE|Table type|
|DATABASE_ID|Database identifier|
|ID|Meta table identifier|
|USER_ID|Table user (in this case, SYS)|
|COLCOUNT|Number of columns|


### M$COLUMNS
---

Displays the column information of the meta table displayed in M​$TABLES.

|Column Name|Description|
|--|--|
|NAME|Column name|
|TYPE|Column type|
|DATABASE_ID|Database identifier|
|ID|Column identifier|
|LENGTH|Column length|
|TABLE_ID|Column table identifier|
|FLAG|(Information for internal use of the server)|
|PART_PAGE_COUNT|Pages per partition|
|PAGE_VALUE_COUNT|Number of data per page|
|MINMAX_CACHE_SIZE|Size of MIN-MAX cache|
|MAX_CACHE_PART_COUNT|Maximum number of partition caches|

## timezone


## Index

* [Timezone of Machbase](#timezone-of-machbase)
* [Timezone Format in Machbase](#timezone-format-in-machbase)
    * [machsql](#machsql)
    * [machloader](#machloader)
    * [SDK](#sdk)
    * [REST API](#rest-api)

## Timezone of Machbase

Machbase assumes that each client's Timezone is valid only in each session.

In general, a time zone is specified as a string representing a specific time.

```
"YYYY-MM-DD HH24:MI:SS ZZZ(Timezone String)"

Example) 
"12:06:56.568+01:00"  
"2006.07.10 at 15:08:56 -05:00"
"09  AM, GMT+09:00"
```

However, the above method not only has the inconvenience of having to designate a specific time based on the time zone every time, but also has a problem in that the amount of data transmission increases linearly when the time zone value is included for a large amount of data.

Therefore, Machbase supports the method of specifying the time zone property for the session in which the client and server are connected.

The following is a step-by-step explanation of the time zone operation provided by Machbase.

* The server operates based on the default time zone provided by the operating system in which the server is installed.<br>
    In other words, if no setting is made, Machbase reads and uses the time zone in which the OS operates.

* If the client program connects to the server without setting the time zone, the client's time zone is set to the server's time zone.<br>
    That is, if the TIMEZONE set in the server is KST, it means that the client also operates in KST.

* If the time zone is explicitly set in the client program, the corresponding session of the server operates in the time zone designated by the client.<br>
    That is, even if the TIMEZONE set in the server is KST, if the client sets the time zone as EDT when connecting, the session operates as EDT.

## Timezone Format in Machbase

Machbase provides only one format consisting of 5 characters to increase ease of use and remove complexity.

That is, the first character is a + or - sign indicating the sign of time, and the following two characters have a value between 00 and 23. And, it is assumed that the last two characters have a time from 00 to 59.

The following shows the format of TIMEZONE supported by Machbase.

```
ex)
TIMEZONE=+0900
TIMEZONE=-0900
```

### machsql
---

When machsql is started, you can set the time zone to operate through the following options.

```
-z, --timezone=+-HHMM
```

You can check the currently set time zone through the SHOW TIMEZONE command.

```
SHOW TIMEZONE;

Mach> show timezone;
Timezone : +0900
```

### machloader
---

When running machloader, you can set the time zone to operate through the following options.

```
-z, --timezone=+-HHMM
```

It connects to the designated time zone and time calculation operates based on the corresponding time zone.

### SDK
---

TIMEZONE has been added to the connection string, and the time zone for the session can be specified.

If TIMEZONE is not specified in the connection string, it operates based on the time zone of the server.

This is the same for CLI, ODBC, JDBC, and DOTNET.

Connection String Example

```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0300
```

### REST API
---

Rest API operates based on the time zone specified in the HTTP protocol HEADER when requesting an operation.

The header is named The-Timezone-Machbase, and the usage is as follows.

```
Authorization: Basic XXXXXXXXXXXXXXXXXXX
...................
The-Timezone-Machbase: +0900
...............
```

As described above, you can specify the desired Timezone string.

If the Timezone is not specified, it operates as the Timezone of the server.

Request example: set to UTC

```bash
curl -H "The-Timezone-Machbase: +0000" -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode 'q=select sysdate from v$tables limit 1'
```

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {
      "name": "sysdate",
      "type": 6,
      "length": 31
    }
  ],
  "timezone": "+0000",
  "data": [
    {
      "sysdate": "2026-06-13 07:58:30 328:941:439"
    }
  ]
}
```

The time zone value set in the "timezone" item is returned to the resulting JSON.

## virtual-table


The Virtual Tables are virtual tables that represent various operational information of the Machbase server in the form of a table. The names of these tables begin with "V$".

This data is used to know what state the Machbase server is operating in.
In addition, various information can be obtained through JOIN operation with other tables in this virtual table.

Virtual Tables are read-only and can not be added / deleted / updated by the user.


## Index

- [Session/System](#sessionsystem)
  - [V$PROPERTY](#vproperty)
  - [V$SESSION](#vsession)
  - [V$SESMEM](#vsesmem)
  - [V$SESSTAT](#vsesstat)
  - [V$SESTIME](#vsestime)
- [V$SYSMEM](#vsysmem)
  - [V$SYSSTAT](#vsysstat)
  - [V$SYSTIME](#vsystime)
  - [V$STMT](#vstmt)
  - [V$VERSION](#vversion)
  - [V$HTTP\_STATUS](#vhttp_status)
  - [V$NEO\_SESSION](#vneo_session)
  - [V$NEO\_STMT](#vneo_stmt)
- [Result Cache](#result-cache)
  - [V$RS\_CACHE\_LIST](#vrs_cache_list)
  - [V$RS\_CACHE\_STAT](#vrs_cache_stat)
- [PVO Statement Cache](#pvo-statement-cache)
  - [V$PVO\_CACHE\_STAT](#vpvo_cache_stat)
  - [V$PVO\_CACHE\_LIST](#vpvo_cache_list)
- [Storage](#storage)
  - [V$STORAGE](#vstorage)
  - [V$STORAGE\_MOUNT\_DATABASES](#vstorage_mount_databases)
  - [V$CACHE](#vcache)
  - [V$CACHE\_OBJECTS](#vcache_objects)
  - [V$STORAGE\_DC\_TABLESPACES](#vstorage_dc_tablespaces)
  - [V$STORAGE\_DC\_TABLESPACE\_DISKS](#vstorage_dc_tablespace_disks)
  - [V$STORAGE\_DC\_DWFILES](#vstorage_dc_dwfiles)
  - [V$STORAGE\_DC\_PAGECACHE](#vstorage_dc_pagecache)
  - [V$STORAGE\_DC\_PAGECACHE\_LRU\_LST](#vstorage_dc_pagecache_lru_lst)
  - [V$STORAGE\_USAGE](#vstorage_usage)
  - [V$STORAGE\_TABLES](#vstorage_tables)
- [Log Table](#log-table)
  - [V$STORAGE\_DC\_TABLES](#vstorage_dc_tables)
  - [V$STORAGE\_DC\_TABLES\_STAT](#vstorage_dc_tables_stat)
  - [V$STORAGE\_DC\_TABLE\_COLUMNS](#vstorage_dc_table_columns)
  - [V$STORAGE\_DC\_TABLE\_COLUMN\_PARTS](#vstorage_dc_table_column_parts)
  - [V$STORAGE\_DC\_TABLE\_INDEXES](#vstorage_dc_table_indexes)
- [LSM(Log Structured Merge) Index](#lsmlog-structured-merge-index)
  - [V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS](#vstorage_dc_lsmindex_level_parts)
  - [V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS\_CACHE](#vstorage_dc_lsmindex_level_parts_cache)
  - [V$STORAGE\_DC\_LSMINDEX\_LEVELS](#vstorage_dc_lsmindex_levels)
  - [V$STORAGE\_DC\_LSMINDEX\_FILES](#vstorage_dc_lsmindex_files)
  - [V$STORAGE\_DC\_LSMINDEX\_AGER\_JOBS](#vstorage_dc_lsmindex_ager_jobs)
- [Volatile Table](#volatile-table)
  - [V$STORAGE\_DC\_VOLATILE\_TABLE](#vstorage_dc_volatile_table)
- [Tag Table](#tag-table)
  - [V$STORAGE\_TAG\_TABLES](#vstorage_tag_tables)
  - [V$STORAGE\_TAG\_CACHE](#vstorage_tag_cache)
  - [V$STORAGE\_TAG\_CACHE\_BASE](#vstorage_tag_cache_base)
  - [V$STORAGE\_TAG\_CACHE\_OBJECTS](#vstorage_tag_cache_objects)
  - [V$STORAGE\_TAG\_TABLE\_FILES](#vstorage_tag_table_files)
  - [V$STORAGE\_TAG\_INDEX](#vstorage_tag_index)
- [Tag Rollup](#tag-rollup)
  - [V$ROLLUP](#vrollup)
- [Stream](#stream)
  - [V$STREAMS](#vstreams)
- [License](#license)
  - [V$LICENSE\_INFO](#vlicense_info)
- [Mutex](#mutex)
  - [V$MUTEX](#vmutex)
  - [V$MUTEX\_WAIT\_STAT](#vmutex_wait_stat)
- [Cluster](#cluster)
  - [V$NODE\_STATUS](#vnode_status)
  - [V$DDL\_INFO](#vddl_info)
  - [V$REPLICATION](#vreplication)
  - [V$REPL\_SENDER](#vrepl_sender)
  - [V$REPL\_SENDER\_META](#vrepl_sender_meta)
  - [V$REPL\_RECEIVER](#vrepl_receiver)
  - [V$REPL\_RECEIVER\_META](#vrepl_receiver_meta)
  - [V$REPL\_READER](#vrepl_reader)
  - [V$REPL\_READER\_META](#vrepl_reader_meta)
  - [V$REPL\_WRITER](#vrepl_writer)
  - [V$REPL\_WRITER\_META](#vrepl_writer_meta)
- [Others](#others)
  - [V$TABLES](#vtables)
  - [V$COLUMNS](#vcolumns)
  - [V$RETENTION\_JOB](#vretention_job)
  - [V$USER\_AUTH\_KEYS](#vuser_auth_keys)



## Session/System

### V$PROPERTY
---

Displays the property information set in the server.

|Column Name|Description|
|--|--|
|NAME|Property name|
|VALUE|Property value|
|TYPE|Data type|
|DEFLT|Default value|
|MIN|Minimum set value|
|MAX|Maximum set value|

### V$SESSION
---

Displays session information connected to the Machbase server.

|Column Name|Description|
|--|--|
|HOSTNAME (Cluster Only)|Name of the HOST which the session is connected.|
|ID|Session identifier|
|CLOSED|Whether connection is closed|
|USER_ID|User identifier|
|LOGIN_TIME|Connection time|
|CLIENT_TYPE|Connected client type|
|USER_NAME|User name|
|USER_IP|User IP address|
|SQL_LOGGING|Leave message in session trace log status<br><br>1: Leaves errors occurring in the Parsing, Validation, Optimization steps<br>2: Leaves result performance of DDL<br>3: (Leaves both cases above)|
|SHOW_HIDDEN_COLS|Whether hidden columns are shown upon SELECT|
|FEEDBACK_APPEND_ERROR|Whether there is feedback to client on APPEND error|
|DEFAULT_DATE_FORMAT|Default input format upon Datetime input |
|HASH_BUCKET_SIZE|Number of Buckets in Temp Hashtable created when performing query|
|MAX_QPX_MEM|Maximum memory size available when performing query|
|RS_CACHE_ENABLE|Whether Result Cache in in use|
|RS_CACHE_TIME_BOUND_MSEC|Maximum elapsed time to store results when using Result Cache|
|RS_CACHE_MAX_MEMORY_PER_QUERY|Maximum size of memory used per query when using Result Cache|
|RS_CACHE_MAX_RECORD_PER_QUERY|Maximum number of results used per query when using Result Cache|
|RS_CACHE_APPROXIMATE_RESULT_ENABLE|Whether to cache approximate query results when using Result Cache|
|IDLE_TIMEOUT|Terminate the session if the client does nothing for that time after the session connected.|
|QUERY_TIMEOUT|Response waiting time for query execution|


### V$SESMEM
---

Displays session memory information.

|Column Name|Description|
|--|--|
|SID|Session identifier|
|ID|Memory manager identifier|
|USAGE|Usage size|


### V$SESSTAT
---

Displays statistical information of the session.

|Column Name|Description|
|--|--|
|SID|Session identifier|
|ID|Statistical information identifier|
|VALUE|Statistical information value|


### V$SESTIME
---

Displays the time information of the session.

|Column Name|Description|
|--|--|
|SID|Session identifier|
|ID|Performance unit identifier|
|ACCUM_TICK|Cumulative time|
|MAX_TICK|Maximum time (per each performance unit)|


## V$SYSMEM

Displays memory information of the system.

|Column Name|Description|
|--|--|
|ID|Memory manager identifier|
|NAME|Memory manager name|
|USAGE|Current usage|
|MAX_USAGE|(Recorded) Maximum usage|


### V$SYSSTAT
---

Displays statistical information of the system.

|Column Name|Description|
|--|--|
|ID|Statistical information identifier|
|NAME|Statistical information name|
|VALUE|Statistical information value|


### V$SYSTIME
---

Displays the time information of the system.

|Column Name|Description|
|--|--|
|ID|Performance unit identifier|
|NAME|Performance unit name|
|ACCUM_TICK|Cumulative time|
|AVG_TICK|Average time (per each performance unit)|
|MIN_TICK|Minimum Time (per each performance unit)|
|MAX_TICK|Maximum Time (per each performance unit)|
|COUNT|Performance frequency|


### V$STMT
---

Displays information about the query statement that the user is currently executing.

|Column Name|Description|
|--|--|
|ID|Query identifier|
|SESS_ID|Performed query session identifier|
|STATE|Query status|
|RECORD_SIZE|Resulting record size of select statements|
|QUERY|Query statement|


### V$VERSION
---

Displays information about Machbase version.

|Column Name|Description|
|--|--|
|BINARY_DB_MAJOR_VERSION|Database major version|
|BINARY_DB_MINOR_VERSION|Database minor version|
|BINARY_META_MAJOR_VERSION|META major version|
|BINARY_META_MINOR_VERSION|META minor version|
|BINARY_CM_MAJOR_VERSION|Client (Communication Level) major version|
|BINARY_CM_MINOR_VERSION|Client (Communication Level) minor version|
|BINARY_SIGNATURE|Version name of DB data files.|
|FILE_DB_MAJOR_VERSION|File DB major version|
|FILE_DB_MINOR_VERSION|File DB minor version|
|FILE_META_MAJOR_VERSION|File META major version|
|FILE_META_MINOR_VERSION|File META minor version|
|FILE_CM_MAJOR_VERSION|File Client (Communication Level) major version|
|FILE_CM_MINOR_VERSION|File Client (Communication Level) minor version|
|FILE_CREATE_TIME|File creation time|
|EDITION|Machbase type|

### V$HTTP_STATUS
---

Displays HTTP service status for the embedded HTTP endpoint.

|Column Name|Description|
|--|--|
|DOC_ROOT|HTTP document root|
|HTTP_PORT|HTTP service port|
|THREAD_COUNT|HTTP worker thread count|
|CONNECT_COUNT|Accepted connection count|
|SERVICE_SUCCESS_COUNT|Successful service count|
|SERVICE_FAILURE_COUNT|Failed service count|
|TOTAL_SERVICE_COUNT|Total service count|
|CURRENT_SERVICE_COUNT|Current service count|
|MAX_HTTP_MEM|Maximum HTTP memory size|

### V$NEO_SESSION
---

Displays session status for Neo protocol clients.

|Column Name|Description|
|--|--|
|ID|Session identifier|
|USER_ID|User identifier|
|USER_NAME|User name|
|STMT_COUNT|Statement count in the session|
|DISCONN_FLAG|Disconnect flag|

### V$NEO_STMT
---

Displays statement status for Neo protocol clients.

|Column Name|Description|
|--|--|
|ID|Statement identifier|
|SESS_ID|Session identifier|
|STATE|Statement state|
|QUERY|Statement text|
|APPEND_SUCCESS_CNT|Append success count|
|APPEND_FAILURE_CNT|Append failure count|


## Result Cache

### V$RS_CACHE_LIST
---

Display the result cache list.

|Column Name|Description|
|--|--|
|TOUCH_TIME|Time cache was used or created|
|USER_ID|Cache user identifier|
|QUERY|Cache query statement|
|TIME_SPENT|Time spent producing result|
|TABLE_COUNT|Number of tables associated with query statement|
|RECORD_COUNT|Number of result records|
|REFERENCE_COUNT|Number of sessions currently being referenced|
|HIT_COUNT|Cache hit count|
|AGGR_TOUCH_TIME|Time the cache was used or created for aggregate results|
|AGGR_HIT_COUNT|Cache hit count for aggregate results|


### V$RS_CACHE_STAT
---

Display statistical information of result cache in one session.


|Column Name|Description|
|--|--|
|CACHE_COUNT|Number of result caches|
|CACHE_HIT|Total cache hit count|
|AGGR_HIT|Total cache hit count for aggregate results|
|CACHE_REPLACED|Cache replacement count|
|CACHE_MEMORY_USAGE|Size of cache memory used|


## PVO Statement Cache
Shows global PVO statement cache status (Standard edition only).

### V$PVO_CACHE_STAT
---

Displays overall statistics of the PVO statement cache.

|Column Name|Description|
|--|--|
|CACHE_ENTRY_COUNT|Number of SQL entries stored in cache|
|CACHE_HANDLE_COUNT|Total cached plans (handles) across SQLs|
|CACHE_MEMORY_USAGE|Current cache memory usage|
|CACHE_MAX_MEMORY_SIZE|Configured cache memory limit|
|CACHE_MAX_PLANS_PER_SQL|Maximum plans allowed per SQL|
|CACHE_MAX_SQL_ENTRIES|Maximum SQL entries allowed (0 = unlimited)|
|CACHE_SHARD_COUNT|Number of cache shards|
|CACHE_HIT|Cache hit count|
|CACHE_MISS|Cache miss count|
|SINGLEFLIGHT_WAIT|Wait count for concurrent same-SQL build|
|BUILD_COUNT|Plan build attempts|
|BUILD_FAIL|Plan build failures|
|INVALIDATE_COUNT|Invalidated plans|
|EVICT_COUNT|Evictions due to limits|
|FLUSH_COUNT|Explicit or internal flush count|

### V$PVO_CACHE_LIST
---

Displays per-SQL details stored in the PVO statement cache.

|Column Name|Description|
|--|--|
|TOUCH_TIME|Last touch time|
|USER_ID|Owner user identifier|
|QUERY|Original SQL text|
|DEFAULT_DATE_FORMAT|Session date format at build time|
|TIMEZONE_OFFSET|Session timezone offset|
|SHOW_HIDDEN_COLS|Whether hidden columns are shown|
|QUERY_PARALLEL_FACTOR|Parallel execution factor|
|HANDLE_COUNT|Number of cached plans|
|BUSY_COUNT|Number of handles currently in use|
|HIT_COUNT|Cache hit count|
|BUILD_IN_PROGRESS|Whether a build is in progress|

## Storage

### V$STORAGE
---

Displays internal information of the storage system.

|Column Name|Description|
|--|--|
|DC_TABLE_FILE_SIZE|Total capacity of disk column data|
|DC_INDEX_FILE_SIZE|Total capacity of index file data|
|DC_TABLESPACE_DWFILE_SIZE|Total capacity of DWFILE for all column data|
|DC_KV_TABLE_FILE_SIZE|Total number of data files of TAGDATA table partition tables|


### V$STORAGE_MOUNT_DATABASES
---

Displays the information of the mounted backup database using the mount function.

|Column Name|Description|
|--|--|
|NAME|Mounted database name|
|PATH|Backup file location|
|BACKUP_TBSID|Backup database tablespace identifier|
|BACKUP_SCN|Backup database identifier|
|MOUNTDB|Backup time|
|DB_BEGIN_TIME|Backup database first entry time|
|DB_END_TIME|Backup database last entry time|
|BACKUP_BEGIN_TIME|Backup begin time|
|BACKUP_END_TIME|Backup end time|
|FLAG|Property flag|


### V$CACHE
---

Displays the comprehensive information on the cache objects containing the results read from the storage system.

|Column Name|Description|
|--|--|
|OBJ_COUNT|Current number of result set cache objects|

### V$CACHE_OBJECTS
---

Displays information about each cache object that contains the results read from the storage system.

|Column Name|Description|
|--|--|
|OID|Object identifier|
|REF_COUNT|Reference count|
|FLAG|(Internal server use flag)|


### V$STORAGE_DC_TABLESPACES
---

Displays the table space information of the storage system.

|Column Name|Description|
|--|--|
|NAME|Tablespace name|
|ID|Tablespace identifier|
|FLAG|Flag indicating tablespace property|
|REF_COUNT|Tablespace reference count|
|DISK_COUNT|Tablespace disk count|


### V$STORAGE_DC_TABLESPACE_DISKS
---

Displays the table space information of the storage system.

|Column Name|Description|
|--|--|
|NAME|Disk name|
|ID|Disk identifier|
|TABLESPACE_ID|Disk tablespace identifier|
|PATH|Disk path|
|IO_THREAD_COUNT|I/O Thread count|
|IO_JOB_COUNT|I/O Job count|
|VIRTUAL_DISK_COUNT|Virtual disk count|


### V$STORAGE_DC_DWFILES
---

Displays the information of the double-write file (DW File) operated by the storage system.


|Column Name|Description|
|--|--|
|TBS_ID|Tablespace identifier|
|DISK_ID|Disk identifier|
|FILE|File path|
|TABLE_ID|Table identifier|
|COLUMN_ID|Column identifier|
|PARTITION_ID|Partition identifier|
|PAGE_ID|Page identifier|
|DISK_OFFSET|Disk offset|
|DISK_IMAGE_SIZE|Disk image size|
|HEAD_CRC32CODE_IMAGE|Head CRC32 Code Image|
|TAIL_CRC32CODE_IMAGE|Tail CRC32 Code Image|
|CRC32CODE_PAGE|CRC32 Code Page|
|HEAD_TIMESTAMP_PAGE|Head Timestamp Page|
|TAIL_TIMESTAMP_PAGE|Tail Timestamp Page|


### V$STORAGE_DC_PAGECACHE
---

Displays information about the Page Cache operating on the storage system

|Column Name|Description|
|--|--|
|MAX_MEM_SIZE|Maximum memory size of Page Cache|
|CUR_MEM_SIZE|Current memory size of Page Cache|
|PAGE_CNT|Number of cached pages|
|CHECK_TIME|Check time|


### V$STORAGE_DC_PAGECACHE_LRU_LST
---

Displays information about the LRU List of Page Cache operated by the storage system.


|Column Name|Description|
|--|--|
|OBJECT_ID|Object identifier|
|LEVEL|Partition level|
|PARTITION_ID|Partition identifier|
|OFFSET|Page Cache Offset|
|SIZE|Page size|
|REF_CNT|Reference count|

### V$STORAGE_USAGE
---

Displays the amount of storage used by the storage system.

|Column Name|Description|
|--|--|
|TOTAL_SPACE|Total storage capacity where the $MACHBASE_HOME/dbs directory is located|
|USED_SPACE|Total storage usage where the $MACHBASE_HOME/dbs directory is located|
|USED_RATIO|Percentage of usage(%)|
|RATIO_CAP|Storage usage limit. Data input/index construction stops when USED_RATIO reaches this limit.|


### V$STORAGE_TABLES
---

Display table details.

|Column Name|Description|
|--|--|
|ID|Table ID|
|TYPE|Table type<br> - Persistent: LOG / TAG Table<br> - Volatile: Volatile Table - Key-Value: Accompanying table of TAG table|
|STATUS|Current Status<br> - Creating...: Creating table by CREATE TABLE query<br> - Normal: normal<br> - Predrop: DROP TABLE query accepted<br> - Dropping...: DROP TABLE query processing<br> - Dropped: DROP TABLE query completed<br> - Mounted: The backed up database loaded with the MOUNT query|
|STORAGE_USAGE|Capacity occupied by the table in storage|


## Log Table

### V$STORAGE_DC_TABLES
---

Displays internal information about Log Table.

|Column Name|Description|
|--|--|
|ID|Table identifier|
|DATABASE_ID|Database identifier|
|CREATE_SCN|System Change Number at time of creation|
|UPDATE_SCN|System Change Number at time of most recent update|
|DDL_REF_COUNT|Number of sessions referencing table in DDL syntax execution|
|BEGIN_RID|Minimum table RID|
|END_RID|Last row ID of table + 1|
|BEGIN_META_RID|ID at start of recording meta information|
|END_META_RID|ID at end of recording meta information|
|END_SYNC_RID|Last row ID recorded on disk + 1|
|FLAG|Flag indicating table property|
|COLUMN_COUNT|Table column count|
|INDEX_COUNT|Table index count|
|INDEX_MIN_END_RID|Last RID recorded in index + 1|
|LAST_ARRIVAL_TIME|Last recorded _arrival_time value|
|LAST_CHECKPOINT_TIME|Last checkpoint time|
|TYPE|Table type|

### V$STORAGE_DC_TABLES_STAT
---

Displays internal information about Log Table.

|Column Name|Description|
|--|--|
|TABLESPACE_ID|Tablespace identifier|
|TABLE_ID|Table identifier|
|COLUMN_ID|Column identifier|
|COUNT|Record count|

### V$STORAGE_DC_TABLE_COLUMNS
---

Displays information about the columns in the Log Table.

|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|DATABASE_ID|Database identifier|
|ID|Column identifier|
|FLAG|Property flag|
|SIZE|Column data size|
|PARTITION_VALUE_COUNT|Maximum number of data stored in partition|
|PAGE_VALUE_COUNT|Maximum number of data stored in page|
|CACHE_VALUE_COUNT|Maximum number of cache values|
|MINMAX_CACHE_SIZE|Maximum size of MIN / MAX cache for column partitions|
|CUR_APPEND_PARTITION_ID|Current partition in progress of input identifier|
|CUR_CACHE_PARTITION_COUNT|Number of partitions that have read data in current cache|
|CUR_MINMAX_CACHE_SIZE|Current Min / MAX cache size|
|END_RID_FOR_DEFAULT_VALUE|Location value of end rid maintaining default value|
|DISK_FILE_SIZE|Total size of column partition data file for that column|
|MEMORY_TOTAL_SIZE|Memory size used by table|
|MEMORY_ALLOC_SIZE|Memory size allocated by table|


### V$STORAGE_DC_TABLE_COLUMN_PARTS
---

Displays column partition information of log table.

|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|DATABASE_ID|Database identifier|
|COLUMN_ID|Column identifier|
|ID|Partition identifier|
|FLAG|Flag indicating column property|
|BEGIN_RID|First RID stored in partition|
|END_RID|Last RID stored in partition|
|END_SYNC_RID|Last RID SYNC ended.<br><br>Data with a RID greater than the starting RID and less than the last SYNC RID is recorded in the partition file.|
|MIN_TIME|First time data was entered into column partition|
|MAX_TIME|Last time data was entered into column partition|
|MAX_VALUE_COUNT_PER_PARTITION|Maximum partition data count|
|MAX_VALUE_COUNT_PER_PAGE|Maximum page data count|
|MAX_PAGE_COUNT|Maximum partition page count|
|PAGE_SIZE|Page size stored in column partition|
|PAGE_COUNT|Page count created in current column partition|
|COMPRESS_RATIO|Column partition compression ratio. If it is 0, data compression has not been performed yet.|
|DISK_FILENAME|Partition file name|
|EXTERNAL_PART_SIZE|A large amount of data is written to the external partition file, indicating the size of the file|
|MIN_VALUE|Minimum column partition value|
|MAX_VALUE|Maximum column partition value|


### V$STORAGE_DC_TABLE_INDEXES
---

Displays index information generated in Log Table.

|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|DATABASE_ID|Database identifier|
|ID|Index identifier|
|FLAG|Flag indicating index property|
|TABLE_BEGIN_RID|First RID entered into table|
|TABLE_END_RID|Last table RID|
|BEGIN_RID|First index RID|
|END_RID|Last index RID|
|END_SYNC_RID|Last recorded RID in file + 1|
|COLUMN_COUNT|Index column count|
|BEGIN_PART_ID|Index first partition identifier|
|END_PART_ID|Index last partition identifier|
|FLUSH_REQUEST_COUNT|Number of index partitions requested to reflect on disk|
|MAX_KEY_SIZE|Maximum key size|
|INDEX_TYPE|Index type|
|DISK_FILE_SIZE|Total size of index partition file for that index|
|LAST_CHECKPOINT_TIME|Last checkpoint time|



## LSM(Log Structured Merge) Index


### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS
---

Displays information about LSM Index partitions.

|Column Name|Description|
|--|--|
|TABLE ID|Index table identifier|
|TABLESPACE_ID|Tablespace identifier|
|INDEX_ID|Index identifier|
|LEVEL|Index partition LSM level|
|PARTITION_ID|Partition identifier|
|BEGIN_RID|First RID entered into partition|
|END_RID|Last RID entered into partition + 1|
|KEY_VALUE_COUNT|Key value count entered into partition|
|KEY_VALUE_TABLE_SIZE|Size of page storing key value|
|KEY_VALUE_TABLE_PAGE_COUNT|Number of pages storing key value|
|MIN_KEY_VALUE|Minimum key value|
|MAX_KEY_VALUE|Maximum key value|
|BITMAP_TABLE_SIZE|Total size of page storing bitmap value|
|BITMAP_TABLE_PAGE_COUNT|Number of pages storing bitmap value|
|META_SIZE|Total size of page storing meta information|
|META_PAGE_COUNT|Number of pages storing meta information|
|TOTAL_BUILD_MSEC|Total time to complete partition|
|KEYVAL_BUILD_MSEC|Total time to complete partition for KeyValue Mode|
|BITMAP_BUILD_MSEC|Total time to complete partition for Bitmap Mode|


### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS_CACHE
---

Displays information about the LSM Index partition cache.


|Column Name|Description|
|--|--|
|TABLESPACE_ID|Tablespace identifier|
|TABLE_ID|Index Table identifier|
|INDEX_ID|Index identifier|
|LEVEL|Index partition LSM level|
|PARTITION_ID|Partition identifier|
|BEGIN_RID|First RID entered into partition|
|END_RID|Last RID entered into partition + 1|
|KEY_VALUE_COUNT|Number of key values entered into partition|
|KEY_VALUE_TABLE_SIZE|Size of page storing key value|
|KEY_VALUE_TABLE_PAGE_COUNT|Number of pages storing key value|
|BITMAP_TABLE_SIZE|Total size of page storing bitmap value|
|BITMAP_TABLE_PAGE_COUNT|Number of pages storing bitmap value|
|META_SIZE|Total size of page storing meta information|
|META_PAGE_COUNT|Number of pages storing meta information|
|MEMORY_SIZE|Memory usage|
|MEMORY_SIZE_RBTREE|Redblack Tree memory usage|


### V$STORAGE_DC_LSMINDEX_LEVELS
---

Displays information about the level of the LSM index.

|Column Name|Description|
|--|--|
|TABLE ID|Table identifier|
|DATABASE_ID|Database identifier|
|INDEX_ID|Index identifier|
|LEVEL|Level|
|BEGIN_RID|First partition RID|
|END_RID|Last partition RID + 1|
|META_BEGIN_RID|RID at start time of recording meta information|
|META_END_RID|RID at end time of recording meta information|
|DELETE_END_RID|Maximum deleted RID + 1|


### V$STORAGE_DC_LSMINDEX_FILES
---

Displays information about the files that make up the LSM Index.

|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|DATABASE_ID|Database identifier|
|INDEX_ID|Index identifier|
|LEVEL|Index partition LSM level|
|PARTITION_ID|Partition identifier|
|BEGIN_RID|Partition first RID|
|END_RID|Partition last RID + 1|
|PATH|Index file location|


### V$STORAGE_DC_LSMINDEX_AGER_JOBS
---

Displays working status of Ager responsible for LSM Index deletion.

|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|INDEX_ID|Index identifier|
|LEVEL|Index partition LSM level|
|BEGIN_RID|First partition RID|
|END_RID|Last partition RID + 1|
|STATE|Index Ager working status|


## Volatile Table

### V$STORAGE_DC_VOLATILE_TABLE
---

Displays information about Volatile Table.


|Column Name|Description|
|--|--|
|MAX_MEM_SIZE|Maximum Volatile Tablespace size|
|CUR_MEM_SIZE|Current Volatile Tablespace size|


## Tag Table

### V$STORAGE_TAG_TABLES
---

Displays information about the partition table in the Tagdata Table.


|Column Name|Description|
|--|--|
|ID|Table identifier|
|TABLE_BEGIN_RID|Table start RID|
|TABLE_END_RID|Table end RID|
|WRITE_END_RID|Last RID which is written to data file.|
|EXT_ROW_COUNT|Number of entries to external partitions in VARCHAR records|
|EXT_WRITE_COUNT|Number of entries to data files in VARCHAR records|
|DISK_INDEX_END_RID|Index end RID stored in storage|
|MEMORY_INDEX_END_RID|Table end RID in memory index|
|DELETE_MIN_DATE|Minimum time of deleted data by execute  DELETE BETWEEN query|
|DELETE_MAX_DATE|Maximum time of deleted data by execute  DELETE BETWEEN/BEFORE query|
|INDEX_STATE|Current Index Build State<br> - IDLE: Build Complete, waiting<br> - PROGRESS: Build in progress<br> - IOWAIT: Waiting for I/O operation in storage<br> - PENDING: Waiting for table read lock<br> - SHUTDOWN:  Stopped. DELETE operation or DROP operation in progress.<br> - ABNORMAL: Abnormal end|
|DELETE_STATE|Current DELETE operation state.<br>There is no IDLE because it is performed only when a DELETE command is entered.<br> - PROGRESS: Deletion in progress<br> - IOWAIT: Waiting for I/O operation in storage<br> - PENDING: Waiting for table read/write lock<br> - SHUTDOWN: Stopped. DELETE operation or DROP operation in progress.<br> - ABNORMAL: Abnormal end|
|SAVE_STATE|Current Table Save operation state.<br> - IDLE: Save Complete, waiting<br> - PROGRESS: Save in progress<br> - IOWAIT: Waiting for I/O operation in storage<br> - PENDING: Waiting for table read lock<br> - SHUTDOWN: Stopped. DELETE operation or DROP operation in progress.<br> - ABNORMAL: Abnormal end|
|VINDEX_STATE|Current VARCHAR Index Build State<br> - IDLE: Build Complete, waiting<br> - PROGRESS: Build in progress<br> - IOWAIT: Waiting for I/O operation in storage<br> - PENDING: Waiting for table read lock<br> - SHUTDOWN:  Stopped. DELETE operation or DROP operation in progress.<br> - ABNORMAL: Abnormal end|


### V$STORAGE_TAG_CACHE
---

Displays the cache information used in the partition table of the Tagdata Table.


|Column Name|Description|
|--|--|
|CATEGORY|Type of object in cache|
|USED_MEMORY|Size of memory in use|
|BLOCK_COUNT|Data cache count|
|CACHE_HIT|Data cache hit count|
|CACHE_MISS|Data cache miss count|
|FLUSHOUT|Number of page flushouts due to data cache crash|
|COLDREAD|Number of data pages read directly from storage|
|MEMORY_WAIT|Number of times data memory waited for cache crash|
|IO_WAIT|Data read operation wait count|

### V$STORAGE_TAG_CACHE_BASE
---

Displays aggregate tag cache pool information.

|Column Name|Description|
|--|--|
|POOL_ID|Cache pool identifier|
|TOTAL_CACHE_MEMORY|Total cache memory|
|TOTAL_OBJECT_COUNT|Total cached object count|
|TOTAL_LRU_LOOP_COUNT|Total LRU loop count|

### V$STORAGE_TAG_CACHE_OBJECTS
---

Displays detailed information about each cache block used in the partition table of the Tagdata Table.

|Column Name|Description|
|--|--|
|CATEGORY|Object classification being cached|
|LATEST_HIT|Last approach time|
|STATUS|Cache status<br> - None: Memory allocation done<br> - Resides: Already stored in cache<br> - Loading: Loading table data from storage<br> - ERROR!: Error appears while loading data|
|WAIT_COUNT|The number of waiting times because the cache could not be read in the Loading state|
|REF_COUNT|Number of sessions currently referencing the cache block|
|HIT_COUNT|Number of times a cache block was referenced|
|TABLE_ID|Table Identifier|
|FILE_ID|File Identifier|
|PART_ID|Partition identifier inside the datafile|
|SAVE_SCN|SCN of table save|
|VSAVE_SCN|SCN of table save|
|DELETE_SCN|SCN of delete operation|
|OFFSET|Datafile offset|
|DATA_SIZE|Data size before compression, or 0|


### V$STORAGE_TAG_TABLE_FILES
---

Displays the file information of the partition table of the Tag Table.


|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|FILE_ID|File identifier|
|STATE|Index status<br> - COMPLETE: Data stored, index build complete<br> - INDEXING: Index build in progress<br> - FILLED: Data is full, waiting for Index build<br> - PARTIAL: Data not yet full, waiting for Index build|
|REF_COUNT|Number of sessions currently referencing the file|
|ROW_COUNT|Number of records stored in the file, including those that were deleted|
|DEL_COUNT|Number of records deleted from the file|
|MIN_DATE|Minimum datatime value of this data file.|
|MAX_DATE|Maximum datatime value of this data file.|


### V$STORAGE_TAG_INDEX
---

Displays index information generated in Tag Table.

|Column Name|Description|
|--|--|
|TABLE_ID|Table identifier|
|INDEX_ID|Index identifier (if INDEX_ID is 4294967295 it is a default index that is created automatically when the tag table is created.)|
|INDEX_STATE|Current index build state<br> - IDLE: Build Complete, waiting<br> - INDEXING: Build in progress<br> - STORAGE FULL: Stopped because of disk full|
|DISK_INDEX_END_RID|Index end RID stored in storage|
|MEMORY_INDEX_END_RID|Table end RID in memory index|
|TABLE_END_RID|Table end RID|


## Tag Rollup

### V$ROLLUP
---

Displays the Rollup information that stores information of the Tagdata table.

|Column Name|Description|
|--|--|
|DATABASE_ID|Database identifier (always -1 for local DB)|
|ID|Rollup job ID|
|ROLLUP_TABLE|Name of the rollup table|
|SOURCE_TABLE|Source table name (TAG/ROLLUP)|
|COLUMN_NAME|Target value column aggregated by this rollup|
|ROOT_TABLE|Root source tag table name|
|USER_ID|Owner user ID|
|INTERVAL_TIME|Rollup interval (msec)|
|WAKEUP_INTERVAL|Wakeup interval (msec)|
|LAST_WAKEUP_TIME|Last time the rollup thread woke up|
|NEXT_WAKEUP_TIME|Next scheduled wakeup time|
|ENABLED|Whether the rollup is enabled (1/0)|
|END_RID|Source table end RID processed by this rollup|
|LAST_ELAPSED_MSEC|Elapsed time of the last rollup run (msec)|
|EXT_TYPE|Extension flag (supports FIRST/LAST when set)|
|PREDICATE|Filter predicate for conditional rollups (NULL if none)|
|RUN_STATE|Current worker state: I=INIT, S=SLEEPING, R=RUNNING|



## Stream

### V$STREAMS
---

|Column Name|Description|
|--|--|
|NAME|The name of stream query.|
|LAST_EX_TIME|Last execution time of this query.|
|TABLE_NAME|The name of table which searched from the query|
|END_RID|The last RID read by stream query|
|STATE|Current state of stream query|
|QUERY_TXT|Query text|
|ERROR_MSG|Error message of the last stream execution|
|FREQUENCY|Minimum wait time for query execution. If it is 0, it is executed every record. If it is not 0, it is executed each time. The unit is nanoseconds.|


## License

### V$LICENSE_INFO
---

Displays license information.


|Column Name|Description|
|--|--|
|ID|License ID|
|ISSUE_DATE|Issue date|
|TYPE|License type|
|CUSTOMER|Customer name|
|PROJECT|Project name|
|COUNTRY_CODE|Country code|
|INSTALL_DATE|Installation date|
|VIOLATE_STATUS|License violation status|
|VIOLATE_MSG|License violation message|

`V$LICENSE_STATUS` is not exposed by the Standard 8.5.4 server. Use
`V$LICENSE_INFO` for the license fields available in Standard edition.


## Mutex

### V$MUTEX
---

Displays current mutex status.

|Column Name|Description|Note|
|--|--|--|
|OBJECT|Address of the mutex object| |
|NAME|The name given when creating the mutex| |
|TYPE|Mutex type| - Mutex: pmuMutex<br> - RW Mutex: pmuRWMutex|
|OWNER|ID of the thread that acquired the mutex| - Mutex: 0 if no thread acquired the mutex.<br> - RW Mutex w/ Read-Lock: 0<br> - RW Mutex w/ Write-Lock: ID of the thread that acquired the write lock.|
|LOCK_COUNT|Number of threads that acquired the mutex| - RW Mutex can be 2 or more.|
|PEND_COUNT|Number of threads waiting to acquire a mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
|TRY_COUNT|Number of attempts to acquire the mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
|CONFLICT_COUNT|Number of failed to acquire mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
|WAIT_TICK|Sum of waiting time to acquire mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS<br> - Do not write to RW Mutex|
|WAIT_TICK_AVG|Average time to success after an attempt to acquire a mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1<br> - Do not write to RW Mutex|
|HELD_TICK|Total time from acquiring the mutex to releasing it| - Collect only when TRACE_MUTEX_WAIT_STATUS=1<br> - Do not write to RW Mutex|
|HELD_TICK_AVG|Average time from acquisition to release of mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1<br> - Do not write to RW Mutex|


### V$MUTEX_WAIT_STAT
---

Shows the call stack of the currently waiting mutex.

|Column Name|Description|Note|
|--|--|--|
|THREAD_ID|ID of the thread waiting to acquire the mutex| |
|OBJECT|Address of the mutex being acquired| - Same as OBJECT in V$MUTEX|
|DEPTH|Call stack depth| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
|SYMBOL|Symbol of function that called acquire mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|



## Cluster

The following virtual tables are cluster edition tables and are not exposed by the
Standard server. Check `V$TABLES` on the running edition before querying them.

### V$NODE_STATUS
---

Displays the Node status for each Cluster. Only one is displayed.


|Column Name|Description|
|--|--|
|NODETYPE|Node type. There are two types that can be viewed by queries.<br> - Broker<br> - Warehouse|
|STATE|Node status|


### V$DDL_INFO
---

Displays DDL information performed by Cluster.

|Column Name|Description|
|--|--|
|SEQUENCENUMBER|DDL sequence number|
|TIME|DDL execution time|
|VALUE|DDL query result value (Internal server use)|
|CLIENT|Client name|
|BROKER|Lead Broker Node name|
|USER|User name|
|SQL|DDL query value|

### V$REPLICATION
---

Displays information about the replication operation.


|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|MODE|(Internal server use)|
|STATE|Node status|
|ADDR|Replication Manager address|
|PORT_NO|Replication Manager port number|
|MAX_SENDER_COUNT|Maximum number of Senders that can be created|
|RUN_SENDER_COUNT|Maximum number of active Senders|

### V$REPL_SENDER
---

Displays Sender replication when running Replication.


|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|ID|Sender identifier|
|STATUS|Sender operational status|
|PAYLOAD_RECV_COUNT|Number of payloads received from sender|
|PAYLOAD_RECV_BYTES|Total payload size received from Sender|
|QUEUE_REMAIN_COUNT|Number of buffers remaining in the Receive Queue|
|NET_SEND_COUNT|Net send count|
|NET_SEND_SIZE|Net send size|
|NET_RECV_COUNT|Net receive count|
|NET_RECV_SIZE|Net receive size|


### V$REPL_SENDER_META
---

Displays Sender metadata when running Replication.


|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|SENDER_ID|Sender identifier|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|

### V$REPL_RECEIVER
---

Displays Receiver information when running Replication.


|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|STATUS|Receiver operational status|
|PAYLOAD_RECV_COUNT|Number of payloads received from sender|
|PAYLOAD_RECV_BYTES|Total payload size received from Sender|
|QUEUE_REMAIN_COUNT|Number of buffers remaining in the Receive Queue|
|NET_SEND_COUNT|Net send count|
|NET_SEND_SIZE|Net send size|
|NET_RECV_COUNT|Net receive count|
|NET_RECV_SIZE|Net receive size|

### V$REPL_RECEIVER_META
---

Displays Receiver metadata when running Replication.

|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|


### V$REPL_READER
---

Displays Reader information when running Replication.

|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|SENDER_ID|Sender identifier|
|ID|Reader identifier|
|STATUS|Reader operation status|
|FETCH_COUNT|FETCH count|

### V$REPL_READER_META
---

Displays Reader metadata when running Replication.



|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|SENDER_ID|Sender identifier|
|ID|Reader identifier|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|


### V$REPL_WRITER
---

Displays Writer information when running Replication.


|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|ID|Writer identifier|
|STATUS|Writer operational status|
|APPEND_COUNT|APPEND count|

### V$REPL_WRITER_META
---

Displays Writer metadata when running Replication.

|Column Name|Description|
|--|--|
|HOSTNAME|Replication Node Hostname|
|ID|Writer identifier|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|


## Others

### V$TABLES
---

Displays all Virtual Tables that start with "V$".

|Column Name|Description|
|--|--|
|NAME|Table name|
|TYPE|Table type|
|DATABASE_ID|Database identifier|
|ID|Table identifier|
|USER_ID|User who created table|
|COLCOUNT|Column count|


### V$COLUMNS
---

Displays column information of Virtual Tables.

|Column Name|Description|
|--|--|
|NAME|Column name|
|TYPE|Column data type|
|DATABASE_ID|Database identifier|
|ID|Column identifier|
|LENGTH|Column size|
|TABLE_ID|Table identifier|
|FLAG|Private data|
|PART_PAGE_COUNT|Unused|
|PAGE_VALUE_COUNT|Unused|
|MINMAX_CACHE_SIZE|Unused|
|MAX_CACHE_PART_COUNT|Unused|

### V$RETENTION_JOB
---

Displays table information to which RETENTION POLICY is applied.

|Column Name|Description|
|-------------------|------------------------------------------|
| USER_NAME         | User name                              |
| TABLE_NAME        | applied table name                      |
| POLICY_NAME       | applied policy name                |
| STATE             | RETENTION state (RUNNING/WAITING/STOPPED) |
| LAST_DELETED_TIME | most recently deleted time                 |

### V$USER_AUTH_KEYS
---

Displays public keys registered for challenge authentication.

|Column Name|Description|
|--|--|
|KEY_ID|Key identifier|
|USER_ID|User identifier|
|USER_NAME|User name|
|KEY_ALGO|Key algorithm|
|KEY_PARAM|Key parameter|
|PUBKEY|Public key text|
|ACTIVATED|Whether the key is active|
|VALID_AFTER|Start date of key validity|
|VALID_BEFORE|End date of key validity|
|COMMENT|Key comment|
