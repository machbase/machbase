---
type: docs
title: '11.3 SDK機能のサポート範囲'
weight: 30
toc: true
aliases:
  - /dbms/development-tools-integration/support-scope-sdk/
  - /dbms/application-integration/support-scope-sdk/
  - /dbms/reference/support-scope-constraints/sdk/
---

アプリケーションの要件に合うSDKを選択できるように、機能別のサポート状況とAPIエントリーポイントを
比較します。インストール、接続、関数、実行コードは各SDKページを参照してください。

初めてSDKを選ぶ場合は[連携方式の選択](../selection-integration-method/)を先に読み、
このページで必要な機能と正確なAPI経路を照合します。

Goの表にある「ネイティブ」は、確認基準がv1.8.4の旧`machgo` APIを指します。
[Go SDK](../go/)はv2の`database/sql` APIを説明しており、v2では旧`machgo`は提供されません。
v1の確認済み機能や最小バージョンをv2へそのまま適用せず、以下のARRAY・選択列Appendなどの
v2固有の確認基準と区別してください。

<a id="support-scope-sdk-nullable-metadata"></a>

## NULL許容性のメタデータ

MachbaseはSELECT結果列のNULL許容性を`NO_NULLS`、`NULLABLE`、`UNKNOWN`で区別します。
アプリケーションは`NULLABLE`と`UNKNOWN`の両方をNULL処理の対象とします。

| SDK | 取得方法 |
|---|---|
| JDBC | `ResultSetMetaData.isNullable()` |
| Python | `cursor.description[i][6]` |
| Goネイティブ | `api.Column.Nullability` |
| Go `database/sql` | `Rows.ColumnTypeNullable()` |
| Node.js | `ColumnMeta.nullable` |
| .NET | `GetSchemaTable()`の`AllowDBNull` |
| SQLCLI・ODBC | ディスクリプターのnullable属性 |

式、集計、VIEW、JOINの結果は`UNKNOWN`になる場合があります。直接の列のスキーマ制約と
検索結果メタデータを同一と考えないでください。

<a id="support-scope-sdk-primary-key-metadata"></a>

## PRIMARY KEYメタデータ

| SDK | 結果列 | テーブルカタログ |
|---|:---:|:---:|
| JDBC | O | `DatabaseMetaData.getPrimaryKeys()` |
| Python | O | カタログSQL |
| Goネイティブ | O | カタログSQL |
| Go `database/sql` | 標準APIなし | カタログSQL |
| Node.js | O | カタログSQL |
| .NET | O | カタログSQL |
| ODBC | 別の結果APIなし | `SQLPrimaryKeys()` |

式・集計・外部JOINのNULL補完側は、元の列のPK属性をそのまま伝達しない場合があります。

<a id="support-scope-sdk-generated-rowid"></a>

## INSERT結果のROWID

Machbase 8.7.0 Standard Editionでは、成功した単一の`INSERT ... VALUES`が対応SDKにROWIDを
提供できます。

| SDK・ツール | 確認方法 | 値がない場合 |
|---|---|---|
| machsql | `SHOW LAST ROWID` | `NULL` |
| Machbase SQLCLI | `SQLGetGeneratedRowID()` | `SQL_NO_DATA` |
| 標準ODBC | 専用の標準APIなし | - |
| JDBC | `Statement.getGeneratedKeys()` | 空の`ResultSet` |
| Python | `cursor.lastrowid` | `None` |
| .NET | `MachCommand.RowId` | `null` |
| Go `database/sql` | `Result.LastInsertId()` | エラー |
| Goネイティブ | 非サポート | - |
| Node.js | 実行結果の`rowId` | `undefined` |

バッチ、`executemany()`、Append、loader、`INSERT ... SELECT`、UPSERTは単一のROWIDを返しません。
SQLの意味とテーブルごとの制約は[ROWID](/dbms/reference/sql/rowid/)を参照してください。

<a id="support-scope-sdk-append"></a>
<a id="append-table-type-matrix"></a>

## Append APIとテーブルタイプ

| API経路 | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION | 基準 |
|---|:---:|:---:|:---:|:---:|:---:|---|
| SQLCLI `SQLAppend*`拡張 | O | O | O | O | O | TRANSACTIONはStandard |
| JDBC `MachStatement.executeAppend*` | O | O | O | O | O | NFX cce422dのソース・テスト |
| Python 2.4 `append*` | O | O | O | O | O | NFX cce422dのソース・テスト |
| .NET `MachAppendWriter` | O | O | O | O | O | NFX cce422dのプロバイダー |
| Go v1.8.4ネイティブ`Appender` | O | O | X | X | O | TRANSACTIONはStandard |
| Go `database/sql`標準API | X | X | X | X | X | `sql.Conn.Raw()`拡張はネイティブ仕様 |
| Nodeソースの`appendBatch()` | O | △ | △ | △ | O | NFX cce422dのソースビルド |
| Nodeソースの`appendOpen()` | O | O | △ | △ | △ | 汎用native/fallback、テーブル別の検証が必要 |

標準クエリ接続とAppendハンドルのライフサイクルを区別し、close・flushの結果を確認します。
`O`は該当ソース・テストで確認した範囲、`△`は汎用経路だけがあり、テーブル別の回帰検証がさらに
必要な範囲です。Append拡張は標準ODBCや`database/sql`の機能ではありません。

### ARRAYと選択列Append

Machbase DBMS 8.7.0のARRAYのサポート範囲は次のとおりです。

| SDK | 密なARRAYの検索・入力 | スパースARRAY | 選択列Append |
|---|:---:|:---:|:---:|
| SQLCLI・C++ | O | O | O |
| Machbase ODBC拡張 | O | O | O |
| JDBC | O | O | O |
| Python | O | O | O |
| Node.js | O | O | O |
| .NET full/legacyプロバイダー | O | O | O |
| Go | v2 mainソース | v2 mainソース | v2 mainソース |

Machbase DBMS 8.7.0サーバーとARRAY機能を含むSDKビルドを合わせて使用します。ARRAYのSQL要素位置と
Machbase専用SDKの位置は0始まりのインデックスです。既存の全行スカラーAppend APIは維持されます。
Node.jsのprepared代替経路も`SparseArray`をサポートします。Goは
[`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17)以降のv2 mainソースを
使用する必要があり、公開v2リリースが指定されるまでは公開モジュールのバージョンだけでサポートを
判断しません。入力方式とAPIの詳細は
[Sparse ARRAYと選択列Append API](../data-input-load-export/array-append/)を参照してください。

<a id="support-scope-sdk-auth-key"></a>

## AUTH KEY

| SDK・ツール | サポート |
|---|:---:|
| machsql、Machbase SQLCLI、ODBC、JDBC | O |
| Goネイティブ、Go `database/sql` | O（neo-client v1.5.0+） |
| Python、Node.js、.NET | X |

鍵の生成・登録・交換は[AUTH KEY認証](/dbms/security-access-control/authentication-auth-key/)、
接続オプションは対応SDKページを参照してください。

<a id="support-scope-sdk-transaction-prepare-bind"></a>

## トランザクション、prepare、bind

| SDK | トランザクションAPI | サーバー側prepare | 名前付きbind API |
|---|:---:|:---:|:---:|
| JDBC | O | O | △（Machbase拡張） |
| Python | X | O | O |
| Goネイティブ | △ | O | O |
| Go `database/sql` | O | O | O |
| .NET | X | X | △ |
| Node.js | X | O | O |
| SQLCLI | △ | O | O |
| ODBC | △ | O | 位置指定bind |

プリペアドステートメントとパラメーターバインディングはトランザクションのサポートとは別です。
プレースホルダーの構文は
[Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。

Machbase 8.7.0 Standard EditionのTAGデータUPDATEは、各SDKの既存の位置指定・名前付きAPIで
NAMEとBASETIMEの条件値をバインドできます。NFX #4127の回帰テストはC/C++ SQLCLI、
Go `database/sql`、JDBC、Node.js、Python、.NETの経路を検証します。ODBCは個別のSDK回帰
マトリクスには含まれず、`?`または名前付きSQLのプレースホルダーを標準`SQLBindParameter()`の
位置番号でバインドします。TAG UPDATEの条件仕様は
[TAGデータUPDATEのバインド](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)を
参照してください。

トランザクション列の`△`は、専用オブジェクトの代わりに同じ接続でトランザクションSQLを直接実行する
経路です。名前付きbind列の`△`は、標準の名前付きバインディングAPIではなく、ドライバー拡張、または
クライアントが値をSQLリテラルに変換する経路を表します。

## 最小確認バージョンと出所

| SDK | 本ドキュメントの確認基準 |
|---|---|
| SQLCLI・JDBC・Python | NFX `cce422d2972`、Pythonパッケージ2.4 |
| Node.js | NFX `cce422d2972`のソースビルド（`package.json` 1.0.1） |
| .NET | Uni 8.0.55、limited 3.1.3、full 3.2.2 |
| Go | 公開済みneo-client v1.8.4、AUTH KEYはv1.5.0+、データベース選択はv1.8.3+ |

NFX cce422dのNode機能の一部は、公開npm 1.0.1の配布後に追加されました。レジストリパッケージの
バージョン文字列だけで同じ機能を想定せず、配布成果物のコミット出所を確認するか、NFXソースビルドを
使用します。

ARRAYと選択列Appendの確認基準は、NFX
`655d1333870313c4951698b89c9a3c9ada11d630`とマージコミット
`f756986c4836982723e2aa7727ec05b7e05e9707`です。サーバーはMachbase DBMS 8.7.0、クライアントは
該当変更以降の検証済みSDK成果物を基準に判断します。

<a id="sdk"></a>

## SDKリファレンス

| SDK | 詳細ドキュメント |
|---|---|
| Machbase SQLCLI・ODBC | [SQLCLIとODBC](../cli-odbc/) |
| JDBC | [JDBC](../jdbc/) |
| Python | [Python](../python/) |
| Node.js / TypeScript | [Node.js / TypeScript](../node-js-typescript/) |
| .NET Connector | [.NET Connector](../net-connector/) |
| Go | [Go](../go/) |
