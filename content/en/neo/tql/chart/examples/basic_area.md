---
title: Basic Area Chart
type: docs
weight: 20
---

```js
FAKE( json({
    ["Mon", 820],
    ["Tue", 932],
    ["Wed", 901],
    ["Thu", 934],
    ["Fri", 1290],
    ["Sat", 1330],
    ["Sun", 1320]
}) )
CHART(
    chartOption({
        "legend":{"show":false},
        "xAxis": {"type": "category", "data": value(0) },
        "yAxis": {},
        "series":[
            {"type": "line","smooth":false, "color":"#7585CE", "areaStyle":{}, "data": value(1)}
        ]
    })
)
```

![basic_area](../../img/basic_area.jpg)