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
                "data": value(0),
                "amplitude": 0,
                "waveAnimation": 0
            }
        ]
    })
)
```

![basic_line](../../img/liquidfill_still.jpg)