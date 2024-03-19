---
title: Gantt with mermaid.js
type: docs
weight: 33
---

This example shows how to utilize mermaid.js library for gantt diagram.

{{< figure src="../img/gantt-webapp-1.jpg" width="600px" >}}

- line 7, `<div>` with `class="mermaid"`.
- line 56, Embed mermaid.js library with `startOnLoad:false`.
- line 28, Use `FILTER_CHANGED()` {{< neo_since ver="8.0.15" />}} that extracts the first and last records of the each states.
- line 46-48, Append mermaid script.

```html {{linenos="table",hl_lines=[7,28,"46-48",56,57]}}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
    <div id=chart class="mermaid" style='width:800px;'></div>
    <script>
        function draw() {
            fetch('/db/tql', {
                method: "POST",
                body: `
                    FAKE(json({
                        ["Task-A", 1692329338, 1.0],
                        ["Task-A", 1692329339, 2.0],
                        ["Task-B", 1692329340, 3.0],
                        ["Task-B", 1692329341, 4.0],
                        ["Task-B", 1692329342, 5.0],
                        ["Task-B", 1692329343, 6.0],
                        ["Task-B", 1692329344, 7.0],
                        ["Task-B", 1692329345, 8.0],
                        ["Task-C", 1692329346, 9.0],
                        ["Task-D", 1692329347, 10],
                        ["Task-D", 1692329348, 11],
                        ["Task-D", 1692329349, 12]
                    }))
                    MAPVALUE(1, parseTime(value(1), "s"))
                    FILTER_CHANGED(value(0), useFirstWithLast(true))
                    GROUP(
                        by(value(0)),
                        first(timeUnix(value(1))),
                        last(timeUnix(value(1)) + 1)
                    )
                    MAPVALUE(1, parseTime(value(1), "s"))
                    MAPVALUE(2, parseTime(value(2), "s"))
                    MAPVALUE(2, timeUnix(value(2)) - timeUnix(value(1)))
                    JSON(timeformat("Default"), tz("Local"))`
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj) {
                let codes = Array(`gantt`)
                codes.push(`    title A Gantt Diagram`)
                codes.push(`    dateFormat YYYY-MM-DD HH:mm:ss`)
                codes.push(`    axisFormat %H:%M:%S`)
                codes.push(`    section Project`)
                obj.data.rows.forEach(rec =>{
                    codes.push(`         ${rec[0]} : task, ${rec[1]}, ${rec[2]}s`)
                })
                let element = document.querySelector("#chart");
                element.innerHTML = codes.join("\n")
                updateGantt()
            })
        }
    </script>
        <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: false });
        window.updateGantt = function() {
            mermaid.run();
        };
        draw();
    </script>
</body>
</html>
```