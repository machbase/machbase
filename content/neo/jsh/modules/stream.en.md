---
title: "stream"
type: docs
weight: 100
draft: true
---

The `stream` module provides Node.js-style stream primitives for JSH applications.
It wraps native Go `io.Reader` and `io.Writer` objects and also provides pure JavaScript `Transform` and in-memory `PassThrough` stream types.

Typical usage looks like this.

```js
const { Readable, Writable, Duplex, PassThrough, Transform } = require('stream');
```

## Exported classes

- `Readable`
- `Writable`
- `Duplex`
- `PassThrough`
- `Transform`

## Readable

Wraps a native reader and exposes a readable stream interface.

<h6>Syntax</h6>

```js
new Readable(reader)
```

- `reader` must be a native object backed by Go's `io.Reader`.

<h6>Methods</h6>

- `read([size])`: Reads the next chunk and returns a `Buffer` or `null`.
- `readString([size[, encoding]])`: Reads the next chunk and returns a string.
- `pause()`: Marks the stream as paused and emits a native pause signal.
- `resume()`: Marks the stream as flowing and emits a native resume signal.
- `isPaused()`: Returns the current paused state.
- `pipe(destination[, options])`: Forwards `data` events to a writable destination. By default, the destination is ended when the source ends.
- `unpipe([destination])`: Stops piping. The current implementation clears `data` listeners on the source stream.
- `destroy([error])`: Closes the stream and optionally emits `error` first.
- `close()`: Alias of `destroy()`.

<h6>Properties</h6>

- `readable`
- `readableEnded`
- `readableFlowing`
- `readableHighWaterMark`

<h6>Events</h6>

- `data`
- `end`
- `error`
- `close`
- `pause`
- `resume`

## Writable

Wraps a native writer and exposes a writable stream interface.

<h6>Syntax</h6>

```js
new Writable(writer)
```

- `writer` must be a native object backed by Go's `io.Writer`.

<h6>Methods</h6>

- `write(chunk[, encoding][, callback])`: Writes a chunk. Supported chunk types are `string`, `Buffer`, and `Uint8Array`.
- `end([chunk][, encoding][, callback])`: Optionally writes one final chunk and then closes the writable side.
- `destroy([error])`: Closes the stream and optionally emits `error` first.
- `close()`: Alias of `destroy()`.

`write()` returns `true` on success and `false` when the stream is no longer writable or an error occurs.

<h6>Properties</h6>

- `writable`
- `writableEnded`
- `writableFinished`
- `writableHighWaterMark`

<h6>Events</h6>

- `finish`
- `error`
- `close`

## Duplex

Combines the readable and writable sides in a single stream.

<h6>Syntax</h6>

```js
new Duplex(reader, writer)
```

- `reader` must be backed by Go's `io.Reader`.
- `writer` must be backed by Go's `io.Writer`.

`Duplex` supports the same read-side methods as `Readable` and the same write-side methods as `Writable`, including `pipe()`, `pause()`, `resume()`, `isPaused()`, `destroy()`, and `close()`.

## PassThrough

Creates an in-memory duplex stream that passes written data through unchanged.

<h6>Syntax</h6>

```js
new PassThrough()
```

`PassThrough` is useful for tests, buffering, and connecting stream-like code without requiring an external native reader or writer.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { PassThrough } = require('stream');

const stream = new PassThrough();
stream.on('data', (chunk) => {
    console.println(chunk.toString());
});

stream.write('Hello, ');
stream.end('stream');

const data = stream.read();
if (data !== null) {
    console.println(data.toString());
}
```

## Transform

Base class for custom transforms implemented in JavaScript.

<h6>Syntax</h6>

```js
new Transform([options])
```

The current constructor accepts an optional `options` object, but the built-in implementation does not consume any options yet.

<h6>Subclass hooks</h6>

- `_transform(chunk, encoding, callback)`: Override to process incoming chunks.
- `_flush(callback)`: Override to emit any remaining output before finishing.

In this runtime, `_transform()` is expected to emit output itself by calling `this.push(...)` for byte chunks, or by emitting `data` directly for object-style output. The second callback value is not used by the built-in implementation.

<h6>Methods</h6>

- `write(chunk[, encoding][, callback])`
- `end([chunk][, encoding][, callback])`
- `push(chunk)`: Pushes output to the readable side. Passing `null` ends the readable side.
- `pipe(destination[, options])`
- `destroy([error])`
- `pause()`
- `resume()`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { Transform } = require('stream');

class UpperCase extends Transform {
    _transform(chunk, encoding, callback) {
        this.push(chunk.toString('utf8').toUpperCase());
        callback();
    }
}

const stream = new UpperCase();
stream.on('data', (chunk) => console.println(chunk.toString()));
stream.write('hello');
stream.end();
```

## Common behavior

- All exported classes inherit from `EventEmitter`.
- `Readable`, `Writable`, `Duplex`, and `PassThrough` use a fixed high-water mark of `16384`.
- `read()` and `readString()` return `null` or an empty string on EOF and update `readableEnded`.
- `end()` on writable streams marks the writable side as ended and emits `finish`. `close` is emitted when the underlying stream is closed.
- `Transform.end()` emits `finish` and then ends the readable side by internally calling `push(null)`.

## Compatibility notes

- This module follows a Node.js-like API shape, but it is not a full drop-in replacement for Node.js streams.
- `Readable.unpipe()` currently removes `data` listeners from the source stream instead of tracking individual destinations.
- `Transform` is best used by subclassing and manually emitting output from `_transform()`.
- For byte-oriented transforms, use `this.push(...)`. For object-oriented parsers, emitting `data` directly is the safer pattern in JSH.