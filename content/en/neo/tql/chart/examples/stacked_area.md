---
title: Stacked Line Chart
type: docs
weight: 40
---

```js
FAKE( json({
    ["Mon", 120, 220, 150, 320, 820],
    ["Tue", 132, 182, 232, 332, 932],
    ["Wed", 101, 191, 201, 301, 901],
    ["Thu", 134, 234, 154, 334, 934],
    ["Fri",  90, 290, 190, 390, 1290],
    ["Sat", 230, 330, 330, 330, 1330],
    ["Sun", 210, 310, 410, 320, 1320]
}) )

CHART(
    theme("dark"),
    chartOption({
        "xAxis": {"data": value(0)},
        "yAxis": {},
        "animation": false,
        "series": [
            {"type": "line", "data":value(1), "name": "email", "stack": "total", "areaStyle":{} },
            {"type": "line", "data":value(2), "name": "ads", "stack": "total", "areaStyle":{} },
            {"type": "line", "data":value(3), "name": "video", "stack": "total", "areaStyle":{} },
            {"type": "line", "data":value(4), "name": "direct", "stack": "total", "areaStyle":{} },
            {"type": "line", "data":value(5), "name": "search", "stack": "total", "areaStyle":{},
                "label": {"show": true, "position": "top"}
            }
        ]
    })
)
```

![stacked_area](../../img/stacked_area.jpg)