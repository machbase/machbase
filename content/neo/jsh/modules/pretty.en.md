---
title: "pretty"
type: docs
weight: 100
---

The `pretty` module formats values and renders terminal-friendly output for JSH applications.
It is useful when you need readable tables, human-friendly byte and duration strings, or
progress indicators for long-running jobs.

Use the API that matches your task:

- Use `Table()` when you want box, CSV, TSV, JSON, NDJSON, HTML, or Markdown table output.
- Use `Bytes()`, `Ints()`, and `Durations()` when you want compact human-readable values.
- Use `Progress()` when you want a terminal progress indicator for long-running work.

## Installation

```js
const pretty = require('pretty');
```

## Table()

Creates a table writer.

<h6>Syntax</h6>

```js
Table(config)
```

<h6>Common options</h6>

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `format` | `String` | Output format such as `box`, `csv`, `tsv`, `json`, `ndjson`, `html`, `md` | `box` |
| `boxStyle` | `String` | Box style such as `light`, `double`, `bold`, `rounded`, `simple`, `compact` | `light` |
| `rownum` | `Boolean` | Include a leading `ROWNUM` column | `true` |
| `timeformat` | `String` | Datetime format | `default` |
| `tz` | `String` | Timezone such as `local`, `UTC`, or an IANA timezone name | `local` |
| `precision` | `Number` | Round floating-point values when `0` or greater | `-1` |
| `header` | `Boolean` | Show header row | `true` |
| `footer` | `Boolean` | Show footer or caption | `true` |
| `pause` | `Boolean` | Pause in terminal paging mode | `true` |
| `nullValue` | `String` | String used for null values | `NULL` |
| `stringEscape` | `Boolean` | Escape non-printable characters as `\uXXXX` | `false` |

<h6>Important methods</h6>

- `appendHeader(values)` append the header row
- `appendRow(row)` append one row
- `appendRows(rows)` append multiple rows
- `append(values)` append a row or rows
- `row(...values)` create a row with table value transformation
- `render()` return the current rendered output as a string
- `close()` flush the remaining rows and return the last rendered output
- `resetRows()` clear buffered rows
- `pauseAndWait()` wait for a terminal key press in paging mode

<h6>Usage example: basic box table</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3,4,5]}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light' });
tw.appendHeader(['Name', 'Age']);
tw.appendRow(tw.row('Alice', 30));
tw.appendRow(tw.row('Bob', 25));
console.println(tw.render());
```

Output:

```text
┌────────┬───────┬─────┐
│ ROWNUM │ NAME  │ AGE │
├────────┼───────┼─────┤
│      1 │ Alice │  30 │
│      2 │ Bob   │  25 │
└────────┴───────┴─────┘
```

<h6>Usage example: floating-point precision</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,4,5]}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light', precision: 2 });
tw.appendHeader(['Item', 'Price']);
tw.appendRow(tw.row('Apple', 1.234));
tw.appendRow(tw.row('Orange', 2.567));
console.println(tw.render());
```

Output:

```text
┌────────┬────────┬───────┐
│ ROWNUM │ ITEM   │ PRICE │
├────────┼────────┼───────┤
│      1 │ Apple  │  1.23 │
│      2 │ Orange │  2.57 │
└────────┴────────┴───────┘
```

<h6>Usage example: time formatting</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,4,5]}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light', timeformat: 'DATETIME', tz: 'UTC' });
tw.appendHeader(['Event', 'Time']);
tw.append(['Start', new Date('2024-03-15T14:30:45.000Z')]);
tw.append(['End', new Date('2024-03-15T18:20:30.000Z')]);
console.println(tw.render());
```

Output:

```text
┌────────┬───────┬─────────────────────┐
│ ROWNUM │ EVENT │ TIME                │
├────────┼───────┼─────────────────────┤
│      1 │ Start │ 2024-03-15 14:30:45 │
│      2 │ End   │ 2024-03-15 18:20:30 │
└────────┴───────┴─────────────────────┘
```

The built-in `timeformat` keywords include `DATETIME`, `DATE`, `TIME`, `RFC3339`, `RFC1123`,
`ANSIC`, `KITCHEN`, `STAMP`, `STAMPMILLI`, `STAMPMICRO`, and `STAMPNANO`.
You can also pass a custom Go-style time layout string.

<h6>Usage example: box styles</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,4]}
const pretty = require('pretty');
for (const style of ['light', 'double', 'bold', 'rounded', 'compact']) {
	const tw = pretty.Table({ boxStyle: style, rownum: false });
	tw.appendHeader(['Col']);
	tw.appendRow(tw.row('Val'));
	console.println(style + ':');
	console.println(tw.render());
}
```

Selected outputs:

```text
light:
┌─────┐
│ COL │
├─────┤
│ Val │
└─────┘

double:
╔═════╗
║ COL ║
╠═════╣
║ Val ║
╚═════╝

compact:
 COL 
─────
 Val 
```

<h6>Usage example: JSON output</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,5]}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'json', rownum: false });
tw.appendHeader(['ID', 'Status', 'Value']);
tw.append([1, 'active', 42.5]);
tw.append([2, 'pending', 31.2]);
console.println(tw.render());
```

Output:

```json
{"columns":["ID","Status","Value"],"rows":[[1,"active",42.5],[2,"pending",31.2]]}
```

<h6>Usage example: CSV output</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,5]}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'csv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

Output:

```text
Name,Score
Alice,98
Bob,87
```

<h6>Usage example: TSV output</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,5]}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'tsv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

Output:

```text
Name	Score
Alice	98
Bob	87
```

<h6>Usage example: NDJSON output</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,5]}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'ndjson', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

Output:

```json
{"Name":"Alice","Score":98}
{"Name":"Bob","Score":87}
```

<h6>Usage example: Markdown output</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,5]}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'md', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

Output:

```md
| Name  | Score |
| ----- | ----: |
| Alice |    98 |
| Bob   |    87 |
```

<h6>Usage example: non-printable string escaping</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,4]}
const pretty = require('pretty');
const tw = pretty.Table({ stringEscape: true, rownum: false });
tw.appendHeader(['Value']);
tw.appendRow(tw.row('hello\u0007world'));
console.println(tw.render());
```

When `stringEscape` is `true`, non-printable characters are rendered as escaped Unicode sequences.

## MakeRow()

Creates an empty row array with the requested size.

<h6>Syntax</h6>

```js
MakeRow(size)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const pretty = require('pretty');
const row = pretty.MakeRow(3);
console.println(row.length);
console.println(Array.isArray(row));
```

## Progress()

Creates a progress writer for terminal output.

<h6>Syntax</h6>

```js
Progress(options)
```

<h6>Options</h6>

- `showPercentage` `Boolean` show percentage, default `true`
- `showETA` `Boolean` show estimated remaining time, default `true`
- `showSpeed` `Boolean` show processing speed, default `true`
- `updateFrequency` `Number` refresh interval in milliseconds, default `250`
- `trackerLength` `Number` progress bar width, default `20`

The returned writer provides `tracker(options)`.
A tracker accepts `message` and `total`, and supports `increment(n)`, `value()`,
`markAsDone()`, and `isDone()`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3,7,8]}
const pretty = require('pretty');
const pw = pretty.Progress({ showPercentage: true, showETA: true });
const tracker = pw.tracker({ message: 'Processing', total: 100 });

let interval = setInterval(function() {
	tracker.increment(10);
	if (tracker.value() >= 100) {
		tracker.markAsDone();
		clearInterval(interval);
	}
}, 200);
```

This feature is intended for interactive terminal sessions. In tests and non-interactive runs,
the important observable state is whether the tracker reaches `isDone()`.

## Bytes()

Formats byte counts as human-readable strings.

<h6>Syntax</h6>

```js
Bytes(value)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Bytes(512));
console.println(pretty.Bytes(1536));
console.println(pretty.Bytes(1048576));
console.println(pretty.Bytes(1073741824));
```

Output:

```text
512B
1.5KB
1.0MB
1.0GB
```

## Ints()

Formats integers with grouping separators.

<h6>Syntax</h6>

```js
Ints(value)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Ints(1234567890));
console.println(pretty.Ints(0));
console.println(pretty.Ints(-999));
```

Output:

```text
1,234,567,890
0
-999
```

## Durations()

Formats durations from nanoseconds into short readable strings.

<h6>Syntax</h6>

```js
Durations(nanoseconds)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Durations(1234));
console.println(pretty.Durations(2340000));
console.println(pretty.Durations(3010000000));
console.println(pretty.Durations(3661000000000));
console.println(pretty.Durations(86400000000000));
```

Output:

```text
1.23μs
2.34ms
3.01s
1h 1m
1d 0h
```

Values under 60 seconds use decimal units such as `μs`, `ms`, and `s`.
Longer durations are shortened to the two highest units, for example `2m 5s`, `1h 1m`, or `2d 0h`.

## Align

Provides alignment constants for advanced column configuration.

Available constants are `default`, `left`, `center`, `justify`, `right`, and `auto`.

## Terminal helpers

The module also exports these helpers:

- `isTerminal()` returns whether stdin is attached to a terminal
- `getTerminalSize()` returns terminal width and height
- `pauseTerminal()` waits for a key press and returns `false` on `q` or `Q`
- `parseTime(value, format, tz)` parses text into a time value

These helpers are mainly useful when you are building interactive terminal tools around `Table()`
or `Progress()`.
