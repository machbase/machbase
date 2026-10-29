---
toc: true
title: "fs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`fs`モジュールは、JSHアプリケーション用にNode.js互換の同期ファイルシステムAPIを提供します。

API名と引数の形式はNode.jsの`fs`モジュールに従いますが、すべての関数は同期的に動作し、JSHの仮想ファイルシステム上で実行されます。Node.jsと動作が異なる点は、各関数の**注意事項**にまとめています。

## パスとマウント {#paths-and-mounts}

JSHは複数の種類のファイルシステムを1つの仮想ディレクトリツリーにマウントして提供します。`fs`関数に渡すパスはこの仮想パスで、相対パスは現在の作業ディレクトリを基準に解決されます。

マウントの種類によって、サポートされる機能が異なります。

| マウントの種類 | 例 | 特徴 |
| --- | --- | --- |
| ホストディレクトリ | `/work`, `/tmp` | オペレーティングシステムのファイルシステムに直接接続されます。すべてのAPIをサポートします。 |
| メモリベース | `/lib` | ファイルの内容をメモリに保持します。`readFile`/`writeFile`などのパスベースのAPIはサポートしますが、書き込み用ファイルディスクリプター（`open(path, 'w')`など）は`ENOTSUP`で失敗します。読み取り用ディスクリプターに対する`fsync()`も`ENOTSUP`を返します。1ファイルの最大サイズは1GiBです。 |
| 読み取り専用（組み込み） | `/usr`, `/sbin` | 実行ファイルに組み込まれたファイルです。書き込み操作は`EACCES`で失敗し、ディスクリプターに対する`fsync()`は`ENOTSUP`を返します。 |
| 共有ファイルシステム | サービス設定による | サービスコントローラーが複数のJSHプロセスに提供する共有ストレージです。1ファイルの最大サイズは1GiBです。 |

{{< callout emoji="⚠️" >}}
異なるマウント間では`rename()`でファイルを移動できず、`EXDEV`エラーが発生します。この場合は`copyFile()`または`cp()`でコピーしてから元のファイルを削除してください。
{{< /callout >}}

マウントの種類にかかわらず、各マウントのルートディレクトリ（例：`/work`、`/lib`）はマウントポイントです。ネストしたマウントによって生じる中間ディレクトリ（例：`/a/b`のみがマウントされている場合の`/a`）もマウントポイントとして扱います。マウントポイントは`rmdir()`、`unlink()`、`rm()`で削除できず、`rename()`の移動元・移動先にも指定できません。これらの操作はすべて`EBUSY`で失敗し、マウントポイントとマウント構成はそのまま維持されます。マウントポイントの**中にある**ファイルやディレクトリは通常どおり削除・移動できます。

## エラー処理 {#error-handling}

ファイルシステム操作が失敗すると、Node.jsと同じ形式の`Error`オブジェクトをスローします。

| プロパティ | 説明 |
| --- | --- |
| `code` | エラーコード文字列。例：`ENOENT`、`EEXIST` |
| `errno` | エラー番号（負の値）。例：`-2` |
| `syscall` | 失敗した操作の名前。例：`open`、`mkdir`、`rmdir` |
| `path` | 対象のパス。ファイルディスクリプターベースの関数（`read()`、`write()`、`close()`、`fstat()`、`fsync()`など）のエラーには含まれません。 |
| `dest` | `rename()`のエラーにおける移動先のパス |

エラーメッセージの形式は`CODE: 説明, syscall 'path'`です。例えば`ENOENT: no such file or directory, open '/work/none.txt'`のようになります。

```js {linenos=table,linenostart=1}
const fs = require('fs');
try {
    fs.readFile('/work/none.txt');
} catch (e) {
    console.println(e.code, e.errno, e.syscall, e.path);
    // ENOENT -2 open /work/none.txt
}
```

<h6>主なエラーコード</h6>

| コード | errno | 意味 |
| --- | --- | --- |
| `EPERM` | -1 | 許可されていない操作 |
| `ENOENT` | -2 | ファイルまたはディレクトリが存在しない |
| `EIO` | -5 | 入出力エラー |
| `EBADF` | -9 | 無効なファイルディスクリプター。閉じられた、または存在しないディスクリプター、読み取り専用で開いたディスクリプターへの書き込みなど |
| `EACCES` | -13 | 権限がない。読み取り専用マウントへの書き込みを含む |
| `EBUSY` | -16 | リソースが使用中。マウントポイントを削除・移動しようとしたときに発生 |
| `EEXIST` | -17 | すでに存在する |
| `EXDEV` | -18 | 異なるマウント間の移動 |
| `ENOTDIR` | -20 | ディレクトリではない |
| `EISDIR` | -21 | ディレクトリに対して許可されていない操作 |
| `EINVAL` | -22 | 無効な引数 |
| `EFBIG` | -27 | ファイルが大きすぎる。メモリベース・共有ファイルシステムの1GiB制限を超過 |
| `ENOSPC` | -28 | ストレージの空き容量不足 |
| `EROFS` | -30 | 読み取り専用ファイルシステム |
| `ENAMETOOLONG` | -36 | ファイル名が長すぎる |
| `ENOTEMPTY` | -39 | ディレクトリが空ではない |
| `ELOOP` | -40 | シンボリックリンクの段数が多すぎる |
| `ENOTSUP` | -95 | サポートされていない操作 |
| `ECONFLICT` | -32009 | （JSH専用）共有ファイルシステムでディスクリプターを開いた後、別のプロセスが同じファイルを変更した |

- `errno`の値は実行プラットフォームに関係なく、上の表の値（Linux基準）に固定されます。macOSやWindowsのNode.jsで報告される`errno`の数値とは異なる場合があるため、エラーの判別には`errno`ではなく`code`を使用してください。
- `offset`、`length`、`position`、`len`などの引数が範囲外の場合は`RangeError`をスローします。`code`は`ERR_OUT_OF_RANGE`で、`errno`はありません。

## readFile() {#readfile}

ファイルを読み取り、文字列（既定: `utf8`）またはバイト配列として返します。

<h6>構文</h6>

```js
readFile(path[, options])
```

- `options`はエンコーディング文字列または`{ encoding }`オブジェクトです。`encoding: null`を指定するとバイト配列を返します。
- ファイル全体をメモリに読み込みます。大きなファイルは`createReadStream()`または`open()`/`read()`で分割して読み取ってください。

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

- 親ディレクトリが存在しない場合は`ENOENT`で失敗します。必要に応じて先に`mkdir(dir, { recursive: true })`を呼び出してください。
- メモリベースのマウントと共有ファイルシステムでは、1GiBを超えるファイルは書き込めません。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile() {#appendfile}

ファイルの末尾にデータを追加します。ファイルがなければ新しく作成します。

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

ファイルの行数（改行基準）を数えます。JSH専用の関数です。

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

ファイルまたはディレクトリが存在するかどうかを`true`/`false`で返します。

<h6>構文</h6>

```js
exists(path)
```

- シンボリックリンクはたどって確認します。リンク先が存在しないリンク（壊れたリンク）は`false`を返します。リンク自体の存在を確認するには`lstat()`を使用してください。
- 権限不足など、その他の理由で確認できない場合も`false`を返します。失敗の原因が必要な場合は`access()`または`stat()`を使用してください。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
console.println(fs.exists('/work/test.txt'));
console.println(fs.exists('/work/not-found.txt'));
```

## stat() {#stat}

ファイルまたはディレクトリのメタデータを返します。パスがシンボリックリンクの場合は、リンク先の情報を返します。

<h6>構文</h6>

```js
stat(path)
```

<h6>返されるフィールド</h6>

- `name`: ファイル名（パスの最後の要素）
- `size`: バイト単位のサイズ
- `mode`: ファイルモードオブジェクト。`String(st.mode)`は`drwxr-xr-x`のような文字列を返します。
- `mtime`, `atime`, `ctime`, `birthtime`: 現在の実装では、すべて更新時刻（`mtime`）と同じ値です。
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

ファイルのメタデータを返します。`stat()`と異なり、パスの最後の要素がシンボリックリンクの場合はリンクをたどらず、リンク自体の情報を返します。返されるフィールドは`stat()`と同じです。ネストしたマウントによって生じる中間ディレクトリは、`stat()`と同様にディレクトリとして返されます。

<h6>構文</h6>

```js
lstat(path)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/target.txt', 'data');
fs.symlink('target.txt', '/work/link.txt');
console.println(fs.lstat('/work/link.txt').isSymbolicLink()); // true
console.println(fs.stat('/work/link.txt').isFile());          // true
```

## readdir() {#readdir}

ディレクトリのエントリを読み取ります。

- 既定: エントリ名の`string[]`を返します。
- `withFileTypes: true`: `name`と型メソッド（`isFile()`、`isDirectory()`、`isSymbolicLink()`など）を持つエントリオブジェクトを返します。
- `recursive: true`: サブディレクトリを含めて再帰的に返します。

<h6>構文</h6>

```js
readdir(path[, options])
```

<h6>注意事項</h6>

- **非再帰の読み取りでは、結果に`.`と`..`のエントリが含まれます。** Node.jsとは異なる動作のため、ディレクトリを走査する際は必ずこの2つのエントリをスキップしてください。スキップしないと、同じディレクトリを無限に再帰する可能性があります。
- 再帰の読み取り（`recursive: true`）では`.`と`..`は含まれません。
  - 文字列の結果は、開始ディレクトリを基準とした相対パス（例: `a/b/file.txt`）です。
  - エントリオブジェクトの`path`プロパティは、エントリが属するディレクトリの相対パスで、開始ディレクトリ直下のエントリでは`''`です。Node.jsの`Dirent.path`（親ディレクトリのフルパス）とは異なります。
- 再帰の読み取りでは、ディレクトリを指すシンボリックリンクの中には入りません。リンクはエントリとしてのみ返されます。
- 再帰の読み取り中にサブディレクトリを読み取れない場合（権限不足など）、読み取り全体がエラーで失敗します。エラーオブジェクトの`path`は失敗したサブディレクトリを指します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const names = fs.readdir('/lib').filter(n => n !== '.' && n !== '..');
const all = fs.readdir('/work', { recursive: true });
console.println(names.length, all.length);
```

## mkdir() {#mkdir}

ディレクトリを作成します。

<h6>構文</h6>

```js
mkdir(path[, options])
```

<h6>オプション</h6>

- `recursive`: `true`の場合、存在しない親ディレクトリも作成し、既存のディレクトリはエラーなしでスキップします。既定値は`false`です。
- `mode`: 作成するディレクトリの権限です。既定値は`0o755`で、再帰作成時は新しく作成するすべてのディレクトリに適用されます。ホストディレクトリでは、オペレーティングシステムのumaskが追加で適用される場合があります。

<h6>動作</h6>

- 非再帰の呼び出し（`recursive: false`）
  - 親ディレクトリが存在しない場合は`ENOENT`で失敗します。親ディレクトリは自動的に作成されません。
  - 対象がすでに存在する場合は、ディレクトリでもファイルでも`EEXIST`で失敗します。
- 再帰の呼び出し（`recursive: true`）
  - パスの途中に同じ名前の**ファイル**がある場合は`EEXIST`で失敗します。Node.jsはこの場合`ENOTDIR`を返します。
  - 戻り値は常に`undefined`です。Node.jsのように最初に作成されたパスは返しません。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
fs.mkdir('/work/private', { mode: 0o700 });
```

## rmdir() {#rmdir}

空のディレクトリを削除します。

<h6>構文</h6>

```js
rmdir(path[, options])
```

- ディレクトリが空でない場合は`ENOTEMPTY`、対象がファイルの場合は`ENOTDIR`で失敗します。
- `{ recursive: true }`を指定すると、先に子エントリをすべて削除します。Node.jsでは非推奨（deprecated）のオプションのため、新しいコードでは`rm(path, { recursive: true })`の使用を推奨します。
- 再帰削除の際、ディレクトリを指すシンボリックリンクはリンクのみを削除し、リンク先の内容は削除しません。
- マウントポイントを指定すると`EBUSY`で失敗します。再帰削除でマウントポイントに遭遇したときの動作は[rm()](#rm)と同じです。

## rm() {#rm}

ファイル、シンボリックリンク、またはディレクトリを削除します。

<h6>構文</h6>

```js
rm(path[, options])
```

<h6>オプション</h6>

- `recursive`: `true`の場合、ディレクトリとその内容をすべて削除します。
- `force`: `true`の場合、対象が存在しないとき（`ENOENT`）のエラーを無視します。

<h6>注意事項</h6>

- 対象の種類は`lstat()`で判別します。シンボリックリンクは、リンク先がディレクトリであっても**リンク自体のみ**が削除され、リンク先のディレクトリとその内容は保持されます。
- `recursive`なしでディレクトリを指定すると、空のディレクトリのみ削除されます。空でない場合は`ENOTEMPTY`で失敗します。
- `force: true`は`ENOENT`のみを無視します。権限不足（`EACCES`）、入出力エラー（`EIO`）などのその他のエラーはそのままスローします。マウントポイントで発生する`EBUSY`も無視しません。
- 再帰削除の途中でエラーが発生すると、ただちに中断します。すでに削除されたエントリは復元されないため、一部のみが削除された状態で残る場合があります。
- マウントポイントは例外的に扱います。対象自体またはその配下にあるマウントポイントは内容のみがすべて削除され、空のディレクトリとして残ります。残りのエントリの削除は続行し、すべてのエントリを処理した後、最初に遭遇したマウントポイントのパスで`EBUSY`をスローします。Linuxでマウントされたディレクトリを`rm -r`で削除した場合と同じ結果です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.rm('/work/a', { recursive: true, force: true });
```

## unlink() {#unlink}

ファイルまたはシンボリックリンクを削除します。

<h6>構文</h6>

```js
unlink(path)
```

- ディレクトリには使用できず、`EISDIR`で失敗します。ディレクトリには`rmdir()`または`rm()`を使用してください。
- シンボリックリンクを指定すると、リンクのみが削除され、リンク先のファイルは保持されます。
- マウントポイントを指定すると`EBUSY`で失敗します。
- Windowsでは、読み取り専用属性のファイルも削除します。

{{< callout emoji="📌" >}}
`unlink()`、`rmdir()`、`rm()`、`rename()`で最後のエントリを削除または移動しても、親ディレクトリはそのまま残ります。メモリベースのマウントと共有ファイルシステムも同様に動作します。
{{< /callout >}}

## rename() {#rename}

同じマウント内で、ファイルまたはディレクトリの名前を変更するか移動します。

<h6>構文</h6>

```js
rename(oldPath, newPath)
```

- 移動先のパスにファイルがある場合は、オペレーティングシステムの`rename`の動作に従って上書きします。
- 異なるマウント間の移動は`EXDEV`で失敗します。この場合、エラーオブジェクトの`dest`プロパティに移動先のパスが格納されます。
- 移動元または移動先がマウントポイントの場合は`EBUSY`で失敗します。

## copyFile() {#copyfile}

単一のファイルをコピーします。

<h6>構文</h6>

```js
copyFile(src, dest[, flags])
```

- 既定では、コピー先のファイルが存在する場合は上書きします。
- `flags`に`constants.COPYFILE_EXCL`を指定すると、コピー先のファイルが存在する場合に`EEXIST`で失敗します。
- `COPYFILE_FICLONE`、`COPYFILE_FICLONE_FORCE`は無視され、通常のコピーを行います。
- ファイルの内容のみをコピーします。コピー元ファイルの権限と更新時刻は保持されません。
- ファイル全体をメモリに読み込んでから書き込むため、非常に大きなファイルのコピーには適していません。

## cp() {#cp}

ファイルまたはディレクトリをコピーします。

<h6>構文</h6>

```js
cp(src, dest[, options])
```

<h6>オプション</h6>

- `recursive`: ディレクトリをコピーするには`true`である必要があります。省略すると、ディレクトリのコピーは`EISDIR`で失敗します。
- `force`: `true`の場合、コピー先にすでにあるファイルを上書きします。

<h6>注意事項</h6>

- **`force`の既定値は`false`です。** コピー先のファイルがすでに存在する場合は`EEXIST`で失敗します。Node.jsの`cpSync()`は既定で上書きするため、動作が異なります。
- コピー元のシンボリックリンクはたどって、リンク先の内容をコピーします。リンク自体はコピーしません。
- ファイルの内容のみをコピーし、権限と更新時刻は保持されません。

## symlink() {#symlink}

シンボリックリンクを作成します。

<h6>構文</h6>

```js
symlink(target, path)
```

- `target`が相対パスの場合、Node.jsと同様に**リンクが置かれるディレクトリを基準に**解決され、相対パスの形のまま保存されます。
- `target`が`/`で始まる場合は、JSHの仮想パスとして扱われます。
- リンク先がマウントされた領域の外を指すことになる場合（例: `../../../etc/passwd`）は`EACCES`で失敗します。
- Node.jsの第3引数（`type`）はサポートしていません。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.mkdir('/work/data', { recursive: true });
fs.writeFile('/work/data/v1.csv', 'a,b\n');
fs.symlink('v1.csv', '/work/data/current.csv');   // /work/data を基準に解決
console.println(fs.readFile('/work/data/current.csv'));
```

## readlink() {#readlink}

シンボリックリンクのリンク先パスを読み取ります。

<h6>構文</h6>

```js
readlink(path)
```

- **戻り値は常に解決済みの絶対仮想パスです。** リンクが相対パス（`v1.csv`）で保存されていても、`/work/data/v1.csv`のように返されます。保存された文字列をそのまま返すNode.jsとは異なります。
- シンボリックリンクではないパスには`EINVAL`をスローします。
- リンクがマウントされた領域の外を指す場合は`ENOENT`をスローします。

## realpath() {#realpath}

すべてのシンボリックリンクと`.`、`..`を解決した実際のパスを返します。

<h6>構文</h6>

```js
realpath(path)
```

- パスの最後の要素だけでなく、途中のディレクトリのシンボリックリンクも解決します。
- パスの要素が存在しない場合は`ENOENT`、循環リンクなどでリンクを40回を超えてたどる必要がある場合は`ELOOP`をスローします。
- 戻り値はJSHの仮想パスです。

## access() {#access}

パスが存在するかどうか、指定した権限でアクセスできるかどうかを確認します。アクセスできる場合は`undefined`を返し、できない場合はエラーをスローします。

<h6>構文</h6>

```js
access(path[, mode])
```

- `mode`は`constants.F_OK`（存在、既定値）、`R_OK`（読み取り）、`W_OK`（書き込み）、`X_OK`（実行）をビットORで組み合わせます。
- パスが存在しない場合は`ENOENT`、権限がない場合は`EACCES`、`mode`が0〜7の範囲外の場合は`EINVAL`をスローします。

<h6>注意事項</h6>

- ホストディレクトリのマウントでは、オペレーティングシステムの権限チェックを使用します。
- Windowsでの動作はNode.jsと同じです。
  - 読み取り専用属性のファイルに`W_OK`をチェックすると`EPERM`をスローします。
  - `X_OK`は存在確認（`F_OK`）と同じように扱われます。
- メモリベース・組み込み・共有ファイルシステムでは、JSHプロセスをファイルの所有者とみなし、ファイルモードの**所有者**の権限ビットで判断します。たとえば`0o600`のファイルは`R_OK`/`W_OK`の検査に成功し、`0o004`のファイルは`R_OK`の検査に失敗します。グループとACLは考慮しません。
- 読み取り専用マウントでの`W_OK`チェックは常に失敗します。
- `access()`で確認してからファイルを開く方法では、その間に状態が変わる可能性があります。可能であれば、ファイルを直接開いてエラーを処理してください。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
try {
    fs.access('/work/test.txt', fs.constants.R_OK | fs.constants.W_OK);
    console.println('readable and writable');
} catch (e) {
    console.println('no access:', e.code);
}
```

## truncate() {#truncate}

ファイルサイズを指定した長さに合わせます。

<h6>構文</h6>

```js
truncate(path[, len])
```

- `len`を省略すると`0`に切り詰めます。
- `len`が現在のサイズより小さい場合は、先頭の`len`バイトのみを残します。
- `len`が現在のサイズより大きい場合はファイルを拡張し、増えた部分は`0`バイトで埋めます。
- `len`が負の値または整数でない場合は`RangeError`（`ERR_OUT_OF_RANGE`）をスローします。
- メモリベースのマウントと共有ファイルシステムで1GiBを超える長さを指定すると`EFBIG`で失敗し、ファイルは変更されません。

## open() {#open}

ファイルを開き、数値のファイルディスクリプターを返します。

<h6>構文</h6>

```js
open(path, flags[, mode])
```

- `flags`: 文字列フラグ、または`constants.O_*`の値を組み合わせた数値フラグです。
- `mode`: ファイルを新しく作成する際に使用する権限です。既定値は`0o666`です。

<h6>文字列フラグ</h6>

| フラグ | 意味 |
| --- | --- |
| `r` | 読み取り。ファイルがなければ失敗 |
| `r+` | 読み書き。ファイルがなければ失敗 |
| `w` | 書き込み。なければ作成し、あれば内容を空にする |
| `w+` | 読み書き。なければ作成し、あれば内容を空にする |
| `a` | 追記。なければ作成 |
| `a+` | 読み取り/追記。なければ作成 |
| `wx`, `wx+`, `ax`, `ax+` | 上と同じだが、ファイルがすでに存在する場合は`EEXIST`で失敗 |

<h6>注意事項</h6>

- 上の表にない文字列フラグは、エラーなしで`r`（読み取り専用）として扱われます。タイプミスがあってもエラーにならず、その後の`write()`が`EBADF`で失敗する場合があるため、フラグ文字列は正確に指定してください。
- メモリベースのマウント（例: `/lib`）では、読み取り用のディスクリプターのみ開けます。書き込みフラグを指定すると`ENOTSUP`で失敗するため、`writeFile()`/`appendFile()`を使用してください。
- 読み取り専用（組み込み）マウントで書き込みフラグを指定して開くと`EACCES`で失敗します。
- 使用したディスクリプターは必ず`close()`で閉じてください。

## close() {#close}

ファイルディスクリプターを閉じます。

<h6>構文</h6>

```js
close(fd)
```

- すでに閉じられた、または存在しないディスクリプターは`EBADF`で失敗します。
- 共有ファイルシステムでは、閉じた時点で変更内容が保存されます。ディスクリプターを開いた後に別のプロセスが同じファイルを変更していた場合は`ECONFLICT`で失敗します。

## read() {#read}

ファイルディスクリプターからデータを読み取ってバッファに格納し、読み取ったバイト数を返します。ファイルの末尾では`0`を返します。

<h6>構文</h6>

```js
read(fd, buffer, offset, length[, position])
```

- `buffer`: データを受け取る`Uint8Array`、`Buffer`、または数値配列
- `offset`: バッファ内で書き込みを開始する位置。既定値は`0`です。
- `length`: 読み取る最大バイト数。既定値は`buffer.length - offset`です。
- `position`: ファイル内で読み取りを開始する位置
  - `null`または省略: 現在のファイル位置から読み取り、読み取った分だけ現在位置が進みます。
  - 0以上の整数: 指定した位置から読み取り、**現在のファイル位置は変わりません。**

<h6>注意事項</h6>

- `offset`、`length`、`position`が範囲外の場合は`RangeError`（`ERR_OUT_OF_RANGE`）をスローします。例えば、`offset + length`がバッファサイズを超える場合や、`position`が負の値の場合です。
- 書き込み専用で開いたディスクリプターを読み取ると`EBADF`で失敗します。
- Linux/macOSでディレクトリのディスクリプターを読み取ると`EISDIR`で失敗します。ディレクトリの内容は`readdir()`で読み取ってください。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.writeFile('/work/data.bin', 'ABCDEFGH');
const fd = fs.open('/work/data.bin', 'r');
const buf = new Uint8Array(4);
fs.read(fd, buf, 0, 4, 4);   // "EFGH" を読み取り、ファイル位置は変わらない
fs.read(fd, buf, 0, 4);      // 現在位置から "ABCD" を読み取る
fs.close(fd);
```

## write() {#write}

バッファまたは文字列のデータをファイルディスクリプターに書き込み、書き込んだバイト数を返します。

<h6>構文</h6>

```js
write(fd, data[, offset[, length[, position]]])
```

- `data`: `Uint8Array`、`Buffer`、数値配列、または文字列。文字列はUTF-8バイトに変換して書き込みます。
- `offset`: `data`内で書き込みを開始するバイト位置。既定値は`0`です。
- `length`: 書き込むバイト数。既定値は`offset`から末尾までです。`0`を指定すると何も書き込みません。
- `position`: ファイル内で書き込みを開始する位置
  - `null`または省略: 現在のファイル位置に書き込み、書き込んだ分だけ現在位置が進みます。
  - 0以上の整数: 指定した位置に書き込み、**現在のファイル位置は変わりません。** 位置がファイルの末尾より後ろの場合、その間は`0`バイトで埋められます。

<h6>注意事項</h6>

- **文字列を書き込む場合も、引数の順序は`(fd, data, offset, length, position)`です。** Node.jsの`writeSync(fd, string, position, encoding)`の形式はサポートしていません。例えば`write(fd, 'Z', 3)`の`3`はファイル位置ではなく`offset`として解釈されるため、`ERR_OUT_OF_RANGE`が発生します。
- 文字列の`offset`と`length`は、文字数ではなくUTF-8の**バイト**単位です。
- `a`、`a+`などの追記モードで開いたディスクリプターは、`position`を指定しても無視し、常にファイルの末尾に書き込みます。
- `offset`、`length`、`position`が範囲外の場合は`RangeError`（`ERR_OUT_OF_RANGE`）をスローします。
- 読み取り専用で開いたディスクリプターに書き込むと`EBADF`で失敗します。
- 共有ファイルシステムで、書き込みの結果が1GiBを超える場合は`EFBIG`で失敗します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const fd = fs.open('/work/out.txt', 'w+');
fs.write(fd, 'Hello World');                // 現在位置に書き込む
fs.write(fd, 'J', 0, 1, 0);                 // 先頭1バイトを上書き: "Jello World"
const bytes = new Uint8Array([0x21, 0x21]);
fs.write(fd, bytes, 0, bytes.length);       // 現在位置に "!!" を追加
fs.close(fd);
```

## fstat() {#fstat}

ファイルディスクリプターのメタデータを返します。

<h6>構文</h6>

```js
fstat(fd)
```

- 返されるオブジェクトは`name`、`size`、`mode`、`mtime`と型メソッド（`isFile()`など）を提供します。`atime`、`ctime`、`birthtime`は含まれません。

## fchmod(), fchown() {#fchmod-fchown}

ファイルディスクリプター基準でモード/所有者を変更します。

<h6>構文</h6>

```js
fchmod(fd, mode)
fchown(fd, uid, gid)
```

- Windowsのホストディレクトリマウントで開いたファイルディスクリプターでは、何もせずに成功します。
- その他のマウントでは、それぞれのファイルシステムの動作に従います。たとえば、読み取り専用（組み込み）マウントのディスクリプターでは`EACCES`をスローします。

## fsync(), fdatasync() {#fsync-fdatasync}

保留中のファイルデータをストレージに同期します。

<h6>構文</h6>

```js
fsync(fd)
fdatasync(fd)
```

- 現在、`fdatasync()`は`fsync()`と同じように動作します。
- 読み取り専用（組み込み）マウントで開いたディスクリプターと、メモリベースのマウント（例：`/lib`）の読み取り用ディスクリプターには同期する対象がないため、`ENOTSUP`をスローします。Node.jsとは異なる動作です。
- 共有ファイルシステムで、ディスクリプターを開いた後に別のプロセスが同じファイルを変更していた場合は`ECONFLICT`で失敗します。

## chmod(), chown() {#chmod-chown}

パス基準でモード/所有者を変更します。

Windowsのホストディレクトリマウントでは、`chmod`/`chown`は何もしない互換動作です。メモリベース、組み込み、共有ファイルシステムでは、それぞれの動作に従います。

<h6>構文</h6>

```js
chmod(path, mode)
chown(path, uid, gid)
```

## createReadStream(), createWriteStream() {#createreadstream-createwritestream}

EventEmitterベースの使用方法と互換性のあるストリームオブジェクトを作成します。

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

アクセス、コピー、ファイルオープンのフラグを含む定数オブジェクトです。

<h6>主なフィールド</h6>

- アクセス: `F_OK`(0), `R_OK`(4), `W_OK`(2), `X_OK`(1)
- コピー: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- ファイルオープン: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

ファイルオープン定数の実際の値は実行プラットフォームによって異なる場合があるため、数値を直接記述せずに定数を使用してください。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.access('/work/test.txt', fs.constants.F_OK);
const fd = fs.open('/work/new.txt', fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL);
fs.close(fd);
```

## 別名 {#aliases}

読みやすさのため、このドキュメントでは`Sync`のない名前でAPIを紹介します。

Node.jsとの互換性のため、`Sync`接尾辞を持つ別名も提供します。2つの名前は同じ関数で、どちらも同期的に動作します。コールバックやPromiseベースのAPIは提供しません。

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
    console.println('Error reading config:', e.code || e);
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

非再帰の`readdir()`の結果には`.`と`..`が含まれるため、必ずスキップしてください。

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
    // 各ファイルを処理
});
```

すべてのパスだけが必要な場合は、`recursive`オプションを使用できます。

```js {linenos=table,linenostart=1}
const fs = require('fs');
fs.readdir('/tmp', { recursive: true }).forEach(p => console.println(p));
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

    fs.copyFile(path, backupPath, fs.constants.COPYFILE_EXCL);
    console.println('Backup created:', backupPath);

    return backupPath;
}

backupFile('/tmp/important.txt');
```

### 例5：安全なファイル書き込み {#example-5-안전한-파일-쓰기}

先に一時ファイルに書き込み、`rename()`で置き換えます。`rename()`は同じマウント内でのみ動作するため、一時ファイルは対象ファイルと同じディレクトリに作成します。

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
        fs.rm(tempPath, { force: true });
        throw e;
    }
}

safeWriteFile('/tmp/data.txt', 'Important data');
```

### 例6：エラーコードに応じた処理 {#example-6-오류-코드에-따른-처리}

```js {linenos=table,linenostart=1}
const fs = require('fs');

function ensureDir(path) {
    try {
        fs.mkdir(path);
    } catch (e) {
        if (e.code === 'EEXIST' && fs.stat(path).isDirectory()) {
            return;   // すでに存在する
        }
        if (e.code === 'ENOENT') {
            fs.mkdir(path, { recursive: true });   // 親ディレクトリがない
            return;
        }
        throw e;
    }
}

ensureDir('/work/output/2024');
```
