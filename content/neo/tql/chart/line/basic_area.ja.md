---
title: 基本的な面グラフ
type: docs
weight: 20
toc: true
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    ["Mon", 820],
    ["Tue", 932],
    ["Wed", 901],
    ["Thu", 934],
    ["Fri", 1290],
    ["Sat", 1330],
    ["Sun", 1320]
}) )
// |   0      1
// +-> day    value
// |
CHART(
    chartOption({
        legend:{ show:false },
        xAxis: { type:"category", data: column(0) },
        yAxis: {},
        series:[
            { type: "line", smooth:false, color:"#7585CE", areaStyle:{}, data: column(1) }
        ]
    })
)
```

{{< figure src="/neo/tql/chart/img/basic_area.jpg" width="500" >}}
