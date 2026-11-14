---
type: docs
title: '16.8 AI Agent Reference'
weight: 100
toc: true
description: 'Machbase DBMSドキュメントを使用するAIエージェントとRAGシステムのための参照先と根拠のガイド'
---

AI Agent Referenceは、AIエージェントとRAGシステムがMachbase DBMS 8.7のドキュメントから
正しい公式リファレンスを見つけるための案内です。SQL構文、SDKのサポート範囲、運用手順は
ここでは再定義せず、各機能の正式なドキュメントにリンクします。

## 構成

| ページ | 目的 |
|--------|------|
| [エージェント利用ガイド](./guide-agent/) | 質問の分類、検証順序、回答の原則 |
| [canonical-url-map](./canonical-url-map/) | トピック別の正規ドキュメントURL |
| [task-map](./task-map/) | ユーザーの作業別の参照・検証順序 |
| [support-matrix](./support-matrix/) | Edition・テーブル・SDKの正式なサポート表の検索 |
| [constraints-index](./constraints-index/) | 制約とエラー条件の正式な参照先 |
| [evidence-map](./evidence-map/) | 主張の種類に応じた根拠の選択 |
| [terminology-disambiguation](./terminology-disambiguation/) | 混同しやすい用語の確認 |
| [sql-generation-rules](./sql-generation-rules/) | SQL生成前の検証規則 |
| [sdk-api-selection-rules](./sdk-api-selection-rules/) | SDKとAPIの選択順序 |
| [operations-checklist](./operations-checklist/) | 安全な運用回答の作成順序 |
| [error-resolution-map](./error-resolution-map/) | エラー診断の正式な参照先 |
| [llms.txt](./llms-txt/) | 機械可読の簡潔なドキュメントマップ |
| [全文とRAGインデックス](./llms-full-txt-chunk-index/) | 全文MarkdownとJSONドキュメントインデックス |

## 機械可読の出力

- [llms.txt](/ja/llms.txt)
- [llms-full.txt](/ja/llms-full.txt)
- [llms-chunks.json](/ja/llms-chunks.json)

上記の出力には現行の日本語DBMSドキュメントのみを含みます。Machbase Neoと
保存用のDBMS 8.5ドキュメントは含みません。

## 利用原則

1. サーバーバージョン、Edition、テーブルタイプ、SDKを最初に確認します。
2. 機能の正式なリファレンスとサポート範囲を併せて読みます。
3. 未確認の構文、デフォルト値、制限、エラーコードを作らないでください。
4. 運用変更では対象、影響、復旧方法、完了条件を明記します。
5. 回答のリンクには公開の正規URLを使用します。
