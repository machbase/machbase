---
title: SINK
type: docs
weight: 21
---

All *tql* scripts must end with one of the sink functions.

The basic SINK function might be `INSERT()` which write the incoming records onto machbase-neo database. `CHART()` function can render various charts with incoming records. `JSON()` and `CSV()` encode incoming data into proper formats.

![tql_sink](../img/tql_sink.jpg)

## INSERT()

*Syntax*: `INSERT( [bridge(),] columns..., table(), tag() )`

`INSERT()` stores incoming records into specified databse table by an 'INSERT' statement for each record.

- `bridge()` *bridge('name')*
- `columns` *string*
- `table()` *table('name')*
- `tag()` *tag('name')*

*Example)*

- Insert records into machbase

```js
INSERT("time", "value", table("example"), tag('temperature'))
```

- Insert records into bridged database

```js
INSERT(bridge("sqlite"), "company", "employee", "created_on", table("example"))
```

## APPEND()

*Syntax*: `APPEND( table() )`

*APPEND()* stores incoming records into specified databse table via the 'append' method of machbase-neo.

- `table()` *table(string)* specify destination table

## CSV()

*Syntax*: `CSV( [tz(), timeformat(), precision(), rownum(), heading(), delimiter(), substituteNull() ] )`

Makes the records of the result in CSV format. The values of the records become the fields of the CSV lines.

For example, if a record was `{key: k, value:[v1,v2]}`, it generates an CSV records as `v1,v2`.

- `tz` *tz(name)* time zone, default is `tz('UTC')`
- `timeformat` *timeformat(string)* specify the format how represents datetime fields, default is `timeformat('ns')`
- `rownum` *rownum(boolean)* adds rownum column
- `precision` *precision(int)* specify precision of float fields, `precision(-1)` means no restriction, `precision(0)` converts to integer
- `heading` *heading(boolean)* add fields names as the first row
- `delimiter` *delimiter(string)* specify fields separator other than the default comma(`,`).
- `substituteNull` *substitute(string)* specify sustitution string for the *NULL* value, default is `substituteNull('NULL')`


## JSON()

*Syntax*: `JSON( [transpose(), tz(), timeformat(), precision(), rownum() ] )`

Generates JSON results from the values of the records.

- `transpose` *transpose(boolean)* transpose rows and columns, it is useful that specifying `transpose(true)` for the most of chart libraries.
- `tz` *tz(name)* time zone, default is `tz('UTC')`
- `timeformat` *timeformat(string)* specify the format how represents datetime fields, default is `timeformat('ns')`
- `rownum` *rownum(boolean)` adds rownum column
- `precision` *precision(int)* specify precision of float fields, `precision(-1)` means no restriction, `precision(0)` converts to integer


## MARKDOWN()

Generates a table in markdown format or HTML.

*Syntax*: `MARKDOWN( [html(), rownum(), brief(), briefCount() ] )`

- `html(boolean)` produce result by HTML renderer, default `false`
- `rownum(boolean)` show rownum column
- `brief(boolean)` omit result rows, `brief(true)` is equivalent with `briefCount(5)`
- `briefCount(limit int)` omit result rows if the records exceeds the given limit, no omition if limit is `0`

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN()
```
{{< /tab >}}
{{< tab >}}
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| 30     | Third line |
| 40     | 4th line |
| 50     | The last is 5th |
{{< /tab >}}
{{< /tabs >}}


If `briefCount()` is applied...

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2) )
```
{{< /tab >}}
{{< tab >}}
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records
{{< /tab >}}
{{< /tabs >}}

## DISCARD()

*Syntax*: `DISCARD()` {{< neo_since ver="8.0.7" />}}

`DISCARD()` silently ignore all records as its name implies, so that no output generates.

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

*Syntax*: `CHART()` {{< neo_since ver="8.0.8" />}}

Generates chart using Apache echarts.

Refer to [CHART() examples](/neo/tql/chart/) for the various usages.

## CHART_LINE()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_LINE()`

Generates a line chart in HTML format.

{{< tabs items="CHART_LINE(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_LINE(
    size("600px", "400px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
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

{{< figure src="../img/chart_line.jpg" width="500" >}}

## CHART_BAR()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_BAR()`

Generates a bar chart in HTML format.

{{< tabs items="CHART_BAR(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_BAR(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
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

{{< figure src="../img/chart_bar.jpg" width="500" >}}

## CHART_SCATTER()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_SCATTER()`

Generates a scatter chart in HTML format.

{{< tabs items="CHART_SCATTER(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_SCATTER(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
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

{{< figure src="../img/chart_scatter.jpg" width="500" >}}

## CHART_LINE3D()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_LINE3D()`

Generates a 3D line chart in HTML format.

{{< tabs items="CHART_LINE3D(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_LINE3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[10, "12-31"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
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

{{< figure src="../img/chart_line3d.jpg" width="500" >}}


## CHART_BAR3D()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_BAR3D()`

Generates a 3D bar chart in HTML format.

{{< tabs items="CHART_BAR3D(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_BAR3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
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

{{< figure src="../img/chart_bar3d.jpg" width="500" >}}

## CHART_SCATTER3D()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_SCATTER3D()`

Generates a 3D scatter chart in HTML format.

{{< tabs items="CHART_SCATTER3D(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_SCATTER3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
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

{{< figure src="../img/chart_scatter3d.jpg" width="500" >}}

## Chart options

### size()

*Syntax*: `size(width, height)`

- `width` *string* chart width in HTML syntax ex) '800px'
- `height` *string* chart height in HTML syntax ex) '800px'

### title()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `title(label)`

- `label` *string*

### subtitle()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `subtitle(label)`

- `label` *string*

### xAxis(), yAxis(), zAxis()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `xAxis(idx, label [, type])`

- `idx` *number* index of column for the axis
- `label` *string* label of the axis
- `type` *string* type fo the axis, available: `'time'` and `'value'`, default is `'value'` if not specified.

> zAxis() is effective only with 3D chart

### dataZoom()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `dataZoom(type, minPercentage, maxPercentage)`

- `type` *string* "slider", "inside"
- `minPercentage` *number* 0 ~ 100
- `maxPercentage` *number* 0 ~ 100

> 2D chart only

### opacity()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `opacity(alpha)`

- `alpha` *number* 0.0 ~ 1.0

> 3D chart only

### autoRotate()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `autoRotate( [speed] )`

- `speed` *number* degree/sec, default is 10

### gridSize()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `gridSize( width, height, depth )`

- `width` *number* percentage (default: 100)
- `height` *number* percentage (default: 100)
- `depth` *number* percentage (default: 100)

> 3D chart only

### seriesLabels()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `seriesLabels( lable... )`

- `label` *string*

Specify the label text of each series.

### toolbox

#### toolboxSaveAsImage()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `toolboxSaveAsImage(filename)` {{< neo_since ver="8.0.4" />}}

- `filename` *string* filename with extension supporting (.png, .jpeg, .svg).

Show the toolbox button to save chart as an image file.

#### toolboxDataZoom()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `toolboxDataZoom()` {{< neo_since ver="8.0.4" />}}

Show the toolbox button for data zoom.

#### toolboxDataView()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `toolboxDataView()` {{< neo_since ver="8.0.4" />}}

Show the toolbox button for raw data viewer.

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

{{< figure src="../img/sink_chart_toolbox.jpg" width="500" >}}

### visualMap()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `visualMap(min, max)`

- `min` *number*
- `max` *number*

It calls `visualMapColor()` internally with pre-defined default colors.

### visualMapColor()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `visualMapColor(min, max, colors...)` {{< neo_since ver="8.0.4" />}}

- `min` *number*
- `max` *number*
- `colors` *colors in array of string*

Example)

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

{{< figure src="../img/sink_chart_visualMapColor.jpg" width="500" >}}

### markArea()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `markArea(coord0, coord1 [, label [, color [, opacity]]])`

- `coord0` *any* : area begining x-value
- `coord1` *any* : area ending x-value
- `label` *string* : title
- `color` *string* : color of area
- `opacity` *number* : 0~1 of opacity

*Example)*

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

{{< figure src="../img/sink_chart_markarea.jpg" width="500" >}}

### markXAxis()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `markXAxis(coord, label)`

- `coord` *any* : marked x-value
- `label` *string* : title

```js {linenos=table,hl_lines=[6],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markXAxis(time('now+1.5s'), 'NOW')
)
```

{{< figure src="../img/chart_marker_x.jpg" width="500" >}}

### markYAxis()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `markYAxis(coord, label)`

- `coord` *any* : marked y-value
- `label` *string* : title

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

{{< figure src="../img/chart_marker_y.jpg" width="500" >}}

### theme()

*Syntax*: `theme(name)`

- `name` *string* theme name

Apply a chart theme.

Available themes : `chalk`, `essos`, `infographic`, `macarons`, `purple-passion`, `roma`, `romantic`, `shine`, `vintage`, `walden`, `westeros`, `wonderland`

{{< tabs items="chalk,essos,infographic,macarons,purple-passion,roma">}}
  {{< tab >}}{{< figure src="../img/theme_chalk.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_essos.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_infographic.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_macarons.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_purple-passion.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_roma.jpg" width="500" >}}{{< /tab >}}
{{< /tabs >}}

{{< tabs items="romantic,shine,vintage,walden,westeros,wonderland">}}
  {{< tab >}}{{< figure src="../img/theme_romantic.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_shine.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_vintage.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_walden.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_westeros.jpg" width="500" >}}{{< /tab >}}
  {{< tab >}}{{< figure src="../img/theme_wonderland.jpg" width="500" >}}{{< /tab >}}
{{< /tabs >}}