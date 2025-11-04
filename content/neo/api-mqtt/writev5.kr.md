---
title: MQTT v5 데이터 쓰기
type: docs
weight: 31
---

## MQTT v5 토픽

{{< neo_since ver="8.0.33" />}}

MQTT v5에서는 사용자 정의 프로퍼티를 각 메시지에 붙일 수 있습니다. 이는 이전 버전(MQTT v3.1/v3.1.1)보다 더 큰 유연성을 제공하며, 메시지에 추가 메타데이터를 포함할 수 있게 해 줍니다.

{{< callout emoji="📌" >}}
참고: 사용자 정의 프로퍼티를 사용하지 않고도 MQTT v3.1 토픽 문법을 MQTT v5에서 그대로 사용할 수 있습니다.
{{< /callout >}}

MQTT v5에서는 토픽을 `db/write/{table}`처럼 간단히 지정하고, 아래 사용자 프로퍼티를 함께 보낼 수 있습니다.

| User Property  | Default  | Values                  |
|:---------------|:--------:|:------------------------|
| format         | `json`   | `csv`, `json`, `ndjson` |
| timeformat     | `ns`     | Time format: `s`, `ms`, `us`, `ns` |
| tz             | `UTC`    | Time Zone: `UTC`, `Local` and location spec |
| compress       |          | `gzip`                  |
| method         | `insert` | `insert`, `append`      |
| reply          |          | Topic to which the server sends the result messages |


**format=csv일 때 추가 프로퍼티** 

| User Property  | Default  | Values                  |
|:---------------|:--------:|:------------------------|
| delimiter      |`,`       |                         |
| header         |          | `skip`, `columns`       |


{{< callout emoji="📌" >}}
append 방식의 특성상 `header=columns`는 `method=append`와 함께 사용할 수 없습니다.
{{< /callout >}}

## APPEND 방식

MQTT는 연결 지향 프로토콜이므로 하나의 세션을 유지한 채 반복해서 데이터를 보낼 수 있습니다.
이 점이 HTTP보다 MQTT를 사용할 때 얻을 수 있는 가장 큰 이점입니다.

아래 예시는 `mosquitto_pub`을 이용한 데모입니다.
이 도구는 메시지 하나를 발행하면 연결을 종료하기 때문에 HTTP `write` API보다 성능이 좋아지지 않을 수도 있고, 어떤 경우에는 더 느릴 수 있습니다.<br/>
연결을 비교적 오래 유지하며 다수 메시지를 전송할 수 있는 클라이언트에서만 이 방식을 사용하시기 바랍니다.

### JSON

**복수 레코드 발행**

아래 예시의 페이로드는 튜플 배열(JSON에서는 배열의 배열)입니다.
하나의 MQTT 메시지로 여러 레코드를 append합니다.
아래처럼 단일 튜플을 전송하는 것도 가능하며 Machbase Neo는 두 형식을 모두 지원합니다.

- mqtt-data.json

```json
[
    [ "my-car", 1670380342000000000, 32.1 ],
    [ "my-car", 1670380343000000000, 65.4 ],
    [ "my-car", 1670380344000000000, 76.5 ]
]
```

- mosquitto_pub

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -f ./mqtt-data.json
```

- JSH 앱

다음 JSH 앱은 JavaScript로 MQTT를 사용해 여러 레코드를 Machbase Neo 테이블에 쓰는 방법을 보여 줍니다.
이 코드는 독립 실행형 JSH 스크립트 또는 TQL 스크립트의 `SCRIPT()` 함수로 실행할 수 있습니다.

append 방식과 배열 페이로드를 사용하면 IoT나 실시간 데이터 수집 시나리오에 적합한 높은 처리량을 확보할 수 있습니다.

주요 코드 부분을 단계별로 살펴보면 다음과 같습니다.

```js {linenos=table,linenostart=1,hl_lines=["24-28",34]}
// 필요한 모듈을 임포트하고 5653 포트의 로컬 MQTT 브로커에 연결하는 클라이언트를 생성합니다.
const system = require("@jsh/system");
const mqtt = require("@jsh/mqtt");
var conf = { serverUrls: ["tcp://127.0.0.1:5653"] };
var client = new mqtt.Client(conf);

// 발행 옵션을 설정합니다.
var pubOpt = {
    topic:"db/write/EXAMPLE", // EXAMPLE 테이블에 데이터를 씁니다.
    qos:0,                    // QoS 0(최대 한 번 전송)
    properties: {
        user: {
            method: "append", // append 모드
            timeformat: "ms", // 타임스탬프 단위는 밀리초입니다.
        },
    },
};

// 전송할 레코드 배열을 준비합니다.
// 각 레코드는 이름, 밀리초 단위 타임스탬프, 값을 포함합니다.
ts = (new Date()).getTime();
var pubPayload = [
    [ "my-car", ts+0, 32.1 ],
    [ "my-car", ts+1, 65.4 ],
    [ "my-car", ts+2, 76.5 ],
];

client.onConnect = ()=>{
    // 클라이언트가 브로커에 연결되면 지정된 옵션으로 페이로드를 발행합니다.
    client.publish(pubOpt, JSON.stringify(pubPayload))
}

// 클라이언트는 3초 타임아웃으로 브로커에 연결하고 데이터를 전송한 뒤,
// 모든 메시지 발송이 완료되면 연결을 종료합니다.
client.connect({timeout:3000});
client.disconnect({waitForEmptyQueue: true, timeout:3000});
```

**단일 레코드 발행**

- mqtt-data.json

```json
[ "my-car", 1670380345000000000, 87.6 ]
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -f ./mqtt-data.json
```

**gzip JSON 발행**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property compress gzip \
    -f mqtt-data.json.gz
```

### NDJSON

{{< neo_since ver="8.0.33" />}}

NDJSON(Newline Delimited JSON)은 각 줄이 완전한 JSON 객체인 스트리밍 형식으로, 대용량 데이터나 스트리밍 데이터를 처리할 때 유용합니다.
각 줄은 테이블 컬럼 이름과 일치하는 필드를 포함해야 합니다.

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property format ndjson \
    -f mqtt-nd.json
```

### CSV

- mqtt-data.csv

```csv
NAME,TIME,VALUE
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
```

```sh {hl_lines=[6]}
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property header skip \
    -D PUBLISH user-property timeformat s \
    -f mqtt-data.csv
```

하이라이트된 `header=skip` 옵션은 첫 줄이 헤더임을 의미합니다.

**gzip CSV 발행**

- mqtt-data.csv.gz

```csv
NAME,TIME,VALUE
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property header skip \
    -D PUBLISH user-property timeformat s \
    -D PUBLISH user-property compress gzip \
    -f mqtt-data.csv.gz
```

## INSERT 방식

MQTT에서 성능을 최적화하려면 append 방식을 사용하는 것이 좋습니다.
데이터 필드 순서가 테이블 컬럼 순서와 다르거나 모든 컬럼을 포함하지 않을 때만 `insert` 방식을 사용하십시오.

데이터 필드 수가 다르거나 순서가 맞지 않으면 기본 append 대신 `insert`를 사용해야 합니다.

### JSON

`db/write`는 `INSERT INTO table(...) VALUES(...)` SQL과 동일하게 동작하므로 JSON 페이로드에 컬럼 정보를 포함해야 합니다.
아래는 `data-write.json` 예시입니다.

- mqtt-data.json
```json {linenos=table,hl_lines=[3]}
{
  "data": {
    "columns": ["name", "time", "value"],
    "rows": [
      [ "wave.pi", 1687481466000000000, 1.2345],
      [ "wave.pi", 1687481467000000000, 3.1415]
    ]
  }
}
```

`method` 프로퍼티의 기본값이 `insert`이므로 생략해도 됩니다.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method insert \
    -f mqtt-data.json
```

### NDJSON

{{< neo_since ver="8.0.33" />}}

이 요청 메시지는 `INSERT INTO {table} (columns...) VALUES (values...)` 구문과 동일한 구조입니다.

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343, "VALUE":2.002}
```

`method` 프로퍼티의 기본값이 `insert`이므로 생략해도 됩니다.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property method insert \
    -D PUBLISH user-property format ndjson \
    -D PUBLISH user-property timeformat s \
    -f mqtt-nd.json
```

### CSV

테이블 컬럼과 필드 수 또는 순서가 다른 CSV 데이터를 INSERT 방식으로 전송하려면 MQTT v5에서 사용자 정의 프로퍼티를 사용해야 합니다.

- mqtt-data.csv

```csv
VALUE,NAME,TIME
87.7,my-car,1670380346000
98.6,my-car,1670380347000
99.9,my-car,1670380348000
```

```sh {hl_lines=[5]}
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -V 5 \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method insert \
    -D PUBLISH user-property header columns \
    -D PUBLISH user-property timeformat ms \
    -f mqtt-data.csv
```

## TQL

`db/tql/{file.tql}` 토픽은 TQL 파일을 실행하는 용도입니다.

데이터를 변환해 저장해야 한다면 적절한 *TQL* 스크립트를 준비하고 `db/tql/{file.tql}` 토픽으로 데이터를 발행하십시오.

MQTT와 *TQL*을 통한 데이터 쓰기 방식은 [As Writing API](../../tql/writing)를 참고해 주십시오.


## 최대 메시지 크기

MQTT 사양에서 PUBLISH 메시지의 최대 페이로드 크기는 256MB입니다. 악의적이거나 오작동하는 클라이언트가 대용량 메시지를 계속 보내면 서버의 네트워크와 자원을 소모해 서비스 장애를 초래할 수 있습니다. 클라이언트가 요구하는 크기보다 약간 크게 최대 메시지 크기를 설정하는 것이 좋습니다. MQTT 기본 최대 메시지 크기는 1MB(`1048576`)이며, 아래와 같이 명령줄 플래그나 설정 파일의 `MaxMessageSizeLimit`로 조정할 수 있습니다.

```sh
machbase-neo serve --mqtt-max-message 1048576
```
