---
title: HTTP client in Go
type: docs
weight: 63
---

## Query

### GET

Make a SQL query with URL escaping.

```go
q := url.QueryEscape("select count(*) from M$SYS_TABLES where name = 'TAGDATA'")
```

Call HTTP GET method.

```go
client := http.Client{}
rsp, err := client.Get("http://127.0.0.1:5654/db/query?q=" + q)
```

Find the full source code in [here]({{< neo_examples_url >}}/go/http_get/http_get.go).

### POST JSON

A client can request a JSON message containing a SQL query.

Make JSON content with a SQL query.

```go
queryJson := `{"q":"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}`
```

Call HTTP POST method with the content.

```go
rsp, err := client.Post(addr, "application/json", bytes.NewBufferString(queryJson))
```

Find the full source code in [here]({{< neo_examples_url >}}/go/http_post_query/http_post_query.go).

### POST FormData

It is possible to send SQL query from HTML form data.

```go
data := url.Values{"q": {"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}}
rsp, err := client.Post(addr, "application/x-www-form-urlencoded", bytes.NewBufferString(data.Encode()))
```

Find the full source code in [here]({{< neo_examples_url >}}/go/http_post_form/http_post_form.go).


## Write

### POST JSON

```go
rows := [][]any{
	{"my-car", time.Now().UnixNano(), 32.1},
	{"my-car", time.Now().UnixNano(), 65.4},
	{"my-car", time.Now().UnixNano(), 76.5},
}
columns := []string{"name", "time", "value", "jsondata"}
writeReq := map[string]any{
	"data": map[string]any{
		"columns": columns,
		"rows":    rows,
	},
}
queryJson, _ := json.Marshal(&writeReq)
rsp, err := client.Post(addr, "application/json", bytes.NewBuffer(queryJson))
```

Full source code is [here]({{< neo_examples_url >}}/go/http_write_json/http_write_json.go).

### POST CSV

```go
rows := []string{
	fmt.Sprintf("my-car,%d,32.1", time.Now().UnixNano()),
	fmt.Sprintf("my-car,%d,65.4", time.Now().UnixNano()),
	fmt.Sprintf("my-car,%d,76.5", time.Now().UnixNano()),
}
rsp, err := client.Post(addr, "text/csv", bytes.NewBuffer([]byte(strings.Join(rows, "\n"))))
```
Full source code is [here]({{< neo_examples_url >}}/go/http_write_csv/http_write_csv.go).