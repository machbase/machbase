---
title: "@jsh/analysis"
type: docs
weight: 70
---

## sort()

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
console.log(ana.sort([1.3, 1.2, 1.1]))

// [1.1, 1.2, 1.3]
```

## sum()

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
console.log(ana.sum([3, 1, 2]))
console.log(ana.sum([1.3, 1.2, 1.1]))

// 6
// 3.6
```

## cdf()

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
x = [];
for( i=1; i<=100; i++) {
    x.push(i);
}
console.log(ana.cdf(1.0, x))

// 0.01
```

## mean

**Usage example**

```js {linenos=table,linenostart=1}
```

## circularMean

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
x = [0, 0.25 * Math.PI, 0.75 * Math.PI];
w = [1, 2, 2.5];
console.log(ana.circularMean(x).toFixed(4))
console.log(ana.circularMean(x, w).toFixed(4))

// 0.9553
// 1.3704
```

## correlation

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
x = [8, -3, 7, 8, -4];
y = [10, 5, 6, 3, -1];
w = [2, 1.5, 3, 3, 2];
console.log(ana.correlation(x, y).toFixed(5))
console.log(ana.correlation(x, y, w).toFixed(5))

// 0.61922
// 0.59915
```

## covariance

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
x = [8, -3, 7, 8, -4];
y1 = [10, 2, 2, 4, 1];
y2 = [12, 1, 11, 12, 0];
console.log(ana.covariance(x, y1).toFixed(4))
console.log(ana.covariance(x, y2).toFixed(4))
console.log(ana.variance(x).toFixed(4))

// 13.8000
// 37.7000
// 37.7000
```

## entropy

**Usage example**

```js {linenos=table,linenostart=1}
const ana = require("@jsh/analysis")
console.log(ana.entropy([0.05, 0.1, 0.9, 0.05]).toFixed(4));
console.log(ana.entropy([0.2, 0.4, 0.25, 0.15]).toFixed(4));
console.log(ana.entropy([0.2, 0, 0, 0.5, 0, 0.2, 0.1, 0, 0, 0]).toFixed(4));
console.log(ana.entropy([0, 0, 1, 0]).toFixed(4));

// 0.6247
// 1.3195
// 1.2206
// 0.0000
```

## geometricMean

**Usage example**

```js {linenos=table,linenostart=1}
```

## harmonicMean

**Usage example**

```js {linenos=table,linenostart=1}
```

## median

**Usage example**

```js {linenos=table,linenostart=1}
```

## quantile

**Usage example**

```js {linenos=table,linenostart=1}
```

## meanStdDev

**Usage example**

```js {linenos=table,linenostart=1}
```

## mode

**Usage example**

```js {linenos=table,linenostart=1}
```

## moment

**Usage example**

```js {linenos=table,linenostart=1}
```

## stdDev

**Usage example**

```js {linenos=table,linenostart=1}
```

## stdErr

**Usage example**

```js {linenos=table,linenostart=1}
```

## linearRegression

**Usage example**

```js {linenos=table,linenostart=1}
```

## fft

**Usage example**

```js {linenos=table,linenostart=1}
```

## interpPiecewiseConstant

**Usage example**

```js {linenos=table,linenostart=1}
```

## interpPiecewiseLinear

**Usage example**

```js {linenos=table,linenostart=1}
```

## interpAkimaSpline

**Usage example**

```js {linenos=table,linenostart=1}
```

## interpFritschButland

**Usage example**

```js {linenos=table,linenostart=1}
```

## interpLinearRegression

**Usage example**

```js {linenos=table,linenostart=1}
```
