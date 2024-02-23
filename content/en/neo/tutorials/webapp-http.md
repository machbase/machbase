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

## Write data

Let's make a html file named `simple-webapp.html`. machbase-neo supports `.html`, `.js` and `.css` file editing {{< neo_since ver="8.0.14" />}}.
If you are using previous version of machbase-neo, please update it or use your favorite editor instead.

{{< figure src="../img/simple-webapp-1.jpg" width="600px" >}}

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
- line 9: Set content-type of the payload, so that machbase-neo interpret it properly.
- line 11-18: The actual data payload in payload. This example has only one record, but it may contain multiple records, 

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
        </script>
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
    </body>
</html>
```