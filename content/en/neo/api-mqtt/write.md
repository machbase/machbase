---
title: MQTT Write API
type: docs
weight: 30
---

## Topic MQTT v3.1/v3.1.1

The topic to write data is named with table name of the destination.

To utilize payload formats other than JSON, construct the MQTT topic by concatenating the table name, payload format, and compression type, each separated by a colon (`:`).

The full syntax of the topic is:

```
db/{method}/{table}:{format}:{compress}
```

**method**:  There are two methods for writing data - `append` and `write`.
The `append` is recommend for the general situation of MQTT environment.
- `append`: writing data in append mode.
- `write`: writing data in INSERT sql statement.

**format**: Current version of machbase-neo supports `json` and `csv`. The default format is `json`.

**compress**: Currently `gzip` is supported.

**Examples**

- `db/append/EXAMPLE` means writing data to the table `EXAMPLE` in `append` method and the payload is JSON.

- `db/append/EXAMPLE:json` is equivalent the example above. The last `:json` part can be omitted, because `json` is the default format.

- `db/append/EXAMPLE:json:gzip` means writing data to the table `EXAMPLE` in `append` method and the payload is gzip compressed JSON.

- `db/append/EXAMPLE:csv` means writing data to the table `EXAMPLE` in `append` method and the payload is CSV.

- `db/write/EXAMPLE:csv` means writing data to the table `EXAMPLE` with `INSERT INTO...` SQL statement and the payload is CSV.

- `db/write/EXAMPLE:csv:gzip` means writing data to the table `EXAMPLE` with `INSERT INTO...` SQL statement and the payload is gzip compressed CSV.


## Topic MQTT v5

{{< neo_since ver="8.0.33" />}}

In MQTT v5, user properties are custom key-value pairs that can be attached to each message. They offer greater flexibility compared to previous versions(MQTT v3.1/v3.1.1) and allow for additional metadata to be included with the message.

{{< callout emoji="📌" >}}
Note: It is also possible to use MQTT v3.1 topic syntax with MQTT v5 without using custom properties.
{{< /callout >}}

When using MQTT v5, the topic syntax can be simply `db/write/{table}`, and the following properties are supported:

| User Property  | Default  | Values                  |
|:---------------|:--------:|:------------------------|
| format         | `json`   | `csv`, `json`, `ndjson` |
| timeformat     | `ns`     | Time format: `s`, `ms`, `us`, `ns` |
| tz             | `UTC`    | Time Zone: `UTC`, `Local` and location spec |
| compress       |          | `gzip`                  |
| method         | `insert` | `insert`, `append`      |
| reply          |          | Topic to which the server sends the result messages |


**Additional properties for format=csv** 

| User Property  | Default  | Values                  |
|:---------------|:--------:|:------------------------|
| delimiter      |`,`       |                         |
| header         |          | `skip`, `columns`       |


{{< callout emoji="📌" >}}
According to the semantics of append method, `header=columns` does not work with `method=append`.
{{< /callout >}}

## APPEND method

Since MQTT is a connection-oriented protocol, a client program can continuously send data while maintaining the same MQTT session. 
This is the real benefit of using MQTT over HTTP for writing data.

In this example, we use `mosquitto_pub` just for demonstration.
Since it makes a connection to MQTT server and close when it finishes to publish a single message.
You will barely see performance gains against HTTP `write` api or some cases it may be worse.<br/>
Use this MQTT method only when a client can keep a connection relatively long time and send multiple messages.

### JSON

**PUBLISH multiple records**

The payload format in the example below is an array of tuples (an array of arrays in JSON).
It appends multiple records to the table through a single MQTT message.
It is also possible to publish a single tuple, as shown below. Machbase Neo accepts both types of payloads via MQTT.

- mqtt-data.json

```json
[
    [ "my-car", 1670380342000000000, 32.1 ],
    [ "my-car", 1670380343000000000, 65.4 ],
    [ "my-car", 1670380344000000000, 76.5 ]
]
```

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -f ./mqtt-data.json
```

{{< /tab >}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE \
    -f ./mqtt-data.json
```

{{< /tab >}}
{{< /tabs >}}

**PUBLISH single record**

- mqtt-data.json

```json
[ "my-car", 1670380345000000000, 87.6 ]
```

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -f ./mqtt-data.json
```

{{< /tab >}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE \
    -f ./mqtt-data.json
```

{{< /tab >}}
{{< /tabs >}}


**PUBLISH gzip JSON**

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property compress gzip \
    -f mqtt-data.json.gz
```

{{< /tab >}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:json:gzip \
    -f mqtt-data.json.gz
```

{{< /tab >}}
{{< /tabs >}}

### NDJSON

{{< neo_since ver="8.0.33" />}}

NDJSON (Newline Delimited JSON) is a format for streaming JSON data where each line is a valid JSON object. This is useful for processing large datasets or streaming data.
Each line should be a complete JSON object where all field names match the columns of the table.

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property format ndjson \
    -f mqtt-nd.json
```

{{< /tab >}}
{{< tab >}}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:ndjson \
    -f mqtt-nd.json
```

{{< /tab >}}
{{< /tabs >}}

### CSV

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

- mqtt-data.csv

```csv
NAME,TIME,VALUE
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
```

```sh {hl_lines=[6]}
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property header skip \
    -D PUBLISH user-property timeformat s \
    -f mqtt-data.csv
```

The highlighted `header` `skip` option indicate that the first line is a header.

{{< /tab >}}
{{< tab >}}

In MQTT v3.1, there is no mechanism to indicate whether the first line is a header or data.
Therefore, the payload must not include a header, and all fields should match the column order in the table.

- mqtt-data.csv

```
my-car,1670380346000000000,87.7
my-car,1670380347000000000,98.6
my-car,1670380348000000000,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:csv \
    -f mqtt-data.csv
```

{{< /tab >}}
{{< /tabs >}}

**PUBLISH gzip CSV**

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

```csv
NAME,TIME,VALUE
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property header skip \
    -D PUBLISH user-property timeformat s \
    -D PUBLISH user-property compress gzip \
    -f mqtt-data.csv.gz
```

{{< /tab >}}
{{< tab >}}

Topic = Table + `:csv:gzip`

```csv
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:csv:gzip \
    -f mqtt-data.csv.gz
```

{{< /tab >}}
{{< /tabs >}}

## INSERT method

It is strongly recommended using append method for the better performance through MQTT.
Refer to `insert` method only in situations where the order of data fields differs from the column order in the table or when not all columns are matched.

If the data has a different number of fields or a different order from the columns in the table,
use the `insert` method instead of the default `append` method.

### JSON


Since `db/write` works in `INSERT INTO table(...) VALUE(...)` SQL statement, it is required the columns in json payload.
The example of `data-write.json` is below.

- mqtt-data.json
```json {linenos=table,hl_lines=[3]}
{
  "data": {
    "columns": ["name", "time", "value"],
    "rows": [
      [ "wave.pi", 1687481466000000000, 1.2345],
      [ "wave.pi", 1687481467000000000, 3.1415]
    ]
  }
}
```

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

The `method` option defaults to `insert`, so it can be omitted.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method insert \
    -f mqtt-data.json
```

{{< /tab >}}
{{< tab >}}

Topic `db/write/{table}` is for `INSERT`.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -f mqtt-data.json
```

{{< /tab >}}
{{< /tabs >}}

### NDJSON

{{< neo_since ver="8.0.33" />}}

This request message is equivalent that consists INSERT SQL statement as `INSERT into {table} (columns...) values (values...)`

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343, "VALUE":2.002}
```

The `method` option defaults to `insert`, so it can be omitted.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method insert \
    -D PUBLISH user-property format ndjson \
    -D PUBLISH user-property timeformat s \
    -f mqtt-nd.json
```

{{< /tab >}}
{{< tab >}}

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

Topic `db/write/{table}:ndjson` is for `INSERT`.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:ndjson \
    -f mqtt-nd.json
```

{{< /tab >}}
{{< /tabs >}}

### CSV

Insert methods with CSV data that has a different number or order of fields compared to the table columns is supported only in MQTT v5 using custom properties.

{{< tabs items="MQTT v5,MQTT v3.1">}}
{{< tab >}}

```csv
VALUE,NAME,TIME
87.7,my-car,1670380346000
98.6,my-car,1670380347000
99.9,my-car,1670380348000
```

```sh {hl_lines=[5]}
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method insert \
    -D PUBLISH user-property header columns \
    -D PUBLISH user-property timeformat ms \
    -f mqtt-data.csv
```

{{< /tab >}}
{{< tab >}}

```csv
my-car,1670380346000000000,87.7
my-car,1670380347000000000,98.6
my-car,1670380348000000000,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE:csv \
    -f mqtt-data.csv
```

{{< /tab >}}
{{< /tabs >}}


## TQL

Topic `db/tql/{file.tql}` is for invoking TQL file.

When the data transforming is required for writing into the database, prepare the proper *tql* script and publish the data to the topic named `db/tql/{file.tql}`.

Please refer to the [As Writing API](../../tql/writing) for the writing data via MQTT and *tql*.


## Max message size

The maximum size of payload in a PUBLISH message is 256MB by MQTT specification. If a malicious or malfunctioning client sends large messages continuously it can consume all of network bandwidth and computing resource of server side then it may lead server to out of service status. It is good practice to set max message limit as just little more than what client applications demand. The default mqtt max message size is 1MB (`1048576`), it can be adjusted by command line flag like below or `MaxMessageSizeLimit` in the configuration file.

```sh
machbase-neo serve --mqtt-max-message 1048576
```

