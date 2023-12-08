---
title: CHART()
type: docs
weight: 51
---

{{< callout type="error" >}}
<b>WARNING</b><br/>
The CHART() function is in **experimental** stage. The syntax of the function *will be changed* in the next releases without notices.
{{< /callout >}}

## CHART
{{< neo_since ver="8.0.8" />}}

The new `CHART()` provides more fine-tuned options to create attractive charts.
It is the new version of API that replaces for the previous `CHART_LINE()`, `CHART_BAR()` and `CHART_SCATTER` functions.

### Line

{{< cards >}}
    {{< card link="./examples/basic_line" title="Basic Line Chart"
            image="./img/basic_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/basic_area" title="Basic Area Chart"
            image="./img/basic_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/stacked_line" title="Stacked Line Chart"
            image="./img/stacked_line.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/stacked_area" title="Stacked Area Chart"
            image="./img/stacked_area.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/area_pieces" title="Area Pieces"
            image="./img/area_pieces.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/step_line" title="Step Line"
            image="./img/step_line.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Bar

{{< cards >}}
    {{< card link="./examples/basic_bar" title="Basic Bar Chart"
            image="./img/basic_bar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/tangential_polar_bar" title="Tangential Polar Bar"
            image="./img/tangential_polar_bar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/bar_category" title="Category Bar"
            image="./img/bar_category.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Pie

{{< cards >}}
    {{< card link="./examples/basic_pie" title="Basic Pie"
            image="./img/basic_pie.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/doughnut" title="Doughnut"
            image="./img/doughnut.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/nightingale" title="Nightingale"
            image="./img/nightingale.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Scatter

{{< cards >}}
    {{< card link="./examples/basic_scatter" title="Basic Scatter Chart"
            image="./img/basic_scatter.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/anscombe_quartet" title="Anscombe's quartet"
            image="./img/anscombe_quartet.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/million_points" title="1M Points"
            image="./img/million_points.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Candlestick

{{< cards >}}
    {{< card link="./examples/basic_candlestick" title="Basic Candlestick"
            image="./img/basic_candlestick.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/candlestick_marketindex" title="Stock Index"
            image="./img/candlestick_marketindex.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/stock_dji" title="Dow-Jones Index"
            image="./img/stock_dji.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Liquidfill

{{< cards >}}
    {{< card link="./examples/liquidfill" title="Liquid Fill"
            image="./img/liquidfill.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/liquidfill_multiple" title="Multiple Waves"
            image="./img/liquidfill_multiple.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/liquidfill_still" title="Still Wave"
            image="./img/liquidfill_still.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Others

{{< cards >}}
    {{< card link="./examples/basic_mix" title="Basic Mix" subtitle="Bar and Line Series"
            image="./img/basic_mix.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/basic_radar" title="Radar"
            image="./img/basic_radar.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/line_airpassengers" title="Air Passengers"
            image="./img/line_airpassengers.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}
