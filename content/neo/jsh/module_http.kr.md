---
title: "@jsh/http"
type: docs
weight: 12
---

{{< neo_since ver="8.0.52" />}}

## request()

간단한 HTTP 클라이언트 요청 헬퍼 함수입니다.

<h6>사용 형식</h6>

```js
request(url, option)
```

<h6>매개변수</h6>

- `url` `String` 요청 대상 주소입니다. 예: `http://192.168.0.120/api/members`
- `option` `Object` 선택적 [ClientRequestOption](#clientrequestoption)입니다.

<h6>반환값</h6>

- `Object` [ClientRequest](#clientrequest)

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    req = http.request("http://127.0.0.1:29876/hello")
    req.do((rsp) => {
        println("url:", rsp.url);
        println("error:", rsp.error());
        println("status:", rsp.status);
        println("statusText:", rsp.statusText);
        println("body:", rsp.text());
    })
} catch (e) {
    println(e.toString());
}
```

## Client

HTTP 클라이언트 객체입니다.

<h6>생성</h6>

| Constructor             | 설명                          |
|:------------------------|:-------------------------------------|
| new Client()            | HTTP 클라이언트를 생성합니다.        |


### do()

지정한 URL로 HTTP 요청을 전송하고 응답을 처리합니다. 메서드, 헤더, 본문 등 옵션과 콜백 함수를 함께 전달할 수 있습니다.

<h6>사용 형식</h6>

```js
client.do(url)
client.do(url, option)
client.do(url, option, callback)
```

<h6>매개변수</h6>

- `url` `String`
- `option` `Object` [ClientRequestOption](#clientrequestoption)
- `callback` `(response) => {}` [ClientResponse](#clientresponse)를 인자로 받는 콜백입니다.

<h6>반환값</h6>

- `Object`

| Property           | Type       | 설명        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | HTTP 상태 코드   |
| statusText         | String     | HTTP 상태 메시지 |
| url                | String     | 요청 URL         |
| error              | String     | 오류 메시지       |

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const client = new http.Client()
client.do(
    "http://127.0.0.1:29876/hello",
    { method:"GET" }, 
    (rsp)=>{
        println("url:", rsp.url);
        println("error:", rsp.error());
        println("status:", rsp.status);
        println("statusText:", rsp.statusText);
        println("content-type:", rsp.headers["Content-Type"]);
        println("body:", rsp.text());
    })
```

## ClientRequestOption

| 옵션                | 타입         | 기본값        | 설명                       |
|:--------------------|:-------------|:--------------|:---------------------------|
| method              | String       | `GET`         | GET, POST, DELETE, PUT 등 HTTP 메서드 |
| headers             | Object       |               | 요청 헤더                  |
| body                | String       |               | 전송할 본문                |
| unix                | String       |               | 유닉스 도메인 소켓 파일 경로 |

`unix` 옵션을 지정하면 해당 소켓 파일로 서버에 연결을 시도합니다.

## ClientRequest

### do()

ClientRequest 객체에서 콜백을 실행해 응답을 처리합니다.

<h6>사용 형식</h6>

```js
do(callback)
```

<h6>매개변수</h6>

- `callback` `(response) => {}` 응답을 처리할 콜백입니다.

<h6>반환값</h6>

없음.

## ClientResponse

<h4>프로퍼티</h4>

| Property           | Type       | 설명        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | 상태 코드 (예: 200, 404) |
| statusText         | String     | 상태 메시지 (예: `200 OK`) |
| headers            | Object     | 응답 헤더           |
| method             | String     | 요청 메서드         |
| url                | String     | 요청 URL            |
| error              | String     | 오류 메시지         |

### text()

응답 본문을 문자열로 반환합니다.

### json()

응답 본문을 JSON 객체로 반환합니다.

### csv()

응답 본문을 CSV 행 배열로 반환합니다.

<!-- ### blob() 
    todo implement bytes stream first.
-->

## Server

HTTP 서버 객체입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http")
const svr = new http.Server({
    network:'tcp',
    address:'127.0.0.1:8080',
})
svr.get("/hello/:name", (ctx) => {
    let name = ctx.param("name");
    let hello = ctx.query("greeting");
    hello = hello == "" ?  "hello" : hello;
    ctx.JSON(http.status.OK, {
        greeting: hello,
        name:  name,
    })
})
svr.static("/html", "/html")
svr.serve();
```

<h6>생성</h6>

| Constructor             | 설명                          |
|:------------------------|:-------------------------------------|
| new Server(options)      | HTTP 서버를 생성합니다.          |

<h6>옵션</h6>

| 옵션         | 타입      | 기본값    | 설명                       |
|:-------------|:----------|:-----------|:--------------------------|
| network      | String    | `tcp`      | `tcp`, `unix`              |
| address      | String    |            | `host:port`, `/path/to/file` |

- TCP/IP 예시: `{network:"tcp", address:"192.168.0.100:8080"}`
- Unix 도메인 소켓 예시: `{network:"unix", address:"/tmp/http.sock"}`

### all()

모든 HTTP 메서드를 한 번에 처리할 라우트를 등록합니다.

<h6>사용 형식</h6>

```js
all(request_path, handler)
```

<h6>매개변수</h6>

- `request_path` `String` 매칭할 URL 경로입니다.
- `handler` `(context) => {}` [context](#servercontext)를 사용해 요청 정보를 처리하는 콜백입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.all("/api/resource", (ctx) => {
    ctx.JSON(http.status.OK, { message: "Handled all methods" });
});
svr.serve();
```

### get()

GET 요청을 처리할 라우트를 등록합니다.

<h6>사용 형식</h6>

```js
get(request_path, handler)
```

<h6>매개변수</h6>

- `request_path` `String` 매칭할 URL 경로입니다.
- `handler` `(context) => {}` 요청을 처리할 콜백입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.get("/hello/:name", (ctx) => {
    const name = ctx.param("name");
    ctx.JSON(http.status.OK, { message: `Hello, ${name}!` });
});
svr.serve();
```


### post()

POST 요청을 처리할 라우트를 등록합니다.

<h6>사용 형식</h6>

```js
post(request_path, handler)
```

<h6>매개변수</h6>

- `request_path` `String` 매칭할 URL 경로입니다.
- `handler` `(context) => {}` 요청 본문 등을 처리할 콜백입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.post("/submit", (ctx) => {
    const data = ctx.body; // 요청 본문에 접근합니다.
    ctx.JSON(http.status.Created, { message: "Data received", data: data });
});
svr.serve();
```

### put()

PUT 요청을 처리할 라우트를 등록합니다.

<h6>사용 형식</h6>

```js
put(request_path, handler)
```

<h6>매개변수</h6>

- `request_path` `String`
- `handler` `(context) => {}` 요청 정보를 처리할 콜백입니다.

<h6>반환값</h6>

없음.

### delete()

DELETE 요청을 처리할 라우트를 등록합니다.

<h6>사용 형식</h6>

```js
delete(request_path, handler)
```

<h6>매개변수</h6>

- `request_path` `String`
- `handler` `(context) => {}` 요청 정보를 처리할 콜백입니다.

<h6>반환값</h6>

없음.

### static()

정적 디렉터리를 라우트에 매핑합니다. HTML, CSS, JavaScript, 이미지 등 정적 자산 제공에 적합합니다.

<h6>사용 형식</h6>

```js
static(request_path, dir_path)
```

<h6>매개변수</h6>

- `request_path` `String` 요청 경로 접두사입니다.
- `dir_path` `String` 제공할 디렉터리 경로입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.static("/public", "/path/to/static/files");
svr.serve();
```

### staticFile()

지정한 파일을 특정 경로로 제공하도록 라우트를 등록합니다.

<h6>사용 형식</h6>

```js
staticFile(request_path, file_path)
```

<h6>매개변수</h6>

- `request_path` `String` 매칭할 URL 경로입니다.
- `file_path` `String` 제공할 파일 경로입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.staticFile("/favicon.ico", "/path/to/favicon.ico");
svr.serve();
```

### loadHTMLGlob()

HTML 템플릿 파일을 일괄 로드합니다.

<h6>사용 형식</h6>

```js
loadHTMLGlob(pattern)
```

<h6>매개변수</h6>

- `pattern` `String` 글롭 패턴입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.loadHTMLGlob("/templates/*.html")
svr.get("/docs/hello.html", ctx => {
    ctx.HTML(http.status.OK, "hello.html", {str:"Hello World", num: 123, bool: true})
})
svr.serve();
```

### serve()

서버를 시작하고 `stop()`이 호출될 때까지 대기합니다.

<h6>사용 형식</h6>

```js
serve()
serve(callback)
```

<h6>매개변수</h6>

- `callback` `(result)=>{}` [ServerResult](#serverresult)를 인자로 받는 선택적 콜백입니다.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.serve((result) => {
    console.log(`Server is listening on ${result.network}://${result.message}`);
});
```

### close()

서버를 중지하고 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<!-- #### router()

## Router

### Methods

#### all()

#### get()

#### post()

#### put()

#### delete()

#### static()

#### staticFile() -->

## ServerResult

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명               |
|:-------------------|:-----------|:-------------------|
| network            | String     | 예: `tcp`          |
| message            | String     | 예: `127.0.0.1:8080` |

## ServerContext

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명               |
|:-------------------|:-----------|:-------------------|
| request            | Object     | [ServerRequest](#serverrequest) |


### abort()

요청 처리를 즉시 중단합니다.

<h6>사용 형식</h6>

```js
abort()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

### redirect()

지정한 상태 코드로 다른 URL에 리다이렉트합니다.

<h6>사용 형식</h6>

```js
redirect(statusCode, url)
```

- `statusCode` `Number` HTTP 상태 코드 (예: `302`, `http.status.Found`)
- `url` `String` 이동할 주소

<h6>반환값</h6>

없음.

### setHeader()

응답 헤더를 설정합니다.

<h6>사용 형식</h6>

```js
setHeader(name, value)
```

<h6>매개변수</h6>

- `name` `String`
- `value` `String`

<h6>반환값</h6>

없음.

### param()

라우트 경로 파라미터 값을 반환합니다.

<h6>사용 형식</h6>

```js
param(name)
```

- `name` `String` 파라미터 이름

<h6>반환값</h6>

- `String` 파라미터 값

### query()

쿼리 문자열 값을 반환합니다.

<h6>사용 형식</h6>

```js
query(name)
```

- `name` `String` 쿼리 키

<h6>반환값</h6>

- `String` 쿼리 값

### TEXT()

텍스트 응답을 전송합니다.

<h6>사용 형식</h6>

```js
TEXT(statusCode, content)
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/text", ctx => {
    ctx.TEXT(http.status.OK, "Hello World");
})

// Content-Type: "text/plain; charset=utf-8"
//
// Hello World
```

```js {linenos=table,linenostart=1}
svr.get("/formats/text", ctx => {
    name = "PI";
    pi = 3.1415;
    ctx.TEXT(http.status.OK, "Hello %s, %3.2f", name, pi);
})

// Content-Type: "text/plain; charset=utf-8"
//
// Hello PI, 3.14
```

### JSON()

JSON 응답을 전송합니다.

<h6>사용 형식</h6>

```js
JSON(statusCode, content)
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/json", ctx => {
    obj = {str:"Hello World", num: 123, bool: true};
    ctx.JSON(http.status.OK, obj);
})

// Content-Type: application/json; charset=utf-8
//
// {"bool":true,"num":123,"str":"Hello World"}
```

```js {linenos=table,linenostart=1}
svr.get("/formats/json-indent", ctx => {
    obj = {str:"Hello World", num: 123, bool: true};
    ctx.JSON(http.status.OK, obj, {indent: true})
})

// Content-Type: application/json; charset=utf-8
//
// {
//     "bool": true,
//     "num": 123,
//     "str": "Hello World"
// }
```

### YAML()

YAML 응답을 전송합니다.

<h6>사용 형식</h6>

```js
YAML(statusCode, content)
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/yaml", ctx => {
    ctx.YAML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/yaml; charset=utf-8
//
// bool: true
// num: 123
// str: Hello World
```

### TOML

TOML 응답을 전송합니다.

<h6>사용 형식</h6>

```js
TOML(statusCode, content)
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/toml", ctx => {
    ctx.TOML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/toml; charset=utf-8
//
// bool = true
// num = 123
// str = 'Hello World'
```

### XML()

XML 응답을 전송합니다.

<h6>사용 형식</h6>

```js
XML(statusCode, content)
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/xml", ctx => {
    ctx.XML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/xml; charset=utf-8
//
// <map><str>Hello World</str><num>123</num><bool>true</bool></map>
```

### HTML()

HTML 템플릿을 렌더링해 응답합니다.

<h6>사용 형식</h6>

```js
HTML(statusCode, template, obj)
```

- `statusCode` `Number` HTTP 응답 코드
- `template` `String` 템플릿 이름
- `obj` `any` 템플릿에 바인딩할 값

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
svr.loadHTMLGlob("/templates/*.html")

svr.get("/hello.html", ctx => {
    obj = {str:"World", num: 123, bool: true};
    ctx.HTML(http.status.OK, "hello.html", obj);
})

// Content-Type: text/html; charset=utf-8
//
// <html>
//     <body>
//         <h1>Hello, World!</h1>
//         <p>num: 123</p>
//         <p>bool: true</p>
//     </body>
// </html>
```

- /templates/hello.html

```html
<html>
    <body>
        <h1>Hello, {{.str}}!</h1>
        <p>num: {{.num}}</p>
        <p>bool: {{.bool}}</p>
    </body>
</html>
```

## ServerRequest

<h6>프로퍼티</h6>

| Property           | Type       | 설명           |
|:-------------------|:-----------|:----------------------|
| method             | String     | 요청 메서드           |
| host               | String     | 요청 호스트           |
| path               | String     | 요청 경로             |
| query              | String     | 쿼리 문자열           |
| header             | Object     | 요청 헤더             |
| body               | Object     | 요청 본문             |
| remoteAddress      | String     | 원격 주소             |

### getHeader()

<h6>사용 형식</h6>

```js
getHeader(name)
```

<h6>매개변수</h6>

- `name` `String` head name. e.g. `Content-Type`, `Content-Length`

<h6>반환값</h6>

- `String` 헤더 값.

## status

HTTP 상태 코드를 제공합니다.

```js
const http = require("@jsh/http");

http.status.OK =                              200;
http.status.Created =                         201;
http.status.Accepted =                        202;
http.status.NonAuthoritativeInfo =            203;
http.status.NoContent =                       204;
http.status.ResetContent =                    205;
http.status.PartialContent =                  206;
http.status.MultipleChoices =                 300;
http.status.MovedPermanently =                301;
http.status.Found =                           302;
http.status.SeeOther =                        303;
http.status.NotModified =                     304;
http.status.UseProxy =                        305;
http.status.TemporaryRedirect =               307;
http.status.PermanentRedirect =               308;
http.status.BadRequest =                      400;
http.status.Unauthorized =                    401;
http.status.PaymentRequired =                 402;
http.status.Forbidden =                       403;
http.status.NotFound =                        404;
http.status.MethodNotAllowed =                405;
http.status.NotAcceptable =                   406;
http.status.ProxyAuthRequired =               407;
http.status.RequestTimeout =                  408;
http.status.Conflict =                        409;
http.status.Gone =                            410;
http.status.LengthRequired =                  411;
http.status.PreconditionFailed =              412;
http.status.RequestEntityTooLarge =           413;
http.status.RequestURITooLong =               414;
http.status.UnsupportedMediaType =            415;
http.status.RequestedRangeNotSatisfiable =    416;
http.status.ExpectationFailed =               417;
http.status.Teapot =                          418;
http.status.UnprocessableEntity =             422;
http.status.Locked =                          423;
http.status.FailedDependency =                424;
http.status.TooEarly =                        425;
http.status.UpgradeRequired =                 426;
http.status.PreconditionRequired =            428;
http.status.TooManyRequests =                 429;
http.status.RequestHeaderFieldsTooLarge =     431;
http.status.UnavailableForLegalReasons =      451;
http.status.InternalServerError =             500;
http.status.NotImplemented =                  501;
http.status.BadGateway =                      502;
http.status.ServiceUnavailable =              503;
http.status.GatewayTimeout =                  504;
http.status.HTTPVersionNotSupported =         505;
http.status.VariantAlsoNegotiates =           506;
http.status.InsufficientStorage =             507;
http.status.LoopDetected =                    508;
http.status.NotExtended =                     510;
http.status.NetworkAuthenticationRequired =   511;
```
