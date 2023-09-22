---
title: TQL Script
type: docs
weight: 6
---

# TQL Script
{:.no_toc}

1. TOC
{:toc}

{: .important }
> For smooth practice, the following query should be run to prepare tables and data.
> ```sql
> CREATE TAG TABLE IF NOT EXISTS EXAMPLE (NAME VARCHAR(20) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);
> INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
> INSERT INTO EXAMPLE VALUES('TAG1', TO_DATE('2021-08-13'), 11);
> ```
>

Supporting script language

1. tengo
 [tengo](https://github.com/d5/tengo) is a Golang like script.
 Supports all builtin pakcages(math, text, times, rand, fmt, json, base64, hex) of tengo except "os" excluded for the security reason.
 And added "context" package for exposing the TQL specific features.

*Syntax*: `SCRIPT({ ... script code... })`

## Context

Returns context object of the script runtime.

### yieldKey, yield

Pass the incoming arguments to the next function.

#### Output CSV

```js
SCRIPT({
    ctx := import("context")
    ctx.yield(0, 1, 2, 3)
    ctx.yield(1, 2, 3, 4)
})
CSV()
```

`result`

```
0,1,2,3
1,2,3,4
```

#### Table Append

```js
SCRIPT({
    ctx := import("context")
    ctx.yield("tag0", 100, 10)
    ctx.yield("tag0", 111, 11)
})
APPEND(table('example'))
```

`result`

```
append 2 rows (success 2, fail 0).
```

### key

Returns the key of the current record.

```js
SQL(`select * from example`)
SCRIPT({
    ctx := import("context")
    ctx.yieldKey(ctx.key(), 0, 1, 2, 3)
})
CSV()
```

`result`

```
TAG0,0,1,2,3
TAG1,0,1,2,3
```

### value

Returns the whole value of the current records in array. If the index is given, it returns the element of the values.

For example, If the current value is `[0, true, "hello", "world"]`

- `value()` returns the whole value array `[0, true, "hello", "world"]`
- `value(0)` returns the first element of the value `0`
- `value(3)` returns the last element of the value `"world"`

```js
SQL(`select * from example`)
SCRIPT({
    ctx := import("context")
    ctx.yield(ctx.value(1), 0, 1, 2, 3)
})
CSV()
```

`result`

```
10,0,1,2,3
11,0,1,2,3
```

## Time

TQL can be used to facilitate conversion between `Timestamp` and `Time format string`.

### Timestamp to Time format string

```js
STRING(param("format_time") ?? "808210800000000000", separator('\n'))
SCRIPT({
    ctx := import("context")
    times := import("times")
    text := import("text")

    epoch_txt := ctx.value()[0]
    epoch := text.parse_int(epoch_txt, 10, 64)
    epoch = epoch / 1000000000

    t_time := times.time_format(epoch, "Mon Jan 2 15:04:05 -0700 MST 2006")

    ctx.yield(epoch, t_time)
})
CSV()
```

`result`
```
808210800,Sat Aug 12 16:00:00 +0900 KST 1995
```

### Time format string to Timestamp

```js
STRING(param("timestamp") ?? "Sat Aug 12 00:00:00 -0700 MST 1995", separator('\n'))
SCRIPT({
    ctx := import("context")
    times := import("times")
    text := import("text")

    time_format := ctx.value()[0]
    epoch := times.parse("Mon Jan 2 15:04:05 -0700 MST 2006", time_format)

    ctx.yield(epoch, time_format)
})
CSV()
```

`result`

```
808210800000000000,Sat Aug 12 00:00:00 -0700 MST 1995
```

