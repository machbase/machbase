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

{{< tabs >}}
{{< tab name="default" >}}

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
{{< tab name="delimiter()" >}}

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

{{< tabs >}}
{{< tab name="default" >}}

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
{{< tab name="transpose()" >}}

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
{{< tab name="rowsFlatten()" >}}

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
{{< tab name="rowsArray()" >}}

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

{{< tabs >}}
{{< tab name="default" >}}

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
{{< tab name="html()" >}}

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

<a id="chart-with-chartjson"></a>
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

이 방식은 DOM 문서에 `<div id='myChart'></div>`가 있을 때 유용합니다.

```html
... in HTML ...
<div id='myChart'></div>
<script>
    fetch('http://127.0.0.1:5654/db/tql/output-chart.tql').then( function(rsp) {
        return rsp.json();
    }).then( function(c) {
        c.jsAssets.concat(c.jsCodeAssets).forEach((src) => {
            const sScript = document.createElement('script');
            sScript.src = src;
            sScript.type = 'text/javascript';
            document.getElementsByTagName('head')[0].appendChild(sScript);
        })
    })
</script>
... omit ...
```

<a id="cache-result-data"></a>
## 결과 데이터 캐시

{{< neo_since ver="8.0.43" />}}

아래와 같이 `CSV()`, `JSON()`, `NDJSON()`, `HTML()` 싱크에 `cache()` 옵션 함수를 지정할 수 있습니다.

```js
SQL( "select * from example limit ?, 1000",  param("offset") ?? 0 )
JSON( cache( param("offset") ?? "0", "60s" ) )
```

`cache()` 옵션은 필수 파라미터 `CACHE_KEY`, `TTL`과 선택 파라미터 `r`을 받습니다.

**구문**: `cache(CACHE_KEY string, TTL string, [r float])`

1. 첫 번째 파라미터 `CACHE_KEY`는 캐시 데이터를 등록하고 검색하는 데 사용하며, 실제 키는
   `[filename] + [source_code_hash] + [CACHE_KEY]`로 구성됩니다.
   따라서 같은 TQL(같은 파일 이름과 같은 코드)을 같은 `CACHE_KEY`로 실행하면 키가 같아지고,
   나중에 실행한 결과가 기존 캐시 데이터를 덮어씁니다.
2. 두 번째 파라미터 `TTL`이 지나면 캐시가 자동으로 삭제됩니다.
   TTL이 지난 뒤 들어온 요청은 실제 DB를 조회해 결과 데이터를 반환하고,
   그 결과를 다시 캐시에 등록합니다.
3. 세 번째 선택 파라미터 `r`은 "선제적 캐시 갱신 비율(preemptive-cache-update-ratio)"이며,
   0보다 크고 1.0보다 작은 값이어야 합니다.
   `r * TTL`과 `TTL` 사이에 들어온 첫 번째 요청에는
   현재 캐시 데이터로 응답한 뒤 쿼리를 실행해 캐시를 갱신합니다.
   이후 요청은 갱신된 결과를 캐시에서 받습니다.
   이를 통해 자주 요청되는 `CACHE_KEY`의 캐시 데이터를 백그라운드에서 계속 갱신할 수 있습니다.

코드를 수정하면 `source_code_hash`가 바뀌므로 캐시 미스가 발생합니다.
`TTL`이 지나 캐시가 자동으로 삭제된 경우에도 캐시 미스가 발생합니다.
두 경우 모두 요청을 실행하고, 그 결과 데이터를 캐시에 등록합니다.

이 동작은 SINK 함수에 `cache()` 옵션을 지정한 경우에만 적용됩니다.
`cache()` 옵션이 없는 TQL은 캐시를 검색하지 않습니다.

> 참고: 캐시를 과도하게 사용하면 메모리가 부족해질 수 있습니다.
> 예를 들어 수십억 건의 레코드를 SELECT하는 TQL에서 `cache()`를 사용하는 경우입니다.
