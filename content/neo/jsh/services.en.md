---
title: Service Manager
type: docs
weight: 100
---

The `service` command manages long-running JSH services through a service controller.
It can read service configurations, install or uninstall services, start and stop them,
and inspect current runtime state.

## Overview

The `service` command talks to a running service controller over JSON-RPC.
It does not directly launch services by itself. Instead, it sends management requests such as:

- Read configuration files
- Apply configuration updates
- Install a service from a JSON file or inline options
- Start and stop a service
- Show service status
- Remove a service registration

## Controller Address

The command requires a controller endpoint.
You can pass it explicitly with `--controller`, or provide it through the `SERVICE_CONTROLLER`
environment variable.

When the `service` command is launched by the machbase-neo runtime, the runtime sets
`SERVICE_CONTROLLER` automatically. In normal JSH service-management workflows, you usually do not
need to specify `--controller` explicitly, so the examples below omit it for readability.

Supported controller address formats are:

- `host:port`
- `tcp://host:port`
- `unix://path`

<h6>Syntax</h6>

```sh
service [--controller=<addr>] <command> [args...]
```

<h6>Common options</h6>

- `-c, --controller <endpoint>` controller address in TCP or Unix socket form
- `-t, --timeout <msec>` RPC timeout in milliseconds, default `5000`
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > service status
```

## Commands

The `service` command supports these subcommands:

- `read`
- `update`
- `reload`
- `install <config.json>`
- `install --name <name> --executable <path> [--arg <arg> ...] [--working-dir <dir>] [--enable] [--env KEY=VALUE ...]`
- `uninstall <service_name>`
- `status [service_name]`
- `start <service_name>`
- `stop <service_name>`
- `details get <service_name> [key] [--format box|json]`
- `details set <service_name> <key> <value> [--detail-type <string|number|boolean|bool|object|json>]`
- `details delete <service_name> <key>`

## Service Configuration Format

A service definition is a JSON object.

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work/app",
  "environment": {
    "APP_MODE": "prod",
    "PORT": "8080"
  },
  "executable": "server.js",
  "args": ["--port", "8080"]
}
```

Common fields are:

| Field | Type | Description |
| --- | --- | --- |
| `name` | `String` | Service name |
| `enable` | `Boolean` | Whether the service should be enabled |
| `working_dir` | `String` | Working directory for the service process |
| `environment` | `Object` | Environment variables as `KEY: VALUE` pairs |
| `executable` | `String` | Executable path or command name |
| `args` | `Array<String>` | Command-line arguments |

## status

Shows either the full service list or one service detail.

<h6>Syntax</h6>

```sh
service status [service_name]
```

When called without a service name, it prints a table with service name, enabled state,
runtime status, PID, and executable.

<h6>Usage example: list services</h6>

```sh
/work > service status
┌───────┬─────────┬─────────┬─────┬────────────┐
│ NAME  │ ENABLED │ STATUS  │ PID │ EXECUTABLE │
├───────┼─────────┼─────────┼─────┼────────────┤
│ alpha │ yes     │ running │ 101 │ echo       │
│ beta  │ no      │ stopped │ -   │ /bin/date  │
└───────┴─────────┴─────────┴─────┴────────────┘
```

With a service name, it prints detailed status including working directory, environment,
and recent output lines.

<h6>Usage example: one service</h6>

```sh
/work > service status alpha
[alpha] ENABLED
  status: running
  exit_code: 0
  pid: 55
  start: echo [ hello, world ]
  cwd: /work
  environment:
    A=1
    B=2
  output:
    line-6
    ...
    line-25
```

## read

Reads service configuration files from the controller configuration directory and reports changes.

<h6>Syntax</h6>

```sh
service read
```

The result is rendered as a single table. Each row includes a `STATUS`
column whose value is one of `UNCHANGED`, `ADDED`, `UPDATED`, `REMOVED`, or `ERRORED`.

The table is rendered in the same pretty box format used by the `service status` list output.

<h6>Usage example</h6>

```sh
/work > service read
┌────────┬───────────┬────────────┬──────────────┬─────────────┬────────────┐
│ NAME   │ STATUS    │ EXECUTABLE │ READ_ERROR   │ START_ERROR │ STOP_ERROR │
├────────┼───────────┼────────────┼──────────────┼─────────────┼────────────┤
│ alpha  │ UNCHANGED │ echo       │              │             │            │
│ beta   │ ADDED     │ node       │              │             │            │
│ old    │ REMOVED   │ sleep      │              │             │            │
│ broken │ ERRORED   │            │ invalid json │             │            │
└────────┴───────────┴────────────┴──────────────┴─────────────┴────────────┘
```

## update and reload

Both commands ask the controller to apply configuration changes.

- `update` applies only the currently detected configuration changes. Added, removed, and updated services are reconciled, while unrelated services are left as-is.
- `reload` rereads configuration files, stops all currently running services first, applies the configuration changes, and then starts only services with `enable=true`.

<h6>Syntax</h6>

```sh
service update
service reload
```

The output contains two sections:

- `ACTIONS`, which lists performed actions such as `UPDATE stop`, `UPDATE start`, `RELOAD stop`, or `RELOAD start`
- `SERVICES`, which shows the resulting service table

## install

Installs a service either from a JSON file or from inline options.
After a successful install, the controller writes the service definition to
`/etc/services/<name>.json`. The file name is determined by the service `name`
from the JSON file or from the `--name` option.

### Install from JSON file

<h6>Syntax</h6>

```sh
service install <config.json>
```

<h6>Usage example</h6>

```sh
/work > service install svc.json
```

If `svc.json` contains `"name": "alpha"`, the installed configuration is stored as
`/etc/services/alpha.json`.

### Install with inline options

<h6>Syntax</h6>

```sh
service install \
  --name <service_name> \
  --executable <path> \
  [--working-dir <dir>] \
  [--enable] \
  [--arg <arg> ...] \
  [--env KEY=VALUE ...]
```

<h6>Inline install options</h6>

- `-n, --name <name>` service name
- `-x, --executable <path>` executable path or command name
- `-w, --working-dir <dir>` working directory
- `--enable` enable the service immediately
- `-a, --arg <arg>` add one executable argument, repeatable
- `-e, --env KEY=VALUE` add one environment variable, repeatable

<h6>Usage example</h6>

```sh
/work > service install \
  --name svc-inline \
  --executable node \
  --working-dir /work/app \
  --enable \
  --arg app.js \
  --arg --port \
  --arg 8080 \
  --env APP_MODE=prod \
  --env PORT=8080
```

This inline form also creates `/etc/services/svc-inline.json` on the controller side.

The command prints a `RESULT` table and then a detailed `SERVICE` section.

## start and stop

Starts or stops a named service.

<h6>Syntax</h6>

```sh
service start <service_name>
service stop <service_name>
```

The output includes the operation result and the current service state.

<h6>Usage example</h6>

```sh
/work > service start alpha
/work > service stop alpha
```

## details

Manages runtime detail values exposed by a service.
These values are separate from the static service configuration and are intended for
runtime metadata such as health status, counters, labels, or custom structured state.

<h6>Syntax</h6>

```sh
service details get <service_name> [key] [--format box|json]
service details set <service_name> <key> <value> [--detail-type <string|number|boolean|bool|object|json>]
service details delete <service_name> <key>
```

<h6>Details options</h6>

- `--format <box|json>` output format for `details get`, default `box`
- `--detail-type <type>` value type for `details set`, default `string`

Supported detail value types are:

- `string`, the default when `--detail-type` is omitted
- `number`
- `boolean` or `bool`
- `object` or `json`

Type handling rules:

- `string` stores the input text as-is
- `number` parses the input as a JSON number
- `boolean` and `bool` parse the input as JSON `true` or `false`
- `object` and `json` parse the input as a JSON object, not an array or scalar

`details set` uses a single RPC request and behaves as an upsert. If the key already exists,
its value is replaced. If it does not exist, the key is created.

When `--format json` is used:

- `service details get <service_name>` prints the full details object
- `service details get <service_name> <key>` prints a JSON object containing only that key

<h6>Usage example: box output</h6>

```sh
/work > service details get alpha
DETAILS (3)
┌─────────┬─────────┬────────────────────┐
│ KEY     │ TYPE    │ VALUE              │
├─────────┼─────────┼────────────────────┤
│ enabled │ boolean │ true               │
│ labels  │ object  │ {"tier":"gold"}    │
│ retries │ number  │ 3                  │
└─────────┴─────────┴────────────────────┘
```

<h6>Usage example: JSON output</h6>

```sh
/work > service details get alpha labels --format json
{
  "labels": {
    "tier": "gold"
  }
}
```

<h6>Usage example: set values</h6>

```sh
/work > service details set alpha mode warm
/work > service details set alpha retries 3 --detail-type number
/work > service details set alpha enabled true --detail-type bool
/work > service details set alpha labels '{"tier":"gold"}' --detail-type json
```

<h6>Usage example: delete a key</h6>

```sh
/work > service details delete alpha labels
```

## uninstall

Removes a service registration.

<h6>Syntax</h6>

```sh
service uninstall <service_name>
```

<h6>Usage example</h6>

```sh
/work > service uninstall alpha
RESULT
uninstall alpha yes removed
```

## Typical Workflow

Create a service JSON file:

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work",
  "executable": "echo",
  "args": ["hello", "world"]
}
```

Then manage it with these commands:

```sh
/work > service install alpha.json
/work > service status
/work > service stop alpha
/work > service start alpha
/work > service uninstall alpha
```

## Notes

- `service` requires a reachable controller endpoint.
- `status` without an argument lists all services; with one argument it shows one service in detail.
- `install` cannot mix a config file path with inline install options.
- Inline `--env` values must use `KEY=VALUE` form.
- Relative config file paths are resolved from the current working directory.