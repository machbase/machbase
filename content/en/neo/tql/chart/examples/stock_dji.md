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
// => date   [open,close,lowest,highest]       volume MA5 MA10 MA20 MA30
MAPVALUE(1, list(value(1), value(2), value(3), value(4)), "DJI")
POPVALUE(2,3,4)

// chart
CHART(
    theme("dark"),
    chartOption({
        "legend":{"bottom": "1%", "left": "center"},
        "grid": [
            {
                "left": "10%",
                "right": "8%",
                "height": "50%"
            },
            {
                "left": "10%",
                "right": "8%",
                "top": "73%",
                "height": "16%"
            }
        ],
        "brush": {
            "xAxisIndex": "all",
            "brushLink": "all",
            "outOfBrush": {
                "colorAlpha": 0.1
            }
        },
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
                "top": "65%",
                "start": 98,
                "end": 100
            }
        ],
        "xAxis": [
            {
                "type": "category",
                "name": "",
                "data": value(0),
                "boundaryGap": false,
                "axisLine": {"onZero": false}
            },
            {
                "type": "category",
                "name": "",
                "gridIndex": 1,
                "data": value(0),
                "axisLine": { "onZero": false },
                "axisLabel": { "show": false}
            }
        ],
        "yAxis": [
            {
                "name": "date",
                "scale": true
            },
            {
                "name": "",
                "scale": true,
                "gridIndex": 1,
                "splitNumber": 2,
                "axisLabel": { "show": false }
            }
        ],
        "series": [
            {
                "name": "Dow-Jones Index",
                "type": "candlestick",
                "data": value(1),
                "smooth": true,
                "itemStyle": {
                    "color": "#ec0000",
                    "color0": "#00da3c",
                    "borderColor": "#ec0000",
                    "borderColor0": "#00da3c",
                    "borderWidth": 0
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