---
title: "readline"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `readline` module provides interactive line input for JSH applications.
It exposes a single `ReadLine` class backed by the native JSH readline implementation.

Typical usage looks like this.

```js
const { ReadLine } = require('readline');
```

## ReadLine

Creates an interactive line reader.

<h6>Syntax</h6>

```js
new ReadLine([options])
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| history | String | `readline` | History file name stored under the JSH config directory. |
| prompt | Function | built-in prompt | Callback that returns the prompt string for each line. |
| submitOnEnterWhen | Function | always submit | Callback that decides whether Enter submits the current input. |
| autoInput | String[] |         | Input sequence used mainly for automated testing. |

If `prompt` is omitted, the first line uses `> ` and continuation lines use `. `-style indentation.
If `history` is omitted, the module uses `readline` as the history file name.
The `history` option is treated as a file name, not a path, and the actual history file is stored under `$HOME/.config/.jsh/`.
Use only a base file name for `history`; do not include directory separators.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'prompt> ' : '....... ',
});
```

## readLine()

Reads one logical input value.

- If the input is single-line, the result is a single string.
- If multi-line input is accepted, the result joins lines with `\n`.
- When the native reader ends with an error, JSH returns an `Error` object.

<h6>Syntax</h6>

```js
reader.readLine([options])
```

`readLine()` accepts the same option shape as the constructor.
Per-call options override constructor options.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: () => 'input> ',
});
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
console.println(line);
```

## addHistory()

Adds a line to readline history.

<h6>Syntax</h6>

```js
reader.addHistory(line)
```

If the same line already exists, the previous entry is removed and the new one is appended at the end.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine();
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
reader.addHistory(line);
```

## close()

Closes the current readline session.

<h6>Syntax</h6>

```js
reader.close()
```

If `close()` is called while `readLine()` is waiting for input, the pending call ends with `EOF`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine();
const timer = setTimeout(() => {
    reader.close();
}, 200);
const line = reader.readLine();
clearTimeout(timer);
```

## prompt option

`prompt` generates the prompt string for each line.

<h6>Signature</h6>

```js
prompt(lineno) => string
```

- `lineno` is zero-based.
- Return the exact prompt text to render for that line.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'sql> ' : '...> ',
});
```

## submitOnEnterWhen option

`submitOnEnterWhen` controls whether pressing Enter submits the current input or continues multi-line editing.

<h6>Signature</h6>

```js
submitOnEnterWhen(lines, idx) => boolean
```

- `lines` is the current line array.
- `idx` is the current line index.
- Return `true` to submit, or `false` to continue editing.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
```

## autoInput option

`autoInput` feeds predefined input into the reader.
This is mainly useful for tests and non-interactive scripts.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: [
        'Hello World',
        ReadLine.CtrlJ,
    ],
});
```

## Multi-line input example

`submitOnEnterWhen` is commonly used to keep editing until the current line satisfies an application rule.

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: ['select *', ReadLine.Enter, 'from dual;', ReadLine.Enter],
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
const text = reader.readLine();
console.println(text);
```

## Static key constants

`ReadLine` exposes many key constants for simulated input and key handling.
Representative constants include:

- Control keys: `CtrlA` ... `CtrlZ`, `CtrlLeft`, `CtrlRight`, `CtrlUp`, `CtrlDown`
- Navigation keys: `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `PageUp`, `PageDown`
- Editing keys: `Backspace`, `Delete`, `Enter`, `ShiftTab`, `Escape`
- Alt keys: `AltA` ... `AltZ`, `ALTBackspace`
- Function keys: `F1` ... `F24`

For complete names, refer to the exported static properties on `ReadLine`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

console.printf('%X\n', ReadLine.CtrlJ);
```

## Behavior notes

- The module uses callback-free synchronous reads at the JavaScript level. `readLine()` returns the completed value directly.
- The implementation supports interactive editing, cursor movement, history, and multi-line input through the native backend.
- `readLine()` can return an `Error` object, so callers should check `line instanceof Error` when they want to handle failures explicitly.
- `close()` is primarily useful for canceling a pending read from another timer or event.
