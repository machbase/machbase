---
title: "mat"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## Dense()

A dense matrix implementation.

<h6>Creation</h6>

```js
Dense(r, c, data)
```

<h6>Parameters</h6>

- `r` `Number` rows
- `c` `Number` columns
- `data` `Number[]` matrix elements

Creates a new Dense matrix of size `r × c`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println(mat.format(a, {format:"a = %v",  prefix: "    "}))

// a = ⎡11  12  13⎤
//     ⎢21  22  23⎥
//     ⎣31  32  33⎦
```

### dims()

Returns the matrix dimensions `(rows, columns)`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println("dims:", a.dims());

// dims: [3, 3]
```

### at()

Returns the value at the specified `(row, col)`.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println("at(1,2):", a.at(1,2));

// at(1,2): 23
```

### set()

Sets the value at the specified position.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
a.set(2,2,55)
console.println(mat.format(a, {format:"a = %v",  prefix: "    "}))

// a = ⎡11  12  13⎤
//     ⎢21  22  23⎥
//     ⎣31  32  55⎦
```

### t()

Creates a transposed matrix.

```js {linenos=table,linenostart=1,hl_lines=[7]}
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

### add()

Performs matrix addition.

```js {linenos=table,linenostart=1,hl_lines=[11]}
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

### sub()

Performs matrix subtraction.

```js {linenos=table,linenostart=1,hl_lines=[11]}
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

### mul()

Performs matrix multiplication.

```js {linenos=table,linenostart=1,hl_lines=[11]}
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

### mulElem()

Performs element-wise multiplication.

```js {linenos=table,linenostart=1,hl_lines=[11]}
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

### divElem()

Performs element-wise division.

```js {linenos=table,linenostart=1,hl_lines=[11]}
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

### inverse()

Calculates the inverse matrix.

```js {linenos=table,linenostart=1,hl_lines=[7]}
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

### solve()

Solves the linear equation `A * X = B` and returns the solution.

### exp()

Computes the matrix exponential.

### pow()

Performs matrix exponentiation.

### scale()

Scales the matrix by a scalar value.

## VecDense

A dense vector type.

<h6>Creation</h6>

```js
VecDense(n, data)
```

<h6>Parameters</h6>

- `n` `Number` vector length (must be greater than 0)
- `data` `Number[]` element array (filled with zeros if omitted)


### cap()

Returns the internal buffer capacity.

### len()

Returns the vector length.

### atVec()

Returns the value at the specified index.

### setVec()

Sets the value at the specified index.

### addVec()

Adds two vectors and stores the result.

### subVec()

Performs vector subtraction.

### mulVec()

Computes matrix-vector multiplication.

### mulElemVec()

Computes element-wise multiplication.

### scaleVec()

Scales the vector by a scalar.

### solveVec()

Solves a linear system and returns the vector solution.

## QR

**QR factorization** is a decomposition of a matrix *A* into a product `A = QR` of an orthonormal matrix *Q* and an upper triangular matrix *R*.
QR decomposition is often used to solve the linear least squares (LLS) problem and is the basis for a particular eigenvalue algorithm, the QR algorithm.

Any real matrix *A* may be decomposed as

```
A = QR
```

where *Q* is an orthogonal matrix and *R* is an upper triangular matrix.
If *A* is invertible, then the factorization is unique if we require the diagonal elements of *R* to be positive.

**Usage example**

```js {linenos=table,linenostart=1,hl_lines=[13,16]}
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


## format()

```js {linenos=table,linenostart=1,hl_lines=["8-13"]}
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
