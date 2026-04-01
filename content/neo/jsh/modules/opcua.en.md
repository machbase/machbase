---
title: "opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `opcua` module provides an OPC UA client API for JSH applications.

## Client

OPC UA client object.

<h6>Creation</h6>

```js
new Client(options)
```

- Returns: `Client`
- Throws `missing client options` if `options` is omitted.

<h6>Options</h6>

| Option              | Type     | Default                         | Description |
|:--------------------|:---------|:--------------------------------|:------------|
| endpoint            | `string` | `""`                            | OPC UA endpoint (`opc.tcp://host:port`) |
| readRetryInterval   | `number` | `100` (clamped to 100 if lower) | Retry interval for `read()` in milliseconds |
| messageSecurityMode | `number` | `MessageSecurityMode.None`      | Security mode. See [MessageSecurityMode](#messagesecuritymode) |

<h6>Usage example</h6>

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

Closes the client connection.

<h6>Syntax</h6>

```js
close()
```

- Returns: `null` on success

### read()

Reads values from the given node list.

<h6>Syntax</h6>

```js
read(readRequest)
```

<h6>Parameters</h6>

- `readRequest` (`object`): [ReadRequest](#readrequest)

<h6>Return value</h6>

- `object[]`: array of [ReadResult](#readresult)

Error behavior:

- Throws an error when `nodes` is missing or empty.

### write()

Writes one or more node values.

<h6>Syntax</h6>

```js
write(...writeRequest)
```

<h6>Parameters</h6>

- `writeRequest` (`object`, variadic): [WriteRequest](#writerequest)

<h6>Return value</h6>

- `object`: [WriteResult](#writeresult)

Error behavior:

- Throws `missing argument` when no argument is provided.

<h6>Usage example</h6>

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

Browses references for one or more nodes.

<h6>Syntax</h6>

```js
browse(browseRequest)
```

<h6>Parameters</h6>

- `browseRequest` (`object`): [BrowseRequest](#browserequest)

<h6>Return value</h6>

- `object[]`: array of [BrowseResult](#browseresult)

Error behavior:

- Throws an error when `nodes` is missing or empty.

<h6>Usage example</h6>

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

Continues a paginated browse request using continuation points returned by [browse()](#browse) or `browseNext()`.

<h6>Syntax</h6>

```js
browseNext(browseNextRequest)
```

<h6>Parameters</h6>

- `browseNextRequest` (`object`): [BrowseNextRequest](#browsenextrequest)

<h6>Return value</h6>

- `object[]`: array of [BrowseResult](#browseresult)

Error behavior:

- Throws an error when `continuationPoints` is missing or empty.

<h6>Usage example</h6>

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

Returns direct child references of a node.

<h6>Syntax</h6>

```js
children(childrenRequest)
```

<h6>Parameters</h6>

- `childrenRequest` (`object`): [ChildrenRequest](#childrenrequest)

<h6>Return value</h6>

- `object[]`: array of [ChildrenResult](#childrenresult)

Error behavior:

- Throws an error when `node` is missing or empty.

<h6>Usage example</h6>

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

| Property            | Type       | Default                      | Description |
|:--------------------|:-----------|:-----------------------------|:------------|
| nodes               | `string[]` |                              | List of OPC UA node IDs to read |
| maxAge              | `number`   | `0`                          | Maximum acceptable cache age in milliseconds |
| timestampsToReturn  | `number`   | `TimestampsToReturn.Neither` | Timestamp return policy |

## ReadResult

| Property        | Type     | Description |
|:----------------|:---------|:------------|
| status          | `number` | OPC UA status code (`uint32`) |
| statusText      | `string` | Status text |
| statusCode      | `string` | Status code name (for example, `StatusGood`) |
| value           | `any`    | Read value |
| type            | `string` | Value type name (for example, `Boolean`, `Int32`, `Double`) |
| sourceTimestamp | `number` | Unix epoch timestamp in milliseconds |
| serverTimestamp | `number` | Unix epoch timestamp in milliseconds |

## WriteRequest

| Property | Type     | Description |
|:---------|:---------|:------------|
| node     | `string` | Target node ID |
| value    | `any`    | Value to write |

## WriteResult

| Property      | Type         | Description |
|:--------------|:-------------|:------------|
| error         | `Error\|null` | Write error |
| timestamp     | `number`     | Response timestamp (Unix epoch milliseconds) |
| requestHandle | `number`     | OPC UA request handle |
| serviceResult | `number`     | OPC UA service result code |
| stringTable   | `string[]`   | OPC UA string table |
| results       | `number[]`   | Per-node status code array |

## BrowseRequest

| Property                       | Type       | Default                  | Description |
|:-------------------------------|:-----------|:-------------------------|:------------|
| nodes                          | `string[]` |                          | List of OPC UA node IDs to browse |
| browseDirection                | `number`   | `BrowseDirection.Forward` | Browse direction |
| referenceTypeId                | `string`   | all references           | Reference type node ID to follow |
| includeSubtypes                | `boolean`  | `true`                   | Whether to include subtypes of `referenceTypeId` |
| nodeClassMask                  | `number`   | `0`                      | Bitmask of node classes to include |
| resultMask                     | `number`   | `BrowseResultMask.All`   | Bitmask of fields to return |
| requestedMaxReferencesPerNode  | `number`   | `0`                      | Server hint for maximum references returned per node before pagination |

## BrowseNextRequest

| Property                  | Type        | Default | Description |
|:--------------------------|:------------|:--------|:------------|
| continuationPoints        | `string[]`  |         | Base64-encoded continuation points returned from `browse()` or `browseNext()` |
| releaseContinuationPoints | `boolean`   | `false` | Releases continuation points on the server without requesting more references |

## BrowseResult

| Property           | Type       | Description |
|:-------------------|:-----------|:------------|
| status             | `number`   | OPC UA status code (`uint32`) |
| statusText         | `string`   | Status text |
| continuationPoint  | `string`   | Base64-encoded continuation point. Empty string when there is no next page |
| references         | `object[]` | Array of [BrowseReference](#browsereference) |

## BrowseReference

| Property         | Type      | Description |
|:-----------------|:----------|:------------|
| referenceTypeId  | `string`  | Reference type node ID |
| isForward        | `boolean` | Whether the reference direction is forward |
| nodeId           | `string`  | Target node ID |
| browseName       | `string`  | Browse name |
| displayName      | `string`  | Display name |
| nodeClass        | `number`  | OPC UA node class value |
| typeDefinition   | `string`  | Type definition node ID |

## ChildrenRequest

| Property       | Type     | Description |
|:---------------|:---------|:------------|
| node           | `string` | Parent node ID |
| nodeClassMask  | `number` | Bitmask of node classes to include |

## ChildrenResult

| Property         | Type      | Description |
|:-----------------|:----------|:------------|
| referenceTypeId  | `string`  | Reference type node ID |
| isForward        | `boolean` | Whether the reference direction is forward |
| nodeId           | `string`  | Child node ID |
| browseName       | `string`  | Browse name |
| displayName      | `string`  | Display name |
| nodeClass        | `number`  | OPC UA node class value |
| typeDefinition   | `string`  | Type definition node ID |

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

## OPCUA Client

This example implements a collector that connects to an OPC UA server, reads system metrics,
and stores them in the database.

**Flow**

1. OPC UA integration: use the `opcua` module to connect to `opc.tcp://localhost:4840` and
    read node values such as `sys_cpu`, `sys_mem`, and `load1`.
2. Periodic collection: use `setInterval()` to read data every 10 seconds.
3. Data ingestion: store collected values in the `EXAMPLE` table (`name`, `time`, `value`).

### Data collector

Save the script as `opcua-client.js`, then run it in the background from the JSH terminal.

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

- `opcua-client.js`

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

### Simulator server

To test `opcua-client.js`, you need an OPC UA server that provides system metric nodes.
If you do not have a real environment, use the simulator from the repository below.
It provides sample data such as `sys_cpu`, `sys_mem`, `load1`, `load5`, and `load15`
to validate collection and visualization flows.

Follow the instructions in the repository to set it up.

[https://github.com/machbase/neo-server/tree/main/jsh/native/opcua/test_server](https://github.com/machbase/neo-server/tree/main/jsh/native/opcua/test_server)

After starting the simulator, run `opcua-client.js` and the OPC UA client will connect
and collect data.
