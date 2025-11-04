---
title: Embed in HTML
type: docs
weight: 10
---

아래 코드를 `basic_line.tql`로 저장해 주십시오. 이 문서에서는 해당 *TQL* 결과를 웹 페이지에 임베드하는 방법을 안내드립니다.

```js
FAKE( linspace(0, 360, 100))
MAPVALUE(2, sin((value(0)/180)*PI))
CHART(
    theme("white"),
    chartOption({
        "xAxis": { "type": "category", "data": column(0) },
        "yAxis": {},
        "series": [ { "type": "line", "data": column(1) } ]
    })
)
```

## IFRAME

```html {linenos=table,hl_lines=[3],linenostart=1}
<html>
<body>
    <iframe src="basic_line.tql" width="600" height="600"/>
</body>
</html>
```

## JSON 응답 활용

TQL 스크립트를 호출할 때 `X-Tql-Output: json` 헤더를 추가하면 {{< neo_since ver="8.0.42" />}} (기존 `X-Chart-Output` 헤더는 사용 중단됨 {{< neo_since ver="8.0.14" />}}) 기본 HTML 대신 JSON을 받을 수 있습니다.  
이 JSON에는 차트를 렌더링하는 데 필요한 자바스크립트 경로가 포함되므로, 원하는 DOM 위치에 직접 삽입할 수 있습니다.  
`X-Tql-Output: json` 헤더는 `CHART()` 싱크에서 `chartJson(true)` 옵션을 사용하는 것과 동일하며, 예시는 [As Reading API](/neo/tql/reading/#chart-with-chartjson) 문서에서 확인할 수 있습니다.

`/db/tql`이 JSON을 반환할 경우, 필요한 스크립트 주소가 함께 제공됩니다.

```json
{
    "chartID": "NDg4ODQ4MzMxMjgyMDYzMzY",
    "jsAssets": ["/web/echarts/echarts.min.js"],
    "jsCodeAssets": ["/web/api/tql-assets/NDg4ODQ4MzMxMjgyMDYzMzY.js"],
    "style": {
        "width": "600px",
        "height": "600px"	
    },
    "theme": "white"
}
```

- `chartID`: ECharts에서 사용되는 랜덤 ID입니다. 필요하면 `chartID()` 옵션으로 직접 지정할 수 있습니다.
- `jsAssets`: ECharts 본체 및 플러그인 경로가 포함됩니다.
- `jsCodeAssets`: 해당 결과 데이터를 렌더링하기 위한 Machbase Neo에서 생성한 자바스크립트입니다.

아래 HTML 예시는 위 JSON을 이용해 차트를 렌더링하는 방법을 보여 줍니다.

```html {linenos=table,hl_lines=[3,14,19,23],linenostart=1}
<html>
<body>
    <script src="/web/echarts/echarts.min.js"></script>
    <div id="chart_is_here"></div>
    <script>
        function loadJS(url) {
            var scriptElement = document.createElement('script');
            scriptElement.src = url;
            document.getElementsByTagName('body')[0].appendChild(scriptElement);
        }
    </script>
    <script>
        fetch("basic_line.tql", {
            headers: { "X-Tql-Output": "json" }
        }).then(function(rsp){
            return rsp.json()
        }).then(function(obj) {
            const chartDiv = document.createElement('div')
            chartDiv.setAttribute("id", obj.chartID)
            chartDiv.style.width = obj.style.width
            chartDiv.style.height = obj.style.height
            document.getElementById('chart_is_here').appendChild(chartDiv)
            obj.jsCodeAssets.forEach((js) => loadJS(js))
        }).catch(function(err){
            console.log("chart fetch error", err)
        })
    </script>
</body>
</html>
```

- 3행: 응답의 `jsAssets`에 포함된 Apache ECharts 라이브러리를 미리 로드합니다.
- 14행: `X-Tql-Output: json` 헤더를 지정해 JSON 메타 정보를 요청합니다. 기본적으로 `GET` 요청 시 HTML 문서를 반환하지만, 이 헤더가 있으면 JSON을 돌려줍니다.
- 23행: 응답의 `jsCodeAssets` 목록을 순회하며 DOM에 동적으로 삽입합니다.

## 동적 TQL 호출

`/db/tql` 엔드포인트는 POST로 전달된 TQL 스크립트를 실행한 뒤 결과 자바스크립트를 제공합니다.  
아래 예시처럼 클라이언트 측에서 자바스크립트를 동적으로 로드할 수 있습니다. 20행에서 `chartID()`를 지정했고, 동일한 `id`를 가진 `<div>`를 미리 준비했습니다.

```html {linenos=table,hl_lines=[4,13,20,34],linenostart=1}
<html>
<body id="body">
    <script src="/web/echarts/echarts.min.js"></script>
    <div id="chart_is_here"></div>
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
                            series: [ { type: "line", data: column(1) } ]
                        })
                    )
            `}
        ).then(function(rsp){
            return rsp.json()
        }).then(function(obj) {
            const chartDiv = document.getElementById('chart_is_here')
            chartDiv.style.width = obj.style.width
            chartDiv.style.height = obj.style.height
            obj.jsCodeAssets.forEach((js) => loadJS(js))
        }).catch(function(err){
            console.log("chart fetch error", err)
        })
    </script>
</body>
</html>
```

## 로딩 순서 문제

위 예시에서 `jsAssets`와 `jsCodeAssets`를 동시에 `loadJS`로 처리하면 다음 코드처럼 순서 문제가 발생할 수 있습니다.

```js {linenos=table,linenostart=38}
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

`jsAssets`에 포함된 ECharts 라이브러리가 완전히 로드되기 전에 `jsCodeAssets`를 실행하려 하면 오류가 발생합니다. 이를 방지하려면 로드 완료 콜백을 활용해 순차적으로 불러와 주십시오.

```js {linenos=table,hl_lines=["5-9"],linenostart=6}
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

마지막 `jsAssets`가 로드된 뒤 `jsCodeAssets`를 불러오면 안전합니다.

```js {linenos=table,hl_lines=[4,"6-8"],linenostart=34}
for (let i = 0; i < obj.jsAssets.length; i++ ){
    if (i < obj.jsAssets.length -1){ 
        loadJS(obj.jsAssets[i])
    } else { // 마지막 자산이 로드되면 jsCodeAssets 로딩 시작
        loadJS(obj.jsAssets[i], () => {
            obj.jsCodeAssets.forEach(js => loadJS(js)) 
        })
    }
}
```
