---
type: docs
title: '11.5.6 移行とトラブルシューティング'
weight: 60
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/migration-troubleshooting/
---

最新のMachbase JDBCはJava 8/JDBC 4.2を基準として、バージョン報告、メタデータ、型変換、
トランザクション、リソースのライフサイクルを標準JDBC仕様に合わせています。
以前の動作に依存するアプリケーションは、次の違いを確認してください。

## 旧ドライバーからの移行

| 領域 | 現在の動作 | アプリケーションの確認事項 |
|------|-----------|------------------------|
| Java/JDBC基準 | Java 8バイトコード、JDBC 4.2を報告 | 実行JDKはJava 8以降を使用します。 |
| ドライバーバージョン | ドライバーとメタデータは3.0.0を報告 | バージョン判定ロジックを更新します。 |
| 自動検出 | JDBCサービスプロバイダーを提供 | 明示的な`Class.forName()`は任意です。 |
| ParameterMetaData | JDBCのprecision、DB型名、Javaクラスを返す | precisionの型別の意味を確認し、保存バイト数とは解釈しません。 |
| トランザクション | 遅延`BEGIN`、実際のcommit/rollback | StandardのTRANSACTION操作を明示的に完了します。 |
| カーソル保持設定 | `CLOSE_CURSORS_AT_COMMIT` | コミット後にResultSetを再検索します。 |
| DatabaseMetaData | 標準結果構造とサポート機能を返す | ドライバー固有の列番号ではなく標準列名を使用します。 |
| 型API | 型指定`getObject()`、`JDBCType`、Boolean、符号なし型、LOB | メタデータのJavaクラスで検索・バインドします。 |
| エラー | 不正な状態で標準`SQLException`を返す | SQLStateでエラーを分岐します。 |
| タイムアウト | クエリ・ネットワークのタイムアウトをサポート | ネットワークタイムアウト後は接続を破棄します。 |
| 接続プール | 論理接続の貸し出し期間と状態初期化 | 閉じたハンドルやメタデータを再利用しません。 |
| 生成キー | Standardの単一INSERTのROWIDを返す | `getGeneratedKeys()`の`ROWID`を読み取ります。 |

名前付きbindは対応サーバーで使用します。旧サーバーが名前付きbindをサポートしない場合は
SQLState `0A000`になるため、位置指定パラメーター`?`に切り替えます。

## 非サポート機能

次のJDBC任意機能はサポートしません。

- セーブポイント
- XAと分散トランザクション
- ストアドプロシージャとCallableStatementの成功経路
- スクロール可能または更新可能なResultSet
- Statement pooling
- 複数結果の同時オープン
- Struct、Ref、SQLXML、UDT型マッピング
- 専用NClobストレージとファクトリー
- Machbase専用RowSetプロバイダー
- JDBC 4.3のシャーディングとリクエスト境界API

Machbase DBMS 8.7.0とARRAY対応JDBCビルドでは、`java.sql.Array`、`createArrayOf()`、
`setArray()`を使用できます。旧ドライバーのARRAY非サポートの説明は適用せず、
[ARRAYと選択列Append](../append-api/#arrayと選択列)のバージョンとインデックス基準を確認します。

非サポート機能は通常、`SQLFeatureNotSupportedException`とSQLState `0A000`を返します。
機能を呼び出す前にDatabaseMetaDataの機能情報を確認します。

## `No suitable driver`

**症状**

`DriverManager.getConnection()`で`No suitable driver`が発生します。

**確認と解決**

1. 実行クラスパスに`machbase.jar`があるか確認します。
2. JARに`META-INF/services/java.sql.Driver`があるか確認します。
3. URLが`jdbc:machbase://<host>:<port>/machbasedb`形式か確認します。
4. 複数バージョンのMachbase JDBC JARが同時に含まれていないか確認します。

## SQLState `0A000`

選択した機能またはサーバーがそのAPIをサポートしていません。セーブポイント、スクロール可能なカーソル、
XAには代替フローを使用します。生成キーはStandard EditionとROWID対応のサーバー・JDBCの組み合わせで
使用し、`DatabaseMetaData.supportsGetGeneratedKeys()`で確認します。
名前付きbindで発生した場合は、位置指定パラメーター`?`を使用します。

## コミット後にResultSetが閉じる

正常な動作です。Machbaseのトランザクションのカーソル保持設定は`CLOSE_CURSORS_AT_COMMIT`です。
コミット前に結果を読み取るか、コミット後にクエリを再実行します。
StatementとPreparedStatementは再利用できます。

## LOG DMLがロールバックされない

手動トランザクションでTRANSACTIONテーブルを変更する前に実行した最初のLOG DMLは、互換経路で
auto-commitとして再実行される場合があります。この入力は後続のロールバック対象ではありません。
ロールバックが必要なデータにはTRANSACTIONテーブルを使用します。

## 複数のTRANSACTIONテーブルをまとめてコミット

通常のコミットとロールバックはサポートしますが、バックエンドのコミット中に障害が発生した場合、
複数のTRANSACTIONテーブルの全体の原子性は保証しません。
重要なアトミック操作は1つのTRANSACTIONテーブルの範囲で設計します。

## ネットワークタイムアウトまたは接続エラー

ソケット読み取りタイムアウトやSQLStateクラス`08`の接続エラーが発生した場合、その物理接続は
再利用しません。接続プールから新しい接続を借り、有効なトランザクションは業務の冪等性ポリシーに
従って最初から再実行します。例外だけでコミットの成否を推測しません。

## クローズしたプールオブジェクトの再利用

論理Connectionを閉じた後、そのConnectionから取得したStatement、ResultSet、DatabaseMetaDataを
次の貸し出し期間で再利用するとSQLState `08003`になります。
各貸し出し期間のオブジェクトはtry-with-resourcesの範囲内だけで使用します。
