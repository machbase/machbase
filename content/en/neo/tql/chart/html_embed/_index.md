---
title: Embed in HTML
weight: 10
---

## IFRAME

```html {linenos=table,hl_lines=[3],linenostart=1}
<html>
    <body>
        <iframe src="doughunut.tql" width="600" height="600"/>
    </body>
</html>
```

## Dynamic TQL

The api `/db/tql` can receive POSTed TQL script and produces the result in javascript.
Caller side javascrpt can load the result javascript dynamically as the example below.

```html {linenos=table,hl_lines=[3,12,38,39],linenostart=1}
<html>
    <body id="body">
        <div id="chart_is_here" style="width:600px; height:600px"/>
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
                `}
            ).then(function(rsp){
                return rsp.json()
            }).then(function(obj) {
                const assets = obj.jsAssets.concat(obj.jsCodeAssets)
                assets.forEach((js) => loadJS(js))
            }).catch(function(err){
                console.log("chart fetch error", err)
            })
        </script>
    </body>
</html>
```

The actual the reponse of `/db/tql` is JSON that points the result javascript.
The line 38, 39 of the above example, it merged `jsAssets` and `jsCodeAssets` and loaded into the HTML document.

```json
{
    "chartID":"chart_is_here",
    "jsAssets": ["/web/echarts/echarts.min.js"],
	"jsCodeAssets": ["/web/api/tql-assets/chart_is_here.js"],
    "style": {
        "width": "600px",
        "height": "600px"	
    },
    "theme": "white"
}
```
