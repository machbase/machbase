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
    series(
        {"type": "category", "smooth":false},
        {"type": "line", "smooth":false, "name": "email", "stack": "total", "areaStyle":{} },
        {"type": "line", "smooth":false, "name": "ads", "stack": "total", "areaStyle":{} },
        {"type": "line", "smooth":false, "name": "video", "stack": "total", "areaStyle":{} },
        {"type": "line", "smooth":false, "name": "direct", "stack": "total", "areaStyle":{} },
        {"type": "line", "smooth":false, "name": "search", "stack": "total", "areaStyle":{},
            "label": {"show": true, "position": "top"}
        }
    )
)
```

![stacked_area](../../img/stacked_area.jpg)