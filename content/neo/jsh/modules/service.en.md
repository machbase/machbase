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

## Client

`Client` is the main service controller client type.

Create it directly with `new service.Client(...)` when you want to keep a reusable client instance.

<h6>Syntax</h6>

```js
new Client([options])
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
const client = new service.Client({ timeout: 1000 });
```

This example assumes `SERVICE_CONTROLLER` is already set in the runtime environment.

Only pass `controller` explicitly when you need to override that default.

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client({
    controller: 'unix:///tmp/example-service-controller.sock',
    timeout: 1000,
});
```

<h6>Main properties</h6>

- `controller`
- `timeout`
- `runtime`
- `details`

**Client methods**

- `call(method[, params], callback)`
- `status([name], callback)`
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
const client = new service.Client();

client.status((err, services) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println('count=', services.length);
});
```

## call()

Calls an arbitrary service controller RPC method directly.

<h6>Syntax</h6>

```js
client.call(method[, params], callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.call('service.list', null, (err, result) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(result.length);
});
```

## status()

Gets the current service status.

- If `name` is omitted, it returns the service list snapshot.
- If `name` is specified, it returns the snapshot of a single service.
- This method matches the `servicectl status [service_name]` command shape.

<h6>Syntax</h6>

```js
client.status([name], callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.status((err, services) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println('count=', services.length);
});

client.status('alpha', (err, snapshot) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(snapshot.status);
});
```

## read()

Reads the service config directory and returns the latest reread snapshot.

<h6>Syntax</h6>

```js
client.read(callback)
```

## update()

Applies the current reread snapshot and returns the update result.

- `update()` applies only the current reread delta.
- It stops, starts, adds, or removes only the services affected by the reread result.

<h6>Syntax</h6>

```js
client.update(callback)
```

## reload()

Reads configs and immediately applies the reload result in one call.

- Unlike `update()`, `reload()` first stops every currently running service.
- After that, it starts only services whose config is enabled.
- This means services that were running before `reload()` are not restarted unless they are enabled in the current config.

<h6>Syntax</h6>

```js
client.reload(callback)
```

## install()

Installs a service from a config object and returns the installed service snapshot.

<h6>Syntax</h6>

```js
client.install(config, callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.install({
    name: 'alpha',
    enable: false,
    executable: 'echo',
    args: ['hello'],
}, (err, snapshot) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(snapshot.config.name, snapshot.status);
});
```

## uninstall()

Uninstalls a service and returns `true` on success.

<h6>Syntax</h6>

```js
client.uninstall(name, callback)
```

## start()

Starts a service and returns the updated service snapshot.

<h6>Syntax</h6>

```js
client.start(name, callback)
```

## stop()

Stops a service and returns the updated service snapshot.

<h6>Syntax</h6>

```js
client.stop(name, callback)
```

## runtime.get()

Gets the runtime snapshot of a service.

- The result includes `output` and `details`.

<h6>Syntax</h6>

```js
client.runtime.get(name, callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.runtime.get('alpha', (err, runtime) => {
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
client.details.get(name[, key], callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.details.get('alpha', 'health', (err, runtime) => {
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
client.details.add(name, key, value, callback)
```

## details.update()

Updates an existing detail key/value pair.

- Returns an error if the key does not exist.

<h6>Syntax</h6>

```js
client.details.update(name, key, value, callback)
```

## details.set()

Sets a detail key/value pair.

- Creates the key if it does not exist, or overwrites it if it does.

<h6>Syntax</h6>

```js
client.details.set(name, key, value, callback)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.details.set('alpha', 'health', 'ok', (err, runtime) => {
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
client.details.delete(name, key, callback)
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
- Connection failures, timeouts, and RPC errors are returned as the first callback argument.
- While a service RPC is pending, the module keeps the request alive internally so that a short top-level script does not exit before the callback runs.
- The keepalive window follows the effective `timeout` value and is released when the request completes, fails, or times out.
- `new Client()` uses `SERVICE_CONTROLLER` by default when `options.controller` is omitted.
