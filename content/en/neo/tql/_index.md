---
title: TQL
type: docs
weight: 40
---

It is required to properly read (translate) data that is sent from sensors.
And also read and send data from database to other systems in demanded format.

The purpose of *TQL* is transforming data format.
This chapter shows how to do this without developing additional applications.

{{< figure src="/images/tql-concept.png" caption="TQL Concept" >}}

## Iris

The example tql code below gives a brief idea of what is TQL for.

{{< tabs items="AVG,STDDEV">}}
{{< tab >}}
```js
CSV(file("https://machbase.com/assets/example/iris.csv"))
GROUP( by(value(4), "species"),
    avg(value(0), "Avg. Sepal L."),
    avg(value(1), "Avg. Sepal W."),
    avg(value(2), "Avg. Petal L."),
    avg(value(3), "Avg. Petal W.")
)
CHART_BAR()
```
![groupbykey_stddev](./img/groupbykey_avg.jpg)
{{</ tab >}}
{{< tab >}}
```js
CSV(file("https://machbase.com/assets/example/iris.csv"))
GROUP( by(value(4), "species"),
    stddev(value(0), "Stddev Sepal L."),
    stddev(value(1), "Stddev Sepal W."),
    stddev(value(2), "Stddev Petal L."),
    stddev(value(3), "Stddev Petal W.")
)
CHART_BAR()
```
![groupbykey_stddev](./img/groupbykey_stddev.jpg)
{{</ tab >}}
{{</ tabs >}}