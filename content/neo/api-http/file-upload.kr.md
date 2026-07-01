---
title: 파일 업로드
type: docs
weight: 25
params:
    tabs:
        sync: true
---

 {{< neo_since ver="8.0.40" />}}

클라이언트는 HTTP *multipart/form-data* 인코딩을 사용해 Machbase-Neo로 임의의 파일을 업로드할 수 있습니다.
첨부된 파일은 지정한 디렉터리에 저장되며,
데이터베이스는 해당 파일의 메타데이터를 JSON 문자열 형태로 컬럼에 보관합니다.

각 파트의 이름은 컬럼명, 값은 문자열 표현이 되도록 *multipart/form-data* 형식으로 컬럼과 값을 전송해 주십시오.
파일을 저장할 디렉터리를 지정하려면 `JSON` 타입 컬럼에 파일을 첨부하면서 `X-Store-Dir` 헤더를 함께 보내야 합니다.
`X-Store-Dir`에 지정한 디렉터리가 없으면 서버가 자동으로 생성합니다.
파일 본문은 UUID 형식으로 생성된 고유 이름을 사용해 해당 디렉터리에 저장됩니다.

## 파일 업로드

아래 예시는 `STASH` 테이블이 이미 생성되어 있다고 가정합니다.

```sql {hl_lines=[4]}
CREATE TAG TABLE STASH(
    NAME     VARCHAR(80)  primary key,
    TIME     DATETIME basetime,
    DATA     JSON
)
```

{{< tabs >}}
{{< tab name="HTTP" >}}
이 예시는 Visual Studio Code의 REST Client 확장을 사용합니다.

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
이 예시는 `-F` 옵션을 사용한 `curl`로 *multipart/form-data* 형식의 POST 요청을 전송합니다.

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
  이 예시는 `requests`를 사용해 *multipart/form-data* 형식으로 파일을 업로드합니다.

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
이 예시는 `fetch`와 `FormData`를 사용해 *multipart/form-data* 형식으로 파일을 업로드합니다.

```javascript
async function uploadFile(file) {
  if (!file) {
    throw new Error("업로드할 파일을 먼저 선택하세요.");
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
form.Add(fileContent, "DATA", "image_file.png");

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

### 응답 메시지
파일 업로드가 완료되면 서버는 다음과 같이 저장된 파일 정보를 응답합니다.

- ID : 서버에서 부여한 고유 ID
- FN : 원본 파일 이름
- SZ : 파일 크기
- CT : 콘텐츠 유형
- SD : 서버 측에 저장된 디렉터리 경로

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

### X-Store-Dir

업로드한 파일은 `X-Store-Dir` 헤더에 지정한 디렉터리에 저장되며,
파일 이름은 응답에 포함된 `ID` 값을 기반으로 생성됩니다.
앞선 예시처럼 각 파트의 헤더에 `X-Store-Dir`을 포함할 수도 있고,
요청의 최상위 헤더로 지정할 수도 있습니다.

**`${data}`**<br/>
`X-Store-Dir` 경로에서 `${data}` 변수를 사용하면 데이터베이스 홈 디렉터리를 의미합니다. 이 디렉터리는 machbase-neo 프로세스를 실행할 때 `--data` 플래그로 지정하거나, 해당 플래그가 없으면 실행 파일이 위치한 디렉터리 아래의 `machbase_home` 서브디렉터리를 기본값으로 사용합니다. 자세한 내용은 [명령줄 플래그](/neo/operations/command-line/) 문서를 참고해 주십시오.

예를 들어 `X-Store-Dir: ${data}/store`로 설정하면 업로드된 파일은 `some/path/to/machbase_home/store/file_name_is_ID_of_the_response`에 저장됩니다.

### 메타데이터

위 예시의 `DATA` 컬럼은 업로드된 파일의 메타 정보를 포함한 JSON 형식 문자열로 조회할 수 있습니다.

```sql
SELECT DATA FROM STASH
WHERE NAME = 'camera-1';
```

또는 JSON Path를 사용할 수 있습니다.

```sql
SELECT DATA FROM STASH
WHERE NAME = 'camera-1'
AND DATA->'$.FN' = 'image_file.svg';
```

**`/db/query` 조회**

다음은 `/db/query` API로 SELECT 쿼리를 실행하는 예시입니다.

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

**JSON Path 조회: `->` 표기**

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

`DATA` 컬럼에는 아래와 같이 파일 정보가 저장되어 있습니다.

```json
{
  "data": {
    "columns": [ "EXTDATA" ],
    "types": [ "string" ],
    "rows": [
      [
        "{\"ID\":\"1ef8a87f-96bd-6576-9ff5-972fa7638db8\",\"FN\":\"image_file.png\",\"SZ\":12692,\"CT\":\"image/png\",\"SD\":\"/tmp/store\"}"
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "843.666µs"
}
```

JSON 타입 컬럼에서 특정 필드를 추출하려면 JSON Path를 사용하십시오.

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

## 파일 내용 조회

파일 본문은 쿼리 API로 접근할 수 있습니다.

`http://{server_address}/db/query/file/{table}/{column}/{ID}`

테이블이 TAG 테이블이라면 `tag` 매개변수를 지정하면 응답 속도를 높일 수 있습니다.

`http://{server_address}/db/query/{tag_table}/{column}/{ID}?tag=camera-1`

LOG 테이블의 경우 레코드가 삽입된 시점을 기준으로 `ID`가 생성되고, TAG 테이블은 레코드의 기준 시간 컬럼에서 `ID`를 만듭니다.

`ID`에는 타임스탬프 정보가 포함되어 있으므로 Machbase-Neo는 TAG 테이블에서는 `TIME between A and B`, LOG 테이블에서는 `_ARRIVAL_TIME between A and B` 절에 이를 활용해 검색 범위를 좁힙니다.
`ID`에 포함된 타임스탬프가 기준 시간이나 LOG 테이블의 `_ARRIVAL_TIME`과 완전히 일치하지는 않지만, 검색 성능 향상에는 유용합니다.

### HTTP GET

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

### HTML에서 &lt;img&gt; 사용

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8"/>
</body>
</html>
```

TAG 테이블에서 태그 이름을 알고 있다면 `tag` 쿼리 매개변수를 사용해 조회 성능을 향상시킬 수 있습니다.

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/STASH/DATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8?tag=camera-1"/>
</body>
</html>
```

## 예시

### 자바스크립트

자바스크립트로 파일을 업로드하는 예시입니다.

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

### 파이썬

파이썬으로 파일을 업로드하는 예시입니다.

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
