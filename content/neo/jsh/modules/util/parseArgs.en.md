---
title: "parseArgs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `util/parseArgs` module parses command-line style argument arrays.
It is exposed both as `require('util/parseArgs')` and as `require('util').parseArgs`.

## parseArgs()

Parses an argument array using one or more configuration objects.

<h6>Syntax</h6>

```js
parseArgs(args, ...configs)
```

<h6>Parameters</h6>

- `args` `String[]`: Argument array to parse.
- `...configs` `Object`: One or more parser configurations.

When multiple configs are passed and some of them include `command`, the parser tries to match `args[0]` to the command name and uses the matching configuration.

<h6>Configuration fields</h6>

| Field | Type | Default | Description |
|:------|:-----|:--------|:------------|
| `command` | String |        | Sub-command name matched against `args[0]`. |
| `options` | Object | `{}` | Option definitions. |
| `strict` | Boolean | `true` | Throws on unknown options and unexpected positionals. |
| `allowNegative` | Boolean | `false` | Enables `--no-` form for boolean long options. |
| `tokens` | Boolean | `false` | Includes token details in the result. |
| `allowPositionals` | Boolean | derived from `positionals` | Allows positional arguments. |
| `positionals` | Array |        | Positional definition list. |
| `usage` | String |        | Used by `formatHelp()`. |
| `description` | String |        | Used by `formatHelp()`. |
| `longDescription` | String |        | Used by `formatHelp()` in multi-command help. |

## Option definitions

Each entry in `config.options` is keyed by the JavaScript property name.
The parser automatically converts camelCase names to kebab-case flags.

For example, `maxRetryCount` maps to `--max-retry-count`.

| Field | Type | Description |
|:------|:-----|:------------|
| `type` | String | One of `boolean`, `string`, `integer`, `float`. |
| `short` | String | One-letter short flag such as `v` for `-v`. |
| `multiple` | Boolean | Collects repeated values into an array. |
| `default` | any | Default value applied before parsing. |
| `description` | String | Help text used by `formatHelp()`. |

Supported forms include:

- Long options such as `--output file.txt`
- Inline long values such as `--output=file.txt`
- Short options such as `-o file.txt`
- Inline short values such as `-o=file.txt`
- Short boolean groups such as `-abc`
- Option terminator `--`

## Positional definitions

`positionals` can contain simple strings or detailed objects.

Simple form:

```js
positionals: ['inputFile', 'outputFile']
```

Detailed form:

```js
positionals: [
    { name: 'input-file' },
    { name: 'output-file', optional: true, default: 'stdout' },
    { name: 'files', variadic: true }
]
```

Rules:

- Variadic positionals must be the last positional.
- Missing required positionals raise `TypeError`.
- Named positional keys are converted from kebab-case to camelCase in `result.namedPositionals`.

## Return value

`parseArgs()` returns an object with these fields.

| Field | Type | Description |
|:------|:-----|:------------|
| `values` | Object | Parsed option values. |
| `positionals` | String[] | Positional values in order. |
| `namedPositionals` | Object | Present when `positionals` are configured. |
| `tokens` | Object[] | Present when `tokens: true`. |
| `command` | String | Present when a sub-command config matched. |

## Usage example

```js {linenos=table,linenostart=1}
const { parseArgs } = require('util');

const result = parseArgs(['-v', '--output', 'file.txt', 'input.sql'], {
    options: {
        verbose: { type: 'boolean', short: 'v' },
        output: { type: 'string' }
    },
    allowPositionals: true,
    positionals: ['input-file']
});

console.println(JSON.stringify(result.values));
console.println(JSON.stringify(result.namedPositionals));
```

## Number parsing

Use `integer` for whole-number arguments and `float` for decimal numbers.

- `integer` rejects values that contain a decimal point.
- Both `integer` and `float` return JavaScript numbers.

```js {linenos=table,linenostart=1}
const { parseArgs } = require('util');

const result = parseArgs(['--port', '8080', '--ratio', '0.75'], {
    options: {
        port: { type: 'integer' },
        ratio: { type: 'float' }
    }
});
```

## Negative booleans

With `allowNegative: true`, boolean long options accept `--no-...`.

```js {linenos=table,linenostart=1}
const { parseArgs } = require('util');

const result = parseArgs(['--no-color', '--verbose'], {
    options: {
        color: { type: 'boolean' },
        verbose: { type: 'boolean' }
    },
    allowNegative: true
});
```

## Sub-command parsing

When multiple configs are supplied, the first argument can select a command-specific config.

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const commitConfig = {
    command: 'commit',
    options: {
        message: { type: 'string', short: 'm' },
        all: { type: 'boolean', short: 'a' }
    }
};

const pushConfig = {
    command: 'push',
    options: {
        force: { type: 'boolean', short: 'f' }
    },
    allowPositionals: true,
    positionals: ['remote', { name: 'branch', optional: true }]
};

const result = parseArgs(['push', '-f', 'origin', 'main'], commitConfig, pushConfig);
console.println(result.command);
console.println(JSON.stringify(result.namedPositionals));
```

## parseArgs.formatHelp()

Generates human-readable help text from the same config structure used by `parseArgs()`.

<h6>Syntax</h6>

```js
parseArgs.formatHelp(...configs)
```

It supports both:

- single-command help output
- multi-command help output with command summaries and per-command sections

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const help = parseArgs.formatHelp({
    usage: 'Usage: myapp [options] <file>',
    options: {
        userName: { type: 'string', short: 'u', description: 'User name', default: 'guest' },
        enableDebug: { type: 'boolean', short: 'd', description: 'Enable debug mode', default: false }
    },
    positionals: [
        { name: 'file', description: 'Input file to process' }
    ]
});

console.println(help);
```

## parseArgs.toKebabCase()

Converts a JavaScript camelCase option name to its CLI kebab-case form.

<h6>Syntax</h6>

```js
parseArgs.toKebabCase(name)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

console.println(parseArgs.toKebabCase('maxRetryCount'));
```

## Behavior notes

- The first argument must be an array, otherwise `TypeError` is thrown.
- In `strict` mode, unknown options and unexpected positionals raise `TypeError`.
- `multiple: true` collects repeated values into arrays.
- Defaults are applied before parsing explicit option values.
- The parser accepts both `require('util').parseArgs` and `require('util/parseArgs')` usage.