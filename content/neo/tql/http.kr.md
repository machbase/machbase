---
title: HTTP()
type: docs
weight: 49
---

`HTTP()` SRC는 TQL 스크립트 안에서 HTTP 요청을 전송하고 응답을 바로 확인하실 수 있도록 지원합니다.  
외부 API를 연동하거나 데이터 파이프라인 일부에서 HTTP 엔드포인트를 시험할 때 유용합니다.

*구문*: `HTTP(text)` {{< neo_since ver="8.0.53" />}}

- `text`: HTTP 요청을 기술한 문자열입니다.

## TQL 사용 예시

구문은 [RFC 2616](https://www.rfc-editor.org/rfc/rfc2616)을 따르며, 요청 메서드·헤더·본문을 모두 지정할 수 있습니다.

**예시**

`HTTP()` 소스를 사용합니다.

{{< tabs items="TEXT,HTML-simple,HTML-detail">}}
{{< tab >}}
```
HTTP({
    GET http://127.0.0.1:5654/db/query
        ?q=select * from example limit 3
        &format=csv
        &timeformat=default
        &tz=UTC
})
TEXT()
```
{{< /tab >}}
{{< tab >}}
```html
HTTP({
    POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

    {
        "q": "select * from example limit 3",
        "format": "csv",
        "timeformat": "default"
    }
})
HTML(`<pre>{{ .Value 0 }}</pre>`)
```
{{< /tab >}}
{{< tab >}}
```html
HTTP({
    POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

    {
        "q": "select * from example limit 3",
        "format": "csv",
        "timeformat": "default"
    }
})
HTML({
    {{- with .Value 0 -}}
    <pre>
        {{- .StatusLine }}{{"\n"}}
        {{- .Header }}{{"\n\n"}}
        {{- .Body -}}
    </pre>
    {{- end}}
})
```
{{< /tab >}}
{{< /tabs >}}

요청을 작성한 뒤 TQL을 실행해 주십시오.  
결과 창에는 헤더와 본문을 포함한 HTTP 응답이 출력됩니다.

**응답 예시**

```
HTTP/1.1 200 OK
Content-Length: 212
Content-Type: text/csv; charset=utf-8
Date: Mon, 02 Jun 2025 03:42:33 GMT

NAME,TIME,VALUE
work-11-0,2025-03-19 01:56:19.824,0.00
work-11-0,2025-03-19 01:56:19.824,1.00
work-11-0,2025-03-19 01:56:19.824,2.00
```

### 워크시트

마크다운 셀 안에서 `http` 코드 펜스를 사용해 요청을 작성할 수 있습니다.

**예시**

~~~text
### HTTP Client Example

```http
POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

{
    "q": "select * from example limit 3",
    "format": "box",
    "timeformat": "default"
}
```
~~~

{{< figure src="../img/http_wrk_example.jpg" width="700" >}}


### 마크다운

`http` 코드 펜스는 `.md` 파일에서도 동일하게 동작합니다.

~~~
## HTTP Example

Code fence with `http`.

```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from example limit 2
    &format=ndjson
    &timeformat=default&tz=local
```
~~~

{{< figure src="../img/http_md_example.jpg" width="637" >}}


## 쿼리 문자열

요청 행에 쿼리 문자열을 바로 포함할 수 있습니다.

~~~
```http
GET https://example.com/comments?page=2&pageSize=10
```
~~~

쿼리 파라미터가 많다면 가독성을 위해 여러 줄로 나눌 수 있습니다.  
요청 행 다음에 `?` 또는 `&`로 시작하는 줄은 쿼리 파라미터로 해석됩니다.

~~~
```http
GET https://example.com/comments
    ?page=2
    &pageSize=10
```
~~~

## 요청 헤더

요청 행(및 쿼리 문자열) 다음의 내용부터 첫 번째 빈 줄까지는 요청 헤더로 인식됩니다.  
헤더는 한 줄에 하나씩 `field-name: field-value` 형식으로 작성해 주십시오.

**예시**

```
User-Agent: http-client
Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4
Content-Type: application/json
```


## 요청 본문

요청 본문을 포함하려면 헤더 뒤에 빈 줄을 추가한 뒤 본문을 작성합니다. 빈 줄 아래의 모든 내용이 본문으로 처리됩니다.

**예시**

~~~
```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

<request>
    <name>sample</name>
    <time>Wed, 21 Oct 2015 18:27:50 GMT</time>
</request>
```
~~~

**외부 파일 사용**

본문을 파일로 지정하려면 줄의 맨 앞에 `<`를 두고 파일 탐색기에서 보이는 경로를 입력합니다.  
운영체제의 절대 경로를 사용할 때는 경로 앞에 `@`를 붙여 주십시오.

예를 들어:
- `< /doc.xml` : TQL 루트 디렉터리에 있는 파일을 가리킵니다.
- `< @/home/data/doc.xml` : 운영체제의 절대 경로 `/home/data/doc.xml`을 가리킵니다.

~~~
```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

< /data/demo.xml
```
~~~

## 멀티파트 폼 데이터

요청 본문이 `multipart/form-data`라면 텍스트와 파일 업로드를 함께 보낼 수 있습니다.

~~~
```http
POST https://api.example.com/user/upload
Content-Type: multipart/form-data; boundary=----Boundary7MA4YWxkTrZu0gW

------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="text"

title
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="1.png"
Content-Type: image/png

< /data/1.png
------Boundary7MA4YWxkTrZu0gW--
```
~~~

## x-www-form-urlencoded

`application/x-www-form-urlencoded` 본문은 여러 줄로 나누어 작성할 수 있습니다.  
첫 번째 줄 이후에는 각 키-값 쌍을 `&`로 시작해 주십시오.

~~~
```http
POST https://api.example.com/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=foo
&password=bar
```
~~~

---

이처럼 유연한 HTTP 요청 구문을 활용하면 TQL 스크립트 안에서 다양한 HTTP 기능과 포맷을 손쉽게 테스트하고 자동화하실 수 있습니다.
