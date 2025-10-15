---
title: "@jsh/mqtt"
type: docs
weight: 11
---

{{< neo_since ver="8.0.52" />}}


## Client

MQTT 클라이언트입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const mqtt = require("@jsh/mqtt");
const client = new mqtt.Client({ serverUrls: ["tcp://127.0.0.1:1236"] });
try {
    client.onConnect = connAck => { println("connected."); }
    client.onConnectError = err => { println("connect error", err); }
    client.connect({timeout: 10*1000});
    client.publish("test/topic", "Hello, MQTT!", 0)
} catch(e) {
    console.log("Error:", e);
} finally {
    client.disconnect({waitForEmptyQueue:true});
}
```

<h6>생성</h6>

| Constructor             | 설명                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | 옵션과 함께 MQTT 클라이언트를 생성합니다. |

<h6>옵션</h6>

| 옵션                               | 타입         | 기본값        | 설명                       |
|:-----------------------------------|:-------------|:---------------|:---------------------------|
| serverUrls                         | String[]     |                | 브로커 주소 목록           |
| keepAlive                          | Number       | `10`           | Keep Alive 초              |
| cleanStart                         | Boolean      | `true`         | 클린 세션 여부             |
| username                           | String       |                | 사용자 이름                |
| password                           | String       |                | 비밀번호                   |
| clientID                           | String       | 랜덤 ID        | 클라이언트 ID              |
| debug                              | Boolean      | `false`        | 디버그 로그 출력 여부       |
| sessionExpiryInterval              | Number       | `60`           | 세션 만료 시간(초)         |
| connectRetryDelay                  | Number       | `10`           | 재접속 지연(초)            |
| connectTimeout                     | Number       | `10`           | 접속 타임아웃(초)          |
| packetTimeout                      | Number       | `5`            | 패킷 타임아웃(초)          |
| queue                              | String       | `memory`       | 메시지 큐 저장 방식        |

### connect()

<h6>사용 형식</h6>

```js
connect(opts)
```

<h6>매개변수</h6>

- `opts` `Object`

| Property           | Type       | 설명                      |
|:-------------------|:-----------|:--------------------------|
| timeout            | Number     | 접속 타임아웃(밀리초)     |

<h6>반환값</h6>

없음.

### disconnect()

<h6>사용 형식</h6>

```js
disconnect(opts)
```

<h6>매개변수</h6>

- `opts` `Object`

| Property           | Type       | 설명                               |
|:-------------------|:-----------|:-----------------------------------|
| waitForEmptyQueue  | Boolean    | 큐가 빌 때까지 기다릴지 여부        |
| timeout            | Number     | 종료 대기 타임아웃(밀리초)          |

<h6>반환값</h6>

없음.

### subscribe()

<h6>사용 형식</h6>

```js
subscribe(opts)
```

<h6>매개변수</h6>

- `opts` `Object` *SubscriptionOption*

<h6>SubscriptionOption</h6>

| Property           | Type       | 설명                         |
|:-------------------|:-----------|:-----------------------------|
| **subscriptions**  | Object[]   | *Subscription* 배열          |
| properties         | Object     | *Properties* 객체            |

<h6>Subscription</h6>

| Property           | Type       | 설명                         |
|:-------------------|:-----------|:-----------------------------|
| **topic**          | String     | 구독할 토픽                  |
| qos                | Number     | `0`, `1`, `2`                |
| retainHandling     | Number     | Retain 처리 방식             |
| noLocal            | Boolean    | 로컬 발행 메시지 수신 차단   |
| retainAsPublished  | Boolean    | retain 플래그 유지 여부      |

<h6>Properties</h6>

| Property           | Type       | 설명                         |
|:-------------------|:-----------|:-----------------------------|
| user               | Object     | 사용자 정의 프로퍼티         |

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js
const topicName = 'sensor/temperature';
client.subscribe({subscriptions:[{topic:topicName, qos:0}]});
```

### unsubscribe()

<h6>사용 형식</h6>

```js
unsubscribe(opts)
```

<h6>매개변수</h6>

- `opts` `Object` *UnsubscribeOption*

<h6>UnsubscribeOption</h6>

| Property           | Type       | 설명                         |
|:-------------------|:-----------|:-----------------------------|
| **topics**         | String[]   | 해지할 토픽 목록             |
| properties         | Object     | *Properties* 객체             |

<h6>Properties</h6>

| Property           | Type       | 설명                         |
|:-------------------|:-----------|:-----------------------------|
| user               | Object     | 사용자 정의 프로퍼티         |

<h6>반환값</h6>

없음.

<h6>사용 예시</h6>

```js
const topicName = 'sensor/temperature';
client.unsubscribe({topics:[topicName]});
```

### publish()

<h6>사용 형식</h6>

```js
publish(opts, payload)
```

<h6>매개변수</h6>

- `opts` `Object` *PublishOptions*
- `payload` `String` 또는 `Number`

<h6>PublishOptions</h6>

| Property           | Type       | 설명                         |
|:-------------------|:-----------|:-----------------------------|
| **topic**          | String     | 발행할 토픽                   |
| qos                | Number     | `0`, `1`, `2`                |
| packetID           | String     | 패킷 ID                       |
| retain             | Boolean    | retain 플래그                 |
| properties         | Object     | MQTT v5 프로퍼티              |


<h6>반환값</h6>

- `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| reasonCode         | Number     |                       |
| properties         | Object     |                       |

<h6>사용 예시</h6>

```js
let r = client.publish('sensor/temperature', 'Hello World', 1)
console.log(r.reasonCode)
```

### onMessage callback

Callback function that receives a message.

<h6>사용 형식</h6>

```js
function (msg) { }
```

- `msg` `Object` Message

<h6>Message</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| packetID           | Number     |                       |
| topic              | String     |                       |
| qos                | Number     | 0, 1, 2               |
| retain             | Boolean    |                       |
| payload            | Object     | Payload               |
| properties         | Object     | Properties            |

<h6>Payload</h6>

- `msg.payload.bytes()`
- `msg.payload.string()`

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| correlationData    | byte[]     |                       |
| contentType        | String     |                       |
| responseTopic      | String     |                       |
| payloadFormat      | Number     | or undefined          |
| messageExpiry      | Number     | or undefined          |
| subscriptionIdentifier | Number | or undefined          |
| topicAlias         | Number     | or undefined          |
| user               | Object     | user properties       |

### onConnect callback

On connect callback.

<h6>사용 형식</h6>

```js
function (ack) { }
```

<h6>매개변수</h6>

- `ack` `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| sessionPresent     | Boolean    |                       |
| reasonCode         | Number     |                       |
| properties         | Object     | Properties            |

<h6>Properties</h6>

| Property              | Type       | Description           |
|:----------------------|:-----------|:----------------------|
| reasonString          | String     |                       |
| reasonInfo            | String     |                       |
| assignedClientID      | String     |                       |
| authMethod            | String     |                       |
| serverKeepAlive       | Number     | or undefined          |
| sessionExpiryInterval | Number     | or undefined          |
| user                  | Object     |                       |

<h6>반환값</h6>

없음.

### onConnectError callback

On connect error callback.

<h6>사용 형식</h6>

```js
function (err) { }
```

<h6>매개변수</h6>

- `error` `String`

<h6>반환값</h6>

없음.

### onDisconnect callback

On disconnect callback

<h6>사용 형식</h6>

```js
function (disconn) { }
```

<h6>매개변수</h6>

- `disconn` `Object`

<h6>반환값</h6>

없음.

### onClientError callback

On client error callback

<h6>사용 형식</h6>

```js
function (err) { }
```

<h6>매개변수</h6>

- `err` `String`

<h6>반환값</h6>

없음.
