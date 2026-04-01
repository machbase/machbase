---
title: "parser"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `parser` module provides streaming decoders for CSV and NDJSON data.
It is designed for use with JSH streams and emits parsed objects through events.

Typical usage looks like this.

```js
const parser = require('parser');
```

## Exported members

- `csv(options)`
- `ndjson(options)`
- `CSVParser`
- `NDJSONParser`

## csv()

Creates a CSV parser stream.

<h6>Syntax</h6>

```js
parser.csv([options])
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `separator` | String | `,` | Field separator |
| `quote` | String | `"` | Quote character |
| `escape` | String | same as `quote` | Escape character used for escaped quotes |
| `headers` | `true` / `false` / `String[]` | `true` | Header handling mode |
| `skipLines` | Number | `0` | Number of initial lines to ignore |
| `skipComments` | Boolean \| String | `false` | Skip comment lines; when a string is given it becomes the comment prefix |
| `strict` | Boolean | `false` | Fail when a row has a different column count |
| `mapHeaders` | Function | | Maps header names |
| `mapValues` | Function | | Maps field values before row emission |
| `trimLeadingSpace` | Boolean | `true` | Trim leading spaces from each field |

<h6>Return value</h6>

Returns a `CSVParser` instance.

## CSVParser

CSV parser class exported by the module.

<h6>Creation</h6>

```js
new parser.CSVParser([options])
```

The constructor accepts the same options as `parser.csv()`.

<h6>Events</h6>

- `headers`: emitted once after the header row is parsed
- `data`: emitted for each parsed row object
- `error`: emitted when strict parsing fails
- `end`: emitted when the upstream stream finishes

<h6>Properties</h6>

- `bytesWritten`: number of input bytes received
- `bytesRead`: number of bytes consumed by the parser

<h6>Row shape</h6>

- When `headers` is omitted or `true`, the first non-skipped line becomes the header row.
- When `headers` is `false`, fields are exposed as `"0"`, `"1"`, `"2"`, ...
- When `headers` is an array, those names are used and the first line is treated as data.
- In non-strict mode, extra columns are emitted as `_N` fields such as `_3`.

## ndjson()

Creates an NDJSON parser stream.

<h6>Syntax</h6>

```js
parser.ndjson([options])
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `strict` | Boolean | `true` | Fail on invalid JSON lines instead of skipping them |

<h6>Return value</h6>

Returns an `NDJSONParser` instance.

## NDJSONParser

NDJSON parser class exported by the module.

<h6>Creation</h6>

```js
new parser.NDJSONParser([options])
```

The constructor accepts the same options as `parser.ndjson()`.

<h6>Events</h6>

- `data`: emitted for each parsed JSON object
- `warning`: emitted for invalid lines when `strict: false`
- `error`: emitted when strict parsing fails
- `end`: emitted when the upstream stream finishes

`warning` event objects contain:

| Property | Type | Description |
|:---------|:-----|:------------|
| `line` | Number | Line number of the skipped record |
| `data` | String | Original trimmed line text |
| `error` | String | Parse error message |

<h6>Properties</h6>

- `bytesWritten`: number of input bytes received
- `bytesRead`: number of bytes consumed by the parser

## CSV example

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.csv')
    .pipe(parser.csv({
        headers: true,
        mapValues: ({ header, value }) => header === 'age' ? parseInt(value, 10) : value,
    }))
    .on('headers', (headers) => {
        console.println(headers.join(','));
    })
    .on('data', (row) => {
        console.println(row.name, row.age);
    });
```

## NDJSON example

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.ndjson')
    .pipe(parser.ndjson({ strict: false }))
    .on('data', (obj) => {
        console.println(obj.id);
    })
    .on('warning', (warn) => {
        console.println('Skipped line:', warn.line);
    });
```

## Progress example

Both parser streams expose `bytesWritten` and `bytesRead`, so progress can be tracked while streaming.

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

const decoder = parser.csv();

fs.createReadStream('/work/sample.csv', { highWaterMark: 8 })
    .pipe(decoder)
    .on('data', () => {
        console.println(decoder.bytesWritten, decoder.bytesRead);
    });
```

## Behavior notes

- Both parser classes extend the JSH `stream.Transform` implementation.
- Parsed rows and objects are emitted through `data` events.
- Empty lines are ignored by both parsers.
- `NDJSONParser` trims each line before parsing.
- `CSVParser` removes a trailing `\r` so `\r\n` input is handled correctly.