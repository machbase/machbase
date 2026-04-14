---
title: "tail"
type: docs
weight: 120
---

The `util/tail` module provides a polling-based single-file follower with behavior similar to `tail -F`.
It is designed for caller-managed lifecycle: the caller periodically invokes `poll()` (typically with `setInterval()`).

It is available:

- `require('util/tail')`

## tail.create()

Creates a tailer instance.

<h6>Syntax</h6>

```js
tail.create(path, options)
```

<h6>Parameters</h6>

- `path` `String`: Target file path to follow.
- `options` `Object`:
  - `fromStart` `Boolean` (default: `false`)
    - `false`: Start following from the current end of file.
    - `true`: Start reading from the beginning on first poll.

<h6>Returned object</h6>

| Method/Field | Type | Description |
|:-------------|:-----|:------------|
| `path` | String | Path used to create the tailer |
| `poll(callback?)` | Function | Reads newly appended lines and returns `String[]` |
| `close()` | Function | Closes file handle and ends the tailer |

`poll(callback?)` behavior:

- Return value: array of newly detected lines (`String[]`)
- If `callback` is provided, the same array is passed to the callback
- Returns an empty array when there are no new lines
- Reflects truncate/rotation state at poll time

## Basic usage example

```js {linenos=table,linenostart=1}
const tail = require('util/tail');

const follower = tail.create('/tmp/app.log', { fromStart: false });

const tm = setInterval(function () {
    const lines = follower.poll(function (arr) {
        // arr is String[]
    });

    for (let i = 0; i < lines.length; i++) {
        console.println(lines[i]);
    }
}, 500);

// cleanup example
setTimeout(function () {
    clearInterval(tm);
    follower.close();
}, 10_000);
```

## SSE adapter

`util/tail/sse` is an adapter that emits tail output as SSE frames.

- `require('util/tail/sse')`
- `require('util/tail').sse`

### tail/sse.create()

<h6>Syntax</h6>

```js
tailSSE.create(path, options)
```

<h6>Parameters</h6>

- `path` `String`: Target file path to follow.
- `options` `Object`:
  - `fromStart` `Boolean` (default: `false`)
  - `event` `String` (default: empty string)
  - `retryMs` `Number` (optional)
  - `write` `Function` (optional)
    - If omitted, output is written to `process.stdout.write()`

<h6>Returned object</h6>

| Method | Description |
|:-------|:------------|
| `writeHeaders()` | Writes SSE response headers |
| `poll()` | Reads new lines, emits SSE `event/data` frames, returns `String[]` |
| `send(data, event?)` | Emits one arbitrary SSE event payload |
| `comment(text)` | Emits an SSE comment frame (`: ...`) |
| `close()` | Closes the internal tailer |

## cgi-bin SSE example

```js {linenos=table,linenostart=1}
const tailSSE = require('util/tail/sse');

const target = process.env.QUERY_FILE || '/tmp/app.log';
const intervalMs = Number(process.env.QUERY_INTERVAL_MS || 500);

const adapter = tailSSE.create(target, {
    fromStart: false,
    event: 'log',
    retryMs: 1500,
});

adapter.writeHeaders();

const timer = setInterval(function () {
    try {
        adapter.poll();
    } catch (err) {
        adapter.send(String(err), 'error');
        clearInterval(timer);
        adapter.close();
        process.exit(0);
    }
}, intervalMs);

process.on('SIGINT', function () {
    clearInterval(timer);
    adapter.close();
    process.exit(0);
});
```

## Behavior notes

- Polling cadence and lifecycle (cleanup/stop) are controlled by the caller.
- If the file does not exist, `poll()` returns an empty array; following begins after the file appears.
- Rotation and truncation are detected and applied at poll time.
