---
title: "dbus"
type: docs
weight: 100
---

{{< neo_since ver="8.5.5" />}}

The `dbus` module provides Linux-only D-Bus APIs for JSH applications.
It supports method calls, property access, introspection, signal subscription, and name-owner watching.

## Module load

```js
const dbus = require("dbus");
const conn = new dbus.Connection({ busType: dbus.BusType.Session });
```

If the runtime OS is not Linux, creating a connection fails.

## BusType

- `dbus.BusType.Session`
- `dbus.BusType.System`

## Connection

D-Bus connection object.

<h6>Creation</h6>

```js
new dbus.Connection(options)
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| busType | `string` | `dbus.BusType.Session` | D-Bus bus type |

<h6>Return value</h6>

- `Connection`

Error behavior:

- Throws when `busType` is invalid.
- Throws when the platform is not Linux.

### close()

Closes the current D-Bus connection.

<h6>Syntax</h6>

```js
conn.close()
```

<h6>Return value</h6>

- `undefined`

This method is idempotent and can be called more than once.

### object()

Creates an [ObjectProxy](#objectproxy) bound to destination/path.

<h6>Syntax</h6>

```js
conn.object(destination, path)
```

<h6>Parameters</h6>

- `destination` (`string`): Service name (for example, `org.freedesktop.DBus`)
- `path` (`string`): Object path (for example, `/org/freedesktop/DBus`)

<h6>Return value</h6>

- `ObjectProxy`

### call()

Calls a D-Bus method.

<h6>Syntax</h6>

```js
conn.call(request)
```

<h6>Parameters</h6>

- `request` (`object`): [CallRequest](#callrequest)

<h6>Return value</h6>

- `object`: [CallResult](#callresult)

Error behavior:

- Throws when required fields are missing.
- Throws when the object path is invalid.

### getProperty()

Reads a D-Bus property.

<h6>Syntax</h6>

```js
conn.getProperty(request)
```

<h6>Parameters</h6>

- `request` (`object`): [PropertyRequest](#propertyrequest)

<h6>Return value</h6>

- `object`: [PropertyResult](#propertyresult)

### setProperty()

Writes a D-Bus property.

<h6>Syntax</h6>

```js
conn.setProperty(request)
```

<h6>Parameters</h6>

- `request` (`object`): [SetPropertyRequest](#setpropertyrequest)

<h6>Return value</h6>

- `undefined`

### introspect()

Gets introspection metadata for an object.

<h6>Syntax</h6>

```js
conn.introspect(request)
```

<h6>Parameters</h6>

- `request` (`object`): [IntrospectRequest](#introspectrequest)

<h6>Return value</h6>

- `object`: [IntrospectionNode](#introspectionnode)

### subscribeSignal()

Subscribes to D-Bus signals matching criteria.

<h6>Syntax</h6>

```js
conn.subscribeSignal(request)
```

<h6>Parameters</h6>

- `request` (`object`): [SignalWatchRequest](#signalwatchrequest)

<h6>Return value</h6>

- `Connection` (for chaining)

Error behavior:

- Throws `missing signal match criteria` when all match fields are empty.

### unsubscribeSignal()

Unsubscribes a previously registered signal match.

<h6>Syntax</h6>

```js
conn.unsubscribeSignal(request)
```

<h6>Parameters</h6>

- `request` (`object`): [SignalWatchRequest](#signalwatchrequest)

<h6>Return value</h6>

- `Connection` (for chaining)

Error behavior:

- Throws when no matching subscription exists.

### watchName()

Starts watching owner changes for a bus name.

<h6>Syntax</h6>

```js
conn.watchName(name)
```

<h6>Parameters</h6>

- `name` (`string`): D-Bus well-known name

<h6>Return value</h6>

- `Connection` (for chaining)

### unwatchName()

Stops watching owner changes for a bus name.

<h6>Syntax</h6>

```js
conn.unwatchName(name)
```

<h6>Parameters</h6>

- `name` (`string`): D-Bus well-known name

<h6>Return value</h6>

- `Connection` (for chaining)

Error behavior:

- Throws `name watch not found` when there is no active watch for the name.

### getNameOwner()

Gets the current owner for a bus name.

<h6>Syntax</h6>

```js
conn.getNameOwner(name)
```

<h6>Parameters</h6>

- `name` (`string`): D-Bus well-known name

<h6>Return value</h6>

- `object`: [NameOwnerResult](#nameownerresult)

If the name has no owner, this method does not throw and returns `hasOwner: false`.

## Events

`Connection` extends `EventEmitter`.

### signal

Emitted on every subscribed D-Bus signal.

```js
conn.on("signal", (sig) => {
    console.println(sig.interface, sig.member, sig.body);
});
```

### name-owner-changed

Emitted when a watched name changes owner.

```js
conn.on("name-owner-changed", (evt) => {
    console.println(evt.name, evt.oldOwner, evt.newOwner);
});
```

## ObjectProxy

Created with `conn.object(destination, path)`.

### call()

```js
obj.call(method, ...args)
```

- Returns: same shape as [CallResult](#callresult)

### getProperty() / get()

```js
obj.getProperty(name, interfaceName)
obj.get(name, interfaceName)
```

- `getProperty()` returns [PropertyResult](#propertyresult)
- `get()` returns the property value only (`result.value`)

### setProperty() / set()

```js
obj.setProperty(name, value, interfaceName)
obj.set(name, value, interfaceName)
```

### introspect()

```js
obj.introspect()
```

- Returns: [IntrospectionNode](#introspectionnode)

### subscribeSignal() / unsubscribeSignal()

```js
obj.subscribeSignal(member, interfaceName)
obj.unsubscribeSignal(member, interfaceName)
```

These are convenience wrappers that pass destination/path automatically.

## Request/response structures

## CallRequest

| Property | Type | Description |
|:---------|:-----|:------------|
| destination | `string` | Service name |
| path | `string` | Object path |
| method | `string` | Fully qualified method name (`Interface.Method`) |
| args | `any[]` | Method arguments |
| flags | `number` | D-Bus call flags |

## CallResult

| Property | Type | Description |
|:---------|:-----|:------------|
| destination | `string` | Service name |
| path | `string` | Object path |
| method | `string` | Method name used for the call |
| body | `any[]` | Returned values |

## PropertyRequest

| Property | Type | Description |
|:---------|:-----|:------------|
| destination | `string` | Service name |
| path | `string` | Object path |
| interface | `string` | Interface name |
| name | `string` | Property name |

## PropertyResult

| Property | Type | Description |
|:---------|:-----|:------------|
| signature | `string` | D-Bus signature |
| value | `any` | Property value |

## SetPropertyRequest

| Property | Type | Description |
|:---------|:-----|:------------|
| destination | `string` | Service name |
| path | `string` | Object path |
| interface | `string` | Interface name |
| name | `string` | Property name |
| value | `any` | Property value to write |

## IntrospectRequest

| Property | Type | Description |
|:---------|:-----|:------------|
| destination | `string` | Service name |
| path | `string` | Object path |

## IntrospectionNode

| Property | Type | Description |
|:---------|:-----|:------------|
| name | `string` | Node path/name |
| interfaces | `object[]` | Interface metadata list |
| children | `object[]` | Child node list |

Each interface includes methods/signals/properties/annotations.

## SignalWatchRequest

| Property | Type | Description |
|:---------|:-----|:------------|
| destination | `string` | Optional, kept for symmetry with object-based calls |
| sender | `string` | Signal sender filter |
| path | `string` | Object path filter |
| interface | `string` | Interface filter |
| member | `string` | Member filter |

At least one of `sender`, `path`, `interface`, `member` must be provided.

## NameOwnerResult

| Property | Type | Description |
|:---------|:-----|:------------|
| name | `string` | Requested bus name |
| owner | `string` | Unique name (`:1.xx`) or empty string |
| hasOwner | `boolean` | Whether an owner currently exists |

## Usage examples

### 1) Basic method call

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

const temp = obj.call("com.plc.manufacture.Interval.GetTemperature");
console.println("temperature:", temp.body[0]);

conn.close();
```

### 2) Property read and write

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const dev = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));
dev.set("Mode", "MANUAL", "com.plc.manufacture.Status");
console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));

conn.close();
```

### 3) Introspection

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");
const node = obj.introspect();

for (const iface of node.interfaces) {
    console.println("iface:", iface.name);
}

conn.close();
```

### 4) Signal subscription

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

obj.subscribeSignal("TemperatureChanged", "com.plc.manufacture.Interval");
conn.on("signal", (sig) => {
    if (sig.member !== "TemperatureChanged") {
        return;
    }
    console.println("temperature changed:", sig.body[0]);
});
```

### 5) Name watch

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const name = "com.example.Worker";

const owner = conn.getNameOwner(name);
console.println("has owner:", owner.hasOwner);

conn.watchName(name);
conn.on("name-owner-changed", (evt) => {
    if (evt.name === name) {
        console.println("owner changed:", evt.oldOwner, "->", evt.newOwner);
    }
});
```

## Error behavior notes

- Calling methods after `conn.close()` throws `connection not initialized`.
- Missing required fields in request objects throws an error.
- Invalid object paths throw an error.
- `getNameOwner()` returns `{ hasOwner: false }` when the name exists but has no owner.
- D-Bus tests and runtime behavior are Linux-only.
