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
    theme("dark"),
    global({
        "legend":{"show":false}
    }),
    series(
        {"type": "category"},
        {"type": "line","smooth":false, "color":"#7585CE", "areaStyle":{}}
    )
)
```

![basic_area](../../img/basic_area.jpg)