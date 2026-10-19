---
title: メトリクス
type: docs
weight: 101
toc: true
---

{{< neo_since ver="8.7.0" />}}

Machbase Neo はサーバーの状態とリクエスト処理の統計を収集し、
`SYS._NEO_STATZ` テーブルに保存します。
SQL で必要なメトリクスと期間を指定して取得し、
TQL の `SQL()` と `CHART()` を組み合わせて可視化できます。

このドキュメントの例は、`sys` ユーザーで接続して実行してください。
`_NEO_STATZ` はサーバーが自動的に作成・管理するため、
手動でテーブルを作成したり、データを挿入したりする必要はありません。

## 保存構造と収集間隔

`_NEO_STATZ` は次の 3 つのカラムを持つ通常のトランザクションテーブルです。
TAG テーブルではありません。

| カラム | 型 | 説明 |
|:-------|:---|:-----|
| `NAME` | `VARCHAR(100)` | メトリクスのキー |
| `TIME` | `DATETIME` | 1 分間の集計区間の開始時刻 |
| `VALUE` | `DOUBLE` | その区間のメトリクス値 |

`(NAME, TIME)` には一意インデックスがあります。
進行中の区間の値は同じ行を更新し、次の区間に移ると新しい行を保存します。

- **収集間隔:** システム状態など定期的に収集する項目は 10 秒ごとに測定します。
  HTTP リクエストの統計は、リクエストが処理されるときに収集します。
- **保存解像度:** 1 分です。10 秒ごとに収集しても、各サンプルを別の行には保存しません。
- **現在の区間:** まだ完了していない 1 分間の区間も保存するため、
  同じ `TIME` の `VALUE` が変化することがあります。
- **保持期間:** 8 日間です。書き込み処理中に 15 分間隔で古いデータを削除するため、
  8 日を過ぎた行が次の削除処理まで残ることがあります。

### 値の解釈

すべての `VALUE` がサーバー起動後の累積値や 1 分間の平均値というわけではありません。
項目の収集方法に応じて、次のように解釈してください。

| 方法 | 保存される値 | 例 |
|:-----|:-------------|:---|
| 状態値（Gauge） | 区間内で最後に測定した値 | `runtime:heap_inuse`, `sys:session:count` |
| 合計（Counter） | 区間内で収集した値の合計 | `http:count`, `http:send_bytes` |
| 累積値の差分（Odometer） | 累積カウンターの基準値に対する最後の値の差分 | `sys:execute:count`, `sys:pool:wait_count` |
| 分布（Histogram） | サンプル数とパーセンタイル | `http:latency`, `http:latency:p99` |

たとえば、`http:latency` はレイテンシーではなく、**その区間のサンプル数**です。
実際のレイテンシーは `http:latency:p50`、`http:latency:p90`、
`http:latency:p99` に保存されます。
単位が `ns` の値を `1000000` で割ると `ms` に変換できます。

リクエストがなかった区間には、HTTP メトリクスの行が存在しないことがあります。
**行が存在しないことと、値が 0 であることは異なります。**
現在の区間の合計・差分・パーセンタイルは、その時点までの値です。
1 分間の区間の差分を、そのまま秒あたりの処理量として解釈しないでください。

## メトリクスのキーを探す

収集されるキーは、設定や使用中の機能によって異なります。
まず、現在のサーバーに実際に保存されているキーを確認してください。

```sql
SELECT NAME FROM _NEO_STATZ GROUP BY NAME ORDER BY NAME;
```

特定のカテゴリだけを確認するには、`LIKE` で絞り込みます。

```sql
SELECT NAME FROM _NEO_STATZ WHERE NAME LIKE 'http:%'
GROUP BY NAME
ORDER BY NAME;
```

各キーの保存期間と行数をまとめて確認することもできます。

```sql
SELECT NAME, MIN(TIME) AS FIRST_TIME, MAX(TIME) AS LAST_TIME, COUNT(*) AS POINTS
FROM _NEO_STATZ
GROUP BY NAME
ORDER BY NAME;
```

HTTP 関連のキーは、リクエストが処理された後に現れます。
MQTT 関連のキーは MQTT ブローカーの使用中に、
ロールアップ関連のキーは収集対象のロールアップがある場合に現れます。
過去に保存されたキーは、その機能を使用しなくなっても保持期間中は取得できる場合があります。

## SQL で取得する

次のクエリは、直近 1 時間の Go ヒープ使用量を時刻順に取得します。
`SYSDATE - 1h` を `SYSDATE - 30m`、`SYSDATE - 1d` などに変更すると、
取得期間を調整できます。

```sql
SELECT TIME, VALUE
FROM _NEO_STATZ
WHERE NAME = 'runtime:heap_inuse'
  AND TIME >= SYSDATE - 1h
ORDER BY TIME;
```

進行中の 1 分間の区間を除き、完了した区間だけを取得するには、次の条件を追加します。

```sql
SELECT TIME, VALUE
FROM _NEO_STATZ
WHERE NAME = 'runtime:heap_inuse'
  AND TIME >= SYSDATE - 1h
  AND TIME < DATE_TRUNC('minute', SYSDATE)
ORDER BY TIME;
```

## TQL で可視化する

Web UI の TQL エディターで次の例を実行してください。
`SQL()` で取得した `TIME` と値を `list()` で組み合わせると、
時間軸チャートの 1 点になります。
別のメトリクスを描画するには、`NAME` 条件、単位変換、チャートの名前を変更してください。
取得結果は `ORDER BY TIME` で並べ替えます。

### ヒープ使用量

バイト単位のヒープ使用量を MiB に変換して表示します。

```js
SQL(`
    SELECT TIME, VALUE / 1048576.0 AS HEAP_MIB
    FROM _NEO_STATZ
    WHERE NAME = 'runtime:heap_inuse'
      AND TIME >= SYSDATE - 1h
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "MiB" },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "Go heap", type: "line", showSymbol: false, data: column(1) }
        ]
    })
)
```

### データベース接続プール

異なるキーを 1 つのチャートに表示するには、
`CASE` と `GROUP BY TIME` で同じ時刻の値を 1 行にまとめます。
次の例は、開いている接続数と使用中の接続数を比較します。
ここでの `MAX()` は異なる時刻間の最大値を求めるのではなく、
同じ `TIME` で各キーに対応する値を選択する役割を持ちます。

```js
SQL(`
    SELECT TIME,
        MAX(CASE WHEN NAME = 'sys:pool:open' THEN VALUE END) AS OPEN_CONNS,
        MAX(CASE WHEN NAME = 'sys:pool:in_use' THEN VALUE END) AS IN_USE_CONNS
    FROM _NEO_STATZ
    WHERE NAME IN ('sys:pool:open', 'sys:pool:in_use')
      AND TIME >= SYSDATE - 1h
    GROUP BY TIME
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Connections", minInterval: 1 },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "Open", type: "line", showSymbol: false, data: column(1) },
            { name: "In use", type: "line", showSymbol: false, data: column(2) }
        ]
    })
)
```

### HTTP 応答レイテンシー

すべての HTTP リクエストの p50・p90・p99 レイテンシーを ms 単位で比較します。
パーセンタイルは、各 1 分間の区間で収集されたサンプルの分布を表します。
リクエストがないと結果が空になる場合があるため、
先にサーバーの HTTP API を使用してから実行してください。

```js
SQL(`
    SELECT TIME,
        MAX(CASE WHEN NAME = 'http:latency:p50' THEN VALUE END) / 1000000.0 AS P50,
        MAX(CASE WHEN NAME = 'http:latency:p90' THEN VALUE END) / 1000000.0 AS P90,
        MAX(CASE WHEN NAME = 'http:latency:p99' THEN VALUE END) / 1000000.0 AS P99
    FROM _NEO_STATZ
    WHERE NAME IN ('http:latency:p50', 'http:latency:p90', 'http:latency:p99')
      AND TIME >= SYSDATE - 1h
    GROUP BY TIME
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "ms" },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "p50", type: "line", showSymbol: false, data: column(1) },
            { name: "p90", type: "line", showSymbol: false, data: column(2) },
            { name: "p99", type: "line", showSymbol: false, data: column(3) }
        ]
    })
)
```

クエリのキーを `http:query:latency:p50` などに変更すると、
`/db/query` リクエストだけを比較できます。
取得期間を延ばしても、保存された 1 分の解像度は変わりません。
また、複数区間の p99 を単純平均しても、期間全体の p99 にはなりません。

## 主なメトリクス一覧

以下は、サーバーに組み込まれている主な収集項目です。
実際にキーが存在するかどうかは、前述の SQL で確認してください。
表の「状態」は最後の測定値、「合計」は区間内の合計、
「差分」は累積カウンターの差分を意味します。

### システムと Go ランタイム

CPU・メモリ使用率と TCP 接続数は、ホストシステムを対象とします。
Go ランタイムの項目は、Machbase Neo プロセスを対象とします。

| キー | 方法 | 説明 / 単位 |
|:-----|:-----|:------------|
| `ps:cpu_percent` | 状態 | ホストの CPU 使用率 / % |
| `ps:mem_percent` | 状態 | ホストのメモリ使用率 / % |
| `runtime:goroutines` | 状態 | Go のゴルーチン数 |
| `runtime:heap_inuse` | 状態 | Go ヒープの使用中スパンのサイズ / bytes |
| `runtime:cgo_call` | 差分 | cgo 呼び出し回数 |
| `netstat:tcp_established` | 状態 | ESTABLISHED の TCP 接続数 |
| `netstat:tcp_fin_wait1` | 状態 | FIN_WAIT1 の TCP 接続数 |
| `netstat:tcp_fin_wait2` | 状態 | FIN_WAIT2 の TCP 接続数 |
| `netstat:tcp_time_wait` | 状態 | TIME_WAIT の TCP 接続数 |
| `netstat:tcp_close_wait` | 状態 | CLOSE_WAIT の TCP 接続数 |
| `netstat:tcp_listen` | 状態 | LISTEN の TCP ソケット数 |

### データベース

| キー | 方法 | 説明 / 単位 |
|:-----|:-----|:------------|
| `sys:sysmem` | 状態 | `V$SYSMEM` の `USAGE` の合計 / bytes |
| `sys:session:count` | 状態 | 閉じられていない DB セッション数 |
| `sys:append:open` | 差分 | APPEND を開いた回数 |
| `sys:append:close` | 差分 | APPEND を閉じた回数 |
| `sys:append:data:success` | 差分 | `APPEND_DATA_SUCCESS` の増加量 |
| `sys:append:data:failure` | 差分 | `APPEND_DATA_FAILURE` の増加量 |
| `sys:execute:count` | 差分 | `V$SYSTIME` の `EXECUTE` 実行回数の増加量 |
| `sys:execute:time:avg` | 状態 | セッション間の `V$SESTIME.MAX_MSEC` の平均 / ns |
| `sys:execute:time:max` | 状態 | セッション間の `V$SESTIME.MAX_MSEC` の最大値 / ns |

`sys:execute:time:avg` は、個々の SQL 実行時間全体の平均ではなく、
各セッションの `MAX_MSEC` を平均した結果です。

### サーバー内部の接続プール

サーバーが使用するデフォルトの `database/sql` 接続プールの統計です。
サーバー全体の DB セッション数を表す `sys:session:count` と区別してください。

| キー | 方法 | 説明 / 単位 |
|:-----|:-----|:------------|
| `sys:pool:max_open` | 状態 | 最大接続数の設定。0 は無制限 |
| `sys:pool:open` | 状態 | 開いている接続数 |
| `sys:pool:in_use` | 状態 | 使用中の接続数 |
| `sys:pool:idle` | 状態 | アイドル接続数 |
| `sys:pool:wait_count` | 差分 | 接続を待機した回数 |
| `sys:pool:wait_duration` | 差分 | 接続待機時間の合計 / ns |
| `sys:pool:max_idle_closed` | 差分 | 最大アイドル接続数の制限により閉じられた接続数 |
| `sys:pool:max_idletime_closed` | 差分 | 最大アイドル時間の超過により閉じられた接続数 |
| `sys:pool:max_lifetime_closed` | 差分 | 最大存続時間の超過により閉じられた接続数 |

### HTTP

リクエスト数・バイト数・ステータスコード別の回数は、区間内の合計です。
レイテンシーの基本キーにはサンプル数を、
`:p50`・`:p90`・`:p99` のキーには ns 単位のレイテンシーを保存します。

| キー | 説明 |
|:-----|:-----|
| `http:count` | HTTP リクエストの総数 |
| `http:latency` | HTTP リクエスト全体のレイテンシーのサンプル数 |
| `http:latency:p50`,<br/> `http:latency:p90`,<br/> `http:latency:p99` | HTTP リクエスト全体のレイテンシーのパーセンタイル / ns |
| `http:write:count` | `/db/write` リクエスト数 |
| `http:write:latency` | `/db/write` リクエストのレイテンシーのサンプル数 |
| `http:write:latency:p50`,<br/> `http:write:latency:p90`,<br/> `http:write:latency:p99` | `/db/write` リクエストのレイテンシーのパーセンタイル / ns |
| `http:query:count` | `/db/query` リクエスト数 |
| `http:query:latency` | `/db/query` リクエストのレイテンシーのサンプル数 |
| `http:query:latency:p50`,<br/> `http:query:latency:p90`,<br/> `http:query:latency:p99` | `/db/query` リクエストのレイテンシーのパーセンタイル / ns |
| `http:tql:count` | `/db/tql` リクエスト数 |
| `http:tql:latency` | `/db/tql` リクエストのレイテンシーのサンプル数 |
| `http:tql:latency:p50`,<br/> `http:tql:latency:p90`,<br/> `http:tql:latency:p99` | `/db/tql` リクエストのレイテンシーのパーセンタイル / ns |
| `http:recv_bytes` | 収集されたリクエスト本文サイズの合計 / bytes |
| `http:send_bytes` | 収集されたレスポンス本文サイズの合計 / bytes |
| `http:status_1xx`, `http:status_2xx`,<br/> `http:status_3xx`, `http:status_4xx`,<br/> `http:status_5xx` | ステータスコードのクラス別レスポンス数 |

### MQTT

以下の項目はすべて、ブローカー統計の最後の測定値です。
特に受信・送信バイト数やメッセージ数などの累積統計も、
HTTP の区間内合計とは異なり、**ブローカーが提供する累積値そのもの**を保存します。

| キー | 説明 / 単位 |
|:-----|:------------|
| `mqtt:recv_bytes` | 累積受信バイト数 / bytes |
| `mqtt:send_bytes` | 累積送信バイト数 / bytes |
| `mqtt:recv_msgs` | 累積受信 PUBLISH メッセージ数 |
| `mqtt:send_msgs` | 累積送信 PUBLISH メッセージ数 |
| `mqtt:drop_msgs` | 累積ドロップメッセージ数 |
| `mqtt:recv_pkts` | 累積受信パケット数 |
| `mqtt:send_pkts` | 累積送信パケット数 |
| `mqtt:retained` | 保持中の retain メッセージ数 |
| `mqtt:subscriptions` | サブスクリプション数 |
| `mqtt:clients` | 接続中、またはセッションが保持されているクライアント数 |
| `mqtt:clients_connected` | 接続中のクライアント数 |
| `mqtt:clients_disconnected` | 切断されているがセッションが保持されているクライアント数 |
| `mqtt:inflight` | 送信中のメッセージ数 |
| `mqtt:inflight_dropped` | 送信中にドロップされた累積メッセージ数 |

### TQL キャッシュ

以下の項目も最後の測定値を保存します。
`items` は現在の項目数で、それ以外はキャッシュが集計した累積回数です。

| キー | 説明 |
|:-----|:-----|
| `tql:cache:items` | 現在のキャッシュ項目数 |
| `tql:cache:evictions` | キャッシュから削除された累積項目数 |
| `tql:cache:insertions` | キャッシュへの累積挿入回数 |
| `tql:cache:hits` | 累積キャッシュヒット数 |
| `tql:cache:misses` | 累積キャッシュミス数 |

### ロールアップ

`<rollup_table>` には、小文字に変換されたロールアップテーブル名が入ります。
すべての項目は最後の測定値を保存します。

| キー | 説明 / 単位 |
|:-----|:------------|
| `sys:rollup:<rollup_table>:gap` | 元テーブルとロールアップ処理位置の RID 差分の合計 |
| `sys:rollup:<rollup_table>:last_elapse` | そのロールアップの `LAST_ELAPSED_MSEC` の最大値を ns に変換した値 |
| `sys:rollup_global:gap` | 収集対象の全ロールアップの gap の合計 |
| `sys:rollup_global:last_elapse` | 直前の収集間隔内に実行されたロールアップの最大実行時間 / ns |

`sys:rollup_global:last_elapse` は、直前の収集間隔内に実行されたロールアップがなければ 0 です。
