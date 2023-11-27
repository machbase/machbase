---
title: Anscombe's quartet
type: docs
weight: 310
---

```js

FAKE( json({
    [1701059601000000000,  4.26, 3.1 ,  5.39, 12.5],
    [1701059602000000000,  5.68, 4.74,  5.73, 6.89],
    [1701059603000000000,  7.24, 6.13,  6.08, 5.25],
    [1701059604000000000,  4.82, 7.26,  6.42, 7.91],
    [1701059605000000000,  6.95, 8.14,  6.77, 5.76],
    [1701059606000000000,  8.81, 8.77,  7.11, 8.84],
    [1701059607000000000,  8.04, 9.14,  7.46, 6.58],
    [1701059608000000000,  8.33, 9.26,  7.81, 8.47],
    [1701059609000000000, 10.84, 9.13,  8.15, 5.56],
    [1701059610000000000,  7.58, 8.74, 12.74, 7.71],
    [1701059611000000000,  9.96, 8.1 ,  8.84, 7.04]
}) )

MAPVALUE(0, time(value(0)))

CHART(
    global({
        "theme": "dark",
        "legend": {"show": false},
        "grid": [
            { "left":  "7%", "top": "7%", "width": "38%", "height": "38%" },
            { "right": "7%", "top": "7%", "width": "38%", "height": "38%" },
            { "left":  "7%", "bottom": "7%", "width": "38%", "height": "38%" },
            { "right": "7%", "bottom": "7%", "width": "38%", "height": "38%" }
        ]
    }),
    xAxis(
        { "type":"time", "gridIndex": 0, "min": 1701059598000, "max": 1701059614000 },
        { "type":"time", "gridIndex": 1, "min": 1701059598000, "max": 1701059614000 },
        { "type":"time", "gridIndex": 2, "min": 1701059598000, "max": 1701059614000 },
        { "type":"time", "gridIndex": 3, "min": 1701059598000, "max": 1701059614000 }
    ),
    yAxis(
        { "gridIndex": 0, "min": 0, "max": 15 },
        { "gridIndex": 1, "min": 0, "max": 15 },
        { "gridIndex": 2, "min": 0, "max": 15 },
        { "gridIndex": 3, "min": 0, "max": 15 }
    ),
    series(
        {   "type": "time" },
        {   "name": "I",
            "type": "scatter",
            "xAxisIndex": 0,
            "yAxisIndex": 0,
            "markLine": {
                "symbol": ["none", "none"],
                "data": [
                    [ {"coord": [1701059598000, 3]}, {"coord": [1701059614000, 13]} ]
                ]
            }
        },
        {   "name": "II",
            "type": "scatter",
            "xAxisIndex": 1,
            "yAxisIndex": 1,
            "markLine": {
                "symbol": ["none", "none"],
                "data": [
                    [ {"coord": [1701059598000, 3]}, {"coord": [1701059614000, 13]} ]
                ]
            }
        },
        {
            "name": "III",
            "type": "scatter",
            "xAxisIndex": 2,
            "yAxisIndex": 2,
            "markLine": {
                "symbol": ["none", "none"],
                "data": [
                    [ {"coord": [1701059598000, 3]}, {"coord": [1701059614000, 13]} ]
                ]
            }
        },
        {
            "name": "IV",
            "type": "scatter",
            "xAxisIndex": 3,
            "yAxisIndex": 3,
            "markLine": {
                "symbol": ["none", "none"],
                "data": [
                    [
                        {"coord": [1701059598000, 3]},
                        {"coord": [1701059614000, 13]}
                    ]
                ]
            }
        }
    )
)
```

![anscombe_quartet](../../img/anscombe_quartet.jpg)