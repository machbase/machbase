---
title: "http"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`http` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 HTTP 클라이언트/서버 API를 제공합니다.

## request()

`ClientRequest` 객체를 생성합니다.

지원 시그니처:

- `request(url[, options][, callback])`
- `request(options[, callback])`

- 반환값: `ClientRequest`
- `callback`을 지정하면 응답 수신 시 `IncomingMessage`를 인자로 전달받습니다.

<h6>사용 형식</h6>

```js
request(url[, options][, callback])
request(options[, callback])
```

<h6>주요 요청 옵션</h6>

- `url` (`string` 또는 `URL`)
- `protocol`, `host`, `hostname`, `port`, `path`
- `method`
- `headers`
- `auth` (`Authorization: Basic ...`으로 변환)
- `agent`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,4]}
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.on('response', (res) => {
  console.println(res.statusCode, res.statusMessage);
});
req.end();
```

## get()

GET 요청 축약 함수입니다. 내부적으로 `request()`를 만들고 자동으로 `end()`를 호출합니다.

지원 시그니처:

- `get(url[, options][, callback])`
- `get(options[, callback])`

- 반환값: `ClientRequest`
- `callback`을 지정하지 않은 경우 `response` 이벤트 리스너로 응답을 처리할 수 있습니다.

<h6>사용 형식</h6>

```js
get(url[, options][, callback])
get(options[, callback])
```

**status**

HTTP 상태 코드 맵입니다.

예시:

- `http.status.OK`
- `http.status.NotFound`
- `http.status.InternalServerError`

**동작 참고**

- `response.ok`는 상태 코드가 `200`~`299`일 때 `true`입니다.
- `response.headers`의 키는 소문자로 정규화됩니다.
- `setHeader()`/`getHeader()`/`hasHeader()`/`removeHeader()`는 헤더 이름을 대소문자 구분 없이 처리합니다.
- `write()`를 여러 번 호출하면 요청 본문이 누적된 뒤 전송됩니다.

## ClientRequest

`request()`/`get()`가 반환하는 요청 객체입니다.

**ClientRequest 헤더 메서드**

- `setHeader(name, value)`
- `getHeader(name)`
- `hasHeader(name)`
- `removeHeader(name)`
- `getHeaders()`
- `getHeaderNames()`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,5]}
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Test-Header', 'TestValue');
console.println(req.hasHeader('X-Test-Header'));
console.println(req.getHeader('X-Test-Header'));
req.end();
```

**ClientRequest.write()**

요청 본문 청크를 기록합니다.

- `chunk`는 `string`, `Uint8Array`를 지원합니다.
- 성공 시 `true`, 실패 시 `false`를 반환합니다.

<h6>사용 형식</h6>

```js
write(chunk[, encoding][, callback])
```

**ClientRequest.end()**

요청을 종료하고 전송합니다.

- `callback`을 전달하면 응답 객체(`IncomingMessage`)를 인자로 전달받습니다.

<h6>사용 형식</h6>

```js
end([data[, encoding]][, callback])
```

**ClientRequest.destroy()**

요청 객체를 파기하고 필요 시 에러 이벤트를 발생시킵니다.

<h6>사용 형식</h6>

```js
destroy([err])
```

**ClientRequest 이벤트**

- `response` (`IncomingMessage`)
- `error` (`Error`)
- `end` ()

## IncomingMessage

HTTP 응답 객체입니다.

<h6>주요 프로퍼티</h6>

- `statusCode`
- `statusMessage`
- `ok` (2xx이면 true)
- `headers`
- `rawHeaders`
- `httpVersion`
- `complete`
- `raw` (내부 Go 응답 객체)

**IncomingMessage 본문 메서드**

- `text([encoding])`
- `json()`
- `readBody([encoding])`
- `readBodyBuffer()`

- `text()`/`readBody()`의 기본 인코딩은 `utf-8`입니다.
- `json()`은 파싱 실패 시 예외를 발생시킬 수 있습니다.

**IncomingMessage 유틸리티 메서드**

- `setTimeout(msecs[, callback])`
- `close()`

응답 본문은 일반적인 처리 흐름에서 자동으로 닫히며, 필요 시 `close()`를 명시적으로 호출할 수 있습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,5]}
const http = require('http');
http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println(res.ok, res.statusCode);
  console.println(res.text());
});
```

## Server

HTTP 서버 객체입니다.

<h6>생성</h6>

```js
new Server([options])
```

<h6>옵션</h6>

- `network`: `tcp` 또는 `unix` (기본값: `tcp`)
- `address`: `host:port` 또는 unix socket 경로
- `env`: env object (optional), 파일 시스템에 접근하기위해 요구됨.

**Server 라우트/정적 메서드**

- `get(path, handler)`
- `static(path, root)`
- `staticFile(path, file)`

**Server 템플릿 메서드**

- `loadHTMLFiles(...files)`
- `loadHTMLGlob(pattern)`

**Server 라이프사이클 메서드**

- `serve([callback])`
- `close([callback])`

`serve(callback)`는 `{ network, address }`를 전달합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4,5]}
const http = require('http');
const server = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
server.get('/hello/:name', (ctx) => {
  const name = ctx.param('name');
  ctx.json(http.status.OK, { greeting: 'hello', name });
});
server.serve();
```

**Server context**

핸들러는 요청/응답 헬퍼를 포함한 `ctx`를 인자로 받습니다.

<h6>요청 헬퍼</h6>

- `ctx.request.path`
- `ctx.request.query`
- `ctx.request.body`
- `ctx.request.getHeader(name)`
- `ctx.param(name)`
- `ctx.query(name)`

<h6>응답 헬퍼</h6>

- `ctx.setHeader(name, value)`
- `ctx.redirect(status, url)`
- `ctx.abort()`
- `ctx.text(status, format[, ...args])`
- `ctx.json(status, data[, { indent: boolean }])`
- `ctx.html(status, template, data)`
- `ctx.yaml(status, data)`
- `ctx.toml(status, data)`
- `ctx.xml(status, data)`

## 클라이언트 예제

### GET 요청 (callback)

```js {linenos=table,linenostart=1,hl_lines=[3]}
const http = require('http');

http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  console.println('Body:', res.text());
});
```

### GET 요청 (event listener)

```js {linenos=table,linenostart=1,hl_lines=[4]}
const http = require('http');

const req = http.get('http://127.0.0.1:8080/hello');
req.on('response', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  console.println('Body:', res.text());
});
```

### 요청 헤더 설정/조회

```js {linenos=table,linenostart=1,hl_lines=[4,5,6]}
const http = require('http');

const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Trace-Id', 'trace-001');
console.println(req.hasHeader('x-trace-id'));
console.println(req.getHeader('X-Trace-Id'));
req.end();
```

### 응답 헤더/본문 읽기

```js {linenos=table,linenostart=1,hl_lines=[7,8,9]}
const http = require('http');

http.get('http://127.0.0.1:8080/hello', (res) => {
  const contentType = res.headers['content-type'];
  const contentLength = res.headers['content-length'];

  console.println('Content-Type:', contentType);
  console.println('Content-Length:', contentLength);
  console.println('Body:', res.text());
});
```

### POST JSON 요청

```js {linenos=table,linenostart=1,hl_lines=[4,14]}
const http = require('http');

const req = http.request('http://127.0.0.1:8080/echo', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
});

req.on('response', (res) => {
  if (!res.ok) {
    throw new Error('request failed: ' + res.statusCode);
  }
  console.println(res.json());
});

req.on('error', (err) => {
  console.println('Request error:', err.message);
});

req.write('{"message":"hello"}');
req.end();
```

### 404 응답 처리

```js {linenos=table,linenostart=1,hl_lines=[5]}
const http = require('http');

http.get('http://127.0.0.1:8080/notfound', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  if (!res.ok) {
    console.println('Request failed');
  }
});
```

### URL 객체 기반 요청

서버가 실행 중일 때 GET 요청을 보내고 JSON 본문을 파싱합니다.

```js {linenos=table,linenostart=1}
const http = require('http');

try {
  const url = new URL('http://127.0.0.1:56802/hello/Steve');
  const req = http.request(url);
  req.end((response) => {
    const { statusCode, statusMessage } = response;
    console.println('Status Code:', statusCode);
    console.println('Status Message:', statusMessage);
    console.println('Body:', response.json());
  });
} catch (e) {
  console.println(e.message);
}
```

## 서버 예제

### 간단한 HTTP 서버

`127.0.0.1:56802`에서 서버를 실행하고 `/hello/:name` 경로로 JSON을 반환합니다.

```js {linenos=table,linenostart=1}
const http = require('http');

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:56802' });

svr.get('/hello/:name', (ctx) => {
  const name = ctx.param('name');
  ctx.json(http.status.OK, {
    message: 'greetings',
    name: name,
  });
});

svr.serve((result) => {
  console.println('server started', result.network, result.address);
});
```

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

```json
{"message":"greetings","name":"Karl"}
```

### 정적 콘텐츠/리다이렉트

```js {linenos=table,linenostart=1}
svr.staticFile('/readme', '/path/to/file.txt');
svr.static('/static', '/path/to/static_dir');

svr.get('/readme', (ctx) => {
  ctx.redirect(http.status.Found, '/docs/readme.html');
});
```

### RESTful API

```js {linenos=table,linenostart=1}
let list = [
  { title: 'Indiana Jones', id: 59793, studio: ['Paramount'] },
  { title: 'Star Wars', id: 64821, studio: ['Lucasfilm'] },
];

svr.get('/movies', (ctx) => {
  ctx.json(http.status.OK, list);
});

svr.post('/movies', (ctx) => {
  const obj = ctx.request.body;
  list.push(obj);
  ctx.json(http.status.Created, obj);
});

svr.delete('/movies/:id', (ctx) => {
  const id = parseInt(ctx.param('id'));
  list = list.filter((item) => item.id !== id);
  ctx.json(http.status.NoContent);
});
```

다음 명령으로 각 호출을 확인하실 수 있습니다.

- GET 요청
```sh
curl -o - http://127.0.0.1:56802/movies
```
```json
[
  { "id": 59793, "studio": [ "Paramount" ], "title": "Indiana Jones" },
  { "id": 64821, "studio": [ "Lucasfilm" ], "title": "Star Wars" }
]
```

- POST 요청

```sh
curl -o - -X POST http://127.0.0.1:56802/movies \
    -H "Content-Type: application/json" \
    -d '{"title":"new movie", "id":12345, "studio":["HomeVideo"]}'
```

- DELETE 요청

```sh
curl -v -o - -X DELETE http://127.0.0.1:56802/movies/12345
```

```sh
< HTTP/1.1 204 No Content
< Content-Type: text/plain; charset=utf-8
< Date: Thu, 08 May 2025 20:39:34 GMT
<
```

### HTML 템플릿

다음 설정은 `/*.html` 패턴과 일치하는 모든 HTML 템플릿을 로드합니다.
템플릿을 사용하면 미리 정의된 레이아웃과 실행 시간 데이터를 조합해 동적으로 HTML 응답을 생성하실 수 있습니다.

```js {linenos=table,linenostart=1}
svr.loadHTMLGlob('/*.html');

svr.get('/movielist', (ctx) => {
  const obj = {
    subject: 'Movie List',
    list: [
      { title: 'Indiana Jones', id: 59793, studio: ['Paramount'] },
      { title: 'Star Wars', id: 64821, studio: ['Lucasfilm'] },
    ],
  };
  ctx.html(http.status.OK, 'movie_list.html', obj);
});
```


- HTML 템플릿 코드 `movie_list.html`

```html
<html>
    <body>
        <h1>{{.subject}}</h1>
        <ol>
        {{range .list }}
            <li> {{.id}} {{.title}} {{.studio}}
        {{end}}
        </ol>
    </body>
</html>
```

`/movielist` 엔드포인트에 GET 요청을 보내면,
서버는 `movie_list.html` 템플릿과 `obj` 데이터를 이용해 HTML 페이지를 생성합니다.

```sh
curl -o - http://127.0.0.1:56802/movielist
```

```html
<html>
    <body>
        <h1>Movie List</h1>
        <ol>
            <li> 59793 Indiana Jones [Paramount]
            <li> 64821 Star Wars [Lucasfilm]
        </ol>
    </body>
</html>
```