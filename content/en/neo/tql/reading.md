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

## CSV format

> {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}}
> When tql script is saved, the editor shows the link icon on the top right corner, click it to copy the address of the script file.

{{% steps %}}

### Save *tql* file
Save the code below as `output-csv.tql`.

```js
SQL( `select * from example limit 2` )
CSV()
```

### Client GET request

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

{{% /steps %}}

## JSON format

{{% steps %}}

### Save *tql* file
Save the code below as `output-json.tql`.

```js
SQL( `select * from example limit 2` )
JSON()
```

### Client GET request
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

## JSON format with `transpose()`

{{% steps %}}

### Save *tql* file
Save the code below as `output-json.tql`.

```js
SQL( `select * from example limit 2` )
JSON( transpose(true) )
```

### Client GET request
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


## MARKDOWN format

{{% steps %}}

### Save *tql* file
Save the code below as `output-markdown.tql`.

```js
SQL( `select * from example limit 2` )
MARKDOWN()
```

### Client GET request
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


## MARKDOWN format with `html()`

{{% steps %}}

### Save *tql* file
Save the code below as `output-markdown.tql`.

```js
SQL( `select * from example limit 2` )
MARKDOWN( html(true) )
```

### Client GET request
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

## CHART format

{{% steps %}}

### Save *tql* file
Save the code below as `output-chart.tql`.

```js
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART_BAR()
```

### Client GET request
Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

{{< figure src="../img/reading-chart-bar.jpg" width="500" >}}

{{% /steps %}}

### CHART types

{{< tabs items="CHART_LINE,CHART_BAR,CHART_SCATTER" >}}
    
    {{< tab >}}
    ```js
    FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
    CHART_LINE()
    ```
    {{< figure src="/images/chart_line.jpg" width="500" >}}
    {{< /tab >}}

    {{< tab >}}
    ```js
    FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
    CHART_BAR()
    ```
    {{< figure src="/images/chart_bar.jpg" width="500" >}}
    {{< /tab >}}
    {{< tab >}}
    ```js
    FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
    CHART_SCATTER()
    ```
    {{< figure src="/images/chart_scatter.jpg" width="500" >}}
    {{< /tab >}}
{{< /tabs >}}