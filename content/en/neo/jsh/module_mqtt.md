---
title: "@jsh/mqtt"
type: docs
weight: 11
---

{{< neo_since ver="8.0.52" />}}


## Client

The MQTT client.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const mqtt = require("@jsh/mqtt");

const client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:1236"],
        keepAlive: 30,
        cleanStart: true,
        onConnect: (ack) => {
            println("connected.");
        },
        onConnectError: (err) => {
            println("connect error", err);
        },
    });

try {    
    client.connect();
    client.awaitConnect(1000);
    client.publish("test/topic", "Hello, MQTT!", 0)
} catch(e) {
    console.log("Error:", e);
} finally {
    client.disconnect();
}
```

<h6>Creation</h6>

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | Instantiates a MQTT client object with an options |

<h6>Options</h6>

| Option                             | Type         | Default        | Description         |
|:-----------------------------------|:-------------|:---------------|:--------------------|
| serverUrls                         | String[]     |                | server addresses    |
| keepAlive                          | Number       | `10`           |                     |
| cleanStart                         | Boolean      | `true`         | clean session       |
| username                           | String       |                |                     |
| password                           | String       |                |                     |
| clientID                           | String       | random id      |                     |
| [onConnect](#onconnect)            | function     |                | (ack) => {}         |
| [onConnectError](#onconnecterror)  | function     |                | (err) => {}         |
| [onDisconnect](#ondisconnect)      | function     |                | (disconnect) => {}  |
| [onClientError](#onclienterror)    | function     |                | (err) => {}         |
| debug                              | Boolean      | `false`        |                     |
| sessionExpiryInterval              | Number       | `60`           |                     |
| connectRetryDelay                  | Number       | `10`           |                     |
| connectTimeout                     | Number       | `10`           |                     |
| packetTimeout                      | Number       | `5`            |                     |
| queue                              | String       |                | `memory`            |

### connect()

<h6>Syntax</h6>

```js
connect()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

### disconnect()

<h6>Syntax</h6>

```js
disconnect(opt)
```

<h6>Parameters</h6>

- `opt` `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| waitForEmptyQueue  | Boolean    |                       |
| timeout            | Number     | disconnect wait timeout in milliseconds |

<h6>Return value</h6>

None.

### awaitConnect()

<h6>Syntax</h6>

```js
awaitConnect(timeout)
```

<h6>Parameters</h6>

- `timeout` `Number` time in milliseconds.

<h6>Return value</h6>

None.

### awaitDisconnect()

<h6>Syntax</h6>

```js
awaitDisconnect(timeout)
```

<h6>Parameters</h6>

- `timeout` `Number` time in milliseconds.

<h6>Return value</h6>

None.

### subscribe()

<h6>Syntax</h6>

```js
subscribe(opts)
```

<h6>Parameters</h6>

- `opts` `Object` *SubscriptionOption*

<h6>SubscriptionOption</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| subscriptions      | Object[]   | Array of *Subscription* |
| userProperties     | Object     | key-value object      |

<h6>Subscription</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| topic              | String     |                       |
| qos                | Number     | `0`, `1`, `2`         |
| retainHandling     | Number     |                       |
| noLocal            | Boolean    |                       |
| retainAsPublished  | Boolean    |                       |

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js
const topicName = 'sensor/temperature';
client.subscribe({subscriptions:[{topic:topicName, qos:0}]});
```

### publish()

<h6>Syntax</h6>

```js
publish(topic, payload, qos)
```

<h6>Parameters</h6>

- `topic` `String`
- `payload` `String` or `Number`
- `qos` `Number` QoS `0`, `1`, `2`

<h6>Return value</h6>

- `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| reasonCode         | Number     |                       |
| properties         | Object     |                       |

<h6>Usage example</h6>

```js
let r = client.publish('sensor/temperature', 'Hello World', 1)
console.log(r.reasonCode)
```

### addPublishReceived()

<h6>Syntax</h6>

```js
addPublishReceived(callback)
```

<h6>Parameters</h6>

- `callback` `(msg) => {}` onPublishReceived callback

<h6>Return value</h6>

None.

## onPublishReceived callback

Callback function that receives a message.

<h6>Syntax</h6>

```js
function (msg) {}
```

<h6>Parameters</h6>

- `msg` `Object` Message

<h6>Message</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| packetID           | Number     |                       |
| topic              | String     |                       |
| qos                | Number     | 0, 1, 2               |
| retain             | Boolean    |                       |
| payload            | Object     | Payload               |
| properties         | Object     | Properties            |

<h6>Payload</h6>

- `msg.payload.bytes()`
- `msg.payload.string()`

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| correlationData    | byte[]     |                       |
| contentType        | String     |                       |
| responseTopic      | String     |                       |
| payloadFormat      | Number     | or undefined          |
| messageExpiry      | Number     | or undefined          |
| subscriptionIdentifier | Number | or undefined          |
| topicAlias         | Number     | or undefined          |
| user               | Object     |                       |

## onConnect callback

On connect callback.

<h6>Syntax</h6>

```js
funciton (ack) { }
```

<h6>Parameters</h6>

- `ack` `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| sessionPresent     | Boolean    |                       |
| reasonCode         | Number     |                       |
| properties         | Object     | Properties            |

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| reasonString       | String     |                       |
| reasonInfo         | String     |                       |
| assignedClientID   | String     |                       |
| authMethod         | String     |                       |
| serverKeepAlive    | Number     | or undefined          |
| sessionExpiryInterval | Number  | or undefined          |
| user               | Object     |                       |

<h6>Return value</h6>

None.

## onConnectError callback

On connect error callback.

<h6>Syntax</h6>

```js
funciton (err) { }
```

<h6>Parameters</h6>

- `error` `String`

<h6>Return value</h6>

None.

## onDisconnect callback

On disconnect callback

<h6>Syntax</h6>

```js
funciton (disconn) { }
```

<h6>Parameters</h6>

- `disconn` `Object`

<h6>Return value</h6>

None.

## onClientError callback

On client error callback

<h6>Syntax</h6>

```js
funciton (err) { }
```

<h6>Parameters</h6>

- `err` `String`

<h6>Return value</h6>

None.
