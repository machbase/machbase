---
title: "fs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`fs` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 동기 파일 시스템 API를 제공합니다.

API 이름과 인자 형식은 Node.js의 `fs` 모듈을 따르지만, 모든 함수는 동기 방식으로 동작하며 JSH의 가상 파일 시스템 위에서 실행됩니다. Node.js와 동작이 다른 부분은 각 함수의 **주의사항**에 정리되어 있습니다.

## 경로와 마운트

JSH는 여러 종류의 파일 시스템을 하나의 가상 디렉터리 트리에 마운트하여 제공합니다. `fs` 함수에 전달하는 경로는 이 가상 경로이며, 상대 경로는 현재 작업 디렉터리를 기준으로 해석됩니다.

마운트 종류에 따라 지원하는 기능이 다릅니다.

| 마운트 종류 | 예시 | 특징 |
| --- | --- | --- |
| 호스트 디렉터리 | `/work`, `/tmp` | 운영체제 파일 시스템에 직접 연결됩니다. 모든 API를 지원합니다. |
| 메모리 기반 | `/lib` | 파일 내용을 메모리에 보관합니다. `readFile`/`writeFile` 등 경로 기반 API는 지원하지만, 쓰기용 파일 디스크립터(`open(path, 'w')` 등)는 `ENOTSUP`으로 실패합니다. 읽기용 디스크립터에 대한 `fsync()`도 `ENOTSUP`을 반환합니다. 파일 하나의 최대 크기는 1GiB입니다. |
| 읽기 전용(내장) | `/usr`, `/sbin` | 실행 파일에 내장된 파일입니다. 쓰기 작업은 `EACCES`로 실패하며, 디스크립터에 대한 `fsync()`는 `ENOTSUP`을 반환합니다. |
| 공유 파일 시스템 | 서비스 설정에 따름 | 서비스 컨트롤러가 여러 JSH 프로세스에 제공하는 공유 저장소입니다. 파일 하나의 최대 크기는 1GiB입니다. |

{{< callout emoji="⚠️" >}}
서로 다른 마운트 사이에서는 `rename()`으로 파일을 이동할 수 없으며 `EXDEV` 오류가 발생합니다. 이 경우 `copyFile()` 또는 `cp()`로 복사한 뒤 원본을 삭제하세요.
{{< /callout >}}

마운트 종류와 관계없이 각 마운트의 루트 디렉터리(예: `/work`, `/lib`)는 마운트 지점입니다. 하위 경로에 다른 마운트가 있는 디렉터리도 마운트 지점으로 취급합니다. 중첩 마운트 때문에 생긴 중간 디렉터리(예: `/a/b`만 마운트되었을 때의 `/a`)뿐 아니라, 상위 마운트에 실제로 존재하는 디렉터리(예: `/data/inner`가 마운트된 경우 루트 마운트의 `/data`)도 여기에 해당합니다. 이런 디렉터리를 제거하거나 옮기면 하위 마운트가 연결될 위치를 잃기 때문입니다. 마운트 지점은 `rmdir()`, `unlink()`, `rm()`으로 제거할 수 없고, `rename()`의 원본이나 대상으로도 쓸 수 없습니다. 이런 작업은 모두 `EBUSY`로 실패하며, 마운트 지점과 마운트 구성은 그대로 유지됩니다. 마운트 지점 **안의** 파일과 디렉터리는 평소처럼 제거하거나 이동할 수 있습니다.

## 오류 처리

파일 시스템 작업이 실패하면 Node.js와 같은 형식의 `Error` 객체를 던집니다.

| 속성 | 설명 |
| --- | --- |
| `code` | 오류 코드 문자열. 예: `ENOENT`, `EEXIST` |
| `errno` | 오류 번호(음수). 예: `-2` |
| `syscall` | 실패한 작업 이름. 예: `open`, `mkdir`, `rmdir` |
| `path` | 대상 경로. 파일 디스크립터 기반 함수(`read()`, `write()`, `close()`, `fstat()`, `fsync()` 등)의 오류에는 포함되지 않습니다. |
| `dest` | `rename()` 오류일 때 대상 경로 |

오류 메시지 형식은 `CODE: 설명, syscall 'path'`입니다. 예를 들어 `ENOENT: no such file or directory, open '/work/none.txt'`와 같습니다.

```js {linenos=table,linenostart=1}
const fs = require('fs');
try {
    fs.readFile('/work/none.txt');
} catch (e) {
    console.println(e.code, e.errno, e.syscall, e.path);
    // ENOENT -2 open /work/none.txt
}
```

<h6>주요 오류 코드</h6>

| 코드 | errno | 의미 |
| --- | --- | --- |
| `EPERM` | -1 | 허용되지 않은 작업 |
| `ENOENT` | -2 | 파일 또는 디렉터리가 없음 |
| `EIO` | -5 | 입출력 오류 |
| `EBADF` | -9 | 잘못된 파일 디스크립터. 닫혔거나 존재하지 않는 디스크립터, 또는 읽기 전용으로 연 디스크립터에 쓰는 경우 등 |
| `EACCES` | -13 | 권한 없음. 읽기 전용 마운트에 쓰는 경우 포함 |
| `EBUSY` | -16 | 리소스가 사용 중. 마운트 지점을 제거하거나 이동하려 할 때 발생 |
| `EEXIST` | -17 | 이미 존재함 |
| `EXDEV` | -18 | 서로 다른 마운트 사이의 이동 |
| `ENOTDIR` | -20 | 디렉터리가 아님 |
| `EISDIR` | -21 | 디렉터리에 허용되지 않는 작업 |
| `EINVAL` | -22 | 잘못된 인자 |
| `EFBIG` | -27 | 파일이 너무 큼. 메모리 기반·공유 파일 시스템의 1GiB 제한 초과 |
| `ENOSPC` | -28 | 저장 공간 부족 |
| `EROFS` | -30 | 읽기 전용 파일 시스템 |
| `ENAMETOOLONG` | -36 | 파일 이름이 너무 김 |
| `ENOTEMPTY` | -39 | 디렉터리가 비어 있지 않음 |
| `ELOOP` | -40 | 심볼릭 링크 단계가 너무 많음 |
| `ENOTSUP` | -95 | 지원하지 않는 작업 |
| `ECONFLICT` | -32009 | (JSH 전용) 공유 파일 시스템에서 디스크립터를 연 뒤 다른 프로세스가 같은 파일을 변경함 |

- `errno` 값은 실행 플랫폼과 관계없이 위 표의 값(Linux 기준)으로 고정됩니다. macOS나 Windows의 Node.js에서 보고되는 `errno` 숫자와 다를 수 있으므로, 오류 판별에는 `errno` 대신 `code`를 사용하세요.
- `offset`, `length`, `position`, `len`처럼 인자 범위가 잘못된 경우에는 `RangeError`를 던지며, `code`는 `ERR_OUT_OF_RANGE`이고 `errno`는 없습니다.
- 인자 타입이 잘못된 경우(예: `read()`의 `buffer`에 일반 배열이나 `writeFile()`의 `data`에 숫자를 전달)에는 `TypeError`를 던지며, `code`는 `ERR_INVALID_ARG_TYPE`이고 `errno`는 없습니다.
- 알 수 없는 인코딩 이름을 지정하면(`writeFile()`, `appendFile()`) `TypeError`를 던지며, `code`는 `ERR_UNKNOWN_ENCODING`입니다.

<h6>Windows에서의 오류 코드 차이</h6>

이 문서에 적힌 오류 코드는 Linux 기준입니다. 메모리 기반·내장·공유 파일 시스템은 JSH가 직접 판정하므로 모든 플랫폼에서 문서와 같은 코드를 반환합니다. 반면 Windows의 호스트 디렉터리 마운트에서는 운영체제가 반환한 오류를 Node.js(libuv)와 같은 방식으로 변환하므로, 다음과 같이 코드가 다를 수 있습니다.

| 상황 | Linux | Windows |
| --- | --- | --- |
| 경로 중간 구성 요소가 파일임 (예: `stat('/work/file.txt/child')`, `writeFile('/work/file.txt/x')`) | `ENOTDIR` | `ENOENT` |
| `rename()` 대상 경로의 중간 구성 요소가 파일임 (예: `rename('/work/a', '/work/file.txt/a')`) | `ENOTDIR` | 다른 코드(예: `EBUSY`, `EIO`) |
| 디렉터리를 자기 하위 경로로 `rename()` | `EINVAL` | `EPERM` |
| 다른 프로세스가 사용 중인 파일을 삭제하거나 이동 | 성공 | `EBUSY` 또는 `EPERM` |
| 읽기 전용 속성 파일에 `access(W_OK)` | `EACCES` | `EPERM` |

여러 플랫폼에서 실행되는 스크립트는 특정 코드 하나에 의존하기보다 실패 여부를 기준으로 처리하는 것이 안전합니다.

## readFile()

파일을 읽어 문자열(기본: `utf8`) 또는 `Buffer`로 반환합니다.

<h6>사용 형식</h6>

```js
readFile(path[, options])
```

- `options`는 인코딩 문자열 또는 `{ encoding }` 객체입니다. `'buffer'` 또는 `{ encoding: null }`을 지정하면 `Buffer`를 반환합니다.
- 파일 전체를 메모리로 읽습니다. 큰 파일은 `createReadStream()` 또는 `open()`/`read()`로 나누어 읽으세요.

<h6>주의사항</h6>

- **Node.js와 달리 `options`를 생략하면 `Buffer`가 아니라 UTF-8 문자열을 반환합니다.** 바이너리 데이터는 반드시 `'buffer'` 또는 `{ encoding: null }`을 지정해 읽으세요.
- 반환되는 `Buffer`는 `Uint8Array`이므로 인덱스 접근, `length`, `slice()`, `subarray()`, `map()` 등을 그대로 사용할 수 있습니다. Node.js와 같이 `slice()`는 복사본이 아니라 원본과 메모리를 공유하는 `Buffer`를 반환합니다. 일반 배열이 아니므로 `Array.isArray()`는 `false`이고, `concat()` 등 배열 전용 메서드는 없으며, `JSON.stringify()` 결과도 숫자 배열이 아닙니다. 배열이 필요하면 `Array.from(buf)`로 변환하세요.
- 문자열로 읽을 때는 현재 UTF-8로만 디코딩합니다. `'hex'`, `'base64'` 등을 지정해도 UTF-8 문자열을 반환하므로, 이런 형식이 필요하면 `Buffer`로 읽은 뒤 `buf.toString('hex')`처럼 변환하세요.
- 바이너리 파일을 복사할 때는 `writeFile(dst, readFile(src, 'buffer'))`처럼 `Buffer` 그대로 전달하면 바이트가 보존됩니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const content = fs.readFile('/lib/fs.js', 'utf8');
console.println(content.length);
```

## writeFile()

파일에 데이터를 씁니다. 파일이 없으면 생성하고, 있으면 덮어씁니다.

<h6>사용 형식</h6>

```js
writeFile(path, data[, options])
```

- `data`: 문자열, `Buffer`, `Uint8Array` 등의 TypedArray 또는 `DataView`. 이 밖의 값(숫자, `null`, `undefined`, `toString()`을 가진 객체 등)을 전달하면 Node.js와 같이 `TypeError`(`ERR_INVALID_ARG_TYPE`)를 던지고 파일은 만들거나 바꾸지 않습니다.
  - (JSH 확장) `ArrayBuffer`와 바이트 값의 숫자 배열(예: `[65, 66]`)도 받습니다. `zlib`, `archive/zip`, `archive/tar`, `mqtt` 등이 반환하는 `ArrayBuffer`나 `http` 응답의 `readBodyBuffer()` 결과를 그대로 쓸 수 있습니다. 숫자 배열의 각 요소는 `Uint8Array.from()`과 같이 하위 8비트만 사용합니다. Node.js는 두 타입 모두 거부하므로 Node.js와 함께 쓰는 코드라면 `Buffer`나 `Uint8Array`로 변환해 전달하세요.
  - `Int16Array`처럼 요소가 1바이트보다 큰 TypedArray나 `DataView`는 메모리상의 바이트를 그대로 씁니다.
- `options`: 인코딩 문자열 또는 `{ encoding }` 객체. 인코딩은 `data`가 문자열일 때만 사용하며 기본값은 `'utf8'`입니다.
  - 지원 인코딩: `'utf8'`(`'utf-8'`), `'hex'`, `'base64'`, `'base64url'`, `'latin1'`(`'binary'`), `'ascii'`, `'utf16le'`(`'ucs2'`, `'ucs-2'`, `'utf-16le'`). 대소문자를 구분하지 않습니다.
  - `'buffer'`와 `null`은 JSH 관례로 허용하며 문자열을 UTF-8로 씁니다.
  - 그 밖의 이름은 `TypeError`(`ERR_UNKNOWN_ENCODING`)를 던집니다.
- 상위 디렉터리가 없으면 `ENOENT`로 실패합니다. 필요하면 먼저 `mkdir(dir, { recursive: true })`를 호출하세요.
- 메모리 기반 마운트와 공유 파일 시스템에서는 1GiB를 넘는 파일을 쓸 수 없습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
fs.writeFile('/work/data.bin', Uint8Array.from([0x89, 0x50, 0x4e, 0x47]));
fs.writeFile('/work/hex.bin', '89504e47', 'hex');   // same 4 bytes
```

## appendFile()

파일 끝에 데이터를 추가합니다. 파일이 없으면 새로 생성합니다.

<h6>사용 형식</h6>

```js
appendFile(path, data[, options])
```

- `data`와 `options`의 규칙은 `writeFile()`과 같습니다. 허용되지 않는 타입이면 `TypeError`(`ERR_INVALID_ARG_TYPE`)를 던지고 파일은 바꾸지 않습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFile('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLines()

파일의 줄 수(개행 기준)를 계산합니다. JSH 전용 함수입니다.

<h6>사용 형식</h6>

```js
countLines(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.countLines('/work/append.txt'));
```

## exists()

파일 또는 디렉터리의 존재 여부를 `true`/`false`로 반환합니다.

<h6>사용 형식</h6>

```js
exists(path)
```

- 심볼릭 링크는 따라가서 확인합니다. 대상이 없는 링크(끊어진 링크)는 `false`를 반환합니다. 링크 자체의 존재를 확인하려면 `lstat()`를 사용하세요.
- 권한 부족 등 다른 이유로 확인할 수 없는 경우에도 `false`를 반환합니다. 실패 원인이 필요하면 `access()` 또는 `stat()`를 사용하세요.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.exists('/work/test.txt'));
console.println(fs.exists('/work/not-found.txt'));
```

## stat()

파일 또는 디렉터리 메타데이터를 반환합니다. 경로가 심볼릭 링크이면 링크가 가리키는 대상의 정보를 반환합니다.

<h6>사용 형식</h6>

```js
stat(path)
```

<h6>반환 필드</h6>

- `name`: 파일 이름(경로를 제외한 마지막 구성 요소)
- `size`: 바이트 단위 크기
- `mode`: 파일 모드 객체. `String(st.mode)`는 `drwxr-xr-x`와 같은 문자열을 반환합니다.
- `mtime`, `atime`, `ctime`, `birthtime`: 현재 구현에서는 모두 수정 시각(`mtime`)과 같은 값입니다.
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat()

파일 메타데이터를 반환합니다. `stat()`와 달리 경로의 마지막 구성 요소가 심볼릭 링크이면 링크를 따라가지 않고 링크 자체의 정보를 반환합니다. 반환 필드는 `stat()`와 같습니다. 중첩 마운트 때문에 생긴 중간 디렉터리는 `stat()`과 같이 디렉터리로 조회됩니다.

<h6>사용 형식</h6>

```js
lstat(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/target.txt', 'data');
fs.symlink('target.txt', '/work/link.txt');
console.println(fs.lstat('/work/link.txt').isSymbolicLink()); // true
console.println(fs.stat('/work/link.txt').isFile());          // true
```

## readdir()

디렉터리 항목을 읽습니다.

- 기본값: 항목 이름의 `string[]`을 반환합니다.
- `withFileTypes: true`: `name`과 타입 메서드(`isFile()`, `isDirectory()`, `isSymbolicLink()` 등)를 가진 엔트리 객체를 반환합니다.
- `recursive: true`: 하위 디렉터리를 포함해 재귀적으로 반환합니다.

<h6>사용 형식</h6>

```js
readdir(path[, options])
```

<h6>주의사항</h6>

- **비재귀 조회에서는 `.`와 `..` 항목이 결과에 포함됩니다.** Node.js와 다른 동작이므로 디렉터리를 순회할 때는 반드시 두 항목을 건너뛰어야 합니다. 건너뛰지 않으면 같은 디렉터리를 무한히 재귀할 수 있습니다.
- 재귀 조회(`recursive: true`)에서는 `.`와 `..`가 포함되지 않습니다.
  - 문자열 결과는 시작 디렉터리 기준의 상대 경로(예: `a/b/file.txt`)입니다.
  - 엔트리 객체의 `path` 속성은 항목이 속한 디렉터리의 상대 경로이며, 시작 디렉터리 바로 아래 항목은 `''`입니다. Node.js의 `Dirent.path`(부모 디렉터리의 전체 경로)와 다릅니다.
- 재귀 조회는 디렉터리를 가리키는 심볼릭 링크 안으로 들어가지 않습니다. 링크는 항목으로만 반환됩니다.
- 재귀 조회 도중 하위 디렉터리를 읽지 못하면(권한 부족 등) 조회 전체가 오류로 실패합니다. 오류 객체의 `path`는 실패한 하위 디렉터리를 가리킵니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const names = fs.readdir('/lib').filter(n => n !== '.' && n !== '..');
const all = fs.readdir('/work', { recursive: true });
console.println(names.length, all.length);
```

## mkdir()

디렉터리를 생성합니다.

<h6>사용 형식</h6>

```js
mkdir(path[, options])
```

<h6>옵션</h6>

- `recursive`: `true`이면 없는 상위 디렉터리를 함께 생성하고, 이미 존재하는 디렉터리는 오류 없이 넘어갑니다. 기본값은 `false`입니다.
- `mode`: 생성할 디렉터리의 권한입니다. 기본값은 `0o755`이며, 재귀 생성 시 새로 만드는 모든 디렉터리에 적용됩니다. 호스트 디렉터리에서는 운영체제의 umask가 추가로 적용될 수 있습니다.

<h6>동작</h6>

- 비재귀 호출(`recursive: false`)
  - 상위 디렉터리가 없으면 `ENOENT`로 실패합니다. 상위 디렉터리를 자동으로 만들지 않습니다.
  - 대상이 이미 존재하면 디렉터리이든 파일이든 `EEXIST`로 실패합니다.
- 재귀 호출(`recursive: true`)
  - 경로 중간에 같은 이름의 **파일**이 있으면 `EEXIST`로 실패합니다. Node.js는 이 경우 `ENOTDIR`을 반환합니다.
  - 반환값은 항상 `undefined`입니다. Node.js처럼 처음 생성된 경로를 반환하지 않습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
fs.mkdir('/work/private', { mode: 0o700 });
```

## rmdir()

비어 있는 디렉터리를 제거합니다.

<h6>사용 형식</h6>

```js
rmdir(path[, options])
```

- 디렉터리가 비어 있지 않으면 `ENOTEMPTY`, 대상이 파일이나 심볼릭 링크이면 `ENOTDIR`로 실패합니다.
- `{ recursive: true }`를 지정하면 하위 항목을 먼저 모두 제거합니다. Node.js에서는 사용 중단(deprecated)된 옵션이므로 새 코드에서는 `rm(path, { recursive: true })` 사용을 권장합니다.
- 재귀 제거 시 하위 항목 중 디렉터리를 가리키는 심볼릭 링크는 링크만 제거하며, 링크 대상의 내용은 삭제하지 않습니다.
- `path` 자체가 심볼릭 링크이면 `recursive`를 지정해도 링크를 따라가지 않고 `ENOTDIR`로 실패합니다. 링크와 링크 대상은 모두 그대로 유지됩니다. 링크 자체를 제거하려면 `unlink()` 또는 `rm()`을 사용하세요.
- 마운트 지점을 지정하면 `EBUSY`로 실패합니다. 재귀 제거에서 마운트 지점을 만났을 때의 동작은 [rm()](#rm)과 같습니다.

## rm()

파일, 심볼릭 링크 또는 디렉터리를 제거합니다.

<h6>사용 형식</h6>

```js
rm(path[, options])
```

<h6>옵션</h6>

- `recursive`: `true`이면 디렉터리와 그 내용을 모두 제거합니다.
- `force`: `true`이면 대상이 존재하지 않을 때(`ENOENT`) 오류를 무시합니다.

<h6>주의사항</h6>

- 대상 유형은 `lstat()`로 판별합니다. 심볼릭 링크는 가리키는 대상이 디렉터리이더라도 **링크 자체만** 제거되며, 대상 디렉터리와 그 내용은 보존됩니다.
- `recursive` 없이 디렉터리를 지정하면 비어 있는 디렉터리만 제거됩니다. 비어 있지 않으면 `ENOTEMPTY`로 실패합니다.
- `force: true`는 `ENOENT`만 무시합니다. 권한 부족(`EACCES`), 입출력 오류(`EIO`) 등 다른 오류는 그대로 던집니다. 마운트 지점에서 발생하는 `EBUSY`도 무시하지 않습니다.
- 재귀 제거 도중 오류가 발생하면 즉시 중단됩니다. 이때 이미 제거된 항목은 복구되지 않으므로 일부만 삭제된 상태로 남을 수 있습니다.
- 마운트 지점은 예외적으로 처리합니다. 대상 자체나 그 하위에 있는 마운트 지점은 내용만 모두 제거되고, 빈 디렉터리로 남습니다. 나머지 항목은 계속 제거하며, 모든 항목을 처리한 뒤 처음 만난 마운트 지점의 경로로 `EBUSY`를 던집니다. Linux에서 마운트된 디렉터리를 `rm -r`로 지울 때와 같은 결과입니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.rm('/work/a', { recursive: true, force: true });
```

## unlink()

파일 또는 심볼릭 링크를 제거합니다.

<h6>사용 형식</h6>

```js
unlink(path)
```

- 디렉터리에는 사용할 수 없으며 `EISDIR`로 실패합니다. 디렉터리는 `rmdir()` 또는 `rm()`을 사용하세요.
- 심볼릭 링크를 지정하면 링크만 제거되고 대상 파일은 유지됩니다.
- 마운트 지점을 지정하면 `EBUSY`로 실패합니다.
- Windows에서는 읽기 전용 속성의 파일도 제거합니다.

{{< callout emoji="📌" >}}
`unlink()`, `rmdir()`, `rm()`, `rename()`으로 마지막 항목을 제거하거나 옮겨도 상위 디렉터리는 그대로 남습니다. 메모리 기반 마운트와 공유 파일 시스템도 같은 방식으로 동작합니다.
{{< /callout >}}

## rename()

같은 마운트 안에서 파일 또는 디렉터리의 이름을 변경하거나 이동합니다.

<h6>사용 형식</h6>

```js
rename(oldPath, newPath)
```

- 대상 경로에 파일이 있으면 운영체제의 `rename` 동작에 따라 덮어씁니다.
- 서로 다른 마운트 사이의 이동은 `EXDEV`로 실패합니다. 이 경우 오류 객체의 `dest` 속성에 대상 경로가 담깁니다.
- 원본이나 대상이 마운트 지점이면 `EBUSY`로 실패합니다.
- 디렉터리를 자기 자신의 하위 경로로 옮기면(예: `/work/a` → `/work/a/b`) `EINVAL`로 실패하며, 원본은 그대로 유지됩니다.
- 오류는 Linux의 `rename`과 같은 순서로 판정합니다. 원본이 없으면 `ENOENT`, 대상 경로의 상위에 파일이 있으면 `ENOTDIR`(파일을 자기 하위 경로로 옮기는 경우 포함), 대상의 상위 디렉터리가 없으면 `ENOENT`, 그다음에 자기 하위 경로 여부(`EINVAL`)를 확인합니다. 메모리 기반 마운트와 공유 파일 시스템도 같은 오류 코드를 반환합니다.

## copyFile()

단일 파일을 복사합니다.

<h6>사용 형식</h6>

```js
copyFile(src, dest[, flags])
```

- 기본적으로 대상 파일이 있으면 덮어씁니다.
- `flags`에 `constants.COPYFILE_EXCL`을 지정하면 대상 파일이 있을 때 `EEXIST`로 실패합니다.
- `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`는 무시되며 일반 복사를 수행합니다.
- 파일 내용만 복사합니다. 원본 파일의 권한과 수정 시각은 유지되지 않습니다.
- 파일 전체를 메모리로 읽은 뒤 쓰므로 매우 큰 파일 복사에는 적합하지 않습니다.

## cp()

파일 또는 디렉터리를 복사합니다.

<h6>사용 형식</h6>

```js
cp(src, dest[, options])
```

<h6>옵션</h6>

- `recursive`: 디렉터리를 복사하려면 `true`여야 합니다. 생략하면 디렉터리 복사는 `EISDIR`로 실패합니다.
- `force`: `true`이면 대상에 이미 있는 파일을 덮어씁니다.

<h6>주의사항</h6>

- **`force`의 기본값은 `false`입니다.** 대상 파일이 이미 있으면 `EEXIST`로 실패합니다. Node.js의 `cpSync()`는 기본적으로 덮어쓰므로 동작이 다릅니다.
- 원본의 심볼릭 링크는 따라가서 대상 내용을 복사합니다. 링크 자체는 복사하지 않습니다. 재귀 복사 중 디렉터리를 가리키는 링크를 만나면 일반 디렉터리로 복사하고, 파일을 가리키는 링크는 파일 내용을 복사합니다.
- 재귀 복사 중 링크를 따라갈 때 다음 경우는 실패합니다.
  - 링크가 지금 복사 중인 원본 디렉터리나 그 상위를 가리키면(순환 링크) `ELOOP`
  - 링크가 가리키는 디렉터리 안에 복사 대상 경로가 있으면 `ERR_FS_CP_EINVAL`
  - 링크 대상이 없으면(끊어진 링크) `ENOENT`
- 재귀 복사 도중 오류가 발생하면 즉시 중단됩니다. 이미 복사된 항목은 되돌리지 않으므로 일부만 복사된 상태로 남을 수 있습니다.
- 파일 내용만 복사하며, 권한과 수정 시각은 유지되지 않습니다.
- 원본과 대상이 같은 경로이거나, 디렉터리를 자기 자신의 하위 경로로 복사하면(예: `/work/a` → `/work/a/b`) 아무것도 만들지 않고 `ERR_FS_CP_EINVAL`로 실패합니다. 심볼릭 링크를 해석한 실제 경로로 비교하므로, 링크를 거쳐 지정해도 같은 결과입니다. 이 오류는 Node.js와 같은 코드를 사용하며 `errno` 속성은 없습니다.

## symlink()

심볼릭 링크를 생성합니다.

<h6>사용 형식</h6>

```js
symlink(target, path)
```

- `target`이 상대 경로이면 Node.js와 같이 **링크가 위치한 디렉터리를 기준으로** 해석되며, 상대 경로 형태 그대로 저장됩니다.
- `target`이 `/`로 시작하면 JSH 가상 경로로 취급됩니다.
- 링크의 대상이 마운트된 영역 밖을 가리키게 되면(예: `../../../etc/passwd`) `EACCES`로 실패합니다.
- Node.js의 세 번째 인자(`type`)는 지원하지 않습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/data', { recursive: true });
fs.writeFile('/work/data/v1.csv', 'a,b\n');
fs.symlink('v1.csv', '/work/data/current.csv');   // relative to /work/data
console.println(fs.readFile('/work/data/current.csv'));
```

## readlink()

심볼릭 링크의 대상 경로를 읽습니다.

<h6>사용 형식</h6>

```js
readlink(path)
```

- **반환값은 항상 해석이 끝난 절대 가상 경로입니다.** 링크가 상대 경로(`v1.csv`)로 저장되어 있어도 `/work/data/v1.csv`처럼 반환됩니다. 저장된 문자열을 그대로 반환하는 Node.js와 다릅니다.
- 심볼릭 링크가 아닌 경로에는 `EINVAL`을 던집니다.
- 링크가 마운트 영역 밖을 가리키면 `ENOENT`를 던집니다.

## realpath()

모든 심볼릭 링크와 `.`, `..`를 해석한 실제 경로를 반환합니다.

<h6>사용 형식</h6>

```js
realpath(path)
```

- 경로의 마지막 구성 요소뿐 아니라 중간 디렉터리의 심볼릭 링크도 해석합니다.
- 경로 구성 요소가 존재하지 않으면 `ENOENT`, 순환 링크 등으로 링크를 40번 넘게 따라가야 하면 `ELOOP`을 던집니다.
- 반환값은 JSH 가상 경로입니다.

## access()

경로가 존재하는지, 지정한 권한으로 접근할 수 있는지 확인합니다. 접근할 수 있으면 `undefined`를 반환하고, 그렇지 않으면 오류를 던집니다.

<h6>사용 형식</h6>

```js
access(path[, mode])
```

- `mode`는 `constants.F_OK`(존재, 기본값), `R_OK`(읽기), `W_OK`(쓰기), `X_OK`(실행)를 비트 OR로 조합합니다.
- 경로가 없으면 `ENOENT`, 권한이 없으면 `EACCES`, `mode`가 0~7 범위를 벗어나면 `EINVAL`을 던집니다.

<h6>주의사항</h6>

- 호스트 디렉터리 마운트에서는 운영체제의 권한 검사를 사용합니다.
- Windows 동작은 Node.js와 같습니다.
  - 읽기 전용 속성의 파일에 `W_OK`를 검사하면 `EPERM`을 던집니다.
  - `X_OK`는 존재 여부(`F_OK`)와 같게 취급됩니다.
- 메모리 기반·내장·공유 파일 시스템에서는 JSH 프로세스를 파일 소유자로 보고 파일 모드의 **소유자** 권한 비트로 판단합니다. 예를 들어 `0o600` 파일은 `R_OK`/`W_OK` 검사를 통과하고, `0o004` 파일은 `R_OK` 검사에 실패합니다. 그룹과 ACL은 고려하지 않습니다.
- 읽기 전용 마운트에서 `W_OK` 검사는 항상 실패합니다.
- 중첩 마운트 때문에 생긴 중간 디렉터리(예: `/a/b`만 마운트되었을 때의 `/a`)는 `stat()`과 마찬가지로 권한 `0o755`인 디렉터리로 판단하므로 `W_OK` 검사를 통과합니다. 하지만 상위 마운트에 해당 디렉터리가 실제로 없으면, 그 안에 파일이나 디렉터리를 만들 때 `ENOENT`로 실패합니다. `access()` 결과만으로 쓰기 성공을 보장할 수 없으므로 실제로 쓰기를 시도하고 오류를 처리하세요.
- `access()`로 확인한 뒤 파일을 여는 방식은 그 사이에 상태가 바뀔 수 있습니다. 가능하면 파일을 직접 열고 오류를 처리하세요.

<h6>사용 예시</h6>

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

파일 크기를 지정한 길이로 맞춥니다.

<h6>사용 형식</h6>

```js
truncate(path[, len])
```

- `len`을 생략하면 `0`으로 자릅니다.
- `len`이 현재 크기보다 작으면 앞의 `len` 바이트만 남깁니다.
- `len`이 현재 크기보다 크면 파일을 확장하고, 늘어난 부분은 `0` 바이트로 채웁니다.
- `len`이 음수이거나 정수가 아니면 `RangeError`(`ERR_OUT_OF_RANGE`)를 던집니다.
- 메모리 기반 마운트와 공유 파일 시스템에서 1GiB를 넘는 길이를 지정하면 `EFBIG`으로 실패하며, 파일은 변경되지 않습니다.

## open()

파일을 열고 숫자 파일 디스크립터를 반환합니다.

<h6>사용 형식</h6>

```js
open(path, flags[, mode])
```

- `flags`: 문자열 플래그 또는 `constants.O_*` 값을 조합한 숫자 플래그입니다.
- `mode`: 파일을 새로 만들 때 사용할 권한입니다. 기본값은 `0o666`입니다.

<h6>문자열 플래그</h6>

| 플래그 | 의미 |
| --- | --- |
| `r` | 읽기. 파일이 없으면 실패 |
| `r+` | 읽기/쓰기. 파일이 없으면 실패 |
| `w` | 쓰기. 없으면 생성, 있으면 내용을 비움 |
| `w+` | 읽기/쓰기. 없으면 생성, 있으면 내용을 비움 |
| `a` | 추가 쓰기. 없으면 생성 |
| `a+` | 읽기/추가 쓰기. 없으면 생성 |
| `wx`, `wx+`, `ax`, `ax+` | 위와 같되 파일이 이미 있으면 `EEXIST`로 실패 |

<h6>주의사항</h6>

- 위 표에 없는 문자열 플래그는 오류 없이 `r`(읽기 전용)로 처리됩니다. 오타가 있어도 오류가 나지 않고 이후 `write()`가 `EBADF`로 실패할 수 있으므로 플래그 문자열을 정확히 지정하세요.
- 메모리 기반 마운트(예: `/lib`)에서는 읽기용 디스크립터만 열 수 있습니다. 쓰기 플래그를 지정하면 `ENOTSUP`으로 실패하므로 `writeFile()`/`appendFile()`을 사용하세요.
- 읽기 전용(내장) 마운트에 쓰기 플래그로 열면 `EACCES`로 실패합니다.
- 사용한 디스크립터는 반드시 `close()`로 닫아야 합니다.

## close()

파일 디스크립터를 닫습니다.

<h6>사용 형식</h6>

```js
close(fd)
```

- 이미 닫혔거나 존재하지 않는 디스크립터는 `EBADF`로 실패합니다.
- 공유 파일 시스템에서는 닫는 시점에 변경 내용이 저장됩니다. 디스크립터를 연 뒤 다른 프로세스가 같은 파일을 변경했다면 `ECONFLICT`로 실패합니다.

## read()

파일 디스크립터에서 데이터를 읽어 버퍼에 채우고, 읽은 바이트 수를 반환합니다. 파일 끝에서는 `0`을 반환합니다.

<h6>사용 형식</h6>

```js
read(fd, buffer, offset, length[, position])
```

- `buffer`: 데이터를 받을 `Buffer`, `Uint8Array` 등의 TypedArray 또는 `DataView`. (JSH 확장) `ArrayBuffer`도 받으며, 읽은 데이터는 해당 `ArrayBuffer`에 직접 채워집니다. 일반 배열이나 문자열을 전달하면 Node.js와 같이 `TypeError`(`ERR_INVALID_ARG_TYPE`)를 던집니다.
- `offset`: 버퍼에서 쓰기 시작할 바이트 위치. 기본값은 `0`입니다.
- `length`: 읽을 최대 바이트 수. 기본값은 `buffer.byteLength - offset`입니다.
- `position`: 파일에서 읽기 시작할 위치
  - `null` 또는 생략: 현재 파일 위치에서 읽고, 읽은 만큼 현재 위치가 이동합니다.
  - 0 이상의 정수: 지정한 위치에서 읽으며, **현재 파일 위치는 바뀌지 않습니다.**

<h6>주의사항</h6>

- `offset`, `length`, `position`이 범위를 벗어나면 `RangeError`(`ERR_OUT_OF_RANGE`)를 던집니다. 예를 들어 `offset + length`가 버퍼 크기를 넘거나 `position`이 음수인 경우입니다.
- `Int16Array`처럼 요소가 1바이트보다 큰 TypedArray나 `DataView`를 전달해도 `offset`과 `length`는 요소 수가 아니라 **바이트** 단위로 해석합니다(Node.js와 같음).
- 쓰기 전용으로 연 디스크립터를 읽으면 `EBADF`로 실패합니다.
- Linux/macOS에서 디렉터리 디스크립터를 읽으면 `EISDIR`로 실패합니다. 디렉터리 내용은 `readdir()`로 읽으세요.

<h6>사용 예시</h6>

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

버퍼나 문자열 데이터를 파일 디스크립터에 쓰고, 쓴 바이트 수를 반환합니다. Node.js의 `fs.writeSync()`와 같이 데이터 종류에 따라 두 가지 형식을 사용합니다.

<h6>사용 형식</h6>

```js
write(fd, buffer[, offset[, length[, position]]])
write(fd, buffer[, options])
write(fd, string[, position[, encoding]])
write(fd, string, offset, length[, position])   // JSH legacy form
```

**버퍼 형식**

- `buffer`: `Buffer`, `Uint8Array` 등의 TypedArray 또는 `DataView`. (JSH 확장) `ArrayBuffer`와 바이트 값의 숫자 배열(예: `[65, 66]`)도 받습니다. Node.js는 둘 다 거부합니다.
- `offset`: `buffer`에서 쓰기 시작할 바이트 위치. 숫자가 아니면 `0`입니다.
- `length`: 쓸 바이트 수. 숫자가 아니면 `buffer.byteLength - offset`입니다. `0`을 지정하면 아무것도 쓰지 않습니다.
- `options`: `{ offset, length, position }` 객체. 세 번째 인자가 객체이거나 `null`이면 이 형식으로 해석합니다. 생략한 항목은 위의 기본값을 따릅니다.

**문자열 형식**

- `string`: 쓸 문자열.
- 세 번째 인자는 `offset`이 아니라 **`position`** 입니다.
- `encoding`: 문자열을 바이트로 바꿀 인코딩. 기본값은 `'utf8'`이며 지원 인코딩은 `writeFile()`과 같습니다. Node.js와 같이 알 수 없는 인코딩 이름은 `'utf8'`로 처리합니다.

**문자열 형식 (JSH 이전 형식)**

- 이전 버전 JSH 코드와의 호환을 위해, **네 번째 인자가 숫자이면** `write(fd, string, offset, length[, position])`으로 해석합니다. 문자열을 UTF-8 바이트로 바꾼 뒤 버퍼 형식과 같은 규칙으로 `offset`과 `length`(바이트 단위)를 적용합니다. `offset`이 숫자가 아니면 `0`입니다.
- Node.js에서는 네 번째 인자가 인코딩 이름이므로 이 형식이 쓰이지 않습니다. 새로 작성하는 코드는 `write(fd, Buffer.from(str), offset, length, position)`을 사용하세요.

**공통**

- `position`: 파일에서 쓰기 시작할 위치
  - 숫자가 아닌 값(`null`, 생략 등): 현재 파일 위치에 쓰고, 쓴 만큼 현재 위치가 이동합니다.
  - 0 이상의 정수: 지정한 위치에 쓰며, **현재 파일 위치는 바뀌지 않습니다.** 위치가 파일 끝보다 뒤이면 그 사이는 `0` 바이트로 채워집니다.

<h6>주의사항</h6>

- **문자열을 쓸 때 인자가 세 개 이하이거나 네 번째 인자가 인코딩이면 세 번째 인자는 파일 위치입니다.** 예를 들어 `write(fd, 'Z', 3)`은 파일의 3번째 바이트 위치에 `Z`를 씁니다. 이전 버전 JSH에서 `write(fd, str, offset)`처럼 세 번째 인자를 문자열 내 offset으로 쓰던 코드는 동작이 달라지므로 `write(fd, Buffer.from(str), offset)`으로 바꾸세요.
- 숫자, 일반 객체, `null` 등을 전달하면 Node.js와 같이 `TypeError`(`ERR_INVALID_ARG_TYPE`)를 던집니다.
- `Int16Array`처럼 요소가 1바이트보다 큰 TypedArray나 `DataView`도 `offset`과 `length`를 요소 수가 아니라 바이트 단위로 해석합니다(Node.js와 같음).
- `'hex'` 인코딩으로 길이가 홀수인 문자열을 쓰면 `TypeError`(`ERR_INVALID_ARG_VALUE`)를 던집니다.
- `a`, `a+` 등 추가 모드로 연 디스크립터는 `position`을 지정해도 무시하고 항상 파일 끝에 씁니다.
- `offset`, `length`가 버퍼 범위를 벗어나거나 `position`이 음수 또는 정수가 아닌 숫자이면 `RangeError`(`ERR_OUT_OF_RANGE`)를 던집니다. 음수 `position`을 거부하는 것은 JSH 동작이며, Node.js는 현재 위치에 씁니다.
- 읽기 전용으로 연 디스크립터에 쓰면 `EBADF`로 실패합니다.
- 공유 파일 시스템에서 쓴 결과가 1GiB를 넘으면 `EFBIG`으로 실패합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const fd = fs.open('/work/out.txt', 'w+');
fs.write(fd, 'Hello World');                // write at the current position
fs.write(fd, 'J', 0);                       // overwrite the first byte: "Jello World"
const bytes = new Uint8Array([0x21, 0x21]);
fs.write(fd, bytes, 0, bytes.length);       // append "!!" at the current position
fs.write(fd, Buffer.from('xyz'), { offset: 1, length: 1, position: 1 }); // "Jyllo World!!"
fs.write(fd, '2a', 2, 'hex');               // write 0x2a ('*') at position 2: "Jy*lo World!!"
fs.close(fd);
```

## fstat()

파일 디스크립터의 메타데이터를 반환합니다.

<h6>사용 형식</h6>

```js
fstat(fd)
```

- 반환 객체는 `name`, `size`, `mode`, `mtime`과 타입 메서드(`isFile()` 등)를 제공합니다. `atime`, `ctime`, `birthtime`은 포함되지 않습니다.

## fchmod(), fchown()

파일 디스크립터 기준으로 모드/소유자를 변경합니다.

<h6>사용 형식</h6>

```js
fchmod(fd, mode)
fchown(fd, uid, gid)
```

- Windows 호스트 디렉터리에서 연 파일 디스크립터에서는 아무 작업도 하지 않고 성공합니다.
- 그 밖의 마운트에서는 해당 파일 시스템의 동작을 따릅니다. 예를 들어 읽기 전용(내장) 마운트의 디스크립터에는 `EACCES`를 던집니다.

## fsync(), fdatasync()

대기 중인 파일 데이터를 저장소로 동기화합니다.

<h6>사용 형식</h6>

```js
fsync(fd)
fdatasync(fd)
```

- 현재 `fdatasync()`는 `fsync()`와 같게 동작합니다.
- 읽기 전용(내장) 마운트에서 연 디스크립터와 메모리 기반 마운트(예: `/lib`)의 읽기용 디스크립터는 동기화할 대상이 없으므로 `ENOTSUP`을 던집니다. Node.js와 다른 동작입니다.
- 공유 파일 시스템에서 디스크립터를 연 뒤 다른 프로세스가 같은 파일을 변경했다면 `ECONFLICT`로 실패합니다.

## chmod(), chown()

경로 기준으로 모드/소유자를 변경합니다.

Windows 호스트 디렉터리에서는 `chmod`/`chown`이 no-op 호환 동작입니다. 메모리 기반·내장·공유 파일 시스템에서는 해당 파일 시스템의 동작을 따릅니다.

<h6>사용 형식</h6>

```js
chmod(path, mode)
chown(path, uid, gid)
```

## createReadStream(), createWriteStream()

EventEmitter 기반 사용과 호환되는 스트림 객체를 생성합니다.

<h6>사용 형식</h6>

```js
createReadStream(path[, options])
createWriteStream(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const rs = fs.createReadStream('/work/in.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/out.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## platform(), arch()

런타임 플랫폼과 아키텍처 문자열을 반환합니다.

<h6>사용 형식</h6>

```js
platform()
arch()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.platform());
console.println(fs.arch());
```

## constants

접근, 복사, 파일 열기 플래그를 담은 상수 객체입니다.

<h6>주요 필드</h6>

- 접근: `F_OK`(0), `R_OK`(4), `W_OK`(2), `X_OK`(1)
- 복사: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- 파일 열기: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

파일 열기 상수의 실제 값은 실행 플랫폼에 따라 다를 수 있으므로 숫자를 직접 쓰지 말고 상수를 사용하세요.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.access('/work/test.txt', fs.constants.F_OK);
const fd = fs.open('/work/new.txt', fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL);
fs.close(fd);
```

## Aliases

가독성을 위해 이 문서에서는 non-`Sync` 이름으로 API를 소개합니다.

Node.js 호환을 위해 `Sync` 접미사 형태도 별칭으로 함께 제공합니다. 두 이름은 같은 함수이며 모두 동기 방식으로 동작합니다. 콜백이나 Promise 기반 API는 제공하지 않습니다.

예: `readFileSync`, `writeFileSync`, `appendFileSync`, `readdirSync`, `mkdirSync`, `rmSync`, `statSync`, `openSync`, `closeSync`, `readSync`, `writeSync`, `fstatSync`, `fsyncSync`, `fdatasyncSync`.


## Examples

### Example 1: JSON 파일 읽기 및 파싱

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

### Example 2: 로그 파일 쓰기

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

### Example 3: 디렉터리 트리 순회

비재귀 `readdir()` 결과에는 `.`와 `..`가 포함되므로 반드시 건너뛰어야 합니다.

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

간단히 모든 경로만 필요하다면 `recursive` 옵션을 사용할 수 있습니다.

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.readdir('/tmp', { recursive: true }).forEach(p => console.println(p));
```

### Example 4: 파일 백업

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

### Example 5: 안전한 파일 쓰기

임시 파일에 먼저 쓰고 `rename()`으로 교체합니다. `rename()`은 같은 마운트 안에서만 동작하므로 임시 파일은 대상 파일과 같은 디렉터리에 만듭니다.

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

### Example 6: 오류 코드에 따른 처리

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
