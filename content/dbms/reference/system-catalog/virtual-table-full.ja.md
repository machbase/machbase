---
type: docs
title: '16.3.5 仮想テーブルの完全リファレンス'
weight: 80
toc: true
tocSort: true
---

Virtual Tableは、Machbaseサーバーの運用情報をテーブル形式で提供する読み取り専用の仮想テーブルで、名前は`V$`で始まります。サーバー状態の参照や、他のテーブルとのJOINによる運用データの分析に使用します。INSERT、UPDATE、DELETEはサポートしません。

## 目次

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

サーバーに設定されたプロパティ情報を表示します。

| 列名 | 説明 |
| ----- | ------------ |
| NAME | プロパティ名 |
| VALUE | プロパティ値 |
| TYPE | データ型 |
| DEFLT | デフォルト値 |
| MIN | 設定できる最小値 |
| MAX | 設定できる最大値 |

### V$SESSION
---

MACHBASEサーバーに接続したセッションの情報を表示します。

| 列名 | 説明 |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| HOSTNAME (Cluster Only) | セッションが接続したHOST名 |
| ID | セッション識別子 |
| CLOSED | 接続が閉じているかどうか |
| USER_ID | ユーザー識別子 |
| LOGIN_TIME | 接続時刻 |
| CLIENT_TYPE | 接続クライアントのタイプ |
| USER_NAME | ユーザー名 |
| CURRENT_DB_ID | セッションの現在の論理データベース識別子 |
| CURRENT_DB_NAME | セッションの現在のデータベース名 |
| USER_IP | ユーザーIP |
| SQL_LOGGING | 該当セッションのトレースログにメッセージを記録するかどうか<br>解析、検証、最適化段階のエラーを記録します。<br>DDLの実行結果を記録します。<br>（両方を記録します） |
| SHOW_HIDDEN_COLS | SELECTで隠し列を表示するかどうか |
| FEEDBACK_APPEND_ERROR | APPENDでエラーを検出したら即座に失敗させるかどうか |
| DEFAULT_DATE_FORMAT | Datetime取り込み時のデフォルト入力形式 |
| MAX_QPX_MEM | クエリ実行時に使用できる最大メモリサイズ |
| IDLE_TIMEOUT | 接続後、指定時間クライアントが何もしなければセッションを終了 |
| QUERY_TIMEOUT | クエリ実行時の応答待機時間 |
| DDL_LOCK_TIMEOUT (Standard Only) | 競合するDDLロックの待機時間（秒）。`0`は即座にエラーを返します。 |
| TRANSACTION_BUSY_TIMEOUT_MS | TRANSACTION書き込み競合の待機時間（ミリ秒）。`-1`は待機を続け、`0`は即座にエラーを返します。 |

### V$SESMEM
---

セッションのメモリ情報を表示します。

| 列名 | 説明 |
| ----- | ----------- |
| SID | セッション識別子 |
| ID | メモリマネージャー識別子 |
| USAGE | 使用サイズ |

### V$SESSTAT
---

セッションの統計情報を表示します。

| 列名 | 説明 |
| ----- | --------- |
| SID | セッション識別子 |
| ID | 統計情報識別子 |
| VALUE | 統計情報の値 |

### V$SESTIME
---

セッションの時間情報を表示します。

`ACCUM_MSEC`と`MAX_MSEC`はミリ秒単位の`DOUBLE`値です。

| 列名 | 説明 |
| ---------- | -------------- |
| SID | セッション識別子 |
| ID | 実行単位の識別子 |
| ACCUM_MSEC | 累積時間 |
| MAX_MSEC | 各実行の最大時間 |

### V$SYSMEM
---

システムのメモリ情報を表示します。

| 列名 | 説明 |
| --------- | ------------ |
| ID | メモリマネージャー識別子 |
| NAME | メモリマネージャー名 |
| USAGE | 現在の使用量 |
| MAX_USAGE | 記録された最大使用量 |

### V$SYSSTAT
---

システムの統計情報を表示します。

| 列名 | 説明 |
| ----- | --------- |
| ID | 統計情報識別子 |
| NAME | 統計情報名 |
| VALUE | 統計情報の値 |

### V$SYSTIME
---

システムの時間情報を表示します。

`ACCUM_MSEC`、`AVG_MSEC`、`MIN_MSEC`、`MAX_MSEC`はミリ秒単位の`DOUBLE`値です。

| 列名 | 説明 |
| ---------- | -------------- |
| ID | 実行単位の識別子 |
| NAME | 実行単位の名前 |
| ACCUM_MSEC | 累積時間 |
| AVG_MSEC | 各実行の平均時間 |
| MIN_MSEC | 各実行の最小時間 |
| MAX_MSEC | 各実行の最大時間 |
| COUNT | 実行回数 |

### V$STMT
---

ユーザーが現在実行しているクエリの情報を表示します。

| 列名 | 説明 |
| ----------- | ----------------------------- |
| ID | クエリ識別子 |
| SESS_ID | クエリを実行したセッションの識別子 |
| STATE | クエリ状態 |
| RECORD_SIZE | SELECT文の実行中の場合、結果レコードのサイズ |
| QUERY | クエリのテキスト |

### V$VERSION
---

MACHBASEのバージョン情報を表示します。

| 列名 | 説明 |
| ------------------------- | ---------------------------------------- |
| BINARY_DB_MAJOR_VERSION | DBメジャーバージョン |
| BINARY_DB_MINOR_VERSION | DBマイナーバージョン |
| BINARY_META_MAJOR_VERSION | METAメジャーバージョン |
| BINARY_META_MINOR_VERSION | METAマイナーバージョン |
| BINARY_CM_MAJOR_VERSION | Client（Communication Level）メジャーバージョン |
| BINARY_CM_MINOR_VERSION | Client（Communication Level）マイナーバージョン |
| BINARY_SIGNATURE | DBサーバーファイルのバージョン名 |
| FILE_DB_MAJOR_VERSION | File DBメジャーバージョン |
| FILE_DB_MINOR_VERSION | File DBマイナーバージョン |
| FILE_META_MAJOR_VERSION | File METAメジャーバージョン |
| FILE_META_MINOR_VERSION | File METAマイナーバージョン |
| FILE_CM_MAJOR_VERSION | File Client（Communication Level）メジャーバージョン |
| FILE_CM_MINOR_VERSION | File Client（Communication Level）マイナーバージョン |
| FILE_CREATE_TIME | ファイル作成時刻 |
| EDITION | MACHBASEの種類 |

### V$DATABASES
---

アクティブな論理データベースとマウント済みデータベースの状態を表示します。`DATABASE_ID`は論理
カタログ識別子であり、物理的な`TABLESPACE_ID`とは異なります。

| 列名 | 説明 |
| ----------- | ------ |
| DATABASE_ID | 論理データベース識別子 |
| SOURCE_DATABASE_ID | マウント済みバックアップの元のデータベース識別子 |
| NAME | データベース名またはマウントのエイリアス |
| KIND | `ACTIVE`または`MOUNTED` |
| ACCESS_MODE | `READ_WRITE`または`READ_ONLY` |
| CAN_USE | `USE`で選択できるかどうか |
| STATE | ライフサイクルの状態 |
| IS_DEFAULT | デフォルトの`MACHBASEDB`かどうか |

```sql
SELECT database_id, name, kind, access_mode, can_use, state, is_default
  FROM v$databases
 ORDER BY database_id;
```

### V$DATABASE_OPERATIONS
---

データベースのライフサイクル操作の状態とエラーを表示します。

| 列名 | 説明 |
| ----------- | ------ |
| OPERATION_ID | 操作識別子 |
| DATABASE_ID | 対象論理データベース識別子 |
| DATABASE_NAME | 対象データベース名 |
| STATE | 操作状態 |
| LAST_ERROR | 失敗原因 |
| CREATED_AT | 作成時刻 |
| UPDATED_AT | 最終変更時刻 |

```sql
SELECT operation_id, database_name, state, last_error
  FROM v$database_operations
 ORDER BY operation_id DESC;
```

### V$NEO_SESSION
---

Neoプロトコルクライアントのセッション状態を表示します。

| 列名 | 説明 |
| -- | -- |
| ID | セッション識別子 |
| USER_ID | ユーザー識別子 |
| USER_NAME | ユーザー名 |
| STMT_COUNT | セッションのステートメント数 |
| DISCONN_FLAG | 切断フラグ |

### V$NEO_STMT
---

Neoプロトコルクライアントのステートメント状態を表示します。

| 列名 | 説明 |
| -- | -- |
| ID | ステートメント識別子 |
| SESS_ID | セッション識別子 |
| STATE | ステートメント状態 |
| QUERY | ステートメントのテキスト |
| APPEND_SUCCESS_CNT | Append成功件数 |
| APPEND_FAILURE_CNT | Append失敗件数 |

## PVO Statement Cache
Standard Edition専用のグローバルなPVO Statement Cacheの状態を参照します。

### V$PVO_CACHE_STAT
---

PVO Statement Cacheの全体統計を表示します。

| 列名 | 説明 |
| -- | -- |
| CACHE_ENTRY_COUNT | キャッシュに格納されたSQLエントリー数 |
| CACHE_HANDLE_COUNT | 全SQLのキャッシュ済み計画（ハンドル）数 |
| CACHE_MEMORY_USAGE | 使用中のキャッシュメモリサイズ |
| CACHE_MAX_MEMORY_SIZE | 設定されたキャッシュメモリ上限 |
| CACHE_MAX_PLANS_PER_SQL | SQL当たりの最大許容計画数 |
| CACHE_MAX_SQL_ENTRIES | 最大許容SQLエントリー数（0は無制限） |
| CACHE_SHARD_COUNT | キャッシュのシャード数 |
| CACHE_HIT | キャッシュヒット回数 |
| CACHE_MISS | キャッシュミス回数 |
| SINGLEFLIGHT_WAIT | 同じSQLの同時構築を待機した回数 |
| BUILD_COUNT | 計画の構築試行回数 |
| BUILD_FAIL | 構築失敗回数 |
| INVALIDATE_COUNT | 無効化された計画数 |
| EVICT_COUNT | メモリ上限などによるキャッシュの追い出し回数 |
| FLUSH_COUNT | 明示的/内部フラッシュ回数 |

### V$PVO_CACHE_LIST
---

PVO Statement Cacheに保存されたSQL別の詳細情報を表示します。

| 列名 | 説明 |
| -- | -- |
| TOUCH_TIME | 最終アクセス時刻 |
| USER_ID | SQLを所有するユーザーID |
| QUERY | 元のSQLテキスト |
| DEFAULT_DATE_FORMAT | 実行時の日付形式 |
| TIMEZONE_OFFSET | 実行時のタイムゾーンオフセット |
| SHOW_HIDDEN_COLS | 隠し列を表示するかどうか |
| QUERY_PARALLEL_FACTOR | 並列実行係数 |
| HANDLE_COUNT | 保持する計画（ハンドル）数 |
| BUSY_COUNT | 同時に使用中のハンドル数 |
| HIT_COUNT | キャッシュヒット回数 |
| BUILD_IN_PROGRESS | 構築中かどうか |

## Storage
### V$STORAGE
---

ストレージシステムの内部情報を表示します。

| 列名 | 説明 |
| ------------------------- | ------------------------------------ |
| DC_TABLE_FILE_SIZE | ディスク上の列データの総容量 |
| DC_INDEX_FILE_SIZE | インデックスファイルデータの総容量 |
| DC_TABLESPACE_DWFILE_SIZE | 全列データ用DWFILEの総容量 |
| DC_KV_TABLE_FILE_SIZE | TAGDATAテーブルのパーティションテーブルが持つデータファイルの総容量 |

### V$STORAGE_MOUNT_DATABASES
---

マウント機能でマウントしたバックアップデータベースの情報を表示します。

| 列名 | 説明 |
| ----------------- | ---------------------- |
| NAME | マウント済みデータベース名 |
| PATH | バックアップファイルの場所 |
| BACKUP_TBSID | バックアップデータベースのテーブルスペース識別子 |
| BACKUP_SCN | バックアップデータベースの識別子 |
| MOUNTDB | MOUNT時に指定したデータベースのエイリアス |
| DB_BEGIN_TIME | バックアップデータベースの最初の取り込み時刻 |
| DB_END_TIME | バックアップデータベースの最後の取り込み時刻 |
| BACKUP_BEGIN_TIME | バックアップ実行の開始時刻 |
| BACKUP_END_TIME | バックアップ実行の終了時刻 |
| FLAG | プロパティフラグ |

### V$CACHE
---

Storage Managerで読み取った結果をキャッシュするオブジェクトの集計情報を表示します。

| 列名 | 説明 |
| --------- | ---------------- |
| OBJ_COUNT | 結果セットのキャッシュオブジェクトの現在数 |

### V$CACHE_OBJECTS
---

ストレージシステムで読み取った結果をキャッシュする各オブジェクトの情報を表示します。

| 列名 | 説明 |
| --------- | -------------- |
| OID | オブジェクト識別子 |
| REF_COUNT | 参照カウント |
| FLAG | サーバー内部用フラグ |

### V$STORAGE_DC_TABLESPACES
---

ストレージシステムのテーブルスペース情報を表示します。

| 列名 | 説明 |
| ---------- | ---------------------------- |
| NAME | テーブルスペース名 |
| ID | テーブルスペース識別子 |
| FLAG | テーブルスペースのプロパティを示すフラグ |
| REF_COUNT | テーブルスペースの参照回数 |
| DISK_COUNT | テーブルスペースに属するディスク数 |

### V$STORAGE_DC_TABLESPACE_DISKS
---

ストレージシステムのテーブルスペース情報を表示します。

| 列名 | 説明 |
| ------------------ | ------------------- |
| NAME | ディスク名 |
| ID | ディスク識別子 |
| TABLESPACE_ID | ディスクが属するテーブルスペースの識別子 |
| PATH | ディスクのパス |
| IO_THREAD_COUNT | I/Oスレッド数 |
| IO_JOB_COUNT | I/Oジョブ数 |
| VIRTUAL_DISK_COUNT | 仮想ディスク数 |

### V$STORAGE_DC_DWFILES
---

ストレージシステムが管理するダブルライトファイル（DW File）の情報を表示します。

| 列名 | 説明 |
| -------------------- | ----------------------- |
| TBS_ID | テーブルスペース識別子 |
| DISK_ID | ディスク識別子 |
| FILE | ファイルのパス |
| TABLE_ID | テーブル識別子 |
| COLUMN_ID | 列識別子 |
| PARTITION_ID | パーティション識別子 |
| PAGE_ID | ページ識別子 |
| DISK_OFFSET | ディスクオフセット |
| DISK_IMAGE_SIZE | ディスクイメージサイズ |
| HEAD_CRC32CODE_IMAGE | CRC32コードのヘッドイメージ |
| TAIL_CRC32CODE_IMAGE | CRC32コードのテールイメージ |
| CRC32CODE_PAGE | CRC32コードのページ |
| HEAD_TIMESTAMP_PAGE | タイムスタンプのヘッドページ |
| TAIL_TIMESTAMP_PAGE | タイムスタンプのテールページ |

### V$STORAGE_DC_PAGECACHE
---

ストレージシステムが管理するページキャッシュの情報を表示します。

| 列名 | 説明 |
| ------------ | ---------------------- |
| MAX_MEM_SIZE | ページキャッシュの最大メモリサイズ |
| CUR_MEM_SIZE | ページキャッシュの現在のメモリサイズ |
| PAGE_CNT | キャッシュされたページ数 |
| CHECK_TIME | 検査時刻 |

### V$STORAGE_DC_PAGECACHE_LRU_LST
---

ストレージシステムが管理するページキャッシュのLRUリストの情報を表示します。

| 列名 | 説明 |
| ------------ | ------------------- |
| SIZE | ページサイズ |
| REF_CNT | 参照回数 |
| PARTITION_ID | パーティション識別子 |
| OFFSET | ページキャッシュのオフセット |
| OBJECT_ID | オブジェクト識別子 |
| LEVEL | パーティションレベル |

### V$STORAGE_USAGE
---

ストレージシステムで使用中のストレージ使用量を表示します。

| 列名 | 説明 |
| ----------- | ------------------------------------------------------ |
| TOTAL_SPACE | $MACHBASE_HOME/dbsディレクトリがあるストレージの総容量 |
| USED_SPACE | $MACHBASE_HOME/dbsディレクトリがあるストレージの使用量 |
| USED_RATIO | 使用率（%） |
| RATIO_CAP | ストレージ使用量の上限。USED_RATIOがこの上限に達すると、取り込み/インデックス構築が停止します。 |

### V$STORAGE_TABLES
---

テーブルの詳細情報を表示します。

| 列名 | 説明 |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID | テーブルのID |
| TYPE | テーブルタイプ<br>Persistent: LOGテーブルとTAGテーブル<br>Volatile: Volatileテーブル<br>Key-Value: TAGテーブルの補助テーブル |
| STATUS | 現在の状態<br>Creating...: CREATE TABLEでテーブル作成中<br>Normal: 正常<br>Predrop: DROP TABLEコマンドを受け付けた状態<br>Dropping...: DROP TABLEコマンドの実行中<br>Dropped: DROP TABLEコマンドの完了<br>Mounted: バックアップデータベースをmountコマンドで読み込んだ状態 |
| STORAGE_USAGE | 該当テーブルがストレージ上で占有する容量 |

## Log Table
### V$STORAGE_DC_TABLES
---

Logテーブルの内部情報を表示します。

| 列名 | 説明 |
| -------------------- | ------------------------------------------ |
| ID | テーブルの識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| CREATE_SCN | 作成時のシステム変更番号（System Change Number） |
| UPDATE_SCN | 最終変更時のシステム変更番号（System Change Number） |
| DDL_REF_COUNT | DDL実行で該当テーブルを参照しているセッション数 |
| BEGIN_RID | テーブルの最小RID |
| END_RID | テーブルの最後のRow ID + 1 |
| BEGIN_META_RID | メタデータの記録開始時点のID |
| END_META_RID | メタデータの記録終了時点のID |
| END_SYNC_RID | ディスクに記録された最後のRow ID + 1 |
| FLAG | テーブルのプロパティを示すフラグ |
| COLUMN_COUNT | テーブルの列数 |
| INDEX_COUNT | テーブルのインデックス数 |
| INDEX_MIN_END_RID | インデックスに記録された最後のRID + 1 |
| LAST_ARRIVAL_TIME | 最後に記録された\_arrival_timeの値 |
| LAST_CHECKPOINT_TIME | 最後にチェックポイントを通過した時点 |
| TYPE | テーブルタイプ |

### V$STORAGE_DC_TABLES_STAT
---

Logテーブルの内部情報を表示します。

| 列名 | 説明 |
| ------------- | ----------- |
| TABLESPACE_ID | テーブルスペース識別子 |
| TABLE_ID | テーブル識別子 |
| COUNT | レコード数 |
| COLUMN_ID | 列識別子 |

### V$STORAGE_DC_TABLE_COLUMNS
---

Logテーブルの列情報を表示します。

| 列名 | 説明 |
| ------------------------- | ------------------------------- |
| TABLE_ID | テーブル識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| ID | 列識別子 |
| FLAG | プロパティフラグ |
| SIZE | 列のデータサイズ |
| PARTITION_VALUE_COUNT | パーティションに保存する最大データ数 |
| PAGE_VALUE_COUNT | ページに保存する最大データ数 |
| CACHE_VALUE_COUNT | キャッシュ値の最大数 |
| MINMAX_CACHE_SIZE | 列パーティションのMIN/MAXキャッシュの最大サイズ |
| CUR_APPEND_PARTITION_ID | 現在取り込み中のパーティション識別子 |
| CUR_CACHE_PARTITION_COUNT | 現在のキャッシュにデータを読み込んだパーティション数 |
| CUR_MINMAX_CACHE_SIZE | 現在のMIN/MAXキャッシュサイズ |
| END_RID_FOR_DEFAULT_VALUE | この値より小さいRIDを持つ列値にはデフォルト値を使用 |
| DISK_FILE_SIZE | 該当列の列パーティションデータファイルの合計サイズ |
| MEMORY_TOTAL_SIZE | テーブルが使用中のメモリサイズ |
| MEMORY_ALLOC_SIZE | テーブルに割り当てられたメモリサイズ |

### V$STORAGE_DC_TABLE_COLUMN_PARTS
---

Logテーブルの列パーティション情報を表示します。

| 列名 | 説明 |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| TABLE_ID | テーブル識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| COLUMN_ID | 列識別子 |
| ID | パーティション識別子 |
| FLAG | 列のプロパティを示すフラグ |
| BEGIN_RID | パーティションに保存された最小RID |
| END_RID | パーティションに保存された最後のRID |
| END_SYNC_RID | SYNCが完了した最後のRID。<br>開始RIDより大きく最後のSYNC RIDより小さいRIDを持つデータは、パーティションファイルに記録されています。 |
| MIN_TIME | 列パーティションに最初にデータを取り込んだ時刻 |
| MAX_TIME | 列パーティションに最後にデータを取り込んだ時刻 |
| MAX_VALUE_COUNT_PER_PARTITION | パーティションの最大データ数 |
| MAX_VALUE_COUNT_PER_PAGE | ページ当たりの最大データ数 |
| MAX_PAGE_COUNT | パーティション当たりの最大ページ数 |
| PAGE_SIZE | 列パーティションに保存されたページのサイズ |
| PAGE_COUNT | 現在の列パーティションに作成されたページ数 |
| COMPRESS_RATIO | 列パーティションの圧縮率。0はまだデータ圧縮を実行していないことを示します。 |
| DISK_FILENAME | パーティションファイル名 |
| EXTERNAL_PART_SIZE | 大きな値を記録する外部パーティションファイルのサイズ |
| MIN_VALUE | 列パーティションの最小値 |
| MAX_VALUE | 列パーティションの最大値 |

### V$STORAGE_DC_TABLE_INDEXES
---

Logテーブルに作成されたインデックス情報を表示します。

| 列名 | 説明 |
| -------------------- | ---------------------------- |
| TABLE_ID | テーブル識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| ID | インデックス識別子 |
| FLAG | インデックスのプロパティを示すフラグ |
| TABLE_BEGIN_RID | テーブルに取り込まれた最小RID |
| TABLE_END_RID | テーブルの最後のRID |
| BEGIN_RID | インデックスの最小RID |
| END_RID | インデックスの最大RID |
| END_SYNC_RID | ファイルに記録された最大RID+1 |
| COLUMN_COUNT | インデックスの列数 |
| BEGIN_PART_ID | インデックスの最初のパーティション識別子 |
| END_PART_ID | インデックスの最後のパーティション識別子 |
| FLUSH_REQUEST_COUNT | ディスクへの反映を要求されたインデックスパーティション数 |
| MAX_KEY_SIZE | 最大キーサイズ |
| INDEX_TYPE | インデックスタイプ |
| DISK_FILE_SIZE | 該当インデックスのパーティションファイルの合計サイズ |
| LAST_CHECKPOINT_TIME | 最後にチェックポイントを通過した時点 |

## LSM(Log Structured Merge) Index
### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS
---

LSMインデックスのパーティション情報を表示します。

| 列名 | 説明 |
| -------------------------- | --------------------------------------- |
| TABLE ID | インデックスが作成されたテーブルの識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| INDEX_ID | インデックス識別子 |
| LEVEL | インデックスパーティションのLSMレベル |
| PARTITION_ID | パーティション識別子 |
| BEGIN_RID | パーティションに取り込まれた最小RID |
| END_RID | パーティションに取り込まれた最大RID+1 |
| KEY_VALUE_COUNT | パーティションに取り込まれたキー値の数 |
| KEY_VALUE_TABLE_SIZE | キー値を保存するページのサイズ |
| KEY_VALUE_TABLE_PAGE_COUNT | キー値を保存するページ数 |
| MIN_KEY_VALUE | 最小キー値 |
| MAX_KEY_VALUE | 最大キー値 |
| BITMAP_TABLE_SIZE | ビットマップ値を保存するページの合計サイズ |
| BITMAP_TABLE_PAGE_COUNT | ビットマップ値を保存するページ数 |
| META_SIZE | メタデータを保存するページの合計サイズ |
| META_PAGE_COUNT | メタデータを保存するページ数 |
| TOTAL_BUILD_MSEC | 該当パーティションの完成までの合計時間 |
| KEYVAL_BUILD_MSEC | KeyValue Modeで該当パーティションの完成までの合計時間 |
| BITMAP_BUILD_MSEC | Bitmap Modeで該当パーティションの完成までの合計時間 |

### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS_CACHE
---

LSMインデックスのパーティションキャッシュ情報を表示します。

| 列名 | 説明 |
| -------------------------- | --------------------------- |
| BEGIN_RID | パーティションに取り込まれた最小RID |
| BITMAP_TABLE_PAGE_COUNT | ビットマップ値を保存するページ数 |
| BITMAP_TABLE_SIZE | ビットマップ値を保存するページの合計サイズ |
| END_RID | パーティションに取り込まれた最大RID+1 |
| INDEX_ID | インデックス識別子 |
| KEY_VALUE_COUNT | パーティションに取り込まれたキー値の数 |
| KEY_VALUE_TABLE_PAGE_COUNT | キー値を保存するページ数 |
| KEY_VALUE_TABLE_SIZE | キー値を保存するページのサイズ |
| LEVEL | インデックスパーティションのLSMレベル |
| MEMORY_SIZE | メモリ使用量 |
| MEMORY_SIZE_RBTREE | 赤黒木が使用したメモリ量 |
| META_PAGE_COUNT | メタデータを保存するページ数 |
| META_SIZE | メタデータを保存するページの合計サイズ |
| PARTITION_ID | パーティション識別子 |
| TABLE_ID | インデックスが作成されたテーブルの識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |

### V$STORAGE_DC_LSMINDEX_LEVELS
---

LSMインデックスのレベル情報を表示します。

| 列名 | 説明 |
| -------------- | ---------------------- |
| TABLE_ID | テーブル識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| INDEX_ID | インデックス識別子 |
| LEVEL | レベル |
| BEGIN_RID | パーティションの最初のRID |
| END_RID | パーティションの最後のRID+1 |
| META_BEGIN_RID | メタデータの記録開始時点のRID |
| META_END_RID | メタデータの記録終了時点のRID |
| DELETE_END_RID | 削除されたRIDの最大値+1 |

### V$STORAGE_DC_LSMINDEX_FILES
---

LSMインデックスを構成するファイルの情報を表示します。

| 列名 | 説明 |
| ------------ | --------------- |
| TABLE_ID | テーブル識別子 |
| TABLESPACE_ID | テーブルスペース識別子 |
| INDEX_ID | インデックス識別子 |
| LEVEL | インデックスパーティションのLSMレベル |
| PARTITION_ID | パーティション識別子 |
| BEGIN_RID | パーティションの最初のRID |
| END_RID | パーティションの最後のRID+1 |
| PATH | インデックスファイルの場所 |

### V$STORAGE_DC_LSMINDEX_AGER_JOBS
---

LSMインデックスの削除を担当するAgerの作業状態を表示します。

| 列名 | 説明 |
| --------- | ------------------ |
| TABLE_ID | テーブル識別子 |
| INDEX_ID | インデックス識別子 |
| LEVEL | インデックスパーティションのLSMレベル |
| BEGIN_RID | パーティションの最初のRID |
| END_RID | パーティションの最後のRID+1 |
| STATE | Index Agerの作業状態 |

## Volatile Table
### V$STORAGE_DC_VOLATILE_TABLE
---

Volatileテーブルの情報を表示します。

| 列名 | 説明 |
| ------------ | --------------------------- |
| MAX_MEM_SIZE | Volatileテーブルスペースの最大サイズ |
| CUR_MEM_SIZE | Volatileテーブルスペースの現在のサイズ |

## Tag Table
### V$STORAGE_TAG_TABLES
---

Tagdataテーブルのパーティションテーブルの情報を表示します。

| 列名 | 説明 |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID | テーブル識別子 |
| TABLE_BEGIN_RID | テーブルの開始RID |
| TABLE_END_RID | テーブルの終了RID |
| WRITE_END_RID | データファイルに記録された最後のRID |
| EXT_ROW_COUNT | VARCHARレコードのうち外部パーティションに取り込まれた件数 |
| EXT_WRITE_COUNT | VARCHARレコードのうちデータファイルに記録された件数 |
| DISK_INDEX_END_RID | ストレージに保存されたインデックスの終了RID |
| MEMORY_INDEX_END_RID | メモリインデックスにあるテーブルの終了RID |
| DELETE_MIN_DATE | DELETE ... BETWEEN ...実行時の削除対象の最小時刻 |
| DELETE_MAX_DATE | DELETE ... BETWEEN ...またはDELETE ... BEFORE ...実行時の削除対象の最大時刻 |
| INDEX_STATE | 現在のインデックス構築状態<br>IDLE: 構築完了、待機中<br>PROGRESS: 構築中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取りロック待機<br>SHUTDOWN: 停止。DELETEまたはDROP操作が実行中<br>ABNORMAL: 異常終了 |
| DELETE_STATE | 現在のDELETE操作の状態。DELETEコマンドを受けたときのみ実行するため、IDLEはありません。<br>PROGRESS: 削除中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取り/書き込みロック待機<br>SHUTDOWN: 停止。DELETE操作は実行されていません<br>ABNORMAL: 異常終了 |
| SAVE_STATE | 現在のテーブル保存操作の状態<br>IDLE: 保存完了、待機中<br>PROGRESS: 保存中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取りロック待機<br>SHUTDOWN: 停止。DELETEまたはDROP操作が実行中<br>ABNORMAL: 異常終了 |
| VINDEX_STATE | 現在のVARCHARインデックス構築状態<br>IDLE: 構築完了、待機中<br>PROGRESS: 構築中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取りロック待機<br>SHUTDOWN: 停止。DELETEまたはDROP操作が実行中<br>ABNORMAL: 異常終了 |

### V$STORAGE_TAG_CACHE
---

Tagdataテーブルのパーティションテーブルが使用するキャッシュ情報を表示します。

| 列名 | 説明 |
| ----------- | ------------------------ |
| POOL_ID | キャッシュプール識別子 |
| CATEGORY | キャッシュされているオブジェクトの分類 |
| USED_MEMORY | 使用中のメモリサイズ |
| BLOCK_COUNT | データキャッシュ数 |
| CACHE_HIT | データキャッシュヒット回数 |
| CACHE_MISS | データキャッシュミス回数 |
| FLUSHOUT | データキャッシュの競合でページを解放した回数 |
| COLD_READ | ストレージから直接読み取ったデータページ数 |
| MEMORY_WAIT | データメモリがキャッシュの競合で待機した回数 |
| IO_WAIT | データ読み取り操作の待機回数 |

### V$STORAGE_TAG_CACHE_BASE
---

タグキャッシュプールの集計情報を表示します。

| 列名 | 説明 |
| -- | -- |
| POOL_ID | キャッシュプール識別子 |
| TOTAL_CACHE_MEMORY | キャッシュメモリの合計 |
| TOTAL_OBJECT_COUNT | キャッシュオブジェクトの総数 |
| TOTAL_LRU_LOOP_COUNT | LRUループの総数 |

### V$STORAGE_TAG_CACHE_OBJECTS
---

Tagdataテーブルのパーティションテーブルが使用する各キャッシュブロックの詳細情報を表示します。

| 列名 | 説明 |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
| CATEGORY | キャッシュされているオブジェクトの分類 |
| LATEST_HIT | 最終アクセス時刻 |
| STATUS | キャッシュ状態<br>None: メモリ割り当て完了<br>Resides: キャッシュに保持された状態<br>Loading: ストレージからテーブルデータを読み込み中<br>ERROR!: データ読み込み中にエラーが発生 |
| WAIT_COUNT | Loading状態でキャッシュを読めずに待機した回数 |
| REF_COUNT | 現在のキャッシュブロックを参照中のセッション数 |
| HIT_COUNT | キャッシュブロックの参照回数 |
| TABLE_ID | テーブル識別子 |
| FILE_ID | ファイル識別子 |
| PART_ID | データファイル内のパーティション識別子 |
| SAVE_SCN | テーブル保存SCN |
| VSAVE_SCN | テーブル保存SCN |
| DELETE_SCN | DELETE操作のSCN |
| OFFSET | データファイルオフセット |
| DATA_SIZE | 圧縮前のデータサイズ、または0 |

### V$STORAGE_TAG_TABLE_FILES
---

Tagdataテーブルのパーティションテーブルのファイル情報を表示します。

| 列名 | 説明 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| TABLE_ID | テーブル識別子 |
| FILE_ID | ファイル識別子 |
| STATE | インデックス構築状態<br>COMPLETE: データ保存・インデックス構築完了<br>INDEXING: インデックス構築中<br>FILLED: データが満杯でインデックス構築待機中<br>PARTIAL: まだデータが満杯でなくインデックス構築待機中 |
| REF_COUNT | 現在のファイルを参照中のセッション数 |
| ROW_COUNT | 削除済みレコードを含めたファイル内のレコード数 |
| DEL_COUNT | ファイルから削除されたレコード数 |
| MIN_DATE | 該当ファイルに記録されたデータの最小日付 |
| MAX_DATE | 該当ファイルに記録されたデータの最大日付 |

### V$STORAGE_TAG_INDEX
---

Tagdataテーブルに作成されたインデックス情報を表示します。

| 列名 | 説明 |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| TABLE_ID | テーブル識別子 |
| INDEX_ID | インデックス識別子（INDEX_IDが4294967295の場合、tagテーブルの作成時に自動作成されるデフォルトインデックスを示す） |
| INDEX_STATE | インデックス構築状態<br>IDLE: 構築完了、待機中<br>INDEXING: 構築中<br>STORAGE FULL: ディスクが満杯のため構築停止 |
| DISK_INDEX_END_RID | 最後にディスクに反映されたインデックスのEndRID |
| MEMORY_INDEX_END_RID | 最後にメモリに反映されたインデックスのEndRID |
| TABLE_END_RID | 最後にテーブルに反映されたデータのEndRID |

## Tag Rollup
### V$ROLLUP
---

TagdataテーブルのRollup情報を表示します。

| 列名 | 説明 |
| -------------- | ------------------------------------------------------- |
| DATABASE_ID | 論理データベース識別子 |
| ID | RollupジョブID |
| ROLLUP_TABLE | Rollupテーブル名 |
| SOURCE_TABLE | 集計対象テーブル名（TAG/ROLLUP） |
| COLUMN_NAME | 集計対象の値の列 |
| ROOT_TABLE | 最上位のソースタグテーブル名 |
| USER_ID | 所有者のUser ID |
| INTERVAL_TIME | データ集計間隔（ミリ秒） |
| WAKEUP_INTERVAL | Rollupジョブの実行間隔（ミリ秒） |
| LAST_WAKEUP_TIME | 直近のwakeup時刻 |
| NEXT_WAKEUP_TIME | 次回のwakeup予定時刻 |
| ENABLED | Rollupが有効かどうか（1/0） |
| END_RID | このRollupが処理したSource Tableの最後のRID |
| LAST_ELAPSED_MSEC | 直前のRollup実行の所要時間（ミリ秒） |
| EXT_TYPE | 拡張（EXTENSION）の有無のフラグ |
| PREDICATE | 条件付きロールアップのフィルター式（NULLは条件なし） |
| RUN_STATE | スレッド状態: I=INIT, S=SLEEPING, R=RUNNING |

## License
### V$LICENSE_INFO
---

ライセンス情報を表示します。

| 列名 | 説明 |
| ---------------- | ---------------------- |
| ID | ライセンスID |
| ISSUE_DATE | 発行日 |
| TYPE | ライセンスタイプ |
| CUSTOMER | 顧客名 |
| PROJECT | プロジェクト名 |
| COUNTRY_CODE | 国コード |
| INSTALL_DATE | インストール日 |
| VIOLATE_STATUS | ライセンス違反状態 |
| VIOLATE_MSG | ライセンス違反メッセージ |

`V$LICENSE_STATUS`はStandard 8.5.4サーバーでは公開されていません。Standard Editionで
参照できるライセンスのフィールドには`V$LICENSE_INFO`を使用してください。

## Mutex
### V$MUTEX
---

現在のミューテックスの状態を表示します。

`WAIT_MSEC`、`WAIT_AVG_MSEC`、`HELD_MSEC`、`HELD_AVG_MSEC`はミリ秒単位の`DOUBLE`値です。

| フィールド名 | 説明 | 備考 |
| -------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| OBJECT | ミューテックスオブジェクトのアドレス |  |
| NAME | ミューテックス作成時に付けた名前 |  |
| TYPE | ミューテックスタイプ | Mutex: pmuMutex<br>RW Mutex: pmuRWMutex |
| OWNER | ミューテックスを取得したスレッドのID | Mutex: 取得したスレッドがなければ0<br>RW Mutex w/ Read-Lock: 0<br>RW Mutex w/ Write-Lock: 書き込みロックを取得したスレッドのID |
| LOCK_COUNT | ミューテックスを取得したスレッド数 | RW Mutexでは2以上になる場合があります。 |
| PEND_COUNT | ミューテックスの取得待機中のスレッド数 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集 |
| TRY_COUNT | ミューテックスの取得試行回数 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集 |
| CONFLICT_COUNT | ミューテックスの取得失敗回数 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集 |
| WAIT_MSEC | ミューテックスの取得待機時間の合計 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集<br>RW Mutexでは記録しない |
| WAIT_AVG_MSEC | ミューテックスの取得試行から成功までの平均時間 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集<br>RW Mutexでは記録しない |
| HELD_MSEC | ミューテックスの取得から解放までの合計時間 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集<br>RW Mutexでは記録しない |
| HELD_AVG_MSEC | ミューテックスの取得から解放までの平均時間 | TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集<br>RW Mutexでは記録しない |

### V$MUTEX_WAIT_STAT
---

現在ミューテックスを待機しているコールスタックを表示します。

| フィールド | 説明 | 備考 |
| --------- | ------------------- | -------------------------------- |
| THREAD_ID | ミューテックスの取得待機中のスレッドID |  |
| OBJECT | 取得を試みているミューテックスのアドレス | V$MUTEXのOBJECTと同じ |
| DEPTH | 呼び出しの深さ | TRACE_MUTEX_WAIT_STACK=1の場合のみ収集 |
| SYMBOL | ミューテックスの取得を呼び出した関数のシンボル | TRACE_MUTEX_WAIT_STACK=1の場合のみ収集 |

## Cluster

次の仮想テーブルはCluster Edition専用で、Standardサーバーでは公開されません。
実行中のEditionで参照できることを`V$TABLES`で確認してから使用してください。

### V$NODE_STATUS
---

クラスターの各ノードの状態を表示します。1行だけ表示します。

| 列名 | 説明 |
| -------- | ------------------------------------------------------------- |
| NODETYPE | ノードタイプ。クエリで参照できるタイプは次の2つのみです。<br>Broker<br>Warehouse |
| STATE | ノード状態 |

### V$DDL_INFO
---

クラスターで実行したDDL情報を表示します。

| 列名 | 説明 |
| -------------- | ----------------------- |
| SEQUENCENUMBER | DDLのシーケンス番号 |
| TIME | DDL実行時刻 |
| VALUE | DDLクエリの結果値（サーバー内部用） |
| CLIENT | クライアント名 |
| BROKER | Leader Brokerのノード名 |
| USER | ユーザー名 |
| SQL | DDLクエリの値 |

### V$REPLICATION
---

レプリケーションの動作情報を表示します。

| 列名 | 説明 |
| ---------------- | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| MODE | サーバー内部用 |
| STATE | ノード状態 |
| ADDR | Replication Managerのアドレス |
| PORT_NO | Replication Managerのポート番号 |
| MAX_SENDER_COUNT | 作成できるSenderの最大数 |
| RUN_SENDER_COUNT | 動作中のSenderの最大数 |

### V$REPL_SENDER
---

レプリケーション動作時のSender情報を表示します。

| 列名 | 説明 |
| ------------------ | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| ID | Sender識別子 |
| STATUS | Senderスレッドの動作状態 |
| PAYLOAD_RECV_COUNT | Senderから受信したペイロード数 |
| PAYLOAD_RECV_BYTES | Senderから受信したペイロードの合計サイズ |
| QUEUE_REMAIN_COUNT | Receive Queueに残るバッファー数 |
| NET_SEND_COUNT | 総送信回数 |
| NET_SEND_SIZE | 総送信サイズ |
| NET_RECV_COUNT | 総受信回数 |
| NET_RECV_SIZE | 総受信サイズ |

### V$REPL_SENDER_META
---

レプリケーション動作時のSenderメタデータを表示します。

| 列名 | 説明 |
| ---------- | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| SENDER_ID | Sender識別子 |
| TABLE_ID | 対象テーブル識別子 |
| TABLE_TYPE | 対象テーブルタイプ |
| BEGIN_RID | 対象レコードの開始RID |
| END_RID | 対象レコードの終了RID |

### V$REPL_RECEIVER
---

レプリケーション動作時のReceiver情報を表示します。

| 列名 | 説明 |
| ------------------ | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| STATUS | Receiverスレッドの動作状態 |
| PAYLOAD_RECV_COUNT | Senderから受信したペイロード数 |
| PAYLOAD_RECV_BYTES | Senderから受信したペイロードの合計サイズ |
| QUEUE_REMAIN_COUNT | Receive Queueに残るバッファー数 |
| NET_SEND_COUNT | 総送信回数 |
| NET_SEND_SIZE | 総送信サイズ |
| NET_RECV_COUNT | 総受信回数 |
| NET_RECV_SIZE | 総受信サイズ |

### V$REPL_RECEIVER_META
---

レプリケーション動作時のReceiverメタデータを表示します。

| 列名 | 説明 |
| ---------- | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| TABLE_ID | 対象テーブル識別子 |
| TABLE_TYPE | 対象テーブルタイプ |
| BEGIN_RID | 対象レコードの開始RID |
| END_RID | 対象レコードの終了RID |

### V$REPL_READER
---

レプリケーション動作時のReader情報を表示します。

| 列名 | 説明 |
| ----------- | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| SENDER_ID | Sender識別子 |
| ID | Reader識別子 |
| STATUS | Readerスレッドの動作状態 |
| FETCH_COUNT | FETCH実行回数 |

### V$REPL_READER_META
---

レプリケーション動作時のReaderメタデータを表示します。

| 列名 | 説明 |
| ---------- | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| SENDER_ID | Sender識別子 |
| ID | Reader識別子 |
| TABLE_ID | 対象テーブル識別子 |
| TABLE_TYPE | 対象テーブルタイプ |
| BEGIN_RID | 対象レコードの開始RID |
| END_RID | 対象レコードの終了RID |

### V$REPL_WRITER
---

レプリケーション動作時のWriter情報を表示します。

| 列名 | 説明 |
| ------------ | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| ID | Writer識別子 |
| STATUS | Writerスレッドの動作状態 |
| APPEND_COUNT | APPEND実行回数 |

### V$REPL_WRITER_META
---

レプリケーション動作時のWriterメタデータを表示します。

| 列名 | 説明 |
| ---------- | ---------------------------------- |
| HOSTNAME | レプリケーションが動作するノードのホスト名 |
| ID | Writer識別子 |
| TABLE_ID | 対象テーブル識別子 |
| TABLE_TYPE | 対象テーブルタイプ |
| BEGIN_RID | 対象レコードの開始RID |
| END_RID | 対象レコードの終了RID |

## Others
### V$TABLES
---

V$で始まるすべての仮想テーブルを表示します。

| 列名 | 説明 |
| ----------- | ------------ |
| NAME | テーブル名 |
| TYPE | テーブルタイプ |
| DATABASE_ID | データベース識別子 |
| ID | テーブル識別子 |
| USER_ID | テーブルを作成したユーザー |
| COLCOUNT | 列数 |

### V$COLUMNS
---

仮想テーブルの列情報を表示します。

| 列名 | 説明 |
| -------------------- | ---------- |
| NAME | 列名 |
| TYPE | 列のデータ型 |
| DATABASE_ID | データベース識別子 |
| ID | 列の識別子 |
| LENGTH | 列のサイズ |
| TABLE_ID | テーブル識別子 |
| FLAG | 非公開データ |
| PART_PAGE_COUNT | 未使用 |
| PAGE_VALUE_COUNT | 未使用 |
| MINMAX_CACHE_SIZE | 未使用 |
| MAX_CACHE_PART_COUNT | 未使用 |

### V$RETENTION_JOB
---

RETENTION POLICYが適用されたテーブルの情報を表示します。

| 列名 | 説明 |
| ------------------- | ------------------------------------------ |
| USER_NAME | ユーザー名 |
| TABLE_NAME | 対象TAG TABLE名 |
| POLICY_NAME | 適用されているPOLICY名 |
| STATE | RETENTION状態（RUNNING/WAITING/STOPPED） |
| LAST_DELETED_TIME | 最後に削除した時刻 |

### V$USER_AUTH_KEYS
---

チャレンジ認証に登録された公開鍵情報を表示します。

| 列名 | 説明 |
| -- | -- |
| KEY_ID | 鍵識別子 |
| USER_ID | ユーザー識別子 |
| USER_NAME | ユーザー名 |
| KEY_ALGO | 鍵アルゴリズム |
| KEY_PARAM | 鍵パラメーター |
| PUBKEY | 公開鍵のテキスト |
| ACTIVATED | 鍵が有効かどうか |
| VALID_AFTER | 鍵の有効期間の開始日 |
| VALID_BEFORE | 鍵の有効期間の終了日 |
| COMMENT | 鍵の説明 |
