---
toc: true
title: "path"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`path`モジュールは、Node.jsに似たパス操作のヘルパーを提供します。
JSHの既定のエクスポートはPOSIX実装で、`path.posix`と`path.win32`の名前空間も提供します。

一般的な使用方法は以下のとおりです。

```js
const path = require('path');
```

## 既定のエクスポート {#기본-export}

`require('path')`は、POSIXパスの実装を返します。

既定の動作は以下のとおりです。

- パス区切り文字は`/`
- リスト区切り文字は`:`
- `join()`や`resolve()`などの関数はPOSIX形式で動作

次の名前空間も使用できます。

- `path.posix`
- `path.win32`

## 共通プロパティ {#공통-속성}

| プロパティ | POSIX | win32 |
|:-----|:------|:------|
| `sep` | `/` | `\\` |
| `delimiter` | `:` | `;` |

## resolve() {#resolve}

複数のパス要素を絶対パスに解決します。

<h6>構文</h6>

```js
path.resolve(...segments)
```

既定の実装では、基準パスが必要な場合に現在の作業ディレクトリを使用します。

## normalize() {#normalize}

パス区切り文字を正規化し、`.`と`..`のセグメントを解決します。

<h6>構文</h6>

```js
path.normalize(value)
```

## isAbsolute() {#isabsolute}

パスが絶対パスかどうかを返します。

<h6>構文</h6>

```js
path.isAbsolute(value)
```

## join() {#join}

現在のパス形式に従ってパス要素を結合し、結果を正規化します。

<h6>構文</h6>

```js
path.join(...segments)
```

## relative() {#relative}

あるパスから別のパスへの相対パスを返します。

<h6>構文</h6>

```js
path.relative(from, to)
```

## dirname() {#dirname}

パスのディレクトリ部分を返します。

<h6>構文</h6>

```js
path.dirname(value)
```

## basename() {#basename}

パスの最後の構成要素を返します。
`ext`を指定すると、一致する接尾辞を除去します。

<h6>構文</h6>

```js
path.basename(value)
path.basename(value, ext)
```

## extname() {#extname}

先頭のドットを含むファイル拡張子を返します。

<h6>構文</h6>

```js
path.extname(value)
```

## parse() {#parse}

パスを構造化したフィールドに分解します。

<h6>構文</h6>

```js
path.parse(value)
```

<h6>戻り値</h6>

`parse()`は、以下のフィールドを持つオブジェクトを返します。

- `root`
- `dir`
- `base`
- `ext`
- `name`

## format() {#format}

解析済みのパスオブジェクトからパス文字列を構成します。

<h6>構文</h6>

```js
path.format(pathObject)
```

`pathObject`には、`dir`、`root`、`base`、`name`、`ext`を指定できます。

## 使用例 {#사용-예시}

```js {linenos=table,linenostart=1}
const path = require('path');

console.println(path.join('/work', 'demo', 'file.txt'));
console.println(path.dirname('/work/demo/file.txt'));
console.println(path.basename('/work/demo/file.txt', '.txt'));
console.println(path.extname('/work/demo/file.txt'));
```

## parse()/format() 例 {#parseformat-예시}

```js {linenos=table,linenostart=1}
const path = require('path');

const parsed = path.parse('/work/demo/file.txt');
console.println(JSON.stringify(parsed));

const rebuilt = path.format({
    dir: '/work/demo',
    name: 'file',
    ext: '.txt'
});
console.println(rebuilt);
```

## POSIX / win32名前空間 {#posix--win32-namespace}

既定の動作に関係なくPOSIXまたはWindowsのパス規則を明示的に使用するには、`path.posix`または`path.win32`を指定します。

```js {linenos=table,linenostart=1}
const path = require('path');

console.println(path.posix.join('/a', 'b', 'c.txt'));
console.println(path.win32.join('C:\\temp', 'demo', 'file.txt'));
```

## 動作に関する注意 {#동작-참고}

- JSHの既定のエクスポートはPOSIXに基づきます。
- 公開関数では、該当する引数に文字列が必要です。入力が不正な場合は`TypeError`が発生します。
- `parse()`と`format()`は、Node.jsに似たオブジェクト構造を使用します。
- JSHをWindows以外のシステムで実行している場合も、`path.win32`を使用できます。
