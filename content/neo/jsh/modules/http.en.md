---
title: "http"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `http` module provides Node.js-compatible HTTP client and server APIs for JSH applications.

## request()

Creates a `ClientRequest` object.

Supported signatures:

- `request(url[, options][, callback])`
- `request(options[, callback])`

- Returns: `ClientRequest`
- If `callback` is provided, it receives `IncomingMessage` when a response arrives.

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

- Returns: `ClientRequest`
- If `callback` is omitted, handle the response with the `response` event listener.

<h6>Syntax</h6>

```js
get(url[, options][, callback])
get(options[, callback])
```

**status**

HTTP status-code map.

Examples:

- `http.status.OK`
- `http.status.NotFound`
- `http.status.InternalServerError`

**Behavior notes**

- `response.ok` is `true` for status codes in the `200`-`299` range.
- Keys in `response.headers` are normalized to lowercase.
- `setHeader()` / `getHeader()` / `hasHeader()` / `removeHeader()` treat header names case-insensitively.
- Multiple `write()` calls accumulate request body data before sending.

## ClientRequest

Outgoing request object returned by `request()` / `get()`.

**ClientRequest header methods**

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

**ClientRequest.write()**

Writes body chunks.

- `chunk` supports `string` and `Uint8Array`
- returns `true` on success, `false` on failure

<h6>Syntax</h6>

```js
write(chunk[, encoding][, callback])
```

**ClientRequest.end()**

Finishes and sends the request.

- If `callback` is provided, it receives the response object (`IncomingMessage`).

<h6>Syntax</h6>

```js
end([data[, encoding]][, callback])
```

**ClientRequest.destroy()**

Destroys request object and optionally emits an error.

<h6>Syntax</h6>

```js
destroy([err])
```

**ClientRequest events**

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
- `raw` (internal Go response object)

**IncomingMessage body methods**

- `text([encoding])`
- `json()`
- `readBody([encoding])`
- `readBodyBuffer()`

- `text()` and `readBody()` use `utf-8` by default.
- `json()` can throw if parsing fails.

**IncomingMessage utility methods**

- `setTimeout(msecs[, callback])`
- `close()`

Response bodies are typically closed automatically in normal processing flow, and `close()` can be called explicitly when needed.

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
- `env`: env object (optional), It is required to access the filesystem.

**Server route and static methods**

- `get(path, handler)`
- `static(path, root)`
- `staticFile(path, file)`

**Server template methods**

- `loadHTMLFiles(...files)`
- `loadHTMLGlob(pattern)`

**Server lifecycle methods**

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

**Server context**

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

## Client examples

### GET request (callback)

```js {linenos=table,linenostart=1,hl_lines=[3]}
const http = require('http');

http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  console.println('Body:', res.text());
});
```

### GET request (event listener)

```js {linenos=table,linenostart=1,hl_lines=[4]}
const http = require('http');

const req = http.get('http://127.0.0.1:8080/hello');
req.on('response', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  console.println('Body:', res.text());
});
```

### Set and read request headers

```js {linenos=table,linenostart=1,hl_lines=[4,5,6]}
const http = require('http');

const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Trace-Id', 'trace-001');
console.println(req.hasHeader('x-trace-id'));
console.println(req.getHeader('X-Trace-Id'));
req.end();
```

### Read response headers and body

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

### POST request with JSON

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

### Handle 404 responses

```js {linenos=table,linenostart=1,hl_lines=[5]}
const http = require('http');

http.get('http://127.0.0.1:8080/notfound', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  if (!res.ok) {
    console.println('Request failed');
  }
});
```

### Request with URL object

When the server is running, send a GET request and parse the JSON body.

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

## Server examples

### Simple HTTP server

Runs a server on `127.0.0.1:56802` and returns JSON from `/hello/:name`.

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

### Static content and redirect

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


- GET
```sh
curl -o - http://127.0.0.1:56802/movies
```
```json
[
  { "id": 59793, "studio": [ "Paramount" ], "title": "Indiana Jones" },
  { "id": 64821, "studio": [ "Lucasfilm" ], "title": "Star Wars" }
]
```

- POST

```sh
curl -o - -X POST http://127.0.0.1:56802/movies \
    -H "Content-Type: application/json" \
    -d '{"title":"new movie", "id":12345, "studio":["HomeVideo"]}'
```

- DELETE

```sh
curl -v -o - -X DELETE http://127.0.0.1:56802/movies/12345
```

```sh
< HTTP/1.1 204 No Content
< Content-Type: text/plain; charset=utf-8
< Date: Thu, 08 May 2025 20:39:34 GMT
<
```

### HTML templates

This line enables the server to load all HTML template files matching the `/*.html` pattern.
These templates allow the server to dynamically generate HTML responses by combining predefined layouts with data provided during runtime.

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

- HTML Template Code `movie_list.html`

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

Sends a GET request to the `/movielist` endpoint.
The server responds with an HTML page generated using the `movie_list.html` template and the `obj` data.

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
