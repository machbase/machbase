---
layout : post
title : 'エラーコード'
type: docs
weight: 10
toc: true
---

| コード | サーバーメッセージ（原文） | 説明 |
|--|--|--|
|1|Failed to create file<%s>, errno = %d.|ファイルの作成に失敗しました。|
|2|Failed to truncate file<%s>, errno = %d.|ファイルの切り詰めに失敗しました。|
|3|Failed to duplicate file<%s>, errno = %d.|ファイルの複製に失敗しました。|
|4|Failed to copy file<%s> to file<%s>, errno = %d.|ファイルの複製に失敗しました。|
|5|Failed to rename file<%s> to file<%s>, errno = %d.|ファイル名の変更に失敗しました。|
|6|Failed to remove file<%s>, errno = %d.|ファイルの削除に失敗しました。|
|7|Failed to get key file<%s>, errno = %d.|ファイルのキーの取得に失敗しました。|
|8|Failed to create pipe<%s>, errno = %d.|パイプの作成に失敗しました。|
|9|Failed to statistic file<%s>, errno = %d.|ファイルの統計情報の取得に失敗しました。|
|10|Failed to open file<%s>, errno = %d.|ファイルを開けませんでした。|
|11|Failed to close file<%s>, errno = %d.|ファイルを閉じられませんでした。|
|12|Failed to seek file<%s>, offset:%lld, Whence:%d, errno = %d.|ファイルのシークに失敗しました。|
|13|Failed to read file<%s>, size:%llu, errno = %d.|ファイルの読み取りに失敗しました。|
|14|Failed to write file<%s>, size:%llu, errno = %d.|ファイルの書き込みに失敗しました。|
|15|Failed to read file<%s> (offset:%llu, req size:%llu, read size: %llu), errno = %d.|ファイルの読み取りに失敗しました。|
|16|Failed to write file<%s> (offset:%llu, req size:%llu, read size: %llu), errno = %d.|ファイルの書き込みに失敗しました。|
|17|Failed to sync file<%s>, errno = %d.|ファイルの同期に失敗しました。|
|18|Failed to lock file<%s>, errno = %d.|ファイルのロックに失敗しました。|
|19|Failed to trylock file<%s>, errno = %d.|ファイルのロック試行に失敗しました。|
|20|Failed to unlock file<%s>, errno = %d.|ファイルのロック解除に失敗しました。|
|21|There is no file extension.|ファイルの拡張子エラーが発生しました。|
|22|Failed to rename file<%s> to file<%s>, retry count<%d>, msec<%d>, errno = %d.|ファイル操作に失敗しました。|
|31|Error occurred during snprintf: buffer size<%d>, errno = %d.|snprintf の実行中にエラーが発生しました。|
|61|Failed to getenv variable<%s>, errno = %d.|環境変数の取得に失敗しました。|
|62|Failed to setenv variable<%s> to value<%s>, errno = %d.|環境変数の設定に失敗しました。|
|67|Failed to opendir <%s>, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|68|Failed to closedir, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|69|Failed to readdir, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|70|Failed to rewinddir, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|71|Failed to makedir <%s>, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|72|Failed to removedir, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|73|Failed to setcwd, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|74|Failed to getcwd, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|75|Failed to gethome, errno = %d.|ホームディレクトリの取得に失敗しました。|
|76|Path<%s> is too long, errno = %d.|ファイルパスのエラーが発生しました。|
|77|Path<%s/%s> is too long, errno = %d.|ファイルパスのエラーが発生しました。|
|78|Path<%s/%s/%s> is too long, errno = %d.|ファイルパスのエラーが発生しました。|
|79|The directory does not exist in this path<%s>, errno = %d.|ディレクトリ関連の関数が失敗しました。|
|80|Failed to call removedir (%s), errno = %d.|ディレクトリ関連の関数が失敗しました。|
|91|%1$s(): [%2$d: %3$s]|メタデータベース関連の関数が失敗しました。|
|92|%1$s(): [%2$d: %3$s]|メタデータベース関連の関数が失敗しました。|
|121|Stack create failed, errno = %d.|スタックデータ構造のエラーが発生しました。|
|122|Stack push failed, errno = %d.|スタックデータ構造のエラーが発生しました。|
|123|Stack pop failed, errno = %d.|スタックデータ構造のエラーが発生しました。|
|131|Failed to allocate memory(%lu bytes), errno = %d.|メモリの割り当てに失敗しました。|
|132|Memory allocation error (alloc'd: %llu, max: %llu).|メモリの割り当てに失敗しました。|
|133|Failed to allocate memory (ID = %d) (Request Size = %llu) : (Current Allocated Size / PROCESS_MAX_SIZE (%llu/%llu)).|メモリの割り当てに失敗しました。|
|141|Failed to create memory pool, errno = %d.|メモリの割り当てに失敗しました。|
|142|Failed to allocate memory from memory pool, errno = %d.|メモリの割り当てに失敗しました。|
|151|Failed to create mutex, errno = %d.|ミューテックスオブジェクトのエラーが発生しました。|
|152|Failed to destroy mutex, errno = %d.|ミューテックスオブジェクトのエラーが発生しました。|
|153|Failed to lock mutex, errno = %d.|ミューテックスのロックエラーが発生しました。|
|154|Failed to trylock mutex, errno = %d.|ミューテックスのロックエラーが発生しました。|
|155|Failed to unlock mutex, errno = %d.|ミューテックスのロック解除エラーが発生しました。|
|161|Failed to create queue, errno = %d.|キューデータ構造のエラーが発生しました。|
|162|Failed to destroy queue, errno = %d.|キューデータ構造のエラーが発生しました。|
|163|Failed to enqueue queue, errno = %d.|キューデータ構造のエラーが発生しました。|
|164|Failed to dequeue queue, errno = %d.|キューデータ構造のエラーが発生しました。|
|171|Failed to create thread_attr, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|172|Failed to destroy thread_attr, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|173|Failed to set thread_attr bound, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|174|Failed to set thread_attr detach, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|175|Failed to set thread_attr stack size, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|176|Failed to create thread, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|177|Failed to detach thread, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|178|Failed to join thread, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|179|Failed to get id of thread, errno = %d.|スレッド関連の関数でエラーが発生しました。|
|191|Failed to create thread condition variable, errno = %d.|スレッドの条件変数を作成できませんでした。|
|192|Failed to destroy thread condition variable, errno = %d.|スレッドの条件変数を削除できませんでした。|
|193|Failed to call cond_timedwait, errno = %d.|cond_timedwait の呼び出しに失敗しました。|
|194|Failed to call cond_signal, errno = %d.|cond_signal の呼び出しに失敗しました。|
|195|Failed to call cond_broadcast, errno = %d.|cond_broadcast の呼び出しに失敗しました。|
|196|Failed to call cond_wait, errno = %d.|cond_wait の呼び出しに失敗しました。|
|201|Failed to create rwlock, errno = %d.|rwlock の作成に失敗しました。|
|202|Failed to destroy rwlock, errno = %d.|rwlock の削除に失敗しました。|
|203|Failed to call rwlock_lock_read, errno = %d.|rwlock_lock_read の呼び出しに失敗しました。|
|204|Failed to call rwlock_trylock_read, errno = %d.|rwlock_trylock_read の呼び出しに失敗しました。|
|205|Failed to call rwlock_lock_write, errno = %d.|rwlock_lock_write の呼び出しに失敗しました。|
|206|Failed to call rwlock_trylock_write, errno = %d.|rwlock_trylock_write の呼び出しに失敗しました。|
|211|RBTREE buffer<%d> is too small for value<%d>, errno = %d.|値を格納する RBTREE バッファーが小さすぎます。|
|212|RBTREE cursor op not applicable. errno = %d.|RBTREE カーソルでこの操作は実行できません。|
|213|RBTREE node is already freed, errno = %d.|RBTREE ノードは既に解放されています。|
|216|Key already exists.|キーが既に存在します。|
|221|LZO compress failed, errno = %d.|LZO 圧縮に失敗しました。|
|222|LZO decompress failed, errno = %d.|LZO の展開に失敗しました。|
|231|Failed to get CPU count, errno = %d.|CPU 数の取得に失敗しました。|
|232|Configuration file does not exist(%S).|使用しません。|
|251|Tlsf memory manager initialization failed, errno = %d.|TLSF メモリマネージャーの初期化に失敗しました。|
|252|Tlsf memory manager finalization failed, errno = %d.|TLSF メモリマネージャーの終了処理に失敗しました。|
|253|Tlsf memory manager allocation(%lld) failed, errno = %d.|TLSF メモリマネージャーによる割り当てに失敗しました。|
|254|Tlsf memory manager free failed, errno = %d.|TLSF メモリマネージャーによる解放に失敗しました。|
|255|Tlsf memory manager control failed, errno = %d.|TLSF メモリマネージャーの制御に失敗しました。|
|256|Tlsf memory manager shrink failed, errno = %d.|TLSF メモリマネージャーの縮小に失敗しました。|
|257|Tlsf memory manager getstatistics failed, errno = %d.|TLSF メモリマネージャーの統計情報の取得に失敗しました。|
|271|The session is closed.|セッションは閉じられています。|
|272|The session is canceled.|セッションはキャンセルされています。|
|291|The license is invalid or expired.|ライセンスが無効、または期限切れです。|
|292|The value<%s> does not exist in the license file.|該当する値がライセンスファイルにありません。|
|293|Failed to get hardware key, errno =%d|ハードウェアキーの取得に失敗しました。|
|294|Failed to verify the license, errno = %d|ライセンスの確認に失敗しました。|
|300|Invalid date value.(%s)|日時の値が無効です。|
|301|Invalid network string.(%s)|IP アドレスの文字列が無効です。|
|321|Error in initializing sha1, errno = %d|sha1 の初期化に失敗しました。|
|322|Error in updating sha1, errno = %d|sha1 の更新に失敗しました。|
|323|Error in finalizing sha1, errno = %d|sha1 の終了処理に失敗しました。|
|324|Invalid SHA type.(%d)|SHA 型が無効です。|
|326|Invalid SHA hex string.(%s)|SHA の 16 進文字列が無効です。|
|341|Parallel job thread abnormally terminated|並列処理のスレッドが異常終了しました。|
|342|The thread count should be between %d and %d|スレッド数は指定範囲内である必要があります。|
|361|Error in setting a log to the buffer of the result file: %s, errno = %d|出力ファイルのバッファーにログを設定する際にエラーが発生しました。|
|381|Regular expression error: an error occurred at offset %d of (%s).|正規表現の指定位置でエラーが発生しました。|
|400|This DB file is older than binary (no meta-version table). Check database image and binary.|DB ファイルが実行ファイルより古いバージョンです。DB イメージと実行ファイルを確認してください。|
|401|Version mismatched. In Executable DB(%d.%d) META(%d.%d) CM(%d.%d) But, In File DB(%d.%d) META(%d.%d) CM(%d.%d)|バージョンが一致しません。実行ファイルとデータベースファイルのバージョンが異なります。|
|420|Error in getting system information by the sysinfo, errno = %d|システム情報の取得中にエラーが発生しました。|
|421|Error in getting stack information by the pmuSysSetStackSize, errno = %d|pmuSysSetStackSize によるスタック情報の取得中にエラーが発生しました。|
|422|Error in setting stack information by the pmuSysSetStackSize, errno = %d|pmuSysSetStackSize によるスタック情報の設定中にエラーが発生しました。|
|431|mmap (size<%u>) error, errno = %d|mmap エラーが発生しました。|
|432|unmap (address<%p>, size<%u>) error, errno = %d|unmap エラーが発生しました。|
|451|Failed to set the CPU affinity [%u, %u), errno = %d|CPU アフィニティの設定に失敗しました。|
|452|The IDs of CPUs should be between [0, %u), but [%u, %u) given.|CPU ID は指定範囲内である必要があります。|
|453|Maximum abs value of CPU_AFFINITY_COUNT(%d) should be less than CPU count(%u).|CPU_AFFINITY_COUNT の絶対値の最大値は CPU 数未満である必要があります。|
|461|Failed to get the number of CPUs in sysconf, errno = %d|sysconf による CPU 数の取得に失敗しました。|
|471|Failed to initialize a heap.|ヒープデータ構造のエラーが発生しました。|
|472|Heap push failed, errno = %d|ヒープデータ構造のエラーが発生しました。|
|491|Error in json dump.|JSON の操作・変換エラーが発生しました。|
|492|Error in json load.|JSON の操作・変換エラーが発生しました。|
|493|json object error: %s|JSON の操作・変換エラーが発生しました。|
|494|Error in json-array.|JSON の操作・変換エラーが発生しました。|
|495|Error in json-string (%s).|JSON の操作・変換エラーが発生しました。|
|496|Error in json-integer (%lld).|JSON の操作・変換エラーが発生しました。|
|497|Error in json-real (%lf).|JSON の操作・変換エラーが発生しました。|
|498|Error in json copy.|JSON の操作・変換エラーが発生しました。|
|499|Error in json pack.|JSON の操作・変換エラーが発生しました。|
|500|Error in json unpack.|JSON の操作・変換エラーが発生しました。|
|501|No data matches for the json path (%s)|JSON の操作・変換エラーが発生しました。|
|502|Json path is too long.|JSON の操作・変換エラーが発生しました。|
|503|Error json object set (%s).|JSON の操作・変換エラーが発生しました。|
|504|Error json array append.|JSON の操作・変換エラーが発生しました。|
|505|Error encode base64.|Base64 エンコードエラーが発生しました。|
|506|Error decode base64.|Base64 デコードエラーが発生しました。|
|600|Invalid property value: %s.|プロパティ値が無効です。|
|601|Failed to convert %s to UTF8. (%s, errno=%d)|UTF8 への変換に失敗しました。|
|602|Buffer size is not enough for code conversion. (%d > %d)|文字コード変換用のバッファーサイズが不足しています。|
|701|Geohash invalid precision (%u)|geohash の精度が無効です。|
|702|Geohash invalid length|geohash の長さが無効です。|
|703|Geohash invalid direction|geohash の方向が無効です。|
|1000|File<%s> is invalid.|ファイルが無効です。|
|1001|Invalid object storage id, errno = %d.|オブジェクトストレージが無効です。|
|1002|Object storage<%d> already freed, errno = %d.|オブジェクトストレージは既に解放されています。|
|1003|Group storage dir<%s> already exists, errno = %d.|グループストレージのディレクトリが既に存在します。|
|1004|Object filename<%s> is invalid, errno = %d.|オブジェクトのファイル名が無効です。|
|1005|Disk file<%s> is in use, errno = %d.|ディスクファイルが使用中です。|
|1006|Functionality is not supported yet.|この機能はまだサポートしていません。|
|1007|There is no available disk space for writing <%lld>bytes to the file<%s>, errno = %d.|ファイルへの書き込みに必要なディスク空き容量がありません。|
|1008|Error in the duplicating file<%s>, errno = %d.|ファイルの複製中にエラーが発生しました。|
|1009|Error in the read file size.(<io: %u>, <disk: %u>)|読み取ろうとしたサイズと実際に読み取ったサイズが異なります。|
|1010|Used media space is reached to threshold. (%4.1lf%% cap < %4.1lf%% used)|使用中のメディア容量がしきい値に達しました。|
|1011|Error in the write file size.(<write: %u>, <written: %u>)|書き込もうとしたサイズと実際に書き込んだサイズが異なります。|
|1031|The database in <%s> has already been mounted.|データベースは既にマウントされています。|
|1032|The database in <%s> is not mounted.|データベースはマウントされていません。|
|1033|The mount operation of database in <%s> is not completed.|データベースのマウント処理が完了していません。|
|1034|The mounted database<%s> is busy.|マウントしたデータベースが使用中です。|
|1035|The database creation is not complete. Destroy it and create a new one.|データベースの作成が完了していません。削除して再作成してください。|
|1036|The database creation is not complete. Destroy it and create a new one.|データベースの作成が完了していません。削除して再作成してください。|
|1037|The mount database<%s> is not backed up from the primary database|マウントしたデータベースは、現在のデータベースから取得したバックアップではありません。|
|1038|Cannot find MountDB with <TBSID: %lld>.|該当する TBSID に対応する MountDB が見つかりません。|
|1039|Mount DB<%s>'s state is invalid.|マウントデータベースの状態が無効です。|
|1101|Error in reading column partition cache block. Reading block of RID<%lld> in the column partition<%lld> failed, errno = %d.|列パーティションのキャッシュブロックの読み取り中にエラーが発生しました。|
|1102|Invalid cache object.|キャッシュオブジェクトが無効です。|
|1103|Error occurred in checkpoint thread. Processing abnormal shutdown.|チェックポイントスレッドでエラーが発生し、処理中に異常終了しました。|
|1104|Error in waiting to read a page.|ページの読み取り待機中にエラーが発生しました。|
|1105|Error in clear thread of the page cache.|ページキャッシュのクリアスレッドでエラーが発生しました。|
|1106|It<%llu> is smaller than the max size value of the page cache currently set<%llu>.|現在設定されているページキャッシュの最大サイズより小さい値です。|
|1107|It<%llu> is impossible to set a value larger than the memory size set in the current process<%llu>.|現在のプロセスに設定されたメモリサイズを超える値は指定できません。|
|1108|Invalid page id in column partition. Page id<%d> is greater than the page max id<%d>.|列パーティションのページ ID が最大ページ ID を超えています。|
|1201|Duplicated table id<%llu> in SYS_STORAGE_TABLES, errno = %d.|SYS_STORAGE_TABLES に重複するテーブル ID があります。|
|1202|Duplicated table id<%llu>, column id<%u> in the SYS_STORAGE_COLUMNS, errno = %d.|SYS_STORAGE_COLUMNS に重複するテーブル ID と列 ID があります。|
|1203|Table id<%lld> does not exist in SYS_STORAGE_TABLES, errno = %d.|テーブル ID が SYS_STORAGE_TABLES に存在しません。|
|1204|Duplicated (table id<%llu>, index id<%llu>) in SYS_STORAGE_INDEXES, errno = %d.|SYS_STORAGE_INDEXES に重複する項目があります。|
|1205|Duplicated (table id<%llu>, index id<%llu>, column id<%u>) in SYS_STORAGE_INDEXES_COLUMNS, errno = %d.|SYS_STORAGE_INDEXES_COLUMNS に重複する項目があります。|
|1206|Index id<%llu> of table id<%llu> dose not exist in SYS_STORAGE_INDEXES, errno = %d.|テーブルのインデックス ID が SYS_STORAGE_INDEXES に存在しません。|
|1207|Available recovery modes: simple, complex, reset|使用できる復旧モードは simple、complex、reset です。|
|1301|Partition range does not exist. Partition id is less than <%lld> in the table(id<%lld>) with partitions between <%lld> and <%lld>.|パーティション範囲が存在しません。指定範囲内のパーティションがテーブルにありません。|
|1302|Invalid record range. No such record whose id is less than <%llu> in the table(id<%llu>) with records between <%llu> and <%llu>.|レコード範囲が無効です。指定範囲内のレコードがテーブルにありません。|
|1303|Maximum number of columns in a table is %d.|テーブルに指定できる列数の上限は %d です。|
|1304|Invalid column ID (<%d>).|列 ID が無効です。|
|1305|Invalid table ID (<%llu>).|テーブル ID が無効です。|
|1306|Table has been dropped.|テーブルが削除されました。|
|1307|Table structure was modified.|テーブル構造が変更されました。|
|1308|Invalid fixed column size. Invalid value size(<%u>) for the fixed column.|固定長列のサイズが無効です。|
|1309|Invalid varying column size. Value size(<%u>) for the variable column is greater than the max size (<%u>).|可変長列のサイズが最大値を超えています。|
|1310|Table flush thread terminated abnormally.|テーブルのフラッシュスレッドが異常終了しました。|
|1311|Table column partition prepare thread terminated abnormally.|テーブルの列パーティション準備スレッドが異常終了しました。|
|1312|Failed to read the head of the table column partition file (<%s>).|テーブルの列パーティションファイルのヘッダーを読み取れませんでした。|
|1313|Failed to read the table column partition file (<%s>).|テーブルの列パーティションファイルを読み取れませんでした。|
|1314|Index build thread terminated abnormally.|インデックス構築スレッドが異常終了しました。|
|1315|Invalid table type<%d>.|テーブルタイプが無効です。|
|1316|Column size<%u> is too big.|列のサイズが大きすぎます。|
|1317|Value of the time column(<%lld>) is less than the last time value(<%lld>).|時刻列の値が最後の時刻値より小さい値です。|
|1318|The size of VARCHAR column must be less than (<%llu>).|VARCHAR 列のサイズを小さくする必要があります。|
|1319|The size of column value must be less than (<%u>).|列の値のサイズを小さくする必要があります。|
|1320|There is an index on the column(<%u>) of the table(<%llu>)|テーブルの列にインデックスが存在します。|
|1321|This feature is not supported on this table type.|このテーブルタイプでは、この機能をサポートしていません。|
|1322|The new column size(<%u>) should be greater than the old one(<%u>)|新しい列のサイズは既存の列のサイズより大きい必要があります。|
|1323|The table(%llu) reached max column count limit (%u) already.|テーブルの列数が既に上限に達しています。|
|1324|An error occurred adjusting end rid of the table<%llu> column partition(<%llu>), errno = %d.|テーブルの列パーティションの終了 RID を調整する際にエラーが発生しました。|
|1325|The end RID<%lld> of the column<%d> is less than the end RID<%llu> of the table<%llu>|列の終了 RID がテーブルの終了 RID より小さい値です。|
|1330|The column with ID<%hu> does not exist in the table with ID<%llu>|該当する ID の列がテーブルに存在しません。|
|1331|Table checkpoint thread terminated abnormally.|テーブルのチェックポイントスレッドが異常終了しました。|
|1332|Partition ID <%llu> of the table(id<%llu>) does not exist between <%llu> and <%llu>.|テーブルのパーティション ID が指定範囲内に存在しません。|
|1333|The table<%llu> in the backup database<%s> has been mounted already.|バックアップデータベースのテーブルは既にマウントされています。|
|1334|The table is busy with mounting.|テーブルをマウント中です。|
|1335|The mounted table is busy with unmounting.|マウントしたテーブルをマウント解除中です。|
|1336|The mounted table is invalid.|マウントしたテーブルが無効です。|
|1337|The mounted table is busy.|マウントしたテーブルが使用中です。|
|1338|The table is not mounted.|テーブルはマウントされていません。|
|1339|The table<%llu> of the backup tablespace<%s> is different from the table in main database.|バックアップテーブルスペースのテーブルが、現在のデータベースのテーブルと異なります。|
|1340|The table<%llu> of the backup tablespace<%s> is dropped from the main database.|バックアップテーブルスペースのテーブルは、現在のデータベースでは削除されています。|
|1341|There is a mounted table in the table<%llu>.|このテーブルにはマウントしたテーブルがあります。|
|1342|The mount table<end_rid:%llu> has more furture data than the base table<end_rid:%llu.>|マウントしたテーブルには、元のテーブルより先のデータ（終了 RID が大きいデータ）が含まれています。|
|1343|Cannot update columns with indexes in VOLATILE / LOOKUP table.|VOLATILE/LOOKUP テーブルでは、インデックスを持つ列を更新できません。|
|1344|The memory size<%llu bytes> of VOLATILE / LOOKUP tables exceeds <%llu bytes>.|VOLATILE/LOOKUP テーブルのメモリ使用量が上限を超えました。|
|1345|The value of the column<%u> must not be NULL|該当する列の値を NULL にすることはできません。|
|1346|Current Allocate Memory / PROCESS_MAX_SIZE (%llu/%llu), increase PROCESS_MAX_SIZE property and restart.|PROCESS_MAX_SIZE を増やして、割り当てるメモリを拡張し、再起動してください。|
|1401|Invalid index type. Index type<%d> does not exist.|指定したインデックスタイプは存在しません。|
|1402|Index id(<%llu>) does not exist in table id <%llu>.|該当するインデックス ID がテーブルに存在しません。|
|1403|Index has invalid column count(<%d>).|インデックスの列数が無効です。|
|1404|Index has invalid key value count(<%d>).|インデックスのキー値の数が無効です。|
|1405|Index has invalid key value size(<%d>).|インデックスのキー値のサイズが無効です。|
|1406|Index column file(<%s>) is invalid.|インデックスの列ファイルが無効です。|
|1407|Failed to read the head of the index column partition file(<%s>).|インデックスの列パーティションファイルのヘッダーを読み取れませんでした。|
|1408|Failed to read the index column partition file(<%s>).|インデックスの列パーティションファイルを読み取れませんでした。|
|1409|Type of the column for the index is invalid.|インデックスに使用する列の型が無効です。|
|1410|Index flush thread terminated abnormally.|インデックスのフラッシュスレッドが異常終了しました。|
|1411|Index build thread terminated abnormally.|インデックス構築スレッドが異常終了しました。|
|1412|The keyword size<%d> should be less than the max size<%d>.|キーワードのサイズは最大サイズ未満である必要があります。|
|1413|The word bit count(%d) is over than %d in the partition<%lld> of the index <%lld>|インデックスパーティションのワードビット数が上限を超えています。|
|1414|Invalid key count <%u> is not equal to the count <%u> in partition <%lld> of index <%lld>.|キー数がインデックスパーティション内のキー数と一致しません。|
|1415|The level<%u> of the index is bigger than the max level<%u>|インデックスのレベルが最大レベルを超えています。|
|1416|The partition size<%u> of level<%u> is bigger than the max level<%u>|このレベルのパーティションサイズが、最大レベルのパーティションサイズを超えています。|
|1417|The index has been dropped.|インデックスが削除されました。|
|1418|The key already exists in the unique index.|一意インデックスにキーが既に存在します。|
|1419|The primary index is already created on the table.|テーブルには既にプライマリインデックスが作成されています。|
|1420|The number<%llu> of key values is different from the number<%llu> of bitvectors.|キー値の数とビットベクトルの数が異なります。|
|1421|The partition file<%llu> on the level<%u> of the index<%llu> is invalid.(KPC:%u, BPC:%u)|インデックスの該当レベルにあるパーティションファイルが無効です。|
|1422|NULL value is not allowed for the primary index column|プライマリインデックスでは NULL 値を使用できません。|
|1423|TAG cache exhausted, increase TAG_CACHE_MAX_MEMORY_SIZE(%llu)|TAG キャッシュが枯渇しました。TAG_CACHE_MAX_MEMORY_SIZE を増やしてください。|
|1424|Could not allocate TAG cache: (Table,part=%llu,%llu) offset/size=%llu/%llu|TAG キャッシュを割り当てられません。|
|1425|Failed to allocate index memory (Current Allocated Size / Threshold size (%llu/%llu)).|インデックスのメモリ割り当てに失敗しました。|
|1426|Not ready to build keyvalue index (Current Count / Target Count (%llu/%llu) in File).|keyvalue インデックスを構築する準備ができていません。|
|1501|Invalid page id in cpfile. Page id<%d> for the column partition file<%s> is greater than the page max id.|cpfile のページ ID が最大ページ ID を超えています。|
|1502|Error in reading page<%d> in the column partition file<%s>. Page timestamps <head:%lld, tail:%lld> are invalid.|列パーティションファイルの読み取り中に、無効なタイムスタンプを検出しました。|
|1503|Error in reading page<%d> in the column partition file<%s>. Page checksum <write:%#X, read:%#X> are invalid|列パーティションファイルの読み取り中に、無効なページチェックサムを検出しました。|
|1504|The size<%u> of the column partition file<%s> is too small. It is supposed to be greater than the size<%u>|列パーティションファイルのサイズが小さすぎます。|
|1505|The offset<%u> and size<%u> of the update value for the page<id:%u, offset:%u, size:%u> in the column partition file<%s> is invalid|列パーティションファイルのページ更新オフセットとサイズが無効です。|
|1506|The checksum<write:%#X, read:%#X> of the head of the column partition file<%s> is invalid.|列パーティションファイルのヘッダーチェックサムが無効です。|
|1551|Error in getting the fd of the file<%s> from the fd cache.|fd キャッシュからファイル記述子を取得する際にエラーが発生しました。|
|1601|Ager thread terminated abnormally.|Ager スレッドが異常終了しました。|
|1631|There is no root dir<%s> for the database backup.|データベースバックアップのルートディレクトリがありません。|
|1632|The database is not destroyed.|データベースが削除されていません。|
|1633|Failed to write data<%u> of the backup stat file<%s>.|バックアップの stat ファイルに書き込めませんでした。|
|1634|Failed to read data<%u> of the backup stat file<%s>.|バックアップの stat ファイルを読み取れませんでした。|
|1635|The backup statfile<%s> is invalid(CRC<H:%u, B:%u, T:%u).|バックアップの stat ファイルが無効です。|
|1636|The backup <%s> is not completed.|バックアップが完了していません。|
|1637|The backup <%s> has already exist.|バックアップが既に存在します。|
|1638|The end rid<%llu> of the table<%llu> in the restored database is invalid.|復元したデータベースのテーブルの END RID が無効です。|
|1639|The name<%s> of backup is too long, errno = %d.|バックアップ名が長すぎます。|
|1640|The backup file<%s> already exists.|バックアップファイルが既に存在します。|
|1641|The backup file<%s> has the invalid magic string<%s>.|バックアップファイルのマジック文字列が無効です。|
|1642|The header of backup file<%s> has the invalid crc32<%u>.|バックアップファイルのヘッダーの crc32 値が無効です。|
|1643|Length<%u> of backup file<%s> is too long.|バックアップファイルが大きすぎます。|
|1644|The page size <%u> of backup file<%s> is invalid.|バックアップファイルのページサイズが無効です。|
|1645|The file size <%llu> of the head is different from the size<%llu> on the disk.|ヘッダーに記録されたファイルサイズとディスク上のファイルサイズが異なります。|
|1646|The backup file is invalid since the backup is not completed.|バックアップが未完了のため、バックアップファイルが無効です。|
|1647|Incremental backup should be preceded by the last backup.|増分バックアップは既存のバックアップに続けて実行する必要があります。|
|1648|Backup targets are different from that of previous target.|バックアップ対象が既存のバックアップ対象と異なります。|
|1701|The tablespace<%s> is still referenced by other objects such as tables and indexes.|テーブルスペースが他のテーブルやインデックスなどから参照されています。|
|1702|The tablespace<%s> does not exist in the database.|テーブルスペースがデータベースに存在しません。|
|1703|The SYSTEM_TABLESPACE cannot be dropped.|SYSTEM_TABLESPACE は削除できません。|
|1704|Tablespace already exists. <%s>|テーブルスペースが既に存在します。|
|1705|The dir<%s> for the tablespace<%s> of datadisk<%s> already exists.|データディスク用のテーブルスペースディレクトリが既に存在します。|
|1706|Disk<%s> does not exist in the tablespace<%s>.|ディスクがテーブルスペースに存在しません。|
|1707|The parallel I/O of a disk should be between %d and %d.|ディスクの並列 I/O の値が許容範囲外です。|
|1708|Failed to read <%ld> bytes from the file<%s>, errno = %d.|ファイルの読み取りに失敗しました。|
|1709|The page<offset:%u, size:%u> of the file<%s> is invalid because it has the invalid timestamp<head:%lld, tail:%lld>|ファイルページのタイムスタンプが無効です。|
|1710|The page<offset:%u, size:%u> of the file<%s> is invalid because it has the invalid crc<memory:%u, disk:%u>|ファイルページの CRC 値が無効です。|
|1711|Failed to create directory<%s> for virtual disk.|仮想ディスク用のディレクトリを作成できませんでした。|
|1712|Failed to allocate memory for directory to be removed.|ディレクトリ削除用のメモリを割り当てられませんでした。|
|1801|Error in waiting to read value: value offset<%lld>, value size<%u>, and file<%s>|値の読み取り待機中にエラーが発生しました。|
|1821|The image in the DWFile<%s> is invalid.|DW ファイルのイメージが無効です。|
|1841|The operation is aborted by ART.|ART（Automatic Recovery Test）によって処理が中断されました。|
|1851|Variable length columns are not allowed in tag table.|TAG テーブルでは可変長列を使用できません。|
|1852|Another deletion is in progress for table <%llX>.|削除処理が既に実行中です。|
|1853|Cannot create append file for Key-Value table <%llX>, errno = %d.|keyvalue テーブルの append ファイルを作成できません。|
|1854|Cannot sync append file for Key-Value table <%llX>, errno = %d.|keyvalue テーブルの append ファイルを同期できません。|
|1855|Cannot close append file for Key-Value table <%llX>, errno = %d.|keyvalue テーブルの append ファイルを閉じられません。|
|1856|Cannot create data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのデータファイルを作成できません。|
|1857|Cannot open data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのデータファイルを開けません。|
|1858|Cannot read data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのデータファイルを読み取れません。|
|1859|Cannot write data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのデータファイルに書き込めません。|
|1860|Data file <%llX> is corrupted for Key-Value table <%llX>.|keyvalue テーブルのデータファイルが破損しています。|
|1861|Cannot create index file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのインデックスファイルを作成できません。|
|1862|Cannot open index file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのインデックスファイルを開けません。|
|1863|Cannot read <.%s> file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのファイルを読み取れません。|
|1864|Cannot write <.%s> file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue テーブルのファイルに書き込めません。|
|1865|Index file <%llX> is corrupted for Key-Value table <%llX>.|keyvalue テーブルのインデックスファイルが破損しています。|
|1866|Cannot perform I/O for Key-Value table <%llX>.|keyvalue テーブルの I/O 操作を実行できません。|
|1867|Invalid path to append file for Key-Value table <%llX>, errno = %d.|keyvalue テーブルの append ファイルのパスが無効です。|
|1868|Cannot open append file for Key-Value table <%llX>, errno = %d.|keyvalue テーブルの append ファイルを開けません。|
|1869|RID-based SELECT is not allowed without datafile, Table<%llX>/RID<%llu>.|データファイルがない場合、RID に基づく SELECT は使用できません。|
|1870|Cannot open append file for mounted Key-Value table <%llX>, errno = %d.|マウントした keyvalue テーブルの append ファイルを開けません。|
|1871|Cannot read append file for mounted Key-Value table <%llX>, errno = %d.|マウントした keyvalue テーブルの append ファイルを読み取れません。|
|1872|Another backup is in progress for table <%llX>.|このテーブルのバックアップが進行中です。|
|1873|No index-file <%llx> for Key-Value table Table<%llX>.|keyvalue テーブルのインデックスファイルがありません。|
|1874|Cannot open file <%llX> for Key-Value table <%llX> path<%s>, errno = %d.|keyvalue テーブルのファイルを開けませんでした。|
|1875|Cannot find unpurged node for Key-Value table <%llX>.|keyvalue テーブルの未パージのノードが見つかりません。|
|1876|Fail to %s decompress file <%llX> for key-value table<%llx>, error = %d|keyvalue テーブルのファイルの展開に失敗しました。|
|1877|Tag stat for id[%llu] is not found.|該当する ID のタグ統計がありません。|
|1878|Cannot write stat file for Key-Value table <%llX> path<%s> errno = %d.|keyvalue テーブルの stat ファイルに書き込めませんでした。|
|1879|Cannot read stat file for Key-Value table <%llX> path<%s> errno = %d.|keyvalue テーブルの stat ファイルを読み取れませんでした。|
|1880|Cannot open stat file for Key-Value table <%llX> path<%s>, errno = %d.|keyvalue テーブルの stat ファイルを開けませんでした。|
|1881|Stat File Invalid TableID[%llu], TablePath[%s].|stat ファイルが無効です。|
|1882|No kvindex-file <%llx> for Key-Value table Table<%llX>.|このテーブルの kvindex ファイルがありません。|
|1883|Value of the time column(<%lld>) must be greater than or equal to <%lld>.|時刻列の値が無効です。|
|1884|keyvalue table<%llx> thread for [%s] stopped.|keyvalue テーブルのスレッドが終了しました。|
|1885|Data row value is corrupted: required RID<%llu>, value RID<%llu>.|データ行の値が破損しています。|
|1886|%s varchar data is corrupted: required VRID<%u>, value VRID<%u>.|Varchar データが破損しています。|
|1900|Snapshot ID <%s> is invalid.|スナップショット ID が無効です。|
|1901|Cannot snapshot with no table.|存在しないテーブルではスナップショットを使用できません。|
|1902|Snapshot timed out.|スナップショットがタイムアウトしました。|
|1903|Snapshot ID <%s> does not exist.|スナップショット ID が存在しません。|
|1904|Snapshot ID <%s> already exists.|スナップショット ID が既に存在します。|
|1910|Cannot freeze with no table.|存在しないテーブルを凍結できません。|
|1911|Snapshot already frozen.|スナップショットは既に凍結されています。|
|1951|Failed to call function <%s>, errno=%d|関数の呼び出しに失敗しました。|
|1952|Table (0x%llx) resource busy (%s).|テーブルのリソースが使用中です。|
|2000|Memory allocation error, Error code = %d|メモリ割り当てエラーが発生しました。|
|2001|Error in opening meta.|メタデータを開く際にエラーが発生しました。|
|2002|Error in executing meta.|メタデータ処理の実行中にエラーが発生しました。|
|2003|Error in closing meta.|メタデータを閉じる際にエラーが発生しました。|
|2004|Error in creating hash. (errno=%d)|ハッシュの作成中にエラーが発生しました。|
|2005|Error in allocating memory.|メモリの割り当て中にエラーが発生しました。|
|2006|Error in adding hash. (errno=%d)|ハッシュへの追加中にエラーが発生しました。|
|2007|Error in fetching meta.|メタデータのフェッチ中にエラーが発生しました。|
|2008|Error in traversing hash.|ハッシュの検索中にエラーが発生しました。|
|2009|Insufficient parser memory.|パーサーのメモリが不足しています。|
|2010|Syntax error: near token (%s).|構文エラーが発生しました。|
|2011|Unrecognized token (%s).|認識できないトークンです。|
|2012|Single row error. Single-row subquery returns more than one row. (NOT USED)|単一行サブクエリが複数行を返しました。（未使用）|
|2013|A GROUP BY clause is required before HAVING.|HAVING 句の前に GROUP BY 句が必要です。|
|2014|Column name is duplicated: (%s).|列名が重複しています。|
|2015|Invalid column type: (%s).|列の型が無効です。|
|2016|Table property (%s) does not exist.|テーブルプロパティが存在しません。|
|2017|Error in converting table property. Cannot convert string (%s) to integer.|テーブルプロパティの文字列を整数に変換できません。|
|2018|Table property value is out of range: (%s).|テーブルプロパティの値が範囲外です。|
|2019|Column size should be specified on a variable column type.|可変長の列型には列サイズを指定する必要があります。|
|2020|Invalid size specified. Cannot specify type size to (%s).|サイズ指定が無効です。|
|2021|Cannot create bitmap index on data type (%s)|このデータ型にはビットマップインデックスを作成できません。|
|2022|Cannot create keyword index on data type (%s)|このデータ型にはキーワードインデックスを作成できません。|
|2023|snprintf function error (%d).|snprintf 関数のエラーが発生しました。|
|2024|Table %s already exists.|テーブルが既に存在します。|
|2025|Table %s does not exist.|テーブルが存在しません。|
|2026|The number of insert values and that of columns are mismatched.|入力値の数と列数が一致しません。|
|2027|Error in table insert column integer conversion. Insert value conversion to integer error (%s).|テーブルへの入力列の値を整数に変換できません。|
|2028|Error in table insert column double conversion. Insert value conversion to double error (%s)|テーブルへの入力列の値を double に変換できません。|
|2029|Error in table insert column time format. Insert _arrival_time value conversion error.|テーブルへの入力列の時刻形式が無効です。_arrival_time の変換中にエラーが発生しました。|
|2030|Column name (%s) does not exist.|列名が存在しません。|
|2031|Resource busy (%s).|リソースが使用中です。|
|2032|Type conversion error: error occurred while comparing the values of type (%s) and type (%s).|型の値を比較する際に型変換エラーが発生しました。|
|2033|Cannot concatenate non varchar types.|VARCHAR 以外の型は連結できません。|
|2034|Invalid format of time expression.|時刻式の形式が無効です。|
|2035|Function [%s] does not exist.|関数が存在しません。|
|2036|Function [%s] argument is mismatched.|関数の引数が一致しません。|
|2037|Function [%s] argument data type is mismatched.|関数の引数のデータ型が一致しません。|
|2038|Table [%s] does not exist.|テーブルが存在しません。|
|2039|No table specified in the target list.|対象リストに指定したテーブルがありません。|
|2040|Invalid time range.|時間範囲が無効です。|
|2041|Time value must be positive.|時刻値は正の値である必要があります。|
|2042|Expression cannot have a NULL value.|式に NULL 値を使用できません。|
|2043|Group function is not allowed here.|ここでは集計関数を使用できません。|
|2044|Not a GROUP BY expression.|GROUP BY の式ではありません。|
|2045|Type is not supported(typecode is %u). Internal error.|この型はサポートしていません。|
|2046|String buffer is not enough.|文字列バッファーが不足しています。|
|2047|Lock buffer is not enough. Table counts are too many.|テーブル数が多すぎるため、ロックバッファーが不足しています。|
|2048|Bind parameter count is overflowed. (max=%u)|バインドパラメーター数が上限を超えました。|
|2049|Cannot apply bind parameter.|バインドパラメーターを適用できません。|
|2050|Bind data from client is corrupted.|クライアントがバインドしたデータが破損しています。|
|2051|Bind data type unknown (typecode is %u).|不明なバインドデータ型です。|
|2052|Cannot insert data into this table (%s).|このテーブルにデータを挿入できません。|
|2053|Failed to convert type (%s) to type (%s).|型変換に失敗しました。|
|2054|Aggregation error on function usage (NOT USED)|関数の使用に関する集計エラーです。（未使用）|
|2055|Invalid insert value.|入力値が無効です。|
|2056|Column name (%s) not found.|列名が見つかりません。|
|2057|Only literal type can be used in SEARCH keyword.|SEARCH キーワードにはリテラル型のみ使用できます。|
|2058|Index %s already exists|インデックスが既に存在します。|
|2059|Index %s does not exist|インデックスが存在しません。|
|2060|Composite index is not supported.|複合インデックスはサポートしていません。|
|2061|Cannot divide a value by zero.|値を 0 で除算することはできません。|
|2062|Cannot calculate date type.|日付型の演算はできません。|
|2063|Invalid search type. Search type must be VARCHAR.|検索の型が無効です。VARCHAR である必要があります。|
|2064|Invalid time format. (format: \"year/mon/day hour:min:sec\")|時刻形式が無効です。形式は "year/mon/day hour:min:sec" です。|
|2065|Index property (%s) dose not exist.|インデックスプロパティが存在しません。|
|2066|Invalid index property value: (%s).|インデックスプロパティの値が無効です。|
|2067|Error in TO_ADDR4 function aggregate. Argument type to TO_ADDR4 function must be an integer.|TO_ADDR4 関数の処理でエラーが発生しました。引数の型は整数である必要があります。|
|2068|Invalid IPv4 address format (%s).|IPv4 アドレスの形式が無効です。|
|2069|%s index can only be created for %s table.|インデックスは特定のテーブルにのみ作成できます。|
|2070|Search predicate needs keyword index.|検索条件にはキーワードインデックスが必要です。|
|2071|Only one index is allowed for a single column.|1 つの列に作成できるインデックスは 1 個だけです。|
|2072|Cannot delete data from this table (%s).|このテーブルからデータを削除できません。|
|2073|Invalid DELETE condition. %s|DELETE 条件が無効です。|
|2074|Invalid delete time range. BEFORE time range should be older than present.|削除の時間範囲が無効です。BEFORE の時刻は現在時刻より前である必要があります。|
|2075|Table(%s) record does not exist in meta database.|テーブルのレコードがメタデータベースに存在しません。|
|2076|Table(%lld) record does not exist in meta database.|テーブルのレコードがメタデータベースに存在しません。|
|2077|Invalid %s size. %s type size cannot be more than %d.|サイズが無効です。|
|2078|Invalid statement type. Statement type(%d) is unsupported.|ステートメントの型が無効、またはサポート対象外です。|
|2079|The number of function (%s) arguments is not matched.|関数の引数の数が一致しません。|
|2080|User (%s) does not exist.|ユーザーが存在しません。|
|2081|Invalid username/password.|ユーザー名またはパスワードが無効です。|
|2082|User (%s) already exists.|ユーザーが既に存在します。|
|2083|You cannot drop yourself(%s).|ユーザーは自分自身を削除できません。|
|2084|User drop error. This user's tables still exist. Drop those tables first.|このユーザーのテーブルが残っているため、ユーザーを削除できません。先にテーブルを削除してください。|
|2085|The user(%s) does not have alter privileges.|ユーザーに変更権限がありません。|
|2086|The user(%s) does not have connect privileges.|ユーザーに接続権限がありません。|
|2087|The user does not have access privileges on table(%s.%s).|ユーザーにテーブルへのアクセス権限がありません。|
|2088|Error in altering table. Only the LOG table can be altered.|テーブルを変更できません。変更できるのは LOG テーブルだけです。|
|2089|Error in altering table. Column name(%s) already exists.|テーブルを変更できません。列名が既に存在します。|
|2090|Error in altering table. Only varchar type can be modified.|テーブルを変更できません。変更できるのは varchar 型だけです。|
|2091|Error in altering table. Varchar length should be greater than previous value length|テーブルを変更できません。varchar の長さは以前の値より大きい必要があります。|
|2092|Error in altering table. Column (%s) cannot be dropped.|テーブルを変更できません。この列は削除できません。|
|2093|Error in altering table. Column (%s) having index cannot be dropped.|テーブルを変更できません。インデックスがある列は削除できません。|
|2094|Error in altering table. Column (%s) already exists.|テーブルを変更できません。列が既に存在します。|
|2095|Error in truncating table. Only the LOG table can be truncated.|テーブルを TRUNCATE できません。対象にできるのは LOG テーブルだけです。|
|2096|Error in truncating table. Table %s does not exist.|テーブルを TRUNCATE できません。テーブルが存在しません。|
|2097|Error in altering table. The table must have at least one column.|テーブルを変更できません。少なくとも 1 つの列が必要です。|
|2098|Error in joining tables. Only equi-join is allowed.|テーブルを結合できません。等価結合のみ使用できます。|
|2099|Error in joining tables. The OR condition for a join predicate is not allowed.|テーブルを結合できません。結合条件に OR は使用できません。|
|2100|Error in joining tables. The join predicate cannot use functions.|テーブルを結合できません。結合条件に関数は使用できません。|
|2101|Error in joining tables. Cannot join without join predicate.|結合条件なしでテーブルを結合できません。|
|2102|Collector (%s.%s) does not exist.|Collector が存在しません。|
|2103|The collector (%s.%s) already exists.|Collector が既に存在します。|
|2104|The template file (%s) does not exist.|テンプレートファイルが存在しません。|
|2105|The template format (%s : %s : %d) is invalid.|テンプレートの形式が無効です。|
|2106|The collector (%s.%s) is already running.|Collector は既に実行中です。|
|2107|The collector (%s.%s) is not running.|Collector は実行中ではありません。|
|2108|Error in loading collector template. The value (%s) is invalid.|Collector テンプレートの読み込み中に、無効な値を検出しました。|
|2109|Cannot join two or more LOG tables.|2 つ以上の LOG テーブルを結合できません。|
|2110|Search condition argument is too short. It needs more than (%d) characters.|検索条件の引数が短すぎます。|
|2111|Invalid option.|オプションが無効です。|
|2112|Cannot use DISTINCT with GROUP BY clause.|DISTINCT と GROUP BY による集計は併用できません。|
|2113|Cannot use DISTINCT with aggregation function.|DISTINCT と集計関数は併用できません。|
|2114|DISTINCT clause is not allowed here.|ここでは DISTINCT 句を使用できません。|
|2115|Internal column cannot be modified.|内部列は変更できません。|
|2116|Search predicate must use an index.|検索条件はインデックスを使用する必要があります。|
|2117|DDL on table (%s) is forbidden.|このテーブルに対する DDL は禁止されています。|
|2118|Lock object was already initialized. (Do not use select and append simultaneously in single session.)|ロックオブジェクトは既に初期化されています。1 つのセッションで select と append を同時に使用しないでください。|
|2119|This functionality has not been implemented.|未実装の機能です。|
|2120|Invalid session ID (%s).|セッション ID が無効です。|
|2121|No privileges to kill the session.|セッションを終了する権限がありません。|
|2122|No privileges to cancel the session.|セッションをキャンセルする権限がありません。|
|2123|Table id (%lld) does not exist in meta database.|テーブル ID がメタデータベースに存在しません。|
|2124|Column id (%llu) does not exist in table (%llu).|列 ID がテーブルに存在しません。|
|2125|Error in converting string (%s) to datetime with heuristic method. Check the default date string format in this session.|文字列から日時への自動判定による変換でエラーが発生しました。セッションのデフォルト日時文字列形式を確認してください。|
|2126|ORDER BY clause is not allowed in a subquery|サブクエリでは ORDER BY 句を使用できません。|
|2127|Only integer constants must be used for ORDER BY column position.|ORDER BY の列位置には整数定数のみ指定できます。|
|2128|ORDER BY column position %d is out of range - should be between 1 and %d.|ORDER BY の列位置が範囲外です。|
|2129|GROUP BY terms must be integer constants|GROUP BY 句の項は整数定数である必要があります。|
|2130|A GROUP BY clause is required before HAVING|HAVING 句の前に GROUP BY 句が必要です。|
|2131|Single row error. Single-row subquery returns more than one row.|単一行サブクエリが複数行を返しました。|
|2132|Cannot use subquery on HAVING, ORDER BY and GROUP BY clauses.|HAVING、ORDER BY、GROUP BY 句ではサブクエリを使用できません。|
|2133|Invalid subquery.|サブクエリが無効です。|
|2134|Too many REGEXP in WHERE clause. No more than %d REGEXP in WHERE clause.|WHERE 句の REGEXP が多すぎます。設定された数を超えて使用できません。|
|2135|WHERE clause has to return a boolean result.|WHERE 句は真偽値を返す必要があります。|
|2136|Invalid tablespace type.|テーブルスペースの型が無効です。|
|2137|There are too many disks<%ud> for tablespace %s.|テーブルスペースのディスク数が多すぎます。|
|2138|The PARALLEL_IO value<%d> for the disk<%s> must be higher than <%d>.|ディスクの PARALLEL_IO を大きくする必要があります。|
|2139|MINMAX CACHE is not allowed for VARCHAR column(%s).|VARCHAR 列では MINMAX CACHE を使用できません。|
|2140|This type of tables do not support the tablespace functionality.|このテーブルタイプはテーブルスペース機能に対応していません。|
|2141|Type comparison error.|型の比較エラーが発生しました。|
|2142|Cannot use lob type in the GROUP BY clause.|GROUP BY 句では LOB 型を使用できません。|
|2143|Cannot use lob type in the ORDER BY clause.|ORDER BY 句では LOB 型を使用できません。|
|2144|Outerjoin permits only 2 tables.|外部結合では 2 つのテーブルだけを使用できます。|
|2145|The string cannot be converted to number value.(%s)|文字列を数値に変換できません。|
|2146|Cannot join tables with timeseries function.|時系列関数を使用する場合は、テーブルを結合できません。|
|2147|Cannot use inline view with timeseries function.|時系列関数とインラインビューは併用できません。|
|2148|Invalid IPv6 address format.(%s)|IPv6 アドレスの形式が無効です。|
|2149|Error in executing CONTAINS. Cannot convert from type(%d) to type(%d).|CONTAINS の実行中に型を変換できませんでした。|
|2150|Network type error. Network Mask length does not match with the column's length.(mask=%s, column=%s)|ネットワーク型が無効です。ネットワークマスクの長さが列の長さと一致しません。|
|2151|Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.|テーブルスペースにディスクを追加できません。有効なライセンスがない場合、複数のディスクを使用できません。|
|2152|Error in setting column property. You should specify a positive value of column property PARTITION_PAGE_COUNT as well as PAGE_VALUE_COUNT.|列プロパティを設定できません。PARTITION_PAGE_COUNT と PAGE_VALUE_COUNT には正の値を指定してください。|
|2153|Wrong column property name(%s). You should specify a valid property name.|列プロパティ名が無効です。有効な名前を指定してください。|
|2154|Select set operator parsing error.|SELECT の集合演算子の解析エラーが発生しました。|
|2155|Only UNION ALL set operator is supported.|集合演算子は UNION ALL のみサポートしています。|
|2156|Set operator column types are mismatched on (%d)th column.|集合演算子の列の型が一致しません。|
|2157|Internal error on validating query|クエリの検証中に内部エラーが発生しました。|
|2158|Error in evaluating data type. You must specify a valid data type.|データ型の評価中にエラーが発生しました。有効なデータ型を指定してください。|
|2159|FROM DATETIME' must be earlier than 'TO DATETIME'.|FROM DATETIME は TO DATETIME より前の時刻である必要があります。|
|2160|Error in doing unmount table(%s). You can unmount only mounted tables.|テーブルのマウントを解除できません。マウント済みのテーブルだけが対象です。|
|2161|Error in executing DDL. You cannot execute DDL with mounted DB. (*NOT USED*)|マウントしたデータベースでは DDL を実行できません。（未使用）|
|2162|Error in doing unmount DB. You cannot umount database which is not mounted.|データベースのマウントを解除できません。マウントされていません。|
|2163|Invalid directory path (%s). You should specify a valid path.|ディレクトリパスが無効です。パスを指定してください。|
|2164|Invalid index property. Property (%s) for index cannot be altered.|インデックスプロパティが無効です。指定したプロパティは変更できません。|
|2165|Function (%s) is not allowed here.|ここではこの関数を使用できません。|
|2166|Cannot use ORDER BY clause with aggregation function.|集計関数と ORDER BY 句は併用できません。|
|2167|GROUP_CONCAT function error. Separator should be a string constant.|GROUP_CONCAT の区切り文字は文字列定数である必要があります。|
|2168|Operator argument count or type is mismatched.|演算子の引数の数または型が一致しません。|
|2169|Invalid column property value: (%s)|列属性の値が無効です。|
|2170|Every specified table or inline view in FROM clause must have its own alias.|FROM 句に指定した各テーブルまたはインラインビューには、一意の別名が必要です。|
|2171|VOLATILE / LOOKUP table cannot have more than one primary key.|VOLATILE/LOOKUP テーブルに複数の主キーを定義できません。|
|2172|Primary key is allowed only for VOLATILE / LOOKUP table.|主キーは VOLATILE/LOOKUP テーブルでのみ使用できます。|
|2173|Cannot create columns with data type (%s) in VOLATILE / LOOKUP table.|VOLATILE/LOOKUP テーブルでは、このデータ型の列を作成できません。|
|2174|The index already exists in the column(%s).|列にインデックスが既に存在します。|
|2175|SET clause must be written as a list of 'column = value' expression.|SET 句は「列 = 値」の式のリストで記述する必要があります。|
|2176|Cannot update primary key column in SET clause.|SET 句で主キー列を更新できません。|
|2177|ON DUPLICATE UPDATE clause is allowed only in LOOKUP / VOLATILE table.|ON DUPLICATE UPDATE 句は LOOKUP/VOLATILE テーブルでのみ使用できます。|
|2178|Error in updating table. Column name (%s) does not exist in this table.|テーブルを更新できません。このテーブルに列名が存在しません。|
|2179|INSERT on a %s table without primary key value cannot be proceeded.|主キー値なしでテーブルに挿入できません。|
|2180|Primary key is mandatory for UPDATE.|UPDATE には主キーが必要です。|
|2181|Invalid index name starting with (%s) which is the same as primary key index.|インデックス名が無効です。プライマリインデックスと同じ接頭辞で始まっています。|
|2182|You cannot drop the primary key index (%s).|プライマリキーインデックスは削除できません。|
|2183|Append mode for table (%s) is not supported.|このテーブルは APPEND モードに対応していません。|
|2184|Specified property value is invalid in %s table.|テーブルに指定したプロパティ値が無効です。|
|2185|Invalid database name. This database name is already used for mount.|データベース名が無効です。この名前は既にマウントに使用されています。|
|2186|Invalid database name.|データベース名が無効です。|
|2187|Error in unmounting database. Some tables in mounted database are accessed by other transactions|他のトランザクションが、マウント済みデータベース内のテーブルを参照しているため、マウントを解除できません。|
|2188|The database is not mounted.|データベースはマウントされていません。|
|2189|Error in deleting rows. Only rows in VOLATILE / LOOKUP table can be deleted.|行を削除できません。削除できるのは VOLATILE/LOOKUP テーブルの行だけです。|
|2190|Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)|UPDATE/DELETE 条件が無効です。「主キー列 = 値」で指定してください。|
|2191|WHERE clause in DELETE statement is not supported yet.|DELETE 文の WHERE 句はまだサポートしていません。|
|2192|Index type for keyword index only supports keyword bitmap or keyword LSM.|キーワードインデックスのタイプは、キーワードビットマップまたはキーワード LSM のみサポートしています。|
|2193|Error in creating collector. The regular expression file (%s) does not exist.|Collector を作成できません。正規表現ファイルが存在しません。|
|2194|Error in creating collector. The regular expression file path has not specified.|Collector を作成できません。正規表現ファイルのパスが未指定です。|
|2195|Buffer size insufficient.|バッファーサイズが不足しています。|
|2196|Error in loading data. File (%s) does not exist.|データをロードできません。ファイルが存在しません。|
|2197|Error in loading data with automatic mode. The table (%s) already exists.|自動モードでデータをロードできません。テーブルが既に存在します。|
|2198|Error in loading data. The table (%s) doesn't exists.|データをロードできません。テーブルが存在しません。|
|2199|CSV parsing error occurred in %d line: [%s]|CSV の解析中にエラーが発生しました。|
|2200|[%s] is not valid string terminator or encloser.|文字列の終端文字または囲み文字が無効です。|
|2201|The automatic loading mode is invalid.|自動ロードモードが無効です。|
|2202|The automatic column detection has been failed. No data or invalid headers.|列の自動検出に失敗しました。データがないか、ヘッダーが無効です。|
|2203|Invalid encoding.|エンコーディングが無効です。|
|2204|Failed to convert %s to UTF8.|UTF8 への変換に失敗しました。|
|2205|A modulo operator can be applied only for integer types.|剰余演算子は整数型にのみ適用できます。|
|2206|Tablespace name cannot be specified in non automode|非自動モードではテーブルスペース名を指定できません。|
|2207|Error in saving table into file (%s). File already exists.|テーブルをファイルに保存できません。ファイルが既に存在します。|
|2208|Expression argument type is mismatched.|式の引数の型が一致しません。|
|2209|Error in connecting to collector manager. The collector manager (%s:%d) doesn't exists.|Collector Manager に接続できません。Collector Manager が存在しません。|
|2210|Error in executing CREATE command. The collector manager (%s) returns error.|CREATE コマンドの実行中に Collector Manager がエラーを返しました。|
|2211|Error in executing DROP command. The collector manager (%s) returns error.|DROP コマンドの実行中に Collector Manager がエラーを返しました。|
|2212|Error in running collector manager. The collector manager (%s) is already running.|Collector Manager を実行できません。既に実行中です。|
|2213|Error in stopping collector manager. The collector manager (%s) is not running.|Collector Manager を停止できません。実行中ではありません。|
|2214|Error in starting collector manager. The collector manager (%s) is already started.|Collector Manager を起動できません。既に実行中です。|
|2215|Error in starting command execution. The collector manager (%s) returns error.|コマンドの実行開始時に Collector Manager がエラーを返しました。|
|2216|Error in executing collector CREATE command. The collector (%s.%s) returns error.|Collector 作成コマンドの実行中に Collector がエラーを返しました。|
|2217|Error in receiving meta data from collector manager (%s-%s:%d).|Collector Manager からのメタデータ受信中にエラーが発生しました。|
|2218|Collector manager (%s) does not exist.|Collector Manager がありません。|
|2219|Error in creating collector manager. The collector manager (%s) already exists.|Collector Manager を作成できません。既に存在します。|
|2220|Error in executing command. The collector manager (%s) returns error.|コマンドの実行中に Collector Manager がエラーを返しました。|
|2221|Manager name is not specified.|Manager 名が指定されていません。|
|2222|Error in read protocol. Send %s protocol, but received %d protocol.|プロトコルの読み取りエラーが発生しました。|
|2223|Unable to establish connection with collectormanager (%s).|Collector Manager に接続できません。|
|2224|Manager name is not specified.|Manager 名が指定されていません。|
|2225|Invalid set column unit.|列単位の設定が無効です。|
|2226|Invalid character ('%c').|文字が無効です。|
|2227|The collector source (%s.%s) already exists.|Collector のソースが既に存在します。|
|2228|Invalid procedure (%s).|プロシージャーが無効です。|
|2229|Invalid argument value for function (%s).|関数の引数の値が無効です。|
|2230|Wrong number of arguments in call to '%s'.|関数の呼び出し時の引数の数が無効です。|
|2231|strcpy function error (%d).|strcpy 関数のエラーが発生しました。|
|2232|Calculation argument type (%s), (%s) error.|演算の引数の型が無効です。|
|2233|Error occurred at column (%u): (%s)|列でエラーが発生しました。|
|2234|Set operator columns counts are mismatched by %d and %d.|集合演算子の左右で列数が一致しません。|
|2235|SERIES BY clause is not allowed here.|ここでは SERIES BY 句を使用できません。|
|2236|For a table list in FROM clause, The number of tables should be less than 32.|FROM 句のテーブル数は 32 未満である必要があります。|
|2237|The index <%s> is not an index for the table <%s>.|このインデックスは対象テーブルのインデックスではありません。|
|2238|This type of join is not allowed.|このタイプの結合は使用できません。|
|2239|Invalid use of aggregation function.|集計関数の使用方法が無効です。|
|2240|Cannot fetch column with type (%s).|この型の列はフェッチできません。|
|2241|Join between LOG table and fixed table is not supported in Cluster Edition.|Cluster Edition では、LOG テーブルと固定テーブルの結合はサポートしていません。|
|2242|Only equal predicate for joining LOG tables is available in Cluster Edition.|Cluster Edition の LOG テーブルの結合では、等価述語のみ使用できます。|
|2243|DELETE statement with the number of rows is not supported in Cluster Edition.|Cluster Edition では、行数を指定する DELETE 文はサポートしていません。|
|2244|Allocate collector columns meta failure.|Collector の列メタデータの割り当てに失敗しました。|
|2245|Allocate collector column target failure.|Collector の列ターゲットの割り当てに失敗しました。|
|2246|Identifier %.*s is too long.|識別子が長すぎます。|
|2247|DATETIME earlier than 1970-01-01 00:00:00 (UTC) is not valid.|1970-01-01 00:00:00（UTC）より前の DATETIME は無効です。|
|2248|Insufficient column definitions.|列定義が不足しています。|
|2249|Invalid DELETE condition.|DELETE 条件が無効です。|
|2250|You cannot execute DDL on compoment table/index of TAGDATA table explictly.|TAGDATA テーブルの構成テーブル・インデックスに対して DDL を明示的に実行できません。|
|2251|You cannot define columns with duplicate flag (%s) in TAGDATA table.|TAGDATA テーブルに、同じフラグを持つ列を重複して定義できません。|
|2252|Invalid column type (%s) for flag (%s) in TAGDATA table.|TAGDATA テーブルのフラグに対する列の型が無効です。|
|2253|Mandatory column definition (PRIMARY KEY / BASETIME) is missing.|必須列（PRIMARY KEY/BASETIME）の定義がありません。|
|2254|Column flag (%s) is only allowed for TAG table.|列フラグは TAG テーブルでのみ使用できます。|
|2255|Primary key of TAGDATA table is not defined in metadata.|TAGDATA テーブルの主キーがメタデータに定義されていません。|
|2256|Metadata column definition is allowed only in TAGDATA table.|メタデータ列の定義は TAGDATA テーブルでのみ使用できます。|
|2257|Metadata insertion is allowed only in TAGDATA table.|メタデータの挿入は TAGDATA テーブルでのみ使用できます。|
|2258|Metadata key (%.*s) for the TAG table has already been inserted.|TAG テーブルのメタデータキーは既に挿入されています。|
|2259|Metadata of TAGDATA table is not found. (Key = %s)|TAGDATA テーブルのメタデータが見つかりません。|
|2260|Failed to allocate new metadata of TAGDATA table (Current Size=%llu).|TAGDATA テーブルの新しいメタデータを割り当てられませんでした。|
|2261|You cannot insert metadata into TAGDATA table with ON DUPLICATE KEY UPDATE clause.|ON DUPLICATE KEY UPDATE 句を使用して TAGDATA テーブルにメタデータを挿入できません。|
|2262|Direct DML on component tables of TAGDATA table is not allowed.|TAGDATA テーブルの構成テーブルへの直接の DML は使用できません。|
|2263|You can create only one TAGDATA table.|TAGDATA テーブルは 1 個だけ作成できます。|
|2264|Cannot read a column (%s) in ROLLUP query because it is not a ROLLUP column.|ROLLUP クエリでこの列を読み取れません。ROLLUP 列ではありません。|
|2265|Reading TAGDATA table without primary key condition is not allowed.|主キー条件なしで TAGDATA テーブルを読み取ることはできません。|
|2266|You cannot delete raw data of TAGDATA table with WHERE condition.|WHERE 条件を使用して TAGDATA テーブルの生データを削除できません。|
|2267|Primary key in TAGDATA table should be compared by '=' or 'IN' operation.|TAGDATA テーブルの主キーは、= または IN 演算子で比較する必要があります。|
|2268|Primary key in TAGDATA table should be compared with constant value.|TAGDATA テーブルの主キーは定数値と比較する必要があります。|
|2269|Outerjoin on TAGDATA table is not allowed.|TAGDATA テーブルでは外部結合を使用できません。|
|2270|TAGDATA table's name should be 'TAG'.|TAGDATA テーブルの名前は TAG である必要があります。|
|2271|You must insert key value of TAGDATA table as constant.|TAGDATA テーブルのキー値は定数で挿入する必要があります。|
|2272|Index id (%llu) does not exist in meta database.|インデックス ID（%llu）がメタデータベースに存在しません。|
|2273|The user does not have privileges on TAGDATA DDL.|ユーザーに TAGDATA の DDL を実行する権限がありません。|
|2274|Failed to free new metadata of TAGDATA table.|TAGDATA テーブルの新しいメタデータを解放できませんでした。|
|2275|The INSERT SELECT statement to the TAGDATA table is not allowed in enterprise edition.|Enterprise Edition では TAGDATA テーブルへの INSERT SELECT 文は使用できません。|
|2276|Component table (%s) of TAGDATA table already exists.|TAGDATA テーブルの構成テーブルが既に存在します。|
|2277|Table or index name that starts with '_TAG' is reserved.|_TAG で始まるテーブル名・インデックス名は予約されています。|
|2278|UPDATE statement is not allowed for %s.|UPDATE 文は使用できません。|
|2279|Invalid tag name insertion to TAGDATA table (name = '%s').|TAGDATA テーブルに挿入しようとしたタグ名が無効です。|
|2280|Invalid tag name insertion due to wrong bind variable.|バインド変数が不正なため、挿入するタグ名が無効です。|
|2281|DURATION clause is not applicable on %s.|DURATION 句を適用できません。|
|2282|The DELETE statement for table '%s' is already been executed.|このテーブルに対する DELETE 文が既に実行中です。|
|2283|IN subquery on TAGDATA table is not allowed.|TAGDATA テーブルでは IN サブクエリを使用できません。|
|2284|Internal NULL value exists in the condition expression.|条件式に内部 NULL 値が存在します。|
|2285|Internal error: %s.|内部エラーが発生しました。|
|2286|Memory allocation failed while creating TAGDATA table. You may need to decrease TAG_DATA_PART_SIZE in machbase.conf.|TAGDATA テーブルの作成中にメモリを割り当てられませんでした。machbase.conf の TAG_DATA_PART_SIZE を小さくする必要がある場合があります。|
|2287|TAGDATA name value (%s) is too long.|TAGDATA のタグ名の値が長すぎます。|
|2288|Aggregate function is expected at (%.*s).|集計関数が必要です。|
|2289|Non-constant expression is not allowed for PIVOT values.|PIVOT 値に非定数の式は使用できません。|
|2290|%s cannot be altered.|変更できません。|
|2291|Table name 'TAG' must be used for TAGDATA table.|テーブル名 TAG は TAGDATA テーブル専用です。|
|2292|The order of columns in TAGDATA table must be (PRIMARY, BASETIME, SUMMARIZED, other columns, .. ).|TAGDATA テーブルの列順は PRIMARY、BASETIME、SUMMARIZED、その他の列である必要があります。|
|2293|Column meta for bind param[%d] is not available.|バインドパラメーターに対応する列メタデータを取得できません。|
|2294|JOIN more than one TAGDATA table is not supported.|複数の TAG テーブルの結合はサポートしていません。|
|2295|Invalid ordinal number ID_COLUMN (%lld) and TIME_COLUMN (%lld).|ID_COLUMN、TIME_COLUMN の序数が無効です。|
|2296|Interpolation requires only one BETWEEN expression.|補間クエリには BETWEEN 式が 1 つだけ必要です。|
|2297|BETWEEN has invalid expression (%s).|BETWEEN 式が無効です。|
|2298|FREQUENCE must be a factor of INTERPOLATION_INTERVAL (%lld).|FREQUENCE は INTERPOLATION_INTERVAL の約数である必要があります。|
|2299|Only BETWEEN condition is supported.|BETWEEN 条件のみサポートしています。|
|2300|Interpolation column is missing. (%s)|補間列がありません。|
|2301|Some properties are missing for interpolation.|補間に必要なプロパティの一部がありません。|
|2302|Invalid interpolation interval property: %lld.|補間間隔のプロパティが無効です。|
|2303|You must use higher ROLLUP unit.|より大きい ROLLUP 単位を使用してください。|
|2304|Interpolation is not applicable on (%s).|補間を適用できません。|
|2305|JOIN is not applicable for interpolation.|補間には JOIN を適用できません。|
|2306|Interpolation interval value(%lld) should be less than checkpoint interval value(%lld).|補間間隔はチェックポイント間隔より小さい必要があります。|
|2307|Interpolation interval value(%lld) should be less than ROLLUP unit (%s).|補間間隔は ROLLUP 単位より小さい必要があります。|
|2308|Checkpoint interval value(%lld) should be less than ROLLUP unit (%s).|チェックポイント間隔は ROLLUP 単位より小さい必要があります。|
|2309|Checkpoint interval value(%lld) should be divide by interpolation value(%lld).|チェックポイント間隔は補間間隔で割り切れる必要があります。|
|2310|Invalid interpolation checkpoint property: %lld.|補間チェックポイントのプロパティが無効です。|
|2311|%s cannot be used in interpolation query.|補間クエリでは使用できません。|
|2312|Rollup delete can only be done on the Interpolation Tag table.|ROLLUP データの削除は補間 TAG テーブルでのみ実行できます。|
|2313|Unable to execute ROLLUP DELETE with the given range.|指定範囲で ROLLUP DELETE を実行できません。|
|2314|Regular duration backup does not support a backup of the TAG table (Try incremental backup which permits the action on the TAG table).|期間指定バックアップは TAG テーブルに対応していません。TAG テーブルに対応する増分バックアップを試してください。|
|2315|Snapshot is not supported.|スナップショットはサポートしていません。|
|2316|Invalid expression in DURATION clause: %.*s|DURATION 句の式が無効です。|
|2317|Function execution failed: %s (errno=%d)|関数の実行に失敗しました。|
|2318|Can not connect Lookup Node|Lookup ノードに接続できません。|
|2319|Error on Lookup Node|Lookup ノードでエラーが発生しました。|
|2320|Lookup Node is not ready|Lookup ノードの準備ができていません。|
|2321|Data is not found in Lookup Node.|Lookup ノードでデータが見つかりません。|
|2322|Mandatory column definition (PRIMARY KEY) is missing.|必須列（PRIMARY KEY）の定義がありません。|
|2323|Table REFRESH is not applicable on %s.|テーブルのリフレッシュを適用できません。|
|2324|Cannot delete tagmeta. there exist data with deleted_tag key.|削除対象のタグキーを持つデータが存在するため、タグメタデータを削除できません。|
|2325|Integer %s type overflow.|整数型のオーバーフローが発生しました。|
|2326|Backup/Mount is not supported.|バックアップ・マウントはサポートしていません。|
|2327|Pivot is not supported in rollup query.|ROLLUP クエリでは PIVOT をサポートしていません。|
|2328|Cannot insert a new tag since the number of tags has exceeded MAX_TAG_COUNT(%lld).|タグ数が MAX_TAG_COUNT を超えているため、新しいタグを挿入できません。|
|2329|Cannot insert a new tag since the number of tags has exceeded TAG_COUNT_LIMIT(%lld).|タグ数が TAG_COUNT_LIMIT を超えているため、新しいタグを挿入できません。|
|2330|Mandatory column definition (ULONG / DATETIME) is missing.|必須列（ULONG/DATETIME）の定義がありません。|
|2331|RANGE expression is not applicable on the table (%s).|このテーブルに RANGE 式を適用できません。|
|2332|Unable to create an index on the column (%s).|この列にはインデックスを作成できません。|
|2333|This column(%s) can't be more than %d.|この列は %d 個を超えて作成できません。|
|2334|Tag Index is not yet supported.|タグインデックスはまだサポートしていません。|
|2335|Failed to delete all on this table. It is recommended to use EXEC TABLE_REFRESH(%s).|テーブルの全データを削除できませんでした。EXEC TABLE_REFRESH の使用を推奨します。|
|2336|CASCADE option is not applicable on %s.|CASCADE オプションを適用できません。|
|2337|Unable to define more than one column attribute (%s).|複数の列属性を定義することはできません。|
|2339|The type of %s column (%s) is different from that of VALUE column (%s).|列の型が VALUE 列の型と異なります。|
|2340|SUMMARIZED column does not exist for %s.|SUMMARIZED 列がありません。|
|2341|SUMMARIZED value is greater than UPPER LIMIT.|SUMMARIZED 値が UPPER LIMIT を超えています。|
|2342|SUMMARIZED value is less than LOWER LIMIT.|SUMMARIZED 値が LOWER LIMIT 未満です。|
|2343|LOWER LIMIT must not be greater than UPPER LIMIT.|LOWER LIMIT は UPPER LIMIT を超えることはできません。|
|2344|Not numeric type. (%s)|数値型ではありません。|
|2345|Column flag (%s) is only allowed for TAGMETA table.|列フラグは TAGMETA テーブルでのみ使用できます。|
|2346|Column type (%s) is not allowed for default value.|この列の型はデフォルト値として使用できません。|
|2347|SYSDATE is only allowed for default value.|SYSDATE はデフォルト値としてのみ使用できます。|
|2348|Alter table set %s not support on cluster.|クラスタでは、指定したプロパティの ALTER TABLE SET はサポートしていません。|
|2349|Bind variable is not supported for new tag.|新しいタグにバインド変数は使用できません。|
|2350|The function (%s) requires OVER clause.|この関数には OVER 句が必要です。|
|2351|Window function is allowed only in SELECT list.|ウィンドウ関数は SELECT リストでのみ使用できます。|
|2352|OVER clause is not applicable on (%s).|OVER 句を適用できません。|
|2353|Invalid data type (%s) in OVER clause.|OVER 句の型が無効です。|
|2354|Constant is not allowed in OVER clause.|OVER 句では定数を使用できません。|
|2355|Type (%s) is not supported.|サポートしていない型です。|
|2356|Origin must be the first day of the month.|Origin は対象月の 1 日である必要があります。|
|2600|SEQUENCE property is not applicable in the table.|このテーブルには SEQUENCE 属性を適用できません。|
|2601|Invalid function in a SEQUENCE column. NEXTVAL must be used.|SEQUENCE 列の関数が無効です。NEXTVAL を使用してください。|
|2602|NEXTVAL is applicable only in INSERT statement.|NEXTVAL は INSERT 文でのみ使用できます。|
|2603|NEXTVAL is applicable only in SEQUENCE columns.|NEXTVAL は SEQUENCE 列にのみ適用できます。|
|2604|Sequence column must be LONG type.|SEQUENCE 列は LONG 型である必要があります。|
|2651|Dependent ROLLUP table exists.|依存する ROLLUP テーブルがあります。|
|2652|Not a ROLLUP table. (%s)|ROLLUP テーブルではありません。|
|2653|Rollup interval must be greater than source rollup interval.|ROLLUP 間隔はソースの ROLLUP 間隔より大きい必要があります。|
|2654|ROLLUP (%s) is not found.|ROLLUP が見つかりません。|
|2655|Rollup interval source rollup interval Must Divide Zero.|ROLLUP 間隔はソースの ROLLUP 間隔で割り切れる必要があります。|
|2656|Rollup interval must positive integer.|ROLLUP 間隔は正の整数である必要があります。|
|2657|Rollup interval must be smaller than year.|ROLLUP 間隔は 1 年未満である必要があります。|
|2658|ROLLUP is not enabled for %s.|ROLLUP が有効になっていません。|
|2659|Rollup maximum count is 100.|ROLLUP の最大数は 100 です。|
|2670|Rollup user ID(%d) is not equal to Source user ID(%d)|ROLLUP のユーザー ID とソースのユーザー ID が一致しません。|
|2671|Invalid type for ROLLUP column (%s).|ROLLUP 列の型が無効です。|
|2672|Json path is not specified on %s.|JSON パスが指定されていません。|
|2673|Json path is not applicable on %s.|JSON パスを適用できません。|
|2674|ROLLUP query must have a target column.|ROLLUP クエリには対象列が必要です。|
|2675|Cannot use more than one ROLLUP column in a ROLLUP query.|ROLLUP クエリで複数の ROLLUP 列は使用できません。|
|2676|Not a TAG table.|TAG テーブルではありません。|
|2677|Invalid rollup time unit (%s).|ROLLUP の時間単位が無効です。|
|2678|WITH ROLLUP requires a SUMMARIZED column.|WITH ROLLUP には SUMMARIZED 列が必要です。|
|2679|Failed to create ROLLUP by WITH ROLLUP option.|WITH ROLLUP オプションによる ROLLUP の作成に失敗しました。|
|2680|ROLLUP (%s) is already started.|ROLLUP は既に開始されています。|
|2681|ROLLUP (%s) is already stopped.|ROLLUP は既に停止しています。|
|2682|ROLLUP extension type is different.|ROLLUP の拡張種別が異なります。|
|2683|Cannot read a column (%s) in ROLLUP query because it is not a ROLLUP time column.|ROLLUP クエリでこの列を読み取れません。ROLLUP の時刻列ではありません。|
|2684|Dependent ROLLUP table does not exist.|依存する ROLLUP テーブルがありません。|
|2685|There are no applicable ROLLUP tables.|適用できる ROLLUP テーブルがありません。|
|2700|Policy (%s) already exists.|ポリシーが既に存在します。|
|2701|Policy (%s) does not exists.|ポリシーが存在しません。|
|2702|Policy (%s) is in use.|ポリシーが使用中です。|
|2703|Table (%s) has no retention policy.|テーブルに保持ポリシーがありません。|
|2704|Table (%s) already has a retention policy.|テーブルには既に保持ポリシーがあります。|
|2705|Retention duration must be longer than 1 day.|保持期間の指定値が無効です。1 以上の値を指定してください。サーバーメッセージの「1 day」は旧仕様の表記です。|
|2706|Retention interval must be longer than 1 hour.|保持処理の実行間隔が無効です。1 以上の値を指定してください。サーバーメッセージの「1 hour」は旧仕様の表記です。|
|2707|Retention is not applicable on the table (%s).|このテーブルに保持ポリシーを適用できません。|
|2708|Only SYS user can create or drop RETENTION.|RETENTION を作成・削除できるのは SYS ユーザーだけです。|
|2800|The stream query is too long. (max=2048)|ストリームクエリが長すぎます。|
|2801|The stream query is not applicable.|ストリームクエリを適用できません。|
|2802|Cannot get table information.|テーブル情報を取得できません。|
|2803|Specified stream query statement has no LOG table.|指定したストリームクエリに LOG テーブルがありません。|
|2804|Specified stream query statement has more than 1 LOG tables.|指定したストリームクエリに複数の LOG テーブルがあります。|
|2805|The stream query (%s) is not found.|ストリームクエリが見つかりません。|
|2806|The stream query (%s) already exists.|ストリームクエリが既に存在します。|
|2807|The stream query (%s) is already started.|ストリームクエリは既に開始されています。|
|2808|The stream query (%s) is already stopped.|ストリームクエリは既に停止しています。|
|2809|The stream query (%s) is still running.|ストリームクエリが実行中です。|
|2810|Cannot execute the stream query (%s).|ストリームクエリを実行できません。|
|2811|The stream query (%s) is executed automatically by the system.|システムがストリームクエリを自動実行します。|
|2812|The Frequency clause is not allowed here.|ここでは Frequency 句を使用できません。|
|2813|Invalid ROLLUP expression. (Token = %s, Unit = %ld)|ROLLUP 式が無効です。|
|2814|Invalid ROLLUP target. BASETIME column of TAGDATA table is the only target.|ROLLUP の対象が無効です。TAG テーブルの BASETIME 列のみ指定できます。|
|2815|Different ROLLUP expressions are used in a single SELECT query.|1 つの SELECT クエリに異なる ROLLUP 式が使用されています。|
|2816|Only rollup column with aggregate function can be referenced in ROLLUP SELECT query.|ROLLUP SELECT クエリでは、集計関数を使用する ROLLUP 列だけを参照できます。|
|2817|ROLLUP expression must be used in SELECT query.|SELECT クエリには ROLLUP 式を指定する必要があります。|
|2818|Invalid ROLLUP target (%s).|ROLLUP の対象が無効です。|
|2819|ROLLUP thread is running.|ROLLUP スレッドが稼働中です。|
|2820|ROLLUP thread is not running.|ROLLUP スレッドは稼働していません。|
|2821|Another DDL/DELETE/SNAPSHOT is in progress.|DDL/DELETE/SNAPSHOT が実行中です。|
|2822|Invalid expression in ROLLUP query : %.*s|ROLLUP クエリの式が無効です。|
|2823|Invalid table in ROLLUP query: %s|ROLLUP クエリのテーブルが無効です。|
|2825|Extended column(%s) cannot be used in ROLLUP query.|拡張列は ROLLUP クエリで使用できません。|
|2826|User (%s) can't revoke from table (%s.%s).|ユーザーはテーブルに対する権限を取り消せません。|
|2827|User does not have grant privileges.|ユーザーに権限を付与する権限がありません。|
|2828|User does not have revoke privileges.|ユーザーに権限を取り消す権限がありません。|
|2829|Only SYS user can create or drop user.|ユーザーを作成・削除できるのは SYS ユーザーだけです。|
|2830|The user does not have (%s) privilege on table(%s.%s).|ユーザーにテーブルに対する権限がありません。|
|2831|You can't grant UPDATE privilege on Log Table.|LOG テーブルには UPDATE 権限を付与できません。|
|2832|You can't revoke UPDATE privilege on Log Table.|LOG テーブルの UPDATE 権限は取り消せません。|
|2833|You can only grant SELECT privileges on Mounted database.|マウントしたデータベースには SELECT 権限だけを付与できます。|
|3000|Statement ID overflow (Limit = %u, Curr = %u).|ステートメント ID の上限を超えました。|
|3001|Statement query length is zero.|ステートメントのクエリ長が 0 です。|
|3002|Task pool initialization error.|タスクプールの初期化エラーが発生しました。|
|3003|Statement pool initialization error.|ステートメントプールの初期化エラーが発生しました。|
|3004|Queue creation error.|キューの作成エラーが発生しました。|
|3005|Statement allocation error.|ステートメントの割り当てエラーが発生しました。|
|3006|Unknown meta type error (typecode is %u). Internal error.|不明なメタデータ型です。（内部エラー）|
|3007|Insufficient protocol buffer size. Increase it.|プロトコルバッファーのサイズが不足しています。サイズを増やしてください。|
|3008|Invalid protocol state. Check your application again. (Protocol = %s, State = %s)|プロトコルの状態が無効です。アプリケーションを確認してください。|
|3009|Invalid execute protocol data (%s).|実行プロトコルのデータが無効です。|
|3010|Error in fetch protocol: not enough buffer size to execute it. Increase the size.|バッファー不足によるフェッチプロトコルのエラーです。バッファーサイズを増やしてください。|
|3011|Send error.|送信エラーが発生しました。|
|3012|Memory allocation error.|メモリの割り当てエラーが発生しました。|
|3013|Invalid table name for append table. Table name is omitted.|APPEND 先のテーブル名が指定されていません。|
|3014|Invalid append protocol data (%s).|APPEND プロトコルのデータが無効です。|
|3015|Endian is not specified for append. Check endian information.|入力のエンディアンが未指定です。エンディアン情報を確認してください。|
|3016|Too many columns are specified for append. Cannot append more than %d columns|入力に指定した列数が多すぎます。|
|3017|Too large record size for append. Cannot append more than %d bytes per record.|入力レコードのサイズが大きすぎます。|
|3018|It exceeds the specified max. block size (%d). Check append data structure of your applcation.|指定した最大ブロックサイズを超えました。アプリケーションの APPEND データ構造を確認してください。|
|3019|Explain plan error. Use it for SELECT statement only.|実行計画を表示できません。実行計画は SELECT 文でのみ使用できます。|
|3020|Explain plan is not allowed in prepared mode.|Prepared モードでは実行計画を表示できません。|
|3021|Protocol versions are not matched: Server (%d.%d.%d) Client (%d.%d.%d)|サーバーとクライアントのプロトコルバージョンが一致しません。|
|3022|Failed to get handle limit from the system.|システムのハンドル上限を取得できませんでした。|
|3023|Handle limit(%d) from the system is less than that of property(%d). Tune system handle limit or decrease the property 'HANDLE_LIMIT'|システムのハンドル上限がプロパティ値未満です。システム側の上限を調整するか、HANDLE_LIMIT を小さくしてください。|
|3024|Invalid session ID (%llu).|セッション ID が無効です。|
|3025|Not enough privileges to manipulate the session. (%llu)|セッションを操作する権限が不足しています。|
|3026|You should log in with the same user name in the target session. Now (%d) Target(%d)|操作対象のセッションと同じユーザー名でログインする必要があります。|
|3027|This statement has been canceled.|ステートメントがキャンセルされました。|
|3028|Invalid session property name. Name (%s) does not exist.|セッションプロパティ名が無効です。その名前は存在しません。|
|3029|Error in converting session property (%s). Cannot convert string (%s) to integer.|セッションプロパティの変換でエラーが発生しました。文字列を整数に変換できません。|
|3030|Invalid session property value. Check the session value (%s)|セッションプロパティの値が無効です。設定値を確認してください。|
|3031|Protocol error.|プロトコルエラーが発生しました。|
|3032|Error in getting license meta. Check DB image and binary.|ライセンスメタデータの取得でエラーが発生しました。DB イメージとバイナリーファイルを確認してください。|
|3033|Error in opening meta.|メタデータを開く際にエラーが発生しました。|
|3034|Error in executing meta.|メタデータ処理中にエラーが発生しました。|
|3035|Error in closing meta.|メタデータを閉じる際にエラーが発生しました。|
|3036|The license is expired(%s).|ライセンスが期限切れです。|
|3037|The license is invalid or the license file does not exist(%s).|ライセンスファイルが存在しないか無効です。|
|3038|License violation detected. You have exceeded your license limit(%u) or expiry date(%s). For more information, contact sales@machbase.com.|ライセンス違反です。上限を超えているか期限切れです。詳細は sales@machbase.com にお問い合わせください。|
|3039|Session count exceed: (maxcount =%llu).|許可されたセッション数を超えました。|
|3040|Unable to shutdown since the server is busy.|未完了の処理があるため、サーバーを停止できません。|
|3041|AppendBatch error: %s.|AppendBatch に失敗しました。|
|3042|Recovery in progress.|復旧処理を実行中です。|
|3043|Array Execute is not applicable for SELECT query.|SELECT クエリでは配列実行を使用できません。|
|3044|Wrong TIMEZONE string error: %s.|タイムゾーンが無効です。|
|3045|Invalid context at %s.|コンテキストが無効です。|
|3046|Communication module error (rc=%d): [%s].|通信モジュールでエラーが発生しました。|
|3047|Failed to call function %s (rc=%d)|関数の呼び出しに失敗しました。|
|3100|Append Operation is not supported in Cluster Edition|Cluster Edition では APPEND 操作をサポートしていません。|
|3101|Can't convert (%s) to number|数値に変換できません。|
|3102|Can't decode in base64|Base64 をデコードできません。|
|3103|not supported JSON type (%d)|サポートしていない JSON 型です。|
|3104|Column count for append is not matched with Meta|入力の列数がメタデータと一致しません。|
|3105|The table type for append is not valid|入力先のテーブルタイプが無効です。|
|3106|the JSON format is not valid|JSON 形式が無効です。|
|3107|Can't get the meta info for append table|入力先テーブルのメタデータを取得できません。|
|3108|Can't read data from or write data into network buffer|ネットワークバッファーからの読み取り、または書き込みができません。|
|3109|The URL (%s) is not valid format|URL の形式が無効です。|
|3110|Timeout in waiting for response|応答待ちがタイムアウトしました。|
|3111|Can't connect to proxy server (%s:%d)|プロキシサーバーに接続できません。|
|3112|Tag name in JSON must be string type|タグ名は string 型である必要があります。|
|3113|Tag name (%s) does not exist in meta list|タグ名がメタデータのリストにありません。|
|3114|The HTTP memory request exceeded the limit of (%lld). Change the property (HTTP_MAX_MEM) and restart server|HTTP のメモリ要求が上限を超えました。HTTP_MAX_MEM を変更してサーバーを再起動してください。|
|3115|Table name is omitted from the JSON format|JSON にテーブル名が指定されていません。|
|3116|Wrong Base64 Format Received|Base64 形式が無効です。|
|3117|Only Basic Authorization Accept To Login.|ログインには Basic 認証のみ使用できます。|
|3118|There is No Authorization Header.|認証ヘッダーがありません。|
|3119|The value of tag default column<%d> must not be NULL|TAG の基本列の値は NULL にできません。|
|3120|The timezone (%s) is invalid.|タイムゾーンが無効です。|
|3121|Fail to get json object|JSON オブジェクトの取得に失敗しました。|
|3122|There is no argument for Rest API|REST API の引数がありません。|
|3123|Count value is not valid for Rest API|REST API の Count 値が無効です。|
|3124|Interval value is not valid for Rest API|REST API の Interval 値が無効です。|
|3125|Interval type is not valid for Rest API|REST API の Interval 型が無効です。|
|3126|The requested URL for the REST API is not valid|要求された REST API の URL が無効です。|
|3127|The requested URL for the REST API is not supported|要求された REST API の URL はサポートしていません。|
|3128|TAG_STAT is not available for table %s.|このテーブルでは TAG_STAT を使用できません。|
|3200|Server is not running.|サーバーは稼働していません。|
|3201|Invalid statement state: (%d)|ステートメントの状態が無効です。|
|3202|Column index is out of range.|列インデックスが範囲外です。|
|3203|The length of data exceeded the size of buffer.|データ長がバッファーサイズを超えています。|
|3204|Append data ip string is null.|入力データの IP 部分が空です。|
|3205|Append data datetime string(%s) is null.|入力データの時刻部分が空です。|
|3206|Invalid column type (%d).|列の型が無効です。|
|3207|Invalid statement type (%d).|ステートメントの型が無効です。|
|3208|Server thread error: %d - %s|サーバースレッドで問題が発生しました。|
|3209|statement is busy. (%d)|ステートメントが使用中です。|
|3210|This connection has been already disconnected|接続が切断されています。|
|3211|Database already exists.|データベースは既に作成されています。|
|3212|Database does not exist.|データベースが存在しません。|
|3213|Server is running.|サーバーは稼働中です。|
|3214|Failed to open dbs(%s) directory.|dbs ディレクトリを開けませんでした。|
|3215|ALTER SESSION statement is not supported.|ALTER SESSION はサポートしていません。|
