---
title: Embed in HTML
type: docs
weight: 10
---

아래 코드를 `basic_map.tql`로 저장해 주십시오. 이 문서에서는 해당 *TQL* 결과를 웹 페이지에 임베드하는 방법을 설명합니다.

```js
SCRIPT({
    $.yield({
        type:"polygon",
        coordinates:[[37,-109.05],[41,-109.03],[41,-102.05],[37,-102.05]],
        properties: {
            fill: false
        }
    });
    $.yield({
        type: "marker",
        coordinates:[38.9934,-105.5018],
        properties: {
            popup:{content: Date()}
        }
    });
    $.yield({
        type: "circleMarker",
        coordinates:[38.935,-105.520],
        properties:{ radius: 40, fillOpacity:0.4, stroke: false }
    });
})
GEOMAP()
```

## IFRAME

```html {linenos=table,hl_lines=[3],linenostart=1}
<html>
<body>
    <iframe src="basic_map.tql" width="600" height="600"/>
</body>
</html>
```

## JSON 응답 활용

`X-Tql-Output: json` 헤더를 추가해 *.tql* 스크립트를 호출하면 기본 HTML 대신 JSON을 받을 수 있습니다.  
이를 통해 원하는 DOM 위치에 지도를 직접 삽입할 수 있습니다.  
`X-Tql-Output: json` 헤더는 `GEOMAP( geoMapJson(true) )` 옵션과 동일하게 동작합니다.

`/db/tql/basic_map.tql`이 JSON을 반환하면 다음과 같은 정보가 포함됩니다.

```json
{
    "geomapID":"MTcwMzE3NjYwMjA0Nzg1NjY0",
    "style": {
        "width": "600px",
        "height": "600px",
        "grayscale": 0
    },
    "jsAssets": ["/web/geomap/leaflet.js"],
    "cssAssets": ["/web/geomap/leaflet.css"],
    "jsCodeAssets": [
        "/web/api/tql-assets/MTcwMzE3NjYwMjA0Nzg1NjY0_opt.js",
        "/web/api/tql-assets/MTcwMzE3NjYwMjA0Nzg1NjY0.js"
    ]
}
```

- `geomapID`: 지도에 사용할 랜덤 ID. 필요 시 `geomapID()` 옵션으로 지정할 수 있습니다.
- `jsAssets`: Leaflet 라이브러리 및 플러그인 경로.
- `cssAssets`: Leaflet에 필요한 CSS 파일 목록.
- `jsCodeAssets`: 결과 데이터를 렌더링하는 데 필요한 자바스크립트.

아래 HTML 예시는 위 JSON을 이용해 지도를 렌더링하는 방법을 보여 줍니다.

```html {linenos=table,hl_lines=[3,6,17,22,26],linenostart=1}
<html>
<head>
    <link rel="stylesheet" href="/web/geomap/leaflet.css">
</head>
<body>
    <script src="/web/geomap/leaflet.js"></script>
    <div id="map_is_here"></div>
    <script>
        function loadJS(url) {
            var scriptElement = document.createElement('script');
            scriptElement.src = url;
            document.getElementsByTagName('body')[0].appendChild(scriptElement);
        }
    </script>
    <script>
        fetch("basic_map.tql", {
            headers: { "X-Tql-Output": "json" }
        }).then(function(rsp){
            return rsp.json()
        }).then(function(obj) {
            const mapDiv = document.createElement('div')
            mapDiv.setAttribute("id", obj.geomapID)
            mapDiv.style.width = obj.style.width
            mapDiv.style.height = obj.style.height
            document.getElementById('map_is_here').appendChild(mapDiv)
            obj.jsCodeAssets.forEach((js) => loadJS(js))
        }).catch(function(err){
            console.log("geomap fetch error", err)
        })
    </script>
</body>
</html>
```

- 3행: 응답 `cssAssets`에 포함된 Leaflet 스타일시트를 미리 로드합니다.
- 6행: `jsAssets`의 Leaflet 라이브러리를 미리 로드합니다.
- 17행: `X-Tql-Output: json` 헤더를 사용해 JSON 메타 정보를 요청합니다.
- 26행: 응답의 `jsCodeAssets`를 순차적으로 DOM에 추가합니다.

## 동적 TQL 호출

`/db/tql` 엔드포인트는 POST로 전달된 TQL 스크립트를 실행하고 결과 자바스크립트를 반환합니다.  
아래 예시처럼 클라이언트 측에서 동적으로 로드할 수 있습니다. 40행에서 `geomapID("map_is_here")`로 ID를 지정했고, 동일한 `id`를 가진 `<div>`를 준비했습니다.

```html {linenos=table,hl_lines=[3,6,16,40,47],linenostart=1}
<html>
<head>
    <link rel="stylesheet" href="/web/geomap/leaflet.css">
</head>
<body id="body">
    <script src="/web/geomap/leaflet.js"></script>
    <div id="map_is_here" style="width:100%; height:100%;"></div>
    <script>
        function loadJS(url) {
            var scriptElement = document.createElement('script');
            scriptElement.src = url;
            document.getElementsByTagName('body')[0].appendChild(scriptElement);
        }
    </script>
    <script>
        fetch("/db/tql", {
            method:"POST", 
            body:`
            SCRIPT({
                $.yield({
                    type:"polygon",
                    coordinates:[[37,-109.05],[41,-109.03],[41,-102.05],[37,-102.05]],
                    properties: {
                        fill: false
                    }
                });
                $.yield({
                    type: "marker",
                    coordinates:[38.9934,-105.5018],
                    properties: {
                        popup:{content: Date()}
                    }
                });
                $.yield({
                    type: "circleMarker",
                    coordinates:[38.935,-105.520],
                    properties:{ radius: 40, fillOpacity:0.4, stroke: false }
                });
            })
            GEOMAP( geomapID("map_is_here") )`
        }).then(function(rsp){
            return rsp.json()
        }).then(function(obj) {
            const mapDiv = document.getElementById('map_is_here')
            obj.jsCodeAssets.forEach((js) => loadJS(js))
        }).catch(function(err){
            console.log("geomap fetch error", err)
        })
    </script>
</body>
</html>
```

## 로딩 순서 문제

`jsAssets`와 `jsCodeAssets`를 동시에 로드하면 다음과 같은 코드에서 순서 문제가 발생할 수 있습니다.

```js {linenos=table,linenostart=38}
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

`jsAssets`에 포함된 Leaflet 라이브러리가 완료되기 전에 `jsCodeAssets`가 실행되면 오류가 날 수 있습니다.  
이를 방지하려면 로드 완료 콜백을 사용해 순차적으로 로드하십시오.

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

마지막 `jsAssets`가 로드된 후 `jsCodeAssets`를 불러오면 안전합니다.

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
