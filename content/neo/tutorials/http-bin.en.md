---
title: HTTP Binary Column Tutorial
type: docs
weight: 35
---

{{< callout emoji="📌">}}
This tutorial shows how to write and read a `binary` column through the HTTP `write` and `query` APIs.
{{< /callout >}}

{{< neo_since ver="8.5.0" />}}

## Create the example table

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double,
  bindata binary
);
```

In the HTTP API, a `binary` column is represented as text. The write API detects the input encoding from the value itself, and the query API uses the `binaryformat` parameter to choose the output encoding.

## Binary Text Rules

When the write API receives a string value for a `binary` column, it decodes the value by the following rules.

| Input text | Meaning |
| --- | --- |
| `0x0102` | Decoded as hexadecimal because it starts with the `0x` or `0X` prefix. |
| `AQI=` | Decoded as standard base64 because it does not have the `0x` prefix. |

The default query output is hexadecimal text.

| `binaryformat` | Output example | Description |
| --- | --- | --- |
| omitted or `hex` | `0x0102` | Prints all bytes as hexadecimal text. |
| `base64` | `AQI=` | Prints standard base64 text. |
| `bytes` | `[1 2]` | Prints byte values as a decimal array. |
| `preview` | `0x0102030405..` | Prints only the first bytes as hexadecimal text for quick inspection. |

For the examples below:

- `0x0102` and `AQI=` represent the same bytes.
- `0x0304` and `AwQ=` represent the same bytes.

## Write binary data with JSON

This example uses the HTTP Write API with `method=insert`. JSON input can use both hexadecimal text and base64 text.

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=insert
Content-Type: application/json

{
  "data": {
    "columns": ["name", "time", "value", "bindata"],
    "rows": [
      ["json-hex", 1713675600, 1.23, "0x0102"],
      ["json-base64", 1713675601, 2.34, "AwQ="]
    ]
  }
}
```
~~~

## Write binary data with CSV

This example uses the HTTP Write API with `method=append`. In CSV input, a `binary` column value is also text: values with the `0x` prefix are decoded as hexadecimal, and other values are decoded as base64.

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=append
  &header=columns
Content-Type: text/csv

name,time,value,bindata
csv-hex,1713675610,10.5,0x0102
csv-base64,1713675611,20.5,AwQ=
```
~~~

## Query the data with the default format

Use the Query API with `format=json`. If `binaryformat` is omitted, the `bindata` column is returned as hexadecimal text.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-hex','json-base64','csv-hex','csv-base64')
  &timeformat=s
  &format=json
```
~~~

```json
{
  "data": {
    "rows": [
      ["json-hex", 1713675600, 1.23, "0x0102"],
      ["json-base64", 1713675601, 2.34, "0x0304"],
      ["csv-hex", 1713675610, 10.5, "0x0102"],
      ["csv-base64", 1713675611, 20.5, "0x0304"]
    ]
  }
}
```

## Query the data as base64

To receive base64 text, set `binaryformat=base64`. The same option applies to `format=csv`, `format=ndjson`, and `format=box`.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-hex','json-base64','csv-hex','csv-base64')
  &timeformat=s
  &format=csv
  &binaryformat=base64
```
~~~

```csv
NAME,TIME,VALUE,BINDATA
json-hex,1713675600,1.23,AQI=
json-base64,1713675601,2.34,AwQ=
csv-hex,1713675610,10.5,AQI=
csv-base64,1713675611,20.5,AwQ=
```
