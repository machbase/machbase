---
title: "zip"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`archive/zip` 모듈은 JSH에서 ZIP 아카이브를 생성하고 해제하는 기능을 제공합니다.
메모리 기반 헬퍼, 스트림 스타일 API, 파일 기반 `Zip` 클래스를 지원합니다.

작업 방식에 따라 다음 API를 선택하면 됩니다.

- 아카이브가 이미 메모리에 있다면 `zipSync()`, `unzipSync()`를 사용합니다.
- 파일을 읽어 `.zip` 파일로 저장하거나 디스크로 추출하려면 `Zip` 클래스를 사용합니다.
- 이벤트 기반으로 처리하려면 `createZip()`, `createUnzip()`를 사용합니다.

## 설치

```js
const zip = require('archive/zip');
```

## zipSync()

ZIP 아카이브를 동기 방식으로 생성합니다.

<h6>사용 형식</h6>

```js
zipSync(data)
```

<h6>파라미터</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

`data`가 단일 문자열 또는 바이트 버퍼이면 생성되는 엔트리 이름은 기본적으로 `data`가 됩니다.
배열을 전달하면 각 요소는 `{ name, data }` 형태의 엔트리 객체로 처리됩니다.

<h6>반환값</h6>

ZIP 아카이브 바이트를 담은 `ArrayBuffer`를 반환합니다.

이 방식은 간단한 테스트를 하거나, 아카이브를 먼저 메모리에서 만든 뒤 다른 곳에 저장할 때 유용합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,6]}
const zip = require('archive/zip');
const archive = zip.zipSync([
	{ name: 'alpha.txt', data: 'Alpha' },
	{ name: 'dir/beta.txt', data: 'Beta' }
]);
console.println(archive.constructor.name);
```

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const zip = require('archive/zip');
const archive = zip.zipSync('hello zip');
const entries = zip.unzipSync(archive);
console.println(entries[0].name, new Uint8Array(entries[0].data).length);
```

## unzipSync()

ZIP 아카이브 바이트를 동기 방식으로 해제하여 엔트리 객체 배열을 반환합니다.

<h6>사용 형식</h6>

```js
unzipSync(buffer)
```

<h6>파라미터</h6>

- `buffer` `ArrayBuffer | Uint8Array | Number[]`

<h6>반환값</h6>

엔트리 객체 배열을 반환합니다.

각 엔트리에는 `name`, `data`, `comment`, `method`, `compressedSize`, `size`, `isDir`,
`modified` 필드가 포함될 수 있습니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[6,7,8]}
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

## zip()

ZIP 생성 기능의 콜백 스타일 비동기 래퍼입니다.

<h6>사용 형식</h6>

```js
zip(data, callback)
```

콜백 시그니처는 `(err, archive)`입니다.

## unzip()

ZIP 해제 기능의 콜백 스타일 비동기 래퍼입니다.

<h6>사용 형식</h6>

```js
unzip(buffer, callback)
```

콜백 시그니처는 `(err, entries)`입니다.

스트림 이벤트를 직접 다루지 않고 콜백 기반 흐름으로 처리하고 싶을 때 이 래퍼가 적합합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,4,5]}
const zip = require('archive/zip');

zip.zip('payload', function(err, archive) {
	if (err) throw err;
	zip.unzip(archive, function(err2, entries) {
		if (err2) throw err2;
		console.println(entries[0].name, new Uint8Array(entries[0].data).length);
	});
});
```

## createZip()

스트림 스타일 ZIP writer를 생성합니다.

반환된 객체는 `write()`로 엔트리를 받고, `end()`가 호출되면 `data` 이벤트로 아카이브 바이트를 내보냅니다.

이 API는 이벤트 기반이지만, Node.js 파일 스트림처럼 중간 결과를 계속 내보내기보다는 `end()` 시점에 작업을 마무리하는 방식에 가깝습니다.

<h6>사용 형식</h6>

```js
createZip()
```

## createUnzip()

스트림 스타일 ZIP reader를 생성합니다.

아카이브 바이트를 `write()`로 전달한 뒤 `end()`를 호출하면, 추출된 각 항목에 대해 `entry` 이벤트가 발생합니다.

<h6>사용 형식</h6>

```js
createUnzip()
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[5,10,14,15]}
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

## Zip

`Zip`은 ZIP 아카이브를 만들고, 저장하고, 읽고, 추출하기 위한 파일 지향 헬퍼 클래스입니다.

<h6>생성자</h6>

```js
new zip.Zip(filePath?)
```

`filePath`를 지정하면 해당 파일에서 아카이브를 읽어옵니다.

### addFile()

파일 시스템의 파일을 읽어 아카이브 엔트리로 추가합니다.

```js
addFile(filePath[, entryName])
```

### addBuffer()

문자열 또는 바이트 버퍼를 아카이브 엔트리로 추가합니다.

```js
addBuffer(data, entryName[, options])
```

### addEntry()

엔트리 객체를 직접 추가합니다.

```js
addEntry(entry)
```

지원되는 ZIP 엔트리 필드는 다음과 같습니다.

- `name` `String` 필수 엔트리 경로
- `data` `String | ArrayBuffer | Uint8Array | Number[]` 파일 내용
- `comment` `String` 엔트리 설명
- `method` `Number` 압축 방식

`addFile()`은 이미 디스크에 있는 파일을 묶을 때 가장 간단합니다.
`addBuffer()`는 메모리에서 생성한 내용을 바로 넣을 때 적합합니다.
`addEntry()`는 `comment` 같은 엔트리 메타데이터를 함께 지정하고 싶을 때 유용합니다.

### getEntries()

현재 아카이브 엔트리의 얕은 복사본을 반환합니다.

```js
getEntries()
```

### writeTo()

아카이브를 파일로 저장합니다.

```js
writeTo(filePath)
```

### extractAllTo()

엔트리를 디렉터리로 추출합니다.

```js
extractAllTo(outputDir[, overwrite])
extractAllTo(outputDir, options)
extractAllTo(outputDir, overwrite, options)
```

`options`는 다음 값을 지원합니다.

- `overwrite` `Boolean` `true`이면 기존 파일을 덮어씁니다.
- `filter` `Function | RegExp | String | String[]` 추출할 엔트리를 선택합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[6,9,10]}
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

<h6>사용 예시: 파일을 묶고 다시 추출하기</h6>

```js {linenos=table,linenostart=1,hl_lines=[8,9,12,14]}
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

<h6>사용 예시: 조건부 추출</h6>

```js {linenos=table,linenostart=1,hl_lines=[8,13,18]}
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

## 참고

- `filter`는 콜백, `RegExp`, 문자열, 엔트리 이름 배열을 사용할 수 있습니다.
- `extractAllTo()`는 대상 파일이 이미 존재하고 `overwrite`가 `false`이면 오류를 발생시킵니다.
- ZIP 엔트리 메타데이터에는 `comment`, `method`, `compressedSize`, `size`가 포함될 수 있습니다.
- ZIP 엔트리는 TAR의 `symlink`, `linkname` 같은 링크 메타데이터를 지원하지 않습니다.
