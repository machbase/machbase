---
title: Metrics
type: docs
weight: 101
---

{{< callout type="warning" >}}
**BETA Warning**<br/>
The features described in this document are subject to change and may be updated in future releases.
{{< /callout >}}

The metrics are provided in 1 minute, 5 minutes and 15 minutes sampling periods.

## HTTP API
To retrieve the metrics via the RESTful API, use the endpoint:
```
http://127.0.0.1:5654/db/statz?interval=[1m|5m|15m]
```
This endpoint allows you to specify the interval for which you want to gather metrics,
choosing from 1 minute, 5 minutes, or 15 minutes.
Please note that this endpoint is only accessible from the same machine (localhost) by default.

## TQL with CHART

The example below shows how to render machbase-neo's HTTP latency distribution in a chart.
It uses `FAKE( statz(period, metrics...) )` SRC function, and then makes time-value pairs for input of the `CHART()`.

{{< tabs items="CHART,Code">}}
{{< tab >}}
{{< figure src="../img/metrics_http_latency.jpg" width="600" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE(statz("1m", 
    "machbase:http:latency_p50",
    "machbase:http:latency_p90",
    "machbase:http:latency_p99"
))

MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))

CHART(
    size("600px", "300px"),
    chartJSCode({
        function yformatter(val, idx){
            if (val > 1000000000) {
                return `${val/1000000000} s`;
            } else if (val > 1000000) {
                return `${val/1000000} ms`;
            } else if (val > 1000) {
                return `${val/1000} µs`;
            }
            return `${val} ns`
        }
    }),
    chartOption({
        animation: false,
        yAxis: { type: "value", axisLabel:{ formatter: yformatter }},
        xAxis: { type: "time", axisLabel:{ rotate: -90 }},
        series: [
            {type: "line", data: column(3), areaStyle:{}, smooth:false, name: "p99"},
            {type: "line", data: column(2), areaStyle:{}, smooth:false, name: "p90"},
            {type: "line", data: column(1), areaStyle:{}, smooth:false, name: "p50"},
        ],
        tooltip: {trigger: "axis"},
        legend: {data:['p50', 'p90', 'p99']}
    })
)
```

{{< /tab >}}
{{< /tabs >}}

## Metrics
All metrics are based on the selected sampling period,
which can be one of the following:<br/> 1 minute (`1m`), 5 minutes (`5m`), or 15 minutes (`15m`).

### HTTP

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:http:count`                  |            | Total number of HTTP requests                 |
| `machbase:http:latency_p50`            |  ns.       | HTTP response latency at the 50th percentile (median) |
| `machbase:http:latency_p90`            |  ns.       | HTTP response latency at the 90th percentile  |
| `machbase:http:latency_p99`            |  ns.       | HTTP response latency at the 99th percentile  |
| `machbase:http:recv_bytes`             | byte       | Total size of HTTP request payloads           |
| `machbase:http:send_bytes`             | byte       | Total size of HTTP response payloads          |
| `machbase:http:status_1xx`             |            | Number of HTTP responses with 1xx status codes|
| `machbase:http:status_2xx`             |            | Number of HTTP responses with 2xx status codes|
| `machbase:http:status_3xx`             |            | Number of HTTP responses with 3xx status codes|
| `machbase:http:status_4xx`             |            | Number of HTTP responses with 4xx status codes|
| `machbase:http:status_5xx`             |            | Number of HTTP responses with 5xx status codes|

### MQTT

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:mqtt:recv_bytes`             | byte       | total number of bytes received      |
| `machbase:mqtt:send_bytes`             | byte       | total number of bytes sent          |
| `machbase:mqtt:recv_pkts`              |            | the total number of publish messages received |
| `machbase:mqtt:send_pkts`              |            | total number of messages of any type sent  |
| `machbase:mqtt:recv_msgs`              |            | total number of publish messages received  |
| `machbase:mqtt:send_msgs`              |            | total number of publish messages sent      |
| `machbase:mqtt:drop_msgs`              |            | total number of publish messages dropped to slow subscriber  |
| `machbase:mqtt:retained`               |            | total number of retained messages active on the broker  |
| `machbase:mqtt:subscriptions`          |            | total number of subscriptions active on the broker  |
| `machbase:mqtt:clients`                |            | total number of connected and disconnected clients with a persistent session currently connected and registered  |
| `machbase:mqtt:clients_connected`      |            | number of currently connected clients  |
| `machbase:mqtt:clients_disconnected`   |            | total number of persistent clients (with clean session disabled) that are registered at the broker but are currently disconnected  |
| `machbase:mqtt:inflight`               |            | the number of messages currently in-flight  | 
| `machbase:mqtt:inflight_dropped`       |            | the number of inflight messages which were dropped  | 

### TQL

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:tql:cache:count_avg`         |            | Average number of items in the TQL cache |
| `machbase:tql:cache:count_max`         |            | Maximum number of items in the TQL cache |
| `machbase:tql:cache:count_min`         |            | Minimum number of items in the TQL cache |
| `machbase:tql:cache:data_size_avg`     | byte       | Average total size of the TQL cache      |
| `machbase:tql:cache:data_size_max`     | byte       | Maximum total size of the TQL cache      |
| `machbase:tql:cache:data_size_min`     | byte       | Minimum total size of the TQL cache      |
| `machbase:tql:cache:evictions`         |            | Number of items evicted from the TQL cache |
| `machbase:tql:cache:insertions`        |            | Number of new items inserted into the TQL cache |
| `machbase:tql:cache:hits`              |            | Number of cache hits in the TQL cache   |
| `machbase:tql:cache:misses`            |            | Number of cache misses in the TQL cache |

### Database Sessions

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:session:append:count`        |            | Total number of appenders used      |
| `machbase:session:append:in_use`       |            | Number of appenders currently open  |
| `machbase:session:conn:count`          |            | Total number of connections used    |
| `machbase:session:conn:in_use`         |            | Number of connections currently open|
| `machbase:session:stmt:count`          |            | Total number of statements used     |
| `machbase:session:stmt:in_use`         |            | Number of statements currently open |
| `machbase:session:conn:use_time_avg`   |  ns.       | Average connection usage time       |
| `machbase:session:conn:use_time_max`   |  ns.       | Maximum connection usage time       |
| `machbase:session:conn:use_time_min`   |  ns.       | Minimum connection usage time       |
| `machbase:session:conn:wait_time_avg`  |  ns.       | Average wait time for fetch iteration limit |
| `machbase:session:conn:wait_time_max`  |  ns.       | Maximum wait time for fetch iteration limit |
| `machbase:session:conn:wait_time_min`  |  ns.       | Minimum wait time for fetch iteration limit |
| `machbase:session:query:count`         |            | Total number of queries (only those using fetch iteration) |
| `machbase:session:query:exec_time_avg` |  ns.       | Average execution time of prepared statements |
| `machbase:session:query:exec_time_max` |  ns.       | Maximum execution time of prepared statements |
| `machbase:session:query:exec_time_min` |  ns.       | Minimum execution time of prepared statements |
| `machbase:session:query:fetch_time_avg`|  ns.       | Average fetch time                 |
| `machbase:session:query:fetch_time_max`|  ns.       | Maximum fetch time                 |
| `machbase:session:query:fetch_time_min`|  ns.       | Minimum fetch time                 |
| `machbase:session:query:wait_time_avg` |  ns.       | Average wait time for iteration limit       |
| `machbase:session:query:wait_time_max` |  ns.       | Maximum wait time for iteration limit       |
| `machbase:session:query:wait_time_min` |  ns.       | Minimum wait time for iteration limit       |
| `machbase:session:query:hwm:elapse`    |  ns.       | High Water Marked Query total elapsed time  |
| `machbase:session:query:hwm:exec_time` |  ns.       | High Water Marked Query's statement preparation time|
| `machbase:session:query:hwm:fetch_time`|  ns.       | High Water Marked Query's fetch time        |
| `machbase:session:query:hwm:wait_time` |  ns.       | High Water Marked Query's iteration limit wait time |
| `machbase:session:query:hwm:sql_args`  | []string   | High Water Marked Query's SQL bind variables |
| `machbase:session:query:hwm:sql_text`  | string     | High Water Marked Query's SQL text           |

### Go

| Metric                             | Unit       | Description                          |
|:-----------------------------------|:----------:|:-------------------------------------|
| `go:heap_in_use_avg`               | byte       | Average heap usage                   |
| `go:heap_in_use_max`               | byte       | Maximum heap usage                   |
| `go:heap_in_use_min`               | byte       | Minimum heap usage                   |
| `go:cgo_call_avg`                  |            | Average number of CGO function calls |
| `go:cgo_call_max`                  |            | Maximum number of CGO function calls |
| `go:cgo_call_min`                  |            | Minimum number of CGO function calls |
| `go:goroutine_avg`                 |            | Average number of goroutines         |
| `go:goroutine_max`                 |            | Maximum number of goroutines         |
| `go:goroutine_min`                 |            | Minimum number of goroutines         |

