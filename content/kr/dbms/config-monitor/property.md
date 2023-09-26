---
layout : post
title : 'Property'
type: docs
---

프로퍼티란 __$MACHBASE_HOME/conf/machbase.conf__ 파일에 정의되어 있는 키-값 의 쌍을 의미한다.

이 값들은 마크베이스 서버가 시작할 때 설정되고 실행시 지속적으로 이용된다. 성능 튜닝을 위해서 이 값을 변경하려면 이 값들에 대한 의미를 이해하고, 주의 깊게 설정하여야 한다.

## 목차

* [CPU_AFFINITY_BEGIN_ID](#cpu_affinity_begin_id)
* [CPU_AFFINITY_COUNT](#cpu_affinity_count)
* [CPU_COUNT](#cpu_count)
* [CPU_PARALLEL](#cpu_parallel)
* [DBS_PATH](#dbs_path)
* [DEFAULT_LSM_MAX_LEVEL](#default_lsm_max_level)
* [DISK_BUFFER_COUNT](#disk_buffer_count)
* [DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC](#disk_columnar_index_checkpoint_interval_sec)
* [DISK_COLUMNAR_INDEX_FDCACHE_COUNT](#disk_columnar_index_fdcache_count)
* [DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE](#disk_columnar_page_cache_max_size)
* [DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC](#disk_columnar_table_checkpoint_interval_sec)
* [DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT](#disk_columnar_table_column_fdcache_count)
* [DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE](#disk_columnar_table_column_minmax_cache_size)
* [DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE](#disk_columnar_table_column_part_flush_mode)
* [DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC](#disk_columnar_table_column_part_io_interval_min_sec)
* [DISK_COLUMNAR_TABLE_COLUMN_PARTITION_PRECREATE_COUNT](#disk_columnar_table_column_partition_precreate_count)
* [DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE](#disk_columnar_table_time_inversion_mode)
* [DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE](#disk_columnar_tablespace_dwfile_ext_size)
* [DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE](#disk_columnar_tablespace_dwfile_int_size)
* [DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE](#disk_columnar_tablespace_memory_ext_size)
* [DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE](#disk_columnar_tablespace_memory_max_size)
* [DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE](#disk_columnar_tablespace_memory_min_size)
* [DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT](#disk_columnar_tablespace_memory_slowdown_high_limit_pct)
* [DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC](#disk_columnar_tablespace_memory_slowdown_msec)
* [DISK_IO_THREAD_COUNT](#disk_io_thread_count)
* [DISK_TABLESPACE_DIRECT_IO_FSYNC](#disk_tablespace_direct_io_fsync)
* [DISK_TABLESPACE_DIRECT_IO_READ](#disk_tablespace_direct_io_read)
* [DISK_TABLESPACE_DIRECT_IO_WRITE](#disk_tablespace_direct_io_write)
* [DISK_TAG_AUTO_RECLAIM](#disk_tag_auto_reclaim)
* [DUMP_APPEND_ERROR](#dump_append_error)
* [DUMP_TRACE_INFO](#dump_trace_info)
* [DURATION_BEGIN](#duration_begin)
* [DURATION_GAP](#duration_gap)
* [FEEDBACK_APPEND_ERROR](#feedback_append_error)
* [GRANT_REMOTE_ACCESS](#grant_remote_access)
* [HTTP_THREAD_COUNT](#http_thread_count)
* [INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD](#index_build_max_row_count_per_thread)
* [INDEX_BUILD_THREAD_COUNT](#index_build_thread_count)
* [INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX](#index_flush_max_request_count_per_index)
* [INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT](#index_level_partition_ager_thread_count)
* [INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT](#index_level_partition_build_memory_high_limit_pct)
* [INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT](#index_level_partition_build_thread_count)
* [LOOKUP_APPEND_UPDATE_ON_DUPKEY](#lookup_append_update_on_dupkey)
* [MAX_QPX_MEM](#max_qpx_mem)
* [MEMORY_ROW_TEMP_TABLE_PAGESIZE](#memory_row_temp_table_pagesize)
* [PID_PATH](#pid_path)
* [PORT_NO](#port_no)
* [PROCESS_MAX_SIZE](#process_max_size)
* [QUERY_PARALLEL_FACTOR](#query_parallel_factor)
* [ROLLUP_FETCH_COUNT_LIMIT](#rollup_fetch_count_limit)
* [RS_CACHE_APPROXIMATE_RESULT_ENABLE](#rs_cache_approximate_result_enable)
* [RS_CACHE_ENABLE](#rs_cache_enable)
* [RS_CACHE_MAX_MEMORY_PER_QUERY](#rs_cache_max_memory_per_query)
* [RS_CACHE_MAX_MEMORY_SIZE](#rs_cache_max_memory_size)
* [RS_CACHE_MAX_RECORD_PER_QUERY](#rs_cache_max_record_per_query)
* [RS_CACHE_TIME_BOUND_MSEC](#rs_cache_time_bound_msec)
* [SHOW_HIDDEN_COLS](#show_hidden_cols)
* [TABLE_SCAN_DIRECTION](#table_scan_direction)
* [TAGDATA_AUTO_META_INSERT](#tagdata_auto_meta_insert)
* [TAG_PARTITION_COUNT](#tag_partition_count)
* [TAG_DATA_PART_SIZE](#tag_data_part_size)
* [TAG_TABLE_META_MAX_SIZE](#tag_table_meta_max_size)
* [TRACE_LOGFILE_COUNT](#trace_logfile_count)
* [TRACE_LOGFILE_PATH](#trace_logfile_path)
* [TRACE_LOGFILE_SIZE](#trace_logfile_size)
* [UNIX_PATH](#unix_path)
* [VOLATILE_TABLESPACE_MEMORY_MAX_SIZE](#volatile_tablespace_memory_max_size)

## CPU_AFFINITY_BEGIN_ID

마크베이스 서버가 사용할 CPU의 시작 번호이다. 마크베이스 서버의 CPU사용량을 조절하기 위해서 사용한다.

||Value|
|-|-----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|    0|

## CPU_AFFINITY_COUNT

마크베이스 서버가 사용할 CPU의 수이다. 0으로 설정하면 마크베이스 서버가 모든 CPU를 사용한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|	0|

## CPU_COUNT

시스템에 설정된 CPU의 수를 지정한다. 이 값을 기반으로 마크베이스의 스레드 수를 결정한다. 0으로 지정한 경우에는 시스템의 모든 CPU를 사용한다.

||Value|
|-|----|
|최소값|    0 (시스템에 물리적으로 설치된 CPU수)|
|최대값|	2^32 -1|
|기본값|	0|

## CPU_PARALLEL

CPU당 생성할 스레드의 수를 지정한다. 만약 이 값이 2이고 cpu의 수가 2인 경우, 두개의 CPU마다 병렬 스레드가 2개씩 생성되므로 병렬처리 스레드의 수가 4가 된다. 이 값이 너무 큰 경우, 메모리가 빨리 소모될 수 있다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 -1|
|기본값|	1|

## DBS_PATH

마크베이스 서버의 기본 데이터가 저장될 경로를 지정한다. 기본값은 "?/dbs"로, $MACHBASE_HOME/dbs 를 의미한다.

||Value|
|-|----|
|기본값|	?/dbs|

## DEFAULT_LSM_MAX_LEVEL

LSM인덱스의 기본 레벨을 설정한다. 인덱스를 생성할 때 MAX_LEVEL값을 입력하지 않으면 이 값이 적용된다.

||Value|
|-|----|
|최소값|	0|
|최대값|	3|
|기본값|	2|

## DISK_BUFFER_COUNT

디스크 입출력을 위한 버퍼의 수를 지정한다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	16|

## DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스에 대한 체크포인트 주기를 설정한다. 너무 길게 설정할 경우, 인덱스 빌드에 오류가 발생할 수 있다.

||Value|
|-|----|
|최소값|	1 (sec)|
|최대값|    2^32 -1 (sec)|
|기본값|	120 (sec)|

## DISK_COLUMNAR_INDEX_FDCACHE_COUNT

오픈한 인덱스 파티션 파일 디스크립터의 수를 지정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 -1|
|기본값|	0|

## DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH

마크베이스 서버를 종료할 때, 인덱스 정보를 디스크에 모두 반영할 것인지를 설정한다. 이 값을 '1'로 설정하면 모든 인덱스 정보를 디스크에 반영하고 종료하므로 종료시 대기 시간이 길어질 수 있다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	0 (False)|

## DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE

페이지 캐쉬의 최대 크기를 설정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	2 * 1024 * 1024 * 1024|

## DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

테이블 데이터의 체크포인트 주기를 설정한다. 이 값이 너무 크면 재시작시 복구 시간이 매우 길어지고, 이 값이 너무 작으면 I/O가 자주 발생하여 전체 성능이 저하될 수 있다.

||Value|
|-|----|
|최소값|	1 (sec)|
|최대값|	2^32 -1 (sec)|
|기본값|	120 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT

테이블의 컬럼 데이터에 대한 오픈된 파일 설명자의 최대 수를 지정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	0|

## DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE

_ARRIVAL_TIME 컬럼에 설정되는 기본 MINMAX 캐쉬의 크기를 설정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	100 *1024 * 1024|

## DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

컬럼 파티션 파일의 자동 플러쉬 주기를 설정한다.

||Value|
|-|----|
|최소값|	0 (sec)|
|최대값|	2^32-1 (sec)|
|기본값|	60 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

파티션 파일을 디스크에 반영하는 주기를 설정한다. 파티션이 설정된 갯수보다 더 많은 데이터를 입력받으면 이 주기와 관계없이 디스크에 반영된다.

||Value|
|-|----|
|최소값|	0 (sec)|
|최대값|	2^32-1 (sec)|
|기본값|	3 (sec)|

## DISK_COLUMNAR_TABLE_COLUMN_PARTITION_PRECREATE_COUNT

테이블에 대해서 사용할 예정인 컬럼 파티션 객체의 사전 생성 수를 정의한다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32-1|
|기본값|	3|

## DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE

설정된 값 만큼 _ARRIVAL_TIME컬럼의 값이 감소하더라도 입력을 허용한다. 만약 0인 경우 _ARRIVAL_TIME컬럼 값의 최대값보다 작은 값이 입력되면 이는 오류로 처리된다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	1 (True)|


## DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE

시작시 복구를 위해서 사용되는 더블 라이트 파일이 한번에 증가하는 크기를 지정한다.

||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^32 - 1|
|기본값|	1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE

파일 생성시에 더블라이트 파일이 확보하는 용량을 지정한다.

||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^32 - 1|
|기본값|	2* 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE

컬럼 파티션을 위해서 확보하는 메모리의 블록 크기를 지정한다.

||Value|
|-|----|
|최소값|	1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	2* 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE

로그 테이블에 의하여 할당된 최대 메모리 크기를 지정한다. 만약 서버가 이 값 이상의 메모리를 할당하게 되면, 메모리 사용량이 이 값 이하로 줄어들 때 까지 메모리 할당이 대기하므로 성능이 저하된다. 이 값은 물리적 메모리의 50~80% 정도로 설정할 것을 추천한다.

||Value|
|-|----|
|최소값|	256 * 1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	8 * 1024 * 1024 * 1024|

## DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE

마크베이스 서버가 시작할 때, 메모리 할당에 의한 성능 저하를 막기 위해서 이 값 만큼 메모리를 사전 확보한다. 데이터 입력 버퍼로만 이 메모리를 사용하므로, 메모리가 충분할 경우에만 사용할 것을 추천한다.

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

컬럼 데이터 파일을 위한 메모리 사용량이 기준을 초과한 경우, 매 레코드 입력시에 다음의 대기 시간을 설정한다.

||Value|
|-|----|
|최소값|	0 (msec)|
|최대값|	2^32 - 1 (msec)|
|기본값|	1 (msec)|


## DISK_IO_THREAD_COUNT

데이터를 디스크에 기록하는 입출력 스레드의 수를 설정한다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 -1|
|기본값|	3|

## DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O를 실행할 경우, 데이터 파일에 대해서 fsync는 불필요하다. Direct I/O 를 사용할 경우 fsync를 사용하지 않도록 하면 데이터 I/O 성능을 향상시킬 수 있다 (0으로 설정).
Fsync를 수행하지 않아도 일반적 상황에서는 데이터 유실이 없으나 전원이 꺼지는 등의 장애 상황이 발생할 수 있는 경우에는 fsync를 수행하도록 설정해야 한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 DIRECT I/O 를 사용할 것인지를 설정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 DIRECT I/O 를 사용할 것인지 설정한다. 파일 시스템에 따라서 DIRECT I/O 지원하지 않는 경우(ex: ZFS), 0으로 설정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	1|

## DISK_TAG_AUTO_RECLAIM

TAG 데이터에 대해서 사용되지 않는 공간을 자동 확보할 것인지의 여부를 결정한다. 기본값인 1인 경우, 자동 공간 확보 기능이 동작하고 0 인 경우에는 동작하지 않으며 사용자가 ALTER TABLE문을 이용하여 해당 기능을 직접 수행해야 한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	1|

## DUMP_APPEND_ERROR

이 값을 1로 설정하면 Append API 가 실패한 경우 $MACHBASE_HOME/trc/machbase.trc 파일에 에러 내용을 기록한다.
이 상황에서 append 성능이 매우 저하될 수 있으므로 테스트용으로만 사용할 것을 권장한다.

사용자 application에서 에러를 검사하고 싶으면 SQLAppendSetErrorCallback API 를 사용하는 것이 도움이 된다.


||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## DUMP_TRACE_INFO

서버는 일정한 주기로 DBMS 시스템 상태 정보를 machbase.trc 파일에 주기적으로 기록하는데, 이 주기를 설정한다.
0으로 설정하면 기록하지 않는다.

||Value|
|-|----|
|최소값|	0 (sec)|
|최대값|	2^32 - 1 (sec)|
|기본값|	60 (sec)|

## DURATION_BEGIN

DURATION 절을 지정하지 않은 SELECT 문에 대해서 기본을 설정하는 duration 값 중 시작시점을 설정한다.
만약 60을 설정해 두었다면, 현재 시각에서 60초 이전의 데이터를 검색하게 된다.

기본값은 0으로 모든 데이터를 검색한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	0|

## DURATION_GAP
DURATION 절을 지정하지 않은 SELECT 문에 대해서 기본을 설정하는 duration 값 중 기간을 설정한다.

만약 60을 설정해 두었다면, 현재 시각에서 60초 동안의 데이터를 검색하게 된다.
DURATION_BEGIN 값도 60이라면, 현재 시각에서 60초 이전부터 60초 동안의 데이터를 검색하게 된다.
기본값은 0으로 모든 데이터를 검색한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	Non-zero|
|기본값|	0|

## FEEDBACK_APPEND_ERROR

Append API 실행시 오류가 발생하였을 경우, 오류 데이터를 클라이언트에 전송할지를 설정한다. 0이면 클라이언트에 오류 데이터를 전송하지 않으며 1이면 클라이언트에 오류 정보를 전송한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	1|

## GRANT_REMOTE_ACCESS

원격지에서 데이터베이스에 접근할 수 있는지를 결정한다. 0이면 원격지 접속이 차단된다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|    1 (True)|

## HTTP_THREAD_COUNT

마크베이스의 웹 서버가 사용할 스레드의 개수를 설정 가능하다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1024|
|기본값|    32|

## INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD

인덱스 빌드 스레드가 인덱싱 되지 않은 레코드의 수가 이 값 이상이 되면 인덱스를 추가하기 시작한다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	100000|

## INDEX_BUILD_THREAD_COUNT

인덱스 생성 스레드의 수를 지정한다. 0으로 설정되면 인덱스를 생성하지 않는다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|	3|

## INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX

인덱스당 최대 flush 요청 수를 지정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2 ^ 32 - 1|
|기본값|	3|

## INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT

LSM 인덱스 생성시에 필요없는 인덱스 파일의 삭제를 위한 스레드의 갯수를 지정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1024|
|기본값|	1|

## INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT

LSM 인덱스 생성을 위한 최대 메모리 사용량의 퍼센트로 설정한다. 이 퍼센트는 마크베이스가 사용하는 최대 메모리사용량 대비하여 설정된다. 메모리 사용량이 한도를 초과하면, LSM 파티션 병합은 중지된다.

||Value|
|-|----|
|최소값|	0|
|최대값|	100|
|기본값|	70|

## INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT

LSM 인덱스의 생성을 위한 병합 연산을 수행하는 스레드의 수를 결정한다.

||Value|
|-|----|
|최소값|	1|
|최대값|    1024|
|기본값|	3|

## LOOKUP_APPEND_UPDATE_ON_DUPKEY

Lookup 테이블에 Append 할 때 Primary Key가 중복일 경우 어떻게 처리할지 지정한다.

* 0 : Append 실패
* 1 : 해당 Primary Key 에 대해서 Row를 Update 한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## MAX_QPX_MEM

GROUP BY, DISTINCT, ORDER BY 절을 수행하기 위해서 질의처리기가  이용하는 메모리의 최대 양을 설정한다.
하나의 질의문이 이보다 큰 값으로 메모리를 사용하게 되면 질의는 취소된다. 이때, 에러메시지를 클라이언트에 전송하고, machbase.trc 파일에 관련 내용이 기록된다.

||Value|
||-|----|
|최소값|	1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	500 * 1024 * 1024|

## MEMORY_ROW_TEMP_TABLE_PAGESIZE

Volatile table및 lookup 테이블을 위한 임시 테이블 스페이스의 페이지 크기를 설정한다. Volatile 테이블 및 lookup 테이블의 레코드들은 페이지에 저장되므로 volatile을 위한 최대 레코드 크기보다 커야 한다.
페이지에 N개의 레코드를 입력하고 싶으면 이 값을 최대 레코드 크기 * N으로 설정해야 한다.

||Value|
|-|----|
|최소값|	8 * 1024|
|최대값|	2^32 - 1|
|기본값|	32 * 1024|

## PID_PATH

마크베이스 서버 프로세스의 PID파일이 기록되는 위치를 지정한다. 기본값은 "?/conf"이며 이는 $MACHBASE_HOME/conf 를 의미한다.

||Value|
|-|----|
|기본값|	?/conf|

|PID_PATH 값|	PID 파일 위치 경로|
|-|----|
|지정되지 않음|	$MACHBASE_HOME/conf/machbase.pid|
|?/test|	$MACHBASE_HOME/test/machbase.pid|
|/tmp|	/tmp/machbase.pid|

## PORT_NO

마크베이스 서버 프로세스가 클라이언트와 통신하기 위한 TCP/IP 포트를 지정한다. 기본값은 5656이다.

||Value|
|-|----|
|최소값|	1024|
|최대값|	65535|
|기본값|	5656|

## PROCESS_MAX_SIZE

마크베이스 서버 프로세스인 machbased 프로그램이 사용하는 최대 메모리 사이즈를 지정한다. 이 제한값 이상의 메모리를 사용하려고 하면 서버는 다음과 같이 동작하여 메모리의 사용량을 줄이려고 시도한다. 메모리 제한을 초과한 경우, 다음의 방법으로 메모리 사용량을 줄인다.

데이터 입력을 중지하거나 오류로 처리
인덱스 생성 속도를 떨어뜨림
이 경우, 성능이 매우 저하되므로, 메모리 과다 사용 원인을 찾아서 해결하여야 한다.

||Value|
|-|----|
|최소값|	1024 * 1024 * 1024|
|최대값|	2^64 - 1|
|기본값|	8 * 1024 * 1024 * 1024|

## QUERY_PARALLEL_FACTOR

병렬 질의 실행기의 실행 스레드의 수를 지정한다.

||Value|
|-|----|
|최소값|	1|
|최대값|	100|
|기본값|	8|

## ROLLUP_FETCH_COUNT_LIMIT

롤업 스레드가 한번에 패치해올 데이터양을 제한한다.

0으로 설정할 경우 제한이 없다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^32 - 1|
|기본값|	3000000|

## RS_CACHE_APPROXIMATE_RESULT_ENABLE

결과값 캐쉬의 추측 모드(approximate result mode)를 사용할지의 여부를 결정한다. 이 값이 1이면 결과값 캐쉬를 사용할 때, 추측 값을 얻고(매우 빠르지만 데이터가 부정확할 수 있다.) 0 이면 정확한 값을 얻는다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	0 (False)|

## RS_CACHE_ENABLE

결과값 캐쉬를 사용할 지의 여부를 결정한다.

||Value|
|-|----|
|최소값|	0 (False)|
|최대값|	1 (True)|
|기본값|	1 (True)|

## RS_CACHE_MAX_MEMORY_PER_QUERY

결과값 캐쉬가 사용할 메모리의 양을 설정한다. 특정 질의 결과의 메모리 사용량이 이 값을 초과하면, 해당 질의의 결과는 결과값 캐쉬에 저장되지 않는다.

||Value|
|-|----|
|최소값|	1024|
|최대값|	2^64 - 1|
|기본값|	16 * 1024 * 1024|

## RS_CACHE_MAX_MEMORY_SIZE

결과값 캐쉬의 최대 메모리 사용량을 지정한다.

||Value|
|-|----|
|최소값|	32 * 1024|
|최대값|	2^64 - 1|
|기본값|	512 * 1024 * 1024|

## RS_CACHE_MAX_RECORD_PER_QUERY

결과값 캐쉬에 저장되는 최대 레코드 갯수이다. 만약 질의의 결과 레코드의 수가 이 값 이상이면 해당 질의 결과값은 캐쉬에 저장하지 않는다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^64 - 1|
|기본값|	10000|

## RS_CACHE_TIME_BOUND_MSEC

특정 질의가 매우 빠르게 실행된 경우에는 그 결과값을 결과값 캐쉬에 저장하지 않는 것이 메모리 사용량을 줄일 수 있으므로 캐쉬에 저장하지 않는것이 좋다.

이 값은 어느 정도 빨리 실행된 질의를 캐쉬에 저장하지 않을지를 결정한다. 0으로 설정된 경우에는 모든 질의결과를 결과집합캐쉬에 저장한다.

||Value|
|-|----|
|최소값|	0 (msec)|
|최대값|	2^64 - 1 (msec)|
|기본값|	1000 (msec)|

## SHOW_HIDDEN_COLS

_ARRIVAL_TIME 컬럼은 기본 설정으로는 SELECT * FROM 질의에 의해서 표시되지 않는다. 그러나 이 값이 1로 설정된 경우에는 해당 컬럼을 표시한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	1|
|기본값|	0|

## TABLE_SCAN_DIRECTION

태그 테이블의 스캔 방향을 설정할 수 있다. 프로퍼티 값은 -1,0, 1중 택일이며 기본값은 0이다.


* -1 : 역방향 스캔
* 0  : Tag Table(정방향 스캔), Log Table(역방향 스캔)
* 1  : 정방향 스캔

||Value|
|-|----|
|최소값|	-1|
|최대값|	1|
|기본값|	0|

## TAGDATA_AUTO_META_INSERT
{{<callout type="info">}}
5.5 에서는 TAGDATA_AUTO_NAME_INSERT 이다. 값의 범위도 0/1 이다.
5.7 이하에서는 기본값이 1 이다.
{{</callout>}}

TAGDATA 테이블에 APPEND/INSERT 를 통해 데이터를 입력할 때, 일치하는 TAG_NAME 이 없을 경우 어떻게 처리할 것인지를 정한다.

* 0 : 입력이 실패한다.
* 1 : 입력을 원하는 TAG_NAME 값을 입력한다. 추가 메타데이터 컬럼이 존재할 경우, 해당 컬럼의 값은 모두 NULL 로 입력된다.
* 2 : 입력을 원하는 TAG_NAME 값과 함께, 추가 메타데이터 컬럼 값도 같이 입력한다.
APPEND 에서만 유효한 설정이며, INSERT 는 추가 메타데이터 컬럼 값을 입력할 수 없기 때문에 1과 같이 작동한다.
이 설정을 한 이후에는, APPEND 에서 반드시 메타데이터 컬럼 값까지 포함시킨 APPEND Parameter 로 입력해야 한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2|
|기본값|	2|

## TAG_TABLE_META_MAX_SIZE

TAGDATA Table 생성 시 Metadata 영역을 보관할 메모리의 최대 크기를 설정한다.

||Value|
|-|----|
|최소값|	1024*1024|
|최대값|	2^32-1|
|기본값|	100*1024*1024|

## TAG_PARTITION_COUNT

Tag 테이블을 구성하는 Key Value 테이블의 개수를 지정한다.

||Value|
|--|--|
|최소값| 1|
|최대값| 4|
|기본값| 1024 |

## TAG_DATA_PART_SIZE

Tag 데이터 저장공간의 파티션 크기를 결정한다.

||Value|
|--|--|
|최소값| 1048576 (1MB)|
|최대값| 1073741824 (1GB)|
|기본값| 16777216 (16MB) |

## TRACE_LOGFILE_COUNT

TRACE_LOGFILE_PATH에 생성되는 로그 트레이스 파일의 최대 수를 지정한다. 디스크 공간을 절약하기 위해서, 최대 개수 이상의 로그파일이 생성되면 가장 오래된 로그파일을 삭제한다.

로그 트레이스 파일의 최대 개수 이상의 로그파일이 생성되어 가장 오래된 파일이 삭제될 경우 삭제된 파일의 이름이 가장 최신의 로그파일로 저장이 된다.

||Value|
|-|----|
|최소값|	1|
|최대값|	2^32 - 1|
|기본값|	1000|

## TRACE_LOGFILE_PATH

로그 트레이스 파일들(machbase.trc, machadmin.trc, machsql.trc)의 경로를 설정한다.
이 파일들은 마크베이스의 시작, 종료, 실행시 내부 정보를 지속적으로 기록한다. 기본값인 ?/trc의 의미는 $MACHBASE_HOME/trc 를 의미한다.

||Value|
|-|----|
|기본값|	?/conf|

|TRACE_LOGFILE_PATH 값|	trc 디렉터리 위치|
|-|----|
|지정되지 않음|	$MACHBASE_HOME/trc/|
|?/test|	$MACHBASE_HOME/test/|
|/tmp|	/tmp/|

## TRACE_LOGFILE_SIZE

로그 트레이스 파일의 최대 크기를 설정한다. 만약 크기 이상의 데이터를 기록하여야 한다면, 신규로 log 파일을 생성할 것이다.


||Value|
|-|----|
|최소값|	10 * 1024 * 1024|
|최대값|	2^32 - 1|
|기본값|	10 * 1024 * 1024|

## UNIX_PATH

Unix domain socket 파일의 경로를 설정한다. 사용자가 설정하지 않았을 경우의 기본 값은 ?/conf/machbase-unix 이다.

||Value|
|-|----|
|기본값|	?/conf/machbase-unix|

## VOLATILE_TABLESPACE_MEMORY_MAX_SIZE

시스템의 모든 volatile, lookup 테이블의 메모리 사용량 총계의 한도를 설정한다.

||Value|
|-|----|
|최소값|	0|
|최대값|	2^64 - 1|
|기본값|	2 * 1024 * 1024 * 1024|
