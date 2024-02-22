---
title: Embed in HTML
type: docs
weight: 10
---

## IFRAME

```html {linenos=table,hl_lines=[3],linenostart=1}
<html>
    <body>
        <iframe src="basic_line.tql" width="600" height="600"/>
    </body>
</html>
```

## JSON Response

Call *.tql* script file with a custom HTTP header `X-Chart-Output: json` {{< neo_since ver="8.0.14" />}} 
to produce the result in JSON instead of full HTML document,
so that caller can embed the chart into any place of the HTML DOM.

When the reponse of `/db/tql` is JSON, it contains required addresses of the result javascript.

```json
{
    "chartID":"NDg4ODQ4MzMxMjgyMDYzMzY",
    "jsAssets": ["/web/echarts/echarts.min.js"],
	"jsCodeAssets": ["/web/api/tql-assets/NDg4ODQ4MzMxMjgyMDYzMzY.js"],
    "style": {
        "width": "600px",
        "height": "600px"	
    },
    "theme": "white"
}
```

The line 22, 23 of the below example, it merged `jsAssets` and `jsCodeAssets` and loaded into the HTML document.

```html {linenos=table,hl_lines=[3,13,18,"22-23"],linenostart=1}
<html>
    <body id="body">
        <div id="chart_is_here"/>
        <script>
            function loadJS(url) {
                var scriptElement = document.createElement('script');
                scriptElement.src = url;
                document.getElementsByTagName('body')[0].appendChild(scriptElement);
            }
        </script>
        <script>
            fetch("basic_line.tql", {
                headers: { "X-Chart-Output": "json" }
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj) {
                const chartDiv = document.createElement('div')
                chartDiv.setAttribute("id", obj.chartID)
                chartDiv.style.width = obj.style.width
                chartDiv.style.height = obj.style.height
                document.getElementById('chart_is_here').appendChild(chartDiv)
                const assets = obj.jsAssets.concat(obj.jsCodeAssets)
                assets.forEach((js) => loadJS(js))
            }).catch(function(err){
                console.log("chart fetch error", err)
            })
        </script>
    </body>
</html>
```

## Dynamic TQL

The api `/db/tql` can receive POSTed TQL script and produces the result in javascript.
Caller side javascrpt can load the result javascript dynamically as the example below.

In this example, the `chartID()` (line 19) is provided and the document has a `<div>` with the same `id`.

```html {linenos=table,hl_lines=[3,12,19,38,39],linenostart=1}
<html>
    <body id="body">
        <div id="chart_is_here"/>
        <script>
            function loadJS(url) {
                var scriptElement = document.createElement('script');
                scriptElement.src = url;
                document.getElementsByTagName('body')[0].appendChild(scriptElement);
            }
        </script>
        <script>
            fetch("/db/tql", 
                {
                    method:"POST", 
                    body:`
                        FAKE( linspace(0, 360, 100) )
                        MAPVALUE( 1, sin(value(0)/180*PI) )
                        CHART(
                            chartID("chart_is_here"),
                            chartOption({
                                xAxis: { type: "category", data: column(0) },
                                yAxis: {},
                                series: [
                                    {
                                        type: "line",
                                        data: column(1)
                                    }
                                ]
                            })
                        )
                `}
            ).then(function(rsp){
                return rsp.json()
            }).then(function(obj) {
                const chartDiv = document.getElementById('chart_is_here')
                chartDiv.style.width = obj.style.width
                chartDiv.style.height = obj.style.height
                const assets = obj.jsAssets.concat(obj.jsCodeAssets)
                assets.forEach((js) => loadJS(js))
            }).catch(function(err){
                console.log("chart fetch error", err)
            })
        </script>
    </body>
</html>
```

## Loading Sequence Problem

In the examples above, we loaded the result javascript files in a time for briefness.
```js {linenos=table,linenostart=38}
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

In real application, the chart library (apache echarts) in `obj.jsAssets` might not be completely loaded before `obj.jsCodeAssets` are loaded.
If there is a problem in loading sequence, it can be fixed like below code.

Add `load` event listener to enable callback for load-completion.

```js {linenos=table,hl_lines=["5-9"],linenostart=5}
function loadJS(url, callback) {
    var scriptElement = document.createElement('script');
    scriptElement.src = url;
    document.getElementsByTagName('body')[0].appendChild(scriptElement);
    scriptElement.addEventListener("load", ()=>{
        if (callback !== undefined) {
            callback()
        }
    })
}
```

When the last `jsAssets` loaded, start to load `jsCodeAssets`.

```js {linenos=table,hl_lines=[5,"7-9"],linenostart=38}
// const assets = obj.jsAssets.concat(obj.jsCodeAssets)
// assets.forEach((js) => loadJS(js))
for (let i = 0; i < obj.jsAssets.length; i++ ){
    if (i < obj.jsAssets.length -1){ 
        loadJS(obj.jsAssets[i])
    } else { // when the last asset is loaded, start to load jsCodeAssets
        loadJS(obj.jsAssets[i], () => {
            obj.jsCodeAssets.forEach(js => loadJS(js)) 
        })
    }
}
```