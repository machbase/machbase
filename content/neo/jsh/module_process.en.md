---
title: "process"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

The `process` module is specifically designed for use in JSH applications.

## env

The JSH runtime environment object.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.env.get('HOME'));
```

## execPath

The absolute file path to the executable file of the current process on the host operating system.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.execPath);
```

## pid

The process ID of the current process.
The value type is number and represents the process ID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.pid);
```

## ppid

The process ID of the parent process.
The value type is number and represents the parent process ID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.ppid);
```

## platform

A string that identifies the operating system platform of the host machine. Common values include `windows`, `linux`, and `darwin` (macOS).

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.platform);
```

## arch

A string that identifies the operating system architecture of the host machine.
Common values include `amd64`, `aarch64`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.arch);
```

## version

A string that identifies the JSH runtime version.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.version);
```

## versions

An object that provides detailed runtime version information.

- `versions.jsh`: JSH runtime version string
- `versions.go`: Go runtime version string

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
console.println('jsh:', process.versions.jsh);
console.println('go :', process.versions.go);
```

## title

A string that identifies the current program.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.title);
```


## stdin, stdout, stderr

Streams for stdin, stdout, and stderr.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
process.stdout.write('Enter text: ');
const text = process.stdin.readLine();
console.println('Your input:', text);

// Output:
// Enter text: hello?
// Your input: hello?
```

## addShutdownHook()

Add a callback function that will be called at the termination of the current process.

<h6>Syntax</h6>

```js
addShutdownHook(()=>{})
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
process.addShutdownHook(()=>{
    console.println("shutdown hook called.");
})
console.println("running...")

// Output:
// running...
// shutdown hook called.
```

## exit()

Exit the current process. If the *code* is omitted, default is `0`.

<h6>Syntax</h6>

```js
exit([code])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
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

```js {linenos=table,linenostart=1,hl_lines=[2]}
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

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```

## exec()

Executes a JavaScript command file and returns its exit code.

<h6>Syntax</h6>

```js
exec(command, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const path = process.which('echo');
const code = process.exec(path, 'hello from exec');
console.println('exit code:', code);
```

## execString()

Executes JavaScript source code from a string and returns its exit code.

<h6>Syntax</h6>

```js
execString(source, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
const code = process.execString("console.println('hello from execString')");
console.println('exit code:', code);
```

## dispatchEvent()

Dispatches an event to an event emitter object on the JSH event loop.

This function returns `true` if the event is scheduled, `false` if the event loop is already terminated.

<h6>Syntax</h6>

```js
dispatchEvent(target, eventName, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[4]}
const process = require('process');
process.on('hello', (msg) => console.println(msg));
const ok = process.dispatchEvent(process, 'hello', 'from dispatchEvent');
console.println('scheduled:', ok);
```

## now()

Returns the current time as a JavaScript date-time object.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
const now = process.now();
console.println(typeof now); // object
```

## chdir()

Changes the current working directory.

If `path` is empty, JSH resolves it to `$HOME`.

<h6>Syntax</h6>

```js
chdir(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const process = require('process');
console.println('before:', process.cwd());
process.chdir('/lib');
console.println('after :', process.cwd());
```

## cwd()

Returns the current working directory path.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.cwd());
```

## nextTick()

Schedules a callback to run on the next event loop turn.

If the first argument is not a function, this call does nothing and returns `undefined`.

<h6>Syntax</h6>

```js
nextTick(callback, ...args)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
console.println('main');
process.nextTick((a, b) => console.println('tick:', a, b), 'first', 'second');
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

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const mem = process.memoryUsage();
console.println(typeof mem.rss, typeof mem.heapUsed);
```

## cpuUsage()

Returns CPU usage information.

Current implementation returns placeholder numeric values (`0`) for both fields.

<h6>Returned fields</h6>

- `user`
- `system`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const cpu = process.cpuUsage();
console.println(typeof cpu.user, typeof cpu.system);
```

## uptime()

Returns process uptime in seconds as a number.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
const up = process.uptime();
console.println('uptime >= 0:', up >= 0);
```

## hrtime()

Returns a high-resolution time tuple as `[seconds, nanoseconds]`.

If a previous tuple is provided, it returns the elapsed time from that point.

<h6>Syntax</h6>

```js
hrtime([previous])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const process = require('process');
const start = process.hrtime();
const diff = process.hrtime([start[0], start[1]]);
console.println(Array.isArray(diff), diff.length);
```

## kill()

Sends a signal request to the given process id.

Current implementation is a placeholder:

- returns an `Error` object when `pid` is missing
- returns `true` when `pid` is provided (signal defaults to `SIGTERM`)

<h6>Syntax</h6>

```js
kill(pid[, signal])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const process = require('process');
console.println(process.kill(12345, 'SIGKILL'));
```

## dumpStack()

Prints the current JavaScript call stack up to the specified depth for debugging.

<h6>Syntax</h6>

```js
dumpStack(depth)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const process = require('process');
function trace() {
    process.dumpStack(5);
}
trace();
```

