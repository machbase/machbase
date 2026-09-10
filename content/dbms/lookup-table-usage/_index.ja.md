---
type: docs
title: '9. LOOKUPテーブルの活用'
weight: 90
toc: true
---

LOOKUPテーブルは、永続保存した基準情報やマスターデータをサーバー起動時にメモリへロードし、
PRIMARY KEYをキーに高速参照するテーブルです。
メモリ常駐構造、JSON/SEQUENCE、JOIN、一般の述語に基づくDMLを説明します。

## この章の構成

| 節 | 内容 |
|----|------|
| [概要と選択基準](./overview-use-criteria/) | LOOKUPテーブルの用途と適用条件 |
| [テーブル構造とスキーマ](./table-structure-schema/) | 列構成、PK構造、スキーマ設計 |
| [作成、変更、削除](./create-alter-drop/) | DDL: CREATE、ALTER、DROP |
| [データ入力と変更](./data-input-mutation/) | INSERT、Append、再ロード、削除 |
| [クエリと分析](./query-analysis/) | SELECT、JOIN、条件検索 |
| [インデックスとパフォーマンス](./index-performance/) | 赤黒木インデックス、セカンダリインデックス、チューニング |
| [運用とデータライフサイクル](./operations-lifecycle/) | バックアップ・復旧、データの永続性 |
| [制約、エラー、トラブルシューティング](./constraints-errors-troubleshooting/) | 制限、エラー原因、対処 |
| [活用パターンとシナリオ](./patterns-scenarios/) | コードテーブル、マスターデータ、しきい値管理 |
| [PRIMARY KEYポリシー](./primary-key-policy/) | 自然キーと代理キー、PK不変の原則 |
| [SEQUENCE列](./sequence-column/) | 自動増分番号の設定とNEXTVALの使用方法 |
| [JSON列とJSONクエリ](./json-column-query/) | JSON列のサポート範囲、パス条件検索、PRIMARY KEYの制約 |
| [一般述語のUPDATE/DELETE](./predicate-update-delete/) | 非PK・範囲・文字列・日付・JSONパス条件による変更 |
