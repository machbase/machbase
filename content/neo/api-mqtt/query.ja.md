---
toc: true
title: MQTTの検索
type: docs
weight: 20
---

MQTTでデータベースクエリを実行するには、`db/query`トピックにリクエストを送信します。サーバーは、`db/reply`トピック、またはリクエストの`reply`フィールドで指定したトピックに結果を返します。

## クエリJSON {#쿼리-json}

| パラメーター       | 既定値 | 説明                                           |
|:----------- |---------|:------------------------------------------------------|
| **q**       | _n/a_   | 実行するSQLクエリ文字列                                      |
| p           |         | 省略可能。SQLプレースホルダーに渡すバインドパラメーターです。<br/>- `?`の位置パラメーター（JSON配列）：`["name", 1234]` {{< neo_since ver="8.0.75" />}}<br/>- `:name`の名前付きパラメーター（JSONオブジェクト）：`{"name": "wave.sin", "n": 5}` {{< neo_since ver="8.7.0" />}} |
| db          |         | 省略可能。複数データベース環境で使用する対象データベース名です。 {{< neo_since ver="8.7.0" />}} |
| reply       | db/reply| クエリ結果を受信するトピック                                       |
| format      | json    | 結果形式：json、csv、box                               |
| timeformat  | ns      | 時刻の単位：s、ms、us、ns                                |
| tz          | UTC     | タイムゾーン：UTC、Local、地域指定                           |
| compress    | _圧縮なし_ | 圧縮方式：gzip                                  |
| rownum      | false   | 行番号を含めるかどうか：true、false                          |

**`format=json`で使用できる追加パラメーター** {{< neo_since ver="8.0.12" />}}

以下のオプションは、`format=json`の場合にのみ使用できます。

| パラメーター       | 既定値 | 説明                                                              |
|:----------- |---------|:--------------------------------------------------------------------------|
| transpose   | false   | 行配列の代わりに、列配列（`cols`）を生成します。                                     |
| rowsFlatten | false   | JSONオブジェクトの`rows`フィールドの配列次元を1つ減らします。                          |
| rowsArray   | false   | 各レコードをオブジェクトとする配列のJSONを生成します。                         |

**`format=csv`で使用できるパラメーター**

| パラメーター       | 既定値 | 説明                                                              |
|:----------- |---------|:--------------------------------------------------------------------------|
| header      |         | `skip`を指定するとヘッダーを含めません。 |
| precision   | -1      | 浮動小数点数の桁数：-1は丸めなし、0は整数             |

基本例では、クライアントが`db/reply/#`を購読し、`reply`に`db/reply/my_query`を指定して`db/query`トピックにクエリを発行します。これにより、複数のメッセージから自身への応答を識別できます。バインドプレースホルダーを使用する場合は、`p`フィールドに`?`用のJSON配列を指定します。

```json
{
    "q": "select name,time,value from example where name = ? limit ?",
    "p": ["wave.sin", 5],
    "format": "csv",
    "reply": "db/reply/my_query"
}
```

または、`:name`の名前付きパラメーター用のJSONオブジェクトを指定します。 {{< neo_since ver="8.7.0" />}}

```json
{
    "q": "select name,time,value from example where name = :name limit :n",
    "p": {"name": "wave.sin", "n": 5},
    "format": "csv",
    "reply": "db/reply/my_query"
}
```

{{< figure src="/neo/api-mqtt/img/query_mqttx.png" width="600px" caption="MQTTでクエリを実行して応答を受信する例（MQTTX.appを使用）">}}

## クライアントの例 {#클라이언트-예시}

### JSHアプリ {#jsh-앱}

{{< neo_since ver="8.5.0" />}}

この例では、応答トピックを購読し、SQLクエリを発行して、MQTTで結果を受信する手順を説明します。

1. **応答トピックの購読**  
   まず、`db/reply/my_query`のような結果を受信するトピックを購読します。

2. **SQLクエリの発行**  
   SQLクエリ（`q`）、結果形式（`format`）、応答トピック（`reply`）を含むメッセージを、`db/query`トピックに発行します。

3. **応答の受信と処理**  
   サーバーはクエリを処理し、指定した応答トピックに結果を送信します。クライアントはメッセージを受信して結果を出力します。

JSHのサンプルコード：

```js {linenos=table,linenostart=1,hl_lines=["7-9",18,28]}
const process = require("process");
const mqtt = require("mqtt");

const topicReply = "db/reply/my_query";
const topicQuery = "db/query";
const queryRequest = {
    q: `select name,time,value from example limit 5`,
    format: 'csv',
    reply: topicReply,
};

var client = new mqtt.Client({
    servers: ["tcp://127.0.0.1:5653"],
    keepAlive: 10,
});
client.on('open', () => {
    console.println('---- subscribe:', topicReply);
    client.subscribe(topicReply, {qos:0})
});
client.on('error', (err) => {
    console.println('MQTT ERROR:', err.message);
});
client.on('close', () => {
    console.println('---- disconnected');
});
client.on('subscribed', (topic, reason) => {
    console.println('---- publish:', topicQuery);
    client.publish(topicQuery, JSON.stringify(queryRequest));
});
client.on('message', (msg) => {
    console.println('---- reply')
    console.println(msg.payload);
    client.unsubscribe(msg.topic);
});
client.on('unsubscribed', (topic, reason) => {
    console.println('---- unsubscribed:', topic, 'reason:', reason);
    setTimeout(()=>{
        client.close();
    }, 500)
});
```

実行と結果出力：

```sh
/work > ./mqtt_query.js
---- subscribe: db/reply/my_query ----
---- publish: db/query ----
---- reply ----
name,time,value
my-car,1782260468085501458,1.2345
my-car,1782260474814668541,1.35795
my-car,1782260474827077041,1.4814
my-car,1782260474839257291,1.60485

---- unsubscribed: db/reply/my_query reason: 0 ----
---- disconnected ----
```


### Node.js クライアント {#nodejs-클라이언트}

```sh
npm install mqtt --save
```

```js {linenos=table,linenostart=1}
const mqtt = require("mqtt");

const client = mqtt.connect("mqtt://127.0.0.1:5653", {
    clean: true,
    connectTimeout: 3000,
    autoUseTopicAlias: true,
    protocolVersion: 5,
});

const sqlText = "SELECT time,value FROM example "+
    "where name = 'neo_cpu.percent' limit 3";

client.on("connect", () => {
    client.subscribe("db/reply/#", (err) => {
        if (!err) {
            const req = {
                q: sqlText,
                format: "box",
                precision: 1,
                timeformat: "15:04:05",
            };
            client.publish("db/query", JSON.stringify(req));
        }
    });
});

client.on("message", (topic, message) => {
    console.log(message.toString());
    client.end();
});
```

```sh
$ node main.js

+----------+-------+
| TIME     | VALUE |
+----------+-------+
| 05:46:19 | 69.4  |
| 05:46:22 | 26.4  |
| 05:46:25 | 42.8  |
+----------+-------+
```

### Go クライアント {#go-클라이언트}

**応答の構造定義**

```go
type Result struct {
	Success bool       `json:"success"`
	Reason  string     `json:"reason"`
	Elapse  string     `json:"elapse"`
	Data    ResultData `json:"data"`
}

type ResultData struct {
	Columns []string `json:"columns"`
	Types   []string `json:"types"`
	Rows    [][]any  `json:"rows"`
}
```

**`db/reply`の購読**

```go {linenos=table,linenostart=1}
client.Subscribe("db/reply", 1, func(_ paho.Client, msg paho.Message) {
    buff := msg.Payload()
    result := Result{}
    if err := json.Unmarshal(buff, &result); err != nil {
        panic(err)
    }
    if !result.Success {
        fmt.Println("RECV: query failed:", result.Reason)
        return
    }
    if len(result.Data.Rows) == 0 {
        fmt.Println("Empty result")
        return
    }
    for i, rec := range result.Data.Rows {
        // 各レコードに必要な処理を実行します。
        name := rec[0].(string)
        ts := time.Unix(0, int64(rec[1].(float64)))
        value := float64(rec[2].(float64))
        fmt.Println(i+1, name, ts, value)
    }
})
```

**'db/query'への発行**

```go
jsonStr := `{ "q": "select * from EXAMPLE order by time desc limit 5" }`
client.Publish("db/query", 1, false, []byte(jsonStr))
```
