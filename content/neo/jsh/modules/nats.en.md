---
title: "nats"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `nats` module provides a NATS client for JSH applications.
Like the MQTT module, it is event-driven and automatically starts connecting when a `Client` is created.

Typical usage looks like this.

```js
const nats = require('nats');
```

## Client

NATS client object.

<h6>Creation</h6>

```js
new Client(options)
```

<h6>Options</h6>

| Option | Type | Description |
|:-------|:-----|:------------|
| `servers` | String[] | NATS server URLs such as `nats://127.0.0.1:4222` |
| `name` | String | Connection name |
| `user` | String | Authentication user |
| `password` | String | Authentication password |
| `token` | String | Authentication token |
| `noRandomize` | Boolean | Disable server randomization |
| `noEcho` | Boolean | Disable echo of this client's published messages |
| `verbose` | Boolean | Enable verbose protocol behavior |
| `pedantic` | Boolean | Enable pedantic protocol checks |
| `allowReconnect` | Boolean | Enable reconnect handling |
| `maxReconnect` | Number | Maximum reconnect attempts |
| `reconnectWait` | Number | Reconnect wait in milliseconds |
| `timeout` | Number | Connect timeout in milliseconds |
| `drainTimeout` | Number | Drain timeout in milliseconds |
| `flusherTimeout` | Number | Flush timeout in milliseconds |
| `pingInterval` | Number | Ping interval in milliseconds |
| `maxPingsOut` | Number | Maximum outstanding pings |
| `retryOnFailedConnect` | Boolean | Retry when the first connection fails |
| `skipHostLookup` | Boolean | Skip host lookup optimization |

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const nats = require('nats');

const client = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
    name: 'test-client',
    allowReconnect: true,
    maxReconnect: 10,
    reconnectWait: 2000,
    timeout: 10 * 1000,
});
```

## Properties

### config

`client.config` exposes the parsed native NATS configuration.

Representative fields include:

- `servers`
- `name`
- `allowReconnect`
- `maxReconnect`
- `reconnectWait`
- `timeout`

```js
console.println(client.config.servers);
console.println(client.config.timeout);
```

## Methods

### publish()

Publishes a message to a subject.

<h6>Syntax</h6>

```js
publish(subject, message[, options])
```

<h6>Parameters</h6>

- `subject` `String`
- `message` `String` | `Uint8Array` | `Object` | `Array`
- `options` `Object` (optional)

Supported `options` fields:

| Option | Type | Description |
|:-------|:-----|:------------|
| `reply` | String | Reply subject for request/reply patterns |

Objects and arrays are JSON-encoded before publishing.

<h6>Return value</h6>

None. Result is delivered by `published` or `error` events.

### subscribe()

Subscribes to a subject.

<h6>Syntax</h6>

```js
subscribe(subject[, options])
```

<h6>Parameters</h6>

- `subject` `String`
- `options` `Object` (optional)

Supported `options` fields:

| Option | Type | Description |
|:-------|:-----|:------------|
| `queue` | String | Queue group name for queue subscriptions |

<h6>Return value</h6>

None. Result is delivered by `subscribed` or `error` events.

### close()

Closes the client connection.

<h6>Syntax</h6>

```js
close()
```

## Events

### open

Emitted after the connection is established.

```js
client.on('open', () => { ... })
```

### message

Emitted when a subscribed message is received.

```js
client.on('message', (msg) => { ... })
```

`msg` fields:

| Property | Type | Description |
|:---------|:-----|:------------|
| `topic` | String | Alias of the subject for MQTT-style handlers |
| `subject` | String | NATS subject |
| `reply` | String | Reply subject for request/reply workflows |
| `payload` | String | Message payload |

### subscribed

Emitted when the server accepts a subscription.

```js
client.on('subscribed', (subject, reason) => { ... })
```

- `subject` `String`
- `reason` `Number`

The current implementation uses `1` for successful subscribe acknowledgment.

### published

Emitted after a publish request completes.

```js
client.on('published', (subject, reason) => { ... })
```

- `subject` `String`
- `reason` `Number`

The current implementation uses `0` for successful publish completion.

### error

Emitted when connection, subscribe, or publish fails.

```js
client.on('error', (err) => { ... })
```

- `err` `Error`

### close

Emitted when `close()` is called.

```js
client.on('close', () => { ... })
```

## Basic pub/sub example

```js {linenos=table,linenostart=1}
const nats = require('nats');

const client = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
    name: 'test-client',
    timeout: 10 * 1000,
});

client.on('open', () => {
    console.println('Connected');
    client.subscribe('test.subject');
});

client.on('subscribed', (subject, reason) => {
    console.println('Subscribed to:', subject, 'reason:', reason);
    client.publish('test.subject', 'Hello, NATS!');
});

client.on('message', (msg) => {
    console.println('Message received on subject:', msg.subject, 'payload:', msg.payload);
    client.close();
});

client.on('close', () => {
    console.println('Disconnected');
});
```

## Request/reply example

For request/reply workflows, subscribe to a reply subject and publish with `options.reply`.

```js {linenos=table,linenostart=1}
const nats = require('nats');

const handler = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
});
handler.on('open', () => {
    handler.subscribe('request.subject');
});
handler.on('message', (msg) => {
    handler.publish(msg.reply, 'pong');
});

const requester = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
});
requester.on('open', () => {
    requester.subscribe('reply.subject');
    requester.publish('request.subject', 'ping', { reply: 'reply.subject' });
});
requester.on('message', (msg) => {
    console.println(msg.payload);
    requester.close();
    handler.close();
});
```

## Behavior notes

- `Client` starts connecting automatically from the constructor.
- Queue subscriptions are enabled through `subscribe(subject, { queue: 'workers' })`.
- Calling `publish()` or `subscribe()` before the connection is open emits an `error` event.
- Message payloads are exposed as strings by the current implementation.