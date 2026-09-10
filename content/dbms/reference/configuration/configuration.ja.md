---
type: docs
title: '16.2.1 設定プロパティ辞典'
weight: 10
toc: true
---

`$MACHBASE_HOME/conf/machbase.conf`で設定するStandard Editionの主なプロパティの辞典です。
特に記載がない場合はサーバーの再起動が必要です。

## サーバーの基本設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `PORT_NO` | 5656 | 1024~65535 | クライアントのTCP/IP接続ポート |
| `BIND_IP_ADDRESS` | 0.0.0.0 | - | クライアントリスナーのバインドIP。`0.0.0.0`はすべてのインターフェース |
| `GRANT_REMOTE_ACCESS` | 1 | 0~1 | リモート接続の許可。0はローカル接続のみ許可 |
| `MAX_SESSION_COUNT` | 4096 | 64~2^64-1 | 同時セッションの最大数 |
| `MAX_STMT_COUNT_PER_SESSION` | 1024 | 512~2^32-1 | セッション当たりの最大ステートメント数 |
| `SESSION_IDLE_TIMEOUT_SEC` | 0 | 0~2^64-1 | セッションのアイドルタイムアウト（秒）。0は無効 |
| `SESSION_QUERY_TIMEOUT_SEC` | 0 | 0~2^64-1 | クエリ実行タイムアウト（秒）。0は無効 |
| `UNIX_PATH` | machbase-unix | - | Unixドメインソケットのファイル名 |
| `DBS_PATH` | ?/dbs | - | データベースファイルの保存先（`?`は`$MACHBASE_HOME`） |
| `PID_PATH` | ?/conf | - | PIDファイルの保存先 |

## CPU / スレッド設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `CPU_COUNT` | 1 | 0~2^32-1 | 使用するCPU数。0はすべて使用 |
| `CPU_PARALLEL` | 1 | 1~2^32-1 | CPU当たりの並列スレッド数 |
| `CPU_AFFINITY_BEGIN_ID` | 0 | 0~2^32-1 | CPUアフィニティの開始番号 |
| `CPU_AFFINITY_COUNT` | 0 | 0~2^32-1 | CPUアフィニティで使用するCPU数。0はすべて |
| `DISK_IO_THREAD_COUNT` | 3 | 1~2^32-1 | ディスクI/Oスレッド数 |
| `INDEX_BUILD_THREAD_COUNT` | 3 | 0~2^32-1 | インデックス構築スレッド数。0はインデックスを作成しない |
| `INDEX_LEVEL_PARTITION_BUILD_THREAD_COUNT` | 3 | 1~1024 | LSMインデックスのマージスレッド数 |
| `INDEX_LEVEL_PARTITION_AGER_THREAD_COUNT` | 1 | 1~1024 | LSMインデックスの不要ファイル削除スレッド数 |
| `QUERY_PARALLEL_FACTOR` | 0 | 0~100 | 並列クエリ実行スレッド数。Standardのデフォルト値は0、Clusterは4 |

## メモリ設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `PROCESS_MAX_SIZE` | 8GB | 1GB~2^64-1 | サーバープロセスの最大メモリ（バイト）。配布サンプルでは`16GB`の場合がある |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE` | 8GB | 256MB~2^64-1 | LOGテーブルの入力バッファー上限。総メモリ予算内で調整 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_MIN_SIZE` | 100MB | 1MB~2^64-1 | サーバー起動時に事前確保するメモリ |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_EXT_SIZE` | 2MB | 1MB~2^64-1 | 列パーティションのメモリブロックサイズ |
| `DISK_COLUMNAR_TABLESPACE_DWFILE_INT_SIZE` | 2MB | 1MB~2^32-1 | データの整合性/復旧用ダブルライトファイルの初期サイズ |
| `DISK_COLUMNAR_TABLESPACE_DWFILE_EXT_SIZE` | 1MB | 1MB~2^32-1 | ダブルライトファイルの拡張サイズ |
| `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` | 2GB | 0~2^64-1 | ページキャッシュの最大サイズ（バイト） |
| `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` | 2GB | 0~2^64-1 | Volatile/Lookupテーブル全体のメモリ上限 |
| `MAX_QPX_MEM` | 1GB | 1MB~2^64-1 | GROUP BY/ORDER BYなどのクエリ処理の最大メモリ |
| `MEMORY_ROW_TEMP_TABLE_PAGESIZE` | 32768 | 8KB~2^32-1 | Volatile/Lookup一時テーブルのページサイズ（バイト） |

## ディスクI/O設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `DISK_BUFFER_COUNT` | 16 | 1~2^32-1 | ディスクI/Oバッファー数 |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 0~1 | 書き込みのDirect I/Oの有効化。ZFSなど非対応のファイルシステムでは0に設定 |
| `DISK_TABLESPACE_DIRECT_IO_READ` | 0 | 0~1 | 読み取りのDirect I/Oの有効化 |
| `DISK_TABLESPACE_DIRECT_IO_FSYNC` | 0 | 0~1 | Direct I/Oでのfsyncの有効化 |
| `DISK_TABLESPACE_SYNCHRONOUS` | 1 | 0~3 | 同期ポリシー。0=OFF, 1=NORMAL, 2=FULL, 3=EXTRA |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | 0~2^32-1 | パーティションファイルをディスクへ反映する間隔（秒） |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE` | 0 | 0~1 | 列パーティションが満杯になったときだけフラッシュするかどうか |
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 1~2^32-1 | テーブルのチェックポイント間隔（秒） |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 1~2^32-1 | インデックスのチェックポイント間隔（秒） |
| `DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE` | 1 | 0~1 | LOGの時刻逆転時、1=直前の時刻+1nsに補正、0=入力を拒否 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_HIGH_LIMIT_PCT` | 80 | 0~100 | メモリ使用量のしきい値（%）。超過時は入力速度を低下 |
| `DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_MSEC` | 1 | 0~2^32-1 | しきい値超過時のレコード当たりの待機時間（ms） |

LOGの`DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE=1`は、明示した過去の時刻をそのまま
保存するという意味ではありません。直前の`_ARRIVAL_TIME`より小さい値は補正されます。
同じ時刻はこの逆転条件に該当しないため、すべての行の時刻が一意になるわけでもありません。
移行時には[時間モデル](/dbms/log-table-usage/arrival-time-model/)のソート順と対象の状態も確認してください。

## インデックス設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `DEFAULT_LSM_MAX_LEVEL` | 2 | 0~3 | LSMインデックスのデフォルト最大レベル |
| `INDEX_BUILD_MAX_ROW_COUNT_PER_THREAD` | 100000 | 1~2^32-1 | インデックス構築を開始する未インデックスレコード数 |
| `INDEX_FLUSH_MAX_REQUEST_COUNT_PER_INDEX` | 3 | 1~2^32-1 | インデックス当たりの最大フラッシュ要求数 |
| `INDEX_LEVEL_PARTITION_BUILD_MEMORY_HIGH_LIMIT_PCT` | 70 | 0~100 | LSMインデックス構築時の最大メモリ使用率（%） |
| `DISK_COLUMNAR_INDEX_SHUTDOWN_BUILD_FINISH` | 0 | 0~1 | 終了時にすべてのインデックスをディスクへ反映するかどうか |
| `DISK_COLUMNAR_INDEX_FDCACHE_COUNT` | 0 | 0~2^32-1 | オープンするインデックスパーティションのファイル記述子数 |
| `DISK_COLUMNAR_TABLE_COLUMN_FDCACHE_COUNT` | 0 | 0~2^32-1 | オープンする列のファイル記述子数 |
| `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` | 100MB | 0~2^64-1 | `_ARRIVAL_TIME`列のMINMAXキャッシュサイズ（バイト） |

## TAGテーブル設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `TAG_CACHE_ENABLE` | 31 | 0~31 | TAGキャッシュの使用範囲（ビットOR）。0=無効, 1=map, 2=row, 4=data file, 8=varchar file, 16=delete vector |
| `TAG_CACHE_MAX_MEMORY_SIZE` | 512MB | 32KB~2^64-1 | TAGキャッシュプール1つ当たりの最大メモリ（バイト） |
| `TAG_CACHE_POOL_COUNT` | 1 | 1~128 | TAGキャッシュプール数。総上限 = `TAG_CACHE_MAX_MEMORY_SIZE × TAG_CACHE_POOL_COUNT` |
| `TAG_MEMORY_INDEX_TYPE` | 1 | 0~1 | メモリインデックスの種類。0=RBTree, 1=BTree |
| `TAG_MEMORY_INDEX_PANOUT` | 255 | 127~65536 | B-Treeインデックスの次数。`TAG_MEMORY_INDEX_TYPE=1`で適用 |
| `TAGDATA_AUTO_META_INSERT` | 2 | 0~2 | TAG_NAMEが存在しない場合の処理。0=失敗、1=名前のみ挿入、2=メタデータを含めて挿入 |
| `TAG_TABLE_META_MAX_SIZE` | 524288000 | 1MB~2^32-1 | TAGDATAテーブルのメタデータの最大メモリ（バイト） |
| `TAG_PARTITION_COUNT` | 4 | 1~1024 | TagテーブルのKey Valueパーティション数 |
| `TAG_DATA_PART_SIZE` | 16MB | 1MB~1GB | Tagデータパーティションサイズ（バイト） |
| `ROLLUP_FETCH_COUNT_LIMIT` | 3000000 | 0~2^32-1 | ロールアップスレッドが1回にフェッチするデータ数。0は無制限 |

## セキュリティ設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `ENABLE_CASE_SENSITIVE_PASSWORD` | 0 | 0~1 | パスワードの大文字小文字の区別。0は大文字に変換 |

## セッション / クエリ設定

`TABLE_SCAN_DIRECTION`はTAG専用の設定ではありません。LOGなど、スキャン方向を使用する
クエリにも影響する場合があります。最終出力のソート順も保証しません。
出力順序はORDER BYで指定し、実際のアクセスパスはEXPLAINで確認してください。

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `TABLE_SCAN_DIRECTION` | 0 | -1~1 | -1=逆方向、0=テーブルタイプのデフォルト値、1=順方向 |
| `DDL_LOCK_TIMEOUT` | 0 | 0~1000000 | Standard EditionのDDLロック待機時間（秒）。0は即座にエラーを返す |
| `SHOW_HIDDEN_COLS` | 0 | 0~1 | `SELECT *`で`_ARRIVAL_TIME`列を表示するかどうか |
| `DURATION_BEGIN` | 0 | 0~2^32-1 | `DURATION`を指定しないSELECTのデフォルト開始オフセット（秒） |
| `DURATION_GAP` | 0 | 0~2^31-1 | `DURATION`を指定しないSELECTのデフォルト期間（秒） |
| `LOOKUP_APPEND_UPDATE_ON_DUPKEY` | 0 | 0~1 | LookupテーブルへのAppend時の重複キー処理。0=失敗、1=UPDATE |
| `LIN_HASH_BIT_SIZE` | 7 | 1~31 | 内部リニアハッシュの初期バケットビット数 |

`machbase.conf`の`DDL_LOCK_TIMEOUT`は、サーバー再起動後に新規セッションへコピーされます。
現在のセッションの値は`ALTER SESSION SET DDL_LOCK_TIMEOUT = seconds`で変更し、`V$SESSION`で確認します。
Cluster Editionではこのプロパティを提供しません。

## TRANSACTION設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `TRANSACTION_BUSY_TIMEOUT_MS` | 30000 | -1~2147483647 | 再試行可能なTRANSACTIONロック競合の待機時間（ms）。-1はキャンセル・解除まで待機、0は即座に返す |
| `TRANSACTION_SYNCHRONOUS` | 2 | 1~2 | TRANSACTIONテーブルのトランザクション永続性レベル。1=NORMAL, 2=FULL |
| `TRANSACTION_JOURNAL_MODE` | 4 | 0~4 | TRANSACTIONのジャーナルモード。0=DELETE, 4=WAL |

新規セッションはサーバーのTRANSACTION_BUSY_TIMEOUT_MSをコピーします。現在の接続では
ALTER SESSIONで変更できます。この値は、すべてのbusyエラーの最小待機時間を保証しません。
WALで古い読み取りスナップショットを書き込みに切り替える際の競合は、-1でも即座に返される場合があります。
この場合は同じ文を繰り返さず、ROLLBACKして新しいトランザクションで読み取りと判断からやり直してください。
[2つの接続を使う演習](/dbms/rdb-table-usage/locking-conflict-timeout/)では、
一時的な書き込みロックとスナップショットの競合を比較できます。

## ログ / 診断設定

| プロパティ | デフォルト値 | 範囲 | 説明 |
|----------|--------|------|------|
| `TRACE_LOG_LEVEL` | 277 | 0~2^32-1 | トレースログの詳細レベル。値が大きいほど詳細 |
| `TRACE_LOGFILE_PATH` | ?/trc | - | トレースログファイルの保存先 |
| `TRACE_LOGFILE_SIZE` | 10MB | 1MB~2^32-1 | トレースログファイルの最大サイズ（バイト） |
| `TRACE_LOGFILE_COUNT` | 1000 | 1~2^32-1 | トレースログファイルの最大数 |
| `DUMP_TRACE_INFO` | 300 | 0~2^32-1 | DBMSの状態をtrcに記録する間隔（秒）。0は無効 |
| `DUMP_APPEND_ERROR` | 0 | 0~1 | Append APIのエラーをtrcに記録するかどうか。テスト目的のみの使用を推奨 |
| `FEEDBACK_APPEND_ERROR` | 1 | 0~1 | Appendのエラーデータをクライアントに送信するかどうか |
| `GEN_CORE_FILE` | 1 | 0~1 | 異常終了時のcoreファイル生成の有効化 |
| `GEN_CALLSTACK_FOR_ABORT_ERROR` | 0 | 0~1 | 異常終了時のコールスタック記録の有効化 |

## プロパティの参照例

```sql
-- 現在適用されているすべてのプロパティ値を参照
SELECT name, value, type FROM v$property ORDER BY name;

-- 特定のプロパティの詳細を参照
SELECT name, value, min, max
  FROM v$property
 WHERE name = 'MAX_SESSION_COUNT';
```

動的に変更できるプロパティは、サーバーを再起動せずに`ALTER SYSTEM SET`で変更できます。

```sql
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET SESSION_QUERY_TIMEOUT_SEC = 30;
```
