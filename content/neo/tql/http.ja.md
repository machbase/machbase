---
title: HTTP()
type: docs
weight: 49
toc: true
---

`HTTP()` SRCを使うと、TQLスクリプト内からHTTPリクエストを送信し、レスポンスをすぐに確認できます。  
外部APIとの連携や、データパイプライン内のHTTPエンドポイントのテストに便利です。

*構文*: `HTTP(text)` {{< neo_since ver="8.0.53" />}}

- `text`：HTTPリクエストを記述した文字列です。

## TQLの使用例 {#tql-사용-예시}

構文は [RFC 2616](https://www.rfc-editor.org/rfc/rfc2616) に従い、リクエストメソッド、ヘッダー、本文を指定できます。

**例**

`HTTP()` ソースを使用します。

{{< tabs >}}
{{< tab name="TEXT" >}}
```
HTTP({
    GET http://127.0.0.1:5654/db/query
        ?q=select * from example limit 3
        &format=csv
        &timeformat=default
        &tz=UTC
})
TEXT()
```
{{< /tab >}}
{{< tab name="HTML（簡易）" >}}
```html
HTTP({
    POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

    {
        "q": "select * from example limit 3",
        "format": "csv",
        "timeformat": "default"
    }
})
HTML(`<pre>{{ .Value 0 }}</pre>`)
```
{{< /tab >}}
{{< tab name="HTML（詳細）" >}}
```html
HTTP({
    POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

    {
        "q": "select * from example limit 3",
        "format": "csv",
        "timeformat": "default"
    }
})
HTML({
    {{- with .Value 0 -}}
    <pre>
        {{- .StatusLine }}{{"\n"}}
        {{- .Header }}{{"\n\n"}}
        {{- .Body -}}
    </pre>
    {{- end}}
})
```
{{< /tab >}}
{{< /tabs >}}

リクエストを記述し、TQLを実行してください。  
結果ウィンドウに、ヘッダーと本文を含むHTTPレスポンスが表示されます。

**レスポンスの例**

```
HTTP/1.1 200 OK
Content-Length: 212
Content-Type: text/csv; charset=utf-8
Date: Mon, 02 Jun 2025 03:42:33 GMT

NAME,TIME,VALUE
work-11-0,2025-03-19 01:56:19.824,0.00
work-11-0,2025-03-19 01:56:19.824,1.00
work-11-0,2025-03-19 01:56:19.824,2.00
```

### ワークシート {#워크시트}

Markdownセル内に `http` コードフェンスを使ってリクエストを記述できます。

**例**

~~~text
### HTTPクライアントの例

```http
POST http://127.0.0.1:5654/db/query
    Content-Type: application/json

{
    "q": "select * from example limit 3",
    "format": "box",
    "timeformat": "default"
}
```
~~~

{{< figure src="/neo/tql/img/http_wrk_example.jpg" width="700" >}}


### Markdown {#마크다운}

`http` コードフェンスは `.md` ファイルでも同様に動作します。

~~~
## HTTPの例

Code fence with `http`.

```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from example limit 2
    &format=ndjson
    &timeformat=default&tz=local
```
~~~

{{< figure src="/neo/tql/img/http_md_example.jpg" width="637" >}}


## クエリ文字列 {#쿼리-문자열}

リクエスト行にクエリ文字列を直接指定できます。

~~~
```http
GET https://example.com/comments?page=2&pageSize=10
```
~~~

クエリパラメーターが多い場合は、読みやすいように複数行に分けられます。  
リクエスト行の後にある `?` または `&` で始まる行は、クエリパラメーターとして解釈されます。

~~~
```http
GET https://example.com/comments
    ?page=2
    &pageSize=10
```
~~~

## リクエストヘッダー {#요청-헤더}

リクエスト行（およびクエリ文字列）の後から最初の空行までは、リクエストヘッダーとして認識されます。  
ヘッダーは1行に1つ、`field-name: field-value` 形式で記述してください。

**例**

```
User-Agent: http-client
Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4
Content-Type: application/json
```


## リクエスト本文 {#요청-본문}

リクエスト本文を含めるには、ヘッダーの後に空行を挿入して本文を記述します。空行より後のすべての内容が本文として扱われます。

**例**

~~~
```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

<request>
    <name>sample</name>
    <time>Wed, 21 Oct 2015 18:27:50 GMT</time>
</request>
```
~~~

**外部ファイルの使用**

本文をファイルで指定するには、行頭に `<` を置き、ファイルエクスプローラーに表示されるパスを入力します。  
OSの絶対パスを使用する場合は、パスの前に `@` を付けてください。

例：
- `< /doc.xml`：TQLルートディレクトリ内のファイルを示します。
- `< @/home/data/doc.xml`：OSの絶対パス `/home/data/doc.xml` を示します。

~~~
```http
POST https://example.com/comments HTTP/1.1
Content-Type: application/xml
Authorization: token xxx

< /data/demo.xml
```
~~~

## マルチパートフォームデータ {#멀티파트-폼-데이터}

リクエスト本文が `multipart/form-data` の場合、テキストとアップロードファイルをまとめて送信できます。

~~~
```http
POST https://api.example.com/user/upload
Content-Type: multipart/form-data; boundary=----Boundary7MA4YWxkTrZu0gW

------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="text"

title
------Boundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="1.png"
Content-Type: image/png

< /data/1.png
------Boundary7MA4YWxkTrZu0gW--
```
~~~

## x-www-form-urlencoded

`application/x-www-form-urlencoded` の本文は、複数行に分けて記述できます。  
2行目以降のキーと値のペアは、`&` で始めてください。

~~~
```http
POST https://api.example.com/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=foo
&password=bar
```
~~~

---

この柔軟なHTTPリクエスト構文により、TQLスクリプト内でさまざまなHTTP機能や形式を簡単にテストし、自動化できます。
