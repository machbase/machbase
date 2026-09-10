---
toc: true
title: グローバル
type: docs
weight: 900
---

追加のモジュールを読み込まずに使用できる、グローバル関数とオブジェクトです。

タイマーAPIはJSHイベントループの実装を使用し、`console`オブジェクトは標準出力とログ
出力を提供します。

## setTimeout() {#settimeout}

指定した時間（ミリ秒）が経過した後、コールバックを1回実行します。

追加の引数は、そのままコールバック関数に渡されます。

<h6>構文</h6>

```js
setTimeout(callback, delayMs[, ...args])
```

<h6>戻り値</h6>

- タイマーハンドルオブジェクト。`clearTimeout()`に渡すと実行を取り消せます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3,4]}
setTimeout((name, count) => {
	console.println("Timeout with args:", name, count);
}, 50, "test", 42);

// 出力：
// Timeout with args: test 42
```

## clearTimeout() {#cleartimeout}

`setTimeout()`で登録した処理がまだ実行されていない場合は、取り消します。

実行済みまたは取り消し済みのタイマーに再度呼び出しても、追加の動作は行いません。

<h6>構文</h6>

```js
clearTimeout(timer)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const timer = setTimeout(() => {
	console.println("should not run");
}, 100);

clearTimeout(timer);
clearTimeout(timer);
```

## setInterval() {#setinterval}

指定した間隔（ミリ秒）でコールバックを繰り返し実行します。

繰り返し実行を停止するには、返されたハンドルを`clearInterval()`に渡します。

<h6>構文</h6>

```js
setInterval(callback, delayMs[, ...args])
```

<h6>戻り値</h6>

- インターバルハンドルオブジェクト。`clearInterval()`に渡すと繰り返し実行を停止できます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,6]}
let count = 0;
const timer = setInterval(() => {
	count++;
	console.println("count:", count);
	if (count >= 3) {
		clearInterval(timer);
	}
}, 100);
```

## clearInterval() {#clearinterval}

`setInterval()`で登録した繰り返し処理を停止します。

<h6>構文</h6>

```js
clearInterval(interval)
```

## setImmediate() {#setimmediate}

現在の実行が終了した後、次のイベントループでできるだけ早くコールバックを実行します。

タイマーの遅延を使わずに、非同期の後続処理を予約する場合に便利です。

<h6>構文</h6>

```js
setImmediate(callback[, ...args])
```

<h6>戻り値</h6>

- 即時実行処理のハンドルオブジェクト。`clearImmediate()`に渡すと実行を取り消せます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
console.println("Add event loop");
setImmediate(() => {
	console.println("event loop called");
});

// 出力：
// Add event loop
// event loop called
```

## clearImmediate() {#clearimmediate}

`setImmediate()`で予約したコールバックがまだ実行されていない場合は、取り消します。

<h6>構文</h6>

```js
clearImmediate(immediate)
```

## console {#console}

グローバルな`console`オブジェクトは、ログ出力と標準出力のメソッドを提供します。

## console.log() {#consolelog}

情報レベルのログを出力します。出力にはレベルを表す`INFO`が含まれます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
console.log("Hello, World!");

// 出力：
// INFO  Hello, World!
```

## console.debug() {#consoledebug}

デバッグレベルのログを出力します。

## console.info() {#consoleinfo}

情報レベルのログを出力します。`console.log()`と同じレベルを使用します。

## console.warn() {#consolewarn}

警告レベルのログを出力します。

## console.error() {#consoleerror}

エラーレベルのログを出力します。

## console.print() {#consoleprint}

値を続けて出力し、末尾に改行を追加しません。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
console.print("hello", "world");

// 出力：
// helloworld
```

## console.println() {#consoleprintln}

値の間に空白を挿入して出力し、末尾に改行を追加します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
console.println("hello", "world");

// 出力：
// hello world
```

## console.printf() {#consoleprintf}

書式文字列を使用して出力します。

<h6>構文</h6>

```js
console.printf(format, ...args)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
console.printf("value=%d, name=%s\n", 42, "neo");

// 出力：
// value=42, name=neo
```

