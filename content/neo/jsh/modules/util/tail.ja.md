---
toc: true
title: "tail"
type: docs
weight: 120
---

`util/tail`モジュールは、単一ファイルを`tail -F`のように追跡する、ポーリング方式のtailerを提供します。
呼び出し元が`setInterval()`で`poll()`を定期的に呼び出す方式を前提に設計されています。

次の形式で使用できます。

- `require('util/tail')`

## tail.create() {#tailcreate}

tailerのインスタンスを作成します。

<h6>構文</h6>

```js
tail.create(path, options)
```

<h6>パラメーター</h6>

- `path` `String`: 追跡するファイルのパス
- `options` `Object`:
  - `fromStart` `Boolean` (既定値： `false`)
    - `false`: 作成時点のファイル末尾から追跡
    - `true`: 作成時点のファイル先頭から読み取り

<h6>返されるオブジェクト</h6>

| メソッド/フィールド | 型 | 説明 |
|:------------|:-----|:-----|
| `path` | String | 作成時に指定したパス |
| `poll(callback?)` | Function | 新しい行を読み取り、`String[]`で返す |
| `close()` | Function | ファイルハンドルを閉じてtailerを終了 |

`poll(callback?)`の動作：

- 戻り値: 新たに検出した行の配列（`String[]`）
- `callback`を渡すと、同じ配列をコールバック引数にも渡す
- 読み取る新しい行がなければ空配列を返す
- ポーリング時にファイルの切り詰め・ローテーションを反映

## 基本的な使用例 {#기본-사용-예시}

```js {linenos=table,linenostart=1}
const tail = require('util/tail');

const follower = tail.create('/tmp/app.log', { fromStart: false });

const tm = setInterval(function () {
    const lines = follower.poll(function (arr) {
        // arrはString[]
    });

    for (let i = 0; i < lines.length; i++) {
        console.println(lines[i]);
    }
}, 500);

// クリーンアップの例
setTimeout(function () {
    clearInterval(tm);
    follower.close();
}, 10_000);
```

## SSEアダプター {#sse-어댑터}

`util/tail/sse`は、tailの結果をSSE形式で出力するアダプターです。

- `require('util/tail/sse')`
- `require('util/tail').sse`

### tail/sse.create() {#tailssecreate}

<h6>構文</h6>

```js
tailSSE.create(path, options)
```

<h6>パラメーター</h6>

- `path` `String`: 追跡するファイルのパス
- `options` `Object`:
  - `fromStart` `Boolean` (既定値： `false`)
  - `event` `String` (既定値： 空文字列)
  - `retryMs` `Number` (省略可能)
  - `write` `Function` (省略可能)
    - 出力関数を省略すると`process.stdout.write()`を使用

<h6>返されるオブジェクト</h6>

| メソッド | 説明 |
|:-------|:-----|
| `writeHeaders()` | SSEレスポンスヘッダーを出力 |
| `poll()` | 新しい行を読み取り、`event/data`フレームを出力して`String[]`を返す |
| `send(data, event?)` | 任意のデータ1件をSSEフレームとして出力 |
| `comment(text)` | SSEコメントフレーム（`: ...`）を出力 |
| `close()` | 内部のtailerを終了 |

## cgi-bin SSE 例 {#cgi-bin-sse-예시}

```js {linenos=table,linenostart=1}
const tailSSE = require('util/tail/sse');
const process = require('process');

const path = process.env.get('SCRIPT_NAME');
const target = '/work/'+path.substring(0, path.lastIndexOf('/')) + '/app.log';

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

process.on('SIGTERM', function () {
    clearInterval(timer);
    adapter.close();
    process.exit(0);
});
```

## 動作に関する注意 {#동작-참고}

- ポーリング間隔とライフサイクル（終了・クリーンアップ）は、呼び出し元が制御します。
- ファイルが存在しない場合、`poll()`は空配列を返し、ファイル作成後の次のポーリングで追跡を開始します。
- ローテーションと切り詰めは、ポーリング時に検出して反映します。
