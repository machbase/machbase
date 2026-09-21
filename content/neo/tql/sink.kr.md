---
title: SINK
type: docs
weight: 21
---

모든 *tql* 스크립트는 반드시 하나의 싱크(SINK) 함수로 끝나야 합니다.

기본 싱크 함수는 입력 레코드를 Machbase Neo 데이터베이스에 저장하는 `INSERT()`입니다. `CHART()`는 입력 레코드를 다양한 차트로 렌더링하고, `JSON()`과 `CSV()`는 입력 데이터를 각각 JSON·CSV 형식으로 인코딩합니다.

![tql_sink](/neo/tql/img/tql_sink.jpg)

## INSERT()

*구문*: `INSERT( [bridge(),] columns..., table() [, tag()] )`

`INSERT()`는 입력 레코드마다 `INSERT` 문을 실행해 지정한 데이터베이스 테이블에 저장합니다.

- `bridge()` *bridge('name')*: 선택 옵션입니다.
- `columns` *string*: 컬럼 이름 목록입니다.
- `table()` *table('name')*: 대상 테이블 이름을 지정합니다.
- `tag()` *tag('name')*: 선택 옵션으로, 태그 테이블에만 사용할 수 있습니다.

{{< tabs >}}
{{< tab name="Example" >}}
태그 이름이 들어 있는 레코드를 Machbase에 기록합니다.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582790, 23.45],
    ["temperature", 1708582791, 24.56]
}))
MAPVALUE(1, value(1)*1000000000) // convert epoch sec to nanosec
INSERT("name", "time", "value", table("example"))
```
{{< /tab >}}
{{< tab name="PUSHVALUE()" >}}
`PUSHVALUE()`로 "name" 필드를 추가해 같은 태그 이름으로 레코드를 Machbase에 기록합니다.

```js {{linenos=table,hl_lines=[5,7]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
PUSHVALUE(0, "temperature")
MAPVALUE(1, value(1)*1000000000) // convert epoch sec to nanosec
INSERT("name","time", "value", table("example"))
```
{{< /tab >}}
{{< tab name="tag()" >}}
대상이 태그 테이블이면 `tag()` 옵션으로 모든 레코드를 같은 태그 이름으로 Machbase에 기록할 수 있습니다.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
MAPVALUE(0, value(0)*1000000000) // convert epoch sec to nanosec
INSERT("time", "value", table("example"), tag('temperature'))
```
{{< /tab >}}
{{< /tabs >}}

브리지로 연결한 외부 데이터베이스에 레코드를 삽입할 수도 있습니다.

```js {{linenos=table,hl_lines=[2]}}
INSERT(
    bridge("sqlite"),
    "company", "employee", "created_on", table("mem_example")
)
```

## APPEND()

*구문*: `APPEND( table() )`

`APPEND()`는 Machbase Neo의 append 메서드로 입력 레코드를 지정한 데이터베이스 테이블에 저장합니다.

- `table()` *table(string)*: 대상 테이블을 지정합니다.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582794, 12.34],
    ["temperature", 1708582795, 13.45]
}))
MAPVALUE(1, value(1)*1000000000 ) // convert epoch sec to nanosec
APPEND( table("example") )
```

## CSV()

*구문*: `CSV( [tz(), timeformat(), precision(), rownum(), heading(), delimiter(), nullValue(), binaryformat() ] )`

결과 레코드를 CSV 형식으로 출력합니다. 각 레코드의 값이 CSV 행의 필드가 됩니다.
데이터의 끝은 마지막에 연속된 개행 문자 두 개(`\n\n`)로 구분합니다.

예를 들어 레코드가 `{key: k, value:[v1,v2]}`라면 CSV 레코드 `v1,v2`를 생성합니다.

- `tz` *tz(name)*: 시간대, 기본값은 `tz('UTC')`입니다.
- `timeformat` *timeformat(string)*: `DATETIME` 필드의 출력 형식, 기본값은 `timeformat('ns')`입니다.
- `rownum` *rownum(boolean)*: 행 번호 컬럼을 추가합니다.
- `precision` *precision(int)*: 부동소수점 필드의 정밀도입니다. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환합니다.
- `heading` *heading(boolean)*: 첫 행에 필드 이름을 추가합니다.
- `delimiter` *delimiter(string)*: 기본값인 쉼표(`,`) 대신 사용할 필드 구분자를 지정합니다.
- `nullValue()`: `NULL` 값을 대체할 문자열을 지정합니다. 기본값은 `nullValue('NULL')`입니다. {{< neo_since ver="8.0.14" />}}
- `cache()`: 결과 데이터를 캐시합니다. 자세한 내용은 [결과 데이터 캐시](../reading/#cache-result-data)를 참고해 주십시오. {{< neo_since ver="8.0.43" />}}
- `binaryformat()` *binaryformat(string)*: BINARY 컬럼의 출력 형식을 지정합니다. `hex`, `base64`, `bytes`, `preview`를 지원합니다. {{< neo_since ver="8.5.2" />}}

{{< tabs >}}
{{< tab name="default" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
CSV()
```

```csv
1,10
2,20
3,30
```
{{< /tab >}}
{{< tab name="heading()" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true) )
```

```csv
x,x10
1,10
2,20
3,30
```
{{< /tab >}}
{{< tab name="delimiter()" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true), delimiter("|") )
```

```csv
x|x10
1|10
2|20
3|30
```
{{< /tab >}}
{{< tab name="nullValue()" >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
FAKE( json({ ["A", 123], ["B", null], ["C", 234] }) )
CSV( nullValue("***") )
```

```csv
A,123
B,***
C,234
```
{{< /tab >}}
{{< /tabs >}}

## JSON()

*구문*: `JSON( [transpose(), tz(), timeformat(), precision(), rownum(), rowsFlatten(), rowsArray(), binaryformat() ] )`

레코드의 값으로 JSON 결과를 생성합니다.

- `transpose` *transpose(boolean)*: 행과 열을 전치합니다. 대부분의 차트 라이브러리에서는 `transpose(true)`를 지정하는 편이 편리합니다.
- `tz` *tz(name)*: 시간대, 기본값은 `tz('UTC')`입니다.
- `timeformat` *timeformat(string)*: `DATETIME` 필드의 출력 형식, 기본값은 `timeformat('ns')`입니다.
- `rownum` *rownum(boolean)*: 행 번호 컬럼을 추가합니다.
- `precision` *precision(int)*: 부동소수점 필드의 정밀도입니다. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환합니다.
- `rowsFlatten` *rowsFlatten(boolean)*: JSON 객체의 *rows* 필드 배열 차원을 한 단계 줄입니다. `JSON()`에 `transpose(true)`와 `rowsFlatten(true)`를 함께 지정하면 `rowsFlatten(true)`는 무시되고 `transpose(true)`만 결과에 적용됩니다. {{< neo_since ver="8.0.12" />}}
- `rowsArray` *rowsArray(boolean)*: 각 레코드를 객체로 표현한 배열만 담은 JSON을 생성합니다. `rowsArray(true)`는 `transpose(true)`와 `rowsFlatten(true)`보다 우선합니다. {{< neo_since ver="8.0.12" />}}
- `cache()`: 결과 데이터를 캐시합니다. 자세한 내용은 [결과 데이터 캐시](../reading/#cache-result-data)를 참고해 주십시오. {{< neo_since ver="8.0.43" />}}
- `binaryformat()` *binaryformat(string)*: BINARY 컬럼의 출력 형식을 지정합니다. `hex`, `base64`, `bytes`, `preview`를 지원합니다. {{< neo_since ver="8.5.2" />}}

{{< tabs >}}
{{< tab name="default" >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
JSON()
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "column" ],
        "types": [ "double", "double" ],
        "rows": [ [ 1, 10 ], [ 2, 20 ], [ 3, 30 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "228.541µs"
}
```
{{< /tab >}}
{{< tab name="transpose()" >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( transpose(true) )
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "cols": [ [ 1, 2, 3 ], [ 10, 20, 30 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "121.375µs"
}
```
{{< /tab >}}
{{< tab name="rowsFlatten()" >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsFlatten(true) )
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "rows": [ 1, 10, 2, 20, 3, 30 ]
    },
    "success": true,
    "reason": "success",
    "elapse": "130.916µs"
}
```
{{< /tab >}}
{{< tab name="rowsArray()" >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsArray(true) )
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "rows": [ { "x": 1, "x10": 10 }, { "x": 2, "x10": 20 }, { "x": 3, "x10": 30 } ]
    },
    "success": true,
    "reason": "success",
    "elapse": "549.833µs"
}
```
{{< /tab >}}
{{< /tabs >}}

## NDJSON()

*구문*: `NDJSON( [tz(), timeformat(), rownum(), binaryformat()] )` {{< neo_since ver="8.0.33" />}}

레코드의 값으로 NDJSON 결과를 생성합니다.

NDJSON(Newline Delimited JSON)은 각 줄이 유효한 JSON 객체인 스트리밍용 JSON 데이터 형식입니다. JSON 객체를 한 번에 하나씩 처리할 수 있으므로 대용량 데이터셋이나 스트리밍 데이터를 처리할 때 유용합니다.
데이터의 끝은 마지막에 연속된 개행 문자 두 개(`\n\n`)로 구분합니다.

- `tz` *tz(name)*: 시간대, 기본값은 `tz('UTC')`입니다.
- `timeformat` *timeformat(string)*: `DATETIME` 필드의 출력 형식, 기본값은 `timeformat('ns')`입니다.
- `rownum` *rownum(boolean)*: 행 번호 컬럼을 추가합니다.
- `cache()`: 결과 데이터를 캐시합니다. 자세한 내용은 [결과 데이터 캐시](../reading/#cache-result-data)를 참고해 주십시오. {{< neo_since ver="8.0.43" />}}
- `binaryformat()` *binaryformat(string)*: BINARY 컬럼의 출력 형식을 지정합니다. `hex`, `base64`, `bytes`, `preview`를 지원합니다. {{< neo_since ver="8.5.2" />}}

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL(`select * from example where name = 'neo_load1' limit 3`)
NDJSON(timeformat('Default'), tz('local'), rownum(true))
```

```json
{"NAME":"neo_load1","ROWNUM":1,"TIME":"2024-09-06 14:46:19.852","VALUE":4.58}
{"NAME":"neo_load1","ROWNUM":2,"TIME":"2024-09-06 14:46:22.853","VALUE":4.69}
{"NAME":"neo_load1","ROWNUM":3,"TIME":"2024-09-06 14:46:25.852","VALUE":4.69}

```

## MARKDOWN()

마크다운 또는 HTML 형식의 표를 생성합니다.

*구문*: `MARKDOWN( [ options... ] )`

- `tz(string)`: 시간대, 기본값은 `tz('UTC')`입니다.
- `timeformat(string)`: `DATETIME` 필드의 출력 형식, 기본값은 `timeformat('ns')`입니다.
- `html(boolean)`: HTML 렌더러로 결과를 생성합니다. 기본값은 `false`입니다.
- `rownum(boolean)`: 행 번호 컬럼을 표시합니다.
- `precision` *precision(int)*: 부동소수점 필드의 정밀도입니다. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환합니다.
- `brief(boolean)`: 결과 행을 생략합니다. `brief(true)`는 `briefCount(5)`와 같습니다.
- `briefCount(limit int)`: 레코드 수가 지정한 한도를 넘으면 결과 행을 생략합니다. 한도가 `0`이면 생략하지 않습니다.
- `binaryformat()` *binaryformat(string)*: BINARY 컬럼의 출력 형식을 지정합니다. `hex`, `base64`, `bytes`, `preview`를 지원합니다. {{< neo_since ver="8.5.2" />}}

{{< tabs >}}
{{< tab name="default" >}}
```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN()
```

```
|column0 | column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| 30     | Third line |
| 40     | 4th line |
| 50     | The last is 5th |
```
{{< /tab >}}
{{< tab name="briefCount" >}}

```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2) )
```

```
|column0 | column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records
```
{{< /tab >}}
{{< tab name="html" >}}

```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2), html(true) )
```

|column0 | column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records

{{< /tab >}}
{{< /tabs >}}

## HTML()

*구문*: `HTML(templates...)` {{< neo_since ver="8.0.52" />}}

제공한 템플릿으로 HTML 문서를 생성합니다.

자세한 사용법과 예제는 [HTML](../html/) 문서를 참고해 주십시오.

## TEXT()

*구문*: `TEXT(templates...)` {{< neo_since ver="8.0.52" />}}

제공한 템플릿으로 텍스트 문서를 생성합니다.

`HTML()`과 비슷하게 동작하지만 데이터에 HTML 이스케이프를 적용하지 않습니다.

## DISCARD()

*구문*: `DISCARD()` {{< neo_since ver="8.0.7" />}}

`DISCARD()`는 이름 그대로 모든 레코드를 조용히 버리므로 아무것도 출력하지 않습니다.

```js {linenos=table,hl_lines=[8],linenostart=1}
FAKE( json({
    [ 1, "hello" ],
    [ 2, "world" ]
}))
WHEN( value(0) == 2, do( value(0), strToUpper(value(1)), {
    ARGS()
    WHEN( true, doLog("OUTPUT:", value(0), value(1)) )
    DISCARD()
}))
CSV()
```

## CHART()

*구문*: `CHART()` {{< neo_since ver="8.0.8" />}}

Apache ECharts로 차트를 생성합니다.

다양한 사용법은 [CHART() 예제](/neo/tql/chart/)를 참고해 주십시오.


<!-- ## 사용 중단

### CHART_LINE()

> **사용 중단**: CHART()를 대신 사용해 주십시오.

*구문*: `CHART_LINE()`

HTML 형식의 라인 차트를 생성합니다.

{{< tabs >}}
{{< tab name="CHART_LINE()" >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_LINE(
    size("600px", "400px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "line",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_line.jpg" width="500" >}}

### CHART_BAR()

> **사용 중단**: CHART()를 대신 사용해 주십시오.

*구문*: `CHART_BAR()`

HTML 형식의 막대 차트를 생성합니다.

{{< tabs >}}
{{< tab name="CHART_BAR()" >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_BAR(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "bar",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_bar.jpg" width="500" >}}

### CHART_SCATTER()

> **사용 중단**: CHART()를 대신 사용해 주십시오.

*구문*: `CHART_SCATTER()`

HTML 형식의 산점도 차트를 생성합니다.

{{< tabs >}}
{{< tab name="CHART_SCATTER()" >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_SCATTER(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "scatter",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_scatter.jpg" width="500" >}}

### CHART_LINE3D()

> **사용 중단**: CHART()를 대신 사용해 주십시오.

*구문*: `CHART_LINE3D()`

HTML 형식의 3D 라인 차트를 생성합니다.

{{< tabs >}}
{{< tab name="CHART_LINE3D()" >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_LINE3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=[10, "12-31"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "line3D",
        lineStyle: { "width": 2 },
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_line3d.jpg" width="500" >}}


### CHART_BAR3D()

> **사용 중단**: CHART()를 대신 사용해 주십시오.

*구문*: `CHART_BAR3D()`

HTML 형식의 3D 막대 차트를 생성합니다.

{{< tabs >}}
{{< tab name="CHART_BAR3D()" >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_BAR3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "bar3D",
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_bar3d.jpg" width="500" >}}

### CHART_SCATTER3D()

> **사용 중단**: CHART()를 대신 사용해 주십시오.

*구문*: `CHART_SCATTER3D()`

HTML 형식의 3D 산점도 차트를 생성합니다.

{{< tabs >}}
{{< tab name="CHART_SCATTER3D()" >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_SCATTER3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab name="CHART()" >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "scatter3D",
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/neo/tql/img/chart_scatter3d.jpg" width="500" >}}

### title()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `title(label)`

- `label` *string*

### subtitle()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `subtitle(label)`

- `label` *string*

### xAxis(), yAxis(), zAxis()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `xAxis(idx, label [, type])`

- `idx` *number* 축에 사용할 컬럼의 인덱스
- `label` *string* 축 레이블
- `type` *string* 축 타입. `'time'`과 `'value'`를 지정할 수 있으며, 지정하지 않으면 기본값은 `'value'`입니다.

> zAxis()는 3D 차트에서만 적용됩니다.

### dataZoom()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `dataZoom(type, minPercentage, maxPercentage)`

- `type` *string* "slider", "inside"
- `minPercentage` *number* 0 ~ 100
- `maxPercentage` *number* 0 ~ 100

> 2D 차트 전용입니다.

### opacity()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `opacity(alpha)`

- `alpha` *number* 0.0 ~ 1.0

> 3D 차트 전용입니다.

### autoRotate()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `autoRotate( [speed] )`

- `speed` *number* 초당 회전 각도(도/초), 기본값은 10입니다.

### gridSize()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `gridSize( width, height, depth )`

- `width` *number* 백분율(기본값: 100)
- `height` *number* 백분율(기본값: 100)
- `depth` *number* 백분율(기본값: 100)

> 3D 차트 전용입니다.

### seriesLabels()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `seriesLabels( label... )`

- `label` *string*

각 시리즈의 레이블 텍스트를 지정합니다.

### toolbox

#### toolboxSaveAsImage()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `toolboxSaveAsImage(filename)` {{< neo_since ver="8.0.4" />}}

- `filename` *string* 확장자를 포함한 파일 이름. 지원하는 확장자는 .png, .jpeg, .svg입니다.

차트를 이미지 파일로 저장하는 툴박스 버튼을 표시합니다.

#### toolboxDataZoom()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `toolboxDataZoom()` {{< neo_since ver="8.0.4" />}}

데이터 확대/축소용 툴박스 버튼을 표시합니다.

#### toolboxDataView()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `toolboxDataView()` {{< neo_since ver="8.0.4" />}}

원본 데이터를 보여 주는 툴박스 버튼을 표시합니다.

```js {linenos=table,hl_lines=["6-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '20ms')) )
CHART_LINE( 
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    size('400px', '300px'),
    toolboxSaveAsImage('image.png'),
    toolboxDataZoom(),
    toolboxDataView()
)
```

{{< figure src="/neo/tql/img/sink_chart_toolbox.jpg" width="500" >}}

### visualMap()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `visualMap(min, max)`

- `min` *number*
- `max` *number*

미리 정의된 기본 색상으로 내부에서 `visualMapColor()`를 호출합니다.

### visualMapColor()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `visualMapColor(min, max, colors...)` {{< neo_since ver="8.0.4" />}}

- `min` *number*
- `max` *number*
- `colors` *문자열 배열로 지정한 색상*

*예*

```js {linenos=table,hl_lines=["6-11"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '20ms')) )
CHART_LINE( 
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    visualMapColor(-2.0, 2.0, 
        "#a50026", "#d73027", "#f46d43", "#fdae61", "#e0f3f8", 
        "#abd9e9", "#74add1", "#4575b4", "#313695", "#313695", 
        "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#fdae61",
        "#f46d43", "#d73027", "#a50026"
    )
)
```

{{< figure src="/neo/tql/img/sink_chart_visualMapColor.jpg" width="500" >}}

### markArea()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `markArea(coord0, coord1 [, label [, color [, opacity]]])`

- `coord0` *any*: 영역이 시작하는 x 값
- `coord1` *any*: 영역이 끝나는 x 값
- `label` *string*: 제목
- `color` *string*: 영역 색상
- `opacity` *number*: 불투명도(0~1)

*예*

```js {linenos=table,hl_lines=["6-7"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markArea(time('now+1s'), time('now+2s'), 'Error', '#ff000033'),
    markArea(time('now+1.5s'), time('now+2.5s'), 'Marked', '#22ff0022')
 )
```

{{< figure src="/neo/tql/img/sink_chart_markarea.jpg" width="500" >}}

### markXAxis()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `markXAxis(coord, label)`

- `coord` *any*: 표시할 x 값
- `label` *string*: 제목

```js {linenos=table,hl_lines=[6],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markXAxis(time('now+1.5s'), 'NOW')
)
```

{{< figure src="/neo/tql/img/chart_marker_x.jpg" width="500" >}}

### markYAxis()

> **사용 중단**: CHART()에서 chartOption()을 대신 사용해 주십시오.

*구문*: `markYAxis(coord, label)`

- `coord` *any*: 표시할 y 값
- `label` *string*: 제목

```js {linenos=table,hl_lines=[6,7],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markYAxis(1.0, 'max'),
    markYAxis(-1.0, 'min')
)
```

{{< figure src="/neo/tql/img/chart_marker_y.jpg" width="500" >}} -->
