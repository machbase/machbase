---
title: "process"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `process` module is specifically designed for use in JSH applications.

## addShutdownHook()

Add a callback function that will be called at the termination of the current process.

<h6>Syntax</h6>

```js
addShutdownHook(()=>{})
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.addShutdownHook(()=>{
    console.println("shutdown hook called.");
})
console.println("running...")

// Output:
// running...
// shutdown hook called.
```

## arch

A string that identifies the operating system architecture of the host machine.
Common values include `amd64`, `aarch64`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.arch);
```

## argv

An array of command-line arguments passed to the current process.

- `argv[0]`: Absolute path to the JSH executable
- `argv[1]`: Name (or path) of the script being executed
- `argv[2:]`: Remaining arguments passed to the script

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('argv[0]:', process.argv[0]);
console.println('argv[1]:', process.argv[1]);
console.println('argv[2]:', process.argv[2]);
console.println('argv   :', process.argv);
```

## chdir()

Changes the current working directory.

If `path` is empty, JSH resolves it to `$HOME`.

<h6>Syntax</h6>

```js
chdir(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('before:', process.cwd());
process.chdir('/lib');
console.println('after :', process.cwd());
```

## cpuUsage()

Returns CPU usage information.

Current implementation returns placeholder numeric values (`0`) for both fields.

<h6>Returned fields</h6>

- `user`
- `system`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const cpu = process.cpuUsage();
console.println(typeof cpu.user, typeof cpu.system);
```

## cwd()

Returns the current working directory path.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.cwd());
```

## exit()

Exit the current process. If the *code* is omitted, default is `0`.

<h6>Syntax</h6>

```js
exit([code])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.exit(-1);
```


## which()

Finds a JavaScript command in `PATH` and returns the resolved file path.

If the command does not include `.js`, it is added automatically.

<h6>Syntax</h6>

```js
which(command)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.which('echo')); // e.g. /sbin/echo.js
```

## expand()

Expands environment variables such as `$HOME` and `${HOME}` in a string.

<h6>Syntax</h6>

```js
expand(value)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```

## env

The JSH runtime environment object.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.env.get('HOME'));
```


## exec()

Executes a JavaScript command file and returns its exit code.

<h6>Syntax</h6>

```js
exec(command, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const path = process.which('echo');
const code = process.exec(path, 'hello from exec');
console.println('exit code:', code);
```

## execPath

The absolute file path to the executable file of the current process on the host operating system.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.execPath);
```

## execString()

Executes JavaScript source code from a string and returns its exit code.

<h6>Syntax</h6>

```js
execString(source, ...args)

## hrtime()

Returns a high-resolution time tuple as `[seconds, nanoseconds]`.

If a previous tuple is provided, it returns the elapsed time from that point.

<h6>Syntax</h6>

```js
hrtime([previous])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const start = process.hrtime();
const diff = process.hrtime([start[0], start[1]]);
console.println(Array.isArray(diff), diff.length);
```

## kill()

Sends a real OS signal to the given process id.

- `pid` must be a positive integer.
- If `signal` is omitted, the default is `SIGTERM`.
- Returns `true` on success.
- Returns an `Error` object on failure.
- `signal` may be either a string name or a numeric signal number.

String signal names are case-insensitive, and the `SIG` prefix may be omitted.

This alias support applies to `process.kill()`.

Examples:

- `SIGTERM`
- `term`
- `sigint`

The following numeric signals are currently supported.

| Number | Literal |
| --- | --- |
| `0` | none |
| `1` | `SIGHUP` |
| `2` | `SIGINT` |
| `3` | `SIGQUIT` |
| `6` | `SIGABRT` |
| `9` | `SIGKILL` |
| `10` | `SIGUSR1` |
| `11` | `SIGSEGV` |
| `12` | `SIGUSR2` |
| `13` | `SIGPIPE` |
| `14` | `SIGALRM` |
| `15` | `SIGTERM` |

Signal `0` does not send a real signal. It can be used to check whether the target process exists and whether the caller has permission to signal it.

On Windows, `process.kill(pid, 'SIGINT')` does not behave like a Unix `kill(2)` signal send.
Instead, JSH tries to deliver an interrupt-style console control event to the target process group so that the target can observe it as a `SIGINT`-like interruption.
This is the closest available behavior to Node.js interrupt semantics on Windows, but it is best-effort.
In particular, it requires a console-attached target process group and may fail when Windows cannot route the control event.

On Windows, `SIGTERM`, `SIGQUIT`, and `SIGKILL` are handled as termination requests rather than Unix-style distinct signals.

<h6>Syntax</h6>

```js
kill(pid[, signal])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.kill(12345, 'SIGKILL'));
console.println(process.kill(12345, 'term'));
console.println(process.kill(12345, 15));
```

<h6>Windows interrupt example</h6>

```js
const process = require('process');
console.println(process.kill(12345, 'SIGINT'));
```

If Windows cannot route the control event, `process.kill()` returns an `Error` object.

<h6>Process existence check example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.kill(process.pid, 0));
```

## memoryUsage()

Returns memory usage information as an object.

Current implementation returns placeholder numeric values (`0`) for all fields.

<h6>Returned fields</h6>

- `rss`
- `heapTotal`
- `heapUsed`
- `external`
- `arrayBuffers`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const mem = process.memoryUsage();
console.println(typeof mem.rss, typeof mem.heapUsed);
```

## nextTick()

Schedules a callback to run on the next event loop turn.

If the first argument is not a function, this call does nothing and returns `undefined`.

<h6>Syntax</h6>

```js
nextTick(callback, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('main');
process.nextTick((a, b) => console.println('tick:', a, b), 'first', 'second');
```

## now()

Returns the current time as a JavaScript date-time object.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const now = process.now();
console.println(typeof now); // object
```

## pid

The process ID of the current process.
The value type is number and represents the process ID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.pid);
```

## platform

A string that identifies the operating system platform of the host machine. Common values include `windows`, `linux`, and `darwin` (macOS).

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.platform);
```

## ppid

The process ID of the parent process.
The value type is number and represents the parent process ID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.ppid);
```

## Signal Events

`process` can receive signal events like an `EventEmitter`.

At the time of writing, the following signal names are supported.

- `SIGHUP`
- `SIGINT`
- `SIGQUIT`
- `SIGABRT`
- `SIGKILL`
- `SIGUSR1`
- `SIGSEGV`
- `SIGUSR2`
- `SIGPIPE`
- `SIGALRM`
- `SIGTERM`

Signal event listener names are case-insensitive.
Event names must use the `SIG`-prefixed form.

For example, these names are treated the same.

- `SIGTERM`
- `sigterm`

Bare aliases such as `term` are not treated as signal event names.
They remain ordinary `EventEmitter` event names.

When a listener is registered, JSH forwards the corresponding OS signal as an event.
If no listener is registered, the process follows the operating system's default signal behavior.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');

process.on('sigint', () => {
    console.println('caught SIGINT');
});
```

<h6>Listener registration examples</h6>

```js
process.on('sigterm', handler);
process.once('SIGTERM', handler);
process.addListener('sigquit', handler);
```

## stdin, stdout, stderr

Streams for stdin, stdout, and stderr.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.stdout.write('Enter text: ');
const text = process.stdin.readLine();
console.println('Your input:', text);

// Output:
// Enter text: hello?
// Your input: hello?
```

## title

A string that identifies the current program.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.title);
```

## uptime()

Returns process uptime in seconds as a number.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const up = process.uptime();
console.println('uptime >= 0:', up >= 0);
```

## version

A string that identifies the JSH runtime version.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.version);
```

## versions

An object that provides detailed runtime version information.

- `versions.jsh`: JSH runtime version string
- `versions.go`: Go runtime version string

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('jsh:', process.versions.jsh);
console.println('go :', process.versions.go);
```

## which()

Finds a JavaScript command in `PATH` and returns the resolved file path.

If the command does not include `.js`, it is added automatically.

<h6>Syntax</h6>

```js
which(command)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.which('echo')); // e.g. /sbin/echo.js
```

## dispatchEvent()

Dispatches an event to an event emitter object on the JSH event loop.

This function returns `true` if the event is scheduled, `false` if the event loop is already terminated.

<h6>Syntax</h6>

```js
dispatchEvent(target, eventName, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.on('hello', (msg) => console.println(msg));
const ok = process.dispatchEvent(process, 'hello', 'from dispatchEvent');
console.println('scheduled:', ok);
```

## dumpStack()

Prints the current JavaScript call stack up to the specified depth for debugging.

<h6>Syntax</h6>

```js
dumpStack(depth)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
function trace() {
    process.dumpStack(5);
}
trace();
```

## expand()

Expands environment variables such as `$HOME` and `${HOME}` in a string.

<h6>Syntax</h6>

```js
expand(value)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```

