---
title: "opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

`opcua` 모듈은 JSH 애플리케이션에서 OPC UA 서버에 읽기/쓰기를 수행하는 클라이언트 API를 제공합니다.

## Client

OPC UA 클라이언트 객체입니다.

<h6>생성</h6>

```js
new Client(options)
```

- 반환값: `Client`
- `options`를 생략하면 예외(`missing client options`)가 발생합니다.

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

- 반환값: 성공 시 `null`

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

- `nodes`가 없거나 비어 있으면 예외가 발생합니다.

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

### browse()

하나 이상의 노드에 대한 참조를 탐색합니다.

<h6>사용 형식</h6>

```js
browse(browseRequest)
```

<h6>매개변수</h6>

- `browseRequest` (`object`): [BrowseRequest](#browserequest)

<h6>반환값</h6>

- `object[]`: [BrowseResult](#browseresult) 배열

오류 동작:

- `nodes`가 없거나 비어 있으면 예외가 발생합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const results = client.browse({
        nodes: ["ns=1;i=85"],
        nodeClassMask: ua.NodeClass.Variable,
        requestedMaxReferencesPerNode: 2,
    });

    console.println("continuationPoint:", results[0].continuationPoint);
    results[0].references.forEach((ref) => {
        console.println(ref.browseName, ref.nodeId, ref.nodeClass);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### browseNext()

`browse()` 또는 `browseNext()`가 반환한 continuation point를 사용해 다음 페이지를 계속 조회합니다.

<h6>사용 형식</h6>

```js
browseNext(browseNextRequest)
```

<h6>매개변수</h6>

- `browseNextRequest` (`object`): [BrowseNextRequest](#browsenextrequest)

<h6>반환값</h6>

- `object[]`: [BrowseResult](#browseresult) 배열

오류 동작:

- `continuationPoints`가 없거나 비어 있으면 예외가 발생합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });

    let results = client.browse({
        nodes: ["ns=1;i=85"],
        nodeClassMask: ua.NodeClass.Variable,
        requestedMaxReferencesPerNode: 2,
    });

    while (results[0].continuationPoint) {
        results = client.browseNext({
            continuationPoints: [results[0].continuationPoint],
        });
        results[0].references.forEach((ref) => {
            console.println(ref.browseName, ref.nodeId, ref.nodeClass);
        });
    }
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### children()

지정한 노드의 직접 자식 참조를 반환합니다.

<h6>사용 형식</h6>

```js
children(childrenRequest)
```

<h6>매개변수</h6>

- `childrenRequest` (`object`): [ChildrenRequest](#childrenrequest)

<h6>반환값</h6>

- `object[]`: [ChildrenResult](#childrenresult) 배열

오류 동작:

- `node`가 없거나 비어 있으면 예외가 발생합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const refs = client.children({
        node: "ns=1;i=85",
        nodeClassMask: ua.NodeClass.Variable,
    });

    refs.forEach((ref) => {
        console.println(ref.browseName, ref.nodeId, ref.nodeClass);
    });
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

## BrowseRequest

| 프로퍼티                      | 타입       | 기본값                    | 설명 |
|:------------------------------|:-----------|:--------------------------|:-----|
| nodes                         | `string[]` |                           | 탐색할 OPC UA 노드 ID 목록 |
| browseDirection               | `number`   | `BrowseDirection.Forward` | 탐색 방향 |
| referenceTypeId               | `string`   | 모든 reference            | 따라갈 참조 타입 노드 ID |
| includeSubtypes               | `boolean`  | `true`                    | `referenceTypeId`의 하위 타입 포함 여부 |
| nodeClassMask                 | `number`   | `0`                       | 포함할 노드 클래스 비트마스크 |
| resultMask                    | `number`   | `BrowseResultMask.All`    | 반환할 필드 비트마스크 |
| requestedMaxReferencesPerNode | `number`   | `0`                       | 서버가 노드별 최대 참조 수를 나누어 반환하도록 요청하는 힌트 |

## BrowseNextRequest

| 프로퍼티                 | 타입       | 기본값  | 설명 |
|:-------------------------|:-----------|:--------|:-----|
| continuationPoints       | `string[]` |         | `browse()` 또는 `browseNext()`가 반환한 base64 continuation point 목록 |
| releaseContinuationPoints| `boolean`  | `false` | 다음 참조를 요청하지 않고 서버 측 continuation point를 해제할지 여부 |

## BrowseResult

| 프로퍼티          | 타입       | 설명 |
|:------------------|:-----------|:-----|
| status            | `number`   | OPC UA 상태 코드(`uint32`) |
| statusText        | `string`   | 상태 텍스트 |
| continuationPoint | `string`   | base64 continuation point. 다음 페이지가 없으면 빈 문자열 |
| references        | `object[]` | [BrowseReference](#browsereference) 배열 |

## BrowseReference

| 프로퍼티        | 타입      | 설명 |
|:----------------|:----------|:-----|
| referenceTypeId | `string`  | 참조 타입 노드 ID |
| isForward       | `boolean` | 정방향 참조 여부 |
| nodeId          | `string`  | 대상 노드 ID |
| browseName      | `string`  | Browse 이름 |
| displayName     | `string`  | Display 이름 |
| nodeClass       | `number`  | OPC UA 노드 클래스 값 |
| typeDefinition  | `string`  | 타입 정의 노드 ID |

## ChildrenRequest

| 프로퍼티      | 타입     | 설명 |
|:--------------|:---------|:-----|
| node          | `string` | 부모 노드 ID |
| nodeClassMask | `number` | 포함할 노드 클래스 비트마스크 |

## ChildrenResult

| 프로퍼티        | 타입      | 설명 |
|:----------------|:----------|:-----|
| referenceTypeId | `string`  | 참조 타입 노드 ID |
| isForward       | `boolean` | 정방향 참조 여부 |
| nodeId          | `string`  | 자식 노드 ID |
| browseName      | `string`  | Browse 이름 |
| displayName     | `string`  | Display 이름 |
| nodeClass       | `number`  | OPC UA 노드 클래스 값 |
| typeDefinition  | `string`  | 타입 정의 노드 ID |

## BrowseDirection

- `BrowseDirection.Forward`
- `BrowseDirection.Inverse`
- `BrowseDirection.Both`
- `BrowseDirection.Invalid`

## NodeClass

- `NodeClass.Unspecified`
- `NodeClass.Object`
- `NodeClass.Variable`
- `NodeClass.Method`
- `NodeClass.ObjectType`
- `NodeClass.VariableType`
- `NodeClass.ReferenceType`
- `NodeClass.DataType`
- `NodeClass.View`

## BrowseResultMask

- `BrowseResultMask.None`
- `BrowseResultMask.ReferenceTypeId`
- `BrowseResultMask.IsForward`
- `BrowseResultMask.NodeClass`
- `BrowseResultMask.BrowseName`
- `BrowseResultMask.DisplayName`
- `BrowseResultMask.TypeDefinition`
- `BrowseResultMask.All`
- `BrowseResultMask.ReferenceTypeInfo`
- `BrowseResultMask.TargetInfo`

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

## OPCUA 클라이언트

이 예제는 OPC UA 서버에 연결해 시스템 지표를 읽고 데이터베이스에 저장하는 수집기를 구현합니다.

**동작 흐름**

1. OPC UA 연동: `opcua` 모듈을 사용해 `opc.tcp://localhost:4840` 서버에 연결하고 `sys_cpu`, `sys_mem`, `load1` 등 노드 값을 조회합니다.
2. 주기 수집: `setInterval()`을 활용해 10초마다 데이터를 읽습니다.
3. 데이터 적재: 수집한 값은 `EXAMPLE` 테이블에 `name`, `time`, `value` 컬럼으로 저장합니다.

### 데이터 수집기

스크립트를 `opcua-client.js`로 저장한 뒤 JSH 터미널에서 백그라운드로 실행하십시오.

```
jsh / > opcua-client
jsh / > ps
┌──────┬──────┬──────┬──────────────────┬────────┐ 
│  PID │ PPID │ USER │ NAME             │ UPTIME │ 
├──────┼──────┼──────┼──────────────────┼────────┤ 
│ 1044 │ 1    │ sys  │ /opcua-client.js │ 13s    │ 
│ 1045 │ 1025 │ sys  │ ps               │ 0s     │ 
└──────┴──────┴──────┴──────────────────┴────────┘ 
```

- opcua-client.js

```js {linenos=table,linenostart=1}
opcua = require("opcua");
process = require("process");
machcli = require("machcli");

const nodes = [
    "ns=1;s=sys_cpu",
    "ns=1;s=sys_mem",
    "ns=1;s=load1",
    "ns=1;s=load5",
    "ns=1;s=load15",
];
const tags = [
    "sys_cpu", "sys_mem", "sys_load1", "sys_load5", "sys_load15"
];
const dbConf = { host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' };
const sqlText = `INSERT INTO EXAMPLE (name,time,value) values(?,?,?)`;
const uaClient = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
process.addShutdownHook(()=>{
    uaClient.close();
});
setInterval(()=>{
    const ts = process.now();
    const vs = uaClient.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
    });
    var dbClient, conn;
    try {
        dbClient = new machcli.Client(dbConf);
        conn = dbClient.connect();
        vs.forEach((v, idx) => {
            if( v.value !== null ) {
                conn.exec(sqlText, tags[idx], ts, v.value);
            }
        })
    } catch (e) {
        console.println("Error:", e.message);
    } finally {
        conn && conn.close();
        dbClient && dbClient.close();
    }
}, 10*1000);
```

### 시뮬레이터 서버

`opcua-client.js`를 시험하려면 필요한 시스템 지표 노드를 제공하는 OPC UA 서버가 필요합니다.
실환경이 없다면 아래 저장소에서 제공하는 시뮬레이터를 사용해 주십시오.
`sys_cpu`, `sys_mem`, `load1`, `load5`, `load15` 등의 샘플 데이터를 제공하여 수집기 및 시각화 흐름을 검증하실 수 있습니다.

설정 방법은 저장소의 안내를 따르시면 됩니다.

[https://github.com/machbase/neo-server/tree/main/jsh/native/opcua/test_server](https://github.com/machbase/neo-server/tree/main/jsh/native/opcua/test_server)

시뮬레이터를 실행한 뒤 `opcua-client.js`를 가동하면 OPC UA 클라이언트가 정상적으로 연결되어 데이터를 수집합니다.
