---
title: "@jsh/system"
type: docs
weight: 5
---

{{< neo_since ver="8.0.52" />}}

## now()

Get the process id of the current process.

<h4>Syntax</h4>

```js
now()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

Current time in native object.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
const m = require("@jsh/system")
console.log("now =", m.now())
```

## sleep()

Get the process id of the current process.

<h4>Syntax</h4>

```js
sleep(seconds)
```

<h6>Parameters</h6>

`seconds` *Number* sleep time in seconds

<h6>Return value</h6>

None.

<h4>Usage example</h4>

```js {linenos=table,linenostart=1}
const m = require("@jsh/system")
m.sleep(10)
```
