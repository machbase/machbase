---
type: docs
title: '11. 開発とアプリケーション連携'
weight: 110
toc: true
aliases:
  - /dbms/reference/sdk-api/
  - /dbms/application-integration/
---

アプリケーションの要件に合う連携方式を選び、SDK別のインストール・APIと共通の運用原則を確認します。
言語別の実装は各SDKページ、複数SDKに共通する判断基準は選択・概念・サポート範囲のページを参照します。

## 読む順序

1. [連携方式の選択](selection-integration-method/)で言語と入力方式に合うインターフェースを選びます。
2. [共通の連携概念](concepts-common/)で認証、時間値、バインディング、トランザクション、再試行を確認します。
3. [SDK機能のサポート範囲](sdk-support-scope/)で必要な機能の実際のサポート状況を比較します。
4. 該当言語のSDKページでインストール、接続、実行コードを確認します。
5. [データの入力とエクスポート](data-input-load-export/)で作業別の手順を適用します。
   SQLのROWIDの意味は[ROWID](../reference/sql/rowid/)を参照してください。
   Machbase DBMS 8.7.0のARRAYの部分入力は
   [Sparse ARRAYと選択列Append API](data-input-load-export/array-append/)を参照してください。

## SDK別リファレンス

| 環境 | ドキュメント |
|---|---|
| C/C++ネイティブまたはODBC | [Machbase SQLCLIとODBC](cli-odbc/) |
| Java・Spring | [JDBC](jdbc/) |
| Python | [Python](python/) |
| Node.js・TypeScript | [Node.js / TypeScript](node-js-typescript/) |
| C#・VB.NET | [.NET Connector](net-connector/) |
| Goネイティブ・`database/sql` | [Go](go/) |

## 共通の接続情報

| 項目 | デフォルト値 | 説明 |
|---|---|---|
| HOST | `127.0.0.1` | Machbaseサーバーのホスト名またはIP |
| PORT | `5656` | Machbaseサーバーポート（`machbase.conf`の`PORT_NO`） |
| USER | `SYS` | ユーザーID |
| PASSWORD | `MANAGER` | ユーザーパスワード |

本番環境では専用ユーザーと必要最小限の権限を使用します。アカウントと認証設定は
[アカウント、権限、アクセス制御](../security-access-control/)を参照してください。

## 既存のサポート範囲リンク

NULL・PRIMARY KEYメタデータ、ROWID、Append、AUTH KEYのSDK別サポート状況は
[SDK機能のサポート範囲](sdk-support-scope/)で確認してください。

<a id="support-scope-sdk-nullable-metadata"></a>
<a id="support-scope-sdk-primary-key-metadata"></a>
<a id="support-scope-sdk-generated-rowid"></a>
<a id="support-scope-sdk-append"></a>
<a id="support-scope-sdk-auth-key"></a>
<a id="support-scope-sdk-transaction-prepare-bind"></a>
<a id="sdk"></a>
