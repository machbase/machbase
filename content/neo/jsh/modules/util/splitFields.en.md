---
title: "splitFields"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `util/splitFields` module splits a string into fields using whitespace separators while preserving quoted substrings.
Load it with `require('util/splitFields')`.

## splitFields()

Splits a string by space, tab, newline, and carriage return characters.
Text wrapped in single or double quotes is kept as a single field.

<h6>Syntax</h6>

```js
splitFields(str[, options])
```

<h6>Parameters</h6>

- `str` `String`: Input text to split.
- `options` `Object`: Optional configuration object. The current implementation accepts the parameter but does not use it.

<h6>Return value</h6>

`String[]`

## Usage example

```js {linenos=table,linenostart=1}
const splitFields = require('util/splitFields');

console.println(JSON.stringify(splitFields('cmd "arg 1" "arg 2"')));
console.println(JSON.stringify(splitFields("hello 'world foo' bar")));
console.println(JSON.stringify(splitFields('foo\tbar\nbaz')));
```

## Behavior

- Consecutive whitespace is treated as a single separator.
- Empty fields are omitted from the result.
- Quote characters are removed from the returned values.
- Unclosed quotes keep consuming characters until the end of the string.
- Tabs and newlines inside quoted text are preserved.

## Examples

Basic whitespace splitting:

```js
splitFields('  foo   bar baz  ');
// ['foo', 'bar', 'baz']
```

Double quotes:

```js
splitFields('hello "world foo" bar');
// ['hello', 'world foo', 'bar']
```

Single quotes:

```js
splitFields("hello 'world foo' bar");
// ['hello', 'world foo', 'bar']
```

Mixed quoting:

```js
splitFields("a \"b c\" d 'e f' g");
// ['a', 'b c', 'd', 'e f', 'g']
```

## Notes

- The input must be a string, otherwise `TypeError` is thrown.
- Escape sequences inside quotes are not interpreted specially.
- This function is useful for shell-like tokenization when full command parsing is unnecessary.