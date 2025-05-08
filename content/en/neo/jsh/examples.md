---
title: Examples
type: docs
weight: 1
---

## HTTP Server

This example demonstrates how to create a simple HTTP server using the `@jsh/http` module.
The server listens on a specified address and port (`127.0.0.1:56802`)
and provides a RESTful API endpoint (`/hello/:name`).
When a client sends a GET request to this endpoint with a name parameter,
the server responds with a JSON object containing a greeting message and the provided name.

This example is ideal for learning how to build lightweight HTTP servers with dynamic routing and JSON responses in JavaScript.

<h6>Key Features:</h6>

1. **Daemonization**: The script checks if it is running as a daemon using `process.ppid()`. If not, it daemonizes itself using `process.daemonize()` to run in the background.
2. **Routing**: The server uses a route (`/hello/:name`) to extract the `name` parameter from the URL.
3. **JSON Response**: The server responds with a JSON object containing the `name` and a greeting message.

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
const {println} = require("@jsh/process");
const http = require("@jsh/http")

// This ensures the server runs as a background process.
if( process.ppid() == 1 ) {
    runServer();
} else {
    process.daemonize();
}

function runServer() {
    // Creates an HTTP server bound to the specified address and port.
    const svr = new http.Server({network:'tcp', address:'127.0.0.1:56802'})
    // Route Handling
    svr.get("/hello/:name", (ctx) => {
        let name = ctx.param("name")
        // Defines a GET route that extracts the `name` parameter
        // from the URL and responds with a JSON object.
        ctx.JSON(http.status.OK, {
            "name": name,
            "message": "greetings",
        })
    })

    // Starts the server and logs the address it is listening on.
    svr.listen( (evt)=>{ 
        println("server started", "http://"+evt.address) ;
    });
}
```

<h6>Usage:</h6>

1. Run the script to start the server.
2. Use a tool like `curl` to send a GET request to the server:

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

The server will respond with:

```json
{"message":"greetings","name":"Karl"}
```

## HTTP Client

This example demonstrates how to create an HTTP client using the `@jsh/http` module.
The client sends a GET request to a specified URL  and processes the server's response.
It showcases how to handle HTTP requests and parse JSON responses in JavaScript.

This example is ideal for learning how to build HTTP clients in JavaScript, handle responses, and parse JSON data.

<h6>Key Features:</h6>

1. **Request Handling**: The client sends an HTTP GET request to the server.
2. **Response Parsing**: The response is parsed to extract details such as status, headers, and body content.
3. **Error Handling**: The example includes a `try-catch` block to handle potential errors during the request.

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    // Creates an HTTP GET request to the specified URL.
    req = http.request("http://127.0.0.1:56802/hello/Steve")
    // Logs the URL, status, and headers.
    //  Parses the response body as JSON and logs the `message` and `name` fields.
    req.do((rsp) => {
        // url: http://127.0.0.1:56802/hello/Steve
        println("url:", rsp.url);
        // error: <nil>
        println("error:", rsp.error());
        // status: 200
        println("status:", rsp.status);
        // statusText: 200 OK
        println("statusText:", rsp.statusText);
        // content-type: application/json; charset=utf-8
        println("content-type:", rsp.headers["Content-Type"]);
        obj = rsp.json(); // parse content body to JSON object
        // greetings, Steve
        println("body:", `${obj.message}, ${obj.name}`);
    })
} catch (e) {
    // Catches and logs any errors that occur during the request.
    println(e);
}
```

<h6>Usage:</h6>

1. Ensure the HTTP server is running (refer to the HTTP Server example).
2. Run the script to send a GET request to the server.

## MQTT Subscriber

The MQTT Subscriber example demonstrates how to create a background application that connects to an MQTT broker, subscribes to a specific topic, and processes incoming messages.
Using the `@jsh/process` and `@jsh/mqtt` modules, the script runs as a daemon, ensuring it operates in the background.
It handles events such as connection establishment, message reception, and disconnection, showcasing how to build a robust and efficient MQTT client in JavaScript.
This example is ideal for scenarios requiring real-time message processing and lightweight background operations.

- Create an application as `mqtt-sub.js`.

```js {linenos=table,linenostart=1}
// This script creates a background MQTT subscriber that connects to a broker,
// subscribes to a topic (test/topic), and processes incoming messages.
// It demonstrates how to handle connection events, errors,
// and message reception efficiently using JavaScript.
//
// Provides utilities for process management,
// such as daemonizing and printing.
const process = require("@jsh/process");
const println = process.println;
// Provides MQTT client functionality for connecting to brokers
// and handling messages.
const mqtt = require("@jsh/mqtt");

// Checks the parent process ID.
// If it equals 1, the process is already running as a daemon.
if( process.ppid() == 1 ) {
    // If the process is a daemon, it calls runBackground() to start
    // the MQTT subscriber logic.
    console.log("mqtt-sub start...")
    runBackground();
    console.log("mqtt-sub terminated.")
} else {
    // If the process is not a daemon, process.daemonize() is called to
    // restart the process as a background daemon.
    process.daemonize();
}

// Defines the main function for the MQTT subscriber logic.
function runBackground() {
    // A variable to hold the MQTT client instance.
    var client;
    // Specifies the topic (test/topic) to which the subscriber will listen.
    var testTopic = "test/topic";
    client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:5653"],
        keepAlive: 30,
        cleanStart: true,
        onConnect: (ack) => {
            // Triggered when the client successfully connects to the broker.
            // It subscribes to the test/topic with QoS level 0.
            println("connected.");
            println("subscribe to", testTopic);
            client.subscribe({subscriptions:[{topic:testTopic, qos:0}]});
        },
        onConnectError: (err) => {
            // Triggered if there is an error during connection.
            println("connect error", err);
        },
        onDisconnect: (disconn) => {
            // Triggered when the client disconnects from the broker.
            println("disconnected.");
        },
        onMessage: (msg) => {
            // Triggered when a message is received.
            // It logs the topic, QoS, and payload of the message.
            println("recv topic:", msg.topic,
                "QoS:", msg.qos,
                "payload:", msg.payload.string())
        },
    });
    try {
        // Initiates the connection to the MQTT broker.
        client.connect();
        // Keeps the process running indefinitely,
        // allowing the subscriber to listen for messages.
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

The System Monitoring example demonstrates how to create a lightweight system monitoring tool using the `@jsh/process` and `@jsh/psutil` modules.
This script runs as a background daemon and periodically collects key system metrics, such as CPU usage, memory utilization, and load averages over the past 1, 5, and 15 minutes.
The monitoring task is scheduled to execute every 15 seconds using a cron-like syntax.
The collected data is formatted and printed with timestamps, providing a clear snapshot of the system's performance at regular intervals.
This example showcases how to leverage JavaScript for efficient process management and real-time system monitoring.

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
const psutil = require("@jsh/psutil");

// Checks the parent process ID. If it equals 1,
// the process is already running as a daemon.
if( process.ppid() == 1 ) {
    // If it is already a daemon,
    // the `runSysmon()` function is executed to start
    // system monitoring.
    runSysmon();
} else {
    // If the process is not a daemon,
    // `process.daemonize()` is called to restart the process
    // as a background daemon.
    process.daemonize();
}

function runSysmon() {
    // Schedules a task to run at specific intervals.
    // Here, it runs every 15 seconds (0,15,30,45 in the cron-like syntax).
    // The callback function receives a UNIX epoch timestamp (ts) in milliseconds
    // for when the task is executed
    process.schedule("0,15,30,45 * * * * *", (ts) => {
        // Retrieves the system's load averages for the past 1, 5, and 15 minutes.
        // The values are destructured into load1, load5, and load15.
        let {load1, load5, load15} = psutil.loadAvg();
        // Retrieves information about virtual memory usage, including total, used, and free memory.
        let mem = psutil.memVirtual();
        // Calculates the CPU usage percentage since the last call.
        // The first argument (0) specifies the interval in seconds,
        // if it is 0 like this example, it calculates from the previous call.
        // the second argument (false) disables per-CPU statistics.
        let cpu = psutil.cpuPercent(0, false);

        process.println(
            new Date(ts).toLocaleString("en-US"),
            "Load1: "+load1.toFixed(2),
            "Load5: "+load5.toFixed(2),
            "Load15: "+load15.toFixed(2),
            "CPU: "+cpu[0].toFixed(2) +"%",
            "MEM: "+mem.usedPercent.toFixed(2)+"%",
        );
    })
}

// The output shows the timestamp, load averages, CPU usage,
// and memory usage at each scheduled interval.
//
// 05/03/2025, 10:22:00 Load1: 1.81 Load5: 2.52 Load15: 2.77 CPU: 7.45% MEM: 62.42%
// 05/03/2025, 10:22:15 Load1: 1.78 Load5: 2.48 Load15: 2.75 CPU: 3.75% MEM: 62.41%
// 05/03/2025, 10:22:30 Load1: 2.22 Load5: 2.55 Load15: 2.77 CPU: 5.40% MEM: 62.30%
// 05/03/2025, 10:22:45 Load1: 1.86 Load5: 2.46 Load15: 2.73 CPU: 4.94% MEM: 62.39%
// 05/03/2025, 10:23:00 Load1: 1.81 Load5: 2.42 Load15: 2.71 CPU: 5.32% MEM: 62.41%

```

## Machbase Client

This example demonstrates how to connect to another Machbase instance via port 5656 and execute a query.

Set `lowerCaseColumns: true` at line 8 to ensure that the query results use lower-cased property names in the record object, as demonstrated at line 21.

`sourceSource` supports two formats for historical reasons: the first uses a semi-colon delimiter, while the second uses a space delimiter. Both are equivalent.

1. Classic Format: `SERVER=${host};PORT_NO=${port};UID=${user};PWD=${pass}`
2. Name=Value Format: `host=<ip> port=<port> user=<username> password=<pass>`


```js {linenos=table,linenostart=1,hl_lines=[8,21]}
db = require("@jsh/db");
host = "192.168.0.207"
port = 5656
user = "sys"
pass = "manager"
client = db.Client({
    driver: "machbase",
    dataSource: `host=${host} port=${port} user=${user} password=${pass}`,
    lowerCaseColumns: true
})

try {
    sqlText = "select * from example where name = ? limit ?,?";
    tag = "my-car";
    off = 10;
    limit = 5;

    conn = client.connect()
    rows = conn.query(sqlText, tag, off, limit)
    for( rec of rows) {
        console.log(rec.name, rec.time, rec.value)
    }
} catch(e) {
    console.error(e.message)
} finally {
    rows.close()
    conn.close()
}
```

## Machbase Append

```js {linenos=table,linenostart=1,hl_lines=[10,16]}
const db = require("@jsh/db");
const { now, parseTime } = require("@jsh/system");

client = new db.Client({lowerCaseColumns:true});
var conn = null;
var appender = null;
try{
    console.log("supportAppend:", client.supportAppend);
    conn = client.connect();
    appender = conn.appender("example", "name", "time", "value");
    let ts = (new Date()).getTime(); // unix epoch (ms.)
    for (let i = 0; i < 100; i++) {
        // add 10 millisec.
        ts = ts + 10;
        // name, time, value
        appender.append("tag-append", parseTime(ts, "ms"), i);
    }
} catch(e) {
    console.log("Error:", e);
} finally {
    if (appender) appender.close();
    if (conn) conn.close();
}
console.log("append:", appender.result());

// supportAppend: true
// append: {success:100, fail:0}
```

## SQLite

This example demonstrates how to use the `@jsh/db` module to interact with an in-memory SQLite database.
It covers creating a table, inserting data, and querying the database.
This example is ideal for learning how to perform basic database operations in JavaScript using SQLite.

```js {linenos=table,linenostart=1,hl_lines=[6]}
const db = require("@jsh/db");

// Intializes a new SQLite client with an in-memory database.
client = new db.Client({
    driver:"sqlite",
    dataSource:"file::memory:?cache=shared"
});

try{
    conn = client.connect()
    // Creates a table named `mem_example`
    // with three columns: `id`, `company`, and `employee`.
    conn.exec(`
        CREATE TABLE IF NOT EXISTS mem_example(
            id         INTEGER NOT NULL PRIMARY KEY,
            company    TEXT,
            employee   INTEGER
        )
    `);

    // Inserts a record into the `mem_example` table with the values
    // `'Fedel-Gaylord'` for `company` and `12` for `employee`.
    conn.exec(`INSERT INTO mem_example(company, employee) values(?, ?);`, 
        'Fedel-Gaylord', 12);

    // Queries all rows from the `mem_example` table and logs the results to the console.
    rows = conn.query(`select * from mem_example`);
    for( rec of rows ) {
        console.log(...rec)
    }
}catch(e){
    // Handles any errors that occur during database operations 
    console.error(e.message);
}finally{
    // Ensures that the `rows` and `conn` objects are closed to release resources.
    rows.close();
    conn.close();
}
```

When the script is run, it outputs the inserted record:
```plaintext
1 Fedel-Gaylord 12
```
