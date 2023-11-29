---
title: TIMEWINDOW()
type: docs
weight: 62
---

## Motivation

Analyzing and visualizing data stored in a DATABASE, one of the most cumbersome tasks is the process of refining it when there is no data in the desired time range or when there are multiple data.

For example, when you try to display an time-value chart in some fixed intervals, if you simply query the data with a SELECT query and input it into the chart library, the time interval between the retrieved records may be different from the chart's time-axis (there could be no intermediate data or there are many dense data in a timer-period), making it impossible to process them in the desired format.

Usually, application developers create an array of fixed "time" intervals and iteratively fills the elements (slots) of the array by traversing the query result records. When a slot has already a value, it is maintained as a single value through a specific operation (min, max, first, last, ...), and at the last, slots without values are filled with arbitrary values (0 or NULL).

To alleviate the repetitive and cumbersome work in the application development process, a new TQL function called `TIMEWINDOW()` has been introduced in v8.0.5.

### Syntax

The syntax is as follows. {{< neo_since ver="8.0.5" />}}

```js
TIMEWINDOW(fromTime, untilTime, period, [nullValue], columns...)
```

The first and second arguments, *fromTime* and *untilTime*, are the time range of the x-axis to be drawn. Regardless of the existence of actual data, you can specify the desired time range. Note that fromTime is inclusive and untilTime is exclusive.

The third argument, period, represents the time interval. In the example above, it can be expressed as period(“1s”).

The fourth argument, nullValue, is optional, and you can specify a value to use instead of the data that does not exist for a specific slot. If not specified, it is filled with NULL, and if specified as `nullValue(0)``, it is filled with 0.

In the last variadic arguments, specify the aggregation functions as string according to the order of each column. The available values are:

| aggregations     |    description          |
|:---------------- | :---------------------- |
| `time`           | Specifies that the column in that order is the time (timestamp) of the data.  |
| `avg`            | It obtains the average of the data as the representative value of the period. |
| `sum`            | Total sum of the data                             |
| `max`, `min`     | The maximum, minimum value of the data            |
| `first`, `last`  | The first,last value of the data of the period    |
| `rss`            | Root Sum Square         |
| `rms`            | Root Mean Square        |

| statistics       | description             |
|:---------------- | :---------------------- |
| `mean`           | mean                    |
| `median`         | median (lower value)    |
| `median-interpolated` | median (lower interpolated value) |
| `stddev`         | standard deviation      |
| `stderr`         | standard error          |
| `entropy`        | Shannon entropy of a distribution. The natural logarithm is used. |

These statistic functions differ from the other aggregational functions above in that they hold all the values of the corresponding period in memory buffer and generate the value when the time window changed.

## Example

### Basic

Bringing the vibration data from the [Fast Fourier Transform](../fft/) example. In the example, data is generated every 1ms, so there are 1,000 records within 1 second. Executing the following TQL produces data at 1-second intervals, and if there is no actual data (record) in the desired time period, it is filled with the default value NULL.

```js
SQL(`select time, value from example
     where name = 'sig.1'
     and time between 1700022915692366000 and 1701022924562366000`)
TIMEWINDOW(
    time(1700022912 * 1000000000),
    time(1700022929 * 1000000000),
    period("1s"),
    "time",
    "last")
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

If you want to generate vibration data without query for briefness, Use the next example instead.

```js
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
TIMEWINDOW(
    time('now - 2s'),
    time('now + 13s'),
    period("1s"),
    "time",
    "last")
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

![ex-tw-1](../img/ex-tw-1.jpg)

### nullValue()

Let's add `nullValue(100)` and execute again. The `NULL` values are replaced with the given value `100`.

```js
TIMEWINDOW(
    time('now - 2s'),
    time('now + 13s'),
    period("1s"),
    nullValue(100),
    "time",
    "last")
```

![ex-tw-2](../img/ex-tw-2.jpg)


## Interpolation

It is possible to obtain interpolated data by referring to adjacent values beyond filling empty values (NULL) with a constant specified by `nullValue()`. Using the example above, change the last argument of TIMEWINDOW() from `"last"` to `"last:LinearRegression"` and execute it again. You can see that the value predicted by Linear Regression is filled in the row where NULL was returned because there was no value.

![ex-tw-3](../img/ex-tw-3.jpg)

The available interpolation algorithms are:

| interpolation                 | description              |
| :---------------------------- | :----------------------- |
| `:PiecewiseConstant`          | A left-continuous, piecewise constant 1-dimensional interpolator. |
| `:PiecewiseLinear`            | A piecewise linear 1-dimensional interpolator |
| `:AkimaSpline`                | A piecewise cubic 1-dimensional interpolation with continuous value and first derivative. <br/> See https://www.iue.tuwien.ac.at/phd/rottinger/node60.html |
| `:FritschButland`             | A piecewise cubic 1-dimensional interpolation with continuous value and first derivative. <br/> See Fritsch, F. N. and Butland, J., "A method for constructing local monotone piecewise cubic interpolants" (1984), SIAM J. Sci. Statist. Comput., 5(2), pp. 300-304. |
| `:LinearRegression`           | Linear regression with nearby values                  |

The example below shows how to get original data and interpolated data together at once.

```js
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
PUSHVALUE(2, value(1), 'predict')
TIMEWINDOW(
    time('now - 2s'),
    time('now + 13s'),
    period("1s"),
    "time",
    "last",
    "last:LinearRegression")
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

![ex-tw-4](../img/ex-tw-4.jpg)

### fallback

The interpolation can fail when there are not enough values nearby to predict, then the `nullValue()` is applied instead. The `nullValue()` is not given, then `NULL` is returned.