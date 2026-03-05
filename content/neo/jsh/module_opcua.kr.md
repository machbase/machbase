---
title: "opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

`@jsh/opcua` 모듈은 JSH 애플리케이션에서 OPC UA 서버에 읽기/쓰기를 수행하는 클라이언트 API를 제공합니다.

## Client

OPC UA 클라이언트 객체입니다.

<h6>생성</h6>

```js
new Client(options)
```

- 반환값: `Client`
- `options`를 생략하면 예외(`missing arguments`)가 발생합니다.

<h6>옵션</h6>

| 옵션                | 타입     | 기본값                          | 설명 |
|:--------------------|:---------|:--------------------------------|:-----|
| endpoint            | `string` | `""`                            | OPC UA 서버 엔드포인트 (`opc.tcp://host:port`) |
| readRetryInterval   | `number` | `100` (100ms 미만이면 100으로 보정) | `read()` 재시도 간격(밀리초) |
| messageSecurityMode | `number` | `MessageSecurityMode.None`      | 보안 모드. [MessageSecurityMode](#messagesecuritymode) 참고 |

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");
const nodes = [
    "ns=1;s=NoPermVariable",
    "ns=1;s=ReadWriteVariable",
    "ns=1;s=ReadOnlyVariable",
    "ns=1;s=NoAccessVariable",
];

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const values = client.read({
        nodes,
        timestampsToReturn: ua.TimestampsToReturn.Both,
    });
    values.forEach((v, idx) => {
        console.println(nodes[idx], v.status, v.statusCode, v.value, v.type);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### close()

클라이언트 연결을 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

- 반환값: 없음 (`undefined`)

### read()

지정한 노드 목록을 읽습니다.

<h6>사용 형식</h6>

```js
read(readRequest)
```

<h6>매개변수</h6>

- `readRequest` (`object`): [ReadRequest](#readrequest)

<h6>반환값</h6>

- `object[]`: [ReadResult](#readresult) 배열

오류 동작:

- 인자가 없거나 1개가 아니면 예외(`missing argument`)
- `nodes`가 비어 있으면 예외(`missing nodes`)

### write()

하나 이상의 노드 값을 기록합니다.

<h6>사용 형식</h6>

```js
write(...writeRequest)
```

<h6>매개변수</h6>

- `writeRequest` (`object`, 가변 인자): [WriteRequest](#writerequest)

<h6>반환값</h6>

- `object`: [WriteResult](#writeresult)

오류 동작:

- 인자가 없으면 예외(`missing argument`)

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });

    let rsp = client.read({ nodes: ["ns=1;s=rw_bool", "ns=1;s=rw_int32"] });
    console.println("read response:", rsp[0].value, rsp[1].value);

    rsp = client.write(
        { node: "ns=1;s=rw_bool", value: false },
        { node: "ns=1;s=rw_int32", value: 1234 },
    );
    console.println("write response error:", rsp.error, ", results:", rsp.results);

    rsp = client.read({ nodes: ["ns=1;s=rw_bool", "ns=1;s=rw_int32"] });
    console.println("read response:", rsp[0].value, rsp[1].value);
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

## ReadRequest

| 프로퍼티            | 타입       | 기본값                       | 설명 |
|:--------------------|:-----------|:-----------------------------|:-----|
| nodes               | `string[]` |                               | 읽을 OPC UA 노드 ID 목록 |
| maxAge              | `number`   | `0`                           | 허용 가능한 캐시 연령(밀리초) |
| timestampsToReturn  | `number`   | `TimestampsToReturn.Neither` | 타임스탬프 반환 정책 |

## ReadResult

| 프로퍼티        | 타입     | 설명 |
|:----------------|:---------|:-----|
| status          | `number` | OPC UA 상태 코드(`uint32`) |
| statusText      | `string` | 상태 텍스트 |
| statusCode      | `string` | 상태 코드 이름(예: `StatusGood`) |
| value           | `any`    | 읽은 값 |
| type            | `string` | 값 타입 이름(예: `Boolean`, `Int32`, `Double`) |
| sourceTimestamp | `number` | 소스 타임스탬프(Unix epoch milliseconds) |
| serverTimestamp | `number` | 서버 타임스탬프(Unix epoch milliseconds) |

## WriteRequest

| 프로퍼티 | 타입     | 설명 |
|:---------|:---------|:-----|
| node     | `string` | 기록 대상 노드 ID |
| value    | `any`    | 기록할 값 |

## WriteResult

| 프로퍼티      | 타입       | 설명 |
|:--------------|:-----------|:-----|
| error         | `Error\|null` | 요청 처리 오류 |
| timestamp     | `number`   | 응답 타임스탬프(Unix epoch milliseconds) |
| requestHandle | `number`   | OPC UA 요청 핸들 |
| serviceResult | `number`   | OPC UA 서비스 결과 코드 |
| stringTable   | `string[]` | OPC UA 문자열 테이블 |
| results       | `number[]` | 노드별 상태 코드 배열 |

## MessageSecurityMode

- `MessageSecurityMode.None`
- `MessageSecurityMode.Sign`
- `MessageSecurityMode.SignAndEncrypt`
- `MessageSecurityMode.Invalid`

## TimestampsToReturn

- `TimestampsToReturn.Source`
- `TimestampsToReturn.Server`
- `TimestampsToReturn.Both`
- `TimestampsToReturn.Neither`
- `TimestampsToReturn.Invalid`
