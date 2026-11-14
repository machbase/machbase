---
type: docs
title: '16. リファレンス'
weight: 160
toc: true
---

構文、関数、設定、システムカタログの正確な定義を確認するための総合リファレンスです。
SDK/APIドキュメントは第11章「開発とアプリケーション連携」を、概念や使用例は各機能の章を参照してください。

## 構成

| セクション | 説明 |
|------|------|
| [SQLリファレンス](./sql/) | SQL構文辞典、関数辞典、データ型、ヒント、相対時間式 |
| [設定リファレンス](./configuration/) | machbase.confのプロパティ、動的に変更できるプロパティ一覧 |
| [コマンドラインツール](./command-line-tools/) | machsql、machadmin、machloaderなどのCLIツールのオプション |
| [開発ツール連携](../development-tools-integration/) | Go、Python、Java、CのクライアントSDK/API（第11章） |
| [システムカタログ](./system-catalog/) | V$、M$SYSビュー一覧と列の説明 |
| [エラーコード](./error-codes/) | エラー番号、メッセージ、原因、対処方法 |
| [サポート範囲と制約](./support-scope-constraints/) | テーブルタイプ別の機能サポート可否と既知の制約 |
| [AI Agent Reference](./ai-agent-reference/) | AI・RAG向けの案内、正式な参照先のマップ、LLM出力 |

## 活用方法

- **構文の確認** → [SQL構文辞典](./sql/syntax/)
- **関数の引数と戻り値** → [SQL関数辞典](./sql/functions/)
- **データ型の範囲とデフォルト値** → [データ型辞典](./sql/types/)
- **設定値の意味と許容範囲** → [設定リファレンス](./configuration/)
- **エラー原因の特定** → [エラーコード](./error-codes/)

> 動作の仕組み、選択基準、運用ガイドは、該当機能の章を参照してください。
