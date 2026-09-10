---
title: 極座標の接線方向の棒グラフ
type: docs
weight: 120
toc: true
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    ["A", 2],
    ["B", 1.2],
    ["C", 2.4],
    ["D", 3.6]
}) )

CHART(
    chartOption({
        title: {
            text: "Tangential Polar Bar Label Position (middle)"
        },
        polar: { radius: [30, "80%"] },
        radiusAxis: {
            type: "category",
            data: column(0)
        },
        angleAxis: { max: 4, startAngle: 90 },
        tooltip: {},
        series: {   
            type: "bar",
            coordinateSystem: "polar",
            data: column(1),
            label: {
                show: true,
                position: "middle",
                formatter: "{b}: {c}"
            }
        }
    })
)
```

{{< figure src="/neo/tql/chart/img/tangential_polar_bar.jpg" width="500" >}}
