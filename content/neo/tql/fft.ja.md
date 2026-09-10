---
title: FFT()
type: docs
weight: 70
toc: true
---

## 高速フーリエ変換 {#고속-푸리에-변환}

{{< callout emoji="📌" >}}
実習を進める前に、以下のクエリを実行してテーブルとデータを準備してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## サンプルデータの生成 {#샘플-데이터-생성}

Web UIで新しい *tql* エディターを開き、以下のコードをコピーして実行してください。

この例では、`oscillator()` が15Hz・振幅1.0と24Hz・振幅1.5を合成した波形を生成します。
また、`CHART_SCATTER()` には、X軸の下にスライダーを表示する `dataZoom()` オプション関数を指定しています。

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

## 生成したデータをデータベースに保存する {#생성한-데이터를-데이터베이스에-저장하기}

生成したデータを 'signal' というタグ名でデータベースに保存してください。

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

実行結果ウィンドウに「10000 rows inserted.」と表示されます。

テストマシン（Apple Mac mini M1）では約270msかかりました。以下の例のように `APPEND()` を使用すると、約65ms（約4倍高速）に短縮できます。

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
`APPEND` は、入力レコードのフィールドがテーブルのカラムと順序・型まで正確に一致する場合にのみ動作します。
{{< /callout >}}

## データベースからデータを読み取る {#데이터베이스에서-데이터-읽기}

以下のコードは、'example' テーブルに保存したデータを読み取ります。

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

## 高速フーリエ変換を実行する {#고속-푸리에-변환-수행}

`SQL_SELECT()` ソースと `CHART_LINE()` シンクの間に、データ変換関数を追加します。

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

## 動作の仕組み {#동작-방식}

{{% steps %}}

### SQL_SELECT()
`SQL_SELECT(...)` 関数は、クエリ結果を `{key: rownum, value: (time, value)}` 形式のレコードとして渡します。

### MAPKEY('sample')
`MAPKEY('sample')` 関数は、すべてのレコードに固定キー 'sample' を設定します。各レコードの *key* は `'sample'` となり、*value* の `(time, value)` は維持されます。`{key: 'sample', value:(time, value)}`

### GROUPBYKEY()
`GROUPBYKEY()` は、同じキーを持つレコードを結合します。この例では、すべてのクエリ結果が1つのレコードにまとまり、`{key: 'sample', value:[ (time1, value1), (time2, value2), ..., (timeN, valueN) ]}` となります。

### FFT()
`FFT()` は、レコードの値に高速フーリエ変換を適用し、`(time, value)` 配列を `(frequency, amplitude)` 配列に変換します。`{key: 'sample', value:[ (Hz1, Ampl1), (Hz2, Ampl2), ... ]}`

{{% /steps %}}

## 時間軸を追加する {#시간-축-추가}

次の例は、時間軸を追加して周波数変換の結果を時系列として可視化します。

```js {linenos=table,hl_lines=["3-7"],linenostart=1}
SQL(`select time, value from example where name = 'signal' order by time`)

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

`SQL_SELECT()` で直近10秒の範囲を指定する場合は、次のように記述できます。

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

## 時間軸を追加した場合の動作 {#시간-축-추가-동작-방식}

{{% steps %}}

### SQL_SELECT()

`SQL_SELECT(...)` 関数は、クエリ結果を `{key: rownum, value: (time, value)}` 形式で渡します。

### MAPKEY()
`MAPKEY( roundTime(value(0), '500ms'))` は、`value(0)` を500ミリ秒のバケット境界に切りそろえた結果を新しいキーに設定します。レコードは `{key: (time/500ms)*500ms, value:(time, value)}` 形式に変換されます。

### GROUPBYKEY()
`GROUPBYKEY()` は、レコードを500ミリ秒単位でグループ化します。`{key: time1In500ms, value:[(time1, value1), (time2, value2)...]}`

### FFT()
`FFT()` は、各レコードに高速フーリエ変換を適用します。省略可能な `minHz(0)` と `maxHz(100)` は、可視化用に出力範囲を制限します。`{key:time1In500ms, value:[(Hz1, Ampl1), ...]}`、`{key:'time2In500ms', value:[(Hz1, Ampl1), ...]}`、...

### FLATTEN()
`FLATTEN()` は、値配列の次元を減らし、複数のレコードに分割します。各周波数と振幅のペアが個別のレコードとして出力されます。

### PUSHKEY()
`PUSHKEY('fft')` は、すべてのレコードに固定キー 'fft' を設定し、以前のキーを値配列の先頭に移動します。`{key:'fft', value:(time1In500ms, Hz1, Ampl1)}`、`{key:'fft', value:(time1In500ms, Hz2, Ampl2)}`...

{{% /steps %}}
