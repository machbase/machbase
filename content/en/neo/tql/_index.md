---
title: TQL
type: docs
weight: 70
---

It is required to properly read and transform data that has been sent by sensors.
And also read and send data from database to other systems in demanded format.

### Output format independent

{{< tabs items="CSV,JSON,CHART">}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select time, value from example where name='signal' limit 100` )
CSV( timeformat("Default") )
```
{{< figure src="./img/tql_intro_csv.jpg">}}
{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select time, value from example where name='signal' limit 100` )
JSON( timeformat("Default") )
```
{{< figure src="./img/tql_intro_json.jpg">}}
{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2-9],linenostart=1}
SQL( `select time, value from example where name='signal' limit 100` )
CHART(
    size("600px", "340px"),
    chartOption({
        xAxis:{data:column(0)},
        yAxis:{},
        series:[ { type:"line", data:column(1)} ]
    })
)
```
{{< figure src="./img/tql_intro.jpg">}}
{{</ tab >}}
{{</ tabs >}}

### Data source independent

{{< tabs items="JSON,CSV,SQL">}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-5"]}}
FAKE( json({ 
    [ "A", 1.0 ],
    [ "B", 1.5 ],
    [ "C", 2.0 ],
    [ "D", 2.5 ] }))

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{</ tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-4"]}}
CSV(`A,1.0
B,1.5
C,2.0
D,2.5`, field(1, floatType(), "value"))

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{</ tab >}}
{{< tab >}}
```js  {{linenos="table",hl_lines=[1]}}
SQL(`select time, value from example where name = 'signal' limit 4`)

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{</ tab >}}
{{</ tabs >}}

The purpose of *TQL* is transforming data format.
This chapter shows how to do this without developing additional applications.

### N:M transforming

{{< figure src="/images/tql-concept.png" caption="TQL Concept" >}}

### Iris

The example tql code below gives a brief idea of what is TQL for.

{{< tabs items="AVG,STAT">}}
{{< tab >}}
- avg. values of each classes.
```js
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
GROUP( by(value(4), "species"),
    avg(value(0), "Avg. Sepal L."),
    avg(value(1), "Avg. Sepal W."),
    avg(value(2), "Avg. Petal L."),
    avg(value(3), "Avg. Petal W.")
)
CHART(
    chartOption({
        "xAxis":{"type": "category", "data": column(0)},
        "yAxis": {},
        "legend": {"show": true},
        "series": [
            { "type": "bar", "name": "Avg. Sepal L.", "data": column(1)},
            { "type": "bar", "name": "Avg. Sepal W.", "data": column(2)},
            { "type": "bar", "name": "Avg. Petal L.", "data": column(3)},
            { "type": "bar", "name": "Avg. Petal W.", "data": column(4)}
        ]
    })
)
```
{{< figure src="./img/groupbykey_avg.jpg" width="500" >}}
{{</ tab >}}
{{< tab >}}
- min, median, avg, max, stddev of sepal length of the setosa class.
```js
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
FILTER( strToUpper(value(4)) == "IRIS-SETOSA")
GROUP( by(value(4)), 
    min(value(0), "Min"),
    median(value(0), "Median"),
    avg(value(0), "Avg"),
    max(value(0), "Max"),
    stddev(value(0), "StdDev.")
)
CHART(
    chartOption({
        "xAxis": { "type": "category", "data": ["iris-setosa"]},
        "yAxis": {},
        "legend": {"show": "true"},
        "series": [
            {"type":"bar", "name": "Min", "data": column(1)},
            {"type":"bar", "name": "Median", "data": column(2)},
            {"type":"bar", "name": "Avg", "data": column(3)},
            {"type":"bar", "name": "Max", "data": column(4)},
            {"type":"bar", "name": "StdDev.", "data": column(5)}
        ]
    })
)
```
{{< figure src="./img/groupbykey_stddev.jpg" width="500" >}}
{{</ tab >}}
{{</ tabs >}}

## In this chapter

{{< children_toc />}}
