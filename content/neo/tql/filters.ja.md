---
title: ノイズフィルター
type: docs
weight: 80
toc: true
---

## センサーの測定値とノイズ {#센서-측정과-노이즈}

IoT環境で収集する値は、いずれもセンサーで測定したデータです。すべてのセンサーには一定のノイズが不可避的に含まれます。理論上、完全にノイズのないデータは数学的に生成した仮想データだけです。以下の例は、ノイズのない純粋な信号を表します。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_pure.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[6]}}
SCRIPT({
    x = []; y = [];
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        x.push( val );
        y.push( Math.sin( 1.2*2*Math.PI*val ) );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)

SET(sig, sin(1.2 * 2 * PI * value(0)) )
MAPVALUE(1, $sig)

CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< /tabs >}}

一般に、除去したいノイズは観測対象の信号より高い周波数を持ちます。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_pure_noise.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[4,7,8]}}
SCRIPT({
    x = []; y = []; z = [];
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        x.push( val );
        y.push( Math.sin( 1.2*2*Math.PI*val ) );
        z.push( 0.09 * Math.cos(9*2*Math.PI*val) +
                0.15 * Math.sin(12*2*Math.PI*val) );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value" },
            { type: "line", data: z, name:"noise" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)

SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig)
MAPVALUE(2, $noise)

CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
            { type: "line", data: column(2), name:"noise" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

実際のセンサーの測定値には、上記のようにノイズが混ざります。分析では、このノイズを除去して信号を観察します。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_mix_noise.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js
SCRIPT({
    x = []; y = [];
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) +
                0.15 * Math.sin(12*2*Math.PI*val);
        x.push( val );
        y.push( sig+noise );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value+noise" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## 平均フィルター {#평균-필터}

センサーのゼロ点校正（zero-point calibration）のように、連続する値の平均を取るとノイズを低減できます。以下は単純平均を適用した例です。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_avg.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[4,13]}}
SCRIPT({
    const filter = require("mathx/filter")
    const { arrange } = require("mathx");
    const avg = new filter.Avg();
    x = []; y = []; z = [];
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        x.push( val );
        y.push( sig );
        z.push( avg.eval(sig+noise) );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value+noise" },
            { type: "line", data: z, name:"AVG" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_AVG(2, value(1))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"AVG" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## 移動平均 {#이동-평균}

蓄積した全サンプルの平均を計算する代わりに、固定サイズのサンプル区間（ウィンドウ）内で平均を計算します。株価チャートでよく使うn日移動平均と同じ考え方です。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_movavg.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[4,13]}}
SCRIPT({
    const filter = require("mathx/filter")
    const { arrange } = require("mathx");
    const movavg = new filter.MovAvg(10);
    x = []; y = []; z = [];
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        x.push( val );
        y.push( sig );
        z.push( movavg.eval(sig+noise) );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value+noise" },
            { type: "line", data: z, name:"MA(10)" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_MOVAVG(2, value(1), 10)
CHART(
    size("600px", "400px"),
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
{{< /tab >}}
{{< /tabs >}}

## ローパスフィルター {#저역-통과-필터}

移動平均は扱いやすく理解も容易ですが、いくつかの制約があります。

ウィンドウ内のすべてのサンプルに同じ重みを適用するため、最新の傾向を反映するまでに時間がかかる場合があります。
また、値が大きく変化する区間への応答が比較的鈍くなります。
これを補うため、平均の計算時にウィンドウ内の新しい値と古い値に異なる重みを付ける方法がよく使われます。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_lpf.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[4,13]}}
SCRIPT({
    const filter = require("mathx/filter")
    const { arrange } = require("mathx");
    const lowpass = new filter.Lowpass(0.40);
    x = []; y = []; z = [];
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        x.push( val );
        y.push( sig );
        z.push( lowpass.eval(sig+noise) );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value+noise" },
            { type: "line", data: z, name:"lpf" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_LOWPASS(2, $sig + $noise, 0.40)
CHART(
    size("600px", "400px"),
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
{{< /tab >}}
{{< /tabs >}}

## カルマンフィルター {#칼만-필터}

`MAP_KALMAN()` 関数の `model()` 引数は、数学的なシステム変数を表す入力値を受け取ります。最適なシステム値の決定方法は、この文書の対象外です。
ただし、TQLで簡単なカルマンフィルターモデルを適用し、試行を繰り返して経験的に最適なパラメーターを探すことは容易です。

以下の例は、`model` の値の変化がグラフに与える影響を示します。
さまざまな `model` 値を適用し、グラフの変化を確認してください。

{{< tabs >}}
{{< tab name="チャート" >}}

{{< figure src="/neo/tql/img/filter_kalman.jpg" width="600px" >}}

{{< /tab >}}
{{< tab name="SCRIPT" >}}
```js {{linenos=table,hl_lines=[4,15]}}
SCRIPT({
    const filter = require("mathx/filter")
    const { arrange } = require("mathx");
    const kalman = new filter.Kalman(0.1, 0.5, 1.0);
    x = []; y = []; z = [];
    ts = new Date();
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        ts.setSeconds(ts.getSeconds() + 1);
        x.push( val );
        y.push( sig );
        z.push( kalman.eval(ts, sig+noise) );
    }
    $.yield({
        xAxis:{ type: "category", data: x},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: y, name:"value+noise" },
            { type: "line", data: z, name:"kalman" },
        ],
        legend: { bottom: 10 },
    });
})
CHART(size("600px", "400px"))
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_KALMAN(2, $sig + $noise, model(0.1, 0.6, 1.0))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"kalman" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}
