---
title: "zlib"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`zlib` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 스타일 압축/해제 API를 제공합니다.
gzip, deflate, raw deflate, auto-detected unzip, 동기 helper, callback 기반 비동기 helper, stream 스타일 처리를 지원합니다.

일반적으로 아래처럼 사용합니다.

```js
const zlib = require('zlib');
```

## 동기 메서드

이 메서드들은 `ArrayBuffer`를 반환합니다.

### gzipSync()

gzip 형식으로 데이터를 압축합니다.

```js
gzipSync(data)
```

### gunzipSync()

gzip 데이터를 해제합니다.

```js
gunzipSync(data)
```

### deflateSync()

deflate 형식으로 데이터를 압축합니다.

```js
deflateSync(data)
```

### inflateSync()

deflate 데이터를 해제합니다.

```js
inflateSync(data)
```

### deflateRawSync()

raw deflate 형식으로 데이터를 압축합니다.

```js
deflateRawSync(data)
```

### inflateRawSync()

raw deflate 데이터를 해제합니다.

```js
inflateRawSync(data)
```

### unzipSync()

gzip 또는 deflate 데이터를 자동 감지해 해제합니다.

```js
unzipSync(data)
```

<h6>입력 타입</h6>

압축 메서드는 `String` 또는 binary 입력을 받을 수 있습니다.
해제 메서드는 압축된 binary 입력을 기대합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

const compressed = zlib.gzipSync('Hello, World!');
const decompressed = zlib.gunzipSync(compressed);
const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
console.println(text);
```

## 비동기 메서드

이 메서드들은 callback 기반입니다.

### gzip(), gunzip(), deflate(), inflate(), deflateRaw(), inflateRaw(), unzip()

<h6>사용 형식</h6>

```js
gzip(data, callback)
gunzip(data, callback)
deflate(data, callback)
inflate(data, callback)
deflateRaw(data, callback)
inflateRaw(data, callback)
unzip(data, callback)
```

callback 시그니처는 다음과 같습니다.

```js
(err, result) => {}
```

`result`는 `ArrayBuffer`로 전달됩니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

zlib.gzip('Hello, World!', (err, compressed) => {
    if (err) {
        console.println(err.message);
        return;
    }
    zlib.gunzip(compressed, (err2, decompressed) => {
        if (err2) {
            console.println(err2.message);
            return;
        }
        const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
        console.println(text);
    });
});
```

## 스트림 생성 메서드

이 모듈은 stream 스타일 압축/해제 객체도 제공합니다.

- `createGzip()`
- `createGunzip()`
- `createDeflate()`
- `createInflate()`
- `createDeflateRaw()`
- `createInflateRaw()`
- `createUnzip()`

각 factory는 다음 멤버를 가진 zlib stream 객체를 반환합니다.

| 멤버 | 설명 |
|:-----|:-----|
| `write(data)` | 입력 데이터를 stream에 기록 |
| `end([data])` | 필요하면 마지막 chunk를 기록하고 stream 종료 |
| `on(event, callback)` | `data`, `end`, `error` 이벤트 리스너 등록 |
| `pipe(dest[, options])` | 출력 데이터를 다른 writable destination으로 전달 |
| `flush()` | 지원되는 경우 대기 중인 압축 출력을 flush |
| `close()` | 내부 압축/해제 객체를 종료 |
| `bytesWritten` | 지금까지 받아들인 입력 바이트 수 |
| `bytesRead` | 지금까지 생성한 출력 바이트 수 |

## 스트리밍 예시

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

const gzip = zlib.createGzip();
gzip.on('data', (chunk) => {
    console.println('compressed bytes:', chunk.byteLength);
});
gzip.on('end', () => {
    console.println('done');
});

gzip.write('Hello, ');
gzip.end('World!');
```

## pipe()

`pipe()`는 다음 destination을 지원합니다.

- `write(chunk)`와 선택적 `end()`를 가진 JavaScript writable destination
- `writer`로 노출된 native writer-backed 객체

기본적으로 `pipe()`는 zlib stream이 끝날 때 destination의 `end()`도 호출합니다.
이 동작은 `{ end: false }`로 끌 수 있습니다.

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

const gzip = zlib.createGzip();
const dest = {
    write(chunk) {
        return true;
    },
    end() {
        console.println('dest ended');
    }
};

gzip.pipe(dest, { end: false });
gzip.write('hello');
gzip.end();
```

## 진행률 추적

stream 객체는 실행 중 byte counter를 제공합니다.

- `bytesWritten`: 소비한 입력 바이트 총량
- `bytesRead`: 생성한 출력 바이트 총량

이 counter는 데이터가 흐르는 동안 계속 갱신되므로 `data` callback 안에서도 확인할 수 있습니다.

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

const compressed = zlib.gzipSync('NAME,AGE\nAlice,30\nBob,25\n');
const gunzip = zlib.createGunzip();

gunzip.on('data', function(chunk) {
    console.println('input bytes:', gunzip.bytesWritten);
    console.println('output bytes:', gunzip.bytesRead);
});

gunzip.write(compressed);
gunzip.end();
```

## constants

모듈은 zlib 상수들을 `zlib.constants`로 export합니다.

대표적인 값:

- `Z_NO_FLUSH`, `Z_SYNC_FLUSH`, `Z_FINISH` 같은 flush 상수
- `Z_NO_COMPRESSION`, `Z_BEST_SPEED`, `Z_BEST_COMPRESSION`, `Z_DEFAULT_COMPRESSION` 같은 압축 레벨 상수
- `Z_OK`, `Z_STREAM_END`, `Z_DATA_ERROR` 같은 상태/반환 상수

```js {linenos=table,linenostart=1}
const { constants } = require('zlib');

console.println(constants.Z_BEST_COMPRESSION);
```

## 호환성 참고

- API 모양은 Node.js와 비슷하지만, Node.js `zlib`의 완전한 drop-in replacement는 아닙니다.
- stream의 `on()`은 `data`, `end`, `error` callback만 지원합니다.
- 각 zlib stream은 이벤트 타입별 callback을 하나만 저장하므로, 같은 이벤트에 대해 나중에 등록한 `on()`이 이전 callback을 대체합니다.
- 비동기 helper는 callback 기반만 제공하며 promise 기반 variant는 없습니다.