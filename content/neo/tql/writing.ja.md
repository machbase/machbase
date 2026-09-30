---
title: 書き込みAPIとして使用
type: docs
weight: 04
toc: true
---

{{< callout type="info" >}}
以下の例を実行する前に、次のSQLでテーブルを準備してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## `INSERT` CSV {#insert-csv}

### 1. TQLファイルを作成する {#1-tql-파일-생성}

次のコードを `input-csv.tql` として保存してください。  
TQLスクリプトを保存すると、エディターの右上に <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> アイコンが表示されます。クリックすると、スクリプトのアドレスをコピーできます。

```js {linenos=table,hl_lines=["7"]}
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, datetimeType('ns'), 'time'),
    field(2, doubleType(), 'value'),
    header(false)
)
SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

### 2. HTTP POST {#2-http-post}

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

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary @- << 'EOF'
TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
EOF
```

{{< /tab >}}

{{< /tabs >}}

**レスポンス:**

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

### 3. MQTT PUBLISH {#3-mqtt-publish}

以下の例のように、`db/tql/{tql_path}` トピックにPUBLISHします。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/tql/input-csv.tql -s << 'EOF'
TAG1,1628866800000000000,12
TAG1,1628953200000000000,13
EOF
```

## `APPEND` CSV {#append-csv}

### 1. TQLファイルを作成する {#1-tql-파일-생성-1}

次のコードを `append-csv.tql` として保存してください。  
TQLスクリプトを保存すると、エディターの右上に <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> アイコンが表示されます。クリックすると、スクリプトのアドレスをコピーできます。

```js {linenos=table,hl_lines=["7"]}
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

### 2. HTTP POST {#2-http-post-1}

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

```sh
curl -X POST http://127.0.0.1:5654/db/tql/append-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary @- << 'EOF'
TAG2,1628866800000000000,12
TAG2,1628953200000000000,13
EOF
```

{{< /tab >}}

{{< /tabs >}}

### 3. MQTT PUBLISH {#3-mqtt-publish-1}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/tql/append-csv.tql -s << 'EOF'
TAG3,1628866800000000000,12
TAG3,1628953200000000000,13
EOF
```

## カスタムJSON {#커스텀-json}

### 1. TQLファイルを作成する {#1-tql-파일-생성-2}

`SCRIPT()` 関数でカスタム形式のJSONを解析します。  
次のコードを `input-json.tql` として保存してください。

```js {linenos=table}
SCRIPT({
    obj = JSON.parse($.payload)
    obj.data.rows.forEach(r => $.yield(...r))
})
SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

### 2. HTTP POST {#2-http-post-2}

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

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-json.tql \
    -H "Content-Type: application/json" \
    --data-binary @- << 'EOF'
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
EOF
```

{{< /tab >}}

{{< /tabs >}}

### 3. MQTT PUBLISH {#3-mqtt-publish-2}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/tql/input-json.tql -s << 'EOF'
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
EOF
```

## カスタムテキスト {#커스텀-텍스트}

データを加工してからデータベースに保存する場合は、適切な *tql* スクリプトを用意し、`db/tql/{tql_file.tql}` トピックにデータを送信してください。

### 1. TQLファイルを作成する {#1-tql-파일-생성-3}

次の例は、複数行のテキストデータを加工してテーブルに書き込む方法を示します。

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
        $.yield('text_'+idx, (new Date()), parseInt(part));
    });
})
CSV(timeformat('default'))
// SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

{{< /tab >}}

{{< tab name="MAP" >}}

MAP関数による変換例です。

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
// Uncomment the line below for the real action
// SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

{{< /tab >}}

{{< /tabs >}}

**結果の例**

```csv
text_0,2023-12-02 11:03:36.054,12
text_1,2023-12-02 11:03:36.054,23
text_2,2023-12-02 11:03:36.054,78
text_3,2023-12-02 11:03:36.054,89
text_4,2023-12-02 11:03:36.054,90
```

上記のコードを実行して問題がなければ、最後の行の `CSV()` を `SQL(...)` に変更してデプロイしてください。

スクリプトを `script-post-lines.tql` として保存し、テストデータを `db/tql/script-post-lines.tql` トピックに送信します。

### 2. HTTP POST {#2-http-post-3}

同じTQLファイルをHTTP POSTリクエストでも使用できます。

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

{{< /tab >}}

{{< tab name="cURL" >}}

```sh
curl http://127.0.0.1:5654/db/tql/script-post-lines.tql \
  -H "Content-Type: text/plain" \
  --data-binary @- << 'EOF'
110000
221111
332222
442222
EOF
```

{{< /tab >}}

{{< /tabs >}}

**レスポンス:**

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

### 3. MQTT PUBLISH {#3-mqtt-publish-3}

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/script-post-lines.tql -s << 'EOF'
110000
221111
332222
442222
EOF
```

その後、データが正しく変換・保存されたことを確認します。

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
