---
title: Liquidfill
type: docs
weight: 500
---

```js
FAKE(json({
    [0.6]
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