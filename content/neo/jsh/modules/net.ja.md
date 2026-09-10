---
toc: true
title: "net"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`net`モジュールは、JSHアプリケーションで使用できるNode.js互換のTCPネットワークAPIを提供します。

## createServer() {#createserver}

TCPサーバーを作成します。

対応するシグネチャ：

- `createServer([connectionListener])`
- `createServer([options][, connectionListener])`

- 戻り値: `Server`
- `connectionListener`を指定すると、`connection`イベントのリスナーとして登録されます。

<h6>構文</h6>

```js
createServer([options][, connectionListener])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const net = require('net');

const server = net.createServer((socket) => {
	socket.on('data', (data) => {
		const msg = data.toString();
		socket.write('Echo: ' + msg);
	});
});

server.listen(0, '127.0.0.1');
```

## createConnection() / connect() {#createconnection--connect}

TCPクライアントソケットを作成し、サーバーに接続します。

対応するシグネチャ：

- `createConnection(port[, host][, connectListener])`
- `createConnection(options[, connectListener])`
- `connect(...)` (`createConnection`の別名)

- 戻り値: `Socket`

<h6>構文</h6>

```js
createConnection(port[, host][, connectListener])
createConnection(options[, connectListener])
connect(port[, host][, connectListener])
connect(options[, connectListener])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const net = require('net');

const client = net.createConnection({ port: 5650, host: '127.0.0.1' }, () => {
	client.write('Hello Server\n');
});

client.on('data', (data) => {
	console.println(data.toString().trim());
	client.end();
});
```

## IP検証ユーティリティ {#ip-검증-유틸리티}

IP文字列を検証するユーティリティ関数です。

- `isIP(input)`は、`4`、`6`、`0`のいずれかを返します。
- `isIPv4(input)`は、`boolean`を返します。
- `isIPv6(input)`は、`boolean`を返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const net = require('net');
console.println(net.isIP('127.0.0.1')); // 4
console.println(net.isIPv4('127.0.0.1')); // true
console.println(net.isIPv6('::1')); // true
```

## Server {#server}

`createServer()`が返すTCPサーバーオブジェクトです。

<h6>主なプロパティ</h6>

- `listening`
- `connections`

**Server メソッド**

- `listen(port[, host][, backlog][, callback])`
- `listen(options[, callback])`
- `close([callback])`
- `address()`
- `getConnections([callback])`
- `ref()`
- `unref()`

**Server イベント**

- `connection` (`Socket`)
- `listening` ()
- `close` ()
- `error` (`Error`)

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const net = require('net');
const server = net.createServer();

server.on('listening', () => {
	const addr = server.address();
	console.println(addr.family, addr.address, addr.port);
});

server.listen(0, '127.0.0.1', () => {
	console.println('server ready');
});
```

## Socket {#socket}

TCPクライアント/サーバー接続オブジェクトです。

<h6>主なプロパティ</h6>

- `connecting`
- `readable`
- `writable`
- `destroyed`
- `bytesRead`
- `bytesWritten`
- `localAddress`
- `localPort`
- `remoteAddress`
- `remotePort`
- `remoteFamily`

**Socket メソッド**

- `connect(port[, host][, connectListener])`
- `connect(options[, connectListener])`
- `write(data[, encoding][, callback])`
- `end([data[, encoding]][, callback])`
- `destroy([error])`
- `setTimeout(timeout[, callback])`
- `setNoDelay([noDelay])`
- `setKeepAlive([enable][, initialDelay])`
- `setEncoding([encoding])`
- `address()`
- `pause()`
- `resume()`
- `ref()`
- `unref()`

**Socket イベント**

- `connect` ()
- `data` (`Buffer`)
- `end` ()
- `close` (`hadError`)
- `error` (`Error`)
- `finish` ()

**動作に関する注意**

- `data`イベントのペイロードは、`Buffer`で渡されます。
- `write()`は、`string`、`Buffer`、`Array`、`Uint8Array`互換の値に対応しています。
- 現在のネイティブ実装では、`pause()`と`resume()`は何も処理しません（no-op）。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const net = require('net');
const client = net.connect(5650, '127.0.0.1');

client.on('connect', () => {
	client.setNoDelay(true);
	client.write('ping\n');
});

client.on('data', (data) => {
	console.println('received:', data.toString().trim());
	client.end();
});

client.on('close', (hadError) => {
	console.println('closed, hadError=', hadError);
});
```
