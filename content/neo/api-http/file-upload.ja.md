---
toc: true
title: ファイルのアップロード
type: docs
weight: 25
params:
    tabs:
        sync: true
---

 {{< neo_since ver="8.0.40" />}}

クライアントは、HTTPの*multipart/form-data*エンコーディングで、Machbase Neoに任意のファイルをアップロードできます。
添付したファイルは指定ディレクトリに保存され、
データベースは、そのファイルのメタデータをJSON文字列として列に保存します。

各パートの名前を列名、値をデータの文字列表現として、*multipart/form-data*形式で送信します。
保存先ディレクトリを指定するには、`JSON`型の列にファイルを添付し、`X-Store-Dir`ヘッダーを送信します。
`X-Store-Dir`のディレクトリがない場合は、サーバーが自動作成します。
ファイル本体は、UUID形式の一意の名前で、そのディレクトリに保存されます。

## ファイルのアップロード {#파일-업로드}

以下の例では、`STASH`テーブルが作成済みであることを前提とします。

```sql {hl_lines=[4]}
CREATE TAG TABLE STASH(
    NAME     VARCHAR(80)  primary key,
    TIME     DATETIME basetime,
    DATA     JSON
)
```

{{< tabs >}}
{{< tab name="HTTP" >}}
この例では、Visual Studio CodeのREST Client拡張機能を使用します。

~~~
```http
POST http://127.0.0.1:5654/db/write/STASH
Content-Type: multipart/form-data; boundary=----Boundary7MA4YWxkTrZu0gW

------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="NAME"

camera-1
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="TIME"

now
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="DATA"; filename="image_file.svg"
X-Store-Dir: /tmp/store
Content-Type: image/svg

<svg xmlns="http://w3.org" width="100" height="100" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="red" />
  <circle cx="50" cy="50" r="40" fill="blue" />
</svg>
------Boundary7MA4YWxkTrZu0gW--
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
この例では、`curl`の`-F`オプションで、*multipart/form-data*形式のPOSTリクエストを送信します。

```sh {hl_lines=[4]}
curl -X POST 'http://127.0.0.1:5654/db/write/STASH' \
  -F 'NAME=camera-1' \
  -F 'TIME=now' \
  -F 'DATA=@-;filename=image_file.svg;headers="X-Store-Dir: /tmp/store"' << 'EOF'
<svg xmlns="http://w3.org" width="100" height="100" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="red" />
  <circle cx="50" cy="50" r="40" fill="blue" />
</svg>
EOF
```
{{< /tab >}}
{{< tab name="Python" >}}
  この例では、`requests`で*multipart/form-data*形式のファイルをアップロードします。

  ```python
  import requests

  url = "http://127.0.0.1:5654/db/write/STASH"

  with open("./data/image_file.svg", "rb") as image_file:
    response = requests.post(
      url,
      data={"NAME": "camera-1", "TIME": "now"},
      files={"DATA": ("image_file.svg", image_file, "image/svg")},
      headers={"X-Store-Dir": "/tmp/store"},
    )

  response.raise_for_status()
  print(response.text)
  ```
{{< /tab >}}
{{< tab name="Javascript" >}}
この例では、`fetch`と`FormData`で*multipart/form-data*形式のファイルをアップロードします。

```javascript
async function uploadFile(file) {
  if (!file) {
    throw new Error("先にアップロードするファイルを選択してください。");
  }

  const formData = new FormData();
  formData.append("NAME", "camera-1");
  formData.append("TIME", "now");
  formData.append("DATA", file, file.name);

  const response = await fetch("http://127.0.0.1:5654/db/write/STASH", {
    method: "POST",
    headers: { "X-Store-Dir": "/tmp/store" },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  console.log(await response.text());
}

const fileInput = document.querySelector("input[type=file]");
uploadFile(fileInput.files[0]);
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Net.Http.Headers;

using var client = new HttpClient();
using var form = new MultipartFormDataContent();

form.Add(new StringContent("camera-1"), "NAME");
form.Add(new StringContent("now"), "TIME");

using var fileStream = File.OpenRead("./data/image_file.svg");
using var fileContent = new StreamContent(fileStream);
fileContent.Headers.ContentType = new MediaTypeHeaderValue("image/svg");
form.Add(fileContent, "DATA", "image_file.svg");

using var request = new HttpRequestMessage(HttpMethod.Post, "http://127.0.0.1:5654/db/write/STASH")
{
  Content = form,
};
request.Headers.Add("X-Store-Dir", "/tmp/store");

var response = await client.SendAsync(request);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

### レスポンスメッセージ {#응답-메시지}
アップロードが完了すると、サーバーは保存したファイルの情報を以下のように返します。

- ID : サーバーが割り当てた一意のID
- FN : 元のファイル名
- SZ : ファイルサイズ
- CT : コンテンツタイプ
- SD : サーバー側の保存先ディレクトリのパス

```json
{
  "success":true,
  "reason":"success, 1 record(s) inserted",
  "elapse":"10.611208ms",
  "data":{
    "files":{
      "DATA":{
        "ID":"1f174fd2-cbd9-6d0e-b8a7-23fa7e810e6d",
        "FN":"image_file.svg",
        "SZ":177,
        "CT":"image/svg+xml",
        "SD":"/tmp/store"
      }
    }
  }
}
```

### X-Store-Dir {#x-store-dir}

アップロードしたファイルは、`X-Store-Dir`ヘッダーのディレクトリに保存され、
ファイル名は、応答に含まれる`ID`値に基づいて生成されます。
前述の例のように、各パートのヘッダーに`X-Store-Dir`を含めることも、
リクエスト全体のヘッダーに指定することもできます。

**`${data}`**<br/>
`X-Store-Dir`のパスに`${data}`を使用すると、データベースのホームディレクトリを表します。このディレクトリは、machbase-neoの起動時に`--data`で指定します。省略した場合は、実行ファイルのディレクトリ配下の`machbase_home`を既定値として使用します。詳細は、[コマンドラインフラグ](/neo/operations/command-line/)を参照してください。

たとえば、`X-Store-Dir: ${data}/store`を指定すると、ファイルは`some/path/to/machbase_home/store/file_name_is_ID_of_the_response`に保存されます。

### メタデータ {#메타데이터}

上記の`DATA`列は、アップロードしたファイルのメタ情報を含むJSON形式の文字列として取得できます。

```sql
SELECT DATA FROM STASH
WHERE NAME = 'camera-1';
```

JSON Pathを使用することもできます。

```sql
SELECT DATA FROM STASH
WHERE NAME = 'camera-1'
AND DATA->'$.FN' = 'image_file.svg';
```

**`/db/query` 検索**

以下は、`/db/query` APIでSELECTクエリを実行する例です。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select DATA from STASH where NAME = 'camera-1'
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - 'http://127.0.0.1:5654/db/query' \
  --data-urlencode "q=select DATA from STASH\
  where NAME = 'camera-1'"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={"q": "select DATA from STASH where NAME = 'camera-1'"},
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select DATA from STASH where NAME = 'camera-1'",
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
var sql = Uri.EscapeDataString("select DATA from STASH where NAME = 'camera-1'");

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

**JSON Pathの検索：`->`表記**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select DATA from STASH where NAME = 'camera-1' and DATA->'$.FN' = 'image_file.svg'
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - 'http://127.0.0.1:5654/db/query' \
  --data-urlencode "q=select DATA from STASH\
  where NAME = 'camera-1' \
  and DATA->'$.FN' = 'image_file.svg'"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={
    "q": (
      "select DATA from STASH "
      "where NAME = 'camera-1' "
      "and DATA->'$.FN' = 'image_file.svg'"
    )
  },
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    q: "select DATA from STASH where NAME = 'camera-1' and DATA->'$.FN' = 'image_file.svg'",
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
var sql = Uri.EscapeDataString(
  "select DATA from STASH where NAME = 'camera-1' and DATA->'$.FN' = 'image_file.svg'"
);

var response = await client.GetAsync($"http://127.0.0.1:5654/db/query?q={sql}");
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

`DATA`列には、以下のファイル情報が保存されています。

```json
{
  "data": {
    "columns": [ "DATA" ],
    "types": [ "string" ],
    "rows": [
      [
        "{\"ID\":\"1ef8a87f-96bd-6576-9ff5-972fa7638db8\",\"FN\":\"image_file.svg\",\"SZ\":177,\"CT\":\"image/svg+xml\",\"SD\":\"/tmp/store\"}"
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "843.666µs"
}
```

JSON型の列から特定のフィールドを抽出するには、JSON Pathを使用します。

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?format=ndjson
    &q=SELECT NAME, TIME, DATA->'$.ID' as FID  FROM STASH WHERE NAME = 'camera-1'
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "format=ndjson"   \
  --data-urlencode "q=SELECT NAME, TIME, DATA->'$.ID' as FID  \
  FROM STASH WHERE NAME = 'camera-1'"
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query",
  params={
  "format": "ndjson",
  "q": "SELECT NAME, TIME, DATA->'$.ID' as FID FROM STASH WHERE NAME = 'camera-1'",
  },
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function runQuery() {
  const params = new URLSearchParams({
    format: "ndjson",
    q: "SELECT NAME, TIME, DATA->'$.ID' as FID FROM STASH WHERE NAME = 'camera-1'",
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
var sql = Uri.EscapeDataString(
  "SELECT NAME, TIME, DATA->'$.ID' as FID FROM STASH WHERE NAME = 'camera-1'"
);

var response = await client.GetAsync(
  $"http://127.0.0.1:5654/db/query?format=ndjson&q={sql}"
);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

```json
{"NAME":"camera-1","TIME":1728950208158594000,"FID":"1ef8a87f-96bd-6576-9ff5-972fa7638db8"}
{"NAME":"camera-1","TIME":1728953137384133000,"FID":"1ef8a8ec-b602-6cac-8fb1-ac9c0c1b981b"}
```

## ファイル内容の取得 {#파일-내용-조회}

ファイル本体には、クエリAPIでアクセスできます。

`http://{server_address}/db/query/file/{table}/{column}/{ID}`

TAGテーブルの場合は、`tag`パラメーターを指定すると応答を高速化できます。

`http://{server_address}/db/query/file/{tag_table}/{column}/{ID}?tag=camera-1`

LOGテーブルの`ID`は、レコードの挿入時刻に基づきます。TAGテーブルでは、レコードの基準時刻列から`ID`を生成します。

`ID`にはタイムスタンプ情報が含まれるため、Machbase NeoはTAGテーブルでは`TIME between A and B`、LOGテーブルでは`_ARRIVAL_TIME between A and B`を使い、検索範囲を絞り込みます。
`ID`のタイムスタンプは、基準時刻やLOGテーブルの`_ARRIVAL_TIME`と完全には一致しませんが、検索性能の改善に役立ちます。

### HTTP GET {#http-get}

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
GET http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o ./img-download.svg \
  http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.get(
  "http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8"
)
response.raise_for_status()
with open("./img-download.svg", "wb") as output_file:
  output_file.write(response.content)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function downloadFile() {
  const response = await fetch(
  "http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8"
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  const blob = await response.blob();

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "img-download.svg";
  link.click();
  URL.revokeObjectURL(link.href);
}

downloadFile();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;

using var client = new HttpClient();
var bytes = await client.GetByteArrayAsync(
  "http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8"
);

await File.WriteAllBytesAsync("./img-download.svg", bytes);
```
{{< /tab >}}
{{< /tabs >}}

### HTMLでの&lt;img&gt;の使用 {#html에서-ltimggt-사용}

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8"/>
</body>
</html>
```

TAGテーブルでタグ名が分かっている場合は、`tag`クエリパラメーターで検索性能を向上できます。

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8?tag=camera-1"/>
</body>
</html>
```

## 例 {#예시}

### JavaScript {#자바스크립트}

JavaScriptでファイルをアップロードする例です。

```js
const request = require('request');
const fs = require('fs');

let req = {
    method: 'POST',
    url: 'http://127.0.0.1:5654/db/write/STASH',
    headers: {"X-Store-Dir": "/tmp/store"},
    formData: {
        NAME: 'camera-1',
        TIME: 'now',
        DATA:  fs.createReadStream('./image_file.svg'), 
    },
};

request(req, function(err, res, body){
    if (err) { console.log(err);
    } else { console.log(body); }
})
```

### Python {#파이썬}

Pythonでファイルをアップロードする例です。

```python
from pathlib import Path

import requests

url = "http://127.0.0.1:5654/db/write/STASH"
file_path = Path("./image_file.svg")

with file_path.open("rb") as image_file:
  response = requests.post(
    url,
    headers={"X-Store-Dir": "/tmp/store"},
    data={"NAME": "camera-1", "TIME": "now"},
    files={"DATA": (file_path.name, image_file, "image/svg")},
  )

response.raise_for_status()
print(response.text)
```
