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
{{< neo_since ver="8.0.7" />}}

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

### Scatter

{{< cards >}}
    {{< card link="./examples/basic_scatter" title="Basic Scatter Chart"
            image="./img/basic_scatter.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/anscombe_quartet" title="Anscombe's quartet"
            image="./img/anscombe_quartet.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/scatter_band" title="Scatter Band"
            image="./img/scatter_band.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}

### Others

{{< cards >}}
    {{< card link="./examples/basic_mix" title="Basic Mix" subtitle="Bar and Line Series"
            image="./img/basic_mix.jpg" method="Fill" options="600x q80 webp">}}
    {{< card link="./examples/basic_pie" title="Basic Pie"
            image="./img/basic_pie.jpg" method="Fill" options="600x q80 webp">}}
{{< /cards >}}
