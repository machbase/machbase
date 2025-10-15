---
title: SINK
type: docs
weight: 21
---

모든 *tql* 스크립트는 반드시 하나의 싱크(SINK) 함수로 끝나야 합니다.

기본적으로 `INSERT()`를 사용해 Machbase Neo 데이터베이스에 레코드를 저장할 수 있으며, `CHART()`는 입력 레코드를 다양한 차트로 렌더링합니다. `JSON()`과 `CSV()`는 데이터를 각각 JSON·CSV 형식으로 출력합니다.

![tql_sink](../img/tql_sink.jpg)

## INSERT()

*구문*: `INSERT( [bridge(),] columns..., table() [, tag()] )`

`INSERT()`는 들어오는 각 레코드를 지정한 테이블에 `INSERT` 문으로 저장합니다.

- `bridge()` *bridge('name')*: 선택 옵션입니다.
- `columns` *string*: 컬럼 이름 목록입니다.
- `table()` *table('name')*: 대상 테이블을 지정합니다.
- `tag()` *tag('name')*: 선택 옵션으로, 태그 테이블에만 사용할 수 있습니다.

{{<tabs items="Example,PUSHVALUE(),tag()">}}
{{<tab>}}
태그 이름을 포함한 레코드를 Machbase에 기록합니다.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582790, 23.45],
    ["temperature", 1708582791, 24.56]
}))
MAPVALUE(1, value(1)*1000000000) // 초 단위를 나노초로 변환
INSERT("name", "time", "value", table("example"))
```
{{< /tab >}}
{{<tab>}}
`PUSHVALUE()`로 `name` 필드를 추가해 동일한 태그 이름으로 기록합니다.

```js {{linenos=table,hl_lines=[5,7]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
PUSHVALUE(0, "temperature")
MAPVALUE(1, value(1)*1000000000) // 초 단위를 나노초로 변환
INSERT("name","time", "value", table("example"))
```
{{< /tab >}}
{{<tab>}}
대상 테이블이 태그 테이블이라면 `tag()` 옵션으로 태그 이름을 지정할 수 있습니다.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
MAPVALUE(0, value(0)*1000000000) // 초 단위를 나노초로 변환
INSERT("time", "value", table("example"), tag('temperature'))
```
{{< /tab >}}
{{< /tabs >}}

브리지를 통해 외부 데이터베이스에 삽입할 수도 있습니다.

```js {{linenos=table,hl_lines=[2]}}
INSERT(
    bridge("sqlite"),
    "company", "employee", "created_on", table("mem_example")
)
```

## APPEND()

*구문*: `APPEND( table() )`

`APPEND()`는 Machbase Neo의 append 메서드를 사용해 레코드를 저장합니다.

- `table()` *table(string)*: 대상 테이블을 지정합니다.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582794, 12.34],
    ["temperature", 1708582795, 13.45]
}))
MAPVALUE(1, value(1)*1000000000 ) // 초 단위를 나노초로 변환
APPEND( table("example") )
```

## CSV()

*구문*: `CSV( [tz(), timeformat(), precision(), rownum(), heading(), delimiter(), nullValue() ] )`

레코드를 CSV 형식으로 출력합니다. 각 레코드의 값이 CSV 행의 필드가 되며, 두 개의 연속 개행(`\n\n`)을 데이터 종료로 인식합니다.

예를 들어 레코드가 `{key: k, value:[v1,v2]}`라면 결과는 `v1,v2`입니다.

- `tz` *tz(name)*: 타임존, 기본값 `tz('UTC')`
- `timeformat` *timeformat(string)*: `DATETIME` 출력 형식, 기본값 `timeformat('ns')`
- `rownum` *rownum(boolean)*: 행 번호 컬럼 추가
- `precision` *precision(int)*: 부동소수점 정밀도. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환
- `heading` *heading(boolean)*: 첫 행에 컬럼 이름 포함
- `delimiter` *delimiter(string)*: 구분자 지정(기본값 `,`)
- `nullValue()` : `NULL` 값을 대체할 문자열(기본값 `nullValue('NULL')`) {{< neo_since ver="8.0.14" />}}
- `substituteNull` *substitute(string)*: 이전 버전 옵션(현재는 `nullValue()` 사용)
- `cache()` : 결과 데이터를 캐시합니다. {{< neo_since ver="8.0.43" />}}

{{< tabs items="default,heading(),delimiter(),nullValue()">}}
{{< tab >}}
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
{{< tab >}}
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
{{< tab >}}
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
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
FAKE( json({ ["A", 123], ["B", null], ["C", 234] }) )
CSV( nullValue("***") )
```
```csv
A|123
B|***
C|234
```
{{< /tab >}}
{{< /tabs >}}

## JSON()

*구문*: `JSON( [transpose(), tz(), timeformat(), precision(), rownum(), rowsFlatten(), rowsArray() ] )`

레코드를 JSON 형식으로 변환합니다.

- `transpose` *transpose(boolean)*: 행과 열을 전치합니다. 많은 차트 라이브러리에서 `transpose(true)`가 유용합니다.
- `tz` *tz(name)*: 타임존, 기본값 `tz('UTC')`
- `timeformat` *timeformat(string)*: `DATETIME` 출력 형식, 기본값 `timeformat('ns')`
- `rownum` *rownum(boolean)*: 행 번호 컬럼 추가
- `precision` *precision(int)*: 부동소수점 정밀도. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환
- `rowsFlatten` *rowsFlatten(boolean)*: `rows` 배열의 차원을 1단계 줄입니다. `transpose(true)`와 함께 사용하면 `rowsFlatten(true)`는 무시됩니다. {{< neo_since ver="8.0.12" />}}
- `rowsArray` *rowsArray(boolean)*: 각 레코드를 객체 배열로 반환합니다. `transpose(true)` 및 `rowsFlatten(true)`보다 우선합니다. {{< neo_since ver="8.0.12" />}}
- `cache()` : 결과 데이터를 캐시합니다. {{< neo_since ver="8.0.43" />}}

{{< tabs items="default,transpose(),rowsFlatten(),rowsArray()">}}
{{< tab >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
JSON()
```

```json {hl_lines=[5]}
{
    "data": {
        "columns": [ "x" ],
        "types": [ "double" ],
        "rows": [ [ 1, 10 ], [ 2, 20 ], [ 3, 30 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "228.541µs"
}
```
{{< /tab >}}
{{< tab >}}
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
    "elapse": "183.542µs"
}
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
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
    "elapse": "189.417µs"
}
```
{{< /tab >}}
{{< tab >}}
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
    "elapse": "197.201µs"
}
```
{{< /tab >}}
{{< /tabs >}}

## NDJSON()

*구문*: `NDJSON( [tz(), timeformat(), rownum()] )` {{< neo_since ver="8.0.33" />}}

레코드를 NDJSON(Newline Delimited JSON) 형식으로 변환합니다. NDJSON은 한 줄당 하나의 JSON 객체를 포함하므로 대용량 데이터나 스트리밍 처리에 유리합니다. 데이터의 끝은 두 개의 연속 개행(`\n\n`)으로 표시됩니다.

- `tz` *tz(name)*: 타임존, 기본값 `tz('UTC')`
- `timeformat` *timeformat(string)*: `DATETIME` 출력 형식, 기본값 `timeformat('ns')`
- `rownum` *rownum(boolean)*: 행 번호 컬럼 추가
- `cache()` : 결과 데이터를 캐시합니다. {{< neo_since ver="8.0.43" />}}

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

테이블을 마크다운 또는 HTML 형태로 생성합니다.

*구문*: `MARKDOWN( [ options... ] )`

- `tz(string)` 타임존, 기본값 `tz('UTC')`
- `timeformat(string)` `DATETIME` 출력 형식, 기본값 `timeformat('ns')`
- `html(boolean)` HTML 렌더러로 출력 여부(기본값 `false`)
- `rownum(boolean)` 행 번호 컬럼 표시
- `precision` *precision(int)*: 부동소수점 정밀도. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환
- `brief(boolean)` 결과 행 생략 여부. `brief(true)`는 `briefCount(5)`와 동일
- `briefCount(limit int)` 레코드 수가 제한을 넘으면 행을 생략합니다(0이면 생략 없음)

{{< tabs items="default,briefCount,html">}}
{{< tab >}}
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
{{< tab >}}

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
{{< tab >}}

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

제공한 템플릿을 활용해 HTML 문서를 생성합니다. 자세한 예시는 [HTML](../html/) 문서를 참고해 주십시오.

## TEXT()

*구문*: `TEXT(templates...)` {{< neo_since ver="8.0.52" />}}

제공한 템플릿을 활용해 텍스트 문서를 생성합니다. 데이터에 HTML 이스케이프를 적용하지 않는다는 점만 `HTML()`과 다릅니다.

## DISCARD()

*구문*: `DISCARD()` {{< neo_since ver="8.0.7" />}}

`DISCARD()`는 이름처럼 모든 레코드를 조용히 무시하므로 어떠한 출력도 생성하지 않습니다.

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
