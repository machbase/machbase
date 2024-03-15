---
title: Iris Sepal Length
type: docs
weight: 110
---

- Line 3: `BOXPLOT()` is available {{< neo_since ver="8.0.15" />}}.
- Line 4: `value(0)` sepal length
- Line 5: `value(4)` species
- Line 7: `boxplotOutput("chart")` makes `BOXPLOT()` to yield records those formats are fit to echarts.
- Line 18: a series for the boxplot.
- Line 19: column().flat() is required to display outlier points.

```js {linenos=table,hl_lines=[4,5,7,18,19]}
CSV(file("https://machbase.com/assets/example/iris.csv"))

BOXPLOT(
    value(0),
    category(value(4)),
    order("Iris-setosa", "Iris-Vericolor"),
    boxplotOutput("chart")
)

MAPVALUE(0, strToUpper(strTrimPrefix(value(0), "Iris-")))

CHART(
    chartOption({
        grid: { bottom: "15%" },
        xAxis:{ type:"category", boundaryGap: true, data: column(0) },
        yAxis:{ type:"value", name: "sepal length", min:4, max:8, splitArea:{ show: true } },
        series:[
            { name: "sepal length", type:"boxplot", data: column(1) },
            { name: "outlier", type:"scatter", data: column(2).flat() },
        ],
        tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
        legend: {show: true, bottom:'2%'},
        title:[ { text: "Iris Sepal Length", left: "center" } ]
    })
)
```

{{< figure src="../../img/boxplot_iris_sepal_length.jpg" width="500" >}}
