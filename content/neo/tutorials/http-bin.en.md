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

In the HTTP API, the `bindata` column is represented differently depending on the format.

- When writing JSON, send the binary value as a base64-encoded string.
- When writing CSV, send the binary value as a base64-encoded field.
- When querying in JSON, the binary value is returned as a base64 string.
- When querying in CSV, the binary value is returned as a base64 string.

For the examples below:

- `AQI=` means the binary bytes `0x01 0x02`
- `AwQ=` means the binary bytes `0x03 0x04`

## Write binary data with JSON

This example uses the HTTP Write API with `method=insert`.

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
      ["json-insert", 1713675600, 1.23, "AQI="],
      ["json-insert", 1713675601, 2.34, "AwQ="]
    ]
  }
}
```
~~~

## Write binary data with CSV

This example uses the HTTP Write API with `method=append`.

The `bindata` field in CSV input should also be base64 text.

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=append
  &header=columns
Content-Type: text/csv

name,time,value,bindata
csv-append,1713675610,10.5,AQI=
csv-append,1713675611,20.5,AwQ=
```
~~~

## Query the data as JSON

Use the Query API with `format=json`.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-insert','csv-append')
  &timeformat=s
  &format=json
```
~~~

In the JSON response, the `bindata` column is returned as base64 text.

```json
{
  "data": {
    "rows": [
      ["json-insert", 1713675600, 1.23, "AQI="],
      ["json-insert", 1713675601, 2.34, "AwQ="],
      ["csv-append", 1713675610, 10.5, "AQI="],
      ["csv-append", 1713675611, 20.5, "AwQ="]
    ]
  }
}
```

## Query the data as CSV

Use the Query API with `format=csv`.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-insert','csv-append')
  &timeformat=s
  &format=csv
```
~~~

In the CSV response, the `bindata` column is returned as hexadecimal text with the `0x` prefix.

```csv
NAME,TIME,VALUE,BINDATA
json-insert,1713675600,1.23,AQI=
json-insert,1713675601,2.34,AwQ=
csv-append,1713675610,10.5,AQI=
csv-append,1713675611,20.5,AwQ=
```