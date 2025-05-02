---
title: "@jsh/process"
type: docs
weight: 1
---

{{< neo_since ver="8.0.52" />}}

The `@jsh/process` module is specifically designed for use in JSH applications 
and is not available in the `SCRIPT()` function within TQL, unlike other JSH modules.

## pid()

Get the process id of the current process.

<h4>Syntax</h4>

```js
pid()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

A number value that represents the process ID.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
const m = require("@jsh/process")
console.log("my pid =", m.pid())
```

## ppid()

Get the process id of the parent process.

<h4>Syntax</h4>

```js
ppid()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

A number value that represents the parent process ID.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
const m = require("@jsh/process")
console.log("parent pid =", m.ppid())
```

## args()

Get command line arguments

<h4>Syntax</h4>

```js
args()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

`String[]`

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
args = p.args();
x = parseInt(args[1]);
console.log("x =", x);
```

## cwd()

Get the current working directory

<h4>Syntax</h4>

```js
cwd()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
console.log("cwd :", p.cwd());
```

## cd()

Change the current working directory.

<h4>Syntax</h4>

```js
cd(path)
```

<h6>Parameters</h6>

`path` : directory path to move

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
p.cd('/dir/path');
console.log("cwd :", p.cwd());
```

## readDir()

Read files and sub-directories of the given directory.

<h4>Syntax</h4>

```js
readDir(path, callback)
```

<h6>Parameters</h6>

- `path`: `String` path to the directory
- `callback`: function ([DirEntry](#DirEntry)) [undefined|Boolean] callback function. if it returns false, the iteration will stop.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}

```

## DirEntry

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| name               | String     |                    |
| isDir              | Boolean    |                    |
| readOnly           | Boolean    |                    |
| type               | String     |                    |
| size               | Number     |                    |
| virtual            | Boolean    |                    |

<!-- ## readLine()

...

<h4>Syntax</h4>

```js
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
``` -->

## print()

Write arguments into the output, the default output is the log file or stdout if log filename is not set.

<h4>Syntax</h4>

```js
print(...args)
```

<h6>Parameters</h6>

`args` `...any` Variable length of argument to write.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.print("Hello", "World!", "\n")
```

## println()

Write arguments into the output, the default output is the log file or stdout if log filename is not set.

<h4>Syntax</h4>

```js
print(...args)
```

<h6>Parameters</h6>

`args` `...any` Variable length of argument to write.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.println("Hello", "World!")
```

## exec()

Run another JavaScript application.

<h4>Syntax</h4>

```js
exec(cmd, ...args)
```

<h6>Parameters</h6>

`cmd` `String` .js file path to run
`args` `...String` arguments to pass to the cmd.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.exec("/sbin/hello.js")
```

## daemonize()

Run the current script file as a daemon process with its parent process ID set to `1`.

<h4>Syntax</h4>

```js
daemonize()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.daemonize()
if( p.ppid() == 1) {
    doBackgroundJob()
} else {
    p.print("daemonize self, then exit")
}
```

## sleep()

Pause the current control flow.
This function is provided in the process module for convenience and has an equivalent in the `@jsh/system` module.

<h4>Syntax</h4>

```js
sleep(duration)
```

<h6>Parameters</h6>

`duration` `Number` sleep duration in milliseconds.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.sleep(1000) // 1 sec.
```

## kill()

Terminate a process using the specified process ID (pid).

<h4>Syntax</h4>

```js
kill(pid)
```

<h6>Parameters</h6>

`pid` `Number` pid of target process.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.kill(123)
```

## ps()

List all currently running processes.

<h4>Syntax</h4>

```js
ps()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

[`Process[]`](#Process): Array of Process objects.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
list = p.ps()
for( const x of list ) {
    console.log(
        p.pid, 
        (p.ppid == 0xFFFFFFFF ? "-" : p.ppid), 
        p.user, 
        p.name, 
        p.uptime)
}
```

## Process

Process information that returned by `ps()`.

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| pid                | Number     | process ID         |
| ppid               | Number     | process ID of the parent |
| user               | String     | username (e.g: `sys`)    |
| name               | String     | Script file name         |
| uptime             | String     | Elapse duration since started  |


## addCleanup()
Add a function to execute when the current JavaScript VM terminates.

<h4>Syntax</h4>

```js
addCleanup(fn)
```

<h6>Parameters</h6>

`fn` `()=>{}` callback function

<h6>Return value</h6>

`Number` A token for remove the cleanup callback.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1,hl_lines=[2]}
p = require("@jsh/process")
p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}

// run - 0
// run - 1
// run - 2
// terminated
```

## removeCleanup()

Remove a previously registered cleanup callback using the provided token.

<h4>Syntax</h4>

```js
removeCleanup(token)
```

<h6>Parameters</h6>

`token` `Number` token that returned by `addCleanup()`.

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1,hl_lines=[2,6]}
p = require("@jsh/process")
token = p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}
p.removeCleanup(token)

// run - 0
// run - 1
// run - 2
```
