---
title: "uuid"
type: docs
weight: 100
draft: true
---

## UUID

UUID 생성기입니다.

<h6>사용 형식</h6>

{{< neo_since ver="8.0.75" />}}
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
