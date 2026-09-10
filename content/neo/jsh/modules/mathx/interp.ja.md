---
toc: true
title: "interp"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## PiecewiseConstant {#piecewiseconstant}

データセットに区分定数補間を適用します。各区間の近傍データ点を使って関数値を近似するため、階段状のデータに適しています。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.PiecewiseConstant();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 30
```

## PiecewiseLinear {#piecewiselinear}

データ点を直線で結ぶ区分線形補間を提供します。データ点間を滑らかに遷移させる場合に便利です。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.PiecewiseLinear();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## AkimaSpline {#akimaspline}

Akimaスプライン補間により、データ点を通る滑らかな曲線を生成し、データが疎な領域での振動を抑えます。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.AkimaSpline();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## FritschButland {#fritschbutland}

Fritsch-Butland補間を適用し、補間値の単調性を維持します。値の順序を保つ必要があるデータセットに適しています。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.FritschButland();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## LinearRegression {#linearregression}

`LinearRegression`は、データセットに線形回帰に基づく補間を適用します。 
データから得た最良適合直線を使い、指定した点での関数値を予測します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.LinearRegression();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## ClampedCubic {#clampedcubic}

境界での傾きを指定するクランプ三次補間を提供します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.ClampedCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NaturalCubic {#naturalcubic}

自然境界条件を使用する三次補間です。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.NaturalCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NotAKnotCubic {#notaknotcubic}

Not-a-Knot条件を適用する三次スプライン補間です。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.NotAKnotCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```
