---
layout : post
title : 仮想テーブル
type : docs
toc: true
weight: 0
---

サーバーの運用情報をテーブル形式で表示します。名前は V$ で始まります。

情報を読み取って保存し、サーバーの稼働状態を確認するために使用します。
他のテーブルと JOIN して、関連情報を取得することもできます。

読み取り専用で、ユーザーがデータを追加、削除、更新することはできません。


## 目次 {#index}

- [セッションとシステム](#sessionsystem)
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
- [結果キャッシュ](#result-cache)
  - [V$RS\_CACHE\_LIST](#vrs_cache_list)
  - [V$RS\_CACHE\_STAT](#vrs_cache_stat)
- [PVO ステートメントキャッシュ](#pvo-statement-cache)
  - [V$PVO\_CACHE\_STAT](#vpvo_cache_stat)
  - [V$PVO\_CACHE\_LIST](#vpvo_cache_list)
- [ストレージ](#storage)
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
- [Log テーブル](#log-table)
  - [V$STORAGE\_DC\_TABLES](#vstorage_dc_tables)
  - [V$STORAGE\_DC\_TABLES\_STAT](#vstorage_dc_tables_stat)
  - [V$STORAGE\_DC\_TABLE\_COLUMNS](#vstorage_dc_table_columns)
  - [V$STORAGE\_DC\_TABLE\_COLUMN\_PARTS](#vstorage_dc_table_column_parts)
  - [V$STORAGE\_DC\_TABLE\_INDEXES](#vstorage_dc_table_indexes)
- [LSM インデックス](#lsmlog-structured-merge-index)
  - [V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS](#vstorage_dc_lsmindex_level_parts)
  - [V$STORAGE\_DC\_LSMINDEX\_LEVEL\_PARTS\_CACHE](#vstorage_dc_lsmindex_level_parts_cache)
  - [V$STORAGE\_DC\_LSMINDEX\_LEVELS](#vstorage_dc_lsmindex_levels)
  - [V$STORAGE\_DC\_LSMINDEX\_FILES](#vstorage_dc_lsmindex_files)
  - [V$STORAGE\_DC\_LSMINDEX\_AGER\_JOBS](#vstorage_dc_lsmindex_ager_jobs)
- [Volatile テーブル](#volatile-table)
  - [V$STORAGE\_DC\_VOLATILE\_TABLE](#vstorage_dc_volatile_table)
- [Tag テーブル](#tag-table)
  - [V$STORAGE\_TAG\_TABLES](#vstorage_tag_tables)
  - [V$STORAGE\_TAG\_CACHE](#vstorage_tag_cache)
  - [V$STORAGE\_TAG\_CACHE\_BASE](#vstorage_tag_cache_base)
  - [V$STORAGE\_TAG\_CACHE\_OBJECTS](#vstorage_tag_cache_objects)
  - [V$STORAGE\_TAG\_TABLE\_FILES](#vstorage_tag_table_files)
  - [V$STORAGE\_TAG\_INDEX](#vstorage_tag_index)
- [Tag ロールアップ](#tag-rollup)
  - [V$ROLLUP](#vrollup)
- [ストリーム](#stream)
  - [V$STREAMS](#vstreams)
- [ライセンス](#license)
  - [V$LICENSE\_INFO](#vlicense_info)
- [ミューテックス](#mutex)
  - [V$MUTEX](#vmutex)
  - [V$MUTEX\_WAIT\_STAT](#vmutex_wait_stat)
- [クラスタ](#cluster)
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
- [その他](#others)
  - [V$TABLES](#vtables)
  - [V$COLUMNS](#vcolumns)
  - [V$RETENTION\_JOB](#vretention_job)
  - [V$USER\_AUTH\_KEYS](#vuser_auth_keys)



## セッションとシステム {#sessionsystem}

### V$PROPERTY {#vproperty}
---

サーバーに設定されたプロパティを表示します。

|列名|説明|
|--|--|
|NAME|プロパティ名|
|VALUE|プロパティ値|
|TYPE|データ型|
|DEFLT|デフォルト値|
|MIN|設定できる最小値|
|MAX|設定できる最大値|

### V$SESSION {#vsession}
---

接続中のセッション情報を表示します。

|列名|説明|
|--|--|
|HOSTNAME (Cluster Only)|セッションが接続したHOST名|
|ID|セッション識別子|
|CLOSED|接続が閉じているかどうか|
|USER_ID|ユーザー識別子|
|LOGIN_TIME|接続時刻|
|CLIENT_TYPE|接続クライアントのタイプ|
|USER_NAME|ユーザー名|
|USER_IP|ユーザーIP|
|SQL_LOGGING|セッションのログ設定。<br>1：解析、検証、最適化のエラー<br>2：DDL の実行結果<br>3：両方|
|SHOW_HIDDEN_COLS|SELECTで隠し列を表示するかどうか|
|FEEDBACK_APPEND_ERROR|APPEND エラーをクライアントへ通知するか|
|DEFAULT_DATE_FORMAT|Datetime取り込み時のデフォルト入力形式|
|HASH_BUCKET_SIZE|クエリーの一時ハッシュテーブルのバケット数|
|MAX_QPX_MEM|クエリ実行時に使用できる最大メモリサイズ|
|RS_CACHE_ENABLE|結果キャッシュを使用するか|
|RS_CACHE_TIME_BOUND_MSEC|結果キャッシュへ保存する実行時間の下限（ミリ秒）|
|RS_CACHE_MAX_MEMORY_PER_QUERY|結果キャッシュのクエリーごとの最大メモリ量|
|RS_CACHE_MAX_RECORD_PER_QUERY|結果キャッシュのクエリーごとの最大結果件数|
|RS_CACHE_APPROXIMATE_RESULT_ENABLE|近似結果をキャッシュするか|
|IDLE_TIMEOUT|接続後、指定時間クライアントが何もしなければセッションを終了|
|QUERY_TIMEOUT|クエリ実行時の応答待機時間|


### V$SESMEM {#vsesmem}
---

セッションのメモリ情報を表示します。

|列名|説明|
|--|--|
|SID|セッション識別子|
|ID|メモリマネージャー識別子|
|USAGE|使用サイズ|


### V$SESSTAT {#vsesstat}
---

セッションの統計を表示します。

|列名|説明|
|--|--|
|SID|セッション識別子|
|ID|統計情報識別子|
|VALUE|統計情報の値|


### V$SESTIME {#vsestime}
---

セッションの時間情報を表示します。

|列名|説明|
|--|--|
|SID|セッション識別子|
|ID|実行単位の識別子|
|ACCUM_TICK|累積時間|
|MAX_TICK|処理単位ごとの最大時間|


## V$SYSMEM {#vsysmem}

システムのメモリ情報を表示します。

|列名|説明|
|--|--|
|ID|メモリマネージャー識別子|
|NAME|メモリマネージャー名|
|USAGE|現在の使用量|
|MAX_USAGE|記録された最大使用量|


### V$SYSSTAT {#vsysstat}
---

システムの統計を表示します。

|列名|説明|
|--|--|
|ID|統計情報識別子|
|NAME|統計情報名|
|VALUE|統計情報の値|


### V$SYSTIME {#vsystime}
---

システムの時間情報を表示します。

|列名|説明|
|--|--|
|ID|実行単位の識別子|
|NAME|実行単位の名前|
|ACCUM_TICK|累積時間|
|AVG_TICK|処理単位ごとの平均時間|
|MIN_TICK|処理単位ごとの最小時間|
|MAX_TICK|処理単位ごとの最大時間|
|COUNT|実行回数|


### V$STMT {#vstmt}
---

現在実行しているクエリーを表示します。

|列名|説明|
|--|--|
|ID|クエリ識別子|
|SESS_ID|クエリを実行したセッションの識別子|
|STATE|クエリ状態|
|RECORD_SIZE|SELECT文の実行中の場合、結果レコードのサイズ|
|QUERY|クエリのテキスト|
 

### V$VERSION {#vversion}
---

Machbase のバージョン情報です。

|列名|説明|
|--|--|
|BINARY_DB_MAJOR_VERSION|DBメジャーバージョン|
|BINARY_DB_MINOR_VERSION|DBマイナーバージョン|
|BINARY_META_MAJOR_VERSION|METAメジャーバージョン|
|BINARY_META_MINOR_VERSION|METAマイナーバージョン|
|BINARY_CM_MAJOR_VERSION|Client（Communication Level）メジャーバージョン|
|BINARY_CM_MINOR_VERSION|Client（Communication Level）マイナーバージョン|
|BINARY_SIGNATURE|DB データファイルのバージョン名|
|FILE_DB_MAJOR_VERSION|File DBメジャーバージョン|
|FILE_DB_MINOR_VERSION|File DBマイナーバージョン|
|FILE_META_MAJOR_VERSION|File METAメジャーバージョン|
|FILE_META_MINOR_VERSION|File METAマイナーバージョン|
|FILE_CM_MAJOR_VERSION|File Client（Communication Level）メジャーバージョン|
|FILE_CM_MINOR_VERSION|File Client（Communication Level）マイナーバージョン|
|FILE_CREATE_TIME|ファイル作成時刻|
|EDITION|MACHBASEの種類|

### V$HTTP_STATUS {#vhttp_status}
---

組み込み HTTP エンドポイントの状態を表示します。

|列名|説明|
|--|--|
|DOC_ROOT|HTTP のドキュメントルート|
|HTTP_PORT|HTTP サービスポート|
|THREAD_COUNT|HTTP ワーカースレッド数|
|CONNECT_COUNT|受け付けた接続数|
|SERVICE_SUCCESS_COUNT|サービス成功回数|
|SERVICE_FAILURE_COUNT|サービス失敗回数|
|TOTAL_SERVICE_COUNT|サービス合計回数|
|CURRENT_SERVICE_COUNT|現在のサービス数|
|MAX_HTTP_MEM|HTTP の最大メモリ量|

### V$NEO_SESSION {#vneo_session}
---

Neo プロトコルのセッション状態を表示します。

|列名|説明|
|--|--|
|ID|セッション識別子|
|USER_ID|ユーザー識別子|
|USER_NAME|ユーザー名|
|STMT_COUNT|セッションのステートメント数|
|DISCONN_FLAG|切断フラグ|

### V$NEO_STMT {#vneo_stmt}
---

Neo プロトコルのステートメント状態を表示します。

|列名|説明|
|--|--|
|ID|ステートメント識別子|
|SESS_ID|セッション識別子|
|STATE|ステートメント状態|
|QUERY|ステートメントのテキスト|
|APPEND_SUCCESS_CNT|Append成功件数|
|APPEND_FAILURE_CNT|Append失敗件数|


## 結果キャッシュ {#result-cache}

### V$RS_CACHE_LIST {#vrs_cache_list}
---

結果キャッシュの一覧を表示します。

|列名|説明|
|--|--|
|TOUCH_TIME|キャッシュの作成または利用時刻|
|USER_ID|キャッシュのユーザー識別子|
|QUERY|キャッシュしたクエリー|
|TIME_SPENT|結果生成に要した時間|
|TABLE_COUNT|クエリーが参照するテーブル数|
|RECORD_COUNT|結果行数|
|REFERENCE_COUNT|現在参照しているセッション数|
|HIT_COUNT|キャッシュヒット回数|
|AGGR_TOUCH_TIME|集計結果キャッシュの作成または利用時刻|
|AGGR_HIT_COUNT|集計結果のヒット数|


### V$RS_CACHE_STAT {#vrs_cache_stat}
---

セッションの結果キャッシュ統計を表示します。


|列名|説明|
|--|--|
|CACHE_COUNT|結果キャッシュ数|
|CACHE_HIT|合計ヒット数|
|AGGR_HIT|集計結果の合計ヒット数|
|CACHE_REPLACED|キャッシュ置換回数|
|CACHE_MEMORY_USAGE|キャッシュの使用メモリ量|


## PVO ステートメントキャッシュ {#pvo-statement-cache}
グローバル PVO キャッシュの状態です。Standard 専用です。

### V$PVO_CACHE_STAT {#vpvo_cache_stat}
---

PVO キャッシュ全体の統計を表示します。

|列名|説明|
|--|--|
|CACHE_ENTRY_COUNT|キャッシュに格納されたSQLエントリー数|
|CACHE_HANDLE_COUNT|全SQLのキャッシュ済み計画（ハンドル）数|
|CACHE_MEMORY_USAGE|使用中のキャッシュメモリサイズ|
|CACHE_MAX_MEMORY_SIZE|設定されたキャッシュメモリ上限|
|CACHE_MAX_PLANS_PER_SQL|SQL当たりの最大許容計画数|
|CACHE_MAX_SQL_ENTRIES|最大許容SQLエントリー数（0は無制限）|
|CACHE_SHARD_COUNT|キャッシュのシャード数|
|CACHE_HIT|キャッシュヒット回数|
|CACHE_MISS|キャッシュミス回数|
|SINGLEFLIGHT_WAIT|同じSQLの同時構築を待機した回数|
|BUILD_COUNT|計画の構築試行回数|
|BUILD_FAIL|構築失敗回数|
|INVALIDATE_COUNT|無効化された計画数|
|EVICT_COUNT|メモリ上限などによるキャッシュの追い出し回数|
|FLUSH_COUNT|明示的/内部フラッシュ回数|

### V$PVO_CACHE_LIST {#vpvo_cache_list}
---

保存された SQL ごとの詳細を表示します。

|列名|説明|
|--|--|
|TOUCH_TIME|最終アクセス時刻|
|USER_ID|SQLを所有するユーザーID|
|QUERY|元のSQLテキスト|
|DEFAULT_DATE_FORMAT|構築時のセッション日時書式|
|TIMEZONE_OFFSET|セッションのタイムゾーンオフセット|
|SHOW_HIDDEN_COLS|隠し列を表示するかどうか|
|QUERY_PARALLEL_FACTOR|並列実行係数|
|HANDLE_COUNT|保持する計画（ハンドル）数|
|BUSY_COUNT|同時に使用中のハンドル数|
|HIT_COUNT|キャッシュヒット回数|
|BUILD_IN_PROGRESS|構築中かどうか|

## ストレージ {#storage}

### V$STORAGE {#vstorage}
---

ストレージシステムの内部情報です。

|列名|説明|
|--|--|
|DC_TABLE_FILE_SIZE|ディスク上の列データの総容量|
|DC_INDEX_FILE_SIZE|インデックスファイルデータの総容量|
|DC_TABLESPACE_DWFILE_SIZE|全列データ用DWFILEの総容量|
|DC_KV_TABLE_FILE_SIZE|TAGDATA パーティションテーブルのデータファイルの合計サイズ（バイト）|


### V$STORAGE_MOUNT_DATABASES {#vstorage_mount_databases}
---

マウントされたバックアップ DB の情報です。

|列名|説明|
|--|--|
|NAME|バックアップデータベースの内部名|
|PATH|バックアップファイルの場所|
|BACKUP_TBSID|バックアップデータベースのテーブルスペース識別子|
|BACKUP_SCN|バックアップデータベースの識別子|
|MOUNTDB|マウント時に指定したデータベース名（別名）|
|DB_BEGIN_TIME|バックアップデータベースの最初の取り込み時刻|
|DB_END_TIME|バックアップデータベースの最後の取り込み時刻|
|BACKUP_BEGIN_TIME|バックアップ実行の開始時刻|
|BACKUP_END_TIME|バックアップ実行の終了時刻|
|FLAG|プロパティフラグ|


### V$CACHE {#vcache}
---

ストレージから読み取った結果を保持するキャッシュオブジェクトの集計情報です。

|列名|説明|
|--|--|
|OBJ_COUNT|結果セットのキャッシュオブジェクトの現在数|

### V$CACHE_OBJECTS {#vcache_objects}
---

結果を保持するキャッシュオブジェクトごとの情報です。

|列名|説明|
|--|--|
|OID|オブジェクト識別子|
|REF_COUNT|参照数|
|FLAG|サーバー内部用フラグ|


### V$STORAGE_DC_TABLESPACES {#vstorage_dc_tablespaces}
---

ストレージのテーブルスペース情報です。

|列名|説明|
|--|--|
|NAME|テーブルスペース名|
|ID|テーブルスペース識別子|
|FLAG|テーブルスペースのプロパティを示すフラグ|
|REF_COUNT|テーブルスペースの参照数|
|DISK_COUNT|テーブルスペースに属するディスク数|


### V$STORAGE_DC_TABLESPACE_DISKS {#vstorage_dc_tablespace_disks}
---

テーブルスペース内のディスク情報です。

|列名|説明|
|--|--|
|NAME|ディスク名|
|ID|ディスク識別子|
|TABLESPACE_ID|ディスクが属するテーブルスペースの識別子|
|PATH|ディスクのパス|
|IO_THREAD_COUNT|I/Oスレッド数|
|IO_JOB_COUNT|I/Oジョブ数|
|VIRTUAL_DISK_COUNT|仮想ディスク数|


### V$STORAGE_DC_DWFILES {#vstorage_dc_dwfiles}
---

二重書き込み（DW）ファイルの情報です。


|列名|説明|
|--|--|
|TBS_ID|テーブルスペース識別子|
|DISK_ID|ディスク識別子|
|FILE|ファイルのパス|
|TABLE_ID|テーブル識別子|
|COLUMN_ID|列の識別子|
|PARTITION_ID|パーティション識別子|
|PAGE_ID|ページ識別子|
|DISK_OFFSET|ディスクオフセット|
|DISK_IMAGE_SIZE|ディスクイメージサイズ|
|HEAD_CRC32CODE_IMAGE|イメージ先頭のCRC32コード|
|TAIL_CRC32CODE_IMAGE|イメージ末尾のCRC32コード|
|CRC32CODE_PAGE|ページのCRC32コード|
|HEAD_TIMESTAMP_PAGE|ページ先頭のタイムスタンプ|
|TAIL_TIMESTAMP_PAGE|ページ末尾のタイムスタンプ|


### V$STORAGE_DC_PAGECACHE {#vstorage_dc_pagecache}
---

ページキャッシュの情報です。

|列名|説明|
|--|--|
|MAX_MEM_SIZE|ページキャッシュの最大メモリサイズ|
|CUR_MEM_SIZE|ページキャッシュの現在のメモリサイズ|
|PAGE_CNT|キャッシュされたページ数|
|CHECK_TIME|検査時刻|


### V$STORAGE_DC_PAGECACHE_LRU_LST {#vstorage_dc_pagecache_lru_lst}
---

ページキャッシュの LRU リスト情報です。


|列名|説明|
|--|--|
|OBJECT_ID|オブジェクト識別子|
|LEVEL|パーティションレベル|
|PARTITION_ID|パーティション識別子|
|OFFSET|ページキャッシュのオフセット|
|SIZE|ページサイズ|
|REF_CNT|参照数|

### V$STORAGE_USAGE {#vstorage_usage}
---

ストレージ使用量を表示します。

|列名|説明|
|--|--|
|TOTAL_SPACE|$MACHBASE_HOME/dbsディレクトリがあるストレージの総容量|
|USED_SPACE|$MACHBASE_HOME/dbsディレクトリがあるストレージの使用量|
|USED_RATIO|使用率（%）|
|RATIO_CAP|ストレージ使用量の上限。USED_RATIOがこの上限に達すると、取り込み/インデックス構築が停止します。|


### V$STORAGE_TABLES {#vstorage_tables}
---

テーブルの詳細を表示します。

|列名|説明|
|--|--|
|ID|テーブルのID|
|TYPE|型。<br>Persistent：LOG/TAG<br>Volatile：Volatile<br>Key-Value：TAG の構成テーブル|
|STATUS|現在の状態<br>Creating...: CREATE TABLEでテーブル作成中<br>Normal: 正常<br>Predrop: DROP TABLEコマンドを受け付けた状態<br>Dropping...: DROP TABLEコマンドの実行中<br>Dropped: DROP TABLEコマンドの完了<br>Mounted: バックアップデータベースをmountコマンドで読み込んだ状態|
|STORAGE_USAGE|該当テーブルがストレージ上で占有する容量|


## Log テーブル {#log-table}

### V$STORAGE_DC_TABLES {#vstorage_dc_tables}
---

Log テーブルの内部情報です。

|列名|説明|
|--|--|
|ID|テーブル識別子|
|DATABASE_ID|データベース識別子|
|CREATE_SCN|作成時のシステム変更番号（System Change Number）|
|UPDATE_SCN|最終変更時のシステム変更番号（System Change Number）|
|DDL_REF_COUNT|DDL実行で該当テーブルを参照しているセッション数|
|BEGIN_RID|テーブルの最小RID|
|END_RID|テーブルの最後のRow ID + 1|
|BEGIN_META_RID|メタデータの記録開始時点のID|
|END_META_RID|メタデータの記録終了時点のID|
|END_SYNC_RID|ディスクに記録された最後のRow ID + 1|
|FLAG|テーブルのプロパティを示すフラグ|
|COLUMN_COUNT|テーブルの列数|
|INDEX_COUNT|テーブルのインデックス数|
|INDEX_MIN_END_RID|インデックスに記録された最後のRID + 1|
|LAST_ARRIVAL_TIME|最後に記録された\_arrival_timeの値|
|LAST_CHECKPOINT_TIME|最後にチェックポイントを通過した時点|
|TYPE|テーブルタイプ|

### V$STORAGE_DC_TABLES_STAT {#vstorage_dc_tables_stat}
---

Log テーブルの内部情報です。

|列名|説明|
|--|--|
|TABLESPACE_ID|テーブルスペース識別子|
|TABLE_ID|テーブル識別子|
|COLUMN_ID|列の識別子|
|COUNT|レコード数|

### V$STORAGE_DC_TABLE_COLUMNS {#vstorage_dc_table_columns}
---

Log テーブルの列情報です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|DATABASE_ID|データベース識別子|
|ID|列の識別子|
|FLAG|プロパティフラグ|
|SIZE|列のデータサイズ|
|PARTITION_VALUE_COUNT|パーティションに保存する最大データ数|
|PAGE_VALUE_COUNT|ページに保存する最大データ数|
|CACHE_VALUE_COUNT|キャッシュ値の最大数|
|MINMAX_CACHE_SIZE|列パーティションのMIN/MAXキャッシュの最大サイズ|
|CUR_APPEND_PARTITION_ID|現在取り込み中のパーティション識別子|
|CUR_CACHE_PARTITION_COUNT|現在のキャッシュにデータを読み込んだパーティション数|
|CUR_MINMAX_CACHE_SIZE|現在のMIN/MAXキャッシュサイズ|
|END_RID_FOR_DEFAULT_VALUE|既定値を保持する範囲の end RID|
|DISK_FILE_SIZE|該当列の列パーティションデータファイルの合計サイズ|
|MEMORY_TOTAL_SIZE|テーブルが使用中のメモリサイズ|
|MEMORY_ALLOC_SIZE|テーブルに割り当てられたメモリサイズ|


### V$STORAGE_DC_TABLE_COLUMN_PARTS {#vstorage_dc_table_column_parts}
---

Log の列パーティション情報です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|DATABASE_ID|データベース識別子|
|COLUMN_ID|列の識別子|
|ID|パーティション識別子|
|FLAG|列のプロパティを示すフラグ|
|BEGIN_RID|パーティションに保存された最小RID|
|END_RID|パーティションに保存された最後のRID|
|END_SYNC_RID|SYNCが完了した最後のRID。<br>開始RIDより大きく最後のSYNC RIDより小さいRIDを持つデータは、パーティションファイルに記録されています。|
|MIN_TIME|列パーティションに最初にデータを取り込んだ時刻|
|MAX_TIME|列パーティションに最後にデータを取り込んだ時刻|
|MAX_VALUE_COUNT_PER_PARTITION|パーティションの最大データ数|
|MAX_VALUE_COUNT_PER_PAGE|ページ当たりの最大データ数|
|MAX_PAGE_COUNT|パーティション当たりの最大ページ数|
|PAGE_SIZE|列パーティションに保存されたページのサイズ|
|PAGE_COUNT|現在の列パーティションに作成されたページ数|
|COMPRESS_RATIO|列パーティションの圧縮率。0はまだデータ圧縮を実行していないことを示します。|
|DISK_FILENAME|パーティションファイル名|
|EXTERNAL_PART_SIZE|大きな値を記録する外部パーティションファイルのサイズ|
|MIN_VALUE|列パーティションの最小値|
|MAX_VALUE|列パーティションの最大値|


### V$STORAGE_DC_TABLE_INDEXES {#vstorage_dc_table_indexes}
---

Log に作成したインデックス情報です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|DATABASE_ID|データベース識別子|
|ID|インデックス識別子|
|FLAG|インデックスのプロパティを示すフラグ|
|TABLE_BEGIN_RID|テーブルに取り込まれた最小RID|
|TABLE_END_RID|テーブルの最後のRID|
|BEGIN_RID|インデックスの最小RID|
|END_RID|インデックスの最大RID|
|END_SYNC_RID|ファイルに記録された最大RID+1|
|COLUMN_COUNT|インデックスの列数|
|BEGIN_PART_ID|インデックスの最初のパーティション識別子|
|END_PART_ID|インデックスの最後のパーティション識別子|
|FLUSH_REQUEST_COUNT|ディスクへの反映を要求されたインデックスパーティション数|
|MAX_KEY_SIZE|最大キーサイズ|
|INDEX_TYPE|インデックスタイプ|
|DISK_FILE_SIZE|該当インデックスのパーティションファイルの合計サイズ|
|LAST_CHECKPOINT_TIME|最後にチェックポイントを通過した時点|



## LSM（Log-Structured Merge）インデックス {#lsmlog-structured-merge-index}


### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS {#vstorage_dc_lsmindex_level_parts}
---

LSM のパーティション情報です。

|列名|説明|
|--|--|
|TABLE_ID|インデックスが作成されたテーブルの識別子|
|TABLESPACE_ID|テーブルスペース識別子|
|INDEX_ID|インデックス識別子|
|LEVEL|インデックスパーティションのLSMレベル|
|PARTITION_ID|パーティション識別子|
|BEGIN_RID|パーティションに取り込まれた最小RID|
|END_RID|パーティションに取り込まれた最大RID+1|
|KEY_VALUE_COUNT|パーティションに取り込まれたキー値の数|
|KEY_VALUE_TABLE_SIZE|キー値を保存するページのサイズ|
|KEY_VALUE_TABLE_PAGE_COUNT|キー値を保存するページ数|
|MIN_KEY_VALUE|最小キー値|
|MAX_KEY_VALUE|最大キー値|
|BITMAP_TABLE_SIZE|ビットマップ値を保存するページの合計サイズ|
|BITMAP_TABLE_PAGE_COUNT|ビットマップ値を保存するページ数|
|META_SIZE|メタデータを保存するページの合計サイズ|
|META_PAGE_COUNT|メタデータを保存するページ数|
|TOTAL_BUILD_MSEC|該当パーティションの完成までの合計時間|
|KEYVAL_BUILD_MSEC|KeyValue Modeで該当パーティションの完成までの合計時間|
|BITMAP_BUILD_MSEC|Bitmap Modeで該当パーティションの完成までの合計時間|


### V$STORAGE_DC_LSMINDEX_LEVEL_PARTS_CACHE {#vstorage_dc_lsmindex_level_parts_cache}
---

LSM のパーティションキャッシュ情報です。


|列名|説明|
|--|--|
|TABLESPACE_ID|テーブルスペース識別子|
|TABLE_ID|インデックスが作成されたテーブルの識別子|
|INDEX_ID|インデックス識別子|
|LEVEL|インデックスパーティションのLSMレベル|
|PARTITION_ID|パーティション識別子|
|BEGIN_RID|パーティションに取り込まれた最小RID|
|END_RID|パーティションに取り込まれた最大RID+1|
|KEY_VALUE_COUNT|パーティションに取り込まれたキー値の数|
|KEY_VALUE_TABLE_SIZE|キー値を保存するページのサイズ|
|KEY_VALUE_TABLE_PAGE_COUNT|キー値を保存するページ数|
|BITMAP_TABLE_SIZE|ビットマップ値を保存するページの合計サイズ|
|BITMAP_TABLE_PAGE_COUNT|ビットマップ値を保存するページ数|
|META_SIZE|メタデータを保存するページの合計サイズ|
|META_PAGE_COUNT|メタデータを保存するページ数|
|MEMORY_SIZE|メモリ使用量|
|MEMORY_SIZE_RBTREE|赤黒木が使用したメモリ量|


### V$STORAGE_DC_LSMINDEX_LEVELS {#vstorage_dc_lsmindex_levels}
---

LSM のレベル情報です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|DATABASE_ID|データベース識別子|
|INDEX_ID|インデックス識別子|
|LEVEL|レベル|
|BEGIN_RID|パーティションの最初のRID|
|END_RID|パーティションの最後のRID+1|
|META_BEGIN_RID|メタデータの記録開始時点のRID|
|META_END_RID|メタデータの記録終了時点のRID|
|DELETE_END_RID|削除されたRIDの最大値+1|


### V$STORAGE_DC_LSMINDEX_FILES {#vstorage_dc_lsmindex_files}
---

LSM を構成するファイル情報です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|DATABASE_ID|データベース識別子|
|INDEX_ID|インデックス識別子|
|LEVEL|インデックスパーティションのLSMレベル|
|PARTITION_ID|パーティション識別子|
|BEGIN_RID|パーティションの最初のRID|
|END_RID|パーティションの最後のRID+1|
|PATH|インデックスファイルの場所|


### V$STORAGE_DC_LSMINDEX_AGER_JOBS {#vstorage_dc_lsmindex_ager_jobs}
---

LSM の削除を担当する Ager の状態です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|INDEX_ID|インデックス識別子|
|LEVEL|インデックスパーティションのLSMレベル|
|BEGIN_RID|パーティションの最初のRID|
|END_RID|パーティションの最後のRID+1|
|STATE|Index Agerの作業状態|


## Volatile テーブル {#volatile-table}

### V$STORAGE_DC_VOLATILE_TABLE {#vstorage_dc_volatile_table}
---

Volatile テーブルの情報です。


|列名|説明|
|--|--|
|MAX_MEM_SIZE|Volatileテーブルスペースの最大サイズ|
|CUR_MEM_SIZE|Volatileテーブルスペースの現在のサイズ|


## Tag テーブル {#tag-table}

### V$STORAGE_TAG_TABLES {#vstorage_tag_tables}
---

Tag を構成するパーティションテーブルの情報です。


|列名|説明|
|--|--|
|ID|テーブル識別子|
|TABLE_BEGIN_RID|テーブルの開始RID|
|TABLE_END_RID|最後にテーブルに反映されたデータのEndRID|
|WRITE_END_RID|データファイルに記録された最後のRID|
|EXT_ROW_COUNT|VARCHARレコードのうち外部パーティションに取り込まれた件数|
|EXT_WRITE_COUNT|VARCHARレコードのうちデータファイルに記録された件数|
|DISK_INDEX_END_RID|最後にディスクに反映されたインデックスのEndRID|
|MEMORY_INDEX_END_RID|メモリインデックスにあるテーブルの終了RID|
|DELETE_MIN_DATE|DELETE ... BETWEEN ...実行時の削除対象の最小時刻|
|DELETE_MAX_DATE|DELETE ... BETWEEN ...またはDELETE ... BEFORE ...実行時の削除対象の最大時刻|
|INDEX_STATE|現在のインデックス構築状態<br>IDLE: 構築完了、待機中<br>PROGRESS: 構築中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取りロック待機<br>SHUTDOWN: 停止。DELETEまたはDROP操作が実行中<br>ABNORMAL: 異常終了|
|DELETE_STATE|DELETE の状態。コマンド実行時のみ動作するため IDLE はない。<br>PROGRESS：削除中<br>IOWAIT：ストレージ I/O 待ち<br>PENDING：テーブル読み書きロック待ち<br>SHUTDOWN：停止。DELETE 操作は実行されない<br>ABNORMAL：異常終了|
|SAVE_STATE|現在のテーブル保存操作の状態<br>IDLE: 保存完了、待機中<br>PROGRESS: 保存中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取りロック待機<br>SHUTDOWN: 停止。DELETEまたはDROP操作が実行中<br>ABNORMAL: 異常終了|
|VINDEX_STATE|現在のVARCHARインデックス構築状態<br>IDLE: 構築完了、待機中<br>PROGRESS: 構築中<br>IOWAIT: ストレージI/O待機<br>PENDING: テーブルの読み取りロック待機<br>SHUTDOWN: 停止。DELETEまたはDROP操作が実行中<br>ABNORMAL: 異常終了|


### V$STORAGE_TAG_CACHE {#vstorage_tag_cache}
---

Tag パーティションテーブルのキャッシュ情報です。


|列名|説明|
|--|--|
|CATEGORY|キャッシュされているオブジェクトの分類|
|USED_MEMORY|使用中のメモリサイズ|
|BLOCK_COUNT|データキャッシュ数|
|CACHE_HIT|データキャッシュヒット回数|
|CACHE_MISS|データキャッシュミス回数|
|FLUSHOUT|キャッシュの退避によるページフラッシュ回数|
|COLDREAD|ストレージから直接読み取ったデータページ数|
|MEMORY_WAIT|キャッシュの退避を待った回数|
|IO_WAIT|データ読み取り操作の待機回数|

### V$STORAGE_TAG_CACHE_BASE {#vstorage_tag_cache_base}
---

Tag キャッシュプールの集計情報です。

|列名|説明|
|--|--|
|POOL_ID|キャッシュプール識別子|
|TOTAL_CACHE_MEMORY|キャッシュメモリの合計|
|TOTAL_OBJECT_COUNT|キャッシュオブジェクトの総数|
|TOTAL_LRU_LOOP_COUNT|LRUループの総数|

### V$STORAGE_TAG_CACHE_OBJECTS {#vstorage_tag_cache_objects}
---

各キャッシュブロックの詳細です。

|列名|説明|
|--|--|
|CATEGORY|キャッシュされているオブジェクトの分類|
|LATEST_HIT|最終アクセス時刻|
|STATUS|キャッシュ状態<br>None: メモリ割り当て完了<br>Resides: キャッシュに保持された状態<br>Loading: ストレージからテーブルデータを読み込み中<br>ERROR!: データ読み込み中にエラーが発生|
|WAIT_COUNT|Loading状態でキャッシュを読めずに待機した回数|
|REF_COUNT|現在のキャッシュブロックを参照中のセッション数|
|HIT_COUNT|キャッシュブロックの参照回数|
|TABLE_ID|テーブル識別子|
|FILE_ID|ファイル識別子|
|PART_ID|データファイル内のパーティション識別子|
|SAVE_SCN|テーブル保存SCN|
|VSAVE_SCN|テーブル保存SCN|
|DELETE_SCN|DELETE操作のSCN|
|OFFSET|データファイルオフセット|
|DATA_SIZE|圧縮前のデータサイズ、または0|


### V$STORAGE_TAG_TABLE_FILES {#vstorage_tag_table_files}
---

Tag パーティションテーブルのファイル情報です。


|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|FILE_ID|ファイル識別子|
|STATE|インデックス構築状態<br>COMPLETE: データ保存・インデックス構築完了<br>INDEXING: インデックス構築中<br>FILLED: データが満杯でインデックス構築待機中<br>PARTIAL: まだデータが満杯でなくインデックス構築待機中|
|REF_COUNT|現在のファイルを参照中のセッション数|
|ROW_COUNT|削除済みレコードを含めたファイル内のレコード数|
|DEL_COUNT|ファイルから削除されたレコード数|
|MIN_DATE|ファイルの最小日時|
|MAX_DATE|ファイルの最大日時|


### V$STORAGE_TAG_INDEX {#vstorage_tag_index}
---

Tag に作成したインデックス情報です。

|列名|説明|
|--|--|
|TABLE_ID|テーブル識別子|
|INDEX_ID|インデックス識別子（INDEX_IDが4294967295の場合、tagテーブルの作成時に自動作成されるデフォルトインデックスを示す）|
|INDEX_STATE|インデックス構築状態<br>IDLE: 構築完了、待機中<br>INDEXING: 構築中<br>STORAGE FULL: ディスクが満杯のため構築停止|
|DISK_INDEX_END_RID|最後にディスクに反映されたインデックスのEndRID|
|MEMORY_INDEX_END_RID|メモリインデックスにあるテーブルの終了RID|
|TABLE_END_RID|最後にテーブルに反映されたデータのEndRID|


## Tag ロールアップ {#tag-rollup}

### V$ROLLUP {#vrollup}
---

Tag のロールアップ情報を表示します。

|列名|説明|
|--|--|
|DATABASE_ID|DB 識別子（ローカル DB は常に -1）|
|ID|RollupジョブID|
|ROLLUP_TABLE|Rollupテーブル名|
|SOURCE_TABLE|集計対象テーブル名（TAG/ROLLUP）|
|COLUMN_NAME|集計対象の値の列|
|ROOT_TABLE|最上位のソースタグテーブル名|
|USER_ID|所有者のUser ID|
|INTERVAL_TIME|集計間隔（ms）|
|WAKEUP_INTERVAL|起動間隔（ms）|
|LAST_WAKEUP_TIME|直近のwakeup時刻|
|NEXT_WAKEUP_TIME|次回のwakeup予定時刻|
|ENABLED|Rollupが有効かどうか（1/0）|
|END_RID|このRollupが処理したSource Tableの最後のRID|
|LAST_ELAPSED_MSEC|直前のRollup実行の所要時間（ミリ秒）|
|EXT_TYPE|拡張フラグ（設定時は FIRST/LAST に対応）|
|PREDICATE|条件付きロールアップのフィルター式（NULLは条件なし）|
|RUN_STATE|スレッド状態: I=INIT, S=SLEEPING, R=RUNNING|



## ストリーム {#stream}

### V$STREAMS {#vstreams}
---

ストリームの情報を表示します。

|列名|説明|
|--|--|
|NAME|ストリームクエリー名|
|LAST_EX_TIME|最終実行時刻|
|TABLE_NAME|クエリーの参照テーブル名|
|END_RID|最後に読み取った RID|
|STATE|現在の状態|
|QUERY_TXT|クエリのテキスト|
|ERROR_MSG|前回実行のエラーメッセージ|
|FREQUENCY|最小実行間隔（ナノ秒）。0 はレコードごと、それ以外は指定間隔で実行|


## ライセンス {#license}

### `V$LICENSE_INFO` {#vlicense_info}
---

ライセンス情報を表示します。


|列名|説明|
|--|--|
|ID|ライセンスID|
|ISSUE_DATE|発行日|
|TYPE|ライセンスタイプ|
|CUSTOMER|顧客名|
|PROJECT|プロジェクト名|
|COUNTRY_CODE|国コード|
|INSTALL_DATE|インストール日|
|VIOLATE_STATUS|ライセンス違反状態|
|VIOLATE_MSG|ライセンス違反メッセージ|

Standard 8.5.4 は `V$LICENSE_STATUS` を公開していません。
Standard のライセンス情報には `V$LICENSE_INFO` を使用します。


## ミューテックス {#mutex}

### V$MUTEX {#vmutex}
---

ミューテックスの現在の状態を表示します。

|列名|説明|備考|
|--|--|--|
|OBJECT|ミューテックスオブジェクトのアドレス| |
|NAME|ミューテックス作成時に付けた名前| |
|TYPE|ミューテックスタイプ|Mutex：pmuMutex<br>RW Mutex：pmuRWMutex|
|OWNER|ミューテックスを取得したスレッドのID|Mutex: 取得したスレッドがなければ0<br>RW Mutex w/ Read-Lock: 0<br>RW Mutex w/ Write-Lock: 書き込みロックを取得したスレッドのID|
|LOCK_COUNT|ミューテックスを取得したスレッド数|RW Mutexでは2以上になる場合があります。|
|PEND_COUNT|ミューテックスの取得待機中のスレッド数|TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集|
|TRY_COUNT|ミューテックスの取得試行回数|TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集|
|CONFLICT_COUNT|ミューテックスの取得失敗回数|TRACE_MUTEX_WAIT_STATUS=1の場合のみ収集|
|WAIT_TICK|取得までの待ち時間の合計|TRACE_MUTEX_WAIT_STATUS=1 の場合のみ収集。RW Mutex は記録対象外|
|WAIT_TICK_AVG|取得試行から成功までの平均時間|TRACE_MUTEX_WAIT_STATUS=1 の場合のみ収集。RW Mutex は記録対象外|
|HELD_TICK|取得から解放までの合計時間|TRACE_MUTEX_WAIT_STATUS=1 の場合のみ収集。RW Mutex は記録対象外|
|HELD_TICK_AVG|取得から解放までの平均時間|TRACE_MUTEX_WAIT_STATUS=1 の場合のみ収集。RW Mutex は記録対象外|


### V$MUTEX_WAIT_STAT {#vmutex_wait_stat}
---

待機中のミューテックスのコールスタックを表示します。

|列名|説明|備考|
|--|--|--|
|THREAD_ID|ミューテックスの取得待機中のスレッドID| |
|OBJECT|取得を試みているミューテックスのアドレス|V$MUTEXのOBJECTと同じ|
|DEPTH|コールスタックの深さ|TRACE_MUTEX_WAIT_STACK=1の場合のみ収集|
|SYMBOL|取得を呼び出した関数のシンボル|TRACE_MUTEX_WAIT_STACK=1の場合のみ収集|



## クラスタ {#cluster}

以下は Cluster Edition 専用で、Standard には公開されません。
実行前に、稼働中のエディションの `V$TABLES` を確認してください。

### V$NODE_STATUS {#vnode_status}
---

クラスタのノード状態を表示します。自ノードの 1 行だけです。


|列名|説明|
|--|--|
|NODETYPE|ノードタイプ。クエリで参照できるタイプは次の2つのみです。<br>Broker<br>Warehouse|
|STATE|ノード状態|


### V$DDL_INFO {#vddl_info}
---

クラスタで実行した DDL 情報です。

|列名|説明|
|--|--|
|SEQUENCENUMBER|DDLのシーケンス番号|
|TIME|DDL実行時刻|
|VALUE|DDLクエリの結果値（サーバー内部用）|
|CLIENT|クライアント名|
|BROKER|Leader Brokerのノード名|
|USER|ユーザー名|
|SQL|DDLクエリの値|

### V$REPLICATION {#vreplication}
---

レプリケーションの動作情報です。


|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|MODE|サーバー内部用|
|STATE|ノード状態|
|ADDR|Replication Managerのアドレス|
|PORT_NO|Replication Managerのポート番号|
|MAX_SENDER_COUNT|作成できるSenderの最大数|
|RUN_SENDER_COUNT|動作中の Sender 数|

### V$REPL_SENDER {#vrepl_sender}
---

レプリケーション Sender の情報です。


|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|ID|Sender識別子|
|STATUS|Senderスレッドの動作状態|
|PAYLOAD_RECV_COUNT|Senderから受信したペイロード数|
|PAYLOAD_RECV_BYTES|Senderから受信したペイロードの合計サイズ|
|QUEUE_REMAIN_COUNT|Receive Queueに残るバッファー数|
|NET_SEND_COUNT|総送信回数|
|NET_SEND_SIZE|総送信サイズ|
|NET_RECV_COUNT|総受信回数|
|NET_RECV_SIZE|総受信サイズ|


### V$REPL_SENDER_META {#vrepl_sender_meta}
---

Sender のメタデータです。


|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|SENDER_ID|Sender識別子|
|TABLE_ID|対象テーブル識別子|
|TABLE_TYPE|対象テーブルタイプ|
|BEGIN_RID|対象レコードの開始RID|
|END_RID|対象レコードの終了RID|

### V$REPL_RECEIVER {#vrepl_receiver}
---

レプリケーション Receiver の情報です。


|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|STATUS|Receiverスレッドの動作状態|
|PAYLOAD_RECV_COUNT|Senderから受信したペイロード数|
|PAYLOAD_RECV_BYTES|Senderから受信したペイロードの合計サイズ|
|QUEUE_REMAIN_COUNT|Receive Queueに残るバッファー数|
|NET_SEND_COUNT|総送信回数|
|NET_SEND_SIZE|総送信サイズ|
|NET_RECV_COUNT|総受信回数|
|NET_RECV_SIZE|総受信サイズ|

### V$REPL_RECEIVER_META {#vrepl_receiver_meta}
---

Receiver のメタデータです。

|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|TABLE_ID|対象テーブル識別子|
|TABLE_TYPE|対象テーブルタイプ|
|BEGIN_RID|対象レコードの開始RID|
|END_RID|対象レコードの終了RID|


### V$REPL_READER {#vrepl_reader}
---

レプリケーション Reader の情報です。

|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|SENDER_ID|Sender識別子|
|ID|Reader識別子|
|STATUS|Readerスレッドの動作状態|
|FETCH_COUNT|FETCH実行回数|

### V$REPL_READER_META {#vrepl_reader_meta}
---

Reader のメタデータです。



|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|SENDER_ID|Sender識別子|
|ID|Reader識別子|
|TABLE_ID|対象テーブル識別子|
|TABLE_TYPE|対象テーブルタイプ|
|BEGIN_RID|対象レコードの開始RID|
|END_RID|対象レコードの終了RID|


### V$REPL_WRITER {#vrepl_writer}
---

レプリケーション Writer の情報です。


|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|ID|Writer識別子|
|STATUS|Writerスレッドの動作状態|
|APPEND_COUNT|APPEND実行回数|

### V$REPL_WRITER_META {#vrepl_writer_meta}
---

Writer のメタデータです。

|列名|説明|
|--|--|
|HOSTNAME|レプリケーションが動作するノードのホスト名|
|ID|Writer識別子|
|TABLE_ID|対象テーブル識別子|
|TABLE_TYPE|対象テーブルタイプ|
|BEGIN_RID|対象レコードの開始RID|
|END_RID|対象レコードの終了RID|


## その他 {#others}

### `V$TABLES` {#vtables}
---

V$ で始まるすべての仮想テーブルを表示します。

|列名|説明|
|--|--|
|NAME|テーブル名|
|TYPE|テーブルタイプ|
|DATABASE_ID|データベース識別子|
|ID|テーブル識別子|
|USER_ID|テーブルを作成したユーザー|
|COLCOUNT|列数|


### V$COLUMNS {#vcolumns}
---

仮想テーブルの列情報です。

|列名|説明|
|--|--|
|NAME|列名|
|TYPE|列のデータ型|
|DATABASE_ID|データベース識別子|
|ID|列の識別子|
|LENGTH|列のサイズ|
|TABLE_ID|テーブル識別子|
|FLAG|非公開データ|
|PART_PAGE_COUNT|未使用|
|PAGE_VALUE_COUNT|未使用|
|MINMAX_CACHE_SIZE|未使用|
|MAX_CACHE_PART_COUNT|未使用|

### V$RETENTION_JOB {#vretention_job}
---

保持ポリシーを適用したテーブルの情報です。

|列名|説明|
|-------------------|------------------------------------------|
| USER_NAME         |ユーザー名|
| TABLE_NAME        |対象TAG TABLE名|
| POLICY_NAME       |適用されているPOLICY名|
| STATE             |RETENTION状態（RUNNING/WAITING/STOPPED）|
| LAST_DELETED_TIME |最後に成功した削除処理の基準時刻（この時刻より前のデータが削除対象）|

### V$USER_AUTH_KEYS {#vuser_auth_keys}
---

チャレンジ認証用の登録公開鍵を表示します。

|列名|説明|
|--|--|
|KEY_ID|鍵識別子|
|USER_ID|ユーザー識別子|
|USER_NAME|ユーザー名|
|KEY_ALGO|鍵アルゴリズム|
|KEY_PARAM|鍵パラメーター|
|PUBKEY|公開鍵テキスト。X.509 から登録した場合は抽出した公開鍵|
|ACTIVATED|鍵が有効かどうか|
|VALID_AFTER|鍵の有効期間の開始日|
|VALID_BEFORE|鍵の有効期間の終了日|
|ADDITIONAL_INFO|サーバー生成のメタデータ。例：`type=PUBLIC_KEY`、`type=CERTIFICATE; cert_not_after=YYYY-MM-DD`|
|COMMENT|鍵の説明|
