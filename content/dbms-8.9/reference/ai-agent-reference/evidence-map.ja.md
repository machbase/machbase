---
type: docs
title: '16.8.6 evidence-map'
weight: 60
toc: true
---

回答で述べる内容の種類に応じて、適切な公開の根拠を選択します。

| 主張の種類 | 優先する根拠 |
|----------|-----------|
| SQL構文・関数・型 | [SQLリファレンス](/dbms-8.9/reference/sql/) |
| Edition・テーブル・SDKのサポート | [サポート範囲と制約](/dbms-8.9/reference/support-scope-constraints/)と[SDKのサポート範囲](/dbms-8.9/development-tools-integration/sdk-support-scope/) |
| 設定キー・デフォルト値 | [設定リファレンス](/dbms-8.9/reference/configuration/)と配布パッケージの設定ファイル |
| システム状態の列 | [システムカタログ](/dbms-8.9/reference/system-catalog/) |
| CLIオプション | [コマンドラインツール](/dbms-8.9/reference/command-line-tools/)と配布パッケージの`--help` |
| エラーの意味・対処 | [エラーコード](/dbms-8.9/reference/error-codes/)と[トラブルシューティング](/dbms-8.9/troubleshooting/) |
| 運用手順 | [運用、設定、復旧](/dbms-8.9/operations-configuration-recovery/) |

## 検証規則

- バージョンとEditionの条件を根拠とともに保持します。
- 例の結果を一般的な保証や性能値として扱わないでください。
- 公開の正式リファレンスにない事実は、確認が必要であることを明記します。
- 内部の開発履歴は公開マニュアルのリンクの代わりにはなりません。
