---
title: TQLの概要
type: docs
weight: 01
toc: true
---

Machbase Neoは、Transforming Query Language（TQL）と、その実行用APIを提供します。

一般的なアプリケーション開発では、データベースから取得した表形式（行と列）の結果を必要なデータ構造に変換し、加工してから、JSON、CSV、チャートなど必要な形式で出力します。
TQLでは、この処理を数行のスクリプトで実装できます。作成したTQLをHTTPエンドポイントとして公開し、他のアプリケーションからAPIのように呼び出すこともできます。

## TQLとは {#tql이란}

TQL（Transforming Query Language）は、データ変換用のDSLです。
データストリームの流れを定義します。各データ単位（レコード）は、*key* と *value* で構成されます。

- key：通常は自動増加する整数（クエリ結果のROWNUMに相当）
- value：実際のデータフィールドを格納するタプル

![tql_records](/neo/tql/img/tql_records.jpg)

TQLスクリプトは、データを取得してレコードを生成する *SRC* 関数で始まり、レコードを出力する *SINK* 関数で終わります。
*SRC* と *SINK* の間では、必要に応じて *MAP* 関数でデータを変換できます。

![tql_flow_min](/neo/tql/img/tql_flow_min.jpg)

TQLスクリプトでは、数学計算、簡単な文字列の連結、外部データベースとの連携などによってレコードを変換する必要がある場合があります。このような処理は *MAP* 関数で定義します。

したがって、TQLスクリプトは *SRC* 関数で始まり、*SINK* 関数で終わる必要があります。その間に、必要な変換を行う *MAP* 関数を0個以上配置できます。

![tql_flow](/neo/tql/img/tql_flow.jpg)

### SRC {#src}

TQLでは、複数のSRC関数を使用できます。

- `SQL()`：Machbase Neo、またはブリッジで接続した外部DBでSQLを実行してレコードを生成
- `FAKE()`：テスト用の仮想データを生成
- `CSV()`：CSVファイルを読み取り
- `BYTES()`：ファイルシステム、クライアントのHTTPリクエスト、MQTTペイロードからバイナリデータを読み取り

![tql_src](/neo/tql/img/tql_src.jpg)

### SINK {#sink}

- `INSERT()`：レコードをMachbase Neoのデータベースに書き込み
- `CHART()`：レコードをチャートとして描画
- `JSON()`、`CSV()`：データをそれぞれJSON、CSV形式にエンコードし、他のアプリケーションとの連携や見やすい表示を容易にする

![tql_sink](/neo/tql/img/tql_sink.jpg)

### MAP {#map}

*MAP* 関数は、データを別の形式に変換するための主要なツールです。
数学演算、文字列処理、形式変換、外部システムとの連携などを実行できます。
*MAP* 関数を使うと、アプリケーションの要件に合わせてデータを効率よく処理し、形を変えられます。

![tql_map](/neo/tql/img/tql_map.jpg)

## TQLの実行 {#tql-실행}

{{% steps %}}

### Web UIに接続する {#웹-ui-접속}

ブラウザーでMachbase NeoのWeb UI（既定のアドレスは `http://127.0.0.1:5654/`）にアクセスし、アカウント（`sys` / `manager`）でログインしてください。

### 新しいTQLを作成する {#새-tql-만들기}

`New...` ページで `TQL` を選択してください。

{{< figure src="/images/web-tql-pick.png" width="550" >}}

### サンプルコードを実行する {#예제-코드-실행}

サンプルTQLコードをコピーしてTQLエディターに貼り付け、エディター左上の ▶︎ アイコンをクリックしてください。
以下の画像のように、周波数1.5Hz、振幅1.0の波形がチャートに出力されます。

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

## さまざまな出力形式 {#다양한-출력-형식}

CSVやJSONなどのデータ形式を見ていきます。

- **CSV**：スプレッドシートなど、CSVファイルに対応したアプリケーションへデータをエクスポートする場合に便利です。
- **JSON**：解析しやすく、JavaScriptと連携しやすいため、WebアプリケーションやAPIに適しています。

TQLを使うと、数行のコードでデータをこれらの形式に簡単に変換できます。

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

## APIとして使用する {#api로-활용하기}

エディター右上の保存アイコンをクリックして、コードを `hello.tql` として保存してください。
その後、Webブラウザーで [http://127.0.0.1:5654/db/tql/hello.tql](http://127.0.0.1:5654/db/tql/hello.tql) にアクセスするか、ターミナルで `curl` コマンドを実行してデータを取得できます。

| アイコン | 説明 |
|--------|:-----|
| {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}} | TQLスクリプトを保存すると、エディターの右上にリンクアイコンが表示されます。クリックすると、スクリプトファイルのアドレスをコピーできます。 |

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

### JSON()に変更する {#json으로-변경}

`CSV()` を `JSON()` に変更して保存し、再度実行してください。

{{< figure src="/images/web-hello-tql-json.jpg" width="500" >}}

ターミナルで `curl` を使って `hello.tql` を呼び出すと、JSON形式で結果を取得できます。

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```

HTTPヘッダーを含むJSONレスポンスの例です。

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

### transpose()を指定したJSON() {#transpose를-적용한-json}

データ可視化アプリケーションを開発する場合は、TQLのJSON出力で結果を行単位から列単位に転置（transpose）できることを覚えておくと便利です。
`JSON(transpose(true))` を指定して再度呼び出すと、結果のJSONに `cols` 配列が含まれます。

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

この機能は、他のアプリケーションからデータにアクセスできるRESTful APIを作成する最も簡単な方法です。

### INSERT {#insert}

`CSV()` を `INSERT("time", "value", table("example"), tag("temperature"))` に変更して再実行してください。

{{< figure src="/images/web-tql-insert.png" width="500" >}}

### テーブルを検索する {#테이블-조회}

```js
SQL('select * from example limit 10')
CSV()
```

{{< figure src="/images/web-tql-select.png" width="500" >}}
