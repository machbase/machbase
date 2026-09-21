---
title: Tag Analyzer
type: docs
weight: 26
toc: true
---

Tag Analyzerでタグデータを可視化し、比較・分析できます。

## 1. クイックスタート

データが入ったタグテーブルを用意します。

### 1.1 Tag Analyzerの作成 {#create-tag-analyzer}

**+ → Tag Analyzer → New Chart**を開きます。設定、タグ、集計方法を選び、**Apply**をクリックします。

{{< figure
  src="/images/web-ui/tag-analyzer/create-chart-ja.gif"
  alt="Tag Analyzerでチャートを作成"
  caption="デモ 1.1: チャートの作成"
>}}

### 1.2 画面構成 {#screen-overview}

**ボード**（Board）はチャートをまとめる画面です。UIではチャートを**パネル**（Panel）と呼びます。
画像の番号は、以下のセクション番号に対応しています。

{{< figure
  src="/images/web-ui/tag-analyzer/controls-overview.png"
  alt="Board（紫の外枠）、2. ボードコントロール（紫）、3. パネルコントロールと3.1 範囲（コーラルオレンジ）、3.2 ツール（水色、Extraを表示）、4. パネルエディター（黄）、凡例（グレー）"
  caption="図 1.2: 画面構成"
>}}

### 1.3 基本的な範囲操作 {#basic-range-control}

チャート上部の範囲をクリックし、**From/To**を設定して**Apply**をクリックします。
ナビゲーターのドラッグや拡大・縮小で表示範囲を調整できます。

{{< figure
  src="/images/web-ui/tag-analyzer/basic-range-control-ja.gif"
  alt="範囲の設定、ナビゲーターの移動、拡大"
  caption="デモ 1.3: 基本的な範囲操作"
>}}

### 1.4 便利なツール {#handy-tools}

- **Refresh data:** 現在の範囲を保ったままデータを再読み込みします。
- **Extra → Expand to full data range:** データの全範囲を表示します。

{{< figure
  src="/images/web-ui/tag-analyzer/handy-tools-ja.gif"
  alt="データの更新、全範囲の表示、系列の表示切り替え"
  caption="デモ 1.4: 便利なツール"
>}}

### 1.5 チャートの編集 {#edit-a-chart}

歯車ボタンで設定を開きます。**Apply**で変更を適用し、**Close**でエディターを閉じます。

{{< figure
  src="/images/web-ui/tag-analyzer/edit-chart-ja.gif"
  alt="チャートのタイトルと表示スタイルを変更"
  caption="デモ 1.5: チャートの編集"
>}}

### 1.6 保存と再表示 {#save-and-reopen}

**Save**で`.taz`ファイルに保存します。File Explorerから開くと、ボードを再表示できます。

{{< figure
  src="/images/web-ui/tag-analyzer/save-reopen-ja.gif"
  alt="Tag Analyzerのボードを保存して再度開く"
  caption="デモ 1.6: 保存と再表示"
>}}

### 1.7 チャートの削除 {#delete-a-chart}

**Delete panel**（ごみ箱）をクリックし、削除を確定します。

{{< figure
  src="/images/web-ui/tag-analyzer/delete-chart-ja.gif"
  alt="ボードからチャートを削除"
  caption="デモ 1.7: チャートの削除"
>}}

チャートは`.taz`ボード内の1つの項目です。削除しても、`.taz`ファイルとテーブルのデータは残ります。

### 1.8 TAZファイルの削除 {#delete-a-taz-file}

**File Explorer**で`.taz`ファイルを右クリックし、**Delete**を選んで削除を確定します。
保存したボードが削除されます。テーブルのデータは残ります。

{{< figure
  src="/images/web-ui/tag-analyzer/delete-taz-ja.gif"
  alt="File ExplorerからTAZファイルを削除"
  caption="デモ 1.8: TAZファイルの削除"
>}}

## 2. ボードコントロール {#2-board-controls}

上部のツールバーで、共有範囲、更新、保存、重ね合わせを操作します。

{{< figure
  src="/images/web-ui/tag-analyzer/board-controls.png"
  alt="ボードのツールバー: 範囲、更新、保存、重ね合わせ、ヘルプを紫で表示"
  caption="図 2: ボードコントロール"
>}}

### 2.1 ボードの範囲設定 {#set-shared-ranges}

**TIME**または**DIST**で、時間軸・数値軸のパネルに共有するナビゲーター範囲を設定します。
どちらも**From/To**を使います。パネル独自の範囲設定が優先されます。

<details>
<summary>範囲の入力例</summary>

| X軸 | From → To | 意味 |
|---|---|---|
| 時間 | `now-1h` → `now` | 現在時刻から過去1時間。 |
| 時間 | `last-1h` → `last` | 保存済みの最新データを終点とする1時間。 |
| 時間 | `first` → `first+1h` | 保存済みデータの先頭から1時間。 |
| 数値 | `0` → `100` | X軸の値が0から100の範囲。 |

日時の直接入力やプリセット範囲の選択もできます。
数値範囲にはスライダーとプリセットがあります。開始値は終了値より小さくしてください。

</details>

### 2.2 更新 {#refresh-and-show-all-data}

- **Refresh data:** 各パネルの現在の範囲を保ったまま、全パネルを再読み込みします。
- **Refresh ranges:** データの範囲を再確認し、`last-1h`などの式を含む範囲設定を再適用します。
- **Expand all panels to full data range:** 各パネルでデータの全範囲を表示します。

範囲が未設定の場合、範囲の更新では中央付近の区間が表示されます。全データを見るには全範囲表示ボタンを使います。

### 2.3 保存 {#save-changes-or-create-a-copy}

**Save**は現在の`.taz`ファイルに保存し、**Save as**は別の名前やフォルダーに保存します。
**Ctrl+S**（macOSでは**Cmd+S**）でも保存できます。エディターの変更は保存前に適用してください。

`.taz`ファイルにはチャート設定、範囲、ハイライト、注釈が保存されます。テーブルのデータはコピーされません。

### 2.4 チャートの重ね合わせ {#compare-charts-with-overlap}

1. 各チャートのタイトル横のチェックボックスを選択します。
2. ボードの**Overlap chart**をクリックします。
3. 移動量を設定します。時間軸のチャートでは単位も選びます。
4. 矢印でチャートの位置を合わせます。

{{< figure
  src="/images/web-ui/tag-analyzer/compare-charts-overlap-ja.gif?v=b466239541"
  alt="チャートを選択し、10日ずつ3回移動して位置を合わせる"
  caption="デモ 2.4: チャートの重ね合わせ"
>}}

{{< figure
  src="/images/web-ui/tag-analyzer/overlap-controls.png"
  alt="重ね合わせ画面: 更新、凡例、拡大・移動、元の範囲と変更後の範囲、移動操作、閉じるボタン"
  caption="図 2.4: チャートの重ね合わせ"
>}}

各チャートに読み込み済みの範囲があり、X軸の種類が同じである必要があります。複数系列のチャートにも対応しています。

<details>
<summary>位置合わせの仕組み</summary>

**Original**は元の範囲、**Altered**は位置合わせと移動後の範囲です。

各チャートの最初の描画点を0として揃えます。時間軸は経過時間、数値軸は相対値で表示されます。
移動すると、比較画面内でそのチャートの全系列が一緒に動きます。

</details>

**Help**（?）で操作ガイドを開きます。

## 3. パネルコントロール {#3-panel-controls}

### 3.1 範囲 {#range-and-navigation}

#### 3.1.1 メインチャートの操作 {#main-panel-range-controls}

{{< figure
  src="/images/web-ui/tag-analyzer/range-main-panel.png"
  alt="メインチャートの操作: 表示範囲、ドラッグ、移動矢印、拡大・縮小、Focus"
  caption="図 3.1.1: メインチャートの操作"
>}}

- **表示範囲:** チャート上部の範囲をクリックし、**From/To**を設定します。
- **移動・拡大:** 左右の矢印と拡大・縮小ボタンを使います。ドラッグで拡大するには、
  **General → Use Zoom when dragging**を有効にします。
- **Focus:** 表示範囲をナビゲーター範囲に設定し、その中央を拡大します。

#### 3.1.2 ナビバーの操作 {#navigator-range-controls}

{{< figure
  src="/images/web-ui/tag-analyzer/range-navigator.png"
  alt="ナビバーの操作: 選択範囲、サイズ変更ハンドル、移動矢印、範囲入力"
  caption="図 3.1.2: ナビバーの操作"
>}}

- **選択範囲:** ドラッグでメインチャートの表示範囲を移動し、両端のドラッグで幅を変更します。
- **左右の矢印:** ナビゲーターの範囲を前後に移動します。
- **ナビゲーター下部の範囲:** どちらかの端点をクリックし、**From/To**を設定します。

<details>
<summary>設定済みの範囲</summary>

**Panel Editor → Range**の**Main Range**は、表示範囲に優先して使われます。
個別に設定した**Nav Range**は、ボードの範囲より優先されます。
範囲選択やハイライトのツールが有効な間、ドラッグはそれぞれの操作に使われます。

</details>

### 3.2 ツール {#panel-control-tools}

ツールバーの左から順に説明します。

{{< figure
  src="/images/web-ui/tag-analyzer/panel-controls.png"
  alt="パネルのツール: 左からRAW、範囲選択、範囲更新、パネルエディター、削除、Extra"
  caption="図 3.2: ツール"
>}}

#### 3.2.1 RAW {#view-raw-data}

**RAW**で、区間ごとの集計表示と個々のデータ行の表示を切り替えます。
集計モードでは、各系列の**AVG**、**MIN**、**MAX**などの集計方法を使います。

<details>
<summary>RAWの上限とサンプリング</summary>

メインチャートのサンプリングを使わない場合、RAWの取得上限は**1系列あたり20,000行**です。
上限に達すると、表示範囲が取得できたデータに合わせて狭まることがあります。
範囲を絞るか、**Data Setting → Use main chart sampling**を有効にしてください。

メインチャートがRAWモードでも、ナビゲーターには平均値やサンプリングされたデータが表示される場合があります。

</details>

#### 3.2.2 範囲選択 {#inspect-statistics}

**Select data range**をクリックし、メインチャート上をドラッグします。
ポップアップに選択範囲内の各系列の最小値、最大値、平均値が表示されます。
統計には読み込み済みの点を使うため、集計モードでは集計後の値を対象にします。

{{< figure
  src="/images/web-ui/tag-analyzer/select-range.png"
  alt="Select Rangeボタン、選択範囲、最小値・最大値・平均値の統計"
  caption="図 3.2.2: 範囲選択"
>}}

<span id="analyze-frequencies-with-fft"></span>

**FFT**

FFTは**RAWモードの時間軸チャート**で使えます。
範囲を選び、**Open FFT chart**をクリックして系列を選択します。

{{< figure
  src="/images/web-ui/tag-analyzer/fft-analysis-ja.gif?v=af51e90883"
  alt="RAWモードで範囲を選択してFFTスペクトルを開く"
  caption="デモ 3.2.2: FFT"
>}}

<details>
<summary>FFTの設定</summary>

- **2D:** 周波数と振幅を表示します。
- **3D:** 時間に伴う周波数の変化を表示します。区間と単位を設定します。
- **Min Hz / Max Hz:** 周波数範囲を制限します。両方を`0`にすると制限しません。
- **Apply values:** 入力した設定でチャートを再生成します。

3D FFTには1区間あたり16サンプル以上が必要です。全区間で不足する場合は、区間を広げるか選択するデータを増やしてください。

</details>

#### 3.2.3 範囲更新 {#refresh-this-panel}

データの範囲を再確認し、設定済みの範囲を再適用します。

#### 3.2.4 パネルエディター {#panel-editor-tool}

設定タブについては[パネルエディター](#4-panel-settings)を参照してください。

#### 3.2.5 削除 {#delete-panel-tool}

[チャートの削除](#delete-a-chart)を参照してください。

#### 3.2.6 Extra {#extra-panel-tools}

{{< figure
  src="/images/web-ui/tag-analyzer/panel-extra-tools.png"
  alt="Extraメニュー"
  caption="図 3.2.6: Extra"
>}}

<span id="add-highlights-and-annotations"></span>

- **Highlight:** 範囲をドラッグで選び、ラベルを入力して**Apply**をクリックします。
- **Annotation:** チャートをクリックし、系列を選び、注釈を入力して**Apply**をクリックします。
- **Set global range:** このパネルの範囲を、同じX軸の種類を持つパネルにコピーします。
- **Reload data:** 現在の範囲を保ったままデータを再読み込みします。
- **Expand to full data range:** このパネルでデータの全範囲を表示します。

描画ツールをオフにして既存のラベルをクリックすると、編集・削除できます。
ハイライトと注釈を残すには、ボードを保存してください。

## 4. パネルエディター {#4-panel-settings}

チャートの歯車ボタンをクリックします。**Apply**で変更を適用し、**Close**でエディターを閉じます。

**変更を適用した後、`.taz`ボードを保存してください。**

### 4.1 General {#general}

{{< figure
  src="/images/web-ui/tag-analyzer/editor-general.png"
  alt="パネルエディター: Generalタブ"
  caption="図 4.1: General"
>}}

- **Chart title:** パネル名を変更します。
- **Use Zoom when dragging:** ドラッグで選択した範囲を拡大します。オフにすると表示範囲をドラッグで移動できます。
- **Order raw data by time:** RAWの点をX軸の値で並べ替えてから描画します。
- **Normalize values:** 現在は右Y軸の自動範囲を**0–100**に設定します。描画する値自体は変換しません。
- **Save current visible range in TAZ:** メインチャートとナビゲーターの現在の表示範囲をボードに保存します。
  オフの場合、再度開くと設定済みの範囲を使います。

### 4.2 Data {#data}

{{< figure
  src="/images/web-ui/tag-analyzer/editor-data.png"
  alt="パネルエディター: Dataタブ"
  caption="図 4.2: Data"
>}}

- **Add new series:** データベース、テーブル、X軸と値の列、タグを選びます。
- **Calculation mode:** **AVG**、**MIN**、**MAX**、**SUM**など、区間ごとの集計方法を選びます。
  同じタグを2回追加すると、異なる集計方法を比較できます。
- **Alias / Color:** チャートと凡例に表示する系列名と色を設定します。
- **×:** パネルから系列を削除します。少なくとも1つの系列が必要です。

### 4.3 Data Setting {#data-setting}

{{< figure
  src="/images/web-ui/tag-analyzer/editor-data-setting.png"
  alt="パネルエディター: Data Settingタブ"
  caption="図 4.3: Data Setting"
>}}

- **Main Chart / Nav Bar Data Density:** 各チャートの1ピクセルあたりの点数を設定します。
  高くすると、より詳細なデータを取得します。両方を空欄にすると自動調整します。
- **Use main chart sampling:** 入力したサンプリング値でRAWデータを取得します。
  オフの場合、メインチャートは通常のRAWクエリを使います。
- **Use navigation sampling:** ナビゲーターにサンプリングしたRAWデータを使います。
  オフの場合、時間軸のナビゲーターには区間ごとの平均値を表示します。

### 4.4 Axes {#axes}

{{< figure
  src="/images/web-ui/tag-analyzer/editor-axes.png"
  alt="パネルエディター: Axesタブ"
  caption="図 4.4: Axes"
>}}

- **Start the Y-axis at zero / Show tick marks:** Y軸の範囲に0を含め、軸のグリッド線を表示します。
- **Custom scale:** Y軸の最小値と最大値を設定します。空欄は**Auto**です。
  RAWチャートには別のスケール設定があります。
- **LCL / UCL:** 入力した値に下側・上側管理限界線を表示します。
- **Right Y-axis:** 独立したスケールを有効にし、使用する系列を選びます。
  コピーボタンで左Y軸の設定をコピーできます。

### 4.5 Display {#display}

{{< figure
  src="/images/web-ui/tag-analyzer/editor-display.png"
  alt="パネルエディター: Displayタブ"
  caption="図 4.5: Display"
>}}

- **Preset:** **Line**、**Scatter**、**Zone**（面）を選びます。
  点や線のスタイルを変更すると**Custom**に切り替わります。
- **Display data points / Point Radius:** データ点のマーカーを表示し、サイズを設定します。
- **Display legend / Connect gaps:** 凡例を表示し、欠損部分を線でつなぎます。
- **Opacity Of Fill Area / Line Thickness:** 塗りつぶしの不透明度と線の太さを調整します。

### 4.6 Range {#main-range}

{{< figure
  src="/images/web-ui/tag-analyzer/editor-range.png"
  alt="パネルエディター: Rangeタブ"
  caption="図 4.6: Range"
>}}

- **Nav Range:** ナビゲーターに表示する範囲を設定します。
- **Main Range:** メインチャートに最初に表示する範囲を設定します。
- **From / To:** 時間または数値の開始・終了値を入力するか、プリセット範囲を選びます。
  **Clear**で個別の範囲設定を解除します。
