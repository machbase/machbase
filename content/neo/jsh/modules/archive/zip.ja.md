---
toc: true
title: "zip"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`archive/zip`モジュールは、JSHでZIPアーカイブを作成・展開します。
メモリ上のヘルパー、ストリーム形式のAPI、ファイルベースの`Zip`クラスを提供します。

処理方法に合わせて、以下のAPIを選択します。

- アーカイブがメモリ上にある場合は、`zipSync()`と`unzipSync()`を使用します。
- ファイルを読み込んで`.zip`ファイルに保存する場合や、ディスクに展開する場合は、`Zip`クラスを使用します。
- イベント駆動で処理する場合は、`createZip()`と`createUnzip()`を使用します。

## インストール {#설치}

```js
const zip = require('archive/zip');
```

## zipSync() {#zipsync}

ZIPアーカイブを同期的に作成します。

<h6>構文</h6>

```js
zipSync(data)
```

<h6>パラメーター</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

`data`が単一の文字列またはバイトバッファーの場合、作成するエントリの既定の名前は`data`です。
配列を渡す場合は、各要素を`{ name, data }`形式のエントリオブジェクトとして扱います。

<h6>戻り値</h6>

ZIPアーカイブのバイト列を含む`ArrayBuffer`を返します。

簡単なテストや、メモリ上でアーカイブを作成してから別の場所に保存する場合に便利です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const zip = require('archive/zip');
const archive = zip.zipSync([
	{ name: 'alpha.txt', data: 'Alpha' },
	{ name: 'dir/beta.txt', data: 'Beta' }
]);
console.println(archive.constructor.name);
```

```js {linenos=table,linenostart=1}
const zip = require('archive/zip');
const archive = zip.zipSync('hello zip');
const entries = zip.unzipSync(archive);
console.println(entries[0].name, new Uint8Array(entries[0].data).length);
```

## unzipSync() {#unzipsync}

ZIPアーカイブのバイト列を同期的に展開し、エントリオブジェクトの配列を返します。

<h6>構文</h6>

```js
unzipSync(buffer)
```

<h6>パラメーター</h6>

- `buffer` `ArrayBuffer | Uint8Array | Number[]`

<h6>戻り値</h6>

エントリオブジェクトの配列を返します。

各エントリには、`name`、`data`、`comment`、`method`、`compressedSize`、`size`、`isDir`、
`modified`フィールドを含む場合があります。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const zip = require('archive/zip');
const archive = zip.zipSync([
	{ name: 'one.txt', data: 'One' },
	{ name: 'two.txt', data: 'Two' }
]);
const entries = zip.unzipSync(archive);
console.println(entries[0].name, entries[0].size);
console.println(entries[1].name, entries[1].size);
console.println(entries.length);
```

## zip() {#zip}

ZIP作成機能の、コールバック形式の非同期ラッパーです。

<h6>構文</h6>

```js
zip(data, callback)
```

コールバックのシグネチャは`(err, archive)`です。

## unzip() {#unzip}

ZIP展開機能の、コールバック形式の非同期ラッパーです。

<h6>構文</h6>

```js
unzip(buffer, callback)
```

コールバックのシグネチャは`(err, entries)`です。

ストリームイベントを直接管理せずに、コールバック方式で処理する場合に適しています。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const zip = require('archive/zip');

zip.zip('payload', function(err, archive) {
	if (err) throw err;
	zip.unzip(archive, function(err2, entries) {
		if (err2) throw err2;
		console.println(entries[0].name, new Uint8Array(entries[0].data).length);
	});
});
```

## createZip() {#createzip}

ストリーム形式のZIP writerを作成します。

返されるオブジェクトは、`write()`でエントリを受け取り、`end()`が呼び出されると、`data`イベントでアーカイブのバイト列を出力します。

このAPIはイベント駆動ですが、Node.jsのファイルストリームのように中間結果を逐次出力せず、`end()`の時点で処理を完了します。

<h6>構文</h6>

```js
createZip()
```

## createUnzip() {#createunzip}

ストリーム形式のZIP readerを作成します。

アーカイブのバイト列を`write()`で渡してから`end()`を呼び出すと、展開した項目ごとに`entry`イベントが発生します。

<h6>構文</h6>

```js
createUnzip()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const zip = require('archive/zip');
const writer = zip.createZip();
let archive = null;

writer.on('data', function(chunk) {
	archive = chunk;
});

writer.on('end', function() {
	const reader = zip.createUnzip();
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

## Zip {#zip-1}

`Zip`は、ZIPアーカイブの作成、保存、読み込み、展開を行うファイル指向のヘルパークラスです。

<h6>コンストラクター</h6>

```js
new zip.Zip(filePath?)
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

対応するZIPエントリのフィールドは以下のとおりです。

- `name` `String` 必須のエントリパス
- `data` `String | ArrayBuffer | Uint8Array | Number[]` ファイルの内容
- `comment` `String` エントリの説明
- `method` `Number` 圧縮方式

`addFile()`は、ディスク上にあるファイルをまとめる最も簡単な方法です。
`addBuffer()`は、メモリ上で生成した内容を直接追加する場合に適しています。
`addEntry()`は、`comment`などのエントリのメタデータも指定する場合に便利です。

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
const zip = require('archive/zip');

const z = new zip.Zip();
z.addBuffer('hello world', 'app.log');
z.addEntry({ name: 'config.json', data: '{"enabled":true}' });
z.writeTo('/tmp/data.zip');

const saved = new zip.Zip('/tmp/data.zip');
saved.extractAllTo('/tmp/out', {
	overwrite: true,
	filter: function(entry) {
		return entry.name === 'app.log';
	}
});
```

<h6>使用例: ファイルをまとめて再展開する</h6>

```js {linenos=table,linenostart=1}
const fs = require('fs');
const zip = require('archive/zip');
const base = '/tmp/zip-files';

fs.mkdir(base + '/input', { recursive: true });
fs.writeFile(base + '/input/one.txt', 'One', 'utf8');
fs.writeFile(base + '/input/two.txt', 'Two', 'utf8');

const archive = new zip.Zip();
archive.addFile(base + '/input/one.txt');
archive.addFile(base + '/input/two.txt', 'renamed-two.txt');
archive.writeTo(base + '/sample.zip');

const loaded = new zip.Zip(base + '/sample.zip');
loaded.extractAllTo(base + '/out', true);
console.println(fs.readFile(base + '/out/renamed-two.txt', 'utf8'));
```

<h6>使用例: 条件付きの展開</h6>

```js {linenos=table,linenostart=1}
const zip = require('archive/zip');
const fs = require('fs');
const base = '/tmp/zip-filter';

const archive = zip.zipSync([
	{ name: 'keep/a.txt', data: 'A' },
	{ name: 'keep/b.log', data: 'B' },
	{ name: 'skip/c.txt', data: 'C' }
]);

fs.writeFile(base + '.zip', Array.from(new Uint8Array(archive)), 'buffer');

const loaded = new zip.Zip(base + '.zip');
loaded.extractAllTo(base + '-out', {
	overwrite: true,
	filter: /\.txt$/
});
```

## 注意 {#참고}

- `filter`には、コールバック、`RegExp`、文字列、エントリ名の配列を使用できます。
- `extractAllTo()`は、対象ファイルが存在し、`overwrite`が`false`の場合にエラーを発生させます。
- ZIPエントリのメタデータには、`comment`、`method`、`compressedSize`、`size`を含む場合があります。
- ZIPエントリは、TARの`symlink`や`linkname`のようなリンクメタデータには対応していません。
