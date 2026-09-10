---
toc: true
title: "spatial"
type: docs
weight: 10
---

{{< neo_since ver="8.0.75" />}}

## haversine() {#haversine}

`haversine()`は、2つの緯度・経度座標間の大円距離を計算します。
球面上の2点間の距離（kmなど）を求めるハバーサイン（Haversine）の公式を使用します。

**使用例**

```js {linenos=table,linenostart=1}
m = require("mathx/spatial");
latLon1 = [45.04, 7.42];  // イタリアのトリノ
latLon2 = [3.09, 101.42]; // マレーシアのクアラルンプール
distance = m.haversine({radius: 6371, coordinates:[latLon1, latLon2]})
console.log(distance.toFixed(0), "Km");

// 10078 Km
```
