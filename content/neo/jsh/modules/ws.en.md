---
title: "ws"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `ws` module provides a WebSocket client for JSH applications.
It exposes a single `WebSocket` class built on top of the native Go WebSocket client.

Typical usage looks like this.

```js
const { WebSocket } = require('ws');
```

## WebSocket

Creates a WebSocket client connection.

<h6>Syntax</h6>

```js
new WebSocket(url)
```

<h6>Parameters</h6>

- `url` `String`: WebSocket server address such as `ws://host:port/path` or `wss://host:port/path`.

If `url` is missing or is not a string, the constructor throws `TypeError`.

## Properties

| Property | Type | Description |
|:---------|:-----|:------------|
| `url` | String | Original WebSocket URL passed to the constructor. |
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

- The module implements a WebSocket client only. It does not provide server-side upgrade handling.
- Connection establishment is started asynchronously from the constructor.
- Connection failures are reported through the `error` event.
- Incoming messages may be text or binary, but the JavaScript `send()` method is intended for text message usage.