---
title: 메트릭
type: docs
weight: 101
---

{{< callout type="warning" >}}
**베타 주의**<br/>
본 문서에서 설명하는 기능은 향후 릴리스에서 변경될 수 있습니다.
{{< /callout >}}

메트릭은 1분, 5분, 15분 샘플링 주기로 제공됩니다.

## HTTP API
RESTful API로 메트릭을 가져오려면 다음 엔드포인트를 사용하십시오.
```
http://127.0.0.1:5654/debug/statz?interval=[1m|5m|15m]&format=[json|html]
```
이 엔드포인트에서 1분, 5분, 15분 중 원하는 주기를 지정할 수 있습니다.
기본적으로 동일한 머신(localhost)에서만 접근할 수 있다는 점에 유의하십시오.

기본 출력 형식은 JSON이며, `format=html`을 지정하면 HTML 테이블로 응답합니다.

## TQL with CHART

아래 예시는 machbase-neo의 HTTP 지연 분포를 차트로 시각화하는 방법을 보여 줍니다.
`FAKE( statz(period, metrics...) )` SRC 함수를 사용해 시간-값 쌍을 생성한 뒤 `CHART()`에 전달합니다.

{{< tabs items="CHART,Code">}}
{{< tab >}}
{{< figure src="/neo/operations/img/metrics_http_latency.jpg" width="600" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE(statz("15m", 
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
            if (val > 1000000000)   { return `${val/1000000000} s`; }
            else if (val > 1000000) { return `${val/1000000} ms`; } 
            else if (val > 1000)    { return `${val/1000} µs`; }
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
        tooltip: { trigger: "axis", valueFormatter: yformatter },
        legend: {}
    })
)
```

{{< /tab >}}
{{< /tabs >}}

## 메트릭 목록
모든 메트릭은 선택한 샘플링 주기를 기준으로 하며, 1분(`1m`), 5분(`5m`), 15분(`15m`) 중 하나를 사용할 수 있습니다.

### HTTP

| Metric                      |  Description                                                |
|:----------------------------|:------------------------------------------------------------|
| `machbase:http:count`       |  전체 HTTP 요청 수                                          |
| `machbase:http:latency_p50` |  HTTP 응답 지연 50 분위수(중앙값, ns)                       |
| `machbase:http:latency_p90` |  HTTP 응답 지연 90 분위수(ns)                              |
| `machbase:http:latency_p99` |  HTTP 응답 지연 99 분위수(ns)                              |
| `machbase:http:recv_bytes`  |  HTTP 요청 페이로드 총 크기                                 |
| `machbase:http:send_bytes`  |  HTTP 응답 페이로드 총 크기                                 |
| `machbase:http:status_1xx`  |  1xx 상태 코드 응답 수                                      |
| `machbase:http:status_2xx`  |  2xx 상태 코드 응답 수                                      |
| `machbase:http:status_3xx`  |  3xx 상태 코드 응답 수                                      |
| `machbase:http:status_4xx`  |  4xx 상태 코드 응답 수                                      |
| `machbase:http:status_5xx`  |  5xx 상태 코드 응답 수                                      |

### MQTT

| Metric                        | Description                                   |
|:------------------------------|:----------------------------------------------|
| `machbase:mqtt:recv_bytes`    | 수신한 총 바이트 수(바이트)                             |
| `machbase:mqtt:send_bytes`    | 전송한 총 바이트 수                                     |
| `machbase:mqtt:recv_pkts`     | 수신한 PUBLISH 메시지 개수                              |
| `machbase:mqtt:send_pkts`     | 전송한 전체 메시지 개수                                 |
| `machbase:mqtt:recv_msgs`     | 수신한 PUBLISH 메시지 개수                              |
| `machbase:mqtt:send_msgs`     | 전송한 PUBLISH 메시지 개수                              |
| `machbase:mqtt:drop_msgs`     | 느린 구독자 때문에 드롭된 PUBLISH 메시지 개수           |
| `machbase:mqtt:retained`      | 브로커에 유지(retain)된 메시지 개수                      |
| `machbase:mqtt:subscriptions` | 브로커에 등록된 구독 수                                  |
| `machbase:mqtt:clients`       | 현재 연결되었거나 세션이 유지된 전체 클라이언트 수      |
| `machbase:mqtt:clients_connected`      | 현재 연결된 클라이언트 수                      |
| `machbase:mqtt:clients_disconnected`   | 브로커에 등록되어 있지만 현재는 연결되지 않은 지속 세션 클라이언트 수 |
| `machbase:mqtt:inflight`               | 현재 전송 중인(in-flight) 메시지 수               |
| `machbase:mqtt:inflight_dropped`       | 전송 중 드롭된 메시지 수                           |

### TQL

| Metric                                         | Description                                     |
|:-----------------------------------------------|:------------------------------------------------|
| `machbase:tql:cache:count_[avg\|max\|min]`     | TQL 캐시 항목 수                                 |
| `machbase:tql:cache:data_size_[avg\|max\|min]` | TQL 캐시 전체 크기(바이트)                        |
| `machbase:tql:cache:evictions`                 | 캐시에서 제거된 항목 수                           |
| `machbase:tql:cache:insertions`                | 캐시에 새로 삽입된 항목 수                         |
| `machbase:tql:cache:hits`                      | 캐시 히트 수                                      |
| `machbase:tql:cache:misses`                    | 캐시 미스 수                                      |

### Database Sessions

| Metric                                             | Description                         |
|:---------------------------------------------------|:------------------------------------|
| `machbase:session:append:count`                    | 사용된 앱팬더 총 수                              |
| `machbase:session:append:in_use`                   | 현재 열려 있는 앱팬더 수                         |
| `machbase:session:conn:count`                      | 사용된 연결 총 수                                 |
| `machbase:session:conn:in_use`                     | 현재 열려 있는 연결 수                             |
| `machbase:session:stmt:count`                      | 사용된 스테이트먼트 총 수                          |
| `machbase:session:stmt:in_use`                     | 현재 열려 있는 스테이트먼트 수                      |
| `machbase:session:conn:use_time_[avg\|max\|min]`   | 연결 사용 시간(ns)                                 |
| `machbase:session:conn:wait_time_[avg\|max\|min]`  | 가져오기(fech) 한도 대기 시간(ns)                   |
| `machbase:session:query:count`                     | 쿼리 총 수(페치 반복을 사용하는 쿼리)               |
| `machbase:session:query:exec_time_[avg\|max\|min]` | 준비된 스테이트먼트 실행 시간(ns)                   |
| `machbase:session:query:fetch_time_[avg\|max\|min]`| 페치 시간(ns)                                      |
| `machbase:session:query:wait_time_[avg\|max\|min]` | 반복 한도 대기 시간(ns)                             |
| `machbase:session:query:hwm:elapse`                | High Water Mark 쿼리의 총 경과 시간(ns)              |
| `machbase:session:query:hwm:exec_time`             | High Water Mark 쿼리의 스테이트먼트 준비 시간(ns)    |
| `machbase:session:query:hwm:fetch_time`            | High Water Mark 쿼리의 페치 시간(ns)                |
| `machbase:session:query:hwm:wait_time`             | High Water Mark 쿼리의 반복 한도 대기 시간(ns)      |
| `machbase:session:query:hwm:sql_args`              | High Water Mark 쿼리의 SQL 바인드 변수([]string)     |
| `machbase:session:query:hwm:sql_text`              | High Water Mark 쿼리의 SQL 텍스트                   |

### Go

| Metric                             | Description                          |
|:-----------------------------------|:-------------------------------------|
| `go:heap_in_use_[avg\|max\|min]`   | 힙 사용량(바이트)                     |
| `go:cgo_call_[avg\|max\|min]`      | CGO 함수 호출 수                      |
| `go:goroutine_[avg\|max\|min]`     | 고루틴 개수                           |
