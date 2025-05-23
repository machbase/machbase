---
title: Basic Line Chart
type: docs
weight: 10
---

## SRC :: FAKE()

```js {linenos=table,linenostart=1}
FAKE( linspace(0, 360, 100))
// |   0
// +-> x
// |
MAPVALUE(1, sin((value(0)/180)*PI))
// |   0   1
// +-> x   sin(x)
// |
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

{{< figure src="../../img/basic_line.jpg" width="500" >}}

## SRC :: SCRIPT()

```js
SCRIPT({
    for( x = 0; x < 360; x+=3.6) {
        $.yield(x, Math.sin(x/180*Math.PI));
    }
})
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

## SRC :: SQL()

{{% steps %}}

### Prepare data

```js {linenos=table,linenostart=1}
FAKE( arrange(1, 100, 1))
// |   0
// +-> seq
// |
MAPVALUE(1, sin((2*PI*value(0)/100)))
// |   0       1
// +-> seq     value
// |
MAPVALUE(0, timeAdd("now-100s", strSprintf("+%.fs", value(0))))
// |   0       1
// +-> time    value
// |
PUSHVALUE(0, "chart-line")
// |   0       1       2
// +-> name    time    value
// |
APPEND(table("example"))
```

### SQL() to CHART()

```js {linenos=table,hl_lines=[4,10],linenostart=1}
SQL(`select time, value from example where name = 'chart-line'`)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0).map((v, idx) => [v, column(1)[idx]])
            }
        ]
    })
)
```

{{% /steps %}}

{{< figure src="../../img/basic_line_sql.jpg" width="500" >}}
