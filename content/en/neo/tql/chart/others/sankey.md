---
title: Sankey
type: docs
weight: 930
---

```js
FAKE(csv(
`a,a1,5
a,a2,3
b,b1,8
a,b1,3
b1,a1,1
b1,c,2
`))
MAPVALUE(0, dict("source", value(0), "target", value(1), "value", value(2)))
POPVALUE(1,2)
CHART(
    chartOption({
        "series": {
            "type": "sankey",
            "layout": "none",
            "emphasis": {
                "focus": "adjacency"
            },
            "links": column(0),
            "data": [
                {"name": "a"}, {"name": "b"}, {"name": "a1"}, {"name": "a2"}, {"name": "b1"}, {"name": "c"}
            ]
        }
    })
)
```

{{< figure src="../../img/sankey.jpg" width="500" >}}
