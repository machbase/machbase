---
title: SCRIPT()
type: docs
weight: 65
---

**tengo**

[tengo](https://github.com/d5/tengo) is a Golang like script.
The additional package "context" package is available that is exposing the TQL specific functionalities
based the default packages from tengo.

TQL can execute user defined script within `SCRIPT()` by passing codes inside `{`, `}`.

{{< callout type="info" >}}
<b>IMPORTANT</b><br/>
If the script doesn't call `context.yield()` and `context.drop()` explicitly for a record,
it passes the record to the next function without any changes.
{{< /callout >}}


![map_script](../img/map_script.jpg)

A context in the code of `SCRIPT()` provides serveral methods.

| method                |  description|
|:--------------------- | :----------------------------------------------------------------|
| `ctx.key()`           | returns the key of the current record                        |
| `ctx.value(idx)`      | returns the value of `idx`th value of the current record <br/>or returns whole records in an array if `idx` is omitted.   |
| `ctx.drop()`          | discards the current record                                 |
| `ctx.yield(values...)`| produces a new record from the given values... arguments    |
| `ctx.yieldKey(key, values...)`| produces a new record from the given key and values...   |
| `ctx.param(name [, default])` | returns the value of the request parameter for the given name.<br/>If the param specified by `name` *string* does not exists,it returns `default` *string*.<br/> If `default` is not specified, it returns empty string`""`   |
| `ctx.bridge(name)`    | returns bridge instance of the given name                        |
| `ctx.println(args...)`| print log message to the web console                             |

## context package

### context.yield()

Pass the incoming arguments to the next function.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
SCRIPT({
    ctx := import("context")
    ctx.yield(0, 1, 2, 3)
    ctx.yield(1, 2, 3, 4)
})
CSV()
```
{{< /tab >}}
{{< tab >}}
```csv
0,1,2,3
1,2,3,4
```
{{< /tab >}}
{{< /tabs >}}

### context.key()

Returns the key of the current record.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
FAKE( linspace(1,2,2))
MAPKEY("hello")
SCRIPT({
    ctx := import("context")
    ctx.yield(ctx.key(), ctx.value(0))
})
CSV()
```
{{< /tab >}}
{{< tab >}}
```csv
hello,1
hello,2
```
{{< /tab >}}
{{< /tabs >}}

### context.value()

Returns the whole value of the current records in array. If the index is given, it returns the element of the values.

For example, If the current record is `[0, true, "hello", "world"]`

- `context.value()` returns the whole values of the record `[0, true, "hello", "world"]`
- `context.value(0)` returns the first element of the record `0`
- `context.value(3)` returns the last element of the record `"world"`

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
FAKE( linspace(1,2,2))
SCRIPT({
    ctx := import("context")
    ctx.yield(ctx.value(0), ctx.value(0)*10)
})
CSV()
```
{{< /tab >}}
{{< tab >}}
```csv
1,10
2,20
```
{{< /tab >}}
{{< /tabs >}}

## times package

### times.time_format()

Convert timestamp to a string.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
STRING(param("format_time") ?? "808210800000000000")
SCRIPT({
    ctx := import("context")
    times := import("times")
    text := import("text")

    epoch_txt := ctx.value(0)
    epoch := text.parse_int(epoch_txt, 10, 64)
    epoch = epoch / 1000000000

    t_time := times.time_format(epoch, "Mon Jan 2 15:04:05 -0700 MST 2006")

    ctx.yield(epoch, t_time)
})
CSV()
```
{{< /tab >}}
{{< tab >}}
```csv
808210800,Sat Aug 12 16:00:00 +0900 KST 1995
```
{{< /tab >}}
{{< /tabs >}}


### times.parse()

Convert a string to timestamp.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
STRING(param("timestamp") ?? "Sat Aug 12 00:00:00 -0700 MST 1995")
SCRIPT({
    ctx := import("context")
    times := import("times")
    text := import("text")

    time_format := ctx.value(0)
    epoch := times.parse("Mon Jan 2 15:04:05 -0700 MST 2006", time_format)

    ctx.yield(epoch, time_format)
})
CSV()
```
{{< /tab >}}
{{< tab >}}
```csv
808210800000000000,Sat Aug 12 00:00:00 -0700 MST 1995
```
{{< /tab >}}
{{< /tabs >}}

## json package

### json.decode()

Parse JSON string.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
STRING(payload() ?? {{
  "tag": "pump",
  "data": {
    "string": "Hello TQL?",
    "number": "123.456",
    "time": 1687405320,
    "boolean": true
  },
  "array": ["elements", 234.567, 345.678, false]
}})
SCRIPT({
  json := import("json")
  ctx := import("context")
  // parse value as json
  obj := json.decode(ctx.value(0))
  // conditional expression
  if obj.data.boolean {
    // yield multiple records
    ctx.yield(obj.tag+"_0", obj.data.time*1000000000, obj.data.number)
    ctx.yield(obj.tag+"_1", obj.data.time*1000000000, obj.array[1])
    ctx.yield(obj.tag+"_2", obj.data.time*1000000000, obj.array[2])    
  } else {
    // discard the current record
    ctx.drop()
  }
})
CSV()
```
{{< /tab >}}
{{< tab >}}
```csv
pump_0,1687405320000000000,123.456
pump_1,1687405320000000000,234.567
pump_2,1687405320000000000,345.678
```
{{< /tab >}}
{{< /tabs >}}

If the script ends with `APPEND(...)` or `INSERT(...)` instead of `CSV()` the final result records will be written into database.

## Example

Open a new *tql* editor on the web ui and copy the code below and run it.

In this example, `linspace(-4,4,100)` generates an array contains 100 elements which are ranged from -4.0 to 4.0 in every `8/100` step. `meshgrid()` takes two array and produce meshed new array. As result of FAKE() in the example produces an array of 10000 elements (100 x 100 meshed) contains array of two float point numbers.
`SCRIPT()` function takes a code block which enclosed by `{` and `}` and run it for each record.
It takes the current record via `context.value()` then yield transformed data via `context.yield()`.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
SCRIPT({
  math := import("math")
  // Define a custom function in the script
  calc := func(a, b) {
    return math.sin(math.pow(a, 2) + math.pow(b, 2)) /
           (math.pow(a, 2) + math.pow(b, 2))
  }
  // Receive values of the record from context
  ctx := import("context")
  values := ctx.value()
  x := values[0]
  y := values[1]
  z := calc(x, y)
  // Yield new value
  //  - yieldKey() build and passes new value with new key to the next step.
  //  - yeild() build and passes new value to the next step with the received key from previous step
  ctx.yield(x, y, z)
})
CHART_LINE3D(
  // chart size in HTML syntax
  size('500px', '500px'),
  // width, height, depth grids in percentage
  gridSize(100,50,100),
  lineWidth(5), visualMap(-0.1, 1),
  // rotation speed in degree per sec.
  autoRotate(20)
)
```
{{< /tab >}}
{{< tab >}}
![web-tql-script-wave](/images/web-tql-script-wave.gif)
{{< /tab >}}
{{< /tabs >}}

The SCRIPT code above is actually equivalent with the TQL `MAPVALUE(2, ...)` function below.
The math functions used in MAPVALUE became available {{< neo_since ver="8.0.6" />}}.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
MAPVALUE(2,
    sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2))
)
CHART_LINE3D(
  // chart size in HTML syntax
  size('500px', '500px'),
  // width, height, depth grids in percentage
  gridSize(100,50,100),
  lineWidth(5), visualMap(-0.1, 1),
  // rotation speed in degree per sec.
  autoRotate(20)
)
```
{{< /tab >}}
{{< tab >}}
![web-tql-script-wave](/images/web-tql-script-wave.gif)
{{< /tab >}}
{{< /tabs >}}
