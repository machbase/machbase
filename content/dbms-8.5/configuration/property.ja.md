---
layout : post
title : プロパティ
type : docs
toc: true
weight: 0
---

サーバーの設定を、$MACHBASE_HOME/conf/machbase.conf にキーと値の組として保存します。
起動時に読み込まれ、稼働中に使用されます。性能調整で変更する場合は、各項目の意味を理解して慎重に設定してください。

## 目次 {#index}

- [目次](#index)
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


## CPU_AFFINITY_BEGIN_ID {#cpu_affinity_begin_id}

使用する CPU の開始番号です。CPU の使用範囲を制御します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## CPU_AFFINITY_COUNT {#cpu_affinity_count}

使用する CPU 数です。0 はすべての CPU を使用します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## CPU_COUNT {#cpu_count}

システムの CPU 数を指定し、スレッド数の決定に使用します。0 は実際の全 CPU を使用します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0（実装 CPU 数を自動検出）</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

## CPU_PARALLEL {#cpu_parallel}

CPU あたりのスレッド数です。値が 2、CPU 数が 2 なら、合計 4 並列になります。大きすぎるとメモリを多く消費します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## DBS_PATH {#dbs_path}

基本データの保存先です。既定は ?/dbs、つまり $MACHBASE_HOME/dbs です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>既定値</td>
      <td>?/dbs</td>
    </tr>
  </tbody>
</table>


## DEFAULT_LSM_MAX_LEVEL {#default_lsm_max_level}

LSM の既定レベルです。CREATE INDEX で MAX_LEVEL を省略すると適用します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>3</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## DISK_BUFFER_COUNT {#disk_buffer_count}

ディスク I/O バッファーの数です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC {#disk_columnar_index_checkpoint_interval_sec}

インデックスのチェックポイント間隔です。長すぎると構築時にエラーが発生する場合があります。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1 (sec)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 -1 (sec)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>120 (sec)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_INDEX_FDCACHE_COUNT {#disk_columnar_index_fdcache_count}

開いておくインデックスパーティションのファイルディスクリプター数です。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH {#disk_columnar_index_shutdown_build_finish}

停止時にインデックス情報をディスクへ反映するかを指定します。1 はすべて反映してから終了するため、待ち時間が長くなる場合があります。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0 (False)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE {#disk_columnar_page_cache_max_size}

ページキャッシュの最大サイズです。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>32 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC {#disk_columnar_table_checkpoint_interval_sec}

テーブルデータのチェックポイント間隔です。長すぎると再起動時の復旧が長くなり、短すぎると I/O が増えて性能が低下します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1 (sec)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1 (sec)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>120 (sec)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT {#disk_columnar_table_column_fdcache_count}

テーブルの列データ用に開くファイルディスクリプターの最大数です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE {#disk_columnar_table_column_minmax_cache_size}
_ARRIVAL_TIME の既定の MINMAX キャッシュサイズです。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2 ^ 64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>100 *1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE {#disk_columnar_table_column_part_flush_mode}

列パーティションが満杯の場合だけフラッシュするかを指定します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC {#disk_columnar_table_column_part_io_interval_min_sec}
パーティションファイルをディスクへ反映する間隔です。設定したパーティション数を超える入力がある場合は、間隔に関係なく反映します。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (sec)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32-1 (sec)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>3 (sec)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE {#disk_columnar_table_time_inversion_mode}

1 は _ARRIVAL_TIME が小さくなる入力も許可します。0 は、既存の最大時刻より前の値をエラーにします。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (False)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1 (True)</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE {#disk_columnar_tablespace_dwfile_ext_size}

起動時の復旧に使用する二重書き込みファイルの、1 回の拡張サイズです。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE {#disk_columnar_tablespace_dwfile_int_size}
二重書き込みファイルの作成時に確保する領域です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>2 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE {#disk_columnar_tablespace_memory_ext_size}

列パーティション用に確保するメモリブロックのサイズです。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>2 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE {#disk_columnar_tablespace_memory_max_size}

Log テーブルの最大メモリ量です。上限を超える場合、使用量が下がるまで確保を待ちます。物理メモリの 50～80% を推奨します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>256 * 1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>8 * 1024 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE {#disk_columnar_tablespace_memory_min_size}

起動時に事前確保するメモリです。実行中の確保による性能低下を防ぎます。入力バッファー専用なので、メモリに余裕がある場合だけ使用してください。

表 24．値の範囲


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>100 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT {#disk_columnar_tablespace_memory_slowdown_high_limit_pct}

Log の入力時にメモリ使用量が指定値を超えると、入力速度を制限します。

```c
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE * (DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT / 100)
```

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>100</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>80</td>
    </tr>
  </tbody>
</table>


## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC {#disk_columnar_tablespace_memory_slowdown_msec}

列データファイル用のメモリ使用量が基準を超えた場合、レコード入力ごとの待ち時間を指定します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (msec)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1 (msec)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1 (msec)</td>
    </tr>
  </tbody>
</table>


## DISK_IO_THREAD_COUNT {#disk_io_thread_count}

ディスクへ書き込む I/O スレッド数です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>3</td>
    </tr>
  </tbody>
</table>


## DISK_TABLESPACE_DIRECT_IO_FSYNC {#disk_tablespace_direct_io_fsync}

Direct I/O では、データファイルの fsync を省略（0）すると I/O 性能を改善できます。
ただし、停電などの障害時のデータ保護が必要な場合は fsync を有効にしてください。通常時に損失がなくても、障害時には同期が必要です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_TABLESPACE_DIRECT_IO_READ {#disk_tablespace_direct_io_read}

読み取りに Direct I/O を使用するかを指定します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DISK_TABLESPACE_DIRECT_IO_WRITE {#disk_tablespace_direct_io_write}

書き込みに Direct I/O を使用するかを指定します。ZFS など未対応のファイルシステムでは 0 にしてください。

||値|
|-|----|
|最小値|    0|  
|最大値|    1|  
|既定値|    1|


## DISK_TABLESPACE_SYNCHRONOUS {#disk_tablespace_synchronous}

ディスクテーブルスペースの同期ポリシーです。

|値|モード|説明|
|--|--|--|
|0|OFF|同期しない|
|1|NORMAL|二重書き込みファイルへの書き込み時とバックアップ時に同期|
|2|FULL|NORMAL に加え、ファイルクローズ時と end-RID 調整時に同期|
|3|EXTRA|FULL に加え、書き込みごとに同期|

||値|
|-|----|
|最小値| 0|
|最大値| 3|
|既定値| 1|


## DUMP_APPEND_ERROR {#dump_append_error}
1 にすると APPEND API のエラーを $MACHBASE_HOME/trc/machbase.trc に記録します。
入力性能が大きく低下するため、テスト用途に限定することを推奨します。

アプリケーションで確認するには SQLAppendSetErrorCallback を使用します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DUMP_TRACE_INFO {#dump_trace_info}

DBMS の状態を machbase.trc に定期記録する間隔です。
0 は記録しません。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (sec)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1 (sec)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>300 (sec)</td>
    </tr>
  </tbody>
</table>


## DURATION_BEGIN {#duration_begin}

DURATION を省略した SELECT の検索範囲について、新しい側の基準時刻を現在から何秒さかのぼるか指定します。
60 なら新しい側の時刻は現在の 60 秒前です。

DURATION_BEGIN と DURATION_GAP が両方とも 0 の場合、既定の時間範囲を適用せず、全データを対象にします。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## DURATION_GAP {#duration_gap}

DURATION を省略した SELECT で、新しい側の基準時刻から過去にさかのぼる検索期間（秒）を指定します。

* DURATION_BEGIN が 0、DURATION_GAP が 60 なら、現在の 60 秒前から現在までが対象です。
* 両方が 60 なら、現在の 120 秒前から 60 秒前までが対象です。

両方が 0 の場合は全データを対象にします。時間範囲を設定する場合は、DURATION_GAP に正の値を指定してください。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^31 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## ENABLE_CASE_SENSITIVE_PASSWORD {#enable_case_sensitive_password}

パスワードの大文字と小文字を区別するかを指定します。

* 0：区別しない。作成、変更、認証時に大文字へ変換。
* 1：区別する。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## FEEDBACK_APPEND_ERROR {#feedback_append_error}

APPEND エラーをクライアントへ送信するかを指定します。0 は送信なし、1 はエラー情報を送信します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

## GEN_CALLSTACK_FOR_ABORT_ERROR {#gen_callstack_for_abort_error}

異常終了後にコールスタックを記録するかを指定します。

||値|
|-|----|
|最小値| 0|
|最大値| 1|
|既定値| 0|


## GEN_CORE_FILE {#gen_core_file}

異常終了後にコアファイルを記録するかを指定します。

||値|
|-|----|
|最小値| 0|
|最大値| 1|
|既定値| 1|


## GRANT_REMOTE_ACCESS {#grant_remote_access}

リモート接続を許可するかを指定します。0 は拒否します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (False)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1 (True)</td>
    </tr>
  </tbody>
</table>


## `BIND_IP_ADDRESS` {#bind_ip_address}

INET/HTTP のバインド IP です。ネイティブ INET は `GRANT_REMOTE_ACCESS=1` の場合だけこの値を使用し、0 の場合はループバックにバインドします。HTTP は常に `BIND_IP_ADDRESS` を使用するため、HTTP もローカルに限定する場合は `127.0.0.1` を指定してください。`0.0.0.0` はすべてのインターフェースを意味します。

| 項目 | 値 |
|:--|:--|
| 既定値 | 0.0.0.0 |

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>既定値</td>
      <td>0.0.0.0</td>
    </tr>
  </tbody>
</table>


## HTTP_AUTH {#http_auth}

REST API の Basic 認証を有効にするかを指定します。

||値|
|-|----|
|最小値| 0|
|最大値| 1|
|既定値| 0|


## HTTP_ENABLE {#http_enable}

REST API サービスを有効にするかを指定します。

||値|
|-|----|
|最小値| 0|
|最大値| 1|
|既定値| 1|


## HTTP_MAX_MEM {#http_max_mem}

Web セッションごとの最大メモリ量です。

||値|
|-|----|
|最小値| 1 * 1024 * 1024|
|最大値| 2^64 - 1|
|既定値| 536870912 (512MB)|


## HTTP_PORT_NO {#http_port_no}

REST API のポートです。

||値|
|-|----|
|最小値| 1024|
|最大値| 65535|
|既定値| 5657|


## HTTP_THREAD_COUNT {#http_thread_count}

Web サーバーのスレッド数です。

||値|
|-|----|
|最小値| 0|  
|最大値| 1024|
|既定値| 2|


## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD {#index_build_max_row_count_per_thread}
未索引のレコード数がこの値を超えると、構築スレッドがインデックスの追加を開始します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>100000</td>
    </tr>
  </tbody>
</table>


## INDEX_BUILD_THREAD_COUNT {#index_build_thread_count}
インデックス構築スレッド数です。0 は構築しません。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>3</td>
    </tr>
  </tbody>
</table>


## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX {#index_flush_max_request_count_per_index}
インデックスごとの最大フラッシュ要求数です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT {#index_level_partition_ager_thread_count}
LSM 構築後に不要なファイルを削除するスレッド数です。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT {#index_level_partition_build_memory_high_limit_pct}
LSM 構築の最大メモリ使用率です。Machbase の最大メモリ量を基準にします。上限を超えると、LSM のパーティションマージを停止します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>100</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>70</td>
    </tr>
  </tbody>
</table>

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT {#index_level_partition_build_thread_count}
LSM 構築でマージを実行するスレッド数です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

## LIN_HASH_BIT_SIZE {#lin_hash_bit_size}
内部の線形ハッシュの初期バケットビット幅です。型は UINT32。変更によりハッシュ処理の内部スキャン順が変わるため、`ORDER BY` のないクエリーは以前と異なる順になる場合があります。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>31</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>7</td>
    </tr>
  </tbody>
</table>

### 確認SQL {#확인-sql}

```sql
SELECT name, value, type, min_value, max_value
  FROM v$property
 WHERE name = 'LIN_HASH_BIT_SIZE';
```


## LOOKUP_APPEND_UPDATE_ON_DUPKEY {#lookup_append_update_on_dupkey}
Lookup への APPEND で主キーが重複した場合の動作です。

* 0：失敗。
* 1：該当主キーの行を更新。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## MAX_QPX_MEM {#max_qpx_mem}

クエリープロセッサーが GROUP BY、DISTINCT、`ORDER BY` に使用する最大メモリ量です。
1 クエリーが超過すると取り消し、クライアントへエラーを返して machbase.trc に記録します。

||値|
|--|----|
|最小値|    1024 * 1024|
|最大値|    2^64 - 1|
|既定値|    1024 * 1024 * 1024|


## MAX_SESSION_COUNT {#max_session_count}

最大同時セッション数です。上限を超える新規接続は拒否します。

||値|
|--|----|
|最小値|    64|
|最大値|    2^64 - 1|
|既定値|    4096|


## MAX_STMT_COUNT_PER_SESSION {#max_stmt_count_per_session}

セッションあたりの最大ステートメント数です。超過すると作成に失敗します。

||値|
|--|----|
|最小値|    512|
|最大値|    2^32 - 1|
|既定値|    1024|


## SESSION_IDLE_TIMEOUT_SEC {#session_idle_timeout_sec}

アイドル時間の上限（秒）です。超えると切断します。0 は無効です。

||値|
|--|----|
|最小値|    0 (sec)|
|最大値|    2^64 - 1 (sec)|
|既定値|    0 (sec)|


## SESSION_QUERY_TIMEOUT_SEC {#session_query_timeout_sec}

クエリー時間の上限（秒）です。超えると取り消します。0 は無効です。

||値|
|--|----|
|最小値|    0 (sec)|
|最大値|    2^64 - 1 (sec)|
|既定値|    0 (sec)|


## MEMORY_ROW_TEMP_TABLE_PAGESIZE {#memory_row_temp_table_pagesize}
Volatile/Lookup 用の一時テーブルスペースのページサイズです。レコードを格納するため、最大レコードサイズより大きくします。
1 ページに N 行を格納する場合は、最大レコードサイズ × N を指定します。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>8 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>32 * 1024</td>
    </tr>
  </tbody>
</table>


## PID_PATH {#pid_path}
サーバープロセスの PID ファイルの保存先です。既定値 ?/conf は $MACHBASE_HOME/conf を表します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>既定値</td>
      <td>?/conf</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <th>PID_PATH の値</th>
    <th>PID ファイルの保存先</th>
  </thead>
  <tbody>
    <tr>
      <td>未指定</td>
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


## PORT_NO {#port_no}
クライアントとの TCP/IP 通信ポートです。既定値は 5656 です。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>65535</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>5656</td>
    </tr>
  </tbody>
</table>


## PROCESS_MAX_SIZE {#process_max_size}
サーバープロセス machbased の最大メモリ量です。超過時は、使用量を抑えるために次のように動作します。

* 入力を停止、またはエラーにする。
* インデックス構築速度を下げる。

性能が大きく低下するため、過剰使用の原因を調査して解消してください。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>32 * 1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>8 * 1024 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_ENABLE {#pvo_cache_enable}
グローバル PVO ステートメントキャッシュの有効/無効です。Standard 専用です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (無効)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (有効)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_SHARD_COUNT {#pvo_cache_shard_count}
PVO キャッシュのシャード数です。起動時のみ適用し、変更には再起動が必要です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>256</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>16</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_MAX_MEMORY_SIZE {#pvo_cache_max_memory_size}
PVO キャッシュ全体のメモリ上限（バイト）です。シャードに均等に分配されます。動的変更できます。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>32768</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>268435456</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_MAX_PLANS_PER_SQL {#pvo_cache_max_plans_per_sql}
SQL ごとにキャッシュするプラン（ハンドル）の最大数です。動的変更できます。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>512</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>512</td>
    </tr>
  </tbody>
</table>

## PVO_CACHE_MAX_SQL_ENTRIES {#pvo_cache_max_sql_entries}
PVO キャッシュの SQL エントリー上限です。0 は無制限。シャードに分配され、動的変更できます。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## QUERY_PARALLEL_FACTOR {#query_parallel_factor}
並列クエリーの実行スレッド数です。
Standard の既定値は 0、Cluster は 4 です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>100</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## ROLLUP_FETCH_COUNT_LIMIT {#rollup_fetch_count_limit}
ロールアップスレッドが 1 回で取得するデータ量を制限します。

0 は無制限です。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>3000000</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_APPROXIMATE_RESULT_ENABLE {#rs_cache_approximate_result_enable}
結果キャッシュの近似モードです。1 は推測値を使用して高速ですが、不正確な場合があります。0 は正確な値を取得します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0 (False)</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_ENABLE {#rs_cache_enable}
結果キャッシュを使用するかを指定します。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (false)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1 (True)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1 (True)</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_MAX_MEMORY_PER_QUERY {#rs_cache_max_memory_per_query}
1 つのクエリー結果に使うキャッシュメモリの上限です。超える結果は保存しません。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>16 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_MAX_MEMORY_SIZE {#rs_cache_max_memory_size}
結果キャッシュ全体の最大メモリ量です。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>32 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>512 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_MAX_RECORD_PER_QUERY {#rs_cache_max_record_per_query}
キャッシュする結果の最大行数です。超える結果は保存しません。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## RS_CACHE_TIME_BOUND_MSEC {#rs_cache_time_bound_msec}
短時間で実行できるクエリーは、キャッシュしない方がメモリを節約できます。
キャッシュ対象外にする実行時間のしきい値です。0 は全結果を対象にします。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0 (msec)</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64 - 1 (msec)</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>1000 (msec)</td>
    </tr>
  </tbody>
</table>


## SHOW_HIDDEN_COLS {#show_hidden_cols}
既定値 0 では SELECT * に _ARRIVAL_TIME を表示しません。1 は表示します。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## TABLE_SCAN_DIRECTION {#table_scan_direction}
テーブルのスキャン方向です。-1、0、1 を指定し、既定値は 0 です。

* -1：逆方向。
* 0：Tag は順方向、Log は逆方向。
* 1：順方向。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>-1</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## TAG_CACHE_ENABLE {#tag_cache_enable}

ビット OR のフラグで TAG キャッシュを有効にします。

* 0：無効
* 1：TAG マップ
* 2：行データ
* 4：データファイル
* 8：外部 VARCHAR ファイル
* 16：削除ベクトル

||値|
|--|----|
|最小値|    0|
|最大値|    31|
|既定値|    31|


## TAG_CACHE_MAX_MEMORY_SIZE {#tag_cache_max_memory_size}

TAG キャッシュプールごとの最大メモリ量（バイト）です。予約する合計は TAG_CACHE_MAX_MEMORY_SIZE × TAG_CACHE_POOL_COUNT です。

||値|
|--|----|
|最小値|    32 * 1024|
|最大値|    2^64 - 1|
|既定値|    512 * 1024 * 1024|


## TAG_CACHE_POOL_COUNT {#tag_cache_pool_count}

TAG キャッシュプール数です。

||値|
|--|----|
|最小値|    1|
|最大値|    128|
|既定値|    1|


## TAG_MEMORY_INDEX_TYPE {#tag_memory_index_type}

TAG のメモリインデックス型です。

* 0：RBTree
* 1：BTree

||値|
|--|----|
|最小値|    0|
|最大値|    1|
|既定値|    1|


## TAG_MEMORY_INDEX_PANOUT {#tag_memory_index_panout}

TAG メモリインデックスの B ツリーの次数（分岐数）です。`TAG_MEMORY_INDEX_TYPE=1` の場合に有効です。

||値|
|--|----|
|最小値|    127|
|最大値|    65536|
|既定値|    255|


## TAGDATA_AUTO_META_INSERT {#tagdata_auto_meta_insert}
{{<callout type="info">}}
5.5 では TAGDATA_AUTO_NAME_INSERT という名前で、
0 と 1 のみをサポートしました。5.7 以前の既定値は 1 です。
{{</callout>}}

TAGDATA の APPEND/INSERT でタグ名が未登録の場合の処理です。

* 0：入力失敗。
* 1：タグ名を登録。追加メタデータ列はすべて NULL。
* 2：タグ名と追加メタデータ値を登録。
    * APPEND でのみ有効。INSERT は追加メタデータを入力できないため、1 と同じ動作。
    * APPEND 引数にはメタデータ値も含める必要があります。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## TAG_TABLE_META_MAX_SIZE {#tag_table_meta_max_size}

TAGDATA 作成時のメタデータ領域の最大メモリ量です。

||値|
|-|----|
|最小値|    1024*1024|
|最大値|    2^32-1|
|既定値|    524288000|


## TAG_PARTITION_COUNT {#tag_partition_count}

Tag を構成する Key Value テーブル数です。

||値|
|--|--|
|最小値| 1|
|最大値| 1024|
|既定値| 4 |

## TAG_DATA_PART_SIZE {#tag_data_part_size}

Tag のパーティションサイズです。

||値|
|--|--|
|最小値| 1048576 (1MB)|
|最大値| 1073741824 (1GB)|
|既定値| 16777216 (16MB) |

## TRACE_LOGFILE_COUNT {#trace_logfile_count}

TRACE_LOGFILE_PATH に生成するログの最大数です。超えると最も古いログを削除し、ディスクを節約します。

削除した古いファイル名を、新しいログに再利用します。

||値|
|-|----|
|最小値|    1|
|最大値|    2^32 - 1|
|既定値|    1000|


## TRACE_LOGFILE_PATH {#trace_logfile_path}
machbase.trc、machadmin.trc、machsql.trc の保存先です。
起動、終了、稼働中の内部情報を記録します。既定の ?/trc は $MACHBASE_HOME/trc です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>既定値</td>
      <td>?/trc</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <th>TRACE_LOGFILE_PATH </th>
    <th>trc ディレクトリ</th>
  </thead>
  <tbody>
    <tr>
      <td>未指定</td>
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


## TRACE_LOGFILE_SIZE {#trace_logfile_size}
ログファイルの最大サイズです。超える場合は、新しいファイルを作成します。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>1024 * 1024</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^32-1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>10 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>


## TRACE_LOG_LEVEL {#trace_log_level}

トレースログの詳細レベルです。値が大きいほど詳細を記録します。

||値|
|-|----|
|最小値| 0|
|最大値| 2^32 - 1|
|既定値| 277|


## UNIX_PATH {#unix_path}
Unix ドメインソケット名です。

<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>既定値</td>
      <td>machbase-unix</td>
    </tr>
  </tbody>
</table>


## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE {#volatile_tablespace_memory_max_size}
すべての Volatile/Lookup テーブルが使用する合計メモリ量です。


<table>
  <thead>
    <th> </th>
    <th>値</th>
  </thead>
  <tbody>
    <tr>
      <td>最小値</td>
      <td>0</td>
    </tr>
    <tr>
      <td>最大値</td>
      <td>2^64-1</td>
    </tr>
    <tr>
      <td>既定値</td>
      <td>2 * 1024 * 1024 * 1024</td>
    </tr>
  </tbody>
</table>
