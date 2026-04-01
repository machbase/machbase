---
title: "nats"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`nats` 모듈은 JSH 애플리케이션에서 사용할 수 있는 NATS 클라이언트를 제공합니다.
`mqtt` 모듈과 비슷하게 이벤트 기반으로 동작하며, `Client`를 생성하면 자동으로 연결을 시작합니다.

일반적으로 아래처럼 사용합니다.

```js
const nats = require('nats');
```

## Client

NATS 클라이언트 객체입니다.

<h6>생성</h6>

```js
new Client(options)
```

<h6>옵션</h6>

| 옵션 | 타입 | 설명 |
|:-----|:-----|:-----|
| `servers` | String[] | `nats://127.0.0.1:4222` 같은 NATS 서버 URL 목록 |
| `name` | String | 연결 이름 |
| `user` | String | 인증 사용자 |
| `password` | String | 인증 비밀번호 |
| `token` | String | 인증 토큰 |
| `noRandomize` | Boolean | 서버 랜덤 선택 비활성화 |
| `noEcho` | Boolean | 자신이 발행한 메시지 echo 비활성화 |
| `verbose` | Boolean | verbose 프로토콜 동작 활성화 |
| `pedantic` | Boolean | pedantic 프로토콜 검사 활성화 |
| `allowReconnect` | Boolean | 재연결 허용 |
| `maxReconnect` | Number | 최대 재연결 횟수 |
| `reconnectWait` | Number | 재연결 대기 시간(밀리초) |
| `timeout` | Number | 연결 타임아웃(밀리초) |
| `drainTimeout` | Number | drain 타임아웃(밀리초) |
| `flusherTimeout` | Number | flush 타임아웃(밀리초) |
| `pingInterval` | Number | ping 간격(밀리초) |
| `maxPingsOut` | Number | 최대 outstanding ping 수 |
| `retryOnFailedConnect` | Boolean | 최초 연결 실패 시 재시도 |
| `skipHostLookup` | Boolean | host lookup 최적화 건너뛰기 |

<h6>사용 예시</h6>

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

## 속성

### config

`client.config`는 파싱된 네이티브 NATS 설정을 노출합니다.

대표적인 필드는 다음과 같습니다.

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

## 메서드

### publish()

subject에 메시지를 발행합니다.

<h6>사용 형식</h6>

```js
publish(subject, message[, options])
```

<h6>매개변수</h6>

- `subject` `String`
- `message` `String` | `Uint8Array` | `Object` | `Array`
- `options` `Object` (선택)

지원하는 `options` 필드:

| 옵션 | 타입 | 설명 |
|:-----|:-----|:-----|
| `reply` | String | request/reply 패턴에 사용할 reply subject |

Object와 Array는 발행 전에 JSON으로 인코딩됩니다.

<h6>반환값</h6>

없음. 결과는 `published` 또는 `error` 이벤트로 전달됩니다.

### subscribe()

subject를 구독합니다.

<h6>사용 형식</h6>

```js
subscribe(subject[, options])
```

<h6>매개변수</h6>

- `subject` `String`
- `options` `Object` (선택)

지원하는 `options` 필드:

| 옵션 | 타입 | 설명 |
|:-----|:-----|:-----|
| `queue` | String | queue subscription용 queue group 이름 |

<h6>반환값</h6>

없음. 결과는 `subscribed` 또는 `error` 이벤트로 전달됩니다.

### close()

클라이언트 연결을 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

## 이벤트

### open

연결이 완료되면 발생합니다.

```js
client.on('open', () => { ... })
```

### message

구독한 메시지를 받으면 발생합니다.

```js
client.on('message', (msg) => { ... })
```

`msg` 필드:

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| `topic` | String | MQTT 스타일 handler 호환용 subject alias |
| `subject` | String | NATS subject |
| `reply` | String | request/reply 흐름에서 사용할 reply subject |
| `payload` | String | 메시지 payload |

### subscribed

서버가 subscription을 수락하면 발생합니다.

```js
client.on('subscribed', (subject, reason) => { ... })
```

- `subject` `String`
- `reason` `Number`

현재 구현에서는 subscribe 성공 시 `1`을 사용합니다.

### published

publish 요청이 완료되면 발생합니다.

```js
client.on('published', (subject, reason) => { ... })
```

- `subject` `String`
- `reason` `Number`

현재 구현에서는 publish 성공 완료 시 `0`을 사용합니다.

### error

연결, subscribe, publish 실패 시 발생합니다.

```js
client.on('error', (err) => { ... })
```

- `err` `Error`

### close

`close()`를 호출하면 발생합니다.

```js
client.on('close', () => { ... })
```

## 기본 pub/sub 예시

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

## request/reply 예시

request/reply 흐름에서는 reply subject를 먼저 구독하고, `options.reply`를 지정해 발행합니다.

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

## 동작 참고

- `Client`는 constructor에서 자동으로 연결을 시작합니다.
- queue subscription은 `subscribe(subject, { queue: 'workers' })`로 사용할 수 있습니다.
- 연결이 열리기 전에 `publish()` 또는 `subscribe()`를 호출하면 `error` 이벤트가 발생합니다.
- 현재 구현에서 메시지 payload는 문자열로 노출됩니다.