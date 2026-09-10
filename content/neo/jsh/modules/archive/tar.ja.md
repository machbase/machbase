---
toc: true
title: "tar"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`archive/tar`モジュールは、JSHでTARアーカイブを作成・展開します。
シンプルなメモリ上のヘルパー、ストリーム形式のAPI、ファイルベースの`Tar`クラスを提供します。

処理方法に合わせて、以下のAPIを選択します。

- アーカイブがメモリ上にある場合は、`tarSync()`と`untarSync()`を使用します。
- ファイルを読み込んで`.tar`ファイルに保存する場合や、ディスクに展開する場合は、`Tar`クラスを使用します。
- イベント駆動で処理する場合は、`createTar()`と`createUntar()`を使用します。

## インストール {#설치}

```js
const tar = require('archive/tar');
```

## tarSync() {#tarsync}

TARアーカイブを同期的に作成します。

<h6>構文</h6>

```js
tarSync(data)
```

<h6>パラメーター</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

`data`が単一の文字列またはバイトバッファーの場合、作成するエントリの既定の名前は`data`です。
配列を渡す場合は、各要素を`{ name, data }`形式のエントリオブジェクトとして扱います。

<h6>戻り値</h6>

TARアーカイブのバイト列を含む`ArrayBuffer`を返します。

簡単なテストや、メモリ上でアーカイブを作成してから別の場所に保存する場合に便利です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const tar = require('archive/tar');
const archive = tar.tarSync([
	{ name: 'alpha.txt', data: 'Alpha' },
	{ name: 'dir/beta.txt', data: 'Beta' }
]);
console.println(archive.constructor.name);
```

```js {linenos=table,linenostart=1}
const tar = require('archive/tar');
const archive = tar.tarSync('hello tar');
const entries = tar.untarSync(archive);
console.println(entries[0].name, new Uint8Array(entries[0].data).length);
```

## untarSync() {#untarsync}

TARアーカイブのバイト列を同期的に展開し、エントリオブジェクトの配列を返します。

<h6>構文</h6>

```js
untarSync(buffer)
```

<h6>パラメーター</h6>

- `buffer` `ArrayBuffer | Uint8Array | Number[]`

<h6>戻り値</h6>

エントリオブジェクトの配列を返します。

各エントリには、`name`、`data`、`mode`、`size`、`isDir`、`modified`、`typeflag`、`type`、
`linkname`フィールドを含む場合があります。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
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

## tar() {#tar}

TAR作成機能の、コールバック形式の非同期ラッパーです。

<h6>構文</h6>

```js
tar(data, callback)
```

コールバックのシグネチャは`(err, archive)`です。

## untar() {#untar}

TAR展開機能の、コールバック形式の非同期ラッパーです。

<h6>構文</h6>

```js
untar(buffer, callback)
```

コールバックのシグネチャは`(err, entries)`です。

ストリームイベントを直接管理せずに、コールバック方式で処理する場合に適しています。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const tar = require('archive/tar');

tar.tar('payload', function(err, archive) {
	if (err) throw err;
	tar.untar(archive, function(err2, entries) {
		if (err2) throw err2;
		console.println(entries[0].name, new Uint8Array(entries[0].data).length);
	});
});
```

## createTar() {#createtar}

ストリーム形式のTAR writerを作成します。

返されるオブジェクトは、`write()`でエントリを受け取り、`end()`が呼び出されると、`data`イベントでアーカイブのバイト列を出力します。

このAPIはイベント駆動ですが、Node.jsのファイルストリームのように中間結果を逐次出力せず、`end()`の時点で処理を完了します。

<h6>構文</h6>

```js
createTar()
```

## createUntar() {#createuntar}

ストリーム形式のTAR readerを作成します。

アーカイブのバイト列を`write()`で渡してから`end()`を呼び出すと、展開した項目ごとに`entry`イベントが発生します。

<h6>構文</h6>

```js
createUntar()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
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

## Tar {#tar-1}

`Tar`は、TARアーカイブの作成、保存、読み込み、展開を行うファイル指向のヘルパークラスです。

<h6>コンストラクター</h6>

```js
new tar.Tar(filePath?)
```

`filePath`を指定すると、そのファイルからアーカイブを読み込みます。

### addFile() {#addfile}

ファイルシステムのファイルを読み込み、アーカイブエントリとして追加します。

```js
addFile(filePath[, entryName])
```

### addBuffer() {#addbuffer}

文字列またはバイトバッファーを、アーカイブエントリとして追加します。

```js
addBuffer(data, entryName[, options])
```

### addEntry() {#addentry}

エントリオブジェクトを直接追加します。

```js
addEntry(entry)
```

対応するTARエントリのフィールドは以下のとおりです。

- `name` `String` 必須のエントリパス
- `data` `String | ArrayBuffer | Uint8Array | Number[]` ファイルの内容
- `mode` `Number` ファイルモード
- `modified` `Date` 更新時刻
- `type` `String` 例：`file`、`dir`、`symlink`、`link`
- `typeflag` `Number` 生のTARタイプフラグ
- `linkname` `String` `symlink`または`link`のリンク先パス
- `isDir` `Boolean` ディレクトリエントリかどうか

`addFile()`は、ディスク上にあるファイルをまとめる最も簡単な方法です。
`addBuffer()`は、メモリ上で生成した内容を直接追加する場合に適しています。
`addEntry()`は、ディレクトリエントリやリンクのメタデータなど、TAR固有のプロパティが必要な場合に使用します。

### getEntries() {#getentries}

現在のアーカイブエントリの浅いコピーを返します。

```js
getEntries()
```

### writeTo() {#writeto}

アーカイブをファイルに保存します。

```js
writeTo(filePath)
```

### extractAllTo() {#extractallto}

エントリをディレクトリに展開します。

```js
extractAllTo(outputDir[, overwrite])
extractAllTo(outputDir, options)
extractAllTo(outputDir, overwrite, options)
```

`options`は、以下の値に対応しています。

- `overwrite` `Boolean` `true`の場合、既存のファイルを上書きします。
- `filter` `Function | RegExp | String | String[]` 展開するエントリを選択します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
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

<h6>使用例: ファイルをまとめて再展開する</h6>

```js {linenos=table,linenostart=1}
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

<h6>使用例: 条件付きの展開</h6>

```js {linenos=table,linenostart=1}
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

## 注意 {#참고}

- ディレクトリエントリは`isDir: true`で返され、名前の末尾に`/`が付きます。
- `filter`には、コールバック、`RegExp`、文字列、エントリ名の配列を使用できます。
- `extractAllTo()`は、対象ファイルが存在し、`overwrite`が`false`の場合にエラーを発生させます。
- TAR固有のリンクメタデータは、`type: 'symlink'`または`type: 'link'`と`linkname`の組み合わせで指定できます。
