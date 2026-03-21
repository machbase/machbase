---
title: "mqtt"
type: docs
weight: 100
---

{{< neo_since ver="8.0.74" />}}

`mqtt`는 JSH의 MQTT 클라이언트 모듈입니다.

JSH 애플리케이션에서는 일반적으로 아래처럼 사용합니다.

```js
const mqtt = require('mqtt');
```

현재 API는 이벤트 기반이며, `Client`를 생성하면 자동으로 브로커 연결을 시도합니다.

## Client

MQTT 클라이언트 객체입니다.

<h6>생성</h6>

```js
new Client(options)
```

<h6>옵션</h6>

| 옵션                              | 타입      | 기본값  | 설명 |
|:----------------------------------|:----------|:--------|:-----|
| servers                           | String[]  |         | MQTT 브로커 URL 목록 (예: `tcp://127.0.0.1:1883`) |
| username                          | String    |         | 브로커 인증 사용자 이름 |
| password                          | String    |         | 브로커 인증 비밀번호 |
| keepAlive                         | Number    | `30`    | Keep Alive(초) |
| connectRetryDelay                 | Number    | `0`     | 재접속 지연(밀리초) |
| cleanStartOnInitialConnection     | Boolean   | `false` | 최초 연결 시 MQTT v5 clean start 여부 |
| connectTimeout                    | Number    | `0`     | 연결 타임아웃(밀리초) |

<h6>사용 예시</h6>

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

## 메서드

### publish()

토픽으로 메시지를 발행합니다.

<h6>사용 형식</h6>

```js
publish(topic, message[, options])
```

<h6>매개변수</h6>

- `topic` `String`
- `message` `String` | `Uint8Array` | `Object` | `Array`
- `options` `Object` (선택)

| 옵션       | 타입    | 기본값  | 설명 |
|:-----------|:--------|:--------|:-----|
| qos        | Number  | `0`     | QoS 레벨 |
| retain     | Boolean | `false` | Retain 플래그 |
| properties | Object  |         | MQTT v5 발행 프로퍼티 |

`options.properties` 필드:

| 프로퍼티                  | 타입    | 설명 |
|:--------------------------|:--------|:-----|
| payloadFormat             | Number  | Payload format indicator |
| messageExpiry             | Number  | 만료 시간 |
| contentType               | String  | 콘텐츠 타입 |
| responseTopic             | String  | 응답 토픽 |
| correlationData           | String  | 바이트로 변환됨 |
| topicAlias                | Number  | Topic alias |
| subscriptionIdentifier    | Number  | Subscription identifier |
| user                      | Object  | 사용자 정의 프로퍼티 (`key: value`) |

<h6>반환값</h6>

없음. 결과는 `published` 또는 `error` 이벤트로 전달됩니다.

### subscribe()

토픽을 구독합니다.

<h6>사용 형식</h6>

```js
subscribe(topic[, options])
```

<h6>매개변수</h6>

- `topic` `String`
- `options` `Object` (선택)

| 옵션               | 타입    | 기본값 | 설명 |
|:-------------------|:--------|:-------|:-----|
| qos                | Number  | `1`    | QoS 레벨 |
| retainHandling     | Number  |         | MQTT v5 retain handling |
| noLocal            | Boolean | `false` | 동일 클라이언트가 발행한 메시지 수신 여부 |
| retainAsPublished  | Boolean | `false` | 브로커의 retain 플래그 유지 여부 |
| properties         | Object  |         | MQTT v5 구독 프로퍼티 |

`options.properties` 필드:

| 프로퍼티               | 타입   | 설명 |
|:-----------------------|:-------|:-----|
| subscriptionIdentifier | Number | Subscription identifier |
| user                   | Object | 사용자 정의 프로퍼티 (`key: value`) |

<h6>반환값</h6>

없음. 결과는 `subscribed` 또는 `error` 이벤트로 전달됩니다.

<h6>사용 예시</h6>

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

### unsubscribe()

토픽 구독을 해제합니다.

<h6>사용 형식</h6>

```js
unsubscribe(topic[, options])
```

<h6>매개변수</h6>

- `topic` `String`
- `options` `Object` (선택)

| 옵션       | 타입   | 설명 |
|:-----------|:-------|:-----|
| properties | Object | MQTT v5 구독 해제 프로퍼티 |

`options.properties` 필드:

| 프로퍼티 | 타입   | 설명 |
|:---------|:-------|:-----|
| user     | Object | 사용자 정의 프로퍼티 (`key: value`) |

<h6>반환값</h6>

없음. 결과는 `unsubscribed` 또는 `error` 이벤트로 전달됩니다.

<h6>사용 예시</h6>

```js
client.unsubscribe('test/topic', {
    properties: {
        user: {
            source: 'example',
        },
    },
});
```

### close()

클라이언트 연결을 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

<h6>반환값</h6>

없음. `close` 이벤트가 발생합니다.

## 이벤트

### open

클라이언트 연결이 완료되면 발생합니다.

```js
client.on('open', () => { ... })
```

### message

구독한 메시지를 수신하면 발생합니다.

```js
client.on('message', (msg) => { ... })
```

`msg` 필드:

| 프로퍼티   | 타입   | 설명 |
|:-----------|:-------|:-----|
| topic      | String | 토픽 이름 |
| payload    | Buffer | 바이너리 안전한 메시지 페이로드 |
| payloadText| String | UTF-8로 디코딩한 텍스트 편의 필드 |
| properties | Object | MQTT v5 publish 프로퍼티 |

`msg.properties` 필드:

| 프로퍼티               | 타입   | 설명 |
|:-----------------------|:-------|:-----|
| payloadFormat          | Number | Payload format indicator |
| messageExpiry          | Number | 만료 시간 |
| contentType            | String | 콘텐츠 타입 |
| responseTopic          | String | 응답 토픽 |
| correlationData        | Buffer | 바이너리 안전한 correlation data |
| topicAlias             | Number | Topic alias |
| subscriptionIdentifier | Number | Subscription identifier |
| user                   | Object | 사용자 정의 프로퍼티 |

텍스트 메시지는 `msg.payloadText` 또는 `msg.payload.toString()`으로 읽을 수 있습니다.

바이너리 메시지는 `msg.payload`를 그대로 사용합니다.

```js
client.on('message', (msg) => {
    console.println('Payload is buffer:', Buffer.isBuffer(msg.payload));
    console.println('Payload bytes:', Array.from(msg.payload).join(','));
});
```

MQTT v5 publish 프로퍼티는 `msg.properties`로 접근할 수 있습니다.

```js
client.on('message', (msg) => {
    console.println('Content type:', msg.properties.contentType);
    console.println('Response topic:', msg.properties.responseTopic);
    console.println('Correlation data:', msg.properties.correlationData.toString());
    console.println('User source:', msg.properties.user.source);
});
```

### subscribed

구독 ACK를 받으면 발생합니다.

```js
client.on('subscribed', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` (MQTT reason code)

### published

발행 ACK를 받으면 발생합니다.

```js
client.on('published', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` (MQTT reason code)

### unsubscribed

구독 해제 ACK를 받으면 발생합니다.

```js
client.on('unsubscribed', (topic, reason) => { ... })
```

- `topic` `String`
- `reason` `Number` (MQTT reason code)

### error

연결, 구독, 구독 해제, 발행 중 오류가 발생하면 전달됩니다.

```js
client.on('error', (err) => { ... })
```

- `err` `Error`

연결 전이거나 `close()` 호출 후 `publish()`, `subscribe()`, `unsubscribe()`를 호출하면 `error` 이벤트로 오류가 전달됩니다.

### close

`close()` 호출 시 발생합니다.

```js
client.on('close', () => { ... })
```

## MQTT v5 쓰기 프로퍼티 예시

아래 예시는 MQTT v5 write API의 사용자 프로퍼티를 사용해 `db/write/{table}` 토픽으로 데이터를 기록합니다.

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
