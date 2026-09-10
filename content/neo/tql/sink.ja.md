---
title: SINK
type: docs
weight: 21
toc: true
---

すべての *tql* スクリプトは、いずれか1つのシンク（SINK）関数で終える必要があります。

`INSERT()` は、入力レコードをMachbase Neoデータベースに保存する基本的なシンクです。`CHART()` は入力レコードをさまざまなチャートとして描画し、`JSON()` と `CSV()` は適切な形式にエンコードします。

![tql_sink](/neo/tql/img/tql_sink.jpg)

## INSERT()

*構文*: `INSERT( [bridge(),] columns..., table() [, tag()] )`

`INSERT()` は、入力レコードごとに `INSERT` 文を実行して、指定したデータベーステーブルに保存します。

- `bridge()` *bridge('name')*：省略可能です。
- `columns` *string*：カラム名のリスト。
- `table()` *table('name')*：保存先のテーブル名を指定します。
- `tag()` *tag('name')*：省略可能です。タグテーブルにのみ使用できます。


{{< tabs >}}
{{< tab name="例" >}}
タグ名を含むレコードをMachbaseに書き込みます。

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582790, 23.45],
    ["temperature", 1708582791, 24.56]
}))
MAPVALUE(1, value(1)*1000000000) // エポック秒をナノ秒に変換
INSERT("name", "time", "value", table("example"))
```
{{</tab>}}
{{< tab name="PUSHVALUE()" >}}
`PUSHVALUE()` で "name" フィールドを追加し、同じタグ名でレコードをMachbaseに書き込みます。
```js {{linenos=table,hl_lines=[5,7]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
PUSHVALUE(0, "temperature")
MAPVALUE(1, value(1)*1000000000) // エポック秒をナノ秒に変換
INSERT("name","time", "value", table("example"))
```
{{</tab>}}
{{< tab name="tag()" >}}
保存先がタグテーブルの場合、`tag()` オプションを使って同じタグ名でレコードをMachbaseに書き込めます。
```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
MAPVALUE(0, value(0)*1000000000) // エポック秒をナノ秒に変換
INSERT("time", "value", table("example"), tag('temperature'))
```
{{</tab>}}
{{</tabs>}}

ブリッジ接続したデータベースにレコードを挿入します。

```js {{linenos=table,hl_lines=[2]}}
INSERT(
    bridge("sqlite"),
    "company", "employee", "created_on", table("mem_example")
)
```

## APPEND()

*構文*: `APPEND( table() )`

`APPEND()` は、Machbase Neoのappendメソッドで入力レコードを指定したデータベーステーブルに保存します。

- `table()` *table(string)*：保存先のテーブルを指定します。

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582794, 12.34],
    ["temperature", 1708582795, 13.45]
}))
MAPVALUE(1, value(1)*1000000000 ) // エポック秒をナノ秒に変換
APPEND( table("example") )
```

## CSV()

*構文*: `CSV( [tz(), timeformat(), precision(), rownum(), heading(), delimiter(), nullValue(), binaryformat() ] )`

結果のレコードをCSV形式で出力します。各レコードの値がCSV行のフィールドになります。
末尾の連続する2つの改行文字（`\n\n`）がデータの終端を示します。

たとえば、レコードが `{key: k, value:[v1,v2]}` の場合、CSVレコード `v1,v2` を生成します。

- `tz` *tz(name)*：タイムゾーン。既定値は `tz('UTC')` です。
- `timeformat` *timeformat(string)*：DATETIMEフィールドの出力形式。既定値は `timeformat('ns')` です。
- `rownum` *rownum(boolean)*：行番号カラムを追加します。
- `precision` *precision(int)*：浮動小数点フィールドの精度。`precision(-1)` は制限なし、`precision(0)` は整数に変換します。
- `heading` *heading(boolean)*：先頭行にフィールド名を追加します。
- `delimiter` *delimiter(string)*：フィールドの区切り文字を指定します。既定値はカンマ（`,`）です。
- `nullValue()`：*NULL* の代替文字列。既定値は `nullValue('NULL')` です。{{< neo_since ver="8.0.14" />}}
- `cache()`：結果データをキャッシュします。詳細は[結果データのキャッシュ](../reading/#cache-result-data)を参照してください。{{< neo_since ver="8.0.43" />}}
- `binaryformat()` *binaryformat(string)*：BINARYカラムのエンコード形式。`hex`、`base64`、`bytes`、`preview` をサポートします。{{< neo_since ver="8.5.2" />}}

{{< tabs >}}
{{< tab name="既定" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
CSV()
```
```csv
1,10
2,20
3,30
```
{{</ tab >}}
{{< tab name="heading()" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true) )
```
```csv
x,x10
1,10
2,20
3,30
```
{{</ tab >}}
{{< tab name="delimiter()" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true), delimiter("|") )
```
```csv
x|x10
1|10
2|20
3|30
```
{{</ tab >}}
{{< tab name="nullValue()" >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
FAKE( json({ ["A", 123], ["B", null], ["C", 234] }) )
CSV( nullValue("***") )
```
```csv
A,123
B,***
C,234
```
{{</ tab >}}
{{</ tabs >}}

## JSON()

*構文*: `JSON( [transpose(), tz(), timeformat(), precision(), rownum(), rowsFlatten(), rowsArray(), binaryformat() ] )`

レコードの値からJSON形式の結果を生成します。

- `transpose` *transpose(boolean)*：行と列を転置します。多くのチャートライブラリでは `transpose(true)` が便利です。
- `tz` *tz(name)*：タイムゾーン。既定値は `tz('UTC')` です。
- `timeformat` *timeformat(string)*：DATETIMEフィールドの出力形式。既定値は `timeformat('ns')` です。
- `rownum` *rownum(boolean)*：行番号カラムを追加します。
- `precision` *precision(int)*：浮動小数点フィールドの精度。`precision(-1)` は制限なし、`precision(0)` は整数に変換します。
- `rowsFlatten` *rowsFlatten(boolean)*：JSONオブジェクトの *rows* フィールドの配列の次元を減らします。`JSON()` に `transpose(true)` と `rowsFlatten(true)` を両方指定した場合、`rowsFlatten(true)` は無視され、`transpose(true)` だけが適用されます。{{< neo_since ver="8.0.12" />}}
- `rowsArray` *rowsArray(boolean)*：各レコードをオブジェクトとする配列を生成します。`rowsArray(true)` は `transpose(true)` と `rowsFlatten(true)` より優先されます。{{< neo_since ver="8.0.12" />}}
- `cache()`：結果データをキャッシュします。詳細は[結果データのキャッシュ](../reading/#cache-result-data)を参照してください。{{< neo_since ver="8.0.43" />}}
- `binaryformat()` *binaryformat(string)*：BINARYカラムのエンコード形式。`hex`、`base64`、`bytes`、`preview` をサポートします。{{< neo_since ver="8.5.2" />}}

{{< tabs >}}
{{< tab name="既定" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
JSON()
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "column" ],
        "types": [ "double", "double" ],
        "rows": [ [ 1, 10 ], [ 2, 20 ], [ 3, 30 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "228.541µs"
}
```
{{</ tab >}}
{{< tab name="transpose()" >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( transpose(true) )
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "cols": [ [ 1, 2, 3 ], [ 10, 20, 30 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "121.375µs"
}
```
{{</ tab >}}
{{< tab name="rowsFlatten()" >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsFlatten(true) )
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "rows": [ 1, 10, 2, 20, 3, 30 ]
    },
    "success": true,
    "reason": "success",
    "elapse": "130.916µs"
}
```
{{</ tab >}}
{{< tab name="rowsArray()" >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsArray(true) )
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "rows": [ { "x": 1, "x10": 10 }, { "x": 2, "x10": 20 }, { "x": 3, "x10": 30 } ]
    },
    "success": true,
    "reason": "success",
    "elapse": "549.833µs"
}
```
{{</ tab >}}
{{</ tabs >}}

## NDJSON()

*構文*: `NDJSON( [tz(), timeformat(), rownum(), binaryformat()] )` {{< neo_since ver="8.0.33" />}}

レコードの値からNDJSON形式の結果を生成します。

NDJSON（Newline Delimited JSON）は、各行が有効なJSONオブジェクトである、JSONデータのストリーミング形式です。JSONオブジェクトを1つずつ扱えるため、大規模なデータセットやストリーミングデータの処理に適しています。
末尾の連続する2つの改行文字（`\n\n`）がデータの終端を示します。

- `tz` *tz(name)*：タイムゾーン。既定値は `tz('UTC')` です。
- `timeformat` *timeformat(string)*：DATETIMEフィールドの出力形式。既定値は `timeformat('ns')` です。
- `rownum` *rownum(boolean)*：行番号カラムを追加します。
- `cache()`：結果データをキャッシュします。詳細は[結果データのキャッシュ](../reading/#cache-result-data)を参照してください。{{< neo_since ver="8.0.43" />}}
- `binaryformat()` *binaryformat(string)*：BINARYカラムのエンコード形式。`hex`、`base64`、`bytes`、`preview` をサポートします。{{< neo_since ver="8.5.2" />}}

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL(`select * from example where name = 'neo_load1' limit 3`)
NDJSON(timeformat('Default'), tz('local'), rownum(true))
```

```json
{"NAME":"neo_load1","ROWNUM":1,"TIME":"2024-09-06 14:46:19.852","VALUE":4.58}
{"NAME":"neo_load1","ROWNUM":2,"TIME":"2024-09-06 14:46:22.853","VALUE":4.69}
{"NAME":"neo_load1","ROWNUM":3,"TIME":"2024-09-06 14:46:25.852","VALUE":4.69}

```

## MARKDOWN()

Markdown形式またはHTML形式の表を生成します。

*構文*: `MARKDOWN( [ options... ] )`

- `tz(string)`：タイムゾーン。既定値は `tz('UTC')` です。
- `timeformat(string)`：DATETIMEフィールドの出力形式。既定値は `timeformat('ns')` です。
- `html(boolean)`：HTMLレンダラーで結果を生成します。既定値は `false` です。
- `rownum(boolean)`：行番号カラムを表示します。
- `precision` *precision(int)*：浮動小数点フィールドの精度。`precision(-1)` は制限なし、`precision(0)` は整数に変換します。
- `brief(boolean)`：結果行を省略します。`brief(true)` は `briefCount(5)` と同じです。
- `briefCount(limit int)`：レコード数が指定した上限を超えると、結果行を省略します。`0` の場合は省略しません。
- `binaryformat()` *binaryformat(string)*：BINARYカラムのエンコード形式。`hex`、`base64`、`bytes`、`preview` をサポートします。{{< neo_since ver="8.5.2" />}}

{{< tabs >}}
{{< tab name="既定" >}}
```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN()
```
```
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| 30     | Third line |
| 40     | 4th line |
| 50     | The last is 5th |
```
{{< /tab >}}
{{< tab name="briefCount" >}}

```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2) )
```

```
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records
```
{{< /tab >}}
{{< tab name="html" >}}

```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2), html(true) )
```

|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records

{{< /tab >}}
{{< /tabs >}}

## HTML()

*構文*: `HTML(templates...)` {{< neo_since ver="8.0.52" />}}

指定したテンプレートを使ってHTML文書を生成します。

詳しい使い方と例は [HTML](../html/) を参照してください。

## TEXT()

*構文*: `TEXT(templates...)` {{< neo_since ver="8.0.52" />}}

指定したテンプレートを使ってテキスト文書を生成します。

`HTML()` と同様に動作しますが、データにHTMLエスケープを適用しません。

## DISCARD()

*構文*: `DISCARD()` {{< neo_since ver="8.0.7" />}}

`DISCARD()` は、すべてのレコードを何も出力せずに破棄します。

```js {linenos=table,hl_lines=[8],linenostart=1}
FAKE( json({
    [ 1, "hello" ],
    [ 2, "world" ]
}))
WHEN( value(0) == 2, do( value(0), strToUpper(value(1)), {
    ARGS()
    WHEN( true, doLog("OUTPUT:", value(0), value(1)) )
    DISCARD()
}))
CSV()
```

## CHART()

*構文*: `CHART()` {{< neo_since ver="8.0.8" />}}

Apache EChartsでチャートを生成します。

さまざまな使用例は [CHART()の例](/neo/tql/chart/)を参照してください。


<!-- ## 非推奨

### CHART_LINE()

> **非推奨**：代わりにCHART()を使用してください。

*構文*: `CHART_LINE()`

HTML形式の折れ線グラフを生成します。

{{< tabs >}}
{{< tab name="CHART_LINE()" >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--&gt; time   value
// |
CHART_LINE(
    size("600px", "400px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--&gt; time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "line",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_line.jpg" width="500" >}}

### CHART_BAR()

> **非推奨**：代わりにCHART()を使用してください。

*構文*: `CHART_BAR()`

HTML形式の棒グラフを生成します。

{{< tabs >}}
{{< tab name="CHART_BAR()" >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--&gt; time   value
// |
CHART_BAR(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--&gt; time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "bar",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_bar.jpg" width="500" >}}

### CHART_SCATTER()

> **非推奨**：代わりにCHART()を使用してください。

*構文*: `CHART_SCATTER()`

HTML形式の散布図を生成します。

{{< tabs >}}
{{< tab name="CHART_SCATTER()" >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--&gt; time   value
// |
CHART_SCATTER(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--&gt; time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "scatter",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_scatter.jpg" width="500" >}}

### CHART_LINE3D()

> **非推奨**：代わりにCHART()を使用してください。

*構文*: `CHART_LINE3D()`

HTML形式の3D折れ線グラフを生成します。

{{< tabs >}}
{{< tab name="CHART_LINE3D()" >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--&gt; x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--&gt; x   y   z
// |
CHART_LINE3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=[10, "12-31"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--&gt; x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--&gt; x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "line3D",
        lineStyle: { "width": 2 },
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_line3d.jpg" width="500" >}}


### CHART_BAR3D()

> **非推奨**：代わりにCHART()を使用してください。

*構文*: `CHART_BAR3D()`

HTML形式の3D棒グラフを生成します。

{{< tabs >}}
{{< tab name="CHART_BAR3D()" >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--&gt; x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--&gt; x   y   z
// |
CHART_BAR3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--&gt; x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--&gt; x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "bar3D",
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_bar3d.jpg" width="500" >}}

### CHART_SCATTER3D()

> **非推奨**：代わりにCHART()を使用してください。

*構文*: `CHART_SCATTER3D()`

HTML形式の3D散布図を生成します。

{{< tabs >}}
{{< tab name="CHART_SCATTER3D()" >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--&gt; x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--&gt; x   y   z
// |
CHART_SCATTER3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--&gt; x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--&gt; x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "scatter3D",
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_scatter3d.jpg" width="500" >}}

### title()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `title(label)`

- `label` *string*

### subtitle()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `subtitle(label)`

- `label` *string*

### xAxis(), yAxis(), zAxis()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `xAxis(idx, label [, type])`

- `idx` *number*：軸に使用するカラムのインデックス。
- `label` *string*：軸のラベル。
- `type` *string*：軸の型。`'time'` と `'value'` を指定できます。省略時は `'value'` です。

> zAxis()は3Dチャートでのみ有効です。

### dataZoom()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `dataZoom(type, minPercentage, maxPercentage)`

- `type` *string* "slider", "inside"
- `minPercentage` *number* 0 ~ 100
- `maxPercentage` *number* 0 ~ 100

> 2Dチャート専用です。

### opacity()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `opacity(alpha)`

- `alpha` *number* 0.0 ~ 1.0

> 3Dチャート専用です。

### autoRotate()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `autoRotate( [speed] )`

- `speed` *number*：度/秒。既定値は10です。

### gridSize()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `gridSize( width, height, depth )`

- `width` *number*：割合（既定値：100）。
- `height` *number*：割合（既定値：100）。
- `depth` *number*：割合（既定値：100）。

> 3Dチャート専用です。

### seriesLabels()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `seriesLabels( label... )`

- `label` *string*

各系列のラベル文字列を指定します。

### toolbox

#### toolboxSaveAsImage()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `toolboxSaveAsImage(filename)` {{< neo_since ver="8.0.4" />}}

- `filename` *string*：拡張子を含むファイル名。対応する拡張子は .png、.jpeg、.svg です。

チャートを画像ファイルとして保存するツールボックスボタンを表示します。

#### toolboxDataZoom()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `toolboxDataZoom()` {{< neo_since ver="8.0.4" />}}

データをズームするツールボックスボタンを表示します。

#### toolboxDataView()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `toolboxDataView()` {{< neo_since ver="8.0.4" />}}

生データを表示するツールボックスボタンを表示します。

```js {linenos=table,hl_lines=["6-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '20ms')) )
CHART_LINE( 
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    size('400px', '300px'),
    toolboxSaveAsImage('image.png'),
    toolboxDataZoom(),
    toolboxDataView()
)
```

{{< figure src="/neo/tql/img/sink_chart_toolbox.jpg" width="500" >}}

### visualMap()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `visualMap(min, max)`

- `min` *number*
- `max` *number*

定義済みの既定色を指定して、内部で `visualMapColor()` を呼び出します。

### visualMapColor()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `visualMapColor(min, max, colors...)` {{< neo_since ver="8.0.4" />}}

- `min` *number*
- `max` *number*
- `colors`：色を指定する文字列の配列。

例：

```js {linenos=table,hl_lines=["6-11"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '20ms')) )
CHART_LINE( 
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    visualMapColor(-2.0, 2.0, 
        "#a50026", "#d73027", "#f46d43", "#fdae61", "#e0f3f8", 
        "#abd9e9", "#74add1", "#4575b4", "#313695", "#313695", 
        "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#fdae61",
        "#f46d43", "#d73027", "#a50026"
    )
)
```

{{< figure src="/neo/tql/img/sink_chart_visualMapColor.jpg" width="500" >}}

### markArea()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `markArea(coord0, coord1 [, label [, color [, opacity]]])`

- `coord0` *any*：領域の開始位置のX値。
- `coord1` *any*：領域の終了位置のX値。
- `label` *string*：タイトル。
- `color` *string*：領域の色。
- `opacity` *number*：不透明度（0～1）。

*例*

```js {linenos=table,hl_lines=["6-7"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markArea(time('now+1s'), time('now+2s'), 'Error', '#ff000033'),
    markArea(time('now+1.5s'), time('now+2.5s'), 'Marked', '#22ff0022')
 )
```

{{< figure src="/neo/tql/img/sink_chart_markarea.jpg" width="500" >}}

### markXAxis()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `markXAxis(coord, label)`

- `coord` *any*：マークする位置のX値。
- `label` *string*：タイトル。

```js {linenos=table,hl_lines=[6],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markXAxis(time('now+1.5s'), 'NOW')
)
```

{{< figure src="/neo/tql/img/chart_marker_x.jpg" width="500" >}}

### markYAxis()

> **非推奨**：代わりにCHART()でchartOption()を使用してください。

*構文*: `markYAxis(coord, label)`

- `coord` *any*：マークする位置のY値。
- `label` *string*：タイトル。

```js {linenos=table,hl_lines=[6,7],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markYAxis(1.0, 'max'),
    markYAxis(-1.0, 'min')
)
```

{{< figure src="/neo/tql/img/chart_marker_y.jpg" width="500" >}} -->
