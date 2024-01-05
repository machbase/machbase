---
title: Glance at TQL
type: docs
weight: 01
---

machbase-neo supports Transforming Query Language and execution API.

As application developers, we generally take similar approching to build applications that utilize databases.
The process is starting typically with quering database and retrieving data in a tabular form(rows and colums), converting it into the desired data structure,
then manipulating and displaying the final result into demanded shapes such as JSON, CSV or chart.

TQL is simplifying this process within few lines of script. And other inter-working applications call the TQL via HTTP endpoint as if it is an executable API.

## What is TQL

TQL (transforming Query Language) is a DSL for the data manipulation.
It defines a flow of data stream, and the individual data unit is a record.
A records has *key* and *value*, a key is generally auto-generated sequential integer like *ROWNUM* of query result.
a value is a tuple that contains actual data fields.

![tql_records](../img/tql_records.jpg)

TQL script starts with *SRC* (source) that defines how to retrieve data and generates records by transforming the raw data. The *SINK* should be the end of TQL script which defines how to output records.

![tql_flow_min](../img/tql_flow_min.jpg)

In some cases TQL script needs to transform records, involving mathematic calculation, simply string concatenation or interacts with external databases.
Those tasks can be defined in *MAP* functions.

So, TQL script should start with *SRC* and end with *SINK* and it can has zero or one more *MAP* functions.

![tql_flow](../img/tql_flow.jpg)

### SRC

There are serveral SRC functions. For example, `SQL()` produces records by querying machbase-neo database or even external (bridged) databases with the given sql statement. `FAKE()` generates artifitial data. `CSV()` can read csv data, `BYTES()` reads arbitrary binary data from file system or client's HTTP request and MQTT payload.

![tql_src](../img/tql_src.jpg)

### SINK

The basic SINK function might be `INSERT()` which writes the incoming records onto machbase-neo database. `CHART()` function renders a chart with incoming records. `JSON()` and `CSV()` encode incoming data into proper formats.

![tql_sink](../img/tql_sink.jpg)

### MAP

*MAP* functions are the core of the transforming data from a shape to an other.

![tql_map](../img/tql_map.jpg)

## Run TQL

{{% steps %}}

### Open Web UI
Open machbase-neo web UI with your web browser,
the default address is `http://127.0.0.1:5654/`, username `sys` and password `manager`.

### New TQL page
Select "TQL" on the 'New...' page.
<br/>
{{< figure src="/images/web-tql-pick.png" width="550" >}}

### Copy the code and run

Copy and paste the sample TQL code into the TQL editor.

Then click ▶︎ icon on the top left of the editor, it will display a line chart as the image below.
Which is a wave that has 1.5 Hz frequency and 1.0 amplitude.

{{% /steps %}}

{{< tabs items="SCATTER,LINE,BAR">}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER()
```
{{< figure src="../img/web-hello-tql-chart-scatter.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_LINE()
```
{{< figure src="../img/web-hello-tql-chart-line.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_BAR()
```
{{< figure src="../img/web-hello-tql-chart-bar.jpg" width="500" >}}
{{< /tab >}}
{{< /tabs >}}

Let's try some CSV,JSON formats.

{{< tabs items="JSON-rows,JSON-cols,CSV,MARKDOWN,HTML">}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON()
```
{{< figure src="../img/web-hello-tql-json.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON( transpose(true) )
```
{{< figure src="../img/web-hello-tql-json-transpose.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CSV()
```
{{< figure src="../img/web-hello-tql-csv.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN()
```
{{< figure src="../img/web-hello-tql-markdown.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN( html(true) )
```
{{< figure src="../img/web-hello-tql-markdown-html.jpg" width="500" >}}
{{< /tab >}}
{{< /tabs >}}


## TQL as API

Save this code as `hello.tql` (click save icon on the top right of the editor) and open it with web browser at [http://127.0.0.1:5654/db/tql/hello.tql](http://127.0.0.1:5654/db/tql/hello.tql), or use *curl* command on the terminal.

> {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}}
> When tql script is saved, the editor shows the link icon on the top right corner, click it to copy the address of the script file.

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
>
< HTTP/1.1 200 OK
< Content-Type: text/csv
< Transfer-Encoding: chunked
<
1686787739025518000,-0.238191
1686787739035518000,-0.328532
1686787739045518000,-0.415960
1686787739055518000,-0.499692
1686787739065518000,-0.578992
...omit...
```

### JSON()

Let's try to change `CSV()` to `JSON()`, save and execute again.
    {{< figure src="/images/web-hello-tql-json.jpg" width="500" >}}

And invoke the hello.tql with `curl` from terminal.

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
< HTTP/1.1 200 OK
< Content-Type: application/json
< Transfer-Encoding: chunked
<
{
"data": {
    "columns": [ "time", "value" ],
    "types": [ "datetime", "double" ],
    "rows": [
    [ 1686788907538618000, 0.9344920354538058 ],
    [ 1686788907548618000, 0.8968436523101743 ],
    ...omit...
},
"success": true,
"reason": "success",
"elapse": "956.291µs"
}
```

### JSON() with transpose()

If you are developing a data visualization application, it shall be helpful to know that *tql* JSON output supports transpose the result in columns instead of rows. Apply `JSON( transpose(true) )` and invoke it again. The result JSON contains *cols* array.

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
< HTTP/1.1 200 OK
< Content-Type: application/json
< Transfer-Encoding: chunked
<
{
"data": {
    "columns": [ "time", "value" ],
    "types": [ "datetime", "double" ],
    "cols": [
        [ 1686789517241103000, ...omit..., 1686789520231103000],
        [ -0.7638449771082523, ...omit..., 0.8211935584502427]
    ]
},
"success": true,
"reason": "success",
"elapse": "1.208166ms"
}
```

This feature is the simplest way for deveropers to create RESTful APIs providing other applications accessing data.

### INSERT

Change `CSV()` to `INSERT("time", "value", table("example"), tag("temperature"))` and execute again.

{{< figure src="/images/web-tql-insert.png" width="500" >}}

### Select Table

```js
SQL('select * from tag limit 10')
CSV()
```

{{< figure src="/images/web-tql-select.png" width="500" >}}
