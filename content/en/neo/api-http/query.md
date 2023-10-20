---
title: Query via http
type: docs
weight: 20
---

There are three different ways of executing SQL statement via HTTP.
Those api support not only "SELECT" but also "CREATE TABLE", "ALTER TABLE", "INSERT"... all other SQL statements.

## Get

**Request Params**

| param       | default | description                   |
|:----------- |---------|:----------------------------- |
| **q**       | _n/a_   | SQL query string              |
| format      | json    | Result data format: json, csv, box |
| timeformat  | ns      | Time format: s, ms, us, ns    |
| tz          | UTC     | Time Zone: UTC, Local and location spec |
| compress    | _no compression_   | compression method: gzip      |
| rownum      | false   | including rownum: true, false |
| heading     | true    | showing heading: true, false  |
| precision   | -1      | precision of float value, -1 for no round, 0 for int |

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

[List of Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
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

**Response in JSON format (default)**

Set query param `format=json` or omit it for the default value.

```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```

The server responses in `Content-Type: application/json`.

| name         | type       |  description                        |
|:------------ |:-----------|:------------------------------------|
| **success**  | bool       | `true` if query execution successed |
| **reason**   | string     | execution result message, this will contains error message if `success` is `false`  |
| **elapse**   | string     | elapse time of the query execution    |
| data         |            | exists only when execution successed  |
| data.columns | array of strings | represents columns of result    |
| data.types   | array of strings | represents data types of result |
| data.rows    | array of tuples  | a tuple represents a record     |

```json
{
  "success": true,
  "reason": "success",
  "elapse": "281.288µs",
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1676337568, 0 ],
      [ "wave.sin", 1676337569, 0.406736 ]
    ]
  }
}
```

**Response in BOX format**

Set query param `format=box` in the request.

```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" --data-urlencode "format=box"
```

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

```
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" --data-urlencode "format=csv"
```

The response comes with `Content-Type: text/csv`

```csv
NAME,TIME,VALUE
wave.sin,1676337568,0.000000
wave.sin,1676337569,0.406736
```

## Post JSON

It is also possible to request query in JSON form as below example.

**Request JSON message**

| name         | type       |  description                        |
|:------------ |:-----------|:------------------------------------|
| q            | string     | SQL query string                    |

```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    -H 'Content-Type: application/json' \
    -d '{ "q":"select * from EXAMPLE" }'
```

## Post Form Data

HTML Form data format is available too. HTTP header `Content-type` should be `application/x-www-form-urlencoded` in this case.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from TAGDATA"
```

## DDL

The HTTP "Query" API doesn't accept only "SELECT" SQL but also DDL. So it is possible to create and drop tables via HTTP API

### Create table

```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```

- response

    ```json
    {"success":true,"reason":"success","elapse":"92.489922ms"}
    ```

### Drop table

```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=drop table EXAMPLE"
```

- response

    ```json
    {"success":true,"reason":"executed.","elapse":"185.37292ms"}
    ```
