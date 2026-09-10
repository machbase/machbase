---
title: ダッシュボード
type: docs
weight: 25
toc: true
---

## 概要
ダッシュボードは Machbase のデータをチャートで可視化します。複数のチャートパネルを組み合わせ、各パネルのサイズと位置を調整できます。指定した間隔で自動更新することもできます。

### ダッシュボードの開始
Machbase Neo のホーム画面で DASHBOARD をクリックすると、新しいダッシュボードを作成できます。

{{< figure src="/images/web-ui/main-dashboard.jpg" width="600" >}}

左側の EXPLORER で保存済みのダッシュボードファイル（`*.dsh`）を選択すると、表示・編集できます。保存済みのダッシュボードへのリンクから表示専用モードで開くこともできます（「ダッシュボードの操作」参照）。

## ダッシュボード
### 画面構成

{{< figure src="/images/web-ui/dashboard-screen.jpg" width="600" >}}

ダッシュボードはデータを表示する複数のチャートで構成されます。各パネルを任意の位置とサイズで配置できます。

1. チャートの表示領域
2. ダッシュボードのタイトル
3. ダッシュボードの操作領域

### チャートの追加
操作領域の [+] をクリックするとチャート設定画面が開きます。設定後に [Save] をクリックすると、パネルを追加します。詳細は「チャート設定」を参照してください。

新しいチャートはデフォルトサイズで配置されます。右下をドラッグしてサイズを、上部をドラッグして位置を変更できます。

### ダッシュボードの操作
#### Time Range
ダッシュボード全体の時間範囲を表示します。固定期間や現在時刻に連動する範囲を指定できます。`now` は現在時刻、`h/m/s` は時・分・秒です。
例: `now-3h` は現在時刻の 3 時間前を表します。

#### ダッシュボードの操作ボタン

{{< figure src="/images/web-ui/dashboard-control.jpg" width="400" >}}

1. チャートを追加します。
2. データを再取得して更新します。
3. データの検索時間範囲を設定します。
    - `now` は現在時刻、`last` はデータベースに保存された最後の時刻です。
    - Quick Range を選択すると From/To を自動設定します。
    - `<` と `>` で範囲を 50% ずつ移動します。`now` または `last` を使用している場合は絶対時刻に変換します。
    - 自動更新間隔を設定すると、指定周期で再描画します。
4. ダッシュボードを保存します（拡張子 `.dsh`）。
    - 新規の場合はファイル名と保存フォルダーを指定できます。
5. 別名で保存します。
6. 表示専用モードのリンクをクリップボードにコピーします。
    - 保存済みのダッシュボードでのみ使用できます。
    - ログインが必要です。表示専用モードでは時間範囲の調整と更新だけを行えます。
7. 変数を設定します。{{< neo_since ver="8.0.46" />}}
    **変数の定義**
{{< figure src="/images/web-ui/variables-1.jpg" width="600" >}}
    使用する変数を表示・追加・編集・削除できます。
    - [+ New variable]: 変数を作成します。
      {{< figure src="/images/web-ui/variables-2.jpg" width="600" >}}
        * Label: 変数入力フィールドのタイトル。
        * Variable Name: チャート設定で使用する変数名（例: `{{variable_name}}`）。
        * Value: 変数入力フィールドの選択肢。
    - 既存の変数をクリックすると編集できます。
    - [Export]、[Import]: 変数設定をエクスポート・インポートします。

    **変数の使用**
    - チャート設定での使用
{{< figure src="/images/web-ui/variables-19.jpg" width="600" >}}
        適用する場所に Variable Name を入力します。
    - ダッシュボードでの変更
        1. 変数を定義すると、タイトルの横に入力フィールドが表示されます。
{{< figure src="/images/web-ui/variables-10.jpg" width="300" >}}
        2. 入力アイコンをクリックして値を選択します。
{{< figure src="/images/web-ui/variables-11.jpg" width="300" >}}

## チャートパネル
### 画面構成

{{< figure src="/images/web-ui/panel-screen.jpg" width="600" >}}

1. パネルヘッダーのドラッグ
    上部をドラッグして移動します。
2. サイズ変更
    右下をドラッグします。
3. 凡例の切り替え
    凡例をクリックしてシリーズの表示・非表示を切り替えます。
4. パネルメニュー
    右上のボタンから次のメニューを開きます。
    - Setting: チャート設定を編集します（「チャート設定」参照）。
    - Duplicate: チャートを複製します。
    - Show Taganalyzer: 現在のチャートの内容を Tag Analyzer で表示します。{{< neo_since ver="8.0.49" />}} TAG テーブルでのみ使用できます。
    - Show TQL: TQL チャートの HTML ビューアーを表示します。TQL チャートでのみ使用できます。
    - Delete: パネルを削除します。
    - Save to tql: チャートの内容を TQL ファイルに保存します。

#### TQL への保存
ダッシュボードは内部で TQL を生成してチャートを表示します。Save to tql でその TQL を保存できます。

{{< figure src="/images/web-ui/save2tql.jpg" width="400" >}}

- File Name: 保存する TQL ファイル名。
- Output: 保存する TQL の種類。DATA はデータ取得用、CHART はチャート描画用です。
- Block: DATA の場合だけ使用し、Tag Name を指定します。

## チャート設定
### 概要

{{< figure src="/images/web-ui/chart-setting.jpg" width="600" >}}

1. パネルタイトル
2. チャートタイプ
    - Info: タイプの説明を表示します。
    - Preview: サンプルデータでプレビューします。
3. Link Mode
    ダッシュボードの時間範囲と自動更新に連動するかを指定します。
    - With: 連動（デフォルト）。
    - Without: 連動しません。
4. Query
    - 1 つのチャートに複数の Query を定義できます。
    - Link Mode で解除しない限り、すべての Query はダッシュボードの時間範囲と自動更新に従います。
5. Transform
    - Query の結果から新しいデータを計算します。{{< neo_since ver="8.0.46" />}}
    - 生成したデータも Query と同様に表示・非表示を選択でき、同じオプションを使用します。
6. Chart Option
    - 使用できる設定はチャートタイプによって異なります。
    - 「チャートタイプ別のオプション」を参照してください。

### Query
1 つのチャートで複数の Query を使用し、それぞれを個別に設定できます。

#### 変換関数
{{< figure src="/images/web-ui/taz_chart_functions.jpg" width="600" >}}
- X: 時刻・カテゴリーに適用する式。
- Y: 数値に適用する式。
- 全体: X と Y 全体に適用する式。
このタブの式は Option タブの設定より優先します。対数変換など、Query 結果を数式で加工する場合に使用します。

#### Tag-Based Query Mode
TAG テーブル専用のモードです。
- Table: テーブル名。
- Tag: タグ名を入力または選択。
- Aggregator: X 軸の時間間隔で適用する集計関数。
  選択肢: value、sum、avg、min、max、count。value は集計せずに生データを使用します。
- Alias: 凡例の表示名。

#### Advanced Query Mode
クエリの構成を直接指定します。
{{< figure src="/images/web-ui/chart-setting-advanced-query.jpg" width="600" >}}
- Table: テーブル名。
- Time Field: X 軸の時刻列。
- Value Field: Y 軸の値列。
- Aggregator: 集計関数（Tag-Based と同じ）。
- Alias: 凡例の表示名。
- Filter: WHERE 条件。複数の条件は AND で結合します。

#### Transform Data
Query の結果から新しいデータを計算します。{{< neo_since ver="8.0.46" />}}
- 2 つ以上の Query を定義します。
{{< figure src="/images/web-ui/transform-1.jpg" width="600" >}}
- 計算専用の Query は Visible アイコンをオフにして非表示にできます。
{{< figure src="/images/web-ui/transform-2.jpg" width="600" >}}
- Transform タブで Query を選択し、表示された英字を使用して式を入力します（例: `log(B/A)`）。
{{< figure src="/images/web-ui/transform-3.jpg" width="600" >}}
- [?] で簡単なヘルプを表示します。使用できる数学関数は TQL > Utility Functions の Math を参照してください。
{{< figure src="/images/web-ui/transform_help.jpg" width="400" >}}
Query 結果を再計算するため、単一 Query より遅くなる場合があります。

#### Control Function
{{< figure src="/images/web-ui/chart-setting-qurey-tool.jpg" width="200" >}}
- a. クエリを直接入力します。{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/custom_query.jpg" width="600" >}}
    - SELECT は時刻（ミリ秒）、値の順に指定します。
      例: `SELECT TO_TIMESTAMP(TIME ROLLUP {{period_value}} {{period_unit}}) / 1000000 AS TIME, avg(VALUE) AS 'Usage'`
    - 組み込み変数とユーザー定義変数を使用できます。組み込み変数は「TQL チャート設定」を参照してください。
    - [?] で簡単なヘルプを表示します。
- b. 取得した値に適用する式を入力します（例: `value * 1.5`）。
- c. Query を表示するかを指定します。{{< neo_since ver="8.0.46" />}}
- d. チャートの色を指定します。
- e. Advanced Query Mode と Tag-Based Query Mode を切り替えます。
- f. Query を削除します。

### TQL チャート
ユーザー定義の TQL ファイルをダッシュボードで使用します。SINK が CHART の TQL ファイルだけを使用できます。

{{< figure src="/images/web-ui/tql-chart-setting.jpg" width="600" >}}

#### TQL チャート設定
**Tql path:** TQL ファイルを選択します。
**Params:** 渡すパラメーターを登録します。値を直接入力するか、時間範囲や X 軸間隔などの組み込み変数を使用できます。
- Time range: 他のチャートとの時刻同期に使用します。
  | パラメーター | 説明 |
  |:--|:--|
  | {{from_str}} | 日時文字列（YYYY-MM-DD HH:MI:SS） |
  | {{from_s}},{{from_ms}},{{from_us}},{{from_ns}} | UNIX タイムスタンプ（秒・ミリ秒・マイクロ秒・ナノ秒） |
  | {{to_str}} | 日時文字列（YYYY-MM-DD HH:MI:SS） |
  | {{to_s}},{{to_ms}},{{to_us}},{{to_ns}} | UNIX タイムスタンプ（秒・ミリ秒・マイクロ秒・ナノ秒） |
- period: 時間範囲とパネルサイズから計算する X 軸間隔。
  | パラメーター | 説明 |
  |:--|:--|
  | {{period}} | 期間表現（例: 10s） |
  | {{period_value}} | 期間の値（例: 10） |
  | {{period_unit}} | 期間の単位（例: sec） |

#### TQL ファイルでのパラメーターの使用
`param()` でダッシュボードから渡されたパラメーターを参照できます。

TQL の例:
```sql
SQL(strSprintf(`
SELECT date_trunc('%s', TIME, %1.0f) as TIME, avg(VALUE) as VALUE
FROM EXAMPLE
WHERE TIME between FROM_UNIXTIME(%1.0f) and FROM_UNIXTIME(%1.0f) AND NAME IN ('%s')
GROUP BY TIME ORDER BY TIME`, 
(param('period_unit') ?? 'msec'), 
parseFloat(param('period_value') ?? 10), 
parseFloat(param('from') ?? 1703055573), 
parseFloat(param('to') ?? 1703055583),
(param('tag') ?? 'tag01')
))

CHART_LINE()
```
**SQL():**  
- `param()` と `strSprintf()` でクエリを動的に生成します。  
- 主なパラメーター  
  - `period_unit`: 時間間隔の単位（デフォルト `msec`）  
  - `period_value`: 間隔の値（デフォルト 10）  
  - `from`, `to`: 検索期間  
  - `tag`: 検索するタグ（デフォルト `tag01`）

**CHART_LINE():**
- クエリ結果を折れ線チャートに表示します。

### チャートタイプ別のオプション
#### 共通オプション
- パネルオプション
| オプション | 説明 |
|:-----|:-----|
| Title | パネルに表示するタイトル |
| Theme | チャートテーマ（TQL > CHART を参照） |

- 凡例オプション
| オプション | 説明 |
|:-----|:-----|
| Show legend | 凡例の表示 |
| Vertical | 縦方向の位置（top / center / bottom） |
| Horizontal | 横方向の位置（left / center / right） |
| Alignment type | 配置方向（horizontal / vertical） |

- パネルの余白  
パネル枠とチャートの間の余白を設定します。凡例のスペースが必要な場合は、十分な余白を確保してください。
| オプション | 説明 |
|:-----|:-----|
| Top | 上の余白 |
| Bottom | 下の余白 |
| Left | 左の余白 |
| Right | 右の余白 |

- ツールチップ
| オプション | 説明 |
|:-----|:-----|
| Show tooltip | ツールチップの使用 |
| Type | ツールチップのタイプ（axis / item） |
| Unit | ツールチップに表示する単位 |
| Decimals | 小数点以下の桁数 |

- xAxis
| オプション | 説明 |
|:-----|:-----|
| Interval type | X 軸の時間間隔の単位（none / sec / min / hour。none は自動計算） |
| Interval value | X 軸の間隔の値 |

- yAxis  
[+] で 2 つ目の Y 軸を追加できます。 {{< neo_since ver="8.0.46" />}} 使用するシリーズを選択すると、以下は基本 Y 軸と同じオプションです。
| オプション | 説明 |
|:-----|:-----|
| Position | Y 軸の位置（left / right） |
| Offset | 軸とラベルの間隔 |
| Type | Y 軸の値の型 |
| - Unit | 単位 |
| - Decimals | 小数点以下の桁数 |
| - Name | Y 軸名（軸の上部に表示） |
| Min | 最小値 |
| Max | 最大値 |
| Start at zero | Y 軸に常に 0 を含めるか |

#### Line

{{< figure src="/images/web-ui/line-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Fill area | 塗りつぶしを使用（0〜1 の不透明度を指定） |
| Smooth line | 滑らかな曲線で表示 |
| Show symbols | データポイントの表示 |
| Symbol type | シンボルのタイプ（circle / rect / roundRect / triangle / diamond / pin / arrow） |
| Symbol size | シンボルサイズ |
| Symbol rotate | シンボルの回転角度 |
| Symbol offset | シンボル位置のオフセット |
| Stack | シリーズを積み上げ表示 |
| Step style | 階段状の線のスタイル |
| Emphasis | ホバー時の強調設定 |
| Animation | アニメーションの使用 |

#### Area
{{< figure src="/images/web-ui/line-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Fill area | 塗りつぶしを使用（不透明度 0〜1） |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

#### Column
{{< figure src="/images/web-ui/bar-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Bar width | 棒の幅 |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

#### Column range
{{< figure src="/images/web-ui/bar-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Bar width | 棒の幅 |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

- Query オプション  
Column range は、シリーズごとに最大値と最小値のクエリが必要です。
| オプション | 説明 |
|:-----|:-----|
| Max query | 最大値を返す Query |
| Min query | 最小値を返す Query |

#### Column step
{{< figure src="/images/web-ui/bar-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Bar width | 棒の幅 |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

#### Stacked column
{{< figure src="/images/web-ui/bar-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Bar width | 棒の幅 |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

- 積み上げオプション
| オプション | 説明 |
|:-----|:-----|
| Stacked column | 積み上げモードの使用 |
| Stacked type | 積み上げ方式（normal / percent） |

#### XY column
{{< figure src="/images/web-ui/bar-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Bar width | 棒の幅 |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

- Query オプション
| オプション | 説明 |
|:-----|:-----|
| Value Field | Y 軸の値に使用する列 |
| Category Field | X 軸のカテゴリーに使用する列 |

#### Stacked area
{{< figure src="/images/web-ui/line-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Fill area | 塗りつぶしの使用 |
| Smooth line | 曲線で表示 |
| Emphasis | 強調設定 |
| Animation | アニメーションの使用 |

- 積み上げオプション
| オプション | 説明 |
|:-----|:-----|
| Stacked area | 積み上げモードの使用 |
| Stacked type | 積み上げ方式（normal / percent） |

#### Scatter

{{< figure src="/images/web-ui/scatter-chart-setting.jpg" width="600" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Large data mode | 大量データの処理モード |

- シンボルオプション
| オプション | 説明 |
|:-----|:-----|
| Type | シンボルのタイプ（circle / rect / roundRect / triangle / diamond / pin / arrow） |
| Size | シンボルサイズ |

#### Adv scatter
{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/adv-scatter-chart-setting.jpg" width="600" >}}

- xAxis
| オプション | 説明 |
|:-----|:-----|
| Type | X 軸の値の型 |
| - Unit | 単位 |
| - Decimals | 小数点以下の桁数 |
| Min | 最小値 |
| Max | 最大値 |
| Start at zero | X 軸に常に 0 を含める |
| Series | X 軸のシリーズ（デフォルトは最初の Query） |

- シンボルオプション
| オプション | 説明 |
|:-----|:-----|
| Type | シンボルのタイプ（circle / rect / roundRect / triangle / diamond / pin / arrow） |
| Size | シンボルサイズ |

#### Gauge

{{< figure src="/images/web-ui/gauge-chart-setting.jpg" width="250" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Min | 最小値 |
| Max | 最大値 |

- 軸オプション
| オプション | 説明 |
|:-----|:-----|
| Label distance | ラベルと円形ラインの距離（負の値は外側） |
| Show axis tick | 目盛りの表示 |
| Setting line colors | 値の範囲に応じた線の色（比率 0〜1） |

- Anchor
| オプション | 説明 |
|:-----|:-----|
| Show anchor | 中央の円の表示 |
| Size | 中央の円のサイズ |

- 表示値
| オプション | 説明 |
|:-----|:-----|
| Font size | ゲージ内部の値のフォントサイズ |
| Offset from center | 中心からの距離 |
| Decimal places | 小数点以下の桁数 |
| Active animation | アニメーションの使用 |

#### Pie

{{< figure src="/images/web-ui/pie-chart-setting.jpg" width="250" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Doughnut ratio | ドーナツモードの比率（0〜100） |
| Nightingale mode | Nightingale モード（値に応じて半径を変更） |

#### Liquid fill

{{< figure src="/images/web-ui/liquid_fill-chart-setting.jpg" width="250" >}}

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Shape | 形状（container / circle / rect / roundRect / triangle / diamond / pin / arrow） |
| Unit | 表示値の単位 |
| Digit | 小数点以下の桁数 |
| Font size | フォントサイズ |
| Wave min | 波形の最小値 |
| Wave max | 波形の最大値 |
| Wave amplitude | 波形の振幅（0 は直線） |
| Background color | 波形領域の背景色 |
| Wave animation | 波形アニメーションの使用 |
| Outline | 輪郭の表示 |

#### Text
{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/text-chart-setting.jpg" width="250" >}}

最初の Query 結果をテキストで表示します。2 つ目の Query を追加すると背景チャートに使用します。
- テキストオプション
| オプション | 説明 |
|:-----|:-----|
| Font size | フォントサイズ |
| Unit | 単位 |
| Digit | 小数点以下の桁数 |
| Color | 色 |

- チャートオプション
| オプション | 説明 |
|:-----|:-----|
| Type | 背景チャートのタイプ（line / bar / scatter） |
| Opacity | 塗りつぶしの不透明度（0〜1。line のみ） |
| Symbol size | データポイントのサイズ（0 は非表示） |
| Color | 色 |

#### Geomap
{{< neo_since ver="8.0.46" />}}
{{< figure src="/images/web-ui/geomap-chart-setting.jpg" width="400" >}}

- ツールチップ
| オプション | 説明 |
|:-----|:-----|
| Time | ツールチップに時刻を表示 |
| Latitude, Longitude | 緯度・経度を表示 |

- Interval
| オプション | 説明 |
|:-----|:-----|
| Interval type | X 軸の時間間隔の単位（none / sec / min / hour。none は自動計算） |
| Interval value | X 軸の間隔の値 |

- 地図オプション
| オプション | 説明 |
|:-----|:-----|
| Use zoom control | 地図のズームコントロールの使用 |
| Series | Query ごとに設定 |
| - Latitude | 緯度の列名（別名または集計列を選択可能） |
| - Longitude | 経度の列名（別名または集計列を選択可能） |
| - Marker shape | マーカー形状（marker、circleMarker、circle） |
| - Marker radius | マーカー半径（circleMarker: ピクセル、circle: メートル） |
