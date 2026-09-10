---
title: HTML()
type: docs
weight: 50
toc: true
---

`HTML()` シンクは、テンプレート言語を使用して結果をHTML文書または要素として出力します。  
クエリ結果に合わせて、HTMLの構造と表示を自由に構成できます。

*構文*: `HTML(templates...)` {{< neo_since ver="8.0.53" />}}

- `templates`：1つ以上のテンプレート文字列、または `file(path)` 参照です。各引数にテンプレート文字列を直接記述するか、`file(path)` で外部ファイルを読み込めます。テンプレートにはGoのHTMLテンプレート言語を使用します。詳しい構文は [templateの文書](https://pkg.go.dev/html/template)を参照してください。
- `cache()`：結果データをキャッシュします。詳細は[結果データのキャッシュ](../reading/#cache-result-data)を参照してください。

テンプレート内では、現在のレコードのフィールド値や行番号にアクセスする値オブジェクトを使用できます。  
HTMLテンプレートのコンテキストで使用できるフィールドとプロパティを以下に示します。

## メソッド {#메서드}

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

## 関数 {#함수}

### `timeformat`

**構文**

```
{{ timeformat <format> <timezone> }}
```

**使用例**

```html {linenos=table,hl_lines=[6]}
SCRIPT({
    $.yield(new Date(), "Hello World");
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

**使用例**

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

- `?param=Line` パラメーターを付けてTQLスクリプトを呼び出してください。

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

## 使用例 {#활용-예시}

{{< tabs >}}
{{< tab name=".V" >}}

`.V` は、フィールド名をキーとするマップオブジェクトです。

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
{{< tab name=".Value" >}}

`.Value` は、現在のレコードのフィールドにインデックスでアクセスする関数です。

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
{{< tab name=".Values" >}}

`.Values` は、現在のレコードのすべてのフィールド値を格納する配列です。

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

## コンテキスト {#컨텍스트}

テンプレートは、HTML、CSS、JavaScript、URIのコンテキストを認識します。  
各パイプラインにエスケープ関数が自動で適用され、安全に描画されます。

たとえば、`{{.Value 0}}`、`{{.Value 1}}`、`{{.Value 2}}` は、それぞれのコンテキストに応じたエスケープ関数を適用する形式に変換されます。

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

- 出力：

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

`{{.Value 0}}` の値が `O'Reilly: How are <i>you</i>?` の場合、以下の例のように各コンテキストで表現されます。

```html {linenos="table"}
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML({
  {{.Value 0}}
})

// 出力：
//  O&#39;Reilly: How are &lt;i&gt;you&lt;/i&gt;?
```


```html {linenos="table"}
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a href="/path?p={{.ValueHTML 0}}">`)

// 出力：
//  <a href="/path?p=O%27Reilly%3a%20How%20are%20%3ci%3eyou%3c%2fi%3e%3f">
```

```html {linenos="table"}
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a onx='f("{{.Value 0}}")'>`)

// 出力：
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

// 出力：
// <script>
// function doMsg(msg){ console.log(msg); }
// </script>
// <a onClick='doMsg("Hello World?")'>here</a>
```

文字列以外の値もJavaScriptコンテキストで使用できます。  
レコードがオブジェクトの場合、次のように出力されます。

```html {{linenos="table"}}
SCRIPT({
    $.yield({A: "foo", B:"bar"})
})
HTML({
    <script>var pair = {{ .Value 0 }};</script>
})
```

出力結果は次のとおりです。

```html
<script>var pair = {"A":"foo","B":"bar"};</script>
```

## エスケープしない文字列 {#이스케이프되지-않은-문자열}

既定では、すべてのパイプラインが通常のテキスト文字列を生成するとみなし、適切なコンテキストに応じてエスケープ処理を自動的に追加します。

データが通常のテキストでない場合は、型を指定して重複したエスケープを防げます。  
HTML、JS、URLなどの型は安全なコンテンツとして扱われ、エスケープの対象外になります。

次のテンプレートを実行すると：

```js {{linenos="table"}}
SCRIPT({
    $.yield(`<b>World</b>`)
})
HTML({
    Hello, {{ .ValueHTML 0 }}!
})
```

結果は次のとおりです。

```html
Hello, <b>World</b>!
```

自動エスケープを適用すると、次のように出力されます。

```
Hello, &lt;b&gt;World&lt;b&gt;!
```
