---
title: MQTT Query API
type: docs
weight: 20
---

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