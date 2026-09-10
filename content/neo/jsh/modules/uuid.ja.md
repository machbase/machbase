---
toc: true
title: "uuid"
type: docs
weight: 100
draft: true
---

## UUID {#uuid}

UUIDジェネレーターです。

<h6>構文</h6>

{{< neo_since ver="8.0.75" />}}
```js
new UUID(ver)
```

<h6>パラメーター</h6>

`ver` UUIDのバージョン。1、4、6、7のいずれかを指定します。

<h6>戻り値</h6>

新しいUUIDジェネレーターオブジェクト。

### eval() {#eval}

<h6>構文</h6>

```js
eval()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

`String` 生成されたUUID。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const {UUID} = require("@jsh/generator")
gen = new UUID(1);
for(i=0; i < 3; i++) {
    console.log(gen.eval());
}

// 868c8ec0-2180-11f0-b223-8a17cad8d69c
// 868c97b2-2180-11f0-b223-8a17cad8d69c
// 868c98d4-2180-11f0-b223-8a17cad8d69c
```
