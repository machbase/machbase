---
title: "http"
type: docs
weight: 12
---

{{< neo_since ver="8.0.73" />}}

The `http` module provides Node.js-compatible HTTP client and server APIs for JSH applications.

## request()

Creates a `ClientRequest` object.

Supported signatures:

- `request(url[, options][, callback])`
- `request(options[, callback])`

<h6>Syntax</h6>

```js
request(url[, options][, callback])
request(options[, callback])
```

<h6>Main request options</h6>

- `url` (`string` or `URL`)
- `protocol`, `host`, `hostname`, `port`, `path`
- `method`
- `headers`
- `auth` (converted to `Authorization: Basic ...`)
- `agent`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,4]}
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.on('response', (res) => {
  console.println(res.statusCode, res.statusMessage);
});
req.end();
```

## get()

Shortcut for GET requests. Internally creates a request and calls `end()` automatically.

Supported signatures:

- `get(url[, options][, callback])`
- `get(options[, callback])`

<h6>Syntax</h6>

```js
get(url[, options][, callback])
get(options[, callback])
```

## Agent

HTTP agent wrapper.

<h6>Creation</h6>

```js
new Agent([options])
```

<h6>Methods</h6>

- `destroy()`

## ClientRequest

Outgoing request object returned by `request()` / `get()`.

## ClientRequest header methods

- `setHeader(name, value)`
- `getHeader(name)`
- `hasHeader(name)`
- `removeHeader(name)`
- `getHeaders()`
- `getHeaderNames()`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,5]}
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Test-Header', 'TestValue');
console.println(req.hasHeader('X-Test-Header'));
console.println(req.getHeader('X-Test-Header'));
req.end();
```

## ClientRequest.write()

Writes body chunks.

- `chunk` supports `string` and `Uint8Array`
- returns `true` on success, `false` on failure

<h6>Syntax</h6>

```js
write(chunk[, encoding][, callback])
```

## ClientRequest.end()

Finishes and sends the request.

<h6>Syntax</h6>

```js
end([data[, encoding]][, callback])
```

## ClientRequest.destroy()

Destroys request object and optionally emits an error.

<h6>Syntax</h6>

```js
destroy([err])
```

## ClientRequest events

- `response` (`IncomingMessage`)
- `error` (`Error`)
- `end` ()

## IncomingMessage

HTTP response object.

<h6>Main properties</h6>

- `statusCode`
- `statusMessage`
- `ok` (true for 2xx)
- `headers`
- `rawHeaders`
- `httpVersion`
- `complete`

## IncomingMessage body methods

- `text([encoding])`
- `json()`
- `readBody([encoding])`
- `readBodyBuffer()`

## IncomingMessage utility methods

- `setTimeout(msecs[, callback])`
- `close()`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,5]}
const http = require('http');
http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println(res.ok, res.statusCode);
  console.println(res.text());
});
```

## Server

HTTP server object.

<h6>Creation</h6>

```js
new Server([options])
```

<h6>Options</h6>

- `network`: `tcp` or `unix` (default: `tcp`)
- `address`: `host:port` or unix socket path

## Server route and static methods

- `get(path, handler)`
- `static(path, root)`
- `staticFile(path, file)`

## Server template methods

- `loadHTMLFiles(...files)`
- `loadHTMLGlob(pattern)`

## Server lifecycle methods

- `serve([callback])`
- `close([callback])`

`serve(callback)` receives `{ network, address }`.

<h6>Usage example</h6>

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

Handler receives `ctx` with request and response helpers.

<h6>Request helpers</h6>

- `ctx.request.path`
- `ctx.request.query`
- `ctx.request.body`
- `ctx.request.getHeader(name)`
- `ctx.param(name)`
- `ctx.query(name)`

<h6>Response helpers</h6>

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

HTTP status-code map.

Examples:

- `http.status.OK`
- `http.status.NotFound`
- `http.status.InternalServerError`
