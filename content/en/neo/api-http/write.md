---
title: Write via http
type: docs
weight: 30
---

Even `query` api can execute 'INSERT' statement, it is not an efficient way to write data,
since clients should build a static sql text in `q` parameter for the every request.
The proper way writing data is the `write` api which is the `INSERT` statement equivalent. 
And another benefit of `write` is that a client application can insert multiple records in a single `write` request.

## Request endpoint and params

Write API's endpoint is "/db/write/" following by table name, `/db/write/{TABLE}`

| param       | default | description                     |
|:----------- |---------|:------------------------------- |
| timeformat  | ns      | Time format: s, ms, us, ns      |
| tz          | UTC     | Time Zone: UTC, Local and location spec |
| method      | insert  | Writing methods: insert, append  |

**Available parameters with `Content-Type: text/csv`**

These options are only applicable when the content body is in CSV format.

| param       | default | description                     |
|:----------- |---------|:------------------------------- |
| heading     | false   | If CSV contains header line, set `true` to skip the first line|
| delimiter   | ,       | CSV delimiter, ignored if content is not csv |


**Content-Type Header**

The machbase-neo server recognizes the format of incoming data stream by `Content-Type` header,
for example, `Content-Type: application/json` for JSON data, `Content-Type: text/csv` for csv data.

**Content-Encoding Header**

If client sends gzip'd compress stream, it should set the header `Content-Encoding: gzip` 
that tells the machbase-neo the incoming data stream is encoded in gzip.


## Request JSON

This request message is equivalent that consists INSERT SQL statement as `INSERT into {table} (columns...) values (values...)`

| name         | type       |  description                        |
|:------------ |:-----------|:------------------------------------|
| data         | object           |                               |
| data.columns | array of strings | represents columns            |
| data.rows    | array of tuples  | values of records             |

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "my-car", 1670380342000000000, 1.0001 ],
            [ "my-car", 1670380343000000000, 2.0002 ]
        ]
    }
}
```

{{< tabs items="JSON,JSON(gzip)">}}
{{< tab >}}

Set `Content-Type` header as `application/json`.

```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    --data-binary "@post-data.json"
```
{{< /tab >}}
{{< tab >}}

Set the header `Content-Encoding: gzip` tells machbase-neo that the incoming stream is gzip-compressed.

```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.json.gz"
```

{{< /tab >}}
{{< /tabs >}}

### Request JSON with timeformat

When time fields are string format instead of UNIX epoch.

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "my-car", "2022-12-07 02:32:22", 1.0001 ],
            [ "my-car", "2022-12-07 02:32:23", 2.0002 ]
        ]
    }
}
```

Add `timeformat` and `tz` query parameters.

```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=DEFAULT&tz=Asia/Seoul' \
    -H "Content-Type: application/json" \
    --data-binary "@post-data.json"
```

## Request CSV

If csv data has header line like below, set the `heading=true` query param.

```csv
NAME,TIME,VALUE
my-car,1670380342000000000,1.0001
my-car,1670380343000000000,2.0002
```

{{< tabs items="CSV,CSV(gzip)">}}
{{< tab >}}
The `Content-Type` header should be `text/csv`.

```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?heading=true \
    -H "Content-Type: text/csv" \
    --data-binary "@post-data.csv"
```
{{< /tab >}}
{{< tab >}}

Set the header `Content-Encoding: gzip` telling machbase-neo that the incoming stream is gzip-compressed.

```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?heading=true \
    -H "Content-Type: text/csv" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.csv.gz"
```
{{< /tab >}}
{{< /tabs >}}

### Request CSV with timeformat

```csv
NAME,TIME,VALUE
my-car,2022-12-07 11:32:22,1.0001
my-car,2022-12-07 11:32:22,2.0002
```

Add `timeformat` and `tz` query parameters.

```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?heading=true&timeformat=Default&tz=Asia/Seoul' \
    -H "Content-Type: text/csv" \
    --data-binary "@post-data.csv"
```

## INSERT vs. APPEND
The `/db/write` API writes the posted data with “INSERT INTO…” statement by default. As long as the total number of records to write is small, there is not a big difference from “append” method.

When you are writing a large amount of data (e.g. more than several hundreds thousands records), Use `method=append` parameter that specify machbase-neo to use “append” method instead of “INSERT INTO…” statement which is implicitly specified as `method=insert`.

## Example

Please refer to the detail of the API [Request endpoint and params](/neo/api-http/write#request-endpoint-and-params)

**Test Table**

```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```

**Time**

The time stored in the sample files saved in these examples is represented in Unix epoch, measured in seconds. Therefore, when loading the data, it should be performed with the `timeformat=s` option specified. If the data has been stored in a different resolution, this option needs to be modified to ensure proper input. Note that in Machbase Neo, the default time resolution is assumed to be in `nanoseconds (ns)` and is executed accordingly.

### Insert JSON file with epoch time

**Prepare data file**

`data-epoch-1.json`
[download](/assets/example/data-epoch-1.json)

```json
{
  "data":  {
    "columns":["NAME","TIME","VALUE"],
    "rows": [
        ["wave.sin",1676432361,0],
        ["wave.sin",1676432362,0.406736],
        ["wave.sin",1676432363,0.743144],
        ["wave.sin",1676432364,0.951056],
        ["wave.sin",1676432365,0.994522]
    ]
  }
}
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s" \
    -H "Content-Type: application/json" \
    --data-binary "@data-epoch-1.json"
```

**Select rows**

```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE"
```


### Insert CSV file with epoch time and header

If csv data has header line like below, set the `heading=true` query param.

**Prepare data file**

`data-epoch-1-header.csv`
[download](/assets/example/data-epoch-1-header.csv)

```
NAME,TIME,VALUE
wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s&heading=true" \
    -H "Content-Type: text/csv" \
    --data-binary "@data-epoch-1-header.csv"
```

### Insert CSV file with epoch time and no header

If csv data has header line like below, set the `heading=false` query param.

**Prepare data file**

`data-epoch-1-no-header.csv`
[download](https://docs.machbase.com/assets/example/data-epoch-1-no-header.csv)

```
wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s&heading=false" \
    -H "Content-Type: text/csv" \
    --data-binary "@data-epoch-1-no-header.csv"
```

### Append a large CSV file

When loading a large CSV file, using the "append" method can allow data to be input several times faster compared to the "insert" method.

**Prepare data file**

`data-epoch-bulk.csv`
[download](https://docs.machbase.com/assets/example/data-epoch-bulk.csv)

```
wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
......
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s&heading=false&method=append" \
    -H "Content-Type: text/csv" \
    --data-binary "@data-epoch-bulk.csv"
```

### Insert CSV file in default time format

**Prepare data file**

`data-timeformat-1.csv`
[download](https://docs.machbase.com/assets/example/data-timeformat-1.csv)

```
wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111,0.222222
wave.sin,2023-02-15 03:39:23.222,0.333333
wave.sin,2023-02-15 03:39:24.333,0.444444
wave.sin,2023-02-15 03:39:25.444,0.555555
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?heading=false&timeformat=Default" \
    -H "Content-Type: text/csv" \
    --data-binary "@data-timeformat-1.csv"
```

**Select rows**

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "timeformat=Default"      \
    --data-urlencode "format=csv"
```

```
NAME,TIME,VALUE
wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111,0.222222
wave.sin,2023-02-15 03:39:23.222,0.333333
wave.sin,2023-02-15 03:39:24.333,0.444444
wave.sin,2023-02-15 03:39:25.444,0.555555
```

### Insert CSV file in default timeformat with Time Zone

**Prepare data file**

`data-timeformat-1-tz-seoul.csv`
[download](https://docs.machbase.com/assets/example/data-timeformat-1-tz-seoul.csv)

```
wave.sin,2023-02-15 12:39:21,0.111111
wave.sin,2023-02-15 12:39:22.111,0.222222
wave.sin,2023-02-15 12:39:23.222,0.333333
wave.sin,2023-02-15 12:39:24.333,0.444444
wave.sin,2023-02-15 12:39:25.444,0.555555
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?heading=false&timeformat=Default&tz=Asia/Seoul" \
        -H "Content-Type: text/csv" \
        --data-binary "@data-timeformat-1-tz-seoul.csv"
```

**Select rows in UTC**

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "timeformat=Default"      \
    --data-urlencode "format=csv"
```

```
NAME,TIME,VALUE
wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111,0.222222
wave.sin,2023-02-15 03:39:23.222,0.333333
wave.sin,2023-02-15 03:39:24.333,0.444444
wave.sin,2023-02-15 03:39:25.444,0.555555
```

### Insert CSV file in `RFC3339` time format

**Prepare data file**

`data-timeformat-rfc3339.csv`
[download](https://docs.machbase.com/assets/example/data-timeformat-rfc3339.csv)

```
wave.sin,2023-02-15T03:39:21Z,0.111111
wave.sin,2023-02-15T03:39:22Z,0.222222
wave.sin,2023-02-15T03:39:23Z,0.333333
wave.sin,2023-02-15T03:39:24Z,0.444444
wave.sin,2023-02-15T03:39:25Z,0.555555
```

**Post data**

```sh
 curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?heading=false&timeformat=RFC3339" \
        -H "Content-Type: text/csv" \
        --data-binary "@data-timeformat-rfc3339.csv"
```

**Select rows in UTC**

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=csv"              \
    --data-urlencode "timeformat=RFC3339"
```

```
NAME,TIME,VALUE
wave.sin,2023-02-15T03:39:21Z,0.111111
wave.sin,2023-02-15T03:39:22Z,0.222222
wave.sin,2023-02-15T03:39:23Z,0.333333
wave.sin,2023-02-15T03:39:24Z,0.444444
wave.sin,2023-02-15T03:39:25Z,0.555555
```

### Insert CSV file in `RFC3339Nano` time format with `America/New_York`

**Prepare data file**

`data-timeformat-rfc3339nano-tz-newyork.csv`
[download](https://docs.machbase.com/assets/example/data-timeformat-rfc3339nano-tz-newyork.csv)

```
wave.sin,2023-02-14T22:39:21.000000000-05:00,0.111111
wave.sin,2023-02-14T22:39:22.111111111-05:00,0.222222
wave.sin,2023-02-14T22:39:23.222222222-05:00,0.333333
wave.sin,2023-02-14T22:39:24.333333333-05:00,0.444444
wave.sin,2023-02-14T22:39:25.444444444-05:00,0.555555
```

**Post data**

```sh
 curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?heading=false&timeformat=RFC3339Nano&tz=America/New_York" \
        -H "Content-Type: text/csv"  \
        --data-binary "@data-timeformat-rfc3339nano-tz-newyork.csv"
```

**Select rows in America/New_York**

```sh
curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339Nano"  \
    --data-urlencode "tz=America/New_York"
```

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

### Insert CSV file in custom time format

**Prepare data file**

`data-timeformat-custom-1.csv`
[download](https://docs.machbase.com/assets/example/data-timeformat-custom-1.csv)

```
wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111111111,0.222222
wave.sin,2023-02-15 03:39:23.222222222,0.333333
wave.sin,2023-02-15 03:39:24.333333333,0.444444
wave.sin,2023-02-15 03:39:25.444444444,0.555555
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?heading=false&timeformat=Default" \
        -H "Content-Type: text/csv" \
        --data-binary "@data-timeformat-custom-1.csv"
```

**Select rows in `UTC`**

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=csv"              \
    --data-urlencode "timeformat=Default"
```

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

### Insert CSV file in custom time format with `America/New_York`

**Prepare data file**

`data-timeformat-custom-2.csv`
[download](https://docs.machbase.com/assets/example/data-timeformat-custom-2.csv)
> `hour:min:sec-SPLIT-year-month-day` format in newyork timezone
```
wave.sin,10:39:21-SPLIT-2023-02-14 ,0.111111
wave.sin,10:39:22.111111111-SPLIT-2023-02-14 ,0.222222
wave.sin,10:39:23.222222222-SPLIT-2023-02-14 ,0.333333
wave.sin,10:39:24.333333333-SPLIT-2023-02-14 ,0.444444
wave.sin,10:39:25.444444444-SPLIT-2023-02-14 ,0.555555
```

**Post data**

```sh
curl -X POST "http://127.0.0.1:5654/db/write/EXAMPLE?heading=false&timeformat=03:04:05.999999999-SPLIT-2006-01-02&tz=America/New_York" \
        -H "Content-Type: text/csv" \
        --data-binary "@data-timeformat-custom-2.csv"
```

**Select rows in `UTC`**

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=csv"              \
    --data-urlencode "timeformat=2006-01-02 03:04:05.999999999"
```

```
NAME,TIME,VALUE
wave.sin,2023-02-14 03:39:21,0.111111
wave.sin,2023-02-14 03:39:22.111111111,0.222222
wave.sin,2023-02-14 03:39:23.222222222,0.333333
wave.sin,2023-02-14 03:39:24.333333333,0.444444
wave.sin,2023-02-14 03:39:25.444444444,0.555555
```

`select rows in default time format in America/New_York Time Zone`

```sh
curl -o - http://127.0.0.1:5654/db/query       \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=csv"              \
    --data-urlencode "timeformat=Default" \
    --data-urlencode "tz=America/New_York"
```

```
NAME,TIME,VALUE
wave.sin,2023-02-14 10:39:21,0.111111
wave.sin,2023-02-14 10:39:22.111,0.222222
wave.sin,2023-02-14 10:39:23.222,0.333333
wave.sin,2023-02-14 10:39:24.333,0.444444
wave.sin,2023-02-14 10:39:25.444,0.555555
```
