---
title: Iris Sepal Length
type: docs
weight: 110
---

- Line 6: `BOXPLOT()` is available {{< neo_since ver="8.0.15" />}}.
- Line 7: `value(0)` sepal length
- Line 8: `value(4)` species
- Line 10: `boxplotOutput("chart")` makes `BOXPLOT()` to yield records those formats are fit to echarts.
- Line 19: a series for the boxplot.
- Line 20: column().flat() is required to display outlier points.

```js {linenos=table,hl_lines=[7,8,10,19,20]}
CSV(file("https://machbase.com/assets/example/iris.csv"))
MAPVALUE(4, "SETOSA", where(value(4) == "Iris-setosa"))
MAPVALUE(4, "VERSICOLOR", where(value(4) == "Iris-versicolor"))
MAPVALUE(4, "VIRGINICA", where(value(4) == "Iris-virginica"))

BOXPLOT(
    value(0),
    category(value(4)),
    order("SETOSA", "VERSICOLOR"),
    boxplotOutput("chart")
)

CHART(
    chartOption({
        grid: { bottom: "15%" },
        xAxis:{ type:"category", boundaryGap: true, data: column(0) },
        yAxis:{ type:"value", name: "sepal length", min:4, max:8, splitArea:{ show: true } },
        series:[
            { name: "sepal length", type:"boxplot", data: column(1)},
            { name: "outlier", type:"scatter", data: column(2).flat()},
        ],
        tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
        legend: {show: true, bottom:'2%'},
        title:[ { text: "Iris Sepal Length", left: "center" } ]
    })
)
```

{{< figure src="../../img/boxplot_iris_sepal_length.jpg" width="500" >}}
