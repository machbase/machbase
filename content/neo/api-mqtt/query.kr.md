---
title: MQTT 조회
type: docs
weight: 20
---

MQTT에서 데이터베이스 쿼리를 실행하려면 `db/query` 토픽으로 요청을 보내십시오. 서버는 `db/reply` 토픽 또는 요청의 `reply` 필드에 지정한 토픽으로 결과를 돌려줍니다.

## 쿼리 JSON

| param       | default | description                                           |
|:----------- |---------|:------------------------------------------------------|
| **q**       | _n/a_   | 실행할 SQL 쿼리 문자열                                      |
| reply       | db/reply| 쿼리 결과를 받을 토픽                                       |
| format      | json    | 결과 형식: json, csv, box                               |
| timeformat  | ns      | 시간 단위: s, ms, us, ns                                |
| tz          | UTC     | 시간대: UTC, Local, 지역 지정                           |
| compress    | _no compression_ | 압축 방식: gzip                                  |
| rownum      | false   | 행 번호 포함 여부: true, false                          |
| heading     | true    | 헤더 표시 여부: true, false                              |
| precision   | -1      | 부동소수점 자릿수: -1은 반올림 없음, 0은 정수             |

**`format=json`에서 사용 가능한 추가 매개변수** {{< neo_since ver="8.0.12" />}}

다음 옵션은 `format=json`일 때만 사용할 수 있습니다.

| param       | default | description                                                              |
|:----------- |---------|:--------------------------------------------------------------------------|
| transpose   | false   | 행 대신 열 배열(`cols`)을 생성합니다.                                     |
| rowsFlatten | false   | JSON 객체의 `rows` 필드 차원을 한 단계 줄입니다.                          |
| rowsArray   | false   | 각 레코드를 객체 배열로 구성한 JSON을 생성합니다.                         |


기본 예시는 클라이언트가 `db/reply/#`를 구독한 뒤 `reply` 필드를 `db/reply/my_query`로 지정해 `db/query` 토픽으로 쿼리를 발행하고, 여러 메시지 중 자신의 응답만 구분하는 방법을 보여 줍니다.

```json
{
    "q": "select name,time,value from example limit 5",
    "format": "csv",
    "reply": "db/reply/my_query"
}
```

{{< figure src="/neo/api-mqtt/img/query_mqttx.png" width="600px" caption="A demonstration shows how to query and receive responses over MQTT. (Using MQTTX.app)">}}

## 클라이언트 예시

### JSH 앱

{{< neo_since ver="8.0.52" />}}

이 예제에서는 응답 토픽을 구독하고 SQL 쿼리를 발행한 뒤 MQTT를 통해 결과를 받는 과정을 살펴봅니다.

1. **응답 토픽 구독**  
   먼저 `db/reply/my_query`처럼 결과를 받을 토픽을 구독합니다.

2. **SQL 쿼리 발행**  
   `db/query` 토픽으로 SQL 쿼리(`q`), 결과 형식(`format`), 응답 토픽(`reply`)을 포함한 메시지를 발행합니다.

3. **응답 수신 및 처리**  
   서버가 쿼리를 처리하면 지정한 응답 토픽으로 결과를 전송합니다. 클라이언트는 메시지를 받아 결과를 출력합니다.

Below is the complete code example:

```js {linenos=table,linenostart=1,hl_lines=["9-11","13-17","20-24"]}
const process = require("@jsh/process");
const mqtt = require("@jsh/mqtt");

const topicReply = "db/reply/my_query";
const topicQuery = "db/query";
try {
    var conf = { serverUrls: ["tcp://127.0.0.1:5653"] };
    var client = new mqtt.Client(conf);
    client.onConnect = () => {
        client.subscribe({subscriptions:[{topic:topicReply, qos: 1}]})
    }
    var received = false
    client.onMessage = (msg) => {
        console.log('---- reply ----')
        console.log(msg.payload.string());
        received = true
    }

    client.connect( {timeout: 1000} );
    client.publish({topic:topicQuery, qos: 1}, JSON.stringify({
        q: `select name,time,value from example limit 5`,
        format: 'csv',
        reply: topicReply,
    }))
    do {
        process.sleep(100);
    } while(!received)
    client.unsubscribe({topics:[topicReply]})
    client.disconnect({timeout:1000});
} catch (e) {
    console.error("Error:", e.message);
}
```

### Node.js 클라이언트

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

### Go 클라이언트

**응답 구조 정의**

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

**`db/reply` 구독**

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
        // 각 레코드에 대해 필요한 작업을 수행합니다.
        name := rec[0].(string)
        ts := time.Unix(0, int64(rec[1].(float64)))
        value := float64(rec[2].(float64))
        fmt.Println(i+1, name, ts, value)
    }
})
```

**Publish 'db/query'**

```go
jsonStr := `{ "q": "select * from EXAMPLE order by time desc limit 5" }`
client.Publish("db/query", 1, false, []byte(jsonStr))
```
