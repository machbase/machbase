---
title: GROUP()
type: docs
weight: 60
---

{{< neo_since ver="8.0.7" />}}

## Syntax

```
GROUP( [lazy(boolean),] by [, aggregator...] )
```

- `lazy(boolean)` set lazy mode (default: false)
- `by(value [, timewindow()] [, name])` specify how to make group with given value.
- `aggregator` *list of aggregator*, comma separated multiple functions are possible.

> See the [basic example](#basic)


### `by()`

`by()` takes value as the first argument and optionaly `timewindow()` and `name`.

*Syntax*: `by( value [, timewindow] [, name] )`

- `value` grouping value, usually it might be time.
- `timewindow(from, until, period)` timewindow option. 
- `name` *string* set new column name, (default "GROUP")

### `lazy()`

*Syntax*: `lazy(boolean)`

If it set `false` which is default, *GROUP()* works comparing the value of `by()` of the current record to the other value of previous record,
if it founds the value has been changed, then produces new record. As result it can make a group only if the continuous records have a same value of `by()`.
If `lazy(true)` is set, *GROUP()* waits the end of the input stream before yield any record to collecting all records, so that un-sorted `by()` value can be grouped, but it causes heavy memory consumption.

### `timewindow()`

*Syntax*: `timewindow( from, until, period )` {{< neo_since ver="8.0.13" />}}

- `from`, `until` *time* are the time range. Note that *from* is inclusive and *until* is exclusive.
Regardless of the existence of actual data, you can specify the desired time range.
- `period` *duration* represents the time interval between *from* and *until*.

> See the [timewindow example](#timewindow-1)

### `aggregator`

If no aggregator is specified `GROUP` make new array of the raw records for a each group by default.
Takes multiple continuous records that have same value of `by()`, then produces a new record which have value array contains all individual values. For example, if an original records was `{key:k, value:[v1, v2]}`, `{key:k, value:{v3, v4}}`...`{key:k, value:{vx, vy}}`, `GROUP( by(key()) )` produces the new record as `{key:k, value:[[v1,v2],[v3,v4],...,[vx,vy]]}`.

## Aggregator

*Syntax*: `function_name( value [, value...] [, where()] [, nullValue()] [, predict()] [, name])`

- `value` one or more values depends on the function.
- `where( predicate )` take boolean expression for the predication.
- `nullValue(alternative)` specify alternative value to use instead of `NULL` when the aggregator has no value to produce.
- `predict(algorithm)` specify an algorithm to predict value to use instead of `NULL` when the aggregator has no value to produce.
- `name` *string* set the name of the column (default is the name of aggregator).

There are two types of aggregator functions, Type 1 functions only keep the final candidate value for the result.
Type 2 functions hold the whole data of a group, it uses the data to produce the result of the aggregation then release memory for the next group.
If `GROUP()` use `lazy(true)` and Type 2 functions together, it holds the entire input data of the related columns.

#### where()

*Syntax*: `where(predicate)` {{< neo_since ver="8.0.13" />}}

> See the [where example](#where-1)

#### nullValue()

*Syntax*: `nullValue(alternative)` {{< neo_since ver="8.0.13" />}}

> See the [nullValue example](#nullvalue-1)

#### predict()

*Syntax*: `predict(algorithm)` {{< neo_since ver="8.0.13" />}}

> See the [predict example](#predict-1)

| algorithm                    | description              |
| :--------------------------- | :----------------------- |
| `PiecewiseConstant`          | A left-continuous, piecewise constant 1-dimensional interpolator. |
| `PiecewiseLinear`            | A piecewise linear 1-dimensional interpolator |
| `AkimaSpline`                | A piecewise cubic 1-dimensional interpolation with continuous value and first derivative. <br/> See https://www.iue.tuwien.ac.at/phd/rottinger/node60.html |
| `FritschButland`             | A piecewise cubic 1-dimensional interpolation with continuous value and first derivative. <br/> See Fritsch, F. N. and Butland, J., "A method for constructing local monotone piecewise cubic interpolants" (1984), SIAM J. Sci. Statist. Comput., 5(2), pp. 300-304. |
| `LinearRegression`           | Linear regression with nearby values                  |

### options

`where()`, `nullValue()`, `predict()` and `name` arguments are the optional and it represents the `option` of the each function syntax description below.

### functions

#### avg()

Type 1, *Syntax*: `avg(value [, option...])` 

#### sum()

Type 1, *Syntax*: `sum(value [, option...])` 

#### first()

Type 1, *Syntax*: `first(value [, option...])` 

#### last()

Type 1, *Syntax*: `last(value [, option...])` 

#### min()

Type 1, *Syntax*: `min(value [, option...])` 

#### max()

Type 1, *Syntax*: `max(value [, option...])` 

#### rss()

Type 1, *Syntax*: `max(value [, option...])` 

Root sum square

#### rms()

Type 1, *Syntax*: `rms(value [, option...])` 

Root mean square

#### lrs()

Type 2, *Syntax*: `lrs(x, y [, option...])` {{< neo_since ver="8.0.13" />}}

Linear Regression Slope, assuming *x*-*y* is a point on a othogonal coordinate system. *x* can be number or time type.

#### mean()

Type 2, *Syntax*: `mean(value [, option...])` 

#### quantile()

Type 2, *Syntax*: `quantile(value, p [, option...])` {{< neo_since ver="8.0.13" />}}

Quantile (lower value)

#### quantileInterpolated()

Type 2, *Syntax*: `quantileInterpolated(value, p [, option...])` {{< neo_since ver="8.0.13" />}}

Quantile (lower value)

#### median()

Type 2, *Syntax*: `median(value [, option...])`

Equivalent to `quantile(value, 0.5 [, option...])` 

#### medianInterpolated()

Type 2, *Syntax*: `medianInterpolated(value [, option...])`

Equivalent to `quantileInterpolated(value, 0.5 [, option...])` 

#### stddev()

Type 2, *Syntax*: `stddev(value [, option...])`

standard deviation 

#### stderr()

Type 2, *Syntax*: `stderr(value [, option...])`

standard error 

#### entropy()

Type 2, *Syntax*: `entropy(value [, option...])`

Shannon entropy of a distribution. The natural logarithm is used.

#### mode()

Type 2, *Syntax*: `mode(value [, option...])`

The most common value in the dataset.

Strict float64 equality is used when comparing values, so users should take caution.
If several values are the mode, any of them may be returned.

## Examples

### Basic

```js {linenos=table,hl_lines=["4-9"],linenostart=1}
FAKE(json({
    ["A",1], ["A",2], ["B",3], ["B", 4]
}))
GROUP(
    by( value(0), "CATEGORY" ),
    avg( value(1), "AVG" ),
    sum( value(1), "SUM"),
    first( value(1) * 10, "x10")
)
CSV( header(true) )
```

**Result**
{{< figure src="../img/group-type1-ex1.jpg" width="600" >}}

### timewindow()

`FAKE()` generates time-value at every 1ms, so there are 1,000 records within 1 second.
Executing the below TQL produces data at 1-second intervals (`period("1s")` in `timewindow()`),
and if there is no actual data (record) in the desired time period, it is filled with the default value NULL.

```js {linenos=table,hl_lines=[8],linenostart=1}
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
GROUP(
    by( value(0),
        timewindow(time('now - 2s'), time('now + 13s'), period("1s")),
        "TIME"
    ),
    last( value(1),
          "LAST"
    )
)
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

{{< figure src="../img/group-tw-ex1.jpg" >}}

### nullValue()

Let’s add nullValue(100) and execute again. The NULL values are replaced with the given value 100.

```js {linenos=table,hl_lines=[12],linenostart=1}
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
GROUP(
    by( value(0),
        timewindow(time('now - 2s'), time('now + 13s'), period("1s")),
        "TIME"
    ),
    last( value(1),
          nullValue(100),
          "LAST"
    )
)
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

{{< figure src="../img/group-tw-ex2.jpg" >}}

### predict()

It is possible to obtain interpolated data by referring to adjacent values beyond filling empty values (NULL) with a constant specified by `nullValue()`.
Using the example above, add `predict("LinearRegression")` to `last()` and execute it again. You can see that the value predicted by Linear Regression is filled in the records where NULL was returned because there was no value.

The `predict()` may fail to produce interpolation value when there are not enough values nearby to predict, then the `nullValue()` is applied instead. If `nullValue()` is not given, then `NULL` is returned.

```js {linenos=table,hl_lines=[12],linenostart=1}
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
GROUP(
    by( value(0),
        timewindow(time('now - 2s'), time('now + 13s'), period("1s")),
        "TIME"
    ),
    last( value(1),
          predict("LinearRegression"),
          nullValue(100),
          "LAST"
    )
)
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

{{< figure src="../img/group-tw-ex3.jpg" >}}

### where()

Let's say there are two sensors that measure temperature and humidity, each one store the data per every 1 sec.
In real world, there is always time difference among the sensor systems. So the stored data might be below samples.

{{< figure src="../img/group-where-ex1.jpg" >}}

Record #5 humidity data store earlier than expect and it happens on record #9 again.
Let's normalize the data in second precision.

```js {linenos=table,hl_lines=["15-18"],linenostart=1}
FAKE( json({
    ["temperature", 1691800174010, 16],
    ["humidity",    1691800174020, 64],
    ["temperature", 1691800175001, 17],
    ["humidity",    1691800175010, 63],
    ["humidity",    1691800176999, 66],
    ["temperature", 1691800176020, 18],
    ["temperature", 1691800177125, 18],
    ["humidity",    1691800177293, 66],
    ["humidity",    1691800177998, 66],
    ["temperature", 1691800178184, 18]
}) )
MAPVALUE(1, parseTime(value(1), "ms", "UTC"))

GROUP(
    by( roundTime(value(1), "1s")),
    avg( value(2) )
)

CSV( timeformat("Default"), header(true) )
```

{{< figure src="../img/group-where-ex2.jpg" width="600">}}

`roundTime(..., "1s")` makes time value aligned in second, then make records grouped that has same time.
`avg(...)` produces the average value of a group.

But it lost first column value that indicates temperature and humidity, so the result values are meaningless.
To solve this problem use `where()`. Aggregator functions accept values only when `where()` returns `true`.

```js {linenos=table,hl_lines=[4,7],linenostart=15}
GROUP(
    by( roundTime(value(1), "1s"), "TIME"),
    avg( value(2),
         where( value(0) == 'temperature' ),
         "TEMP" ),
    avg( value(2),
         where( value(0) == 'humidity' ),
         "HUMI" )
)
```

{{< figure src="../img/group-where-ex3.jpg" width="600" >}}

It is also possible to interpolate the missing data of the last record with `predict()` or `nullValue()`

```js {linenos=table,hl_lines=[8],linenostart=15}
GROUP(
    by( roundTime(value(1), "1s"), "TIME"),
    avg( value(2),
         where( value(0) == 'temperature' ),
         "TEMP" ),
    avg( value(2),
         where( value(0) == 'humidity' ),
         predict("PiecewiseLinear"),
         "HUMI" )
)
```

{{< figure src="../img/group-where-ex4.jpg" width="600" >}}

### Chart

```js {linenos=table,hl_lines=["4-8"],linenostart=1}
CSV(file("https://machbase.com/assets/example/iris.csv"))
FILTER( strToUpper(value(4)) == "IRIS-SETOSA")
GROUP( by(value(4)), 
    min(value(0), "Min"),
    median(value(0), "Median"),
    avg(value(0), "Avg"),
    max(value(0), "Max"),
    stddev(value(0), "StdDev.")
)
CHART(
    chartOption({
        "xAxis": { "type": "category", "data": ["iris-setosa"]},
        "yAxis": {},
        "legend": {"show": "true"},
        "series": [
            {"type":"bar", "name": "Min", "data": column(1)},
            {"type":"bar", "name": "Median", "data": column(2)},
            {"type":"bar", "name": "Avg", "data": column(3)},
            {"type":"bar", "name": "Max", "data": column(4)},
            {"type":"bar", "name": "StdDev.", "data": column(5)}
        ]
    })
)
```

**Result**
{{< figure src="../img/groupbykey_stddev.jpg" width="476" >}}
