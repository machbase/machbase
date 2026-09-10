---
toc: true
title: Grid.jsを使ったWebアプリ
type: docs
weight: 32
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

この例は、machbase-neoのデータをGrid.jsライブラリで表示する方法を示します。

{{< figure src="/neo/tutorials/img/grid-webapp-1.jpg" width="600px" >}}

- 18〜19行目：Grid.jsライブラリを組み込みます。
- 29〜30行目：結果のJSONから列とデータを割り当てます。
- 37行目：ユーザーが再読み込みしたときにデータを更新します。

```html {{linenos="table",hl_lines=["18-19","29-30",37]}}
<html>
<head>
    <script>
        function submitData() {
            const value  = Number(document.getElementById("userInput").value)
            fetch("/db/write/EXAMPLE?timeformat=ms", {
                method: "POST",
                headers: { "Content-Type": "text/csv" },
                body: 'webapp,' + Date.now() + "," + value
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                document.getElementById("rspInput").
                innerHTML = '<li> success:'+obj.success+", reason:"+obj.reason
            })
        }
    </script>
    <link href="https://unpkg.com/gridjs/dist/theme/mermaid.min.css" rel="stylesheet"/>
    <script src="https://unpkg.com/gridjs/dist/gridjs.umd.js"></script>
    <script>
        var grid = null;
        function gridData(){
            const query = `select * from EXAMPLE where name = 'webapp' order by time desc`;
            fetch(`/db/query?timeformat=Default&tz=local&q=`+query).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                if (grid == null) {
                    grid = new gridjs.Grid({
                        columns: obj.data.columns,
                        data: obj.data.rows,
                        width: "800px",
                        pagination:{ limit: 5, summary: false }
                    })
                    grid.render(document.getElementById("rspGrid"))
                } else {
                    grid.updateConfig({
                        data: obj.data.rows,
                    }).forceRender();
                }
            })
        }
    </script>
</head>
<body>
    <h4> Input data </h4>
    <form>
        <input id="userInput">
        <a href="#" onClick="submitData()">Submit</a>
    </form>
    <div id="rspInput"></div>
    <h4> Grid </h4>
    <a href="#" onClick="gridData()">Refresh</a>
    <div id="rspGrid"></div>
</body>
</html>
```
