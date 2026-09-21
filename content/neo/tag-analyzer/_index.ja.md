---
title: Tag Analyzer
type: docs
weight: 26
toc: true
---

Tag Analyzer を使うと、タグテーブルのデータをチャートで可視化し、分析できます。

次のような用途に利用できます。

- 複数のタグのチャートを作成します。
- 時間範囲を調整し、同期します。
- チャートを重ね合わせてデータを比較します。
- 生データの値を確認します。
- FFT で周波数を分析します。
- チャートと設定をボードに保存し、後で開き直します。

<span id="1-quickstart"></span>

## 1. 概要 {#overview}

動画と一部の画像には英語版を使用しています。ボタンやタブの名前は画面の表記に合わせています。

{{< figure
  src="/images/tag-analyzer/created-tag-analyzer-chart.png"
  link="/images/tag-analyzer/created-tag-analyzer-chart.png"
  alt="temperature タグのチャートと時間範囲ナビゲーターを表示した Tag Analyzer ボード"
>}}

### 1.1 Tag Analyzer タブを開く {#create-tag-analyzer-tab}

**+** をクリックし、**TAG ANALYZER** を選択して新しいボードを開きます。

{{< figure
  src="/images/tag-analyzer/create-tag-analyzer-tab.png?v=d14367faf6"
  link="/images/tag-analyzer/create-tag-analyzer-tab.png?v=d14367faf6"
  alt="新しいタブのメニューで、+ ボタンと TAG ANALYZER が強調表示されています。"
  caption="図 1.1: Tag Analyzer タブを開く"
>}}

### 1.2 サンプルデータを追加する（任意） {#prepare-example-data}

Tag Analyzer を試すためのサンプルデータを作成します。すでにデータがある場合は省略できます。

1. 新しいタブのメニューで **SQL** を選択し、下の SQL でテーブルを作成します。
2. 別のタブで **TQL** を選択し、下の TQL でサンプルデータを追加します。

{{< figure
  src="/images/tag-analyzer/prepare-example-data-editors.png?v=169f7f9d00"
  link="/images/tag-analyzer/prepare-example-data-editors.png?v=169f7f9d00"
  alt="+ で新しいタブを開きます。SQL でテーブルを作成し、TQL でサンプルデータを追加します。"
  caption="図 1.2: SQL エディターと TQL エディター"
>}}

**サンプルテーブルの作成（SQL タブで一度だけ実行します）**

```sql
CREATE TAG TABLE IF NOT EXISTS TAG_ANALYZER_DEMO (
    NAME VARCHAR(80) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

**サンプルテーブルへのデータ追加（TQL エディターで実行します）**

```js
FAKE(oscillator(
    freq(1/60, 10, 20),
    range('now-10m', '10m', '1s')
))
PUSHVALUE(0, 'temperature')
APPEND(table('TAG_ANALYZER_DEMO'))
```

### 1.3 最初のチャートを作成する {#create-tag-analyzer}

Tag Analyzer タブで **New Chart** をクリックし、チャート作成ダイアログを開きます。
自分のテーブルとタグを指定するか、次のサンプル設定を使用します。

1. **Chart name** に `Temperature` と入力し、**Line** を選択します。
2. サンプルデータを準備した **Database** と **User** を選択します。
   **Table** に **TAG_ANALYZER_DEMO**、**Time** に **TIME**、**Value** に **VALUE** を指定します。
3. `temperature` を入力し、**Enter** または検索ボタンで検索します。
   **Item list** のタグをクリックすると **Selected** に追加されます。集計方法は **AVG** のままにします。
4. **Apply** をクリックしてチャートを作成します。

{{< figure
  src="/images/tag-analyzer/create-tag-analyzer-chart.png?v=3355dfff00"
  link="/images/tag-analyzer/create-tag-analyzer-chart.png?v=3355dfff00"
  alt="Machbase Neo の画面全体と New Chart ダイアログ。1. 名前と Line を指定します。2. テーブル、TIME、VALUE を選択します。3. temperature を検索して選択します。4. Apply をクリックします。"
  caption="図 1.3: 最初のチャートを作成する"
>}}

### 1.4 画面構成 {#screen-overview}

チャートの準備ができたら、データを探索し、分析できます。

次の画像は Tag Analyzer の画面構成を示しています。

{{< figure
  src="/images/web-ui/tag-analyzer/controls-overview.png?v=c287c40a80"
  alt="Board Control、Panel Control、Range、Tools、Panel Editor の位置を示した画面"
  caption="図 1.4: 画面構成"
>}}

## 2. ボードの操作 {#2-board-controls}

ボードのツールバーで、共通範囲の設定、更新、保存、チャートの重ね合わせを行います。

{{< figure
  src="/images/web-ui/tag-analyzer/board-controls.png"
  alt="範囲、更新、保存、重ね合わせ、ヘルプの位置を示したボードのツールバー"
  caption="図 2: ボードの操作"
>}}

### 2.1 新しいチャートを追加する {#add-a-new-chart}

**New Chart** をクリックすると、現在のボードにチャートを追加できます。

{{< tag-analyzer-features
  id="add-chart"
  title="ボードから新しいチャートを作成する"
  caption="図 2.1: 新しいチャートを追加する"
>}}

### 2.2 ボードの共通範囲を設定する {#set-shared-ranges}

**TIME** では時間軸のチャート、**DIST** では距離軸のチャートに共通するナビゲーターの範囲を設定します。

*各パネルの範囲設定が優先されます。*

| X 軸 | From → To の例 | 意味 |
|---|---|---|
| 時間 | `first` → `last` | 作成したサンプルデータ全体です。 |
| 時間 | `last-5m` → `last` | サンプルの最後の 5 分間です。 |
| 時間 | `first` → `first+5m` | サンプルの最初の 5 分間です。 |

日時を直接入力するか、`first`、`last`、`last-5m` などの相対的な範囲を指定できます。
開始値は終了値より小さくする必要があります。

### 2.3 更新する {#refresh-and-show-all-data}

- **Refresh data:** 現在の範囲を維持して、すべてのパネルのデータを再読み込みします。
- **Refresh ranges:** データの範囲を確認し、`last-5m` などの式を含む範囲設定を再適用します。
- **Expand all panels to full data range:** 各パネルで利用可能なデータ全体を表示します。

範囲が未設定の場合、範囲の更新ではデータの中央付近が表示されます。全体を見るには全範囲表示を使用します。

### 2.4 保存して開き直す {#save-changes-or-create-a-copy}

**Save** は現在の `.taz` ファイルに保存します。**Save as** では別の名前やフォルダーを選択できます。
**Ctrl+S**（macOS では **Cmd+S**）でも保存できます。エディターでの変更は、保存する前に適用します。

`.taz` ファイルにはチャートの設定、範囲、ハイライト、注釈が保存されます。
テーブルのデータ自体はコピーされません。

<span id="save-and-reopen"></span>

ボードのタブを閉じ、File Explorer で保存したファイルをクリックすると、ボードを開き直せます。

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/save-reopen.mp4?v=f5150d7350"
  poster="/images/web-ui/tag-analyzer/save-reopen-poster.webp?v=deb53b81fa"
  alt="Tag Analyzer のボードを保存して開き直す操作"
  caption="デモ 2.4: 保存して開き直す"
>}}

### 2.5 チャートを重ね合わせる {#compare-charts-with-overlap}

Overlap Chart は複数のチャートを重ねて表示し、データのパターンを比較する機能です。
各チャートを X 軸方向に移動すると、異なる時刻に発生したピークやイベントを揃えられます。

{{< overlap-chart >}}

読み込み済みの範囲があり、X 軸の種類が同じチャートを使用します。複数の系列を含むチャートにも対応しています。

<details>
<summary>重ね合わせの位置合わせ</summary>

**Original** は元の範囲、**Altered** は位置合わせと移動後の範囲です。

各チャートの最初の描画点を 0 として揃えます。時間軸では経過時間、数値軸では相対値を表示します。
移動操作は、比較画面内でそのチャートのすべての系列に適用されます。

</details>

**Help (?)** をクリックすると、操作ガイドが開きます。

### 2.6 TAZ ファイルを削除する {#delete-a-taz-file}

**File Explorer** で `.taz` ファイルを右クリックし、**Delete** を選択して確定します。
保存したボードが削除されます。テーブルのデータは保持されます。

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/delete-taz.mp4?v=39e14d44bd"
  poster="/images/web-ui/tag-analyzer/delete-taz-poster.webp?v=bbf4098393"
  alt="File Explorer から TAZ ファイルを削除する操作"
  caption="デモ 2.6: TAZ ファイルを削除する"
>}}

## 3. パネルの操作 {#3-panel-controls}

### 3.1 範囲 {#range-and-navigation}

<span id="basic-range-control"></span>

チャートの範囲をクリックして **From/To** を設定し、**Apply** をクリックします。
ナビゲーターのドラッグや拡大・縮小でも範囲を調整できます。
サンプルデータでは `last-10m` から `last` を指定します。

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/basic-range-control.mp4?v=ad412ac8f7"
  poster="/images/web-ui/tag-analyzer/basic-range-control-poster.webp?v=9f72fa6e77"
  alt="範囲の設定、ナビゲーターの移動、拡大・縮小の操作"
  caption="デモ 3.1: 基本的な範囲操作"
>}}

{{< range-controls >}}

<details>
<summary>範囲設定の優先順位</summary>

[Panel Editor → Range](#main-range) の **Main Range (1)** は、表示範囲の設定で優先されます。
**Nav Range (2)** を個別に設定した場合は、ボードの共通範囲より優先されます。

</details>

### 3.2 ツール {#panel-control-tools}

ツールバーの機能を左から順に紹介します。

{{< figure
  src="/images/web-ui/tag-analyzer/panel-controls.png"
  alt="左から RAW、Select range、Refresh range、Panel Editor、Delete、Extra が並ぶツールバー"
  caption="図 3.2: ツール"
>}}

#### 3.2.1 RAW {#view-raw-data}

**RAW** をクリックすると、区間ごとの集計データと個々の生データを切り替えられます。
集計表示では、各系列に設定した **AVG**、**MIN**、**MAX** などの集計方法を使用します。

<details>
<summary>RAW の取得件数とサンプリング</summary>

メインチャートのサンプリングが無効の場合、RAW では **1 系列あたり最大 20,000 行**を取得します。
上限に達すると、表示範囲が取得できたデータの範囲に縮まる場合があります。
範囲を絞るか、**Data Setting → Use main chart sampling** を有効にします。

メインチャートが RAW モードでも、ナビゲーターには平均値やサンプリングしたデータが表示される場合があります。

</details>

#### 3.2.2 範囲選択と FFT {#inspect-statistics}

選択した範囲の統計値を確認したり、FFT で周波数を分析したりできます。
FFT を使用するには、**RAW モード**と**時間軸のチャート**が必要です。

<span id="analyze-frequencies-with-fft"></span>

{{< fft-demo >}}

`temperature` では **Min Hz** を **0.005**、**Max Hz** を **0.1** に設定し、**Apply values** をクリックします。
サンプルの主な周波数は約 **0.0167 Hz** です。

このサンプルを **3D** で表示する場合は、区間を **1 min** に設定します。各区間には **16 点以上**のデータが必要です。

#### 3.2.3 範囲を更新する {#refresh-this-panel}

データの範囲を確認し、設定した範囲を再適用します。

#### 3.2.4 チャートを編集する {#panel-editor-tool}

<span id="edit-a-chart"></span>

歯車ボタンをクリックして設定を編集します。**Apply** で変更を適用し、**Close** でエディターを閉じます。

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/edit-chart.mp4?v=b4e33d681f"
  poster="/images/web-ui/tag-analyzer/edit-chart-poster.webp?v=608d4edbdf"
  alt="チャートのタイトルとスタイルを変更する操作"
  caption="デモ 3.2.4: チャートを編集する"
>}}

各設定タブについては [Panel Editor](#4-panel-settings) を参照してください。

#### 3.2.5 チャートを削除する {#delete-panel-tool}

<span id="delete-a-chart"></span>

**Delete panel**（ごみ箱）をクリックして確定します。

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/delete-chart.mp4?v=66bf8bb25c"
  poster="/images/web-ui/tag-analyzer/delete-chart-poster.webp?v=cb5b0e6c96"
  alt="ボードからチャートを削除する操作"
  caption="デモ 3.2.5: チャートを削除する"
>}}

チャートは `.taz` ボード内の 1 つの項目です。削除しても `.taz` ファイルとテーブルのデータは保持されます。

#### 3.2.6 ハイライト {#highlight}

<span id="add-highlights-and-annotations"></span>

**Extra → Highlight** でチャートの範囲を強調し、ラベルを付けられます。

{{< markup-guide id="highlight" >}}

#### 3.2.7 注釈 {#annotation}

**Extra → Annotation** で系列内の任意の位置にメモを追加できます。

{{< markup-guide id="annotation" >}}

ハイライトと注釈を保持するには、ボードを保存します。

#### 3.2.8 Extra {#extra-panel-tools}

{{< figure
  src="/images/web-ui/tag-analyzer/panel-extra-tools.png"
  alt="Extra メニュー"
  caption="図 3.2.8: Extra"
>}}

- **Set global range:** このパネルの範囲を、同じ種類の X 軸を持つパネルに適用します。
- **Reload data:** 現在の範囲を維持して、データを再読み込みします。
- **Expand to full data range:** このパネルで利用可能なデータ全体を表示します。

<span id="handy-tools"></span>

{{< tag-analyzer-video
  src="/images/web-ui/tag-analyzer/handy-tools.mp4?v=96adddb1ff"
  poster="/images/web-ui/tag-analyzer/handy-tools-poster.webp?v=770a824754"
  alt="temperature のデータを再読み込みし、全範囲を表示する操作"
  caption="デモ 3.2.8: データの更新と全範囲表示"
>}}

## 4. Panel Editor {#4-panel-settings}

チャートの歯車ボタンをクリックします。**Apply** で変更を適用し、**Close** でエディターを閉じます。

**変更を適用した後、`.taz` ボードを保存して設定を保持します。**

### 4.1 General タブ {#general}

{{< panel-editor-tab id="general" caption="図 4.1: General タブ" >}}

### 4.2 Data タブ {#data}

{{< panel-editor-tab id="data" caption="図 4.2: Data タブ" >}}

### 4.3 Data Setting タブ {#data-setting}

{{< panel-editor-tab id="data-setting" caption="図 4.3: Data Setting タブ" >}}

### 4.4 Axes タブ {#axes}

{{< panel-editor-tab id="axes" caption="図 4.4: Axes タブ" >}}

### 4.5 Display タブ {#display}

{{< panel-editor-tab id="display" caption="図 4.5: Display タブ" >}}

### 4.6 Range タブ {#main-range}

{{< panel-editor-tab id="main-range" caption="図 4.6: Range タブ" >}}
