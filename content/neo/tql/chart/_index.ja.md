---
title: CHART()
type: docs
weight: 51
toc: true
---

*構文*: `CHART(chartOption() [,size()] [, theme()] [, chartJSCode()])` {{< neo_since ver="8.0.8" />}}

## オプション {#옵션}

### chartOption()

*構文*: `chartOption( { Apache EChartsのオプションJSON } )`

### chartJSCode()

*構文*: `chartJSCode( { ユーザー定義のJavaScriptコード } )`

### size()

*構文*: `size(width, height)`

- `width` *string*: チャートの幅（例：`'800px'`）
- `height` *string*: チャートの高さ（例：`'800px'`）

### theme()

*構文*: `theme(name)`

- `name` *string*: テーマ名

チャートにテーマを適用します。使用できるテーマは `white`、`dark`、`chalk`、`essos`、`infographic`、`macarons`、`purple-passion`、`roma`、`romantic`、`shine`、`vintage`、`walden`、`westeros`、`wonderland` です。各テーマのプレビューは[後述のセクション](#themes)を参照してください。

### plugins()

*構文*: `plugins(plugin...)`

- `plugin` *string*: 定義済みのプラグイン名、またはプラグインモジュールのURL

| 定義済みプラグイン | モジュールのパス |
| :----------------- | :------------------|
| liquidfill         | `/web/echarts/echarts-liquidfill.min.js` |
| wordcloud          | `/web/echarts/echarts-wordcloud.min.js`  |
| gl                 | `/web/echarts/echarts-gl.min.js`         |

## 例 {#예시}

新しい `CHART()` 関数では、詳細な設定によりさまざまな可視化を実現できます。従来の `CHART_LINE()`、`CHART_BAR()`、`CHART_SCATTER()`、`CHART_LINE3D()`、`CHART_BAR3D()`、`CHART_SCATTER3D()` 関数を置き換えます。

### 折れ線グラフ {#line}

{{< cards >}}
    {{< card link="./line/basic_line" title="基本的な折れ線グラフ"
            image="/neo/tql/chart/img/basic_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/basic_area" title="基本的な面グラフ"
            image="/neo/tql/chart/img/basic_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/stacked_line" title="積み上げ折れ線グラフ"
            image="/neo/tql/chart/img/stacked_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/stacked_area" title="積み上げ面グラフ"
            image="/neo/tql/chart/img/stacked_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/area_pieces" title="区間別の面グラフ"
            image="/neo/tql/chart/img/area_pieces.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/step_line" title="階段グラフ"
            image="/neo/tql/chart/img/step_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/multiple_x_axes" title="複数のX軸"
            image="/neo/tql/chart/img/multiple_x_axes.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/multiple_y_axes" title="複数のY軸"
            image="/neo/tql/chart/img/multiple_y_axes.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/basic_mix" title="基本的な複合グラフ" subtitle="折れ線と棒の系列"
            image="/neo/tql/chart/img/basic_mix.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/large_area" title="大規模な面グラフ" subtitle="LTTBによるダウンサンプリング"
            image="/neo/tql/chart/img/large_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/line_datatransform" title="データ変換"
            image="/neo/tql/chart/img/line_datatransform.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/line_airpassengers" title="航空旅客数"
            image="/neo/tql/chart/img/line_airpassengers.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/cartesian_coord" title="直交座標系"
            image="/neo/tql/chart/img/cartesian_coord.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 棒グラフ {#bar}

{{< cards >}}
    {{< card link="./bar/basic_bar" title="基本的な棒グラフ"
            image="/neo/tql/chart/img/basic_bar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_category" title="カテゴリ別棒グラフ" subtitle="GROUPのbyとlazy"
            image="/neo/tql/chart/img/bar_category.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_stacked_normalize" title="正規化した積み上げ棒グラフ" subtitle="割合による正規化"
            image="/neo/tql/chart/img/bar_stacked_normalize.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_negative" title="負の値"
            image="/neo/tql/chart/img/bar_negative.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/tangential_polar_bar" title="極座標の接線方向の棒グラフ"
            image="/neo/tql/chart/img/tangential_polar_bar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_largescale" title="大規模な棒グラフ"
            image="/neo/tql/chart/img/bar_largescale.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_race" title="バーチャートレース"
            image="/neo/tql/chart/img/bar_race.gif" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 円グラフ {#pie}

{{< cards >}}
    {{< card link="./pie/basic_pie" title="基本的な円グラフ"
            image="/neo/tql/chart/img/basic_pie.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./pie/doughnut" title="ドーナツグラフ"
            image="/neo/tql/chart/img/doughnut.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./pie/nightingale" title="ナイチンゲールのローズチャート"
            image="/neo/tql/chart/img/nightingale.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 散布図 {#scatter}

{{< cards >}}
    {{< card link="./scatter/basic_scatter" title="基本的な散布図"
            image="/neo/tql/chart/img/basic_scatter.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./scatter/anscombe_quartet" title="アンスコムの四重奏"
            image="/neo/tql/chart/img/anscombe_quartet.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./scatter/million_points" title="100万点の散布図" subtitle="100万点"
            image="/neo/tql/chart/img/million_points.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### レーダーチャート {#radar}

{{< cards >}}
    {{< card link="./radar/basic_radar" title="基本的なレーダーチャート"
            image="/neo/tql/chart/img/basic_radar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./radar/radar_custom" title="カスタムレーダーチャート"
            image="/neo/tql/chart/img/radar_custom.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### ゲージ {#gauge}

{{< cards >}}
    {{< card link="./gauge/basic_gauge" title="基本的なゲージ"
            image="/neo/tql/chart/img/basic_gauge.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./gauge/gauge" title="速度ゲージ"
            image="/neo/tql/chart/img/gauge.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./gauge/gauge_update" title="ゲージの更新"
            image="/neo/tql/chart/img/gauge_update.gif" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### ローソク足チャート {#candlestick}

{{< cards >}}
    {{< card link="./candlestick/basic_candlestick" title="基本的なローソク足チャート"
            image="/neo/tql/chart/img/basic_candlestick.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./candlestick/candlestick_marketindex" title="株価指数"
            image="/neo/tql/chart/img/candlestick_marketindex.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./candlestick/stock_dji" title="ダウ平均株価"
            image="/neo/tql/chart/img/stock_dji.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 箱ひげ図 {#boxplot}

{{< cards >}}
    {{< card link="./boxplot/michelson-morley" title="マイケルソン・モーリーの実験"
            image="/neo/tql/chart/img/boxplot_michelson_morley.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./boxplot/iris-sepal-length" title="アヤメのがく片の長さ"
            image="/neo/tql/chart/img/boxplot_iris_sepal_length.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### GeoJSON

{{< cards >}}
    {{< card link="./geojson/seoul_gu" title="GeoJSON - ソウル"
            image="/neo/tql/chart/img/seoul_gu.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### ヒートマップ {#heatmap}

{{< cards >}}
    {{< card link="./heatmap/heatmap" title="基本的なヒートマップ" subtitle="2万件のデータ"
            image="/neo/tql/chart/img/heatmap.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./heatmap/heatmap_discrete" title="離散値への色の割り当て" subtitle="2万件のデータ"
            image="/neo/tql/chart/img/heatmap_discrete.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./heatmap/heatmap_calendar" title="カレンダーヒートマップ" subtitle="2023年"
            image="/neo/tql/chart/img/heatmap_calendar.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 水位グラフ {#liquidfill}

{{< cards >}}
    {{< card link="./liquidfill/liquidfill" title="水位グラフ"
            image="/neo/tql/chart/img/liquidfill.gif" method="Fill" options="600x q80 webp">}}
    {{< card link="./liquidfill/liquidfill_multiple" title="複数の波"
            image="/neo/tql/chart/img/liquidfill_multiple.gif" method="Fill" options="600x q80 webp">}}
    {{< card link="./liquidfill/liquidfill_still" title="静止した波"
            image="/neo/tql/chart/img/liquidfill_still.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 3D地球儀 {#3d-globe}

{{< cards >}}
    {{< card link="./globe/hello-world" title="はじめての地球儀"
            image="/neo/tql/chart/img/gl-hello-world.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./globe/airline" title="地球儀上の航空路線"
            image="/neo/tql/chart/img/airline.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 3D棒グラフ {#3d-bar}

{{< cards >}}
    {{< card link="./bar3d/bar3d-dataset" title="データセットを使った3D棒グラフ"
            image="/neo/tql/chart/img/bar3d-dataset.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar3d/bar3d-stacked" title="3D積み上げ棒グラフ"
            image="/neo/tql/chart/img/bar3d-stacked.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar3d/bar3d-transparent" title="透明な3D棒グラフ"
            image="/neo/tql/chart/img/bar3d-transparent.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 3D折れ線グラフ {#3d-line}

{{< cards >}}
    {{< card link="./line3d/line3d-othographic" title="正投影"
            image="/neo/tql/chart/img/line3d-othographic.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### その他 {#기타}

{{< cards >}}
    {{< card link="./others/sankey" title="基本的なサンキー図"
            image="/neo/tql/chart/img/sankey.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/wordcloud" title="ワードクラウド"
            image="/neo/tql/chart/img/wordcloud.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/geo_svg_lines" title="SVG地図上の線"
            image="/neo/tql/chart/img/geo_svg_lines.gif" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

## テーマ {#themes}

{{< tabs >}}
{{< tab name="MAPVALUE" >}}
```js {{linenos=table,hl_lines=[6]}}
FAKE( arrange(1, 100, 1))
MAPVALUE(1, sin(2 * PI * 5 * value(0)/100) )
MAPVALUE(2, sin(2 * PI * 5 * (value(0)+5)/100) )
MAPVALUE(3, sin(2 * PI * 5 * (value(0)+10)/100) )
CHART(
    size("500px", "200px"),
    theme("dark"),
    chartOption({
        title:{ text:"theme(dark)" },
        xAxis:{ data:column(0), axisLabel:{show: false} },
        yAxis:{},
        series:[
            {type:"line", data:column(1), name:"series1"},
            {type:"line", data:column(2), name:"series2"},
            {type:"line", data:column(3), name:"series3"},
        ],
        legend:{ bottom: 10 }
    })
)
```
{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[12]}}
SCRIPT({
    for( i = 1; i <= 100; i++) {
        $.yield(
            i,
            Math.sin(2 * Math.PI * 5 * i / 100),
            Math.sin(2 * Math.PI * 5 * (i + 5) / 100),
            Math.sin(2 * Math.PI * 5 * (i + 10) / 100)
        )
    }
})
CHART(
    size("500px", "200px"),
    theme("dark"),
    chartOption({
        title:{ text:"theme(dark)" },
        xAxis:{ data:column(0), axisLabel:{show: false} },
        yAxis:{},
        series:[
            {type:"line", data:column(1), name:"series1"},
            {type:"line", data:column(2), name:"series2"},
            {type:"line", data:column(3), name:"series3"},
        ],
        legend:{ bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

以下の画像は、各テーマを適用したチャートの例です。

**white**
{{< figure src="/neo/tql/img/theme_white.jpg" width="500" >}}

**dark**
{{< figure src="/neo/tql/img/theme_dark.jpg" width="500" >}}

**chalk**
{{< figure src="/neo/tql/img/theme_chalk.jpg" width="500" >}}

**essos**
{{< figure src="/neo/tql/img/theme_essos.jpg" width="500" >}}

**infographic**
{{< figure src="/neo/tql/img/theme_infographic.jpg" width="500" >}}

**macarons**
{{< figure src="/neo/tql/img/theme_macarons.jpg" width="500" >}}

**purple-passion**
{{< figure src="/neo/tql/img/theme_purple-passion.jpg" width="500" >}}

**roma**
{{< figure src="/neo/tql/img/theme_roma.jpg" width="500" >}}

**romantic**
{{< figure src="/neo/tql/img/theme_romantic.jpg" width="500" >}}

**shine**
{{< figure src="/neo/tql/img/theme_shine.jpg" width="500" >}}

**vintage**
{{< figure src="/neo/tql/img/theme_vintage.jpg" width="500" >}}

**walden**
{{< figure src="/neo/tql/img/theme_walden.jpg" width="500" >}}

**westeros**
{{< figure src="/neo/tql/img/theme_westeros.jpg" width="500" >}}

**wonderland**
{{< figure src="/neo/tql/img/theme_wonderland.jpg" width="500" >}}
