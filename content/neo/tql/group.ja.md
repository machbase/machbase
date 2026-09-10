---
title: GROUP()
type: docs
weight: 60
math: true
toc: true
---

{{< neo_since ver="8.0.7" />}}

## 構文 {#구문}

```
GROUP( [lazy(boolean)] [, by()] [, aggregator ...] )
```

- `lazy(boolean)`：遅延モードを設定します（既定値は `false`）。
- `by(value [, timewindow()] [, name])`：グループの分割基準を指定します。  
  {{< neo_since ver="8.0.14" />}}以降は、`by()` を指定せずにデータ全体に集計関数を適用することもできます。
- `aggregator`：1つ以上の集計関数をカンマで区切って指定します。

```js {linenos=table,hl_lines=["7-12"],linenostart=1}
FAKE(json({
    ["A", 1],
    ["A", 2],
    ["B", 3],
    ["B", 4]
}))
GROUP(
    by(value(0), "CATEGORY"),
    avg(value(1), "AVG"),
    sum(value(1), "SUM"),
    first(value(1) * 10, "x10")
)
CSV(header(true))
```

**結果**
{{< figure src="/neo/tql/img/group-type1-ex1.jpg" width="600" >}}

### `by()`

*構文*: `by(value [, timewindow] [, label])`

- `value`：グループ化の基準値。通常は時刻または文字列です。
- `timewindow(from, until, period)`：時間範囲を指定します。
- `label`：新しいカラム名（既定値は `"GROUP"`）。

### `lazy()`

*構文*: `lazy(boolean)`

既定値の `false` の場合、`GROUP()` は現在のレコードと前のレコードの `by()` 値が変わるたびに結果を出力します。  
つまり、連続するレコードの値が同じ場合にのみ、1つのグループになります。  
`lazy(true)` を設定すると、入力ストリームの終端までデータを蓄積してからグループを計算します。未ソートのデータもグループ化できますが、多くのメモリを使用します。

### `timewindow()`

*構文*: `timewindow(from, until, period)` {{< neo_since ver="8.0.13" />}}

- `from`、`until`：開始を含み、終了を含まない時間範囲です。実データの有無にかかわらず、必要な区間を指定できます。
- `period`：`from` と `until` の間の時間間隔を表します。

> [timewindowの例](#timewindow-1)を参照してください。

一定の時間間隔でデータを可視化する際、クエリ結果に空の区間や過密な区間があると、必要な形にデータを整えるのが難しくなります。  
`timewindow()` を使うと、この処理をTQL内で行えます。

### 集計関数（aggregator） {#집계기aggregator}

集計関数を指定しない場合、`GROUP()` は既定で元のレコードをそのまま配列にまとめて返します。  
連続するレコードの `by()` 値が同じ場合、`[[v1,v2], [v3,v4], ...]` 形式の配列を生成します。

集計関数には2種類あります。
- **Type 1**：結果の候補だけを保持し、最終値のみを返します。
- **Type 2**：グループ全体のデータを保持し、計算後にメモリを解放します。`lazy(true)` と併用すると、関連カラムの全データをメモリに保持します。

#### 共通オプション {#공통-옵션}

`where()`、`nullValue()`、`predict()`、`label` は、すべての集計関数で使用できる省略可能なオプションです。

- `where(predicate)`：条件式を満たす値だけを集計します。{{< neo_since ver="8.0.13" />}}
- `nullValue(alternative)`：集計結果がない場合の代替値を指定します。{{< neo_since ver="8.0.13" />}}
- `predict(algorithm)`：値がない場合、補間アルゴリズムによって値を補います。{{< neo_since ver="8.0.13" />}}
- `label`：結果のカラム名（既定値は関数名）

| algorithm            | 説明 |
|:---------------------|:-----|
| `PiecewiseConstant`  | 左連続の区分定数による1次元補間 |
| `PiecewiseLinear`    | 1次元の線形補間 |
| `AkimaSpline`        | 値と1階微分が連続する1次元の3次補間。<br/> https://www.iue.tuwien.ac.at/phd/rottinger/node60.html を参照 |
| `FritschButland`     | 値と1階微分が連続し、単調性を保証する区分3次の1次元補間。<br/> Fritsch, F. N. and Butland, J., "A method for constructing local monotone piecewise cubic interpolants" (1984), SIAM J. Sci. Statist. Comput., 5(2), pp. 300-304を参照 |
| `LinearRegression`   | 隣接値を使った線形回帰による補間 |

## 集計関数 {#집계-함수}

*構文*: `function_name( value [, value...] [, where()] [, nullValue()] [, predict()] [, label])`

関数に応じて1つ以上の値を渡します。以下のType 1関数の `x` は *float* 値です。

- <a id="avg"></a>`avg(x [, option...])`：平均（Type 1）
- <a id="sum"></a>`sum(x [, option...])`：合計（Type 1）
- <a id="count"></a>`count(x [, option...])`：件数（Type 1）{{< neo_since ver="8.0.13" />}}
- <a id="first"></a>`first(x [, option...])`：最初の値（Type 1）
- <a id="last"></a>`last(x [, option...])`：最後の値（Type 1）
- <a id="min"></a>`min(x [, option...])`：最小値（Type 1）
- <a id="max"></a>`max(x [, option...])`：最大値（Type 1）
- <a id="rss"></a>`rss(x [, option...])`：二乗和平方根（Type 1）
- <a id="rms"></a>`rms(x [, option...])`：二乗平均平方根（Type 1）
- `list(x [, option...])`：すべての値をリストにまとめる（Type 2）{{< neo_since ver="8.0.15" />}}

### list() {#list}

Type 2、*構文*: `list(x [, option...])` {{< neo_since ver="8.0.15" />}}

- `x`：*float* 値

`list()` は、すべての *x* 値を集計し、各値を含む1つのリストを生成します。`JSON(rowsArray(true))` や `FLATTEN()` と組み合わせると、結果をさまざまな形式に加工できます。

{{< tabs >}}
{{< tab name="JSON" >}}
```js {linenos=table,hl_lines=[4]}
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0)),
    list(value(1))
)
JSON()
```

```json
{
    "data": {
        "columns": ["GROUP", "LIST"],
        "types": ["string", "list"],
        "rows": [
            ["A", [1,2]],
            ["B", [3,4]],
            ["C", [5]]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "220.375µs"
}
```
{{</ tab >}}
{{< tab name="JSON(rowsArray)" >}}
```js {linenos=table,hl_lines=[4,7]}
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0),"name"),
    avg(value(1), "avg"),
    list(value(1), "values")
)
JSON(rowsArray(true))
```

```json
{
    "data": {
        "columns": ["name", "values", "avg"],
        "types": [ "string", "list", "float64" ],
        "rows": [
            {  "name": "A", "avg": 1.5, "values": [ 1, 2 ] },
            {  "name": "B", "avg": 3.5, "values": [ 3, 4 ] },
            {  "name": "C", "avg": 5,  "values": [ 5 ] }
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "270.25µs"
}
```
{{</ tab >}}
{{< tab name="FLATTEN" >}}
```js {linenos=table,hl_lines=[4,7]}
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0)),
    list(value(1))
)
POPVALUE(0)
FLATTEN()
JSON()
```

```json
{
    "data": {
        "columns": ["LIST"],
        "types": ["list"],
        "rows": [
            [1,2],
            [3,4],
            [5]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "252.625µs"
}
```
{{</ tab >}}
{{</ tabs >}}

### lrs() {#lrs}

Type 2、*構文*: `lrs(x, y [, weight(w)] [, option...])` {{< neo_since ver="8.0.13" />}}

- `x`：*float* または *time*
- `y`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

*x*-*y* を直交座標系の点とみなし、線形回帰の傾きを求めます。*x* は数値型または時刻型です。

### mean() {#mean}

Type 2、*構文*: `mean(x [, weight(w)] [, option...])`

- `x`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

`mean()` は、グループ化した値の加重平均を計算します。すべての重みが1の場合は、性能上、軽量な `avg()` を使用してください。

mean($x$, weight($w$)) = $ \frac{\sum {w_i  x_i}} {\sum {w_i}} $

### cdf() {#cdf}

Type 2、*構文*: `cdf(x, q [, weight(w)] [, option...])` {{< neo_since ver="8.0.14" />}}

- `x`：*float*
- `q`：*float*
- `weight(w)`：省略した場合、すべての重みは1です。

`cdf()` は、*x* の経験累積分布関数の値、すなわちq以下のサンプルの割合を返します。
`cdf()` は理論上 `quantile()` の逆関数ですが、すべての *q* で実際に逆関数になるとは限りません。

### correlation() {#correlation}

Type 2、*構文*: `correlation(x, y [, weight(w)] [, option...])` {{< neo_since ver="8.0.14" />}}

- `x`、`y`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

`correlation()` は、*x* と *y* のサンプル間の加重相関を返します。

correlation($x$, $y$, weight($w$)) = $ \frac{\sum {w_i (x_i - \bar{x}) (y_i - \bar{y})}} {stdX * stdY} $,
（$\bar{x}$ = xの平均、$\bar{y}$ = yの平均）

### covariance() {#covariance}

Type 2、*構文*: `covariance(x, y [, weight(w)] [, option...])` {{< neo_since ver="8.0.14" />}}

- `x`、`y`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

`covariance()` は、*x* と *y* のサンプル間の加重共分散を返します。

covariance($x$, $y$, weight($w$)) = $ \frac{\sum {w_i (x_i - \bar{x}) (y_i - \bar{y})}} { \sum {w_i} -1 } $,
（$\bar{x}$ = xの平均、$\bar{y}$ = yの平均）


### quantile() {#quantile}

Type 2、*構文*: `quantile(x, p [, weight(w)] [, option...])` {{< neo_since ver="8.0.13" />}}

- `x`：*float* 値
- `p`：*float*、割合
- `weight(w)`：省略した場合、すべての重みは1です。

`quantile()` は、サンプルの割合p以上を下側に含むxのサンプル値を返します。pは0から1の範囲で指定します。

サンプルの割合p以上を下側に含む、最小の値qを返します。

### quantileInterpolated() {#quantileinterpolated}

Type 2、*構文*: `quantileInterpolated(x, p [, weight(w)] [, option...])` {{< neo_since ver="8.0.13" />}}

- `x`：*float* 値
- `p`：*float*、割合
- `weight(w)`：省略した場合、すべての重みは1です。

`quantile()` は、サンプルの割合p以上を下側に含むxのサンプル値を返します。pは0から1の範囲で指定します。

`quantileInterpolated()` の戻り値は、線形補間した値です。

### median() {#median}

Type 2、*構文*: `median(x [, weight(w)] [, option...])`

- `x`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

`quantile(x, 0.5 [, option...])` と同じです。

### medianInterpolated() {#medianinterpolated}

Type 2、*構文*: `medianInterpolated(x [, weight(w)] [, option...])`

- `x`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

`quantileInterpolated(x, 0.5 [, option...])` と同じです。

### stddev() {#stddev}

Type 2、*構文*: `stddev(x [, weight(w)] [, option...])`

- `weight(w)`：省略した場合、すべての重みは1です。

`stddev()` は、標本標準偏差を返します。

### stderr() {#stderr}

Type 2、*構文*: `stderr(x [, weight(w)] [, option...])`

- `weight(w)`：省略した場合、すべての重みは1です。

`stderr()` は、指定した値の標準偏差を用いて平均の標準誤差を返します。

### entropy() {#entropy}

Type 2、*構文*: `entropy(x [, option...])`

分布のシャノンエントロピーです。自然対数を使用します。

### mode() {#mode}

Type 2、*構文*: `mode(x [, weight(w)] [, option...])`

- `weight(w)`：省略した場合、すべての重みは1です。

`mode()` は、指定した値と重みに基づき、データセットで最も頻出する値を返します。
値の比較にはfloat64の厳密な等価比較を使用するため、注意してください。
最頻値が複数ある場合、いずれか1つを返します。

### moment() {#moment}

Type 2、*構文*: `moment(x, n [, weight(w)] [, option...])` {{< neo_since ver="8.0.14" />}}

- `x`：float64、値
- `n`：float64、モーメントの次数
- `weight(w)`：省略した場合、すべての重みは1です。

`moment()` は、サンプルの加重 *n* 次モーメントを計算します。

### variance() {#variance}

Type 2、*構文*: `variance(x [, weight(w)] [, option...])` {{< neo_since ver="8.0.14" />}}

- `x`：*float* 値
- `weight(w)`：省略した場合、すべての重みは1です。

`variance()` は、グループ化した値の不偏加重分散を計算します。
重みの合計が1以下の場合は、偏りのある分散推定量を使用する必要があります。

```js {linenos=table,hl_lines=["3-4"],linenostart=1}
FAKE(json({[8,2], [2,2], [-9,6], [15,7], [4,1]}))
GROUP(
    variance(value(0), "VARIANCE"),
    variance(value(0), weight(value(1)), "WEIGHTED VARIANCE")
)
CSV(heading(true), precision(4))
```
{{< figure src="/neo/tql/img/group-variance.jpg" width="600" >}}

## 例 {#examples}

### timewindow() {#timewindow-1}

`FAKE()` は1msごとに時刻と値を生成するため、1秒間に1,000レコードが生成されます。
以下のTQLは、1秒間隔（`timewindow()` の `period("1s")`）のデータを生成します。
必要な時間帯に実データ（レコード）がなければ、既定値のNULLで埋めます。

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

{{< figure src="/neo/tql/img/group-tw-ex1.jpg" >}}

### nullValue() {#nullvalue-1}

`nullValue(100)` を追加して再実行します。NULL値が指定した100に置き換わります。

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

{{< figure src="/neo/tql/img/group-tw-ex2.jpg" >}}

### predict() {#predict-1}

`nullValue()` で空の値（NULL）を定数で埋めるだけでなく、隣接値を参照して補間できます。
上記の例の `last()` に `predict("LinearRegression")` を追加して再実行してください。値がなくNULLを返していたレコードに、線形回帰で予測した値が入ります。

予測に必要な隣接値が不足していると、`predict()` は補間値を生成できない場合があります。その場合は `nullValue()` を適用し、指定されていなければ `NULL` を返します。

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

{{< figure src="/neo/tql/img/group-tw-ex3.jpg" >}}

### where() {#where-1}

温度と湿度を測定する2つのセンサーが、それぞれ1秒ごとにデータを保存するとします。
実際のセンサーシステム間には時刻差があるため、保存データは次の例のようになることがあります。

{{< figure src="/neo/tql/img/group-where-ex1.jpg" >}}

レコード#5の湿度データは想定より早く保存され、レコード#9でも同じことが起きています。
データを秒単位に正規化します。

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
MAPVALUE(1, parseTime(value(1), "ms"))

GROUP(
    by( roundTime(value(1), "1s")),
    avg( value(2) )
)

CSV( timeformat("Default"), header(true) )
```

{{< figure src="/neo/tql/img/group-where-ex2.jpg" width="600">}}

`roundTime(..., "1s")` で時刻を秒単位に揃え、同じ時刻のレコードをグループ化します。
`avg(...)` は、グループの平均値を返します。

ただし、温度か湿度かを示す先頭カラムの情報が失われるため、結果の値に意味がなくなります。
これを解決するには `where()` を使用します。集計関数は、`where()` の条件が `true` の場合にのみ値を受け取ります。

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

{{< figure src="/neo/tql/img/group-where-ex3.jpg" width="600" >}}

`predict()` と `nullValue()` で、最後のレコードの欠損データを補間することもできます。

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

{{< figure src="/neo/tql/img/group-where-ex4.jpg" width="600" >}}

### チャート {#chart}

```js {linenos=table,hl_lines=["4-8"],linenostart=1}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
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

**結果**
{{< figure src="/neo/tql/img/groupbykey_stddev.jpg" width="476" >}}
