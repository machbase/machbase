---
title: "mqtt"
type: docs
weight: 100
---

{{< neo_since ver="8.0.74" />}}

The `mqtt` is the MQTT client module.

In JSH applications, you normally use:

```js
const mqtt = require('mqtt');
```

This module is event-driven and auto-connects when a `Client` is created.

## Client

MQTT client object.

<h6>Creation</h6>

```js
new Client(options)
```

<h6>Options</h6>

| Option                             | Type       | Default | Description |
|:-----------------------------------|:-----------|:--------|:------------|
| servers                            | String[]   |         | MQTT broker URLs (e.g. `tcp://127.0.0.1:1883`) |
| username                           | String     |         | Username for broker authentication |
| password                           | String     |         | Password for broker authentication |
| keepAlive                          | Number     | `30`    | Keep alive in seconds |
| connectRetryDelay                  | Number     | `0`     | Reconnect delay in milliseconds |
| cleanStartOnInitialConnection      | Boolean    | `false` | MQTT v5 clean start on first connection |
| connectTimeout                     | Number     | `0`     | Connect timeout in milliseconds |

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const mqtt = require('mqtt');

const client = new mqtt.Client({
    servers: ['tcp://127.0.0.1:1883'],
    username: 'user',
    password: 'pass',
    keepAlive: 60,
    connectRetryDelay: 2000,
    connectTimeout: 10 * 1000,
    cleanStartOnInitialConnection: true,
});

client.on('open', () => {
    console.println('Connected');
    client.subscribe('test/topic');
});

client.on('subscribed', (topic, reason) => {
    console.println('Subscribed:', topic, 'reason:', reason);
    client.publish('test/topic', 'Hello, MQTT!');
});

client.on('message', (msg) => {
    console.println('Message:', msg.topic, msg.payload);
    client.close();
});

client.on('error', (err) => {
    console.println('Error:', err.message);
});

client.on('close', () => {
    console.println('Disconnected');
});
```

## Methods

### publish()

Publishes a message to a topic.

<h6>Syntax</h6>

```js
publish(topic, message[, options])
```

<h6>Parameters</h6>

- `topic` `String`
- `message` `String` | `Uint8Array` | `Object` | `Array`
- `options` `Object` (optional)

| Option      | Type    | Default | Description |
|:------------|:--------|:--------|:------------|
| qos         | Number  | `0`     | QoS level |
| retain      | Boolean | `false` | Retain flag |
| properties  | Object  |         | MQTT v5 publish properties |

`options.properties` fields:

| Property                  | Type     | Description |
|:--------------------------|:---------|:------------|
| payloadFormat             | Number   | Payload format indicator |
| messageExpiry             | Number   | Expiry interval |
| contentType               | String   | Content type |
| responseTopic             | String   | Response topic |
| correlationData           | String   | Converted to bytes |
| topicAlias                | Number   | Topic alias |
| subscriptionIdentifier    | Number   | Subscription identifier |
| user                      | Object   | User properties (`key: value`) |

<h6>Return value</h6>

None. Result is delivered by `published` or `error` events.

### subscribe()

Subscribes to a topic.

<h6>Syntax</h6>

```js
subscribe(topic)
```

<h6>Parameters</h6>

- `topic` `String`

<h6>Return value</h6>

None. Result is delivered by `subscribed` or `error` events.

Note: current implementation subscribes with QoS 1.

### close()

Closes the client connection.

<h6>Syntax</h6>

```js
close()
```

<h6>Return value</h6>

None. Emits `close` event.

## Events

### open

Emitted after the client is connected.

```js
client.on('open', () => { ... })
```

### message

Emitted when a subscribed message is received.

```js
client.on('message', (msg) => { ... })
```

`msg` fields:

| Property | Type   | Description |
|:---------|:-------|:------------|
| topic    | String | Topic name |
| payload  | String | Message payload |

### subscribed

Emitted when subscription ack is received.

```js
client.on('subscribed', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` (MQTT reason code)

### published

Emitted when publish ack is received.

```js
client.on('published', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` (MQTT reason code)

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

## MQTT v5 write properties example

This example writes to `db/write/{table}` and sets MQTT v5 user properties documented in MQTT v5 write API.

```js {linenos=table,linenostart=1}
const mqtt = require('mqtt');

const client = new mqtt.Client({
    servers: ['tcp://127.0.0.1:5653'],
});

const rows = [
    ['my-car', Date.now(), 32.1],
    ['my-car', Date.now() + 1000, 65.4],
];

client.on('open', () => {
    client.publish('db/write/EXAMPLE', rows, {
        qos: 1,
        properties: {
            user: {
                method: 'append',
                timeformat: 'ms',
            },
        },
    });
});

client.on('published', () => client.close());
client.on('error', (err) => console.println(err.message));
```
