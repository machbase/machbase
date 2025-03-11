---
title: Basics
type: docs
weight: 02
---

## Primitive types

TQL has three types for primitive `string`, `number`, `boolean` and `time`.

### string

Define constant strings as like traditional programming languages with quotation marks, single('), double (") and backtick(`).
The backtick'ed string is useful when you need to define a string in multiple lines including quotation marks inside such as long SQL statement.


*Example)* Escaping single quote with backslash(`\'`)

```js {linenos=table}
SQL( 'select * from example where name=\'temperature\' limit 10' )
CSV()
```

*Example)* Double quote string

```js {linenos=table}
SQL( "select * from example where name='temperature' limit 10" )
CSV()
```

*Example)* Use multi-lines sql statement without escaping by backtick(`)

```js {linenos=table}
SQL( `select * 
      from example 
      where name='temperature'
      limit 10` )
CSV()
```

There is a user convenient way specifying JSON string in a TQL script by using double braces.
It doesn't require quotation marks escaping.

The two string expressions used below are equivalent.

```js {linenos=table}
STRING({{ 
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}})
CSV()
```

```js {linenos=table}
STRING(`{ 
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}`)
CSV()

```

### number

TQL treats all numeric constants as 64bit floating number.

```js {linenos=table}
SQL_SELECT( 'time', 'value', from('example', 'temperature'), limit(10))
CSV()
```

```js {linenos=table}
FAKE( oscillator( freq(12.34, 20), range("now", "1s", "100ms")) )
CSV()
```

### boolean

`true` and `false`

```js {linenos=table}
FAKE( linspace(0, 1, 1))
CSV( heading(false) )
```

### time

Time type values can be created by calling `time()`, `parseTime()` functions, or retrieved from `datetime` column of a SQL query result.

### timeZone

TimeZone type values can be created by calling `tz()` function.

ex) `tz('UTC')`, `tz('Local')`, `tz('Asia/Seoul')`

### list

A list is an array of other values, it can be created by calling `list()` function.

ex) `list(1, 2, 3)`

### dictionary

A dictionary is a set of (string) name and value pairs, created by calling `dict()` function.

ex) `dict("name", "pi", "value", 3.14)`

## Statements

Every statement in TQL should be a function call except the literal constants of string, number and boolean.

```js
// A comment line starts with '//'

// Each statement should start from first column.
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
CSV()
```

## SRC and SINK

Every `.tql` script should start with one source statement which can generates a record or records.
For example, `SQL()`, `SQL_SELECT()` and `SCRIPT()` that generates records with `yield()`, `yieldKey()` can be a source.
And the last statement should be a sink statement that encode the result or write into the database.
For example, `APPEND()`, `INSERT()` and all `CHART()` functions can be a sink.

## MAP functions

There may be zero or more map functions between source and sink statements.
The names of all map functions are with capital letters, in contrast lower case camel notation functions are used as arguments of the other map functions.

```js {linenos=table,hl_lines=["6-7"],linenostart=1}
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
DROP(5)
TAKE(5)
CSV()
```

## Param

When external applications call a *.tql script via HTTP it can provide arguments as query parameters.
The function `param()` is purposed to retrieve the values from query parameters in TQL script.

If the script below saved as 'hello2.tql', applications can call this script by HTTP GET method with `http://127.0.0.1:5654/db/tql/hello2.tql?name=temperature&count=10`.
Then `param('name')` returns "temperature", `param('count')` is 10, as expected.

```js {linenos=table}
SQL_SELECT(
    'time', 'value',
    from('example', param('name')),
    limit( param('count') )
)
CSV()
```

**Example**

{{% steps %}}

### Use `param()`

Save the code below as `example.tql`.

```js
SQL( `select * from example where name = ?`, param('name'))
CSV()
```

### Client GET request

Invoke the tql file with `curl` command with query parameter.

```
curl http://127.0.0.1:5654/db/tql/param.tql?name=TAG0
```

{{% /steps %}}

## Operators

### Arithmetic Operators

The arithmetic operators perform addition `+`, subtraction `-`, multiplication `*`, division `/` operations.

```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 10, 5))
MAPVALUE( 1, value(0) * 100 )
CSV()
```

```csv
1,100
3.25,325
5.5,550
7.75,775
10,1000
```

### Modulo Operator

The modulo operator (also known as the modulus operator), denoted by `%`, is an arithmetic operator.
The modulo division operator produces the remainder of an integer division which is also called the modulus of the operation.

```js {linenos=table,hl_lines=[2]}
FAKE(arrange(1, 10, 1))
FILTER(value(0) % 3 == 0)
CSV()
```

```csv
3
6
9
```

### Concatenation

If operator `+` takes strings as its operands, it returns concatenated string.

```js {linenos=table,hl_lines=[4]}
FAKE(json({
    ["hello", "world"]
}))
MAPVALUE(2, value(0) + " " + value(1) + "?")
CSV()
```

```csv
hello,world,hello world?
```

### Relational Operator

| Relational Op.         | Operator | Desc. |
| :--------------------- | :--  | :-- |
| Equality               | `==` | Returns TRUE if the operands are equal |
| Inequality             | `!=` | Returns TRUE if the operands are not equal |
| Greater Than           | `>`  | Test whether the value of the left operand is greater than the value of the right |
| Greater Than or Equal  | `>=` | Test whether the value of the left operand is greater than or equal to the value of the right |
| Less Than              | `<`  | Test whether the value of the left operand is less than the value of the right |
| Less Than or Equal     | `<=` | Test whether the value of the left operand is less than or equal to the value of the right |


```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 5, 5))
FILTER( value(0) >= 4 )
CSV()
```

```csv
4
5
```

### Logical Operators

Logical operators perform and, or, and not operations.

| Logical Op.| Operator | Desc. |
| :-- | :--  | :-- |
| AND | `&&` | Returns TRUE if both operands evaluate to TRUE |
| OR  | `\|\|` | Returns TRUE if either operand evaluates to TRUE |
| NOT | `!`  | Takes only one operand |

```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 5, 5))
FILTER( value(0) > 0  && mod(value(0), 2) == 0 )
CSV()
```

```csv
2
4
```

### IN Operator

`A in (args...)` returns true if the args contains `A`, otherwise it returns false.

```js {linenos=table,hl_lines=[7]}
FAKE(json({
    ["A", 1.0],
    ["B", 1.5],
    ["C", 2.0],
    ["D", 2.5]
}))
FILTER( value(0) in ("A", "C") )
CSV()
```

```js {linenos=table,hl_lines=[7]}
FAKE(json({
    ["A", 1.0],
    ["B", 1.5],
    ["C", 2.0],
    ["D", 2.5]
}))
FILTER( value(1) in (1.5, 2.5) )
CSV()
```

### Ternary Operator

The ternary operator `? :` is kind of similar to the if-else statements in other programming languages
as it follows the same algorithm as of if-else statement

- Whether param('name') is defined

```js {linenos=table,hl_lines=[4]}
SQL_SELECT(
    'time', 'value',
    from('example',
        param('name') == NULL ? 'temperature' : param('name')
    ),
    limit( param('count') ?? 10 )
)
CSV()
```

- Conditional value changes

```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 5, 5))
MAPVALUE(0, mod(value(0), 2) == 0 ? value(0)*10 : value(0))
CSV()
```

```
1
20
3
40
5
```

### Nil coalescing

`??` operator takes left and right operand. if left operand is defined it returns value of it, if left operand is not defined it returns right operand instead.
The example below shows the common use case of the `??` operator. If caller did not provide query param variables, the right side operand will be taken as a default value.

```js {linenos=table,hl_lines=[3]}
SQL_SELECT(
    'time', 'value',
    from('example', param('name') ?? 'temperature'),
    limit( param('count') ?? 10 )
)
CSV()
```

> {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}}
> When tql script is saved, the editor shows the link icon on the top right corner, click it to copy the address of the script file.

**Example**

{{% steps %}}

#### Use `??`

Save the code below as `param-default.tql`.

```js
SQL( `select * from example limit ?`, param('limit') ?? 1)
CSV()
```

#### HTTP GET

GET request without query param

```sh
curl http://127.0.0.1:5654/db/tql/param-default.tql
```

```csv
TAG0,1628694000000000000,10
```

#### HTTP GET with param

GET request with query param

```sh
curl http://127.0.0.1:5654/db/tql/param-default.tql?limit=2
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

{{% /steps %}}

## Pragma

The `//+ name=value` directive provides instructions on how Machbase Neo should execute the TQL script.

### log-level

{{< neo_since ver="8.0.47" />}}

Set the log-level to one of `[TRACE | DEBUG | INFO | WARN | ERROR]`.
The default is `ERROR`, which suppresses most log messages when called from HTTP and MQTT APIs.

```js {linenos=table,hl_lines=["1"]}
//+ log-level=TRACE
SQL(`select * from my_table where name = ?`, param("name"))
WHEN(true, doLog('hello world'))
CSV()
```

### sql-thread-lock

{{< neo_since ver="8.0.47" />}}

This pragma ensures that the specified `SQL()` runs on a dedicated native thread,
which is terminated once the TQL script completes.
It works only with the SRC `SQL()`.

According to the internal performance tests that runs a hundred HTTP clients simultaneously request to execute the TQL file,
it increases response latency by 35% compared to running without this option,
but it significantly reduces memory consumption.

```js {linenos=table,hl_lines=["1"]}
//+ sql-thread-lock
SQL(`select * from my_table where name = ?`, param("name"))
WHEN(true, doLog('hello world'))
CSV()
```
