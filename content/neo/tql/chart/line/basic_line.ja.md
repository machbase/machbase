---
title: 基本的な折れ線グラフ
type: docs
weight: 10
toc: true
---

## SRC :: FAKE()

```js {linenos=table,linenostart=1}
FAKE( linspace(0, 360, 100))
// |   0
// +-> x
// |
MAPVALUE(1, sin((value(0)/180)*PI))
// |   0   1
// +-> x   sin(x)
// |
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

{{< figure src="/neo/tql/chart/img/basic_line.jpg" width="500" >}}

## SRC :: SCRIPT()

```js {linenos=table,linenostart=1}
SCRIPT({
    for( x = 0; x < 360; x+=3.6) {
        $.yield(x, Math.sin(x/180*Math.PI));
    }
})
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

## SRC :: SQL()

### データの準備 {#prepare-data}

```js {linenos=table,linenostart=1}
FAKE( arrange(1, 100, 1))
// |   0
// +-> seq
// |
MAPVALUE(1, sin((2*PI*value(0)/100)))
// |   0       1
// +-> seq     value
// |
MAPVALUE(0, timeAdd("now-100s", strSprintf("+%.fs", value(0))))
// |   0       1
// +-> time    value
// |
PUSHVALUE(0, "chart-line")
// |   0       1       2
// +-> name    time    value
// |
APPEND(table("example"))
```

### SCRIPTによるデータの準備 {#prepare-data-with-script}

```js {linenos=table,linenostart=1}
SCRIPT({
    const { arrange } = require("mathx");
    now = (new Date()).getTime() - 100 * 1000; // 現在時刻の100秒前。
    for(x of arrange(1, 100, 1)) {
        y = Math.sin(x/100*2*Math.PI)
        ts = new Date(now + x * 1000); // 1秒加算
        $.yield("chart-line", ts, y);
    }
})
APPEND(table("example"))
```

### SQL()からCHART()へ {#sql-to-chart}

```js {linenos=table,hl_lines=[4,10],linenostart=1}
SQL(`select time, value from example where name = 'chart-line'`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0)
            }
        ]
    })
)
```

{{< figure src="/neo/tql/chart/img/basic_line_sql.jpg" width="500" >}}

### SCRIPT()からCHART()へ {#script-to-chart}

```js {{linenos=table,linenostart=1}}
SCRIPT({
    const {Client} = require("machcli");
    var db, conn, rows;
    var data = [];
    const conf = { user: 'sys', password: 'manager' };
    try {
        db = new Client(conf);
        conn = db.connect();
        rows = conn.query(`select time, value from example where name = ?`, 'chart-line')
        for( r of rows) {
            data.push([r.time, r.value]);
        }
    } catch( e ) {
        console.println("ERROR", e.message);
    } finally {
        rows && rows.close();
        conn && conn.close();
        db && db.close();
    }
    $.yield({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: data,
            }
        ]
    })
})
CHART()
```

```html {{linenos=table,linenostart=1}}
SQL(`select time, value from example where name = 'chart-line'`)
SCRIPT({
    data = [];
}, {
    data.push([$.values[0], $.values[1]]);
}, {
    $.yield(data); 
})
HTML(template({
    <span>
        <script src="/web/echarts/echarts.min.js"></script>
        <div id='xyz' style="width:600px;height:400px;"></div>
        <script>
            var data = {{ .Values }};
            var chartDom = document.getElementById('xyz');
            var myChart = echarts.init(chartDom);
            var option = {
                xAxis: { type: "time" },
                yAxis: {},
                tooltip: { trigger:"axis" },
                series: [
                    {type: 'line',  data: data[0], symbol:"none"}
                ]
            };
            option && myChart.setOption(option);
        </script>
    </span>
}))
```
