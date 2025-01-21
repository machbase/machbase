---
title: GEOMAP()
type: docs
weight: 51
draft: true
---

{{< neo_since ver="8.0.40" />}}

*Syntax*: `GEOMAP( [mapId()] [, tileTemplate()] [, size()] )` 

`GEOMAP` generates a map display and shows markers and geometric shapes based on provided coordinates.
It functions similarly to `CHART`, but it uses coordinates instead of scalar values.

The `GEOMAP()` function processes input data in JavaScript Object format.
Each input object must include `type` and `coordinates` fields, with an optional `properties` field.

A layer in the `GEOMAP()` function is an object that is rendered on the map according to its specified type.
For example, a layer with the type `circle` will display a circle on the map based on the provided properties.


### tileTemplate()

*Syntax*: `tileTemplate(url_template)`

The map tile server url template.
The default is `https://tile.openstreetmap.org/{z}/{x}/{y}.png`.

> **Important :** If the map clients (web browsers) cannot access the default tile server 
> due to the firewall and organization's security policy,
> you will need to run your own tile server inside your organization 
> and set the tile server URL using `tileTemplate()`. 
> Instructions on how to run a tile server are beyond the scope of this document.
> Please refer to the following for more information about the tile server:
> https://wiki.openstreetmap.org/wiki/Tile_servers

### mapId()

*Syntax*: `mapId(id)`

If you need to sepcify the map id (*string*) instead of auto-generated one.

### size()

*Syntax*: `size(width, height)`

- `width` *string* map width in HTML syntax ex) `'800px'`
- `height` *string* map height in HTML syntax ex) `'800px'`

## Layers

Layers are markers and geometric shapes that `GEOMAP` shows on the map.

### marker

```js {{linenos=table,hl_lines=["8-11"]}}
FAKE(json({
    [38.9934, -105.5018]
}))

SCRIPT("js", {
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "marker",
        coordinates: [lat, lon]
    });
})

GEOMAP()
```

{{< figure src="../img/geomap-marker.png" width="500" >}}

### circleMarker

**Properties**

| Property        | Default          | Description   |
|:--------------- |:-----------------|:--------------|
| `radius`        | 10               | Radius of the circle marker, in pixels. |

```js {{linenos=table,hl_lines=["8-14"]}}
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT("js", {
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

{{< figure src="../img/geomap-circlemarker.png" width="500" >}}

### circle

**Properties**

| Property        | Default          | Description   |
|:--------------- |:-----------------|:--------------|
| `radius`        | 10               | Radius of the circle, in meters. |

```js {{linenos=table,hl_lines=["8-14"]}}
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT("js", {
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

{{< figure src="../img/geomap-circle.png" width="500" >}}

### polyline

```js
FAKE(json({
    [45.51, -122.68],
    [37.77, -122.43],
    [34.04, -118.2]
}))

SCRIPT("js", {
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

{{< figure src="../img/geomap-polyline.png" width="500" >}}

### polygon

```js
FAKE(json({
    [37, -109.05],
    [41, -109.03],
    [41, -102.05],
    [37, -102.05]
}))

SCRIPT("js", {
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

{{< figure src="../img/geomap-polygon.png" width="500" >}}

## Properties

### Layer Properties

| Property         | Type   | Default   | Description   |
|:--------------- |:-------|:----------|:--------------|
| `stroke`        | Boolean| true      | Whether to draw stroke along the path. Set it to false to disable borders on polygons or circles. |
| `color`         | String | '#3388ff' | Stroke color  |
| `weight`        | Number | 3         | Stroke width in pixels |
| `opacity`       | Number | `1.0`     | The opacity of the marker.|
| `fillColor`     | String |           | Fill color. Defaults to the value of the color property. |
| `fillOpacity`   | Number | 0.2       | Fill opacity. |
| `popup`         | Object | `null`    | See [Popup](#popup). |

### Popup

If layer properties has `popup` object it displays popup message when user click the layer.

| Property         | Type   | Default    | Description   |
|:--------------- |:-------|:-----------|:--------------|
| `content`       | String |            | The content of the popup in HTML. |

```js {{linenos=table,hl_lines=["13-17"]}}
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))

SCRIPT("js", {
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

{{< figure src="../img/geomap-marker-popup.png" width="500" >}}

<!--
## GeoJSON

### FeatureCollection

```js
SCRIPT("js", {
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

{{< figure src="../img/geomap-geojson-collection.png" width="500" >}}

### Feature

```js
SCRIPT("js", {
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

{{< figure src="../img/geomap-geojson-collection.png" width="500" >}}

-->