---
title: "@jsh/opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.52" />}}

## Client

OPC UA 클라이언트입니다.

**사용 예시**

```js {linenos=table,linenostart=1}
opcua = require("@jsh/opcua");
nodes = [
    "ns=1;s=NoPermVariable",
    "ns=1;s=ReadWriteVariable",
    "ns=1;s=ReadOnlyVariable",
    "ns=1;s=NoAccessVariable",
];

try {
    client = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
    vs = client.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
    });
    vs.forEach((v, idx) => {
        console.log(nodes[idx], v.status, v.statusCode, v.value, v.type);
    })
} catch (e) {
    console.log("Error:", e.message);
} finally {
    if (client !== undefined) client.close();
}
```

<h6>생성</h6>

| Constructor             | 설명                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | 옵션과 함께 OPC UA 클라이언트를 생성합니다. |

<h6>옵션</h6>

| 옵션                | 타입         | 기본값        | 설명                              |
|:--------------------|:-------------|:---------------|:----------------------------------|
| endpoint            | String       | `""`           | OPC UA 서버 주소                  |
| readRetryInterval   | Number       | `100`          | 읽기 재시도 간격(밀리초)          |
| messageSecurityMode |              |                | [MessageSecurityMode](#messagesecuritymode) 지정 |

### close()

서버 연결을 종료합니다.

<h6>사용 형식</h6>

```js
close()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

없음.

### read()

<h6>사용 형식</h6>

```js
read(read_request)
```

<h6>매개변수</h6>

`read_request` `Object` [ReadRequest](#readrequest)

<h6>반환값</h6>

`Object[]` [ReadResult](#readresult) 배열

```js
vs = client.read({
    nodes: [ "ns=1;s=ro_bool", "ns=1;s=rw_int32"],
    timestampsToReturn:ua.TimestampsToReturn.Both
});
vs.forEach((v, idx) => {
    console.log(nodes[idx], v.status, v.statusCode, v.value, v.type);
})
```

### write()

<h6>사용 형식</h6>

```js
write(...write_request)
```

<h6>매개변수</h6>

`write_request` `Object` 가변 개수의 [WriteRequest](#writerequest)

<h6>반환값</h6>

`Object` [WriteResult](#writeresult)

```js
rsp = client.write(
    {node: "ns=1;s=rw_bool", value: false},
    {node: "ns=1;s=rw_int32", value: 1234}
)
console.log("results:", rsp.results);
```

## ReadRequest

| 옵션                | 타입         | 기본값        | 설명                         |
|:--------------------|:-------------|:---------------|:--------------------|
| nodes               | String[]     |                | 읽어올 노드 ID 목록          |
| maxAge              | Number       | `100`          | 허용 가능한 캐시 연령(밀리초)|
| timestampsToReturn  |              |                | [TimestampToReturn](#timestamptoreturn) |

## ReadResult

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명                              |
|:-------------------|:-----------|:----------------------------------|
| status             | Number     | 상태 코드                         |
| statusText         | String     | 상태 설명                         |
| statusCode         | String     | OPC UA 상태 코드 문자열            |
| value              | any        | 읽은 값                           |
| sourceTimestamp    | Number     | 소스 타임스탬프(밀리초)           |
| serverTimestamp    | Number     | 서버 타임스탬프(밀리초)           |


## WriteRequest

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명           |
|:-------------------|:-----------|:---------------|
| node               | String     | 노드 ID        |
| value              | any        | 기록할 값      |

## WriteResult

<h6>프로퍼티</h6>

| 프로퍼티           | 타입       | 설명                    |
|:-------------------|:-----------|:------------------------|
| results            | Number[]   | 상태 코드 목록          |
| timestamp          | Number     | 타임스탬프(밀리초)      |
| stringTables       | String[]   | 문자열 테이블           |

## MessageSecurityMode

- `MessageSecurityMode.None`
- `MessageSecurityMode.Sign`
- `MessageSecurityMode.SignAndEncrypt`

## TimestampToReturn

- `TimestampToReturn.Source`
- `TimestampToReturn.Server`
- `TimestampToReturn.Both`
- `TimestampToReturn.Neither`
