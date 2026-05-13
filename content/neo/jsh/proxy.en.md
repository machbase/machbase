---
title: Service Proxy
type: docs
weight: 120
---

{{< neo_since ver="8.5.2" />}}

A JSH service can run its own HTTP server and expose it through machbase-neo at `/web/services/<service_name>/<prefix>/*`.
The service developer does not need to publish the service port to external clients.
Instead, the service registers a proxy endpoint when it starts.
Clients access the service through the same origin as machbase-neo, avoiding separate port discovery and CORS configuration.

## Overview

A service proxy is registered dynamically by a running JSH service through `SERVICE_CONTROLLER`.
HTTP requests that reach a registered route are reverse proxied to the registered target server.

The public route format is:

```text
/web/services/<service_name>/<prefix>/*
```

For example, if the service name is `github.com/acme/chart` and the prefix is `/api/`, clients use this URL:

```text
/web/services/github.com/acme/chart/api/series
```

## Naming Rules

There is no separate namespace restriction for `service_name`.
The first process that registers a given `service_name` and `prefix` pair owns it.
A later registration with the same pair and a different target fails with a conflict error.

For packaged services, using the package name as `service_name` is recommended to avoid service name conflicts.

```javascript
service: 'github.com/acme/chart'
```

A single service can register multiple proxy endpoints.

```javascript
service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080'
}, callback);

service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/assets/',
    target: 'http://127.0.0.1:18081'
}, callback);
```

## Target Restrictions

The proxy target is limited to local endpoints that the machbase-neo server can safely access.

Allowed targets are:

- `http://127.0.0.1:<port>`
- `http://localhost:<port>`
- Other loopback IP addresses
- `unix://<absolute_socket_path>`

External hosts and `https://` targets are not allowed by default.
This prevents the service proxy from becoming an open proxy to arbitrary external addresses.

## Register

Use `proxy.register()` from the `service` module in service code.

```javascript
const service = require('service');

service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080'
}, function(err, entry) {
    if (err) {
        console.println('proxy register failed:', err.message);
        return;
    }
    console.println('proxy registered:', entry.service, entry.prefix);
});
```

A registration entry uses these fields:

| Field | Type | Description |
| --- | --- | --- |
| `service` | `String` | Service name in the public route |
| `prefix` | `String` | Proxy prefix under the service |
| `target` | `String` | Local HTTP or Unix socket endpoint that receives requests |
| `stripPrefix` | `String` | Optional. Public path prefix to remove before forwarding to the target |
| `healthPath` | `String` | Optional. Health check path metadata |

If `stripPrefix` is not specified, `/web/services/<service_name>/<prefix>` is removed before forwarding the request to the target.
For example, `/web/services/github.com/acme/chart/api/series` is delivered to the target server as `/series`.

**stripPrefix**

Use `stripPrefix` when the service's internal router expects part of the public path to remain.
For example, you can register the proxy prefix as `/api/` while keeping `/api/series` visible to the target server by stripping only the service base path.

```javascript
service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080',
    stripPrefix: '/web/services/github.com/acme/chart'
}, callback);
```

With this configuration, paths are forwarded as follows:

| Public request path | Path received by the target server |
| --- | --- |
| `/web/services/github.com/acme/chart/api/series` | `/api/series` |
| `/web/services/github.com/acme/chart/api/healthz` | `/api/healthz` |

If `stripPrefix` is omitted, the default strip prefix is `/web/services/github.com/acme/chart/api`, so the target server receives `/series` and `/healthz` instead.

## Unregister

It is recommended to unregister proxy endpoints when the service exits.

To unregister a specific prefix:

```javascript
service.proxy.unregister('github.com/acme/chart', '/api/', function(err) {
    if (err) {
        console.println('proxy unregister failed:', err.message);
    }
});
```

To unregister all endpoints for a service, omit the prefix.

```javascript
service.proxy.unregister('github.com/acme/chart', function(err) {
    if (err) {
        console.println('proxy unregister failed:', err.message);
    }
});
```

## Query

Use `proxy.list()` and `proxy.get()` to inspect current registrations.

```javascript
service.proxy.list('github.com/acme/chart', function(err, entries) {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(entries));
});

service.proxy.get('github.com/acme/chart', '/api/', function(err, entry) {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(entry));
});
```

## servicectl Management Commands

You can also inspect and manage runtime proxy registrations with `servicectl proxy`.
The command connects to `SERVICE_CONTROLLER`, so use the `--controller` option or the `SERVICE_CONTROLLER` environment variable.

```sh
servicectl proxy list
servicectl proxy list github.com/acme/chart
servicectl proxy get github.com/acme/chart /api/
```

For tests or manual operation, you can also register proxy endpoints directly from the CLI.

```sh
servicectl proxy register github.com/acme/chart /api/ http://127.0.0.1:18080 --health-path /healthz
servicectl proxy unregister github.com/acme/chart /api/
```

If you omit the prefix, as in `proxy unregister <service_name>`, all proxy endpoints registered under that service name are removed.
In normal service code, registering with `service.proxy.register()` on startup and unregistering with `service.proxy.unregister()` on exit is still recommended. Use `servicectl proxy` mostly for operations and debugging.

## TCP Example

This example starts a local HTTP server and registers it at `/web/services/github.com/acme/chart/api/*`.

```javascript
const http = require('http');
const service = require('service');

const serviceName = 'github.com/acme/chart';
const port = 18080;

const server = new http.Server({ network: 'tcp', address: '127.0.0.1:' + port });

server.get('/healthz', function(ctx) {
    ctx.text(http.status.OK, 'ok');
});

server.get('/*path', function(ctx) {
    ctx.json(http.status.OK, { path: ctx.request.path });
});

server.serve(function() {
    service.proxy.register({
        service: serviceName,
        prefix: '/api/',
        target: 'http://127.0.0.1:' + port,
        healthPath: '/healthz'
    }, function(err) {
        if (err) {
            console.println('proxy register failed:', err.message);
            return;
        }
        console.println('proxy ready:', '/web/services/' + serviceName + '/api/');
    });
});

process.on('exit', function() {
    server.close();
    service.proxy.unregister(serviceName, '/api/', function() {});
});
```

## Unix Domain Socket Example

JSH `http.Server` supports `network: 'unix'`.
Binding the service HTTP server to a Unix domain socket avoids opening a service-specific TCP port while still allowing the service proxy to reach it.
Use an absolute socket path after the `unix://` target scheme.

```javascript
const http = require('http');
const service = require('service');

const serviceName = 'github.com/acme/chart';
const socketPath = '/tmp/acme-chart.sock';

const server = new http.Server({ network: 'unix', address: socketPath });

server.get('/healthz', function(ctx) {
    ctx.text(http.status.OK, 'ok');
});

server.get('/*path', function(ctx) {
    ctx.json(http.status.OK, { path: ctx.request.path });
});

server.serve(function() {
    service.proxy.register({
        service: serviceName,
        prefix: '/api/',
        target: 'unix://' + socketPath,
        healthPath: '/healthz'
    }, function(err) {
        if (err) {
            console.println('proxy register failed:', err.message);
            server.close();
            return;
        }
        console.println('proxy ready:', '/web/services/' + serviceName + '/api/');
    });
});

process.on('exit', function() {
    server.close();
    service.proxy.unregister(serviceName, '/api/', function() {});
});
```

For example, `/web/services/github.com/acme/chart/api/series` is forwarded to `/series` on the service server connected through the Unix socket.
The socket path must be absolute. In production, use a path that does not conflict with other services.

## Notes

- Registrations are runtime state. A service must register again after restart.
- The first process to register a `service_name` and `prefix` pair owns that route.
- Unregistered `/web/services/<service_name>/<prefix>/*` requests do not fall back to other package handlers.
- Services should use loopback addresses or Unix domain sockets instead of public external ports.
