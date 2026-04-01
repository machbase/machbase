---
title: "interp"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## PiecewiseConstant

The `PiecewiseConstant` performs piecewise constant interpolation on a dataset. 
It approximates the value of a function by using the nearest data point in each interval. 
This method is useful for step-like data.

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.PiecewiseConstant();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 30
```

## PiecewiseLinear

The `PiecewiseLinear` performs piecewise linear interpolation on a dataset. 
It approximates the value of a function by connecting data points with straight lines. 
This method is useful for smooth transitions between data points.

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.PiecewiseLinear();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## AkimaSpline

The `AkimaSpline` performs Akima spline interpolation on a dataset. 
This method creates a smooth curve that passes through the data points, avoiding oscillations in regions with sparse data.

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.AkimaSpline();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## FritschButland

The `FritschButland` performs Fritsch-Butland interpolation on a dataset. 
This method ensures monotonicity in the interpolated values, making it suitable for datasets where preserving order is important.

**Usage example**

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

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.LinearRegression();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## ClampedCubic

The `ClampedCubic` performs linear clamped-cubic interpolation on a dataset. 
It predicts the value of a function at a given point using the best-fit line derived from the data.

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.ClampedCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NaturalCubic

The `ClampedCubic` performs linear natural-cubic interpolation on a dataset. 
It predicts the value of a function at a given point using the best-fit line derived from the data.

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.NaturalCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NotAKnotCubic

The `ClampedCubic` performs linear not-a-knot cubic spline interpolation on a dataset. 
It predicts the value of a function at a given point using the best-fit line derived from the data.

**Usage example**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4];
y = [10, 20, 30, 40];
interp = new m.NotAKnotCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```
