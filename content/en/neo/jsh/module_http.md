---
title: "@jsh/http"
type: docs
weight: 12
---

{{< neo_since ver="8.0.52" />}}

## request()

<h4>Syntax</h4>

```js
request(url, option)
```

<h6>Parameters</h6>

- `url` `String` destination address. e.g. `http://192.168.0.120/api/members`
- `option` `Object` optional [RequestOption](#RequestOption).

<h6>Return value</h6>

`Request` [Request](#Request) Object

<h4>Usage example</h4>

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

### Request.do()

<h4>Syntax</h4>

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
| url                | String     | request url        |

### Response.error()

### Response.text()
