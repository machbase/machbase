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
CSV(file("https://machbase.com/assets/example/iris.csv"),
    field(0, doubleType(), "sepal length"),
    field(1, doubleType(), "sepal width"),
    field(2, doubleType(), "petal length"),
    field(3, doubleType(), "petal width"),
    field(4, stringType(), "species")
)
POPKEY(4)
GROUPBYKEY("avg", "avg", "avg", "avg")
PUSHKEY("result")
CHART_BAR()
```
![groupbykey_stddev](./img/groupbykey_avg.jpg)
{{</ tab >}}
{{< tab >}}
```js
CSV(file("https://machbase.com/assets/example/iris.csv"),
    field(0, doubleType(), "sepal length"),
    field(1, doubleType(), "sepal width"),
    field(2, doubleType(), "petal length"),
    field(3, doubleType(), "petal width"),
    field(4, stringType(), "species")
)
POPKEY(4)
GROUPBYKEY("stddev", "stddev", "stddev", "stddev")
PUSHKEY("result")
CHART_BAR()
```
![groupbykey_stddev](./img/groupbykey_stddev.jpg)
{{</ tab >}}
{{</ tabs >}}