---
title: "os"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `os` module provides Node.js-compatible operating system information APIs for JSH applications.

## arch()

Returns CPU architecture.

<h6>Syntax</h6>

```js
arch()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.arch());
```

## platform()

Returns platform name such as `darwin`, `linux`, or `windows`.

<h6>Syntax</h6>

```js
platform()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.platform());
```

## type()

Returns OS type such as `Darwin`, `Linux`, or `Windows_NT`.

<h6>Syntax</h6>

```js
type()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.type());
```

## release()

Returns kernel release/version string.

<h6>Syntax</h6>

```js
release()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.release());
```

## hostname()

Returns host name.

<h6>Syntax</h6>

```js
hostname()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.hostname());
```

## homedir()

Returns current user home directory.

<h6>Syntax</h6>

```js
homedir()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.homedir());
```

## tmpdir()

Returns the default temporary directory path.

<h6>Syntax</h6>

```js
tmpdir()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.tmpdir());
```

## endianness()

Returns CPU endianness: `BE` or `LE`.

<h6>Syntax</h6>

```js
endianness()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.endianness());
```

## EOL

Platform-specific end-of-line marker.

- POSIX: `\n`
- Windows: `\r\n`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(JSON.stringify(os.EOL));
```

## totalmem(), freemem()

Returns total/free memory in bytes.

<h6>Syntax</h6>

```js
totalmem()
freemem()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println('total:', os.totalmem());
console.println('free :', os.freemem());
```

## uptime()

Returns system uptime in seconds.

<h6>Syntax</h6>

```js
uptime()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.uptime() >= 0);
```

## bootTime()

Returns system boot time as Unix timestamp.

<h6>Syntax</h6>

```js
bootTime()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(os.bootTime() > 0);
```

## loadavg()

Returns load averages as `[1min, 5min, 15min]`.

<h6>Syntax</h6>

```js
loadavg()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const avg = os.loadavg();
console.println(Array.isArray(avg), avg.length);
```

## cpus()

Returns per-CPU information array.

Each item includes fields like:

- `model`, `speed`, `cores`
- `vendor`, `family`, `model`, `stepping`
- `times.user`, `times.nice`, `times.sys`, `times.idle`, `times.irq` (milliseconds)

<h6>Syntax</h6>

```js
cpus()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const list = os.cpus();
console.println(Array.isArray(list), list.length > 0);
```

## cpuCounts()

Returns CPU count.

- `true`: logical CPU count
- `false`: physical CPU count

<h6>Syntax</h6>

```js
cpuCounts(logical)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println(os.cpuCounts(true));
console.println(os.cpuCounts(false));
```

## cpuPercent()

Returns CPU usage percentages.

- `intervalSec`: sampling interval in seconds (`0` for immediate)
- `perCPU`: return per-core values when `true`

<h6>Syntax</h6>

```js
cpuPercent(intervalSec, perCPU)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const os = require('os');
console.println(Array.isArray(os.cpuPercent(0, true)));
```

## networkInterfaces()

Returns network interface information object.

The object shape is:

- key: interface name
- value: array of address objects
  - `address`
  - `family` (`IPv4`/`IPv6`)
  - `internal` (boolean)

<h6>Syntax</h6>

```js
networkInterfaces()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const ifaces = os.networkInterfaces();
console.println(typeof ifaces);
```

## hostInfo()

Returns host information object.

Common fields include:

- `hostname`, `uptime`, `bootTime`, `procs`
- `os`, `platform`, `platformFamily`, `platformVersion`
- `kernelVersion`, `kernelArch`
- `virtualizationSystem`, `virtualizationRole`, `hostId`

<h6>Syntax</h6>

```js
hostInfo()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const info = os.hostInfo();
console.println(typeof info.hostname, typeof info.uptime);
```

## userInfo()

Returns current user information.

Returned fields include:

- `username`, `homedir`, `shell`
- `uid`, `gid`

<h6>Syntax</h6>

```js
userInfo([options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const user = os.userInfo();
console.println(user.username, user.homedir);
```

## diskPartitions()

Returns disk partition list.

<h6>Syntax</h6>

```js
diskPartitions([all])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const parts = os.diskPartitions();
console.println(Array.isArray(parts), parts.length >= 0);
```

## diskUsage()

Returns disk usage for the given path.

Typical fields include `total`, `used`, `free`, `usedPercent`.

<h6>Syntax</h6>

```js
diskUsage(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const usage = os.diskUsage('.');
console.println(typeof usage.total, typeof usage.usedPercent);
```

## diskIOCounters()

Returns disk I/O counters.

- `names` omitted or empty: all devices
- `names` specified: selected devices

<h6>Syntax</h6>

```js
diskIOCounters([names])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const counters = os.diskIOCounters();
console.println(typeof counters);
```

## netProtoCounters()

Returns network protocol counters.

<h6>Syntax</h6>

```js
netProtoCounters([proto])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const os = require('os');
const counters = os.netProtoCounters();
console.println(typeof counters);
```

## constants

An object that contains operating system related constants.

It currently provides the following child objects.

- `os.constants.signals`
- `os.constants.priority`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const os = require('os');

console.println(typeof os.constants.signals.SIGINT);
console.println(typeof os.constants.priority.PRIORITY_NORMAL);
```

## os.constants.signals

An object that provides signal names and their numeric values.

These constants use canonical Unix-style signal numbers for API compatibility.
On Windows, not every numeric value maps to a distinct native signal behavior.

For example, it includes entries such as:

| Literal | Number |
| --- | --- |
| `SIGHUP` | `1` |
| `SIGINT` | `2` |
| `SIGQUIT` | `3` |
| `SIGABRT` | `6` |
| `SIGKILL` | `9` |
| `SIGUSR1` | `10` |
| `SIGSEGV` | `11` |
| `SIGUSR2` | `12` |
| `SIGPIPE` | `13` |
| `SIGALRM` | `14` |
| `SIGTERM` | `15` |

These values can be passed to `process.kill()` as numeric signals.

On Windows, `SIGINT` is treated specially.
JSH attempts to deliver it as an interrupt-style console control event, which is the closest available equivalent.
By contrast, `SIGTERM`, `SIGQUIT`, and `SIGKILL` behave as termination requests on Windows.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[4]}
const os = require('os');
const process = require('process');

process.kill(12345, os.constants.signals.SIGTERM);
```

## Relationship With The process Signal API

`os.constants.signals` provides signal numbers, while the actual signal handling and delivery are performed by the `process` module.

- receive a signal: `process.on('SIGINT', handler)`
- send a signal: `process.kill(pid, os.constants.signals.SIGTERM)`

`process.on()` accepts case-insensitive signal names, but signal event names must still use the canonical `SIG`-prefixed form such as `SIGINT` or `sigint`.
Bare aliases such as `term` are not signal listener names.

`process.kill()` is more permissive and accepts aliases such as `term` in addition to canonical names.
By contrast, `os.constants.signals` exposes canonical constant names only.

On Windows, `process.kill(pid, os.constants.signals.SIGINT)` is best-effort and depends on Windows console routing rules.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,8]}
const os = require('os');
const process = require('process');

process.on('sigint', () => {
  console.println('caught');
});

process.kill(process.pid, os.constants.signals.SIGINT);
```

## os.constants.priority

An object that defines process priority levels.

<h6>Main fields</h6>

| Constant | Meaning |
| --- | --- |
| `PRIORITY_LOW` | low priority |
| `PRIORITY_BELOW_NORMAL` | below-normal priority |
| `PRIORITY_NORMAL` | normal default priority |
| `PRIORITY_ABOVE_NORMAL` | above-normal priority |
| `PRIORITY_HIGH` | high priority |
| `PRIORITY_HIGHEST` | highest priority |

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println(os.constants.priority.PRIORITY_NORMAL);
console.println(os.constants.priority.PRIORITY_HIGH);
```
