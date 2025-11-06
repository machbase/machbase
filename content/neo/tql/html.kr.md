---
title: HTML()
type: docs
weight: 50
---

`HTML()` 싱크는 제공된 템플릿 언어를 이용해 결과를 HTML 문서 또는 요소로 출력합니다.  
이를 통해 쿼리 결과에 맞춰 HTML 구조와 모양을 자유롭게 구성하실 수 있습니다.

*구문*: `HTML(templates...)` {{< neo_since ver="8.0.53" />}}

- `templates`: 하나 이상의 템플릿 문자열 또는 `file(path)` 참조입니다. 각 인자는 직접 작성한 템플릿 문자열이거나 `file(path)`로 외부 파일을 읽어 들일 수 있습니다. 템플릿 내용은 Go HTML 템플릿 언어를 사용합니다. 자세한 문법은 [template 문서](https://pkg.go.dev/html/template)를 참고해 주십시오.
- `cache()` : 결과 데이터를 캐시합니다. 자세한 내용은 [결과 데이터 캐시](../reading/#cache-result-data)를 참조해 주십시오.

템플릿 내부에서는 현재 레코드의 필드 값과 행 번호에 접근할 수 있는 값 객체를 사용할 수 있습니다.  
HTML 템플릿 컨텍스트에서 활용할 수 있는 필드와 속성은 다음과 같습니다.

## 메서드

- `{{ .Columns }}`
- `{{ .Column <idx>}}`
- `{{ .Values }}`
- `{{ .Value <idx> }}`
- `{{ .ValueHTMLAttr <idx> }}`
- `{{ .ValueCSS <idx> }}`
- `{{ .ValueJS <idx> }}`
- `{{ .ValueURL <idx> }}`
- `{{ .ValueString <idx> }}`
- `{{ .V.<field> }}`
- `{{ .Num }}`

## 함수

### `timeformat`

**구문**

```
{{ timeformat <format> <timezone> }}
```

**사용 예시**

```html {linenos=table,hl_lines=[6]}
SCRIPT({
    const { now } = require("@jsh/system");
    $.yield(now(), "Hello World");
})
HTML({
    <li>{{ $.Value 0 | timeformat "RFC3339" "UTC" }}
    <li>{{ $.Value 1 }}
})
```

```html
<li>2025-05-29T08:32:33Z
<li>Hello World
```

### `format`

**사용 예시**

```html {linenos=table,hl_lines=["5-6"]}
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li>{{ $.Value 0 | format "%.2f" }}
    <li>{{ $.Value 1 | format "Say: %s?" }}
})
```

```html
<li> 3.14
<li> Say: Hello World?
```

### `param`

```html {linenos=table,hl_lines=[5,6]}
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ param "prefix" }} {{ $.Value 0 }}
    <li> {{ param "prefix" }} {{ $.Value 1 }}
})
```

- `?param=Line` 파라미터를 포함해 TQL 스크립트를 호출해 주십시오.

```html
<li> Line 3.1415
<li> Line Hello World
```

### `paramDefault`

```html {linenos=table,hl_lines=[5,6]}
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ paramDefault "prefix1" "Line1" }} {{ $.Value 0 }}
    <li> {{ paramDefault "prefix2" "Line2" }} {{ $.Value 1 }}
})
```

```html
<li> Line1 3.1415
<li> Line2 Hello World
```

### `toLower`

```html {linenos=table,hl_lines=[6]}
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ $.Value 0 | format "%.2f" }}
    <li> {{ $.Value 1 | toLower | format "Say: %s?" }}
})
```

```html
<li> 3.14
<li> Say: hello world?
```

### `toUpper`

```html {linenos=table,hl_lines=[6]}
SCRIPT({
    $.yield(3.1415, "Hello World");
})
HTML({
    <li> {{ $.Value 0 | format "%.2f" }}
    <li> {{ $.Value 1 | toUpper | format "Say: %s?" }}
})
```

```html
<li> 3.14
<li> Say: HELLO WORLD?
```

## 활용 예시

{{< tabs items=".V,.Value,.Values">}}
{{< tab >}}

`.V`는 필드 이름을 키로 갖는 맵 객체입니다.

```html {linenos=table,hl_lines=[3,"10-12","16-18",20,23],linenostart=1}
SQL(`SELECT NAME, TIME, VALUE FROM EXAMPLE LIMIT 5`)
HTML({
  {{ if .IsFirst }}
    <html>
    <body>
      <h2>HTML Template Example</h2>
      <hr>
      <table>
      <tr>
        {{range .Columns}}
          <th>{{ . }}</th>
        {{end}}
      </tr>
  {{ end }}
      <tr>
        <td>{{ .V.NAME }}</td>
        <td>{{ .V.TIME | timeformat "RFC3339" "Asia/Seoul"}}</td>
        <td>{{ .V.VALUE }}</td>
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

{{< figure src="/neo/tql/img/html_template_3.jpg" width="452" >}}

{{< /tab >}}
{{< tab >}}

`.Value`는 현재 레코드의 필드를 인덱스로 접근하는 함수입니다.

```html {linenos=table,hl_lines=[9,16,18,20],linenostart=1}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
HTML({
    {{ if .IsFirst }}
        <html>
        <body>
            <h2>HTML Template Example</h2>
            <hr>
    {{ end }}

    <li>{{ .Value 0 }} : {{ .Value 1 }}
    
    {{ if .IsLast }}
        <hr>
        Total: {{ .Num }}
        </body>
        </html>
    {{ end }}
})
```

{{< figure src="/neo/tql/img/html_template.jpg" width="518" >}}

{{< /tab >}}
{{< tab >}}

`.Values`는 현재 레코드의 모든 필드 값을 담고 있는 배열입니다.

```html {linenos=table,hl_lines=[9,16,18,20],linenostart=1}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
HTML({
    {{ if .IsFirst }}
        <html>
        <body>
            <h2>HTML Template Example</h2>
            <hr>
    {{ end }}

    <li>{{ (index .Values 0) }} : {{ (index .Values 1 ) }}
    
    {{ if .IsLast }}
        <hr>
        Total: {{ .Num }}
        </body>
        </html>
    {{ end }}
})
```

{{< figure src="/neo/tql/img/html_template.jpg" width="518" >}}

{{< /tab >}}
{{< /tabs >}}

## 컨텍스트

템플릿은 HTML, CSS, JavaScript, URI 컨텍스트를 이해합니다.  
각 파이프라인에는 자동으로 이스케이프 함수가 적용되어 안전하게 렌더링되도록 보장합니다.

예를 들어 `{{.Value 0}}`, `{{.Value 1}}`, `{{.Value 2}}`는 상황에 맞는 이스케이프 함수가 적용된 형태로 변환됩니다.

```html {linenos="table"}
SCRIPT({
    $.yield(
        `http://maven.org/`,
        `<img src="https://docs.machbase.com/images/java_logo_32.png">`,
        "Java")
    $.yield(
        `http://npmjs.com/`,
        `<img src="https://docs.machbase.com/images/js_logo_32.png">`,
        "JavaScript")
})
HTML({
    <li>
        <a href="{{.Value 0}}">
        {{.ValueHTML 1}}{{.Value 2}}
        </a>
    </li>
})
```

- 출력:

```html
<li>
  <a href="http://maven.org/">
    <img src="https://docs.machbase.com/images/java_logo_32.png">Java
  </a>
</li>
<li>
  <a href="http://npmjs.com/">
    <img src="https://docs.machbase.com/images/js_logo_32.png">JavaScript
  </a>
</li>
```

`{{.Value 0}}` 값이 `O'Reilly: How are <i>you</i>?`라고 가정하면, 아래 예시는 해당 값이 각 컨텍스트에서 어떻게 표현되는지 보여 줍니다.

```html {linenos="table"}
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML({
  {{.Value 0}}
})

// 출력:
//  O&#39;Reilly: How are &lt;i&gt;you&lt;/i&gt;?
```


```html {linenos="table"}
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a href="/path?p={{.ValueHTML 0}}">`)

// 출력:
//  <a href="/path?p=O%27Reilly%3a%20How%20are%20%3ci%3eyou%3c%2fi%3e%3f">
```

```html {linenos="table"}
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a onx='f("{{.Value 0}}")'>`)

// 출력:
//  <a onx="f('O\u0027Reilly: How are \u003ci\u003eyou\u003c\/i\u003e?')">
```

``` {linenos="table"}
SCRIPT({ $.yield(`Hello World?`, `function doMsg(msg){ console.log(msg); }`) })
HTML({
  <script>
  {{.ValueJS 1}}
  </script>
  <a onClick='doMsg("{{.Value 0}}")'>here</a>
})

// 출력:
// <script>
// function doMsg(msg){ console.log(msg); }
// </script>
// <a onClick='doMsg("Hello World?")'>here</a>
```

문자열이 아닌 값도 JavaScript 컨텍스트에서 사용할 수 있습니다.  
레코드가 객체일 경우 다음과 같이 출력됩니다.

```html {{linenos="table"}}
SCRIPT({
    $.yield({A: "foo", B:"bar"})
})
HTML({
    <script>var pair = {{ .Value 0 }};</script>
})
```

출력 결과는 다음과 같습니다.

```html
<script>var pair = {"A":"foo","B":"bar"};</script>
```

## 이스케이프되지 않은 문자열

기본적으로 템플릿은 모든 파이프라인이 일반 텍스트 문자열을 생성한다고 가정하고, 적절한 컨텍스트에 맞춰 자동으로 이스케이프 단계를 추가합니다.

데이터가 일반 텍스트가 아니라면 해당 타입을 지정해 중복 이스케이프를 방지할 수 있습니다.  
HTML, JS, URL 등은 안전한 콘텐츠로 간주되어 이스케이프 대상에서 제외됩니다.

다음 템플릿을 실행하면:

```js {{linenos="table"}}
SCRIPT({
    $.yield(`<b>World</b>`)
})
HTML({
    Hello, {{ .ValueHTML 0 }}!
})
```

결과는 다음과 같습니다.

```html
Hello, <b>World</b>!
```

자동 이스케이프를 적용하면 다음과 같이 출력됩니다.

```
Hello, &lt;b&gt;World&lt;b&gt;!
```
