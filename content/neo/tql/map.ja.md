---
title: MAP
type: docs
weight: 31
math: true
toc: true
---

*MAP* 関数は、データを必要な形式に加工するための基本的な関数です。

## TAKE()

![map_take](/neo/tql/img/map_take.jpg)

*構文*: `TAKE( [offset,] n )`

ストリームの先頭から *n* 件のレコードを取得し、処理を終了します。

- `offset` *number*: 省略可能。指定した位置からレコードを取得します。デフォルトは 0 です。{{< neo_since ver="8.0.6" />}}
- `n` *number*: 取得するレコード数。

{{< tabs >}}
{{< tab name="TAKE(n)" >}}
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
{{< tab name="TAKE(offset n)" >}}
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

![map_drop](/neo/tql/img/map_drop.jpg)

*構文*: `DROP( [offset,] n  )`

先頭の *n* 件のレコードをスキップして除去します。

- `offset` *number*: 省略可能。指定した位置からレコードを除去します。デフォルトは 0 です。{{< neo_since ver="8.0.6" />}}
- `n` *number*: 除去するレコード数。

{{< tabs >}}
{{< tab name="DROP(n)" >}}
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
{{< tab name="DROP(offset n)" >}}
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

![map_filter](/neo/tql/img/map_filter.jpg)

*構文*: `FILTER( condition )`

入力レコードに条件式を適用し、*condition* が真の場合だけ次のステップに渡します。

たとえば、入力レコードが `{key: k1, value[v1, v2]}` の場合、`FILTER(count(V) > 2)` はこのレコードを除去します。`FILTER(count(V) >= 2)` なら、次の関数に渡します。

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

## FILTER_CHANGED()

*構文*: `FILTER_CHANGED( value [, retain(time, duration)] [, useFirstWithLast()] )` {{< neo_since ver="8.0.15" />}}

- `retain(time, duration)`
- `useFirstWithLast(boolean)`

前のレコードと比較して `value` が変化した場合だけレコードを通過させます。  
最初のレコードは常に渡されます。必要に応じて `FILTER_CHANGED()` の後に `DROP(1)` を追加して除去してください。

`retain()` オプションを指定すると、`time` を基準に、指定期間にわたって変更後の `value` を維持したレコードが渡されます。

{{< tabs >}}
{{< tab name="例" >}}
```js {linenos=table,hl_lines=[2,4,10,11,14]}
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
B,1692329340,3
C,1692329346,9
D,1692329347,9.1
```

{{< /tab >}}
{{< tab name="retain()" >}}
```js {linenos=table,hl_lines=[4,6,14]}
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0), retain(value(1), "2s"))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
B,1692329342,5
```
{{< /tab >}}
{{< tab name="useFirstWithLast()" >}}
```js {linenos=table,hl_lines=[4,6,14]}
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0), retain(value(1), "2s"), useFirstWithLast(false))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
B,1692329340,3
```
{{< /tab >}}
{{< tab name="useFirstWithLast()" >}}
```js {linenos=table,hl_lines=[14]}
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0), useFirstWithLast(true))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
A,1692329339,2
B,1692329340,3
B,1692329345,8
C,1692329346,9
C,1692329346,9
D,1692329347,9.1
D,1692329347,9.1
```
{{< /tab >}}
{{< /tabs >}}

## SET()

*構文*: `SET(name, expression)` {{< neo_since ver="8.0.12" />}}

- `name` *keyword*: 変数名。
- `expression` *expression*: 変数に代入する値。

*SET* は、レコードのスコープで使用する変数を定義します。たとえば `SET(var, 10)` で宣言した変数は、以降 `$var` で参照できます。変数は値配列に含まれないため、最終的な SINK の結果には出力されません。

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

## GROUP()

*構文*: `GROUP( [lazy(boolean),] by [, aggregators...] )` {{< neo_since ver="8.0.7" />}}

- `lazy(boolean)`: デフォルトの `false` では、`by()` の値が前のレコードと異なると直ちに集計結果を出力します。`true` では入力ストリームが終了するまでデータを蓄積し、結果をまとめて返します。

- `by(value [, label])`: グループ化の基準となる値。

- `aggregators` *array of aggregator*: 使用する集計関数のリスト。

集計関数の詳細は [GROUP()](/neo/tql/group/) を参照してください。

## PUSHVALUE()

![map_pushvalue](/neo/tql/img/map_pushvalue.jpg)

*構文*: `PUSHVALUE( idx, value [, name] )` {{< neo_since ver="8.0.5" />}}

- `idx` *number*: 新しい値の挿入位置（0 始まり）。
- `value` *expression*: 挿入する値。
- `name` *string*: 列名。デフォルトは `'column'` です。

現在の値配列に新しい列を挿入します。

```js {linenos=table,hl_lines=[2],linenostart=1}
FAKE( linspace(0, 1, 3))
PUSHVALUE(1, value(0) * 10)
CSV()
```

```csv
0.0,0
0.5,5
1.0,10
```

## POPVALUE()

![map_popvalue](/neo/tql/img/map_popvalue.jpg)

*構文*: `POPVALUE( idx [, idx2, idx3, ...] )` {{< neo_since ver="8.0.5" />}}

- `idx` *number*: 除去する列のインデックスのリスト。

指定したインデックスの列を値配列から除去します。

```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( linspace(0, 1, 3))
PUSHVALUE(1, value(0) * 10)
POPVALUE(0)
CSV()
```

```csv
0
5
10
```

## MAPVALUE()

![map_mapvalue](/neo/tql/img/map_mapvalue.jpg)

*構文*: `MAPVALUE( idx, newValue [, newName] )`

- `idx` *number*: 値タプル内のインデックス（0 始まり）。
- `newValue` *expression*: 置換後の値。
- `newName` *string*: 新しい列名。

`MAPVALUE()` は、指定したインデックスの値を別の値に置き換えます。たとえば `MAPVALUE(0, value(0)*10)` は、最初の値を 10 倍した値に置き換えます。

`idx` が範囲外の場合は `PUSHVALUE()` と同様に新しい列を追加します。たとえば `MAPVALUE(-1, value(1)+'_suffix')` は、2 番目の値に `_suffix` を連結した文字列の列を追加します。

```js {linenos=table,hl_lines=[2],linenostart=1}
FAKE( linspace(0, 1, 3))
MAPVALUE(0, value(0) * 10)
CSV()
```

```csv
0
5
10
```

次の例では `MAPVALUE` で数値演算を適用します。

```js {linenos=table,hl_lines=["7-8"],linenostart=1}
FAKE(
    meshgrid(
        linspace(-4,4,100),
        linspace(-4,4, 100)
    )
)
MAPVALUE(2, sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2)))
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D:{},
        xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
        series:[
            {type: "line3D", data: column(0)},
        ]
    })
)
```

{{< figure src="/neo/tql/img/tql-math-example2.jpg" width="400px" >}}

## MAP_DIFF()

*構文*: `MAP_DIFF( idx, value [, newName] )` {{< neo_since ver="8.0.8" />}}

- `idx` *number*: 値タプル内のインデックス（0 始まり）。
- `value` *number*: 計算の基準となる値。
- `newName` *string*: 新しい列名。

`MAP_DIFF()` は、指定した位置の値を現在値と前回値の差（*current - previous*）に置き換えます。

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

*構文*: `MAP_ABSDIFF( idx, value [, label]  )` {{< neo_since ver="8.0.8" />}}

- `idx` *number*  値タプル内のインデックス（0 始まり）。
- `value` *number*
- `label` *string* 指定した文字列を新しい列名にします。

`MAP_ABSDIFF()` は、値を現在値と前回値の差の絶対値 `abs(current - previous)` に置き換えます。

## MAP_NONEGDIFF()

*構文*: `MAP_NONEGDIFF( idx, value [, label]  )` {{< neo_since ver="8.0.8" />}}

- `idx` *number*  値タプル内のインデックス（0 始まり）。
- `value` *number*
- `label` *string* 指定した文字列を新しい列名にします。

`MAP_NONEGDIFF()` は、値を現在値と前回値の差（*current - previous*）に置き換えます。差が 0 未満の場合は 0 を返します。

## MAP_AVG()

*構文*: `MAP_AVG(idx, value [, label] )`  {{< neo_since ver="8.0.15" />}}

- `idx` *number*  値タプル内のインデックス（0 始まり）。
- `value` *number*
- `label` *string* 指定した文字列を新しい列名にします。

`MAP_AVG` は、指定した位置の値を平均フィルターの計算結果に置き換えます。

データ数を $k$ とすると、

$\alpha = \frac{1}{k}$ とします。

$\overline{x_k} = (1 - \alpha) \overline{x_{k-1}} + \alpha x_k$

```js {linenos=table,hl_lines=[3]}
FAKE(arrange(0, 1000, 1))
MAPVALUE(1, sin(2 * PI *10*value(0)/1000))
MAP_AVG(2, value(1))
CHART(
    chartOption({
        xAxis:{ type:"category", data:column(0)},
        yAxis:{},
        series:[
            { type:"line", data:column(1), name:"RAW" },
            { type:"line", data:column(2), name:"AVG" }
        ],
        legend:{ bottom:10}
    })
)
```

{{< figure src="/neo/tql/img/tql-map_avg.jpg" width="500" >}}

## MAP_MOVAVG()

*構文*: `MAP_MOVAVG(idx, value, window [, label] )`  {{< neo_since ver="8.0.8" />}}

- `idx` *number*  値タプル内のインデックス（0 始まり）。
- `value` *number*
- `window` *number* 蓄積するレコード数。
- `label` *string* 指定した文字列を新しい列名にします。

`MAP_MOVAVG` は、指定した位置の値をウィンドウサイズに応じた移動平均に置き換えます。  
値の数がウィンドウサイズに達していない場合は、利用可能な値の合計をその個数で割ります。  
直近の `window` 区間の入力がすべて `NULL`（または数値以外）の場合、結果も `NULL` になります。  
一部の値だけが `NULL` の場合は、`NULL` を除外して平均を計算します。

```js {linenos=table,hl_lines=[6,13]}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_MOVAVG(2, value(1), 10)
CHART(
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"MA(10)" },
        ],
        legend: { bottom: 10 }
    })
)
```

- 5 行目: ノイズを含む信号値を生成します。
- 6 行目: ウィンドウサイズ 10 の移動平均を計算します。

{{< figure src="/neo/tql/img/tql-map_movavg_filter.jpg" width="500" >}}

## MAP_LOWPASS()

*構文*: `MAP_LOWPASS(idx, value, alpha [, label] )`  {{< neo_since ver="8.0.15" />}}

- `idx` *number*: 値タプル内のインデックス（0 始まり）。
- `value` *number*
- `alpha` *number*: 0 < alpha < 1 の範囲の係数。
- `label` *string*: 新しい列名。

`MAP_LOWPASS` は、指定した位置の値を指数加重移動平均（EWMA）に置き換えます。

$ 0 < \alpha < 1$ のとき、

$\overline{x_k} = (1 - \alpha) \overline{x_{k-1}} + \alpha x_k$

```js {linenos=table,hl_lines=[6,13]}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_LOWPASS(2, $sig + $noise, 0.40)
CHART(
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"lpf" },
        ],
        legend: { bottom: 10 }
    })
)
```

- 5 行目: ノイズを含む信号を生成します。
- 6 行目: `alpha = 0.40` のローパスフィルターを適用します。

{{< figure src="/neo/tql/img/tql-map_lowpass_filter.jpg" width="500" >}}


## MAP_KALMAN()

*構文*: `MAP_KALMAN(idx, value, model() [, label])` {{< neo_since ver="8.0.15" />}}
- `idx` *number*: 値タプル内のインデックス（0 始まり）。
- `value` *number*
- `model` *model(initial, progress, observation)*: システム行列を指定します。
- `label` *string*: 新しい列名。


```js {linenos=table,hl_lines=[10]}
FAKE(arrange(0, 10, 0.1))
MAPVALUE(0, round(value(0)*100)/100 )

SET(real, 14.4)
SET(noise, 4 * simplex(1234, value(0)))
SET(measure, $real + $noise)

MAPVALUE(1, $real )
MAPVALUE(2, $measure)
MAP_KALMAN(3, $measure, model(0.1, 0.001, 1.0))
CHART(
    chartOption({
        title:{text:"Kalman filter"},
        xAxis:{type:"category", data:column(0)},
        yAxis:{ min:10, max: 18 },
        series:[
            {type:"line", data:column(1), name:"real"},
            {type:"line", data:column(2), name:"measured"},
            {type:"line", data:column(3), name:"filtered"}
        ],
        tooltip: {show: true, trigger:"axis"},
        legend: { bottom: 10},
        animation: false
    })
)
```

- 4 行目: 真値は定数 `14.4` です。
- 5 行目: 単純なノイズを生成します。
- 6 行目: 真値とノイズを加算して測定値を生成します。
- 10 行目: 測定値にカルマンフィルターを適用します。

{{< figure src="/neo/tql/img/tql-map_kalman_filter.jpg" width="500" >}}

## HISTOGRAM()

`HISTOGRAM()` には 2 つの動作方式があります。入力値の範囲が固定または予測可能な場合は固定ビンを、値の範囲が不明な場合は動的ビンを使用します。

### 固定ビン {#fixed-bins}

*構文*: `HISTOGRAM(value, bins [, category] [, order] )`  {{< neo_since ver="8.0.15" />}}

- `value` *number*
- `bins` *bins(min, max, step)*: ヒストグラムのビン設定。
- `category` *category(name_value)*: 分類列。
- `order` *order(name...string)*: カテゴリーの順序。

`HISTOGRAM()` は、指定したビンごとに値の分布を集計します。ビンは最小値、最大値、ビン幅（`step`）で設定します。値が範囲外の場合は、下限側または上限側のビンが自動的に追加されます。

{{< tabs >}}
{{< tab name="CSV" >}}
```js {{linenos=table,hl_lines=[3]}}
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
HISTOGRAM(value(0), bins(0, 200, 40))
CSV( precision(0), header(true) )
```

```csv
low,high,count
0,40,2
40,80,31
80,120,47
120,160,16
160,200,4
```
{{< /tab >}}
{{< tab name="CHART" >}}
```js {{linenos=table,hl_lines=[3]}}
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
HISTOGRAM(value(0), bins(0, 200, 40))
MAPVALUE(0, strSprintf("%.f~%.f", value(0), value(1)))
CHART(
    chartOption({
        xAxis:{ type:"category", data:column(0)},
        yAxis:{},
        tooltip:{trigger:"axis"},
        series:[
            {type:"bar", data: column(2)}
        ]
    })
)
```
{{< figure src="/neo/tql/img/tql-histogram.jpg" width="500" >}}
{{< /tab >}}
{{< tab name="CATEGORY" >}}
```js {{linenos=table,hl_lines=[4,"13-14"]}}
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
PUSHVALUE(0, key() % 2 == 0 ? "Cat.A" : "Cat.B")
HISTOGRAM(value(1), bins(0, 200, 40), category(value(0)))
MAPVALUE(0, strSprintf("%.f~%.f", value(0), value(1)))
CHART(
    chartOption({
        xAxis:{ type:"category", data:column(0)},
        yAxis:{},
        tooltip:{trigger:"axis"},
        legend:{bottom:5},
        series:[
            {type:"bar", data: column(2), name:"Cat.A"},
            {type:"bar", data: column(3), name:"Cat.B"},
        ]
    })
)
```
{{< figure src="/neo/tql/img/tql-histogram-cat.jpg" width="500" >}}
{{< /tab >}}
{{< /tabs >}}

### 動的ビン {#동적-구간}

*構文*: `HISTOGRAM(value [, bins(maxBins)] )`  {{< neo_since ver="8.0.46" />}}

- `value` *number*
- `bins` *number*: 作成するビンの最大数。デフォルトは 100 です。

`HISTOGRAM()` は、値とビンの最大数を受け取り、入力範囲に合わせてビンを動的に調整します。  
`value` 列は各ビンの平均値、`count` 列はそのビンに属する値の個数を表します。  
したがって、`value × count` はそのビンに属する値の合計と等しくなります。

```js {{linenos=table,hl_lines=[3]}}
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
HISTOGRAM(value(0), bins(5))
CSV( precision(0), header(true) )
```

```csv
value,count
47,12
75,29
99,29
119,18
156,12
```

## BOXPLOT()

*構文*: `BOXPLOT(value, category [, order] [, boxplotInterp] [, boxplotOutput])` {{< neo_since ver="8.0.15" />}}

- `value` *number*
- `category` *category(name_value)*: グループの識別子。
- `order` *order(name...string)*: カテゴリーの順序。
- `boxplotOutput` *boxplotOutput( "" | "chart" | "dict" )*: 出力形式。
- `boxplotInterp` *boxplotInterp(Q1 boolean, Q2 boolean, Q3 boolean)*: 四分位数の補間オプション。

  - 詳細な例は [Michelson & Morley Experiment](../chart/boxplot/michelson-morley) と [Iris Sepal Length](../chart/boxplot/iris-sepal-length) を参照してください。

## TRANSPOSE()

*構文*: `TRANSPOSE( [fixed(columnIdx...) | columnIdx...] [, header(boolean)] )` {{< neo_since ver="8.0.8" />}}

CSV やブリッジを使用して外部 RDBMS から読み込んだデータを Machbase TAG テーブルの構造に合わせるには、列を行に変換する必要がある場合があります。  
`TRANSPOSE` は、複数の列を持つレコードを複数の行に変換します。

- `fixed(columnIdx...)`: 変換せずに保持する列を指定します。変換対象の列指定とは併用できません。
- `columnIdx...`: 変換する列のリストを指定します。`fixed()` とは併用できません。
- `header(boolean)`: `header(true)` では最初のレコードをヘッダーとみなし、変換後のレコードにヘッダー値を新しい列として追加します。

{{< tabs >}}
{{< tab name="TRANSPOSE" >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true), 2, 3, 4 )
MAPVALUE(0, strToUpper(value(0)) + "-" + value(2))
MAPVALUE(1, parseTime(value(1), sqlTimeformat("YYYY/MM/DD")))
MAPVALUE(3, parseFloat(value(3)))
POPVALUE(2)
CSV(timeformat("s"))
```
代表的な使用例を示します。
- 5 行目: 2、3、4 番目の列をヘッダーとともに変換します。
- 6 行目: 都市名と変換した列名を連結します。
- 7 行目: 文字列を時刻に変換します。
- 8 行目: 値の文字列を数値に変換します。
- 9 行目: 不要になった変換元の列名を除去します。

```csv
TOKYO-TEMPERATURE,1701907200,23
TOKYO-HUMIDITY,1701907200,30
TOKYO-NOISE,1701907200,40
BEIJING-TEMPERATURE,1701907200,24
BEIJING-HUMIDITY,1701907200,50
BEIJING-NOISE,1701907200,60
```
{{< /tab >}}
{{< tab name="すべての列" >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE()
CSV()
```
オプションを指定しない場合、すべての列が行に変換されます。
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
{{< tab name="header()" >}}
```js {linenos=table,hl_lines=["5"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true) )
CSV()
```
最初のレコードをヘッダーとみなし、変換した各レコードに新しい列を追加します。
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
{{< tab name="fixed()" >}}
```js {linenos=table,hl_lines=["5", "7"],linenostart=1}
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true), fixed(0, 1) )
// 次と同じ動作
// TRANSPOSE( header(true), 2, 3, 4 )
CSV()
```
"fixed" で指定した列は変換後もそのまま保持されます。
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

## FFT()

![map_fft](/neo/tql/img/map_fft.jpg)

*構文*: `FFT([minHz(value), maxHz(value)])`
- `minHz(value)`: 解析に使用する最小周波数。
- `maxHz(value)`: 解析に使用する最大周波数。

入力レコードの値を `(time, amplitude)` タプルの配列とみなし、高速フーリエ変換（FFT）を適用します。  
変換後はキーを保持したまま、値を `(frequency, amplitude)` タプルの配列に置き換えます。

たとえば入力が `{key: k, value[[t1,a1],[t2,a2],..., [tn,an]]}` の場合、結果は `{key: k, value[[F1,A1],[F2,A2],..., [Fm,Am]]}` になります。

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

{{< figure src="/images/web-fft-tql-2d.png" width="510" >}}

3D 可視化の例を含む詳細は [FFT()](/neo/tql/fft) を参照してください。

## WHEN()

*構文*: `WHEN(condition, doer)` {{< neo_since ver="8.0.7" />}}

- `condition` *boolean*
- `doer` *doer*

`WHEN` は、条件が真の場合に指定した `doer` の処理を実行します。  
レコードの流れには影響せず、定義された副作用の処理だけを実行します。

### doLog()

*構文*: `doLog(args...)` {{< neo_since ver="8.0.7" />}}

Web コンソールにログメッセージを出力します。

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(1, 2, 2))
WHEN( mod(value(0), 2) == 0, doLog(value(0), "is even."))
CSV()
```

### doHttp()

*構文*: `doHttp(method, url, body [, header...])` {{< neo_since ver="8.0.7" />}}

- `method` *string*
- `url` *string*
- `body` *string*
- `header` *string*: 省略可能なヘッダー。

`doHttp` は、指定したメソッド、URL、本文、ヘッダーで HTTP リクエストを送信します。

**使用例**

- 指定した HTTP エンドポイントにイベントを通知します。

```js {linenos=table,hl_lines=["4"],linenostart=1}
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("GET", strSprintf("http://127.0.0.1:8888/notify?value=%.0f", value(0)), nil)
)
CSV()

```

- 現在のレコードを CSV（デフォルト形式）で送信します。

```js {linenos=table,hl_lines=["4"],linenostart=1}
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("POST", "http://127.0.0.1:8888/notify", value())
)
CSV()
```

- 現在のレコードをカスタム JSON 形式で送信します。

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

*構文*: `do(args..., { sub-flow-code })` {{< neo_since ver="8.0.7" />}}

`do` は、受け取った引数 `args...` を使用してサブフローのコードを実行します。

`WHEN()` は、条件に応じて副作用を実行するための機能です。  
そのため、`WHEN` 内のサブフローでは、`CSV`、`JSON`、`CHART_*` など、出力ストリームに結果を書き込む SINK は使用できません。呼び出しても出力は無視され、警告メッセージが表示されます。

サブフローでは、出力ストリームに依存しない `INSERT` と `APPEND` が有効な SINK です。これらを使用すると、メインの TQL フローとは別のテーブルに値を書き込めます。処理が不要な場合は `DISCARD()` を使用して、警告なしでレコードを破棄できます。

```js {linenos=table,hl_lines=["9-13"],linenostart=1}
FAKE( json({
    [ 1, "hello" ],
    [ 2, "你好" ],
    [ 3, "world" ],
    [ 4, "世界" ]
}))
WHEN(
    value(0) % 2 == 0,
    do( "Greetings:", value(0), value(1), {
        ARGS()
        WHEN( true, doLog( value(0), value(2), "idx:", value(1) ) )
        DISCARD()
    })
)
CSV()
```

上記のログから、次の 2 点を確認できます。

1. メインフローは、サブフローの処理が完了するまで待機します。
2. 条件に一致するレコードごとにサブフローが実行されます。

```sh {hl_lines=[3,6],linenostart=1}
2023-12-02 07:54:42.160 TRACE 0xc000bfa580 Task compiled FAKE() → WHEN() → CSV()
2023-12-02 07:54:42.160 TRACE 0xc000bfa840 Task compiled ARGS() → WHEN() → DISCARD()
2023-12-02 07:54:42.160 INFO  0xc000bfa840 Greetings: 你好 idx: 2
2023-12-02 07:54:42.160 DEBUG 0xc000bfa840 Task elapsed 254.583µs
2023-12-02 07:54:42.161 TRACE 0xc000bfa9a0 Task compiled ARGS() → WHEN() → DISCARD()
2023-12-02 07:54:42.161 INFO  0xc000bfa9a0 Greetings: 世界 idx: 4
2023-12-02 07:54:42.161 DEBUG 0xc000bfa9a0 Task elapsed 190.552µs
2023-12-02 07:54:42.161 DEBUG 0xc000bfa580 Task elapsed 1.102681ms
```

**使用例**

サブフローが引数以外のデータを取得する場合は、`args([idx])` オプション関数で渡された引数を再参照できます。

- サブフローの引数を使用してクエリーを実行します。

```js
// 疑似コード
// ...
WHEN( condition,
    do(value(0), {
        SQL(`select time, value from table where name = ?`, args(0))
        // ... MAP 関数による処理 ...
        INSERT(...)
    })
)
// ...
```

- 外部 Web サーバーから CSV ファイルを取得します。

```js
// 疑似コード
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

## FLATTEN()

![map_flatten](/neo/tql/img/map_flatten.jpg)

*構文*: `FLATTEN()`

`GROUPBYKEY()` の逆の処理を行います。多次元タプルを持つレコードを要素ごとに分解し、次元を減らした複数のレコードを生成します。

たとえば入力が `{key:k, value:[[v1,v2],[v3,v4],...,[vx,vy]]}` の場合、結果は `{key:k, value:[v1, v2]}`、`{key:k, value:[v3, v4]}`、...、`{key:k, value:[vx, vy]}` になります。

## MAPKEY()

![map_mapkey](/neo/tql/img/map_mapkey.jpg)

*構文*: `MAPKEY( newkey )`

現在のキーを、指定した新しいキーに置き換えます。

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

![map_pushkey](/neo/tql/img/map_pushkey.jpg)

*構文*: `PUSHKEY( newkey )`

すべてのレコードのキーを指定値に変更し、元のキーを値タプルの先頭に挿入します。

たとえば `{key: 'k1', value: [v1, v2]}` に `PUSHKEY(newkey)` を適用すると、`{key: newkey, values: [k1, v1, v2]}` に変換されます。

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

![map_popkey](/neo/tql/img/map_popkey.jpg)

*構文*: `POPKEY( [idx] )`

現在のキーを除去し、値タプルの *idx* 番目の要素を新しいキーにします。

たとえば `{key: k, value: [v1, v2, v3]}` に `POPKEY(1)` を適用すると、`{key: v2, value:[v1, v3]}` になります。

引数を省略すると `POPKEY(0)` と同じ動作になり、最初の値をキーにします。

{{< tabs >}}
{{< tab name="POPKEY()" >}}
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
{{< tab name="POPKEY(idx)" >}}
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

![map_popkey](/neo/tql/img/map_groupbykey.jpg)

*構文*: `GROUPBYKEY( [lazy(boolean)] )`

- `lazy(boolean)`: デフォルトの `false` では、キーが前のレコードと異なると直ちにグループ化したレコードを返します。`true` では入力ストリームが終了するまで待機します。

`GROUPBYKEY` は `GROUP( by( key() ) )` と同じ動作をします。

## THROTTLE()

*構文*: `THROTTLE(tps)` {{< neo_since ver="8.0.8" />}}

- `tps` *number*: 1 秒あたりに渡すレコード数。

`THROTTLE` は、指定した *tps* に合わせてレコードの転送速度を抑えます。  
保存済みのデータ（CSV など）を一定周期で流し、センサーデバイスをシミュレートする場合に便利です。

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE(linspace(1,5,5))
THROTTLE(5.0)
WHEN(true, doLog("===>tick", value(0)))
CSV()
```

- コンソールログの `"tick"` メッセージは、約 200ms 間隔（毎秒 5 件）で出力されます。
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

カスタムスクリプト言語をサポートします。  
詳細な例は [SCRIPT](../script/) を参照してください。