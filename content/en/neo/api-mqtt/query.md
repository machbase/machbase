---
title: MQTT Query API
type: docs
weight: 20
---

General purposed MQTT brokers deliver messages to all subscribers of the topic as diagram below. When a publisher sends message `M1`, `M2` to the `TOPIC`, both of `SUBSCRIBER-A` and `SUBSCRIBER-B` receive the same messages. 

```mermaid
flowchart LR
PUBLISHER -->|m1,m2| TOPIC

TOPIC -->|m1, m2| A(SUBSCRIBER-A)
TOPIC -->|m1, m2| B(SUBSCRIBER-B)
```

In contrast with general MQTT brokers, machbase-neo delivers messages only if the publisher and subscriber share same connection (or session in terms of MQTT). This means machbase-neo MQTT is not working as a message broker, but it just uses MQTT as transport layer and subscription and publication is scoped per connection.

For example, while `CLIENT-M` and `CLIENT-P` subscribed to same `TOPIC` and waiting messages.
Server sends messages `M1` and `M2` to `TOPIC` that were inscribed to `CLIENT-M`.
Those messages are delivered only to `CLIENT-M` but `CLIENT-P` receives `P1` and `P2` that were explicitly designated to it by server. If another client `PUBLISHER-X` sends `X1` to `TOPIC`, this `X1` will be delivered to server and the other clients will not know about this event.

```mermaid
flowchart LR

SERVER -->|m1, m2| T(TOPIC)
SERVER -->|p1, p2| T(TOPIC)
PUBLISHER-X-->|x1| T(TOPIC)

T -->|m1,m2| M(CLIENT-M)
T -->|p1,p2| P(CLIENT-P)
T -->|x1| SERVER
```

Application needs a preparing step to query machbase-neo via MQTT which is subscribing to `db/reply`.
In the diagram below we shows general procedure assuming `CLIENT` uses QoS 1.
for the notes, machbase-neo support QoS 0, 1 of MQTT v3.1.1 specification.

After established MQTT session by exchanging `CONNECT`and `CONNACK`, Client should subscribe to `db/reply` first before send query message to `db/query`, otherwise it can not receive any "query result".

```mermaid
sequenceDiagram
    CLIENT->> SERVER: CONNECT
    activate SERVER
    SERVER -->> CLIENT: CONNACK
    deactivate SERVER

    CLIENT ->> SERVER: SUBSCRIBE 'db/reply'
    activate SERVER
    SERVER -->> CLIENT: SUBACK
    deactivate SERVER

    loop async
        CLIENT ->> SERVER: PUBLISH 'db/query'
        activate SERVER
        SERVER -->> CLIENT: PUBACK
        deactivate SERVER

        SERVER ->> CLIENT: PUBLISH 'db/reply'
        activate CLIENT
        CLIENT -->> SERVER: PUBACK
        deactivate CLIENT
    end

    CLIENT->> SERVER: DISCONNECT
```

The messages ➍, ➎ are sent by server asynchronous way which is nature of MQTT protocol. Then a client application shouldn't be implemented based specific order of those two messages.


{{< callout emoji="📌" >}}
If client is only publishing to `db/append` for writing data, it is not necessary to subscribe `db/reply`. This topic is required only for receiving query result.
{{< /callout >}}

## Request JSON

| param       | default | description                   |
|:----------- |---------|:----------------------------- |
| **q**       | _n/a_   | SQL query string              |
| reply       | db/reply| The topic where to receive the result of query |
| format      | json    | Result data format: json, csv, box |
| timeformat  | ns      | Time format: s, ms, us, ns    |
| tz          | UTC     | Time Zone: UTC, Local and location spec |
| compress    | _no compression_   | compression method: gzip      |
| rownum      | false   | including rownum: true, false |
| heading     | true    | showing heading: true, false  |
| precision   | -1      | precision of float value, -1 for no round, 0 for int |

**More Parameters in `format=json`** {{< neo_since ver="8.0.12" />}}

Those options are available only when `format=json`

| param       | default | description                   |
|:----------- |---------|:----------------------------- |
| transpose   | false   | produce cols array instead of rows. |
| rowsFlatten | false   | reduce the array dimension of the *rows* field in the JSON object. |
| rowsArray   | false   | produce JSON that contains only array of object for each record.  |


A basic query example shows the client subscribe to `db/reply/#` and publish a query request to `db/query` with *reply* field `db/reply/my_query` so that it can identify the individual reply from multiple messages.

{{< figure src="../img/query_mqttx.png" width="600px" caption="A demonstration shows how to query and receive responses over MQTT. (Using MQTTX.app)">}}

## Sample code


**Define data structure for response**

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

**Subscribe 'db/reply'**

```go
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
        // do something for each record
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