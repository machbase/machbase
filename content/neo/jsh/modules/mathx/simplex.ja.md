---
toc: true
title: "simplex"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## Simplex {#simplex}

Simplexノイズアルゴリズムに基づくノイズジェネレーターです。

<h6>構文</h6>

```js
new Simplex(seed)
```

<h6>パラメーター</h6>

`seed` 乱数のシード値。

<h6>戻り値</h6>

新しいSimplexジェネレーターオブジェクト。

### eval() {#eval}

入力値に応じた決定的なノイズ値を返します。同じ引数を使用すると、常に同じ結果になります。

<h6>構文</h6>

```js
eval(arg1)
eval(arg1, arg2)
eval(arg1, arg2, arg3)
eval(arg1, arg2, arg3, arg4)
```

<h6>パラメーター</h6>

`args` `Number` 次元を表す可変長の数値リスト。1次元から4次元まで、1〜4個の引数を指定できます。

<h6>戻り値</h6>

`Number` ノイズ値。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const g = require("mathx/simplex")
simplex = new g.Simplex(123);
for(i=0; i < 5; i++) {
    noise = simplex.eval(i, i * 0.6).toFixed(3);
    console.log(i, (i*0.6).toFixed(1), "=>", noise);
}

// 0 0.0 => 0.000
// 1 0.6 => 0.349
// 2 1.2 => 0.319
// 3 1.8 => 0.038
// 4 2.4 => -0.364
```
