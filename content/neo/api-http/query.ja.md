---
toc: true
title: HTTPクエリ
type: docs
weight: 10
params:
    tabs:
        sync: true
---

Query APIのエンドポイントは、`/db/query`です。

このAPIは、`SELECT`だけでなく、`CREATE TABLE`、`ALTER TABLE`、`INSERT`など、すべてのSQL文に対応しています。

`/db/query` APIは、*GET*、*POST（JSON）*、*POST（form-data）*に対応し、どの方式でも同じパラメーターを使用できます。

たとえば、*GET*では`format`を`GET /db/query?format=csv`のようなクエリパラメーターで指定でき、
*POST-JSON*では、`{ "format": "csv" }`のようなJSONフィールドで渡せます。

**クエリの例**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh 
curl -o - http://127.0.0.1:5654/db/query \
   --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "select * from EXAMPLE limit 2"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("select * from EXAMPLE limit 2");

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}


## パラメーター {#매개변수}

**クエリパラメーター**

| パラメーター       | 既定値 | 説明                                                |
|:----------- |---------|:-----------------------------------------------------------|
| **q**       | _必須_ | 実行するSQL文です。                                     |
| p           |         | SQLプレースホルダーに渡すバインドパラメーターです。<br/>- `?`の位置パラメーター（JSON配列）：`["name", 1234, 1.23, true]` {{< neo_since ver="8.5.0" />}}<br/>- `:name`の名前付きパラメーター（JSONオブジェクト）：`{"name": "Alice", "n": 2}` {{< neo_since ver="8.7.0" />}} |
| db          |         | 複数データベース環境で使用する対象データベース名です。 {{< neo_since ver="8.7.0" />}} |
| format      | `json`    | 結果のデータ形式：json、csv、box、ndjson                  |
| timeformat  | `ns`      | 時刻の単位：s、ms、us、ns                                  |
| tz          | `UTC`     | タイムゾーン：UTC、Local、地域指定                             |
| binaryformat| `hex`     | バイナリのエンコーディング形式：hex、base64、bytes、preview {{< neo_since ver="8.5.2" />}} |
| compress    | _圧縮なし_   | 圧縮方式：gzip                                      |
| rownum      | `false`   | 行番号を含めるかどうか：true、false                            |

**`format=json`で使用できるパラメーター**

* これらのオプションは`format=json`の場合だけに使用でき、1リクエストにつき1つだけ指定できます。

| パラメーター       | 既定値 | 説明                               |
|:----------- |---------|:------------------------------------------|
| transpose   | false   | 結果を行配列ではなく列配列で返します。              |
| rowsFlatten | false   | JSONオブジェクトの`rows`フィールドの配列次元を1つ減らします。  |
| rowsArray   | false   | 各レコードをオブジェクトとする配列だけのJSONを返します。  |

**`format=csv`で使用できるパラメーター**

| パラメーター       | 既定値 | 説明                                     |
|:----------- |---------|:------------------------------------------------|
| header      |         | `skip`を指定するとヘッダーを含めません。              |
| precision   | `-1`    | 浮動小数点数の桁数：-1は丸めなし、0は整数表示       |

**時刻形式のオプション**
 
* 使用できる時刻形式は、[APIオプション/timeformat](../../options/timeformat/)を参照してください。

## 出力 {#출력}

レスポンスボディの全長が事前に分からない場合、`Transfer-Encoding: chunked`を設定し、`Content-Length`は省略します。応答の終了はHTTPのチャンク転送フレーミングで判定します。本文の改行では判定せず、HTTPクライアントに処理を任せてください。

- `Transfer-Encoding: chunked`: データを複数のチャンクに分けて送信し、ストリーミングに適しています。
- `Content-Length`ヘッダーなし：レスポンスボディの全長が事前に分からないことを示します。

### JSON {#json}

`/db/query` APIの既定の出力形式はJSONです。
クエリパラメーター`format=json`を指定するか、省略して既定値を使用します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "select * from EXAMPLE limit 2"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("select * from EXAMPLE limit 2");

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}


応答は`Content-Type: application/json`で返されます。

| 名前         | 型       |  説明                                                                 |
|:------------ |:-----------|:-----------------------------------------------------------------------------|
| **success**  | bool       | クエリの実行成功時に`true`                                                  |
| **reason**   | string     | 実行結果のメッセージ。`success`が`false`の場合はエラーメッセージを含みます。            |
| **elapse**   | string     | クエリ実行に要した時間                                                      |
| data         |            | 実行成功時だけに存在                                                    |
| data.columns | 文字列の配列 | 結果の列情報を表します。                                          |
| data.types   | 文字列の配列 | 各列のデータ型を表します。                                   |
| data.rows    | レコードの配列 | 結果レコードの配列です。<br/>`transpose=true`の場合、このフィールドは`cols`に置き換わります。 |
| data.cols    | 系列の配列  | 結果の列ごとの系列配列です。<br/>`transpose=true`の場合だけに存在します。  |

{{< tabs >}}
{{< tab name="既定" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1705381958775759000, 0.8563571936170834 ],
      [ "wave.sin", 1705381958785759000, 0.9011510331449053 ],
      [ "wave.sin", 1705381958795759000, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.887042ms"
}
```
{{< /tab >}}
{{< tab name="transpose" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &transpose=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "cols": [
      [ "wave.sin", "wave.sin", "wave.sin" ],
      [ 1705381958775759000, 1705381958785759000, 1705381958795759000 ],
      [ 0.8563571936170834, 0.9011510331449053, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "4.090667ms"
}
```
{{< /tab >}}
{{< tab name="rowsFlatten" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &rowsFlatten=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      "wave.sin", 1705381958775759000, 0.8563571936170834,
      "wave.sin", 1705381958785759000, 0.9011510331449053,
      "wave.sin", 1705381958795759000, 0.9379488170706388
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "2.255625ms"
}
```
{{< /tab >}}
{{< tab name="rowsArray" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &rowsArray=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      { "NAME": "wave.sin", "TIME": 1705381958775759000, "VALUE": 0.8563571936170834 },
      { "NAME": "wave.sin", "TIME": 1705381958785759000, "VALUE": 0.9011510331449053 },
      { "NAME": "wave.sin", "TIME": 1705381958795759000, "VALUE": 0.9379488170706388 }
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "3.178458ms"
}
```
{{< /tab >}}
{{< /tabs >}}

### NDJSON {#ndjson}

リクエストに、`format=ndjson`クエリパラメーターを指定します。 {{< neo_since ver="8.0.33" />}}

NDJSON（Newline Delimited JSON）は、各行が有効なJSONオブジェクトとなるストリーミング形式です。1つずつ処理できるため、大規模なデータやストリーミングデータに適しています。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=ndjson
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "q=select * from EXAMPLE limit 2" \
  --data-urlencode "format=ndjson"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "select * from EXAMPLE limit 2", "format": "ndjson"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
    format: "ndjson",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("select * from EXAMPLE limit 2");

var response = await client.GetAsync(
  $"http://127.0.0.1:5654/db/query?q={sql}&format=ndjson"
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

応答の`Content-Type`は、`application/x-ndjson`です。

```json
{"NAME":"wave.sin","TIME":1705381958775759000,"VALUE":0.8563571936170834}
{"NAME":"wave.sin","TIME":1705381958785759000,"VALUE":0.9011510331449053}

```

### CSV {#csv}

リクエストに、`format=csv`クエリパラメーターを指定します。

CSV形式も1行ずつ処理できるため、大規模なデータやストリーミングデータに適しています。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=csv
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "q=select * from EXAMPLE limit 2" \
  --data-urlencode "format=csv"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "select * from EXAMPLE limit 2", "format": "csv"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
    format: "csv",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("select * from EXAMPLE limit 2");

var response = await client.GetAsync(
  $"http://127.0.0.1:5654/db/query?q={sql}&format=csv"
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

応答の`Content-Type`は、`text/csv; charset=utf-8`です。

```csv
NAME,TIME,VALUE
wave.sin,1705381958775759000,0.8563571936170834
wave.sin,1705381958785759000,0.9011510331449053
```

### BOX {#box}

リクエストに、`format=box`クエリパラメーターを指定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=box
    &timeformat=default
    &tz=Asia/Seoul
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=box" \
    --data-urlencode "timeformat=default" \
    --data-urlencode "tz=Asia/Seoul"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={
    "q": "select * from EXAMPLE limit 2", 
    "format": "box",
    "timeformat": "default",
    "tz": "Asia/Seoul"
  },
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
    format: "box",
    timeformat: "default",
    tz: "Asia/Seoul",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("select * from EXAMPLE limit 2");

var response = await client.GetAsync(
  $"http://127.0.0.1:5654/db/query?q={sql}&format=box&timeformat=default&tz=Asia/Seoul"
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

結果はASCIIの罫線付きのプレーンテキストで、応答の`Content-Type`は`text/plain`です。

```
+---------+-------------------------+--------------------+
| NAME    | TIME(ASIA/SEOUL)        | VALUE              |
+---------+-------------------------+--------------------+
| work-10 | 2024-01-16 14:12:38.775 | 0.8563571936170834 |
| work-10 | 2024-01-16 14:12:38.785 | 0.9011510331449053 |
+---------+-------------------------+--------------------+
```

**CSV形式の応答**

リクエストに、`format=csv`クエリパラメーターを指定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=csv
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "q=select * from EXAMPLE limit 2" \
  --data-urlencode "format=csv"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "select * from EXAMPLE limit 2", "format": "csv"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
    format: "csv",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("select * from EXAMPLE limit 2");

var response = await client.GetAsync(
  $"http://127.0.0.1:5654/db/query?q={sql}&format=csv"
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

応答の`Content-Type`は、`text/csv`です。

```csv
NAME,TIME,VALUE
wave.sin,1705381958775759000,0.8563571936170834
wave.sin,1705381958785759000,0.9011510331449053
```

## POST JSON {#post-json}

以下の例のように、JSON形式でクエリを要求することもできます。

**リクエストのJSONメッセージ**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/json

{
  "q": "select * from EXAMPLE limit ?",
  "p": [2]
}
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    -H 'Content-Type: application/json' \
    --data-binary @- << 'EOF'
{
  "q": "select * from EXAMPLE limit ?",
  "p": [2]
}
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.post(
  "http://127.0.0.1:5654/db/query",
  json={"q": "select * from EXAMPLE limit ?", "p":[2]},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const response = await fetch("http://127.0.0.1:5654/db/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ q: "select * from EXAMPLE limit ?", p:[2] }),
  });

  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Net.Http.Json;

using var client = new HttpClient();

var response = await client.PostAsJsonAsync(
  "http://127.0.0.1:5654/db/query",
  new { q = "select * from EXAMPLE limit ?", p = new[] { 2 } }
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

## POST Form {#post-form}

HTMLフォームデータ形式も使用できます。この場合、HTTPヘッダー`Content-Type`を`application/x-www-form-urlencoded`に設定します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/x-www-form-urlencoded

q=select * from EXAMPLE limit 2
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
  --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.post(
  "http://127.0.0.1:5654/db/query",
  data={"q": "select * from EXAMPLE limit 2"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const body = new URLSearchParams({
    q: "select * from EXAMPLE limit 2",
  });

  const response = await fetch("http://127.0.0.1:5654/db/query", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  console.log(await response.text());
}

runQuery();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Collections.Generic;
using System.Net.Http;

using var client = new HttpClient();
using var content = new FormUrlEncodedContent(
  new[]
  {
    new KeyValuePair<string, string>("q", "select * from EXAMPLE limit 2"),
  }
);

var response = await client.PostAsync("http://127.0.0.1:5654/db/query", content);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

## 使用例 {#examples}

APIの詳細は、以下を参照してください。 
- [リクエストのエンドポイントとパラメーター](/neo/api-http/query)
- [wikipedia.orgのタイムゾーン一覧](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

このチュートリアルでは、以下のデータを事前に作成してください。

{{% steps %}}

### テーブルの作成 {#create-table}

~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/json

{
  "q":"create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
}
```
~~~

### データの挿入 {#insert-table}

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ns
Content-Type: application/json

{
    "data":{
      "columns":["NAME","TIME","VALUE"],
      "rows":[
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

{{% /steps %}}

### CSV形式での検索 {#select-in-csv}

**リクエスト**

CSV形式には、`format=csv`クエリパラメーターを指定します。

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=csv
```
~~~

**レスポンス**
```
NAME,TIME,VALUE
wave.sin,1676432361000000000,0.111111
wave.sin,1676432362111111111,0.222222
wave.sin,1676432363222222222,0.333333
wave.sin,1676432364333333333,0.444444
wave.sin,1676432365444444444,0.555555
```

### BOX形式での検索 {#select-in-box}

**リクエスト**

BOX形式には、`format=box`クエリパラメーターを指定します。

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
```
~~~

**レスポンス**

```
+----------+---------------------+----------+
| NAME     | TIME                | VALUE    |
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### 行番号付きのBOX形式での検索 {#select-in-box-with-rownum}

**リクエスト**

BOX形式には、`format=box`クエリパラメーターを指定します。

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &rownum=true
```
~~~

**レスポンス**

```
+--------+----------+---------------------+----------+
| ROWNUM | NAME     | TIME                | VALUE    |
+--------+----------+---------------------+----------+
|      1 | wave.sin | 1676432361000000000 | 0.111111 |
|      2 | wave.sin | 1676432362111111111 | 0.222222 |
|      3 | wave.sin | 1676432363222222222 | 0.333333 |
|      4 | wave.sin | 1676432364333333333 | 0.444444 |
|      5 | wave.sin | 1676432365444444444 | 0.555555 |
+--------+----------+---------------------+----------+
```


### ヘッダーなしのBOX形式での検索 {#select-in-box-without-heading}

**リクエスト**

ヘッダーなしのBOX形式には、`format=box`と`header=skip`クエリパラメーターを指定します。

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &header=skip
```
~~~

**レスポンス**

```
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### 整数値のBOX形式での検索 {#select-in-box-value-in-integer}

**リクエスト**

整数精度のBOX形式には、`format=box`と`precision=0`クエリパラメーターを指定します。

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &precision=0
```
~~~

**レスポンス**

```
+----------+---------------------+-------+
| NAME     | TIME                | VALUE |
+----------+---------------------+-------+
| wave.sin | 1676432361000000000 | 0     |
| wave.sin | 1676432362111111111 | 0     |
| wave.sin | 1676432363222222322 | 0     |
| wave.sin | 1676432364333333233 | 0     |
| wave.sin | 1676432365444444444 | 1     |
+----------+---------------------+-------+
```
