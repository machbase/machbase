---
title: "http"
type: docs
weight: 12
---

{{< neo_since ver="8.0.73" />}}

`http` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 HTTP 클라이언트/서버 API를 제공합니다.

## request()

`ClientRequest` 객체를 생성합니다.

지원 시그니처:

- `request(url[, options][, callback])`
- `request(options[, callback])`

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

<h6>사용 형식</h6>

```js
get(url[, options][, callback])
get(options[, callback])
```

## Agent

HTTP agent 래퍼 객체입니다.

<h6>생성</h6>

```js
new Agent([options])
```

<h6>메서드</h6>

- `destroy()`

## ClientRequest

`request()`/`get()`가 반환하는 요청 객체입니다.

## ClientRequest 헤더 메서드

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

## ClientRequest.write()

요청 본문 청크를 기록합니다.

- `chunk`는 `string`, `Uint8Array`를 지원합니다.
- 성공 시 `true`, 실패 시 `false`를 반환합니다.

<h6>사용 형식</h6>

```js
write(chunk[, encoding][, callback])
```

## ClientRequest.end()

요청을 종료하고 전송합니다.

<h6>사용 형식</h6>

```js
end([data[, encoding]][, callback])
```

## ClientRequest.destroy()

요청 객체를 파기하고 필요 시 에러 이벤트를 발생시킵니다.

<h6>사용 형식</h6>

```js
destroy([err])
```

## ClientRequest 이벤트

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

## IncomingMessage 본문 메서드

- `text([encoding])`
- `json()`
- `readBody([encoding])`
- `readBodyBuffer()`

## IncomingMessage 유틸리티 메서드

- `setTimeout(msecs[, callback])`
- `close()`

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

## Server 라우트/정적 메서드

- `get(path, handler)`
- `static(path, root)`
- `staticFile(path, file)`

## Server 템플릿 메서드

- `loadHTMLFiles(...files)`
- `loadHTMLGlob(pattern)`

## Server 라이프사이클 메서드

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

## Server context (`ctx`)

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

## status

HTTP 상태 코드 맵입니다.

예시:

- `http.status.OK`
- `http.status.NotFound`
- `http.status.InternalServerError`
