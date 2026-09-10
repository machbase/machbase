---
title: TQL
type: docs
weight: 70
toc: true
---

センサーから届くデータを必要な形式で読み取り、変換したり、
データベースに保存した値を他のシステムが要求する形式で渡したりするには、専用のツールが必要です。
TQLは、こうしたデータを簡単かつ柔軟に加工するためのMachbaseの変換言語です。

### サンプルの 'signal' データを生成する {#예제-signal-데이터-생성}

以下の例で使用するサンプルデータをまず生成します。


{{< tabs >}}
{{< tab name="SCRIPT" >}}
```js
SCRIPT({
    const m = require('mathx');
    const gen = m.oscillator({
        components: [
            {frequencyHz: 15, amplitude: 1.0},
            {frequencyHz: 24, amplitude: 1.5},
        ],
        timeRange: {from: 'now', to: 'now+10s'},
        sample: "1000Hz",
    });
    gen.forEach((g)=>{ $.yield(g[0], g[1]) });
})
SQL(`insert into example(name,time,value) values('signal',?,?)`, 
    value(0), value(1))
```
{{</ tab >}}
{{< tab name="FAKE" >}}
```js
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
SQL(`insert into example(name,time,value) values('signal',?,?)`, 
    value(0), value(1))
```
{{</ tab >}}
{{</ tabs >}}

### 出力形式に依存しない処理 {#출력-형식과-무관하게-사용}

{{< tabs >}}
{{< tab name="CSV" >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
CSV( timeformat("Default") )
```
{{< figure src="/neo/tql/img/tql_intro_csv.jpg">}}
{{< /tab >}}
{{< tab name="JSON" >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
JSON( timeformat("Default") )
```
{{< figure src="/neo/tql/img/tql_intro_json.jpg">}}
{{< /tab >}}
{{< tab name="CHART" >}}
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
{{< figure src="/neo/tql/img/tql_intro.jpg">}}
{{< /tab >}}
{{< tab name="HTML" >}}
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
{{< figure src="/neo/tql/img/tql_intro_html.jpg">}}
{{< /tab >}}
{{< /tabs >}}

### 入力ソースに依存しない処理 {#입력-소스와-무관하게-사용}

{{< tabs >}}
{{< tab name="JSON" >}}
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
{{< tab name="CSV" >}}
```js {{linenos="table",hl_lines=["1-4"]}}
CSV(`A,1.0
B,1.5
C,2.0
D,2.5`, field(1, floatType(), "value"))

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{< /tab >}}
{{< tab name="SQL" >}}
```js  {{linenos="table",hl_lines=[1]}}
SQL(`select time, value from example where name = 'my-car' limit 4`)

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{< /tab >}}
{{< tab name="SCRIPT-json" >}}
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
{{< tab name="SCRIPT-for" >}}
```js {{linenos="table",hl_lines=["1-5"]}}
SCRIPT({
    for (i = 0; i < 10; i++) {
        $.yield("script", Math.random())
    }
})

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{< /tab >}}
{{< /tabs >}}

*TQL* の目的は、データを簡単に変換することです。
この章では、追加のアプリケーションを開発せずにデータをさまざまな形式に加工する方法を説明します。

<!-- ### N:M変換

{{< figure src="/images/tql-concept.png" caption="TQL Concept" >}}
-->

### Irisデモ {#iris-demo}

以下のIrisデータの例で、TQLの用途を簡単に確認できます。

{{< tabs >}}
{{< tab name="AVG" >}}

- クラスごとの平均値

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
{{< figure src="/neo/tql/img/groupbykey_avg.jpg" width="500" >}}
{{< /tab >}}
{{< tab name="STAT" >}}

- setosaクラスのがく片の長さの最小値、中央値、平均値、最大値、標準偏差

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
{{< figure src="/neo/tql/img/groupbykey_stddev.jpg" width="500" >}}
{{< /tab >}}

{{< tab name="SCRIPT-bar" >}}

- JavaScriptを使って各品種の最小値と最大値をまとめて計算します。

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

{{< figure src="/neo/tql/img/iris_script_min_max.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="SCRIPT-boxplot" >}}

- 四分位数に基づく箱ひげ図（boxplot）を生成します。

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
    const mx = require("mathx");
    for( s in board) {
        o = board[s];
        chart.xAxis.data.push(s);
        // がく片の長さ
        o.sepalLength = mx.sort(o.sepalLength)
        min = Math.min(...o.sepalLength);
        max = Math.max(...o.sepalLength);
        q1 = mx.quantile(0.25, o.sepalLength);
        q2 = mx.quantile(0.5, o.sepalLength);
        q3 = mx.quantile(0.75, o.sepalLength);
        chart.series[0].data.push([min, q1, q2, q3, max]);
        // 花弁の長さ
        o.petalLength = mx.sort(o.petalLength)
        min = Math.min(...o.petalLength);
        max = Math.max(...o.petalLength);
        q1 = mx.quantile(0.25, o.petalLength);
        q2 = mx.quantile(0.5, o.petalLength);
        q3 = mx.quantile(0.75, o.petalLength);
        chart.series[1].data.push([min, q1, q2, q3, max]);
    }
    $.yield(chart);
})
CHART()
```

{{< figure src="/neo/tql/img/iris_script_quantile.jpg" width="500" >}}

{{< /tab >}}
{{< /tabs >}}

## この章の内容 {#이-장에서-다루는-내용}

{{< children_toc />}}
