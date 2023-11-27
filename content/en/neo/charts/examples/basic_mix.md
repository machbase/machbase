---
title: Basic Scatter Chart
type: docs
weight: 900
---

```js
FAKE( linspace(0, 360, 50))
MAPVALUE(1, sin((value(0)/180)*PI))
MAPVALUE(2, cos((value(0)/180)*PI))
CHART(
    theme("dark"),
    series(
        {"type": "value"},
        {"type": "bar", "name": "SIN"},
        {"type": "line", "name": "COS", "color":"#093"}
    )
)
```

![basic_mix](../../img/basic_mix.jpg)