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
    global({
        "theme": "dark",
        "polar": { "radius": ["30", "90%"] },
        "angleAxis": { "max": 4, "startAngle": 90 },
        "radiusAxis": {
            "type": "category"
        },
        "legend":{"show":false},
        "tooltip": {}
    }),
    series(
        {   "type": "category"},
        {   "type": "bar",
            "coordinateSystem": "polar",
            "label": {
                "show": true,
                "position": "middle"
            }
        }
    )
)
```

![basic_line](../../img/tangential_polar_bar.jpg)