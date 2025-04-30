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

## readLine()

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
```

## print()

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
```

## exec()

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
```

## daemonize()

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
```

## sleep()

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
```

## kill()

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
```

## ps()

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
```

## addCleanup()

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
```

## removeCleanup()

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
```
