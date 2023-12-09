---
title: Dow-Jones Index
type: docs
weight: 420
---

```js
CSV( file("https://machbase.com/assets/example/stock-DJI.csv") )
DROP(1) // drop header
MAPVALUE(0, value(0), "date")
MAPVALUE(1, parseFloat(value(1)), "open")
MAPVALUE(2, parseFloat(value(2)), "close")
MAPVALUE(3, parseFloat(value(3)), "lowest")
MAPVALUE(4, parseFloat(value(4)), "highest")
MAPVALUE(5, parseFloat(value(5)), "volume")

MAPVALUE(6, movavg(value(2), 5), "MA5")
MAPVALUE(7, movavg(value(2), 10), "MA10")
MAPVALUE(8, movavg(value(2), 20), "MA20")
MAPVALUE(9, movavg(value(2), 30), "MA30")
//make data shape 
MAPVALUE(1, list(value(1), value(2), value(3), value(4)), "DJI")
POPVALUE(2,3,4)
//  |    0    1                            2      3   4    5    6
//  +-> date [open,close,lowest,highest]  volume MA5 MA10 MA20 MA30

MAPVALUE(7, diff(value(2)))
//  |    0    1                            2      3   4    5    6     7
//  +-> date [open,close,lowest,highest]  volume MA5 MA10 MA20 MA30  volumneDiff

MAPVALUE(7, value(7) == NULL || value(7) > 0 ? 1 : -1)
//  |    0    1                            2      3   4    5    6     7
//  +-> date [open,close,lowest,highest]  volume MA5 MA10 MA20 MA30  (1 or -1)

MAPVALUE(2, list(value(0), value(2), value(7)))
POPVALUE(7)
//  |    0    1                            2                        3   4    5    6    
//  +-> date [open,close,lowest,highest]  [date, volume, (1 or -1)] MA5 MA10 MA20 MA30

// chart
CHART(
    theme("dark"),
    chartOption({
        "animation": false,
        "legend":{
            "bottom": 10,
            "left": "center",
            "data":["Dow-Jones Index", "MA5", "MA10", "MA20", "MA30"]
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": { "type": "cross" },
            "borderWidth": 1,
            "borderColor": "#ccc",
            "padding": 10,
            "textStyle": {
                "color": "#aaa"
            }
        },
        "axisPointer": {
            "link": [
                { "xAxisIndex": "all"}
            ],
            "label": {
                "backgroundColor": "#aaa"
            }
        },
        "toolbox": {
            "feature": {
                "dataZoom": {
                    "yAxisIndex": false,
                    "title": { "zoom": "zoom", "back": "restore"}
                },
                "brush": {
                    "type": ["lineX", "clear"],
                    "title": { "lineX": "Horizontal selection", "clear": "Clear selection"}
                }
            }
        },
        "brush": {
            "xAxisIndex": "all",
            "brushLink": "all",
            "outOfBrush": {
                "colorAlpha": 0.1
            }
        },
        "visualMap": {
            "show": false,
            "seriesIndex": 1,
            "dimension": 2,
            "pieces": [
                { "value": 1, "color": "#ec0000" }, 
                { "value": -1, "color": "#00da3c" }
            ]
        },
        "grid": [
            {
                "left": "10%",
                "right": "8%",
                "height": "50%"
            },
            {
                "left": "10%",
                "right": "8%",
                "top": "65%",
                "height": "16%"
            }
        ],
        "dataZoom": [
            {
                "type": "inside",
                "xAxisIndex": [0, 1],
                "start": 98,
                "end": 100
            },
            {
                "show": true,
                "type": "slider",
                "xAxisIndex": [0, 1],
                "top": "85%",
                "start": 98,
                "end": 100
            }
        ],
        "xAxis": [
            {
                "type": "category",
                "data": value(0),
                "boundaryGap": false,
                "axisLine": {"onZero": false},
                "splitLine": {"show": false},
                "min": "dataMin",
                "max": "dataMax",
                "axisPointer": {
                    "z": 100
                }
            },
            {
                "type": "category",
                "gridIndex": 1,
                "data": value(0),
                "boundaryGap": false,
                "axisLine": { "onZero": false },
                "axisTick": { "show": false },
                "splitLine": { "show": false },
                "axisLabel": { "show": false},
                "min": "dataMin",
                "max": "dataMax",
                "axisPointer": {
                    "z": 100
                }
            }
        ],
        "yAxis": [
            {
                "scale": true,
                "splitArea": {
                    "show": true
                }
            },
            {
                "scale": true,
                "gridIndex": 1,
                "splitNumber": 2,
                "axisLabel": { "show": false },
                "axisLine": { "show": false },
                "axisTick": { "show": false },
                "splitLine": { "show": false }
            }
        ],
        "series": [
            {
                "name": "Dow-Jones Index",
                "type": "candlestick",
                "data": value(1),
                "smooth": true,
                "itemStyle": {
                    "color": "#00da3c",
                    "color0": "#ec0000",
                    "borderColor": "#00da3c",
                    "borderColor0": "#ec0000"
                }
            },
            {
                "name": "Volume",
                "type": "bar",
                "data": value(2),
                "xAxisIndex": 1,
                "yAxisIndex": 1
            },
            {
                "name": "MA5",
                "type": "line",
                "data": value(3),
                "lineStyle": {
                    "opacity": 0.5
                }
            },
            {
                "name": "MA10",
                "type": "line",
                "data": value(4),
                "lineStyle": {
                    "opacity": 0.5
                }
            },
            {
                "name": "MA20",
                "type": "line",
                "data": value(5),
                "lineStyle": {
                    "opacity": 0.5
                }
            },
            {
                "name": "MA30",
                "type": "line",
                "data": value(6),
                "lineStyle": {
                    "opacity": 0.5
                }
            }
        ]
    })
)
```

![candlestick_marketindex](../../img/stock_dji.jpg)