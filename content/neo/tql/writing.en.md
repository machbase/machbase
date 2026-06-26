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
    VALUE DOUBLE SUMMARIZED
);
```

## `INSERT` CSV

### 1. Create *tql* file

Save the code below as `input-csv.tql`.
When you save a TQL script, the editor will display a link icon <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> in the top right corner. Click on it to copy the script file's address.

```js {linenos=table,hl_lines=["7"]}
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

### 2. HTTP POST

{{< tabs >}}
{{< tab name="HTTP" >}}

~~~
```http
POST http://127.0.0.1:5654/db/tql/input-csv.tql
Content-Type: text/csv

TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```
~~~

{{< /tab >}}
{{< tab name="cURL" >}}

Prepare data file as `input-csv.csv`

```csv
TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```

Invoke `input-csv.tql` with the data file with `curl` command

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary "@input-csv.csv"
```
{{< /tab >}}
{{< /tabs >}}

**Response:**

```json
{
  "data": {
    "message": "2 rows inserted."
  },
  "elapse": "10ms",
  "reason": "success",
  "success": true
}
```

### 3. MQTT PUBLISH

Prepare data file as `input-csv.csv`

```csv
TAG1,1628866800000000000,12
TAG1,1628953200000000000,13
```

Publish to the topic `db/tql/{tql_path}` as shown in the example below.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f input-csv.csv
```

## `APPEND` CSV

### 1. Create *tql* file

Save the code below as `append-csv.tql`.
When you save a TQL script, the editor will display a link icon <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> in the top right corner. Click on it to copy the script file's address.

```js {linenos=table,hl_lines=["7"]}
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

### 2. HTTP POST

{{< tabs >}}
{{< tab name="HTTP" >}}

~~~
```http
POST http://127.0.0.1:5654/db/tql/append-csv.tql
Content-Type: text/csv

TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```
~~~

{{< /tab >}}
{{< tab name="cURL" >}}

Prepare data file as `append-csv.csv`

```csv
TAG2,1628866800000000000,12
TAG2,1628953200000000000,13
```

Invoke `append-csv.tql` with the data file with `curl` command
```
curl -X POST http://127.0.0.1:5654/db/tql/append-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary "@append-csv.csv"
```
{{< /tab >}}
{{< /tabs >}}

### 3. MQTT PUBLISH

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


## Custom JSON

### 1. Create *tql* file

Use SCRIPT() function to parse a custom format JSON.

Save the code below as `input-json.tql`.

```js {linenos=table}
SCRIPT({
    obj = JSON.parse($.payload)
    obj.data.rows.forEach(r => $.yield(...r))
})
SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

### 2. HTTP POST

{{< tabs >}}
{{< tab name="HTTP" >}}

~~~
```http
POST http://127.0.0.1:5654/db/tql/input-json.tql
Content-Type: application/json

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
~~~

{{< /tab >}}
{{< tab name="cURL" >}}

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

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-json.tql \
    -H "Content-Type: application/json" \
    --data-binary "@input-json.json"
```
{{< /tab >}}
{{< /tabs >}}

### 3. MQTT PUBLISH

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

## Custom Text

When the data transforming is required for writing to the database, prepare the proper *tql* script and publish the data to the topic named `db/tql/`+`{tql_file.tql}`.

### 1. Create tql file

The example code below shows how to handle multi-lines text data for writing into a table.

{{< tabs >}}
{{< tab name="SCRIPT" >}}
```js {linenos=table,hl_lines=[11,12],linenostart=1}
SCRIPT({
    content = $.payload;
    if (!content || content === '') {
        content = "12345\n 23456\n 78901\n 89012\n 90123";
    }
    lines = content
        .split(/\r?\n/)
        .map(line => line.trim())     // trim spaces
        .filter(line => line !== ""); // filter empty lines
    lines.forEach((line, idx) => {
        part = line.substring(0, 2);  // takes the first 2 letters
        $.yield('text_'+idx, (new Date()), parseInt(part))
    });
})
CSV()
// SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```
{{</ tab >}}
{{< tab name="MAP" >}}
Transforming using MAP functions.
```js {linenos=table,hl_lines=["13-15"],linenostart=1}
// payload() returns the payload that arrived via HTTP-POST or MQTT,
// The ?? operator means that if tql is called without content,
//        the right side value is applied
// It is a good practice while the code is being developed on the tql editor of web-ui.
STRING( payload() ?? ` 12345
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
{{</ tabs >}}


**Result**

```csv
text_0,2023-12-02 11:03:36.054,12
text_1,2023-12-02 11:03:36.054,23
text_2,2023-12-02 11:03:36.054,78
text_3,2023-12-02 11:03:36.054,89
text_4,2023-12-02 11:03:36.054,90
```

Run the code above and if there is no error and works as expected, 
then replace the last line `CSV()` with `SQL(...)`.

Save the code as "script-post-lines.tql", then send some test data to the topic `db/tql/script-post-lines.tql`.

### 3. HTTP POST

For the note, the same *tql* file also works with HTTP POST.

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/tql/script-post-lines.tql
Content-Type: text/plain

110000
221111
332222
442222
```
~~~
{{</ tab >}}
{{< tab name="cURL" >}}
```sh
curl http://127.0.0.1:5654/db/tql/script-post-lines.tql \
  -H "Content-Type: text/plain" \
  -d @- << 'EOF'
110000
221111
332222
442222
EOF
```
{{</ tab >}}
{{</ tabs >}}

**Response:**

```json
{
  "data": {
    "message": "4 rows inserted."
  },
  "elapse": "15.80275ms",
  "reason": "success",
  "success": true
}
```

### 3. MQTT PUBLISH

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/script-post-lines.tql -s << 'EOF'
110000
221111
332222
442222
EOF
```

Then find if the data was successfully transformed and stored.

```sh
$ machbase-neo shell "select * from example where name like 'text_%'"
┌────────┬────────┬─────────────────────────┬───────┐
│ ROWNUM │ NAME   │ TIME                    │ VALUE │
├────────┼────────┼─────────────────────────┼───────┤
│      1 │ text_0 │ 2026-06-26 09:25:57.535 │    11 │
│      2 │ text_1 │ 2026-06-26 09:25:57.535 │    22 │
│      3 │ text_2 │ 2026-06-26 09:25:57.544 │    33 │
│      4 │ text_3 │ 2026-06-26 09:25:57.545 │    44 │
└────────┴────────┴─────────────────────────┴───────┘
4 rows selected.
```
