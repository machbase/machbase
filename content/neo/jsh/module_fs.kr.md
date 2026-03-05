---
title: "fs"
type: docs
weight: 4
---

{{< neo_since ver="8.0.73" />}}

`fs` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 동기 파일 시스템 API를 제공합니다.

## readFile()

파일을 읽어 문자열(기본: `utf8`) 또는 바이트 배열로 반환합니다.

<h6>사용 형식</h6>

```js
readFile(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
const content = fs.readFile('/lib/fs/index.js', 'utf8');
console.println(content.length);
```

## writeFile()

파일에 데이터를 씁니다. 파일이 없으면 생성하고, 있으면 덮어씁니다.

<h6>사용 형식</h6>

```js
writeFile(path, data[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile()

파일 끝에 데이터를 추가합니다. 파일이 없으면 새로 생성합니다.

<h6>사용 형식</h6>

```js
appendFile(path, data[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const fs = require('fs');
fs.writeFile('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFile('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLines()

파일의 줄 수(개행 기준)를 계산합니다.

<h6>사용 형식</h6>

```js
countLines(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
console.println(fs.countLines('/work/append.txt'));
```

## exists()

파일 또는 디렉터리의 존재 여부를 `true`/`false`로 반환합니다.

<h6>사용 형식</h6>

```js
exists(path)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
console.println(fs.exists('/work/test.txt'));
console.println(fs.exists('/work/not-found.txt'));
```

## stat()

파일 또는 디렉터리 메타데이터를 반환합니다.

<h6>사용 형식</h6>

```js
stat(path)
```

<h6>반환 필드</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4]}
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat()

파일 메타데이터를 반환합니다. 현재 구현에서는 `stat()`와 동일하게 동작합니다.

<h6>사용 형식</h6>

```js
lstat(path)
```

## readdir()

디렉터리 항목을 읽습니다.

- 기본값: `string[]` 반환
- `withFileTypes: true`: `name`과 타입 메서드를 가진 엔트리 객체 반환
- `recursive: true`: 하위 디렉터리를 포함해 재귀적으로 반환

현재 런타임의 디렉터리 목록에는 `.`와 `..` 항목이 포함됩니다.

<h6>사용 형식</h6>

```js
readdir(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const fs = require('fs');
const names = fs.readdir('/lib');
const entries = fs.readdir('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdir()

디렉터리를 생성합니다. 재귀 생성 옵션을 지원합니다.

<h6>사용 형식</h6>

```js
mkdir(path[, options])
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
```

## rmdir()

디렉터리를 제거합니다. `{ recursive: true }`를 지정하면 하위 항목을 먼저 제거합니다.

<h6>사용 형식</h6>

```js
rmdir(path[, options])
```

## rm()

파일 또는 디렉터리를 제거합니다.

- 디렉터리 제거는 내부적으로 `rmdir()`를 사용합니다.
- `force: true`를 지정하면 오류를 무시합니다.

<h6>사용 형식</h6>

```js
rm(path[, options])
```

## unlink()

파일을 제거합니다.

<h6>사용 형식</h6>

```js
unlink(path)
```

## rename()

같은 mount 파일시스템 내에서 파일/디렉터리 이름을 변경하거나 이동합니다.

<h6>사용 형식</h6>

```js
rename(oldPath, newPath)
```

## copyFile()

단일 파일을 복사합니다.

`COPYFILE_EXCL` 플래그를 사용하면 대상 파일이 있을 때 실패합니다.

<h6>사용 형식</h6>

```js
copyFile(src, dest[, flags])
```

## cp()

파일 또는 디렉터리를 복사합니다.

디렉터리 복사는 `{ recursive: true }`가 필요합니다.

<h6>사용 형식</h6>

```js
cp(src, dest[, options])
```

## symlink()

심볼릭 링크를 생성합니다.

<h6>사용 형식</h6>

```js
symlink(target, path)
```

## readlink()

심볼릭 링크의 대상 경로를 읽습니다.

<h6>사용 형식</h6>

```js
readlink(path)
```

## realpath()

심볼릭 링크 해석 동작을 반영한 실제 경로를 반환합니다.

<h6>사용 형식</h6>

```js
realpath(path)
```

## access()

경로 접근 가능 여부를 확인합니다.

- 경로가 없으면 `ENOENT` 예외를 발생시킵니다.
- 모드 상수 `F_OK`, `R_OK`, `W_OK`, `X_OK`를 지원합니다.

<h6>사용 형식</h6>

```js
access(path[, mode])
```

## truncate()

파일 내용을 잘라냅니다.

- 길이를 생략하면 `0`으로 자릅니다.
- 길이를 지정하면 앞의 `len` 바이트만 유지합니다.

<h6>사용 형식</h6>

```js
truncate(path[, len])
```

## open()

파일을 열고 숫자 파일 디스크립터를 반환합니다.

`r`, `r+`, `w`, `w+`, `a`, `a+`, `wx`, `wx+`, `ax`, `ax+` 문자열 플래그를 지원합니다.

<h6>사용 형식</h6>

```js
open(path, flags[, mode])
```

## close()

파일 디스크립터를 닫습니다.

<h6>사용 형식</h6>

```js
close(fd)
```

## read()

파일 디스크립터에서 버퍼로 데이터를 읽습니다.

<h6>사용 형식</h6>

```js
read(fd, buffer, offset, length[, position])
```

## write()

문자열 또는 버퍼 데이터를 파일 디스크립터에 씁니다.

<h6>사용 형식</h6>

```js
write(fd, buffer, offset, length[, position])
```

## fstat()

파일 디스크립터 기준 메타데이터를 반환합니다.

<h6>사용 형식</h6>

```js
fstat(fd)
```

## fchmod(), fchown()

파일 디스크립터 기준으로 모드/소유자를 변경합니다.

<h6>사용 형식</h6>

```js
fchmod(fd, mode)
fchown(fd, uid, gid)
```

## fsync(), fdatasync()

대기 중인 파일 데이터를 저장소로 동기화합니다.

현재 `fdatasync()`는 `fsync()`와 동일하게 동작합니다.

<h6>사용 형식</h6>

```js
fsync(fd)
fdatasync(fd)
```

## chmod(), chown()

경로 기준으로 모드/소유자를 변경합니다.

현재 런타임 구현에서 Windows에서는 `chmod`/`chown`이 no-op 호환 동작입니다.

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
fs.access('/work/test.txt', fs.constants.F_OK);
```

## Aliases

가독성을 위해 이 문서에서는 non-`Sync` 이름으로 API를 소개합니다.

Node.js 호환을 위해 `Sync` 접미사 형태도 별칭으로 함께 제공합니다.

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
	console.println('Error reading config:', e);
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

### Example 4: 파일 백업

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

### Example 5: 안전한 파일 쓰기

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
