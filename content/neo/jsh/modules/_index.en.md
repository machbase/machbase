---
title: Modules
type: docs
weight: 900
toc: true
---

{{< neo_since ver="8.0.75" />}}

JSH modules are built-in standard library modules for Machbase Neo.
They are available in both TQL `SCRIPT()` blocks and standalone `*.js` applications,
and you can load them with `require()` without installing additional packages.

Some modules use short names such as `fs`, `os`, and `net`, while others are grouped
under names such as `archive/tar`.

## Loading Modules

Use `require()` with the module name you want to load.

```js
const fs = require('fs');
const os = require('os');

console.println('cwd entries:', fs.readDir('.').length);
console.println('platform:', os.platform(), os.arch());
```

JSH modules are part of the runtime, so they can be used immediately as the standard library
for file handling, networking, system information, data formatting, and database access.

Refer to the documents below for the API and examples for each module.


{{< children_toc />}}
