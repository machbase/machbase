---
toc: true
title: テーブルの作成と削除
type: docs
weight: 30
params:
    tabs:
        sync: true
---

HTTPの`query` APIは、`SELECT`文だけでなくDDLも実行できるため、HTTP APIでテーブルを作成・削除できます。

## テーブルの作成 {#create-table}

詳細は、[タグテーブル](/dbms/tag-table-usage/)を参照してください。

**リクエスト**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
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

**レスポンス**

```json
{"success":true,"reason":"Created successfully.","elapse":"92.489922ms"}
```

### IF NOT EXISTS {#if-not-exists}

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
  "q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={
  "q": (
  "create tag table if not exists EXAMPLE "
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
    q: "create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)",
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
  "create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
);

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

### TAG STATISTICS(タグ統計) {#tag-statistics태그-통계}

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode \
  "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)"
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
  "(name varchar(40) primary key, time datetime basetime, value double summarized)"
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
    q: "create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)",
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
  "create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)"
);

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

{{< callout emoji="📢" >}}
**注意** `summarized`キーワードは、対象のタグテーブルへのデータ取り込み時に、内部のタグデータ構造の統計を自動生成することを表します。詳細は、[タグ統計](/dbms/tag-table-usage/query-analysis/)を参照してください。
{{< /callout >}}

## テーブルの削除 {#drop-table}

**リクエスト**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=drop table EXAMPLE
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "q=drop table EXAMPLE"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "drop table EXAMPLE"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function dropTable() {
  const params = new URLSearchParams({
    q: "drop table EXAMPLE",
  });

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`);
  console.log(await response.text());
}

dropTable();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var sql = Uri.EscapeDataString("drop table EXAMPLE");

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**レスポンス**

```json
{"success":true,"reason":"Dropped successfully.","elapse":"185.37292ms"}
```
