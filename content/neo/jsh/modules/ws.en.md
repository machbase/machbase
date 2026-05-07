---
title: "ws"
type: docs
weight: 100
---

{{< neo_since ver="8.5.2" />}}

The `ws` module provides WebSocket client and server APIs for JSH applications.
It exposes `WebSocket` and `WebSocketServer` classes built on top of the native Go WebSocket implementation.

Typical usage looks like this.

```js
const { WebSocket, WebSocketServer } = require('ws');
```

## WebSocket

Creates a WebSocket client connection.

<h6>Syntax</h6>

```js
new WebSocket(url)
new WebSocket(url, protocol)
new WebSocket(url, protocols)
```

<h6>Parameters</h6>

- `url` `String`: WebSocket server address such as `ws://host:port/path` or `wss://host:port/path`.
- `protocol` `String`: one requested subprotocol.
- `protocols` `String[]`: list of requested subprotocols.

If `url` is missing or is not a string, the constructor throws `TypeError`.

## Properties

| Property | Type | Description |
|:---------|:-----|:------------|
| `url` | String | Original WebSocket URL passed to the constructor. |
| `protocol` | String | Negotiated subprotocol, or empty string. |
| `readyState` | Number | Current connection state. |

### readyState values

- `WebSocket.CONNECTING` = `0`
- `WebSocket.OPEN` = `1`
- `WebSocket.CLOSING` = `2`
- `WebSocket.CLOSED` = `3`

### Message type constants

- `WebSocket.TextMessage` = `1`
- `WebSocket.BinaryMessage` = `2`

## send()

Sends a message to the server.

<h6>Syntax</h6>

```js
ws.send(data)
```

<h6>Parameters</h6>

- `data` `String`: Message text to send.

In the current JSH implementation, `send()` is primarily intended for text messages.

If the socket is not open, the module emits an `error` event.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('open', () => {
    ws.send('Hello, server');
});
```

## close()

Closes the current connection.

<h6>Syntax</h6>

```js
ws.close()
```

Calling `close()` transitions the socket through `CLOSING` to `CLOSED` and emits `close`.

## Events

`WebSocket` extends `EventEmitter` and supports normal event-listener patterns such as `on()` and `addListener()`.

### open

Emitted after the client successfully connects.

```js
ws.on('open', () => {
    console.println('connected');
});
```

### close

Emitted when the connection closes.

```js
ws.on('close', () => {
    console.println('closed');
});
```

### message

Emitted when a message arrives from the server.

The callback receives an event-like object with these fields.

| Field | Type | Description |
|:------|:-----|:------------|
| `type` | Number | Message type such as `WebSocket.TextMessage` or `WebSocket.BinaryMessage`. |
| `data` | String or byte data | Message payload. Text messages are exposed as strings. |

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('message', (evt) => {
    console.println(evt.data);
});
```

### error

Emitted when connection or send operations fail.

```js
ws.on('error', (err) => {
    console.println(err.message);
});
```

## WebSocketServer

Creates a WebSocket server attached to an existing `http.Server`.

<h6>Syntax</h6>

```js
new WebSocketServer(options)
```

<h6>Main options</h6>

- `server`: attached `http.Server` instance. Required.
- `path`: accepted WebSocket path. Default is `/`.
- `clientTracking`: keeps the `clients` set when `true`. Default is `true`.
- `verifyClient({ origin, req })`: synchronously decides whether to accept the handshake. Returning `false` rejects the request.
- `handleProtocols(protocols, req)`: selects one value from requested subprotocols.

<h6>Properties</h6>

| Property | Type | Description |
|:---------|:-----|:------------|
| `server` | http.Server | Attached HTTP server. |
| `path` | String | Accepted WebSocket path. |
| `clients` | Set | Connected client set. `null` when `clientTracking === false`. |

### WebSocketServer events

- `connection(socket, request)`
- `error(err)`
- `close()`

### connection request object

The `request` value passed to `connection` is a helper object similar to Node.js `IncomingMessage`.

Main properties:

- `url`
- `method`
- `headers`
- `rawHeaders`
- `path`
- `host`
- `requestUri`
- `httpVersion`
- `complete`
- `remoteAddress`
- `socket.remoteAddress`

Main methods:

- `query(name)`
- `getHeader(name)`
- `hasHeader(name)`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require('http');
const { WebSocketServer } = require('ws');

const server = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
const wss = new WebSocketServer({
    server,
    path: '/ws',
    verifyClient: ({ req }) => req.query('token') === 'allow',
    handleProtocols: (protocols) => {
        if (protocols.indexOf('machbase.rpc') >= 0) {
            return 'machbase.rpc';
        }
        return false;
    },
});

wss.on('connection', (socket, request) => {
    console.println(request.path, request.httpVersion, socket.protocol);
    socket.on('message', (event) => {
        socket.send('echo:' + event.data);
    });
});

server.serve();
```

## Usage example

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');

ws.on('open', () => {
    console.println('websocket open');
    ws.send('test message');
});

ws.on('message', (evt) => {
    console.println(evt.data);
    ws.close();
});

ws.on('close', () => {
    console.println('websocket closed');
});
```

## Behavior notes

- Client connection establishment is started asynchronously from the constructor.
- Connection failures are reported through the `error` event.
- Incoming messages may be text or binary, but the JavaScript `send()` method is intended for text message usage.
- `WebSocketServer` provides a higher-level API attached to `http.Server`, rather than exposing low-level `upgrade` handling.
- `verifyClient()` and `handleProtocols()` are synchronous.
- Promise-based or `await`-style asynchronous flows are not supported inside `verifyClient()` and `handleProtocols()`.
- `request` is a JSH helper object, not a full Node.js `IncomingMessage` implementation. It exposes the main fields and methods such as `url`, `headers`, `query()`, and `getHeader()`.
- `clientTracking` maintains the `clients` set, but it does not add low-level socket management APIs.
- Low-level APIs such as `upgrade`, `handleUpgrade()`, and `noServer` are not currently provided.