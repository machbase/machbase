---
title: チャートパネル
type: docs
weight: 20
toc: true
---

## パネルの操作

- **移動**: パネル上部（ヘッダー）をドラッグします。
- **サイズ変更**: 右下の角をドラッグします。保存時のサイズより小さくすることはできません。
- **凡例の切り替え**: 凡例をクリックすると、そのシリーズを表示・非表示にします。
- **自動更新の表示**: パネルが独自の更新周期を持つ場合、ヘッダーに残り時間を示すリングが表示され、そこから周期の変更や停止ができます。

## パネルメニュー

パネル右上の<img src="/images/web-ui/neo-dashboard/icons/dash_panel_menu.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンをクリックするとメニューが開きます。

{{< media slug="neo-dashboard/panel-menu" width="600" >}}

- **Setting**: チャート設定を編集します（「チャート設定」参照）。
- **Duplicate**: チャートを複製します。複製したパネルは元のすぐ下に配置されます。
- **Show Taganalyzer**: このチャートの内容を Tag Analyzer で開きます。{{< neo_since ver="8.0.49" />}} TAG テーブルを使用するパネルにのみ表示されます。
- **Download data**: パネルが取得したデータを CSV ファイルとしてダウンロードします。
- **Delete**: パネルを削除します。
- **Save to tql**: パネルが内部で使用する TQL をファイルに保存します。ダイアログでファイル名と Output（`CHART` / `DATA(JSON)` / `DATA(CSV)`）を指定し、特定のシリーズだけを選択することもできます。Tql chart、Geomap、Text、Video タイプには表示されません。

チャートタイプによって次の項目も表示されます。

- **Use zoom control**（Geomap）: 地図のズームコントロールを直接オン・オフします。
- **Synchronization**、**Child board**、**Fullscreen**（Video）: 「Video パネル」を参照してください。

## パネル単位の時間・距離範囲

### Time タブ

チャート設定画面の **Time** タブで、そのパネルだけの検索範囲と更新周期を指定できます。

{{< media slug="neo-dashboard/panel-time-tab" width="600" >}}

- **Refresh**: このパネルだけの自動更新周期です。設定するとパネルヘッダーにカウントダウンのリングが表示されます。
- **From / To**: ダッシュボード全体の範囲の代わりに使用する時間範囲です。
- **Quick Range**: よく使う範囲をワンクリックで指定します。

指定しない場合、パネルはダッシュボードの時間範囲と更新設定に従います。

### Distance タブ

距離で検索するパネルには、Time タブの代わりに **Distance** タブが表示されます。

{{< media slug="neo-dashboard/panel-distance-tab" width="600" >}}

- **Refresh**: このパネルだけの自動更新周期です。
- **範囲表示とバッジ**: このパネル独自の範囲を指定すると `Panel` バッジとともにその範囲が表示されます。指定しない場合は `Board` バッジとともにデータ全体の範囲が淡く表示され、パネルはダッシュボードの距離範囲に従います。
- **スライダー・FROM / TO**: 範囲を指定します。`first`、`last-1000` のようなアンカー式も使用できます。
- **Quick windows**: First 10%、First 25%、First 50%、Last 50%、Last 25%、Full から選び、一度に指定します。
- **Clear**: このパネル独自の範囲を消去し、再びダッシュボードの範囲に従わせます。パネル独自の範囲があるときだけ押せます。

独自の範囲を指定したパネルは、ダッシュボードの距離範囲を変更したり `Reset to default` で初期化したりしても、その範囲を使い続けます。
