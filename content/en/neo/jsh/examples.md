---
title: Examples
type: docs
weight: 1
---

## MQTT Subscriber

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


## System Monitoring

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
const psutil = require("@jsh/psutil");

if( process.ppid() == 1 ) {
    runSysmon();
} else {
    process.daemonize();
}

function runSysmon() {
    process.schedule("@every 5s", (ts) => {
        time = new Date(ts.Unix()*1000).
                toLocaleString("ko-KR", {timeZone: "KST"});

        let {load1, load5, load15} = psutil.loadAvg();
        let mem = psutil.memVirtual();
        let cpu = psutil.cpuPercent(0, false);

        process.println(
            time,
            "Load1: "+load1.toFixed(2),
            "Load5: "+load5.toFixed(2),
            "Load15: "+load15.toFixed(2),
            "CPU: "+cpu[0].toFixed(2) +"%",
            "MEM: "+mem.usedPercent.toFixed(2)+"%",
        );
    })
}

// 05/02/2025, 21:05:50 Load1: 11.66 Load5: 5.84 Load15: 5.98 CPU: 15.67% MEM: 61.77
// 05/02/2025, 21:05:55 Load1: 10.72 Load5: 5.74 Load15: 5.95 CPU: 8.06% MEM: 62.18%
// 05/02/2025, 21:06:00 Load1: 9.87 Load5: 5.65 Load15: 5.91 CPU: 8.42% MEM: 61.93%

```
