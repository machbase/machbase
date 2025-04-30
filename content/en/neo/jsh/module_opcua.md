---
title: "@jsh/opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.52" />}}

## Client

The OPCUA client.

**Usage example**

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

### Creation

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | Instantiates a opcua client object with an options |

### Options

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| endpoint            | String       | `""`           | server address      |
| readRetryInterval   | Number       | `100`          | read retry interval in ms. |
| messageSecurityMode | [MessageSecurityMode](#messagesecuritymode) | `MessageSecurityMode.None` |         |

### Methods

| Method                                 | Returns           | Description        |
|:---------------------------------------|:------------------|:-------------------|
| close()                                |                   | disconnect         |
| read(ReadOptions *option*)             | [ReadResult[]](#readresult) |                    |

## ReadOptions

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| nodes               | []String     |                | server address      |
| maxAge              | Number       | `100`          | read retry interval in ms. |
| timestampsToReturn  | [TimestampToReturn](#timestamptoreturn) | `TimestampToReturn.Neither` |      |

## ReadResult

### Properties

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     |                    |
| statusText         | String     |                    |
| statusCode         | String     |                    |
| value              | any        |                    |
| sourceTimestamp    | Time       |                    |
| sourceTimestamp    | Time       |                    |


## MessageSecurityMode

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| None               |            |                    |
| Sign               |            |                    |
| SignAndEncrypt     |            |                    |

## TimestampToReturn

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| Source             |            |                    |
| Server             |            |                    |
| Both               |            |                    |
| Neither            |            |                    |
