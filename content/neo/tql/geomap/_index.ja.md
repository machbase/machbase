---
title: GEOMAP()
type: docs
weight: 51
toc: true
---

{{< neo_since ver="8.0.44" />}}

*構文*: `GEOMAP( [geomapID()] [, tileTemplate()] [, size()] )`

`GEOMAP` は、指定した座標に基づいて地図上にマーカーと図形を描画します。  
`CHART` と似ていますが、スカラー値の代わりに座標を使用します。対応する座標系は [WGS84](https://en.wikipedia.org/wiki/World_Geodetic_System) です。

入力データはJavaScriptオブジェクトで指定します。各オブジェクトには `type` と `coordinates` フィールドが必須で、`properties` は省略可能です。  
`type` に応じたレイヤーを地図上に描画します。たとえば `type: "circle"` は、指定した座標に円を表示します。

### tileTemplate()

*構文*: `tileTemplate(url_template)`

タイルサーバーのURLテンプレートを指定します。既定値は `https://tile.openstreetmap.org/{z}/{x}/{y}.png` です。

> **重要：** 社内のファイアウォールやセキュリティポリシーによって既定のタイルサーバーにアクセスできない場合は、内部にタイルサーバーを構築し、`tileTemplate()` でURLを設定してください。  
> タイルサーバーの構築方法はこの文書の対象外です。詳細は https://wiki.openstreetmap.org/wiki/Tile_servers を参照してください。

### tileGrayscale()

*構文*: `tileGrayscale(scale)`

- `scale` *float*：タイル画像をグレースケールで表示する際の値（0 ≤ scale ≤ 1.0、既定値は `0`）

### geomapID()

*構文*: `geomapID(id)`

自動生成されるIDの代わりに使用する地図のID（文字列）を指定します。

### size()

*構文*: `size(width, height)`

- `width` *string*：地図の幅（例：`'800px'`）
- `height` *string*：地図の高さ（例：`'600px'`）

## レイヤー {#레이어}

レイヤーは、地図上に表示するマーカーや図形です。  
`GEOMAP()` の入力はJavaScriptオブジェクトで表した辞書構造です。`type` と `coordinates` フィールドは必須で、`properties` は省略可能です。

**形式**

```js
{
    type: "circle", // marker、circleMarker、polylineなど
    coordinates: [Lat, Lon],
    properties: {
        radius: Radius,
        color: "#FF0000",
        weight: 1
    }
}
```

| 名前           | 型                     | 説明 |
|:---------------|:-------------------------|:-----|
| `type`         | `String`                 | レイヤーの種類（`marker`、`circle`、`circleMarker` など） |
| `coordinates`  | `[]Float`, `[][]Float`… | 緯度と経度の配列 |
| `properties`   | `Dictionary`            | レイヤーの種類に応じたオプション。[プロパティ](#properties)を参照 |

### marker

```js {{linenos=table,hl_lines=["8-11"]}}
FAKE(json({
    [38.9934, -105.5018]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "marker",
        coordinates: [lat, lon]
    });
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-marker.png" width="500" >}}

### circleMarker

**プロパティ**

| プロパティ           | 既定値 | 説明 |
|:---------------|:-------|:-----|
| `radius`       | 10     | ピクセル単位の半径 |

```js {{linenos=table,hl_lines=["8-14"]}}
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circleMarker",
        coordinates: [lat, lon],
        properties:{
            radius: 40
        }
    });
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-circlemarker.png" width="500" >}}

### circle

**プロパティ**

| プロパティ     | 既定値 | 説明 |
|:---------|:-------|:-----|
| `radius` | 10     | メートル単位の半径 |

```js {{linenos=table,hl_lines=["8-14"]}}
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circle",
        coordinates: [lat, lon],
        properties:{
            radius: 400
        }
    });
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-circle.png" width="500" >}}

### polyline

```js
FAKE(json({
    [45.51, -122.68],
    [37.77, -122.43],
    [34.04, -118.2]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polyline",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-polyline.png" width="500" >}}

### polygon

```js
FAKE(json({
    [37, -109.05],
    [41, -109.03],
    [41, -102.05],
    [37, -102.05]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polygon",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-polygon.png" width="500" >}}

## プロパティ {#properties}

### レイヤー共通のプロパティ {#레이어-공통-속성}

| プロパティ          | 型    | 既定値     | 説明 |
|:--------------|:--------|:-----------|:-----|
| `stroke`      | Boolean | `true`     | 輪郭線を描画するかどうか |
| `color`       | String  | `'#3388ff'`| 輪郭線の色 |
| `weight`      | Number  | `3`        | 輪郭線の太さ（px） |
| `opacity`     | Number  | `1.0`      | レイヤーの不透明度 |
| `fillColor`   | String  |            | 塗りつぶしの色（省略時は `color` と同じ） |
| `fillOpacity` | Number  | `0.2`      | 塗りつぶしの不透明度 |
| `popup`       | Object  | `null`     | [ポップアップ](#popup)を参照 |
| `tooltip`     | Object  | `null`     | [ツールチップ](#tooltip)を参照 |

### ポップアップ {#popup}

レイヤーの `properties` に `popup` オブジェクトを指定すると、クリック時にポップアップメッセージを表示します。

| プロパティ       | 型    | 既定値 | 説明 |
|:-----------|:--------|:-------|:-----|
| `content`  | String  |        | テキストまたはHTMLコンテンツ |
| `open`     | Boolean | `false`| 初期状態でポップアップを開くかどうか |
| `maxWidth` | Number  | `300`  | ポップアップの最大幅（px） |
| `minWidth` | Number  | `50`   | ポップアップの最小幅（px） |

```js {{linenos=table,hl_lines=["13-17"]}}
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))

SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            popup: {
                content: '<b>'+name+'</b>'
            }
        }
    });
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-marker-popup.png" width="500" >}}

### ツールチップ {#tooltip}

{{< neo_since ver="8.0.44" />}}

地図のレイヤー上に短いテキストを表示します。

| プロパティ        | 型    | 既定値 | 説明 |
|:------------|:--------|:-------|:-----|
| `content`   | String  |        | テキストまたはHTMLコンテンツ |
| `open`      | Boolean | `false`| 初期状態で表示するかどうか |
| `direction` | String  | `auto` | ツールチップの方向（`right`、`left`、`top`、`bottom`、`center`、`auto`） |
| `permanent` | Boolean | `false`| マウスオーバーなしで常に表示するかどうか |
| `opacity`   | Number  | `0.9`  | ツールチップの不透明度 |

```js {{linenos=table,hl_lines=["13-17"]}}
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))
SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            tooltip: {
                content: '<b>'+name+'</b>',
                direction: "auto",
                permanent: true
            }
        }
    });
})
GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-marker-tooltip.png" width="500" >}}

<!--
## GeoJSON

### FeatureCollection

```js
SCRIPT({
    $.yield({
        type: "FeatureCollection",
        features: [
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [102.0, 0.5]
                }
            },
            {
                type: "Feature",
                geometry: {
                    type: "LineString",
                    coordinates: [
                        [102.0, 0.0],[103.0, 1.0],[104.0, 0.0],[105.0, 1.0]
                    ]
                }
            },
            {
                type: "Feature",
                geometry: {
                    type: "Polygon",
                    coordinates: [
                        [
                            [100.0, 0.0],[101.0, 0.0],[101.0, 1.0],
                            [100.0, 1.0],[100.0, 0.0]
                        ]
                    ]
                }
            }
        ]
    });
})

GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-geojson-collection.png" width="500" >}}

### Feature

```js
SCRIPT({
    $.yield({
        type: "Feature",
        geometry: {
            type: "Point",
            coordinates: [102.0, 0.5]
        }
    });
    $.yield({
        type: "Feature",
        geometry: {
            type: "LineString",
            coordinates: [
                [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
            ]
        }
    })
    $.yield({
        type: "Feature",
        geometry: {
            type: "Polygon",
            coordinates: [
                [
                    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
                ]
            ]
        }
    });
})
GEOMAP()
```

{{< figure src="/neo/tql/img/geomap-geojson-collection.png" width="500" >}}

-->

## 例 {#예제}

CSVファイルからテストデータを読み込み、"TRIP" テーブルに挿入します。
このTQLは、指定したURLからCSVファイルをダウンロードし、
CSV文字列を適切なデータ型に変換してから、
TRIPテーブルにレコードを挿入します。

```js {{linenos=table,hl_lines=["6-12",30,35]}}
// CSV形式： TIME, LAT, LON
CSV(file("https://docs.machbase.com/assets/example/data-trajectory-firenze.csv"))
DROP(1) // ヘッダーを除外
SCRIPT({
    // tripテーブルがなければ作成
    $.db().exec("CREATE TAG TABLE IF NOT EXISTS TRIP ("+
        "name varchar(100) primary key, "+
        "time datetime basetime, "+
        "value double summarized, "+
        "lat double, "+
        "lon double "+
    ")")
    // CSV文字列 '23-04-21 16:53:21:123000' を時刻として解析
    function parseTime(str) { 
        y = "20"+str.substr(0,2);
        m = str.substr(3,2) - 1;
        d = str.substr(6,2);
        hours = str.substr(9, 2);
        mins = str.substr(12,2);
        secs = str.substr(15, 2);
        milli = str.substr(18, 3)
        var D = new Date(y, m, d, hours, mins, secs, milli);
        return (D.getFullYear() == y && D.getMonth() == m && D.getDate() == d) ? D : 'invalid date';
    }
}, {
    var ts = parseTime($.values[0]).getTime(); // エポックミリ秒
    var lat = parseFloat($.values[1]);
    var lon = parseFloat($.values[2]);
    // name、time、value、lat、lonを出力
    $.yield("firenze", ts, 0, lat, lon)
})
// エポック値をミリ秒からナノ秒に換算してdatetime型に変換
MAPVALUE(1, time(value(1)*1000000))
// tripテーブルに挿入
SQL(`INSERT INTO TRIP (name, time, value, lat, lon) values(?,?,?,?,?)`, 
    value(0), value(1), value(2), value(3), value(4))
```

### 軌跡 {#궤적}

{{< tabs >}}
{{< tab name="SQL" >}}
```js {{linenos=table,hl_lines=[5,7]}}
SQL(`SELECT time, lat, lon FROM TRIP
     WHERE name = 'firenze' ORDER BY time`)
SCRIPT({
    // 時刻をエポックナノ秒に変換してDate（JavaScript）を生成
    var timestamp = new Date($.values[0].unixNano()/1000000); 
    // coordinate [lat, lon]
    var coord = [$.values[1], $.values[2]]; 
    $.yield({
        type:"circle",
        coordinates: coord,
        properties: {
            radius: 15,
            tooltip: {
                content: ""+timestamp
            }
        }
    });
})
GEOMAP()
```
{{< /tab >}}
{{< tab name="CSV" >}}
```js {{linenos=table,hl_lines=["8-11"]}}
// CSV形式： TIME, LAT, LON
CSV(file("https://docs.machbase.com/assets/example/data-trajectory-firenze.csv"))

DROP(1) // ヘッダーを除外

SCRIPT({
    var timestamp = $.values[0];
    var coord = [
        parseFloat($.values[1]), 
        parseFloat($.values[2])
    ];
    $.yield({
        type:"circle",
        coordinates: coord,
        properties: {
            radius: 15,
            tooltip: {
                content: timestamp
            }
        }
    });
})

GEOMAP()
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/geomap/img/trajectory-firenze.png" width="600" >}}

### 距離と速度 {#거리와-속도}

ハバーサインの公式で2地点間の移動距離をメートル単位で計算し、
2地点の時刻差から移動速度を時速（km/h）で計算します。

{{< tabs >}}
{{< tab name="SQL" >}}
```js {{linenos=table,hl_lines=[7,"22-23",28]}}
SQL(`SELECT time, lat, lon FROM TRIP
     WHERE name = 'firenze' ORDER BY time`)
// 距離と速度を計算
SCRIPT({
    var EarthRadius = 6378137.0; // meters
    function degreesToRadians(d) { return d * Math.PI / 180; }
    function distance(p1, p2) {  // ハバーサインの公式による距離
        lat1 = degreesToRadians(p1[0]);
        lon1 = degreesToRadians(p1[1]);
        lat2 = degreesToRadians(p2[0]);
        lon2 = degreesToRadians(p2[1]);
        diffLat = lat2 - lat1;
        diffLon = lon2 - lon1;
        a = Math.pow(Math.sin(diffLat/2), 2) + Math.cos(lat1)*Math.cos(lat2)*Math.pow(Math.sin(diffLon/2), 2);
        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return c * EarthRadius;
    }
    var prevLoc, prevTs, dist;
},{
    var ts = $.values[0].unix(); // Unixエポック秒
    var coord = [$.values[1], $.values[2]];
    dist = prevLoc === undefined ? 0 : distance(prevLoc, coord);
    speed = prevTs === undefined ? 0 : dist*3.600 / (ts - prevTs);
    prevLoc = coord;
    prevTs = ts;
    $.yield({
        type:"circleMarker",
        coordinates: coord,
        properties: {
            radius: 4,
            tooltip: {
                content: "speed: "+speed.toFixed(0)+" KM/H<br/>"+
                         "dist: "+dist.toFixed(0)+" m",
            }
        }
    });
})
GEOMAP()
```
{{< /tab >}}
{{< tab name="CSV" >}}
```js {{linenos=table,hl_lines=["20-22",30,51,"45-46"]}}
// CSV形式： TIME("23-04-21 16:53:21:568000"), LAT, LON
CSV(file("https://docs.machbase.com/assets/example/data-trajectory-firenze.csv"))

// 先頭行のヘッダーを除外
DROP(1) 

// 文字列から時刻と座標を解析
SCRIPT({
    function parseTime(str) { // parse '23-04-21 16:53:21'
        y = str.substr(0,2)+2000;
        m = str.substr(3,2) - 1;
        d = str.substr(6,2);
        hours = str.substr(9, 2);
        mins = str.substr(12,2);
        secs = str.substr(15, 2);
        var D = new Date(y, m, d,hours, mins, secs);
        return (D.getFullYear() == y && D.getMonth() == m && D.getDate() == d) ? D : 'invalid date';
    }
},{ 
    var ts = parseTime($.values[0]).getTime()/1000; // エポック秒
    var lat = parseFloat($.values[1]);
    var lon = parseFloat($.values[2]);
    $.yield(ts, lat, lon);
})

// 距離と速度を計算
SCRIPT({
    var EarthRadius = 6378137.0; // meters
    function degreesToRadians(d) { return d * Math.PI / 180; }
    function distance(p1, p2) {  // ハバーサインの公式による距離
        lat1 = degreesToRadians(p1[0]);
        lon1 = degreesToRadians(p1[1]);
        lat2 = degreesToRadians(p2[0]);
        lon2 = degreesToRadians(p2[1]);
        diffLat = lat2 - lat1;
        diffLon = lon2 - lon1;
        a = Math.pow(Math.sin(diffLat/2), 2) + Math.cos(lat1)*Math.cos(lat2)*Math.pow(Math.sin(diffLon/2), 2);
        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return c * EarthRadius;
    }
    var prevLoc, prevTs, dist;
},{
    var ts = $.values[0];
    var coord = [$.values[1], $.values[2]];
    dist = prevLoc === undefined ? 0 : distance(prevLoc, coord);
    speed = prevTs === undefined ? 0 : dist*3.600 / (ts - prevTs);
    prevLoc = coord;
    prevTs = ts;
    $.yield({
        type:"circleMarker",
        coordinates: coord,
        properties: {
            radius: 4,
            tooltip: {
                content: "speed: "+speed.toFixed(0)+" KM/H<br/>"+
                         "dist: "+dist.toFixed(0)+" m",
            }
        }
    });
})
GEOMAP()
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/geomap/img/trajectory-firenze-speed.png" width="600" >}}
