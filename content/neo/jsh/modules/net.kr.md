---
title: "net"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`net` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 TCP 네트워킹 API를 제공합니다.

## createServer()

TCP 서버를 생성합니다.

지원 시그니처:

- `createServer([connectionListener])`
- `createServer([options][, connectionListener])`

- 반환값: `Server`
- `connectionListener`를 지정하시면 `connection` 이벤트 리스너로 등록됩니다.

<h6>사용 형식</h6>

```js
createServer([options][, connectionListener])
```

<h6>사용 예시</h6>

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

## createConnection() / connect()

TCP 클라이언트 소켓을 생성하고 서버에 연결합니다.

지원 시그니처:

- `createConnection(port[, host][, connectListener])`
- `createConnection(options[, connectListener])`
- `connect(...)` (`createConnection`의 별칭)

- 반환값: `Socket`

<h6>사용 형식</h6>

```js
createConnection(port[, host][, connectListener])
createConnection(options[, connectListener])
connect(port[, host][, connectListener])
connect(options[, connectListener])
```

<h6>사용 예시</h6>

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

## IP 검증 유틸리티

IP 문자열 값 검증을 위한 유틸리티 함수입니다.

- `isIP(input)`은 `4`, `6`, `0` 중 하나를 반환합니다.
- `isIPv4(input)`은 `boolean`을 반환합니다.
- `isIPv6(input)`은 `boolean`을 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const net = require('net');
console.println(net.isIP('127.0.0.1')); // 4
console.println(net.isIPv4('127.0.0.1')); // true
console.println(net.isIPv6('::1')); // true
```

## Server

`createServer()`가 반환하는 TCP 서버 객체입니다.

<h6>주요 프로퍼티</h6>

- `listening`
- `connections`

**Server 메서드**

- `listen(port[, host][, backlog][, callback])`
- `listen(options[, callback])`
- `close([callback])`
- `address()`
- `getConnections([callback])`
- `ref()`
- `unref()`

**Server 이벤트**

- `connection` (`Socket`)
- `listening` ()
- `close` ()
- `error` (`Error`)

<h6>사용 예시</h6>

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

## Socket

TCP 클라이언트/서버 연결 객체입니다.

<h6>주요 프로퍼티</h6>

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

**Socket 메서드**

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

**Socket 이벤트**

- `connect` ()
- `data` (`Buffer`)
- `end` ()
- `close` (`hadError`)
- `error` (`Error`)
- `finish` ()

**동작 참고**

- `data` 이벤트 payload는 `Buffer`로 전달됩니다.
- `write()`는 `string`, `Buffer`, `Array`, `Uint8Array` 호환 값을 지원합니다.
- `pause()`/`resume()`은 현재 네이티브 구현에서 no-op으로 동작합니다.

<h6>사용 예시</h6>

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
