---
layout : post
title : 'Virtual Table'
type: docs
---

Virtual Table은 마크베이스 서버의 다양한 운영 정보들을 테이블 형태로 표현하는 가상 테이블이다. 이 테이블들의 이름은 V$문자로 시작한다.

마크베이스 서버가 어떤 상태로 동작하고 있는지를 알기 위해서 이 데이터를 읽어서 저장해 두고 이용할 수 있다. 
추가로, 이 Virtual Table 을 다른 테이블들과 JOIN 연산을 통해서 다양한 정보를 얻을 수 있다.

Virtual Table 은 읽기 전용으로 사용자가 추가/삭제/갱신할 수 없다.

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
* [Result Cache](#result-cache)
  * [V$RS\_CACHE\_LIST](#vrs_cache_list)
  * [V$RS\_CACHE\_STAT](#vrs_cache_stat)
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
  * [V$STORAGE\_TAG\_CACHE\_OBJECTS](#vstorage_tag_cache_objects)
  * [V$STORAGE\_TAG\_TABLE\_FILES](#vstorage_tag_table_files)
  * [V$STORAGE\_TAG\_INDEX](#vstorage_tag_index)
* [Tag Rollup](#tag-rollup)
  * [V$ROLLUP](#vrollup)
* [Stream](#stream)
  * [V$STREAMS](#vstreams)
* [License](#license)
  * [V$LICENSE\_INFO](#vlicense_info)
  * [V$LICENSE\_STATUS](#vlicense_status)
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

## Session/System
### V$PROPERTY
---

서버에 설정된 프로퍼티 정보를 표시한다.

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

MACHBASE 서버에 접속된 세션 정보를 표시한다.

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
| SQL_LOGGING                        | 해당 세션의 Trace Log 에 메시지를 남길지 여부<br>Parsing, Validation, Optimization 단계에서 발생하는 에러를 남긴다.<br>DDL을 수행한 결과를 남긴다.<br>(위의 두 케이스 모두 남긴다) |
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

세션 메모리 정보를 표시한다.

| 컬럼 이름 | 설명          |
| ----- | ----------- |
| SID   | 세션 식별자      |
| ID    | 메모리 매니저 식별자 |
| USAGE | 사용 크기       |

### V$SESSTAT
---

세션의 통계 정보를 표시한다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| SID   | 세션 식별자    |
| ID    | 통계 정보 식별자 |
| VALUE | 통계 정보 값   |

### V$SESTIME
---

세션의 시간 정보를 표시한다.

| 컬럼 이름      | 설명             |
| ---------- | -------------- |
| SID        | 세션 식별자         |
| ID         | 수행 단위 식별자      |
| ACCUM_TICK | 누적 시간          |
| MAX_TICK   | (각 수행 중) 최대 시간 |

### V$SYSMEM
---

시스템의 메모리 정보를 표시한다.

| 컬럼 이름     | 설명           |
| --------- | ------------ |
| ID        | 메모리 매니저 식별자  |
| NAME      | 메모리 매니저 이름   |
| USAGE     | 현재 사용량       |
| MAX_USAGE | (기록된) 최대 사용량 |

### V$SYSSTAT
---

시스템의 통계 정보를 표시한다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| ID    | 통계 정보 식별자 |
| NAME  | 통계 정보 이름  |
| VALUE | 통계 정보 값   |

### V$SYSTIME
---

시스템의 시간 정보를 표시한다.

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

사용자가 현재 실행중인 쿼리문에 대한 정보를 표시한다.

| 컬럼 이름       | 설명                            |
| ----------- | ----------------------------- |
| ID          | 쿼리 식별자                        |
| SESS_ID     | 쿼리를 수행한 세션 식별자                |
| STATE       | 쿼리 상태                         |
| RECORD_SIZE | SELECT 구문 수행 중인 경우, 결과 레코드 크기 |
| QUERY       | 쿼리 구문                         |

### V$VERSION
---

MACHBASE 의 버전에 대한 정보를 표시한다.

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

## Result Cache
### V$RS_CACHE_LIST
---

결과 캐시 목록을 표시한다.

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

하나의 세션에서의 결과 캐시의 통계 정보를 표시한다.

| 컬럼 이름              | 설명                |
| ------------------ | ----------------- |
| CACHE_COUNT        | 결과 캐시의 개수         |
| CACHE_HIT          | 총 캐시 히트 횟수        |
| AGGR_HIT           | 집계 결과의 총 캐시 히트 횟수 |
| CACHE_REPLACED     | 캐시 교체 횟수          |
| CACHE_MEMORY_USAGE | 캐시로 사용된 메모리 크기    |

## Storage
### V$STORAGE
---

저장 시스템의 내부 정보를 표시한다.

| 컬럼 이름                     | 설명                                   |
| ------------------------- | ------------------------------------ |
| DC_TABLE_FILE_SIZE        | 디스크 컬럼 데이터의 총 용량                     |
| DC_INDEX_FILE_SIZE        | 인덱스 파일 데이터의 총 용량                     |
| DC_TABLESPACE_DWFILE_SIZE | 모든 컬럼데이터를 위한 DWFILE의 총 용량            |
| DC_KV_TABLE_FILE_SIZE     | TAGDATA 테이블의 파티션 테이블이 가지는 데이터파일 총 용량 |

### V$STORAGE_MOUNT_DATABASES
---

마운트 기능을 이용하여 마운트한 백업 데이터베이스의 정보를 표시한다.

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

Storage Manager 에서 읽은 결과를 캐싱한, 캐시 객체에 대한 종합 정보를 표시한다.

| 컬럼 이름     | 설명               |
| --------- | ---------------- |
| OBJ_COUNT | 결과집합 캐시 객체의 현재 수 |

### V$CACHE_OBJECTS
---

저장 시스템에서 읽은 결과를 캐싱한, 각 캐시 객체에 대한 정보를 표시한다.

| 컬럼 이름     | 설명             |
| --------- | -------------- |
| OID       | 객체식별자          |
| REF_COUNT | 참조 카운트         |
| FLAG      | (서버 내부 사용 플래그) |

### V$STORAGE_DC_TABLESPACES
---

저장 시스템의 테이블스페이스 정보를 표시한다.

| 컬럼 이름      | 설명                           |
| ---------- | ---------------------------- |
| NAME       | 테이블스페이스 이름                   |
| ID         | 테이블스페이스 식별자                  |
| FLAG       | 테이블스페이스 Property 를 나타내는 Flag |
| REF_COUNT  | 테이블스페이스 참조 횟수                |
| DISK_COUNT | 테이블스페이스에 속한 디스크 개수           |

### V$STORAGE_DC_TABLESPACE_DISKS
---

저장 시스템의 테이블스페이스 정보를 표시한다.

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

저장 시스템에서 운용하는 Double-write 파일 (DW File) 의 정보를 표시한다.

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

저장 시스템에서 운용하는 Page Cache 에 대한 정보를 표시한다.

| 컬럼 이름        | 설명                     |
| ------------ | ---------------------- |
| MAX_MEM_SIZE | Page Cache 의 최대 메모리 크기 |
| CUR_MEM_SIZE | Page Cache 의 현재 메모리 크기 |
| PAGE_CNT     | 캐싱된 페이지 개수             |
| CHECK_TIME   | 검사 시간                  |

### V$STORAGE_DC_PAGECACHE_LRU_LST
---

저장 시스템에서 운용하는 Page Cache 의 LRU List 에 대한 정보를 표시한다.

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

저장 시스템에서 사용 중인 스토리지의 사용량을 표시한다.

| 컬럼 이름       | 설명                                                     |
| ----------- | ------------------------------------------------------ |
| TOTAL_SPACE | $MACHBASE_HOME/dbs 디렉터리가 위치한 스토리지의 총 용량                |
| USED_SPACE  | $MACHBASE_HOME/dbs 디렉터리가 위치한 스토리지의 사용량                 |
| USED_RATIO  | 사용량 비율(%)                                              |
| RATIO_CAP   | 스토리지 사용량 한계. USED_RATIO이 이 한계에 도달하면 데이터 입력/인덱스 구축이 멈춤. |

### V$STORAGE_TABLES
---

테이블의 상세 정보를 표시한다.

| 컬럼 이름         | 설명                                                                                                                                                                                                         |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID            | 테이블의 ID                                                                                                                                                                                                    |
| TYPE          | 테이블 형태<br>Persistent: LOG 테이블과 TAG 테이블<br>Volatile: 휘발성(Volatile) 테이블<br>Key-Value: TAG 테이블의 부속 테이블                                                                                                        |
| STATUS        | 현재 상태<br>Creating...: CREATE TABLE로 테이블 생성 진행중<br>Normal: 정상<br>Predrop: DROP TABLE 명령 접수 상태<br>Dropping...: DROP TABLE 명령 수행 상태<br>Dropped: DROP TABLE 명령 완료 상태<br>Mounted: 백업된 데이터베이스를 mount 명령으로 불러온 상태 |
| STORAGE_USAGE | 해당 테이블이 스토리지에서 점유한 용량                                                                                                                                                                                      |

## Log Table
### V$STORAGE_DC_TABLES
---

Log Table 에 대한 내부 정보를 표시한다.

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

Log Table 에 대한 내부 정보를 표시한다.

| 컬럼 이름         | 설명          |
| ------------- | ----------- |
| TABLESPACE_ID | 테이블스페이스 식별자 |
| TABLE_ID      | 테이블 식별자     |
| COUNT         | 레코드 개수      |
| COLUMN_ID     | 컬럼 식별자      |

### V$STORAGE_DC_TABLE_COLUMNS
---

Log Table 의 컬럼에 대한 정보를 표시한다.

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

Log Table 의 컬럼 파티션 정보를 표시한다.

| 컬럼 이름                         | 설명                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| TABLE_ID                      | 테이블 식별자                                                                            |
| DATABASE_ID                   | 데이터베이스 식별자                                                                         |
| COLUMN_ID                     | 컬럼 식별자                                                                             |
| ID                            | 파티션 식별자                                                                            |
| FLAG                          | 컬럼 Property 를 나타내는 Flag                                                            |
| BEGIN_RID                     | 파티션에 저장된 최소 RID                                                                    |
| END_RID                       | 파티션에 저장된 최종 RID                                                                    |
| END_SYNC_RID                  | SYNC가 끝난 최종 RID.<br>시작 RID 보다 크고 마지막 SYNC RID 보다 작은 RID 를 갖는 데이터는 파티션 파일에 기록되어 있다. |
| MIN_TIME                      | 컬럼 파티션에 최초로 데이터를 입력한 시간                                                            |
| MAX_TIME                      | 컬럼 파티션에 마지막으로 데이터를 입력한 시간                                                          |
| MAX_VALUE_COUNT_PER_PARTITION | 파티션의 최대 데이터 수                                                                      |
| MAX_VALUE_COUNT_PER_PAGE      | 페이지당 최대 데이터 수                                                                      |
| MAX_PAGE_COUNT                | 파티션당 최대 페이지의 수                                                                     |
| PAGE_SIZE                     | 컬럼 파티션에 저장된 페이지의 크기                                                                |
| PAGE_COUNT                    | 현재 컬럼 파티션에 생성된 페이지의 수                                                              |
| COMPRESS_RATIO                | 컬럼 파티션의 압축률. 0이면 아직 데이터 압축이 실행되지 않은 경우이다.                                          |
| DISK_FILENAME                 | 파티션 파일의 이름                                                                         |
| EXTERNAL_PART_SIZE            | 데이터의 양이 큰 값은 외부 파티션 파일에 기록하는데, 그 파일의 크기를 표시                                        |
| MIN_VALUE                     | 컬럼 파티션의 최소값                                                                        |
| MAX_VALUE                     | 컬럼 파티션의 최대값                                                                        |

### V$STORAGE_DC_TABLE_INDEXES
---

Log Table 에 생성된 인덱스 정보를 표시한다.

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

LSM Index 파티션에 대한 정보를 표시한다.

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

LSM Index 파티션 캐시에 대한 정보를 표시한다.

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

LSM 인덱스의 레벨에 관한 정보를 표시한다.

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

LSM Index 를 구성하는 파일에 대한 정보를 표시한다.

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

LSM Index 의 삭제를 담당하는 Ager 의 작업 상태를 표시한다.

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

Volatile Table 에 대한 정보를 표시한다.

| 컬럼 이름        | 설명                          |
| ------------ | --------------------------- |
| MAX_MEM_SIZE | Volatile Tablespace 의 최대 크기 |
| CUR_MEM_SIZE | Volatile Tablespace 의 현재 크기 |

## Tag Table
### V$STORAGE_TAG_TABLES
---

Tagdata Table 의 파티션 테이블에 대한 정보를 표시한다.

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
| INDEX_STATE          | 현재 인덱스 구축 상태<br>IDLE: 구축 완료, 대기중.<br>PROGRESS: 구축 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됨. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료                |
| DELETE_STATE         | 현재 DELETE 연산의 상태. DELETE 명령이 들어올 때에만 수행되므로 IDLE이 없다.<br>PROGRESS: 삭제 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기/쓰기 잠금 대기중<br>SHUTDOWN: 정지됨. DELETE 연산이 진행되지 않음.<br>ABNORMAL: 비정상 종료 |
| SAVE_STATE           | 현재 테이블 저장 연산의 상태.<br>IDLE: 저장 완료, 대기중.<br>PROGRESS: 저장 진행중<br>IOWAIT: 스토리지에 입출력 연산 대기.<br>PENDING: 테이블에 읽기 잠금 대기중<br>SHUTDOWN: 정지됨. DELETE 연산, 혹은 DROP 연산 진행중.<br>ABNORMAL: 비정상 종료           |

### V$STORAGE_TAG_CACHE
---

Tagdata Table 의 파티션 테이블에서 사용하는 캐시 정보를 표시한다.

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

### V$STORAGE_TAG_CACHE_OBJECTS
---

Tagdata Table의 파티션 테이블에서 사용하는 각각의 캐시 블럭에 대한 상세정보를 표시한다.

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

Tagdata Table 의 파티션 테이블의 파일 정보를 표시한다.

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

Tagdata Table 에 생성된 인덱스 정보를 표시한다.

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

Tagdata 테이블의 Rollup 정보를 표시한다.

| 컬럼 이름             | 설명                                  |
| ----------------- | ----------------------------------- |
| ID                | Rollup 작업 ID                        |
| ROLLUP_TABLE      | Rollup 이 저장할 테이블 이름                 |
| SOURCE_TABLE      | Rollup 이 조회할 테이블 이름                 |
| USER_ID           | Rollup Table과 Source Table의 User ID |
| ROOT_TABLE        | 최상위 Source Table 이름                 |
| INTERVAL          | Rollup의 실행 주기 (sec)                 |
| ENABLED           | Rollup 진행 여부를 나타냄                   |
| END_RID           | Source Table의 마지막 RID               |
| LAST_ELAPSED_MSEC | 최근에 진행했던 Rollup의 경과 시간              |

## Stream
### V$STREAMS
---

Stream 정보를 표시한다.

| 컬럼 이름        | 설명                                                                          |
| ------------ | --------------------------------------------------------------------------- |
| NAME         | 서버에 등록된 stream질의의 이름. 서버내에서 유일해야 함.                                         |
| LAST_EX_TIME | 해당 STREAM질의가 마지막으로 수행된 시간                                                   |
| TABLE_NAME   | STREAM질의의 검색 대상 테이블 이름                                                      |
| END_RID      | STREAM 질의가 마지막으로 읽어 들인 RID                                                  |
| STATE        | STREAM질의의 현재 상태                                                             |
| QUERY_TXT    | 사용자가 입력한 STREAM질의의 원본                                                       |
| ERROR_MSG    | 마지막으로 실행했을 때의 에러 메시지                                                        |
| FREQUENCY    | 질의 수행의 최소 대기 시간. 0이면 매 레코드마다 실행되며 0이 아니면 해당 시간이 지날 때 마다 수행된다.<br>단위는 나노초이다. |

## License
### V$LICENSE_INFO
---

라이선스 정보를 표시한다.

| 컬럼 이름            | 설명                     |
| ---------------- | ---------------------- |
| INSTALL_DATE     | 설치일                    |
| TYPE             | 라이선스 유형                |
| POLICY           | 라이선스 정책 유형             |
| CUSTOMER         | 고객사 이름                 |
| ISSUE_DATE       | 발행일                    |
| ID               | 호스트 ID                 |
| EXPIRY_DATE      | 만료일                    |
| SIZE_LIMIT       | 일 입력제한량                |
| ADDENDUM         | 추가 데이터 비율              |
| VIOLATION_ACTION | 위반 시 행동                |
| VIOLATION_LIMIT  | 서비스가 중단될 위반 횟수 (매월 갱신) |
| STOP_ACTION      | 중단 행동                  |
| RESET_FLAG       | (서버 내부 사용)             |

### V$LICENSE_STATUS
---

라이선스 상태를 표시한다.

| 컬럼 이름               | 설명                   |
| ------------------- | -------------------- |
| USER_DATA_PER_DAY   | 하루에 입력할 수 있는 데이터 제한량 |
| PREVIOUS_CHECK_DATE | 직전 라이선스 검사일          |
| VIOLATION_COUNT     | 라이선스 위반 횟수           |
| STOP_ENABLED        | (제거됨)                |

## Mutex
### V$MUTEX
---

현재 뮤텍스 상태를 보여준다.

| 필드명            | 설명                         | 비고                                                                                                         |
| -------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| OBJECT         | 뮤텍스 객체의 주소                 |                                                                                                            |
| NAME           | 뮤텍스 생성시 부여한 이름             |                                                                                                            |
| TYPE           | 뮤텍스 타입                     | Mutex: pmuMutex<br>RW Mutex: pmuRWMutex                                                                    |
| OWNER          | 뮤텍스를 획득한 스레드의 ID           | Mutex: 뮤텍스를 획득한 스레드가 없으면 0.<br>RW Mutex w/ Read-Lock: 0<br>RW Mutex w/ Write-Lock: Write Lock을 획득한 스레드의 ID |
| LOCK_COUNT     | 뮤텍스를 획득한 스레드 개수            | RW Mutex는 2 이상이 될 수 있음.                                                                                    |
| PEND_COUNT     | 뮤텍스를 획득하려고 대기 중인 스레드 개수    | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| TRY_COUNT      | 뮤텍스를 획득하려고 시도한 회수          | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| CONFLICT_COUNT | 뮤텍스 획득에 실패한 회수             | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집                                                                          |
| WAIT_TICK      | 뮤텍스 획득 대기 시간의 총합           | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| WAIT_TICK_AVG  | 뮤텍스 획득 시도 후 성공까지의 평균 시간    | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| HELD_TICK      | 뮤텍스를 획득한 이후 해제할 때까지의 시간 총합 | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |
| HELD_TICK_AVG  | 뮤텍스 획득 이후 해제까지의 시간 평균      | TRACE_MUTEX_WAIT_STATUS=1일 때에만 수집<br>RW Mutex에는 기록하지 않음                                                    |

### V$MUTEX_WAIT_STAT
---

현재 대기중인 뮤텍스의 콜스택을 보여준다.

| 필드        | 설명                  | 비고                               |
| --------- | ------------------- | -------------------------------- |
| THREAD_ID | 뮤텍스 획득 대기 중인 스레드 ID |                                  |
| OBJECT    | 획득 시도 중인 뮤텍스의 주소    | V$MUTEX의 OBJECT와 동일              |
| DEPTH     | 호출 깊이               | TRACE_MUTEX_WAIT_STACK=1일 때에만 수집 |
| SYMBOL    | 뮤텍스 획득을 호출한 함수의 심볼  | TRACE_MUTEX_WAIT_STACK=1일 때에만 수집 |

## Cluster

### V$NODE_STATUS
---

Cluster 각 Node 의 상태를 표시한다. 1건만 표시된다.

| 컬럼 이름    | 설명                                                            |
| -------- | ------------------------------------------------------------- |
| NODETYPE | Node 의 유형. 쿼리로 조회 가능한 Type 은 두 가지 뿐이다.<br>Broker<br>Warehouse |
| STATE    | Node 의 상태                                                     |

### V$DDL_INFO
---

Cluster 에서 수행한 DDL 정보를 표시한다.

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

Replication 작동에 대한 정보를 표시한다.

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

Replication 작동 시, Sender 의 정보를 표시한다.

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

Replication 작동 시, Sender 의 메타데이터를 표시한다.

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

Replication 작동 시, Receiver 의 정보를 표시한다.

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

Replication 작동 시, Receiver 의 메타데이터를 표시한다.

| 컬럼 이름      | 설명                                 |
| ---------- | ---------------------------------- |
| HOSTNAME   | Replication 이 작동되는 Node 의 Hostname |
| TABLE_ID   | 대상 테이블 식별자                         |
| TABLE_TYPE | 대상 테이블 유형                          |
| BEGIN_RID  | 대상 레코드의 시작 RID                     |
| END_RID    | 대상 레코드의 끝 RID                      |

### V$REPL_READER
---

Replication 작동 시, Reader 의 정보를 표시한다.

| 컬럼 이름       | 설명                                 |
| ----------- | ---------------------------------- |
| HOSTNAME    | Replication 이 작동되는 Node 의 Hostname |
| SENDER_ID   | Sender 식별자                         |
| ID          | Reader 식별자                         |
| STATUS      | Reader Thread의 작동상태                |
| FETCH_COUNT | FETCH 수행 횟수                        |

### V$REPL_READER_META
---

Replication 작동 시, Reader 의 메타데이터를 표시한다.

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

Replication 작동 시, Writer 의 정보를 표시한다.

| 컬럼 이름        | 설명                                 |
| ------------ | ---------------------------------- |
| HOSTNAME     | Replication 이 작동되는 Node 의 Hostname |
| ID           | Writer 식별자                         |
| STATUS       | Writer Thread 의 작동상태               |
| APPEND_COUNT | APPEND 수행 횟수                       |

### V$REPL_WRITER_META
---

Replication 작동 시, Writer 의 메타데이터를 표시한다.

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

V$로 시작하는 모든 Virtual Table 을 표시한다.

| 컬럼 이름       | 설명           |
| ----------- | ------------ |
| NAME        | 테이블 이름       |
| TYPE        | 테이블 유형       |
| DATABASE_ID | 데이터베이스 식별자   |
| ID          | 테이블 식별자      |
| USER ID     | 테이블을 생성한 사용자 |
| COLCOUNT    | 컬럼의 갯수       |

### V$COLUMNS
---

Virtual Table 의 컬럼 정보를 표시한다.

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

RETENTION POLICY가 적용된 테이블 정보를 표시한다.

| 컬럼 이름         | 설명                                     |
|-------------------|------------------------------------------|
| USER_NAME         | 사용자 이름                              |
| TABLE_NAME        | 대상 TAG TABLE 이름                      |
| POLICY_NAME       | 적용되어 있는 POLICY 이름                |
| STATE             | RETENTION 상태 (RUNNING/WAITING/STOPPED) |
| LAST_DELETED_TIME | 마지막으로 삭제된 시간                   |
