---
title: Scatter Band
type: docs
weight: 320
---

```js
FAKE( linspace(0, 10, 10000) )

MAPVALUE(0, random()*10)
MAPVALUE(1, sin(value(0)) - value(0)*(0.1*random()) + 1)
MAPVALUE(2, sin(value(0)) - value(0)*(0.1*random()) - 1)

CHART(
    global({
        "legend": { "show": false },
        "theme": "dark"
    }),
    xAxis(""),
    yAxis(""),
    dataZoom("slider", 0, 100),
    series(
        {   "type": "value"},
        {   "type": "scatter",
            "itemStyle": {
                "color": "#9ECB7F",
                "opacity": 0.3
            }
        },
        {   "type": "scatter",
            "itemStyle": {
                "color": "#5872C0",
                "opacity": 0.3
            }
        }
    )
)
```

![scatter_band](../../img/scatter_band.jpg)