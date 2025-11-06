---
title: As Reading API
type: docs
weight: 05
---

{{< callout type="info" >}}
예제를 실행하려면 아래 SQL을 먼저 실행해 테이블과 데이터를 준비해 주십시오.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
VALUE DOUBLE SUMMARIZED);

INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 11);
```

TQL 스크립트를 저장하면 편집기 우측 상단에 <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> 아이콘이 표시됩니다. 클릭하면 스크립트 주소를 복사할 수 있습니다.

## CSV

{{< tabs items="default,delimiter()" >}}
{{< tab >}}
아래 코드를 `output-csv.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
CSV()
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```
{{< /tab >}}
{{< tab >}}
아래 코드를 `output-csv.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
CSV( delimiter("|") )
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0|1628694000000000000|10
TAG0|1628780400000000000|11
```
{{< /tab >}}
{{< /tabs >}}

## JSON

{{< tabs items="default,transpose(),rowsFlatten(),rowsArray()" >}}
{{< tab >}}
아래 코드를 `output-json.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON()
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-8"]}
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "rows": [
            [ "TAG0", 1628694000000000000, 10 ],
            [ "TAG0", 1628780400000000000, 11 ]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "770.078µs"
}
```
{{< /tab >}}
{{< tab >}}
아래 코드를 `output-json.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( transpose(true) )
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-9"]}
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "cols": [
            [ "TAG0", "TAG0" ],
            [ 1628694000000000000, 1628780400000000000 ],
            [ 10, 11 ]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```
{{< /tab >}}
{{< tab >}}
아래 코드를 `output-json.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( rowsFlatten(true) )
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-8"]}
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "rows": [
            "TAG0", 1628694000000000000, 10,
            "TAG0", 1628780400000000000, 11
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```
{{< /tab >}}
{{< tab >}}
아래 코드를 `output-json.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( rowsArray(true) )
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-8"]}
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "rows": [
            { "NAME": "TAG0", "TIME": 1628694000000000000, "VALUE": 10 },
            { "NAME": "TAG0", "TIME": 1628780400000000000, "VALUE": 11 }
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```
{{< /tab >}}
{{< /tabs >}}

## NDJSON

아래 코드를 `output-ndjson.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
NDJSON( )
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-ndjson.tql
```

```json {hl_lines=["5-8"]}
{ "NAME": "TAG0", "TIME": 1628694000000000000, "VALUE": 10 }↵
{ "NAME": "TAG0", "TIME": 1628780400000000000, "VALUE": 11 }↵
↵
```

## MARKDOWN

{{< tabs items="default,html()">}}
{{< tab >}}
아래 코드를 `output-markdown.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
MARKDOWN()
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

```
|NAME|TIME|VALUE|
|:-----|:-----|:-----|
|TAG0|1628694000000000000|10.000000|
|TAG0|1628780400000000000|11.000000|
```
{{< /tab >}}
{{< tab >}}
아래 코드를 `output-markdown.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
MARKDOWN( html(true) )
```

*curl* 명령으로 TQL을 호출해 주십시오.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

```html
<div>
<table>
<thead>
    <tr><th align="left">NAME</th><th align="left">TIME</th><th align="left">VALUE</th></tr>
</thead>
<tbody>
    <tr><td align="left">TAG0</td><td align="left">1628694000000000000</td><td align="left">10.000000</td></tr>
    <tr><td align="left">TAG0</td><td align="left">1628780400000000000</td><td align="left">11.000000</td>
    </tr>
</tbody>
</table>
</div>
```
{{< /tab >}}
{{< /tabs >}}

## HTML

`HTML()` 함수는 제공된 템플릿 언어를 활용해 결과를 HTML 문서로 출력합니다.  
쿼리 결과에 맞춰 HTML 구조와 스타일을 자유롭게 구성하실 수 있습니다.

`{{ .V.column_name }}`처럼 컬럼 값을 읽거나, `{{ if .IsFirst }}`, `{{ if .IsLast }}` 조건을 이용해 첫 행과 마지막 행에 맞춘 템플릿 제어가 가능합니다. 이를 활용하면 표, 보고서 등 다양한 HTML 표현을 TQL 스크립트만으로 생성할 수 있습니다.

```html {linenos=table,hl_lines=["10-14"]}
SQL(`select name, time, value from example limit 5`)
HTML({
{{ if .IsFirst }}
    <html>
    <body>
        <h2>HTML Template Example</h2>
        <hr>
        <table>
{{ end }}
    <tr>
        <td>{{ .V.name }}</td>
        <td>{{ .V.time }}</td>
        <td>{{ .V.value }}</td>
    </tr>
{{ if .IsLast }}
    </table>
        <hr>
        Total: {{ .Num }}
    </body>
    </html>
{{ end }}
})
```

{{< figure src="/neo/tql/img/html_template_2.jpg" width="518" >}}

## CHART

**TQL 파일 저장**

아래 코드를 `output-chart.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[4,6],linenostart=1}
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

**HTTP GET**

웹 브라우저에서 `http://127.0.0.1:5654/db/tql/output-chart.tql` 주소를 열어 주십시오.

{{< figure src="/neo/tql/img/reading-chart-bar.jpg" width="500" >}}

> 기존 `CHART_LINE()`, `CHART_BAR()`, `CHART_SCATTER()` 계열 함수는 새로운 `CHART()` 함수로 대체되었습니다.  
> 예시는 [CHART()](/neo/tql/chart) 문서를 참고해 주십시오.

### chartJson() 활용

**TQL 파일 저장**

아래 코드를 `output-chart.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[3],linenostart=1}
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartJson(true),
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

**HTTP GET**

웹 브라우저에서 `http://127.0.0.1:5654/db/tql/output-chart.tql` 주소를 열어 주십시오.

```json
{
  "chartID":"MzM3NjYzNjg5MTYxNjQ2MDg_", 
  "jsAssets": ["/web/echarts/echarts.min.js"],
  "jsCodeAssets": ["/web/api/tql-assets/MzM3NjYzNjg5MTYxNjQ2MDg_.js"],
  "style": {
      "width": "600px",
      "height": "600px"	
  },
  "theme": "white"
}
```

### chartID() 활용

**TQL 파일 저장**

아래 코드를 `output-chart.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=[3],linenostart=1}
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartID("myChart"),
    chartJson(true),
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

**HTTP GET**

웹 브라우저에서 `http://127.0.0.1:5654/db/tql/output-chart.tql` 주소를 열어 주십시오.

```json
{
  "chartID":"myChart", 
  "jsAssets": ["/web/echarts/echarts.min.js"],
  "jsCodeAssets": ["/web/api/tql-assets/myChart.js"],
  "style": {
      "width": "600px",
      "height": "600px"	
  },
  "theme": "white"
}
```
