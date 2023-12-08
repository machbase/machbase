---
title: Tangential Polar Bar
type: docs
weight: 120
---

```js
FAKE( json({
    ["A", 2],
    ["B", 1.2],
    ["C", 2.4],
    ["D", 3.6]
}) )

CHART(
    theme("dark"),
    chartOption({
        "title": {
            "text": "Tangential Polar Bar Label Position (middle)"
        },
        "polar": { "radius": [30, "80%"] },
        "radiusAxis": {
            "type": "category",
            "data": value(0)
        },
        "angleAxis": { "max": 4, "startAngle": 90 },
        "tooltip": {},
        "series": {   
            "type": "bar",
            "coordinateSystem": "polar",
            "data": value(1),
            "label": {
                "show": true,
                "position": "middle",
                "formatter": "{b}: {c}"
            }
        }
    })
 )
```

![basic_line](../../img/tangential_polar_bar.jpg)