---
toc: true
title: 乱数データのWebアプリ
type: docs
weight: 31
---

{{< callout emoji="📌">}}
この例を実行する前に、`EXAMPLE`テーブルを作成してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE  (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

この例では、毎秒乱数データを生成し、グラフを自動更新します。

{{< figure src="/neo/tutorials/img/random-webapp-1.jpg" width="600px" >}}

- 11行目：「start」ボタンを押すとタイマーが動作し、`EXAMPLE`テーブルにデータを記録します。
- 13行目：ペイロードはCSV形式です。
- 37行目：`SQL_SELECT()`と`CHART()`を組み合わせてグラフを描画します。

```html {{linenos="table",hl_lines=[11,"13-14",26,37]}}
<html>
<head>
    <script>
        var timer
        function toggleTimer(){
            const btn = document.getElementById('btn')
            if (btn.value == 'start') {
                btn.value = 'stop'
                timer = setInterval(function(){
                    // 新しい乱数値を挿入
                    fetch("http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ms", {
                        method: "POST",
                        headers: { "Content-Type": "text/csv" },
                        body: "webapp," + Date.now() + "," + Math.random()
                    });
                    // グラフを更新
                    chartData();
                }, 1000)
            } else {
                btn.value = 'start'
                clearTimeout(timer);
            }
        }

        function loadJS(url) {
            var scriptElement = document.getElementById("chartScript")
            if ( scriptElement != null) {
                scriptElement.remove()
            }
            scriptElement = document.createElement('script');
            scriptElement.id = "chartScript"
            scriptElement.src = url;
            document.getElementsByTagName('head')[0].appendChild(scriptElement);
        }

        function chartData() {
            fetch(`http://127.0.0.1:5654/db/tql`, {
                method: "POST",
                body: ` SQL_SELECT("time", "value", from("example", "webapp"), between("last-60s", "last"))
                        MAPVALUE(0, list(value(0), value(1)))
                        POPVALUE(1)
                        CHART(
                            size("600px", "400px"),
                            chartID('rspChart'),
                            theme('dark'),
                            chartOption({
                                xAxis:{ type: "time", axisLabel: { rotate: 30, interval:5 } },
                                yAxis:{ min: 0, max: 1.0},
                                animation: true,
                                series:[ { type:"line", data:column(0) } ]
                            })
                        )`
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                document.getElementById('rspChart').style.width = obj.style.width
                document.getElementById('rspChart').style.height = obj.style.height
                obj.jsCodeAssets.forEach(js => loadJS(js)) 
            })
        }
    </script>
    <script src="http://127.0.0.1:5654/web/echarts/echarts.min.js"></script>
</head>
<body>
    <input type="button" id="btn" value="start" onclick="toggleTimer()" style="height:32px;width:64px;"/>
    <br/><br/>
    <div id=rspChart></div>
</body>
</html>
```
