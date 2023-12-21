---
title: Basic Scatter Chart
type: docs
weight: 300
---

```js
FAKE( linspace(0, 360, 100) )
MAPVALUE( 2, sin((value(0)/180)*PI) )
CHART(
    chartOption({
        "xAxis":{ "data": column(0) },
        "yAxis":{},
        "series":[
            {"type":"scatter", "data": column(1)}
        ]
    })
)
```

![basic_line](../../img/basic_scatter.jpg)