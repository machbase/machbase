---
title: チャート設定
type: docs
weight: 30
toc: true
---

## 概要

{{< media slug="neo-dashboard/chart-setting-preview" width="600" >}}

チャート設定画面は 3 つの領域に分かれます。

- **プレビュー**: 現在の設定で描画したチャートです。
- **シリーズ設定**: 検索するデータ（Series）、計算（Transform）、このパネルだけの範囲（Time または Distance）をタブで指定します。
- **チャートオプション**: チャートタイプと表示オプションを指定します。

## プレビュー

右上の`Apply`はプレビューを更新し、`Save`は設定したパネルをダッシュボードに追加します。`Discard`は変更を破棄して戻ります。

- **Discard**: 保存せずにチャート設定画面を閉じます。
- **Apply**: 変更した設定でプレビューを再描画します。変更がない場合は **Refresh** と表示され、押すとデータを再検索します。
- **Save**: 新しいパネルはダッシュボードに追加し、既存のパネルは変更内容を反映して画面を閉じます。

## シリーズ設定

タブの右にある `Total n / 12` は、Visible がオンの Series と Transform の数です。1 つのパネルには最大 12 個まで表示できます。

### 基本入力

TAG テーブルを検索するときに使う基本の入力です。

{{< media slug="neo-dashboard/query-tag-based" width="600" >}}

- **Table**: 検索するテーブル。一覧にはテーブル名の下に `データベース · 所有者` が表示されます。`{{変数名}}` の形式で変数を直接入力することもできます。Gauge、Pie、Liquid fill タイプでは、TAG テーブルごとのタグ別統計ビュー `V$<テーブル>_STAT` も一覧に表示されます。統計列（`ROW_COUNT`、`MIN_VALUE`、`MAX_VALUE` など）を Value field に選ぶと、タグの件数・最小値・最大値を表示できます。
- **Tag**: 使用するタグ名。右の<img src="/images/web-ui/neo-dashboard/icons/dash_tag_search.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンでタグ検索ダイアログを開きます。
- **Time field / Value field**: X 軸の基準列と Y 軸の値列。値の列が JSON 型の場合は **JSON key** 選択欄が追加され、JSON 内部のパスを指定できます。
- **Aggregator**: X 軸の間隔ごとに適用する集計関数です。`value`（集計せず生データ）、`sum`、`avg`、`min`、`max`、`count` に加えて `diff`、`diff (abs)`、`diff (no-negative)` を使用できます。
- **Alias**: 凡例に表示する名前。

### 詳細入力（Expand）

シリーズ行の **Expand** <img src="/images/web-ui/neo-dashboard/icons/dash_series_expand.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンを押すと、値の列と条件を直接指定する入力に切り替わります。Table と Time field は基本入力と同じです。

- **Value field**: 値の列です。値ごとに Aggregator と Alias を指定し、Geomap タイプでは<img src="/images/web-ui/neo-dashboard/icons/dash_add_series.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンで値を複数追加できます。
- **Filter**: WHERE 条件を入力します。<img src="/images/web-ui/neo-dashboard/icons/dash_add_series.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンで追加した条件は `AND` で結合され、条件行の **Typing** <img src="/images/web-ui/neo-dashboard/icons/dash_series_typing.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンを押すと条件式を直接入力できます。
- **Duration From / To**: LOG テーブルでのみ表示されます。検索範囲の開始と終了をどれだけずらすかを `-30s`、`+30s` のような形式で指定します。

LOG や VIEW など TAG テーブル以外のテーブルは最初から詳細入力で表示され、基本入力には切り替えられません。

### SQL を直接入力する（Typing）

{{< neo_since ver="8.0.46" />}}

シリーズ行の **Typing** <img src="/images/web-ui/neo-dashboard/icons/dash_series_typing.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンを押すと、検索内容全体を SQL で記述できます。Line と Bar タイプでのみ使用でき、Aggregator が `diff` 系の場合は切り替えられません。

{{< media slug="neo-dashboard/query-typing-mode" width="600" >}}

- SELECT 句は「時刻（ミリ秒）」の次に「値」の順で構成します。
- ダッシュボードが提供する組み込み変数（`{{period_value}}`、`{{period_unit}}` など）とユーザー定義変数を併用できます。組み込み変数の一覧は「TQL チャート」を参照してください。

### シリーズ行のアイコン

{{< media slug="neo-dashboard/query-control-icons" width="200" >}}

左から順に次の機能です。

- <img src="/images/web-ui/neo-dashboard/icons/dash_series_typing.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Typing**: SQL 直接入力に切り替えます。SQL 入力中は **Selecting** に変わり、押すと選択入力に戻ります。
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_formula.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Enter formula**: 取得した値に適用する式を入力します（例: `value * 1.5`）。
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_visible.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Visible**: このシリーズをチャートに表示するかを指定します。計算だけに使うシリーズはオフにします。
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_color.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Color**: シリーズの色を指定します。
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_expand.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Expand**: 詳細入力に切り替えます。詳細入力中は **Collapse** に変わり、押すと基本入力に戻ります。
- <img src="/images/web-ui/neo-dashboard/icons/dash_series_delete.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> **Delete**: シリーズを削除します。

### Transform

{{< neo_since ver="8.0.46" />}}

定義したシリーズの結果から新しいデータを計算します。Line、Bar、Scatter、Pie、Adv scatter、Liquid fill、Gauge、Text タイプでタブが表示されます。まず計算に使うシリーズを 2 つ以上定義します。

{{< media slug="neo-dashboard/query-two-series" width="600" >}}

次に **Transform** タブで行を追加し、式を記述します。

{{< media slug="neo-dashboard/transform-filled" width="600" >}}

- **Alias**: 生成されるシリーズの名前。
- **Series**: 計算に使用するシリーズを選択します。
- **Formula**: 選択したシリーズの前に表示される英字を使って式を書きます（例: `log(B/A)`）。
- <img src="/images/web-ui/neo-dashboard/icons/dash_transform_help.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンで簡単なヘルプを表示します。使用できる数学関数は左メニュー「TQL > Utility Functions」の Math を参照してください。

Transform で作成したシリーズは通常のシリーズと同じように扱います。

- 行の右にある **Visible** <img src="/images/web-ui/neo-dashboard/icons/dash_series_visible.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">・**Color** <img src="/images/web-ui/neo-dashboard/icons/dash_series_color.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">で表示の有無と色を指定します。計算だけに使った元のシリーズは Visible をオフにし、結果のシリーズだけを表示できます。
- チャートオプションでシリーズを選ぶ場所（yAxis の Series、Text の Series など）に **Alias** の名前で表示されます。Alias が空の場合は `TRANSFORM_VALUE(0)` のように番号付きの名前になります。
- Visible がオンの Transform の結果も `Total n / 12` に含まれます。

※ シリーズの結果を再計算して描画するため、計算のないシリーズより遅くなる場合があります。

### Time・Distance タブ

このパネルだけの検索範囲と更新周期を指定します。距離で検索するパネルには、Time タブの代わりに Distance タブが表示されます。詳しくは「チャートパネル」のパネル単位の時間・距離範囲を参照してください。

## チャートオプション

上部でチャートタイプを選び、その下で表示オプションを指定します。タイプごとに異なるオプションは「チャートタイプ別のオプション」を参照してください。

以下のオプションは複数のチャートタイプに共通して表示されます。表示されるタイプは次のとおりです。

- **Panel option**: TQL、Video 以外のすべてのタイプ
- **Legend・Panel padding・Tooltip**: TQL、Video、Text、Geomap 以外のすべてのタイプ
- **xAxis・yAxis**: Line、Bar、Scatter、Adv scatter

### Panel option

| オプション | 説明 |
|:-----|:-----|
| Title | パネルに表示するタイトル。Geomap では右側のカラーピッカーでタイトルの色も指定します。 |
| Theme | チャートテーマ（左メニュー「TQL > CHART」参照） |

### Legend

| オプション | 説明 |
|:-----|:-----|
| Show legend | 凡例の表示 |
| Vertical | 縦方向の位置（top / center / bottom） |
| Horizontal | 横方向の位置（left / center / right） |
| Alignment type | 配置方向（horizontal / vertical） |

### Panel padding

パネル枠とチャートの間の余白です。凡例のスペースが必要な場合は余白を十分に確保してください。

| オプション | 説明 |
|:-----|:-----|
| Top | 上の余白 |
| Bottom | 下の余白 |
| Left | 左の余白 |
| Right | 右の余白 |

### Tooltip

| オプション | 説明 |
|:-----|:-----|
| Show tooltip | ツールチップの使用 |
| Type | ツールチップのタイプ（item / axis） |
| Unit | ツールチップに表示する単位 |
| Decimals | 小数点以下の桁数 |

### xAxis

| オプション | 説明 |
|:-----|:-----|
| Interval type | X 軸の間隔の単位。時間軸では none / sec / min / hour、距離軸では none / value から選びます。none は自動計算です。 |
| Interval value | X 軸の間隔の値 |

距離の基準軸を使うパネルと Adv scatter では、**Options** に値軸のオプション（Unit・Decimals・Min・Max・Start at zero）も表示されます。

### yAxis

{{< neo_since ver="8.0.46" />}}

| オプション | 説明 |
|:-----|:-----|
| Name | Y 軸名 |
| Position | Y 軸の位置（left / right） |
| Offset | 軸を既定の位置から移動する距離（ピクセル） |
| Tick options | 目盛り値の Unit（単位）、Decimals（小数点以下の桁数）、Min（最小値）、Max（最大値）、Start at zero（常に 0 を含める） |
| Thresholds | **Add threshold** で値と色を指定したしきい値線を追加します。複数追加できます。（Line / Bar / Scatter） |

<img src="/images/web-ui/neo-dashboard/icons/dash_add_series.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンで Y 軸をもう 1 つ追加し（最大 2 つ）、追加した軸の **Series** でその軸に描くシリーズを選択します。追加した軸のオプションは基本の Y 軸と同じです。
