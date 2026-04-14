---
title: "util"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `util` module group provides small helper APIs that are commonly used by JSH applications and built-in commands.

The current module group includes:

- `util/parseArgs` for command-line style argument parsing
- `util/splitFields` for shell-like field splitting with quote handling

Load each helper through its direct module path.

```js
const parseArgs = require('util/parseArgs');
const splitFields = require('util/splitFields');
```

Use `parseArgs` when you need structured option parsing, named positionals, sub-command routing, or help text generation.
Use `splitFields` when you need to split a command-like string by whitespace while preserving quoted substrings.

{{< children_toc />}}