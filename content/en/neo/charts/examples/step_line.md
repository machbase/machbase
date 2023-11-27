---
title: Stacked Line Chart
type: docs
weight: 60
---

```js
FAKE( json({
    ["Mon", 120, 220, 450],
    ["Tue", 132, 282, 432],
    ["Wed", 101, 201, 401],
    ["Thu", 134, 234, 454],
    ["Fri", 90,  290, 590],
    ["Sat", 230, 430, 530],
    ["Sun", 210, 410, 510]
}) )
CHART(
    toolboxSaveAsImage("step-line.jpg"),
    theme("dark"),
    global({
        "legend":{ "show":true },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": true
        }
    }),
    series(
        {"type": "category"},
        {"type": "line", "smooth":false, "step": "start", "name": "Step Start"},
        {"type": "line", "smooth":false, "step": "middle", "name": "Step Middle"},
        {"type": "line", "smooth":false, "step": "end", "name": "Step End"}
    )
)
```

![step_line](../../img/step_line.jpg)