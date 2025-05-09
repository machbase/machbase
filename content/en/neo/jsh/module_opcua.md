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

<h6>Creation</h6>

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | Instantiates a opcua client object with an options |

<h6>Options</h6>

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| endpoint            | String       | `""`           | server address      |
| readRetryInterval   | Number       | `100`          | read retry interval in ms. |
| messageSecurityMode |              | |  [MessageSecurityMode](#messagesecuritymode) |

### close()

Disconnect.

<h6>Syntax</h6>

```js
close()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

### read()

<h6>Syntax</h6>

```js
read(option)
```

<h6>Parameters</h6>

`option` `Object[]` Array of [ReadOptions](#readoptions)

<h6>Return value</h6>

None.

## ReadOptions

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| nodes               | []String     |                | server address      |
| maxAge              | Number       | `100`          | read retry interval in ms. |
| timestampsToReturn  |              |  | [TimestampToReturn](#timestamptoreturn)     |

## ReadResult

<h6>Properties</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     |                    |
| statusText         | String     |                    |
| statusCode         | String     |                    |
| value              | any        |                    |
| sourceTimestamp    | Number     | Unix epoch (milliseconds) |
| sourceTimestamp    | Number     | Unix epoch (milliseconds) |


## MessageSecurityMode

- `MessageSecurityMode.None`
- `MessageSecurityMode.Sign`
- `MessageSecurityMode.SignAndEncrypt`

## TimestampToReturn

- `TimestampToReturn.Source`
- `TimestampToReturn.Server`
- `TimestampToReturn.Both`
- `TimestampToReturn.Neither`
