---
title: SCRIPT()
type: docs
weight: 55
---

*Syntax*: `SCRIPT(language, [{init_code},] {main_code})`

- *language* : specify the script language (set `"js"` for Javascript)
- *init_code* : initialize code (optional)
- *main_code* : script code

The *init_code* is optional and runs only once at the beginning. The *main_code* is mandatory and cannot be omitted.

## Javascript

TQL supports the `SCRIPT()` function, which utilizes JavaScript (ECMA5) in both **SRC** and **MAP** contexts {{< neo_since ver="8.0.36" />}}.
This feature offers developers the flexibility to use a familiar programming language,
enhancing their ability to create more dynamic and powerful scripts within TQL.

Machbase-neo exposes the `$` variable as the context object. JavaScript can access and yield records and database through this context.

- `$.payload` Input data of the request.
- `$.params` Input query parameters of the request.
- `$.key`, `$.values` Javascript access point to the key and values of the current record. It is only available if the `SCRIPT()` is a MAP function.
- `$.yield()` Yield a new record with values
- `$.yieldKey()` Yield a new record with key and values
- `$.db()` Returns a new database connection.
- `$.db().query()` Execute SQL query.
- `$.db().exec()` Execute non-SELECT SQL.
- `$.request().do()` Request HTTP to the remote server.

**Caveat Emptor**

- `use strict` does nothing.
- ECMA5 only. Some ES6 features e.g. Typed Arrays and back-tick string interpolation are not supported.
- Regular expression is not fully compatible with the ECMA5 specification.
    The following regular expression syntax is incompatible:
    
    - `(?=)`  Lookahead (positive), it produces a parsing error
    - `(?!)`  Lookahead (backhead), it produces a parsing error
    - `\1`,`\2`,`\3`, ...    Backreference, it produces a parsing error

### `$.payload`

JavaScript can access the input data of the request using `$.payload`. If there is no input data, `$.payload` will be `undefined`.

```js {{linenos=table,hl_lines=[2]}}
SCRIPT("js", {
    var data = $.payload;
    if (data === undefined) {
        data = '{ "prefix": "name", "offset": 0, "limit": 10}';
    }
    var obj = JSON.parse(data);
    $.yield(obj.prefix, obj.offset, obj.limit);
})
CSV()
```

Call the tql file without any request body which makes the `$.payload` is `undefined`.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

Then the result is the default values: `name,0,10`.

Call the tql file with a custom data.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql \
-d '{"prefix":"testing", "offset":10, "limit":10}'
```

Then the result is: `testing,10,10`

### `$.params`

JavaScript can access the request's query parameters using `$.params`.
The value of a query parameter can be accessed in two ways: using dot notation (`$.params.name`) 
or bracket notation (`$.params["name"]`).
Both forms are interchangeable and can be used based on the context or preference.

```js {{linenos=table,hl_lines=["2-4"]}}
SCRIPT("js", {
    var prefix = $.params.prefix ? $.params.prefix : "name";
    var offset = $.params.offset ? $.params.offset : 0;
    var limit = $.params.limit ? $.params.limit: 10;
    $.yield(obj.prefix, obj.offset, obj.limit);
})
CSV()
```

Call the tql file without parameters.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

The result will be the default values: `name,0,10`.

Call the tql file with parameters.

```sh
curl -o - -X POST "http://127.0.0.1:5654/db/tql/test.tql?"\
"prefix=testing&offset=12&limit=20"
```

The result is: `testing,12,20`.


### `$.key`

Access the key of the current record.
This is defined only when `SCRIPT` is used as a MAP function.
If `SCRIPT` is used as an SRC function, it will be `undefined`.

```js {{linenos=table,hl_lines=["7"]}}
SCRIPT("js", {
    for( i = 0; i < 3; i++) {
        $.yieldKey(i, "hello-"+(i+1));
    }
})
SCRIPT("js", {
    $.yieldKey($.key, $.values[0], 'key is '+$.key);
})
CSV()
```

```csv
hello-1,key is 0
hello-2,key is 1
hello-3,key is 2
```

### `$.values`

Access the values of the current record.
This is defined only when `SCRIPT` is used as a MAP function.
If `SCRIPT` is used as an SRC function, it will be `undefined`.

```js {{linenos=table,hl_lines=["7"]}}
SCRIPT("js", {
        $.yield("string", 10, 3.14);
})
SCRIPT("js", {
    $.yield(
        "the first value is "+$.values[0],
        "2nd value is "+$.values[1],
        "3rd is "+$.values[2]
    );
})
CSV()
```

The output is:

`the first value is string,2nd value is 10,3rd is 3.14`

### `$.yield()`

Yield the new record to the next step, with the key automatically assigned as a sequentially increasing number.

### `$.yieldKey()`

`yieldKey()` functions similarly to `$.yield()`, with the exception that the first argument specifies the key of the record.

### `$.db()`

Returns a new database connection. The connection provides `query()`, `exec()` functions.

### `$.db().query()`

JavaScript can query the database using `$.db().query()`. 
Apply a callback function with `forEach()` to the return value of `query()` to iterate over the query results.

If the callback function of `.forEach()` explicitly returns `false`, the iteration stops immediately.
If the callback function returns `true` or does not return anything (which means it returns `undefined`), 
the iteration continues until the end of the query result.

```js {{linenos=table,hl_lines=["7-9"]}}
SCRIPT("js", {
    var data = $.payload;
    if (data === undefined) {
        data = '{ "tag": "name", "offset": 0, "limit": 5 }';
    }
    var obj = JSON.parse(data);
    $.db().query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
        obj.tag, obj.offset, obj.limit
    ).forEach( function(row){
        name = row[0]
        time = row[1]
        value = row[2]
        $.yield(name, time, value);
    })
})
CSV()
```

```csv
cpu.percent,1725330085908925000,73.9
cpu.percent,1725343895315420000,73.6
cpu.percent,1725343898315887000,6.1
cpu.percent,1725343901314955000,10.8
cpu.percent,1725343904315952000,40
```

### `$.db().exec()`

If the SQL is not a SELECT statement, use `$.db().exec()` to execute INSERT, DELETE, CREATE TABLE statements.

```js {{linenos=table,hl_lines=["10-14", "21-22"]}}
SCRIPT("js", {
    for( i = 0; i < 3; i++) {
        ts = Date.now()*1000000; // ms to ns
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT("js", {
    // This section contains initialization code
    // that runs once before processing the first record.
    err = $.db().exec("CREATE TAG TABLE IF NOT EXISTS example ("+
        "NAME varchar(80) primary key,"+
        "TIME datetime basetime,"+
        "VALUE double"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // This section contains the main code
    // that runs over every record.
    err = $.db().exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```

### `$.request().do()`

*Syntax*: `$.request(url [, option]).do(callback)`

**Request option**

```js
{
    method: "GET|POST|PUT|DELETE", // default is "GET"
    headers: { "Authorization": "Bearer auth-token"}, // key value map
    body: "body content if the method is POST or PUT"
}
```
The actual request is made when `.then()` is called with a callback function to handle the response. The callback function receives a Response object as an argument, which provides several properties and methods.

**Response**

| Property         | Type    | Description  |
|:-----------------|:-------:|:-------------|
| `.ok`            | Boolean | `true` if the status code of the response is success. (`200<= status < 300`) |
| `.status`        | Number  | http response code |
| `.statusText`    | String  | status code and message. e.g. `200 OK` |
| `.url`           | String  | request url      |
| `.headers`       | Map     | response headers | 

The Response object provides useful methods that serves the body content of the response.

| Method                 | Description  |
|:-----------------------|:-------------|
| `.text(callback(txt))` | Call the callback with content in a string |
| `.blob(callback(bin))` | Call the callback with content in a binary array |
| `.csv(callback(row))`  | Parse the content into CSV format and call `callback()` for each row (record). |
<!-- | .json(callback(obj)) | Parse the content into JSON object or array and call `callback()` for each object. **not yet implemented** | -->

**Usage**

```js
$.request("https://server/path", {
    method: "GET",
    headers: { "Authorization": "Bearer auth-token" }
  }).do( function(rsp){
    console.log("ok:", rsp.ok);
    console.log("status:", rsp.status);
    console.log("statusText:", rsp.statusText);
    console.log("url:", rsp.url);
    console.log("Content-Type:", rsp.headers["Content-Type"]);
});
```

## Examples

### Hello World

```js
SCRIPT("js", {
    console.log("Hello World?");
})
DISCARD()
```

**Result**

{{< figure src="../img/script_js_helloworld.png" width="550px" >}}

### JSON parser

```js {{linenos=table,hl_lines=["11"]}}
SCRIPT("js", {
    $.result = {
        columns: ["NAME", "AGE", "IS_MEMBER", "HOBBY"],
        types: ["string", "int32", "bool", "string"],
    }
},{
    content = $.payload;
    if (content === undefined) {
        content = '{"name":"James", "age": 24, "isMember": true, "hobby": ["book", "game"]}';
    }
    obj = JSON.parse(content);
    $.yield(obj.name, obj.age, obj.isMember, obj.hobby.join(","));
})
JSON()
```

**Result**
```json
{
    "data": {
        "columns": [ "NAME", "AGE", "IS_MEMBER", "HOBBY" ],
        "types": [ "string", "int32", "bool", "string" ],
        "rows": [
            [ "James", 24, true, "book,game" ]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "627.958µs"
}
```

### Fetch CSV

```js {{linenos=table,hl_lines=["17-19"]}}
SCRIPT("js", {
    $.result = {
        columns: ["SepalLen", "SepalWidth", "PetalLen", "PetalWidth", "Species"],
        types: ["double", "double", "double", "double", "string"]
    };
},{
    $.request("https://docs.machbase.com/assets/example/iris.csv")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("url:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        var err = rsp.csv(function(fields){
            $.yield(fields[0], fields[1], fields[2], fields[3], fields[4]);
        })
        if (err !== undefined) {
            console.warn(err);
        }
    })
})
CSV(header(true))
```

### Fetch JSON text

This example demonstrates how to fetch JSON content from a remote server and parse it using Javascript.

```js {{linenos=table,hl_lines=["17-23"]}}
SCRIPT("js", {
    $.result = {
        columns: ["ID", "USER_ID", "TITLE", "COMPLETED"],
        types: ["int64", "int64", "string", "boolean"]
    };
},{
    $.request("https://jsonplaceholder.typicode.com/todos")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("URL:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        rsp.text( function(txt){
            list = JSON.parse(txt);
            for (i = 0; i < list.length; i++) {
                obj = list[i];
                $.yield(obj.id, obj.userId, obj.title, obj.completed);
            }
        })
    })
})
CSV(header(false))
```

<!-- ### Fetch JSON

> TODO: not implemented yet

```js
SCRIPT("js", {
    $.result = {
        columns: ["ID", "USER_ID", "TITLE", "COMPLETED"],
        types: ["int64", "int64", "string", "boolean"]
    };
},{
    $.request("https://jsonplaceholder.typicode.com/todos")
     .do( function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("URL:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        rsp.json(function(obj){
            $.yield(obj.id, obj.userId, obj.title, obj.completed);
        });
    })
})
CSV(header(false))
``` -->

<!-- ## tengo

[tengo](https://github.com/d5/tengo) is a Golang-like scripting language. The additional "context" package is available, exposing TQL-specific functionalities based on the default packages from Tengo.

TQL can execute user-defined scripts within `SCRIPT()` by passing code inside `{` and `}`.

{{< callout type="info" >}}
<b>IMPORTANT</b><br/>
If the script doesn't call `context.yield()` and `context.drop()` explicitly for a record,
it passes the record to the next function without any changes.
{{< /callout >}}


![map_script](../img/map_script.jpg)

A context in the code of `SCRIPT()` provides several methods.

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

### context package

#### context.yield()

Pass the incoming arguments to the next function.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["3-4"],linenostart=1}
SCRIPT("tengo", {
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

#### context.key()

Returns the key of the current record.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE( linspace(1,2,2))
MAPKEY("hello")
SCRIPT("tengo", {
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

#### context.value()

Returns the whole value of the current records in array. If the index is given, it returns the element of the values.

For example, If the current record is `[0, true, "hello", "world"]`

- `context.value()` returns the whole values of the record `[0, true, "hello", "world"]`
- `context.value(0)` returns the first element of the record `0`
- `context.value(3)` returns the last element of the record `"world"`

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["4"],linenostart=1}
FAKE( linspace(1,2,2))
SCRIPT("tengo", {
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

### times package

#### times.time_format()

Convert timestamp to a string.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["11"],linenostart=1}
STRING(param("format_time") ?? "808210800000000000")
SCRIPT("tengo", {
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


#### times.parse()

Convert a string to timestamp.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["8"],linenostart=1}
STRING(param("timestamp") ?? "Sat Aug 12 00:00:00 -0700 MST 1995")
SCRIPT("tengo", {
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

### json package

#### json.decode()

Parse JSON string.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=[15,17,"19-21"],linenostart=1}
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
SCRIPT("tengo", {
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

### Example

Open a new *tql* editor on the web ui and copy the code below and run it.

In this example, `linspace(-4,4,100)` generates an array contains 100 elements which are ranged from -4.0 to 4.0 in every `8/100` step. `meshgrid()` takes two array and produce meshed new array. As result of FAKE() in the example produces an array of 10000 elements (100 x 100 meshed) contains array of two float point numbers.
`SCRIPT()` function takes a code block which enclosed by `{` and `}` and run it for each record.
It takes the current record via `context.value()` then yield transformed data via `context.yield()`.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
SCRIPT("tengo", {
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
  //  - yield() build and passes new value to the next step with the received key from previous step
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
```js {linenos=table,hl_lines=["2-4"],linenostart=1}
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
{{< /tabs >}} -->
