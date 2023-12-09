---
title: Category Bar
type: docs
weight: 130
---

```js
FAKE( json({
    ["Brazil", 18203, 19325],
    ["Indonesia", 23489, 23438],
    ["USA", 29034, 31000],
    ["India", 104970, 121594],
    ["Chilna", 131744, 134141],
    ["World", 630230, 681807]
}) )
CHART(
    chartOption({
        "legend":{"show":true},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "xAxis": { "type": "category" },
        "yAxis": { },
        "series": [
            { "type": "bar", "name": "2011", "data": value(1) },
            { "type": "bar", "name": "2022", "data": value(2) }
        ]
    })
)
```

![bar_category](../../img/bar_category.jpg)