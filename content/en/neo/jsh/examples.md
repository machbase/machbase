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
    const svr = new http.Server({
        network:'tcp',
        address:'127.0.0.1:56802',
    })
    // Route Handling
    svr.get("/hello/:name", ctx => {
        let name = ctx.param("name")
        // Defines a GET route that extracts the `name` parameter
        // from the URL and responds with a JSON object.
        ctx.JSON(http.status.OK, {
            "name": name,
            "message": "greetings",
        })
    })

    // Starts the server and logs the address it is listening on.
    svr.serve( evt => { 
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

### Unix Domain Socket

The Unix Domain Socket example demonstrates how to create an HTTP server that communicates using a Unix domain socket instead of a TCP/IP network socket.
This approach is useful for inter-process communication (IPC) on the same machine.

**Workflow:**

1. *Unix Domain Socket* Communication:
    - Uses a file-based socket (/tmp/service.sock) for local communication.
2. Efficient IPC:
    - Ideal for scenarios where processes on the same machine need to communicate without network overhead.
3. Compatibility with Tools:
    - Supports tools like curl for testing and interacting with the server.

```js {linenos=table,linenostart=1,hl_lines=[4,5]}
const http = require("@jsh/http");

const svr = new http.Server({
    network: "unix",
    address: "/tmp/service.sock",
});
svr.get("/hello/:name", (ctx) => {
    const name = ctx.param("name");
    ctx.JSON(http.status.OK, { message: `Hello, ${name}!` });
});
svr.serve();
```

Use curl to send a request to the server via the Unix domain socket:

```sh
curl -o - --unix-socket /tmp/service.sock http://localhost/hello/Karl
```

### Static Content

```js {linenos=table,linenostart=1}
svr.staticFile("/readme", "/path/to/file.txt");
svr.static("/static", "/path/to/static_dir");
```

### Redirect

```js {linenos=table,linenostart=1}
svr.get("/readme", ctx => {
    ctx.redirect(http.status.Found, "/docs/readme.html");
});
```

### RESTful API

```js {linenos=table,linenostart=1}
svr.get("/movies", ctx => {
    list = [
        {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
        {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
    ]
    ctx.JSON(http.status.OK, list);
})
svr.post("/movies", ctx => {
    obj = ctx.request.body;
    console.log("post:", JSON.stringify(obj));
    ctx.JSON(http.status.Created, {success: true});
});
svr.delete("/movies/:id", ctx => {
    let id = ctx.param("id");
    console.log("delete:", id)
    ctx.TEXT(http.status.NoContent, "Deleted.")
})
```

- GET
```sh
curl -o - http://127.0.0.1:56802/movies
```
```json
[
  { "id": 59793, "studio": [ "Paramount" ], "title": "Indiana Jones" },
  { "id": 64821, "studio": [ "Lucasfilm" ], "title": "Star Wars" }
]
```

- POST

```sh
curl -o - -X POST http://127.0.0.1:56802/movies \
    -H "Content-Type: application/json" \
    -d '{"title":"new movie", "id":12345, "studio":["Unknown"]}'
```

- DELETE

```sh
curl -v -o - -X DELETE http://127.0.0.1:56802/movies/12345
```

```sh
< HTTP/1.1 204 No Content
< Content-Type: text/plain; charset=utf-8
< Date: Thu, 08 May 2025 20:39:34 GMT
<
```

### HTML Templates

This line enables the server to load all HTML template files matching the `/*.html` pattern.
These templates allow the server to dynamically generate HTML responses by combining predefined layouts with data provided during runtime.

```js
svr.loadHTMLGlob("/*.html")

// Defines a GET route /movielist that serves an HTML page.
svr.get("/movielist", ctx => {
    obj = {
        subject: "Movie List",
        list: [
            {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
            {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
        ]
    }
    ctx.HTML(http.status.OK, "movie_list.html", obj)
})
```

- HTML Template Code `movie_list.html`

```html
<html>
    <body>
        <h1>{{.subject}}</h1>
        <ol>
        {{range .list }}
            <li> {{.id}} {{.title}} {{.studio}}
        {{end}}
        </ol>
    </body>
</html>
```

Sends a GET request to the `/movielist` endpoint.
The server responds with an HTML page generated using the `movie_list.html` template and the `obj` data.

```sh
curl -o - http://127.0.0.1:56802/movielist
```

```html
<html>
    <body>
        <h1>Movie List</h1>
        <ol>
            <li> 59793 Indiana Jones [Paramount]
            <li> 64821 Star Wars [Lucasfilm]
        </ol>
    </body>
</html>
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
    // Parses the response body as JSON 
    // and logs the `message` and `name` fields.
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

### Unix Domain Socket

Use `{unix: "/path/to/unix_domain_socket/file"}` option to connect server using the unix domain socket.

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    req = http.request("http://localhost/movies", {unix:"/tmp/test.sock"})
    req.do((rsp) => {
        obj = rsp.json();
        println(JSON.stringify(obj))
    })
} catch (e) {
    println(e.toString());
}
```

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

## System Monitoring

### Data Collector

The System Monitoring example demonstrates how to create a lightweight system monitoring tool using the `@jsh/process` and `@jsh/psutil` modules.
This script runs as a background daemon and periodically collects key system metrics, such as CPU usage, memory utilization, and load averages over the past 1, 5, and 15 minutes.

The monitoring task is scheduled to execute every 15 seconds using a cron-like syntax.
The collected data is formatted and printed with timestamps, providing a clear snapshot of the system's performance at regular intervals.
This example showcases how to leverage JavaScript for efficient process management and real-time system monitoring.

Save the example code as `sysmon.js` and execute it through the `JSH` terminal.
It will store system load averages, CPU usage, and memory utilization percentages into the database table named "EXAMPLE".

```sh
jsh / > sysmon
jsh / > ps
┌──────┬──────┬──────┬─────────────────┬──────────┐ 
│  PID │ PPID │ USER │ NAME            │ UPTIME   │ 
├──────┼──────┼──────┼─────────────────┼──────────┤ 
│ 1040 │ 1    │ sys  │ /sysmon.js      │ 2h37m43s │ 
│ 1042 │ 1025 │ sys  │ ps              │ 0s       │ 
└──────┴──────┴──────┴─────────────────┴──────────┘ 
```

- sysmon.js

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
const psutil = require("@jsh/psutil");
const db = require("@jsh/db");
const system = require("@jsh/system");

const tableName = "EXAMPLE";
const tagPrefix = "sys_";

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
  // The callback function receives a UNIX epoch (tick) in milliseconds
  // for when the task is executed
  process.schedule("0,15,30,45 * * * * *", (tick) => {
    // Retrieves the system's load averages for the past 1, 5, and 15 minutes.
    // The values are destructured into load1, load5, and load15.
    let {load1, load5, load15} = psutil.loadAvg();
    // Retrieves information about virtual memory usage,
    // including total, used, and free memory.
    let mem = psutil.memVirtual();
    // Calculates the CPU usage percentage since the last call.
    // The first argument (0) specifies the interval in seconds,
    // if it is 0 like this example, it calculates from the previous call.
    // the second argument (false) disables per-CPU statistics.
    let cpu = psutil.cpuPercent(0, false);
    // Convert current time from milliseconds UNIX epoch to native time.
    let ts = system.parseTime(tick, "ms")
    try{
      client = new db.Client({lowerCaseColumns:true});
      conn = client.connect();
      appender = conn.appender(tableName, "name","time","value");
      appender.append(tagPrefix+"load1", ts, load1);
      appender.append(tagPrefix+"load5", ts, load5);
      appender.append(tagPrefix+"load15", ts, load15);
      appender.append(tagPrefix+"cpu", ts, cpu[0]);
      appender.append(tagPrefix+"mem", ts, mem.usedPercent);
    } finally {
      appender.close();
      conn.close();
    }
  })
}
```

### Chart TQL

Since the system usage data is stored in the database, querying and visualizing it becomes straightforward.

```js {linenos=table,linenostart=1}
SQL(`select time, value from EXAMPLE
    where name = ? and time between ? and ?`, 
    "sys_load1", time("now -12000s"), time("now"))
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    size("500px", "300px"),
    chartJSCode({
        function yformatter(val, idx){ return val.toFixed(1) }
    }),
    chartOption({
        animation: false,
        yAxis: { type: "value", axisLabel:{ formatter: yformatter }},
        xAxis: { type: "time", axisLabel:{ rotate: -90 }},
        series: [
            {type: "line", data: column(0), name: "LOAD1", symbol:"none"},
        ],
        tooltip: {trigger: "axis", valueFormatter: yformatter},
        legend: {}
    })
)
```

{{< figure src="../img/sysmon-tql.jpg" width="538">}}

### Chart TQL with SCRIPT()

```js {linenos=table,linenostart=1}
SCRIPT({
    const db = require("@jsh/db");
    const client = new db.Client();
    const tags = [ "load1", "load5", "load15" ];
    const end = (new Date()).getTime();
    const begin = end - 240*(60*1000);
    var result = {};
    try {
        conn = client.connect();
        for(tag of tags) {
            rows = conn.query(`
                select time, value from example
                where name = 'sys_${tag}'
                and time between ${begin}000000 and ${end}000000`);
            lst = [];
            for( r of rows ) lst.push([r.time, r.value]);
            if(rows) rows.close();
            result[tag] = lst;
        }
    } catch(e) {
        console.log(e.message);
    } finally {
        if(conn) conn.close();
    }
    $.yield({
      animation: false,
      yAxis: { type: "value", axisLabel:{ }},
      xAxis: { type: "time", axisLabel:{ rotate: -90 }},
      series: [
        {type:"line", data:result.load1, name:"LOAD1", symbol:"none", smooth:true},
        {type:"line", data:result.load5, name:"LOAD5", symbol:"none", smooth:true},
        {type:"line", data:result.load15, name:"LOAD15", symbol:"none", smooth:true},
      ],
      tooltip: {trigger: "axis"},
      legend: {}
    });
})
CHART( size("500px", "300px") )
```

{{< figure src="../img/sysmon-tql-js.jpg" width="500">}}

### Chart TQL in HTML

Save the following HTML code as `sysmon.html` and open it in a web browser to visualize the system monitoring data.

- sysmon.html

```html {linenos=table,linenostart=1}
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>System Monitoring Chart</title>
  <script src="/web/echarts/echarts.min.js"></script>
  <script>
    function loadJS(url) {
      var scriptElement = document.createElement('script');
      scriptElement.src = url;
      document.getElementsByTagName('body')[0].appendChild(scriptElement);
      }
    function buildTQL(table, tag, begin, end, format) {
      return `
      SQL("select time, value from ${table} "+
        "where name = '${tag}' "+
        "and time between ${begin}000000 and ${end}000000")
      MAPVALUE(1, list(value(0), value(1)))
      CHART(
        size("400px", "200px"),
        chartJSCode({
            function unitFormat(val){
                return val.toFixed(1);
            }
            function percentFormat(val) {
                return ""+val.toFixed(0)+"%";
            }
        }),
        chartOption({
            animation: false,
            yAxis: { type: "value", axisLabel:{ formatter:${format} }},
            xAxis: { type: "time", axisLabel:{ rotate: -90 }},
            series: [
              {type:"line", data:column(1), name:"${tag}", symbol:"none"},
            ],
            tooltip: {trigger: "axis", valueFormatter:${format} },
            legend: {}
        })
      )`
    }
    function loadChart(containerID, table, tag, begin, end, format) {
      fetch('/db/tql',
        {method:"POST", body: buildTQL(table, tag, begin, end, format)}
      )
      .then(response => {
        return response.json()
      })
      .then(obj => {
        const container = document.getElementById(containerID)
        const chartDiv = document.createElement('div')
        chartDiv.setAttribute("id", obj.chartID)
        chartDiv.style.width = obj.style.width
        chartDiv.style.height = obj.style.height
        container.appendChild(chartDiv)
        obj.jsCodeAssets.forEach((js) => loadJS(js))
      })
      .catch(error => {
        console.error('Error fetching chart data:', error);
      });
    }
   </script>
</head>
<body>
  <div style='display:flex;float:left;flex-flow:row wrap'>
    <div id="chart1" style="width: 400px; height: 200px;"></div>
    <div id="chart2" style="width: 400px; height: 200px;"></div>
    <div id="chart3" style="width: 400px; height: 200px;"></div>
    <div id="chart4" style="width: 400px; height: 200px;"></div>
  </div>
  <script>
    let end = (new Date()).getTime(); // now in millisec.
    let begin = end - 30*(60*1000);   // 30 minutes before
    loadChart('chart1', "EXAMPLE", "sys_load1", begin, end, "unitFormat")
    loadChart('chart2', "EXAMPLE", "sys_load5", begin, end, "unitFormat")
    loadChart('chart3', "EXAMPLE", "sys_cpu", begin, end, "percentFormat")
    loadChart('chart4', "EXAMPLE", "sys_mem", begin, end, "percentFormat")
  </script>
</body>
</html>
```

{{< figure src="../img/sysmon-html.jpg" width="600">}}

### Chart in HTML Template

This example demonstrates how to create an HTTP server route (`/sysmon`) that serves an HTML page containing a chart.
The server fetches system monitoring data (e.g., load averages) from a database
and dynamically generates the chart using the ECharts library.
The HTML template (`http-sysmon.html`) is populated with the retrieved data,
allowing for real-time visualization of system metrics such as `load1`, `load5`, and `load15`.
This approach showcases how to integrate server-side data processing with client-side chart rendering for effective data visualization.

- `sysmon-server.js`
```js {linenos=table,linenostart=1,hl_lines=[18,41]}
const process = require("@jsh/process");
const http = require("@jsh/http")
const db = require("@jsh/db")

if( process.ppid() == 1 ) {
    try {
        runServer();
    }catch(e) {
        console.log("server error", e)
    }
} else {
    process.daemonize({reload:true});
}

function runServer() {
    const tags = [ "load1", "load5", "load15", "cpu", "mem" ];
    const svr = new http.Server({address:'127.0.0.1:56802'})
    svr.loadHTMLGlob("/*.html")
    svr.get("/sysmon", ctx => {
        const end = (new Date()).getTime();
        const begin = end - 20*(60*1000); // last 20 min.
        var result = {};
        try {
            client = new db.Client();
            conn = client.connect();
            for( tag of tags ) {
                rows = conn.query(`
                    select time, value from example
                    where name = 'sys_${tag}'
                    and time between ${begin}000000 and ${end}000000`)
                lst = [];
                for( r of rows ) lst.push([r.time, r.value]);
                if(rows) rows.close();
                result[tag] = lst;
            }
        } catch(e) {
            console.log(e);
        } finally {
            if (conn) conn.close();
        }
        ctx.HTML(http.status.OK, "http-sysmon.html", result)
    })
    svr.serve( (result)=>{ 
        console.log("server started", "http://"+result.address) ;
    });
}
```

- `http-sysmon.html`

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
</head>
<body>
<div style='display:flex;float:left;flex-flow:row wrap;width:100%;'>
    <div id="load" style="width:400px;height:300px;margin:4px;"></div>
    <div id="cpu" style="width:400px;height:300px;margin:4px;"></div>
    <div id="mem" style="width:400px;height:300px;margin:4px;"></div>
</div>
<script>
    function doChart(element, title, data) {
        let chart = echarts.init(element, "dark");
        chart.setOption({
            animation:false, "color":["#80FFA5", "#00DDFF", "#37A2FF"],
            title:{"text":title},
            legend:{ bottom: 7 }, tooltip:{"trigger":"axis"},
            xAxis:{type:"time", axisLabel:{ rotate: -90 }},
            yAxis:{type:"value"},
            series: data,
        });
    }
    doChart(document.getElementById('load'), "System Load Avg.", [
        { type:"line", name:"load1", symbol:"none", data:{{.load1}} },
        { type:"line", name:"load5", symbol:"none", data:{{.load5}} },
        { type:"line", name:"load15", symbol:"none", data:{{.load15}} },
    ])
    doChart(document.getElementById('cpu'), "CPU Usage", [
        { type:"line", name:"cpu usage", symbol:"none", data:{{.cpu}} },
    ])
    doChart(document.getElementById('mem'), "Memory Usage", [
        { type:"line", name:"mem usage", symbol:"none", data:{{.mem}} },
    ])
</script>
</body>
</html>
```

{{< figure src="../img/sysmon-template.jpg" width="600">}}

## OPCUA Client

The OPCUA Client example demonstrates how to create a data collector that connects to an OPC UA server, retrieves system metrics, and stores them in a database for further analysis and visualization. 

**Workflow:**

1. OPC UA Integration:
    - Connects to an OPC UA server using the `@jsh/opcua` module to read data.
    - The script connects to an OPC UA server at `opc.tcp://localhost:4840`.
    - It reads specific nodes (e.g., `cpu_percent`, `mem_percent`, `load1`, etc.) to retrieve system metrics.
2. Scheduled Data Collection:
    - Uses a cron-like schedule to periodically fetch data from the OPC UA server.
    - The script schedules a task to run every 10 seconds using `process.schedule`.
    - At each interval, it reads the values of the specified nodes and stores them in the database.
3. Database Storage:
    - Stores the collected data in a database table (`EXAMPLE`) for persistence and analysis.
    - The collected data is inserted into the `EXAMPLE` table with columns for `name`, `time`, and `value`.
4. Data Visualization:
    - The collected data can be visualized using the chart examples provided in the *System Monitoring* example.
    - The stored data can be visualized using the chart examples from the *System Monitoring* example. For instance, you can use the provided TQL or HTML chart examples to display metrics like CPU usage, memory utilization, and load averages.

### Data Collector

Save the script as opcua-client.js and run it in the background using the JSH terminal:

```
jsh / > opcua-client
jsh / > ps
┌──────┬──────┬──────┬──────────────────┬────────┐ 
│  PID │ PPID │ USER │ NAME             │ UPTIME │ 
├──────┼──────┼──────┼──────────────────┼────────┤ 
│ 1044 │ 1    │ sys  │ /opcua-client.js │ 13s    │ 
│ 1045 │ 1025 │ sys  │ ps               │ 0s     │ 
└──────┴──────┴──────┴──────────────────┴────────┘ 
```

- opcua-client.js

```js {linenos=table,linenostart=1}
opcua = require("@jsh/opcua");
process = require("@jsh/process");
system = require("@jsh/system");
db = require("@jsh/db");

if( process.ppid() == 1 ) {
  runClient();
} else {
  process.daemonize();
}

function runClient() {
  const nodes = [
    "ns=1;s=cpu_percent",
    "ns=1;s=mem_percent",
    "ns=1;s=load1",
    "ns=1;s=load5",
    "ns=1;s=load15",
  ];
  const tags = [
    "sys_cpu", "sys_mem", "sys_load1", "sys_load5", "sys_load15"
  ];
  const tableName = "EXAMPLE";
  try {
    uaClient = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
    dbClient = new db.Client({lowerCaseColumns:true});
    conn = dbClient.connect();
    
    process.schedule("0,10,20,30,40,50 * * * * *", tick => {
      ts = system.parseTime(tick, "ms")
      vs = uaClient.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
      });
      sqlText = `INSERT INTO ${tableName} (name,time,value) values(?,?,?)`
      vs.forEach((v, idx) => {
        if( v.value !== null ) {
            conn.exec(sqlText, tags[idx], ts, v.value);
        }
      })
    })
  } catch (e) {
    process.println("Error:", e.message);
  } finally {
    conn.close();
    uaClient.close();
  }
}
```
