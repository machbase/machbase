---
title: "tar"
type: docs
weight: 100
---

The `archive/tar` module creates and extracts TAR archives in JSH.
It supports simple in-memory helpers, stream-style APIs, and a file-based `Tar` class.

Use the API that matches your task:

- Use `tarSync()` and `untarSync()` when the archive is already in memory.
- Use `Tar` when you want to read files, save `.tar` files, or extract them to disk.
- Use `createTar()` and `createUntar()` when you want event-driven processing.

## Installation

```js
const tar = require('archive/tar');
```

## tarSync()

Creates a TAR archive synchronously.

<h6>Syntax</h6>

```js
tarSync(data)
```

<h6>Parameters</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

If `data` is a single string or byte buffer, the created entry name defaults to `data`.
If `data` is an array, each item should be an entry object such as `{ name, data }`.

<h6>Return value</h6>

Returns an `ArrayBuffer` that contains TAR archive bytes.

This form is useful for quick tests or for building an archive before writing it somewhere else.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,6]}
const tar = require('archive/tar');
const archive = tar.tarSync([
	{ name: 'alpha.txt', data: 'Alpha' },
	{ name: 'dir/beta.txt', data: 'Beta' }
]);
console.println(archive.constructor.name);
```

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const tar = require('archive/tar');
const archive = tar.tarSync('hello tar');
const entries = tar.untarSync(archive);
console.println(entries[0].name, new Uint8Array(entries[0].data).length);
```

## untarSync()

Extracts TAR archive bytes synchronously and returns entry objects.

<h6>Syntax</h6>

```js
untarSync(buffer)
```

<h6>Parameters</h6>

- `buffer` `ArrayBuffer | Uint8Array | Number[]`

<h6>Return value</h6>

Returns an array of entry objects.

Each entry can include `name`, `data`, `mode`, `size`, `isDir`, `modified`, `typeflag`, `type`,
and `linkname`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[7,8,9]}
const tar = require('archive/tar');
const archive = tar.tarSync([
	{ name: 'assets', isDir: true, type: 'dir' },
	{ name: 'assets/readme.txt', data: 'hello' },
	{ name: 'current', type: 'symlink', linkname: 'assets/readme.txt' }
]);
const entries = tar.untarSync(archive);
console.println(entries[0].name, entries[0].isDir, entries[0].type);
console.println(entries[1].name, entries[1].size, entries[1].type);
console.println(entries[2].name, entries[2].type, entries[2].linkname);
```

## tar()

Provides a callback-style asynchronous wrapper for TAR archive creation.

<h6>Syntax</h6>

```js
tar(data, callback)
```

The callback follows the `(err, archive)` form.

## untar()

Provides a callback-style asynchronous wrapper for TAR extraction.

<h6>Syntax</h6>

```js
untar(buffer, callback)
```

The callback follows the `(err, entries)` form.

Use these wrappers when you want callback-based control flow without managing stream events directly.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4,5]}
const tar = require('archive/tar');

tar.tar('payload', function(err, archive) {
	if (err) throw err;
	tar.untar(archive, function(err2, entries) {
		if (err2) throw err2;
		console.println(entries[0].name, new Uint8Array(entries[0].data).length);
	});
});
```

## createTar()

Creates a stream-style TAR writer.

The returned object accepts entry objects through `write()` and emits archive bytes through the
`data` event when `end()` is called.

This API is event-driven, but it still finalizes work on `end()` rather than emitting extracted
files progressively like a Node.js file stream.

<h6>Syntax</h6>

```js
createTar()
```

## createUntar()

Creates a stream-style TAR reader.

Write archive bytes with `write()`, then call `end()` to emit one `entry` event per extracted item.

<h6>Syntax</h6>

```js
createUntar()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[5,10,14,15]}
const tar = require('archive/tar');
const writer = tar.createTar();
let archive = null;

writer.on('data', function(chunk) {
	archive = chunk;
});

writer.on('end', function() {
	const reader = tar.createUntar();
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

## Tar

`Tar` is a file-oriented helper class for building, saving, loading, and extracting TAR archives.

<h6>Constructor</h6>

```js
new tar.Tar(filePath?)
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

Supported TAR entry fields:

- `name` `String` required entry path
- `data` `String | ArrayBuffer | Uint8Array | Number[]` file content
- `mode` `Number` file mode
- `modified` `Date` modification time
- `type` `String` such as `file`, `dir`, `symlink`, or `link`
- `typeflag` `Number` raw TAR type flag
- `linkname` `String` link target for `symlink` or `link`
- `isDir` `Boolean` marks a directory entry

`addFile()` is the most direct option when the source data already exists on disk.
`addBuffer()` is useful when the content is generated in memory.
`addEntry()` is the lowest-level form and is required for TAR directory or link metadata.

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

```js {linenos=table,linenostart=1,hl_lines=[7,8,9]}
const tar = require('archive/tar');

const t = new tar.Tar();
t.addEntry({ name: 'docs', isDir: true, type: 'dir' });
t.addEntry({ name: 'docs/readme.txt', data: 'hello tar' });
t.addEntry({ name: 'latest', type: 'symlink', linkname: 'docs/readme.txt' });
t.writeTo('/tmp/bundle.tar');

const saved = new tar.Tar('/tmp/bundle.tar');
saved.extractAllTo('/tmp/out', {
	overwrite: true,
	filter: function(entry) {
		return entry.name.endsWith('.txt');
	}
});
```

<h6>Usage example: create from files and extract again</h6>

```js {linenos=table,linenostart=1,hl_lines=[8,9,12,14]}
const fs = require('fs');
const tar = require('archive/tar');
const base = '/tmp/tar-files';

fs.mkdir(base + '/input', { recursive: true });
fs.writeFile(base + '/input/one.txt', 'One', 'utf8');
fs.writeFile(base + '/input/two.txt', 'Two', 'utf8');

const archive = new tar.Tar();
archive.addFile(base + '/input/one.txt');
archive.addFile(base + '/input/two.txt', 'renamed-two.txt');
archive.writeTo(base + '/sample.tar');

const loaded = new tar.Tar(base + '/sample.tar');
loaded.extractAllTo(base + '/out', true);
console.println(fs.readFile(base + '/out/renamed-two.txt', 'utf8'));
```

<h6>Usage example: filter extraction</h6>

```js {linenos=table,linenostart=1,hl_lines=[8,13,18]}
const tar = require('archive/tar');
const fs = require('fs');
const base = '/tmp/tar-filter';

const archive = tar.tarSync([
	{ name: 'keep/a.txt', data: 'A' },
	{ name: 'keep/b.log', data: 'B' },
	{ name: 'skip/c.txt', data: 'C' }
]);

fs.writeFile(base + '.tar', Array.from(new Uint8Array(archive)), 'buffer');

const loaded = new tar.Tar(base + '.tar');
loaded.extractAllTo(base + '-out', {
	overwrite: true,
	filter: /\.txt$/
});
```

## Notes

- Directory entries are returned with `isDir: true`, and their names end with `/`.
- `filter` may be a callback, `RegExp`, string match, or array of entry names.
- `extractAllTo()` throws an error if the destination file already exists and `overwrite` is `false`.
- TAR-specific link metadata is supported through `type: 'symlink'` or `type: 'link'` with `linkname`.
