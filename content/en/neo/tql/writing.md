---
title: As Writing API
type: docs
weight: 04
---


{{< callout type="info" >}}
For the examples, create a table with the following SQL statements.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
VALUE DOUBLE SUMMARIZED);
```

## `INSERT` CSV

| Icon      | Description |
|-----------|:------------|
| {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}} | When tql script is saved, the editor shows the link icon on the top right corner, click it to copy the address of the script file. |


{{% steps %}}

### Save *tql* file

Save the code below as `input-csv.tql`.

```js
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
INSERT("name", "time", "value", table("example"))
```

### HTTP POST

Prepare data file as `input-csv.csv`

```csv
TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```

Invoke `input-csv.tql` with the data file with `curl` command

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-csv.tql \
    -H "Content-Type: application/csv" \
    --data-binary "@input-csv.csv"
```

### MQTT PUBLISH

Prepare data file as `input-csv.csv`

```csv
TAG1,1628866800000000000,12
TAG1,1628953200000000000,13
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f input-csv.csv
```

{{% /steps %}}

## `APPEND` CSV

{{% steps %}}

### Save *tql* file

Save the code below as `append-csv.tql`.

```js
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

### HTTP POST

Prepare data file as `append-csv.csv`

```csv
TAG2,1628866800000000000,12
TAG2,1628953200000000000,13
```

Invoke `append-csv.tql` with the data file with `curl` command
```
curl -X POST http://127.0.0.1:5654/db/tql/append-csv.tql \
    -H "Content-Type: application/csv" \
    --data-binary "@append-csv.csv"
```

### MQTT PUBLISH

Prepare data file as `append-csv.csv`

```csv
TAG3,1628866800000000000,12
TAG3,1628953200000000000,13
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f append-csv.csv
```

{{% /steps %}}


## Custom JSON

{{% steps %}}

### Save *tql* file

Use SCRIPT() function to parse a custom format JSON.

Save the code below as `input-json.tql`.

```js
BYTES(payload())
SCRIPT({
  json := import("json")
  ctx := import("context")
  val := ctx.value()
  obj := json.decode(val[0])
  for i := 0; i < len(obj.data.rows); i++ {
    ctx.yield(obj.data.rows[i][0], obj.data.rows[i][1], obj.data.rows[i][2])
  }
})
INSERT("name", "time", "value", table("example"))
```

### HTTP POST

Prepare data file as `input-json.json`

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG0", 1628866800000000000, 12 ],
      [ "TAG0", 1628953200000000000, 13 ]
    ]
  }
}
```

Invoke `input-csv.tql` with the data file with `curl` command
```
curl -X POST http://127.0.0.1:5654/db/tql/input-json.tql \
    -H "Content-Type: application/json" \
    --data-binary "@input-json.json"
```

### MQTT PUBLISH

Prepare data file as `input-json.json`

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG1", 1628866800000000000, 12 ],
      [ "TAG1", 1628953200000000000, 13 ]
    ]
  }
}
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-json.tql \
    -f input-json.json
```
{{% /steps %}}

## Custom Text

When the data transforming is required for writing to the database, prepare the proper *tql* script and publish the data to the topic named `db/tql/`+`{tql_file.tql}`.

The example code below shows how to handle multi-lines text data for writing into a table.

{{< tabs items="MAP,SCRIPT">}}
{{< tab >}}
Transforming using MAP functions
```js {linenos=table,hl_lines=["13-15"],linenostart=1}
// payload() returns the payload that arrived via HTTP-POST or MQTT,
// The ?? operator means that if tql is called without content,
//        the right side value is applied
// It is a good practice while the code is being developed on the tql editor of web-ui.
STRING(payload() ?? ` 12345
                     23456
                     78901
                     89012
                     90123
                  `, separator('\n'), trimspace(true))
FILTER( len(value(0)) > 0 )   // filter empty line
// transforming data
MAPVALUE(-1, time("now"))     // equiv. PUSHVALUE(0, time("now"))
MAPVALUE(-1, "text_"+key())   // equiv. PUSHVALUE(0, "text_"+key())
MAPVALUE(2, strSub( value(2), 0, 2 ) )

// Run this code in the tql editor of web-ui for testing
CSV( timeformat("DEFAULT") )
// Use APPEND(table('example')) for the real action
// APPEND(table('example'))
```
{{</ tab >}}
{{< tab >}}
Alternative version of transforming using SCRIPT()
```js {linenos=table,hl_lines=["9-22"],linenostart=1}
STRING(payload() ?? ` 12345
                     23456
                     78901
                     89012
                     90123
                  `, separator('\n'), trimspace(true))
FILTER( len(value(0)) > 0) // filter empty line
// transforming data
SCRIPT({
  text := import("text")
  times := import("times")
  ctx := import("context")
  key := ctx.key()
  values := ctx.value()
  str := text.trim_space(values[0]) // trim spaces
  str = text.substr(str, 0, 2)      // takes the first 2 letters of the line
  ctx.yieldKey(
      "text_"+key,                // compose new key (which is NAME column of the table)
      times.now(),                // current time
      text.parse_int(str, 10, 64) // convert to number type 
  )
})
CSV()
```
{{</ tab >}}
{{</ tabs >}}

**Result**
```csv
text_1,2023-12-02 11:03:36.054,12
text_2,2023-12-02 11:03:36.054,23
text_3,2023-12-02 11:03:36.054,78
text_4,2023-12-02 11:03:36.054,89
text_5,2023-12-02 11:03:36.054,90
```

Run the code above and if there is no error and works as expected, 
then replace the last line `CSV()` with `APPEND(table('example'))`.

Save the code as "script-post-lines.tql", then send some test data to the topic `db/tql/script-post-lines.tql`.

- `cat lines.txt`

```
110000
221111
332222
442222
```

### HTTP POST

For the note, the same *tql* file also works with HTTP POST.

```sh
curl -H "Content-Type: text/plain" \
    --data-binary @lines.txt \
    http://127.0.0.1:5654/db/tql/script-post-lines.tql
```

### MQTT PUBLISH

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/script-post-lines.tql \
    -f lines.txt
```

Then find if the data was successfully transformed and stored.

```sh
$ machbase-neo shell "select * from example where name like 'text_%'"
 ROWNUM  NAME    TIME(LOCAL)              VALUE     
────────────────────────────────────────────────────
      1  text_3  2023-07-14 08:51:10.926  44.000000 
      2  text_0  2023-07-14 08:51:10.925  11.000000 
      3  text_1  2023-07-14 08:51:10.926  22.000000 
      4  text_2  2023-07-14 08:51:10.926  33.000000 
4 rows fetched.
```
