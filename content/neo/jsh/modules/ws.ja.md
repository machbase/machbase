---
toc: true
title: "ws"
type: docs
weight: 100
---

{{< neo_since ver="8.5.2" />}}

`ws`モジュールは、JSHアプリケーション用のWebSocketクライアント/サーバーAPIを提供します。
GoのネイティブWebSocket実装を基盤とする、`WebSocket`クラスと`WebSocketServer`クラスを提供します。

一般的な使用方法は以下のとおりです。

```js
const { WebSocket, WebSocketServer } = require('ws');
```

## WebSocket {#websocket}

WebSocketクライアント接続を作成します。

<h6>構文</h6>

```js
new WebSocket(url)
new WebSocket(url, protocol)
new WebSocket(url, protocols)
```

<h6>パラメーター</h6>

- `url` `String`: `ws://host:port/path`、`wss://host:port/path`などのWebSocketサーバーアドレス
- `protocol` `String`: 要求するサブプロトコル1つ
- `protocols` `String[]`: 要求するサブプロトコルの一覧

`url`がない場合や文字列以外の場合、コンストラクターは`TypeError`を発生させます。

## プロパティ {#속성}

| プロパティ | 型 | 説明 |
|:-----|:-----|:-----|
| `url` | String | コンストラクターに渡した元のWebSocket URL |
| `protocol` | String | ネゴシエートしたサブプロトコル。ない場合は空文字列 |
| `readyState` | Number | 現在の接続状態 |

### readyStateの値 {#readystate-값}

- `WebSocket.CONNECTING` = `0`
- `WebSocket.OPEN` = `1`
- `WebSocket.CLOSING` = `2`
- `WebSocket.CLOSED` = `3`

### メッセージ型の定数 {#메시지-타입-상수}

- `WebSocket.TextMessage` = `1`
- `WebSocket.BinaryMessage` = `2`

## send() {#send}

サーバーにメッセージを送信します。

<h6>構文</h6>

```js
ws.send(data)
```

<h6>パラメーター</h6>

- `data` `String`: 送信するテキストメッセージ

現在のJSH実装では、`send()`はテキストメッセージの使用を前提に設計されています。

ソケットが開いていない場合は、`error`イベントが発生します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('open', () => {
    ws.send('Hello, server');
});
```

## close() {#close}

現在の接続を閉じます。

<h6>構文</h6>

```js
ws.close()
```

`close()`を呼び出すと、ソケットは`CLOSING`を経て`CLOSED`に移行し、`close`イベントを発生させます。

## イベント {#이벤트}

`WebSocket`は`EventEmitter`を継承しているため、`on()`や`addListener()`などの一般的なイベントリスナーの方式を使用できます。

### open {#open}

クライアントの接続成功後に発生します。

```js
ws.on('open', () => {
    console.println('connected');
});
```

### close {#close-1}

接続が閉じると発生します。

```js
ws.on('close', () => {
    console.println('closed');
});
```

### message {#message}

サーバーからメッセージが届くと発生します。

コールバックは、以下のフィールドを持つイベント形式のオブジェクトを受け取ります。

| フィールド | 型 | 説明 |
|:-----|:-----|:-----|
| `type` | Number | `WebSocket.TextMessage`、`WebSocket.BinaryMessage`などのメッセージ型 |
| `data` | Stringまたはバイトデータ | メッセージのペイロード。テキストメッセージは文字列で提供されます。 |

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('message', (evt) => {
    console.println(evt.data);
});
```

### error {#error}

接続または送信処理が失敗すると発生します。

```js
ws.on('error', (err) => {
    console.println(err.message);
});
```

## WebSocketServer {#websocketserver}

WebSocketサーバーを作成し、既存の`http.Server`に接続します。

<h6>構文</h6>

```js
new WebSocketServer(options)
```

<h6>主なオプション</h6>

- `server`: 接続する`http.Server`インスタンス。必須。
- `path`: 受け付けるWebSocketパス。既定値は`/`。
- `clientTracking`: `true`の場合、`clients`集合を保持します。既定値は`true`。
- `verifyClient({ origin, req })`: ハンドシェイクを受け付けるかどうかを同期的に決定します。`false`を返すとリクエストを拒否します。
- `handleProtocols(protocols, req)`: 要求されたサブプロトコルの一覧から、選択する値を返します。

<h6>プロパティ</h6>

| プロパティ | 型 | 説明 |
|:-----|:-----|:-----|
| `server` | http.Server | 接続したHTTPサーバー |
| `path` | String | 受け付けるWebSocketパス |
| `clients` | Set | 接続中のクライアント集合。`clientTracking === false`の場合は`null` |

### WebSocketServer イベント {#websocketserver-이벤트}

- `connection(socket, request)`
- `error(err)`
- `close()`

### 接続リクエストオブジェクト {#connection-request-object}

`connection`イベントの`request`は、Node.jsの`IncomingMessage`に似たヘルパーオブジェクトです。

主なプロパティ：

- `url`
- `method`
- `headers`
- `rawHeaders`
- `path`
- `host`
- `requestUri`
- `httpVersion`
- `complete`
- `remoteAddress`
- `socket.remoteAddress`

主なメソッド：

- `query(name)`
- `getHeader(name)`
- `hasHeader(name)`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const http = require('http');
const { WebSocketServer } = require('ws');

const server = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
const wss = new WebSocketServer({
    server,
    path: '/ws',
    verifyClient: ({ req }) => req.query('token') === 'allow',
    handleProtocols: (protocols) => {
        if (protocols.indexOf('machbase.rpc') >= 0) {
            return 'machbase.rpc';
        }
        return false;
    },
});

wss.on('connection', (socket, request) => {
    console.println(request.path, request.httpVersion, socket.protocol);
    socket.on('message', (event) => {
        socket.send('echo:' + event.data);
    });
});

server.serve();
```

## 使用例 {#사용-예시}

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');

ws.on('open', () => {
    console.println('websocket open');
    ws.send('test message');
});

ws.on('message', (evt) => {
    console.println(evt.data);
    ws.close();
});

ws.on('close', () => {
    console.println('websocket closed');
});
```

## 動作に関する注意 {#동작-참고}

- クライアント接続は、コンストラクター内で非同期に開始します。
- 接続失敗は、`error`イベントで通知します。
- 受信メッセージはテキストまたはバイナリですが、JavaScriptの`send()`メソッドはテキストメッセージ用に使用してください。
- `WebSocketServer`は、低水準の`upgrade`イベントではなく、`http.Server`に接続する高水準APIを提供します。
- `verifyClient()`と`handleProtocols()`は同期的に動作します。
- `verifyClient()`と`handleProtocols()`内では、Promiseや`await`に基づく非同期処理は使用できません。
- `request`は、Node.jsの`IncomingMessage`の完全な実装ではなく、`url`、`headers`、`query()`、`getHeader()`などの主要なフィールド・メソッドを提供するヘルパーオブジェクトです。
- `clientTracking`は`clients`集合を保持しますが、低水準のソケット制御APIは追加しません。
- `upgrade`、`handleUpgrade()`、`noServer`などの低水準APIは、現在提供していません。
