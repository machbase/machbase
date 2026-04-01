---
title: "interp"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## PiecewiseConstant

계단형 데이터를 위해 구간별 상수 보간을 수행합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.PiecewiseConstant();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 30
```

## PiecewiseLinear

데이터 지점을 직선으로 연결하는 구간별 선형 보간을 제공합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.PiecewiseLinear();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## AkimaSpline

Akima 스플라인 보간으로 매끄러운 곡선을 생성합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.AkimaSpline();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## FritschButland

단조성을 유지하는 Fritsch-Butland 보간을 수행합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.FritschButland();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## LinearRegression

The `LinearRegression` performs linear regression-based interpolation on a dataset. 
It predicts the value of a function at a given point using the best-fit line derived from the data.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.LinearRegression();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## ClampedCubic

경계 기울기를 지정하는 클램프 cubic 보간을 제공합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.ClampedCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NaturalCubic

자연 경계 조건을 사용하는 cubic 보간입니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.NaturalCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NotAKnotCubic

Not-a-Knot 조건을 적용한 cubic 스플라인 보간입니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.NotAKnotCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```
