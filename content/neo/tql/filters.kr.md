---
title: 노이즈 필터
type: docs
weight: 80
---

## 센서 측정과 노이즈

IoT 환경에서 수집되는 값은 모두 센서를 통해 측정된 데이터입니다. 모든 센서는 필연적으로 일정 수준의 노이즈(잡음)를 포함하며, 이론적으로 완전히 깨끗한 데이터는 수학적으로 생성한 가상 데이터일 뿐입니다. 아래 예제는 노이즈가 없는 순수한 신호를 표현합니다.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< figure src="/neo/tql/img/filter_pure.jpg" width="600px" >}}

{{< /tab >}}
{{< tab >}}
```js
SCRIPT({
    $.result = { columns: ["val", "sig"], types: ["double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        $.yield( val, sig );
    }
})
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
{{< tab >}}
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

일반적으로 우리가 제거하고 싶은 노이즈는 관측 대상 신호보다 더 높은 주파수를 갖습니다.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< figure src="/neo/tql/img/filter_pure_noise.jpg" width="600px" >}}

{{< /tab >}}
{{< tab >}}
```js
SCRIPT({
    $.result = { columns: ["val", "sig", "noise"], types: ["double", "double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) +
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig, noise );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
            { type: "line", data: column(2), name:"noise" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
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

실제 센서로부터 측정된 값은 위와 같은 노이즈가 섞인 형태가 되며, 분석 과정에서는 이 노이즈를 필터링해 신호를 관찰하고 싶어집니다.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< figure src="/neo/tql/img/filter_mix_noise.jpg" width="600px" >}}

{{< /tab >}}
{{< tab >}}
```js
SCRIPT({
    $.result = { columns: ["val", "sig"], types: ["double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) +
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
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

## 평균 필터

센서의 영점 보정(zero-point calibration)처럼 연속된 값을 평균하면 노이즈가 줄어드는 효과가 있습니다. 아래 예시는 단순 평균을 적용한 결과입니다.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< figure src="/neo/tql/img/filter_avg.jpg" width="600px" >}}

{{< /tab >}}
{{< tab >}}
```js
SCRIPT({
    const filter = require("@jsh/filter")
    const avg = new filter.Avg();
    const { arrange } = require("@jsh/generator");
}, {
    for( val of arrange(1, 5, 0.03)) {
        sig = Math.sin(1.2*2*Math.PI*val);
        noise = 0.09*Math.cos(9*2*Math.PI*val)+0.15*Math.sin(12*2*Math.PI*val);
        avg.push(sig + noise);
        $.yield(val, sig + noise, avg.value());
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"avg" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MOVAVG( value(1), window(10) )
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"avg" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## 누적 평균, 이동 평균, 지수 평균

Machbase TQL은 누적 평균, 이동 평균, 지수 평균 등을 쉽게 적용할 수 있는 필터 함수를 제공합니다. 각 필터에 관한 상세 예제는 하위 문서에서 확인할 수 있습니다.

## 시계열 필터 요약

- **AVG / MOVAVG** : 저주파 신호에서 고주파 노이즈를 제거할 때 사용합니다.
- **EWMA** : 최근 데이터에 더 많은 가중치를 주어 추이를 부드럽게 관찰할 수 있습니다.
- **Median Filter** : 순간적인 이상치에 민감할 때 유용합니다.

{{< children_toc />}}
