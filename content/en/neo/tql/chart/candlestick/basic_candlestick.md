---
title: Basic Candlestick Chart
type: docs
weight: 400
---

```js {{linenos=table,linenostart=1}}
FAKE(json({
    ["2017-10-24", 20, 34, 10, 38 ], 
    ["2017-10-25", 40, 35, 30, 50 ],
    ["2017-10-26", 31, 38, 33, 44 ],
    ["2017-10-27", 38, 15,  5, 42 ]
}))

MAPVALUE(1, list(value(1), value(2), value(3), value(4)))
POPVALUE(2, 3, 4)
CHART(
    chartOption({
        legend: { show: false },
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            { type: "candlestick", data: column(1) }
        ]
    })
)
```

{{< figure src="../../img/basic_candlestick.jpg" width="500" >}}
