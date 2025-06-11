---
title: Basic Gauge
type: docs
weight: 10
---

```js {{linenos=table,linenostart=1}}
FAKE(linspace(55, 60, 1))
CHART(
    chartOption({
        tooltip: {
            formatter: "{a} <br/>{b} : {c}%"
        },
        series: [
            {
                name: "Pressure",
                type: "gauge",
                detail: {
                    formatter: "{value}"
                },
                data: [
                    {
                        value: column(0)[0],
                        name: "PRESSURE"
                    }
                ]
            }
        ]
    })
)
```

{{< figure src="../../img/basic_gauge.jpg" width="500" >}}
