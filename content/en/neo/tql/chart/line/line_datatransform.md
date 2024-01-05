---
title: Data transform
type: docs
weight: 90
---

```js
CSV( file("https://machbase.com/assets/example/life-expectancy-table.csv") )
DROP(1) // skip header line
// |   0          1                 2            3         4
// +-> income     life expectancy   population   Country   Year
// |
POPVALUE(1,2)
// |   0          1         2
// +-> income     Country   Year
// |
FILTER( value(1) in ("Germany", "France") )
// |   0          1         2
// +-> income     Country   Year
// |
MAPVALUE(0, parseFloat(value(0)))
// |   0          1         2
// +-> income     Country   Year
// |
MAPVALUE(3, value(1) == "Germany" ? value(0) : 0)
MAPVALUE(4, value(1) == "France" ? value(0) : 0)
// |   0          1         2         3            4
// +-> income     Country   Year   Germany-income  France-income
// |
GROUP( by(value(2)), max(value(3)), max(value(4)) )
// |   0      1               2
// +-> Year   Germany-income  France-income
// |
CHART(
    chartOption({
        xAxis: { name: "Year", type: "category", data: column(0) },
        yAxis: { name: "Income"},
        legend: { show: true },
        tooltip: {
            trigger: "axis",
            formatter:"{b}<br/> {a0}:{c0}<br/> {a1}:{c1}"
        },
        series: [
            {
                type: "line",
                name: "Germany",
                showSymbol: false,
                data: column(1),
                tooltip: ["income"]
            },
            {
                type: "line",
                name: "France",
                showSymbol: false,
                data: column(2),
                tooltip: ["income"]
            }
        ]
    })
)
```

{{< figure src="../../img/line_datatransform.jpg" width="500" >}}