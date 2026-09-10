---
toc: true
title: "splitFields"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`util/splitFields`モジュールは、文字列を空白文字でフィールドに分割し、引用符で囲まれた部分は1つのフィールドとして保持します。
`require('util/splitFields')`で読み込んで使用します。

## splitFields() {#splitfields}

空白、タブ、改行、復帰を区切り文字として文字列を分割します。
単一引用符または二重引用符で囲まれたテキストは、1つのフィールドとして保持します。

<h6>構文</h6>

```js
splitFields(str[, options])
```

<h6>パラメーター</h6>

- `str` `String`: 分割する入力文字列
- `options` `Object`: 省略可能な設定オブジェクト。現在の実装では、このパラメーターを受け取りますが使用しません。

<h6>戻り値</h6>

`String[]`

## 使用例 {#사용-예시}

```js {linenos=table,linenostart=1}
const splitFields = require('util/splitFields');

console.println(JSON.stringify(splitFields('cmd "arg 1" "arg 2"')));
console.println(JSON.stringify(splitFields("hello 'world foo' bar")));
console.println(JSON.stringify(splitFields('foo\tbar\nbaz')));
```

## 動作 {#동작-방식}

- 連続する空白は、1つの区切りとして扱います。
- 空のフィールドは結果に含めません。
- 戻り値に引用符は含まれません。
- 引用符が閉じられていない場合は、文字列の末尾まで同じフィールドとして扱います。
- 引用符内のタブと改行はそのまま保持します。

## 例 {#예제}

基本的な空白での分割：

```js
splitFields('  foo   bar baz  ');
// ['foo', 'bar', 'baz']
```

二重引用符の処理：

```js
splitFields('hello "world foo" bar');
// ['hello', 'world foo', 'bar']
```

単一引用符の処理：

```js
splitFields("hello 'world foo' bar");
// ['hello', 'world foo', 'bar']
```

引用符が混在する場合の処理：

```js
splitFields("a \"b c\" d 'e f' g");
// ['a', 'b c', 'd', 'e f', 'g']
```

## 注意事項 {#참고-사항}

- 入力値は文字列である必要があります。それ以外は`TypeError`が発生します。
- 引用符内のエスケープシーケンスは特別に解釈しません。
- 完全なコマンドライン解析が不要で、シェルに似たトークン分割だけが必要な場合に便利です。
