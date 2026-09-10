---
title: 複数の波を使った水位グラフ
type: docs
weight: 510
toc: true
---

```js {{linenos="table",hl_lines=[6,9]}}
FAKE(json({
    [0.6, 0.5, 0.4, 0.3]
}))
TRANSPOSE()
CHART(
    plugins("liquidfill"),
    chartOption({
        series: [
            { type: "liquidFill", data: column(0) }
        ]
    })
)
```

{{< figure src="/neo/tql/chart/img/liquidfill_multiple.jpg" width="500" >}}
