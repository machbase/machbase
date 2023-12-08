---
title: Basic Mix
type: docs
weight: 900
---

```js
FAKE( linspace(0, 360, 50))
MAPVALUE(1, sin((value(0)/180)*PI))
MAPVALUE(2, cos((value(0)/180)*PI))
CHART(
    theme("dark"),
    chartOption({
        "xAxis": { "data": value(0) },
        "yAxis": {},
        "series": [
            {"type": "bar", "name": "SIN", "data": value(1)},
            {"type": "line", "name": "COS", "color":"#093", "data": value(2)}
        ]
    })
)
```

![basic_mix](../../img/basic_mix.jpg)