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
    client.awaitConnection(1000);
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

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| serverUrls          | []String     |                | server addresses    |
| keepAlive           | Number       | `10`           |                     |
| cleanStart          | Boolean      | false          | clean session       |
| username            | String       |                |                     |
| password            | String       |                |                     |
| clientID            | String       | random id      |                     |
| onClientError       | function     |                | (err) => {}         |
| onConnect           | function     |                | (ack) => {}         |
| onConnectError      | function     |                | (err) => {}         |
| onDisconnect        | function     |                | (disconnect) => {}  |
| onMessage           | function     |                | (msg) => {}         |

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
disconnect()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

### awaitConnection()

<h6>Syntax</h6>

```js
awaitConnection()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

### subscribe()

<h6>Syntax</h6>

```js
subscribe(opts)
```

<h6>Parameters</h6>

- `opts` `Object` [SubscriptionOption](#subscriptionoption)

<h6>Return value</h6>

None.

### publish()

<h6>Syntax</h6>

```js
publish()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.


## SubscriptionOption

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| subscriptions      | Object[]   | Array of [Subscription](#subscriptions) |
| userProperties     | Object     | key-value object      |

## Subscription

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| topic              | String     |                       |
| qos                | Number     | `0`, `1`, `2`         |
| retainHandling     | Number     |                       |
| noLocal            | Boolean    |                       |
| retainAsPublished  | Boolean    |                       |

## onMessage()

On publish message callback.

<h6>Syntax</h6>

```js
funciton (msg) { }
```

<h6>Parameters</h6>

- `msg` `Message` [Message](#message)

<h6>Return value</h6>

None.


### Message

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| packetID           | Number     |                       |
| qos                | Number     |                       |
| retain             | Boolean    |                       |
| topic              | String     |                       |
| payload            | Object     | [Payload](#payload)   |
| properties         | Object     | [MessageProperties](#messageproperties) |
| user               | Object     | [UserProperties](#userproperties)       |

### Payload

#### bytes()

<h6>Syntax</h6>

```js
bytes()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

Array of bytes.

#### string()

<h6>Syntax</h6>

```js
string()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String

### MessageProperties

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| correlationData    |            |                       |
| contentType        |            |                       |
| responseTopic      |            |                       |
| payloadFormat      |            |                       |
| messageExpiry      |            |                       |
| subscriptionIdentifier |        |                       |
| topicAlias         |            |                       |

### UserProperties

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
|                    |            |                       |

## onConnect()

On connect callback.

<h6>Syntax</h6>

```js
funciton (ack) { }
```

<h6>Parameters</h6>

- `ack` `Object`

<h6>Return value</h6>

None.

## onConnectError()

On connect error callback.

<h6>Syntax</h6>

```js
funciton (err) { }
```

<h6>Parameters</h6>

- `error` `String`

<h6>Return value</h6>

None.

## onDisconnect()

On disconnect callback

<h6>Syntax</h6>

```js
funciton (disconn) { }
```

<h6>Parameters</h6>

- `disconn` `Object`

<h6>Return value</h6>

None.

## onClientError()

On client error callback

<h6>Syntax</h6>

```js
funciton (err) { }
```

<h6>Parameters</h6>

- `err` `String`

<h6>Return value</h6>

None.
