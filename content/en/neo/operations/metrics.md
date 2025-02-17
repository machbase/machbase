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

### Go

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `go:num_cgo_call_avg`                  |            | Average number of calls of CGO functions |
| `go:num_cgo_call_max`                  |            | Max number of calls of CGO functions     |
| `go:num_cgo_call_min`                  |            | Min number of calls of CGO functions     |
| `go:num_goroutine_avg`                 |            | Average number of go routines            |
| `go:num_goroutine_max`                 |            | Max number of go routines                |
| `go:num_goroutine_min`                 |            | Min number of go routines                |

### HTTP

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:http:count`                  |            | Total HTTP request count                 |
| `machbase:http:latency_p50`            |  ns.       | HTTP response latency in 0.5 quantile    |
| `machbase:http:latency_p90`            |  ns.       | HTTP response latency in 0.9 quantile    |
| `machbase:http:latency_p99`            |  ns.       | HTTP response latency in 0.99 quantile   |
| `machbase:http:recv_bytes`             | byte       | HTTP request payload size                |
| `machbase:http:send_bytes`             | byte       | HTTP response payload size               |
| `machbase:http:status_1xx`             |            | HTTP responses that replied in 1xx status|
| `machbase:http:status_2xx`             |            | HTTP responses that replied in 2xx status|
| `machbase:http:status_3xx`             |            | HTTP responses that replied in 3xx status|
| `machbase:http:status_4xx`             |            | HTTP responses that replied in 4xx status|
| `machbase:http:status_5xx`             |            | HTTP responses that replied in 5xx status|

### TQL

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:tql:cache:count_avg`         |            | Average number of TQL cache items          |
| `machbase:tql:cache:count_max`         |            | Max number of TQL cache items              |
| `machbase:tql:cache:count_min`         |            | Min number of TQL cache items              |
| `machbase:tql:cache:data_size_avg`     | byte       | Average size of the total TQL cache        |
| `machbase:tql:cache:data_size_max`     | byte       | Max size of the total TQL cache            |
| `machbase:tql:cache:data_size_min`     | byte       | Min size of the total TQL cache            |
| `machbase:tql:cache:evictions`         |            | TQL count of the evicted items removed from the cache |
| `machbase:tql:cache:insertions`        |            | The count of the new items inserted into the cache |
| `machbase:tql:cache:hits`              |            | TQL cache hit count                        |
| `machbase:tql:cache:misses`            |            | TQL cache miss count                       |

### Database

| Metric                                 | Unit       | Description                         |
|:---------------------------------------|:----------:|:------------------------------------|
| `machbase:session:append:count`        |            | The number of appenders used             |
| `machbase:session:append:in_use`       |            | The number of appenders that are in open state |
| `machbase:session:conn:count`          |            | The number of conn used                  |
| `machbase:session:conn:in_use`         |            | The number of conn that are in open state|
| `machbase:session:stmt:count`          |            | The number of stmt used                  |
| `machbase:session:stmt:in_use`         |            | The number of stmt that are in open state|
| `machbase:session:conn:use_time_avg`   |  ns.       | Average time of conn uses                |
| `machbase:session:conn:use_time_max`   |  ns.       | Max time of conn uses                    |
| `machbase:session:conn:use_time_min`   |  ns.       | Min time of conn uses                    |
| `machbase:session:conn:wait_time_avg`  |  ns.       | Average time of the fetch iteration limit wait |
| `machbase:session:conn:wait_time_max`  |  ns.       | Max time of the fetch iteration limit wait|
| `machbase:session:conn:wait_time_min`  |  ns.       | Min time of the fetch iteration limit wait|
| `machbase:session:query:count`         |            | Total queries (only that use fetch iteration)   |
| `machbase:session:query:exec_time_avg` |  ns.       | Average time of the prepare stmt. time     |
| `machbase:session:query:exec_time_max` |  ns.       | Max time of the prepare stmt. time         |
| `machbase:session:query:exec_time_min` |  ns.       | Min time of the prepare stmt. time         |
| `machbase:session:query:fetch_time_avg`|  ns.       | Average time of the fetch time             |
| `machbase:session:query:fetch_time_max`|  ns.       | Max time of the fetch time                 |
| `machbase:session:query:fetch_time_min`|  ns.       | Min time of the fetch time                 |
| `machbase:session:query:wait_time_avg` |  ns.       | Average time of the iteration limit wait   |
| `machbase:session:query:wait_time_max` |  ns.       | Max time of the iteration limit wait       |
| `machbase:session:query:wait_time_min` |  ns.       | Min time of the iteration limit wait       |
| `machbase:session:query:hwm:elapse`    |  ns.       | High Water Marked Query total elapse time  |
| `machbase:session:query:hwm:exec_time` |  ns.       | High Water Marked Query's stmt prepare time|
| `machbase:session:query:hwm:fetch_time`|  ns.       | High Water Marked Query's fetch time       |
| `machbase:session:query:hwm:wait_time` |  ns.       | High Water Marked Query's iteration limit wait |
| `machbase:session:query:hwm:sql_args`  | []string   | High Water Marked Query's SQL bind variables |
| `machbase:session:query:hwm:sql_text`  | string     | High Water Marked Query's SQL              |

