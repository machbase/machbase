---
title: FFT()
type: docs
weight: 70
---

## Fast Fourier Transform

{{< callout emoji="📌" >}}
For smooth practice, the following query should be run to prepare tables and data.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## Generates sample data

Open a new *tql* editor on the web ui and copy the code below and run it.

In this example, `oscillator()` generates a composite wave of 15Hz 1.0 + 24Hz 1.5.
And `CHART_SCATTER()` has `dataZoom()` option function that provides an slider under the x-Axis.

{{< tabs >}}
{{< tab name="SCRIPT" >}}
```js {linenos=table,hl_lines=["3-11"],linenostart=1}
SCRIPT({
    const m = require('mathx');
    const data = m.oscillator({
        components: [
            { frequencyHz:15, amplitude:1.0 },
            { frequencyHz:24, amplitude:1.5 },
        ],
        timeRange: { from:"now", to:"now+10s"},
        sample:"1000Hz",
        noise: { amplitude: 0.3 },
    });
    const s = m.series(data, {xKey:"ts", yKey:"amp"})
    $.yield({
        xAxis:{ data: s.ts },
        yAxis: {},
        series: [ { type:"scatter", data: s.amp } ],
        dataZoom: { type: 'slider', start: 95, end: 100 },
    })
})
CHART( size("600px", "350px") )
```
{{</ tab >}}
{{< tab name="FAKE" >}}
```js {linenos=table,hl_lines=["2-5"],linenostart=1}
FAKE( 
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
CHART_SCATTER( size("600px", "350px"), dataZoom('slider', 95, 100) )
```
{{</ tab >}}
{{</ tabs >}}

{{< figure src="/images/web-fft-tql-fake.png" width="500" >}}

## Store data into database

Store the generated data into the database with the tag name 'signal'.

{{< tabs >}}
{{< tab name="SCRIPT" >}}
```js {linenos=table,hl_lines=[13,16]}
SCRIPT({
    const m = require('mathx');
    const data = m.oscillator({
        components: [
            { frequencyHz:15, amplitude:1.0 },
            { frequencyHz:24, amplitude:1.5 },
        ],
        timeRange: { from:"now", to:"now+10s"},
        sample:"1000Hz",
        noise: { amplitude: 0.3 },
    });
    for( d of data ) {
        $.yield(d[0], d[1]);
    }
})
SQL('insert into example values(?,?,?)','signal',value(0),value(1))
```
{{</ tab >}}
{{< tab name="FAKE" >}}
```js {linenos=table,hl_lines=["10"],linenostart=1}
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
SQL('insert into example values(?,?,?)','signal',value(0),value(1))
```
{{</ tab >}}
{{</ tabs >}}

It will show "10000 rows inserted." message in the "Result" pane.

For a comment, it took about *270ms* in a test machine (Apple mac mini M1), but using `APPEND()` method in the example below, took *65ms* (x4 faster).

{{< tabs >}}
{{< tab name="SCRIPT" >}}
```js {linenos=table,hl_lines=[13,16]}
SCRIPT({
    const m = require('mathx');
    const data = m.oscillator({
        components: [
            { frequencyHz:15, amplitude:1.0 },
            { frequencyHz:24, amplitude:1.5 },
        ],
        timeRange: { from:"now", to:"now+10s"},
        sample:"1000Hz",
        noise: { amplitude: 0.3 },
    });
    for( d of data ) {
        $.yield('signal', d[0], d[1]);
    }
})
APPEND( table('example') )
```
{{</ tab >}}
{{< tab name="FAKE" >}}
```js {linenos=table,hl_lines=[10,14]}
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
PUSHVALUE(0,'signal')
// |    0         1      2
// +--> 'signal' time   magnitude
// |
APPEND( table('example') )
```
{{</ tab >}}
{{</ tabs >}}

{{< callout type="warning" >}}
The 'APPEND' works only when fields of input records exactly match with columns of the table in order and types.
{{< /callout >}}

## Read data from database

The code below reads the stored data from the 'example' table.

{{< tabs >}}
{{< tab name="SQL">}}
```js
SQL(`select time, value from example where name = 'signal' order by time`)
CHART(
    size("600px", "350px"), 
    chartOption({
        xAxis:{ data: column(0) },
        yAxis:{},
        series:[ {type:"line", data: column(1), showAllSymbol:true } ],
        dataZoom:{type:"slider", start:95, end: 100},
    })
)
```
{{</ tab >}}
{{< tab name="SQL_SELECT">}}
```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
CHART_LINE( size("600px", "350px"), dataZoom('slider', 95, 100))
```
{{</ tab >}}
{{</ tabs >}}

{{< figure src="/images/web-fft-tql-query.png" width="500" >}}

## Fast Fourier Transform

Add few data manipulation function between `SQL_SELECT()` source and `CHART_LINE()` sink.

{{< tabs >}}
{{< tab name="SQL">}}
```js
SQL(`select time, value from example where name = 'signal' order by time`)
CHART(
    size("600px", "350px"), 
    chartOption({
        xAxis:{ data: column(0) },
        yAxis:{},
        series:[ {type:"line", data: column(1), showAllSymbol:true } ],
        dataZoom:{type:"slider", start:95, end: 100},
    })
)
```
{{</ tab >}}
{{< tab name="SQL_SELECT">}}
```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
CHART_LINE( size("600px", "350px"), dataZoom('slider', 95, 100))
```
{{</ tab >}}
{{</ tabs >}}

{{< figure src="/images/web-fft-tql-query.png" width="500" >}}

## 고속 푸리에 변환 수행

`SQL_SELECT()` 소스와 `CHART_LINE()` 싱크 사이에 몇 가지 데이터 변환 함수를 추가합니다.

{{< tabs >}}
{{< tab name="GROUPBYKEY" >}}
```js {linenos=table,hl_lines=["2-4"],linenostart=1}
SQL(`select time, value from example where name = 'signal' order by time`)
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< tab name="SCRIPT-1" >}}
```js {linenos=table,hl_lines=12}
SQL(`select time, value from example where name = 'signal' order by time`)
SCRIPT({
    var times = [];
    var values = [];
},{
    ts = $.values[0];
    val = $.values[1];
    times.push(ts);
    values.push(val);
},{
    const mx = require("mathx");
    const result = mx.fft(times, values);
    const s = mx.series(result, {xKey:"freq", yKey:"amp"});
    $.yield({
        xAxis:{ name: "Hz", data: s.freq, axisLabel:{ }},
        yAxis:{ name: "Amplitude" },
        series:[ { type:"line", data: s.amp} ],
        dataZoom: { type:"slider", start: 0, end: 10 },
        tooltip:{ trigger: "axis" },
    });
})
CHART(size("600px", "350px"))
```
{{</ tab >}}
{{< tab name="SCRIPT-2" >}}
```js {linenos=table,hl_lines=[11,12],linenostart=1}
SQL(`select time, value from example where name = 'signal' order by time`)
SCRIPT({
    var times = [];
    var values = [];
},{
    ts = $.values[0];
    val = $.values[1];
    times.push(ts);
    values.push(val);
},{
    const mx = require("mathx");
    result = mx.fft(times, values);
    for(i = 0; i < result.length; i++) {
        $.yield(...result[i]);
    }
})
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/images/web-fft-tql-2d.png" width="500" >}}

## How it works

{{% steps %}}

### SQL_SELECT()
`SQL_SELECT(...)` yields records from the query result in the form of `{key: rownum, value: (time, value) }`

### MAPKEY('sample')
`MAPKEY('sample')` sets the constant string 'sample' as a new key for all records.
As result all records have same *key* `'sample'` and `(time, value)` as *value*. `{key: 'sample', value:(time, value)}`

### GROUPBYKEY()
`GROUPBYKEY()` merge all records that has the same key. In this example, all query results are combined into a record that has same *key* 'sample' and value is an array of tuples which formed `{key: 'sample', value:[ (time1, value1), (time2, value2), ..., (timeN, valueN) ]}`.

### FFT()
`FFT()` applies Fast Fourier Transform on the value of the record and transform the value (time-value) into an array of tuples (frequency-amplitude). `{key: 'sample', value:[ (Hz1, Ampl1), (Hz2, Ampl2), ... ]}`.

{{% /steps %}}

## Adding time axis

```js {linenos=table,hl_lines=["3-7"],linenostart=1}
SQL_SELECT( 'time', 'value', from('example', 'signal'), between('last-10s', 'last'))

MAPKEY( roundTime(value(0), '500ms') )
GROUPBYKEY()
FFT(minHz(0), maxHz(100))
FLATTEN()
PUSHKEY('fft')
CHART_BAR3D(
      xAxis(0, 'time', 'time'),
      yAxis(1, 'Hz'),
      zAxis(2, 'Amp'),
      size('600px', '600px'), visualMap(0, 1.5), theme('westeros')
)
```

{{< figure src="/images/web-fft-tql-3d.png" width="500" >}}

## How it works

{{% steps %}}

### SQL_SELECT()

`SQL_SELECT(...)` yields records from the query result. `{key: time, value: (value) }`

### MAPKEY()
`MAPKEY( roundTime(value(0), '500ms'))` sets the new key with the result of roundTime `value(0)` by 500 milliseconds. 
As result the records are transformed into `{key: (time/500ms)*500ms, value:(time, value)}`

### GROUPBYKEY()
`GROUPBYKEY()` makes records grouped in every 500ms. `{key: time1In500ms, value:[(time1, value1), (time2, value2)...]}`

### FFT()
`FFT()` applies Fast Fourier Transform for each record. The optional functions `minHz(0)` and `maxHz(100)` limits the scope of the output just for the better visualization. `{key:time1In500ms, value:[(Hz1, Ampl1), ...]}`, `{key:'time2In500ms', value:[(Hz1, Ampl1), ...]}`, ...

### FLATTEN()
`FLATTEN()` reduces the dimension of the value array by splitting into multiple records. As result it yields.

### PUSHKEY()
`PUSHKEY('fft')` sets the constant string 'fft' as new key for all records. and the previous key will be "pushed" into the first place of value array. `{key:'fft', value:(time1In500ms, Hz1, Ampl1)}`, `{key:'fft', value:(time1In500ms, Hz2, Ampl2)}`...

{{% /steps %}}


