---
title: Nightingale
type: docs
weight: 930
---

```js
FAKE(csv(`rose 1,rose 2,rose 3,rose 4,rose 5,rose 6,rose 7,rose 8
40,38,32,30,28,26,22,18
`))

TRANSPOSE(header(true))
MAPVALUE(0, dict("name", value(0), "value", value(1)))

CHART(
    theme("dark"),
    chartOption({
        "legend": {
            "top": "bottom"
        },
        "toolbox": {
            "show": true,
            "feature": {
                "saveAsImage": { "show": true, "title": "save as image" }
            }
        },
        "series": [
            {
                "name": "Nightingale Chart",
                "type": "pie",
                "radius": ["50", "250"],
                "center": ["50%", "50%"],
                "roseType": "area",
                "itemStyle": {
                    "borderRadius": 8
                },
                "data": value(0)
            }
        ]
    })
)
```

![basic_mix](../../img/nightingale.jpg)