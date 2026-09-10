---
type: docs
title: '13. 運用・設定・復旧'
weight: 130
toc: true
---

Machbase サーバーの起動・停止、設定変更、監視、バックアップ・リストア、Cluster 運用を扱います。
日常運用の手順を先に整え、変更と復旧は計画に従って実施します。

## この章の構成

| 順序 | 節 | 内容 |
|-----:|------|------|
| 13.1 | [サーバーとデータベースの運用](./server-database/) | 起動・停止、データベースの作成・削除、ライセンス |
| 13.2 | [複数データベース](./multi-database/) | 論理データベース、権限、バックアップ・リストア、クライアント連携 |
| 13.3 | [設定の運用](./configuration/) | 設定ファイル、メモリ、ネットワーク、ストレージ、タイムゾーン |
| 13.4 | [ALTER SYSTEM の運用](./alter-system/) | 実行時の設定変更とシステム制御 |
| 13.5 | [データ保持ポリシー](./policy-data-retention/) | Retention の作成、適用、確認、解除 |
| 13.6 | [監視と診断](./diagnosis-observability/) | システムビュー、ログ、セッション、容量、障害の兆候 |
| 13.7 | [スキーマ変更チェックリスト](./checklist-schema-alter/) | DDL 前後の影響分析と検証 |
| 13.8 | [バックアップ・リストア・マウント](./backup-restore-mount/) | オンラインバックアップ、オフラインリストア、読み取り専用マウント |
| 13.9 | [Cluster の運用](./cluster/) | トポロジー、ノードの追加・削除、状態管理 |

日常点検には[サーバーとデータベースの運用](./server-database/)、[設定の運用](./configuration/)、
[監視と診断](./diagnosis-observability/)を利用します。複数データベースを導入する前に
[複数データベース](./multi-database/)を確認してください。スキーマや設定の変更には
[ALTER SYSTEM の運用](./alter-system/)と[スキーマ変更チェックリスト](./checklist-schema-alter/)、
障害復旧とバックアップ検証には[バックアップ・リストア・マウント](./backup-restore-mount/)を参照します。
