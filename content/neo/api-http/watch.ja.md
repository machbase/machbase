---
toc: true
title: 最新データの監視
type: docs
weight: 21
---

## Server-Sent Eventsの利用 {#server-sent-events-활용}

クライアントは、サーバーからのストリーミングイベントを受信して、指定したテーブルの最新レコードをリアルタイムに取得できます。

Server-Sent Events（SSE）は、1つのHTTP接続を維持し、サーバーからクライアントに更新を継続的にプッシュする技術です。
ライブフィード、通知、リアルタイム分析など、継続的なデータ更新を必要とするアプリケーションで広く使用されています。

**Server-Sent Events（SSE）の特徴**

1. **単方向通信**：サーバーからクライアントに更新を送信できますが、同じ接続でクライアントからサーバーにデータを送信することはできません。
2. **持続的な接続**：クライアントは1つのHTTP接続を開いたままにし、サーバーは新しいデータが発生するたびに更新を送信します。
3. **自動再接続**：接続が切れると、クライアントが自動的に再接続を試みます。
4. **シンプルなAPI**：SSEは、Webアプリケーションで実装しやすいシンプルなAPIを提供します。

**SSEの動作**
1. **クライアントのリクエスト**：クライアントがサーバーにHTTPリクエストを送り、更新の受信を開始します。
2. **サーバーの送信**：サーバーは、MIMEタイプ`text/event-stream`の形式で更新ストリームを送信します。
3. **クライアントの処理**：クライアントは受信後すぐにデータを処理し、通常はユーザーインターフェースをリアルタイムに更新します。

Webブラウザーは、1つのホストに同時に開くSSE接続の数を制限します。リソースの枯渇を防ぎ、ネットワークリソースを効率的に使用するためです。主な点は以下のとおりです。

**ブラウザーのSSE接続制限**

1. **接続数の制限**：多くのブラウザーは、1ホストあたりのSSE接続を最大6本程度に制限します。
2. **リソース管理**：接続数の制限により、メモリやネットワーク帯域を管理し、単一ページがブラウザーやサーバーのリソースを過度に使用することを防ぎます。
3. **公平な利用**：この制限により、複数のタブやアプリケーションがネットワークリソースを公平に使用でき、特定のアプリケーションによる接続の独占を防ぎます。

堅牢で効率的なリアルタイムWebアプリケーションを実装するには、この制限を把握して守る必要があります。接続制限を考慮して設計すると、操作性とリソース利用を改善できます。


## 最新データの監視 {#최신-데이터-감시}

{{< neo_since ver="8.0.35" />}}

SSE（Server-Sent Events）のエンドポイントは以下のとおりです。

```
/db/watch/{table}
```

*watch* APIが対応するクエリパラメーターは以下のとおりです。

| パラメーター       | 既定値 | 説明                                                                    |
|:----------- |---------|:-------------------------------------------------------------------------------|
| timeformat  | `ns`     | 出力時刻の単位：s、ms、us、ns                                                  |
| tz          | `UTC`    | 出力のタイムゾーン：UTC、Local、地域指定                                             |
| period      | `3s`     | 更新間隔                                                                      |
| keep-alive  | `30s`    | 接続を維持してTCPタイムアウトを防ぐため、サーバーがコメントメッセージを送信する間隔 |


**タグテーブル**

対象がタグテーブルの場合は、`tag`パラメーターを必ず指定してください。

| パラメーター       | 既定値 | 説明                                                                 |
|:----------- |---------|:----------------------------------------------------------------------------|
| **tag**     |         | タグ名の配列                                                              |
| parallelism | `0`     | 並列処理数を指定します。<br/>0またはタグ数より大きい値を指定すると、タグ数を使用します。 |

{{< callout emoji="📌" >}}
このAPIは、指定した*period*内の各タグの最新データだけを配信します。<br/>
期間内に複数の値が取り込まれても、最新の値だけを送信します。
{{< /callout >}}


**ログテーブル**

| パラメーター       | 既定値 | 説明                                                                                         |
|:----------- |---------|:----------------------------------------------------------------------------------------------------|
| max-rows    | `20`   | 更新間隔ごとにサーバーが送信するレコードの最大数です。<br/>指定した数を超えるレコードは、その回の送信では省略します。<br/>上限は100です。 |

## cURL 例 {#curl-예시}

`curl`コマンドで、タグの最新値をストリームとして受信します。

```sh
curl -o - -v "http://127.0.0.1:5654/db/watch/example"\
"?tag=machbase:ps:cpu_percent&tag=machbase:ps:mem_percent&period=3s&timeformat=s"
```

クライアントが接続を維持している間、サーバーは継続してデータを送信します。

```sh
data: {"NAME":"machbase:ps:mem_percent","TIME":1774408680,"VALUE":54.96323903401693}

data: {"NAME":"machbase:ps:cpu_percent","TIME":1774408680,"VALUE":5.2510271571351295}

data: {"NAME":"machbase:ps:mem_percent","TIME":1774408740,"VALUE":52.28118896484375}

data: {"NAME":"machbase:ps:cpu_percent","TIME":1774408740,"VALUE":4.519490930962651}

^C
```

## JavaScriptの例 {#자바스크립트-예시}

```html
<html>
<body>
    <h1>Server-Sent Events 例</h1>
    <div id="messages"></div>
    <script>
        // EventSourceインスタンスを作成します。
        const addr = 'http://127.0.0.1:5654/db/watch/EXAMPLE';
        const params = 'tag=machbase:ps:cpu_percent&tag=machbase:ps:mem_percent&period=3s&keep-alive=30s&timeformat=default';
        const eventSource = new EventSource(`${addr}?${params}`);

        // メッセージを表示するdivを取得します。
        const messagesDiv = document.getElementById('messages');

        // 受信したメッセージを処理します。
        eventSource.onmessage = function (event) {
            // 新しい要素を作成します。
            const pre = document.createElement('pre');
            const msg = JSON.parse(event.data);
            // イベントデータをテキストとして設定します。
            pre.textContent = event.data + ' => ' + msg.NAME + ':' + msg.VALUE;
            // 要素をメッセージ用divに追加します。
            messagesDiv.appendChild(pre);
        };

        // エラーを処理します。
        eventSource.onerror = function (event) {
            console.error('EventSource failed:', event);
        };
    </script>
</body>
</html>
```

## Pythonの例 {#파이썬-예시}

```python
import requests
import sseclient

# Server-Sent Eventsのエンドポイントに接続するURLを定義します。
url = 'http://127.0.0.1:5654/db/watch/EXAMPLE'
params = {
    'tag': ['machbase:ps:cpu_percent', 'machbase:ps:mem_percent'],
    'period': '3s',
    'keep-alive': '30s',
    'timeformat': 'default'
}

# ストリーミングリクエストを作成します。
response = requests.get(url, params=params, stream=True)

# sseclientでServer-Sent Eventsを処理します。
client = sseclient.SSEClient(response)

# 受信したメッセージを出力します。
for event in client.events():
    print(event.data)
```
