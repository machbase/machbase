---
title: "@jsh/spatial"
type: docs
weight: 70
---

{{< neo_since ver="8.0.52" />}}

## haversine()

`haversine()`은 두 위도·경도 좌표 간의 대권 거리를 계산합니다.
구 위에 놓인 두 지점의 거리(km 등)를 구할 때 사용하는 하버사인(Haversine) 공식을 적용합니다.

**사용 예시**

```js {linenos=table,hl_lines=[4],linenostart=1}
m = require("@jsh/spatial");
latLon1 = [45.04, 7.42];  // 이탈리아 토리노
latLon2 = [3.09, 101.42]; // 말레이시아 쿠알라룸푸르
distance = m.haversine({radius: 6371, coordinates:[latLon1, latLon2]})
console.log(distance.toFixed(0), "Km");

// 10078 Km
```
