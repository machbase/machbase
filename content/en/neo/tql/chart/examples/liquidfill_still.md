---
title: Liquidfill Still Wave
type: docs
weight: 520
---

```js
FAKE(json({
    [0.6, 0.5, 0.4, 0.3]
}))
TRANSPOSE()
CHART(
    theme("dark"),
    plugins("liquidfill"),
    chartOption({
        "series": [
            { "type": "liquidFill", "data": value(0) }
        ]
    })
)
```

![basic_line](../../img/liquidfill_still.jpg)
