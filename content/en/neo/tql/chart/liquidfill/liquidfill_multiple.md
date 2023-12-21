---
title: Liquidfill Multiple Waves
type: docs
weight: 510
---

```js
FAKE(json({
    [0.6, 0.5, 0.4, 0.3]
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

{{< figure src="../../img/liquidfill_multiple.jpg" width="500" >}}
