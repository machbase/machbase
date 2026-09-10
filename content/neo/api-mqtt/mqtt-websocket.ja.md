---
toc: true
title: JavaScript & WebSocket
type: docs
weight: 63
---

JavaScriptクライアントでは、[MQTT.jsのGitHubリポジトリ](https://github.com/mqttjs/MQTT.js)のMQTT.jsライブラリを使用します。

## Node.js {#nodejs}

`mqtt.js`ライブラリをインストールします。

```sh
npm install mqtt --save
```

`main.js`ファイルを作成します。

```js
const mqtt = require("mqtt");

const client = mqtt.connect("mqtt://127.0.0.1:5653", {
    clean: true,
    connectTimeout: 3000,
    autoUseTopicAlias: true,
    protocolVersion: 5,
});

client.on("connect", () => {
    client.subscribe("db/reply/#", (err) => {
        if (!err) {
            const req = {
                q: "SELECT * FROM example where name = 'neo_cpu.percent' limit 3",
                format: "box",
                timeformat: "default",
                tz: "local",
                precision: 2
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

`node`コマンドで`main.js`を実行します。

```sh
$ node main.js

+-----------------+-------------------------+-------+
| NAME            | TIME                    | VALUE |
+-----------------+-------------------------+-------+
| neo_cpu.percent | 2024-09-06 14:46:19.852 | 69.40 |
| neo_cpu.percent | 2024-09-06 14:46:22.853 | 26.40 |
| neo_cpu.percent | 2024-09-06 14:46:25.852 | 42.80 |
+-----------------+-------------------------+-------+
```

## WebSocket {#websocket}

Machbase Neo v8.0.28以降は、WebSocket経由のMQTTに対応しています。

プロジェクトにMQTT.jsを組み込むには、以下のCDNスクリプトタグを追加します。

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
````

既定のWebSocketエンドポイントは、Machbase NeoのHTTPサーバーが提供する`ws://127.0.0.1:5654/web/api/mqtt`です。


```html
<html>

<head>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
</head>

<body>
    <script type="text/javascript">
        const url = 'ws://localhost:5654/web/api/mqtt'

        // MQTTクライアントのインスタンスを作成します。
        const options = {
            // クリーンセッション
            clean: true,
            connectTimeout: 4000,
        }
        const client = mqtt.connect(url, options)
        client.on('connect', function () {
            console.log('Connected')
            // クエリ結果を受信するために'db/reply'トピックを購読します。
            client.subscribe('db/reply', function (err) {
                if (!err) {
                    // 'db/query'トピックにクエリを発行します。
                    const req = {q: "SELECT * FROM example limit 10", format:"box", precision: 2}
                    client.publish('db/query', JSON.stringify(req))
                }
            })
        })

        // メッセージを受信します。
        client.on('message', function (topic, message) {
            // 受信したメッセージを画面に表示します。
            document.getElementById("rspQuery").innerHTML = '<pre>'+message.toString()+'</pre>'
            client.end()
        })

    </script>
    <div id="rspQuery"></div>
</body>

</html>
```
