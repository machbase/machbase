---
title: Examples
type: docs
weight: 1
---

## HTTP Server

This example shows how to build a simple HTTP server using the `http` module.
The server listens on `127.0.0.1:56802` and provides a REST endpoint at `/hello/:name`.
When a client sends a GET request with a name parameter,
the server responds with a JSON object containing a greeting message and the provided name.

This is a practical example for learning dynamic routing and JSON responses in a lightweight server.

<h6>Key Features</h6>

1. **Routing**: Extracts `name` from `/hello/:name`.
2. **JSON response**: Returns a JSON object with message and name.

```js {linenos=table,linenostart=1}
const http = require('http');

const svr = new http.Server({network:'tcp', address:'127.0.0.1:56802'});

svr.get('/hello/:name', (ctx) => {
    const name = ctx.param("name")
    ctx.json(http.status.OK, {
        message: "greetings",
        name: name,
    })
})

svr.serve((result) =>{
    console.println('server started', result.network, result.address);
});
```

<h6>Usage</h6>

1. Open *JSH* console.
2. Run the script to start the server.
3. Send a GET request with `curl` (or similar tool):

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

The server will respond with:

```json
{"message":"greetings","name":"Karl"}
```

### Static Content

```js {linenos=table,linenostart=1}
svr.staticFile("/readme", "/path/to/file.txt");
svr.static("/static", "/path/to/static_dir");
```

### Redirect

```js {linenos=table,linenostart=1}
svr.get("/readme", ctx => {
    ctx.redirect(http.status.Found, "/docs/readme.html");
});
```

### RESTful API

```js {linenos=table,linenostart=1}
svr.get("/movies", ctx => {
    list = [
        {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
        {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
    ]
    ctx.json(http.status.OK, list);
})
svr.post("/movies", ctx => {
    let obj = ctx.request.body;
    list.push(obj);
    ctx.json(http.status.Created, obj);
});
svr.delete("/movies/:id", ctx => {
    let id = parseInt(ctx.param('id'));
    list = list.filter(item => item.id !== id);
    ctx.json(http.status.NoContent)
})
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

### HTML Templates

This line enables the server to load all HTML template files matching the `/*.html` pattern.
These templates allow the server to dynamically generate HTML responses by combining predefined layouts with data provided during runtime.

```js
svr.loadHTMLGlob("/*.html")

// Defines a GET route /movielist that serves an HTML page.
svr.get("/movielist", ctx => {
    obj = {
        subject: "Movie List",
        list: [
            {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
            {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
        ]
    }
    ctx.HTML(http.status.OK, "movie_list.html", obj)
})
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

## HTTP Client

This example demonstrates how to create an HTTP client with the `http` module.
The client sends a GET request to a target URL and processes the response.
It is useful for learning request handling and JSON response parsing.

<h6>Key Features</h6>

1. **Request handling**: Sends an HTTP GET request.
2. **Response parsing**: Reads status and body.
3. **Error handling**: Handles request errors with `try-catch`.

```js {linenos=table,linenostart=1}
const http = require('http')
try {
    const url = new URL('http://127.0.0.1:56802/hello/Steve');
    // Creates a GET request to the specified URL.
    const req = http.request(url);
    req.end((response) => {
        const {statusCode, statusMessage} = response;
        console.println("Status Code:", statusCode);
        console.println("Status Message:", statusMessage);
        console.println("Body:", response.json());
    })
} catch (e) {
    // Prints errors during request processing.
    println(e.message);
}
// Output:
//
// Status Code: 200
// Status Message: 200 OK
// Body: {message:greetings, name:Steve}
```

<h6>Usage</h6>

1. Ensure the HTTP server example is running.
2. Run the script to send a GET request.

