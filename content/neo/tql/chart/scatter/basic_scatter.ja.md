---
title: 基本的な散布図
type: docs
weight: 300
toc: true
---

```js {{linenos=table,linenostart=1}}
FAKE( linspace(0, 360, 100) )
MAPVALUE( 2, sin((value(0)/180)*PI) )
CHART(
    chartOption({
        xAxis:{ data: column(0) },
        yAxis:{},
        series:[
            { type:"scatter", data: column(1) }
        ]
    })
)
```

{{< figure src="/neo/tql/chart/img/basic_scatter.jpg" width="500" >}}
