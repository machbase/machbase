---
type: docs
title: '11.1 連携方式の選択'
weight: 10
toc: true
aliases:
  - /dbms/application-integration/selection-integration-method/
  - /dbms/application-integration/guide-drivers/
---

プロジェクトの言語、入力特性、デプロイ環境に合う連携方式を選択します。

<a id="selection-guide-integration-method"></a>

## 選択基準

| 要件 | 優先して検討する方式 |
|----------|------------------|
| C/C++ネイティブのコレクター | SQLCLI |
| ODBCマネージャー・DSNベースのアプリケーション | ODBC |
| Java・Spring | JDBC |
| Pythonによる分析・自動化 | `machbaseapi` |
| C#・VB.NET | .NET Connector |
| Goのコレクター・サービス | v2の`database/sql`。旧v1ではネイティブ`machgo`も使用可能 |
| Node.js・TypeScriptバックエンド | `@machbase/ts-client` |
| R分析環境 | Machbase ODBCドライバーとRODBC |
| 大きなファイルの一括入力・エクスポート | machloader、csvimport、csvexport |
| 継続的なTAG・LOGの大量入力 | 選択したSDKのAppend API |

ブラウザーから5656ポートに直接接続しません。バックエンドでクエリを実行し、必要な結果のみを渡します。

## 決定手順

1. アプリケーションの言語で保守可能な公式ドライバーを選びます。
2. 5656ポートへの接続、OSとランタイムの互換性を確認します。
3. SQL、プリペアドステートメント、Append、トランザクションの必要な機能を決めます。
4. [SDK機能のサポート表](../sdk-support-scope/)で実際のサポート状況を確認します。
5. サンプルデータでタイムスタンプ、NULL、数値、文字列の往復を検証します。
6. 目標の行サイズ・同時接続数・バッチサイズで負荷テストします。

Appendのサポートだけでドライバーを決定しません。フラッシュ遅延、サーバーのエラー処理応答、再接続、
失敗行の処理まで実際のSDKで確認します。TRANSACTION DMLには明示的トランザクションのサポート範囲を
確認し、TAG・LOGのAppendを同じロールバック単位とは考えないでください。

<a id="distinction-sdk-api-canonical-owner"></a>

<a id="정본-구분"></a>

## トピック別の詳細ドキュメント

| 内容 | 詳細ドキュメント |
|------|------|
| SDKのインストール・接続・API・完全なコード | 本章のSDK別ページ |
| 共通の認証・バインディング・トランザクション・再試行 | [共通の連携概念](../concepts-common/) |
| SDK別の機能サポート状況 | [SDK機能のサポート範囲](../sdk-support-scope/) |
| SQL・設定・コマンドラインの詳細 | [第16章 リファレンス](/dbms/reference/) |
| 入力・エクスポート方式の選択 | [データの入力とエクスポート](../data-input-load-export/) |

連携方式を選んだら、該当SDKページのインストールと接続例を実行します。
機能のサポート状況は、ドキュメントに記載されたバージョンと実際の配布成果物を合わせて確認します。
