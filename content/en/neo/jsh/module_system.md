---
title: "@jsh/system"
type: docs
weight: 5
---

{{< neo_since ver="8.0.52" />}}

## now()

Get the process id of the current process.

<h6>Syntax</h6>

```js
now()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

Current time in native object.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const m = require("@jsh/system")
console.log("now =", m.now())
```


## parseTime()

<h6>Syntax</h6>

```js
parseTime(epoch, epoch_format)
parseTime(datetime, format)
parseTime(datetime, format, location)
```

<h6>Parameters</h6>

- `epoch` `Number`
- `epoch_format` `String` "s", "ms", "us", "ns"
- `datetime` `String`
- `format` `String`
- `location` `Location` timezone, default is 'Local' if omitted., e.g. system.location('EST'), system.location('America/New_York')

<h6>Return value</h6>

Time in native object

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const system = require("@jsh/system");
ts = system.parseTime(
    "2023-10-01 12:00:00",
    "2006-01-02 15:04:05",
    system.location("UTC"));
println(ts.In(system.location("UTC")).Format("2006-01-02 15:04:05"));

// 2023-10-01 12:00:00
```


## location()

<h6>Syntax</h6>

```js
location(timezone)
```

<h6>Parameters</h6>

- `timezone` `String` time zone, e.g. `"UTC"`, `"Local"`, `"GMT"`, `"ETS"`, `"America/New_York"`...

<h6>Return value</h6>

Location in native object

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const system = require("@jsh/system");
ts = system.time(1).In(system.location("UTC"));
println(ts.Format("2006-01-02 15:04:05"));

// 1970-01-01 00:00:01
```
