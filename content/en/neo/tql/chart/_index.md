---
title: CHART()
type: docs
weight: 51
---

{{< neo_since ver="8.0.8" />}}

The new `CHART()` provides more fine-tunable options to create attractive charts.
It is the new version of API that replaces for the previous `CHART_LINE()`, `CHART_BAR()`, `CHART_SCATTER`, `CHART_LINE3D`, `CHART_BAR3D()` and `CHART_SCATTER3D()` functions.

### Line

{{< cards >}}
    {{< card link="./line/basic_line" title="Basic Line Chart"
            image="./img/basic_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/basic_area" title="Basic Area Chart"
            image="./img/basic_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/stacked_line" title="Stacked Line Chart"
            image="./img/stacked_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/stacked_area" title="Stacked Area Chart"
            image="./img/stacked_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/area_pieces" title="Area Pieces"
            image="./img/area_pieces.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/step_line" title="Step Line"
            image="./img/step_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/cartesian_coord" title="Cartesian Coordinate System"
            image="./img/cartesian_coord.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/multiple_x_axes" title="Multiple X axes"
            image="./img/multiple_x_axes.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/large_area" title="Large Area Chart" subtitle="lttb downsampling"
            image="./img/large_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./line/line_datatransform" title="Data Transform"
            image="./img/line_datatransform.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Bar

{{< cards >}}
    {{< card link="./bar/basic_bar" title="Basic Bar Chart"
            image="./img/basic_bar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/tangential_polar_bar" title="Tangential Polar Bar"
            image="./img/tangential_polar_bar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_category" title="Category Bar"
            image="./img/bar_category.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_negative" title="Negative Values"
            image="./img/bar_negative.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_largescale" title="Large Scale Bar Chart"
            image="./img/bar_largescale.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar/bar_race" title="Bar race"
            image="./img/bar_race.gif" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Pie

{{< cards >}}
    {{< card link="./pie/basic_pie" title="Basic Pie"
            image="./img/basic_pie.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./pie/doughnut" title="Doughnut"
            image="./img/doughnut.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./pie/nightingale" title="Nightingale"
            image="./img/nightingale.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Scatter

{{< cards >}}
    {{< card link="./scatter/basic_scatter" title="Basic Scatter Chart"
            image="./img/basic_scatter.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./scatter/anscombe_quartet" title="Anscombe's quartet"
            image="./img/anscombe_quartet.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./scatter/million_points" title="1M Points" subtitle="1 million points"
            image="./img/million_points.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Candlestick

{{< cards >}}
    {{< card link="./candlestick/basic_candlestick" title="Basic Candlestick"
            image="./img/basic_candlestick.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./candlestick/candlestick_marketindex" title="Stock Index"
            image="./img/candlestick_marketindex.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./candlestick/stock_dji" title="Dow-Jones Index"
            image="./img/stock_dji.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Heatmap

{{< cards >}}
    {{< card link="./heatmap/heatmap" title="Basic Heatmap" subtitle="20K data"
            image="./img/heatmap.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./heatmap/heatmap_discrete" title="Discrete Mapping of Colors" subtitle="20K data"
            image="./img/heatmap_discrete.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./heatmap/heatmap_calendar" title="Calendar Heatmap" subtitle="Year 2023"
            image="./img/heatmap_calendar.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Liquidfill

{{< cards >}}
    {{< card link="./liquidfill/liquidfill" title="Liquid Fill"
            image="./img/liquidfill.gif" method="Fill" options="600x q80 webp">}}
    {{< card link="./liquidfill/liquidfill_multiple" title="Multiple Waves"
            image="./img/liquidfill_multiple.gif" method="Fill" options="600x q80 webp">}}
    {{< card link="./liquidfill/liquidfill_still" title="Still Waves"
            image="./img/liquidfill_still.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 3D Globe
{{< cards >}}
    {{< card link="./globe/hello-world" title="Hello World"
            image="./img/gl-hello-world.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./globe/airline" title="Airline on Globe"
            image="./img/airline.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### 3D Bar

{{< cards >}}
    {{< card link="./bar3d/bar3d-dataset" title="3D Bar with Dataset"
            image="./img/bar3d-dataset.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar3d/bar3d-stacked" title="Stacked 3D Bar"
            image="./img/bar3d-stacked.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./bar3d/bar3d-transparent" title="Transparent 3D Bar"
            image="./img/bar3d-transparent.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Others

{{< cards >}}
    {{< card link="./others/basic_mix" title="Basic Mix" subtitle="Bar and Line Series"
            image="./img/basic_mix.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/basic_radar" title="Radar"
            image="./img/basic_radar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/line_airpassengers" title="Air Passengers"
            image="./img/line_airpassengers.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/sankey" title="Basic Sankey"
            image="./img/sankey.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/gauge" title="Basic Gauge"
            image="./img/gauge.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/wordcloud" title="Word Cloud"
            image="./img/wordcloud.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./others/geo_svg_lines" title="GEO SVG Lines"
            image="./img/geo_svg_lines.gif" method="Fill" options="600x q80 webp">}}
{{< /cards >}}
