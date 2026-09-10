---
title: 水位グラフ
type: docs
weight: 500
toc: true
---

```js {{linenos="table",hl_lines=[5,8]}}
FAKE(json({
    [0.6]
}))
CHART(
    plugins("liquidfill"),
    chartOption({
        series: [
            { type: "liquidFill", data: column(0) }
        ]
    })
)
```

{{< figure src="/neo/tql/chart/img/liquidfill.jpg" width="500" >}}
