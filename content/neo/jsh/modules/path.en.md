---
title: "path"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `path` module provides path manipulation helpers similar to Node.js.
In JSH, the default export is the POSIX implementation, and the module also exposes `path.posix` and `path.win32` namespaces.

Typical usage looks like this.

```js
const path = require('path');
```

## Default export

`require('path')` returns the POSIX path implementation.

That means:

- path separator is `/`
- list delimiter is `:`
- functions such as `join()` and `resolve()` behave like POSIX path utilities

You can also access:

- `path.posix`
- `path.win32`

## Common properties

| Property | POSIX | win32 |
|:---------|:------|:------|
| `sep` | `/` | `\\` |
| `delimiter` | `:` | `;` |

## resolve()

Resolves a sequence of paths into an absolute path.

<h6>Syntax</h6>

```js
path.resolve(...segments)
```

The default implementation uses the current working directory when it needs a base path.

## normalize()

Normalizes path separators and resolves `.` and `..` segments.

<h6>Syntax</h6>

```js
path.normalize(value)
```

## isAbsolute()

Returns whether a path is absolute.

<h6>Syntax</h6>

```js
path.isAbsolute(value)
```

## join()

Joins path segments using the active path style and normalizes the result.

<h6>Syntax</h6>

```js
path.join(...segments)
```

## relative()

Returns a relative path from one location to another.

<h6>Syntax</h6>

```js
path.relative(from, to)
```

## dirname()

Returns the directory part of a path.

<h6>Syntax</h6>

```js
path.dirname(value)
```

## basename()

Returns the last path component.
If `ext` is provided, the matching suffix is removed.

<h6>Syntax</h6>

```js
path.basename(value)
path.basename(value, ext)
```

## extname()

Returns the file extension including the leading dot.

<h6>Syntax</h6>

```js
path.extname(value)
```

## parse()

Splits a path into structured fields.

<h6>Syntax</h6>

```js
path.parse(value)
```

<h6>Return value</h6>

`parse()` returns an object with:

- `root`
- `dir`
- `base`
- `ext`
- `name`

## format()

Builds a path string from a parsed path object.

<h6>Syntax</h6>

```js
path.format(pathObject)
```

`pathObject` may contain `dir`, `root`, `base`, `name`, and `ext`.

## Usage example

```js {linenos=table,linenostart=1}
const path = require('path');

console.println(path.join('/work', 'demo', 'file.txt'));
console.println(path.dirname('/work/demo/file.txt'));
console.println(path.basename('/work/demo/file.txt', '.txt'));
console.println(path.extname('/work/demo/file.txt'));
```

## parse()/format() example

```js {linenos=table,linenostart=1}
const path = require('path');

const parsed = path.parse('/work/demo/file.txt');
console.println(JSON.stringify(parsed));

const rebuilt = path.format({
    dir: '/work/demo',
    name: 'file',
    ext: '.txt'
});
console.println(rebuilt);
```

## POSIX and win32 namespaces

Use `path.posix` or `path.win32` when you need explicit behavior regardless of the current default.

```js {linenos=table,linenostart=1}
const path = require('path');

console.println(path.posix.join('/a', 'b', 'c.txt'));
console.println(path.win32.join('C:\\temp', 'demo', 'file.txt'));
```

## Behavior notes

- The default JSH export is POSIX-oriented.
- All public functions require string arguments where applicable and throw `TypeError` for invalid input.
- `parse()` and `format()` use a Node.js-like object shape.
- `path.win32` is available for Windows path handling even when JSH is running on a non-Windows system.