---
title: HTMLへの埋め込み
type: docs
weight: 10
toc: true
---

以下のコードを `basic_line.tql` として保存してください。この文書では、この *TQL* の結果をWebページに埋め込む方法を説明します。

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

## JSONレスポンスの利用 {#json-응답-활용}

TQLスクリプトの呼び出し時に `X-Tql-Output: json` ヘッダーを追加すると {{< neo_since ver="8.0.42" />}}、既定のHTMLの代わりにJSONを取得できます（従来の `X-Chart-Output` ヘッダーは非推奨です {{< neo_since ver="8.0.14" />}}）。  
このJSONにはチャートの描画に必要なJavaScriptのパスが含まれるため、任意のDOM位置に直接挿入できます。  
`X-Tql-Output: json` ヘッダーは、`CHART()` シンクで `chartJson(true)` オプションを使用する場合と同じです。例は[読み取りAPIとして使用](/neo/tql/reading/#chart-with-chartjson)を参照してください。

`/db/tql` がJSONを返す場合、必要なスクリプトのアドレスも含まれます。

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

- `chartID`: EChartsで使用するランダムなIDです。必要に応じて `chartID()` オプションで指定できます。
- `jsAssets`: ECharts本体とプラグインのパスを含みます。
- `jsCodeAssets`: 結果データの描画用にMachbase Neoが生成したJavaScriptです。

以下のHTMLは、上記のJSONを使ってチャートを描画する例です。

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

- 3行目：レスポンスの `jsAssets` に含まれるApache EChartsライブラリを事前に読み込みます。
- 14行目：`X-Tql-Output: json` ヘッダーを指定してJSONメタ情報を要求します。`GET` リクエストは既定でHTML文書を返しますが、このヘッダーを指定するとJSONを返します。
- 23行目：レスポンスの `jsCodeAssets` リストを走査し、DOMに動的に挿入します。

## TQLの動的な呼び出し {#동적-tql-호출}

`/db/tql` エンドポイントは、POSTで渡されたTQLスクリプトを実行し、結果のJavaScriptを返します。  
以下の例のように、クライアント側でJavaScriptを動的に読み込めます。20行目で `chartID()` を指定し、同じ `id` を持つ `<div>` をあらかじめ用意しています。

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

## 読み込み順序の問題 {#로딩-순서-문제}

上記の例で `jsAssets` と `jsCodeAssets` を同時に `loadJS` で処理すると、次のコードのように順序の問題が発生することがあります。

```js {linenos=table,linenostart=38}
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

`jsAssets` に含まれるEChartsライブラリの読み込みが完了する前に `jsCodeAssets` を実行すると、エラーが発生します。読み込み完了時のコールバックを使い、順番に読み込んでください。

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
