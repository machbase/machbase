---
toc: true
title: "fs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`fs`モジュールは、JSHアプリケーション用にNode.js互換の同期ファイルシステムAPIを提供します。

## readFile() {#readfile}

ファイルを読み取り、文字列（既定値：`utf8`）またはバイト配列で返します。

<h6>構文</h6>

```js
readFile(path[, options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const content = fs.readFile('/lib/fs.js', 'utf8');
console.println(content.length);
```

## writeFile() {#writefile}

ファイルにデータを書き込みます。ファイルがなければ作成し、あれば上書きします。

<h6>構文</h6>

```js
writeFile(path, data[, options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile() {#appendfile}

ファイルの末尾にデータを追加します。ファイルがなければ作成します。

<h6>構文</h6>

```js
appendFile(path, data[, options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/append.txt', 'Line 1\n', 'utf8');
fs.appendFile('/work/append.txt', 'Line 2\n', 'utf8');
```

## countLines() {#countlines}

改行を基準に、ファイルの行数を数えます。

<h6>構文</h6>

```js
countLines(path)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.countLines('/work/append.txt'));
```

## exists() {#exists}

ファイルまたはディレクトリが存在するかどうかを、`true`または`false`で返します。

<h6>構文</h6>

```js
exists(path)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.exists('/work/test.txt'));
console.println(fs.exists('/work/not-found.txt'));
```

## stat() {#stat}

ファイルまたはディレクトリのメタデータを返します。

<h6>構文</h6>

```js
stat(path)
```

<h6>返されるフィールド</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat() {#lstat}

ファイルのメタデータを返します。現在の実装では、`stat()`と同じ動作です。

<h6>構文</h6>

```js
lstat(path)
```

## readdir() {#readdir}

ディレクトリエントリを読み取ります。

- 既定値：`string[]`を返す
- `withFileTypes: true`: `name`と型判定メソッドを持つエントリオブジェクトを返す
- `recursive: true`: サブディレクトリを含めて再帰的に返す

現在のランタイムのディレクトリ一覧には、`.`と`..`が含まれます。

<h6>構文</h6>

```js
readdir(path[, options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const names = fs.readdir('/lib');
const entries = fs.readdir('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdir() {#mkdir}

ディレクトリを作成します。再帰的な作成オプションに対応しています。

<h6>構文</h6>

```js
mkdir(path[, options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
```

## rmdir() {#rmdir}

ディレクトリを削除します。`{ recursive: true }`を指定すると、子エントリを先に削除します。

<h6>構文</h6>

```js
rmdir(path[, options])
```

## rm() {#rm}

ファイルまたはディレクトリを削除します。

- ディレクトリの削除には、内部で`rmdir()`を使用します。
- `force: true`を指定すると、エラーを無視します。

<h6>構文</h6>

```js
rm(path[, options])
```

## unlink() {#unlink}

ファイルを削除します。

<h6>構文</h6>

```js
unlink(path)
```

## rename() {#rename}

同じマウント済みファイルシステム内で、ファイル・ディレクトリの名前を変更するか移動します。

<h6>構文</h6>

```js
rename(oldPath, newPath)
```

## copyFile() {#copyfile}

単一ファイルをコピーします。

`COPYFILE_EXCL`フラグを指定すると、対象ファイルが存在する場合は失敗します。

<h6>構文</h6>

```js
copyFile(src, dest[, flags])
```

## cp() {#cp}

ファイルまたはディレクトリをコピーします。

ディレクトリをコピーするには、`{ recursive: true }`が必要です。

<h6>構文</h6>

```js
cp(src, dest[, options])
```

## symlink() {#symlink}

シンボリックリンクを作成します。

<h6>構文</h6>

```js
symlink(target, path)
```

## readlink() {#readlink}

シンボリックリンクのリンク先パスを読み取ります。

<h6>構文</h6>

```js
readlink(path)
```

## realpath() {#realpath}

シンボリックリンクを解決した実際のパスを返します。

<h6>構文</h6>

```js
realpath(path)
```

## access() {#access}

パスにアクセスできるかどうかを確認します。

- パスが存在しない場合は、`ENOENT`例外を発生させます。
- モード定数`F_OK`、`R_OK`、`W_OK`、`X_OK`に対応しています。

<h6>構文</h6>

```js
access(path[, mode])
```

## truncate() {#truncate}

ファイルの内容を切り詰めます。

- 長さを省略すると、`0`に切り詰めます。
- 長さを指定すると、先頭の`len`バイトだけを保持します。

<h6>構文</h6>

```js
truncate(path[, len])
```

## open() {#open}

ファイルを開き、数値のファイルディスクリプターを返します。

文字列フラグ`r`、`r+`、`w`、`w+`、`a`、`a+`、`wx`、`wx+`、`ax`、`ax+`に対応しています。

<h6>構文</h6>

```js
open(path, flags[, mode])
```

## close() {#close}

ファイルディスクリプターを閉じます。

<h6>構文</h6>

```js
close(fd)
```

## read() {#read}

ファイルディスクリプターからバッファーにデータを読み取ります。

<h6>構文</h6>

```js
read(fd, buffer, offset, length[, position])
```

## write() {#write}

文字列またはバッファーのデータを、ファイルディスクリプターに書き込みます。

<h6>構文</h6>

```js
write(fd, buffer, offset, length[, position])
```

## fstat() {#fstat}

ファイルディスクリプターに対応するメタデータを返します。

<h6>構文</h6>

```js
fstat(fd)
```

## fchmod(), fchown() {#fchmod-fchown}

ファイルディスクリプターでモード・所有者を変更します。

<h6>構文</h6>

```js
fchmod(fd, mode)
fchown(fd, uid, gid)
```

## fsync(), fdatasync() {#fsync-fdatasync}

保留中のファイルデータをストレージに同期します。

現在の`fdatasync()`は、`fsync()`と同じ動作です。

<h6>構文</h6>

```js
fsync(fd)
fdatasync(fd)
```

## chmod(), chown() {#chmod-chown}

パスでモード・所有者を変更します。

現在のランタイム実装では、Windowsの`chmod`と`chown`は何も処理しない互換動作（no-op）です。

<h6>構文</h6>

```js
chmod(path, mode)
chown(path, uid, gid)
```

## createReadStream(), createWriteStream() {#createreadstream-createwritestream}

EventEmitter方式の使用と互換性のある、ストリームオブジェクトを作成します。

<h6>構文</h6>

```js
createReadStream(path[, options])
createWriteStream(path[, options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const rs = fs.createReadStream('/work/in.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/out.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## platform(), arch() {#platform-arch}

ランタイムのプラットフォームとアーキテクチャの文字列を返します。

<h6>構文</h6>

```js
platform()
arch()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.platform());
console.println(fs.arch());
```

## constants {#constants}

アクセス、コピー、ファイルを開く操作のフラグを含む定数オブジェクトです。

<h6>主なフィールド</h6>

- アクセス： `F_OK`, `R_OK`, `W_OK`, `X_OK`
- コピー： `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- ファイルを開く操作： `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.access('/work/test.txt', fs.constants.F_OK);
```

## 別名 {#aliases}

読みやすさのため、このドキュメントでは`Sync`のない名前でAPIを紹介します。

Node.jsとの互換性のため、`Sync`接尾辞を持つ別名も提供します。

例： `readFileSync`, `writeFileSync`, `appendFileSync`, `readdirSync`, `mkdirSync`, `rmSync`, `statSync`, `openSync`, `closeSync`, `readSync`, `writeSync`, `fstatSync`, `fsyncSync`, `fdatasyncSync`.


## 使用例 {#examples}

### 例1：JSONファイルの読み取りと解析 {#example-1-json-파일-읽기-및-파싱}

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

### 例2：ログファイルの書き込み {#example-2-로그-파일-쓰기}

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

### 例3：ディレクトリツリーの走査 {#example-3-디렉터리-트리-순회}

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
	// 各ファイルを処理
});
```

### 例4：ファイルのバックアップ {#example-4-파일-백업}

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

### 例5：安全なファイル書き込み {#example-5-안전한-파일-쓰기}

```js {linenos=table,linenostart=1}
const fs = require('fs');

function safeWriteFile(path, data) {
	const tempPath = path + '.tmp';

	try {
		// 先に一時ファイルに書き込み
		fs.writeFile(tempPath, data, 'utf8');

		// 成功した場合は対象の名前に変更
		fs.rename(tempPath, path);

		console.println('File written safely');
	} catch (e) {
		// 一時ファイルがあれば削除
		if (fs.exists(tempPath)) {
			fs.unlink(tempPath);
		}
		throw e;
	}
}

safeWriteFile('/tmp/data.txt', 'Important data');
```
