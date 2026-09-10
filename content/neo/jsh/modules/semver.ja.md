---
toc: true
title: "semver"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`semver`モジュールは、JSHアプリケーションにセマンティックバージョンの比較機能を提供します。

一般的な使用方法は以下のとおりです。

```js
const semver = require('semver');
```

## エクスポートされる関数 {#내보내는-함수}

- `satisfies(version, constraint)`
- `maxSatisfying(versions, constraint)`
- `compare(left, right)`

## satisfies() {#satisfies}

バージョンがセマンティックバージョンの制約を満たすかどうかを確認します。

<h6>構文</h6>

```js
semver.satisfies(version, constraint)
```

<h6>パラメーター</h6>

- `version` `String`
- `constraint` `String`

<h6>戻り値</h6>

`version`が`constraint`を満たす場合は`true`、それ以外は`false`を返します。

空の制約と`latest`は、`*`として扱います。

## maxSatisfying() {#maxsatisfying}

制約を満たすバージョンのうち、最も高いバージョンを返します。

<h6>構文</h6>

```js
semver.maxSatisfying(versions, constraint)
```

<h6>パラメーター</h6>

- `versions` `String[]`
- `constraint` `String`

<h6>戻り値</h6>

最も適合する元のバージョン文字列を返します。
一致するバージョンがない場合は、空文字列を返します。

形式が不正な候補バージョンはスキップします。

## compare() {#compare}

2つのセマンティックバージョンを比較します。

<h6>構文</h6>

```js
semver.compare(left, right)
```

<h6>パラメーター</h6>

- `left` `String`
- `right` `String`

<h6>戻り値</h6>

- `-1`: `left < right`
- `0`: `left === right`
- `1`: `left > right`

## 使用例 {#사용-예제}

```js {linenos=table,linenostart=1}
const semver = require('semver');

console.println(semver.satisfies('1.4.2', '1.2 - 1.4'));
console.println(semver.satisfies('2.0.0', '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.2.0', '1.4.2', '2.0.0'], '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.0.0', '1.1.4', '1.2.0'], '~1.1'));
console.println(semver.compare('1.1.0', '1.2.0'));
console.println(semver.compare('1.2.0', '1.1.0'));
console.println(semver.compare('1.2.0', '1.2.0'));
```

## 動作に関する注意 {#동작-메모}

- `version`、`left`、`right`、`constraint`が不正な場合は、エラーが発生します。
- バージョンと制約は、解析前に前後の空白を除去します。
- 制約の解析は、`1.2 - 1.4`、`~1.1`などの範囲表現に対応する内部のセマンティックバージョン規則に従います。
