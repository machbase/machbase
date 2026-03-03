---
title: "fs"
type: docs
weight: 4
---

{{< neo_since ver="8.0.73" />}}

The `fs` module provides synchronous, Node.js-compatible file system APIs for JSH applications.

## readFileSync()

Reads a file and returns its content as a string (default: `utf8`) or as bytes.

<h6>Syntax</h6>

```js
readFileSync(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
const content = fs.readFileSync('/lib/fs/index.js', 'utf8');
console.println(content.length);
```

## writeFileSync()

Writes data to a file. Creates the file or overwrites existing content.

<h6>Syntax</h6>

```js
writeFileSync(path, data[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.writeFileSync('/work/test.txt', 'Hello', 'utf8');
```

## appendFileSync()

Appends data to a file. Creates the file when it does not exist.

<h6>Syntax</h6>

```js
appendFileSync(path, data[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const fs = require('fs');
fs.writeFileSync('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFileSync('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLinesSync()

Counts newline-separated lines in a file.

<h6>Syntax</h6>

```js
countLinesSync(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
console.println(fs.countLinesSync('/work/append.txt'));
```

## existsSync()

Returns `true` if a file or directory exists.

<h6>Syntax</h6>

```js
existsSync(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
console.println(fs.existsSync('/work/test.txt'));
console.println(fs.existsSync('/work/not-found.txt'));
```

## statSync()

Returns file or directory metadata.

<h6>Syntax</h6>

```js
statSync(path)
```

<h6>Returned fields</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const fs = require('fs');
const st = fs.statSync('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstatSync()

Returns file metadata. Current implementation behaves the same as `statSync()`.

<h6>Syntax</h6>

```js
lstatSync(path)
```

## readdirSync()

Reads directory entries.

- Default: returns `string[]`
- `withFileTypes: true`: returns entry objects with `name` and type methods
- `recursive: true`: returns recursive entries

The current runtime directory listing includes `.` and `..` entries.

<h6>Syntax</h6>

```js
readdirSync(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
const names = fs.readdirSync('/lib');
const entries = fs.readdirSync('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdirSync()

Creates a directory. Supports recursive creation.

<h6>Syntax</h6>

```js
mkdirSync(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.mkdirSync('/work/a/b/c', { recursive: true });
```

## rmdirSync()

Removes a directory. With `{ recursive: true }`, removes children first.

<h6>Syntax</h6>

```js
rmdirSync(path[, options])
```

## rmSync()

Removes a file or directory.

- Directory removal uses `rmdirSync()` internally
- `force: true` suppresses errors

<h6>Syntax</h6>

```js
rmSync(path[, options])
```

## unlinkSync()

Removes a file.

<h6>Syntax</h6>

```js
unlinkSync(path)
```

## renameSync()

Renames or moves a file/directory in the same mounted filesystem.

<h6>Syntax</h6>

```js
renameSync(oldPath, newPath)
```

## copyFileSync()

Copies a single file.

`COPYFILE_EXCL` fails when destination exists.

<h6>Syntax</h6>

```js
copyFileSync(src, dest[, flags])
```

## cpSync()

Copies a file or directory.

Directory copy requires `{ recursive: true }`.

<h6>Syntax</h6>

```js
cpSync(src, dest[, options])
```

## symlinkSync()

Creates a symbolic link.

<h6>Syntax</h6>

```js
symlinkSync(target, path)
```

## readlinkSync()

Reads a symbolic link target.

<h6>Syntax</h6>

```js
readlinkSync(path)
```

## realpathSync()

Returns a resolved path with symlink resolution behavior.

<h6>Syntax</h6>

```js
realpathSync(path)
```

## accessSync()

Checks path accessibility.

- Throws `ENOENT` when path does not exist
- Supports mode constants: `F_OK`, `R_OK`, `W_OK`, `X_OK`

<h6>Syntax</h6>

```js
accessSync(path[, mode])
```

## truncateSync()

Truncates file content.

- No length: truncates to `0`
- With length: keeps first `len` bytes

<h6>Syntax</h6>

```js
truncateSync(path[, len])
```

## openSync()

Opens a file and returns a numeric file descriptor.

Supports string flags such as `r`, `r+`, `w`, `w+`, `a`, `a+`, `wx`, `wx+`, `ax`, `ax+`.

<h6>Syntax</h6>

```js
openSync(path, flags[, mode])
```

## closeSync()

Closes a file descriptor.

<h6>Syntax</h6>

```js
closeSync(fd)
```

## readSync()

Reads from a file descriptor into a buffer.

<h6>Syntax</h6>

```js
readSync(fd, buffer, offset, length[, position])
```

## writeSync()

Writes string or buffer data to a file descriptor.

<h6>Syntax</h6>

```js
writeSync(fd, buffer, offset, length[, position])
```

## fstatSync()

Returns metadata from a file descriptor.

<h6>Syntax</h6>

```js
fstatSync(fd)
```

## fchmodSync(), fchownSync()

Changes mode/owner via file descriptor.

<h6>Syntax</h6>

```js
fchmodSync(fd, mode)
fchownSync(fd, uid, gid)
```

## fsyncSync(), fdatasyncSync()

Flushes pending file data to storage.

`fdatasyncSync()` currently uses the same behavior as `fsyncSync()`.

<h6>Syntax</h6>

```js
fsyncSync(fd)
fdatasyncSync(fd)
```

## chmodSync(), chownSync()

Changes mode/owner by path.

On Windows, `chmod`/`chown` are no-op compatible behaviors in the current runtime implementation.

<h6>Syntax</h6>

```js
chmodSync(path, mode)
chownSync(path, uid, gid)
```

## createReadStream(), createWriteStream()

Creates stream objects compatible with EventEmitter-based usage.

<h6>Syntax</h6>

```js
createReadStream(path[, options])
createWriteStream(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
const rs = fs.createReadStream('/work/in.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/out.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## platform(), arch()

Returns runtime platform and architecture strings.

<h6>Syntax</h6>

```js
platform()
arch()
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
console.println(fs.platform());
console.println(fs.arch());
```

## constants

Constant object for access, copy, and open flags.

<h6>Main fields</h6>

- Access: `F_OK`, `R_OK`, `W_OK`, `X_OK`
- Copy: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- Open: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.accessSync('/work/test.txt', fs.constants.F_OK);
```

## Aliases

For Node.js compatibility, the module also exports non-`Sync` aliases.

Examples: `readFile`, `writeFile`, `appendFile`, `readdir`, `mkdir`, `rm`, `stat`, `open`, `close`, `read`, `write`, `fstat`, `fsync`, `fdatasync`.
