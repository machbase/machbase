---
title: "simplex"
type: docs
weight: 10
---

{{< neo_since ver="8.0.74" />}}

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
const g = require("mathx/simplex")
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