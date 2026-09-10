---
toc: true
title: "nats"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`nats`モジュールは、JSHアプリケーション用のNATSクライアントを提供します。
`mqtt`モジュールと同様にイベント駆動で動作し、`Client`の作成時に自動的に接続を開始します。

一般的な使用方法は以下のとおりです。

```js
const nats = require('nats');
```

## Client {#client}

NATSクライアントオブジェクトです。

<h6>作成</h6>

```js
new Client(options)
```

<h6>オプション</h6>

| オプション | 型 | 説明 |
|:-----|:-----|:-----|
| `servers` | String[] | `nats://127.0.0.1:4222`などのNATSサーバーURLの一覧 |
| `name` | String | 接続名 |
| `user` | String | 認証ユーザー |
| `password` | String | 認証パスワード |
| `token` | String | 認証トークン |
| `noRandomize` | Boolean | サーバーのランダム選択を無効化 |
| `noEcho` | Boolean | 自身が発行したメッセージのエコーを無効化 |
| `verbose` | Boolean | verboseプロトコル動作を有効化 |
| `pedantic` | Boolean | pedanticプロトコル検査を有効化 |
| `allowReconnect` | Boolean | 再接続を許可 |
| `maxReconnect` | Number | 再接続の最大試行回数 |
| `reconnectWait` | Number | 再接続の待機時間（ミリ秒） |
| `timeout` | Number | 接続のタイムアウト（ミリ秒） |
| `drainTimeout` | Number | drainのタイムアウト（ミリ秒） |
| `flusherTimeout` | Number | フラッシュのタイムアウト（ミリ秒） |
| `pingInterval` | Number | pingの間隔（ミリ秒） |
| `maxPingsOut` | Number | 応答待ちのpingの最大数 |
| `retryOnFailedConnect` | Boolean | 初回接続の失敗時に再試行 |
| `skipHostLookup` | Boolean | ホスト検索の最適化をスキップ |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const nats = require('nats');

const client = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
    name: 'test-client',
    allowReconnect: true,
    maxReconnect: 10,
    reconnectWait: 2000,
    timeout: 10 * 1000,
});
```

## プロパティ {#속성}

### config {#config}

`client.config`は、解析済みのネイティブNATS設定を提供します。

代表的なフィールドは以下のとおりです。

- `servers`
- `name`
- `allowReconnect`
- `maxReconnect`
- `reconnectWait`
- `timeout`

```js
console.println(client.config.servers);
console.println(client.config.timeout);
```

## メソッド {#메서드}

### publish() {#publish}

サブジェクトにメッセージを発行します。

<h6>構文</h6>

```js
publish(subject, message[, options])
```

<h6>パラメーター</h6>

- `subject` `String`
- `message` `String` | `Uint8Array` | `Object` | `Array`
- `options` `Object` (省略可能)

対応する`options`のフィールド：

| オプション | 型 | 説明 |
|:-----|:-----|:-----|
| `reply` | String | 要求・応答方式で使用する応答サブジェクト |

ObjectとArrayは、発行前にJSONにエンコードします。

<h6>戻り値</h6>

なし。結果は`published`または`error`イベントで通知します。

### subscribe() {#subscribe}

サブジェクトを購読します。

<h6>構文</h6>

```js
subscribe(subject[, options])
```

<h6>パラメーター</h6>

- `subject` `String`
- `options` `Object` (省略可能)

対応する`options`のフィールド：

| オプション | 型 | 説明 |
|:-----|:-----|:-----|
| `queue` | String | キューサブスクリプション用のキューグループ名 |

<h6>戻り値</h6>

なし。結果は`subscribed`または`error`イベントで通知します。

### close() {#close}

クライアント接続を閉じます。

<h6>構文</h6>

```js
close()
```

## イベント {#이벤트}

### open {#open}

接続が完了すると発生します。

```js
client.on('open', () => { ... })
```

### message {#message}

購読したメッセージを受信すると発生します。

```js
client.on('message', (msg) => { ... })
```

`msg`のフィールド：

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| `topic` | String | MQTT形式のハンドラーとの互換性のためのサブジェクトの別名 |
| `subject` | String | NATSサブジェクト |
| `reply` | String | 要求・応答処理で使用する応答サブジェクト |
| `payload` | String | メッセージのペイロード |

### subscribed {#subscribed}

サーバーが購読を受け付けると発生します。

```js
client.on('subscribed', (subject, reason) => { ... })
```

- `subject` `String`
- `reason` `Number`

現在の実装では、購読成功時に`1`を使用します。

### published {#published}

発行リクエストが完了すると発生します。

```js
client.on('published', (subject, reason) => { ... })
```

- `subject` `String`
- `reason` `Number`

現在の実装では、発行の成功時に`0`を使用します。

### error {#error}

接続、購読、発行の失敗時に発生します。

```js
client.on('error', (err) => { ... })
```

- `err` `Error`

### close {#close-1}

`close()`を呼び出すと発生します。

```js
client.on('close', () => { ... })
```

## 基本的な発行・購読の例 {#기본-pubsub-예시}

```js {linenos=table,linenostart=1}
const nats = require('nats');

const client = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
    name: 'test-client',
    timeout: 10 * 1000,
});

client.on('open', () => {
    console.println('Connected');
    client.subscribe('test.subject');
});

client.on('subscribed', (subject, reason) => {
    console.println('Subscribed to:', subject, 'reason:', reason);
    client.publish('test.subject', 'Hello, NATS!');
});

client.on('message', (msg) => {
    console.println('Message received on subject:', msg.subject, 'payload:', msg.payload);
    client.close();
});

client.on('close', () => {
    console.println('Disconnected');
});
```

## 要求・応答の例 {#requestreply-예시}

要求・応答処理では、応答サブジェクトを先に購読し、`options.reply`を指定して発行します。

```js {linenos=table,linenostart=1}
const nats = require('nats');

const handler = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
});
handler.on('open', () => {
    handler.subscribe('request.subject');
});
handler.on('message', (msg) => {
    handler.publish(msg.reply, 'pong');
});

const requester = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
});
requester.on('open', () => {
    requester.subscribe('reply.subject');
    requester.publish('request.subject', 'ping', { reply: 'reply.subject' });
});
requester.on('message', (msg) => {
    console.println(msg.payload);
    requester.close();
    handler.close();
});
```

## 動作に関する注意 {#동작-참고}

- `Client`は、コンストラクターで自動的に接続を開始します。
- キューサブスクリプションは、`subscribe(subject, { queue: 'workers' })`で使用できます。
- 接続が開く前に`publish()`または`subscribe()`を呼び出すと、`error`イベントが発生します。
- 現在の実装では、メッセージのペイロードは文字列で提供されます。
