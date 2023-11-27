---
title: Basic Bar Chart
type: docs
weight: 110
---

```js
FAKE( linspace(0, 360, 50) )
MAPVALUE( 2, sin((value(0)/180)*PI) )
CHART(
    theme("dark"),
    series(
        {"type": "value"},
        {"type": "bar", "name": "value"}
    )
)
```

![basic_line](../../img/basic_bar.jpg)