---
title: "zlib"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

The `zlib` module provides Node.js-style compression and decompression APIs for JSH applications.
It supports gzip, deflate, raw deflate, auto-detected unzip, synchronous helpers, callback-based asynchronous helpers, and stream-style processing.

Typical usage looks like this.

```js
const zlib = require('zlib');
```

## Synchronous methods

These methods return an `ArrayBuffer`.

### gzipSync()

Compresses data using gzip.

```js
gzipSync(data)
```

### gunzipSync()

Decompresses gzip data.

```js
gunzipSync(data)
```

### deflateSync()

Compresses data using deflate.

```js
deflateSync(data)
```

### inflateSync()

Decompresses deflate data.

```js
inflateSync(data)
```

### deflateRawSync()

Compresses data using raw deflate.

```js
deflateRawSync(data)
```

### inflateRawSync()

Decompresses raw deflate data.

```js
inflateRawSync(data)
```

### unzipSync()

Decompresses gzip or deflate data using automatic format detection.

```js
unzipSync(data)
```

<h6>Input type</h6>

Compression methods accept `String` or binary input.
Decompression methods expect compressed binary input.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

const compressed = zlib.gzipSync('Hello, World!');
const decompressed = zlib.gunzipSync(compressed);
const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
console.println(text);
```

## Asynchronous methods

These methods are callback-based.

### gzip(), gunzip(), deflate(), inflate(), deflateRaw(), inflateRaw(), unzip()

<h6>Syntax</h6>

```js
gzip(data, callback)
gunzip(data, callback)
deflate(data, callback)
inflate(data, callback)
deflateRaw(data, callback)
inflateRaw(data, callback)
unzip(data, callback)
```

The callback signature is:

```js
(err, result) => {}
```

`result` is returned as an `ArrayBuffer`.

<h6>Usage example</h6>

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

## Stream factory methods

The module also provides stream-style compression and decompression objects.

- `createGzip()`
- `createGunzip()`
- `createDeflate()`
- `createInflate()`
- `createDeflateRaw()`
- `createInflateRaw()`
- `createUnzip()`

Each factory returns a zlib stream object with these members.

| Member | Description |
|:-------|:------------|
| `write(data)` | Writes input data into the stream. |
| `end([data])` | Optionally writes one final chunk and finishes the stream. |
| `on(event, callback)` | Registers a listener for `data`, `end`, or `error`. |
| `pipe(dest[, options])` | Pipes stream output to another writable destination. |
| `flush()` | Flushes pending compression output when supported. |
| `close()` | Closes the underlying compression/decompression object. |
| `bytesWritten` | Number of input bytes accepted so far. |
| `bytesRead` | Number of output bytes produced so far. |

## Streaming example

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

`pipe()` supports:

- JavaScript writable destinations with `write(chunk)` and optional `end()`
- native writer-backed objects exposed as `writer`

By default, `pipe()` calls the destination's `end()` when the zlib stream ends.
You can disable that behavior with `{ end: false }`.

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

## Progress tracking

Streaming objects expose running byte counters.

- `bytesWritten`: total input bytes consumed
- `bytesRead`: total output bytes produced

These counters are updated while data flows, so they can be checked inside `data` callbacks.

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

The module exports zlib constants as `zlib.constants`.

Representative values include:

- flush constants such as `Z_NO_FLUSH`, `Z_SYNC_FLUSH`, `Z_FINISH`
- compression levels such as `Z_NO_COMPRESSION`, `Z_BEST_SPEED`, `Z_BEST_COMPRESSION`, `Z_DEFAULT_COMPRESSION`
- return/status constants such as `Z_OK`, `Z_STREAM_END`, `Z_DATA_ERROR`

```js {linenos=table,linenostart=1}
const { constants } = require('zlib');

console.println(constants.Z_BEST_COMPRESSION);
```

## Compatibility notes

- The API shape is Node.js-like, but it is not a full drop-in replacement for Node.js `zlib`.
- Stream `on()` supports `data`, `end`, and `error` callbacks only.
- Each zlib stream stores one callback per event type; later `on()` calls for the same event replace the previous callback.
- Async helpers are callback-based only; promise-based variants are not provided.