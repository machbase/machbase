---
title: "os"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

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

## type()

Returns OS type such as `Darwin`, `Linux`, or `Windows_NT`.

<h6>Syntax</h6>

```js
type()
```

## release()

Returns kernel release/version string.

<h6>Syntax</h6>

```js
release()
```

## hostname()

Returns host name.

<h6>Syntax</h6>

```js
hostname()
```

## homedir()

Returns current user home directory.

<h6>Syntax</h6>

```js
homedir()
```

## tmpdir()

Returns the default temporary directory path.

<h6>Syntax</h6>

```js
tmpdir()
```

## endianness()

Returns CPU endianness: `BE` or `LE`.

<h6>Syntax</h6>

```js
endianness()
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

## bootTime()

Returns system boot time as Unix timestamp.

<h6>Syntax</h6>

```js
bootTime()
```

## loadavg()

Returns load averages as `[1min, 5min, 15min]`.

<h6>Syntax</h6>

```js
loadavg()
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

## userInfo()

Returns current user information.

Returned fields include:

- `username`, `homedir`, `shell`
- `uid`, `gid`

<h6>Syntax</h6>

```js
userInfo([options])
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

## diskIOCounters()

Returns disk I/O counters.

- `names` omitted or empty: all devices
- `names` specified: selected devices

<h6>Syntax</h6>

```js
diskIOCounters([names])
```

## netProtoCounters()

Returns network protocol counters.

<h6>Syntax</h6>

```js
netProtoCounters([proto])
```

## constants

OS constants object.

<h6>Main fields</h6>

- `constants.signals`
  - `SIGHUP`, `SIGINT`, `SIGQUIT`, `SIGILL`, `SIGTRAP`, `SIGABRT`, `SIGBUS`, `SIGFPE`, `SIGKILL`, `SIGUSR1`, `SIGSEGV`, `SIGUSR2`, `SIGPIPE`, `SIGALRM`, `SIGTERM`
- `constants.priority`
  - `PRIORITY_LOW`, `PRIORITY_BELOW_NORMAL`, `PRIORITY_NORMAL`, `PRIORITY_ABOVE_NORMAL`, `PRIORITY_HIGH`, `PRIORITY_HIGHEST`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const os = require('os');
console.println(os.constants.signals.SIGINT);
console.println(os.constants.priority.PRIORITY_NORMAL);
```
