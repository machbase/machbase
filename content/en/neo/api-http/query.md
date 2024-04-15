---
title: Query via http
type: docs
weight: 20
---

There are three different ways of executing SQL statement via HTTP.
Those api support not only "SELECT" but also "CREATE TABLE", "ALTER TABLE", "INSERT"... all other SQL statements.

The `query` API supports *GET*, *POST JSON* and *POST form-data*. all those methods have the same parameters.

For example the parameter `format` can be specified in query parameter in *GET* method like `GET /db/query?format=csv`,
or be a JSON field in *POST-JSON* method as `{ "format": "csv" }`.

**Query Example**

```
http://127.0.0.1:5654/db/query?q=select%20*%20from%20EXAMPLE%20limit%202
```

**Query Parameters**

| param       | default | description                   |
|:----------- |---------|:----------------------------- |
| **q**       | _required_ | SQL query string              |
| format      | `json`    | Result data format: json, csv, box |
| timeformat  | `ns`      | Time format: s, ms, us, ns    |
| tz          | `UTC`     | Time Zone: UTC, Local and location spec |
| compress    | _no compression_   | compression method: gzip      |
| rownum      | `false`   | including rownum: true, false |
| heading     | `true`    | showing heading: true, false  |
| precision   | `-1`      | precision of float value, -1 for no round, 0 for int |

**Available parameters with `format=json`** {{< neo_since ver="8.0.12" />}}

* The options are only available when `format=json`. Those options are exclusive each other, applicable only one of them per a request.

| param       | default | description                   |
|:----------- |---------|:----------------------------- |
| transpose   | false   | produce cols array instead of rows. |
| rowsFlatten | false   | reduce the array dimension of the *rows* field in the JSON object. |
| rowsArray   | false   | produce JSON that contains only array of object for each record.  |

**Available timeformat**

| timeformat    |  result                             |
|:------------- |:------------------------------------|
| `Default`     | 2006-01-02 15:04:05.999             |
| `Numeric`     | 01/02 03:04:05PM '06 -0700          |
| `Ansic`       | Mon Jan _2 15:04:05 2006            |
| `Unix`        | Mon Jan _2 15:04:05 MST 2006        |
| `Ruby`        | Mon Jan 02 15:04:05 -0700 2006      |
| `RFC822`      | 02 Jan 06 15:04 MST                 |
| `RFC822Z`     | 02 Jan 06 15:04 -0700               |
| `RFC850`      | Monday, 02-Jan-06 15:04:05 MST      |
| `RFC1123`     | Mon, 02 Jan 2006 15:04:05 MST       |
| `RFC1123Z`    | Mon, 02 Jan 2006 15:04:05 -0700     |
| `RFC3339`     | 2006-01-02T15:04:05Z07:00           |
| `RFC3339Nano` | 2006-01-02T15:04:05.999999999Z07:00 |
| `Kitchen`     | 3:04:05PM                           |
| `Stamp`       | Jan _2 15:04:05                     |
| `StampMili`   | Jan _2 15:04:05.000                 |
| `StampMicro`  | Jan _2 15:04:05.000000              |
| `StampNano`   | Jan _2 15:04:05.000000000           |

## GET

**Response in JSON format (default)**

Set query param `format=json` or omit it for the default value.

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query ^
    --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< /tabs >}}


The server responses in `Content-Type: application/json`.

| name         | type       |  description                        |
|:------------ |:-----------|:------------------------------------|
| **success**  | bool       | `true` if query execution succeed |
| **reason**   | string     | execution result message, this will contains error message if `success` is `false`  |
| **elapse**   | string     | elapse time of the query execution    |
| data         |            | exists only when execution succeed  |
| data.columns | array of strings | represents columns of result    |
| data.types   | array of strings | represents data types of result |
| data.rows    | array of records | array represents the result set records.<br/>This field will be replaced with `cols` if `transpose` is `true` |
| data.cols    | array of series  | array represents the result set column-series.<br/> This element exists when `transpose` is `true` |

{{< tabs items="default,transpose,rowsFlatten,rowsArray">}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
      --data-urlencode "q=select * from EXAMPLE"
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1705381958775759000, 0.8563571936170834 ],
      [ "wave.sin", 1705381958785759000, 0.9011510331449053 ],
      [ "wave.sin", 1705381958795759000, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.887042ms"
}
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
      --data-urlencode "q=select * from EXAMPLE" \
      --data-urlencode "transpose=true"
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "cols": [
      [ "wave.sin", "wave.sin", "wave.sin" ],
      [ 1705381958775759000, 1705381958785759000, 1705381958795759000 ],
      [ 0.8563571936170834, 0.9011510331449053, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "4.090667ms"
}
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
      --data-urlencode "q=select * from EXAMPLE" \
      --data-urlencode "rowsFlatten=true"
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      "wave.sin", 1705381958775759000, 0.8563571936170834,
      "wave.sin", 1705381958785759000, 0.9011510331449053,
      "wave.sin", 1705381958795759000, 0.9379488170706388
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "2.255625ms"
}
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
      --data-urlencode "q=select * from EXAMPLE" \
      --data-urlencode "rowsArray=true"
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      { "NAME": "wave.sin", "TIME": 1705381958775759000, "VALUE": 0.8563571936170834 },
      { "NAME": "wave.sin", "TIME": 1705381958785759000, "VALUE": 0.9011510331449053 },
      { "NAME": "wave.sin", "TIME": 1705381958795759000, "VALUE": 0.9379488170706388 }
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "3.178458ms"
}
```
{{< /tab >}}
{{< /tabs >}}

**Response in BOX format**

Set query param `format=box` in the request.

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" --data-urlencode "format=box"
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query ^
    --data-urlencode "q=select * from EXAMPLE limit 2" --data-urlencode "format=box"
```
{{< /tab >}}
{{< /tabs >}}

The result data in plain text with ascii box. The Content-Type of the response is `plain/text` 

```
+----------+---------------------+----------+
| NAME     | TIME(UTC)           | VALUE    |
+----------+---------------------+----------+
| wave.sin | 1676337568          | 0.000000 |
| wave.sin | 1676337569          | 0.406736 |
+----------+---------------------+----------+
```

**Response in CSV format**

Set query param `format=csv` in the request.

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" --data-urlencode "format=csv"
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query ^
    --data-urlencode "q=select * from EXAMPLE limit 2" --data-urlencode "format=csv"
```
{{< /tab >}}
{{< /tabs >}}

The response comes with `Content-Type: text/csv`

```csv
NAME,TIME,VALUE
wave.sin,1676337568,0.000000
wave.sin,1676337569,0.406736
```

> Use `machbase-neo help tz` and `machbase-neo help timeformat` to see more available options for timezone and timeformat options

```
machbase-neo» help timeformat;
  timeformats:
    epoch
      ns             nanoseconds
      us             microseconds
      ms             milliseconds
      s              seconds
    abbreviations
      Default,-      2006-01-02 15:04:05.999
      Numeric        01/02 03:04:05PM '06 -0700
      Ansic          Mon Jan _2 15:04:05 2006
      Unix           Mon Jan _2 15:04:05 MST 2006
      Ruby           Mon Jan 02 15:04:05 -0700 2006
      RFC822         02 Jan 06 15:04 MST
      RFC822Z        02 Jan 06 15:04 -0700
      RFC850         Monday, 02-Jan-06 15:04:05 MST
      RFC1123        Mon, 02 Jan 2006 15:04:05 MST
      RFC1123Z       Mon, 02 Jan 2006 15:04:05 -0700
      RFC3339        2006-01-02T15:04:05Z07:00
      RFC3339Nano    2006-01-02T15:04:05.999999999Z07:00
      Kitchen        3:04:05PM
      Stamp          Jan _2 15:04:05
      StampMili      Jan _2 15:04:05.000
      StampMicro     Jan _2 15:04:05.000000
      StampNano      Jan _2 15:04:05.000000000
    custom format
      year           2006
      month          01
      day            02
      hour           03 or 15
      minute         04
      second         05 or with sub-seconds '05.999999999'
```

[List of Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) - wikipedia.org
```
machbase-neo» help tz;
  timezones:
    abbreviations
      UTC
      Local
      Europe/London
      America/New_York
      ...
    location examples
      America/Los_Angeles
      Europe/Paris
      ...
    Time Coordinates examples
      UTC+9
```

## POST JSON

It is also possible to request query in JSON form as below example.

**Request JSON message**

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    -H 'Content-Type: application/json' \
    -d '{ "q":"select * from EXAMPLE limit 2" }'
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query ^
    -H "Content-Type: application/json" ^
    -d "{ \"q\":\"select * from EXAMPLE limit 2\" }"
```
{{< /tab >}}
{{< /tabs >}}

## POST Form

HTML Form data format is available too. HTTP header `Content-type` should be `application/x-www-form-urlencoded` in this case.

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query ^
    --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< /tabs >}}

## Examples

Please refer to the detail of the API 
- [Request endpoint and params](/neo/api-http/query)
- [List of Time Zones from wikipedia.org](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

For this tutorials, pre-write data below.

{{% steps %}}

### Data file

Copy and paste on a new file `data-nano-1.json`.

```json
{
    "data":{
      "columns":["NAME","TIME","VALUE"],
      "rows":[
          ["wave.sin",1676432361,0],
          ["wave.sin",1676432362,0.406736],
          ["wave.sin",1676432363,0.743144],
          ["wave.sin",1676432364,0.951056],
          ["wave.sin",1676432365,0.994522]
      ]
    }
}
```
Or download it from [here](https://docs.machbase.com/assets/example/data-epoch-1.json).

### Create table
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
### Write data
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ns \
    -H "Content-Type: application/json"                           \
    --data-binary "@data-nano-1.json"
```

{{% /steps %}}

### Select in CSV

**Request**

Set the `format=csv` query param for CSV format.

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=csv"
```

**Response**
```
NAME,TIME,VALUE
wave.sin,1676432361000000000,0.111111
wave.sin,1676432362111111111,0.222222
wave.sin,1676432363222222222,0.333333
wave.sin,1676432364333333333,0.444444
wave.sin,1676432365444444444,0.555555
```

### Select in BOX

**Request**

Set the `format=box` query param for BOX format.

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"
```

**Response**

```
+----------+---------------------+----------+
| NAME     | TIME                | VALUE    |
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### Select in BOX with rownum

**Request**

Set the `format=box` query param for BOX format.

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "rownum=true"
```

**Response**

```
+--------+----------+---------------------+----------+
| ROWNUM | NAME     | TIME                | VALUE    |
+--------+----------+---------------------+----------+
|      1 | wave.sin | 1676432361000000000 | 0.111111 |
|      2 | wave.sin | 1676432362111111111 | 0.222222 |
|      3 | wave.sin | 1676432363222222222 | 0.333333 |
|      4 | wave.sin | 1676432364333333333 | 0.444444 |
|      5 | wave.sin | 1676432365444444444 | 0.555555 |
+--------+----------+---------------------+----------+
```


### Select in BOX without heading

**Request**

Set the `format=box` and `heading=false` query param for BOX format without header.

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "heading=false"
```

**Response**

```
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### Select in BOX value in INTEGER

**Request**

Set the `format=box` and `precision=0` query param for BOX format with integer precision.

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "precision=0"
```

**Response**

```
+----------+---------------------+-------+
| NAME     | TIME                | VALUE |
+----------+---------------------+-------+
| wave.sin | 1676432361000000000 | 0     |
| wave.sin | 1676432362111111111 | 0     |
| wave.sin | 1676432363222222322 | 0     |
| wave.sin | 1676432364333333233 | 0     |
| wave.sin | 1676432365444444444 | 1     |
+----------+---------------------+-------+
```

### Select in Default Time

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=Default"
```

**Response**

```
+----------+-------------------------+----------+
| NAME     | TIME                    | VALUE    |
+----------+-------------------------+----------+
| wave.sin | 2023-02-15 03:39:21     | 0.111111 |
| wave.sin | 2023-02-15 03:39:22.111 | 0.222222 |
| wave.sin | 2023-02-15 03:39:23.222 | 0.333333 |
| wave.sin | 2023-02-15 03:39:24.333 | 0.444444 |
| wave.sin | 2023-02-15 03:39:25.444 | 0.555555 |
+----------+-------------------------+----------+
```

### Select rows in default time format with `Asia/Seoul`

**Request**
Set query param `timeformat=Default` and `tz=Asia/Seoul`

```sh
 curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=Default"      \
    --data-urlencode "tz=Asia/Seoul"
```

**Response**

```
 +----------+-------------------------+----------+
| NAME     | TIME                    | VALUE    |
+----------+-------------------------+----------+
| wave.sin | 2023-02-15 12:39:21     | 0.111111 |
| wave.sin | 2023-02-15 12:39:22.111 | 0.222222 |
| wave.sin | 2023-02-15 12:39:23.222 | 0.333333 |
| wave.sin | 2023-02-15 12:39:24.333 | 0.444444 |
| wave.sin | 2023-02-15 12:39:25.444 | 0.555555 |
+----------+-------------------------+----------+
```

### Select rows in `RFC3339`

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339"
```

**Response**

```
+----------+----------------------+----------+
| NAME     | TIME                 | VALUE    |
+----------+----------------------+----------+
| wave.sin | 2023-02-15T03:39:21Z | 0.111111 |
| wave.sin | 2023-02-15T03:39:22Z | 0.222222 |
| wave.sin | 2023-02-15T03:39:23Z | 0.333333 |
| wave.sin | 2023-02-15T03:39:24Z | 0.444444 |
| wave.sin | 2023-02-15T03:39:25Z | 0.555555 |
+----------+----------------------+----------+
```

### Select in RFC3339 with Nano precision

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339Nano"
```

**Response**

```
 +----------+--------------------------------+----------+
| NAME     | TIME                           | VALUE    |
+----------+--------------------------------+----------+
| wave.sin | 2023-02-15T03:39:21Z           | 0.111111 |
| wave.sin | 2023-02-15T03:39:22.111111111Z | 0.222222 |
| wave.sin | 2023-02-15T03:39:23.222222322Z | 0.333333 |
| wave.sin | 2023-02-15T03:39:24.333333233Z | 0.444444 |
| wave.sin | 2023-02-15T03:39:25.444444444Z | 0.555555 |
+----------+--------------------------------+----------+
```

### Select in RFC3339 with Nano precision in America/New_York Time Zone

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339Nano"  \
    --data-urlencode "tz=America/New_York"
```

**Response**

```
+----------+-------------------------------------+----------+
| NAME     | TIME                                | VALUE    |
+----------+-------------------------------------+----------+
| wave.sin | 2023-02-14T22:39:21-05:00           | 0.111111 |
| wave.sin | 2023-02-14T22:39:22.111111111-05:00 | 0.222222 |
| wave.sin | 2023-02-14T22:39:23.222222222-05:00 | 0.333333 |
| wave.sin | 2023-02-14T22:39:24.333333333-05:00 | 0.444444 |
| wave.sin | 2023-02-14T22:39:25.444444444-05:00 | 0.555555 |
+----------+-------------------------------------+----------+
```

### Select in Custom Time Format

In Machbase Neo Rest API, specific numbers are used to replace the format of certain time.
Set query param `timeformat=<custom-format-as-below>`

```bash
 custom format
      year           2006
      month          01
      day            02
      hour           03 or 15
      minute         04
      second         05 or with sub-seconds '05.999999999'
```

### Typical Custom Time Format

**Request**

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=2006-01-02 03:04:05.999999999"
```

**Response**
```
+----------+-------------------------------+----------+
| NAME     | TIME                          | VALUE    |
+----------+-------------------------------+----------+
| wave.sin | 2023-02-15 03:39:21           | 0.111111 |
| wave.sin | 2023-02-15 03:39:22.111111111 | 0.222222 |
| wave.sin | 2023-02-15 03:39:23.222222222 | 0.333333 |
| wave.sin | 2023-02-15 03:39:24.333333333 | 0.444444 |
| wave.sin | 2023-02-15 03:39:25.444444444 | 0.555555 |
+----------+-------------------------------+----------+
```

### Typical Re-ordered Custom Time Format

**Request**

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=03:04:05.999999999-ReOrder-2006-01-02 "
```

**Response**

```
+----------+----------------------------------------+----------+
| NAME     | TIME                                   | VALUE    |
+----------+----------------------------------------+----------+
| wave.sin | 03:39:21-ReOrder-2023-02-15            | 0.111111 |
| wave.sin | 03:39:22.111111111-ReOrder-2023-02-15  | 0.222222 |
| wave.sin | 03:39:23.222222222-ReOrder-2023-02-15  | 0.333333 |
| wave.sin | 03:39:24.333333333-ReOrder-2023-02-15  | 0.444444 |
| wave.sin | 03:39:25.444444444-ReOrder-2023-02-15  | 0.555555 |
+----------+----------------------------------------+----------+
```

### Typical Re-ordered Custom Time Format in America/New_York Time Zone

**Request**

```sh
 curl -o - http://127.0.0.1:5654/db/query                                 \
    --data-urlencode "q=select * from EXAMPLE"                            \
    --data-urlencode "format=box"                                         \
    --data-urlencode "timeformat=03:04:05.999999999-ReOrder-2006-01-02 "  \
    --data-urlencode "tz=America/New_York"
```

**Response**

```
+----------+----------------------------------------+----------+
| NAME     | TIME                                   | VALUE    |
+----------+----------------------------------------+----------+
| wave.sin | 10:39:21-ReOrder-2023-02-14            | 0.111111 |
| wave.sin | 10:39:22.111111111-ReOrder-2023-02-14  | 0.222222 |
| wave.sin | 10:39:23.222222222-ReOrder-2023-02-14  | 0.333333 |
| wave.sin | 10:39:24.333333333-ReOrder-2023-02-14  | 0.444444 |
| wave.sin | 10:39:25.444444444-ReOrder-2023-02-14  | 0.555555 |
+----------+----------------------------------------+----------+
```
