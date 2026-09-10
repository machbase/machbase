---
title: アヤメのがく片の長さ
type: docs
weight: 110
toc: true
---

- 4行目：`BOXPLOT()` が使用可能です {{< neo_since ver="8.0.15" />}}.
- 5行目：`value(0)` はがく片の長さです。
- 6行目：`value(4)` は品種です。
- 8行目：`boxplotOutput("chart")` を指定すると、`BOXPLOT()` はEChartsに適した形式でレコードを出力します。
- 17行目：箱ひげ図の系列です。
- 18行目：外れ値の点を表示するには `column().flat()` が必要です。

```js {linenos=table,hl_lines=[5,6,8,17,18]}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
MAPVALUE(4, strToUpper(strTrimPrefix(value(4), "Iris-")))

BOXPLOT(
    value(0),
    category(value(4)),
    order("SETOSA", "VERSICOLOR", "VIRGINICA"),
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

{{< figure src="/neo/tql/chart/img/boxplot_iris_sepal_length.jpg" width="500" >}}
