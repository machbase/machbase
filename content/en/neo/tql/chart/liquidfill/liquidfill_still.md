---
title: Liquidfill Still Waves
type: docs
weight: 520
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
            {
                "type": "liquidFill",
                "data": column(0),
                "amplitude": 0,
                "waveAnimation": 0
            }
        ]
    })
)
```

{{< figure src="../../img/liquidfill_still.jpg" width="500" >}}
