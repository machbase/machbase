---
title: 파일 업로드
type: docs
weight: 25
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

아래 예시는 `EXAMPLE` 테이블이 이미 생성되어 있다고 가정합니다.

```sql {hl_lines=[5]}
CREATE TAG TABLE EXAMPLE(
    NAME     VARCHAR(80)  primary key,
    TIME     DATETIME basetime,
    VALUE    DOUBLE,
    EXTDATA  JSON
)
```

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
이 예시는 Visual Studio Code의 REST Client 확장을 사용합니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: multipart/form-data; boundary=----Boundary7MA4YWxkTrZu0gW

------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="NAME"

camera-1
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="TIME"

now
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="VALUE"

0
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="EXTDATA"; filename="image_file.png"
X-Store-Dir: /tmp/store
Content-Type: image/png

< /data/image_file.png
------Boundary7MA4YWxkTrZu0gW--
```
~~~
{{< /tab >}}
{{< tab >}}
이 예시는 `-F` 옵션을 사용한 `curl`로 *multipart/form-data* 형식의 POST 요청을 전송합니다.

```sh {hl_lines=[5]}
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE' \
    -F 'NAME=camera-1' \
    -F 'TIME=now' \
    -F 'VALUE=0' \
    -F 'EXTDATA=@./data/image_file.png;headers="X-Store-Dir: /tmp/store"'
```
{{< /tab >}}
{{< /tabs >}}

### X-Store-Dir

업로드한 파일은 `X-Store-Dir` 헤더에 지정한 디렉터리에 저장되며,
파일 이름은 응답에 포함된 `ID` 값을 기반으로 생성됩니다.
앞선 예시처럼 각 파트의 헤더에 `X-Store-Dir`을 포함할 수도 있고,
요청의 최상위 헤더로 지정할 수도 있습니다.

**`${data}`**<br/>
`X-Store-Dir` 경로에서 `${data}` 변수를 사용하면 데이터베이스 홈 디렉터리를 의미합니다. 이 디렉터리는 machbase-neo 프로세스를 실행할 때 `--data` 플래그로 지정하거나, 해당 플래그가 없으면 실행 파일이 위치한 디렉터리 아래의 `machbase_home` 서브디렉터리를 기본값으로 사용합니다. 자세한 내용은 [명령줄 플래그](/neo/operations/command-line/) 문서를 참고해 주십시오.

예를 들어 `X-Store-Dir: ${data}/store`로 설정하면 업로드된 파일은 `some/path/to/machbase_home/store/file_name_is_ID_of_the_response`에 저장됩니다.

### 응답 메시지
파일 업로드가 완료되면 서버는 다음과 같이 저장된 파일 정보를 응답합니다.

- ID : 서버에서 부여한 고유 ID
- FN : 원본 파일 이름
- SZ : 파일 크기
- CT : 콘텐츠 유형
- SD : 서버 측에 저장된 디렉터리 경로

```json
{
  "success": true,
  "reason": "success, 1 record(s) inserted",
  "elapse": "3.772042ms",
  "data": {
    "files": {
      "EXTDATA": {
        "ID": "1ef8a87f-96bd-6576-9ff5-972fa7638db8",
        "FN": "image_file.png",
        "SZ": 12692,
        "CT": "image/png",
        "SD": "/tmp/store"
      }
    }
  }
}
```

위 예시의 `EXTDATA` 컬럼은 업로드된 파일의 메타 정보를 포함한 JSON 형식 문자열로 조회할 수 있습니다.

```sql
SELECT EXTDATA FROM EXAMPLE
WHERE NAME = 'camera-1' 
```

또는 JSON Path를 사용할 수 있습니다.

```sql
SELECT EXTDATA FROM EXAMPLE
WHERE NAME = 'camera-1'
AND EXTDATA->'$.FN' = 'image_file.png';
```

다음은 `/db/query` API로 SELECT 쿼리를 실행하는 예시입니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select EXTDATA from EXAMPLE where NAME = 'camera-1'
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - 'http://127.0.0.1:5654/db/query' \
  --data-urlencode "q=select EXTDATA from EXAMPLE\
    where NAME = 'camera-1'"
```
{{< /tab >}}
{{< /tabs >}}

`->` 표기법을 사용해 JSON Path 조건을 적용한 예시입니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select EXTDATA from EXAMPLE where NAME = 'camera-1' and EXTDATA->'$.FN' = 'image_file.png'
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - 'http://127.0.0.1:5654/db/query' \
  --data-urlencode "q=select EXTDATA from EXAMPLE\
    where NAME = 'camera-1' \
    and EXTDATA->'$.FN' = 'image_file.png'"
```
{{< /tab >}}
{{< /tabs >}}

`EXTDATA` 컬럼에는 아래와 같이 파일 정보가 저장됩니다.

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

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?format=ndjson
    &q=SELECT NAME, TIME, EXTDATA->'$.ID' as FID  FROM EXAMPLE WHERE NAME = 'camera-1'
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
  --data-urlencode "format=ndjson"   \
  --data-urlencode "q=SELECT NAME, TIME, EXTDATA->'$.ID' as FID  \
    FROM EXAMPLE WHERE NAME = 'camera-1'"
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

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o ./img-download.png \
    http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8
```
{{< /tab >}}
{{< /tabs >}}

### HTML에서 &lt;img&gt; 사용

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8"/>
</body>
</html>
```

TAG 테이블에서 태그 이름을 알고 있다면 `tag` 쿼리 매개변수를 사용해 조회 성능을 향상시킬 수 있습니다.

```html
<html>
<body>
<img src="http://127.0.0.1:5654/db/query/file/EXAMPLE/EXTDATA/1ef8a87f-96bd-6576-9ff5-972fa7638db8?tag=camera-1"/>
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
    url: 'http://127.0.0.1:5654/db/write/EXAMPLE',
    headers: {"X-Store-Dir": "/tmp/store"},
    formData: {
        NAME: 'camera-1',
        TIME: 'now',
        VALUE: 0,
        EXTDATA:  fs.createReadStream('./image_file.png'), 
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
import requests

# 파일을 업로드할 URL을 정의합니다.
url = 'http://127.0.0.1:5654/db/write/EXAMPLE'

# 이미지 파일 경로를 지정합니다.
file_path = './image_file.png'

# 이미지를 바이너리 모드로 엽니다.
with open(file_path, 'rb') as file:
    headers = {'X-Store-Dir': '/tmp/store'}
    data = {'NAME': 'camera-1', 'TIME': 'now', 'VALUE': 0}
    files = {'EXTDATA': ('filename.png', file, 'image/png')}

    # POST 요청을 전송합니다.
    response = requests.post(url, data=data, files=files, headers=headers)
    
    # 서버에서 받은 응답을 출력합니다.
    print(response.status_code)
    print(response.text)
```
