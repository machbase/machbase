---
title: "mathx"
type: docs
weight: 100
---

{{< neo_since ver="8.0.74" />}}


## arrange()

등차수열 형태의 숫자 배열을 생성합니다.

<h6>사용 형식</h6>

```js
arrange(start, end, step)
```

<h6>매개변수</h6>

- `start` `Number` 시작값
- `end` `Number` 종료값
- `step` `Number` 증가 폭

<h6>반환값</h6>

`Number[]` 생성된 숫자 배열.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { arrange } = require('mathx');
arrange(0, 6, 3).forEach((i) => console.log(i));

// 0
// 3
// 6
```

## linspace()

지정한 구간을 균등 간격으로 분할한 배열을 생성합니다.

<h6>사용 형식</h6>

```js
linspace(start, end, count)
```

<h6>매개변수</h6>

- `start` `Number` 시작값
- `end` `Number` 종료값
- `count` `Number` 생성할 요소 개수

<h6>반환값</h6>

`Number[]` 생성된 숫자 배열.

<h6>사용 예시</h6>


```js {linenos=table,linenostart=1}
const { linspace } = require('mathx');
linspace(0, 1, 3).forEach((i) => console.log(i));

// 0
// 1.5
// 1
```

## meshgrid()

두 배열의 조합을 기반으로 격자를 생성합니다.

<h6>사용 형식</h6>

```js
meshgrid(arr1, arr2)
```

<h6>매개변수</h6>

- `arr1` `Number[]` 첫 번째 배열
- `arr2` `Number[]` 두 번째 배열

<h6>반환값</h6>

`Number[][]` 숫자 쌍으로 구성된 배열.

<h6>사용 예시</h6>


```js {linenos=table,linenostart=1}
const { meshgrid } = require('mathx');

const gen = meshgrid([1, 2, 3], [4, 5]);
for(i=0; i < gen.length; i++) {
    console.log(JSON.stringify(gen[i]));
}

// [1,4]
// [1,5]
// [2,4]
// [2,5]
// [3,4]
// [3,5]
```

## sort()

배열을 오름차순으로 정렬합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.sort([1.3, 1.2, 1.1])); // [1.1, 1.2, 1.3]
```

## sum()

배열의 합계를 계산합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.sum([3, 1, 2]));       // 6
console.log(m); // 3.6
```

## cdf()

누적 분포 함수(CDF)를 계산합니다. 주어진 `x` 데이터에서 `q` 이하인 비율을 반환합니다.

<h6>사용 형식</h6>

```js
cdf(q, x, weights)
```

- `q` `Number` 기준 값
- `x` `Number[]` 오름차순으로 정렬된 데이터
- `weights` `Number[]` 가중치 배열(생략 시 모두 1, 지정 시 `x`와 길이가 같아야 합니다.)

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [];
for( i=1; i<=100; i++) {
    x.push(i);
}
x = m.sort(x);
console.log(m.cdf(1.0, x)); // 0.01
```

## mean()

산술 평균을 계산합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.mean([1, 2, 3, 4, 5]));  // 3
console.log(m.mean([10, 20, 30]));     // 20
```

## circularMean()

라디안 각도와 같이 순환하는 값을 대상으로 평균을 구합니다. 가중치 배열을 지정할 수도 있습니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [0, 0.25 * Math.PI, 0.75 * Math.PI];
w = [1, 2, 2.5];
console.log(m.circularMean(x).toFixed(4));     // 0.9553
console.log(m.circularMean(x, w).toFixed(4));  // 1.3704
```

## correlation()

두 데이터셋 간 피어슨 상관 계수를 계산합니다. -1~1 범위이며 가중치를 지정할 수도 있습니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [8, -3, 7, 8, -4];
y = [10, 5, 6, 3, -1];
w = [2, 1.5, 3, 3, 2];
console.log(m.correlation(x, y).toFixed(5));     // 0.61922
console.log(m.correlation(x, y, w).toFixed(5));  // 0.59915
```

## covariance()

두 데이터셋 간 공분산을 계산합니다. 양수면 함께 증가하는 경향, 음수면 반대로 움직이는 경향을 의미합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [8, -3, 7, 8, -4];
y1 = [10, 2, 2, 4, 1];
y2 = [12, 1, 11, 12, 0];
console.log(m.covariance(x, y1).toFixed(4)); // 13.8000
console.log(m.covariance(x, y2).toFixed(4)); // 37.7000
console.log(m.variance(x).toFixed(4));       // 37.7000
```

## entropy()

샤논 엔트로피를 계산해 분포의 불확실성을 측정합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.entropy([0.05, 0.1, 0.9, 0.05]).toFixed(4)); // 0.6247
console.log(m.entropy([0.2, 0.4, 0.25, 0.15]).toFixed(4)); // 1.3195
console.log(m.entropy([0.2, 0, 0, 0.5, 0, 0.2, 0.1, 0, 0, 0]).toFixed(4)); // 1.2206
console.log(m.entropy([0, 0, 1, 0]).toFixed(4));           // 0.0000
```

## geometricMean()

양수 배열의 기하 평균을 계산합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.geometricMean([1, 3, 9]).toFixed(4));  // 3.0000
console.log(m.geometricMean([2, 8, 32]).toFixed(4)); // 8.0000
```

## harmonicMean()

양수 배열의 조화 평균을 계산합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.harmonicMean([1, 2, 4]).toFixed(4));    // 1.7143
console.log(m.harmonicMean([10, 20, 30]).toFixed(4)); // 16.3636
```

## median()

정렬된 배열의 중앙값을 반환합니다. 짝수 개라면 두 중앙값의 평균을 돌려줍니다.

입력 배열은 오름차순으로 정렬되어 있어야 합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.median(m.sort([1, 3, 2, 5, 4])));      // 3
console.log(m.median(m.sort([10, 20, 30, 40, 50]))); // 30
```

## medianInterp()

`median`과 동일하지만, 선형 보간을 적용한 값을 반환합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.medianInterp(m.sort([1, 3, 2, 5, 4])));      // 2.5
console.log(m.medianInterp(m.sort([10, 20, 30, 40, 50]))); // 25
```

## quantile()

The `quantile` function calculates the quantile of a given dataset for a specified probability. 
Quantiles divide the dataset into intervals with equal probabilities, such as quartiles (4 intervals) or percentiles (100 intervals). 
This function is useful for understanding the distribution of data.

<h6>사용 형식</h6>

```js
quantile(p, x, weights)
```

- `p` `Number`
- `x` `Number[]` The `x` data must be sorted in increasing order.
- `weights` `Number[]` If weights is not specified then all of the weights are 1. If weights is specified, then length of `x` must equal length of `weights`.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = m.sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
console.log(m.quantile(0.25, data)); // 3
console.log(m.quantile(0.5, data));  // 5
console.log(m.quantile(0.74, data)); // 8
```

## quantileInterp()

`quantile`과 동일하지만 선형 보간 값을 반환합니다.

<h6>사용 형식</h6>

```js
quantileInterp(p, x, weights)
```

- `p` `Number` 백분위 비율
- `x` `Number[]` 정렬된 데이터
- `weights` `Number[]` 가중치 배열(선택)

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = m.sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
console.log(m.quantileInterp(0.25, data)); // 2.5
console.log(m.quantileInterp(0.5, data));  // 5
console.log(m.quantileInterp(0.74, data)); // 7.4
```

## meanStdDev()

평균과 표준편차를 동시에 계산합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = [1, 2, 3, 4, 5];
result = m.meanStdDev(data);
console.log(result.mean.toFixed(2));   // 3.00
console.log(result.stdDev.toFixed(2)); // 1.58
```

## mode()

최빈값을 계산합니다. 결과는 `{value: number, count: number}` 형태입니다.

<h6>사용 형식</h6>

```js
mode(x, weights)
```

- `x` `Number[]` 정렬된 데이터
- `weights` `Number[]` 가중치 배열(선택)

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = m.sort([1, 2, 2, 3, 4]);
console.log(m.mode(data)); // {value:2, count:2}
data = m.sort([1, 1, 2, 3, 4]);
console.log(m.mode(data)); // {value:1, count:2}
```

## moment()

n차 모멘트를 계산합니다. 분포 형태(왜도·첨도 등)를 분석할 때 사용합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = [1, 2, 3, 4, 5];
console.log(m.moment(2, data).toFixed(4)); // 2.5000
console.log(m.moment(4, data).toFixed(4)); // 6.8000
```

## stdDev()

표준편차를 계산합니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.stdDev([1, 2, 3, 4, 5]).toFixed(4));      // 1.5811
console.log(m.stdDev([10, 20, 30, 40, 50]).toFixed(4)); // 15.8114
```

## stdErr()

표본 평균의 표준 오차를 계산합니다. 표준편차를 표본 크기의 제곱근으로 나눈 값입니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
let stddev = m.stdDev([1, 2, 3, 4, 5]);
let sampleSize = 5;
console.log(m.stdErr(stddev, sampleSize).toFixed(4)); // 0.7071
```

## linearRegression()

두 데이터셋을 대상으로 선형 회귀를 수행합니다. 결과는 `y = alpha*x + beta` 형태의 `{slope: alpha, intercept: beta}`입니다.

**사용 예시**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4, 5];
y = [2, 4, 6, 8, 10];
result = m.linearRegression(x, y);
console.log(result.slope.toFixed(4));     // 2.0000
console.log(result.intercept.toFixed(4)); // 0.0000
```

## fft()

빠른 푸리에 변환(FFT)을 수행하여 주파수 성분을 분석합니다.

```js
fft(times, amplitudes)
```

`times`와 `amplitudes` 길이는 동일해야 합니다.

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
