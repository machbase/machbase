---
title: As Reading API
type: docs
weight: 05
---

{{< callout type="info" >}}
For the examples, create a table and insert data with the following SQL statements.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
VALUE DOUBLE SUMMARIZED);

INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 11);
```

## CSV

> {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}}
> When tql script is saved, the editor shows the link icon on the top right corner, click it to copy the address of the script file.

{{% steps %}}

### Save *tql* file
Save the code below as `output-csv.tql`.

```js
SQL( `select * from example limit 2` )
CSV()
```

### HTTP GET

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

{{% /steps %}}

## JSON

{{% steps %}}

### Save *tql* file
Save the code below as `output-json.tql`.

```js
SQL( `select * from example limit 2` )
JSON()
```

### HTTP GET
Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG0", 1628694000000000000, 10 ],
      [ "TAG0", 1628780400000000000, 11 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "770.078µs"
}
```
{{% /steps %}}

## JSON with `transpose()`

{{% steps %}}

### Save *tql* file
Save the code below as `output-json.tql`.

```js
SQL( `select * from example limit 2` )
JSON( transpose(true) )
```

### HTTP GET
Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "cols": [
            [ "TAG0", "TAG0" ],
            [ 1628694000000000000, 1628780400000000000 ],
            [ 10, 11 ]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```
{{% /steps %}}


## MARKDOWN

{{% steps %}}

### Save *tql* file
Save the code below as `output-markdown.tql`.

```js
SQL( `select * from example limit 2` )
MARKDOWN()
```

### HTTP GET
Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

```
|NAME|TIME|VALUE|
|:-----|:-----|:-----|
|TAG0|1628694000000000000|10.000000|
|TAG0|1628780400000000000|11.000000|
```
{{% /steps %}}


## MARKDOWN with `html()`

{{% steps %}}

### Save *tql* file
Save the code below as `output-markdown.tql`.

```js
SQL( `select * from example limit 2` )
MARKDOWN( html(true) )
```

### HTTP GET
Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

```html
<div><table>
<thead>
<tr>
<th align="left">NAME</th>
<th align="left">TIME</th>
<th align="left">VALUE</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">TAG0</td>
<td align="left">1628694000000000000</td>
<td align="left">10.000000</td>
</tr>
<tr>
<td align="left">TAG0</td>
<td align="left">1628780400000000000</td>
<td align="left">11.000000</td>
</tr>
</tbody>
</table>
</div>
```
{{% /steps %}}

## CHART

{{% steps %}}

### Save *tql* file

Save the code below as `output-chart.tql`.

```js {linenos=table,hl_lines=[4,6],linenostart=1}
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

### HTTP GET

Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

{{< figure src="../img/reading-chart-bar.jpg" width="500" >}}

> The legacy `CHART_LINE()`, `CHART_BAR()`, `CHART_SCATTER()` and its family functions are deprecated 
> with the new `CHART()` function.
> Please refer to the [CHART()](/neo/tql/chart) for the examples.

{{% /steps %}}

## CHART with chartJson()

{{% steps %}}

### Save *tql* file

Save the code below as `output-chart.tql`.

```js {linenos=table,hl_lines=[3],linenostart=1}
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartJson(true),
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

### HTTP GET

Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

```json
{
  "chartID":"MzM3NjYzNjg5MTYxNjQ2MDg_", 
  "jsAssets": ["/web/echarts/echarts.min.js"],
  "jsCodeAssets": ["/web/api/tql-assets/MzM3NjYzNjg5MTYxNjQ2MDg_.js"],
  "style": {
      "width": "600px",
      "height": "600px"	
  },
  "theme": "white"
}
```

{{% /steps %}}


## CHART with chartID()

{{% steps %}}

### Save *tql* file

Save the code below as `output-chart.tql`.

```js {linenos=table,hl_lines=[3],linenostart=1}
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartId("myChart"), // chartId() is deprecated, use chartID()
    chartJson(true),
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

### HTTP GET

Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

```json
{
  "chartID":"myChart", 
  "jsAssets": ["/web/echarts/echarts.min.js"],
  "jsCodeAssets": ["/web/api/tql-assets/myChart.js"],
  "style": {
      "width": "600px",
      "height": "600px"	
  },
  "theme": "white"
}
```

This scenario is useful when your DOM document has `<div id='myChart'/>`.

```html
... in HTML ...
<div id='myChart' />
<script>
    fetch('http://127.0.0.1:5654/db/tql/output-chart.tql').then( function(rsp) {
        return rsp.json();
    }).then( function(c) {
        c.jsAssets.concat(c.jsCodeAssets).forEach((src) => {
            const sScript = document.createElement('script');
            sScript.src = src;
            sScript.type = 'text/javascript';
            document.getElementsByTagName('head')[0].appendChild(sScript);
        })
    })
</script>
... omit ...
```

{{% /steps %}}
