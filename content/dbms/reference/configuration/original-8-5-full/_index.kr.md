---
type: docs
title: '17.2.6 전체 설정 레퍼런스'
weight: 95
tocSort: true
---


## property


프로퍼티란 __$MACHBASE_HOME/conf/machbase.conf__ 파일에 정의되어 있는 키-값 의 쌍을 의미합니다.

이 값들은 마크베이스 서버가 시작할 때 설정되고 실행시 지속적으로 이용됩니다. 성능 튜닝을 위해서 이 값을 변경하려면 이 값들에 대한 의미를 이해하고, 주의 깊게 설정하여야 합니다.

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

마크베이스 서버가 사용할 CPU의 시작 번호입니다. 마크베이스 서버의 CPU사용량을 조절하기 위해서 사용합니다.

||Value|
|-|-----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|    0|

## CPU_AFFINITY_COUNT

마크베이스 서버가 사용할 CPU의 수입니다. 0으로 설정하면 마크베이스 서버가 모든 CPU를 사용합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|	0|

## CPU_COUNT

시스템에 설정된 CPU의 수를 지정합니다. 이 값을 기반으로 마크베이스의 스레드 수를 결정합니다. 0으로 지정한 경우에는 시스템의 모든 CPU를 사용합니다.

||Value|
|-|----|
|최소값|    0 (시스템에 물리적으로 설치된 CPU수)|
|최대값|	2^32 -1|
|기본값|	1|

## CPU_PARALLEL

CPU당 생성할 스레드의 수를 지정합니다. 만약 이 값이 2이고 cpu의 수가 2인 경우, 두개의 CPU마다 병렬 스레드가 2개씩 생성되므로 병렬처리 스레드의 수가 4가 됩니다. 이 값이 너무 큰 경우, 메모리가 빨리 소모될 수 있습니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 -1|
|기본값|	1|

## DBS_PATH

마크베이스 서버의 기본 데이터가 저장될 경로를 지정합니다. 기본값은 "?/dbs"로, $MACHBASE_HOME/dbs 를 의미합니다.

||Value|
|-|----|
|기본값|	?/dbs|

## DEFAULT_LSM_MAX_LEVEL

LSM인덱스의 기본 레벨을 설정합니다. 인덱스를 생성할 때 MAX_LEVEL값을 입력하지 않으면 이 값이 적용됩니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	3|
|기본값|	2|

## DISK_BUFFER_COUNT

디스크 입출력을 위한 버퍼의 수를 지정합니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	16|

## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스에 대한 체크포인트 주기를 설정합니다. 너무 길게 설정할 경우, 인덱스 빌드에 오류가 발생할 수 있습니다.

||Value|
|-|----|
|최소값|	1 (sec)|
|최대값|    2^32 -1 (sec)|
|기본값|	120 (sec)|

## DISK_COLUMNAR_INDEX_FDCACHE_COUNT

오픈한 인덱스 파티션 파일 디스크립터의 수를 지정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 -1|
|기본값|	0|

## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH

마크베이스 서버를 종료할 때, 인덱스 정보를 디스크에 모두 반영할 것인지를 설정합니다. 이 값을 '1'로 설정하면 모든 인덱스 정보를 디스크에 반영하고 종료하므로 종료시 대기 시간이 길어질 수 있습니다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	0 (False)|

## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE

페이지 캐쉬의 최대 크기를 설정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	32 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

테이블 데이터의 체크포인트 주기를 설정합니다. 이 값이 너무 크면 재시작시 복구 시간이 매우 길어지고, 이 값이 너무 작으면 I/O가 자주 발생하여 전체 성능이 저하될 수 있습니다.

||Value|
|-|----|
|최소값|	1 (sec)|
|최대값|	2^32 -1 (sec)|
|기본값|	120 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT

테이블의 컬럼 데이터에 대한 오픈된 파일 설명자의 최대 수를 지정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	0|

## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE

_ARRIVAL_TIME 컬럼에 설정되는 기본 MINMAX 캐쉬의 크기를 설정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	100 *1024 * 1024|

## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

컬럼 파티션이 가득 찼을 때만 flush할지 여부를 설정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

파티션 파일을 디스크에 반영하는 주기를 설정합니다. 파티션이 설정된 갯수보다 더 많은 데이터를 입력받으면 이 주기와 관계없이 디스크에 반영됩니다.

||Value|
|-|----|
|최소값|	0 (sec)|
|최대값|	2^32-1 (sec)|
|기본값|	3 (sec)|


## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE

설정된 값 만큼 _ARRIVAL_TIME컬럼의 값이 감소하더라도 입력을 허용합니다. 만약 0인 경우 _ARRIVAL_TIME컬럼 값의 최대값보다 작은 값이 입력되면 이는 오류로 처리됩니다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	1 (True)|


## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE

시작시 복구를 위해서 사용되는 더블 라이트 파일이 한번에 증가하는 크기를 지정합니다.

||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^32 - 1|
|기본값|	1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE

파일 생성시에 더블라이트 파일이 확보하는 용량을 지정합니다.

||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^32 - 1|
|기본값|	2* 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE

컬럼 파티션을 위해서 확보하는 메모리의 블록 크기를 지정합니다.

||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	2* 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

로그 테이블에 의하여 할당된 최대 메모리 크기를 지정합니다. 만약 서버가 이 값 이상의 메모리를 할당하게 되면, 메모리 사용량이 이 값 이하로 줄어들 때 까지 메모리 할당이 대기하므로 성능이 저하됩니다. 이 값은 물리적 메모리의 50~80% 정도로 설정할 것을 추천합니다.

||Value|
|-|----|
|최소값|	256 * 1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	8 * 1024 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

마크베이스 서버가 시작할 때, 메모리 할당에 의한 성능 저하를 막기 위해서 이 값 만큼 메모리를 사전 확보합니다. 데이터 입력 버퍼로만 이 메모리를 사용하므로, 메모리가 충분할 경우에만 사용할 것을 추천합니다.

Table 24. Range of values
||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	100 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT

컬럼 데이터 파일을 위한 메모리 사용량이 제한 값을 이 값을 다음과 같이 이용하여 계산하고, 초과한 경우 입력 성능을 저하시킨다.

```sql
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE * (DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT / 100)
```

||Value|
|-|----|
|최소값|	0|
|최대값|	100|
|기본값|	80|

## DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC

컬럼 데이터 파일을 위한 메모리 사용량이 기준을 초과한 경우, 매 레코드 입력시에 다음의 대기 시간을 설정합니다.

||Value|
|-|----|
|최소값|	0 (msec)|
|최대값|	2^32 - 1 (msec)|
|기본값|	1 (msec)|


## DISK_IO_THREAD_COUNT

데이터를 디스크에 기록하는 입출력 스레드의 수를 설정합니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 -1|
|기본값|	3|

## DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O를 실행할 경우, 데이터 파일에 대해서 fsync는 불필요하다. Direct I/O 를 사용할 경우 fsync를 사용하지 않도록 하면 데이터 I/O 성능을 향상시킬 수 있습니다 (0으로 설정).
Fsync를 수행하지 않아도 일반적 상황에서는 데이터 유실이 없으나 전원이 꺼지는 등의 장애 상황이 발생할 수 있는 경우에는 fsync를 수행하도록 설정해야 합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 DIRECT I/O 를 사용할 것인지를 설정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 DIRECT I/O 를 사용할 것인지 설정합니다. 파일 시스템에 따라서 DIRECT I/O 지원하지 않는 경우(ex: ZFS), 0으로 설정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	1|


## DISK_TABLESPACE_SYNCHRONOUS

디스크 테이블스페이스 파일의 동기화 정책을 설정합니다.

|값|모드|설명|
|--|--|--|
|0|OFF|동기화하지 않음|
|1|NORMAL|더블라이트 파일 쓰기와 백업 시 동기화|
|2|FULL|NORMAL을 포함하며 디스크 파일 close 및 end RID 조정 시 동기화|
|3|EXTRA|FULL을 포함하며 모든 write마다 동기화|

||Value|
|-|----|
|최소값| 0|
|최대값| 3|
|기본값| 1|


## DUMP_APPEND_ERROR

이 값을 1로 설정하면 Append API 가 실패한 경우 $MACHBASE_HOME/trc/machbase.trc 파일에 에러 내용을 기록합니다.
이 상황에서 append 성능이 매우 저하될 수 있으므로 테스트용으로만 사용할 것을 권장합니다.

사용자 application에서 에러를 검사하고 싶으면 SQLAppendSetErrorCallback API 를 사용하는 것이 도움이 됩니다.


||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DUMP_TRACE_INFO

서버는 일정한 주기로 DBMS 시스템 상태 정보를 machbase.trc 파일에 주기적으로 기록하는데, 이 주기를 설정합니다.
0으로 설정하면 기록하지 않는다.

||Value|
|-|----|
|최소값|	0 (sec)|
|최대값|	2^32 - 1 (sec)|
|기본값|	300 (sec)|

## DURATION_BEGIN

DURATION 절을 지정하지 않은 SELECT 문에 대해서 기본을 설정하는 duration 값 중 시작시점을 설정합니다.
만약 60을 설정해 두었다면, 현재 시각에서 60초 이전의 데이터를 검색하게 됩니다.

기본값은 0으로 모든 데이터를 검색합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	0|

## DURATION_GAP
DURATION 절을 지정하지 않은 SELECT 문에 대해서 기본을 설정하는 duration 값 중 기간을 설정합니다.

만약 60을 설정해 두었다면, 현재 시각에서 60초 동안의 데이터를 검색하게 됩니다.
DURATION_BEGIN 값도 60이라면, 현재 시각에서 60초 이전부터 60초 동안의 데이터를 검색하게 됩니다.
기본값은 0으로 모든 데이터를 검색합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^31 - 1|
|기본값|	0|

## ENABLE_CASE_SENSITIVE_PASSWORD

비밀번호의 대소문자 구분 여부를 설정합니다.

* 0: 구분하지 않음. 사용자 생성/변경/인증 시 비밀번호를 대문자로 변환합니다.
* 1: 구분함.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## FEEDBACK_APPEND_ERROR

Append API 실행시 오류가 발생하였을 경우, 오류 데이터를 클라이언트에 전송할지를 설정합니다. 0이면 클라이언트에 오류 데이터를 전송하지 않으며 1이면 클라이언트에 오류 정보를 전송합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	1|

## GEN_CALLSTACK_FOR_ABORT_ERROR

서버가 비정상 종료된 후 call stack을 기록할지 여부를 설정합니다.

||Value|
|-|----|
|최소값| 0|
|최대값| 1|
|기본값| 0|


## GEN_CORE_FILE

서버가 비정상 종료된 후 core 파일을 기록할지 여부를 설정합니다.

||Value|
|-|----|
|최소값| 0|
|최대값| 1|
|기본값| 1|


## GRANT_REMOTE_ACCESS

원격지에서 데이터베이스에 접근할 수 있는지를 결정합니다. 0이면 원격지 접속이 차단됩니다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|    1 (True)|

## BIND_IP_ADDRESS

INET/HTTP 리스너가 바인드할 IP 주소를 지정합니다. Native INET 리스너는 `GRANT_REMOTE_ACCESS=1`인 경우 이 주소를 사용하고, `GRANT_REMOTE_ACCESS=0`인 경우 루프백 주소에 바인드합니다. HTTP 리스너는 항상 `BIND_IP_ADDRESS`를 사용하므로 HTTP도 루프백으로 제한하려면 이 값을 `127.0.0.1`로 설정합니다. `0.0.0.0`은 모든 인터페이스를 의미합니다.

||Value|
|-|----|
|기본값|	0.0.0.0|

## HTTP_AUTH

REST API 서비스에서 Basic Authentication을 사용할지 여부를 설정합니다.

||Value|
|-|----|
|최소값| 0|
|최대값| 1|
|기본값| 0|

## HTTP_ENABLE

REST API 서비스를 사용할지 여부를 설정합니다.

||Value|
|-|----|
|최소값| 0|
|최대값| 1|
|기본값| 1|

## HTTP_MAX_MEM

웹 세션당 최대 메모리를 설정합니다.

||Value|
|-|----|
|최소값| 1 * 1024 * 1024|
|최대값| 2^64 - 1|
|기본값| 536870912 (512MB)|

## HTTP_PORT_NO

REST API 포트 번호를 설정합니다.

||Value|
|-|----|
|최소값| 1024|
|최대값| 65535|
|기본값| 5657|

## HTTP_THREAD_COUNT

마크베이스의 웹 서버가 사용할 스레드의 개수를 설정 가능하다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1024|
|기본값|    2|

## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD

인덱스 빌드 스레드가 인덱싱 되지 않은 레코드의 수가 이 값 이상이 되면 인덱스를 추가하기 시작합니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	100000|

## INDEX_BUILD_THREAD_COUNT

인덱스 생성 스레드의 수를 지정합니다. 0으로 설정되면 인덱스를 생성하지 않는다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|	3|

## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX

인덱스당 최대 flush 요청 수를 지정합니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2 ^ 32 - 1|
|기본값|	3|

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT

LSM 인덱스 생성시에 필요없는 인덱스 파일의 삭제를 위한 스레드의 갯수를 지정합니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	1024|
|기본값|	1|

## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT

LSM 인덱스 생성을 위한 최대 메모리 사용량의 퍼센트로 설정합니다. 이 퍼센트는 마크베이스가 사용하는 최대 메모리사용량 대비하여 설정됩니다. 메모리 사용량이 한도를 초과하면, LSM 파티션 병합은 중지됩니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	100|
|기본값|	70|

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT

LSM 인덱스의 생성을 위한 병합 연산을 수행하는 스레드의 수를 결정합니다.

||Value|
|-|----|
|최소값|	1|
|최대값|    1024|
|기본값|	3|

## LIN_HASH_BIT_SIZE

내부 선형 해시의 초기 버킷 비트 수를 제어합니다. 타입은 `UINT32`이며, 해시 기반 연산의 내부 순회 순서에 영향을 줄 수 있어 정렬을 지정하지 않은 쿼리의 출력 순서가 이전과 달라질 수 있습니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	31|
|기본값|	7|

### 확인 SQL
```sql
SELECT name, value, type, min_value, max_value
  FROM v$property
 WHERE name = 'LIN_HASH_BIT_SIZE';
```

## LOOKUP_APPEND_UPDATE_ON_DUPKEY

Lookup 테이블에 Append 할 때 Primary Key가 중복일 경우 어떻게 처리할지 지정합니다.

* 0 : Append 실패
* 1 : 해당 Primary Key 에 대해서 Row를 Update 합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## MAX_QPX_MEM

GROUP BY, DISTINCT, ORDER BY 절을 수행하기 위해서 질의처리기가  이용하는 메모리의 최대 양을 설정합니다.
하나의 질의문이 이보다 큰 값으로 메모리를 사용하게 되면 질의는 취소됩니다. 이때, 에러메시지를 클라이언트에 전송하고, machbase.trc 파일에 관련 내용이 기록됩니다.

||Value|
|--|----|
|최소값|	1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	1024 * 1024 * 1024|

## MAX_SESSION_COUNT

동시 세션의 최대 개수를 지정합니다. 초과 시 신규 세션이 거부됩니다.

||Value|
|--|----|
|최소값|	64|
|최대값|	2^64 - 1|
|기본값|	4096|

## MAX_STMT_COUNT_PER_SESSION

세션당 생성 가능한 statement의 최대 개수를 지정합니다. 초과 시 statement 생성/사용이 실패합니다.

||Value|
|--|----|
|최소값|	512|
|최대값|	2^32 - 1|
|기본값|	1024|

## SESSION_IDLE_TIMEOUT_SEC

세션 유휴(idle) 상태의 최대 시간을 초 단위로 지정합니다. 설정된 시간을 넘기면 세션 연결을 종료합니다. 0이면 사용하지 않는다.

||Value|
|--|----|
|최소값|	0 (sec)|
|최대값|	2^64 - 1 (sec)|
|기본값|	0 (sec)|

## SESSION_QUERY_TIMEOUT_SEC

쿼리 실행 최대 시간을 초 단위로 지정합니다. 설정된 시간을 넘기면 해당 쿼리를 취소합니다. 0이면 사용하지 않는다.

||Value|
|--|----|
|최소값|	0 (sec)|
|최대값|	2^64 - 1 (sec)|
|기본값|	0 (sec)|

## MEMORY_ROW_TEMP_TABLE_PAGESIZE

Volatile table및 lookup 테이블을 위한 임시 테이블 스페이스의 페이지 크기를 설정합니다. Volatile 테이블 및 lookup 테이블의 레코드들은 페이지에 저장되므로 volatile을 위한 최대 레코드 크기보다 커야 합니다.
페이지에 N개의 레코드를 입력하고 싶으면 이 값을 최대 레코드 크기 * N으로 설정해야 합니다.

||Value|
|-|----|
|최소값|	8 * 1024|
|최대값|	2^32 - 1|
|기본값|	32 * 1024|

## PID_PATH

마크베이스 서버 프로세스의 PID파일이 기록되는 위치를 지정합니다. 기본값은 "?/conf"이며 이는 $MACHBASE_HOME/conf 를 의미합니다.

||Value|
|-|----|
|기본값|	?/conf|

|PID_PATH 값|	PID 파일 위치 경로|
|-|----|
|지정되지 않습니다|	$MACHBASE_HOME/conf/machbase.pid|
|?/test|	$MACHBASE_HOME/test/machbase.pid|
|/tmp|	/tmp/machbase.pid|

## PORT_NO

마크베이스 서버 프로세스가 클라이언트와 통신하기 위한 TCP/IP 포트를 지정합니다. 기본값은 5656입니다.

||Value|
|-|----|
|최소값|	1024|
|최대값|	65535|
|기본값|	5656|

## PROCESS_MAX_SIZE

마크베이스 서버 프로세스인 machbased 프로그램이 사용하는 최대 메모리 사이즈를 지정합니다. 이 제한값 이상의 메모리를 사용하려고 하면 서버는 다음과 같이 동작하여 메모리의 사용량을 줄이려고 시도합니다. 메모리 제한을 초과한 경우, 다음의 방법으로 메모리 사용량을 줄인다.

데이터 입력을 중지하거나 오류로 처리
인덱스 생성 속도를 떨어뜨림
이 경우, 성능이 매우 저하되므로, 메모리 과다 사용 원인을 찾아서 해결하여야 합니다.

||Value|
|-|----|
|최소값|	32 * 1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	8 * 1024 * 1024 * 1024|

## PVO_CACHE_ENABLE

글로벌 PVO Statement Cache 사용 여부를 설정합니다. Standard 에디션에서만 동작합니다.

||Value|
|-|----|
|최소값|	0 (비활성)|
|최대값|	1 (활성)|
|기본값|	1|

## PVO_CACHE_SHARD_COUNT

PVO Statement Cache의 샤드 수를 설정합니다. 초기화 시점에만 적용되므로 변경 시 서버 재시작이 필요하며 런타임 변경은 불가능하다.

||Value|
|-|----|
|최소값|	1|
|최대값|	256|
|기본값|	16|

## PVO_CACHE_MAX_MEMORY_SIZE

PVO Statement Cache 전체가 사용할 최대 메모리 크기(바이트)를 설정합니다. 설정된 값은 샤드 수에 따라 균등 분배되어 적용됩니다. 런타임 변경이 가능하다.

||Value|
|-|----|
|최소값|	32768|
|최대값|	2^64 - 1|
|기본값|	268435456|

## PVO_CACHE_MAX_PLANS_PER_SQL

하나의 SQL에 대해 보관할 수 있는 최대 플랜(핸들) 수를 설정합니다. 런타임 변경이 가능하다.

||Value|
|-|----|
|최소값|	1|
|최대값|	512|
|기본값|	512|

## PVO_CACHE_MAX_SQL_ENTRIES

PVO Statement Cache에 보관할 수 있는 SQL 엔트리의 최대 개수를 설정합니다. 0은 무제한을 의미합니다. 런타임 변경이 가능하며, 샤드 수에 따라 분배되어 적용됩니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	0|

## QUERY_PARALLEL_FACTOR

병렬 질의 실행기의 실행 스레드의 수를 지정합니다. Standard 빌드의 기본값은 0이고, Cluster 빌드의 기본값은 4입니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	100|
|기본값|	0|

## ROLLUP_FETCH_COUNT_LIMIT

롤업 스레드가 한번에 패치해올 데이터양을 제한합니다.

0으로 설정할 경우 제한이 없습니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	3000000|

## RS_CACHE_APPROXIMATE_RESULT_ENABLE

결과값 캐쉬의 추측 모드(approximate result mode)를 사용할지의 여부를 결정합니다. 이 값이 1이면 결과값 캐쉬를 사용할 때, 추측 값을 얻고(매우 빠르지만 데이터가 부정확할 수 있습니다.) 0 이면 정확한 값을 얻는다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	0 (False)|

## RS_CACHE_ENABLE

결과값 캐쉬를 사용할 지의 여부를 결정합니다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	1 (True)|

## RS_CACHE_MAX_MEMORY_PER_QUERY

결과값 캐쉬가 사용할 메모리의 양을 설정합니다. 특정 질의 결과의 메모리 사용량이 이 값을 초과하면, 해당 질의의 결과는 결과값 캐쉬에 저장되지 않는다.

||Value|
|-|----|
|최소값|	1024|
|최대값|	2^64 - 1|
|기본값|	16 * 1024 * 1024|

## RS_CACHE_MAX_MEMORY_SIZE

결과값 캐쉬의 최대 메모리 사용량을 지정합니다.

||Value|
|-|----|
|최소값|	32 * 1024|
|최대값|	2^64 - 1|
|기본값|	512 * 1024 * 1024|

## RS_CACHE_MAX_RECORD_PER_QUERY

결과값 캐쉬에 저장되는 최대 레코드 갯수입니다. 만약 질의의 결과 레코드의 수가 이 값 이상이면 해당 질의 결과값은 캐쉬에 저장하지 않는다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^64 - 1|
|기본값|	10000|

## RS_CACHE_TIME_BOUND_MSEC

특정 질의가 매우 빠르게 실행된 경우에는 그 결과값을 결과값 캐쉬에 저장하지 않는 것이 메모리 사용량을 줄일 수 있으므로 캐쉬에 저장하지 않는것이 좋다.

이 값은 어느 정도 빨리 실행된 질의를 캐쉬에 저장하지 않을지를 결정합니다. 0으로 설정된 경우에는 모든 질의결과를 결과집합캐쉬에 저장합니다.

||Value|
|-|----|
|최소값|	0 (msec)|
|최대값|	2^64 - 1 (msec)|
|기본값|	1000 (msec)|

## SHOW_HIDDEN_COLS

_ARRIVAL_TIME 컬럼은 기본 설정으로는 SELECT * FROM 질의에 의해서 표시되지 않는다. 그러나 이 값이 1로 설정된 경우에는 해당 컬럼을 표시합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## TABLE_SCAN_DIRECTION

태그 테이블의 스캔 방향을 설정할 수 있습니다. 프로퍼티 값은 -1,0, 1중 택일이며 기본값은 0입니다.


* -1 : 역방향 스캔
* 0  : Tag Table(정방향 스캔), Log Table(역방향 스캔)
* 1  : 정방향 스캔

||Value|
|-|----|
|최소값|	-1|
|최대값|	1|
|기본값|	0|

## TAG_CACHE_ENABLE

TAG(키-값) 테이블 캐시 사용 범위를 비트 OR로 지정합니다.

* 0: 캐시 사용 안 함
* 1: TAG map 캐시
* 2: 실제 row 데이터 캐시
* 4: data file 캐시
* 8: 외부 VARCHAR file 캐시
* 16: delete vector 캐시

||Value|
|--|----|
|최소값|	0|
|최대값|	31|
|기본값|	31|

## TAG_CACHE_MAX_MEMORY_SIZE

TAG 캐시 풀 1개당 최대 메모리(바이트)를 지정합니다. 전체 캐시 한도는 `TAG_CACHE_MAX_MEMORY_SIZE * TAG_CACHE_POOL_COUNT` 로 계산됩니다.

||Value|
|--|----|
|최소값|	32 * 1024|
|최대값|	2^64 - 1|
|기본값|	512 * 1024 * 1024|

## TAG_CACHE_POOL_COUNT

TAG 캐시 풀의 개수를 지정합니다.

||Value|
|--|----|
|최소값|	1|
|최대값|	128|
|기본값|	1|

## TAG_MEMORY_INDEX_TYPE

메모리 인덱스 유형을 지정합니다.

* 0: RBTree
* 1: BTree

||Value|
|--|----|
|최소값|	0|
|최대값|	1|
|기본값|	1|

## TAG_MEMORY_INDEX_PANOUT

B-Tree 메모리 인덱스의 차수(order, fanout)를 지정합니다. `TAG_MEMORY_INDEX_TYPE=1`일 때 적용됩니다.

||Value|
|--|----|
|최소값|	127|
|최대값|	65536|
|기본값|	255|

## TAGDATA_AUTO_META_INSERT
{{< callout type="info" >}}
5.5 에서는 TAGDATA_AUTO_NAME_INSERT 입니다. 값의 범위도 0/1 입니다.
5.7 이하에서는 기본값이 1 입니다.
{{< /callout >}}

TAGDATA 테이블에 APPEND/INSERT 를 통해 데이터를 입력할 때, 일치하는 TAG_NAME 이 없을 경우 어떻게 처리할 것인지를 정합니다.

* 0 : 입력이 실패합니다.
* 1 : 입력을 원하는 TAG_NAME 값을 입력합니다. 추가 메타데이터 컬럼이 존재할 경우, 해당 컬럼의 값은 모두 NULL 로 입력됩니다.
* 2 : 입력을 원하는 TAG_NAME 값과 함께, 추가 메타데이터 컬럼 값도 같이 입력합니다.
APPEND 에서만 유효한 설정이며, INSERT 는 추가 메타데이터 컬럼 값을 입력할 수 없기 때문에 1과 같이 작동합니다.
이 설정을 한 이후에는, APPEND 에서 반드시 메타데이터 컬럼 값까지 포함시킨 APPEND Parameter 로 입력해야 합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2|
|기본값|	2|

## TAG_TABLE_META_MAX_SIZE

TAGDATA Table 생성 시 Metadata 영역을 보관할 메모리의 최대 크기를 설정합니다.

||Value|
|-|----|
|최소값|	1024*1024|
|최대값|	2^32-1|
|기본값|	524288000|

## TAG_PARTITION_COUNT

Tag 테이블을 구성하는 Key Value 테이블의 개수를 지정합니다.

||Value|
|--|--|
|최소값| 1|
|최대값| 1024|
|기본값| 4 |

## TAG_DATA_PART_SIZE

Tag 데이터 저장공간의 파티션 크기를 결정합니다.

||Value|
|--|--|
|최소값| 1048576 (1MB)|
|최대값| 1073741824 (1GB)|
|기본값| 16777216 (16MB) |

## TRACE_LOGFILE_COUNT

TRACE_LOGFILE_PATH에 생성되는 로그 트레이스 파일의 최대 수를 지정합니다. 디스크 공간을 절약하기 위해서, 최대 개수 이상의 로그파일이 생성되면 가장 오래된 로그파일을 삭제합니다.

로그 트레이스 파일의 최대 개수 이상의 로그파일이 생성되어 가장 오래된 파일이 삭제될 경우 삭제된 파일의 이름이 가장 최신의 로그파일로 저장이 됩니다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	1000|

## TRACE_LOGFILE_PATH

로그 트레이스 파일들(machbase.trc, machadmin.trc, machsql.trc)의 경로를 설정합니다.
이 파일들은 마크베이스의 시작, 종료, 실행시 내부 정보를 지속적으로 기록합니다. 기본값인 ?/trc의 의미는 $MACHBASE_HOME/trc 를 의미합니다.

||Value|
|-|----|
|기본값|	?/trc|

|TRACE_LOGFILE_PATH 값|	trc 디렉터리 위치|
|-|----|
|지정되지 않습니다|	$MACHBASE_HOME/trc/|
|?/test|	$MACHBASE_HOME/test/|
|/tmp|	/tmp/|

## TRACE_LOGFILE_SIZE

로그 트레이스 파일의 최대 크기를 설정합니다. 만약 크기 이상의 데이터를 기록하여야 한다면, 신규로 log 파일을 생성할 것입니다.


||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^32 - 1|
|기본값|	10 * 1024 * 1024|

## TRACE_LOG_LEVEL

트레이스 로그의 상세 수준을 설정합니다. 값이 높을수록 더 상세한 로그를 기록합니다.

||Value|
|-|----|
|최소값| 0|
|최대값| 2^32 - 1|
|기본값| 277|

## UNIX_PATH

Unix domain socket 이름을 설정합니다.

||Value|
|-|----|
|기본값|	machbase-unix|

## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE

시스템의 모든 volatile, lookup 테이블의 메모리 사용량 총계의 한도를 설정합니다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	2 * 1024 * 1024 * 1024|

## property-cl


[Property](/dbms/reference/configuration/#property)와 별개로, Cluster Edition 에서만 사용 가능한 Property 를 정리합니다.

# 목차
- [목차](#목차)
  - [CLUSTER_LINK_ACCEPT_TIMEOUT](#cluster_link_accept_timeout)
  - [CLUSTER_LINK_BUFFER_SIZE](#cluster_link_buffer_size)
  - [CLUSTER_LINK_CHECK_INTERVAL](#cluster_link_check_interval)
  - [CLUSTER_LINK_CONNECT_RETRY_TIMEOUT](#cluster_link_connect_retry_timeout)
  - [CLUSTER_LINK_CONNECT_TIMEOUT](#cluster_link_connect_timeout)
  - [CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST](#cluster_link_error_add_origin_host)
  - [CLUSTER_LINK_HANDSHAKE_TIMEOUT](#cluster_link_handshake_timeout)
  - [CLUSTER_LINK_HOST](#cluster_link_host)
  - [CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL](#cluster_link_long_term_callback_interval)
  - [CLUSTER_LINK_LONG_WAIT_INTERVAL](#cluster_link_long_wait_interval)
  - [CLUSTER_LINK_MAX_LISTEN](#cluster_link_max_listen)
  - [CLUSTER_LINK_MAX_POLL](#cluster_link_max_poll)
  - [CLUSTER_LINK_PORT_NO](#cluster_link_port_no)
  - [CLUSTER_LINK_RECEIVE_TIMEOUT](#cluster_link_receive_timeout)
  - [CLUSTER_LINK_REQUEST_TIMEOUT](#cluster_link_request_timeout)
  - [CLUSTER_LINK_SEND_RETRY_COUNT](#cluster_link_send_retry_count)
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

특정 Node와 연결할 때, Accept 후 Handshake 메시지를 수신할 때까지의 Timeout.

Timeout 이후까지 수신에 실패하면, 해당 연결은 실패합니다.

기본값은 5초.

|(usec)|	Value|
|------|---------|
|최소값|    0|
|최대값|	2^64 - 1|
|기본값|	5000000|

## CLUSTER_LINK_BUFFER_SIZE

송신/수신 버퍼의 크기를 의미합니다.

이 크기가 모자라면 송신시 버퍼가 비워질 때 까지 재시도하게 됩니다.

|(byte)|	Value|
|------|---------|
|최소값|	1024768|
|최대값|	2^32 - 1|
|기본값|	33554432 (32M)|

## CLUSTER_LINK_CHECK_INTERVAL

특정 Node와 연결된 Socket들을 검사하는, Timeout Thread의 검사 주기.

RECEIVE_TIMEOUT, SESSION_TIMEOUT 을 검사하는 Timeout Thread가 존재합니다.
주기를 짧게 할 수록, 자주 검사하지만 Timeout 판단은 아래의 값에 따라 이루어진다.

기본값은 1초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## CLUSTER_LINK_CONNECT_RETRY_TIMEOUT

특정 Node와 연결이 실패한 이후, 재연결 시도를 반복하는 Timeout

Timeout 이후까지 재연결되지 않는다면, 완전히 단절되었다고 판단합니다.

기본값은 1분.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	60000000|

## CLUSTER_LINK_CONNECT_TIMEOUT

특정 Node와 연결을 시도할 때, 기다리는 시간.

Timeout 이후까지 연결되지 않는다면, CLUSTER_LINK_CONNECT_RETRY_TIMEOUT 이 지나기 전 까지 재연결을 시도합니다.

기본값은 5초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	5000000|

## CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST

Cluster 간 통신 중 발생하는 에러 메시지에, 오류가 발생한 호스트 이름을 추가할지 여부를 선택할 수 있습니다.

자세한 에러 메시지를 표시하고자 한다면, 해당 Property를 켜야 합니다.

기본값은 1이며, 호스트 이름이 출력됩니다.

|(boolean)|	Value|
|------|---------|
|최소값|	0|
|최대값|	1|
|기본값|	1|

## CLUSTER_LINK_HANDSHAKE_TIMEOUT

특정 Node와 Cluster Socket으로 연결된 상태에서, Handshake 메시지를 수신할 때까지의 Timeout

연결이 막 완료된 두 Node는, 연결 상태를 점검하는 차원에서 작은 크기의 Handshake 메시지를 주고 받는다.
Accept한 Node가 Handshake 메시지를 먼저 보내는데, 그 응답을 기다리는 시간을 여기서 설정합니다.

기본값은 5초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	5000000|

## CLUSTER_LINK_HOST

특정 Node와 Cluster Socket 을 연결하기 위한, 현재 Node의 호스트 이름

|(string)|	Value|
|--|--|
|기본값|	localhost|

## CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL

Cluster Socket 으로 수신 되는 메시지를 처리할 Receive Callback 이 수행한 시간을 Long-Term Callback 으로 인식할 시간

수신 Thread의 개수가 제한적이므로, 가급적이면 Receive Callback은 오랜 시간 동안 메시지를 처리하고 있으면 안 됩니다.
이 시간이 지나도록 Receive Callback이 메시지를 처리하고 있다면, Long-Term Callback 으로 인식하고 Trace Log에 그 기록을 남긴다.

기본값은 1초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## CLUSTER_LINK_LONG_WAIT_INTERVAL

Cluster Socket 으로 수신 되는 메시지가 도착할 때 까지의 시간을 Long-Wait Message 로 인식할 시간

수신 시작~수신 종료 까지의 시간이 길면 네트워크 환경의 문제로 볼 수 있습니다.
이 시간이 지나도록 수신 메시지가 도착하지 않는다면, Long-Wait Message 로 인식하고 Trace Log에 그 기록을 남긴다.

기본값은 1초.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## CLUSTER_LINK_MAX_LISTEN

특정 Node와 연결할 때, Socket의 Accept Queue 의 최대 숫자

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	2^31 - 1|
|기본값|	512|

## CLUSTER_LINK_MAX_POLL

특정 Node와 통신할 때, Poll에 의헤서 한번에 조회할 수 있는 최대 Event 수

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	2^31 - 1|
|기본값|	4096|

## CLUSTER_LINK_PORT_NO

특정 Node와 Cluster Socket 을 연결하기 위한, 현재 Node의 포트 번호

|(port)|	Value|
|------|---------|
|최소값|    1024|
|최대값|	65535|
|기본값|	3868|

## CLUSTER_LINK_RECEIVE_TIMEOUT

Timeout Thread가, 마지막 수신 이후로 연결이 끊긴 것을 판단할 때 까지의 Timeout

Cluster Node 간 연결은, 수신이 완료되면 종료되기 때문에 '연결 리스트' 에 존재하는 연결들은 지속적으로 수신을 받고 있어야 합니다.
이 시간이 지나도록 마지막 수신 시각이 갱신되지 않으면, Timeout Thread는 Trace Log에 기록을 남기고 해당 Socket을 닫는다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## CLUSTER_LINK_REQUEST_TIMEOUT

Cluster Socket에서 요청 메시지를 보냈을 때, 요청에 대한 응답이 올 때 까지의 Timeout

특정 메시지의 경우 Request 이후 Answer 전송까지 대기할 수 있는 시간을 따로 지정합니다.
이 시간이 지나도록 응답 메시지가 도착하지 않으면, Trace Log에 기록을 남기고 해당 Socket을 닫는다.

기본값은 60초. 메시지 종류와 수신 처리가 어떻게 될지 모르므로, Timeout이 길다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	60000000|

## CLUSTER_LINK_SEND_RETRY_COUNT

* 5.6 부터 사용 가능합니다.

재시도를 할 때 마다 1ms 씩 쉬게 됩니다. 이 회수를 넘어서서 재시도하게 될 경우 연결을 해제하게 됩니다.송신 버퍼가 비워질 때 까지 송신을 재시도하는 회수.

기본값은 5000.

|(count)|   Value|
|------|---------|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	5000|

## CLUSTER_LINK_SEND_TIMEOUT

Cluster Socket을 통해 메시지를 송신할 때 설정하는 Timeout

송신할 때 해당 Timeout 을 설정하며,
Timeout 까지 송신이 완료되지 않으면 Trace Log에 그 기록을 남긴다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## CLUSTER_LINK_SESSION_TIMEOUT

Timeout Thread가, 특정 세션에서 마지막 수신 이후로 연결이 끊긴 것을 판단할 때 까지의 Timeout

Cluster 연결은, 내부적으로 모든 메시지의 세션을 관리하고 있습니다. 갑자기 세션 정리를 하지 못하게 된 상황에서 필요한 Property 입니다.
이 시간이 지나도록 해당 세션에 대한 마지막 수신 시각이 갱신되지 않으면, Timeout Thread는 Trace Log에 기록을 남기고 해당 세션을 닫는다.

기본값은 1시간.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3600000000|

## CLUSTER_LINK_THREAD_COUNT

특정 Node와 통신할 때, 수신된 메시지를 처리할 Thread의 수

Cluster의 규모가 커지거나, 처리해야 할 연산의 개수가 많아져서 수신 가능한 Thread 가 여유가 없을 때 늘릴 수 있습니다.

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	4096|
|기본값|	16|

## CLUSTER_QUERY_STAT_LOG_ENABLE

수행한 질의에 대한 통계정보를 trace log에 출력합니다.

|(boolean)|	Value|
|------|---------|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## CLUSTER_REPLICATION_BLOCK_SIZE

Cluster Edition 에서, Node 추가로 Replication 을 진행할 때, 한번에 실어 보내는 데이터 크기.

Replication Active 가 되는 Warehouse (=전송을 하는 Warehouse) 에 직접 Property 를 적용해야 합니다.

기본값은 640KB 입니다.

|(size)|	Value|
|------|---------|
|최소값|	64 * 1024|
|최대값|    100 * 1024 * 1024|
|기본값|	640 * 1024 (655360)|


## CLUSTER_WAREHOUSE_DIRECT_DML_ENABLE

Cluster Edition 에서, Warehouse 에 곧바로 접속해 DML 을 수행할 수 있도록 합니다.

* 1 : 수행 가능
* 0 : 수행 불가능. 에러가 반환됩니다.

Warehouse 에 직접 DML 을 수행할 경우 Broker 를 통한 것보다 성능 이점이 있지만, 동일 Group 에 DML 이 전파되지 않는 문제가 있습니다.
따라서, 데이터 불일치로 인한 비상 복구용 혹은 Group 의 데이터 불일치를 감안해도 되는 경우에 한해 사용합니다.

원하는 특정 Warehouse 에 직접 Property 를 적용해야 합니다.

기본값은 0입니다.

{{< callout type="info" >}}
해당 Property 를 켠 채로 Group 내 Warehouse 간의 데이터 차이가 발생하더라도, Coordinator 는 데이터 불일치 여부를 별도로 검사하지 않는다.
{{< /callout >}}

|(boolean)|	Value|
|------|---------|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## COORDINATOR_DBS_PATH

Coordinator 의 데이터 파일이 생성될 디렉터리를 지정합니다.

기본값은 ?/dbs 로 설정되어 있으며, ? 는 $MACHBASE_COORDINATOR_HOME 환경변수로 치환됩니다.
이는 환경변수 $MACHBASE_COORDINATOR_HOME/dbs 디렉터리라는 의미입니다.

Coordinator 에 적용해야 하며, 다른 Node 에는 아무런 효과가 없습니다.

|(path)|	Value|
|------|---------|
|기본값|	?/dbs|


## COORDINATOR_DDL_REQUEST_TIMEOUT

Coordinator가 Node에게 DDL 수행을 요청한 후 대기할 때 까지의 Timeout

이 값은 Coordinator가 각 Node에게 DDL 수행을 요청한 후 대기할 때 까지를 말합니다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	300000000|

## COORDINATOR_DDL_TIMEOUT

Broker가 Coordinator에게 DDL 수행을 요청한 후 대기할 때 까지의 Timeout

이 값은 Broker가 Cluster 전체에 대한 DDL 수행을 Coordinator에게 요청한 후 대기할 때 까지를 의미합니다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	300000000|

## COORDINATOR_DECISION_DELAY

Coordinator가 상태 변경을 요청하고 실제로 반영할 때 까지의 Timeout.

이 시간이 지나도록 실제로 상태가 변경되지 않는 경우, Cluster 상태를 비활성화시킨다.
만약 Warehouse Active의 상태가 변경되지 않았는데 연결된 Standby가 존재하는 경우, Fail-Over 작업을 시작합니다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_DECISION_INTERVAL

Coordinator가 상태 변경을 얼마나 자주 할지 결정할 시간.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_HOST_RESOURCE_ENABLE

Coordinator가 Cluster Node들의 Host Resource 수집 여부

|(boolean)|	Value|
|------|---------|
|최소값|	0(false)|
|최대값|	1(true)|
|기본값|	0(false)|

## COORDINATOR_HOST_RESOURCE_COLLECT_INTERVAL

Cluster Node들이 Host Resource를 수집하는 주기

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_HOST_RESOURCE_INTERVAL

Coordinator가 Node들과 Host Resource를 주고받는 주기

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_HOST_RESOURCE_REQUEST_TIMEOUT

Coordinator가 Node들에게 Host Resource 정보를 요청한 이후 대기할 시간

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	10000000|

## COORDINATOR_NODE_REQUEST_TIMEOUT

Coordinator가 Node에게 명령을 수행하도록 요청한 후 대기할 때 까지의 Timeout

Add/Remove-node, Add/Remove-Package 등의 Node 명령 수행이 포함되어 있어, 짧은 시간으로 잡을 경우 해당 명령 처리가 완료되지 못할 수 있습니다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	600000000|

## COORDINATOR_NODE_TIMEOUT

Coordinator가 Node의 장애를 판단하기 까지 기다릴 시간.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## COORDINATOR_STARTUP_DELAY

Coordinator 시작 직후 Decision Thread를 작동시킬 때 까지의 유예 시간.

Cluster 전체 구동에 오랜 시간이 소요되는 경우, 해당 값을 크게 설정해서 Coordinator의 Node 제어를 더욱 늦게 시작할 수 있습니다.
전체 구동도 하기 전에 Decision Thread가 작동하는 경우, Coordinator가 오판할 가능성이 높아진다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3000000|

## COORDINATOR_STATUS_NODE_INTERVAL

Coordinator가 Node들과 상태 조회 메시지를 주고 받을 주기

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1000000|

## COORDINATOR_STATUS_NODE_REQUEST_TIMEOUT

Coordinator가 Node들에게 상태 조회 요청을 한 이후 대기할 시간.

해당 시간동안 상태 조회 응답이 없으면, Coordinator는 해당 Node의 상태를 갱신하지 않고 계속 진행합니다.
네트워크 상황이 좋지 않은데 상태 갱신을 반드시 해야 하는 경우엔, 값을 늘리는 것을 고려해 볼 수 있습니다.
대신, 상태 조회 응답이 없을 경우엔 값을 늘린 만큼 Coordinator에서 반드시 기다리게 됩니다.

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	15000000|

## COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO

Cluster 로 구성중인 일부 서버의 디스크 사용량이 프로퍼티 값을 넘어가면 해당 host 가 속한 group 이 DISKFULL 상태로 전환됩니다.
DISKFULL 상태의 group 에 대해서는 입력이 제한되고 조회 및 삭제만 가능하다.

프로퍼티 값이 0 인 경우 해당 기능이 disable 됩니다.

|(percent)|	Value|
|------|---------|
|최소값|	0|
|최대값|	99|
|기본값|	0|

## COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO

DISKFULL 상태로 동작중인 서버의  디스크 사용량이 프로퍼티 값 이하로 떨어질 경우 해당 group 이 normal 상태로 전환됩니다.

프로퍼티 값이 0 인 경우 해당 기능이 disable 됩니다.

|(percent)|	Value|
|------|---------|
|최소값|	0|
|최대값|    99|
|기본값|	0|

## DEPLOYER_DBS_PATH

Deployer 의 데이터 파일이 생성될 디렉터리를 지정합니다.

기본값은 ?/dbs 로 설정되어 있으며, ? 는 $MACHBASE_DEPLOYER_HOME 환경변수로 치환됩니다.
이는 환경변수 $MACHBASE_DEPLOYER_HOME /dbs 디렉터리라는 의미입니다.

Deployer 에 적용해야 하며, 다른 Node 에는 아무런 효과가 없습니다.

|(path)|	Value|
|------|---------|
|기본값|	?/dbs|

## EXECUTION_STAGE_MEMORY_MAX

Cluster Edition 에서, SELECT 쿼리를 수행하는 Stage Thread 가 사용하는 Memory 의 최대 크기.

각 Stage 의 최대 크기이므로, Stage 개수가 늘어나는 복잡한 SELECT 쿼리의 경우 요구 메모리가 더 커질 수 있습니다.
최대 크기를 넘는 Stage 가 존재하는 경우, 해당 Stage 는 취소되고 Query 역시 에러와 함께 취소됩니다.

원하는 특정 Warehouse 에 직접 Property 를 적용해야 합니다.

기본값은 1GB 입니다.

|(size)|    Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	1024 *1024 * 1024|

## HTTP_ADMIN_PORT

MWA 또는 machcoordinatoradmin 으로부터 요청을 받을 port number

|(port)|    Value|
|------|---------|
|최소값|	1024|
|최대값|	65535|
|기본값|	5779|

## HTTP_CONNECT_TIMEOUT

machcoordinatoradmin 과 연결할 때 사용하는 timeout

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	30000000|

## HTTP_RECEIVE_TIMEOUT

machcoordinatoradmin 과 통신할 때 사용하는 timeout

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	3600000000|

## HTTP_SEND_TIMEOUT

machcoordinatoradmin 과 통신할 때 사용하는 timeout

|(usec)|	Value|
|------|---------|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	60000000|

## INSERT_BULK_DATA_MAX_SIZE

Append 또는 INSERT-SELECT 수행 시 입력 data block의 최대 크기

|(size)|	Value|
|------|---------|
|최소값|	1024|
|최대값|	10 * 1024 * 1024|
|기본값|	1024 * 1024|

## INSERT_RECORD_COUNT_PER_NODE

입력 수행시 warehouse group 전환을 유도하는 data 입력 개수.

|(count)|	Value|
|------|---------|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	1000|

## LOOKUPNODE_COMMAND_RETRY_MAX_COUNT

Lookup 노드에 명령 및 접속 실패시 재시도 횟수

|(count)|   Value|
|------|---------|
|최소값|	1|
|최대값|	3600|
|기본값|	30|

## STAGE_RESULT_BLOCK_SIZE

하나의 stage 에서 만드는 최대 block 크기

|(size)|    Value|
|------|---------|
|최소값|	1024|
|최대값|	2^32 - 1|
|기본값|	1024 * 1024|

## meta-table


## 목차

- [목차](#목차)
- [사용자 객체](#사용자-객체)
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
- [기타](#기타)
  - [M$TABLES](#mtables)
  - [M$COLUMNS](#mcolumns)


메타 테이블은 Machbase의 스키마 정보를 표현하는 테이블입니다. 테이블 이름은 "M$"로 시작합니다.

이 테이블들은 테이블 이름, 컬럼 정보, 인덱스 정보를 보유하며, DDL 문으로 인한 생성, 수정 및 삭제 정보를 반영합니다.
메타 테이블은 사용자가 추가, 삭제 또는 변경할 수 없습니다.


## 사용자 객체

### M$SYS_TABLES
---

사용자가 생성한 테이블을 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|테이블 이름|
|TYPE|테이블 타입<br> - 0: Log<br> - 1: Fixed<br> - 3: Volatile<br> - 4: Lookup<br> - 5: Key Value<br> - 6: Tag|
|DATABASE_ID|데이터베이스 식별자|
|ID|테이블 식별자|
|USER_ID|테이블 생성 사용자|
|COLCOUNT|컬럼 수|
|FLAG|테이블 타입 분류<br> - 1 : Tag Data Table<br> - 2 : Rollup Table<br> - 4 : Tag Meta Table<br> - 8 : Tag Stat Table|

### M$SYS_TABLE_PROPERTY
---

각 테이블에 적용된 테이블 속성 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|ID|테이블 식별자|
|NAME|속성 이름|
|VALUE|속성 값|


### M$SYS_COLUMNS
---

M$SYS_TABLES에 표시된 사용자 테이블의 컬럼 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|컬럼명|
|TYPE|컬럼 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|컬럼 식별자|
|LENGTH|컬럼 길이|
|TABLE_ID|컬럼의 테이블 식별자|
|FLAG|(서버 내부 사용 정보)|
|PART_PAGE_COUNT|파티션당 페이지 수|
|PAGE_VALUE_COUNT|페이지당 데이터 수|
|MINMAX_CACHE_SIZE|MIN-MAX 캐시 크기|
|MAX_CACHE_PART_COUNT|최대 파티션 캐시 수|
|NEXTVAL|시퀀스 메타데이터를 사용하는 컬럼의 다음 시퀀스 값|


### M$SYS_INDEXES
---

사용자가 생성한 인덱스 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|인덱스 이름|
|TYPE|인덱스 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|인덱스 식별자|
|TABLE_ID|인덱스의 테이블 식별자|
|COLCOUNT|생성된 인덱스의 컬럼 수|
|PART_VALUE_COUNT|인덱스 테이블 파티션당 데이터 수|
|KEY_COMPRESS|키 값 압축 상태|
|MAX_LEVEL|인덱스 최대 레벨 (LSM만)|
|PAGE_SIZE|페이지 크기|
|MAX_KEYWORD_SIZE|최대 키워드 길이 (keyword만)|
|BITMAP_ENCODE|비트맵 인코딩 타입 (RANGE / EQUAL)|


### M$SYS_INDEX_COLUMNS
---

M$SYS_INDEXES에 표시된 사용자 인덱스의 컬럼 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|INDEX_ID|인덱스 식별자|
|INDEX_TYPE|인덱스 타입|
|NAME|컬럼명|
|COL_ID|컬럼 식별자|
|DATABASE_ID|데이터베이스 식별자|
|TABLE_ID|테이블 식별자|
|TYPE|컬럼의 데이터 타입|


### M$SYS_TABLESPACES
---

사용자가 생성한 테이블스페이스 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|테이블스페이스 이름|
|ID|테이블스페이스 식별자|
|DISK_COUNT|테이블스페이스의 디스크 수|


### M$SYS_TABLESPACE_DISKS
---

테이블스페이스가 사용하는 디스크 정보를 유지합니다.

|컬럼명|설명|
|--|--|
|NAME|디스크 이름|
|ID|디스크 식별자|
|TABLESPACE_ID|디스크의 테이블스페이스 식별자|
|PATH|디스크 경로|
|IO_THREAD_COUNT|이 디스크에 할당된 I/O 스레드 수|
|VIRTUAL_DISK_COUNT|이 디스크에 할당된 가상 디스크 단위 수|


### M$SYS_USERS
---

Machbase에 등록된 사용자 정보를 유지합니다.

|컬럼명|설명|
|--|--|
|USER_ID|사용자 식별자|
|NAME|사용자 이름|
|PWD_POLICY_LEVEL|패스워드 정책 레벨|
|VALID_BEFORE|패스워드 유효 종료일|

### M$SYS_VIEWS
---

뷰 정의 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|USER_NAME|소유자 사용자 이름|
|DB_NAME|데이터베이스 이름|
|VIEW_NAME|뷰 이름|
|VIEW_SQL|뷰 정의 SQL 텍스트|

### M$SYS_USER_ACCESS
---

테이블에 부여된 사용자 권한 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|USER_NAME|사용자 이름|
|TABLE_NAME|테이블 이름|
|PRIV|권한 이름|

### M$RETENTION
---

RETENTION POLICY 정보를 표시합니다.

|컬럼명|설명|
|-------------|----------------|
| USER_ID     | 사용자 ID      |
| POLICY_NAME | 정책 이름    |
| DURATION    | 보존 기간(초) |
| INTERVAL    | 업데이트 주기(초) |

## 기타

### M$TABLES
---

M$로 시작하는 모든 메타 테이블을 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|메타 테이블 이름|
|TYPE|테이블 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|메타 테이블 식별자|
|USER_ID|테이블 사용자 (이 경우 SYS)|
|COLCOUNT|컬럼 수|


### M$COLUMNS
---

M$TABLES에 표시된 메타 테이블의 컬럼 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|컬럼명|
|TYPE|컬럼 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|컬럼 식별자|
|LENGTH|컬럼 길이|
|TABLE_ID|컬럼의 테이블 식별자|
|FLAG|(서버 내부 사용 정보)|
|PART_PAGE_COUNT|파티션당 페이지 수|
|PAGE_VALUE_COUNT|페이지당 데이터 수|
|MINMAX_CACHE_SIZE|MIN-MAX 캐시 크기|
|MAX_CACHE_PART_COUNT|최대 파티션 캐시 수|

## timezone


## 목차

* [Machbase의 Timezone](#machbase의-timezone)
* [Machbase의 Timezone 형식](#machbase의-timezone-형식)
    * [machsql](#machsql)
    * [machloader](#machloader)
    * [SDK](#sdk)
    * [REST API](#rest-api)

## Machbase의 Timezone

Machbase는 각 클라이언트의 Timezone이 각 세션에서만 유효하다고 가정합니다.

일반적으로 타임존은 특정 시간을 나타내는 문자열로 지정됩니다.

```
"YYYY-MM-DD HH24:MI:SS ZZZ(Timezone String)"

예제)
"12:06:56.568+01:00"
"2006.07.10 at 15:08:56 -05:00"
"09  AM, GMT+09:00"
```

그러나 위의 방법은 매번 타임존을 기준으로 특정 시간을 지정해야 하는 불편함이 있을 뿐만 아니라, 대량의 데이터에 대해 타임존 값을 포함하면 데이터 전송량이 선형적으로 증가하는 문제가 있습니다.

따라서 Machbase는 클라이언트와 서버가 연결된 세션에 대해 타임존 속성을 지정하는 방법을 지원합니다.

다음은 Machbase가 제공하는 타임존 동작에 대한 단계별 설명입니다.

* 서버는 서버가 설치된 운영 체제에서 제공하는 기본 타임존을 기준으로 작동합니다.<br>
    즉, 설정을 하지 않으면 Machbase는 OS가 작동하는 타임존을 읽어서 사용합니다.

* 클라이언트 프로그램이 타임존을 설정하지 않고 서버에 연결하면, 클라이언트의 타임존은 서버의 타임존으로 설정됩니다.<br>
    즉, 서버에 설정된 TIMEZONE이 KST인 경우, 클라이언트도 KST로 작동한다는 의미입니다.

* 클라이언트 프로그램에서 타임존을 명시적으로 설정하면, 서버의 해당 세션은 클라이언트가 지정한 타임존에서 작동합니다.<br>
    즉, 서버에 설정된 TIMEZONE이 KST이더라도, 클라이언트가 연결할 때 타임존을 EDT로 설정하면 세션은 EDT로 작동합니다.

## Machbase의 Timezone 형식

Machbase는 사용 편의성을 높이고 복잡성을 제거하기 위해 5자로 구성된 하나의 형식만 제공합니다.

즉, 첫 번째 문자는 시간의 부호를 나타내는 + 또는 - 기호이고, 다음 두 문자는 00과 23 사이의 값을 갖습니다. 그리고 마지막 두 문자는 00에서 59까지의 시간을 갖는다고 가정합니다.

다음은 Machbase가 지원하는 TIMEZONE 형식을 보여줍니다.

```
예제)
TIMEZONE=+0900
TIMEZONE=-0900
```

### machsql
---

machsql을 시작할 때 다음 옵션을 통해 작동할 타임존을 설정할 수 있습니다.

```
-z, --timezone=+-HHMM
```

SHOW TIMEZONE 명령을 통해 현재 설정된 타임존을 확인할 수 있습니다.

```
SHOW TIMEZONE;

Mach> show timezone;
Timezone : +0900
```

### machloader
---

machloader를 실행할 때 다음 옵션을 통해 작동할 타임존을 설정할 수 있습니다.

```
-z, --timezone=+-HHMM
```

지정된 타임존으로 연결하며 시간 계산은 해당 타임존을 기준으로 작동합니다.

### SDK
---

연결 문자열에 TIMEZONE이 추가되었으며, 세션에 대한 타임존을 지정할 수 있습니다.

연결 문자열에 TIMEZONE을 지정하지 않으면 서버의 타임존을 기준으로 작동합니다.

이것은 CLI, ODBC, JDBC 및 DOTNET에서 동일합니다.

연결 문자열 예제

```
SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;NLS_USE=UTF8;PORT_NO=5656;TIMEZONE=+0300
```

### REST API
---

Rest API는 작업을 요청할 때 HTTP 프로토콜 HEADER에 지정된 타임존을 기준으로 작동합니다.

헤더 이름은 The-Timezone-Machbase이며, 사용법은 다음과 같습니다.

```
Authorization: Basic XXXXXXXXXXXXXXXXXXX
...................
The-Timezone-Machbase: +0900
...............
```

위에서 설명한 것처럼 원하는 Timezone 문자열을 지정할 수 있습니다.

Timezone이 지정되지 않으면 서버의 Timezone으로 작동합니다.

요청 예제: UTC로 설정

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

결과 JSON의 "timezone" 항목에 설정된 타임존 값이 반환됩니다.

## virtual-table


Virtual Table은 마크베이스 서버의 다양한 운영 정보들을 테이블 형태로 표현하는 가상 테이블입니다. 이 테이블들의 이름은 V$ 문자로 시작합니다.

마크베이스 서버가 어떤 상태로 동작하고 있는지를 알기 위해 이 데이터를 읽어서 저장해 두고 이용할 수 있습니다.
추가로 이 Virtual Table을 다른 테이블들과 JOIN 연산을 통해서 다양한 정보를 얻을 수 있습니다.

Virtual Table은 읽기 전용으로 사용자가 추가하거나 삭제, 갱신할 수 없습니다.

## 목차

* [Session/System](#sessionsystem)
  * [V$PROPERTY](#vproperty)
  * [V$SESSION](#vsession)
  * [V$SESMEM](#vsesmem)
  * [V$SESSTAT](#vsesstat)
  * [V$SESTIME](#vsestime)
* [V$SYSMEM](#vsysmem)
  * [V$SYSSTAT](#vsysstat)
  * [V$SYSTIME](#vsystime)
  * [V$STMT](#vstmt)
  * [V$VERSION](#vversion)
  * [V$HTTP\_STATUS](#vhttp_status)
  * [V$NEO\_SESSION](#vneo_session)
  * [V$NEO\_STMT](#vneo_stmt)
* [Result Cache](#result-cache)
  * [V$RS\_CACHE\_LIST](#vrs_cache_list)
  * [V$RS\_CACHE\_STAT](#vrs_cache_stat)
* [PVO Statement Cache](#pvo-statement-cache)
  * [V$PVO\_CACHE\_STAT](#vpvo_cache_stat)
  * [V$PVO\_CACHE\_LIST](#vpvo_cache_list)
* [Storage](#storage)
  * [V$STORAGE](#vstorage)
  * [V$STORAGE\_MOUNT\_DATABASES](#vstorage_mount_databases)
  * [V$CACHE](#vcache)
  * [V$CACHE\_OBJECTS](#vcache_objects)
  * [V$STORAGE\_DC\_TABLESPACES](#vstorage_dc_tablespaces)
  * [V$STORAGE\_DC\_TABLESPACE\_DISKS](#vstorage_dc_tablespace_disks)
  * [V$STORAGE\_DC\_DWFILES](#vstorage_dc_dwfiles)
  * [V$STORAGE\_DC\_PAGECACHE](#vstorage_dc_pagecache)
  * [V$STORAGE\_DC\_PAGECACHE\_LRU\_LST](#vstorage_dc_pagecache_lru_lst)
  * [V$STORAGE\_USAGE](#vstorage_usage)
  * [V$STORAGE\_TABLES](#vstorage_tables)
* [Log Table](#log-table)
  * [V$STORAGE\_DC\_TABLES](#vstorage_dc_tables)
  * [V$STORAGE\_DC\_TABLES\_STAT](#vstorage_dc_tables_stat)
  * [V$STORAGE\_DC\_TABLE\_COLUMNS](#vstorage_dc_table_columns)
  * [V$STORAGE\_DC\_TABLE\_COLUMN\_PARTS](#vstorage_dc_table_column_parts)
  * [V$STORAGE\_DC\_TABLE\_INDEXES](#vstorage_dc_table_indexes)
* [LSM(Log Structured Merge) Index](#lsmlog-structured-merge-index)
  * [V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS](#vstorage_dc_lsmindex_level_parts)
  * [V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS\_CACHE](#vstorage_dc_lsmindex_level_parts_cache)
  * [V$STORAGE\_DC\_LSMINDEX\_LEVELS](#vstorage_dc_lsmindex_levels)
  * [V$STORAGE\_DC\_LSMINDEX\_FILES](#vstorage_dc_lsmindex_files)
  * [V$STORAGE\_DC\_LSMINDEX\_AGER\_JOBS](#vstorage_dc_lsmindex_ager_jobs)
* [Volatile Table](#volatile-table)
  * [V$STORAGE\_DC\_VOLATILE\_TABLE](#vstorage_dc_volatile_table)
* [Tag Table](#tag-table)
  * [V$STORAGE\_TAG\_TABLES](#vstorage_tag_tables)
  * [V$STORAGE\_TAG\_CACHE](#vstorage_tag_cache)
  * [V$STORAGE\_TAG\_CACHE\_BASE](#vstorage_tag_cache_base)
  * [V$STORAGE\_TAG\_CACHE\_OBJECTS](#vstorage_tag_cache_objects)
  * [V$STORAGE\_TAG\_TABLE\_FILES](#vstorage_tag_table_files)
  * [V$STORAGE\_TAG\_INDEX](#vstorage_tag_index)
* [Tag Rollup](#tag-rollup)
  * [V$ROLLUP](#vrollup)
* [Stream](#stream)
  * [V$STREAMS](#vstreams)
* [License](#license)
  * [V$LICENSE\_INFO](#vlicense_info)
* [Mutex](#mutex)
  * [V$MUTEX](#vmutex)
  * [V$MUTEX\_WAIT\_STAT](#vmutex_wait_stat)
* [Cluster](#cluster)
  * [V$NODE\_STATUS](#vnode_status)
  * [V$DDL\_INFO](#vddl_info)
  * [V$REPLICATION](#vreplication)
  * [V$REPL\_SENDER](#vrepl_sender)
  * [V$REPL\_SENDER\_META](#vrepl_sender_meta)
  * [V$REPL\_RECEIVER](#vrepl_receiver)
  * [V$REPL\_RECEIVER\_META](#vrepl_receiver_meta)
  * [V$REPL\_READER](#vrepl_reader)
  * [V$REPL\_READER\_META](#vrepl_reader_meta)
  * [V$REPL\_WRITER](#vrepl_writer)
  * [V$REPL\_WRITER\_META](#vrepl_writer_meta)
* [Others](#others)
  * [V$TABLES](#vtables)
  * [V$COLUMNS](#vcolumns)
  * [V$RETENTION\_JOB](#vretention_job)
  * [V$USER\_AUTH\_KEYS](#vuser_auth_keys)

## Session/System
### V$PROPERTY
---

서버에 설정된 프로퍼티 정보를 표시합니다.

| 컬럼 이름 | 설명           |
| ----- | ------------ |
| NAME  | 프로퍼티명        |
| VALUE | 프로퍼티 값       |
| TYPE  | 데이터 타입       |
| DEFLT | 기본 값         |
| MIN   | 설정할 수 있는 최소값 |
| MAX   | 설정할 수 있는 최대값 |

### V$SESSION
---

MACHBASE 서버에 접속된 세션 정보를 표시합니다.

| 컬럼 이름                              | 설명                                                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| HOSTNAME (Cluster Only)            | 세션 연결된 HOST 이름                                                                                                                   |
| ID                                 | 세션 식별자                                                                                                                           |
| CLOSED                             | 연결이 닫혀있는지 여부                                                                                                                     |
| USER_ID                            | 사용자 식별자                                                                                                                          |
| LOGIN_TIME                         | 접속 시각                                                                                                                            |
| CLIENT_TYPE                        | 접속 Client 타입                                                                                                                     |
| USER_NAME                          | 사용자 이름                                                                                                                           |
| USER_IP                            | 사용자 IP                                                                                                                           |
| SQL_LOGGING                        | 해당 세션의 Trace Log 에 메시지를 남길지 여부<br>Parsing, Validation, Optimization 단계에서 발생하는 에러를 남깁니다.<br>DDL을 수행한 결과를 남깁니다.<br>(위의 두 케이스 모두 남깁니다) |
| SHOW_HIDDEN_COLS                   | SELECT 시, 숨겨진 컬럼을 나타낼 것인지 여부                                                                                                     |
| FEEDBACK_APPEND_ERROR              | APPEND 시 에러를 찾으면 곧바로 실패할 것인지 여부                                                                                                  |
| DEFAULT_DATE_FORMAT                | Datetime 입력 시 기본 입력 포맷                                                                                                           |
| HASH_BUCKET_SIZE                   | 쿼리 수행 시 생성할, Temp Hashtable 의 Bucket 개수                                                                                          |
| MAX_QPX_MEM                        | 쿼리 수행 시 가용할 최대 메모리 크기                                                                                                            |
| RS_CACHE_ENABLE                    | Result Cache 사용 여부                                                                                                               |
| RS_CACHE_TIME_BOUND_MSEC           | Result Cache 사용 시, 결과를 저장하기 위한 최대 경과 시간                                                                                          |
| RS_CACHE_MAX_MEMORY_PER_QUERY      | Result Cache 사용 시, 쿼리 마다 사용할 최대 메모리 크기                                                                                           |
| RS_CACHE_MAX_RECORD_PER_QUERY      | Result Cache 사용 시, 쿼리 마다 사용할 최대 결과 개수                                                                                            |
| RS_CACHE_APPROXIMATE_RESULT_ENABLE | Result Cache 사용 시, 정확하지 않은 쿼리의 결과를 캐싱해 갈 것인지 여부                                                                                  |
| IDLE_TIMEOUT                       | 세션 연결 후 해당 시간 동안 Client 가 아무일도 하지 않을 시 세션 종료                                                                                     |
| QUERY_TIMEOUT                      | 쿼리 수행 시 응답 대기 시간                                                                                                                 |

### V$SESMEM
---

세션 메모리 정보를 표시합니다.

| 컬럼 이름 | 설명          |
| ----- | ----------- |
| SID   | 세션 식별자      |
| ID    | 메모리 매니저 식별자 |
| USAGE | 사용 크기       |

### V$SESSTAT
---

세션의 통계 정보를 표시합니다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| SID   | 세션 식별자    |
| ID    | 통계 정보 식별자 |
| VALUE | 통계 정보 값   |

### V$SESTIME
---

세션의 시간 정보를 표시합니다.

| 컬럼 이름      | 설명             |
| ---------- | -------------- |
| SID        | 세션 식별자         |
| ID         | 수행 단위 식별자      |
| ACCUM_TICK | 누적 시간          |
| MAX_TICK   | (각 수행 중) 최대 시간 |

### V$SYSMEM
---

시스템의 메모리 정보를 표시합니다.

| 컬럼 이름     | 설명           |
| --------- | ------------ |
| ID        | 메모리 매니저 식별자  |
| NAME      | 메모리 매니저 이름   |
| USAGE     | 현재 사용량       |
| MAX_USAGE | (기록된) 최대 사용량 |

### V$SYSSTAT
---

시스템의 통계 정보를 표시합니다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| ID    | 통계 정보 식별자 |
| NAME  | 통계 정보 이름  |
| VALUE | 통계 정보 값   |

### V$SYSTIME
---

시스템의 시간 정보를 표시합니다.

| 컬럼 이름      | 설명             |
| ---------- | -------------- |
| ID         | 수행 단위 식별자      |
| NAME       | 수행 단위 이름       |
| ACCUM_TICK | 누적 시간          |
| AVG_TICK   | (각 수행 중) 평균 시간 |
| MIN_TICK   | (각 수행 중) 최소 시간 |
| MAX_TICK   | (각 수행 중) 최대 시간 |
| COUNT      | 수행 횟수          |

### V$STMT
---

사용자가 현재 실행중인 쿼리문에 대한 정보를 표시합니다.

| 컬럼 이름       | 설명                            |
| ----------- | ----------------------------- |
| ID          | 쿼리 식별자                        |
| SESS_ID     | 쿼리를 수행한 세션 식별자                |
| STATE       | 쿼리 상태                         |
| RECORD_SIZE | SELECT 구문 수행 중인 경우, 결과 레코드 크기 |
| QUERY       | 쿼리 구문                         |

### V$VERSION
---

MACHBASE 의 버전에 대한 정보를 표시합니다.

| 컬럼 이름                     | 설명                                       |
| ------------------------- | ---------------------------------------- |
| BINARY_DB_MAJOR_VERSION   | DB 메이저 버전                                |
| BINARY_DB_MINOR_VERSION   | DB 마이너 버전                                |
| BINARY_META_MAJOR_VERSION | META 메이저 버전                              |
| BINARY_META_MINOR_VERSION | META 마이너 버전                              |
| BINARY_CM_MAJOR_VERSION   | Client (Communication Level) 메이저 버전      |
| BINARY_CM_MINOR_VERSION   | Client (Communication Level) 마이너 버전      |
| BINARY_SIGNATURE          | DB서버 파일의 버전 명                            |
| FILE_DB_MAJOR_VERSION     | File DB 메이저 버전                           |
| FILE_DB_MINOR_VERSION     | File DB 메이저 버전                           |
| FILE_META_MAJOR_VERSION   | File META 메이저 버전                         |
| FILE_META_MINOR_VERSION   | File META 마이너 버전                         |
| FILE_CM_MAJOR_VERSION     | File Client (Communication Level) 메이저 버전 |
| FILE_CM_MINOR_VERSION     | File Client (Communication Level) 마이너 버전 |
| FILE_CREATE_TIME          | 파일 생성 시각                                 |
| EDITION                   | MACHBASE 유형                              |

### V$HTTP_STATUS
---

임베디드 HTTP 엔드포인트의 HTTP 서비스 상태를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| DOC_ROOT | HTTP 문서 루트 |
| HTTP_PORT | HTTP 서비스 포트 |
| THREAD_COUNT | HTTP 작업 스레드 수 |
| CONNECT_COUNT | 접속 수 |
| SERVICE_SUCCESS_COUNT | 성공한 서비스 수 |
| SERVICE_FAILURE_COUNT | 실패한 서비스 수 |
| TOTAL_SERVICE_COUNT | 전체 서비스 수 |
| CURRENT_SERVICE_COUNT | 현재 서비스 수 |
| MAX_HTTP_MEM | 최대 HTTP 메모리 크기 |

### V$NEO_SESSION
---

Neo 프로토콜 클라이언트의 세션 상태를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| ID | 세션 식별자 |
| USER_ID | 사용자 식별자 |
| USER_NAME | 사용자 이름 |
| STMT_COUNT | 세션의 statement 수 |
| DISCONN_FLAG | 연결 해제 플래그 |

### V$NEO_STMT
---

Neo 프로토콜 클라이언트의 statement 상태를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| ID | statement 식별자 |
| SESS_ID | 세션 식별자 |
| STATE | statement 상태 |
| QUERY | statement 텍스트 |
| APPEND_SUCCESS_CNT | append 성공 건수 |
| APPEND_FAILURE_CNT | append 실패 건수 |

## Result Cache
### V$RS_CACHE_LIST
---

결과 캐시 목록을 표시합니다.

| 컬럼 이름           | 설명                          |
| --------------- | --------------------------- |
| TOUCH_TIME      | 캐시를 사용하거나 생성한 시각            |
| USER_ID         | 캐시를 생성한 사용자 식별자             |
| QUERY           | 캐시를 만든 쿼리문                  |
| TIME_SPENT      | 결과를 생성하기까지 경과 시간            |
| TABLE_COUNT     | 쿼리문과 연관된 테이블 개수             |
| RECORD_COUNT    | 결과 레코드 개수                   |
| REFERENCE_COUNT | 현재 참조중인 세션의 개수              |
| HIT_COUNT       | 캐시 히트 횟수                    |
| AGGR_TOUCH_TIME | 집계 결과인 경우, 캐시를 사용하거나 생성한 시각 |
| AGGR_HIT_COUNT  | 집계 결과인 경우, 캐시 히트 횟수         |

### V$RS_CACHE_STAT
---

하나의 세션에서의 결과 캐시의 통계 정보를 표시합니다.

| 컬럼 이름              | 설명                |
| ------------------ | ----------------- |
| CACHE_COUNT        | 결과 캐시의 개수         |
| CACHE_HIT          | 총 캐시 히트 횟수        |
| AGGR_HIT           | 집계 결과의 총 캐시 히트 횟수 |
| CACHE_REPLACED     | 캐시 교체 횟수          |
| CACHE_MEMORY_USAGE | 캐시로 사용된 메모리 크기    |

## PVO Statement Cache
Standard 에디션에서만 제공되는 글로벌 PVO Statement Cache 상태를 조회합니다.

### V$PVO_CACHE_STAT
---

PVO Statement Cache의 전체 통계를 보여준다.

| 컬럼 이름 | 설명 |
| -- | -- |
| CACHE_ENTRY_COUNT | 캐시에 적재된 SQL 엔트리 수 |
| CACHE_HANDLE_COUNT | 모든 SQL에 대한 캐시된 플랜(핸들) 수 |
| CACHE_MEMORY_USAGE | 사용 중인 캐시 메모리 크기 |
| CACHE_MAX_MEMORY_SIZE | 설정된 캐시 메모리 한도 |
| CACHE_MAX_PLANS_PER_SQL | SQL당 허용되는 최대 플랜 수 |
| CACHE_MAX_SQL_ENTRIES | 허용되는 최대 SQL 엔트리 수 (0은 무제한) |
| CACHE_SHARD_COUNT | 캐시 샤드 개수 |
| CACHE_HIT | 캐시 히트 횟수 |
| CACHE_MISS | 캐시 미스 횟수 |
| SINGLEFLIGHT_WAIT | 동일 SQL 병행 빌드 대기 횟수 |
| BUILD_COUNT | 플랜 빌드 시도 횟수 |
| BUILD_FAIL | 빌드 실패 횟수 |
| INVALIDATE_COUNT | 무효화된 플랜 수 |
| EVICT_COUNT | 메모리 한도 등으로 인한 캐시 축출 횟수 |
| FLUSH_COUNT | 명시적/내부 플러시 횟수 |

### V$PVO_CACHE_LIST
---

PVO Statement Cache에 저장된 SQL별 상세 정보를 보여준다.

| 컬럼 이름 | 설명 |
| -- | -- |
| TOUCH_TIME | 마지막 터치 시각 |
| USER_ID | SQL을 소유한 사용자 ID |
| QUERY | 원본 SQL 텍스트 |
| DEFAULT_DATE_FORMAT | 실행 당시의 날짜 포맷 |
| TIMEZONE_OFFSET | 실행 당시 타임존 오프셋 |
| SHOW_HIDDEN_COLS | 숨김 컬럼 표시 여부 |
| QUERY_PARALLEL_FACTOR | 병렬 실행 계수 |
| HANDLE_COUNT | 보유한 플랜(핸들) 수 |
| BUSY_COUNT | 동시에 사용 중인 핸들 수 |
| HIT_COUNT | 캐시 히트 횟수 |
| BUILD_IN_PROGRESS | 빌드 진행 중 여부 |

## Storage
### V$STORAGE
---

저장 시스템의 내부 정보를 표시합니다.

| 컬럼 이름                     | 설명                                   |
| ------------------------- | ------------------------------------ |
| DC_TABLE_FILE_SIZE        | 디스크 컬럼 데이터의 총 용량                     |
| DC_INDEX_FILE_SIZE        | 인덱스 파일 데이터의 총 용량                     |
| DC_TABLESPACE_DWFILE_SIZE | 모든 컬럼데이터를 위한 DWFILE의 총 용량            |
| DC_KV_TABLE_FILE_SIZE     | TAGDATA 테이블의 파티션 테이블이 가지는 데이터파일 총 용량 |

### V$STORAGE_MOUNT_DATABASES
---

마운트 기능을 이용하여 마운트한 백업 데이터베이스의 정보를 표시합니다.

| 컬럼 이름             | 설명                     |
| ----------------- | ---------------------- |
| NAME              | 마운트된 데이터베이스의 이름        |
| PATH              | 백업 파일의 위치              |
| BACKUP_TBSID      | 백업 데이터베이스의 테이블스페이스 식별자 |
| BACKUP_SCN        | 백업 데이터베이스의 식별자         |
| MOUNTDB           | 백업 시간                  |
| DB_BEGIN_TIME     | 백업 데이터베이스의 최초입력 시간     |
| DB_END_TIME       | 백업 데이터베이스의 최종 입력 시간    |
| BACKUP_BEGIN_TIME | 백업 실행시 시작 시간           |
| BACKUP_END_TIME   | 백업 실행시 종료 시간           |
| FLAG              | 프로퍼티 플래그               |

### V$CACHE
---

Storage Manager 에서 읽은 결과를 캐싱한, 캐시 객체에 대한 종합 정보를 표시합니다.

| 컬럼 이름     | 설명               |
| --------- | ---------------- |
| OBJ_COUNT | 결과집합 캐시 객체의 현재 수 |

### V$CACHE_OBJECTS
---

저장 시스템에서 읽은 결과를 캐싱한, 각 캐시 객체에 대한 정보를 표시합니다.

| 컬럼 이름     | 설명             |
| --------- | -------------- |
| OID       | 객체식별자          |
| REF_COUNT | 참조 카운트         |
| FLAG      | (서버 내부 사용 플래그) |

### V$STORAGE_DC_TABLESPACES
---

저장 시스템의 테이블스페이스 정보를 표시합니다.

| 컬럼 이름      | 설명                           |
| ---------- | ---------------------------- |
| NAME       | 테이블스페이스 이름                   |
| ID         | 테이블스페이스 식별자                  |
| FLAG       | 테이블스페이스 Property 를 나타내는 Flag |
| REF_COUNT  | 테이블스페이스 참조 횟수                |
| DISK_COUNT | 테이블스페이스에 속한 디스크 개수           |

### V$STORAGE_DC_TABLESPACE_DISKS
---

저장 시스템의 테이블스페이스 정보를 표시합니다.

| 컬럼 이름              | 설명                  |
| ------------------ | ------------------- |
| NAME               | 디스크 이름              |
| ID                 | 디스크 식별자             |
| TABLESPACE_ID      | 디스크가 속한 테이블스페이스 식별자 |
| PATH               | 디스크의 경로             |
| IO_THREAD_COUNT    | I/O Thread 개수       |
| IO_JOB_COUNT       | I/O Job 개수          |
| VIRTUAL_DISK_COUNT | 가상 디스크 개수           |

### V$STORAGE_DC_DWFILES
---

저장 시스템에서 운용하는 Double-write 파일 (DW File) 의 정보를 표시합니다.

| 컬럼 이름                | 설명                      |
| -------------------- | ----------------------- |
| TBS_ID               | 테이블스페이스 식별자             |
| DISK_ID              | 디스크 식별자                 |
| FILE                 | 파일의 경로                  |
| TABLE_ID             | 테이블 식별자                 |
| COLUMN_ID            | 컬럼 식별자                  |
| PARTITION_ID         | 파티션 식별자                 |
| PAGE_ID              | 페이지 식별자                 |
| DISK_OFFSET          | 디스크 오프셋                 |
| DISK_IMAGE_SIZE      | 디스크 이미지 크기              |
| HEAD_CRC32CODE_IMAGE | CRC32 Code 의 Head Image |
| TAIL_CRC32CODE_IMAGE | CRC32 Code 의 Tail Image |
| CRC32CODE_PAGE       | CRC32 Code 의 Page       |
| HEAD_TIMESTAMP_PAGE  | Timestamp 의 Head Page   |
| TAIL_TIMESTAMP_PAGE  | Timestamp 의 TailPage    |

### V$STORAGE_DC_PAGECACHE
---

저장 시스템에서 운용하는 Page Cache 에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명                     |
| ------------ | ---------------------- |
| MAX_MEM_SIZE | Page Cache 의 최대 메모리 크기 |
| CUR_MEM_SIZE | Page Cache 의 현재 메모리 크기 |
| PAGE_CNT     | 캐싱된 페이지 개수             |
| CHECK_TIME   | 검사 시간                  |

### V$STORAGE_DC_PAGECACHE_LRU_LST
---

저장 시스템에서 운용하는 Page Cache 의 LRU List 에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명                  |
| ------------ | ------------------- |
| SIZE         | 페이지 크기              |
| REF_CNT      | 참조 횟수               |
| PARTITION_ID | 파티션 식별자             |
| OFFSET       | Page Cache 의 Offset |
| OBJECT_ID    | 객체 식별자              |
| LEVEL        | 파티션 레벨              |

### V$STORAGE_USAGE
---

저장 시스템에서 사용 중인 스토리지의 사용량을 표시합니다.

| 컬럼 이름       | 설명                                                     |
| ----------- | ------------------------------------------------------ |
| TOTAL_SPACE | $MACHBASE_HOME/dbs 디렉터리가 위치한 스토리지의 총 용량                |
| USED_SPACE  | $MACHBASE_HOME/dbs 디렉터리가 위치한 스토리지의 사용량                 |
| USED_RATIO  | 사용량 비율(%)                                              |
| RATIO_CAP   | 스토리지 사용량 한계. USED_RATIO이 이 한계에 도달하면 데이터 입력/인덱스 구축이 멈춤. |

### V$STORAGE_TABLES
---

테이블의 상세 정보를 표시합니다.

| 컬럼 이름         | 설명                                                                                                                                                                                                         |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID            | 테이블의 ID                                                                                                                                                                                                    |
| TYPE          | 테이블 형태<br>Persistent: LOG 테이블과 TAG 테이블<br>Volatile: 휘발성(Volatile) 테이블<br>Key-Value: TAG 테이블의 부속 테이블                                                                                                        |
| STATUS        | 현재 상태<br>Creating...: CREATE TABLE로 테이블 생성 진행중<br>Normal: 정상<br>Predrop: DROP TABLE 명령 접수 상태<br>Dropping...: DROP TABLE 명령 수행 상태<br>Dropped: DROP TABLE 명령 완료 상태<br>Mounted: 백업된 데이터베이스를 mount 명령으로 불러온 상태 |
| STORAGE_USAGE | 해당 테이블이 스토리지에서 점유한 용량                                                                                                                                                                                      |

## Log Table
### V$STORAGE_DC_TABLES
---

Log Table 에 대한 내부 정보를 표시합니다.

| 컬럼 이름                | 설명                                         |
| -------------------- | ------------------------------------------ |
| ID                   | 테이블의 식별자                                   |
| DATABASE_ID          | 데이터베이스 식별자                                 |
| CREATE_SCN           | 생성 당시의 시스템 변경 번호 (System Change Number)    |
| UPDATE_SCN           | 최근 변경 당시의 시스템 변경 번호 (System Change Number) |
| DDL_REF_COUNT        | DDL 구문 수행으로, 해당 테이블을 참조하고 있는 세션의 개수.       |
| BEGIN_RID            | 테이블의 최소 RID                                |
| END_RID              | 테이블의 마지막 Row ID + 1                        |
| BEGIN_META_RID       | 메타 정보를 기록하기 시작한 시점의 ID                     |
| END_META_RID         | 메타 정보의 기록이 종료한 시점의 ID                      |
| END_SYNC_RID         | 디스크에 기록된 마지막 Row ID + 1                    |
| FLAG                 | Table Property 를 나타내는 Flag                 |
| COLUMN_COUNT         | 테이블의 컬럼 수                                  |
| INDEX_COUNT          | 테이블의 인덱스 수                                 |
| INDEX_MIN_END_RID    | 인덱스에 기록된 마지막 RID + 1                       |
| LAST_ARRIVAL_TIME    | 마지막으로 기록된 \_arrival_time 값                 |
| LAST_CHECKPOINT_TIME | 마지막으로 Checkpoint 를 지난 시점                   |
| TYPE                 | 테이블 유형                                     |

### V$STORAGE_DC_TABLES_STAT
---

Log Table 에 대한 내부 정보를 표시합니다.

| 컬럼 이름         | 설명          |
| ------------- | ----------- |
| TABLESPACE_ID | 테이블스페이스 식별자 |
| TABLE_ID      | 테이블 식별자     |
| COUNT         | 레코드 개수      |
| COLUMN_ID     | 컬럼 식별자      |

### V$STORAGE_DC_TABLE_COLUMNS
---

Log Table 의 컬럼에 대한 정보를 표시합니다.

| 컬럼 이름                     | 설명                              |
| ------------------------- | ------------------------------- |
| TABLE_ID                  | 테이블 식별자                         |
| DATABASE_ID               | 데이터베이스 식별자                      |
| ID                        | 컬럼 식별자                          |
| FLAG                      | 프로퍼티 플래그                        |
| SIZE                      | 컬럼의 데이터 크기                      |
| PARTITION_VALUE_COUNT     | 파티션에 저장되는 최대 데이터 수              |
| PAGE_VALUE_COUNT          | 페이지에 저장되는 최대 데이터 수              |
| CACHE_VALUE_COUNT         | 캐시 값의 최대 수                      |
| MINMAX_CACHE_SIZE         | 컬럼 파티션에 대한 MIN/MAX 캐시의 최대 크기    |
| CUR_APPEND_PARTITION_ID   | 현재 입력을 진행중인 파티션의 식별자            |
| CUR_CACHE_PARTITION_COUNT | 현재 캐시에 데이터를 읽어들인 파티션의 수         |
| CUR_MINMAX_CACHE_SIZE     | 현재 MIN/MAX캐시의 크기                |
| END_RID_FOR_DEFAULT_VALUE | 이 값보다 작은 RID를 갖는 컬럼은 디폴트값으로 지정됨 |
| DISK_FILE_SIZE            | 해당 컬럼에 대한 컬럼 파티션 데이터 파일의 전체 크기  |
| MEMORY_TOTAL_SIZE         | 테이블이 사용 중인 메모리 크기               |
| MEMORY_ALLOC_SIZE         | 테이블이 할당받은 메모리 크기                |

### V$STORAGE_DC_TABLE_COLUMN_PARTS
---

Log Table 의 컬럼 파티션 정보를 표시합니다.

| 컬럼 이름                         | 설명                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| TABLE_ID                      | 테이블 식별자                                                                            |
| DATABASE_ID                   | 데이터베이스 식별자                                                                         |
| COLUMN_ID                     | 컬럼 식별자                                                                             |
| ID                            | 파티션 식별자                                                                            |
| FLAG                          | 컬럼 Property 를 나타내는 Flag                                                            |
| BEGIN_RID                     | 파티션에 저장된 최소 RID                                                                    |
| END_RID                       | 파티션에 저장된 최종 RID                                                                    |
| END_SYNC_RID                  | SYNC가 끝난 최종 RID.<br>시작 RID 보다 크고 마지막 SYNC RID 보다 작은 RID 를 갖는 데이터는 파티션 파일에 기록되어 있습니다. |
| MIN_TIME                      | 컬럼 파티션에 최초로 데이터를 입력한 시간                                                            |
| MAX_TIME                      | 컬럼 파티션에 마지막으로 데이터를 입력한 시간                                                          |
| MAX_VALUE_COUNT_PER_PARTITION | 파티션의 최대 데이터 수                                                                      |
| MAX_VALUE_COUNT_PER_PAGE      | 페이지당 최대 데이터 수                                                                      |
| MAX_PAGE_COUNT                | 파티션당 최대 페이지의 수                                                                     |
| PAGE_SIZE                     | 컬럼 파티션에 저장된 페이지의 크기                                                                |
| PAGE_COUNT                    | 현재 컬럼 파티션에 생성된 페이지의 수                                                              |
| COMPRESS_RATIO                | 컬럼 파티션의 압축률. 0이면 아직 데이터 압축이 실행되지 않은 경우입니다.                                          |
| DISK_FILENAME                 | 파티션 파일의 이름                                                                         |
| EXTERNAL_PART_SIZE            | 데이터의 양이 큰 값은 외부 파티션 파일에 기록하는데, 그 파일의 크기를 표시                                        |
| MIN_VALUE                     | 컬럼 파티션의 최소값                                                                        |
| MAX_VALUE                     | 컬럼 파티션의 최대값                                                                        |

### V$STORAGE_DC_TABLE_INDEXES
---

Log Table 에 생성된 인덱스 정보를 표시합니다.

| 컬럼 이름                | 설명                           |
| -------------------- | ---------------------------- |
| TABLE_ID             | 테이블 식별자                      |
| DATABASE_ID          | 데이터베이스 식별자                   |
| ID                   | 인덱스 식별자                      |
| FLAG                 | 인덱스 Property 를 나타내는 Flag     |
| TABLE_BEGIN_RID      | 테이블의 입력된 최소 RID              |
| TABLE_END_RID        | 테이블의 마지막 RID                 |
| BEGIN_RID            | 인덱스의 최소 RID                  |
| END_RID              | 인덱스의 최대 RID                  |
| END_SYNC_RID         | 파일에 기록된 최대 RID+1             |
| COLUMN_COUNT         | 인덱스 컬럼 수                     |
| BEGIN_PART_ID        | 인덱스의 최초 파티션 식별자              |
| END_PART_ID          | 인덱스의 최종 파티션 식별자              |
| FLUSH_REQUEST_COUNT  | 디스크에 반영요청된 인덱스 파티션의 수        |
| MAX_KEY_SIZE         | 최대 키 크기                      |
| INDEX_TYPE           | 인덱스 유형                       |
| DISK_FILE_SIZE       | 해당 인덱스에 대한 인덱스 파티션 파일의 전체 크기 |
| LAST_CHECKPOINT_TIME | 마지막으로 Checkpoint 를 지난 시점     |

## LSM(Log Structured Merge) Index
### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS
---

LSM Index 파티션에 대한 정보를 표시합니다.

| 컬럼 이름                      | 설명                                      |
| -------------------------- | --------------------------------------- |
| TABLE ID                   | 인덱스가 생성된 테이블의 식별자                       |
| TABLESPACE_ID              | 테이블스페이스 식별자                             |
| INDEX_ID                   | 인덱스 식별자                                 |
| LEVEL                      | 인데스 파티션의 LSM 레벨                         |
| PARTITION_ID               | 파티션 식별자                                 |
| BEGIN_RID                  | 파티션에 입력된 최소 RID                         |
| END_RID                    | 파티션에 입력된 최대 RID+1                       |
| KEY_VALUE_COUNT            | 파티션에 입력된 키값의 수                          |
| KEY_VALUE_TABLE_SIZE       | 키값을 저장하는 페이지 크기                         |
| KEY_VALUE_TABLE_PAGE_COUNT | 키값을 저장하는 페이지의 수                         |
| MIN_KEY_VALUE              | 최소 키 값                                  |
| MAX_KEY_VALUE              | 최대 키 값                                  |
| BITMAP_TABLE_SIZE          | 비트맵 값을 저장하는 페이지의 합계                     |
| BITMAP_TABLE_PAGE_COUNT    | 비트맵 값을 저장하는 페이지의 수                      |
| META_SIZE                  | 메타 정보를 저장하는 페이지의 합계                     |
| META_PAGE_COUNT            | 메타 정보를 저장하는 페이지의 수                      |
| TOTAL_BUILD_MSEC           | 해당 파티션을 완성하기 까지의 총 시간                   |
| KEYVAL_BUILD_MSEC          | KeyValue Mode 에서, 해당 파티션을 완성하기 까지의 총 시간 |
| BITMAP_BUILD_MSEC          | Bitmap Mode 에서, 해당 파티션을 완성하기 까지의 총 시간   |

### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS_CACHE
---

LSM Index 파티션 캐시에 대한 정보를 표시합니다.

| 컬럼 이름                      | 설명                          |
| -------------------------- | --------------------------- |
| BEGIN_RID                  | 파티션에 입력된 최소 RID             |
| BITMAP_TABLE_PAGE_COUNT    | 비트맵 값을 저장하는 페이지의 수          |
| BITMAP_TABLE_SIZE          | 비트맵 값을 저장하는 페이지의 합계         |
| END_RID                    | 파티션에 입력된 최대 RID+1           |
| INDEX_ID                   | 인덱스 식별자                     |
| KEY_VALUE_COUNT            | 파티션에 입력된 키값의 수              |
| KEY_VALUE_TABLE_PAGE_COUNT | 키값을 저장하는 페이지의 수             |
| KEY_VALUE_TABLE_SIZE       | 키값을 저장하는 페이지의 크기            |
| LEVEL                      | 인데스 파티션의 LSM 레벨             |
| MEMORY_SIZE                | 메모리 사용량                     |
| MEMORY_SIZE_RBTREE         | Redblack Tree 가 사용한 메모리 사용량 |
| META_PAGE_COUNT            | 메타 정보를 저장하는 페이지의 수          |
| META_SIZE                  | 메타 정보를 저장하는 페이지의 합계         |
| PARTITION_ID               | 파티션 식별자                     |
| TABLE_ID                   | 인덱스가 생성된 테이블의 식별자           |
| TABLESPACE_ID              | 테이블스페이스 식별자                 |

### V$STORAGE_DC_LSMINDEX_LEVELS
---

LSM 인덱스의 레벨에 관한 정보를 표시합니다.

| 컬럼 이름          | 설명                     |
| -------------- | ---------------------- |
| TABLE ID       | 테이블 식별자                |
| DATABASE_ID    | 데이터베이스 식별자             |
| INDEX_ID       | 인덱스 식별자                |
| LEVEL          | 레벨                     |
| BEGIN_RID      | 파티션의 첫번째 RID           |
| END_RID        | 파티션의 마지막 RID+1         |
| META_BEGIN_RID | 메타정보를 기록하기 시작한 시점의 RID |
| META_END_RID   | 메타정보의 기록이 끝난 시점의 RID   |
| DELETE_END_RID | 삭제된 RID 최대값 +1         |

### V$STORAGE_DC_LSMINDEX_FILES
---

LSM Index 를 구성하는 파일에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명              |
| ------------ | --------------- |
| TABLE_ID     | 테이블 식별자         |
| DATABASE_ID  | 데이터베이스 식별자      |
| INDEX_ID     | 인덱스 식별자         |
| LEVEL        | 인데스 파티션의 LSM 레벨 |
| PARTITION_ID | 파티션 식별자         |
| BEGIN_RID    | 파티션의 첫번째 RID    |
| END_RID      | 파티션의 마지막 RID+1  |
| PATH         | 인덱스 파일의 위치      |

### V$STORAGE_DC_LSMINDEX_AGER_JOBS
---

LSM Index 의 삭제를 담당하는 Ager 의 작업 상태를 표시합니다.

| 컬럼 이름     | 설명                 |
| --------- | ------------------ |
| TABLE_ID  | 테이블 식별자            |
| INDEX_ID  | 인덱스 식별자            |
| LEVEL     | 인데스 파티션의 LSM 레벨    |
| BEGIN_RID | 파티션의 첫번째 RID       |
| END_RID   | 파티션의 마지막 RID+1     |
| STATE     | Index Ager 의 작업 상태 |

## Volatile Table
### V$STORAGE_DC_VOLATILE_TABLE
---

Volatile Table 에 대한 정보를 표시합니다.

| 컬럼 이름        | 설명                          |
| ------------ | --------------------------- |
| MAX_MEM_SIZE | Volatile Tablespace 의 최대 크기 |
| CUR_MEM_SIZE | Volatile Tablespace 의 현재 크기 |

## Tag Table
### V$STORAGE_TAG_TABLES
---

Tagdata Table 의 파티션 테이블에 대한 정보를 표시합니다.

| 컬럼 이름                | 설명                                                                                                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID                   | 테이블 식별자                                                                                                                                                                                      |
| TABLE_BEGIN_RID      | 테이블 시작 RID                                                                                                                                                                                   |
| TABLE_END_RID        | 테이블 끝 RID                                                                                                                                                                                    |
| WRITE_END_RID        | 데이터 파일에 기록된 마지막 RID                                                                                                                                                                          |
| EXT_ROW_COUNT        | VARCHAR 레코드 중 외부 파티션에 입력된 개수                                                                                                                                                                 |
| EXT_WRITE_COUNT      | VARCHAR 레코드 중 데이터파일에 기록된 개수                                                                                                                                                                  |
| DISK_INDEX_END_RID   | 스토리지에 저장된 인덱스의 끝 RID                                                                                                                                                                         |
| MEMORY_INDEX_END_RID | 메모리 인덱스에 상주한 테이블 끝 RID                                                                                                                                                                       |
| DELETE_MIN_DATE      | DELETE ... BETWEEN ... 수행시 삭제 대상의 최소 시각                                                                                                                                                      |
| DELETE_MAX_DATE      | DELETE ... BETWEEN ..., 혹은 DELETE ... BEFORE ... 수행시 삭제 대상의 최대 시각                                                                                                                            |
| INDEX_STATE          | 현재 인덱스 구축 상태<br>IDLE: 구축 완료, 대기중.<br>PROGRESS: 구축 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료                |
| DELETE_STATE         | 현재 DELETE 연산의 상태. DELETE 명령이 들어올 때에만 수행되므로 IDLE이 없습니다.<br>PROGRESS: 삭제 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기/쓰기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산이 진행되지 않습니다.<br>ABNORMAL: 비정상 종료 |
| SAVE_STATE           | 현재 테이블 저장 연산의 상태.<br>IDLE: 저장 완료, 대기중.<br>PROGRESS: 저장 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료           |
| VINDEX_STATE         | 현재 VARCHAR 인덱스 구축 상태<br>IDLE: 구축 완료, 대기중.<br>PROGRESS: 구축 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됩니다. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료                |

### V$STORAGE_TAG_CACHE
---

Tagdata Table 의 파티션 테이블에서 사용하는 캐시 정보를 표시합니다.

| 컬럼 이름       | 설명                       |
| ----------- | ------------------------ |
| CATEGORY    | 캐쉬되고 있는 객체 분류            |
| USED_MEMORY | 사용중인 메모리 크기              |
| BLOCK_COUNT | 데이터 캐시 개수                |
| CACHE_HIT   | 데이터 캐시 히트 횟수             |
| CACHE_MISS  | 데이터 캐시 미스 횟수             |
| FLUSHOUT    | 데이터 캐시 충돌로 페이지를 비운 횟수    |
| COLDREAD    | 스토리지에서 직접 읽어온 데이터 페이지 개수 |
| MEMORY_WAIT | 데이터 메모리가 캐시 충돌로 대기한 횟수   |
| IO_WAIT     | 데이터 읽기 연산 대기 횟수          |

### V$STORAGE_TAG_CACHE_BASE
---

태그 캐시 풀의 집계 정보를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| POOL_ID | 캐시 풀 식별자 |
| TOTAL_CACHE_MEMORY | 전체 캐시 메모리 |
| TOTAL_OBJECT_COUNT | 전체 캐시 객체 수 |
| TOTAL_LRU_LOOP_COUNT | 전체 LRU 루프 수 |

### V$STORAGE_TAG_CACHE_OBJECTS
---

Tagdata Table의 파티션 테이블에서 사용하는 각각의 캐시 블럭에 대한 상세정보를 표시합니다.

| 컬럼 이름      | 설명                                                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
| CATEGORY   | 캐쉬되고 있는 객체 분류                                                                                                        |
| LATEST_HIT | 마지막 접근 시각                                                                                                            |
| STATUS     | 캐시 상태<br>None: 메모리 할당을 마친 상태<br>Resides: 캐시에 보존된 상태<br>Loading: 스토리지에서 테이블 데이터를 불러 오는 중<br>ERROR!: 데이터를 불러오는 중 오류 발생 |
| WAIT_COUNT | Loading 상태에서 해당 캐시를 읽지 못해 대기한 회수                                                                                     |
| REF_COUNT  | 현재 캐시 블럭을 참조 중인 세션 수                                                                                                 |
| HIT_COUNT  | 캐시 블럭을 참조한 회수                                                                                                        |
| TABLE_ID   | 테이블 식별자                                                                                                              |
| FILE_ID    | 파일 식별자                                                                                                               |
| PART_ID    | 데이터파일 내부의 파티션 식별자                                                                                                    |
| SAVE_SCN   | 테이블 저장 SCN                                                                                                           |
| VSAVE_SCN  | 테이블 저장 SCN                                                                                                           |
| DELETE_SCN | DELETE 연산 SCN                                                                                                        |
| OFFSET     | 데이터파일 오프셋                                                                                                            |
| DATA_SIZE  | 압축 이전 데이터 크기, 혹은 0                                                                                                   |

### V$STORAGE_TAG_TABLE_FILES
---

Tagdata Table 의 파티션 테이블의 파일 정보를 표시합니다.

| 컬럼 이름     | 설명                                                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| TABLE_ID  | 테이블 식별자                                                                                                                            |
| FILE_ID   | 파일 식별자                                                                                                                             |
| STATE     | 인덱싱 상태<br>COMPLETE: 데이터 저장, 인덱싱 완료<br>INDEXING: 인덱스 구축 중.<br>FILLED: 데이터가 꽉 찬 상태, 인덱싱 대기 중<br>PARTIAL: 아직 데이터가 꽉 차지 않았음. 인덱싱 대기 중. |
| REF_COUNT | 현재 파일을 참조 중인 세션 수                                                                                                                  |
| ROW_COUNT | 삭제됐던 레코드를 포함하여 파일에 저장된 레코드 개수                                                                                                      |
| DEL_COUNT | 파일에서 삭제된 레코드 개수                                                                                                                    |
| MIN_DATE  | 해당 파일에 기록된 데이터의 최소 일자                                                                                                              |
| MAX_DATE  | 해당 파일에 기록된 데이터의 최대 일자                                                                                                              |

### V$STORAGE_TAG_INDEX
---

Tagdata Table 에 생성된 인덱스 정보를 표시합니다.

| 컬럼 이름                | 설명                                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| TABLE_ID             | 테이블 식별자                                                                                               |
| INDEX_ID             | 인덱스 식별자(INDEX_ID가 4294967295인 경우 tag테이블 생성시 자동으로 생성되는 기본 인덱스를 의미함)                                    |
| INDEX_STATE          | 인덱싱 상태<br>IDLE: 인덱싱이 완료되어 대기중인 상태<br>INDEXING: 인덱싱이 진행중인 상태<br>STORAGE FULL: Disk full상태로 인덱싱이 중단된 상태 |
| DISK_INDEX_END_RID   | 마지막으로 disk에 반영된 인덱스의 EndRID                                                                           |
| MEMORY_INDEX_END_RID | 마지막으로 memory에 반영된 인덱스의 EndRID                                                                         |
| TABLE_END_RID        | 테이블에 마지막으로 반영된 데이터의 EndRID                                                                            |

## Tag Rollup
### V$ROLLUP
---

Tagdata 테이블의 Rollup 정보를 표시합니다.

| 컬럼 이름          | 설명                                                      |
| -------------- | ------------------------------------------------------- |
| DATABASE_ID    | 데이터베이스 식별자(로컬 DB는 -1)                                  |
| ID             | Rollup 작업 ID                                            |
| ROLLUP_TABLE   | Rollup 테이블 이름                                         |
| SOURCE_TABLE   | 집계 대상 테이블 이름(TAG/ROLLUP)                                |
| COLUMN_NAME    | 집계 대상 값 컬럼                                               |
| ROOT_TABLE     | 최상위 소스 태그 테이블 이름                                        |
| USER_ID        | 소유자 User ID                                             |
| INTERVAL_TIME  | Rollup 실행 주기(밀리초)                                         |
| WAKEUP_INTERVAL| Wakeup 주기(밀리초)                                          |
| LAST_WAKEUP_TIME| 최근 wakeup 시각                                            |
| NEXT_WAKEUP_TIME| 다음 wakeup 예정 시각                                         |
| ENABLED        | Rollup 활성화 여부(1/0)                                      |
| END_RID        | 이 Rollup이 처리한 Source Table의 마지막 RID                      |
| LAST_ELAPSED_MSEC | 직전 Rollup 실행에 걸린 시간(밀리초)                               |
| EXT_TYPE       | 확장(EXTENSION) 여부 플래그                                     |
| PREDICATE      | 조건 롤업의 필터 식(NULL이면 조건 없음)                              |
| RUN_STATE      | 스레드 상태: I=INIT, S=SLEEPING, R=RUNNING                      |

## Stream
### V$STREAMS
---

Stream 정보를 표시합니다.

| 컬럼 이름        | 설명                                                                          |
| ------------ | --------------------------------------------------------------------------- |
| NAME         | 서버에 등록된 stream질의의 이름. 서버내에서 유일해야 합니다.                                         |
| LAST_EX_TIME | 해당 STREAM질의가 마지막으로 수행된 시간                                                   |
| TABLE_NAME   | STREAM질의의 검색 대상 테이블 이름                                                      |
| END_RID      | STREAM 질의가 마지막으로 읽어 들인 RID                                                  |
| STATE        | STREAM질의의 현재 상태                                                             |
| QUERY_TXT    | 사용자가 입력한 STREAM질의의 원본                                                       |
| ERROR_MSG    | 마지막으로 실행했을 때의 에러 메시지                                                        |
| FREQUENCY    | 질의 수행의 최소 대기 시간. 0이면 매 레코드마다 실행되며 0이 아니면 해당 시간이 지날 때 마다 수행됩니다.<br>단위는 나노초입니다. |

## License
### V$LICENSE_INFO
---

라이선스 정보를 표시합니다.

| 컬럼 이름            | 설명                     |
| ---------------- | ---------------------- |
| ID               | 라이선스 ID               |
| ISSUE_DATE       | 발행일                    |
| TYPE             | 라이선스 유형                |
| CUSTOMER         | 고객사 이름                 |
| PROJECT          | 프로젝트 이름                |
| COUNTRY_CODE     | 국가 코드                  |
| INSTALL_DATE     | 설치일                    |
| VIOLATE_STATUS   | 라이선스 위반 상태             |
| VIOLATE_MSG      | 라이선스 위반 메시지            |

`V$LICENSE_STATUS`는 Standard 8.5.4 서버에서 노출되지 않습니다. Standard 에디션에서
조회 가능한 라이선스 필드는 `V$LICENSE_INFO`를 사용하십시오.

## Mutex
### V$MUTEX
---

현재 뮤텍스 상태를 보여줍니다.

| 필드명            | 설명                         | 비고                                                                                                         |
| -------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| OBJECT         | 뮤텍스 객체의 주소                 |                                                                                                            |
| NAME           | 뮤텍스 생성시 부여한 이름             |                                                                                                            |
| TYPE           | 뮤텍스 타입                     | Mutex: pmuMutex<br>RW Mutex: pmuRWMutex                                                                    |
| OWNER          | 뮤텍스를 획득한 스레드의 ID           | Mutex: 뮤텍스를 획득한 스레드가 없으면 0.<br>RW Mutex w/ Read-Lock: 0<br>RW Mutex w/ Write-Lock: Write Lock을 획득한 스레드의 ID |
| LOCK_COUNT     | 뮤텍스를 획득한 스레드 개수            | RW Mutex는 2 이상이 될 수 있습니다.                                                                                    |
| PEND_COUNT     | 뮤텍스를 획득하려고 대기 중인 스레드 개수    | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| TRY_COUNT      | 뮤텍스를 획득하려고 시도한 회수          | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| CONFLICT_COUNT | 뮤텍스 획득에 실패한 회수             | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| WAIT_TICK      | 뮤텍스 획득 대기 시간의 총합           | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| WAIT_TICK_AVG  | 뮤텍스 획득 시도 후 성공까지의 평균 시간    | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| HELD_TICK      | 뮤텍스를 획득한 이후 해제할 때까지의 시간 총합 | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| HELD_TICK_AVG  | 뮤텍스 획득 이후 해제까지의 시간 평균      | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |

### V$MUTEX_WAIT_STAT
---

현재 대기중인 뮤텍스의 콜스택을 보여줍니다.

| 필드        | 설명                  | 비고                               |
| --------- | ------------------- | -------------------------------- |
| THREAD_ID | 뮤텍스 획득 대기 중인 스레드 ID |                                  |
| OBJECT    | 획득 시도 중인 뮤텍스의 주소    | V$MUTEX의 OBJECT와 동일              |
| DEPTH     | 호출 깊이               | TRACE_MUTEX_WAIT_STACK=1일 때에만 수집 |
| SYMBOL    | 뮤텍스 획득을 호출한 함수의 심볼  | TRACE_MUTEX_WAIT_STACK=1일 때에만 수집 |

## Cluster

다음 가상 테이블은 클러스터 에디션용이며 Standard 서버에서는 노출되지 않습니다.
실행 중인 에디션에서 조회 가능한지 `V$TABLES`로 확인한 뒤 사용하십시오.

### V$NODE_STATUS
---

Cluster 각 Node 의 상태를 표시합니다. 1건만 표시됩니다.

| 컬럼 이름    | 설명                                                            |
| -------- | ------------------------------------------------------------- |
| NODETYPE | Node 의 유형. 쿼리로 조회 가능한 Type 은 두 가지 뿐입니다.<br>Broker<br>Warehouse |
| STATE    | Node 의 상태                                                     |

### V$DDL_INFO
---

Cluster 에서 수행한 DDL 정보를 표시합니다.

| 컬럼 이름          | 설명                      |
| -------------- | ----------------------- |
| SEQUENCENUMBER | DDL 순서 번호               |
| TIME           | DDL 수행 시간               |
| VALUE          | DDL 쿼리 결과 값 (서버 내부 사용)  |
| CLIENT         | 클라이언트 이름                |
| BROKER         | Leader Broker 의 Node 이름 |
| USER           | 사용자 이름                  |
| SQL            | DDL 쿼리 값                |

### V$REPLICATION
---

Replication 작동에 대한 정보를 표시합니다.

| 컬럼 이름            | 설명                                 |
| ---------------- | ---------------------------------- |
| HOSTNAME         | Replication 이 작동되는 Node 의 Hostname |
| MODE             | (서버 내부 사용)                         |
| STATE            | Node 의 상태                          |
| ADDR             | Replication Manager 의 주소           |
| PORT_NO          | Replication Manager 의 포트번호         |
| MAX_SENDER_COUNT | 생성 가능한 Sender 최대 개수                |
| RUN_SENDER_COUNT | 작동중인 Sender 최대 개수                  |

### V$REPL_SENDER
---

Replication 작동 시, Sender 의 정보를 표시합니다.

| 컬럼 이름              | 설명                                 |
| ------------------ | ---------------------------------- |
| HOSTNAME           | Replication 이 작동되는 Node 의 Hostname |
| ID                 | Sender 식별자                         |
| STATUS             | Sender Thread 의 작동상태               |
| PAYLOAD_RECV_COUNT | Sender 로부터 받은 페이로드 개수              |
| PAYLOAD_RECV_BYTES | Sender 로부터 받은 페이로드 크기 총합           |
| QUEUE_REMAIN_COUNT | Receive Queue 에 남은 버퍼의 개수          |
| NET_SEND_COUNT     | 전체 전송 횟수                           |
| NET_SEND_SIZE      | 전체 전송 크기 총합                        |
| NET_RECV_COUNT     | 전체 수신 횟수                           |
| NET_RECV_SIZE      | 전체 수신 크기 총합                        |

### V$REPL_SENDER_META
---

Replication 작동 시, Sender 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID  | Sender 식별자                         |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_RECEIVER
---

Replication 작동 시, Receiver 의 정보를 표시합니다.

| 컬럼 이름              | 설명                                 |
| ------------------ | ---------------------------------- |
| HOSTNAME           | Replication 이 작동되는 Node 의 Hostname |
| STATUS             | Receiver Thread 의 작동상태             |
| PAYLOAD_RECV_COUNT | Sender 로부터 받은 페이로드 개수              |
| PAYLOAD_RECV_BYTES | Sender 로부터 받은 페이로드 크기 총합           |
| QUEUE_REMAIN_COUNT | Receive Queue 에 남은 버퍼의 개수          |
| NET_SEND_COUNT     | 전체 전송 횟수                           |
| NET_SEND_SIZE      | 전체 전송 크기 총합                        |
| NET_RECV_COUNT     | 전체 수신 횟수                           |
| NET_RECV_SIZE      | 전체 수신 크기 총합                        |

### V$REPL_RECEIVER_META
---

Replication 작동 시, Receiver 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_READER
---

Replication 작동 시, Reader 의 정보를 표시합니다.

| 컬럼 이름       | 설명                                 |
| ----------- | ---------------------------------- |
| HOSTNAME    | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID   | Sender 식별자                         |
| ID          | Reader 식별자                         |
| STATUS      | Reader Thread의 작동상태                |
| FETCH_COUNT | FETCH 수행 횟수                        |

### V$REPL_READER_META
---

Replication 작동 시, Reader 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID  | Sender 식별자                         |
| ID         | Reader 식별자                         |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_WRITER
---

Replication 작동 시, Writer 의 정보를 표시합니다.

| 컬럼 이름        | 설명                                 |
| ------------ | ---------------------------------- |
| HOSTNAME     | Replication 이 작동되는 Node 의 Hostname |
| ID           | Writer 식별자                         |
| STATUS       | Writer Thread 의 작동상태               |
| APPEND_COUNT | APPEND 수행 횟수                       |

### V$REPL_WRITER_META
---

Replication 작동 시, Writer 의 메타데이터를 표시합니다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| ID         | Writer 식별자                         |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

## Others
### V$TABLES
---

V$로 시작하는 모든 Virtual Table 을 표시합니다.

| 컬럼 이름       | 설명           |
| ----------- | ------------ |
| NAME        | 테이블 이름       |
| TYPE        | 테이블 유형       |
| DATABASE_ID | 데이터베이스 식별자   |
| ID          | 테이블 식별자      |
| USER_ID     | 테이블을 생성한 사용자 |
| COLCOUNT    | 컬럼의 갯수       |

### V$COLUMNS
---

Virtual Table 의 컬럼 정보를 표시합니다.

| 컬럼 이름                | 설명         |
| -------------------- | ---------- |
| NAME                 | 컬럼명        |
| TYPE                 | 컬럼의 데이터 타입 |
| DATABASE_ID          | 데이터베이스 식별자 |
| ID                   | 컬럼의 식별자    |
| LENGTH               | 컬럼의 크기     |
| TABLE_ID             | 테이블 식별자    |
| FLAG                 | 비공개 데이터    |
| PART_PAGE_COUNT      | (사용되지 않음)  |
| PAGE_VALUE_COUNT     | (사용되지 않음)  |
| MINMAX_CACHE_SIZE    | (사용되지 않음)  |
| MAX_CACHE_PART_COUNT | (사용되지 않음)  |

### V$RETENTION_JOB
---

RETENTION POLICY가 적용된 테이블 정보를 표시합니다.

| 컬럼 이름         | 설명                                     |
|-------------------|------------------------------------------|
| USER_NAME         | 사용자 이름                              |
| TABLE_NAME        | 대상 TAG TABLE 이름                      |
| POLICY_NAME       | 적용되어 있는 POLICY 이름                |
| STATE             | RETENTION 상태 (RUNNING/WAITING/STOPPED) |
| LAST_DELETED_TIME | 마지막으로 삭제된 시간                   |

### V$USER_AUTH_KEYS
---

Challenge 인증에 등록된 공개 키 정보를 표시합니다.

| 컬럼 이름 | 설명 |
| -- | -- |
| KEY_ID | 키 식별자 |
| USER_ID | 사용자 식별자 |
| USER_NAME | 사용자 이름 |
| KEY_ALGO | 키 알고리즘 |
| KEY_PARAM | 키 파라미터 |
| PUBKEY | 공개 키 텍스트 |
| ACTIVATED | 키 활성화 여부 |
| VALID_AFTER | 키 유효 시작일 |
| VALID_BEFORE | 키 유효 종료일 |
| COMMENT | 키 설명 |
