---
title: メトリクス
type: docs
weight: 101
toc: true
---

{{< callout type="warning" >}}
**ベータ版の注意**<br/>
ここで説明する機能は、今後のリリースで変更される場合があります。
{{< /callout >}}

メトリクスは 1 分、5 分、15 分のサンプリング周期で提供します。

## HTTP API
RESTful API でメトリクスを取得するには、次のエンドポイントを使用します。
```
http://127.0.0.1:5654/debug/statz?interval=[1m|5m|15m]&format=[json|html]
```
1 分、5 分、15 分から周期を選択できます。デフォルトでは、同じマシン（localhost）からのみアクセスできます。

デフォルトの出力形式は JSON です。`format=html` を指定すると、HTML の表を返します。

## TQL と CHART {#tql-with-chart}

次の例は、machbase-neo の HTTP レイテンシーの分布をチャートに表示します。
`FAKE( statz(period, metrics...) )` SRC 関数で時刻と値のペアを生成し、`CHART()` に渡します。

{{< tabs >}}
{{< tab name="CHART" >}}
{{< figure src="/neo/operations/img/metrics_http_latency.jpg" width="600" >}}
{{< /tab >}}
{{< tab name="コード" >}}
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

## メトリクス一覧
すべてのメトリクスは、選択したサンプリング周期に基づきます。1 分（`1m`）、5 分（`5m`）、15 分（`15m`）から選択します。

### HTTP

| メトリクス | 説明 |
|:----------------------------|:------------------------------------------------------------|
| `machbase:http:count` | HTTP リクエストの総数 |
| `machbase:http:latency_p50` | HTTP 応答レイテンシーの 50 パーセンタイル（中央値、ns） |
| `machbase:http:latency_p90` | HTTP 応答レイテンシーの 90 パーセンタイル（ns） |
| `machbase:http:latency_p99` | HTTP 応答レイテンシーの 99 パーセンタイル（ns） |
| `machbase:http:recv_bytes` | HTTP リクエストペイロードの合計サイズ |
| `machbase:http:send_bytes` | HTTP 応答ペイロードの合計サイズ |
| `machbase:http:status_1xx` | 1xx ステータスコードの HTTP 応答数 |
| `machbase:http:status_2xx` | 2xx ステータスコードの HTTP 応答数 |
| `machbase:http:status_3xx` | 3xx ステータスコードの HTTP 応答数 |
| `machbase:http:status_4xx` | 4xx ステータスコードの HTTP 応答数 |
| `machbase:http:status_5xx` | 5xx ステータスコードの HTTP 応答数 |

### MQTT

| メトリクス | 説明 |
|:------------------------------|:----------------------------------------------|
| `machbase:mqtt:recv_bytes` | 受信した合計バイト数（バイト） |
| `machbase:mqtt:send_bytes` | 送信した合計バイト数（バイト） |
| `machbase:mqtt:recv_pkts` | 受信した全種類の MQTT パケットの総数 |
| `machbase:mqtt:send_pkts` | 送信した全種類の MQTT パケットの総数 |
| `machbase:mqtt:recv_msgs` | 受信した PUBLISH メッセージの総数 |
| `machbase:mqtt:send_msgs` | 送信した PUBLISH メッセージの総数 |
| `machbase:mqtt:drop_msgs` | 低速なサブスクライバーのために破棄した PUBLISH メッセージの総数 |
| `machbase:mqtt:retained` | ブローカーで保持している retained メッセージ数 |
| `machbase:mqtt:subscriptions` | ブローカーに登録されているサブスクリプション数 |
| `machbase:mqtt:clients` | 現在接続中、または永続セッションを保持して登録されているクライアントの総数 |
| `machbase:mqtt:clients_connected` | 現在接続しているクライアント数 |
| `machbase:mqtt:clients_disconnected` | ブローカーに登録された永続セッションのクライアントのうち、現在切断されているクライアント数 |
| `machbase:mqtt:inflight` | 現在送信処理中（in-flight）のメッセージ数 |
| `machbase:mqtt:inflight_dropped` | 送信処理中に破棄されたメッセージ数 |

### TQL

| メトリクス | 説明 |
|:-----------------------------------------------|:------------------------------------------------|
| `machbase:tql:cache:count_[avg\|max\|min]` | TQL キャッシュの項目数 |
| `machbase:tql:cache:data_size_[avg\|max\|min]` | TQL キャッシュの合計サイズ（バイト） |
| `machbase:tql:cache:evictions` | キャッシュから追い出された項目数 |
| `machbase:tql:cache:insertions` | キャッシュに新しく挿入された項目数 |
| `machbase:tql:cache:hits` | キャッシュヒット数 |
| `machbase:tql:cache:misses` | キャッシュミス数 |

### データベースセッション {#database-sessions}

| メトリクス | 説明 |
|:---------------------------------------------------|:------------------------------------|
| `machbase:session:append:count` | 使用したアペンダーの総数 |
| `machbase:session:append:in_use` | 現在開いているアペンダー数 |
| `machbase:session:conn:count` | 使用した接続の総数 |
| `machbase:session:conn:in_use` | 現在開いている接続数 |
| `machbase:session:stmt:count` | 使用したステートメントの総数 |
| `machbase:session:stmt:in_use` | 現在開いているステートメント数 |
| `machbase:session:conn:use_time_[avg\|max\|min]` | 接続の使用時間（ns） |
| `machbase:session:conn:wait_time_[avg\|max\|min]` | 接続の取得にかかる待機・接続処理時間（ns） |
| `machbase:session:query:count` | クエリの総数（フェッチによる反復処理を使用するクエリ） |
| `machbase:session:query:exec_time_[avg\|max\|min]` | 準備済みステートメントの実行時間（ns） |
| `machbase:session:query:fetch_time_[avg\|max\|min]` | フェッチ時間（ns） |
| `machbase:session:query:wait_time_[avg\|max\|min]` | 反復処理の上限待ち時間（ns） |
| `machbase:session:query:hwm:elapse` | High Water Mark クエリの総経過時間（ns） |
| `machbase:session:query:hwm:exec_time` | High Water Mark クエリのステートメント実行時間（ns） |
| `machbase:session:query:hwm:fetch_time` | High Water Mark クエリのフェッチ時間（ns） |
| `machbase:session:query:hwm:wait_time` | High Water Mark クエリの反復処理の上限待ち時間（ns） |
| `machbase:session:query:hwm:sql_args` | High Water Mark クエリの SQL バインド変数（[]string） |
| `machbase:session:query:hwm:sql_text` | High Water Mark クエリの SQL テキスト（string） |

### Go

| メトリクス | 説明 |
|:-----------------------------------|:-------------------------------------|
| `go:heap_in_use_[avg\|max\|min]` | ヒープ使用量（バイト） |
| `go:cgo_call_[avg\|max\|min]` | CGO 関数の呼び出し数 |
| `go:goroutine_[avg\|max\|min]` | goroutine 数 |
