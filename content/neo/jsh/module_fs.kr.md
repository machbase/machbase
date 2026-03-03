---
title: "fs"
type: docs
weight: 4
---

{{< neo_since ver="8.0.73" />}}

`fs` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 동기 파일 시스템 API를 제공합니다.

## readFileSync()

파일을 읽어 문자열(기본: `utf8`) 또는 바이트 배열로 반환합니다.

<h6>사용 형식</h6>

```js
readFileSync(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
const content = fs.readFileSync('/lib/fs/index.js', 'utf8');
console.println(content.length);
```

## writeFileSync()

파일에 데이터를 씁니다. 파일이 없으면 생성하고, 있으면 덮어씁니다.

<h6>사용 형식</h6>

```js
writeFileSync(path, data[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.writeFileSync('/work/test.txt', 'Hello', 'utf8');
```

## appendFileSync()

파일 끝에 데이터를 추가합니다. 파일이 없으면 새로 생성합니다.

<h6>사용 형식</h6>

```js
appendFileSync(path, data[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const fs = require('fs');
fs.writeFileSync('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFileSync('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLinesSync()

파일의 줄 수(개행 기준)를 계산합니다.

<h6>사용 형식</h6>

```js
countLinesSync(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
console.println(fs.countLinesSync('/work/append.txt'));
```

## existsSync()

파일 또는 디렉터리의 존재 여부를 `true`/`false`로 반환합니다.

<h6>사용 형식</h6>

```js
existsSync(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
console.println(fs.existsSync('/work/test.txt'));
console.println(fs.existsSync('/work/not-found.txt'));
```

## statSync()

파일 또는 디렉터리 메타데이터를 반환합니다.

<h6>사용 형식</h6>

```js
statSync(path)
```

<h6>반환 필드</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const fs = require('fs');
const st = fs.statSync('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstatSync()

파일 메타데이터를 반환합니다. 현재 구현에서는 `statSync()`와 동일하게 동작합니다.

<h6>사용 형식</h6>

```js
lstatSync(path)
```

## readdirSync()

디렉터리 항목을 읽습니다.

- 기본값: `string[]` 반환
- `withFileTypes: true`: `name`과 타입 메서드를 가진 엔트리 객체 반환
- `recursive: true`: 하위 디렉터리를 포함해 재귀적으로 반환

현재 런타임의 디렉터리 목록에는 `.`와 `..` 항목이 포함됩니다.

<h6>사용 형식</h6>

```js
readdirSync(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
const names = fs.readdirSync('/lib');
const entries = fs.readdirSync('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdirSync()

디렉터리를 생성합니다. 재귀 생성 옵션을 지원합니다.

<h6>사용 형식</h6>

```js
mkdirSync(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.mkdirSync('/work/a/b/c', { recursive: true });
```

## rmdirSync()

디렉터리를 제거합니다. `{ recursive: true }`를 지정하면 하위 항목을 먼저 제거합니다.

<h6>사용 형식</h6>

```js
rmdirSync(path[, options])
```

## rmSync()

파일 또는 디렉터리를 제거합니다.

- 디렉터리 제거는 내부적으로 `rmdirSync()`를 사용합니다.
- `force: true`를 지정하면 오류를 무시합니다.

<h6>사용 형식</h6>

```js
rmSync(path[, options])
```

## unlinkSync()

파일을 제거합니다.

<h6>사용 형식</h6>

```js
unlinkSync(path)
```

## renameSync()

같은 mount 파일시스템 내에서 파일/디렉터리 이름을 변경하거나 이동합니다.

<h6>사용 형식</h6>

```js
renameSync(oldPath, newPath)
```

## copyFileSync()

단일 파일을 복사합니다.

`COPYFILE_EXCL` 플래그를 사용하면 대상 파일이 있을 때 실패합니다.

<h6>사용 형식</h6>

```js
copyFileSync(src, dest[, flags])
```

## cpSync()

파일 또는 디렉터리를 복사합니다.

디렉터리 복사는 `{ recursive: true }`가 필요합니다.

<h6>사용 형식</h6>

```js
cpSync(src, dest[, options])
```

## symlinkSync()

심볼릭 링크를 생성합니다.

<h6>사용 형식</h6>

```js
symlinkSync(target, path)
```

## readlinkSync()

심볼릭 링크의 대상 경로를 읽습니다.

<h6>사용 형식</h6>

```js
readlinkSync(path)
```

## realpathSync()

심볼릭 링크 해석 동작을 반영한 실제 경로를 반환합니다.

<h6>사용 형식</h6>

```js
realpathSync(path)
```

## accessSync()

경로 접근 가능 여부를 확인합니다.

- 경로가 없으면 `ENOENT` 예외를 발생시킵니다.
- 모드 상수 `F_OK`, `R_OK`, `W_OK`, `X_OK`를 지원합니다.

<h6>사용 형식</h6>

```js
accessSync(path[, mode])
```

## truncateSync()

파일 내용을 잘라냅니다.

- 길이를 생략하면 `0`으로 자릅니다.
- 길이를 지정하면 앞의 `len` 바이트만 유지합니다.

<h6>사용 형식</h6>

```js
truncateSync(path[, len])
```

## openSync()

파일을 열고 숫자 파일 디스크립터를 반환합니다.

`r`, `r+`, `w`, `w+`, `a`, `a+`, `wx`, `wx+`, `ax`, `ax+` 문자열 플래그를 지원합니다.

<h6>사용 형식</h6>

```js
openSync(path, flags[, mode])
```

## closeSync()

파일 디스크립터를 닫습니다.

<h6>사용 형식</h6>

```js
closeSync(fd)
```

## readSync()

파일 디스크립터에서 버퍼로 데이터를 읽습니다.

<h6>사용 형식</h6>

```js
readSync(fd, buffer, offset, length[, position])
```

## writeSync()

문자열 또는 버퍼 데이터를 파일 디스크립터에 씁니다.

<h6>사용 형식</h6>

```js
writeSync(fd, buffer, offset, length[, position])
```

## fstatSync()

파일 디스크립터 기준 메타데이터를 반환합니다.

<h6>사용 형식</h6>

```js
fstatSync(fd)
```

## fchmodSync(), fchownSync()

파일 디스크립터 기준으로 모드/소유자를 변경합니다.

<h6>사용 형식</h6>

```js
fchmodSync(fd, mode)
fchownSync(fd, uid, gid)
```

## fsyncSync(), fdatasyncSync()

대기 중인 파일 데이터를 저장소로 동기화합니다.

현재 `fdatasyncSync()`는 `fsyncSync()`와 동일하게 동작합니다.

<h6>사용 형식</h6>

```js
fsyncSync(fd)
fdatasyncSync(fd)
```

## chmodSync(), chownSync()

경로 기준으로 모드/소유자를 변경합니다.

현재 런타임 구현에서 Windows에서는 `chmod`/`chown`이 no-op 호환 동작입니다.

<h6>사용 형식</h6>

```js
chmodSync(path, mode)
chownSync(path, uid, gid)
```

## createReadStream(), createWriteStream()

EventEmitter 기반 사용과 호환되는 스트림 객체를 생성합니다.

<h6>사용 형식</h6>

```js
createReadStream(path[, options])
createWriteStream(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
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

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
console.println(fs.platform());
console.println(fs.arch());
```

## constants

접근, 복사, 파일 열기 플래그를 담은 상수 객체입니다.

<h6>주요 필드</h6>

- 접근: `F_OK`, `R_OK`, `W_OK`, `X_OK`
- 복사: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- 파일 열기: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.accessSync('/work/test.txt', fs.constants.F_OK);
```

## Aliases

Node.js 호환을 위해 non-`Sync` 별칭도 함께 제공합니다.

예: `readFile`, `writeFile`, `appendFile`, `readdir`, `mkdir`, `rm`, `stat`, `open`, `close`, `read`, `write`, `fstat`, `fsync`, `fdatasync`.
