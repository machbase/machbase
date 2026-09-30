---
title: TQL 한눈에 보기
type: docs
weight: 01
---

Machbase Neo는 Transforming Query Language(TQL)와 이를 실행할 수 있는 API를 제공합니다.

일반적인 애플리케이션 개발 과정에서는 데이터베이스에서 조회한 테이블 형태(행과 열)의 결과를 원하는 데이터 구조로 변환하고, 가공한 뒤 JSON·CSV·차트 등 필요한 형식으로 출력합니다.
TQL을 사용하면 이러한 과정을 몇 줄의 스크립트로 간단히 처리할 수 있으며, 작성한 TQL은 HTTP 엔드포인트로 노출해 다른 애플리케이션이 API처럼 호출할 수도 있습니다.

## TQL이란?

TQL(Transforming Query Language)은 데이터 변환을 위한 DSL입니다.
데이터 스트림의 흐름을 정의하며, 각 데이터 단위(레코드)는 *key*와 *value*로 구성됩니다.

- key : 보통 자동 증가하는 정수(쿼리 결과의 ROWNUM과 유사)
- value : 실제 데이터 필드를 담고 있는 튜플

![tql_records](/neo/tql/img/tql_records.jpg)

TQL 스크립트는 데이터를 가져와 레코드를 생성하는 *SRC* 함수로 시작하고, 레코드를 출력하는 *SINK* 함수로 끝납니다.
*SRC*와 *SINK* 사이에서는 필요에 따라 *MAP* 함수로 데이터를 변환할 수 있습니다.

![tql_flow_min](/neo/tql/img/tql_flow_min.jpg)

경우에 따라 TQL 스크립트는 수학 계산, 간단한 문자열 연결, 외부 데이터베이스 연동 등을 통해 레코드를 변환해야 합니다. 이러한 작업은 *MAP* 함수로 정의합니다.

따라서 TQL 스크립트는 *SRC* 함수로 시작해 *SINK* 함수로 끝나야 하며, 그 사이에 필요한 변환을 수행하는 *MAP* 함수를 0개 이상 넣을 수 있습니다.

![tql_flow](/neo/tql/img/tql_flow.jpg)

### SRC

TQL에서는 여러 SRC 함수를 사용할 수 있습니다.

- `SQL()` : Machbase Neo 또는 브리지로 연결한 외부 DB에 SQL을 실행해 레코드를 생성
- `FAKE()` : 테스트용 가상 데이터 생성
- `CSV()` : CSV 파일 읽기
- `BYTES()` : 파일 시스템, 클라이언트의 HTTP 요청, MQTT 페이로드에서 바이너리 데이터 읽기

![tql_src](/neo/tql/img/tql_src.jpg)

### SINK

- `INSERT()` : 레코드를 Machbase Neo 데이터베이스에 기록
- `CHART()` : 레코드를 차트로 렌더링
- `JSON()`, `CSV()` : 데이터를 각각 JSON/CSV 형식으로 인코딩해 다른 애플리케이션과 쉽게 연동하거나 보기 좋게 표시

![tql_sink](/neo/tql/img/tql_sink.jpg)

### MAP

*MAP* 함수는 데이터를 다른 형태로 바꾸는 핵심 도구입니다.
수학 연산, 문자열 처리, 형식 변환, 외부 시스템 연동 등을 수행할 수 있습니다.
*MAP* 함수를 사용하면 애플리케이션의 요구 사항에 맞게 데이터를 효율적으로 처리하고 형태를 바꿀 수 있습니다.

![tql_map](/neo/tql/img/tql_map.jpg)

## TQL 실행

{{% steps %}}

### 웹 UI 접속

브라우저에서 Machbase Neo 웹 UI(기본 주소 `http://127.0.0.1:5654/`)에 접속한 뒤 계정(`sys` / `manager`)으로 로그인해 주십시오.

### 새 TQL 만들기

`New...` 페이지에서 `TQL`을 선택해 주십시오.

{{< figure src="/images/web-tql-pick.png" width="550" >}}

### 예제 코드 실행

샘플 TQL 코드를 복사해 TQL 편집기에 붙여넣고, 편집기 좌측 상단의 ▶︎ 아이콘을 클릭해 주십시오.
아래 이미지처럼 주파수 1.5Hz, 진폭 1.0인 파형이 차트로 출력됩니다.

{{% /steps %}}

{{< tabs >}}
{{< tab name="SCATTER" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER()
```

{{< figure src="/neo/tql/img/web-hello-tql-chart-scatter.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="LINE" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_LINE()
```

{{< figure src="/neo/tql/img/web-hello-tql-chart-line.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="BAR" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_BAR()
```

{{< figure src="/neo/tql/img/web-hello-tql-chart-bar.jpg" width="500" >}}

{{< /tab >}}
{{< /tabs >}}

## 다양한 출력 형식

CSV, JSON 같은 데이터 형식을 살펴보겠습니다.

- **CSV** : 스프레드시트 등 CSV 파일을 지원하는 애플리케이션으로 데이터를 내보낼 때 유용합니다.
- **JSON** : 파싱이 쉽고 JavaScript와 연동하기 좋아 웹 애플리케이션과 API에 적합합니다.

TQL을 사용하면 몇 줄의 코드만으로 데이터를 이러한 형식으로 간단히 변환할 수 있습니다.

{{< tabs >}}
{{< tab name="JSON-rows" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON()
```

{{< figure src="/neo/tql/img/web-hello-tql-json.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="JSON-cols" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON(transpose(true))
```

{{< figure src="/neo/tql/img/web-hello-tql-json-transpose.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="CSV" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CSV()
```

{{< figure src="/neo/tql/img/web-hello-tql-csv.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="MARKDOWN" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN()
```

{{< figure src="/neo/tql/img/web-hello-tql-markdown.jpg" width="500" >}}

{{< /tab >}}
{{< tab name="HTML" >}}

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN(html(true))
```

{{< figure src="/neo/tql/img/web-hello-tql-markdown-html.jpg" width="500" >}}

{{< /tab >}}
{{< /tabs >}}

## API로 활용하기

편집기 우측 상단의 저장 아이콘을 눌러 코드를 `hello.tql`로 저장해 주십시오.
이후 웹 브라우저에서 [http://127.0.0.1:5654/db/tql/hello.tql](http://127.0.0.1:5654/db/tql/hello.tql)로 접근하거나, 터미널에서 `curl` 명령으로 호출해 데이터를 받을 수 있습니다.

| 아이콘 | 설명 |
|--------|:-----|
| {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}} | TQL 스크립트를 저장하면 편집기 우측 상단에 링크 아이콘이 표시됩니다. 클릭하면 스크립트 파일의 주소를 복사할 수 있습니다. |

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
>
< HTTP/1.1 200 OK
< Content-Type: text/csv; charset=utf-8
< Transfer-Encoding: chunked
<
1686787739025518000,-0.238191
1686787739035518000,-0.328532
1686787739045518000,-0.415960
1686787739055518000,-0.499692
1686787739065518000,-0.578992
...omit...
```

### JSON()으로 변경

`CSV()`를 `JSON()`으로 바꾼 뒤 저장하고 다시 실행해 주십시오.

{{< figure src="/images/web-hello-tql-json.jpg" width="500" >}}

터미널에서 `curl`로 `hello.tql`을 호출하면 JSON 형식으로 결과를 받을 수 있습니다.

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```

HTTP 헤더를 포함한 JSON 응답 예시입니다.

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
< HTTP/1.1 200 OK
< Content-Type: application/json
< Transfer-Encoding: chunked
<
{
"data": {
    "columns": [ "time", "value" ],
    "types": [ "datetime", "double" ],
    "rows": [
    [ 1686788907538618000, 0.9344920354538058 ],
    [ 1686788907548618000, 0.8968436523101743 ],
    ...omit...
},
"success": true,
"reason": "success",
"elapse": "956.291µs"
}
```

### transpose()를 적용한 JSON()

데이터 시각화 애플리케이션을 개발한다면 TQL의 JSON 출력이 결과를 행 대신 열 단위로 전치(transpose)할 수 있다는 점을 알아 두면 유용합니다.
`JSON(transpose(true))`를 적용해 다시 호출하면 결과 JSON에 `cols` 배열이 포함됩니다.

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
< HTTP/1.1 200 OK
< Content-Type: application/json
< Transfer-Encoding: chunked
<
{
"data": {
    "columns": [ "time", "value" ],
    "types": [ "datetime", "double" ],
    "cols": [
        [ 1686789517241103000, ...omit..., 1686789520231103000],
        [ -0.7638449771082523, ...omit..., 0.8211935584502427]
    ]
},
"success": true,
"reason": "success",
"elapse": "1.208166ms"
}
```

이 기능을 사용하면 다른 애플리케이션이 데이터에 접근할 수 있는 RESTful API를 가장 간단하게 만들 수 있습니다.

### INSERT

`CSV()`를 `INSERT("time", "value", table("example"), tag("temperature"))`로 바꾼 뒤 다시 실행해 주십시오.

{{< figure src="/images/web-tql-insert.png" width="500" >}}

### 테이블 조회

```js
SQL('select * from example limit 10')
CSV()
```

{{< figure src="/images/web-tql-select.png" width="500" >}}
