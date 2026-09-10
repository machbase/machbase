---
toc: true
title: "mat"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## Dense() {#dense}

密行列（Dense Matrix）の実装です。

<h6>作成</h6>

```js
Dense(r, c, data)
```

<h6>パラメーター</h6>

- `r` `Number` 行数
- `c` `Number` 列数
- `data` `Number[]` 行列要素の配列

`r × c`サイズの新しいDense行列を作成します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println(mat.format(a, {format:"a = %v",  prefix: "    "}))

// a = ⎡11  12  13⎤
//     ⎢21  22  23⎥
//     ⎣31  32  33⎦
```

### dims() {#dims}

行列のサイズを`(行, 列)`で返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println("dims:", a.dims());

// dims: [3, 3]
```

### at() {#at}

指定した`(row, col)`の位置の値を返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println("at(1,2):", a.at(1,2));

// at(1,2): 23
```

### set() {#set}

指定した位置の値を設定します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
a.set(2,2,55)
console.println(mat.format(a, {format:"a = %v",  prefix: "    "}))

// a = ⎡11  12  13⎤
//     ⎢21  22  23⎥
//     ⎣31  32  55⎦
```

### t() {#t}

転置行列を作成します。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
console.println(mat.format(A, {format:"A=%v", prefix:"  "}));
B = A.t();
console.println(mat.format(B, {format:"B=%v", prefix:"  "}));

// A=⎡1  2⎤
//   ⎣3  4⎦
// B=⎡1  3⎤
//   ⎣2  4⎦
```

### add() {#add}

行列の加算を行います。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
B = mat.Dense(2, 2, [
    10, 20,
    30, 40,
]);
C = mat.Dense();
C.add(A, B); // C = A + B
console.println(mat.format(C));

// ⎡11 22⎤ 
// ⎣33 44⎦
```

### sub() {#sub}

行列の減算を行います。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
B = mat.Dense(2, 2, [
    10, 20,
    30, 40,
]);
C = mat.Dense();
C.sub(B, A); // C = B - A
console.println(mat.format(C));

// ⎡ 9 18⎤ 
// ⎣27 36⎦
```

### mul() {#mul}

行列の乗算を行います。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
B = mat.Dense(2, 2, [
    10, 20,
    30, 40,
]);
C = mat.Dense();
C.mul(A, B); // C = A * B
console.println(mat.format(C));

// ⎡ 70 100⎤ 
// ⎣150 220⎦
```

### mulElem() {#mulelem}

要素ごとの乗算を行います。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
B = mat.Dense(2, 2, [
    10, 20,
    30, 40,
]);
C = mat.Dense();
C.mulElem(A, B);
console.println(mat.format(C));

// ⎡ 10 40⎤ 
// ⎣ 90 160⎦
```

### divElem() {#divelem}

要素ごとの除算を行います。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
B = mat.Dense(2, 2, [
    10, 20,
    30, 40,
]);
C = mat.Dense();
C.divElem(A, B);
console.println(mat.format(C));

// ⎡0.1  0.1⎤
// ⎣0.1  0.1⎦
```

### inverse() {#inverse}

逆行列を計算します。

```js {linenos=table,linenostart=1}
const mat = require('mathx/mat');
A = mat.Dense(2, 2, [
    1, 2,
    3, 4,
]);
B = mat.Dense();
B.inverse(A);
C = mat.Dense();
C.mul(A, B);
console.println(mat.format(B, {format:"B=%.f", prefix:"  "}));
console.println(mat.format(C, {format:"C=%.f", prefix:"  "}));

//B=⎡-2  1⎤
//  ⎣ 1 -0⎦
//C=⎡1 0⎤
//  ⎣0 1⎦
```

### solve() {#solve}

線形方程式`A * X = B`を解き、その解を返します。

### exp() {#exp}

行列指数関数を計算します。

### pow() {#pow}

行列のべき乗を計算します。

### scale() {#scale}

スカラー値を掛けて、行列をスケーリングします。

## VecDense {#vecdense}

密ベクトル型です。

<h6>作成</h6>

```js
VecDense(n, data)
```

<h6>パラメーター</h6>

- `n` `Number` ベクトルの長さ（0より大きい値）
- `data` `Number[]` 要素の配列（省略すると0で埋める）


### cap() {#cap}

内部バッファーの容量を返します。

### len() {#len}

ベクトルの長さを返します。

### atVec() {#atvec}

指定したインデックスの値を返します。

### setVec() {#setvec}

指定したインデックスの値を設定します。

### addVec() {#addvec}

2つのベクトルを加算し、結果を保存します。

### subVec() {#subvec}

ベクトルの減算を行います。

### mulVec() {#mulvec}

行列とベクトルの積を計算します。

### mulElemVec() {#mulelemvec}

要素ごとの積を計算します。

### scaleVec() {#scalevec}

スカラーを掛けて、ベクトルをスケーリングします。

### solveVec() {#solvevec}

線形系を解き、解ベクトルを求めます。

## QR {#qr}

**QR分解**は、行列*A*を直交行列*Q*と上三角行列*R*の積`A = QR`で表す方法です。
線形最小二乗（LLS）問題の解法や、QR固有値アルゴリズムの基礎として広く使用されます。

任意の実行列*A*は、以下のように分解できます。

```
A = QR
```

ここで*Q*は直交行列、*R*は上三角行列です。
*A*が可逆な場合、*R*の対角要素を正とすると、分解は一意に決まります。

**使用例**

```js {linenos=table,linenostart=1}
const m = require('mathx/mat');
A = m.Dense(4, 2, [
    0, 1,
    1, 1,
    1, 1,
    2, 1,
]);

qr = m.QR();
qr.factorize(A);

Q = m.Dense();
qr.qTo(Q);

R = m.Dense();
qr.rTo(R);

B = m.Dense(4, 1, [1, 0, 2, 1]);
x = m.Dense();
qr.solveTo(x, false, B);
console.println(m.format(x, { format: "x = %.2f", prefix: "    " }));

// x = ⎡0.00⎤
//     ⎣1.00⎦
```


## format() {#format}

```js {linenos=table,linenostart=1}
const m = require("mathx/mat");
A = m.Dense(100, 100);
for (let i = 0; i < 100; i++) {
    for (let j = 0; j < 100; j++) {
        A.set(i, j, i + j);
    }
}
console.println(m.format(A, {
    format: "A = %v",
    prefix: "    ",
    squeeze: true,
    excerpt: 3,
}));

// A = Dims(100, 100)
//     ⎡ 0    1    2  ...  ...   97   98   99⎤
//     ⎢ 1    2    3             98   99  100⎥
//     ⎢ 2    3    4             99  100  101⎥
//      .
//      .
//      .
//     ⎢97   98   99            194  195  196⎥
//     ⎢98   99  100            195  196  197⎥
//     ⎣99  100  101  ...  ...  196  197  198⎦
```
