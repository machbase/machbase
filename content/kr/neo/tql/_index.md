---
title: TQL
type: docs
weight: 70
---

센서에서 전송된 데이터를 원하는 형태로 읽고 변환하시거나,
데이터베이스에 저장된 값을 다른 시스템이 요구하는 형식으로 전달하시려면 전용 도구가 필요합니다.
TQL은 이러한 데이터를 쉽고 유연하게 가공하실 수 있도록 제공되는 Machbase의 변환 언어입니다.

### 출력 형식과 무관하게 사용

{{< tabs items="CSV,JSON,CHART,HTML">}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
CSV( timeformat("Default") )
```
{{< figure src="./img/tql_intro_csv.jpg">}}
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
JSON( timeformat("Default") )
```
{{< figure src="./img/tql_intro_json.jpg">}}
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2-9],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
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
{{< /tab >}}
{{< tab >}}
```html {linenos=table,hl_lines=[2],linenostart=1}
SQL(`SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100`)
HTML({
  {{if .IsFirst }}
    <table>
    <tr>
        <th>TIME</th><th>VALUE</th>
    </tr>
  {{end}}
    <tr>
        <td>{{.V.TIME}}</td><td>{{.V.VALUE}}</td>
    </tr>
  {{if .IsLast }}
    </table>
  {{end}}
})
```
{{< figure src="./img/tql_intro_html.jpg">}}
{{< /tab >}}
{{< /tabs >}}

### 입력 소스와 무관하게 사용

{{< tabs items="JSON,CSV,SQL,SCRIPT-json,SCRIPT-for">}}
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
{{< /tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-4"]}}
CSV(`A,1.0
B,1.5
C,2.0
D,2.5`, field(1, floatType(), "value"))

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{< /tab >}}
{{< tab >}}
```js  {{linenos="table",hl_lines=[1]}}
SQL(`select time, value from example where name = 'my-car' limit 4`)

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{< /tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=[2]}}
SCRIPT({
    list = JSON.parse(`[["A",1.0], ["B",1.5], ["C",2.0], ["D",2.5]]`);
    for( v of list) {
        $.yield(v[0], v[1])
    }
})
MAPVALUE(1, value(1) * 10 )
CSV()
```
{{< /tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-5"]}}
SCRIPT({
    for (i = 0; i < 10; i++) {
        $.yield("script", Math.random())
    }
})

MAPVALUE(1, value(1) * 10 )

CSV()
{{< /tab >}}
{{< /tabs >}}

*TQL*의 목적은 데이터를 손쉽게 변환하는 것입니다.
추가 애플리케이션 개발 없이도 다양한 형태로 데이터를 가공할 수 있는 방법을 이 장에서 소개합니다.

### N:M 변환

{{< figure src="/images/tql-concept.png" caption="TQL Concept" >}}

### Iris

아래 Iris 데이터 예제를 통해 TQL이 어떤 용도로 사용되는지 간단히 살펴볼 수 있습니다.

{{< tabs items="AVG,STAT,SCRIPT-bar,SCRIPT-boxplot">}}
{{< tab >}}

- 클래스별 평균값

```js {{linenos="table"}}
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
{{< /tab >}}
{{< tab >}}

- setosa 클래스의 꽃받침 길이에 대한 최소, 중앙값, 평균, 최대, 표준편차

```js {{linenos="table"}}
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
{{< /tab >}}

{{< tab >}}

- 자바스크립트를 활용해 각 품종의 최소/최대 값을 한꺼번에 계산합니다.

```js {{linenos="table"}}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
SCRIPT({
    var board = {};
},{
    species = $.values[4];
    o = board[species];
    if(o === undefined) {
        o = {
            sepalLength: [],
            sepalWidth: [],
            petalLength: [],
            petalWidth: [],
        };
        board[species] = o;
    }
    o.sepalLength.push(parseFloat($.values[0]));
    o.sepalWidth.push(parseFloat($.values[1]));
    o.petalLength.push(parseFloat($.values[2]));
    o.petalWidth.push(parseFloat($.values[3]))
},{
    chart = {
        xAxis: {type: "category", data:[]},
        yAxis: {},
        legend: {show:true},
        series: [
            {type: "bar", name: "min. sepal L.", data:[]},
            {type: "bar", name: "max. sepal L.", data:[]},
            {type: "bar", name: "min. sepal W.", data:[]},
            {type: "bar", name: "max. sepal W.", data:[]},
            {type: "bar", name: "min. petal L.", data:[]},
            {type: "bar", name: "max. petal L.", data:[]},
            {type: "bar", name: "min. petal W.", data:[]},
            {type: "bar", name: "max. petal W.", data:[]},
        ],
    };
    for( s in board) {
        o = board[s];
        chart.xAxis.data.push(s);
        chart.series[0].data.push(Math.min(...o.sepalLength));
        chart.series[1].data.push(Math.max(...o.sepalLength));
        chart.series[2].data.push(Math.min(...o.sepalWidth));
        chart.series[3].data.push(Math.max(...o.sepalWidth));
        chart.series[4].data.push(Math.min(...o.petalLength));
        chart.series[5].data.push(Math.max(...o.petalLength));
        chart.series[6].data.push(Math.min(...o.petalWidth));
        chart.series[7].data.push(Math.max(...o.petalWidth));
    }
    $.yield(chart);
})
CHART()
```

{{< figure src="./img/iris_script_min_max.jpg" width="500" >}}

{{< /tab >}}
{{< tab >}}

- 사분위수 기반 상자 그림(boxplot)을 생성합니다.

```js {{linenos="table"}}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
SCRIPT({
    var board = {};
},{
    species = $.values[4];
    o = board[species];
    if(o === undefined) {
        o = {
            sepalLength: [],
            sepalWidth: [],
            petalLength: [],
            petalWidth: [],
        };
        board[species] = o;
    }
    o.sepalLength.push(parseFloat($.values[0]));
    o.sepalWidth.push(parseFloat($.values[1]));
    o.petalLength.push(parseFloat($.values[2]));
    o.petalWidth.push(parseFloat($.values[3]))
},{
    chart = {
        title: {text: "Iris Sepal/Petal Length", left: "center"},
        grid: {bottom: "10%"},
        xAxis: {type: "category", data:[], boundaryGap: true},
        yAxis: {type: "value", splitArea:{show:true}},
        legend: {show:true, bottom:"2%"},
        tooltip: {trigger: "item", axisPointer:{type:"shadow"}},
        series: [
            {type: "boxplot", name: "sepal length", data:[]},
            {type: "boxplot", name: "petal length", data:[]},
        ],
    };
    const ana = require("@jsh/analysis");
    for( s in board) {
        o = board[s];
        chart.xAxis.data.push(s);
        // sepal length
        o.sepalLength = ana.sort(o.sepalLength)
        min = Math.min(...o.sepalLength);
        max = Math.max(...o.sepalLength);
        q1 = ana.quantile(0.25, o.sepalLength);
        q2 = ana.quantile(0.5, o.sepalLength);
        q3 = ana.quantile(0.75, o.sepalLength);
        chart.series[0].data.push([min, q1, q2, q3, max]);
        // petal length
        o.petalLength = ana.sort(o.petalLength)
        min = Math.min(...o.petalLength);
        max = Math.max(...o.petalLength);
        q1 = ana.quantile(0.25, o.petalLength);
        q2 = ana.quantile(0.5, o.petalLength);
        q3 = ana.quantile(0.75, o.petalLength);
        chart.series[1].data.push([min, q1, q2, q3, max]);
    }
    $.yield(chart);
})
CHART()
```

{{< figure src="./img/iris_script_quantile.jpg" width="500" >}}

{{< /tab >}}
{{< /tabs >}}

## 이 장에서 다루는 내용

{{< children_toc />}}
