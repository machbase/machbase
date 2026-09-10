---
type: docs
title: '16.6.10 バージョンと互換性'
weight: 100
toc: true
---

Machbase 8.7.0の後方互換性、アップグレード時の注意事項、対応OS/プラットフォームをまとめます。

## 8.7.0の後方互換性

### クライアントドライバーの互換性

| サーバーバージョン | 8.5クライアントドライバー | 8.7.0クライアントドライバー |
|-----------|:---------------------:|:---------------------:|
| 8.7.0サーバー | 限定的な互換性 | 完全互換 |
| 8.5サーバー | 完全互換 | 後方互換 |

- 8.7.0サーバーに8.5クライアントドライバーを使用すると、一部の新機能が動作しない場合があります。
- 旧バージョンのサーバーまたはドライバーの組み合わせでは、Nullableメタデータが従来の値や判定不能の値で返される場合があります。この値に依存するアプリケーションでは、サーバーとSDKの両方を8.7.0へアップグレードしてください。
- CASTのすべての変換先の型と長さ・精度オプションを使用するSQLは、8.7.0サーバーでサポートします。同じ要素数の数値ARRAY全体を`CAST(array_expression AS TYPE[N])`で変換する構文も、このバージョンから使用できます。Cluster Editionでは全ノードをCASTとARRAYに対応した同じバージョンにそろえてください。詳細な構文と変換規則は[CAST関数](/dbms/reference/sql/functions/functions-full/#cast)を参照してください。
- 8.7.0サーバーは`CREATE INDEX IF NOT EXISTS`をサポートします。同じデータベースと所有者に同名のインデックスがある場合、既存の定義を維持して成功するため、繰り返しデプロイした後に実際のインデックスの対応関係を確認してください。旧サーバーではこの構文は使用できません。詳細は[INDEX構文](/dbms/reference/sql/syntax/index-syntax/#create-index-if-not-exists)を参照してください。
- 8.7.0 Standard Editionサーバーでは、TAGデータUPDATEのNAMEとBASETIMEの条件値に位置指定または名前付きバインドパラメーターを使用できます。旧サーバーでは同じプリペアドUPDATEが`ERR-02190`で拒否される場合があります。条件の形式とSDK APIは[TAGデータUPDATEのバインド](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)を参照してください。
- 8.7.0サーバーのBASE DISTANCE TAG統計ビューは、軸列を`*_DISTANCE`という名前と元の`DOUBLE`、`LONG`、`ULONG`型で提供します。従来の`*_TIME`名はエイリアスとして提供せず、既存テーブルもサーバー再起動後に新しいスキーマを使用します。BASE TIME TAGの`*_TIME DATETIME`スキーマは維持します。アプリケーションのSQLと結果マッピングは[TAG別統計ビュー](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema)の変換表に従って変更してください。
- 8.7.0 Standard EditionではSELECT/JOIN計画の改善により、テーブルのスキャン順序とソートしていない結果の返却順序が旧バージョンと異なる場合があります。結果の順序が必要な場合は`ORDER BY`を使用し、アップグレード後は[SELECT/JOINオプティマイザー](/dbms/performance-tuning/performance-query-tuning/#select-join-optimizer)の手順に従って結果と実行計画を併せて確認してください。
- 8.7.0 JDBCドライバーは、複数ホストURLで接続段階のI/Oエラーが発生すると次のホストへの接続を試みます。旧ドライバーが最初のホストの一部のソケットエラーで接続を終了する環境では、8.7.0 JDBCドライバーに置き換え、[複数ホストへの接続](/dbms/development-tools-integration/jdbc/#jdbc-multi-host)のURLとタイムアウト設定を確認してください。
- Machbase DBMS 8.7.0は、固定長の数値ARRAYと選択列Appendをサポートします。ARRAYを使用するアプリケーションはDBMS 8.7.0サーバーと対応機能を含むSDKビルドを併用し、Cluster Editionでは全ノードを一緒にアップグレードしてください。SQLとAPIの詳細は[数値ARRAY型](/dbms/reference/sql/types/array/)と[Sparse ARRAYと選択列Append API](/dbms/development-tools-integration/data-input-load-export/array-append/)を参照してください。
- ARRAY列は、Standard EditionのLOG、VOLATILE、LOOKUP、TRANSACTION、TAG METADATAとCluster EditionのLOGテーブルで`ADD COLUMN`と`DROP COLUMN`をサポートします。既存行へのDEFAULT適用のテーブル別の違いは[DDL構文](/dbms/reference/sql/syntax/ddl-syntax/#add-column)を確認してください。
- ARRAYの公開の位置指定は0始まりです。初期の1始まりのARRAY SQL、疎なオブジェクト、添字付きAppendターゲットを使用するコードでは、各位置を1減らしてください。保存済みARRAYデータと密なARRAYの要素順序は変わらないため、データ移行は不要です。
- サーバーとSDKのバージョンの組み合わせによる機能差は、[サーバーとSDKの互換性](../compatibility-xma-protocol/)を参照してください。

<a id="removed-features-870"></a>

### 8.7.0で削除された機能

Machbase 8.7.0では、次の機能とインターフェースを提供しません。削除された設定、SQL、C APIには
互換レイヤーがないため、アップグレード前に設定ファイル、運用SQL、アプリケーションを変更してください。

| 8.5の機能またはインターフェース | 8.7.0の状態 | ユーザーへの影響 | 移行方法 |
|--------------------------|------------|-------------|-----------|
| DB HTTP/REST（`/machbase`、`/machiot`、ポート5657） | 削除 | 従来のHTTPクエリとAppendリクエストは使用不可 | SQLCLI、ODBC、JDBC、Python、Go、Node.js、.NET SDKを使用 |
| WebAdmin/MWA、静的ClusterAdmin UI | 削除 | Web UIと関連する起動スクリプトは使用不可 | サーバー・クラスターのコマンドラインツールを使用 |
| STREAM SQLとカタログ | 削除 | 登録済みSTREAMの実行と状態参照は不可 | Fluentdまたはアプリケーションのジョブで処理 |
| Result Cache | 削除 | 結果キャッシュの設定、状態参照、フラッシュコマンドは使用不可 | インデックス・ROLLUP・クエリ最適化、またはアプリケーションキャッシュを使用 |
| `machcli.h`と`MachCLI*()` | 削除 | 従来のC/C++ソースとバイナリはそのまま使用不可 | Machbase SQLCLIまたはODBCへ移行 |

次の機能は名前が似ていますが、引き続きサポートします。

| 維持する機能 | 説明 |
|-----------|------|
| Machbase SQLCLI | `<machbase_sqlcli.h>`の`SQL*` API。ODBCとは別のAPI群です。 |
| ODBC、JDBC、言語別SDK | Python、Go、Node.js、.NETを含む対応ドライバーは引き続き使用できます。 |
| MachEngine API | 従来の`Mach*` APIを引き続き使用できます。 |
| PVO Cache | 実行計画オブジェクトを再利用するキャッシュで、削除されたResult Cacheとは異なります。 |
| Coordinator管理REST | データSQL RESTとは別の管理用APIです。Coordinatorの`/admin/`パスは引き続き使用できます。 |

#### アップグレード前の設定ファイルの整理

次のプロパティが8.7.0の`machbase.conf`に残っていると、不明なプロパティとして扱われ、
サーバーが起動しません。バイナリを置き換える前にすべて削除してください。

```text
HTTP_AUTH
HTTP_ENABLE
HTTP_MAX_MEM
HTTP_PORT_NO
RS_CACHE_APPROXIMATE_RESULT_ENABLE
RS_CACHE_ENABLE
RS_CACHE_MAX_MEMORY_PER_QUERY
RS_CACHE_MAX_MEMORY_SIZE
RS_CACHE_MAX_RECORD_PER_QUERY
RS_CACHE_TIME_BOUND_MSEC
STREAM_THREAD_COUNT
STREAM_WAIT_MS
```

従来のSTREAM定義が必要な場合は、8.5サーバーを停止する前に`V$STREAMS`と関連SQLを別途記録します。
8.7.0では`SYS_STREAM_STMTS`、`V$STREAMS`、`V$HTTP_STATUS`、`V$RS_CACHE_LIST`、
`V$RS_CACHE_STAT`は登録されません。

アップグレード後、次の各クエリの結果が`0`であることを確認します。

```sql
SELECT COUNT(*) AS removed_property_count
FROM V$PROPERTY
WHERE NAME IN (
    'HTTP_AUTH', 'HTTP_ENABLE', 'HTTP_MAX_MEM', 'HTTP_PORT_NO',
    'RS_CACHE_APPROXIMATE_RESULT_ENABLE', 'RS_CACHE_ENABLE',
    'RS_CACHE_MAX_MEMORY_PER_QUERY', 'RS_CACHE_MAX_MEMORY_SIZE',
    'RS_CACHE_MAX_RECORD_PER_QUERY', 'RS_CACHE_TIME_BOUND_MSEC',
    'STREAM_THREAD_COUNT', 'STREAM_WAIT_MS'
);

SELECT COUNT(*) AS removed_table_count
FROM V$TABLES
WHERE NAME IN (
    'SYS_STREAM_STMTS', 'V$HTTP_STATUS', 'V$RS_CACHE_LIST',
    'V$RS_CACHE_STAT', 'V$STREAMS'
);
```

### DDLの同時実行の互換性

Machbase 8.7.0では、EditionによってDDLの同時実行ポリシーが異なります。

| Edition | 8.7.0の動作 | `DDL_LOCK_TIMEOUT` |
|---------|------------|--------------------|
| Standard | 独立した異なるオブジェクトのDDLを同時に実行可能 | 提供。デフォルト値は`0`（NOWAIT） |
| Cluster | 従来のカタログ範囲のDDLポリシーを維持 | 提供しない |

Standard Editionで同じオブジェクトや直接関連するオブジェクトのDDLが競合すると、デフォルトでは
`ERR-02031: Resource busy (<object>)`が即座に返されます。旧バージョンの待機動作を前提とする
デプロイスクリプトには、アップグレード後に次のいずれかを明示的に適用します。

- デプロイ用セッションで`ALTER SESSION SET DDL_LOCK_TIMEOUT = seconds`を使用して待機時間に上限を設定します。
- `ERR-02031`に限り、回数を制限した再試行と待機間隔を適用します。
- 再試行前にオブジェクトの状態を確認し、`already exists`、権限エラー、構文エラーは再試行しません。

競合関係と設定方法の詳細は、[DDLの同時実行とロック](/dbms/reference/sql/syntax/ddl-syntax/#ddl-concurrency)を参照してください。

### バックアップファイルの互換性

| バックアップのバージョン | 8.7.0での復元 | 備考 |
|--------------|:-----------:|------|
| 8.5バックアップ | O | `MOUNT`または`machadmin -r`を使用 |
| 8.7.0バックアップ | O | |
| 8.4以前のバックアップ | △ | バージョンによって異なるためテストが必要 |

## 正式なアップグレード手順

実行順序、対応プラットフォーム、事前確認は[アップグレード](../../../installation-deployment-upgrade/upgrade/)を参照してください。
このページではSQL・サーバー・クライアントの互換性に関する事実のみを管理します。
