---
title: HTTP API를 활용한 웹 앱
type: docs
weight: 30
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

## HTML

`simple-webapp.html` 파일을 만들어 봅시다. machbase-neo는 {{< neo_since ver="8.0.14" />}}부터 `.html`, `.js`, `.css` 파일을 직접 편집할 수 있습니다.
이전 버전을 사용 중이라면 업데이트하거나 선호하는 편집기를 사용해 주십시오.

{{< figure src="../img/simple-webapp-1.jpg" width="600px" >}}

파일을 수정 후 저장하고, 편집기 좌측 상단의 ► 버튼을 클릭하면 브라우저에서 바로 열 수 있습니다.

## 데이터 쓰기

아래 코드를 복사해 붙여 넣습니다.

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

- 6행: `timeformat=ms`는 전송하는 타임스탬프가 밀리초 단위 유닉스 에포크임을 나타냅니다. 15행의 `Date.now()`와 연동됩니다.
- 9행: 콘텐츠 타입을 지정해 machbase-neo가 페이로드 형식을 올바르게 해석하도록 합니다.
- 11~18행: 전송할 실제 데이터입니다. 예시는 1건이지만 `rows` 배열에 여러 건을 담을 수 있습니다.

{{< figure src="../img/simple-webapp-2.jpg" width="600px" >}}

## 데이터 조회

`simple-webapp.html`에 데이터를 읽어오는 기능을 추가합니다. `function queryData(){...}`와 "Query" 액션을 더해 주세요.

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

- 28행: 결과의 시간 형식을 밀리초 단위 유닉스 에포크로 지정합니다.

```html {{linenos="table",linenostart=94}}
<h4> Query data </h4>
<input type="radio" name="opt" value="none" checked/>none
<input type="radio" name="opt" value="transpose" />transpose
<input type="radio" name="opt" value="rowsFlatten" />rowsFlatten
<input type="radio" name="opt" value="rowsArray" />rowsArray
<a href="#" onClick="queryData()">Query</a>
<div id=rspQuery></div>
```

{{< figure src="../img/simple-webapp-3.jpg" width="600px" >}}

## Markdown

쿼리 결과를 *TQL*을 이용해 마크다운으로 변환할 수 있습니다. `function markdownData(){...}`와 "Markdown" 버튼을 추가합니다.

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

- 36행: 출력 형태를 HTML 또는 일반 마크다운으로 선택합니다.
- 40행: `MARKDOWN()` TQL 싱크에 `html(boolean)`, `timeformat()`, `tz()` 등의 옵션을 지정합니다.

```html {{linenos="table",linenostart=102}}
<h4> Markdown </h4>
<input type="checkbox" id="htmlMarkdown">HTML Output &nbsp;&nbsp;
<a href="#" onClick="markdownData()">Markdown</a><br/>
<div id=rspMarkdown></div>
```

{{< figure src="../img/simple-webapp-4.jpg" width="600px" >}}

## 차트

HTTP API로 JSON 또는 CSV 데이터를 받아 선호하는 차트 라이브러리를 사용할 수도 있지만, TQL의 `CHART()` 싱크를 이용하면 간편하게 시각화할 수 있습니다.
추가 도구 없이 TQL만으로 데이터를 시각화하는 예시는 다음과 같습니다.

`function chartData()`와 보조 함수 `function loadJS()`를 추가합니다.

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

또한 Apache ECharts 라이브러리를 추가합니다. machbase-neo에 기본 포함되어 있어 바로 사용할 수 있습니다.

```html {{linenos="table",linenostart=84}}
<script src="http://127.0.0.1:5654/web/echarts/echarts.min.js"></script>
```

```html {{linenos="table",linenostart=107}}
<h4> Chart </h4>
<a href="#" onClick="chartData()">Chart</a>
<div id=rspChart></div>
```

{{< figure src="../img/simple-webapp-5.jpg" width="600px" >}}


## 전체 소스 코드

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
