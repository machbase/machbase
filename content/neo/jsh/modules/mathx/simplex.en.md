---
title: "simplex"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## Simplex

A noise generator based on the Simplex noise algorithm.

<h6>Syntax</h6>

```js
new Simplex(seed)
```

<h6>Parameters</h6>

`seed` seed number.

<h6>Return value</h6>

A new Simplex generator object.

### eval()

Returns a random noise value. Repeated calls with the same args inputs will have the same output.

<h6>Syntax</h6>

```js
eval(arg1)
eval(arg1, arg2)
eval(arg1, arg2, arg3)
eval(arg1, arg2, arg3, arg4)
```

<h6>Parameters</h6>

`args` `Number` A variable-length list of numbers, representing dimensions. The function accepts a minimum of one argument (1-dimensional) and a maximum of four arguments (4-dimensional).

<h6>Return value</h6>

`Number` random noise value

<h6>Usage example</h6>

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
