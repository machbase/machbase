---
title: "zip"
type: docs
weight: 100
---

The `archive/zip` module creates and extracts ZIP archives in JSH.
It provides in-memory helpers, stream-style APIs, and a file-based `Zip` class.

Use the API that matches your task:

- Use `zipSync()` and `unzipSync()` when the archive is already in memory.
- Use `Zip` when you want to read files, save `.zip` files, or extract them to disk.
- Use `createZip()` and `createUnzip()` when you want event-driven processing.

## Installation

```js
const zip = require('archive/zip');
```

## zipSync()

Creates a ZIP archive synchronously.

<h6>Syntax</h6>

```js
zipSync(data)
```

<h6>Parameters</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

If `data` is a single string or byte buffer, the created entry name defaults to `data`.
If `data` is an array, each item should be an entry object such as `{ name, data }`.

<h6>Return value</h6>

Returns an `ArrayBuffer` that contains ZIP archive bytes.

This form is useful for quick tests or for building an archive before writing it somewhere else.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,6]}
const zip = require('archive/zip');
const archive = zip.zipSync([
	{ name: 'alpha.txt', data: 'Alpha' },
	{ name: 'dir/beta.txt', data: 'Beta' }
]);
console.println(archive.constructor.name);
```

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const zip = require('archive/zip');
const archive = zip.zipSync('hello zip');
const entries = zip.unzipSync(archive);
console.println(entries[0].name, new Uint8Array(entries[0].data).length);
```

## unzipSync()

Extracts ZIP archive bytes synchronously and returns entry objects.

<h6>Syntax</h6>

```js
unzipSync(buffer)
```

<h6>Parameters</h6>

- `buffer` `ArrayBuffer | Uint8Array | Number[]`

<h6>Return value</h6>

Returns an array of entry objects.

Each entry can include `name`, `data`, `comment`, `method`, `compressedSize`, `size`, `isDir`,
and `modified`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[6,7,8]}
const zip = require('archive/zip');
const archive = zip.zipSync([
	{ name: 'one.txt', data: 'One' },
	{ name: 'two.txt', data: 'Two' }
]);
const entries = zip.unzipSync(archive);
console.println(entries[0].name, entries[0].size);
console.println(entries[1].name, entries[1].size);
console.println(entries.length);
```

## zip()

Provides a callback-style asynchronous wrapper for ZIP archive creation.

<h6>Syntax</h6>

```js
zip(data, callback)
```

The callback follows the `(err, archive)` form.

## unzip()

Provides a callback-style asynchronous wrapper for ZIP extraction.

<h6>Syntax</h6>

```js
unzip(buffer, callback)
```

The callback follows the `(err, entries)` form.

Use these wrappers when you want callback-based control flow without managing stream events directly.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4,5]}
const zip = require('archive/zip');

zip.zip('payload', function(err, archive) {
	if (err) throw err;
	zip.unzip(archive, function(err2, entries) {
		if (err2) throw err2;
		console.println(entries[0].name, new Uint8Array(entries[0].data).length);
	});
});
```

## createZip()

Creates a stream-style ZIP writer.

The returned object accepts entry objects through `write()` and emits archive bytes through the
`data` event when `end()` is called.

This API is event-driven, but it still finalizes work on `end()` rather than emitting extracted
files progressively like a Node.js file stream.

<h6>Syntax</h6>

```js
createZip()
```

## createUnzip()

Creates a stream-style ZIP reader.

Write archive bytes with `write()`, then call `end()` to emit one `entry` event per extracted item.

<h6>Syntax</h6>

```js
createUnzip()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[5,10,14,15]}
const zip = require('archive/zip');
const writer = zip.createZip();
let archive = null;

writer.on('data', function(chunk) {
	archive = chunk;
});

writer.on('end', function() {
	const reader = zip.createUnzip();
	reader.on('entry', function(entry) {
		const text = String.fromCharCode.apply(null, new Uint8Array(entry.data));
		console.println(entry.name + '=' + text);
	});
	reader.write(archive);
	reader.end();
});

writer.write({ name: 'one.txt', data: 'One' });
writer.write({ name: 'two.txt', data: 'Two' });
writer.end();
```

## Zip

`Zip` is a file-oriented helper class for building, saving, loading, and extracting ZIP archives.

<h6>Constructor</h6>

```js
new zip.Zip(filePath?)
```

If `filePath` is provided, the archive is loaded from that file.

### addFile()

Reads a file from the filesystem and appends it as an archive entry.

```js
addFile(filePath[, entryName])
```

### addBuffer()

Appends a string or byte buffer as an archive entry.

```js
addBuffer(data, entryName[, options])
```

### addEntry()

Appends an archive entry object directly.

```js
addEntry(entry)
```

Supported ZIP entry fields:

- `name` `String` required entry path
- `data` `String | ArrayBuffer | Uint8Array | Number[]` file content
- `comment` `String` entry comment
- `method` `Number` compression method

`addFile()` is the most direct option when the source data already exists on disk.
`addBuffer()` is useful when the content is generated in memory.
`addEntry()` is helpful when you also want to attach entry metadata such as `comment`.

### getEntries()

Returns a shallow copy of the current archive entries.

```js
getEntries()
```

### writeTo()

Writes the archive to a file.

```js
writeTo(filePath)
```

### extractAllTo()

Extracts entries to a directory.

```js
extractAllTo(outputDir[, overwrite])
extractAllTo(outputDir, options)
extractAllTo(outputDir, overwrite, options)
```

`options` supports:

- `overwrite` `Boolean` overwrite existing files when `true`
- `filter` `Function | RegExp | String | String[]` selects which entries to extract

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[6,9,10]}
const zip = require('archive/zip');

const z = new zip.Zip();
z.addBuffer('hello world', 'app.log');
z.addEntry({ name: 'config.json', data: '{"enabled":true}' });
z.writeTo('/tmp/data.zip');

const saved = new zip.Zip('/tmp/data.zip');
saved.extractAllTo('/tmp/out', {
	overwrite: true,
	filter: function(entry) {
		return entry.name === 'app.log';
	}
});
```

<h6>Usage example: create from files and extract again</h6>

```js {linenos=table,linenostart=1,hl_lines=[8,9,12,14]}
const fs = require('fs');
const zip = require('archive/zip');
const base = '/tmp/zip-files';

fs.mkdir(base + '/input', { recursive: true });
fs.writeFile(base + '/input/one.txt', 'One', 'utf8');
fs.writeFile(base + '/input/two.txt', 'Two', 'utf8');

const archive = new zip.Zip();
archive.addFile(base + '/input/one.txt');
archive.addFile(base + '/input/two.txt', 'renamed-two.txt');
archive.writeTo(base + '/sample.zip');

const loaded = new zip.Zip(base + '/sample.zip');
loaded.extractAllTo(base + '/out', true);
console.println(fs.readFile(base + '/out/renamed-two.txt', 'utf8'));
```

<h6>Usage example: filter extraction</h6>

```js {linenos=table,linenostart=1,hl_lines=[8,13,18]}
const zip = require('archive/zip');
const fs = require('fs');
const base = '/tmp/zip-filter';

const archive = zip.zipSync([
	{ name: 'keep/a.txt', data: 'A' },
	{ name: 'keep/b.log', data: 'B' },
	{ name: 'skip/c.txt', data: 'C' }
]);

fs.writeFile(base + '.zip', Array.from(new Uint8Array(archive)), 'buffer');

const loaded = new zip.Zip(base + '.zip');
loaded.extractAllTo(base + '-out', {
	overwrite: true,
	filter: /\.txt$/
});
```

## Notes

- `filter` may be a callback, `RegExp`, string match, or array of entry names.
- `extractAllTo()` throws an error if the destination file already exists and `overwrite` is `false`.
- ZIP entry metadata includes `comment`, `method`, `compressedSize`, and `size` when available.
- ZIP entries do not support TAR link metadata such as `symlink` or `linkname`.
