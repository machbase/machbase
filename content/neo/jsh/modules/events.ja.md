---
toc: true
title: "events"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`events`モジュールは、JSHで使用できるシンプルな`EventEmitter`実装を提供します。
複数のJSH組み込みモジュールが、イベント駆動APIの基底クラスとしてこの実装を使用します。

一般的な使用方法は以下のとおりです。

```js
const EventEmitter = require('events');
```

## EventEmitter {#eventemitter}

新しいイベントエミッターのインスタンスを作成します。

<h6>構文</h6>

```js
new EventEmitter()
```

イベント名ごとにリスナーを保存します。変更を行うメソッドの多くはエミッター自身を返すため、呼び出しを連鎖できます。

## on() {#on}

イベントリスナーを登録します。

<h6>構文</h6>

```js
emitter.on(event, listener)
```

`listener`は関数である必要があります。それ以外は`TypeError`が発生します。

## addListener() {#addlistener}

`on()`の別名です。

<h6>構文</h6>

```js
emitter.addListener(event, listener)
```

## once() {#once}

1回だけ実行するリスナーを登録します。

<h6>構文</h6>

```js
emitter.once(event, listener)
```

最初の呼び出し後に自動的に削除されます。

## removeListener() {#removelistener}

一致するリスナーを1つ削除します。

<h6>構文</h6>

```js
emitter.removeListener(event, listener)
```

## off() {#off}

`removeListener()`の別名です。

<h6>構文</h6>

```js
emitter.off(event, listener)
```

## removeAllListeners() {#removealllisteners}

指定したイベントのすべてのリスナーを削除します。引数を省略すると、すべてのイベントリスナーを削除します。

<h6>構文</h6>

```js
emitter.removeAllListeners()
emitter.removeAllListeners(event)
```

## emit() {#emit}

イベントを発生させ、残りの引数をリスナーに渡します。

<h6>構文</h6>

```js
emitter.emit(event, ...args)
```

<h6>戻り値</h6>

- 対応するイベントにリスナーが1つ以上ある場合は`true`
- ない場合は`false`

`error`以外のイベント処理中にリスナーが例外をスローし、エミッターに`error`リスナーがある場合は、`emit('error', err)`でそのエラーを渡します。

## 状態取得ヘルパー {#조회-helper}

### listeners() {#listeners}

指定したイベントに登録済みのリスナー配列の浅いコピーを返します。

```js
emitter.listeners(event)
```

### listenerCount() {#listenercount}

イベントに登録済みのリスナー数を返します。

```js
emitter.listenerCount(event)
```

### eventNames() {#eventnames}

現在登録済みのイベント名一覧を返します。

```js
emitter.eventNames()
```

## リスナー数の制限 {#listener-제한}

### setMaxListeners() {#setmaxlisteners}

リスナー数の警告しきい値を設定します。

```js
emitter.setMaxListeners(n)
```

### getMaxListeners() {#getmaxlisteners}

現在のリスナー数の警告しきい値を返します。

```js
emitter.getMaxListeners()
```

既定の最大値は、イベントごとに`10`個です。
この上限を超えると、`console.warn()`で警告を出力しますが、リスナーの登録自体は阻止しません。

## 使用例 {#사용-예시}

```js {linenos=table,linenostart=1}
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.on('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## once() 例 {#once-예시}

```js {linenos=table,linenostart=1}
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.once('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## 動作に関する注意 {#동작-참고}

- このモジュールは、`EventEmitter`クラスを直接エクスポートします。
- これは軽量な実装であり、Node.jsの`events`を完全に置き換えるものではありません。
- `emit()`ではリスナー配列をコピーして走査するため、イベント発生中にリスナーを削除しても、その回の配信には影響しません。
- リスナー数超過の警告のみを行い、登録自体はブロックしません。
