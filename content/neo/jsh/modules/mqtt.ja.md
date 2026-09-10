---
toc: true
title: "mqtt"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`mqtt`は、JSHのMQTTクライアントモジュールです。

JSHアプリケーションでは、通常は以下のように使用します。

```js
const mqtt = require('mqtt');
```

APIはイベント駆動で動作し、`Client`を作成すると自動的にブローカーへの接続を試みます。

## Client {#client}

MQTTクライアントオブジェクトです。

<h6>作成</h6>

```js
new Client(options)
```

<h6>オプション</h6>

| オプション                              | 型      | 既定値  | 説明 |
|:----------------------------------|:----------|:--------|:-----|
| servers                           | String[]  |         | MQTTブローカーURLの一覧（例：`tcp://127.0.0.1:1883`） |
| username                          | String    |         | ブローカー認証のユーザー名 |
| password                          | String    |         | ブローカー認証のパスワード |
| keepAlive                         | Number    | `30`    | Keep Alive（秒） |
| connectRetryDelay                 | Number    | `0`     | 再接続の遅延（ミリ秒） |
| cleanStartOnInitialConnection     | Boolean   | `false` | 初回接続時のMQTT v5 clean startを有効にするかどうか |
| connectTimeout                    | Number    | `0`     | 接続のタイムアウト（ミリ秒） |

## プロパティ {#속성}

### config {#config}

`client.config`は、ネイティブMQTTクライアントが使用する解析済みの接続設定を提供します。

代表的なフィールドは以下のとおりです。

| フィールド | 型 | 説明 |
|:-----|:-----|:-----|
| `serverUrls` | Array | 解析済みのブローカーURL一覧 |
| `connectUsername` | String | 設定したユーザー名 |
| `connectPassword` | byte data | バイト形式のパスワード |
| `keepAlive` | Number | Keep Aliveの間隔 |
| `reconnectBackoff(n)` | Function | 再接続の遅延を計算する関数 |
| `cleanStartOnInitialConnection` | Boolean | MQTT v5 clean startフラグ |
| `connectTimeout` | Number | 接続のタイムアウト |

```js
console.println(client.config.serverUrls);
console.println(client.config.keepAlive);
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const mqtt = require('mqtt');

const client = new mqtt.Client({
    servers: ['tcp://127.0.0.1:1883'],
    username: 'user',
    password: 'pass',
    keepAlive: 60,
    connectRetryDelay: 2000,
    connectTimeout: 10 * 1000,
    cleanStartOnInitialConnection: true,
});

client.on('open', () => {
    console.println('Connected');
    client.subscribe('test/topic', {
        qos: 0,
        properties: {
            subscriptionIdentifier: 7,
        },
    });
});

client.on('subscribed', (topic, reason) => {
    console.println('Subscribed:', topic, 'reason:', reason);
    client.publish('test/topic', 'Hello, MQTT!');
});

client.on('message', (msg) => {
    console.println('Message:', msg.topic, msg.payloadText);
    client.unsubscribe(msg.topic, {
        properties: {
            user: {
                source: 'example',
            },
        },
    });
});

client.on('unsubscribed', (topic, reason) => {
    console.println('Unsubscribed:', topic, 'reason:', reason);
    client.close();
});

client.on('error', (err) => {
    console.println('Error:', err.message);
});

client.on('close', () => {
    console.println('Disconnected');
});
```

## メソッド {#메서드}

### publish() {#publish}

トピックにメッセージを発行します。

<h6>構文</h6>

```js
publish(topic, message[, options])
```

<h6>パラメーター</h6>

- `topic` `String`
- `message` `String` | `Uint8Array` | `Object` | `Array`
- `options` `Object` (省略可能)

| オプション       | 型    | 既定値  | 説明 |
|:-----------|:--------|:--------|:-----|
| qos        | Number  | `0`     | QoSレベル |
| retain     | Boolean | `false` | Retainフラグ |
| properties | Object  |         | MQTT v5の発行プロパティ |

`options.properties`のフィールド：

| プロパティ                  | 型    | 説明 |
|:--------------------------|:--------|:-----|
| payloadFormat             | Number  | ペイロード形式インジケーター |
| messageExpiry             | Number  | 有効期間 |
| contentType               | String  | コンテンツタイプ |
| responseTopic             | String  | 応答トピック |
| correlationData           | String  | バイトに変換 |
| topicAlias                | Number  | トピックエイリアス |
| subscriptionIdentifier    | Number  | サブスクリプション識別子 |
| user                      | Object  | ユーザー定義プロパティ（`key: value`） |

<h6>戻り値</h6>

なし。結果は`published`または`error`イベントで通知します。

### subscribe() {#subscribe}

トピックを購読します。

<h6>構文</h6>

```js
subscribe(topic[, options])
```

<h6>パラメーター</h6>

- `topic` `String`
- `options` `Object` (省略可能)

| オプション               | 型    | 既定値 | 説明 |
|:-------------------|:--------|:-------|:-----|
| qos                | Number  | `1`    | QoSレベル |
| retainHandling     | Number  |         | MQTT v5のRetain処理 |
| noLocal            | Boolean | `false` | 同じクライアントが発行したメッセージの受信を抑制するかどうか |
| retainAsPublished  | Boolean | `false` | ブローカーのRetainフラグを保持するかどうか |
| properties         | Object  |         | MQTT v5の購読プロパティ |

`options.properties`のフィールド：

| プロパティ               | 型   | 説明 |
|:-----------------------|:-------|:-----|
| subscriptionIdentifier | Number | サブスクリプション識別子 |
| user                   | Object | ユーザー定義プロパティ（`key: value`） |

<h6>戻り値</h6>

なし。結果は`subscribed`または`error`イベントで通知します。

<h6>使用例</h6>

```js
client.subscribe('test/topic', {
    qos: 0,
    properties: {
        subscriptionIdentifier: 7,
        user: {
            source: 'example',
        },
    },
});
```

### unsubscribe() {#unsubscribe}

トピックの購読を解除します。

<h6>構文</h6>

```js
unsubscribe(topic[, options])
```

<h6>パラメーター</h6>

- `topic` `String`
- `options` `Object` (省略可能)

| オプション       | 型   | 説明 |
|:-----------|:-------|:-----|
| properties | Object | MQTT v5の購読解除プロパティ |

`options.properties`のフィールド：

| プロパティ | 型   | 説明 |
|:---------|:-------|:-----|
| user     | Object | ユーザー定義プロパティ（`key: value`） |

<h6>戻り値</h6>

なし。結果は`unsubscribed`または`error`イベントで通知します。

<h6>使用例</h6>

```js
client.unsubscribe('test/topic', {
    properties: {
        user: {
            source: 'example',
        },
    },
});
```

### close() {#close}

クライアント接続を閉じます。

<h6>構文</h6>

```js
close()
```

<h6>戻り値</h6>

なし。`close`イベントが発生します。

## イベント {#이벤트}

### open {#open}

クライアントの接続が完了すると発生します。

```js
client.on('open', () => { ... })
```

### message {#message}

購読したメッセージを受信すると発生します。

```js
client.on('message', (msg) => { ... })
```

`msg`のフィールド：

| プロパティ   | 型   | 説明 |
|:-----------|:-------|:-----|
| topic      | String | トピック名 |
| payload    | Buffer | バイナリデータを保持するメッセージペイロード |
| payloadText| String | UTF-8にデコードしたテキスト用の便利なフィールド |
| properties | Object | MQTT v5の発行プロパティ |

`msg.properties`のフィールド：

| プロパティ               | 型   | 説明 |
|:-----------------------|:-------|:-----|
| payloadFormat          | Number | ペイロード形式インジケーター |
| messageExpiry          | Number | 有効期間 |
| contentType            | String | コンテンツタイプ |
| responseTopic          | String | 応答トピック |
| correlationData        | Buffer | バイナリデータを保持する相関データ |
| topicAlias             | Number | トピックエイリアス |
| subscriptionIdentifier | Number | サブスクリプション識別子 |
| user                   | Object | ユーザー定義プロパティ |

テキストメッセージは、`msg.payloadText`または`msg.payload.toString()`で読み取れます。

バイナリメッセージは、`msg.payload`をそのまま使用します。

```js
client.on('message', (msg) => {
    console.println('Payload is buffer:', Buffer.isBuffer(msg.payload));
    console.println('Payload bytes:', Array.from(msg.payload).join(','));
});
```

MQTT v5の発行プロパティには、`msg.properties`でアクセスできます。

```js
client.on('message', (msg) => {
    console.println('Content type:', msg.properties.contentType);
    console.println('Response topic:', msg.properties.responseTopic);
    console.println('Correlation data:', msg.properties.correlationData.toString());
    console.println('User source:', msg.properties.user.source);
});
```

### subscribed {#subscribed}

購読のACKを受信すると発生します。

```js
client.on('subscribed', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` （MQTT理由コード）

### published {#published}

発行のACKを受信すると発生します。

```js
client.on('published', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` （MQTT理由コード）

### unsubscribed {#unsubscribed}

購読解除のACKを受信すると発生します。

```js
client.on('unsubscribed', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` （MQTT理由コード）

### error {#error}

接続、購読、購読解除、発行でエラーが発生すると通知します。

```js
client.on('error', (err) => { ... })
```

- `err` `Error`

接続前または`close()`の呼び出し後に、`publish()`、`subscribe()`、`unsubscribe()`を呼び出すと、`error`イベントでエラーを通知します。

### close {#close-1}

`close()`の呼び出し時に発生します。

```js
client.on('close', () => { ... })
```

## 動作に関する注意 {#동작-참고}

- `Client`は、コンストラクターで自動的にブローカーへの接続を試みます。
- JavaScriptラッパーは、可能な場合、受信したバイナリペイロードを`Buffer`に変換します。
- テキスト表現が可能なバッファーペイロードでは、`msg.payloadText`が自動的に設定されます。
- MQTT v5の`correlationData`は、バイナリデータを保持する`Buffer`として提供されます。

## MQTT v5の書き込みプロパティの例 {#mqtt-v5-쓰기-프로퍼티-예시}

以下の例は、MQTT v5 write APIのユーザープロパティを使い、`db/write/{table}`トピックにデータを書き込みます。

```js {linenos=table,linenostart=1}
const mqtt = require('mqtt');

const client = new mqtt.Client({
    servers: ['tcp://127.0.0.1:5653'],
});

const rows = [
    ['my-car', Date.now(), 32.1],
    ['my-car', Date.now() + 1000, 65.4],
];

client.on('open', () => {
    client.publish('db/write/EXAMPLE', rows, {
        qos: 1,
        properties: {
            user: {
                method: 'append',
                timeformat: 'ms',
            },
        },
    });
});

client.on('published', () => client.close());
client.on('error', (err) => console.println(err.message));
```
