---
title: "@jsh/http"
type: docs
weight: 12
---

{{< neo_since ver="8.0.52" />}}

## Client

The HTTP client.

### Creation

| Constructor             | Description                          |
|:------------------------|:-------------------------------------|
| new Client()            | Instantiates a HTTP client           |


### Methods

#### do()

<h6>Syntax</h6>

```js
client.do(url)
client.do(url, option)
client.do(url, option, callback)
```

<h6>Parameters</h6>

- `url` `String`
- `option` `Object` [RequestOption](#requestoption)
- `callback` `(response) => {}` callback function.

<h6>Return value</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | http status code   |
| statusText         | String     | http status message|
| url                | String     | request url        |
| error              | String     | error message      |

<h6>Usage example</h6>

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

## request()

<h6>Syntax</h6>

```js
request(url, option)
```

<h6>Parameters</h6>

- `url` `String` destination address. e.g. `http://192.168.0.120/api/members`
- `option` `Object` optional [RequestOption](#RequestOption).

<h6>Return value</h6>

`Request` [Request](#Request) Object

<h6>Usage example</h6>

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

## RequestOption

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| method              | String       | `GET`          | GET, POST, DELETE, PUT... |
| headers             | Object       |                |                     |
| body                | String       |                | Content to send     |


## Request

### Methods

#### do()

<h6>Syntax</h6>

```js
do(callback)
```

<h6>Parameters</h6>

- `callback` `(response) => {}` callback function.


<h6>Return value</h6>

None.

## Response

<h4>Properties</h4>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | status code. e.g. 200, 404 |
| statusText         | String     | e.g. 200 OK        |
| headers            | Object     | response headers   |
| method             | String     | request method     |
| url                | String     | request url        |
| error              | String     | error message      |


## Listener

The HTTP server listener.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http")
const lsnr = new http.Listener({
    network:'tcp',
    address:'127.0.0.1:8080',
})
lsnr.get("/hello/:name", (ctx) => {
    name = ctx.param("name")
    greeting = ctx.query("greeting")
    ctx.JSON(http.status.OK, {
        "greeting": greeting,
        "name": name,
    })
})
lsnr.static("/html", "/html")
lsnr.listen();
```

### Creation

| Constructor             | Description                          |
|:------------------------|:-------------------------------------|
| new Listener(options)   | Instantiates a HTTP client           |

<h6>Options</h6>

| Option       | Type      | Default    | Description         |
|:-------------|:----------|:-----------|:--------------------|
| network      | String    | `tcp`      | network type        |
| address      | String    |            | listen address      |


### Methods

#### all()

Add a route to handle all methods includes GET, POST, PUT, DELETE...

<h6>Syntax</h6>

```js
all(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#HttpContext) parameter providing request-specific details.

<h6>Return value</h6>

None.

#### get()

Add a route to handle GET method.

<h6>Syntax</h6>

```js
get(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#HttpContext) parameter providing request-specific details.

<h6>Return value</h6>

None.

#### post()

Add a route to handle POST method.

<h6>Syntax</h6>

```js
put(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#HttpContext) parameter providing request-specific details.

<h6>Return value</h6>

None.

#### put()

Add a route to handle PUT method.

<h6>Syntax</h6>

```js
put(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#HttpContext) parameter providing request-specific details.

<h6>Return value</h6>

None.

#### delete()

Add a route to handle DELETE method.

<h6>Syntax</h6>

```js
delete(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#HttpContext) parameter providing request-specific details.

<h6>Return value</h6>

None.

#### static()

Defines a route to serve files from a specified static directory in response to requests matching a given path.

<h6>Syntax</h6>

```js
static(request_path, dir_path)
```

<h6>Parameters</h6>

- `request_path` `String`
- `dir_path` `String`

<h6>Return value</h6>

None.

#### staticFile()

Add a route to serve static file content for a specified request path.

<h6>Syntax</h6>

```js
staticFile(request_path, file_path)
```

<h6>Parameters</h6>

- `request_path` `String`
- `file_path` `String`

<h6>Return value</h6>

None.

#### listen()

Blocks the control flow and starts listening until `stop()` is called.

<h6>Syntax</h6>

```js
listen()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

#### close()

Stop and shutdown the listener.

<h6>Syntax</h6>

```js
close()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

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

## HttpContext

### Properties

- request

### Methods

#### abort()

#### redirect()

#### getHeader()

#### setHeader()

#### param()

#### query()

#### TEXT()

#### JSON()

#### HTML()

#### XML()

#### YAML()

#### TOML

## HttpRequest

### Properties

- header
- method
- host
- path
- query
- body
- remoteAddr

### Methods

#### getHeader()
