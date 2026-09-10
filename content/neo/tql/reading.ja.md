---
title: 読み取りAPIとして使用
type: docs
weight: 05
toc: true
---

{{< callout type="info" >}}
例を実行する前に、以下のSQLでテーブルとデータを準備してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
VALUE DOUBLE SUMMARIZED);

INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 11);
```

TQLスクリプトを保存すると、エディターの右上に <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> アイコンが表示されます。クリックすると、スクリプトのアドレスをコピーできます。

## CSV

{{< tabs >}}
{{< tab name="既定" >}}
以下のコードを `output-csv.tql` として保存してください。

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
CSV()
```

*curl* コマンドでTQLを呼び出してください。

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```
{{< /tab >}}
{{< tab name="delimiter()" >}}
以下のコードを `output-csv.tql` として保存してください。

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
CSV( delimiter("|") )
```

*curl* コマンドでTQLを呼び出してください。

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
{{< tab name="既定" >}}
以下のコードを `output-json.tql` として保存してください。

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON()
```

*curl* コマンドでTQLを呼び出してください。

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
以下のコードを `output-json.tql` として保存してください。

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( transpose(true) )
```

*curl* コマンドでTQLを呼び出してください。

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
以下のコードを `output-json.tql` として保存してください。

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( rowsFlatten(true) )
```

*curl* コマンドでTQLを呼び出してください。

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
以下のコードを `output-json.tql` として保存してください。

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( rowsArray(true) )
```

*curl* コマンドでTQLを呼び出してください。

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

以下のコードを `output-ndjson.tql` として保存してください。

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
NDJSON( )
```

*curl* コマンドでTQLを呼び出してください。

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
{{< tab name="既定" >}}
以下のコードを `output-markdown.tql` として保存してください。

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
MARKDOWN()
```

*curl* コマンドでTQLを呼び出してください。

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
以下のコードを `output-markdown.tql` として保存してください。

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
MARKDOWN( html(true) )
```

*curl* コマンドでTQLを呼び出してください。

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

`HTML()` 関数は、テンプレート言語を使って結果をHTML文書として出力します。  
クエリ結果に合わせて、HTMLの構造とスタイルを自由に構成できます。

`{{ .V.column_name }}` のようにカラム値を読み取ったり、`{{ if .IsFirst }}`、`{{ if .IsLast }}` の条件で最初と最後の行に応じてテンプレートを制御したりできます。TQLスクリプトだけで、表やレポートなどのさまざまなHTML表現を生成できます。

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

<a id="chart-with-chartjson"></a>
## CHART

**TQLファイルの保存**

以下のコードを `output-chart.tql` として保存してください。

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

Webブラウザーで `http://127.0.0.1:5654/db/tql/output-chart.tql` を開いてください。

{{< figure src="/neo/tql/img/reading-chart-bar.jpg" width="500" >}}

> 従来の `CHART_LINE()`、`CHART_BAR()`、`CHART_SCATTER()` 系の関数は、新しい `CHART()` 関数に置き換えられました。  
> 例は [CHART()](/neo/tql/chart) を参照してください。

### chartJson()の使用 {#chartjson-활용}

**TQLファイルの保存**

以下のコードを `output-chart.tql` として保存してください。

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

Webブラウザーで `http://127.0.0.1:5654/db/tql/output-chart.tql` を開いてください。

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

### chartID()の使用 {#chartid-활용}

**TQLファイルの保存**

以下のコードを `output-chart.tql` として保存してください。

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

Webブラウザーで `http://127.0.0.1:5654/db/tql/output-chart.tql` を開いてください。

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

この方法は、DOM文書に `<div id='myChart'></div>` がある場合に便利です。

```html
... HTML内 ...
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

## 結果データのキャッシュ {#cache-result-data}

{{< neo_since ver="8.0.43" />}}

以下のように、`CSV()`、`JSON()`、`NDJSON()`、`HTML()` シンクに `cache()` オプション関数を指定できます。

```js
SQL( "select * from example limit ?, 1000",  param("offset") ?? 0 )
JSON( cache( param("offset") ?? "0", "60s" ) )
```

`cache()` オプションは、必須の `CACHE_KEY` と `TTL`、省略可能な `r` を受け取ります。

**構文**: `cache(CACHE_KEY string, TTL string, [r float])`

1. 最初のパラメーター `CACHE_KEY` は、キャッシュデータの登録と検索に使用します。キーは
   `[filename] + [source_code_hash] + [CACHE_KEY]` で構成されます。
   そのため、同じTQL（同じファイル名とコード）を同じ `CACHE_KEY` で実行すると、
   キーは同じになり、後から実行した結果が既存のキャッシュデータを上書きします。
2. 2番目のパラメーター `TTL` は、指定した期間後にキャッシュを自動削除します。
   TTLの経過後に受け取ったリクエストは、実際のDBを検索して結果データを返し、
   その結果を再びキャッシュに登録します。
3. 3番目の省略可能なパラメーター `r` は、先行キャッシュ更新率（preemptive-cache-update-ratio）です。
   0より大きく1.0未満の値を指定します。
   `r * TTL` から `TTL` の間に受け取った最初のリクエストには、
   現在のキャッシュデータを返してからクエリを実行し、キャッシュを更新します。
   後続のリクエストは、更新済みの結果をキャッシュから取得します。
   これにより、頻繁に要求される `CACHE_KEY` のキャッシュデータをバックグラウンドで継続的に更新できます。

コードを変更すると `source_code_hash` が変わるため、キャッシュミスになります。
TTLが経過してキャッシュが自動削除された場合も、キャッシュミスになります。
いずれの場合もリクエストを実行し、その結果をキャッシュに登録します。

この動作は、シンク関数に `cache()` オプションを指定した場合にのみ適用されます。
`cache()` を指定していないTQLは、キャッシュを検索しません。

> 注意：キャッシュを過度に使用すると、メモリが不足する可能性があります。
> たとえば、数十億件のレコードをSELECTするTQLでcache()を使用する場合などです。
