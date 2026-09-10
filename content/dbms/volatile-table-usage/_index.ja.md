---
type: docs
title: '10. VOLATILEテーブルの活用'
weight: 100
toc: true
---

VOLATILEテーブルは、サーバープロセス内で共有されるメモリテーブルです。
再起動時のデータ消失、UPSERT、再作成可能なキャッシュパターンを説明します。

## この章の構成

| 節 | 内容 |
|----|------|
| [概要と選択基準](./overview-use-criteria/) | VOLATILEテーブルの特性と適用判断基準 |
| [テーブル構造とスキーマ](./table-structure-schema/) | PRIMARY KEY設計、列の型、スキーマ構成 |
| [作成、変更、削除](./create-alter-drop/) | CREATE VOLATILE TABLE、DROP、永続性の違い |
| [データ入力と変更](./data-input-mutation/) | INSERT、ON DUPLICATE KEY UPDATE、DELETE |
| [クエリと分析](./query-analysis/) | SELECT、条件検索、LIKE |
| [インデックスとパフォーマンス](./index-performance/) | 赤黒木インデックス、PKインデックス |
| [運用とデータライフサイクル](./operations-lifecycle/) | 運用手順とデータ管理 |
| [制約、エラー、トラブルシューティング](./constraints-errors-troubleshooting/) | 機能制約とエラー対応 |
