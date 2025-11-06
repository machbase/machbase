---
title: Grid.js를 활용한 웹 앱
type: docs
weight: 32
---

{{< callout emoji="📌">}}
예시를 진행하려면 미리 `EXAMPLE` 테이블을 생성해 두어야 합니다.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE  (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

이 예시는 machbase-neo의 데이터를 Grid.js 라이브러리로 표시하는 방법을 보여 줍니다.

{{< figure src="/neo/tutorials/img/grid-webapp-1.jpg" width="600px" >}}

- 18~19행: Grid.js 라이브러리를 포함합니다.
- 29~30행: 결과 JSON에서 컬럼과 데이터를 매핑합니다.
- 37행: 사용자가 새로 고침할 때 데이터를 갱신합니다.

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
