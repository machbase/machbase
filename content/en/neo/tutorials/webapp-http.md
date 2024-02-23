---
title: Web App with HTTP API
type: docs
weight: 30
---

{{< callout emoji="📌">}}
For the demonstration, the following table should be created in advance.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE  (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## HTML

Let's make a html file named `simple-webapp.html`. machbase-neo supports `.html`, `.js` and `.css` file editing {{< neo_since ver="8.0.14" />}}.
If you are using previous version of machbase-neo, please update it or use your favorite editor instead.

{{< figure src="../img/simple-webapp-1.jpg" width="600px" >}}

## Write data

Copy and paste the below codes.

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
                document.getElementById("rspSuccess").innerHTML = "success: " + obj.success
                document.getElementById("rspReason").innerHTML = "reason: " + obj.reason
                document.getElementById("rspElapse").innerHTML = "elapse: " + obj.elapse
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
    <div id="rspSuccess"></div> <div id="rspReason"></div> <div id="rspElapse"></div>
</body>
</html>
```

- line 6: Declare the data payload contains time value in millisecond unix epoc. which is used in line 14 `Date.now()`.
- line 9: Set content-type of the payload, so that machbase-neo interprets it properly.
- line 11-18: The actual data in payload. This example has only one record in the `rows` field, but it may contain multiple records, 

Save the code and open in web browser by click ► button on left top corner of the editor.

{{< figure src="../img/simple-webapp-2.jpg" width="600px" >}}

## Read data

Extend the simple-webapp.html to read data, add new `function queryData(){...}` and "query" action.

```js {{linenos="table",hl_lines=[3],linenostart=26}}
function queryData() {
    const query = `select * from example where name = 'webapp'`
    fetch(`http://127.0.0.1:5654/db/query?timeformat=ms&q=`+query).then(function(rsp){
        return rsp.json()
    }).then(function(obj){
        document.getElementById("rspQuery").innerHTML = '<pre>'+JSON.stringify(obj, null, 2)+'</pre>'
    })
}
```

- line 28: Specify the time format of result should be unix epoch in milliseconds.

```html {{linenos="table",linenostart=44}}
<h4> Query data </h4>
<a href="#" onClick="queryData()">Query</a>
<div id=rspQuery></div>
```

{{< figure src="../img/simple-webapp-3.jpg" width="600px" >}}

## Markdown

The query result can be transform to markdown using *TQL*, let's add `function markdownData(){...}`  and "Markdown" action.

```js {{linenos="table",hl_lines=[2,6],linenostart=35}}
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

- line 36: Get output format option if HTML or MARKDOWN text.
- line 40: `MARKDOWN()` TQL SINK with options `html(boolean)`, `timeformat()`, `tz()`...

```html {{linenos="table",linenostart=61}}
<h4> Markdown </h4>
<a href="#" onClick="markdownData()">Markdown</a> &nbsp;&nbsp;
<input type="checkbox" id="htmlMarkdown">HTML Output<br/>
<div id=rspMarkdown></div>
```

{{< figure src="../img/simple-webapp-4.jpg" width="600px" >}}

## Chart

You can visualize data with any chart library that you preference by retrieving the query result in JSON and CSV.
Still it is useful TQL provides `CHART()` SINK by default.

This example shows how to visualize data with TQL without any extra tool.

Add `function chartData()` and a helper `function loadJS()`.

```js {{linenos="table",hl_lines=[28,32],linenostart=48}}
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

And add Apache echart library, it is already included in machabse-neo for pre-loading.

```html {{linenos="table",linenostart=85}}
<script src="http://127.0.0.1:5654/web/echarts/echarts.min.js"></script>
```

```html {{linenos="table",linenostart=102}}
<h4> Chart </h4>
<a href="#" onClick="chartData()">Chart</a>
<div id=rspChart></div>
```

{{< figure src="../img/simple-webapp-5.jpg" width="600px" >}}


## Full source code

```html {{linenos="table"}}
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
            const query = `select * from example where name = 'webapp'`
            fetch(`http://127.0.0.1:5654/db/query?timeformat=ms&q=`+query).then(function(rsp){
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
    <a href="#" onClick="queryData()">Query</a>
    <div id=rspQuery></div>

    <h4> Markdown </h4>
    <a href="#" onClick="markdownData()">Markdown</a> &nbsp;&nbsp;
    <input type="checkbox" id="htmlMarkdown">HTML Output<br/>
    <div id=rspMarkdown></div>

    <h4> Chart </h4>
    <a href="#" onClick="chartData()">Chart</a>
    <div id=rspChart></div>
</body>
</html>
```