---
title: "mat"
type: docs
weight: 10
---

{{< neo_since ver="8.0.74" />}}

## Dense()

밀집 행렬(Dense Matrix) 구현입니다.

<h6>생성</h6>

```js
Dense(r, c, data)
```

<h6>매개변수</h6>

- `r` `Number` 행(row) 개수
- `c` `Number` 열(column) 개수
- `data` `Number[]` 행렬 요소 배열

`r × c` 크기의 새로운 Dense 행렬을 생성합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println(mat.format(a, {format:"a = %v",  prefix: "    "}))

// a = ⎡11  12  13⎤
//     ⎢21  22  23⎥
//     ⎣31  32  33⎦
```

### dims()

행렬의 `(행, 열)` 크기를 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println("dims:", a.dims());

// dims: [3, 3]
```

### at()

지정한 `(row, col)` 위치의 값을 반환합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const mat = require('mathx/mat');
const a = mat.Dense(3, 3, [11,12,13,21,22,23,31,32,33]);
console.println("at(1,2):", a.at(1,2));

// at(1,2): 23
```

### set()

지정한 위치의 값을 설정합니다.

<h6>사용 예시</h6>

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

전치 행렬을 생성합니다.

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

행렬 덧셈을 수행합니다.

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

행렬 뺄셈을 수행합니다.

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

행렬 곱셈을 수행합니다.

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

원소별(element-wise) 곱셈을 수행합니다.

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

원소별 나눗셈을 수행합니다.

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

역행렬을 구합니다.

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

선형 방정식 `A * X = B`를 풀어 해를 반환합니다.

### exp()

행렬 지수 함수를 계산합니다.

### pow()

행렬 거듭제곱을 수행합니다.

### scale()

스칼라 값을 곱해 행렬을 스케일링합니다.

## VecDense

밀집 벡터 타입입니다.

<h6>생성</h6>

```js
VecDense(n, data)
```

<h6>매개변수</h6>

- `n` `Number` 벡터 길이(0보다 커야 합니다)
- `data` `Number[]` 요소 배열(생략 시 0으로 채워집니다)


### cap()

내부 버퍼 용량을 반환합니다.

### len()

벡터 길이를 반환합니다.

### atVec()

지정한 인덱스의 값을 반환합니다.

### setVec()

지정한 인덱스의 값을 설정합니다.

### addVec()

두 벡터를 더해 결과를 저장합니다.

### subVec()

벡터 뺄셈을 수행합니다.

### mulVec()

행렬과 벡터의 곱을 계산합니다.

### mulElemVec()

원소별 곱을 계산합니다.

### scaleVec()

스칼라를 곱해 벡터를 스케일링합니다.

### solveVec()

선형 시스템을 풀어 벡터 해를 구합니다.

## QR

**QR 분해**는 행렬 *A*를 직교 행렬 *Q*와 상삼각 행렬 *R*의 곱 `A = QR`로 표현하는 방법입니다.
선형 최소제곱(LLS) 문제를 풀거나 QR 고유값 알고리즘의 기초로 널리 사용됩니다.

임의의 실수 행렬 *A*는 다음과 같이 분해할 수 있습니다.

```
A = QR
```

여기서 *Q*는 직교(정규 직교) 행렬, *R*은 상삼각 행렬입니다.
*A*가 가역이면 *R*의 대각 원소를 양수로 두었을 때 분해가 유일하게 결정됩니다.

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
