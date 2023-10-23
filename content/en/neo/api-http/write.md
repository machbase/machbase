---
title: Write via http
type: docs
weight: 30
---

Even `query` api can execute 'INSERT' statement, it is not an effecient way to write data,
since clients should build a static sql text in `q` parameter for the every request.
The proper way writing data is the `write` api which is the `INSERT` statement equivalent. 
And another benefit of `write` is that a client application can insert multiple records in a single `write` request.

## Request endpoint and params

Write API's endpoint is "/db/write/" following by table name, `/db/write/{TABLE}`

| param       | default | description                     |
|:----------- |---------|:------------------------------- |
| timeformat  | ns      | Time format: s, ms, us, ns      |
| tz          | UTC     | Time Zone: UTC, Local and location spec |
| method      | insert  | Wrting methods: insert, append  |
| heading     | false   | If CSV contains header line, set `true` to skip the first line|
| delimiter   | ,       | CSV delimiter, ignored if content is not csv |

The machbase-neo server recognizes the format of incoming data stream by `Content-Type` header,
for example, `Content-Type: application/json` for JSON data, `Content-Type: text/csv` for csv data.

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

Set the header `Content-Encoding: gzip` telling machbase-neo that the incoming stream is gzip-compressed.

```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.json.gz"
```

{{< /tab >}}
{{< /tabs >}}

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

## INSERT vs. APPEND
The `/db/write` API writes the posted data with “INSERT INTO…” statement by default. As long as the total number of records to write is small, there is not a big difference from “append” method.

When you are writing a large amount of data (e.g. more than several hundreds thousands records), Use `method=append` parameter that specify machbase-neo to use “append” method instead of “INSERT INTO…” statement which is implicitly speicified as `method=insert`.