---
title: "@jsh/filter"
type: docs
weight: 60
---

{{< neo_since ver="8.0.52" />}}

## Avg

**Usage example**

```js {linenos=table,linenostart=1}
const { arrange } = require("@jsh/generator");
const m = require("@jsh/filter")
const avg = new m.Avg();
for( x of arrange(10, 30, 10) ) {
    console.log(x,  avg.eval(x).toFixed(2));
}

// 10 10.00
// 20 15.00
// 30 20.00
```

## MovAvg

**Usage example**

```js {linenos=table,linenostart=1}
const { linspace } = require("@jsh/generator");
const m = require("@jsh/filter")
const movAvg = new m.MovAvg(10);
for( x of linspace(0, 100, 100) ) {
    console.log(""+x.toFixed(4)+","+movAvg.eval(x).toFixed(4));
}
```

## Lowpass

**Usage example**

```js {linenos=table,linenostart=1}
const { arrange, Simplex } = require("@jsh/generator");
const m = require("@jsh/filter")
const lpf = new m.Lowpass(0.3);
const simplex = new Simplex(1);

for( x of arrange(1, 10, 1) ) {
    v = x + simplex.eval(x) * 3;
    console.log(x, v.toFixed(2), lpf.eval(v).toFixed(2));
}
```

## Kalman

**Usage example**

```js {linenos=table,linenostart=1}
const m = require("@jsh/filter");
const kalman = new m.Kalman(1.0, 1.0, 2.0);
var ts = 1745484444000; // ms

for( x of [1.3, 10.2, 5.0, 3.4] ) {
    ts += 1000; // add 1 sec.
    console.log(kalman.eval(new Date(ts), x).toFixed(3));
}

// 1.300
// 5.750
// 5.375
// 4.388
```

## KalmanSmoother

**Usage example**

```js {linenos=table,linenostart=1}
const m = require("@jsh/filter");
const kalman = new m.KalmanSmoother(1.0, 1.0, 2.0);
var ts = 1745484444000; // ms
for( x of [1.3, 10.2, 5.0, 3.4] ) {
    ts += 1000; // add 1 sec.
    console.log(kalman.eval(new Date(ts), x).toFixed(2));
}

// 1.30
// 5.75
// 3.52
// 2.70
```

## Kalman Filter vs. Smoother

```js
SCRIPT("js", {
    const { now } = require("@jsh/system");
    const { arrange, Simplex } = require("@jsh/generator");
    const m = require("@jsh/filter")
    const simplex = new Simplex(1234);
    const kalmanFilter = new m.Kalman(0.1, 0.001, 1.0);
    const kalmanSmoother = new m.KalmanSmoother(0.1, 0.001, 1.0);
    const real = 14.4;
}, {
    s_x = []; s_values = []; s_filter = []; s_smooth = [];
    for( x of arrange(0, 10, 0.1)) {
        x = Math.round(x*100)/100;
        measure = real + simplex.eval(x) * 4;
        s_x.push(x);
        s_values.push(measure);
        s_filter.push(kalmanFilter.eval(now(), measure));
        s_smooth.push(kalmanSmoother.eval(now(), measure));
    }
    $.yield({
        title:{text:"Kalman filter vs. smoother"},
        xAxis:{type:"category", data:s_x},
        yAxis:{ min:10, max: 18 },
        series:[
            {type:"line", data:s_values, name:"values"},
            {type:"line", data:s_filter, name:"filter"},
            {type:"line", data:s_smooth, name:"smoother"}
        ],
        tooltip: {show: true, trigger:"axis"},
        legend: { bottom: 10},
        animation: false
    });
})
CHART(size("600px", "400px"))
```

{{< figure src="../img/kalman_filter_smoother.jpg">}}