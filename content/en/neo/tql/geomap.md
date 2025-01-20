---
title: GEOMAP()
type: docs
weight: 51
draft: true
---

*Syntax*: `GEOMAP( [mapId()] [, tileTemplate()] [, size()] )` {{< neo_since ver="8.0.40" />}}

`GEOMAP` generates a map display and shows markers and geometric shapes based on provided coordinates.
It functions similarly to `CHART`, but it uses coordinates instead of scalar values.

### tileTemplate()

*Syntax*: `tileTemplate(url_template)`

The map tile server url template.
The default is `https://tile.openstreetmap.org/{z}/{x}/{y}.png`.

**Important :** If the map clients (web browsers) cannot access the default tile server 
you will need to run your own tile server inside your network 
and set the tile server URL using `tileTemplate()`. 
Instructions on how to run a tile server are beyond the scope of this document.

### mapId()

*Syntax*: `mapId(id)`

If you need to sepcify the map id (*string*) instead of auto-generated one.

### size()

*Syntax*: `size(width, height)`

- `width` *string* map width in HTML syntax ex) `'800px'`
- `height` *string* map height in HTML syntax ex) `'800px'`

The `GEOMAP()` function processes input data in JavaScript Object format. Each input object must include `type` and `value` fields, with an optional `option` field. The object are called "layer" in `GEOMAP()` function. The layers are rendered on the map according to its specified type. For example, a layer with the type `circle` will display a circle on the map based on the provided options.

## Layers

Layers are markers and geometric shapes that `GEOMAP` shows on the map.

### marker

```js {{linenos=table,hl_lines=["8-11"]}}
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018]
}))

SCRIPT("js", {
    var lat = $.values[1];
    var lon = $.values[2];
    $.yield({
        type: "marker",
        value: [lat, lon]
    });
})

GEOMAP()
```

{{< figure src="../img/geomap-marker.png" width="500" >}}

### circleMarker

**Options**

| Option          | Default          | Description   |
|:--------------- |:-----------------|:--------------|
| `radius`        | 10               | Radius of the circle marker, in pixels. |

```js {{linenos=table,hl_lines=["8-14"]}}
FAKE(json({
    ["Eleven Mile State Park", 38.935, -105.520]
}))

SCRIPT("js", {
    var lat = $.values[1];
    var lon = $.values[2];
    $.yield({
        type: "circleMarker",
        value: [lat, lon],
        option:{
            radius: 40
        }
    });
})

GEOMAP()
```

{{< figure src="../img/geomap-circlemarker.png" width="500" >}}

### circle

**Options**

| Option          | Default          | Description   |
|:--------------- |:-----------------|:--------------|
| `radius`        | 10               | Radius of the circle, in meters. |

```js {{linenos=table,hl_lines=["8-14"]}}
FAKE(json({
    ["Eleven Mile State Park", 38.935, -105.520]
}))

SCRIPT("js", {
    var lat = $.values[1];
    var lon = $.values[2];
    $.yield({
        type: "circle",
        value: [lat, lon],
        option:{
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
    ["line", 45.51, -122.68],
    ["line", 37.77, -122.43],
    ["line", 34.04, -118.2]
}))

SCRIPT("js", {
    var points = [];
    function finalize() {
        $.yield({
            type: "polyline",
            value: points
        });
    }
},{
    var lat = $.values[1];
    var lon = $.values[2];
    points.push( [lat, lon] );
})

GEOMAP()
```

{{< figure src="../img/geomap-polyline.png" width="500" >}}

### polygon

```js
FAKE(json({
    ["polygon", 37, -109.05],
    ["polygon", 41, -109.03],
    ["polygon", 41, -102.05],
    ["polygon", 37, -102.05]
}))

SCRIPT("js", {
    var points = [];
    function finalize() {
        $.yield({
            type: "polygon",
            value: points
        });
    }
},{
    var lat = $.values[1];
    var lon = $.values[2];
    points.push( [lat, lon] );
})

GEOMAP()
```

{{< figure src="../img/geomap-polygon.png" width="500" >}}

## Options

### Layer Options

| Option          | Type   | Default   | Description   |
|:--------------- |:-------|:----------|:--------------|
| `stroke`        | Boolean| true      | Whether to draw stroke along the path. Set it to false to disable borders on polygons or circles. |
| `color`         | String | '#3388ff' | Stroke color  |
| `weight`        | Number | 3         | Stroke width in pixels |
| `opacity`       | Number | `1.0`     | The opacity of the marker.|
| `fillColor`     | String |           | Fill color. Defaults to the value of the color option. |
| `fillOpacity`   | Number | 0.2       | Fill opacity. |
| `popup`         | Object | `null`    | See [Popup](#popup). |

### Popup

If layer option has `popup` object it displays popup message when user click the layer.

| Option          | Type   | Default    | Description   |
|:--------------- |:-------|:-----------|:--------------|
| `content`       | String |            | The content of the popup in HTML. |

```js {{linenos=table,hl_lines=["12-16"]}}
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018]
}))

SCRIPT("js", {
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        value: [lat, lon],
        option: {
            popup: {
                content: '<b>'+name+'</b>'
            }
        }
    });
})

GEOMAP()
```

{{< figure src="../img/geomap-marker-popup.png" width="500" >}}
