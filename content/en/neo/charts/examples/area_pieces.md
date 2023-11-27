---
title: Area Pieces
type: docs
weight: 50
---

```js
FAKE(
    json({
        ["2019-10-10", 200],
        ["2019-10-11", 560],
        ["2019-10-12", 750],
        ["2019-10-13", 580],
        ["2019-10-14", 250],
        ["2019-10-15", 300],
        ["2019-10-16", 450],
        ["2019-10-17", 300],
        ["2019-10-18", 100]
    })
)

CHART(
    global({
        "title": {"text": "Area Pieces"},
        "theme": "dark",
        "legend": {"show": false},
        "visualmap":[{
            "type": "piecewise",
            "show": false,
            "dimension": "0",
            "seriesIndex": 0,
            "pieces": [
                {
                    "gt": 1,
                    "lt": 3,
                    "color": "#00F8"
                },
                {
                    "gt": 5,
                    "lt": 7,
                    "color": "#00F8"
                }
            ]
        }]
    }),
    series(
        {
            "type": "category"
        },
        {
            "type": "line",
            "smooth": true,
            "symbol": "none",
            "lineStyle": {
                "color": "#5470C6",
                "width": 5
            },
            "areaStyle":{},
            "markLine": {
                "symbol": ["none", "none"],
                "label": { "show": false },
                "data": [{ "xAxis": 1 }, { "xAxis": 3 }, { "xAxis": 5 }, { "xAxis": 7 }]
            }
        }
    )
)
```


![area_pieces](../../img/area_pieces.jpg)