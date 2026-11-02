---
title: Create, Drop table
type: docs
weight: 30
params:
    tabs:
        sync: true
---

The HTTP "Query" API doesn't accept only "SELECT" SQL but also DDL. So it is possible to create and drop tables via HTTP API

Token authentication is enabled by default. For the examples below, obtain an API token
as described in [API Security](/neo/security/) and replace `<API_TOKEN>` with your token.

## Create table

Please refer to the docs for understanding what is the [Tag Tables](/dbms/feature-table/tag/)

**Request**

{{< tabs >}}
{{< tab name="HTTP">}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
Authorization: Bearer <API_TOKEN>
```
~~~
{{< /tab >}}
{{< tab name="cURL">}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  -H "Authorization: Bearer <API_TOKEN>" \
  --data-urlencode \
  "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< tab name="Python">}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  headers={"Authorization": "Bearer <API_TOKEN>"},
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

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`, {
    headers: { "Authorization": "Bearer <API_TOKEN>" },
  });
  console.log(await response.text());
}

createTable();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "Bearer <API_TOKEN>");
var sql = Uri.EscapeDataString(
  "create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
);

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**Response**

```json
{"success":true,"reason":"Created successfully.","elapse":"92.489922ms"}
```

### IF NOT EXISTS

{{< tabs>}}
{{< tab name="HTTP">}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
Authorization: Bearer <API_TOKEN>
```
~~~
{{< /tab >}}
{{< tab name="cURL">}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  -H "Authorization: Bearer <API_TOKEN>" \
  --data-urlencode \
  "q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< tab name="Python">}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  headers={"Authorization": "Bearer <API_TOKEN>"},
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

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`, {
    headers: { "Authorization": "Bearer <API_TOKEN>" },
  });
  console.log(await response.text());
}

createTable();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "Bearer <API_TOKEN>");
var sql = Uri.EscapeDataString(
  "create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
);

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

### TAG STATISTICS

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)
Authorization: Bearer <API_TOKEN>
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  -H "Authorization: Bearer <API_TOKEN>" \
  --data-urlencode \
  "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  headers={"Authorization": "Bearer <API_TOKEN>"},
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

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`, {
    headers: { "Authorization": "Bearer <API_TOKEN>" },
  });
  console.log(await response.text());
}

createTable();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "Bearer <API_TOKEN>");
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
**Note** The keyword "summarized" refers to the automatic generation of statistics on the internal tag data structure when data is written into the corresponding tag table. For more detailed information, please refer to the link below. [Tag Statistics](/dbms/feature-table/tag/manipulate/extract/#display-statistical-information-by-specific-tag-id)
{{< /callout >}}

## Drop table

**Request**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=drop table EXAMPLE
Authorization: Bearer <API_TOKEN>
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  -H "Authorization: Bearer <API_TOKEN>" \
  --data-urlencode "q=drop table EXAMPLE"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  headers={"Authorization": "Bearer <API_TOKEN>"},
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

  const response = await fetch(`http://127.0.0.1:5654/db/query?${params}`, {
    headers: { "Authorization": "Bearer <API_TOKEN>" },
  });
  console.log(await response.text());
}

dropTable();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "Bearer <API_TOKEN>");
var sql = Uri.EscapeDataString("drop table EXAMPLE");

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**Response**

```json
{"success":true,"reason":"Dropped successfully.","elapse":"185.37292ms"}
```
