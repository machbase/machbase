---
title: ダッシュボードの操作
type: docs
weight: 10
toc: true
---

## 画面構成

{{< media slug="neo-dashboard/statz-board" width="600" >}}

ダッシュボードはデータを表示する複数のチャートで構成されます。各パネルは任意の位置とサイズで配置できます。

- 左上: ダッシュボードのタイトル。クリックしてその場で変更できます。
- 右上: ダッシュボード全体の操作領域。
- 中央: チャートパネルを配置する領域。

## チャートの追加

操作領域の<img src="/images/web-ui/neo-dashboard/icons/dash_new_panel.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンをクリックするとチャート設定画面が開きます。設定後に`Save`をクリックすると、パネルを追加します。  
※ 詳細は「チャート設定」を参照してください。

{{< media slug="neo-dashboard/add-chart" width="600" >}}

パネルが 1 つもない新規ダッシュボードでは、画面中央の<img src="/images/web-ui/neo-dashboard/icons/dash_create_panel.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンからも同じ画面が開きます。  
新しいチャートはデフォルトサイズで配置されます。右下をドラッグしてサイズを、上部をドラッグして位置を変更できます。保存時のサイズより小さくすることはできません。

## 操作ボタン

{{< media slug="neo-dashboard/control-buttons" width="600" >}}

※ 未保存のダッシュボードには以下の 8 個のボタンが表示されます。保存すると表示専用モードのリンクを共有するボタンが追加され、変数を定義するとタイトル横に変数の値と変数アイコンが表示されます。

1. <img src="/images/web-ui/neo-dashboard/icons/dash_new_panel.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> チャートを追加します。
2. <img src="/images/web-ui/neo-dashboard/icons/dash_refresh.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> データを再取得して更新します。
3. `TIME`チップ: 検索に使用する時間範囲を設定します。
4. `DIST`チップ: 距離で検索するパネルの距離範囲を設定します。
5. <img src="/images/web-ui/neo-dashboard/icons/dash_auto_refresh.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 自動更新間隔を設定します。
6. <img src="/images/web-ui/neo-dashboard/icons/dash_save.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> ダッシュボードを保存します（拡張子 `.dsh`）。新規の場合はファイル名と保存フォルダーを指定できます。
7. <img src="/images/web-ui/neo-dashboard/icons/dash_save_as.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 別名で保存します。
8. <img src="/images/web-ui/neo-dashboard/icons/dash_variable_config.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> 変数を設定します。{{< neo_since ver="8.0.46" />}}

## 時間範囲（TIME）

チップをクリックすると範囲設定ダイアログが開きます。

{{< media slug="neo-dashboard/board-time-range" width="420" >}}

- `now` は現在時刻、`last` はデータベースに保存された最後の時刻です。`h`/`m`/`s` は時・分・秒で、例えば `now-3h` は現在時刻の 3 時間前です。
- 「Quick Range」の項目をクリックすると From/To を自動設定します。右側の一覧（`... of data`）はデータの最後の時刻を基準にします。
- チップ左右の `<`、`>` は範囲を 50% ずつ移動します。`now` または `last` を使用している場合は絶対時刻に変換します。

## 距離範囲（Distance）

時間ではなく距離で検索するパネルに適用します。同じダイアログの Distance タブで設定します。

{{< media slug="neo-dashboard/board-dist-range" width="420" >}}

- **対象**: 基準列が DATETIME ではなく数値（距離・走行距離など）のタグテーブルを使うパネルです。このようなテーブルは基準列を `BASE DISTANCE` と宣言して作成します（例: `CREATE TAG TABLE dist_data (NAME VARCHAR(80) PRIMARY KEY, DIST DOUBLE BASE DISTANCE, VALUE DOUBLE SUMMARIZED)`）。ダッシュボードにそのようなパネルがない場合、データ範囲がわからないため `0 – 0` と表示されます。
- **データ範囲（min/max）**: ダイアログを開くとパネルのデータの最小値・最大値を読み込み、スライダーの両端として使用します。スライダーをドラッグするか FROM/TO 入力欄に値を入力して範囲を指定すると、ダイアログ上部に選択した範囲（例: `0 – 1,237.5`）とその長さが表示されます。
- **アンカー式**: 数値の代わりに `first`、`last`、`first+1000`、`last-1000` のようにデータの端を基準に入力できます。時間軸の `last-1h ~ last` と同様に、データが増えても範囲がデータの端に追従します。適用するとチップにも `last-1000 ~ last` のように式がそのまま表示されます。
- **Quick windows**: First 10%、First 25%、First 50%、Last 50%、Last 25%、Full から選び、データ範囲の割合で一度に指定します。押すと FROM/TO がアンカー式で埋まります（例: データ範囲が 0～4,950 のとき First 25% は `first` ~ `first+1237.5`）。
- **`Reset to default`**: 押すとすぐに（Apply なしで）ダッシュボードの距離範囲を消去し、ダイアログを閉じます。チップは点線の空のチップに戻り、パネルはデータ全体の範囲を表示します。チャート設定の Distance タブで独自の範囲を指定したパネルは、その範囲を使い続けます。

## 自動更新

{{< media slug="neo-dashboard/board-autorefresh" width="600" >}}

Off、3 秒、5 秒、10 秒、30 秒、1 分、5 分、10 分、1 時間から選択します。設定すると、その周期でダッシュボード全体を再検索します。パネルごとに異なる周期を使う場合は「チャートパネル」のパネル別自動更新を参照してください。

## 共有

{{< media slug="neo-dashboard/share" width="600" >}}

共有ボタンは保存済みのダッシュボードにのみ表示されます。クリックすると Share ダイアログが開きます。

{{< media slug="neo-dashboard/share-modal" width="600" >}}

- **SNS ボタン**: Facebook、X、メール、WhatsApp でリンクを送信します。
- **リンク**: 表示専用モードのアドレスです。形式は `http://<サーバーアドレス>/web/ui/board/<フォルダーパス>/<ファイル名（拡張子を除く）>` で、右のボタンでコピーします。
- **iframe / embed**: 他の Web ページに埋め込むためのコードです。タブを選び、右のボタンでコピーします。

表示専用モードにはログインが必要です。パネルは編集できず、時間範囲（TIME）・距離範囲（Distance）と自動更新の変更、更新のみ行えます。

## 変数

{{< neo_since ver="8.0.46" />}}

{{< media slug="neo-dashboard/board-variable-config" width="600" >}}

ダッシュボードで使用する変数を表示・追加・編集・削除できます。`Export`、`Import` で変数設定を入出力でき、形式は `LABEL,VARIABLE NAME,VALUES` です。

[+ New variable] をクリックすると変数を定義します。

{{< media slug="neo-dashboard/variable-new" width="600" >}}

- **Label**: 変数入力フィールドに表示するタイトル。
- **Variable Name**: チャート設定で使用する変数名。波括弧なしで `tag` と入力しても `{{tag}}` として保存され、チャート設定では `{{tag}}` の形式で使用します。
- **Value**: 変数入力フィールドで選択できる項目。右の<img src="/images/web-ui/neo-dashboard/icons/dash_variable_add_value.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンで項目を追加します。

変数を定義すると、ダッシュボードのタイトル横に変数の現在値が表示されます。値をクリックすると左側に変数パネルが開き、別の値を選んで`Apply`を押すとチャートに反映されます。タイトル横のアイコンを押すと、すべての変数をまとめて表示します。

{{< media slug="neo-dashboard/variables" width="600" >}}
