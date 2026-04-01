---
title: "ws"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`ws` 모듈은 JSH 애플리케이션에서 사용할 수 있는 WebSocket 클라이언트를 제공합니다.
Go 네이티브 WebSocket client 위에 구현된 `WebSocket` 클래스 하나를 노출합니다.

일반적으로 아래처럼 사용합니다.

```js
const { WebSocket } = require('ws');
```

## WebSocket

WebSocket 클라이언트 연결을 생성합니다.

<h6>사용 형식</h6>

```js
new WebSocket(url)
```

<h6>매개변수</h6>

- `url` `String`: `ws://host:port/path`, `wss://host:port/path` 같은 WebSocket 서버 주소

`url`이 없거나 문자열이 아니면 constructor는 `TypeError`를 발생시킵니다.

## 속성

| 속성 | 타입 | 설명 |
|:-----|:-----|:-----|
| `url` | String | constructor에 전달한 원래 WebSocket URL |
| `readyState` | Number | 현재 연결 상태 |

### readyState 값

- `WebSocket.CONNECTING` = `0`
- `WebSocket.OPEN` = `1`
- `WebSocket.CLOSING` = `2`
- `WebSocket.CLOSED` = `3`

### 메시지 타입 상수

- `WebSocket.TextMessage` = `1`
- `WebSocket.BinaryMessage` = `2`

## send()

서버로 메시지를 전송합니다.

<h6>사용 형식</h6>

```js
ws.send(data)
```

<h6>매개변수</h6>

- `data` `String`: 전송할 텍스트 메시지

소켓이 아직 열려 있지 않으면 `error` 이벤트가 발생합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('open', () => {
    ws.send('Hello, server');
});
```

## close()

현재 연결을 종료합니다.

<h6>사용 형식</h6>

```js
ws.close()
```

`close()`를 호출하면 소켓은 `CLOSING`을 거쳐 `CLOSED`로 전환되고 `close` 이벤트를 emit합니다.

## 이벤트

`WebSocket`은 `EventEmitter`를 상속하므로 `on()`, `addListener()` 같은 일반적인 이벤트 리스너 패턴을 사용할 수 있습니다.

### open

클라이언트 연결이 성공한 뒤 발생합니다.

```js
ws.on('open', () => {
    console.println('connected');
});
```

### close

연결이 종료되면 발생합니다.

```js
ws.on('close', () => {
    console.println('closed');
});
```

### message

서버에서 메시지가 도착하면 발생합니다.

callback은 다음 필드를 가진 event 비슷한 객체를 받습니다.

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `type` | Number | `WebSocket.TextMessage`, `WebSocket.BinaryMessage` 같은 메시지 타입 |
| `data` | String 또는 byte data | 메시지 payload. 텍스트 메시지는 문자열로 노출됩니다. |

```js {linenos=table,linenostart=1}
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('message', (evt) => {
    console.println(evt.data);
});
```

### error

연결 또는 전송 작업이 실패하면 발생합니다.

```js
ws.on('error', (err) => {
    console.println(err.message);
});
```

## 사용 예시

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

## 동작 참고

- 이 모듈은 WebSocket 클라이언트만 제공합니다. 서버 측 upgrade 처리는 포함하지 않습니다.
- 연결 시작은 constructor 내부에서 비동기적으로 진행됩니다.
- 연결 실패는 `error` 이벤트로 보고됩니다.
- 수신 메시지는 text 또는 binary일 수 있지만, JavaScript의 `send()` 메서드는 텍스트 메시지 용도로 사용하는 것이 안전합니다.