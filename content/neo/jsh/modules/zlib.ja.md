---
toc: true
title: "zlib"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`zlib`モジュールは、JSHアプリケーション用にNode.js形式の圧縮・展開APIを提供します。
gzip、deflate、raw deflate、自動検出によるunzip、同期ヘルパー、コールバック方式の非同期ヘルパー、ストリーム形式の処理に対応しています。

一般的な使用方法は以下のとおりです。

```js
const zlib = require('zlib');
```

## 同期メソッド {#동기-메서드}

これらのメソッドは、`ArrayBuffer`を返します。

### gzipSync() {#gzipsync}

gzip形式でデータを圧縮します。

```js
gzipSync(data)
```

### gunzipSync() {#gunzipsync}

gzipデータを展開します。

```js
gunzipSync(data)
```

### deflateSync() {#deflatesync}

deflate形式でデータを圧縮します。

```js
deflateSync(data)
```

### inflateSync() {#inflatesync}

deflateデータを展開します。

```js
inflateSync(data)
```

### deflateRawSync() {#deflaterawsync}

raw deflate形式でデータを圧縮します。

```js
deflateRawSync(data)
```

### inflateRawSync() {#inflaterawsync}

raw deflateデータを展開します。

```js
inflateRawSync(data)
```

### unzipSync() {#unzipsync}

gzipまたはdeflateデータの形式を自動検出して展開します。

```js
unzipSync(data)
```

<h6>入力型</h6>

圧縮メソッドは、`String`またはバイナリ入力を受け取ります。
展開メソッドには、圧縮されたバイナリ入力を指定します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const zlib = require('zlib');

const compressed = zlib.gzipSync('Hello, World!');
const decompressed = zlib.gunzipSync(compressed);
const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
console.println(text);
```

## 非同期メソッド {#비동기-메서드}

これらのメソッドはコールバック方式です。

### gzip(), gunzip(), deflate(), inflate(), deflateRaw(), inflateRaw(), unzip() {#gzip-gunzip-deflate-inflate-deflateraw-inflateraw-unzip}

<h6>構文</h6>

```js
gzip(data, callback)
gunzip(data, callback)
deflate(data, callback)
inflate(data, callback)
deflateRaw(data, callback)
inflateRaw(data, callback)
unzip(data, callback)
```

コールバックのシグネチャは以下のとおりです。

```js
(err, result) => {}
```

`result`は、`ArrayBuffer`で渡されます。

<h6>使用例</h6>

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

## ストリーム生成メソッド {#스트림-생성-메서드}

このモジュールは、ストリーム形式の圧縮・展開オブジェクトも提供します。

- `createGzip()`
- `createGunzip()`
- `createDeflate()`
- `createInflate()`
- `createDeflateRaw()`
- `createInflateRaw()`
- `createUnzip()`

各ファクトリーは、以下のメンバーを持つzlibストリームオブジェクトを返します。

| メンバー | 説明 |
|:-----|:-----|
| `write(data)` | 入力データをストリームに書き込む |
| `end([data])` | 必要に応じて最後のチャンクを書き込み、ストリームを終了 |
| `on(event, callback)` | `data`、`end`、`error`イベントのリスナーを登録 |
| `pipe(dest[, options])` | 出力データを別の書き込み可能な接続先に渡す |
| `flush()` | 対応している場合、保留中の圧縮出力をフラッシュ |
| `close()` | 内部の圧縮・展開オブジェクトを閉じる |
| `bytesWritten` | これまで受け取った入力のバイト数 |
| `bytesRead` | これまで生成した出力のバイト数 |

## ストリーミングの例 {#스트리밍-예시}

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

## pipe() {#pipe}

`pipe()`は、次の接続先に対応しています。

- `write(chunk)`と、省略可能な`end()`を持つJavaScriptの書き込み先
- `writer`として公開されたネイティブwriterを基盤とするオブジェクト

既定では、`pipe()`はzlibストリームの終了時に接続先の`end()`も呼び出します。
この動作は、`{ end: false }`で無効にできます。

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

## 進捗の追跡 {#진행률-추적}

ストリームオブジェクトは、実行中のバイトカウンターを提供します。

- `bytesWritten`: 消費した入力の合計バイト数
- `bytesRead`: 生成した出力の合計バイト数

カウンターはデータ送出中に継続して更新されるため、`data`コールバック内でも確認できます。

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

## constants {#constants}

このモジュールは、zlib定数を`zlib.constants`としてエクスポートします。

代表的な値：

- `Z_NO_FLUSH`、`Z_SYNC_FLUSH`、`Z_FINISH`などのフラッシュ定数
- `Z_NO_COMPRESSION`、`Z_BEST_SPEED`、`Z_BEST_COMPRESSION`、`Z_DEFAULT_COMPRESSION`などの圧縮レベル定数
- `Z_OK`、`Z_STREAM_END`、`Z_DATA_ERROR`などの状態・戻り値の定数

```js {linenos=table,linenostart=1}
const { constants } = require('zlib');

console.println(constants.Z_BEST_COMPRESSION);
```

## 互換性に関する注意 {#호환성-참고}

- APIはNode.jsに似ていますが、Node.jsの`zlib`を完全に置き換えるものではありません。
- ストリームの`on()`は、`data`、`end`、`error`のコールバックのみに対応しています。
- 各zlibストリームはイベントの種類ごとにコールバックを1つだけ保存するため、同じイベントに後から登録した`on()`が以前のコールバックを置き換えます。
- 非同期ヘルパーはコールバック方式のみで、Promise方式は提供しません。
