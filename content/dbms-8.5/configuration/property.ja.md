---
layout : post
title : プロパティ
type : docs
toc: true
weight: 0
---

サーバーの設定を、`$MACHBASE_HOME/conf/machbase.conf` にキーと値の組として保存します。

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

使用する CPU の開始番号です。サーバーの CPU 使用量を制御するために使用します。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|0|

## CPU_AFFINITY_COUNT {#cpu_affinity_count}

使用する CPU 数です。0 はすべての CPU を使用します。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|0|

## CPU_COUNT {#cpu_count}

システムの CPU 数を指定します。この値をもとにスレッド数を決定します。0 はシステムのすべての CPU を使用します。

||値|
|---|---|
|最小値|0 (実装 CPU 数を自動検出)|
|最大値|2^32 - 1|
|既定値|1|

## CPU_PARALLEL {#cpu_parallel}

CPU あたりに生成するスレッド数です。値が 2、CPU 数が 2 なら、合計 4 並列になります。大きすぎるとメモリを急速に消費します。

||値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|1|

## DBS_PATH {#dbs_path}

基本データの保存先です。既定値は `?/dbs`、つまり `$MACHBASE_HOME/dbs` です。

||値|
|---|---|
|既定値|?/dbs|

## DEFAULT_LSM_MAX_LEVEL {#default_lsm_max_level}

LSM インデックスの既定レベルです。インデックス作成時に `MAX_LEVEL` を省略すると適用します。

||値|
|---|---|
|最小値|0|
|最大値|3|
|既定値|2|

## DISK_BUFFER_COUNT {#disk_buffer_count}

ディスク I/O バッファーの数です。

||値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|16|

## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC {#disk_columnar_index_checkpoint_interval_sec}

インデックスのチェックポイント間隔です。長すぎると構築時にエラーが発生する場合があります。

||値|
|---|---|
|最小値|1 (sec)|
|最大値|2^32 - 1 (sec)|
|既定値|120 (sec)|

## DISK_COLUMNAR_INDEX_FDCACHE_COUNT {#disk_columnar_index_fdcache_count}

開いておくインデックスパーティションのファイルディスクリプター数です。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|0|

## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH {#disk_columnar_index_shutdown_build_finish}

停止時にインデックス情報をすべてディスクへ反映するかを指定します。1 はすべて反映してから終了するため、停止時の待ち時間が長くなる場合があります。

||値|
|---|---|
|最小値|0 (False)|
|最大値|1 (True)|
|既定値|0 (False)|

## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE {#disk_columnar_page_cache_max_size}

ページキャッシュの最大サイズです。

||値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|32 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC {#disk_columnar_table_checkpoint_interval_sec}

テーブルデータのチェックポイント間隔です。長すぎると再起動時の復旧が大幅に長くなり、短すぎると I/O が頻繁に発生して全体の性能が低下する場合があります。

||値|
|---|---|
|最小値|1 (sec)|
|最大値|2^32 - 1 (sec)|
|既定値|120 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT {#disk_columnar_table_column_fdcache_count}

テーブルの列データ用に開くファイルディスクリプターの最大数です。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|0|

## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE {#disk_columnar_table_column_minmax_cache_size}

`_ARRIVAL_TIME` 列に設定される既定の MINMAX キャッシュのサイズです。

||値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|100 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE {#disk_columnar_table_column_part_flush_mode}

列パーティションが満杯の場合だけフラッシュするかを指定します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC {#disk_columnar_table_column_part_io_interval_min_sec}

パーティションファイルをディスクへ反映する間隔です。設定したパーティション数を超える入力がある場合は、間隔に関係なく反映します。

||値|
|---|---|
|最小値|0 (sec)|
|最大値|2^32 - 1 (sec)|
|既定値|3 (sec)|

## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE {#disk_columnar_table_time_inversion_mode}

1 は `_ARRIVAL_TIME` 列の値が小さくなる入力も許可します。0 は、`_ARRIVAL_TIME` 列の最大値より小さい値の入力をエラーにします。

||値|
|---|---|
|最小値|0 (False)|
|最大値|1 (True)|
|既定値|1 (True)|

## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE {#disk_columnar_tablespace_dwfile_ext_size}

起動時の復旧に使用する二重書き込みファイルの、1 回の拡張サイズです。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^32 - 1|
|既定値|1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE {#disk_columnar_tablespace_dwfile_int_size}

二重書き込みファイルの作成時に確保する領域です。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^32 - 1|
|既定値|2 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE {#disk_columnar_tablespace_memory_ext_size}

列パーティション用に確保するメモリブロックのサイズです。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^64 - 1|
|既定値|2 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE {#disk_columnar_tablespace_memory_max_size}

Log テーブルが確保する最大メモリ量です。上限を超えて確保しようとすると、使用量が下がるまで確保を待つため、性能が低下します。物理メモリの 50～80% を推奨します。

||値|
|---|---|
|最小値|256 * 1024 * 1024|
|最大値|2^64 - 1|
|既定値|8 * 1024 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE {#disk_columnar_tablespace_memory_min_size}

起動時に事前確保するメモリです。実行中の確保による性能低下を防ぎます。入力バッファー専用なので、メモリに余裕がある場合だけ使用してください。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^64 - 1|
|既定値|100 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT {#disk_columnar_tablespace_memory_slowdown_high_limit_pct}

Log テーブルへの入力時に、列データファイル用のメモリ使用量が、この値を使って次のように計算した上限を超えると、入力速度を制限します。

```c
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE * (DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT / 100)
```

||値|
|---|---|
|最小値|0|
|最大値|100|
|既定値|80|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC {#disk_columnar_tablespace_memory_slowdown_msec}

列データファイル用のメモリ使用量が基準を超えた場合に、レコード入力ごとに待機する時間を指定します。

||値|
|---|---|
|最小値|0 (msec)|
|最大値|2^32 - 1 (msec)|
|既定値|1 (msec)|

## DISK_IO_THREAD_COUNT {#disk_io_thread_count}

ディスクへ書き込む I/O スレッド数です。

||値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|3|

## DISK_TABLESPACE_DIRECT_IO_FSYNC {#disk_tablespace_direct_io_fsync}

Direct I/O を使用する場合、データファイルの fsync は不要です。Direct I/O で fsync を省略（0）すると、データ I/O の性能を改善できます。
通常時は fsync を実行しなくてもデータは失われませんが、停電などの障害が起こり得る環境では fsync を有効にしてください。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## DISK_TABLESPACE_DIRECT_IO_READ {#disk_tablespace_direct_io_read}

読み取りに Direct I/O を使用するかを指定します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## DISK_TABLESPACE_DIRECT_IO_WRITE {#disk_tablespace_direct_io_write}

書き込みに Direct I/O を使用するかを指定します。ファイルシステムが Direct I/O に対応していない場合（ZFS など）は 0 にしてください。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|1|

## DISK_TABLESPACE_SYNCHRONOUS {#disk_tablespace_synchronous}

ディスクテーブルスペースファイルの同期ポリシーです。

|値|モード|説明|
|---|---|---|
|0|OFF|同期しない|
|1|NORMAL|二重書き込みファイルへの書き込み時とバックアップ時に同期|
|2|FULL|NORMAL に加え、ディスクファイルのクローズ時と end-RID 調整時に同期|
|3|EXTRA|FULL に加え、書き込みごとに同期|

||値|
|---|---|
|最小値|0|
|最大値|3|
|既定値|1|

## DUMP_APPEND_ERROR {#dump_append_error}

1 にすると、Append API が失敗した場合にエラー内容を `$MACHBASE_HOME/trc/machbase.trc` に記録します。
入力性能が大きく低下するため、テスト用途に限定することを推奨します。

ユーザーアプリケーションでエラーを確認するには、`SQLAppendSetErrorCallback` API を使用すると便利です。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## DUMP_TRACE_INFO {#dump_trace_info}

DBMS のシステム状態を `machbase.trc` に定期記録する間隔です。
0 は記録しません。

||値|
|---|---|
|最小値|0 (sec)|
|最大値|2^32 - 1 (sec)|
|既定値|300 (sec)|

## DURATION_BEGIN {#duration_begin}

`DURATION` を省略した `SELECT` に適用する既定の duration のうち、開始時点を指定します。検索範囲の新しい側の基準時刻を、現在から何秒さかのぼるかを指定します。
60 なら新しい側の時刻は現在の 60 秒前です。

既定値は 0 です。`DURATION_BEGIN` と `DURATION_GAP` が両方とも 0 の場合、既定の時間範囲を適用せず、全データを対象にします。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|0|

## DURATION_GAP {#duration_gap}

`DURATION` を省略した `SELECT` に適用する既定の duration のうち、期間を指定します。新しい側の基準時刻から過去にさかのぼる検索期間（秒）です。

* `DURATION_BEGIN` が 0、`DURATION_GAP` が 60 なら、現在の 60 秒前から現在までが対象です。
* 両方が 60 なら、現在の 120 秒前から 60 秒前までが対象です。

既定値は 0 です。両方が 0 の場合は全データを対象にします。時間範囲を設定する場合は、`DURATION_GAP` に正の値を指定してください。

||値|
|---|---|
|最小値|0|
|最大値|2^31 - 1|
|既定値|0|

## ENABLE_CASE_SENSITIVE_PASSWORD {#enable_case_sensitive_password}

パスワードの大文字と小文字を区別するかを指定します。

* 0：区別しません。ユーザーの作成、変更、認証時にパスワードを大文字へ変換します。
* 1：区別します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## FEEDBACK_APPEND_ERROR {#feedback_append_error}

Append API の実行中にエラーが発生した場合、エラーデータをクライアントへ送信するかを指定します。0 は送信せず、1 はエラー情報を送信します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|1|

## GEN_CALLSTACK_FOR_ABORT_ERROR {#gen_callstack_for_abort_error}

異常終了後にコールスタックを記録するかを指定します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## GEN_CORE_FILE {#gen_core_file}

異常終了後にコアファイルを記録するかを指定します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|1|

## GRANT_REMOTE_ACCESS {#grant_remote_access}

リモートからデータベースへ接続できるかを指定します。0 はリモート接続を拒否します。

||値|
|---|---|
|最小値|0 (False)|
|最大値|1 (True)|
|既定値|1 (True)|

## BIND_IP_ADDRESS {#bind_ip_address}

INET/HTTP リスナーのバインド IP です。ネイティブ INET リスナーは `GRANT_REMOTE_ACCESS=1` の場合だけこの値を使用し、`GRANT_REMOTE_ACCESS=0` の場合はループバックにバインドします。HTTP リスナーは常に `BIND_IP_ADDRESS` を使用するため、HTTP もループバックに限定する場合は `127.0.0.1` を指定してください。`0.0.0.0` はすべてのインターフェースを意味します。

||値|
|---|---|
|既定値|0.0.0.0|

## HTTP_AUTH {#http_auth}

REST API サービスで Basic 認証を使用するかを指定します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## HTTP_ENABLE {#http_enable}

REST API サービスを有効にするかを指定します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|1|

## HTTP_MAX_MEM {#http_max_mem}

Web セッションごとの最大メモリ量です。

||値|
|---|---|
|最小値|1 * 1024 * 1024|
|最大値|2^64 - 1|
|既定値|536870912 (512MB)|

## HTTP_PORT_NO {#http_port_no}

REST API のポート番号です。

||値|
|---|---|
|最小値|1024|
|最大値|65535|
|既定値|5657|

## HTTP_THREAD_COUNT {#http_thread_count}

Machbase の Web サーバーが使用するスレッド数です。

||値|
|---|---|
|最小値|0|
|最大値|1024|
|既定値|2|

## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD {#index_build_max_row_count_per_thread}

未索引のレコード数がこの値以上になると、構築スレッドがインデックスの追加を開始します。

||値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|100000|

## INDEX_BUILD_THREAD_COUNT {#index_build_thread_count}

インデックス構築スレッド数です。0 はインデックスを構築しません。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|3|

## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX {#index_flush_max_request_count_per_index}

インデックスごとの最大フラッシュ要求数です。

||値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|3|

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT {#index_level_partition_ager_thread_count}

LSM インデックスの構築時に不要になったインデックスファイルを削除するスレッド数です。

||値|
|---|---|
|最小値|1|
|最大値|1024|
|既定値|1|

## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT {#index_level_partition_build_memory_high_limit_pct}

LSM インデックス構築の最大メモリ使用率です。Machbase の最大メモリ使用量を基準にします。上限を超えると、LSM のパーティションマージを停止します。

||値|
|---|---|
|最小値|0|
|最大値|100|
|既定値|70|

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT {#index_level_partition_build_thread_count}

LSM インデックス構築でマージを実行するスレッド数です。

||値|
|---|---|
|最小値|1|
|最大値|1024|
|既定値|3|

## LIN_HASH_BIT_SIZE {#lin_hash_bit_size}

内部の線形ハッシュの初期バケットビット幅を制御します。型は `UINT32` です。変更するとハッシュ処理の内部スキャン順が変わる場合があるため、`ORDER BY` のないクエリーは以前のリリースと異なる順序で出力される場合があります。

||値|
|---|---|
|最小値|1|
|最大値|31|
|既定値|7|

### 確認用 SQL {#verification-sql}

```sql
SELECT name, value, type, min_value, max_value
  FROM v$property
 WHERE name = 'LIN_HASH_BIT_SIZE';
```

## LOOKUP_APPEND_UPDATE_ON_DUPKEY {#lookup_append_update_on_dupkey}

Lookup テーブルへの Append で主キーが重複した場合の動作を指定します。

* 0：Append が失敗します。
* 1：該当する主キーの行を更新します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## MAX_QPX_MEM {#max_qpx_mem}

クエリープロセッサーが `GROUP BY`、`DISTINCT`、`ORDER BY` の実行に使用する最大メモリ量です。
1 つのクエリーがこの値を超えると取り消し、クライアントへエラーを返して `machbase.trc` に記録します。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^64 - 1|
|既定値|1024 * 1024 * 1024|

## MAX_SESSION_COUNT {#max_session_count}

最大同時セッション数です。上限を超える新規セッションは拒否します。

||値|
|---|---|
|最小値|64|
|最大値|2^64 - 1|
|既定値|4096|

## MAX_STMT_COUNT_PER_SESSION {#max_stmt_count_per_session}

セッションあたりの最大ステートメント数です。超過すると作成に失敗します。

||値|
|---|---|
|最小値|512|
|最大値|2^32 - 1|
|既定値|1024|

## SESSION_IDLE_TIMEOUT_SEC {#session_idle_timeout_sec}

アイドル時間の上限（秒）です。超えると切断します。0 は無効です。

||値|
|---|---|
|最小値|0 (sec)|
|最大値|2^64 - 1 (sec)|
|既定値|0 (sec)|

## SESSION_QUERY_TIMEOUT_SEC {#session_query_timeout_sec}

クエリー実行時間の上限（秒）です。超えると取り消します。0 は無効です。

||値|
|---|---|
|最小値|0 (sec)|
|最大値|2^64 - 1 (sec)|
|既定値|0 (sec)|

## MEMORY_ROW_TEMP_TABLE_PAGESIZE {#memory_row_temp_table_pagesize}

Volatile テーブルと Lookup テーブル用の一時テーブルスペースのページサイズです。これらのレコードはページに格納されるため、Volatile テーブルの最大レコードサイズより大きくします。
1 ページに N 行を格納する場合は、最大レコードサイズ * N を指定します。

||値|
|---|---|
|最小値|8 * 1024|
|最大値|2^32 - 1|
|既定値|32 * 1024|

## PID_PATH {#pid_path}

サーバープロセスの PID ファイルの保存先です。既定値 `?/conf` は `$MACHBASE_HOME/conf` を表します。

||値|
|---|---|
|既定値|?/conf|

|PID_PATH の値|PID ファイルの保存先|
|---|---|
|未指定|$MACHBASE_HOME/conf/machbase.pid|
|?/test|$MACHBASE_HOME/test/machbase.pid|
|/tmp|/tmp/machbase.pid|

## PORT_NO {#port_no}

サーバープロセスがクライアントと通信する TCP/IP ポートです。既定値は 5656 です。

||値|
|---|---|
|最小値|1024|
|最大値|65535|
|既定値|5656|

## PROCESS_MAX_SIZE {#process_max_size}

サーバープロセス `machbased` の最大メモリ量です。この上限を超えて使用しようとすると、使用量を抑えるために次のように動作します。

* 入力を停止、またはエラーにします。
* インデックス構築速度を下げます。

性能が大きく低下するため、過剰使用の原因を調査して解消してください。

||値|
|---|---|
|最小値|32 * 1024 * 1024|
|最大値|2^64 - 1|
|既定値|8 * 1024 * 1024 * 1024|

## PVO_CACHE_ENABLE {#pvo_cache_enable}

グローバル PVO ステートメントキャッシュの有効／無効を指定します。Standard エディション専用です。

||値|
|---|---|
|最小値|0 (無効)|
|最大値|1 (有効)|
|既定値|1|

## PVO_CACHE_SHARD_COUNT {#pvo_cache_shard_count}

PVO ステートメントキャッシュのシャード数です。初期化時のみ適用するため、変更にはサーバーの再起動が必要で、実行中は変更できません。

||値|
|---|---|
|最小値|1|
|最大値|256|
|既定値|16|

## PVO_CACHE_MAX_MEMORY_SIZE {#pvo_cache_max_memory_size}

PVO ステートメントキャッシュ全体のメモリ上限（バイト）です。シャードに均等に分配されます。実行中に変更できます。

||値|
|---|---|
|最小値|32768|
|最大値|2^64 - 1|
|既定値|268435456|

## PVO_CACHE_MAX_PLANS_PER_SQL {#pvo_cache_max_plans_per_sql}

SQL ごとにキャッシュするプラン（ハンドル）の最大数です。実行中に変更できます。

||値|
|---|---|
|最小値|1|
|最大値|512|
|既定値|512|

## PVO_CACHE_MAX_SQL_ENTRIES {#pvo_cache_max_sql_entries}

PVO ステートメントキャッシュに保持する SQL エントリーの上限です。0 は無制限です。シャードに分配され、実行中に変更できます。

||値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|0|

## QUERY_PARALLEL_FACTOR {#query_parallel_factor}

並列クエリー実行器の実行スレッド数です。
既定値は Standard ビルドで 0、Cluster ビルドで 4 です。

||値|
|---|---|
|最小値|0|
|最大値|100|
|既定値|0|

## ROLLUP_FETCH_COUNT_LIMIT {#rollup_fetch_count_limit}

ロールアップスレッドが 1 回で取得するデータ量を制限します。

0 は無制限です。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|3000000|

## RS_CACHE_APPROXIMATE_RESULT_ENABLE {#rs_cache_approximate_result_enable}

結果キャッシュの近似モード（approximate result mode）を使用するかを指定します。1 は結果キャッシュ使用時に推測値を返し、非常に高速ですが不正確な場合があります。0 は正確な値を返します。

||値|
|---|---|
|最小値|0 (False)|
|最大値|1 (True)|
|既定値|0 (False)|

## RS_CACHE_ENABLE {#rs_cache_enable}

結果キャッシュを使用するかを指定します。

||値|
|---|---|
|最小値|0 (False)|
|最大値|1 (True)|
|既定値|1 (True)|

## RS_CACHE_MAX_MEMORY_PER_QUERY {#rs_cache_max_memory_per_query}

1 つのクエリー結果が使用できる結果キャッシュのメモリ量です。これを超えるクエリー結果は結果キャッシュに保存しません。

||値|
|---|---|
|最小値|1024|
|最大値|2^64 - 1|
|既定値|16 * 1024 * 1024|

## RS_CACHE_MAX_MEMORY_SIZE {#rs_cache_max_memory_size}

結果キャッシュ全体の最大メモリ量です。

||値|
|---|---|
|最小値|32 * 1024|
|最大値|2^64 - 1|
|既定値|512 * 1024 * 1024|

## RS_CACHE_MAX_RECORD_PER_QUERY {#rs_cache_max_record_per_query}

結果キャッシュに保存する最大レコード数です。クエリー結果のレコード数がこの値を超える場合は、キャッシュに保存しません。

||値|
|---|---|
|最小値|1|
|最大値|2^64 - 1|
|既定値|10000|

## RS_CACHE_TIME_BOUND_MSEC {#rs_cache_time_bound_msec}

非常に短時間で実行されたクエリーの結果は、キャッシュしない方がメモリを節約できます。

この値は、どの程度速く実行されたクエリーをキャッシュ対象外にするかを決めるしきい値です。0 はすべてのクエリー結果を結果キャッシュに保存します。

||値|
|---|---|
|最小値|0 (msec)|
|最大値|2^64 - 1 (msec)|
|既定値|1000 (msec)|

## SHOW_HIDDEN_COLS {#show_hidden_cols}

既定値 0 では、`SELECT * FROM` クエリーに `_ARRIVAL_TIME` 列を表示しません。1 にすると表示します。

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|0|

## TABLE_SCAN_DIRECTION {#table_scan_direction}

Tag テーブルのスキャン方向です。-1、0、1 のいずれかを指定し、既定値は 0 です。

* -1：逆方向スキャン
* 0：Tag テーブルは順方向スキャン、Log テーブルは逆方向スキャン
* 1：順方向スキャン

||値|
|---|---|
|最小値|-1|
|最大値|1|
|既定値|0|

## TAG_CACHE_ENABLE {#tag_cache_enable}

TAG（キー値）テーブルキャッシュの使用範囲を、ビット OR のフラグで指定します。

* 0：キャッシュを使用しない
* 1：TAG マップキャッシュ
* 2：行データキャッシュ
* 4：データファイルキャッシュ
* 8：外部 VARCHAR ファイルキャッシュ
* 16：削除ベクトルキャッシュ

||値|
|---|---|
|最小値|0|
|最大値|31|
|既定値|31|

## TAG_CACHE_MAX_MEMORY_SIZE {#tag_cache_max_memory_size}

TAG キャッシュプールごとの最大メモリ量（バイト）です。キャッシュ全体の上限は `TAG_CACHE_MAX_MEMORY_SIZE * TAG_CACHE_POOL_COUNT` です。

||値|
|---|---|
|最小値|32 * 1024|
|最大値|2^64 - 1|
|既定値|512 * 1024 * 1024|

## TAG_CACHE_POOL_COUNT {#tag_cache_pool_count}

TAG キャッシュプールの数です。

||値|
|---|---|
|最小値|1|
|最大値|128|
|既定値|1|

## TAG_MEMORY_INDEX_TYPE {#tag_memory_index_type}

TAG テーブルのメモリインデックスの種類を指定します。

* 0：RBTree
* 1：BTree

||値|
|---|---|
|最小値|0|
|最大値|1|
|既定値|1|

## TAG_MEMORY_INDEX_PANOUT {#tag_memory_index_panout}

TAG メモリインデックスの B-Tree の次数（order、fanout）です。`TAG_MEMORY_INDEX_TYPE=1` の場合に有効です。

||値|
|---|---|
|最小値|127|
|最大値|65536|
|既定値|255|

## TAGDATA_AUTO_META_INSERT {#tagdata_auto_meta_insert}

{{< callout type="info" >}}
5.5 では `TAGDATA_AUTO_NAME_INSERT` という名前で、0 と 1 のみをサポートしました。
5.7 以前の既定値は 1 です。
{{< /callout >}}

TAGDATA テーブルへ APPEND/INSERT でデータを入力する際、一致する TAG_NAME がない場合の処理を指定します。

* 0：入力が失敗します。
* 1：入力する TAG_NAME の値を登録します。追加メタデータ列がある場合、その値はすべて NULL になります。
* 2：入力する TAG_NAME の値とともに、追加メタデータ列の値も登録します。
    * APPEND でのみ有効です。INSERT は追加メタデータ列の値を入力できないため、1 と同じ動作になります。
    * この設定では、APPEND 時に必ずメタデータ列の値を含む APPEND パラメーターで入力する必要があります。

||値|
|---|---|
|最小値|0|
|最大値|2|
|既定値|2|

## TAG_TABLE_META_MAX_SIZE {#tag_table_meta_max_size}

TAGDATA テーブル作成時に、メタデータ領域を保持するメモリの最大サイズです。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^32 - 1|
|既定値|524288000|

## TAG_PARTITION_COUNT {#tag_partition_count}

Tag テーブルを構成する Key Value テーブルの数です。

||値|
|---|---|
|最小値|1|
|最大値|1024|
|既定値|4|

## TAG_DATA_PART_SIZE {#tag_data_part_size}

Tag データ格納領域のパーティションサイズです。

||値|
|---|---|
|最小値|1048576 (1MB)|
|最大値|1073741824 (1GB)|
|既定値|16777216 (16MB)|

## TRACE_LOGFILE_COUNT {#trace_logfile_count}

`TRACE_LOGFILE_PATH` に生成するログトレースファイルの最大数です。ディスクを節約するため、最大数を超えると最も古いログファイルを削除します。

最大数を超えて最も古いファイルを削除した場合、削除したファイルの名前を最新のログファイルに再利用します。

||値|
|---|---|
|最小値|1|
|最大値|2^32 - 1|
|既定値|1000|

## TRACE_LOGFILE_PATH {#trace_logfile_path}

ログトレースファイル（`machbase.trc`、`machadmin.trc`、`machsql.trc`）の保存先です。
これらのファイルには、Machbase の起動、終了、稼働中の内部情報を継続して記録します。既定値 `?/trc` は `$MACHBASE_HOME/trc` を表します。

||値|
|---|---|
|既定値|?/trc|

|TRACE_LOGFILE_PATH の値|trc ディレクトリの場所|
|---|---|
|未指定|$MACHBASE_HOME/trc/|
|?/test|$MACHBASE_HOME/test/|
|/tmp|/tmp/|

## TRACE_LOGFILE_SIZE {#trace_logfile_size}

ログトレースファイルの最大サイズです。このサイズを超えて記録する必要がある場合は、新しいログファイルを作成します。

||値|
|---|---|
|最小値|1024 * 1024|
|最大値|2^32 - 1|
|既定値|10 * 1024 * 1024|

## TRACE_LOG_LEVEL {#trace_log_level}

トレースログの詳細レベルです。値が大きいほど詳細を記録します。

||値|
|---|---|
|最小値|0|
|最大値|2^32 - 1|
|既定値|277|

## UNIX_PATH {#unix_path}

Unix ドメインソケット名です。

||値|
|---|---|
|既定値|machbase-unix|

## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE {#volatile_tablespace_memory_max_size}

システム内のすべての Volatile テーブルと Lookup テーブルが使用するメモリ総量の上限です。

||値|
|---|---|
|最小値|0|
|最大値|2^64 - 1|
|既定値|2 * 1024 * 1024 * 1024|
