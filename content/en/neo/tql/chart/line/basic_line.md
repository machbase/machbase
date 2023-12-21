---
title: Basic Line Chart
type: docs
weight: 10
---

```js
FAKE( linspace(0, 360, 100))
MAPVALUE(2, sin((value(0)/180)*PI))
CHART(
    chartOption({
        "xAxis": {
            "type": "category",
            "data": column(0)
        },
        "yAxis": {},
        "series": [
            {
                "type": "line",
                "data": column(1)
            }
        ]
    })
)
```

![basic_line](../../img/basic_line.jpg)