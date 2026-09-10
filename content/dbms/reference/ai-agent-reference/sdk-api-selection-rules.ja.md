---
type: docs
title: '16.8.9 sdk-api-selection-rules'
weight: 90
toc: true
---

SDK名だけで機能を判断せず、要件と実際のサポート範囲を併せて確認します。

## 選択順序

1. 言語と標準インターフェースの要件を[連携方法の選択](/dbms/development-tools-integration/selection-integration-method/)で確認します。
2. Append、トランザクション、プリペアドステートメント、名前付きバインド、メタデータ、AUTH KEYの要件を整理します。
3. [SDKのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/)でサポート可否と根拠を確認します。
4. 選択したSDKのページでインストール、接続オプション、型マッピング、エラー処理を確認します。

| 環境 | 正式な参照先 |
|------|------|
| C/C++ SQLCLI・ODBC | [SQLCLIとODBC](/dbms/development-tools-integration/cli-odbc/) |
| Java | [JDBC](/dbms/development-tools-integration/jdbc/) |
| Python | [Python](/dbms/development-tools-integration/python/) |
| Node.js・TypeScript | [Node.js / TypeScript](/dbms/development-tools-integration/node-js-typescript/) |
| .NET | [.NET Connector](/dbms/development-tools-integration/net-connector/) |
| Go | [Go](/dbms/development-tools-integration/go/) |

サーバーとSDKのバージョンの組み合わせは、[互換性](/dbms/reference/support-scope-constraints/compatibility-xma-protocol/)も確認します。
