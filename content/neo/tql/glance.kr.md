---
title: TQL 한눈에 보기
type: docs
weight: 01
---

Machbase Neo는 Transforming Query Language(TQL)와 이를 실행할 수 있는 API를 제공합니다.

일반적인 애플리케이션 개발 과정에서는 데이터베이스에서 조회한 테이블 형태의 결과를 원하는 데이터 구조로 변환하고, 가공한 뒤 JSON·CSV·차트 등으로 출력합니다.  
TQL을 사용하면 이러한 과정을 몇 줄의 스크립트로 간단히 처리할 수 있으며, 작성한 TQL은 HTTP 엔드포인트로 노출해 API처럼 호출할 수도 있습니다.

## TQL이란?

TQL(Transforming Query Language)은 데이터 변환을 위한 DSL입니다.  
데이터 스트림의 흐름을 정의하며, 각 데이터 단위(레코드)는 *key*와 *value*로 구성됩니다.

- key : 보통 자동 증가하는 정수(쿼리 결과의 ROWNUM과 유사)
- value : 실제 데이터를 담고 있는 튜플

![tql_records](/neo/tql/img/tql_records.jpg)

TQL 스크립트는 데이터를 가져오는 *SRC* 함수로 시작하고, 변환 결과를 출력하는 *SINK* 함수로 끝납니다.  
중간에는 필요한 만큼 *MAP* 함수를 삽입해 데이터를 원하는 형태로 변형할 수 있습니다.

![tql_flow_min](/neo/tql/img/tql_flow_min.jpg)

![tql_flow](/neo/tql/img/tql_flow.jpg)

### SRC

- `SQL()` : Machbase Neo 또는 브리지로 연결한 외부 DB에 SQL을 실행해 레코드를 생성
- `FAKE()` : 테스트용 가상 데이터 생성
- `CSV()` : CSV 파일 읽기
- `BYTES()` : 파일 시스템/HTTP 요청/MQTT 페이로드에서 바이너리 데이터 읽기

![tql_src](/neo/tql/img/tql_src.jpg)

### SINK

- `INSERT()` : 레코드를 Machbase Neo 테이블에 기록
- `CHART()` : 레코드를 차트로 렌더링
- `JSON()`, `CSV()` : 데이터를 각각 JSON/CSV 형식으로 인코딩

![tql_sink](/neo/tql/img/tql_sink.jpg)

### MAP

*MAP* 함수는 데이터를 다른 형태로 바꾸는 핵심 도구입니다.  
수학 연산, 문자열 처리, 형식 변환, 외부 시스템 연동 등을 수행할 수 있습니다.

![tql_map](/neo/tql/img/tql_map.jpg)

## TQL 실행

{{% steps %}}

### 웹 UI 접속

브라우저에서 `http://127.0.0.1:5654/`로 접속한 뒤 계정(`sys` / `manager`)으로 로그인해 주십시오.

### 새 TQL 만들기

상단 “New...” 페이지에서 “TQL”을 선택해 주십시오.
{{< figure src="/images/web-tql-pick.png" width="550" >}}

### 예제 코드 실행

샘플 TQL 코드를 에디터에 붙여넣고, 좌측 상단의 ▶︎ 아이콘을 클릭해 주십시오.  
아래 예시는 주파수 1.5Hz, 진폭 1.0인 파형을 차트로 출력합니다.

{{% /steps %}}

{{< tabs items="SCATTER,LINE,BAR">}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER()
```
{{< figure src="/neo/tql/img/web-hello-tql-chart-scatter.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_LINE()
```
{{< figure src="/neo/tql/img/web-hello-tql-chart-line.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_BAR()
```
{{< figure src="/neo/tql/img/web-hello-tql-chart-bar.jpg" width="500" >}}
{{< /tab >}}
{{< /tabs >}}

## 다양한 출력 형식

- **CSV** : 스프레드시트 등 CSV 파일을 읽는 도구와 연동하기에 좋습니다.
- **JSON** : 웹 애플리케이션·API와 연계하기 쉽게 구조화되어 있습니다.

TQL로 간단히 포맷을 변경할 수 있습니다.

{{< tabs items="JSON-rows,JSON-cols,CSV,MARKDOWN,HTML">}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON()
```
{{< figure src="/neo/tql/img/web-hello-tql-json.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON(transpose(true))
```
{{< figure src="/neo/tql/img/web-hello-tql-json-transpose.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CSV()
```
{{< figure src="/neo/tql/img/web-hello-tql-csv.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN()
```
{{< figure src="/neo/tql/img/web-hello-tql-markdown.jpg" width="500" >}}
{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN(html(true))
```
{{< figure src="/neo/tql/img/web-hello-tql-markdown-html.jpg" width="500" >}}
{{< /tab >}}
{{< /tabs >}}

## API로 활용하기

상단 우측 저장 아이콘을 눌러 코드를 `hello.tql`로 저장해 주십시오.  
이후 [http://127.0.0.1:5654/db/tql/hello.tql](http://127.0.0.1:5654/db/tql/hello.tql)로 접근하거나, `curl`로 호출해 데이터를 받을 수 있습니다.

| 아이콘 | 설명 |
|--------|:-----|
| {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}} | 스크립트를 저장하면 우측 상단에 링크 아이콘이 표시됩니다. 클릭하면 스크립트 주소를 복사할 수 있습니다. |

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...
< HTTP/1.1 200 OK
< Content-Type: text/csv
<
1686787739025518000,-0.238191
1686787739035518000,-0.328532
...
```

### JSON()으로 변경

`CSV()`를 `JSON()`으로 바꾼 뒤 저장하고 다시 호출하면 JSON 형식으로 결과를 받을 수 있습니다.

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```
