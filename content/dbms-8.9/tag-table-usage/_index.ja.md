---
type: docs
title: '5. TAGテーブルの活用'
weight: 50
toc: true
---

TAGテーブルは、繰り返し観測する対象の名前と時間軸または距離軸を使って計測履歴を保存します。
本章では、Machbase DBMS 8.7.0のTAG構造、データの入力と検索、メタデータ、補正と運用を説明します。
第3・4章で決定したデプロイ環境とデータモデルを、実際のSQLで確認します。

タグは測定対象を、DATAの1行は1回の観測を表します。METADATAはタグごとに1行の属性であり、
過去の観測ごとに保存する属性ではありません。元の測定値、現在の属性、区間集計、収集時刻を
区別すると、検索結果と訂正範囲を一貫して解釈できます。

## 本章の構成

| 節 | 内容 |
|---|---|
| [概要と使用基準](./overview-use-criteria/) | タグ識別子と観測行、時間軸・距離軸の選択 |
| [テーブル構造とスキーマ](./table-structure-schema/) | 列の順序と型、LSL/USL、BINARYとストレージ設計 |
| [作成、変更、削除](./create-alter-drop/) | 基本DDL、METADATAの拡張、オブジェクトの削除 |
| [データの入力と変更](./data-input-mutation/) | タグの自動登録、SQL・Append・ファイル入力の違い |
| [検索と分析](./query-analysis/) | 区間・最新値・STATの検索と結果の解釈 |
| [インデックスと性能](./index-performance/) | 実データによるアクセスパスの確認 |
| [運用とデータライフサイクル](./operations-lifecycle/) | 削除、保持ポリシー、重複排除の完了確認 |
| [制約、エラー、トラブルシューティング](./constraints-errors-troubleshooting/) | 正常条件と意図的に失敗させる例 |
| [活用パターンとシナリオ](./patterns-scenarios/) | 観測単位・単位系・欠損に応じたモデル |
| [TAGメタデータ](./tag-metadata/) | 登録・検索・更新・削除、JSONとARRAY |
| [TAG data UPDATEとデータ補正](./tag-data-update-correction/) | 直接訂正、NULLへの補正、監査履歴 |
| [tagmetaimportとメタデータの一括登録](./tagmetaimport/) | CSVの準備、入力先、再入力エラーの確認 |

## 実習とサポート範囲

各ページは独立した実習です。準備SQLのテーブルがすでに存在する場合は、別の業務オブジェクト
でないか確認し、無断で削除しないでください。成功例と失敗確認用の例を分けて実行し、
後片付けのSQLは実習で作成したオブジェクトだけに適用します。

TAG DATA UPDATEはStandard Edition専用です。自動重複検査期間、METADATA ALTER、LSL/USLの
詳細操作もEditionごとの範囲を確認します。SQL INSERT、Appendの処理応答、ストレージバッファの
フラッシュ、インデックス・統計処理の完了は、それぞれ意味が異なります。

ROLLUPの作成・検索・再構築の全手順は[第6章](../tag-rollup-usage/)で説明します。
本章では、TAGの訂正と削除が集計に与える影響のみ扱います。
