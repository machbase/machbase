---
title: "@jsh/mqtt"
type: docs
weight: 11
---

{{< neo_since ver="8.0.52" />}}


## Client

The MQTT client.

**Usage example**

```js {linenos=table,linenostart=1}
const mqtt = require("@jsh/mqtt");

const client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:1236"],
        keepAlive: 30,
        cleanStart: true,
    }, (evt, msg) => {
        console.log(evt, msg);
    }
);

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

### Creation

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | Instantiates a MQTT client object with an options |

### Options

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

### Methods

### connect()

### disconnect()

### awaitConnection()

### subscribe()

### publish()

## Examples

### Run subscriber

- Create an application as `mqtt-sub.js`.

```js {linenos=table,linenostart=1,hl_lines=[20,23,31,38,45]}
const process = require("@jsh/process");
const println = process.println;
const mqtt = require("@jsh/mqtt");
if( process.ppid() == 1 ) {
    console.log("mqtt-sub start...")
    runBackground();
    console.log("mqtt-sub terminated.")
} else {
    // make the current process stop,
    // and start new one as a background process.
    process.daemonize();
}
function runBackground() {
    var client;
    var testTopic = "test/topic";
    client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:5653"],
        keepAlive: 30,
        cleanStart: true,
        onConnect: (ack) => {
            println("connected.");
            println("subscribe to", testTopic);
            client.subscribe({subscriptions:[{topic:testTopic, qos:0}]});
        },
        onConnectError: (err) => {
            println("connect error", err);
        },
        onDisconnect: (disconn) => {
            println("disconnected.");
        },
        onMessage: (msg) => {
            println("recv topic:", msg.topic,
                "QoS:", msg.qos,
                "payload:", msg.payload.string())
        },
    });
    try {
        client.connect();
        while(true) {
            process.sleep(1000);
        }
    } catch (e) {
        console.error(e.toString());
    } finally {
        client.disconnect()
    }
}
```

- Run `mqtt-sub.js` from JSH.

```
jsh / > mqtt-sub
jsh / > ps
┌──────┬──────┬──────┬───────────────────┬────────┐ 
│  PID │ PPID │ USER │ NAME              │ UPTIME │ 
├──────┼──────┼──────┼───────────────────┼────────┤ 
│ 1025 │ -    │ sys  │ jsh               │ 4m8s   │ 
│ 1037 │ 1    │ sys  │ /sbin/mqtt-sub.js │ 1s     │ 
│ 1038 │ 1025 │ sys  │ ps                │ 0s     │ 
└──────┴──────┴──────┴───────────────────┴────────┘ 
```

- Send messages using mosquitto_pub or any other MQTT client.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t test/topic -m 'hello?'
```

The `mqtt-sub.js` application received the published message via the subscription.

```
2025/05/02 09:56:18.381 INFO  /sbin/mqtt-sub.js mqtt-sub start...
2025/05/02 09:56:18.382 INFO  /sbin/mqtt-sub.js connected.
2025/05/02 09:56:18.383 INFO  /sbin/mqtt-sub.js subscribe to test/topic
2025/05/02 09:56:26.149 INFO  /sbin/mqtt-sub.js recv topic: test/topic QoS: 0 payload: hello?
```

- You can 
stop the background process `mqtt-sub.js` with `kill <pid>` command.

```
jsh / > kill 1037
jsh / > ps
┌──────┬──────┬──────┬──────┬────────┐ 
│  PID │ PPID │ USER │ NAME │ UPTIME │ 
├──────┼──────┼──────┼──────┼────────┤ 
│ 1025 │ -    │ sys  │ jsh  │ 16m50s │ 
│ 1041 │ 1025 │ sys  │ ps   │ 0s     │ 
└──────┴──────┴──────┴──────┴────────┘ 
```