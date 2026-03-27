---
title: "fs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.73" />}}

The `fs` module provides synchronous, Node.js-compatible file system APIs for JSH applications.

## readFile()

Reads a file and returns its content as a string (default: `utf8`) or as bytes.

<h6>Syntax</h6>

```js
readFile(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
const content = fs.readFile('/lib/fs.js', 'utf8');
console.println(content.length);
```

## writeFile()

Writes data to a file. Creates the file or overwrites existing content.

<h6>Syntax</h6>

```js
writeFile(path, data[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile()

Appends data to a file. Creates the file when it does not exist.

<h6>Syntax</h6>

```js
appendFile(path, data[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const fs = require('fs');
fs.writeFile('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFile('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLines()

Counts newline-separated lines in a file.

<h6>Syntax</h6>

```js
countLines(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
console.println(fs.countLines('/work/append.txt'));
```

## exists()

Returns `true` if a file or directory exists.

<h6>Syntax</h6>

```js
exists(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
console.println(fs.exists('/work/test.txt'));
console.println(fs.exists('/work/not-found.txt'));
```

## stat()

Returns file or directory metadata.

<h6>Syntax</h6>

```js
stat(path)
```

<h6>Returned fields</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat()

Returns file metadata. Current implementation behaves the same as `stat()`.

<h6>Syntax</h6>

```js
lstat(path)
```

## readdir()

Reads directory entries.

- Default: returns `string[]`
- `withFileTypes: true`: returns entry objects with `name` and type methods
- `recursive: true`: returns recursive entries

The current runtime directory listing includes `.` and `..` entries.

<h6>Syntax</h6>

```js
readdir(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
const names = fs.readdir('/lib');
const entries = fs.readdir('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdir()

Creates a directory. Supports recursive creation.

<h6>Syntax</h6>

```js
mkdir(path[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
```

## rmdir()

Removes a directory. With `{ recursive: true }`, removes children first.

<h6>Syntax</h6>

```js
rmdir(path[, options])
```

## rm()

Removes a file or directory.

- Directory removal uses `rmdir()` internally
- `force: true` suppresses errors

<h6>Syntax</h6>

```js
rm(path[, options])
```

## unlink()

Removes a file.

<h6>Syntax</h6>

```js
unlink(path)
```

## rename()

Renames or moves a file/directory in the same mounted filesystem.

<h6>Syntax</h6>

```js
rename(oldPath, newPath)
```

## copyFile()

Copies a single file.

`COPYFILE_EXCL` fails when destination exists.

<h6>Syntax</h6>

```js
copyFile(src, dest[, flags])
```

## cp()

Copies a file or directory.

Directory copy requires `{ recursive: true }`.

<h6>Syntax</h6>

```js
cp(src, dest[, options])
```

## symlink()

Creates a symbolic link.

<h6>Syntax</h6>

```js
symlink(target, path)
```

## readlink()

Reads a symbolic link target.

<h6>Syntax</h6>

```js
readlink(path)
```

## realpath()

Returns a resolved path with symlink resolution behavior.

<h6>Syntax</h6>

```js
realpath(path)
```

## access()

Checks path accessibility.

- Throws `ENOENT` when path does not exist
- Supports mode constants: `F_OK`, `R_OK`, `W_OK`, `X_OK`

<h6>Syntax</h6>

```js
access(path[, mode])
```

## truncate()

Truncates file content.

- No length: truncates to `0`
- With length: keeps first `len` bytes

<h6>Syntax</h6>

```js
truncate(path[, len])
```

## open()

Opens a file and returns a numeric file descriptor.

Supports string flags such as `r`, `r+`, `w`, `w+`, `a`, `a+`, `wx`, `wx+`, `ax`, `ax+`.

<h6>Syntax</h6>

```js
open(path, flags[, mode])
```

## close()

Closes a file descriptor.

<h6>Syntax</h6>

```js
close(fd)
```

## read()

Reads from a file descriptor into a buffer.

<h6>Syntax</h6>

```js
read(fd, buffer, offset, length[, position])
```

## write()

Writes string or buffer data to a file descriptor.

<h6>Syntax</h6>

```js
write(fd, buffer, offset, length[, position])
```

## fstat()

Returns metadata from a file descriptor.

<h6>Syntax</h6>

```js
fstat(fd)
```

## fchmod(), fchown()

Changes mode/owner via file descriptor.

<h6>Syntax</h6>

```js
fchmod(fd, mode)
fchown(fd, uid, gid)
```

## fsync(), fdatasync()

Flushes pending file data to storage.

`fdatasync()` currently uses the same behavior as `fsync()`.

<h6>Syntax</h6>

```js
fsync(fd)
fdatasync(fd)
```

## chmod(), chown()

Changes mode/owner by path.

On Windows, `chmod`/`chown` are no-op compatible behaviors in the current runtime implementation.

<h6>Syntax</h6>

```js
chmod(path, mode)
chown(path, uid, gid)
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
fs.access('/work/test.txt', fs.constants.F_OK);
```

## Aliases

For readability, this document introduces APIs using non-`Sync` names.

For Node.js compatibility, the module also exports `Sync`-suffixed aliases.

Examples: `readFileSync`, `writeFileSync`, `appendFileSync`, `readdirSync`, `mkdirSync`, `rmSync`, `statSync`, `openSync`, `closeSync`, `readSync`, `writeSync`, `fstatSync`, `fsyncSync`, `fdatasyncSync`.


## Examples

### Example 1: Read and Parse JSON File

```js {linenos=table,linenostart=1}
const fs = require('fs');

try {
    const content = fs.readFile('/path/to/config.json', 'utf8');
    const config = JSON.parse(content);
    console.println('Config loaded:', config);
} catch (e) {
    console.println('Error reading config:', e);
}
```

### Example 2: Write Log File

```js {linenos=table,linenostart=1}
const fs = require('fs');

function log(message) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${message}\n`;
    fs.appendFile('/tmp/app.log', logEntry, 'utf8');
}

log('Application started');
log('Processing request');
```

### Example 3: Directory Tree Walker

```js {linenos=table,linenostart=1}
const fs = require('fs');

function walkDir(dir, callback, indent = '') {
    const entries = fs.readdir(dir, { withFileTypes: true });

    entries.forEach(entry => {
        const fullPath = dir + '/' + entry.name;

        if (entry.isDirectory()) {
            console.println(indent + '[DIR] ' + entry.name);
            walkDir(fullPath, callback, indent + '  ');
        } else {
            console.println(indent + entry.name);
            callback(fullPath);
        }
    });
}

walkDir('/tmp', (file) => {
    // Process each file
});
```

### Example 4: File Backup

```js {linenos=table,linenostart=1}
const fs = require('fs');

function backupFile(path) {
    if (!fs.exists(path)) {
        throw new Error('File does not exist');
    }

    const timestamp = Date.now();
    const backupPath = path + '.backup.' + timestamp;

    fs.copyFile(path, backupPath);
    console.println('Backup created:', backupPath);

    return backupPath;
}

backupFile('/tmp/important.txt');
```

### Example 5: Safe File Write

```js {linenos=table,linenostart=1}
const fs = require('fs');

function safeWriteFile(path, data) {
    const tempPath = path + '.tmp';

    try {
        // Write to temporary file first
        fs.writeFile(tempPath, data, 'utf8');

        // If successful, rename to target
        fs.rename(tempPath, path);

        console.println('File written safely');
    } catch (e) {
        // Clean up temp file if it exists
        if (fs.exists(tempPath)) {
            fs.unlink(tempPath);
        }
        throw e;
    }
}

safeWriteFile('/tmp/data.txt', 'Important data');
```
