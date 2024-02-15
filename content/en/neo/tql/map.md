---
title: MAP
type: docs
weight: 31
---

*MAP* functions are the core of the transforming data.

## TAKE()

![map_take](../img/map_take.jpg)

*Syntax*: `TAKE( [offset,] n )`

Takes first *n* records and stop the stream.

- `offset` *number* optional, take records from the offset. (default 0 when omitted) {{< neo_since ver="8.0.6" />}}
- `n` *number* specify how many records to be taken.

{{< tabs items="TAKE(n),TAKE(offset n)">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
TAKE(2)
CSV()
```
```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
TAKE(3, 2)
CSV()
```
```csv
TAG0,1628953200000000000,13
TAG0,1629039600000000000,14
```
{{< /tab >}}
{{< /tabs >}}

## DROP()

![map_drop](../img/map_drop.jpg)

*Syntax*: `DROP( [offset,] n  )`

Ignore first *n* records, it simply drops the *n* records.

- `offset` *number* optional, drop records from the offset. (default 0 when omitted) {{< neo_since ver="8.0.6" />}}
- `n` *number* specify how many records to be dropped.

{{< tabs items="DROP(n),DROP(offset n)">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
DROP(3)
CSV()
```
```csv
TAG0,1628953200000000000,13
TAG0,1629039600000000000,14
TAG0,1629126000000000000,15
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
DROP(2, 3)
CSV()
```
```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
TAG0,1629126000000000000,15
```
{{< /tab >}}
{{< /tabs >}}

## FILTER()

![map_filter](../img/map_filter.jpg)

*Syntax*: `FILTER( condition )`

Apply the condition statement on the incoming record, then it pass the record only if the *condition* is *true*.

For example, if an original record was `{key: k1, value[v1, v2]}` and apply `FILTER(count(V) > 2)`, it simply drop the record. If the codition was `FILTER(count(V) >= 2)`, it pass the record to the next function.

```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
FILTER( value(2) < 12 )
CSV()
```
```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

## MAPKEY()

![map_mapkey](../img/map_mapkey.jpg)

*Syntax*: `MAPKEY( newkey )`

Replace current key value with the given newkey.

```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
MAPKEY(time("now"))
PUSHKEY("do-not-see")
CSV()
```
```csv
1701343504143299000,TAG0,1628694000000000000,10
1701343504143303000,TAG0,1628780400000000000,11
1701343504143308000,TAG0,1628866800000000000,12
1701343504143365000,TAG0,1628953200000000000,13
1701343504143379000,TAG0,1629039600000000000,14
1701343504143383000,TAG0,1629126000000000000,15
```

## PUSHKEY()

![map_pushkey](../img/map_pushkey.jpg)

*Syntax*: `PUSHKEY( newkey )`

Apply new key on each record. The orignal key is push into value tuple.

For example, if an original record was `{key: 'k1', value: [v1, v2]}` and applied `PUSHKEY(newkey)`, it produces the updated record as `{key: newkey, values: [k1, v1, v1]}`.

```js {linenos=table,hl_lines=["10"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
MAPKEY(time("now"))
PUSHKEY("do-not-see")
CSV()
```
```csv
1701343504143299000,TAG0,1628694000000000000,10
1701343504143303000,TAG0,1628780400000000000,11
1701343504143308000,TAG0,1628866800000000000,12
1701343504143365000,TAG0,1628953200000000000,13
1701343504143379000,TAG0,1629039600000000000,14
1701343504143383000,TAG0,1629126000000000000,15
```

## POPKEY()

![map_popkey](../img/map_popkey.jpg)

*Syntax*: `POPKEY( [idx] )`

Drop current key of the record, then promote *idx*th element of *tuple* as a new key.

For example, if an original record was `{key: k, value: [v1, v2, v3]}` and applied `POPKEY(1)`, it produces the updated record as `{key: v2, value:[v1, v3]}`.

if use `POPKEY()` without argument it is equivalent with `POPKEY(0)` which is promoting the first element of the value tuple as the key.

{{< tabs items="POPKEY(),POPKEY(idx)">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
POPKEY()
CSV()
```
```csv
1628694000000000000,10
1628780400000000000,11
1628866800000000000,12
1628953200000000000,13
1629039600000000000,14
1629126000000000000,15
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
POPKEY(1)
CSV()
```
```csv
TAG0,10
TAG0,11
TAG0,12
TAG0,13
TAG0,14
TAG0,15
```
{{< /tab >}}
{{< /tabs >}}

## GROUPBYKEY()

![map_popkey](../img/map_groupbykey.jpg)

*Syntax*: `GROUPBYKEY( [lazy(boolean)] )`

- `lazy(boolean)` If it set `false` which is default, *GROUPBYKEY()* yields new grouped record when the key of incoming record has changed from previous record. If it set `true`, *GROUPBYKEY()* waits the end of the input stream before yield any record. 

`GROUPBYKEY` is equivalent expression with `GROUP( by( key() ) )`.

## GROUP()

*Syntax*: `GROUP( [lazy(boolean),] by [, aggregators...] )` {{< neo_since ver="8.0.7" />}}

- `lazy(boolean)` If it set `false` which is default, *GROUP()* yields new aggregated record when the value of `by()` has changed from previous record. If it set `true`, *GROUP()* waits the end of the input stream before yield any record.

- `by(value [, name])` The value how to group the values.

- `aggregators` *array of aggregator* Aggregate functions

Group aggregation function, please refer to the [GROUP()](/neo/tql/group/) section for the detail description.

## FLATTEN()

![map_flatten](../img/map_flatten.jpg)

*Syntax*: `FLATTEN()`

It works the opposite way of *GROUPBYKEY()*. Take a record whose value is multi-dimension tuple, produces multiple records for each elements of the tuple reducing the dimension.

For example, if an original record was `{key:k, value:[[v1,v2],[v3,v4],...,[vx,vy]]}`, it produces the new multiple records as `{key:k, value:[v1, v2]}`, `{key:k, value:{v3, v4}}`...`{key:k, value:{vx, vy}}`.

## SET()

*Syntax*: `SET(name, expression)` {{< neo_since ver="8.0.12" />}}

- `name` *keyword* variable name
- `expression` *expression* value

*SET* defines a record-scoped variable with given name and value. If a new variable `var` is defined as `SET(var, 10)`, it can be refered as `$var`. Because the variables are not a part of the values, it is not included in the final result of SINK.

```js {linenos=table,hl_lines=["2-3"],linenostart=1}
FAKE( linspace(0, 1, 3))
SET(temp, value(0) * 10)
SET(temp, $temp + 1)
MAPVALUE(1, $temp)
CSV()
```

```csv
0,1
0.5,6
1,11
```
## PUSHVALUE()

*Syntax*: `PUSHVALUE( idx, value [, name] )` {{< neo_since ver="8.0.5" />}}

- `idx` *int* Index where newValue insert at. (0 based)
- `value` *expression* New value
- `name` *string* column's name (default 'column')

Insert the given value into the current values.

## POPVALUE()

*Syntax*: `PUSHVALUE( idx [, idx2, idx3, ...] )` {{< neo_since ver="8.0.5" />}}

- `idx` *int* array of indexes that will removed from values

It removes elements that specified by `idx`es from value array.

## MAPVALUE()

![map_mapvalue](../img/map_mapvalue.jpg)

*Syntax*: `MAPVALUE( idx, newValue [, newName] )`

- `idx` *int*  Index of the value tuple. (0 based)
- `newValue` *expression* New value
- `newName` *string* change column's name with given string

`MAPVALUE()` replaces the value of the element at the given index. For examaple, `MAPVALUE(0, value(0)*10)` replaces a new value that is 10 times of the first element of value tuple.

If the `idx` is out of range, it works as `PUSHVALUE()` does. `MAPVALUE(-1, value(1)+'_suffix')` inserts a new string value that concatenates '_suffix' with the 2nd element of value.

An example usage of math functions with `MAPVALUE`.

```js {linenos=table,hl_lines=["7"],linenostart=1}
FAKE(
    meshgrid(
        linspace(-1.0,1.0,200),
        linspace(-1.0, 1.0, 200)
    )
)
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1),2 )))/10 )
CHART_LINE3D(
    lineWidth(4),
    gridSize(100, 30, 100),
    visualMap(-0.12, 0.12)
)
```

{{< figure src="../img/tql-math-example2.jpg" width="400px" >}}

## MAP_DIFF()

*Syntax*: `MAP_DIFF( idx, value [, newName] )` {{< neo_since ver="8.0.8" />}}

- `idx` *int*  Index of the value tuple. (0 based)
- `value` *float*
- `newName` *string* change column's name with given string

`MAP_DIFF()` replaces the value of the element at the given index with difference between current and previous values (*current - previous*). 

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(0.5, 3, 10) )
MAPVALUE(0, log(value(0)), "VALUE")
MAP_DIFF(1, value(0), "DIFF")
CSV( header(true), precision(3) )
```

```csv
VALUE,DIFF
-0.693,NULL
-0.251,0.442
0.054,0.305
0.288,0.234
0.477,0.189
0.636,0.159
0.773,0.137
0.894,0.121
1.001,0.108
1.099,0.097
```

## MAP_ABSDIFF()

*Syntax*: `MAP_ABSDIFF( idx, value [, newName]  )` {{< neo_since ver="8.0.8" />}}

- `idx` *int*  Index of the value tuple. (0 based)
- `value` *float*
- `newName` *string* change column's name with given string

`MAP_ABSDIFF()` replaces the value of the element at the given index with abolute difference between current and previous value abs(*current - previous*).

## MAP_NONEGDIFF()

*Syntax*: `MAP_NONEGDIFF( idx, value [, newName]  )` {{< neo_since ver="8.0.8" />}}

- `idx` *int*  Index of the value tuple. (0 based)
- `value` *float*
- `newName` *string* change column's name with given string

`MAP_NONEGDIFF()` replaces the value of the element at the given index with difference between current and previous value (*current - previous*). 
If the difference is less than zero it applies zero instead of a negative value.

## MAP_MOVAVG()

*Syntax*: `MAP_MOVAVG(idx, value, lag [, newName] )`  {{< neo_since ver="8.0.8" />}}

- `idx` *int*  Index of the value tuple. (0 based)
- `value` *float*
- `lag` *integer* specifies how many records it accumulates.
- `newName` *string* change column's name with given string

`MAP_MOVAVG` replaces the value of the element at the given index with a moving average of values by given lag count.
If values are not accumulated enough to the `lag`, it applies `NULL` instead.
If all incoming values are `NULL` (or not a number) for the lastest `lag` count, it applies `NULL`.
If some accumulated values are `NULL` (or not a number), it makes average value from only valid values excluding the `NULL`s.

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(1, 10, 10) )
MAP_MOVAVG(1, value(0), 3, "MA_3")
CSV( header(true), precision(3) )
```

```csv
x,MA_3
1.000,NULL
2.000,NULL
3.000,2.000
4.000,3.000
5.000,4.000
6.000,5.000
7.000,6.000
8.000,7.000
9.000,8.000
10.000,9.000
```

## TRANSPOSE()

*Syntax*: `TRANSPOSE( [fixed(columnIdx...) | columnIdx...] [, header(boolean)] )` {{< neo_since ver="8.0.8" />}}

When TQL loads data from CSV or external RDBMS via 'bridge'd SQL query, it may require to transpose columns to fit the record shape to a MACHBASE TAG table.
`TRANSPOSE` produce multiple records from a record that has multiple columns.

- `fixed(columnIdx...)` specify which columns are "fixed", this can not mix-use with transposed columns.
- `columnIdx...` specify multiple columns which are "transposed", this can not mix-use with "fixed()".
- `header(boolean)` if it set `header(true)`, `TRANSPOSE` consider the first record is the hreader record. And it produce the header of the transposed column records as a new column.

{{< tabs items="TRANSPOSE,all columns,header(),fixed()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true), fixed(0, 1) ) // transpose column 2, 3, 4 with its header
MAPVALUE(0, strToUpper(value(0)) + "-" + value(2)) // concatenate city and transposed column name (from header)
MAPVALUE(1, parseTime(value(1), sqlTimeformat("YYYY/MM/DD"), tz("UTC"))) // conver time
MAPVALUE(3, parseFloat(value(3))) // convert value into number
POPVALUE(2) // remove transposed column name, no more needed
CSV(timeformat("s"))
```
This example is a common use case.
```csv
TOKYO-TEMPERATURE,1701907200,23
TOKYO-HUMIDITY,1701907200,30
TOKYO-NOISE,1701907200,40
BEIJING-TEMPERATURE,1701907200,24
BEIJING-HUMIDITY,1701907200,50
BEIJING-NOISE,1701907200,60
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE()
CSV()
```
It transposes all columns into rows if there is no options.
```csv
CITY
DATE
TEMPERATURE
HUMIDITY
NOISE
Tokyo
2023/12/07
23
30
40
Beijing
2023/12/07
24
50
60
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true) )
CSV()
```
It treats the first record as the header and add a new column for each transposed record.
```csv
CITY,Tokyo
DATE,2023/12/07
TEMPERATURE,23
HUMIDITY,30
NOISE,40
CITY,Beijing
DATE,2023/12/07
TEMPERATURE,24
HUMIDITY,50
NOISE,60
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["5", "7"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true), fixed(0, 1) )
// Equiv. with
// TRANSPOSE( header(true), 2, 3, 4 )
CSV()
```
It keeps the "fixed" columns for the new records.
```csv
Tokyo,2023/12/07,TEMPERATURE,23
Tokyo,2023/12/07,HUMIDITY,30
Tokyo,2023/12/07,NOISE,40
Beijing,2023/12/07,TEMPERATURE,24
Beijing,2023/12/07,HUMIDITY,50
Beijing,2023/12/07,NOISE,60
```
{{< /tab >}}
{{< /tabs >}}

## TIMEWINDOW()

*Synatax*: `TIMEWINDOW( fromTime, untilTime, period [, nullValue], columns...)` {{< neo_since ver="8.0.5" />}}

Aggregate raw values between fromTime and untilTime into a periodic duration and fill zero value if any value exists for the period.

- `fromTime` *time* from (inclusive)
- `untilTime` *time* until (exclusive)
- `period` *duration* ex: `period('1s')`
- `nullValue` if a certain period has no actual values it yields the given *alternativeValue*.(default is *NULL*) ex: `nullValue(alternativeValue)`
- `columns` *string* specifies each field's aggration function and indicates which column is the time. It should be one of pre-defines keywords. 

Please refer to the [TIMEWINDOW()](/neo/tql/timewindow/) section for the more information including interpolation methods.

## FFT()

![map_fft](../img/map_fft.jpg)

*Syntax*: `FFT()`

It assumes value of the incoming record is an array of *time,amplitude* tuples, then applies *Fast Fourier Transform* on the array and replaces the value with an array of *frequency,amplitude* tuples. The key remains same.

For example, if the incoming record was `{key: k, value[ [t1,a1],[t2,a2],...[tn,an] ]}`, it transforms the value to `{key:k, value[ [F1,A1], [F2,A2],...[Fm,Am] ]}`.

{{< tabs items="FFT(),RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9"],linenostart=1}
FAKE(
    oscillator(
        freq(15, 1.0), freq(24, 1.5),
        range('now', '10s', '1ms')
    ) 
)
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
    xAxis(0, 'Hz'),
    yAxis(1, 'Amplitude'),
    dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< tab >}}
{{< figure src="/images/web-fft-tql-2d.png" width="510" >}}
{{< /tab >}}
{{< /tabs >}}


## WHEN()

*Syntax*: `WHEN(condition, doer)` {{< neo_since ver="8.0.7" />}}

- `condition` *boolean*
- `doer` *doer*

`WHEN` runs `doer` action if the given condition is `true`.
This function does not affects the flow of records, it just executes the defined *side effect* work.

### doLog()

*Syntax*: `doLog(args...)` {{< neo_since ver="8.0.7" />}}

Prints out log message on the web console.

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(1, 2, 2))
WHEN( mod(value(0), 2) == 0, doLog(value(0), "is even."))
CSV()
```

### doHttp()

*Syntax*: `doHttp(method, url, body [, header...])` {{< neo_since ver="8.0.7" />}}

- `method` *string*
- `url` *string*
- `body` *string*
- `header` *string* optional

`doHttp` requests the http endpoints with given method, url, body and headers.

**Use cases**

- Notify an event to the specific HTTP endpoint.

```js {linenos=table,hl_lines=["4"],linenostart=1}
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("GET", strSprintf("http://127.0.0.1:8888/notify?value=%.0f", value(0)), nil)
)
CSV()

```

- Post the current record to the specific HTTP endpoint in CSV which is default format of `doHttp`.

```js {linenos=table,hl_lines=["4"],linenostart=1}
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("POST", "http://127.0.0.1:8888/notify", value())
)
CSV()
```

- Post the current record in a custom JSON format to the specific HTTP endpoint.

```js {linenos=table,hl_lines=["4-8"],linenostart=1}
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("POST", "http://127.0.0.1:8888/notify", 
        strSprintf(`{"message": "even", "value":%f}`, value(0)),
        "Content-Type: application/json",
        "X-Custom-Header: notification"
    )
)
CSV()
```

### do()

*Syntax*: `do(args..., { sub-flow-code })` {{< neo_since ver="8.0.7" />}}

`do` executes the given sub flow code with passing `args...` arguments.

It is important to keep in mind that `WHEN()` is only for executing a side effect job on a certain condition.
`WHEN-do` sub flow cannot affects to the main flow, which means it cannot use SINKs that produce result on output stream like `CSV`, `JSON`, and `CHART_*`. The output of a sub flow will be ignored silently, any writing attempts from a sink are ignored and showing warning messages.

Effective SINKs in a sub flow may be `INSERT` and `APPEND` which is not related with output stream, so that it can write the specific values on a different table from main TQL flow. Otherwise use `DISCARD()` sink, it silently discards any records in the sub flow without warning messages.

```js {linenos=table,hl_lines=["9-13"],linenostart=1}
FAKE( json({
    [ 1, "hello" ],
    [ 2, "你好" ],
    [ 3, "world" ],
    [ 4, "世界" ]
}))
WHEN(
    mod(value(0), 2) == 0,
    do( "Greetings:", value(0), value(1), {
        ARGS()
        WHEN( true, doLog( value(0), value(2) ) )
        DISCARD()
    })
)
CSV()
```

The log messages of the above code shows the two important points.

1. The main flow is bloked and waits until its sub flow finishes the job.
2. The sub flow is executed every time for a record that matches the condition.

```
2023-12-02 07:54:42.160 TRACE 0xc000bfa580 Task compiled FAKE() → WHEN() → CSV()
2023-12-02 07:54:42.160 TRACE 0xc000bfa840 Task compiled ARGS() → WHEN() → DISCARD()
2023-12-02 07:54:42.160 INFO  0xc000bfa840 Greetings: 你好
2023-12-02 07:54:42.160 DEBUG 0xc000bfa840 Task elapsed 254.583µs
2023-12-02 07:54:42.161 TRACE 0xc000bfa9a0 Task compiled ARGS() → WHEN() → DISCARD()
2023-12-02 07:54:42.161 INFO  0xc000bfa9a0 Greetings: 世界
2023-12-02 07:54:42.161 DEBUG 0xc000bfa9a0 Task elapsed 190.552µs
2023-12-02 07:54:42.161 DEBUG 0xc000bfa580 Task elapsed 1.102681ms
```

**Use cases**

When sub flow retrieves data from other than its arguments, it can access the arguments with `args([idx])` option function.

- Execute query with sub flow's arguments.

```js
// pseudo code
// ...
WHEN( condition,
    do(value(0), {
        SQL(`select time, value from table where name = ?`, args(0))
        // ... some map functions...
        INSERT(...)
    })
)
// ...
```

- Retrieve csv file from external web server

```js
// pseudo code
// ...
WHEN( condition,
    do(value(0), value(1), {
        CSV( file( strSprintf("https://exmaple.com/data_%s.csv?id=%s", args(0), escapeParam(args(1)) )))
        WHEN(true, doHttp("POST", "http://my_server", value()))
        DISCARD()
    })
)
// ...
```

## THROTTLE()

*Syntax*: `THROTTLE(tps)` {{< neo_since ver="8.0.8" />}}

- `tps` *float* specify in number of records per a second.

`THROTTLE` relays a record to the next step with delay to fit to the specified *tps*.
It makes data flow which has a certain period from stored data (e.g a CSV file), 
so that *simulates* a sensor device that sends measurements by periods.

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE(linspace(1,5,5))
THROTTLE(5.0)
WHEN(true, doLog("===>tick", value(0)))
CSV()
```

- At console log, each log time of "tick" message has *200ms.* difference (5 per a second).
```
2023-12-07 09:33:30.131 TRACE 0x14000f88b00 Task compiled FAKE() → THROTTLE() → WHEN() → CSV()
2023-12-07 09:33:30.332 INFO  0x14000f88b00 ===>tick 1
2023-12-07 09:33:30.533 INFO  0x14000f88b00 ===>tick 2
2023-12-07 09:33:30.734 INFO  0x14000f88b00 ===>tick 3
2023-12-07 09:33:30.935 INFO  0x14000f88b00 ===>tick 4
2023-12-07 09:33:31.136 INFO  0x14000f88b00 ===>tick 5
2023-12-07 09:33:31.136 DEBUG 0x14000f88b00
Task elapsed 1.005070167s
```

## SCRIPT()

*Syntax*: `SCRIPT({ ... script code... })`

Supporting user defined script language.

See [SCRIPT](../script/) section for the details with examples.

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

### context package

#### context.yield()

Pass the incoming arguments to the next function.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["3-4"],linenostart=1}
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

#### context.key()

Returns the key of the current record.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
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

### times package

#### times.time_format()

Convert timestamp to a string.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["11"],linenostart=1}
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


#### times.parse()

Convert a string to timestamp.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["8"],linenostart=1}
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

### Example

Open a new *tql* editor on the web ui and copy the code below and run it.

In this example, `linspace(-4,4,100)` generates an array contains 100 elements which are ranged from -4.0 to 4.0 in every `8/100` step. `meshgrid()` takes two array and produce meshed new array. As result of FAKE() in the example produces an array of 10000 elements (100 x 100 meshed) contains array of two float point numbers.
`SCRIPT()` function takes a code block which enclosed by `{` and `}` and run it for each record.
It takes the current record via `context.value()` then yield transformed data via `context.yield()`.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
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
{{< /tabs >}}
