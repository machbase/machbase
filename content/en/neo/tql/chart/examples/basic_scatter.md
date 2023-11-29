---
title: Basic Scatter Chart
type: docs
weight: 300
---

```js
FAKE( linspace(0, 360, 100) )
MAPVALUE( 2, sin((value(0)/180)*PI) )
CHART(
    theme("dark"),
    series(
        {"type": "value"},
        {"type": "scatter", "name": "value"}
    )
)
```

![basic_line](../../img/basic_scatter.jpg)