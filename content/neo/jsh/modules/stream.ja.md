---
toc: true
title: "stream"
type: docs
weight: 100
draft: true
---

`stream`モジュールは、JSHアプリケーションで使用できるNode.js形式の基本的なストリーム型を提供します。
Goの`io.Reader`と`io.Writer`のラッパーに加え、JavaScriptで実装した`Transform`とメモリ上の`PassThrough`ストリームを提供します。

一般的な使用方法は以下のとおりです。

```js
const { Readable, Writable, Duplex, PassThrough, Transform } = require('stream');
```

## エクスポートされるクラス {#exported-classes}

- `Readable`
- `Writable`
- `Duplex`
- `PassThrough`
- `Transform`

## Readable {#readable}

ネイティブのreaderをラップして、読み取り可能なストリームインターフェースを提供します。

<h6>構文</h6>

```js
new Readable(reader)
```

- `reader`は、Goの`io.Reader`を基盤とするネイティブオブジェクトである必要があります。

<h6>メソッド</h6>

- `read([size])`: 次のチャンクを読み取り、`Buffer`または`null`を返します。
- `readString([size[, encoding]])`: 次のチャンクを読み取り、文字列で返します。
- `pause()`: ストリームを一時停止状態にし、ネイティブのpauseシグナルを送ります。
- `resume()`: ストリームをデータ送出状態にし、ネイティブのresumeシグナルを送ります。
- `isPaused()`: 現在の一時停止状態を返します。
- `pipe(destination[, options])`: `data`イベントを書き込み可能な接続先に渡します。既定では、入力元が終了すると接続先でも`end()`を呼び出します。
- `unpipe([destination])`: パイプ接続を解除します。現在の実装では、入力元の`data`リスナーを削除します。
- `destroy([error])`: ストリームを閉じます。`error`がある場合は、先にそのイベントを発生させます。
- `close()`: `destroy()`の別名です。

<h6>プロパティ</h6>

- `readable`
- `readableEnded`
- `readableFlowing`
- `readableHighWaterMark`

<h6>イベント</h6>

- `data`
- `end`
- `error`
- `close`
- `pause`
- `resume`

## Writable {#writable}

ネイティブのwriterをラップして、書き込み可能なストリームインターフェースを提供します。

<h6>構文</h6>

```js
new Writable(writer)
```

- `writer`は、Goの`io.Writer`を基盤とするネイティブオブジェクトである必要があります。

<h6>メソッド</h6>

- `write(chunk[, encoding][, callback])`: チャンクを書き込みます。`string`、`Buffer`、`Uint8Array`型に対応しています。
- `end([chunk][, encoding][, callback])`: 必要に応じて最後のチャンクを書き込み、書き込み側を終了します。
- `destroy([error])`: ストリームを閉じます。`error`がある場合は、先にそのイベントを発生させます。
- `close()`: `destroy()`の別名です。

`write()`は、成功時に`true`を返します。書き込みできない場合やエラーが発生した場合は`false`を返します。

<h6>プロパティ</h6>

- `writable`
- `writableEnded`
- `writableFinished`
- `writableHighWaterMark`

<h6>イベント</h6>

- `finish`
- `error`
- `close`

## Duplex {#duplex}

読み取りと書き込みを1つのストリームに統合した型です。

<h6>構文</h6>

```js
new Duplex(reader, writer)
```

- `reader`は、Goの`io.Reader`を基盤とする必要があります。
- `writer`は、Goの`io.Writer`を基盤とする必要があります。

`Duplex`は、`Readable`の読み取りメソッドと`Writable`の書き込みメソッドを提供し、`pipe()`、`pause()`、`resume()`、`isPaused()`、`destroy()`、`close()`にも対応しています。

## PassThrough {#passthrough}

書き込んだデータをそのまま通過させる、メモリ上の双方向ストリームを作成します。

<h6>構文</h6>

```js
new PassThrough()
```

`PassThrough`は、テスト、一時的なバッファリング、外部のネイティブreader/writerを使わずにストリーム形式のコードを接続する場合に便利です。

<h6>使用例</h6>

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

## Transform {#transform}

JavaScriptで独自の変換処理を作成するための基底クラスです。

<h6>構文</h6>

```js
new Transform([options])
```

現在のコンストラクターは省略可能な`options`オブジェクトを受け取りますが、組み込み実装が使用するオプションはまだありません。

<h6>サブクラスのフック</h6>

- `_transform(chunk, encoding, callback)`: 入力チャンクを処理するようにオーバーライドします。
- `_flush(callback)`: 終了直前に残りの出力を送出するようにオーバーライドします。

現在のランタイムでは、`_transform()`内から直接出力します。バイトチャンクには`this.push(...)`を使用し、オブジェクト形式の出力では`data`を直接発生させる方式がより安全です。コールバックの第2の値は、組み込み実装では使用しません。

<h6>メソッド</h6>

- `write(chunk[, encoding][, callback])`
- `end([chunk][, encoding][, callback])`
- `push(chunk)`: 読み取り側に出力を渡します。`null`を渡すと読み取り側が終了します。
- `pipe(destination[, options])`
- `destroy([error])`
- `pause()`
- `resume()`

<h6>使用例</h6>

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

## 共通の動作 {#common-behavior}

- エクスポートされるすべてのクラスは、`EventEmitter`を継承します。
- `Readable`、`Writable`、`Duplex`、`PassThrough`の高水位マークは、`16384`に固定されています。
- EOFでは、`read()`は`null`、`readString()`は空文字列を返し、`readableEnded`を更新します。
- 書き込みストリームの`end()`は、書き込み側を終了状態にして`finish`を発生させます。基盤となるストリームが閉じられると、`close`が発生します。
- `Transform.end()`は、`finish`を発生させた後、内部で`push(null)`を呼び出して読み取り側も終了します。

## 互換性に関する注意 {#compatibility-notes}

- このモジュールはNode.jsに似たAPIを提供しますが、Node.jsストリームを完全に置き換えるものではありません。
- 現在の`Readable.unpipe()`は接続先を個別に追跡せず、入力元の`data`リスナーを削除します。
- `Transform`は、サブクラスを作成し、`_transform()`内から直接出力する方式での使用に適しています。
- JSHでは、バイト形式の変換は`this.push(...)`を使い、オブジェクト形式のパーサーは`data`を直接発生させる方式がより安全です。
