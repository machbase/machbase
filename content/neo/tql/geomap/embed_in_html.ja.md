---
title: HTMLへの埋め込み
type: docs
weight: 10
toc: true
---

以下のコードを `basic_map.tql` として保存してください。この文書では、この *TQL* の結果をWebページに埋め込む方法を説明します。

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

## JSONレスポンスの利用 {#json-응답-활용}

`X-Tql-Output: json` ヘッダーを付けて *.tql* スクリプトを呼び出すと、既定のHTMLの代わりにJSONを取得できます。  
これにより、任意のDOM位置に地図を直接挿入できます。  
`X-Tql-Output: json` ヘッダーは、`GEOMAP( geoMapJson(true) )` オプションと同じように動作します。

`/db/tql/basic_map.tql` が返すJSONには、次の情報が含まれます。

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

- `geomapID`：地図に使用するランダムなID。必要に応じて `geomapID()` オプションで指定できます。
- `jsAssets`：Leafletライブラリとプラグインのパス。
- `cssAssets`：Leafletに必要なCSSファイルのリスト。
- `jsCodeAssets`：結果データの描画に必要なJavaScript。

以下のHTMLは、上記のJSONを使って地図を描画する例です。

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

- 3行目：レスポンスの `cssAssets` に含まれるLeafletスタイルシートを事前に読み込みます。
- 6行目：`jsAssets` のLeafletライブラリを事前に読み込みます。
- 17行目：`X-Tql-Output: json` ヘッダーでJSONメタ情報を要求します。
- 26行目：レスポンスの `jsCodeAssets` を順番にDOMに追加します。

## TQLの動的な呼び出し {#동적-tql-호출}

`/db/tql` エンドポイントは、POSTで渡されたTQLスクリプトを実行し、結果のJavaScriptを返します。  
以下の例のように、クライアント側で動的に読み込めます。40行目で `geomapID("map_is_here")` によりIDを指定し、同じ `id` を持つ `<div>` を用意しています。

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

## 読み込み順序の問題 {#로딩-순서-문제}

`jsAssets` と `jsCodeAssets` を同時に読み込むと、次のコードのように順序の問題が発生することがあります。

```js {linenos=table,linenostart=38}
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

`jsAssets` に含まれるLeafletライブラリの読み込み完了前に `jsCodeAssets` を実行すると、エラーが発生する場合があります。  
読み込み完了時のコールバックを使い、順番に読み込んでください。

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

最後の `jsAssets` を読み込んでから `jsCodeAssets` を読み込むと、この問題を防げます。

```js {linenos=table,hl_lines=[4,"6-8"],linenostart=34}
for (let i = 0; i < obj.jsAssets.length; i++ ){
    if (i < obj.jsAssets.length -1){ 
        loadJS(obj.jsAssets[i])
    } else { // 最後のアセットの読み込み後にjsCodeAssetsの読み込みを開始
        loadJS(obj.jsAssets[i], () => {
            obj.jsCodeAssets.forEach(js => loadJS(js)) 
        })
    }
}
```
