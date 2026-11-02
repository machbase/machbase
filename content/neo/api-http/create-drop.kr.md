---
title: 테이블 생성과 삭제
type: docs
weight: 30
params:
    tabs:
        sync: true
---

HTTP `query` API는 `SELECT` 구문뿐 아니라 DDL도 실행할 수 있으므로 HTTP API로 테이블을 생성하거나 삭제할 수 있습니다.

토큰 인증은 기본적으로 활성화되어 있습니다. 아래 예시를 실행하려면
[API 보안](/neo/security/)의 안내에 따라 API 토큰을 발급받고 `<API_TOKEN>`을 발급받은 토큰으로 바꾸세요.

## Create table

자세한 내용은 [태그 테이블](/dbms/tag-table-usage/) 문서를 참고해 주십시오.

**요청**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
Authorization: Bearer <API_TOKEN>
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  -H "Authorization: Bearer <API_TOKEN>" \
  --data-urlencode \
  "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
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

**응답**

```json
{"success":true,"reason":"Created successfully.","elapse":"92.489922ms"}
```

### IF NOT EXISTS

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
Authorization: Bearer <API_TOKEN>
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  -H "Authorization: Bearer <API_TOKEN>" \
  --data-urlencode \
  "q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
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

### TAG STATISTICS(태그 통계)

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
**참고** `summarized` 키워드는 해당 태그 테이블에 데이터가 적재될 때 내부 태그 데이터 구조의 통계를 자동으로 생성한다는 의미입니다. 자세한 내용은 [태그 통계](/dbms/tag-table-usage/query-analysis/) 문서를 참고해 주십시오.
{{< /callout >}}

## Drop table

**요청**

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

**응답**

```json
{"success":true,"reason":"Dropped successfully.","elapse":"185.37292ms"}
```
