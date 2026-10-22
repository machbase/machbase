---
title: "fs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `fs` module provides synchronous, Node.js-compatible file system APIs for JSH applications.

API names and argument formats follow the Node.js `fs` module, but every function runs synchronously on top of the JSH virtual file system. Behaviors that differ from Node.js are listed under **Notes** for each function.

## Paths and mounts

JSH mounts several kinds of file systems into a single virtual directory tree. Paths passed to `fs` functions are virtual paths, and relative paths are resolved against the current working directory.

Supported features depend on the mount type.

| Mount type | Example | Characteristics |
| --- | --- | --- |
| Host directory | `/work`, `/tmp` | Directly backed by the operating system file system. All APIs are supported. |
| Memory-backed | `/lib` | File contents are kept in memory. Path-based APIs such as `readFile`/`writeFile` are supported, but write file descriptors (`open(path, 'w')`, etc.) fail with `ENOTSUP`. `fsync()` on a read descriptor also returns `ENOTSUP`. The maximum size of a single file is 1GiB. |
| Read-only (embedded) | `/usr`, `/sbin` | Files embedded in the executable. Write operations fail with `EACCES`, and `fsync()` on a descriptor returns `ENOTSUP`. |
| Shared file system | Depends on the service configuration | Shared storage provided by the service controller to multiple JSH processes. The maximum size of a single file is 1GiB. |

{{< callout emoji="⚠️" >}}
Files cannot be moved between different mounts with `rename()`; it fails with an `EXDEV` error. In that case, copy the file with `copyFile()` or `cp()` and then remove the original.
{{< /callout >}}

Regardless of the mount type, the root directory of each mount (for example, `/work` or `/lib`) is a mount point. Intermediate directories that exist only because of nested mounts (for example, `/a` when only `/a/b` is mounted) are also treated as mount points. A mount point cannot be removed with `rmdir()`, `unlink()`, or `rm()`, and cannot be the source or destination of `rename()`. All such operations fail with `EBUSY`, and the mount point and mount configuration are left unchanged. Files and directories **inside** a mount point can be removed or moved as usual.

## Error handling

When a file system operation fails, an `Error` object in the same format as Node.js is thrown.

| Property | Description |
| --- | --- |
| `code` | Error code string. e.g. `ENOENT`, `EEXIST` |
| `errno` | Error number (negative). e.g. `-2` |
| `syscall` | Name of the failed operation. e.g. `open`, `mkdir`, `rmdir` |
| `path` | Target path. Not included in errors from file-descriptor-based functions (`read()`, `write()`, `close()`, `fstat()`, `fsync()`, etc.). |
| `dest` | Destination path for `rename()` errors |

The error message format is `CODE: description, syscall 'path'`, for example `ENOENT: no such file or directory, open '/work/none.txt'`.

```js {linenos=table,linenostart=1}
const fs = require('fs');
try {
    fs.readFile('/work/none.txt');
} catch (e) {
    console.println(e.code, e.errno, e.syscall, e.path);
    // ENOENT -2 open /work/none.txt
}
```

<h6>Main error codes</h6>

| Code | errno | Meaning |
| --- | --- | --- |
| `EPERM` | -1 | Operation not permitted |
| `ENOENT` | -2 | No such file or directory |
| `EIO` | -5 | Input/output error |
| `EBADF` | -9 | Bad file descriptor. A closed or nonexistent descriptor, or writing to a descriptor opened read-only, etc. |
| `EACCES` | -13 | Permission denied, including writes to a read-only mount |
| `EBUSY` | -16 | Resource busy. Raised when removing or moving a mount point |
| `EEXIST` | -17 | Already exists |
| `EXDEV` | -18 | Move between different mounts |
| `ENOTDIR` | -20 | Not a directory |
| `EISDIR` | -21 | Operation not allowed on a directory |
| `EINVAL` | -22 | Invalid argument |
| `EFBIG` | -27 | File too large. Exceeds the 1GiB limit of memory-backed and shared file systems |
| `ENOSPC` | -28 | No space left on device |
| `EROFS` | -30 | Read-only file system |
| `ENAMETOOLONG` | -36 | File name too long |
| `ENOTEMPTY` | -39 | Directory not empty |
| `ELOOP` | -40 | Too many levels of symbolic links |
| `ENOTSUP` | -95 | Operation not supported |
| `ECONFLICT` | -32009 | (JSH only) Another process modified the same file on the shared file system after the descriptor was opened |

- `errno` values are fixed to the values in the table above (Linux values) regardless of the platform. They may differ from the `errno` numbers reported by Node.js on macOS or Windows, so use `code` rather than `errno` to identify errors.
- When an argument such as `offset`, `length`, `position`, or `len` is out of range, a `RangeError` is thrown with `code` set to `ERR_OUT_OF_RANGE` and no `errno`.

## readFile()

Reads a file and returns its contents as a string (default: `utf8`) or a byte array.

<h6>Syntax</h6>

```js
readFile(path[, options])
```

- `options` is an encoding string or an `{ encoding }` object. Specify `encoding: null` to get a byte array.
- The whole file is read into memory. For large files, read in chunks with `createReadStream()` or `open()`/`read()`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const content = fs.readFile('/lib/fs.js', 'utf8');
console.println(content.length);
```

## writeFile()

Writes data to a file. Creates the file if it does not exist, or overwrites it if it does.

<h6>Syntax</h6>

```js
writeFile(path, data[, options])
```

- Fails with `ENOENT` if the parent directory does not exist. Call `mkdir(dir, { recursive: true })` first if needed.
- On memory-backed mounts and the shared file system, files larger than 1GiB cannot be written.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile()

Appends data to the end of a file. Creates the file if it does not exist.

<h6>Syntax</h6>

```js
appendFile(path, data[, options])
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFile('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLines()

Counts the number of lines in a file (based on newlines). This function is specific to JSH.

<h6>Syntax</h6>

```js
countLines(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.countLines('/work/append.txt'));
```

## exists()

Returns `true`/`false` indicating whether a file or directory exists.

<h6>Syntax</h6>

```js
exists(path)
```

- Symbolic links are followed. A link whose target does not exist (a broken link) returns `false`. Use `lstat()` to check whether the link itself exists.
- Also returns `false` when the check fails for other reasons, such as insufficient permissions. Use `access()` or `stat()` if you need the cause of the failure.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.exists('/work/test.txt'));
console.println(fs.exists('/work/not-found.txt'));
```

## stat()

Returns metadata for a file or directory. If the path is a symbolic link, information about the link target is returned.

<h6>Syntax</h6>

```js
stat(path)
```

<h6>Returned fields</h6>

- `name`: File name (the last path component)
- `size`: Size in bytes
- `mode`: File mode object. `String(st.mode)` returns a string such as `drwxr-xr-x`.
- `mtime`, `atime`, `ctime`, `birthtime`: In the current implementation, all have the same value as the modification time (`mtime`).
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat()

Returns file metadata. Unlike `stat()`, if the last path component is a symbolic link, the link is not followed and information about the link itself is returned. The returned fields are the same as `stat()`. Intermediate directories created by nested mounts are reported as directories, just as with `stat()`.

<h6>Syntax</h6>

```js
lstat(path)
```

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/target.txt', 'data');
fs.symlink('target.txt', '/work/link.txt');
console.println(fs.lstat('/work/link.txt').isSymbolicLink()); // true
console.println(fs.stat('/work/link.txt').isFile());          // true
```

## readdir()

Reads directory entries.

- Default: returns a `string[]` of entry names.
- `withFileTypes: true`: returns entry objects with `name` and type methods (`isFile()`, `isDirectory()`, `isSymbolicLink()`, etc.).
- `recursive: true`: returns entries recursively, including subdirectories.

<h6>Syntax</h6>

```js
readdir(path[, options])
```

<h6>Notes</h6>

- **Non-recursive listings include the `.` and `..` entries.** This differs from Node.js, so always skip these two entries when walking directories. Otherwise, the same directory may be traversed recursively forever.
- Recursive listings (`recursive: true`) do not include `.` and `..`.
  - String results are paths relative to the starting directory (e.g. `a/b/file.txt`).
  - The `path` property of an entry object is the relative path of the directory containing the entry; it is `''` for entries directly under the starting directory. This differs from Node.js `Dirent.path` (the full path of the parent directory).
- Recursive listings do not descend into symbolic links that point to directories. Such links are returned only as entries.
- If a subdirectory cannot be read during a recursive listing (e.g. insufficient permissions), the whole listing fails with an error. The `path` of the error object points to the failed subdirectory.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const names = fs.readdir('/lib').filter(n => n !== '.' && n !== '..');
const all = fs.readdir('/work', { recursive: true });
console.println(names.length, all.length);
```

## mkdir()

Creates a directory.

<h6>Syntax</h6>

```js
mkdir(path[, options])
```

<h6>Options</h6>

- `recursive`: If `true`, missing parent directories are created as well, and existing directories are skipped without error. The default is `false`.
- `mode`: Permissions of the directory to create. The default is `0o755`, and it applies to every directory newly created during recursive creation. On host directories, the operating system umask may also apply.

<h6>Behavior</h6>

- Non-recursive call (`recursive: false`)
  - Fails with `ENOENT` if the parent directory does not exist. Parent directories are not created automatically.
  - Fails with `EEXIST` if the target already exists, whether it is a directory or a file.
- Recursive call (`recursive: true`)
  - Fails with `EEXIST` if a **file** with the same name exists in the middle of the path. Node.js returns `ENOTDIR` in this case.
  - Always returns `undefined`. Unlike Node.js, the first created path is not returned.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
fs.mkdir('/work/private', { mode: 0o700 });
```

## rmdir()

Removes an empty directory.

<h6>Syntax</h6>

```js
rmdir(path[, options])
```

- Fails with `ENOTEMPTY` if the directory is not empty, or `ENOTDIR` if the target is a file.
- With `{ recursive: true }`, all child entries are removed first. This option is deprecated in Node.js, so `rm(path, { recursive: true })` is recommended for new code.
- During recursive removal, symbolic links pointing to directories are removed as links only; the contents of the link target are not deleted.
- Fails with `EBUSY` if a mount point is specified. Recursive removal handles mount points in the same way as [rm()](#rm).

## rm()

Removes a file, symbolic link, or directory.

<h6>Syntax</h6>

```js
rm(path[, options])
```

<h6>Options</h6>

- `recursive`: If `true`, removes the directory and all of its contents.
- `force`: If `true`, ignores the error when the target does not exist (`ENOENT`).

<h6>Notes</h6>

- The target type is determined with `lstat()`. A symbolic link is removed **as a link only**, even if it points to a directory; the target directory and its contents are preserved.
- Without `recursive`, only an empty directory can be removed. A non-empty directory fails with `ENOTEMPTY`.
- `force: true` ignores only `ENOENT`. Other errors, such as insufficient permissions (`EACCES`) and I/O errors (`EIO`), are thrown as is. `EBUSY` raised for a mount point is not ignored either.
- If an error occurs during recursive removal, the operation stops immediately. Entries already removed are not restored, so the tree may be left partially deleted.
- Mount points are an exception. When the target itself or a directory under it is a mount point, only its contents are removed and it is left as an empty directory. Removal continues with the remaining entries, and after all entries are processed, `EBUSY` is thrown with the path of the first mount point encountered. The result is the same as running `rm -r` on a mounted directory on Linux.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.rm('/work/a', { recursive: true, force: true });
```

## unlink()

Removes a file or symbolic link.

<h6>Syntax</h6>

```js
unlink(path)
```

- Cannot be used on directories; fails with `EISDIR`. Use `rmdir()` or `rm()` for directories.
- When a symbolic link is specified, only the link is removed and the target file is kept.
- Fails with `EBUSY` if a mount point is specified.
- On Windows, files with the read-only attribute are also removed.

{{< callout emoji="📌" >}}
Removing or moving the last entry with `unlink()`, `rmdir()`, `rm()`, or `rename()` leaves the parent directory in place. Memory-backed mounts and the shared file system behave the same way.
{{< /callout >}}

## rename()

Renames or moves a file or directory within the same mount.

<h6>Syntax</h6>

```js
rename(oldPath, newPath)
```

- If a file exists at the destination path, it is overwritten according to the operating system `rename` behavior.
- Moving between different mounts fails with `EXDEV`. In this case, the `dest` property of the error object contains the destination path.
- Fails with `EBUSY` if the source or destination is a mount point.

## copyFile()

Copies a single file.

<h6>Syntax</h6>

```js
copyFile(src, dest[, flags])
```

- By default, an existing destination file is overwritten.
- If `constants.COPYFILE_EXCL` is specified in `flags`, it fails with `EEXIST` when the destination file exists.
- `COPYFILE_FICLONE` and `COPYFILE_FICLONE_FORCE` are ignored, and a regular copy is performed.
- Only file contents are copied. The permissions and modification time of the source file are not preserved.
- The whole file is read into memory before writing, so it is not suitable for copying very large files.

## cp()

Copies a file or directory.

<h6>Syntax</h6>

```js
cp(src, dest[, options])
```

<h6>Options</h6>

- `recursive`: Must be `true` to copy a directory. If omitted, copying a directory fails with `EISDIR`.
- `force`: If `true`, existing files at the destination are overwritten.

<h6>Notes</h6>

- **The default value of `force` is `false`.** If a destination file already exists, it fails with `EEXIST`. This differs from Node.js `cpSync()`, which overwrites by default.
- Symbolic links in the source are followed and their target contents are copied. The links themselves are not copied.
- Only file contents are copied; permissions and modification times are not preserved.

## symlink()

Creates a symbolic link.

<h6>Syntax</h6>

```js
symlink(target, path)
```

- If `target` is a relative path, it is resolved **relative to the directory containing the link**, as in Node.js, and stored as the relative path.
- If `target` starts with `/`, it is treated as a JSH virtual path.
- If the link target would point outside the mounted area (e.g. `../../../etc/passwd`), it fails with `EACCES`.
- The Node.js third argument (`type`) is not supported.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/data', { recursive: true });
fs.writeFile('/work/data/v1.csv', 'a,b\n');
fs.symlink('v1.csv', '/work/data/current.csv');   // relative to /work/data
console.println(fs.readFile('/work/data/current.csv'));
```

## readlink()

Reads the target path of a symbolic link.

<h6>Syntax</h6>

```js
readlink(path)
```

- **The return value is always a fully resolved absolute virtual path.** Even if the link is stored as a relative path (`v1.csv`), it is returned as `/work/data/v1.csv`. This differs from Node.js, which returns the stored string as is.
- Throws `EINVAL` for a path that is not a symbolic link.
- Throws `ENOENT` if the link points outside the mounted area.

## realpath()

Returns the real path with all symbolic links, `.`, and `..` resolved.

<h6>Syntax</h6>

```js
realpath(path)
```

- Symbolic links in intermediate directories are resolved as well as the last path component.
- Throws `ENOENT` if a path component does not exist, and `ELOOP` if more than 40 links must be followed, for example due to a link cycle.
- The return value is a JSH virtual path.

## access()

Checks whether a path exists and whether it can be accessed with the specified permissions. Returns `undefined` if accessible; otherwise throws an error.

<h6>Syntax</h6>

```js
access(path[, mode])
```

- `mode` is a bitwise OR of `constants.F_OK` (existence, default), `R_OK` (read), `W_OK` (write), and `X_OK` (execute).
- Throws `ENOENT` if the path does not exist, `EACCES` if permission is denied, and `EINVAL` if `mode` is outside the range 0-7.

<h6>Notes</h6>

- On host directory mounts, the operating system permission check is used.
- On Windows, the behavior is the same as Node.js.
  - Checking `W_OK` on a file with the read-only attribute throws `EPERM`.
  - `X_OK` is treated the same as the existence check (`F_OK`).
- On memory-backed, embedded, and shared file systems, the JSH process is treated as the file owner, and the decision is based on the **owner** permission bits of the file mode. For example, a `0o600` file passes `R_OK`/`W_OK` checks, and a `0o004` file fails the `R_OK` check. Groups and ACLs are not considered.
- `W_OK` checks on read-only mounts always fail.
- The state may change between checking with `access()` and opening the file. Where possible, open the file directly and handle the error.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
try {
    fs.access('/work/test.txt', fs.constants.R_OK | fs.constants.W_OK);
    console.println('readable and writable');
} catch (e) {
    console.println('no access:', e.code);
}
```

## truncate()

Sets the file size to the specified length.

<h6>Syntax</h6>

```js
truncate(path[, len])
```

- If `len` is omitted, the file is truncated to `0`.
- If `len` is smaller than the current size, only the first `len` bytes are kept.
- If `len` is larger than the current size, the file is extended and the added part is filled with `0` bytes.
- Throws a `RangeError` (`ERR_OUT_OF_RANGE`) if `len` is negative or not an integer.
- On memory-backed mounts and the shared file system, a length larger than 1GiB fails with `EFBIG`, and the file is left unchanged.

## open()

Opens a file and returns a numeric file descriptor.

<h6>Syntax</h6>

```js
open(path, flags[, mode])
```

- `flags`: A string flag or a numeric flag combining `constants.O_*` values.
- `mode`: Permissions used when a new file is created. The default is `0o666`.

<h6>String flags</h6>

| Flag | Meaning |
| --- | --- |
| `r` | Read. Fails if the file does not exist |
| `r+` | Read/write. Fails if the file does not exist |
| `w` | Write. Creates the file if missing, truncates it if it exists |
| `w+` | Read/write. Creates the file if missing, truncates it if it exists |
| `a` | Append. Creates the file if missing |
| `a+` | Read/append. Creates the file if missing |
| `wx`, `wx+`, `ax`, `ax+` | Same as above, but fails with `EEXIST` if the file already exists |

<h6>Notes</h6>

- String flags not listed in the table above are treated as `r` (read-only) without error. A typo does not raise an error, and a subsequent `write()` may fail with `EBADF`, so specify flag strings exactly.
- On memory-backed mounts (e.g. `/lib`), only read descriptors can be opened. Write flags fail with `ENOTSUP`, so use `writeFile()`/`appendFile()` instead.
- Opening a file on a read-only (embedded) mount with write flags fails with `EACCES`.
- Always close descriptors with `close()` when you are done.

## close()

Closes a file descriptor.

<h6>Syntax</h6>

```js
close(fd)
```

- A descriptor that is already closed or does not exist fails with `EBADF`.
- On the shared file system, changes are saved when the descriptor is closed. If another process modified the same file after the descriptor was opened, it fails with `ECONFLICT`.

## read()

Reads data from a file descriptor into a buffer and returns the number of bytes read. Returns `0` at the end of the file.

<h6>Syntax</h6>

```js
read(fd, buffer, offset, length[, position])
```

- `buffer`: A `Uint8Array`, `Buffer`, or number array that receives the data
- `offset`: Position in the buffer to start writing. The default is `0`.
- `length`: Maximum number of bytes to read. The default is `buffer.length - offset`.
- `position`: Position in the file to start reading
  - `null` or omitted: Reads from the current file position, and the current position advances by the number of bytes read.
  - Integer of 0 or greater: Reads from the specified position, and **the current file position does not change.**

<h6>Notes</h6>

- Throws a `RangeError` (`ERR_OUT_OF_RANGE`) if `offset`, `length`, or `position` is out of range, for example when `offset + length` exceeds the buffer size or `position` is negative.
- Reading from a descriptor opened write-only fails with `EBADF`.
- On Linux/macOS, reading from a directory descriptor fails with `EISDIR`. Use `readdir()` to read directory contents.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/data.bin', 'ABCDEFGH');
const fd = fs.open('/work/data.bin', 'r');
const buf = new Uint8Array(4);
fs.read(fd, buf, 0, 4, 4);   // reads "EFGH", file position unchanged
fs.read(fd, buf, 0, 4);      // reads "ABCD" from the current position
fs.close(fd);
```

## write()

Writes buffer or string data to a file descriptor and returns the number of bytes written.

<h6>Syntax</h6>

```js
write(fd, data[, offset[, length[, position]]])
```

- `data`: A `Uint8Array`, `Buffer`, number array, or string. Strings are converted to UTF-8 bytes before writing.
- `offset`: Byte position in `data` to start writing from. The default is `0`.
- `length`: Number of bytes to write. The default is from `offset` to the end. Specifying `0` writes nothing.
- `position`: Position in the file to start writing
  - `null` or omitted: Writes at the current file position, and the current position advances by the number of bytes written.
  - Integer of 0 or greater: Writes at the specified position, and **the current file position does not change.** If the position is beyond the end of the file, the gap is filled with `0` bytes.

<h6>Notes</h6>

- **The argument order is `(fd, data, offset, length, position)` even when writing a string.** The Node.js `writeSync(fd, string, position, encoding)` form is not supported. For example, in `write(fd, 'Z', 3)`, `3` is interpreted as `offset`, not as the file position, so `ERR_OUT_OF_RANGE` is thrown.
- For strings, `offset` and `length` are in UTF-8 **bytes**, not characters.
- Descriptors opened in append mode, such as `a` and `a+`, ignore `position` and always write at the end of the file.
- Throws a `RangeError` (`ERR_OUT_OF_RANGE`) if `offset`, `length`, or `position` is out of range.
- Writing to a descriptor opened read-only fails with `EBADF`.
- On the shared file system, a write that makes the file larger than 1GiB fails with `EFBIG`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const fd = fs.open('/work/out.txt', 'w+');
fs.write(fd, 'Hello World');                // write at the current position
fs.write(fd, 'J', 0, 1, 0);                 // overwrite the first byte: "Jello World"
const bytes = new Uint8Array([0x21, 0x21]);
fs.write(fd, bytes, 0, bytes.length);       // append "!!" at the current position
fs.close(fd);
```

## fstat()

Returns metadata for a file descriptor.

<h6>Syntax</h6>

```js
fstat(fd)
```

- The returned object provides `name`, `size`, `mode`, `mtime`, and type methods (`isFile()`, etc.). `atime`, `ctime`, and `birthtime` are not included.

## fchmod(), fchown()

Changes mode/owner by file descriptor.

<h6>Syntax</h6>

```js
fchmod(fd, mode)
fchown(fd, uid, gid)
```

- On Windows, these do nothing and succeed for file descriptors opened on host directory mounts.
- Other mounts follow their own filesystem behavior. For example, descriptors on read-only (embedded) mounts throw `EACCES`.

## fsync(), fdatasync()

Flushes pending file data to storage.

<h6>Syntax</h6>

```js
fsync(fd)
fdatasync(fd)
```

- Currently, `fdatasync()` behaves the same as `fsync()`.
- Descriptors opened on read-only (embedded) mounts and read descriptors on memory-backed mounts (for example, `/lib`) have nothing to synchronize, so `ENOTSUP` is thrown. This differs from Node.js.
- On the shared file system, if another process modified the same file after the descriptor was opened, it fails with `ECONFLICT`.

## chmod(), chown()

Changes mode/owner by path.

On Windows, `chmod`/`chown` are no-op compatible behaviors on host directory mounts. Memory-backed, embedded, and shared file systems follow their own behavior.

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

```js {linenos=table,linenostart=1}
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

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.platform());
console.println(fs.arch());
```

## constants

Constant object containing access, copy, and file open flags.

<h6>Main fields</h6>

- Access: `F_OK` (0), `R_OK` (4), `W_OK` (2), `X_OK` (1)
- Copy: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- File open: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

The actual values of the file open constants may differ by platform, so use the constants instead of hard-coded numbers.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.access('/work/test.txt', fs.constants.F_OK);
const fd = fs.open('/work/new.txt', fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL);
fs.close(fd);
```

## Aliases

For readability, this document introduces APIs with non-`Sync` names.

For Node.js compatibility, `Sync` suffixed aliases are also provided. Both names refer to the same function, and both run synchronously. Callback- or Promise-based APIs are not provided.

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
    console.println('Error reading config:', e.code || e);
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

Non-recursive `readdir()` results include `.` and `..`, so they must always be skipped.

```js {linenos=table,linenostart=1}
const fs = require('fs');

function walkDir(dir, callback, indent = '') {
    const entries = fs.readdir(dir, { withFileTypes: true });

    entries.forEach(entry => {
        if (entry.name === '.' || entry.name === '..') {
            return;
        }
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

If you only need all of the paths, you can use the `recursive` option.

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.readdir('/tmp', { recursive: true }).forEach(p => console.println(p));
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

    fs.copyFile(path, backupPath, fs.constants.COPYFILE_EXCL);
    console.println('Backup created:', backupPath);

    return backupPath;
}

backupFile('/tmp/important.txt');
```

### Example 5: Safe File Write

Write to a temporary file first, then replace the target with `rename()`. Because `rename()` works only within the same mount, create the temporary file in the same directory as the target file.

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
        fs.rm(tempPath, { force: true });
        throw e;
    }
}

safeWriteFile('/tmp/data.txt', 'Important data');
```

### Example 6: Handling Errors by Code

```js {linenos=table,linenostart=1}
const fs = require('fs');

function ensureDir(path) {
    try {
        fs.mkdir(path);
    } catch (e) {
        if (e.code === 'EEXIST' && fs.stat(path).isDirectory()) {
            return;   // already exists
        }
        if (e.code === 'ENOENT') {
            fs.mkdir(path, { recursive: true });   // parent is missing
            return;
        }
        throw e;
    }
}

ensureDir('/work/output/2024');
```
