---
title: Tag Analyzer
type: docs
weight: 26
toc: true
---

## 概要
Tag Analyzer は、TAG テーブルの Rollup を使用してデータをチャートで検索・分析する機能です。
複数のチャートから成るダッシュボードで、各行が 1 つのチャートに対応します。

### 使用できるテーブル
Tag Analyzer の使用条件は次のとおりです。
- TAG テーブルのみ使用できます。
- 検索を高速化するには、Rollup テーブルを事前に作成してください。
  X 軸の間隔は検索する時間範囲から自動的に決まるため、1 秒・1 分・1 時間の基本 Rollup を推奨します。

TAG テーブルと Rollup テーブルの作成例:
```sql
CREATE TAG TABLE tag (NAME VARCHAR(80) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);

CREATE ROLLUP _tag_rollup_sec FROM tag INTERVAL 1 SEC;
CREATE ROLLUP _tag_rollup_min FROM _tag_rollup_sec INTERVAL 1 MIN;
CREATE ROLLUP _tag_rollup_hour FROM _tag_rollup_min INTERVAL 1 HOUR;
```
TAG テーブルの詳細は [TAG テーブル](/neo/sql/tag-table/) を参照してください。

## ダッシュボード
### 画面構成

{{< figure src="/images/web-ui/taz_dashboard_screen.jpg" width="600" >}}

ダッシュボードには、データを表示するチャートが行単位で並びます。各行は 1 つのチャートです。
1. ダッシュボード全体の操作領域。適用中の時間範囲も確認できます。
2. チャートの表示パネル。新しいチャートは既存のチャートの下に追加します。
3. チャートを追加するボタン。常に最下行に表示します。

### チャートの追加
ダッシュボード下部の [+] をクリックすると、チャートを作成できます。

{{< figure src="/images/web-ui/taz_new_chart.jpg" width="300" >}}

1. テーブルの選択
   TAG テーブルだけを一覧に表示します。
2. タグのフィルター
   入力した値を含むタグだけを表示します。
3. 使用可能なタグ
   一覧をページ単位で表示し、下部にページ移動ボタンを表示します。
4. 選択したタグ
   選択済みのタグを表示し、**Calc. mode** を変更できます。同じタグでも Calc. mode が異なれば複数選択できます。*1)
   下部に使用可能なタグ数と選択したタグ数を表示します。
5. チャートタイプの選択
   エリア・ポイント・折れ線チャートを選択できます。外観はチャート設定の Display で変更できます。

*1) **Calc. mode** は、STAT モードで使用する集計関数（avg、min、max、sum、count など）です。

### ダッシュボードの操作
上部のボタンでダッシュボードを操作します。

#### 時間範囲
ダッシュボードに適用中の時間範囲を表示します。From/To に直接値を入力するか、現在時刻に連動させます（now: 現在時刻、h: 時、m: 分、s: 秒）。
例: `now-3h` は現在時刻の 3 時間前です。

#### 操作ボタン

{{< figure src="/images/web-ui/taz_control_dashboard.jpg" width="400" >}}

1. データを再取得してチャートを更新します。時間範囲とスライダーの選択範囲は保持します。
2. データを再取得してチャートを更新し、時間範囲とスライダーの選択範囲を初期設定に戻します。
3. ダッシュボードを拡張子 .taz で保存します。
4. 別名で保存します。
5. Overlap Chart（重ね合わせ）を実行します。詳細は「Overlap Chart」を参照してください。
6. 検索時間範囲を設定します。個別チャートに範囲を設定していなければ、ダッシュボード全体に適用します。
   {{< figure src="/images/web-ui/taz_time_range.jpg" width="300" >}}
   - `now` は現在時刻、`last` は保存データの最後の時刻を表します。
   - Quick Range をクリックすると、その範囲を From/To に設定します。

#### Overlap Chart
複数のチャートを 1 つの画面に重ねて比較します。
1. 比較するチャートのタイトルをクリックします。選択すると枠が強調表示されます。
   {{< figure src="/images/web-ui/taz_overlap_select.jpg" width="600" >}}
   - 単一シリーズのチャートだけを使用できます。
   - 最初に選択したチャートの時間範囲を適用します。そのチャートのタイトルの前にアイコンを表示します。
2. Overlap Chart ボタンをクリックすると、選択したチャートを 1 つにまとめます。
   {{< figure src="/images/web-ui/taz_overlap_view.jpg" width="600" >}}
   タグごとに検索時間範囲を細かく調整して比較できます。

## チャート
### 画面構成

{{< figure src="/images/web-ui/taz_chart_screen.jpg" width="600" >}}

チャート上部に時間範囲、X 軸の間隔、操作ボタンを、下部にスライダーと凡例を表示します。
1. 現在表示している時間範囲。スライダーでダッシュボードの時間範囲内の一部を選択し、詳細を検索できます。Interval は X 軸の目盛り間隔です。
2. チャートの操作ボタン。
   {{< figure src="/images/web-ui/taz_chart_functions.jpg" width="300" >}}
   a. データを再取得して更新します。
   b. チャートを再描画し、時間範囲とスライダーの選択範囲を初期値に戻します。
   c. チャート設定を開きます（「チャート設定」参照）。
   d. チャートを削除します。
   e. RAW Data Mode に切り替えます。
   f. Stat Query を選択してチャート上をドラッグすると統計を検索できます。FFT Chart もここから使用します。
   - **RAW Data Mode** は Calc mode を適用せず、保存された生データを表示します。
     Pixels between tick marks から計算した件数を超えるデータを選択すると、時間範囲とスライダーの選択範囲を調整します。
3. チャートの表示領域。
4. スライダーで選択した検索範囲。`<` と `>` で選択範囲を 50% ずつ移動できます。
5. スライダーと選択範囲を操作します。
   {{< figure src="/images/web-ui/taz_chart_slidebar.jpg" width="300" >}}
   a. 選択範囲の両側を 12.5%（x2）または 25%（x4）ずつ拡張します。チャートの時間範囲とスライダーバーが大きくなります。
   b. 選択範囲の両側を 12.5%（x2）または 25%（x4）ずつ縮小します。チャートの時間範囲とスライダーバーが小さくなります。
   c. チャートの時間範囲をスライダーの全時間範囲に合わせ、スライダーの中央に全長の 50% の選択範囲を配置します。データを詳しく見る場合に使用します。
6. スライダーの移動・サイズ変更で、チャートに表示する検索範囲を設定します。
7. 凡例にデータシリーズを表示します。クリックで表示・非表示を切り替えます。

### FFT Chart
選択範囲の統計を検索すると FFT Chart ボタンが有効になり、その範囲を周波数領域に変換して確認できます。

{{< figure src="/images/web-ui/taz_fft_select.jpg" width="600" >}}

統計を検索した後に FFT Chart ボタンを使用できます。

{{< figure src="/images/web-ui/taz_fft_view.jpg" width="600" >}}

設定手順:
1. FFT チャートで確認するタグを選択します。
2. 解析する周波数（Hz）の範囲を指定します。0 は無制限です。
3. 2D または 3D を選択します。3D には時間軸を追加します。
4. 指定した条件で FFT チャートを生成します。

### チャート設定
現在のチャート設定を変更します。

{{< figure src="/images/web-ui/taz_setting_screen.jpg" width="600" >}}

1. 設定対象のチャート。[Apply] で変更結果をすぐに確認できます。
2. 設定項目のタブ。
   **General**: 一般設定
   **Data**: 使用するタグ
   **Axes**: X 軸・Y 軸
   **Display**: 表示形式
   **Time range**: このチャート専用の時間範囲
3. 選択した項目の値を変更する領域。
4. ボタン。
   **Apply**: 変更を適用し、設定画面を開いたままにします。Cancel で取り消せます。
   **Ok**: 設定画面を閉じます。Apply で反映した変更だけを保持します。
   **Cancel**: 変更を取り消して設定画面を閉じます。

#### General
チャートの基本設定を変更します。  
{{< figure src="/images/web-ui/taz_setting_general.jpg" width="600" >}}
| 項目                     | 説明                                                         |
|:-------------------------|:-------------------------------------------------------------|
| Chart title              | チャートタイトルを変更します。                                      |
| Use Zoom when dragging   | チャート領域のドラッグでズームするかを指定します。       |
| Keep Navigator Position  | 保存時にスライダーの選択範囲も保存するかを指定します。 |

#### Data
チャートで使用するタグを変更します。  
{{< figure src="/images/web-ui/taz_setting_data.jpg" width="600" >}}

**タグ項目の変更**
| 項目      | 説明                                                                 |
|:----------|:---------------------------------------------------------------------|
| Calc Mode | 集計関数を変更します。                                              |
| Tag Names | 使用するタグを変更します。括弧内はテーブル名です。テーブル自体は変更できません。 |
| Alias     | 凡例の表示名を変更します。<br/>未指定の場合はタグ名と Calc Mode を表示します。 |
| Color     | 色を変更します。                                                   |
| X         | タグを削除します。                                              |

**タグの追加**
下部の [+] をクリックすると、チャート作成時と同じ画面からタグを追加できます。

#### Axes
X 軸と Y 軸を設定します。  
{{< figure src="/images/web-ui/taz_setting_axes.jpg" width="600" >}}  
追加 Y 軸の領域を使用するには、先に Set additional Y-axis を有効にしてください。

**X-Axis**
| 項目                          | 説明                                                          |
|:------------------------------|:--------------------------------------------------------------|
| Display the X-Axis tick line  | X 軸の目盛りを表示します。                                        |
| Pixels between tick marks     | X 軸のデータ 1 件に使用するピクセル数。<br/>表示可能件数 = 横方向の解像度 ÷ 設定値。 |
| _(for)_ Raw                   | RAW モードの値。大量データの表示では、通常 1 未満に設定します。 |
| _(for)_ Calculation           | STAT モードの値。                             |
| use Sampling                  | RAW モードで Machbase のサンプリングを使用し、**スライダー**のデータを高速に検索します。 |

**Y-Axis**
| 項目                                | 説明                                                        |
|:------------------------------------|:------------------------------------------------------------|
| The scale of the Y-Axis start at zero | Y 軸を 0 から開始するかを指定します。                           |
| Display the Y-Axis tick line        | Y 軸の目盛りを表示します。*1)                                   |
| Custom scale                        | Y 軸の最小値・最大値を指定します。                         |
| Custom scale for raw data chart     | RAW モードの Y 軸の最小値・最大値を指定します。          |
| use UCL                             | UCL（管理上限）を設定します。                      |
| use LCL                             | LCL（管理下限）を設定します。                      |

*1) 追加 Y 軸を使用する場合は、常に表示します。

**Additional Y-Axis**
| 項目                                | 説明                                                        |
|:------------------------------------|:------------------------------------------------------------|
| Set additional Y-Axis               | 追加 Y 軸を使用するかを設定します。                            |
| The scale of the Y-Axis start at zero | 追加 Y 軸を 0 から開始するかを指定します。                     |
| Display the Y-Axis tick line        | 追加 Y 軸の目盛りを表示します。*1)                               |
| Custom scale                        | 追加 Y 軸の最小値・最大値を指定します。                      |
| Custom scale for raw data chart     | RAW モードの追加 Y 軸の最小値・最大値を指定します。     |
| use UCL                             | 追加 Y 軸の UCL を設定します。                                |
| use LCL                             | 追加 Y 軸の LCL を設定します。                                |
| Select Tag                          | 使用するタグを選択します。<br/>選択済みのタグを再クリックすると解除します。 |

*1) 追加 Y 軸を使用する場合は、常に表示します。

#### Display
チャートの表示形式を設定します。  
{{< figure src="/images/web-ui/taz_setting_display.jpg" width="600" >}}
| 項目                       | 説明                                                                  |
|:---------------------------|:----------------------------------------------------------------------|
| Chart Type                 | 選択したチャートタイプに応じて表示方法を調整します。                       |
| Display data point in the line chart | 折れ線チャートにデータポイントを表示するかを指定します。           |
| Display legend             | 凡例を表示するかを指定します。                                                 |
| Point Radius               | ポイントサイズを指定します。<br/>0 では非表示になります。      |
| Opacity of Fill Area       | エリアチャートの塗りつぶしの不透明度を指定します（0〜1）。<br/>0 では非表示になります。 |
| Line Thickness             | 線の太さを指定します。                                                 |

#### Time range
このチャート専用の時間範囲を設定します。未指定の場合はダッシュボードの時間範囲を使用します。  
{{< figure src="/images/web-ui/taz_setting_timerange.jpg" width="600" >}}
| 項目        | 説明                                                                 |
|:------------|:---------------------------------------------------------------------|
| From        | 時間範囲の開始値を指定します。                                    |
| To          | 時間範囲の終了値を指定します。                                    |
| Quick range | クリックすると、now または last を使用して時間範囲を自動設定します。 |
