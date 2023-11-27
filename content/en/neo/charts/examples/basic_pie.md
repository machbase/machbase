---
title: Pie Chart
type: docs
weight: 910
---

```js
FAKE( json({
    ["Search Engine", 1048 ],
    ["Direct"       ,  735 ],
    ["Email"        ,  580 ],
    ["Union Ads"    ,  484 ],
    ["Video Ads"    ,  300 ]
}) )

CHART(
    global({
        "theme": "dark",
        "tooltip": {
            "trigger": "item"
        },
        "legend": {
            "orient": "vertical",
            "left": "left"
        }
    }),
    series(
        {
            "type": "category"
        },
        {
            "name": "Access From",
            "type": "pie",
            "radius": "70%",
            "emphasis": {
                "itemStyle": {
                    "borderWidth": 10,
                    "borderColor": "#0002"
                }
            }
        }
    )
)
```

![basic_mix](../../img/basic_pie.jpg)