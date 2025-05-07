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
| onClientError       | function     | null           | (err) => {}         |
| onConnect           | function     | null           | (ack) => {}         |
| onConnectError      | function     | null           | (err) => {}         |
| onDisconnect        | function     | null           | (disconnect) => {}  |
| onMessage           | function     | null           | (msg) => {}         |

### connect()

### disconnect()

### awaitConnection()

### subscribe()

### publish()
