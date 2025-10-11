---
title: "@jsh/generator"
type: docs
weight: 50
---

{{< neo_since ver="8.0.52" />}}

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
const { arrange } = require("@jsh/generator")
arrange(0, 6, 3).forEach((i) => console.log(i))

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
const { linspace } = require("@jsh/generator")
linspace(0, 1, 3).forEach((i) => console.log(i))

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
const { meshgrid } = require("@jsh/generator")

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

## random()

`[0.0, 1.0)` 구간의 난수를 반환합니다.

<h6>사용 형식</h6>

```js
random()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`Number` 0.0 이상 1.0 미만의 난수.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const { random } = require("@jsh/generator")
for(i=0; i < 3; i++) {
    console.log(random().toFixed(2))
}

// 0.54
// 0.12
// 0.84
```

## Simplex

Simplex 노이즈 알고리즘 기반 난수 생성기입니다.

<h6>사용 형식</h6>

```js
new Simplex(seed)
```

<h6>매개변수</h6>

`seed` 난수 시드 값.

<h6>반환값</h6>

새 Simplex 생성기 객체.

### eval()

입력 값에 따라 결정적 노이즈 값을 반환합니다. 동일한 인자를 사용하면 항상 같은 결과가 나옵니다.

<h6>사용 형식</h6>

```js
eval(arg1)
eval(arg1, arg2)
eval(arg1, arg2, arg3)
eval(arg1, arg2, arg3, arg4)
```

<h6>매개변수</h6>

`args` `Number` 1~4차원까지 표현할 수 있는 가변 길이 숫자 목록입니다.

<h6>반환값</h6>

`Number` 노이즈 값.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const g = require("@jsh/generator")
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

## UUID

UUID 생성기입니다.

<h6>사용 형식</h6>

```js
new UUID(ver)
```

<h6>매개변수</h6>

`ver` UUID 버전. 1, 4, 6, 7 중 하나여야 합니다.

<h6>반환값</h6>

새 UUID 생성기 객체.

### eval()

<h6>사용 형식</h6>

```js
eval()
```

<h6>매개변수</h6>

없음.

<h6>반환값</h6>

`String` 생성된 UUID.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1}
const {UUID} = require("@jsh/generator")
gen = new UUID(1);
for(i=0; i < 3; i++) {
    console.log(gen.eval());
}

// 868c8ec0-2180-11f0-b223-8a17cad8d69c
// 868c97b2-2180-11f0-b223-8a17cad8d69c
// 868c98d4-2180-11f0-b223-8a17cad8d69c
```
