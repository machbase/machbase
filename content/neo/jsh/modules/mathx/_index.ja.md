---
toc: true
title: "mathx"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}


## arrange() {#arrange}

等差数列の数値配列を生成します。

<h6>構文</h6>

```js
arrange(start, end, step)
```

<h6>パラメーター</h6>

- `start` `Number` 開始値
- `end` `Number` 終了値
- `step` `Number` 増分

<h6>戻り値</h6>

`Array<Number>` 生成された数値配列。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { arrange } = require('mathx');
arrange(0, 6, 3).forEach((i) => console.log(i));

// 0
// 3
// 6
```

## linspace() {#linspace}

指定した区間を等間隔に分割した配列を生成します。

<h6>構文</h6>

```js
linspace(start, end, count)
```

<h6>パラメーター</h6>

- `start` `Number` 開始値
- `end` `Number` 終了値
- `count` `Number` 生成する要素数

<h6>戻り値</h6>

`Array<Number>` 生成された数値配列。

<h6>使用例</h6>


```js {linenos=table,linenostart=1}
const { linspace } = require('mathx');
linspace(0, 1, 3).forEach((i) => console.log(i));

// 0
// 0.5
// 1
```

## meshgrid() {#meshgrid}

2つの配列の組み合わせから格子を生成します。

<h6>構文</h6>

```js
meshgrid(arr1, arr2)
```

<h6>パラメーター</h6>

- `arr1` `Array<Number>` 第1の配列
- `arr2` `Array<Number>` 第2の配列

<h6>戻り値</h6>

`Array<Array<Number>>` 数値のペアからなる配列。

<h6>使用例</h6>


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

## oscillator() {#oscillator}

{{< neo_since ver="8.5.5" />}}

`[time, value]`タプル形式の振動サンプルデータを生成します。

<h6>構文</h6>

```js
oscillator(options)
```

<h6>パラメーター</h6>

- `options` `Object`
- `options.components` `Object[]` 必須。合成する振動成分の一覧
    - `amplitude` `Number` 必須。振幅
    - `frequencyHz` `Number` 必須。周波数（Hz）
    - `phaseRad` `Number` 省略可能。位相オフセット（ラジアン）。既定値`0`
    - `bias` `Number` 省略可能。DCオフセット。既定値`0`
- `options.timeRange` `Object` 必須。時間範囲
    - `from` `Any` 必須
    - `to` `Any` 必須
    - 対応する時刻表現：
        - 数値のエポックナノ秒（例：`0`、`10000000000`）
        - 接尾辞付きのエポック文字列：`s`、`ms`、`us`、`ns`（例：`"10s"`、`"10000ms"`）
        - 文字列の時刻表現：`"now"`、`"now-10s"`
        - RFC3339/RFC3339Nano文字列
- `options.sample` `Number|String` 省略可能
    - 数値：サンプル数として解釈
    - `Hz`/`hz`接尾辞付きの文字列：サンプリング周波数として解釈（例：`"2Hz"`）
- `options.noise` `Number|Object` 省略可能
    - 数値：ノイズの振幅として解釈
    - オブジェクト：`{ amplitude, seed? }`形式。`amplitude`はノイズの強さ、`seed`は再現可能なノイズ用のシードです。

<h6>戻り値</h6>

`Array<[time, Number]>` 生成されたサンプル配列。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { oscillator } = require('mathx');

const gen = oscillator({
        components: [
                { amplitude: 1.0, frequencyHz: 0.1, phaseRad: 0 },
                { amplitude: 0.5, frequencyHz: 0.05 },
        ],
        timeRange: { from: '0s', to: '10s' },
        sample: '2Hz',
        noise: { amplitude: 0.1, seed: 123 },
});

for (let i = 0; i < gen.length; i++) {
        const t = gen[i][0];
        const v = gen[i][1];
        console.log(t, v.toFixed(2));
}
```

## series() {#series}

{{< neo_since ver="8.5.5" />}}

`[time, value]`タプルのサンプル配列を、時刻の配列と値の配列に分割します。

<h6>構文</h6>

```js
series(samples, options)
```

<h6>パラメーター</h6>

- `samples` `Array<[time, Number]>` タプルのサンプル配列
- `options` `Object` 省略可能
    - `xKey` `String` X軸配列のキー名。既定値`"time"`
    - `yKey` `String` Y軸配列のキー名。既定値`"value"`

<h6>戻り値</h6>

2つの配列を含む`Object`を返します。既定の形式は`{ time, value }`です。

<h6>使用例</h6>

```js
const m = require("mathx");
const gen = m.oscillator({
    components: [{ amplitude: 1.0, frequencyHz: 0.1 }],
    timeRange: { from: "0s", to: "10s" },
    sample: 5,
});

const s = m.series(gen);
console.log(s.time.length);  // 5
console.log(s.value.length); // 5

const custom = m.series(gen, { xKey: "ts", yKey: "amp" });
console.log(custom.ts.length);  // 5
console.log(custom.amp.length); // 5
```

## unzip() {#unzip}

{{< neo_since ver="8.5.5" />}}

タプルのサンプル配列を、2つの配列に分割します。

<h6>構文</h6>

```js
unzip(samples)
```

<h6>パラメーター</h6>

- `samples` `Array<[x, y]>` タプルのサンプル配列

<h6>戻り値</h6>

`[Array<x>, Array<y>]`

<h6>使用例</h6>

```js
const m = require("mathx");
const [x, y] = m.unzip([[1, 10], [2, 20], [3, 30]]);
console.log(x); // [1, 2, 3]
console.log(y); // [10, 20, 30]
```

## zip() {#zip}

{{< neo_since ver="8.5.5" />}}

2つの配列を、タプルのサンプル配列に結合します。

<h6>構文</h6>

```js
zip(x, y)
```

<h6>パラメーター</h6>

- `x` `Array<any>` X軸データの配列
- `y` `Array<any>` Y軸データの配列（`x`と同じ長さが必要）

<h6>戻り値</h6>

`Array<[x, y]>`

<h6>使用例</h6>

```js
const m = require("mathx");
const samples = m.zip([1, 2, 3], [10, 20, 30]);
console.log(samples[0]); // [1, 10]
```

## fft() {#fft}

高速フーリエ変換（FFT）で信号の周波数成分を分析します。信号処理やデータ分析に利用できます。

入力は2つの形式に対応し、結果を`[frequency, amplitude]`のペアの配列で返します。

<h6>構文</h6>

```js
fft(times, amplitudes) // 時刻の配列と振幅の配列
fft(timesAndAmplitudes) // [time, amplitude]の配列
```

- `fft(times, amplitudes)`
    `times`と`amplitudes`を、それぞれ別の配列で渡します。
- `fft(timesAndAmplitudes)`
    `[time, amplitude]`のペアの配列を渡します。

`times`と`amplitudes`を別の配列で渡す場合は、両配列の長さを同じにする必要があります。

<h6>戻り値</h6>

`Array<[frequency, amplitude]>` 周波数と振幅のペアの配列。

**使用例**

```js
const m = require("mathx");
const gen = m.oscillator({
    components: [
        {amplitude: 1.0, frequencyHz: 15},
        {amplitude: 1.5, frequencyHz: 24},
    ],
    timeRange: {from: 'now', to: 'now+10s'},
    sample: "1000Hz",
});
// genは(time, amplitude)タプルの配列
// fft()は(time, amplitude)の配列を受け取り、 
// (frequency, amplitude)の配列を返します。
const result = m.fft(gen);
for(i=0; i < result.length; i++) {
    console.println(i, result[i][0], result[i][1]);
}
```

## sort() {#sort}

配列を昇順にソートします。データの整理や、分析の前処理に利用できます。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.sort([1.3, 1.2, 1.1])); // [1.1, 1.2, 1.3]
```

## sum() {#sum}

配列内の数値の合計を計算します。統計や数学の計算で使用します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.sum([3, 1, 2]));       // 6
console.log(m.sum([1.3, 1.2, 1.1])); // 3.6
```

## cdf() {#cdf}

累積分布関数（CDF）を計算します。データ`x`のうち`q`以下のサンプルの割合を返し、確率変数が指定値以下になる確率を表します。統計解析や確率論で、データの分布を理解するために使用します。

<h6>構文</h6>

```js
cdf(q, x, weights)
```

- `q` `Number` 基準値
- `x` `Array<Number>` 昇順にソートしたデータ
- `weights` `Array<Number>` 重みの配列（省略するとすべて1。指定する場合は`x`と同じ長さが必要）

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [];
for( i=1; i<=100; i++) {
    x.push(i);
}
x = m.sort(x);
console.log(m.cdf(1.0, x)); // 0.01
```

## mean() {#mean}

数値配列の算術平均を計算します。すべての要素の合計を要素数で割った値で、データセットの中心傾向を求める統計解析に使用します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.mean([1, 2, 3, 4, 5]));  // 3
console.log(m.mean([10, 20, 30]));     // 20
```

## circularMean() {#circularmean}

ラジアン単位の角度など、循環する値の平均を計算します。角度や時刻のように値が一周するデータに適しています。重みの配列を指定して、加重円周平均を求めることもできます。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [0, 0.25 * Math.PI, 0.75 * Math.PI];
w = [1, 2, 2.5];
console.log(m.circularMean(x).toFixed(4));     // 0.9553
console.log(m.circularMean(x, w).toFixed(4));  // 1.3704
```

## correlation() {#correlation}

2つのデータセットの線形関係を表すピアソン相関係数を計算します。値は-1（完全な負の相関）から1（完全な正の相関）までです。重みを指定して加重相関を求めることもできます。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [8, -3, 7, 8, -4];
y = [10, 5, 6, 3, -1];
w = [2, 1.5, 3, 3, 2];
console.log(m.correlation(x, y).toFixed(5));     // 0.61922
console.log(m.correlation(x, y, w).toFixed(5));  // 0.59915
```

## covariance() {#covariance}

2つのデータセットの共分散を計算します。共分散は2つの確率変数がともに変動する度合いを表し、正なら一緒に増加する傾向、負なら一方の増加に対して他方が減少する傾向を示します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [8, -3, 7, 8, -4];
y1 = [10, 2, 2, 4, 1];
y2 = [12, 1, 11, 12, 0];
console.log(m.covariance(x, y1).toFixed(4)); // 13.8000
console.log(m.covariance(x, y2).toFixed(4)); // 37.7000
console.log(m.variance(x).toFixed(4));       // 37.7000
```

## entropy() {#entropy}

確率分布のシャノンエントロピーを計算し、分布の不確実性やランダム性を測定します。情報理論や統計で使用します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.entropy([0.05, 0.1, 0.9, 0.05]).toFixed(4)); // 0.6247
console.log(m.entropy([0.2, 0.4, 0.25, 0.15]).toFixed(4)); // 1.3195
console.log(m.entropy([0.2, 0, 0, 0.5, 0, 0.2, 0.1, 0, 0, 0]).toFixed(4)); // 1.2206
console.log(m.entropy([0, 0, 1, 0]).toFixed(4));           // 0.0000
```

## geometricMean() {#geometricmean}

正の数の配列の幾何平均を計算します。すべての要素の積のn乗根（nは要素数）です。金融や統計の分析で、平均収益率や成長率を求めるために使用します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.geometricMean([1, 3, 9]).toFixed(4));  // 3.0000
console.log(m.geometricMean([2, 8, 32]).toFixed(4)); // 8.0000
```

## harmonicMean() {#harmonicmean}

正の数の配列の調和平均を計算します。各要素の逆数の算術平均に対する逆数です。速度や密度など、比率を含むデータに適しています。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.harmonicMean([1, 2, 4]).toFixed(4));    // 1.7143
console.log(m.harmonicMean([10, 20, 30]).toFixed(4)); // 16.3636
```

## median() {#median}

昇順にソートした配列の50%経験分位点を返します。`quantile(0.5, x, weights)` と同じで、要素数が偶数でも中央2値の平均を計算するとは限りません。

入力配列は昇順にソートしておく必要があります。ソートされていない場合は例外が発生します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.median(m.sort([1, 3, 2, 5, 4])));      // 3
console.log(m.median(m.sort([10, 20, 30, 40, 50]))); // 30
```

## medianInterp() {#medianinterp}

`median`と同じですが、線形補間を適用した値を返します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.medianInterp(m.sort([1, 3, 2, 5, 4])));      // 2.5
console.log(m.medianInterp(m.sort([10, 20, 30, 40, 50]))); // 25
```

## quantile() {#quantile}

`quantile`関数は、指定した確率に対するデータセットの分位点を計算します。 
分位点は、四分位（4区間）や百分位（100区間）のように、データセットを確率が等しい区間に分割します。 
この関数は、データの分布を理解するために使用します。

<h6>構文</h6>

```js
quantile(p, x, weights)
```

- `p` `Number`
- `x` `Array<Number>` `x`のデータは昇順にソートする必要があります。
- `weights` `Array<Number>` 重みを省略すると、すべて1です。指定する場合は、`x`と`weights`の長さを同じにする必要があります。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = m.sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
console.log(m.quantile(0.25, data)); // 3
console.log(m.quantile(0.5, data));  // 5
console.log(m.quantile(0.74, data)); // 8
```

## quantileInterp() {#quantileinterp}

`quantile`と同じですが、線形補間した値を返します。

<h6>構文</h6>

```js
quantileInterp(p, x, weights)
```

- `p` `Number` 分位点の確率
- `x` `Array<Number>` 昇順にソートしたデータ
- `weights` `Array<Number>` 重みの配列（省略時はすべて1。指定する場合は`x`と同じ長さが必要）

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = m.sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
console.log(m.quantileInterp(0.25, data)); // 2.5
console.log(m.quantileInterp(0.5, data));  // 5
console.log(m.quantileInterp(0.74, data)); // 7.4
```

## meanStdDev() {#meanstddev}

数値配列の平均と標準偏差を同時に計算します。平均は中心傾向、標準偏差はデータのばらつきを表し、統計解析でデータセットの要約に使用します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = [1, 2, 3, 4, 5];
result = m.meanStdDev(data);
console.log(result.mean.toFixed(2));   // 3.00
console.log(result.stdDev.toFixed(2)); // 1.58
```

## mode() {#mode}

データセット内で最も出現頻度が高い値である最頻値を計算します。結果は`{value: number, count: number}`形式です。最頻値が複数ある場合の扱いは実装に依存します。

<h6>構文</h6>

```js
mode(x, weights)
```

- `x` `Array<Number>` 昇順にソートしたデータ
- `weights` `Array<Number>` 重みの配列（省略時はすべて1。指定する場合は`x`と同じ長さが必要）

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = m.sort([1, 2, 2, 3, 4]);
console.log(m.mode(data)); // {value:2, count:2}
data = m.sort([1, 1, 2, 3, 4]);
console.log(m.mode(data)); // {value:1, count:2}
```

## moment() {#moment}

指定した点を基準とするn次モーメントを計算します。歪度（3次モーメント）、尖度（4次モーメント）など、分布の形状を分析するために使用します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
data = [1, 2, 3, 4, 5];
console.log(m.moment(2, data).toFixed(4)); // 2.5000
console.log(m.moment(4, data).toFixed(4)); // 6.8000
```

## stdDev() {#stddev}

数値配列の標準偏差を計算します。標準偏差はデータのばらつきを表し、小さいほど平均に近く、大きいほど広く分散していることを示します。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
console.log(m.stdDev([1, 2, 3, 4, 5]).toFixed(4));      // 1.5811
console.log(m.stdDev([10, 20, 30, 40, 50]).toFixed(4)); // 15.8114
```

## stdErr() {#stderr}

標本平均の標準誤差を計算します。標本平均が母平均を表す精度を示し、標準偏差を標本サイズの平方根で割った値です。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
let stddev = m.stdDev([1, 2, 3, 4, 5]);
let sampleSize = 5;
console.log(m.stdErr(stddev, sampleSize).toFixed(4)); // 0.7071
```

## linearRegression() {#linearregression}

2つのデータセットに線形回帰を適用し、観測値と予測値の残差二乗和を最小にする直線を求めます。予測モデルや傾向分析で使用します。結果は、`y = alpha*x + beta`に対応する`{slope: alpha, intercept: beta}`です。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx');
x = [1, 2, 3, 4, 5];
y = [2, 4, 6, 8, 10];
result = m.linearRegression(x, y);
console.log(result.slope.toFixed(4));     // 2.0000
console.log(result.intercept.toFixed(4)); // 0.0000
```
