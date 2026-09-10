---
toc: true
title: サンプル（作成中）
type: docs
weight: 1
draft: true
---

### Unixドメインソケット {#유닉스-도메인-소켓}

Unixドメインソケットに接続するには、`{unix: "/path/to/unix_domain_socket/file"}`オプションを使用します。

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

## MQTTパブリッシャー {#mqtt-퍼블리셔}

以下のコードは、MQTTブローカーに定期的にメッセージを発行する例です。
- `mqtt.js`を作成し、以下のコードを保存してください。

```js {linenos=table,linenostart=1}
const mqtt = require("@jsh/mqtt");
const process = require("@jsh/process");
const system = require("@jsh/system")

const log = new system.Log("mqtt-demo");
const testTopic = "test/string";

var client = new mqtt.Client({
    serverUrls: ["tcp://127.0.0.1:5653"],
});

try {
    client.onConnectError = err => { log.error("connect error", err); }
    client.onClientError = err => { log.error("client error", err); }
    client.onConnect = (ack) => { log.info("client connected"); }

    client.connect({timeout: 3*1000});
    
    for(i = 0; i < 10; i++) {
        process.sleep(1000);
        r = client.publish({topic: testTopic, qos: 1}, 'Hello World:'+i)
    }
} catch (e) {
    log.error("Error:", e.message);
} finally {
    client.disconnect({waitForEmptyQueue:true})
}
```

## MQTTサブスクライバー {#mqtt-구독자}

この例は、MQTTブローカーに接続して特定のトピックを購読し、受信メッセージを処理するバックグラウンドアプリケーションの実装方法を示します。
`@jsh/process`と`@jsh/mqtt`モジュールでデーモンとして実行し、接続の確立、メッセージ受信、切断などのイベントを処理します。
リアルタイムのメッセージ処理や軽量なバックグラウンド処理に適した方式です。

- `mqtt-sub.js`を作成し、以下のコードを保存してください。

```js {linenos=table,linenostart=1}
// このスクリプトは、MQTTブローカーに接続してトピックtest/topicを購読し、
// 受信メッセージを処理するバックグラウンドのサブスクライバーを作成します。
// 接続イベント、エラー、メッセージ受信をJavaScriptで扱う方法を示します。
//
// @jsh/processは、デーモン化や出力などのプロセス管理ユーティリティを提供します。
const process = require("@jsh/process");
const system = require("@jsh/system")
const log = new system.Log("mqtt-demo");
// @jsh/mqttは、ブローカーへの接続とメッセージ処理用のクライアントを提供します。
const mqtt = require("@jsh/mqtt");

// 親プロセスIDを確認し、デーモンとして実行しているかを判定します。
if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
    // デーモンの場合は、runBackground()で購読処理を実行します。
    log.info("mqtt-sub start...");
    runBackground();
    log.info("mqtt-sub terminated.");
} else {
    // デーモンでなければ、process.daemonize()でバックグラウンドプロセスに移行します。
    process.daemonize();
}

// MQTTの購読処理を行うメイン関数を定義します。
function runBackground() {
    var client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:5653"],
    });
    try {
        // 接続中にエラーが発生すると呼び出されます。
        client.onConnectError = err => { log.warn("connect error", err); }
        // ブローカーとの接続が切れると呼び出されます。
        client.onDisconnect = () => { log.info("disconnected."); }
        var count = 0;
        client.onConnect = ack => {
            log.info("connected.", ack.reasonCode);
            // QoS 2でtest/topicを購読します。
            r = client.subscribe({subscriptions:[{topic:'test/topic', qos: 2}]})
            log.info("subscribe", 'test/topic', "result", r);
            client.onMessage = msg => {
                // メッセージを受信すると、トピック、QoS、ペイロードを記録します。
                log.info("recv topic:", msg.topic,"payload:", msg.payload.string())
                count++;
                return true;
            }
        }

        // MQTTブローカーへの接続を試みます。
        client.connect({timeout: 3*1000});

        // トピックにテストメッセージを発行します。
        for( let i = 0; i < 10; i++) {
            client.publish({topic:'test/topic', qos: 1}, "test num="+i);
        }
        // すべてのメッセージを受信するまで待ちます。
        while(true) {
            if(count >= 10) break;
            process.sleep(100);
        }
        // 購読解除
        client.unsubscribe({topics:['test/topic']})
        // 切断
        client.disconnect({waitForEmptyQueue:true})
    } catch (e) {
        log.error("Error", e.message);
    }
}
```

- JSHで`mqtt-sub.js`を実行してください。

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

- `mosquitto_pub`などのMQTTクライアントでメッセージを送信してください。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t test/topic -m 'hello?'
```

`mqtt-sub.js`アプリケーションは、購読によって発行されたメッセージを受信します。

```
2025/05/02 09:56:18.381 INFO  /sbin/mqtt-sub.js mqtt-sub start...
2025/05/02 09:56:18.382 INFO  /sbin/mqtt-sub.js connected.
2025/05/02 09:56:18.383 INFO  /sbin/mqtt-sub.js subscribe to test/topic
2025/05/02 09:56:26.149 INFO  /sbin/mqtt-sub.js recv topic: test/topic QoS: 0 payload: hello?
```

- `kill <pid>`コマンドで、バックグラウンドプロセス`mqtt-sub.js`を終了できます。

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

## Machbaseクライアント {#machbase-클라이언트}

この例は、ポート5656で別のMachbaseインスタンスに接続し、クエリを実行する方法を示します。

8行目で`lowerCaseColumns: true`を設定すると、21行目のように結果レコードのプロパティ名が小文字に正規化されます。

`dataSource`は、以下の2つの形式に対応しています。

1. 従来の形式： `SERVER=${host};PORT_NO=${port};UID=${user};PWD=${pass}`
2. 名前=値の形式： `host=<ip> port=<port> user=<username> password=<pass>`


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

## Machbase Append {#machbase-append}

以下のコードは、Machbaseテーブルにデータを一括追加する方法を示します。

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
    let ts = (new Date()).getTime(); // Unixエポック時刻（ms）
    for (let i = 0; i < 100; i++) {
        // 10ミリ秒ずつ増やします。
        ts = ts + 10;
        // name、time、valueの順に入力します。
        appender.append("tag-append", parseTime(ts, "ms"), i);
    }
} catch(e) {
    console.log("Error:", e);
} finally {
    if (appender) appender.close();
    if (conn) conn.close();
}
console.log("append:", appender.result());

// 出力例
// supportAppend: true
// append: {success:100, fail:0}
```

## SQLiteクライアント {#sqlite-클라이언트}

この例は、`@jsh/db`モジュールでメモリ上のSQLiteデータベースを作成し、テーブルの作成、データ挿入、検索を行う方法を示します。

```js {linenos=table,linenostart=1,hl_lines=[6]}
const db = require("@jsh/db");

client = new db.Client({
    driver:"sqlite",
    dataSource:"file::memory:?cache=shared"
});

try{
    conn = client.connect()
    // mem_exampleテーブルを作成します。
    conn.exec(`
        CREATE TABLE IF NOT EXISTS mem_example(
            id         INTEGER NOT NULL PRIMARY KEY,
            company    TEXT,
            employee   INTEGER
        )
    `);

    conn.exec(`INSERT INTO mem_example(company, employee) values(?, ?);`, 
        'Fedel-Gaylord', 12);

    rows = conn.query(`select * from mem_example`);
    for( rec of rows ) {
        console.log(...rec)
    }
}catch(e){
    console.error(e.message);
}finally{
    rows.close();
    conn.close();
}
```

実行すると、挿入したレコードを以下のように出力します。
```plaintext
1 Fedel-Gaylord 12
```

## PostgreSQLクライアント {#postgresql-클라이언트}

PostgreSQLサーバーに接続し、テーブルを作成してデータを挿入・検索する例です。

```js {linenos=table,linenostart=1,hl_lines=[]}
const db = require("@jsh/db");
const { now, parseTime } = require("@jsh/system");

client = new db.Client({
    driver: "postgres",
    dataSource: "host=127.0.0.1 port=15455 dbname=db user=dbuser password=dbpass sslmode=disable",
    lowerCaseColumns:true,
});
var conn = null;
var rows = null;
try{
    conn = client.connect();
    r = conn.exec("CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT)");
    console.log("create table:", r.message);
    // create table: Created successfully.

    r = conn.exec("INSERT INTO test (name) VALUES ($1)", "foo")
    console.log("insert foo:", r.message, r.rowsAffected);
    // insert foo: a row inserted. 1

    r = conn.exec("INSERT INTO test (name) VALUES ($1)", "bar")
    console.log("insert bar:", r.message, r.rowsAffected);
    // insert bar: a row inserted. 1

    rows = conn.query("SELECT * FROM test ORDER BY id");
    console.log("cols.names:", JSON.stringify(rows.columnNames()));
    // cols.names: ["id","name"]

    for (const rec of rows) {
        console.log(...rec);
    }
    // 1 foo
    // 2 bar
} catch(e) {
    console.log("Error:", e.message);
} finally {
    if(rows) rows.close();
    if(conn) conn.close();
}
```

## システム監視 {#system-monitoring}

### データ収集プログラム {#데이터-수집기}

このシステム監視の例は、`@jsh/process`と`@jsh/psutil`モジュールで軽量な監視ツールを構成する方法を示します。
スクリプトはデーモンとして実行され、1分・5分・15分の平均負荷とCPU・メモリ使用率を定期的に収集します。

cronに似た構文で15秒ごとに処理を実行し、収集したデータをタイムスタンプとともに保存します。
JavaScriptでプロセスを管理し、リアルタイムメトリクスを取り込む例として利用できます。

コードを`sysmon.js`として保存し、JSHターミナルで実行してください。
システム負荷とCPU・メモリのメトリクスは、`EXAMPLE`テーブルに記録されます。

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

// PIDを確認し、デーモンとして実行しているかを判定します。
if( process.isDaemon() ) {
    // デーモンの場合は、監視を開始します。
    runSysmon();
} else {
    // そうでなければ、バックグラウンドのデーモンに移行します。
    process.daemonize({reload:true});
}

function runSysmon() {
  // 15秒間隔で処理を実行します。
  process.schedule("0,15,30,45 * * * * *", (tick) => {
    // 直近1分・5分・15分の平均負荷を取得します。
    let {load1, load5, load15} = psutil.loadAvg();
    // 仮想メモリの使用率を確認します。
    let mem = psutil.memVirtual();
    // 前回の呼び出し以降のCPU使用率を計算します。
    let cpu = psutil.cpuPercent(0, false);
    // タイムスタンプをネイティブの時刻オブジェクトに変換します。
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

### グラフ用TQL {#차트-tql}

収集したシステムメトリクスはデータベースに保存されるため、TQLで容易に検索・可視化できます。

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

{{< figure src="/neo/jsh/img/sysmon-tql.jpg" width="538">}}

### SCRIPT()を使ったグラフ用TQL {#script-활용-차트-tql}

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

{{< figure src="/neo/jsh/img/sysmon-tql-js.jpg" width="500">}}

### HTMLでのグラフ描画 {#html에서-차트-그리기}

以下のHTMLを`sysmon.html`として保存し、ブラウザーで開くと、収集したシステム監視データを可視化できます。

- sysmon.html

```html {linenos=table,linenostart=1}
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>システム監視グラフ</title>
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
    let end = (new Date()).getTime(); // 現在時刻（ミリ秒）
    let begin = end - 30*(60*1000);   // 30 minutes before
    loadChart('chart1', "EXAMPLE", "sys_load1", begin, end, "unitFormat")
    loadChart('chart2', "EXAMPLE", "sys_load5", begin, end, "unitFormat")
    loadChart('chart3', "EXAMPLE", "sys_cpu", begin, end, "percentFormat")
    loadChart('chart4', "EXAMPLE", "sys_mem", begin, end, "percentFormat")
  </script>
</body>
</html>
```

{{< figure src="/neo/jsh/img/sysmon-html.jpg" width="600">}}

### HTMLテンプレートのグラフ {#html-템플릿-차트}

この例は、`/sysmon`パスを提供するHTTPサーバーを構成し、テンプレートを使ったグラフを返す方法を示します。
サーバーは、データベースから負荷・CPU・メモリのメトリクスを取得し、EChartsテンプレート（`http-sysmon.html`）に渡してリアルタイムに可視化します。

- `sysmon-server.js`
```js {linenos=table,linenostart=1,hl_lines=[14,37]}
const process = require("@jsh/process");
const http = require("@jsh/http")
const db = require("@jsh/db")

if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
    runServer();
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
            client = new db.Client({lowerCaseColumns:true});
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

{{< figure src="/neo/jsh/img/sysmon-template.jpg" width="600">}}


## 統計 {#통계}

次のTQL例は、`@jsh/analysis`モジュールで数値配列の基本統計量を計算する方法を示します。
平均、中央値、分散、標準偏差を求め、`$.yield()`で返すと、CSVなどで容易に利用できます。


```js {linenos=table,linenostart=1}
SCRIPT({
    const system = require("@jsh/system");
    const ana = require("@jsh/analysis");
    xs = ana.sort([
		32.32, 56.98, 21.52, 44.32,
		55.63, 13.75, 43.47, 43.34,
		12.34,
    ]);
    $.yield("data", JSON.stringify(xs))

    mean = ana.mean(xs)
    variance = ana.variance(xs)
    stddev = Math.sqrt(variance)

    median = ana.quantile(0.5, xs)

    $.yield("mean", mean)
    $.yield("median", median)
    $.yield("variance", variance)
    $.yield("std-dev", stddev)
})
CSV()

// 出力例
// data     [12.34,13.75,21.52,32.32,43.34,43.47,44.32,55.63,56.98]
// mean     35.96333333333334
// median   43.34
// variance 285.306875
// std-dev  16.891029423927957
``` 
