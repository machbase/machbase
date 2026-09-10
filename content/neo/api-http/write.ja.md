---
toc: true
title: HTTPの書き込み
type: docs
weight: 20
params:
    tabs:
        sync: true
---

書き込みAPIのエンドポイントは`/db/write/{TABLE}`です。`{TABLE}`は、データを保存するテーブル名です。

`query` APIでも`INSERT`文を実行できますが、リクエストごとに`q`パラメーター用のSQL文字列を構成する必要があり、非効率です。
データの取り込みには、通常は`INSERT`と同じように動作する`write` APIを使用します。
`write` APIでは、1回のリクエストで複数のレコードを一括挿入できます。

<a id="request-endpoint-and-parameters"></a>
## パラメーター {#매개변수}

**書き込みパラメーター**

| パラメーター       | 既定値 | 説明                                                    |
|:----------- |---------|:---------------------------------------------------------------|
| timeformat  | `ns`     | 時刻の単位：`s`、`ms`、`us`、`ns`                               |
| tz          | `UTC`    | タイムゾーン：`UTC`、`Local`、地域指定                              |
| method      | `insert` | 書き込み方式：`insert`、`append`                           |
| db          | `MACHBASEDB` | 複数データベース環境で対象データベース名を指定します。 {{< neo_since ver="8.7.0" />}} |

**INSERT vs. APPEND**

既定では、`/db/write` APIは`INSERT INTO ...`文でデータを保存します。少量のレコードの取り込みでは、`append`方式との性能差はほとんどありません。

数十万件以上の大量データを取り込む場合は、`method=append`を指定します。これにより、暗黙の既定値`method=insert`ではなく、Machbase Neoのappend方式を使用します。

**複数データベース**

サーバーが複数の名前付きデータベースをホストする場合、`db`クエリパラメーターで対象を指定できます。`method=insert`と`method=append`の両方に適用します。JSONボディのリクエストでは、クエリパラメーターの代わり、または併用して、最上位の`"db"`フィールドでも指定できます。両方を指定すると、クエリパラメーターが優先されます。

`db`が省略または空の場合、既定のデータベース`MACHBASEDB`が対象です。データベース名の形式が不正なら`400 Bad Request`を返します。データベースが存在しない場合や、接続ユーザーにアクセス権がない場合もエラーを返します。

```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?db=OTHERDB
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ]
        ]
    }
}
```

```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?db=OTHERDB' \
  -H "Content-Type: application/json" \
  --data-binary @- << 'EOF'
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ]
        ]
    }
}
EOF
```

**Content-Typeヘッダー**

machbase-neoサーバーは、`Content-Type`ヘッダーで入力データストリームの形式を判別します。
JSONには`Content-Type: application/json`、CSVには`Content-Type: text/csv`、行単位のJSONには`Content-Type: application/x-ndjson`を指定します。

**Content-Encodingヘッダー**

クライアントがgzip圧縮したストリームを送信する場合は、`Content-Encoding: gzip`ヘッダーを設定し、入力データのエンコーディングをmachbase-neoに通知します。

## 入力 {#inputs}

### JSON {#json}

このリクエストメッセージは、`INSERT INTO {table} (columns...) VALUES (values...)`文と同じ構造です。

| 名前         | 型       |  説明            |
|:------------ |:-----------|:------------------------|
| data         | object     | データボディ全体        |
| data.columns | 文字列の配列 | 列の一覧を指定します。 |
| data.rows    | タプルの配列  | レコード値の配列です。   |

**JSON**

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
```

`Content-Type`ヘッダーを`application/json`に設定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
  -H "Content-Type: application/json" \
  --data-binary @- << 'EOF'
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

payload = {
  "data": {
  "columns": ["name", "time", "value"],
  "rows": [
      ["json-data", 1670380342000000000, 1.0001],
      ["json-data", 1670380343000000000, 2.0002],
  ],
  }
}

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  json=payload,
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeJson() {
  const payload = {
    data: {
      columns: ["name", "time", "value"],
      rows: [
        ["json-data", 1670380342000000000, 1.0001],
        ["json-data", 1670380343000000000, 2.0002],
      ],
    },
  };

  const response = await fetch("http://127.0.0.1:5654/db/write/EXAMPLE", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  console.log(await response.text());
}

writeJson();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Net.Http.Json;

using var client = new HttpClient();

var response = await client.PostAsJsonAsync(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  new
  {
    data = new
    {
      columns = new[] { "name", "time", "value" },
      rows = new object[]
      {
        new object[] { "json-data", 1670380342000000000L, 1.0001 },
        new object[] { "json-data", 1670380343000000000L, 2.0002 },
      },
    },
  }
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**圧縮JSON**

入力ストリームがgzip圧縮されている場合は、`Content-Encoding: gzip`ヘッダーでmachbase-neoに通知します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/json
Content-Encoding: gzip

< /csv/post-data.json.gz
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
  -H "Content-Type: application/json" \
  -H "Content-Encoding: gzip" \
  --data-binary "@post-data.json.gz"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import gzip
import json

import requests

payload = {
  "data": {
  "columns": ["name", "time", "value"],
  "rows": [
      ["json-data", 1670380342000000000, 1.0001],
      ["json-data", 1670380343000000000, 2.0002],
  ],
  }
}

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  headers={
  "Content-Type": "application/json",
  "Content-Encoding": "gzip",
  },
  data=gzip.compress(json.dumps(payload).encode("utf-8")),
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeCompressedJson() {
  const payload = {
    data: {
      columns: ["name", "time", "value"],
      rows: [
        ["json-data", 1670380342000000000, 1.0001],
        ["json-data", 1670380343000000000, 2.0002],
      ],
    },
  };

  const stream = new Blob([JSON.stringify(payload)])
  .stream()
  .pipeThrough(new CompressionStream("gzip"));
  const compressedBody = await new Response(stream).blob();

  const response = await fetch("http://127.0.0.1:5654/db/write/EXAMPLE", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Encoding": "gzip",
    },
    body: compressedBody,
  });

  console.log(await response.text());
}

writeCompressedJson();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.IO.Compression;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

using var client = new HttpClient();

var payload = new
{
  data = new
  {
    columns = new[] { "name", "time", "value" },
    rows = new object[]
    {
      new object[] { "json-data", 1670380342000000000L, 1.0001 },
      new object[] { "json-data", 1670380343000000000L, 2.0002 },
    },
  },
};

var json = JsonSerializer.Serialize(payload);
using var buffer = new MemoryStream();
using (var gzip = new GZipStream(buffer, CompressionMode.Compress, leaveOpen: true))
using (var writer = new StreamWriter(gzip, Encoding.UTF8))
{
  writer.Write(json);
}

using var content = new ByteArrayContent(buffer.ToArray());
content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
content.Headers.ContentEncoding.Add("gzip");

var response = await client.PostAsync("http://127.0.0.1:5654/db/write/EXAMPLE", content);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**timeformatを使用するJSON**

時刻フィールドがUNIXエポックではなく文字列形式の場合は、`timeformat`と`tz`を指定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=DEFAULT
    &tz=Asia/Seoul
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", "2022-12-07 02:32:22", 1.0001 ],
            [ "json-data", "2022-12-07 02:32:23", 2.0002 ]
        ]
    }
}
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?'\
'timeformat=DEFAULT&'\
'tz=Asia/Seoul' \
  -H "Content-Type: application/json" \
  --data-binary @- << 'EOF'
{
  "data": {
    "columns":["name", "time", "value"],
    "rows": [
        [ "json-data", "2022-12-07 02:32:22", 1.0001 ],
        [ "json-data", "2022-12-07 02:32:23", 2.0002 ]
    ]
  }
}
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

payload = {
  "data": {
  "columns": ["name", "time", "value"],
  "rows": [
      ["json-data", "2022-12-07 02:32:22", 1.0001],
      ["json-data", "2022-12-07 02:32:23", 2.0002],
  ],
  }
}

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  params={"timeformat": "DEFAULT", "tz": "Asia/Seoul"},
  json=payload,
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeJson() {
  const payload = {
    data: {
      columns: ["name", "time", "value"],
      rows: [
        ["json-data", "2022-12-07 02:32:22", 1.0001],
        ["json-data", "2022-12-07 02:32:23", 2.0002],
      ],
    },
  };

  const params = new URLSearchParams({
    timeformat: "DEFAULT",
    tz: "Asia/Seoul",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/write/EXAMPLE?${params}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  console.log(await response.text());
}

writeJson();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Net.Http.Json;

using var client = new HttpClient();

var response = await client.PostAsJsonAsync(
  "http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=DEFAULT&tz=Asia/Seoul",
  new
  {
    data = new
    {
      columns = new[] { "name", "time", "value" },
      rows = new object[]
      {
        new object[] { "json-data", "2022-12-07 02:32:22", 1.0001 },
        new object[] { "json-data", "2022-12-07 02:32:23", 2.0002 },
      },
    },
  }
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

### NDJSON {#ndjson}

NDJSON（Newline Delimited JSON）は、各行が有効なJSONオブジェクトとなるストリーミング形式です。大規模なデータやストリーミングデータの処理に適しています。

このリクエストメッセージも、`INSERT INTO {table} (columns...) VALUES (values...)`文と同じ構造です。

**NDJSON**

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

`Content-Type`ヘッダーを`application/x-ndjson`に設定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/x-ndjson

{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- << 'EOF'
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import json

import requests

rows = [
  {"NAME": "ndjson-data", "TIME": 1670380342000000000, "VALUE": 1.001},
  {"NAME": "ndjson-data", "TIME": 1670380343000000000, "VALUE": 2.002},
]
payload = "\n".join(json.dumps(row) for row in rows)

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  headers={"Content-Type": "application/x-ndjson"},
  data=payload,
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeNdjson() {
  const payload = [
    JSON.stringify({ NAME: "ndjson-data", TIME: 1670380342000000000, VALUE: 1.001 }),
    JSON.stringify({ NAME: "ndjson-data", TIME: 1670380343000000000, VALUE: 2.002 }),
  ].join("\n");

  const response = await fetch("http://127.0.0.1:5654/db/write/EXAMPLE", {
    method: "POST",
    headers: { "Content-Type": "application/x-ndjson" },
    body: payload,
  });

  console.log(await response.text());
}

writeNdjson();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

using var client = new HttpClient();

var lines = new[]
{
  JsonSerializer.Serialize(new { NAME = "ndjson-data", TIME = 1670380342000000000L, VALUE = 1.001 }),
  JsonSerializer.Serialize(new { NAME = "ndjson-data", TIME = 1670380343000000000L, VALUE = 2.002 }),
};

using var content = new StringContent(string.Join("\n", lines), Encoding.UTF8, "application/x-ndjson");
var response = await client.PostAsync("http://127.0.0.1:5654/db/write/EXAMPLE", content);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}


**timeformatを使用するNDJSON**

時刻フィールドがUNIXエポックではなく文字列形式の場合は、以下のように指定します。

```json
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
```

`timeformat`と`tz`パラメーターを指定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=DEFAULT
    &tz=Local
Content-Type: application/x-ndjson

{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=Default&tz=Local' \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- << 'EOF'
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import json

import requests

rows = [
  {"NAME": "ndjson-data", "TIME": "2022-12-07 02:33:22", "VALUE": 1.001},
  {"NAME": "ndjson-data", "TIME": "2022-12-07 02:33:23", "VALUE": 2.002},
]
payload = "\n".join(json.dumps(row) for row in rows)

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  params={"timeformat": "Default", "tz": "Local"},
  headers={"Content-Type": "application/x-ndjson"},
  data=payload,
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeNdjson() {
  const payload = [
    JSON.stringify({ NAME: "ndjson-data", TIME: "2022-12-07 02:33:22", VALUE: 1.001 }),
    JSON.stringify({ NAME: "ndjson-data", TIME: "2022-12-07 02:33:23", VALUE: 2.002 }),
  ].join("\n");

  const params = new URLSearchParams({
    timeformat: "Default",
    tz: "Local",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/write/EXAMPLE?${params}`, {
    method: "POST",
    headers: { "Content-Type": "application/x-ndjson" },
    body: payload,
  });

  console.log(await response.text());
}

writeNdjson();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

using var client = new HttpClient();

var lines = new[]
{
  JsonSerializer.Serialize(new { NAME = "ndjson-data", TIME = "2022-12-07 02:33:22", VALUE = 1.001 }),
  JsonSerializer.Serialize(new { NAME = "ndjson-data", TIME = "2022-12-07 02:33:23", VALUE = 2.002 }),
};

using var content = new StringContent(string.Join("\n", lines), Encoding.UTF8, "application/x-ndjson");
var response = await client.PostAsync(
  "http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=Default&tz=Local",
  content
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}


### CSV {#csv}

以下のオプションは、ボディがCSV形式の場合だけに適用します。

| パラメーター         | 既定値 | 説明                                                                 |
|:------------- |---------|:----------------------------------------------------------------------------|
| header        |         | `skip`：先頭行をスキップします。<br/>`columns`：ヘッダー行の項目がテーブルの列名に対応します。 |
| delimiter     | ,       | フィールド区切り文字                                                                   |

CSVデータにヘッダー行がある場合は、`header=skip`クエリパラメーターで先頭行を無視します。

ヘッダー行で使用する列を指定するには、`header=columns`を使用します。ヘッダーはテーブルの列名と一致する必要があり、内部で`INSERT INTO TABLE(columns...) VALUES(...)`の列一覧として使用します。

ヘッダー行がなく、`header`オプションを省略する場合、各行のフィールドはテーブルの全列の順序と一致する必要があります。`INSERT INTO TABLE VALUES(...)`文に対応するためです。

> append方式の特性上、`method=append`では`header=columns`オプションは動作しません。

**header=skip**

`header=skip`を指定すると、サーバーは先頭行を無視します。データはテーブルの列順に並べてください。

```csv
NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
```

`Content-Type`ヘッダーは、`text/csv`を指定します。
{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip
Content-Type: text/csv

NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip \
  -H "Content-Type: text/csv" \
  --data-binary @- << 'EOF'
NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

payload = """NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
"""

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  params={"header": "skip"},
  headers={"Content-Type": "text/csv"},
  data=payload,
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeCsv() {
  const payload = `NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002`;

  const response = await fetch("http://127.0.0.1:5654/db/write/EXAMPLE?header=skip", {
    method: "POST",
    headers: { "Content-Type": "text/csv" },
    body: payload,
  });

  console.log(await response.text());
}

writeCsv();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Text;

using var client = new HttpClient();

var payload = """
NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
""";

using var content = new StringContent(payload, Encoding.UTF8, "text/csv");
var response = await client.PostAsync(
  "http://127.0.0.1:5654/db/write/EXAMPLE?header=skip",
  content
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**header=columns**

CSVのフィールド順がテーブルの列順と異なる場合や、一部の列だけを含む場合は、`header=columns`を指定します。サーバーは先頭行を列名として扱います。以下の例では、内部で`INSERT INTO EXAMPLE (TIME, NAME, VALUE) VALUES(?, ?, ?)`と同じ文を生成します。

```csv
TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
```

`Content-Type`ヘッダーは、`text/csv`を指定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=columns
Content-Type: text/csv

TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=columns \
  -H "Content-Type: text/csv" \
  --data-binary @- << 'EOF'
TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

payload = """TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
"""

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  params={"header": "columns"},
  headers={"Content-Type": "text/csv"},
  data=payload,
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeCsv() {
  const payload = `TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002`;

  const response = await fetch("http://127.0.0.1:5654/db/write/EXAMPLE?header=columns", {
    method: "POST",
    headers: { "Content-Type": "text/csv" },
    body: payload,
  });

  console.log(await response.text());
}

writeCsv();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Text;

using var client = new HttpClient();

var payload = """
TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
""";

using var content = new StringContent(payload, Encoding.UTF8, "text/csv");
var response = await client.PostAsync(
  "http://127.0.0.1:5654/db/write/EXAMPLE?header=columns",
  content
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**圧縮CSV**

入力ストリームがgzip圧縮されている場合は、`Content-Encoding: gzip`ヘッダーでmachbase-neoに通知します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip
Content-Type: text/csv
Content-Encoding: gzip

< /csv/post-data.json.gz
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip \
  -H "Content-Type: text/csv" \
  -H "Content-Encoding: gzip" \
  --data-binary "@post-data.csv.gz"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import gzip

import requests

payload = """NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
"""

response = requests.post(
  "http://127.0.0.1:5654/db/write/EXAMPLE",
  params={"header": "skip"},
  headers={
  "Content-Type": "text/csv",
  "Content-Encoding": "gzip",
  },
  data=gzip.compress(payload.encode("utf-8")),
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeCompressedCsv() {
  const payload = `NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002`;

  const stream = new Blob([payload])
  .stream()
  .pipeThrough(new CompressionStream("gzip"));
  const compressedBody = await new Response(stream).blob();

  const response = await fetch("http://127.0.0.1:5654/db/write/EXAMPLE?header=skip", {
    method: "POST",
    headers: {
      "Content-Type": "text/csv",
      "Content-Encoding": "gzip",
    },
    body: compressedBody,
  });

  console.log(await response.text());
}

writeCompressedCsv();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.IO.Compression;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;

using var client = new HttpClient();

var payload = """
NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
""";

using var buffer = new MemoryStream();
using (var gzip = new GZipStream(buffer, CompressionMode.Compress, leaveOpen: true))
using (var writer = new StreamWriter(gzip, Encoding.UTF8))
{
  writer.Write(payload);
}

using var content = new ByteArrayContent(buffer.ToArray());
content.Headers.ContentType = new MediaTypeHeaderValue("text/csv");
content.Headers.ContentEncoding.Add("gzip");

var response = await client.PostAsync(
  "http://127.0.0.1:5654/db/write/EXAMPLE?header=skip",
  content
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}


**timeformatを使用するCSV**

`timeformat`と`tz`クエリパラメーターを指定します。

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?header=skip
    &timeformat=Default
    &tz=Asia/Seoul
Content-Type: text/csv

NAME,TIME,VALUE
csv-data,2022-12-07 11:39:32,1.0001
csv-data,2022-12-07 11:39:33,2.0002
```
~~~

## 例 {#예시}

APIの詳細は、[リクエストのエンドポイントとパラメーター](/neo/api-http/write/#request-endpoint-and-parameters)を参照してください。

**テストテーブル**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode \
  "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={
  "q": (
      "create tag table EXAMPLE "
      "(name varchar(40) primary key, time datetime basetime, value double)"
  )
  },
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function createTable() {
  const params = new URLSearchParams({
    q: "create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

createTable();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString(
  "create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
);

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**Time**

この例のサンプルファイルの時刻は、秒単位のUNIXエポック時刻です。読み込む際は、`timeformat=s`を指定してください。他の時刻精度のデータでは、その精度に合わせて変更します。Machbase Neoは、既定で時刻を`ナノ秒（ns）`として扱います。

### エポック時刻を使用するJSON {#json-with-epoch}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=s
Content-Type: application/json

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
~~~

**行の検索**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
```
~~~

### エポック時刻を使用するCSV {#csv-with-epoch}

以下のようにCSVにヘッダー行がある場合は、`header=skip`を指定します。

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=s
    &header=skip
Content-Type: text/csv

NAME,TIME,VALUE
wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144

```
~~~

### ヘッダーなしのCSV {#헤더-없는-csv}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s
Content-Type: text/csv

wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```
~~~

### CSV {#csv-1}

**Insert**

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
Content-Type: text/csv

wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111,0.222222
wave.sin,2023-02-15 03:39:23.222,0.333333
wave.sin,2023-02-15 03:39:24.333,0.444444
wave.sin,2023-02-15 03:39:25.444,0.555555
```
~~~

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &timeformat=Default
    &format=csv
```
~~~

**Append**

大容量のCSVファイルでは、append方式でinsert方式より数倍高速に取り込めます。

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s&method=append
Content-Type: text/csv

wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```
~~~

### タイムゾーンを指定したCSV {#시간대를-지정한-csv}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
    &tz=Asia/Seoul
Content-Type: text/csv

wave.sin,2023-02-15 12:39:21,0.111111
wave.sin,2023-02-15 12:39:22.111,0.222222
wave.sin,2023-02-15 12:39:23.222,0.333333
wave.sin,2023-02-15 12:39:24.333,0.444444
wave.sin,2023-02-15 12:39:25.444,0.555555
```
~~~

**UTCでの検索**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &timeformat=Default
    &format=csv
```
~~~

### `RFC3339` {#rfc3339}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=RFC3339
Content-Type: text/csv

wave.sin,2023-02-15T03:39:21Z,0.111111
wave.sin,2023-02-15T03:39:22Z,0.222222
wave.sin,2023-02-15T03:39:23Z,0.333333
wave.sin,2023-02-15T03:39:24Z,0.444444
wave.sin,2023-02-15T03:39:25Z,0.555555
```
~~~

**UTCでの検索**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=csv
    &timeformat=RFC3339
```
~~~

### タイムゾーン付きの`RFC3339Nano` {#시간대를-포함한-rfc3339nano}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=RFC3339Nano
    &tz=America/New_York
Content-Type: text/csv

wave.sin,2023-02-14T22:39:21.000000000-05:00,0.111111
wave.sin,2023-02-14T22:39:22.111111111-05:00,0.222222
wave.sin,2023-02-14T22:39:23.222222222-05:00,0.333333
wave.sin,2023-02-14T22:39:24.333333333-05:00,0.444444
wave.sin,2023-02-14T22:39:25.444444444-05:00,0.555555
```
~~~


**America/New_Yorkタイムゾーンでの検索**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=box
    &timeformat=RFC3339Nano
    &tz=America/New_York
```
~~~

### Timeformat {#timeformat}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
Content-Type: text/csv

wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111111111,0.222222
wave.sin,2023-02-15 03:39:23.222222222,0.333333
wave.sin,2023-02-15 03:39:24.333333333,0.444444
wave.sin,2023-02-15 03:39:25.444444444,0.555555
```
~~~

**UTCでの検索**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=csv
    &timeformat=Default

```
~~~

### カスタムTimeformat {#사용자-정의-timeformat}

- ニューヨークのタイムゾーンで`hour:min:sec-SPLIT-year-month-day`形式を使用

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=03:04:05.999999999-SPLIT-2006-01-02
    &tz=America/New_York
Content-Type: text/csv

wave.sin,10:39:21-SPLIT-2023-02-14 ,0.111111
wave.sin,10:39:22.111111111-SPLIT-2023-02-14 ,0.222222
wave.sin,10:39:23.222222222-SPLIT-2023-02-14 ,0.333333
wave.sin,10:39:24.333333333-SPLIT-2023-02-14 ,0.444444
wave.sin,10:39:25.444444444-SPLIT-2023-02-14 ,0.555555
```
~~~

**行の検索**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=csv
    &timeformat=2006-01-02 03:04:05.999999999
    &tz=America/New_York
```
~~~
