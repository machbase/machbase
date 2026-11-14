---
type: docs
title: '16.3.5 Complete Virtual Table Reference'
weight: 80
toc: true
tocSort: true
---

Virtual tables are read-only tables that expose Machbase server operational information. Their names
start with `V$`. Use them to inspect server status or JOIN them with other tables to analyze
operational data. INSERT, UPDATE, and DELETE are not supported.

## Contents

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
  * [V$DATABASES](#vdatabases)
  * [V$DATABASE_OPERATIONS](#vdatabase_operations)
  * [V$NEO\_SESSION](#vneo_session)
  * [V$NEO\_STMT](#vneo_stmt)
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

Displays server property settings.

| Column | Description |
| ----- | ------------ |
|NAME|Property name|
|VALUE|Property value|
|TYPE|Data type|
|DEFLT|Default value|
|MIN|Minimum set value|
|MAX|Maximum set value|

### V$SESSION
---

Displays sessions connected to the Machbase server.

| Column | Description |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
|HOSTNAME (Cluster Only)|Name of the HOST which the session is connected.|
|ID|Session identifier|
|CLOSED|Whether connection is closed|
|USER_ID|User identifier|
|LOGIN_TIME|Connection time|
|CLIENT_TYPE|Connected client type|
|USER_NAME|User name|
| CURRENT_DB_ID | Current logical database identifier for the session |
| CURRENT_DB_NAME | Current database name for the session |
|USER_IP|User IP address|
| SQL_LOGGING | Whether to write messages to the session trace log.<br>Logs errors during parsing, validation, and optimization.<br>Logs DDL execution results.<br>(Includes both cases above) |
|SHOW_HIDDEN_COLS|Whether hidden columns are shown upon SELECT|
| FEEDBACK_APPEND_ERROR | Whether to fail immediately when an APPEND error is detected |
|DEFAULT_DATE_FORMAT|Default input format upon Datetime input |
|MAX_QPX_MEM|Maximum memory size available when performing query|
|IDLE_TIMEOUT|Terminate the session if the client does nothing for that time after the session connected.|
|QUERY_TIMEOUT|Response waiting time for query execution|
| DDL_LOCK_TIMEOUT (Standard Only) | Wait for a conflicting DDL lock, in seconds. `0` returns an error immediately. |
| TRANSACTION_BUSY_TIMEOUT_MS | Wait for a TRANSACTION write conflict, in milliseconds. `-1` waits indefinitely; `0` returns an error immediately. |

### V$SESMEM
---

Displays session memory information.

| Column | Description |
| ----- | ----------- |
|SID|Session identifier|
|ID|Memory manager identifier|
|USAGE|Usage size|

### V$SESSTAT
---

Displays session statistics.

| Column | Description |
| ----- | --------- |
|SID|Session identifier|
|ID|Statistical information identifier|
|VALUE|Statistical information value|

### V$SESTIME
---

Displays session timing information.

`ACCUM_MSEC` and `MAX_MSEC` are `DOUBLE` values in milliseconds.

| Column | Description |
| ---------- | -------------- |
|SID|Session identifier|
|ID|Performance unit identifier|
| ACCUM_MSEC | Accumulated time |
| MAX_MSEC | Maximum time per operation |

### V$SYSMEM
---

Displays system memory information.

| Column | Description |
| --------- | ------------ |
|ID|Memory manager identifier|
|NAME|Memory manager name|
|USAGE|Current usage|
|MAX_USAGE|(Recorded) Maximum usage|

### V$SYSSTAT
---

Displays system statistics.

| Column | Description |
| ----- | --------- |
|ID|Statistical information identifier|
|NAME|Statistical information name|
|VALUE|Statistical information value|

### V$SYSTIME
---

Displays system timing information.

`ACCUM_MSEC`, `AVG_MSEC`, `MIN_MSEC`, and `MAX_MSEC` are `DOUBLE` values in milliseconds.

| Column | Description |
| ---------- | -------------- |
|ID|Performance unit identifier|
|NAME|Performance unit name|
| ACCUM_MSEC | Accumulated time |
| AVG_MSEC | Average time per operation |
| MIN_MSEC | Minimum time per operation |
| MAX_MSEC | Maximum time per operation |
|COUNT|Performance frequency|

### V$STMT
---

Displays information about queries currently running for users.

| Column | Description |
| ----------- | ----------------------------- |
|ID|Query identifier|
|SESS_ID|Performed query session identifier|
|STATE|Query status|
|RECORD_SIZE|Resulting record size of select statements|
|QUERY|Query statement|

### V$VERSION
---

Displays Machbase version information.

| Column | Description |
| ------------------------- | ---------------------------------------- |
|BINARY_DB_MAJOR_VERSION|Database major version|
|BINARY_DB_MINOR_VERSION|Database minor version|
|BINARY_META_MAJOR_VERSION|META major version|
|BINARY_META_MINOR_VERSION|META minor version|
|BINARY_CM_MAJOR_VERSION|Client (Communication Level) major version|
|BINARY_CM_MINOR_VERSION|Client (Communication Level) minor version|
| BINARY_SIGNATURE | Version name of the database server binary |
|FILE_DB_MAJOR_VERSION|File DB major version|
|FILE_DB_MINOR_VERSION|File DB minor version|
|FILE_META_MAJOR_VERSION|File META major version|
|FILE_META_MINOR_VERSION|File META minor version|
|FILE_CM_MAJOR_VERSION|File Client (Communication Level) major version|
|FILE_CM_MINOR_VERSION|File Client (Communication Level) minor version|
|FILE_CREATE_TIME|File creation time|
|EDITION|Machbase type|

### V$DATABASES
---

Displays the status of logical active databases and mounted databases. `DATABASE_ID` is a logical
catalog identifier and differs from the physical `TABLESPACE_ID`.

| Column | Description |
|-----------|------|
| DATABASE_ID | Logical database identifier |
| SOURCE_DATABASE_ID | Source database identifier of a mounted backup |
| NAME | Database name or mount alias |
| KIND | `ACTIVE` or `MOUNTED` |
| ACCESS_MODE | `READ_WRITE` or `READ_ONLY` |
| CAN_USE | Whether the database can be selected with `USE` |
| STATE | Lifecycle state |
| IS_DEFAULT | Whether this is the default `MACHBASEDB` |

```sql
SELECT database_id, name, kind, access_mode, can_use, state, is_default
  FROM v$databases
 ORDER BY database_id;
```

### V$DATABASE_OPERATIONS
---

Displays database lifecycle operation status and errors.

| Column | Description |
|-----------|------|
| OPERATION_ID | Operation identifier |
| DATABASE_ID | Target logical database identifier |
| DATABASE_NAME | Target database name |
| STATE | Operation state |
| LAST_ERROR | Failure cause |
| CREATED_AT | Creation timestamp |
| UPDATED_AT | Last update timestamp |

```sql
SELECT operation_id, database_name, state, last_error
  FROM v$database_operations
 ORDER BY operation_id DESC;
```

### V$NEO_SESSION
---

Displays session status for Neo protocol clients.

| Column | Description |
| -- | -- |
|ID|Session identifier|
|USER_ID|User identifier|
|USER_NAME|User name|
|STMT_COUNT|Statement count in the session|
|DISCONN_FLAG|Disconnect flag|

### V$NEO_STMT
---

Displays statement status for Neo protocol clients.

| Column | Description |
| -- | -- |
|ID|Statement identifier|
|SESS_ID|Session identifier|
|STATE|Statement state|
|QUERY|Statement text|
|APPEND_SUCCESS_CNT|Append success count|
|APPEND_FAILURE_CNT|Append failure count|

## PVO Statement Cache
Displays global PVO Statement Cache status, available only in Standard Edition.

### V$PVO_CACHE_STAT
---

Displays overall PVO Statement Cache statistics.

| Column | Description |
| -- | -- |
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

Displays details for each SQL statement stored in PVO Statement Cache.

| Column | Description |
| -- | -- |
|TOUCH_TIME|Last touch time|
|USER_ID|Owner user identifier|
|QUERY|Original SQL text|
| DEFAULT_DATE_FORMAT | Date format at execution time |
| TIMEZONE_OFFSET | Timezone offset at execution time |
|SHOW_HIDDEN_COLS|Whether hidden columns are shown|
|QUERY_PARALLEL_FACTOR|Parallel execution factor|
|HANDLE_COUNT|Number of cached plans|
|BUSY_COUNT|Number of handles currently in use|
|HIT_COUNT|Cache hit count|
|BUILD_IN_PROGRESS|Whether a build is in progress|

## Storage
### V$STORAGE
---

Displays storage system internals.

| Column | Description |
| ------------------------- | ------------------------------------ |
|DC_TABLE_FILE_SIZE|Total capacity of disk column data|
|DC_INDEX_FILE_SIZE|Total capacity of index file data|
|DC_TABLESPACE_DWFILE_SIZE|Total capacity of DWFILE for all column data|
| DC_KV_TABLE_FILE_SIZE | Total data file size of TAGDATA partition tables |

### V$STORAGE_MOUNT_DATABASES
---

Displays backup databases mounted with the mount feature.

| Column | Description |
| ----------------- | ---------------------- |
|NAME|Mounted database name|
|PATH|Backup file location|
|BACKUP_TBSID|Backup database tablespace identifier|
|BACKUP_SCN|Backup database identifier|
| MOUNTDB | Database alias specified when mounting |
|DB_BEGIN_TIME|Backup database first entry time|
|DB_END_TIME|Backup database last entry time|
|BACKUP_BEGIN_TIME|Backup begin time|
|BACKUP_END_TIME|Backup end time|
|FLAG|Property flag|

### V$CACHE
---

Displays aggregate information about objects that cache results read by the Storage Manager.

| Column | Description |
| --------- | ---------------- |
|OBJ_COUNT|Current number of result set cache objects|

### V$CACHE_OBJECTS
---

Displays each object that caches results read from the storage system.

| Column | Description |
| --------- | -------------- |
|OID|Object identifier|
|REF_COUNT|Reference count|
|FLAG|(Internal server use flag)|

### V$STORAGE_DC_TABLESPACES
---

Displays storage system tablespace information.

| Column | Description |
| ---------- | ---------------------------- |
|NAME|Tablespace name|
|ID|Tablespace identifier|
|FLAG|Flag indicating tablespace property|
|REF_COUNT|Tablespace reference count|
|DISK_COUNT|Tablespace disk count|

### V$STORAGE_DC_TABLESPACE_DISKS
---

Displays storage system tablespace information.

| Column | Description |
| ------------------ | ------------------- |
|NAME|Disk name|
|ID|Disk identifier|
|TABLESPACE_ID|Disk tablespace identifier|
|PATH|Disk path|
|IO_THREAD_COUNT|I/O Thread count|
|IO_JOB_COUNT|I/O Job count|
|VIRTUAL_DISK_COUNT|Virtual disk count|

### V$STORAGE_DC_DWFILES
---

Displays doublewrite (DW) files managed by the storage system.

| Column | Description |
| -------------------- | ----------------------- |
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

Displays the page cache managed by the storage system.

| Column | Description |
| ------------ | ---------------------- |
|MAX_MEM_SIZE|Maximum memory size of Page Cache|
|CUR_MEM_SIZE|Current memory size of Page Cache|
|PAGE_CNT|Number of cached pages|
|CHECK_TIME|Check time|

### V$STORAGE_DC_PAGECACHE_LRU_LST
---

Displays the LRU list of the page cache managed by the storage system.

| Column | Description |
| ------------ | ------------------- |
|SIZE|Page size|
|REF_CNT|Reference count|
|PARTITION_ID|Partition identifier|
|OFFSET|Page Cache Offset|
|OBJECT_ID|Object identifier|
|LEVEL|Partition level|

### V$STORAGE_USAGE
---

Displays storage usage.

| Column | Description |
| ----------- | ------------------------------------------------------ |
|TOTAL_SPACE|Total storage capacity where the $MACHBASE_HOME/dbs directory is located|
|USED_SPACE|Total storage usage where the $MACHBASE_HOME/dbs directory is located|
|USED_RATIO|Percentage of usage(%)|
|RATIO_CAP|Storage usage limit. Data input/index construction stops when USED_RATIO reaches this limit.|

### V$STORAGE_TABLES
---

Displays table details.

| Column | Description |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|ID|Table ID|
| TYPE | Table type<br>Persistent: LOG and TAG tables<br>Volatile: Volatile tables<br>Key-Value: Auxiliary tables of TAG tables |
|STATUS|Current Status<br> - Creating...: Creating table by CREATE TABLE query<br> - Normal: normal<br> - Predrop: DROP TABLE query accepted<br> - Dropping...: DROP TABLE query processing<br> - Dropped: DROP TABLE query completed<br> - Mounted: The backed up database loaded with the MOUNT query|
|STORAGE_USAGE|Capacity occupied by the table in storage|

## Log Table
### V$STORAGE_DC_TABLES
---

Displays Log table internals.

| Column | Description |
| -------------------- | ------------------------------------------ |
|ID|Table identifier|
| TABLESPACE_ID | Tablespace identifier |
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

Displays Log table internals.

| Column | Description |
| ------------- | ----------- |
|TABLESPACE_ID|Tablespace identifier|
|TABLE_ID|Table identifier|
|COUNT|Record count|
|COLUMN_ID|Column identifier|

### V$STORAGE_DC_TABLE_COLUMNS
---

Displays Log table column information.

| Column | Description |
| ------------------------- | ------------------------------- |
|TABLE_ID|Table identifier|
| TABLESPACE_ID | Tablespace identifier |
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
| END_RID_FOR_DEFAULT_VALUE | Column values with RIDs below this value use the default value |
|DISK_FILE_SIZE|Total size of column partition data file for that column|
|MEMORY_TOTAL_SIZE|Memory size used by table|
|MEMORY_ALLOC_SIZE|Memory size allocated by table|

### V$STORAGE_DC_TABLE_COLUMN_PARTS
---

Displays Log table column partition information.

| Column | Description |
| ----------------------------- | ---------------------------------------------------------------------------------- |
|TABLE_ID|Table identifier|
| TABLESPACE_ID | Tablespace identifier |
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

Displays indexes created on Log tables.

| Column | Description |
| -------------------- | ---------------------------- |
|TABLE_ID|Table identifier|
| TABLESPACE_ID | Tablespace identifier |
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

Displays LSM index partition information.

| Column | Description |
| -------------------------- | --------------------------------------- |
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

Displays LSM index partition cache information.

| Column | Description |
| -------------------------- | --------------------------- |
|BEGIN_RID|First RID entered into partition|
|BITMAP_TABLE_PAGE_COUNT|Number of pages storing bitmap value|
|BITMAP_TABLE_SIZE|Total size of page storing bitmap value|
|END_RID|Last RID entered into partition + 1|
|INDEX_ID|Index identifier|
|KEY_VALUE_COUNT|Number of key values entered into partition|
|KEY_VALUE_TABLE_PAGE_COUNT|Number of pages storing key value|
|KEY_VALUE_TABLE_SIZE|Size of page storing key value|
|LEVEL|Index partition LSM level|
|MEMORY_SIZE|Memory usage|
|MEMORY_SIZE_RBTREE|Redblack Tree memory usage|
|META_PAGE_COUNT|Number of pages storing meta information|
|META_SIZE|Total size of page storing meta information|
|PARTITION_ID|Partition identifier|
|TABLE_ID|Index Table identifier|
|TABLESPACE_ID|Tablespace identifier|

### V$STORAGE_DC_LSMINDEX_LEVELS
---

Displays LSM index level information.

| Column | Description |
| -------------- | ---------------------- |
| TABLE_ID | Table identifier |
| TABLESPACE_ID | Tablespace identifier |
|INDEX_ID|Index identifier|
|LEVEL|Level|
|BEGIN_RID|First partition RID|
|END_RID|Last partition RID + 1|
|META_BEGIN_RID|RID at start time of recording meta information|
|META_END_RID|RID at end time of recording meta information|
|DELETE_END_RID|Maximum deleted RID + 1|

### V$STORAGE_DC_LSMINDEX_FILES
---

Displays files that make up LSM indexes.

| Column | Description |
| ------------ | --------------- |
|TABLE_ID|Table identifier|
| TABLESPACE_ID | Tablespace identifier |
|INDEX_ID|Index identifier|
|LEVEL|Index partition LSM level|
|PARTITION_ID|Partition identifier|
|BEGIN_RID|Partition first RID|
|END_RID|Partition last RID + 1|
|PATH|Index file location|

### V$STORAGE_DC_LSMINDEX_AGER_JOBS
---

Displays job status for the ager responsible for LSM index deletion.

| Column | Description |
| --------- | ------------------ |
|TABLE_ID|Table identifier|
|INDEX_ID|Index identifier|
|LEVEL|Index partition LSM level|
|BEGIN_RID|First partition RID|
|END_RID|Last partition RID + 1|
|STATE|Index Ager working status|

## Volatile Table
### V$STORAGE_DC_VOLATILE_TABLE
---

Displays Volatile table information.

| Column | Description |
| ------------ | --------------------------- |
|MAX_MEM_SIZE|Maximum Volatile Tablespace size|
|CUR_MEM_SIZE|Current Volatile Tablespace size|

## Tag Table
### V$STORAGE_TAG_TABLES
---

Displays partition tables of Tagdata tables.

| Column | Description |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
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
| DELETE_STATE | Current DELETE operation state. There is no IDLE state because this runs only when a DELETE command is received.<br>PROGRESS: Deletion in progress<br>IOWAIT: Waiting for storage I/O<br>PENDING: Waiting for a table read/write lock<br>SHUTDOWN: Stopped; no DELETE operation is running<br>ABNORMAL: Abnormal termination |
|SAVE_STATE|Current Table Save operation state.<br> - IDLE: Save Complete, waiting<br> - PROGRESS: Save in progress<br> - IOWAIT: Waiting for I/O operation in storage<br> - PENDING: Waiting for table read lock<br> - SHUTDOWN: Stopped. DELETE operation or DROP operation in progress.<br> - ABNORMAL: Abnormal end|
|VINDEX_STATE|Current VARCHAR Index Build State<br> - IDLE: Build Complete, waiting<br> - PROGRESS: Build in progress<br> - IOWAIT: Waiting for I/O operation in storage<br> - PENDING: Waiting for table read lock<br> - SHUTDOWN:  Stopped. DELETE operation or DROP operation in progress.<br> - ABNORMAL: Abnormal end|

### V$STORAGE_TAG_CACHE
---

Displays the cache used by Tagdata partition tables.

| Column | Description |
| ----------- | ------------------------ |
| POOL_ID | Cache pool identifier |
|CATEGORY|Type of object in cache|
|USED_MEMORY|Size of memory in use|
|BLOCK_COUNT|Data cache count|
|CACHE_HIT|Data cache hit count|
|CACHE_MISS|Data cache miss count|
| FLUSHOUT | Pages flushed out because of data cache conflicts |
| COLD_READ | Data pages read directly from storage |
| MEMORY_WAIT | Times data memory waited because of cache conflicts |
|IO_WAIT|Data read operation wait count|

### V$STORAGE_TAG_CACHE_BASE
---

Displays aggregate tag cache pool information.

| Column | Description |
| -- | -- |
|POOL_ID|Cache pool identifier|
|TOTAL_CACHE_MEMORY|Total cache memory|
|TOTAL_OBJECT_COUNT|Total cached object count|
|TOTAL_LRU_LOOP_COUNT|Total LRU loop count|

### V$STORAGE_TAG_CACHE_OBJECTS
---

Displays details for each cache block used by Tagdata partition tables.

| Column | Description |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
|CATEGORY|Object classification being cached|
| LATEST_HIT | Last access timestamp |
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

Displays files of Tagdata partition tables.

| Column | Description |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
|TABLE_ID|Table identifier|
|FILE_ID|File identifier|
|STATE|Index status<br> - COMPLETE: Data stored, index build complete<br> - INDEXING: Index build in progress<br> - FILLED: Data is full, waiting for Index build<br> - PARTIAL: Data not yet full, waiting for Index build|
|REF_COUNT|Number of sessions currently referencing the file|
|ROW_COUNT|Number of records stored in the file, including those that were deleted|
|DEL_COUNT|Number of records deleted from the file|
|MIN_DATE|Minimum datetime value of this data file.|
|MAX_DATE|Maximum datetime value of this data file.|

### V$STORAGE_TAG_INDEX
---

Displays indexes created on Tagdata tables.

| Column | Description |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
|TABLE_ID|Table identifier|
|INDEX_ID|Index identifier (if INDEX_ID is 4294967295 it is a default index that is created automatically when the tag table is created.)|
|INDEX_STATE|Current index build state<br> - IDLE: Build Complete, waiting<br> - INDEXING: Build in progress<br> - STORAGE FULL: Stopped because of disk full|
|DISK_INDEX_END_RID|Index end RID stored in storage|
| MEMORY_INDEX_END_RID | End RID of the index most recently applied to memory |
|TABLE_END_RID|Table end RID|

## Tag Rollup
### V$ROLLUP
---

Displays rollup information for Tagdata tables.

| Column | Description |
| -------------- | ------------------------------------------------------- |
| DATABASE_ID | Logical database identifier |
|ID|Rollup job ID|
|ROLLUP_TABLE|Name of the rollup table|
|SOURCE_TABLE|Source table name (TAG/ROLLUP)|
|COLUMN_NAME|Target value column aggregated by this rollup|
|ROOT_TABLE|Root source tag table name|
|USER_ID|Owner user ID|
| INTERVAL_TIME | Data aggregation interval in milliseconds |
| WAKEUP_INTERVAL | Rollup job execution interval in milliseconds |
|LAST_WAKEUP_TIME|Last time the rollup thread woke up|
|NEXT_WAKEUP_TIME|Next scheduled wakeup time|
|ENABLED|Whether the rollup is enabled (1/0)|
|END_RID|Source table end RID processed by this rollup|
|LAST_ELAPSED_MSEC|Elapsed time of the last rollup run (msec)|
| EXT_TYPE | EXTENSION flag |
|PREDICATE|Filter predicate for conditional rollups (NULL if none)|
|RUN_STATE|Current worker state: I=INIT, S=SLEEPING, R=RUNNING|

## License
### V$LICENSE_INFO
---

Displays license information.

| Column | Description |
| ---------------- | ---------------------- |
|ID|License ID|
|ISSUE_DATE|Issue date|
|TYPE|License type|
|CUSTOMER|Customer name|
|PROJECT|Project name|
|COUNTRY_CODE|Country code|
|INSTALL_DATE|Installation date|
|VIOLATE_STATUS|License violation status|
|VIOLATE_MSG|License violation message|

`V$LICENSE_STATUS` is not exposed by Standard 8.5.4 servers. Use `V$LICENSE_INFO` for license
fields available in Standard Edition.

## Mutex
### V$MUTEX
---

Displays current mutex status.

`WAIT_MSEC`, `WAIT_AVG_MSEC`, `HELD_MSEC`, and `HELD_AVG_MSEC` are `DOUBLE` values in milliseconds.

| Column | Description | Notes |
| -------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------- |
|OBJECT|Address of the mutex object| |
|NAME|The name given when creating the mutex| |
|TYPE|Mutex type| - Mutex: pmuMutex<br> - RW Mutex: pmuRWMutex|
|OWNER|ID of the thread that acquired the mutex| - Mutex: 0 if no thread acquired the mutex.<br> - RW Mutex w/ Read-Lock: 0<br> - RW Mutex w/ Write-Lock: ID of the thread that acquired the write lock.|
|LOCK_COUNT|Number of threads that acquired the mutex| - RW Mutex can be 2 or more.|
|PEND_COUNT|Number of threads waiting to acquire a mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
|TRY_COUNT|Number of attempts to acquire the mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
|CONFLICT_COUNT|Number of failed to acquire mutex| - Collect only when TRACE_MUTEX_WAIT_STATUS=1|
| WAIT_MSEC | Total time waiting to acquire the mutex | Collected only when TRACE_MUTEX_WAIT_STATUS=1<br>Not recorded for RW mutexes |
| WAIT_AVG_MSEC | Average time from an acquisition attempt to success | Collected only when TRACE_MUTEX_WAIT_STATUS=1<br>Not recorded for RW mutexes |
| HELD_MSEC | Total time from acquisition to release | Collected only when TRACE_MUTEX_WAIT_STATUS=1<br>Not recorded for RW mutexes |
| HELD_AVG_MSEC | Average time from acquisition to release | Collected only when TRACE_MUTEX_WAIT_STATUS=1<br>Not recorded for RW mutexes |

### V$MUTEX_WAIT_STAT
---

Displays call stacks currently waiting for mutexes.

| Column | Description | Notes |
| --------- | ------------------- | -------------------------------- |
|THREAD_ID|ID of the thread waiting to acquire the mutex| |
|OBJECT|Address of the mutex being acquired| - Same as OBJECT in V$MUTEX|
| DEPTH | Call stack depth | Collected only when TRACE_MUTEX_WAIT_STACK=1 |
| SYMBOL | Symbol of the function that requested mutex acquisition | Collected only when TRACE_MUTEX_WAIT_STACK=1 |

## Cluster

The following virtual tables are exclusive to Cluster Edition and are not exposed on Standard servers.
Before using them, check `V$TABLES` to confirm availability in the running edition.

### V$NODE_STATUS
---

Displays the status of a cluster node. Returns one row.

| Column | Description |
| -------- | ------------------------------------------------------------- |
|NODETYPE|Node type. There are two types that can be viewed by queries.<br> - Broker<br> - Warehouse|
|STATE|Node status|

### V$DDL_INFO
---

Displays DDL operations executed in the cluster.

| Column | Description |
| -------------- | ----------------------- |
|SEQUENCENUMBER|DDL sequence number|
|TIME|DDL execution time|
|VALUE|DDL query result value (Internal server use)|
|CLIENT|Client name|
|BROKER|Lead Broker Node name|
|USER|User name|
|SQL|DDL query value|

### V$REPLICATION
---

Displays replication operation information.

| Column | Description |
| ---------------- | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|MODE|(Internal server use)|
|STATE|Node status|
|ADDR|Replication Manager address|
|PORT_NO|Replication Manager port number|
|MAX_SENDER_COUNT|Maximum number of Senders that can be created|
|RUN_SENDER_COUNT|Maximum number of active Senders|

### V$REPL_SENDER
---

Displays sender information during replication.

| Column | Description |
| ------------------ | ---------------------------------- |
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

Displays sender metadata during replication.

| Column | Description |
| ---------- | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|SENDER_ID|Sender identifier|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|

### V$REPL_RECEIVER
---

Displays receiver information during replication.

| Column | Description |
| ------------------ | ---------------------------------- |
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

Displays receiver metadata during replication.

| Column | Description |
| ---------- | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|

### V$REPL_READER
---

Displays reader information during replication.

| Column | Description |
| ----------- | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|SENDER_ID|Sender identifier|
|ID|Reader identifier|
|STATUS|Reader operation status|
|FETCH_COUNT|FETCH count|

### V$REPL_READER_META
---

Displays reader metadata during replication.

| Column | Description |
| ---------- | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|SENDER_ID|Sender identifier|
|ID|Reader identifier|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|

### V$REPL_WRITER
---

Displays writer information during replication.

| Column | Description |
| ------------ | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|ID|Writer identifier|
|STATUS|Writer operational status|
|APPEND_COUNT|APPEND count|

### V$REPL_WRITER_META
---

Displays writer metadata during replication.

| Column | Description |
| ---------- | ---------------------------------- |
|HOSTNAME|Replication Node Hostname|
|ID|Writer identifier|
|TABLE_ID|Target table identifier|
|TABLE_TYPE|Target table type|
|BEGIN_RID|Target record start RID|
|END_RID|Target record end RID|

## Others
### V$TABLES
---

Lists all virtual tables with names starting with V$.

| Column | Description |
| ----------- | ------------ |
|NAME|Table name|
|TYPE|Table type|
|DATABASE_ID|Database identifier|
|ID|Table identifier|
|USER_ID|User who created table|
|COLCOUNT|Column count|

### V$COLUMNS
---

Displays virtual table column information.

| Column | Description |
| -------------------- | ---------- |
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

Displays tables with a RETENTION POLICY applied.

| Column | Description |
|-------------------|------------------------------------------|
| USER_NAME         | User name                              |
| TABLE_NAME        | applied table name                      |
| POLICY_NAME       | applied policy name                |
| STATE             | RETENTION state (RUNNING/WAITING/STOPPED) |
| LAST_DELETED_TIME | most recently deleted time                 |

### V$USER_AUTH_KEYS
---

Displays public keys registered for challenge authentication.

| Column | Description |
| -- | -- |
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
