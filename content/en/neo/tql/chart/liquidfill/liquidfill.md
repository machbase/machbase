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
    plugins("liquidfill"),
    chartOption({
        "series": [
            { "type": "liquidFill", "data": column(0) }
        ]
    })
)
```

![basic_line](../../img/liquidfill_still.jpg)