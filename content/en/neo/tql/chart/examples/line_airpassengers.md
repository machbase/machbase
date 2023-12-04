---
title: Air Passengers
type: docs
weight: 920
---

```js
CSV (file("https://machbase.com/assets/example/AirPassengers.csv"))

// drop header : rownames,time,value
DROP(1) 
// drop rownames column
POPVALUE(0)

// year float to "year/month"
MAPVALUE(0,
    strSprintf("%.f/%.f",
        floor(parseFloat(value(0))),
        1+round(12 * (mod(round(parseFloat(value(0))*100), 100)/100)) 
    )
)
// passengers
MAPVALUE(1, parseFloat(value(1)))

CHART(
    theme("dark"),
    series(
        {"type": "category"},
        {"type": "line", "name": "passengers", "smooth": false}
    )
)
```

![basic_line](../../img/line_airpassengers.jpg)