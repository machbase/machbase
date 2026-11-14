---
type: docs
title: '6. TAGテーブルのROLLUP活用'
weight: 60
toc: true
---

ROLLUPは時間軸TAGのデータを事前集計し、検索時に統計を合算して繰り返し分析のコストを減らす機能です。
この章ではMachbase DBMS 8.7.0の基本・条件付き・拡張・JSON・Custom ROLLUPを区別し、
作成から結果検証、再構築までを説明します。

## 最初に区別する3つの間隔

| 概念 | 意味 | 例 |
|---|---|---|
| 作成時のINTERVAL | 保存する集計バケットの間隔 | 1 MIN |
| WAKEUP INTERVAL | 集計ジョブを起動する周期 | 10 SEC |
| クエリのバケット | レポートが要求する結果区間 | `rollup('min', 5, time)` |

同じバケットに複数回の部分集計が保存される場合があります。
基本ROLLUPでは公開クエリ構文が必要な統計をマージし、Customの出力先TAGではユーザーが最終再集計クエリを作成します。
元データの保持期間とROLLUPの保持・再構築ポリシーは別途定めます。

## この章の構成

| 節 | 内容 |
|---|---|
| [概要と選択基準](./overview-use-criteria/) | 基本実習と元データ・集計の比較 |
| [対象TAGの設計](./target-tag-table-design/) | ON/FROM、階層の制約、容量見積もり |
| [作成と削除](./create-delete-rollup/) | CREATE、WITH ROLLUP、IF NOT EXISTSと依存関係 |
| [クエリ構文](./query-syntax-rollup/) | 候補選択、時間単位、origin |
| [条件付きROLLUP](./conditional-rollup/) | 元データのフィルターと明示的な候補選択 |
| [Custom ROLLUP](./custom-rollup/) | 増分結果の再集計とOHLCV階層 |
| [拡張ROLLUP](./extension-rollup/) | FIRST/LASTとOHLCの検証 |
| [JSON ROLLUP](./json-summarized-rollup/) | パス・ドキュメント全体の集計とNULL |
| [制御と状態](./ingestion-control-rollup/) | STOP/START/WAKEUP/FORCE、V$ROLLUPとgap |
| [REBUILD](./rollup-rebuild/) | 実際のサポート対象、バケット境界、訂正 |
| [パフォーマンスチューニング](./performance-tuning-rollup/) | 同じ結果を基準にコストを比較 |
| [活用シナリオ](./patterns-scenarios/) | 複数タグと元データ・集計の役割分担 |

各ページは独立した実習で、オブジェクト名を`ch6_`で区別します。
既存の業務オブジェクトと名前が重複しないことを確認し、意図的なエラー例は成功するスクリプトと分離してください。
固定時刻のデータは、示した固定区間で検索します。実習用テーブル・ROLLUPだけを削除してください。

CustomとREBUILDはStandard Edition専用です。
ROLLUPの作成や取り込みに成功したことだけで、集計が完了したと判断しないでください。
実習では名前を指定したFORCEで処理範囲に追いつき、結果を確認します。

[サポート範囲](../reference/support-scope-constraints/rollup/)と
[トラブルシューティング](../troubleshooting/rollup/)で、制約と診断を引き続き確認してください。
