---
title: Speed Gauge
type: docs
weight: 940
---

```js {{linenos=table,linenostart=1}}
FAKE(json(`[70]`))
CHART(
    chartOption({
        series: [{
            type: "gauge",
            progress: {
                show: true,
                width: 18
            },
            axisLine: {
                lineStyle: {
                    width: 18
                }
            },
            axisTick: {
                show: false
            },
            splitLine: {
                length: 15,
                lineStyle: {
                    width: 2,
                    color: "#999"
                }
            },
            axisLabel: {
                distance: 25,
                color: "#999",
                fontSize: 20
            },
            anchor: {
                show: true,
                showAbove: true,
                size: 25,
                itemStyle: {
                    borderWidth: 10
                }
            },
            title: {
                show: false
            },
            detail: {
                valueAnimation: true,
                fontSize: 80,
                offsetCenter: [0, "70%"]
            },
            data: [
                {
                    value: column(0)
                }
            ]
        }]
    })
)
```

{{< figure src="../../img/gauge.jpg" width="500" >}}
