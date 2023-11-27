---
title: Basic Line Chart
type: docs
weight: 10
---

```js
FAKE( linspace(0, 360, 100) )
MAPVALUE( 2, sin((value(0)/180)*PI) )
CHART(
    theme("dark"),
    series(
        {"type": "value"},
        {"type": "line", "name": "value"}
    )
)
```

![basic_line](../../img/basic_line.jpg)