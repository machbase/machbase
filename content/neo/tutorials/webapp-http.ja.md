---
toc: true
title: HTTP APIのWebアプリ
type: docs
weight: 30
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

## HTML {#html}

`simple-webapp.html`ファイルを作成します。machbase-neoは、{{< neo_since ver="8.0.14" />}}から`.html`、`.js`、`.css`ファイルを直接編集できます。
以前のバージョンを使用している場合は、更新するか任意のエディターを使用してください。

{{< figure src="/neo/tutorials/img/simple-webapp-1.jpg" width="600px" >}}

ファイルを編集して保存し、エディター左上の►ボタンをクリックすると、ブラウザーで開けます。

## データの書き込み {#데이터-쓰기}

以下のコードをコピーして貼り付けます。

```html {{linenos="table",hl_lines=[6,9,"11-18"]}}
<html>
<head>
    <script>
        function submitData() {
            const value  = Number(document.getElementById("userInput").value)
            fetch("http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ms", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "data": {
                        "columns": ["name", "time", "value"],
                        "rows": [
                            [ "webapp", Date.now(), value ]
                        ]
                    }
                })
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                 document.getElementById("rspInput").innerHTML = '<pre>'+JSON.stringify(obj, null, 2)+'</pre>'
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
</body>
</html>
```

- 6行目：`timeformat=ms`は、送信するタイムスタンプがミリ秒単位のUnixエポック時刻であることを示します。15行目の`Date.now()`に対応します。
- 9行目：コンテンツタイプを指定し、machbase-neoがペイロード形式を正しく解釈できるようにします。
- 11〜18行目：送信する実際のデータです。この例は1件ですが、`rows`配列には複数のレコードを含められます。

{{< figure src="/neo/tutorials/img/simple-webapp-2.jpg" width="600px" >}}

## データの検索 {#데이터-조회}

`simple-webapp.html`にデータを読み取る機能を追加します。`function queryData(){...}`と「Query」アクションを追加してください。

```js {{linenos="table",hl_lines=[4],linenostart=26}}
function queryData() {
    const query = `select * from example where name = 'webapp' limit 5`
    const opt  = document.querySelector('input[name="opt"]:checked').value + '=true'
    fetch(`http://127.0.0.1:5654/db/query?timeformat=ms&`+opt+`&q=`+query).then(function(rsp){
        return rsp.json()
    }).then(function(obj){
        document.getElementById("rspQuery").innerHTML = '<pre>'+JSON.stringify(obj, null, 2)+'</pre>'
    })
}
```

- 28行目：結果の時刻形式をミリ秒単位のUnixエポック時刻に指定します。

```html {{linenos="table",linenostart=94}}
<h4> Query data </h4>
<input type="radio" name="opt" value="none" checked/>none
<input type="radio" name="opt" value="transpose" />transpose
<input type="radio" name="opt" value="rowsFlatten" />rowsFlatten
<input type="radio" name="opt" value="rowsArray" />rowsArray
<a href="#" onClick="queryData()">Query</a>
<div id=rspQuery></div>
```

{{< figure src="/neo/tutorials/img/simple-webapp-3.jpg" width="600px" >}}

## Markdown {#markdown}

クエリ結果は、*TQL*でMarkdownに変換できます。`function markdownData(){...}`と「Markdown」ボタンを追加します。

```js {{linenos="table",hl_lines=[2,6],linenostart=36}}
function markdownData() {
    const asHtml = document.getElementById("htmlMarkdown").checked
    fetch(`http://127.0.0.1:5654/db/tql`, {
        method: "POST",
        body: ` SQL("select * from example where name = 'webapp' limit 100")
                MARKDOWN( html(`+asHtml+`), timeformat('Default'), tz('Local'), briefCount(10) )`
    }).then(function(rsp){
        return rsp.text()
    }).then(function(obj){
        document.getElementById("rspMarkdown").innerHTML = '<pre>'+obj+'</pre>'
    })
}
```

- 36行目：出力形式として、HTMLまたは通常のMarkdownを選択します。
- 40行目：TQL SINKの`MARKDOWN()`に、`html(boolean)`、`timeformat()`、`tz()`などのオプションを指定します。

```html {{linenos="table",linenostart=102}}
<h4> Markdown </h4>
<input type="checkbox" id="htmlMarkdown">HTML Output &nbsp;&nbsp;
<a href="#" onClick="markdownData()">Markdown</a><br/>
<div id=rspMarkdown></div>
```

{{< figure src="/neo/tutorials/img/simple-webapp-4.jpg" width="600px" >}}

## グラフ {#차트}

HTTP APIでJSONやCSVデータを取得して任意のグラフライブラリを使用できます。また、TQLの`CHART()` SINKを使用すると簡単に可視化できます。
追加のツールを使わず、TQLだけでデータを可視化する例を示します。

`function chartData()`とヘルパー関数`function loadJS()`を追加します。

```js {{linenos="table",hl_lines=[20,28,32],linenostart=49}}
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
        body: ` SQL("select * from example where name = 'webapp' limit 100")
                MAPVALUE(0, list(value(1), value(2)))
                POPVALUE(1, 2)
                CHART(
                    size("600px", "200px"),
                    chartID('rspChart'),
                    chartOption({
                        xAxis:{ type: "time" },
                        yAxis:{},
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
```

Apache EChartsライブラリも追加します。machbase-neoに組み込まれているため、そのまま使用できます。

```html {{linenos="table",linenostart=84}}
<script src="http://127.0.0.1:5654/web/echarts/echarts.min.js"></script>
```

```html {{linenos="table",linenostart=107}}
<h4> Chart </h4>
<a href="#" onClick="chartData()">Chart</a>
<div id=rspChart></div>
```

{{< figure src="/neo/tutorials/img/simple-webapp-5.jpg" width="600px" >}}


## ソースコード全体 {#전체-소스-코드}

```html {{linenos="table",hl_lines=[4,26,36,49,60,84]}}
<html>
<head>
    <script>
        function submitData() {
            const value  = Number(document.getElementById("userInput").value)
            fetch("http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ms", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "data": {
                        "columns": ["name", "time", "value"],
                        "rows": [
                            [ "webapp", Date.now(), value ]
                        ]
                    }
                })
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                document.getElementById("rspInput").innerHTML = '<pre>'+JSON.stringify(obj, null, 2)+'</pre>'
            })
        }

        function queryData() {
            const query = `select * from example where name = 'webapp' limit 5`
            const opt  = document.querySelector('input[name="opt"]:checked').value + '=true'
            fetch(`http://127.0.0.1:5654/db/query?timeformat=ms&`+opt+`&q=`+query).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                document.getElementById("rspQuery").innerHTML = '<pre>'+JSON.stringify(obj, null, 2)+'</pre>'
            })
        }

        function markdownData() {
            const asHtml = document.getElementById("htmlMarkdown").checked
            fetch(`http://127.0.0.1:5654/db/tql`, {
                method: "POST",
                body: ` SQL("select * from example where name = 'webapp' limit 100")
                        MARKDOWN( html(`+asHtml+`), timeformat('Default'), tz('Local'), briefCount(10) )`
            }).then(function(rsp){
                return rsp.text()
            }).then(function(obj){
                document.getElementById("rspMarkdown").innerHTML = '<pre>'+obj+'</pre>'
            })
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
                body: ` SQL("select * from example where name = 'webapp' limit 100")
                        MAPVALUE(0, list(value(1), value(2)))
                        POPVALUE(1, 2)
                        CHART(
                            size("600px", "200px"),
                            chartID('rspChart'),
                            chartOption({
                                xAxis:{ type: "time" },
                                yAxis:{},
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
    <h4> Input data </h4>
    <form>
        <input id="userInput">
        <a href="#" onClick="submitData()">Submit</a>
    </form>
    <div id="rspInput"></div>

    <h4> Query data </h4>
    <input type="radio" name="opt" value="none" checked/>none
    <input type="radio" name="opt" value="transpose" />transpose
    <input type="radio" name="opt" value="rowsFlatten" />rowsFlatten
    <input type="radio" name="opt" value="rowsArray" />rowsArray
    <a href="#" onClick="queryData()">Query</a>
    <div id=rspQuery></div>

    <h4> Markdown </h4>
    <input type="checkbox" id="htmlMarkdown">HTML Output &nbsp;&nbsp;
    <a href="#" onClick="markdownData()">Markdown</a><br/>
    <div id=rspMarkdown></div>

    <h4> Chart </h4>
    <a href="#" onClick="chartData()">Chart</a>
    <div id=rspChart></div>
</body>
</html>
```
