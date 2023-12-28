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

MAPVALUE(0, list(value(0), value(1)))

CHART(
    chartOption({
        "title": { "text": "Area Pieces" },
        "xAxis": { "type": "category", "boundaryGap": false },
        "yAxis": { "type": "value", "boundaryGap": [0, "30%"] },
        "visualMap":{
            "type": "piecewise",
            "show": false,
            "dimension": 0,
            "seriesIndex": 0,
            "pieces": [
                { "gt": 1, "lt": 3, "color": "rgba(0, 0, 180, 0.4)" },
                { "gt": 5, "lt": 7, "color": "rgba(0, 0, 180, 0.4)" }
            ]
        },
        "series": [
            {
                "type": "line",
                "smooth": 0.6,
                "symbol": "none",
                "data": column(0),
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
        ]
    })
)
```

{{< figure src="../../img/area_pieces.jpg" width="500" >}}