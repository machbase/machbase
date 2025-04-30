---
title: "@jsh/generator"
type: docs
weight: 50
---

{{< neo_since ver="8.0.52" />}}

## arrange()

**Usage example**

```js {linenos=table,linenostart=1}
const { arrange } = require("@jsh/generator")
arrange(0, 6, 3).forEach((i) => console.log(i))

// 0
// 3
// 6
```

## linspace()

**Usage example**

```js {linenos=table,linenostart=1}
const { linspace } = require("@jsh/generator")
linspace(0, 1, 3).forEach((i) => console.log(i))

// 0
// 1.5
// 1
```

## meshgrid()

**Usage example**

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

**Usage example**

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

**Usage example**

```js {linenos=table,linenostart=1}
const {Simplex} = require("@jsh/generator")
simplex = new Simplex(123);
for(i=0; i < 5; i++) {
    console.log(i, simplex.eval(i, i * 0.6).toFixed(3));
}

// 0 0.000
// 1 0.349
// 2 0.319
// 3 0.038
// 4 -0.364
```

## UUID

**Usage example**

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
