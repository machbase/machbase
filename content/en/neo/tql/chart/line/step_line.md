---
title: Step Line
type: docs
weight: 60
---

```js
FAKE( json({
    ["Mon", 120, 220, 450],
    ["Tue", 132, 282, 432],
    ["Wed", 101, 201, 401],
    ["Thu", 134, 234, 454],
    ["Fri", 90,  290, 590],
    ["Sat", 230, 430, 530],
    ["Sun", 210, 410, 510]
}) )
CHART(
    chartOption({
        legend: { show:true },
        grid: [{
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
        }],
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        series: [
            {type: "line", data: column(1), step: "start", name: "Step Start"},
            {type: "line", data: column(2), step: "middle", name: "Step Middle"},
            {type: "line", data: column(3), step: "end", name: "Step End"}
        ]
    })
)
```

{{< figure src="../../img/step_line.jpg" width="500" >}}