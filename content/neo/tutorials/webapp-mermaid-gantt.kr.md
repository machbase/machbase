---
title: mermaid.js 간트 차트
type: docs
weight: 33
---

이 예시는 mermaid.js 라이브러리를 활용해 간트 차트를 표현하는 방법을 보여 줍니다.

{{< figure src="/neo/tutorials/img/gantt-webapp-1.jpg" width="600px" >}}

- 7행: `class="mermaid"`를 가진 `<div>`를 렌더링 영역으로 사용합니다.
- 28행: 각 상태의 첫 번째·마지막 레코드를 추출하는 `FILTER_CHANGED()` {{< neo_since ver="8.0.15" />}}를 사용합니다.
- 46~48행: mermaid 스크립트를 추가합니다.
- 56행: `startOnLoad:false` 옵션으로 mermaid.js를 로드합니다.

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
