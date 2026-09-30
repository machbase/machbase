---
layout : post
title : '프로퍼티'
type: docs
weight: 0
---

프로퍼티란 `$MACHBASE_HOME/conf/machbase.conf` 파일에 정의되어 있는 키-값 쌍을 의미합니다.

이 값들은 마크베이스 서버가 시작할 때 설정되고 실행 중에 계속 사용됩니다. 성능 튜닝을 위해 이 값을 변경하려면 각 값의 의미를 이해하고 주의 깊게 설정해야 합니다.

## 목차

- [목차](#목차)
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

마크베이스 서버가 사용할 CPU의 시작 번호입니다. 마크베이스 서버의 CPU 사용량을 조절하기 위해 사용합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|0|

## CPU_AFFINITY_COUNT

마크베이스 서버가 사용할 CPU의 수입니다. 0으로 설정하면 마크베이스 서버가 모든 CPU를 사용합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|0|

## CPU_COUNT

시스템에 설정된 CPU의 수를 지정합니다. 마크베이스는 이 값을 기반으로 스레드 수를 결정합니다. 0으로 지정하면 시스템의 모든 CPU를 사용합니다.

||Value|
|---|---|
|최소값|0 (시스템에 물리적으로 설치된 CPU 수를 자동 감지)|
|최대값|2^32 - 1|
|기본값|1|

## CPU_PARALLEL

CPU당 생성할 스레드의 수를 지정합니다. 이 값이 2이고 CPU의 수가 2이면 CPU마다 병렬 스레드가 2개씩 생성되므로 병렬 처리 스레드의 수는 4가 됩니다. 이 값이 너무 크면 메모리가 빨리 소모될 수 있습니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|1|

## DBS_PATH

마크베이스 서버의 기본 데이터가 저장될 경로를 지정합니다. 기본값은 `?/dbs`로, `$MACHBASE_HOME/dbs`를 의미합니다.

||Value|
|---|---|
|기본값|?/dbs|

## DEFAULT_LSM_MAX_LEVEL

LSM 인덱스의 기본 레벨을 설정합니다. 인덱스를 생성할 때 `MAX_LEVEL` 값을 입력하지 않으면 이 값이 적용됩니다.

||Value|
|---|---|
|최소값|0|
|최대값|3|
|기본값|2|

## DISK_BUFFER_COUNT

디스크 입출력을 위한 버퍼의 수를 지정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|16|

## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스에 대한 체크포인트 주기를 설정합니다. 너무 길게 설정하면 인덱스 빌드 중에 오류가 발생할 수 있습니다.

||Value|
|---|---|
|최소값|1 (sec)|
|최대값|2^32 - 1 (sec)|
|기본값|120 (sec)|

## DISK_COLUMNAR_INDEX_FDCACHE_COUNT

열어 두는 인덱스 파티션 파일 디스크립터의 수를 지정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|0|

## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH

마크베이스 서버를 종료할 때 인덱스 정보를 디스크에 모두 반영할지 설정합니다. 이 값을 1로 설정하면 모든 인덱스 정보를 디스크에 반영한 뒤 종료하므로 종료 시 대기 시간이 길어질 수 있습니다.

||Value|
|---|---|
|최소값|0 (False)|
|최대값|1 (True)|
|기본값|0 (False)|

## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE

페이지 캐시의 최대 크기를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|32 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

테이블 데이터의 체크포인트 주기를 설정합니다. 이 값이 너무 크면 재시작 시 복구 시간이 매우 길어지고, 너무 작으면 I/O가 자주 발생하여 전체 성능이 저하될 수 있습니다.

||Value|
|---|---|
|최소값|1 (sec)|
|최대값|2^32 - 1 (sec)|
|기본값|120 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT

테이블의 컬럼 데이터에 대해 열어 두는 파일 디스크립터의 최대 수를 지정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|0|

## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE

`_ARRIVAL_TIME` 컬럼에 설정되는 기본 MINMAX 캐시의 크기를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|100 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

컬럼 파티션이 가득 찼을 때만 flush할지 여부를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

파티션 파일을 디스크에 반영하는 주기를 설정합니다. 설정된 파티션 수보다 많은 데이터가 입력되면 이 주기와 관계없이 디스크에 반영됩니다.

||Value|
|---|---|
|최소값|0 (sec)|
|최대값|2^32 - 1 (sec)|
|기본값|3 (sec)|

## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE

1로 설정하면 `_ARRIVAL_TIME` 컬럼의 값이 감소하더라도 입력을 허용합니다. 0이면 `_ARRIVAL_TIME` 컬럼 값의 최대값보다 작은 값이 입력될 때 오류로 처리합니다.

||Value|
|---|---|
|최소값|0 (False)|
|최대값|1 (True)|
|기본값|1 (True)|

## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE

시작 시 복구를 위해 사용되는 더블 라이트 파일이 한 번에 증가하는 크기를 지정합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^32 - 1|
|기본값|1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE

파일을 생성할 때 더블 라이트 파일이 확보하는 용량을 지정합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^32 - 1|
|기본값|2 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE

컬럼 파티션을 위해 확보하는 메모리의 블록 크기를 지정합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^64 - 1|
|기본값|2 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

로그 테이블이 할당하는 최대 메모리 크기를 지정합니다. 서버가 이 값 이상의 메모리를 할당하게 되면 메모리 사용량이 이 값 이하로 줄어들 때까지 메모리 할당이 대기하므로 성능이 저하됩니다. 이 값은 물리 메모리의 50~80% 정도로 설정할 것을 권장합니다.

||Value|
|---|---|
|최소값|256 * 1024 * 1024|
|최대값|2^64 - 1|
|기본값|8 * 1024 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

마크베이스 서버가 시작할 때, 메모리 할당에 의한 성능 저하를 막기 위해 이 값만큼 메모리를 미리 확보합니다. 이 메모리는 데이터 입력 버퍼로만 사용되므로 메모리가 충분할 때만 사용할 것을 권장합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^64 - 1|
|기본값|100 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT

로그 테이블에 데이터를 입력할 때, 컬럼 데이터 파일을 위한 메모리 사용량이 이 값을 사용해 다음과 같이 계산한 제한 값을 초과하면 입력 성능을 제한합니다.

```c
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE * (DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT / 100)
```

||Value|
|---|---|
|최소값|0|
|최대값|100|
|기본값|80|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC

컬럼 데이터 파일을 위한 메모리 사용량이 기준을 초과했을 때, 레코드를 입력할 때마다 대기할 시간을 설정합니다.

||Value|
|---|---|
|최소값|0 (msec)|
|최대값|2^32 - 1 (msec)|
|기본값|1 (msec)|

## DISK_IO_THREAD_COUNT

데이터를 디스크에 기록하는 입출력 스레드의 수를 설정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|3|

## DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O를 사용할 때 데이터 파일에 대한 fsync는 불필요합니다. Direct I/O를 사용할 때 fsync를 수행하지 않도록 설정하면(0) 데이터 I/O 성능을 향상시킬 수 있습니다.
fsync를 수행하지 않아도 일반적인 상황에서는 데이터 유실이 없지만, 전원 차단 등의 장애가 발생할 수 있는 환경에서는 fsync를 수행하도록 설정해야 합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 Direct I/O를 사용할지 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 Direct I/O를 사용할지 설정합니다. 파일 시스템이 Direct I/O를 지원하지 않는 경우(예: ZFS) 0으로 설정해야 합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|1|

## DISK_TABLESPACE_SYNCHRONOUS

디스크 테이블스페이스 파일의 동기화 정책을 설정합니다.

|값|모드|설명|
|---|---|---|
|0|OFF|동기화하지 않음|
|1|NORMAL|더블 라이트 파일 쓰기와 백업 시 동기화|
|2|FULL|NORMAL을 포함하며, 디스크 파일 close 및 end-RID 조정 시 동기화|
|3|EXTRA|FULL을 포함하며, 모든 쓰기마다 동기화|

||Value|
|---|---|
|최소값|0|
|최대값|3|
|기본값|1|

## DUMP_APPEND_ERROR

이 값을 1로 설정하면 Append API가 실패했을 때 `$MACHBASE_HOME/trc/machbase.trc` 파일에 에러 내용을 기록합니다.
이 경우 append 성능이 매우 저하될 수 있으므로 테스트 용도로만 사용할 것을 권장합니다.

사용자 애플리케이션에서 에러를 검사하려면 `SQLAppendSetErrorCallback` API를 사용하는 것이 도움이 됩니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## DUMP_TRACE_INFO

서버가 DBMS 시스템 상태 정보를 `machbase.trc` 파일에 주기적으로 기록하는 주기를 설정합니다.
0으로 설정하면 기록하지 않습니다.

||Value|
|---|---|
|최소값|0 (sec)|
|최대값|2^32 - 1 (sec)|
|기본값|300 (sec)|

## DURATION_BEGIN

`DURATION` 절을 지정하지 않은 `SELECT` 문에 적용하는 기본 duration 값 중 시작 시점을 설정합니다. 검색 범위의 최근 쪽 기준 시각을 현재 시각에서 몇 초 이전으로 할지 지정합니다.
60으로 설정하면 최근 쪽 기준 시각이 현재 시각의 60초 이전이 됩니다.

기본값은 0입니다. `DURATION_BEGIN`과 `DURATION_GAP`이 모두 0이면 기본 시간 범위를 적용하지 않고 모든 데이터를 검색합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|0|

## DURATION_GAP

`DURATION` 절을 지정하지 않은 `SELECT` 문에 적용하는 기본 duration 값 중 기간을 설정합니다. 검색 범위의 최근 쪽 기준 시각에서 과거로 거슬러 올라가는 기간(초)입니다.

* `DURATION_BEGIN`이 0이고 `DURATION_GAP`이 60이면, 현재 시각의 60초 이전부터 현재 시각까지의 데이터를 검색합니다.
* 두 값이 모두 60이면, 현재 시각의 120초 이전부터 60초 이전까지의 데이터를 검색합니다.

기본값은 0입니다. 두 값이 모두 0이면 모든 데이터를 검색합니다. 시간 범위를 설정하려면 `DURATION_GAP`에 양수를 지정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^31 - 1|
|기본값|0|

## ENABLE_CASE_SENSITIVE_PASSWORD

비밀번호의 대소문자 구분 여부를 설정합니다.

* 0: 구분하지 않습니다. 사용자 생성/변경/인증 시 비밀번호를 대문자로 변환합니다.
* 1: 구분합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## FEEDBACK_APPEND_ERROR

Append API 실행 중 오류가 발생했을 때 오류 데이터를 클라이언트에 전송할지 설정합니다. 0이면 클라이언트에 오류 데이터를 전송하지 않고, 1이면 클라이언트에 오류 정보를 전송합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|1|

## GEN_CALLSTACK_FOR_ABORT_ERROR

서버가 비정상 종료된 후 콜 스택을 기록할지 여부를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## GEN_CORE_FILE

서버가 비정상 종료된 후 core 파일을 기록할지 여부를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|1|

## GRANT_REMOTE_ACCESS

원격지에서 데이터베이스에 접근할 수 있는지 결정합니다. 0이면 원격지 접속이 차단됩니다.

||Value|
|---|---|
|최소값|0 (False)|
|최대값|1 (True)|
|기본값|1 (True)|

## BIND_IP_ADDRESS

INET/HTTP 리스너가 바인드할 IP 주소를 지정합니다. Native INET 리스너는 `GRANT_REMOTE_ACCESS=1`인 경우에만 이 주소를 사용하고, `GRANT_REMOTE_ACCESS=0`인 경우 루프백 주소에 바인드합니다. HTTP 리스너는 항상 `BIND_IP_ADDRESS`를 사용하므로 HTTP도 루프백으로 제한하려면 이 값을 `127.0.0.1`로 설정합니다. `0.0.0.0`은 모든 인터페이스를 의미합니다.

||Value|
|---|---|
|기본값|0.0.0.0|

## HTTP_AUTH

REST API 서비스에서 Basic Authentication을 사용할지 여부를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## HTTP_ENABLE

REST API 서비스를 사용할지 여부를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|1|

## HTTP_MAX_MEM

웹 세션당 최대 메모리를 설정합니다.

||Value|
|---|---|
|최소값|1 * 1024 * 1024|
|최대값|2^64 - 1|
|기본값|536870912 (512MB)|

## HTTP_PORT_NO

REST API 포트 번호를 설정합니다.

||Value|
|---|---|
|최소값|1024|
|최대값|65535|
|기본값|5657|

## HTTP_THREAD_COUNT

마크베이스 웹 서버가 사용할 스레드의 수를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1024|
|기본값|2|

## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD

인덱싱되지 않은 레코드의 수가 이 값 이상이 되면 인덱스 빌드 스레드가 인덱스 추가를 시작합니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|100000|

## INDEX_BUILD_THREAD_COUNT

인덱스 생성 스레드의 수를 지정합니다. 0으로 설정하면 인덱스를 생성하지 않습니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|3|

## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX

인덱스당 최대 flush 요청 수를 지정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|3|

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT

LSM 인덱스를 생성할 때 필요 없어진 인덱스 파일을 삭제하는 스레드의 수를 지정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|1024|
|기본값|1|

## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT

LSM 인덱스 생성에 사용할 최대 메모리 사용량을 퍼센트로 설정합니다. 이 퍼센트는 마크베이스가 사용하는 최대 메모리 사용량을 기준으로 합니다. 메모리 사용량이 한도를 초과하면 LSM 파티션 병합이 중지됩니다.

||Value|
|---|---|
|최소값|0|
|최대값|100|
|기본값|70|

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT

LSM 인덱스 생성을 위한 병합 연산을 수행하는 스레드의 수를 결정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|1024|
|기본값|3|

## LIN_HASH_BIT_SIZE

내부 선형 해시의 초기 버킷 비트 수를 제어합니다. 타입은 `UINT32`입니다. 이 값을 조정하면 해시 기반 연산의 내부 순회 순서가 바뀔 수 있어, `ORDER BY`를 지정하지 않은 쿼리의 출력 순서가 이전 릴리스와 달라질 수 있습니다.

||Value|
|---|---|
|최소값|1|
|최대값|31|
|기본값|7|

### 확인 SQL

```sql
SELECT name, value, type, min_value, max_value
  FROM v$property
 WHERE name = 'LIN_HASH_BIT_SIZE';
```

## LOOKUP_APPEND_UPDATE_ON_DUPKEY

Lookup 테이블에 Append할 때 Primary Key가 중복되면 어떻게 처리할지 지정합니다.

* 0: Append가 실패합니다.
* 1: 해당 Primary Key의 Row를 Update합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## MAX_QPX_MEM

`GROUP BY`, `DISTINCT`, `ORDER BY` 절을 수행하기 위해 질의 처리기가 사용하는 메모리의 최대 크기를 설정합니다.
하나의 질의가 이 값보다 많은 메모리를 사용하면 해당 질의는 취소됩니다. 이때 에러 메시지를 클라이언트에 전송하고, `machbase.trc` 파일에 관련 내용을 기록합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^64 - 1|
|기본값|1024 * 1024 * 1024|

## MAX_SESSION_COUNT

동시 세션의 최대 개수를 지정합니다. 초과하면 신규 세션이 거부됩니다.

||Value|
|---|---|
|최소값|64|
|최대값|2^64 - 1|
|기본값|4096|

## MAX_STMT_COUNT_PER_SESSION

세션당 생성할 수 있는 statement의 최대 개수를 지정합니다. 초과하면 statement 생성이 실패합니다.

||Value|
|---|---|
|최소값|512|
|최대값|2^32 - 1|
|기본값|1024|

## SESSION_IDLE_TIMEOUT_SEC

세션 유휴(idle) 상태의 최대 시간을 초 단위로 지정합니다. 설정된 시간을 넘기면 세션 연결을 종료합니다. 0이면 사용하지 않습니다.

||Value|
|---|---|
|최소값|0 (sec)|
|최대값|2^64 - 1 (sec)|
|기본값|0 (sec)|

## SESSION_QUERY_TIMEOUT_SEC

쿼리 실행 최대 시간을 초 단위로 지정합니다. 설정된 시간을 넘기면 해당 쿼리를 취소합니다. 0이면 사용하지 않습니다.

||Value|
|---|---|
|최소값|0 (sec)|
|최대값|2^64 - 1 (sec)|
|기본값|0 (sec)|

## MEMORY_ROW_TEMP_TABLE_PAGESIZE

Volatile 테이블 및 Lookup 테이블을 위한 임시 테이블스페이스의 페이지 크기를 설정합니다. Volatile 테이블 및 Lookup 테이블의 레코드는 페이지에 저장되므로, 이 값은 Volatile 테이블의 최대 레코드 크기보다 커야 합니다.
한 페이지에 N개의 레코드를 입력하려면 이 값을 최대 레코드 크기 * N으로 설정해야 합니다.

||Value|
|---|---|
|최소값|8 * 1024|
|최대값|2^32 - 1|
|기본값|32 * 1024|

## PID_PATH

마크베이스 서버 프로세스의 PID 파일이 기록되는 위치를 지정합니다. 기본값은 `?/conf`이며, `$MACHBASE_HOME/conf`를 의미합니다.

||Value|
|---|---|
|기본값|?/conf|

|PID_PATH 값|PID 파일 위치 경로|
|---|---|
|지정하지 않음|$MACHBASE_HOME/conf/machbase.pid|
|?/test|$MACHBASE_HOME/test/machbase.pid|
|/tmp|/tmp/machbase.pid|

## PORT_NO

마크베이스 서버 프로세스가 클라이언트와 통신하기 위한 TCP/IP 포트를 지정합니다. 기본값은 5656입니다.

||Value|
|---|---|
|최소값|1024|
|최대값|65535|
|기본값|5656|

## PROCESS_MAX_SIZE

마크베이스 서버 프로세스인 `machbased` 프로그램이 사용하는 최대 메모리 크기를 지정합니다. 이 제한값보다 많은 메모리를 사용하려고 하면 서버는 다음과 같이 동작하여 메모리 사용량을 줄입니다.

* 데이터 입력을 중지하거나 오류로 처리합니다.
* 인덱스 생성 속도를 떨어뜨립니다.

이 경우 성능이 매우 저하되므로, 메모리 과다 사용의 원인을 찾아 해결해야 합니다.

||Value|
|---|---|
|최소값|32 * 1024 * 1024|
|최대값|2^64 - 1|
|기본값|8 * 1024 * 1024 * 1024|

## PVO_CACHE_ENABLE

글로벌 PVO Statement Cache 사용 여부를 설정합니다. Standard 에디션에서만 동작합니다.

||Value|
|---|---|
|최소값|0 (비활성)|
|최대값|1 (활성)|
|기본값|1|

## PVO_CACHE_SHARD_COUNT

PVO Statement Cache의 샤드 수를 설정합니다. 초기화 시점에만 적용되므로 변경하려면 서버를 재시작해야 하며, 런타임에는 변경할 수 없습니다.

||Value|
|---|---|
|최소값|1|
|최대값|256|
|기본값|16|

## PVO_CACHE_MAX_MEMORY_SIZE

PVO Statement Cache 전체가 사용할 최대 메모리 크기(바이트)를 설정합니다. 설정된 값은 샤드 수에 따라 균등하게 분배되어 적용됩니다. 런타임에 변경할 수 있습니다.

||Value|
|---|---|
|최소값|32768|
|최대값|2^64 - 1|
|기본값|268435456|

## PVO_CACHE_MAX_PLANS_PER_SQL

하나의 SQL에 대해 보관할 수 있는 최대 플랜(핸들) 수를 설정합니다. 런타임에 변경할 수 있습니다.

||Value|
|---|---|
|최소값|1|
|최대값|512|
|기본값|512|

## PVO_CACHE_MAX_SQL_ENTRIES

PVO Statement Cache에 보관할 수 있는 SQL 엔트리의 최대 개수를 설정합니다. 0은 무제한을 의미합니다. 설정된 값은 샤드 수에 따라 분배되어 적용되며, 런타임에 변경할 수 있습니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|0|

## QUERY_PARALLEL_FACTOR

병렬 질의 실행기의 실행 스레드 수를 지정합니다.
Standard 빌드의 기본값은 0이고, Cluster 빌드의 기본값은 4입니다.

||Value|
|---|---|
|최소값|0|
|최대값|100|
|기본값|0|

## ROLLUP_FETCH_COUNT_LIMIT

롤업 스레드가 한 번에 패치하는 데이터양을 제한합니다.

0으로 설정하면 제한이 없습니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|3000000|

## RS_CACHE_APPROXIMATE_RESULT_ENABLE

결과값 캐시의 추측 모드(approximate result mode)를 사용할지 결정합니다. 이 값이 1이면 결과값 캐시를 사용할 때 추측 값을 얻고(매우 빠르지만 데이터가 부정확할 수 있습니다), 0이면 정확한 값을 얻습니다.

||Value|
|---|---|
|최소값|0 (False)|
|최대값|1 (True)|
|기본값|0 (False)|

## RS_CACHE_ENABLE

결과값 캐시를 사용할지 결정합니다.

||Value|
|---|---|
|최소값|0 (False)|
|최대값|1 (True)|
|기본값|1 (True)|

## RS_CACHE_MAX_MEMORY_PER_QUERY

질의 하나의 결과가 결과값 캐시에서 사용할 수 있는 메모리의 양을 설정합니다. 특정 질의 결과의 메모리 사용량이 이 값을 초과하면 해당 질의의 결과는 결과값 캐시에 저장되지 않습니다.

||Value|
|---|---|
|최소값|1024|
|최대값|2^64 - 1|
|기본값|16 * 1024 * 1024|

## RS_CACHE_MAX_MEMORY_SIZE

결과값 캐시의 최대 메모리 사용량을 지정합니다.

||Value|
|---|---|
|최소값|32 * 1024|
|최대값|2^64 - 1|
|기본값|512 * 1024 * 1024|

## RS_CACHE_MAX_RECORD_PER_QUERY

결과값 캐시에 저장되는 최대 레코드 개수입니다. 질의 결과 레코드의 수가 이 값을 초과하면 해당 질의 결과는 캐시에 저장하지 않습니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^64 - 1|
|기본값|10000|

## RS_CACHE_TIME_BOUND_MSEC

매우 빠르게 실행된 질의의 결과는 결과값 캐시에 저장하지 않는 편이 메모리 사용량을 줄이는 데 좋습니다.

이 값은 얼마나 빨리 실행된 질의를 캐시에 저장하지 않을지 결정합니다. 0으로 설정하면 모든 질의 결과를 결과값 캐시에 저장합니다.

||Value|
|---|---|
|최소값|0 (msec)|
|최대값|2^64 - 1 (msec)|
|기본값|1000 (msec)|

## SHOW_HIDDEN_COLS

기본값인 0이면 `_ARRIVAL_TIME` 컬럼이 `SELECT * FROM` 질의 결과에 표시되지 않습니다. 이 값을 1로 설정하면 해당 컬럼을 표시합니다.

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|0|

## TABLE_SCAN_DIRECTION

태그 테이블의 스캔 방향을 설정합니다. 프로퍼티 값은 -1, 0, 1 중 하나이며 기본값은 0입니다.

* -1: 역방향 스캔
* 0: Tag Table(정방향 스캔), Log Table(역방향 스캔)
* 1: 정방향 스캔

||Value|
|---|---|
|최소값|-1|
|최대값|1|
|기본값|0|

## TAG_CACHE_ENABLE

TAG(키-값) 테이블 캐시의 사용 범위를 비트 OR로 지정합니다.

* 0: 캐시 사용 안 함
* 1: TAG map 캐시
* 2: 실제 row 데이터 캐시
* 4: data file 캐시
* 8: 외부 VARCHAR file 캐시
* 16: delete vector 캐시

||Value|
|---|---|
|최소값|0|
|최대값|31|
|기본값|31|

## TAG_CACHE_MAX_MEMORY_SIZE

TAG 캐시 풀 1개당 최대 메모리(바이트)를 지정합니다. 전체 캐시 한도는 `TAG_CACHE_MAX_MEMORY_SIZE * TAG_CACHE_POOL_COUNT`로 계산됩니다.

||Value|
|---|---|
|최소값|32 * 1024|
|최대값|2^64 - 1|
|기본값|512 * 1024 * 1024|

## TAG_CACHE_POOL_COUNT

TAG 캐시 풀의 개수를 지정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|128|
|기본값|1|

## TAG_MEMORY_INDEX_TYPE

TAG 테이블의 메모리 인덱스 유형을 지정합니다.

* 0: RBTree
* 1: BTree

||Value|
|---|---|
|최소값|0|
|최대값|1|
|기본값|1|

## TAG_MEMORY_INDEX_PANOUT

TAG 메모리 인덱스로 쓰는 B-Tree의 차수(order, fanout)를 지정합니다. `TAG_MEMORY_INDEX_TYPE=1`일 때 적용됩니다.

||Value|
|---|---|
|최소값|127|
|최대값|65536|
|기본값|255|

## TAGDATA_AUTO_META_INSERT

{{< callout type="info" >}}
5.5에서는 이 프로퍼티의 이름이 `TAGDATA_AUTO_NAME_INSERT`이며, 값의 범위도 0/1입니다.
5.7 이하에서는 기본값이 1입니다.
{{< /callout >}}

TAGDATA 테이블에 APPEND/INSERT로 데이터를 입력할 때 일치하는 TAG_NAME이 없으면 어떻게 처리할지 지정합니다.

* 0: 입력이 실패합니다.
* 1: 입력하려는 TAG_NAME 값을 입력합니다. 추가 메타데이터 컬럼이 있으면 해당 컬럼의 값은 모두 NULL로 입력됩니다.
* 2: 입력하려는 TAG_NAME 값과 함께 추가 메타데이터 컬럼 값도 입력합니다.
    * APPEND에서만 유효한 설정입니다. INSERT는 추가 메타데이터 컬럼 값을 입력할 수 없으므로 1과 같이 동작합니다.
    * 이 설정을 사용하면 APPEND 시 반드시 메타데이터 컬럼 값까지 포함한 APPEND 파라미터로 입력해야 합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2|
|기본값|2|

## TAG_TABLE_META_MAX_SIZE

TAGDATA 테이블을 생성할 때 메타데이터 영역을 보관할 메모리의 최대 크기를 설정합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^32 - 1|
|기본값|524288000|

## TAG_PARTITION_COUNT

Tag 테이블을 구성하는 Key Value 테이블의 개수를 지정합니다.

||Value|
|---|---|
|최소값|1|
|최대값|1024|
|기본값|4|

## TAG_DATA_PART_SIZE

Tag 데이터 저장 공간의 파티션 크기를 결정합니다.

||Value|
|---|---|
|최소값|1048576 (1MB)|
|최대값|1073741824 (1GB)|
|기본값|16777216 (16MB)|

## TRACE_LOGFILE_COUNT

`TRACE_LOGFILE_PATH`에 생성되는 로그 트레이스 파일의 최대 수를 지정합니다. 디스크 공간을 절약하기 위해, 최대 개수보다 많은 로그 파일이 생성되면 가장 오래된 로그 파일을 삭제합니다.

최대 개수를 넘어 가장 오래된 파일이 삭제되면, 삭제된 파일의 이름이 가장 최신 로그 파일의 이름으로 사용됩니다.

||Value|
|---|---|
|최소값|1|
|최대값|2^32 - 1|
|기본값|1000|

## TRACE_LOGFILE_PATH

로그 트레이스 파일(`machbase.trc`, `machadmin.trc`, `machsql.trc`)의 경로를 설정합니다.
이 파일들은 마크베이스의 시작, 종료, 실행 시 내부 정보를 계속 기록합니다. 기본값인 `?/trc`는 `$MACHBASE_HOME/trc`를 의미합니다.

||Value|
|---|---|
|기본값|?/trc|

|TRACE_LOGFILE_PATH 값|trc 디렉터리 위치|
|---|---|
|지정하지 않음|$MACHBASE_HOME/trc/|
|?/test|$MACHBASE_HOME/test/|
|/tmp|/tmp/|

## TRACE_LOGFILE_SIZE

로그 트레이스 파일의 최대 크기를 설정합니다. 이 크기보다 많은 데이터를 기록해야 하면 새 로그 파일을 생성합니다.

||Value|
|---|---|
|최소값|1024 * 1024|
|최대값|2^32 - 1|
|기본값|10 * 1024 * 1024|

## TRACE_LOG_LEVEL

트레이스 로그의 상세 수준을 설정합니다. 값이 높을수록 더 상세한 로그를 기록합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^32 - 1|
|기본값|277|

## UNIX_PATH

Unix domain socket 이름을 설정합니다.

||Value|
|---|---|
|기본값|machbase-unix|

## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE

시스템의 모든 Volatile 테이블과 Lookup 테이블이 사용하는 메모리 총량의 한도를 설정합니다.

||Value|
|---|---|
|최소값|0|
|최대값|2^64 - 1|
|기본값|2 * 1024 * 1024 * 1024|
