---
title: "service"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `service` module is a client module for calling the service controller JSON-RPC API from JSH applications.

Typical usage looks like this.

```js
const service = require('service');
```

The service controller address is usually taken from the `SERVICE_CONTROLLER` environment variable prepared by the shell or session.

The controller may listen on a random address for each run, so it is usually not something you hardcode in an application.
Use `options.controller` only when you already know an explicit controller address or intentionally want to talk to a different controller.

## createClient()

Creates a `Client` instance that talks to the service controller.

<h6>Syntax</h6>

```js
createClient([options])
```

<h6>Options</h6>

| Option     | Type   | Default | Description |
|:-----------|:-------|:--------|:------------|
| controller | String |         | Explicit controller address. If omitted, the client uses the `SERVICE_CONTROLLER` environment variable. |
| timeout    | Number | `5000`  | RPC timeout in milliseconds. The same value is also used to keep the callback-based request alive until it completes or times out. |

`controller` does not have a fixed built-in default address.
If neither `SERVICE_CONTROLLER` nor `options.controller` is available, client creation fails.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = service.createClient({ timeout: 1000 });
```

This example assumes `SERVICE_CONTROLLER` is already set in the runtime environment.

Only pass `controller` explicitly when you need to override that default.

```js {linenos=table,linenostart=1}
const service = require('service');
const client = service.createClient({
    controller: 'unix:///tmp/example-service-controller.sock',
    timeout: 1000,
});
```

## call()

Calls an arbitrary service controller RPC method directly.

<h6>Syntax</h6>

```js
call(method[, params][, options], callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');

service.call('service.list', null, (err, result) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(result.length);
});
```

## Client

The client returned by `createClient()`.

<h6>Main properties</h6>

- `controller`
- `timeout`
- `runtime`
- `details`

**Client methods**

- `call(method[, params], callback)`
- `list(callback)`
- `get(name, callback)`
- `read(callback)`
- `update(callback)`
- `reload(callback)`
- `install(config, callback)`
- `uninstall(name, callback)`
- `start(name, callback)`
- `stop(name, callback)`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = service.createClient();

client.list((err, services) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println('count=', services.length);
});
```

## runtime.get()

Gets the runtime snapshot of a service.

- The result includes `output` and `details`.

<h6>Syntax</h6>

```js
runtime.get(name[, options], callback)
client.runtime.get(name, callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');

service.runtime.get('alpha', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(runtime.details || {}));
});
```

## details.get()

Gets service detail values.

- If `key` is omitted, the full `details` snapshot is returned.
- If `key` is specified and missing, the callback receives an error.

<h6>Syntax</h6>

```js
details.get(name[, key][, options], callback)
client.details.get(name[, key], callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');

service.details.get('alpha', 'health', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(runtime.details.health);
});
```

## details.add()

Adds a new detail key/value pair.

- Returns an error if the key already exists.

<h6>Syntax</h6>

```js
details.add(name, key, value[, options], callback)
client.details.add(name, key, value, callback)
```

## details.update()

Updates an existing detail key/value pair.

- Returns an error if the key does not exist.

<h6>Syntax</h6>

```js
details.update(name, key, value[, options], callback)
client.details.update(name, key, value, callback)
```

## details.set()

Sets a detail key/value pair.

- Creates the key if it does not exist, or overwrites it if it does.

<h6>Syntax</h6>

```js
details.set(name, key, value[, options], callback)
client.details.set(name, key, value, callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');

service.details.set('alpha', 'health', 'ok', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(runtime.details.health);
});
```

## details.delete()

Deletes a detail key.

- Returns an error if the key does not exist.

<h6>Syntax</h6>

```js
details.delete(name, key[, options], callback)
client.details.delete(name, key, callback)
```

## parseController()

Parses a controller address string.

- Supported formats: `host:port`, `tcp://host:port`, `unix://path`

<h6>Syntax</h6>

```js
parseController(value)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const endpoint = service.parseController('unix:///tmp/example-service-controller.sock');
console.println(endpoint.network, endpoint.path);
```

## resolveController()

Resolves the controller address.

- If an argument is provided, it is used.
- If omitted, the `SERVICE_CONTROLLER` environment variable is used.

<h6>Syntax</h6>

```js
resolveController([value])
```

<h6>Behavior example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
console.println(service.resolveController());
console.println(service.resolveController('unix:///tmp/example-service-controller.sock'));
```

## Behavior notes

- All APIs use a callback-based asynchronous style.
- Promise / `await` is not used.
- Connection failures, timeouts, and RPC errors are returned as the first callback argument.
- While a service RPC is pending, the module keeps the request alive internally so that a short top-level script does not exit before the callback runs.
- The keepalive window follows the effective `timeout` value and is released when the request completes, fails, or times out.
- `createClient()`, `call()`, `runtime.get()`, and `details.*()` use `SERVICE_CONTROLLER` by default when `options.controller` is omitted.
- Top-level helpers such as `service.details.get(...)` create a client internally for each call.
