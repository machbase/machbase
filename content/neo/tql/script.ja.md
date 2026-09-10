---
title: SCRIPT()
type: docs
weight: 55
toc: true
---

TQLは、**SRC** と **MAP** のコンテキストでJavaScriptを使用できる `SCRIPT()` 関数を提供します {{< neo_since ver="8.0.36" />}}。  
使い慣れたプログラミング言語でロジックを記述し、より柔軟で強力なスクリプトを作成できます。

*構文*: `SCRIPT({main_code})`

*構文*: `SCRIPT({init_code}, {main_code})`

*構文*: `SCRIPT({init_code}, {main_code}, {deinit_code})`

- *init_code*：初期化コード（省略可。ただし *deinit_code* がある場合は必須）
- *main_code*：必須の実行コード
- *deinit_code*：終了時に実行するコード（省略可）

`init_code` は最初に1回だけ実行されます。`main_code` は必須です。

**注意事項**

現在の `SCRIPT()` はGojaベースのJavaScript実行環境を使用します。
Typed Array、テンプレートリテラル（バッククォート文字列）、`const`、アロー関数を使用できます。
`"use strict"` による厳格モードも有効です。
正規表現の先読み（`(?=...)`、`(?!...)`）と後方参照（`\1` など）も使用できます。
対応する言語機能は、利用するMachbase Neoに組み込まれた実行環境のバージョンに従います。

## JSHモジュール {#jsh-모듈}

{{< neo_since ver="8.0.52" />}}

`require()` を使って、`SCRIPT()` 内にJSHモジュールをインポートできます。

```js
SCRIPT({
    const { arrange } = require("mathx")
    arrange(0, 6, 3).forEach((i) =>$.yield(i))
})
CSV()
```

## コンテキストオブジェクト {#컨텍스트-객체}

Machbase Neoは、コンテキストオブジェクトとして `$` 変数を提供します。JavaScriptは、このオブジェクトを通じてレコードやデータベースにアクセスし、新しいレコードを出力できます。

- `$.payload`：リクエスト本文のデータ。`SCRIPT()` がSRCノードの場合にのみ存在し、それ以外は `undefined` です。
- `$.params`：リクエストのクエリパラメーター。
- `$.result`：`SCRIPT()` 関数が出力する結果のカラム名と型を指定します。
- `$.key`、`$.values`：現在のレコードのキーと値にアクセスします。MAPコンテキストでのみ使用できます。
- `$.yield()`：値だけを渡して新しいレコードを出力します。
- `$.yieldKey()`：キーと値を渡して新しいレコードを出力します。
- `$.yieldArray()`：配列1つを引数として受け取り、レコードを出力します。
- `$.db()`：新しいデータベース接続を返します。
- `$.db().query()`：SQLクエリを実行します。
- `$.db().exec()`：SELECT以外のSQLを実行します。
- `$.request().do()`：リモートサーバーにHTTPリクエストを送信します。

### `$.payload`

`$.payload` からリクエスト本文のデータを読み取れます。入力データがない場合は `undefined` です。  
SRCノードとして使用する場合にのみアクセスできます。

```js {{linenos=table,hl_lines=[2]}}
SCRIPT({
    var data = $.payload;
    if (data === undefined) {
        data = '{ "prefix": "name", "offset": 0, "limit": 10}';
    }
    var obj = JSON.parse(data);
    $.yield(obj.prefix, obj.offset, obj.limit);
})
CSV()
```

リクエスト本文なしで呼び出すと、`$.payload` は `undefined` になります。

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

結果は既定値の `name,0,10` です。

リクエスト本文を渡すと、次のように動作します。

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql \
-d '{"prefix":"testing", "offset":10, "limit":10}'
```

結果：`testing,10,10`

### `$.params`

`$.params` は、リクエストのクエリパラメーターを提供します。  
ドット表記（`$.params.name`）と角括弧表記（`$.params["name"]`）の両方を使用できます。

```js {{linenos=table,hl_lines=["2-4"]}}
SCRIPT({
    var prefix = $.params.prefix ? $.params.prefix : "name";
    var offset = $.params.offset ? $.params.offset : 0;
    var limit = $.params.limit ? $.params.limit: 10;
    $.yield(prefix, offset, limit);
})
CSV()
```

パラメーターなしで呼び出す場合：

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

結果：`name,0,10`

パラメーターを渡す場合：

```sh
curl -o - -X POST "http://127.0.0.1:5654/db/tql/test.tql?prefix=testing&offset=12&limit=20"
```

結果：`testing,12,20`

### `$.result`

`SCRIPT` が出力する結果のカラムと型を定義します。  
次の例のように、初期化コード内で設定します。

```js {{linenos=table,hl_lines=["2-5"]}}
SCRIPT({
    $.result = {
        columns: ["val", "sig"],
        types: ["double", "double"] 
    }
},{
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        $.yield( val, sig );
    }
})
JSON()
```

### `$.key`

現在のレコードのキーにアクセスします。MAPコンテキストでのみ定義され、SRCでは `undefined` です。

```js {{linenos=table,hl_lines=["7"]}}
SCRIPT({
    for( i = 0; i < 3; i++) {
        $.yieldKey(i, "hello-"+(i+1));
    }
})
SCRIPT({
    $.yieldKey($.key, $.values[0], 'key is '+$.key);
})
CSV()
```

```csv
hello-1,key is 0
hello-2,key is 1
hello-3,key is 2
```

### `$.values`

現在のレコードの値配列にアクセスします。MAPコンテキストでのみ使用でき、SRCでは `undefined` です。

```js {{linenos=table,hl_lines=["7"]}}
SCRIPT({
        $.yield("string", 10, 3.14);
})
SCRIPT({
    $.yield(
        "the first value is "+$.values[0],
        "2nd value is "+$.values[1],
        "3rd is "+$.values[2]
    );
})
CSV()
```

出力：

`the first value is string,2nd value is 10,3rd is 3.14`

### `$.yield()`

新しいレコードを次のステップに出力します。キーには連番が自動的に割り当てられます。

```js
$.yield(field1, field2, field3);
```

### `$.yieldKey()`

`yieldKey()` は `$.yield()` と同様に動作しますが、最初の引数でレコードのキーを指定します。

```js
$.yieldKey(key, field1, field2, field3);
```

### `$.yieldArray()`

{{< neo_since ver="8.0.39" />}}

配列に格納されたレコードを出力します。
可変長引数を受け取る `$.yield()` と異なり、`$.yieldArray()` はレコードを表す配列1つを受け取ります。
配列を扱う場合に便利です。

```js
var arr = [];
for( i = 0; i < unknown; i++) {
    arr.push(field_values[i]);
}
$.yieldArray(arr);
```

### `$.db()`

新しいデータベース接続を返します。接続は `query()` と `exec()` 関数を提供します。

`$.db({bridge: "sqlite"})` のように *option* オブジェクトを引数に指定すると、
Machbaseデータベースの代わりに、ブリッジ接続したデータベースへの新しい接続を返します。

**オプション**

optionパラメーターは次のバージョンからサポートされます {{< neo_since ver="8.0.37" />}}。

```js
{
    bridge: "name", // ブリッジ名
}
```

### `$.db().query()`

JavaScriptから `$.db().query()` でデータベースを検索できます。
`query()` の戻り値に `forEach()` でコールバック関数を適用し、クエリ結果を反復処理します。

`.forEach()` のコールバック関数が明示的に `false` を返すと、反復処理は直ちに終了します。
`true` を返すか、何も返さない場合（`undefined` を返す場合）は、
クエリ結果の末尾まで反復処理を続けます。

{{< tabs >}}
{{< tab name="MACHBASE" >}}
```js {{linenos=table,hl_lines=["7-10",14]}}
SCRIPT({
  var data = $.payload;
  if (data === undefined) {
    data = '{ "tag": "cpu.percent", "offset": 0, "limit": 3 }';
  }
  var obj = JSON.parse(data);
  $.db()
   .query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
    obj.tag, obj.offset, obj.limit
  ).forEach( function(row){
    name = row[0]
    time = row[1]
    value = row[2]
    $.yield(name, time, value);
  })
})
CSV()
```

```csv
cpu.percent,1725330085908925000,73.9
cpu.percent,1725343895315420000,73.6
cpu.percent,1725343898315887000,6.1
```

{{< /tab >}}
{{< tab name="BRIDGE-SQLITE" >}}
```js {{linenos=table,hl_lines=["7-10",14]}}
SCRIPT({
  var data = $.payload;
  if (data === undefined) {
    data = '{ "tag": "testing", "offset": 0, "limit": 3 }';
  }
  var obj = JSON.parse(data);
  $.db({bridge:"mem"})
   .query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
    obj.tag, obj.offset, obj.limit
  ).forEach( function(row){
    name = row[0]
    time = row[1]
    value = row[2]
    $.yield(name, time, value);
  })
})
CSV()
```

```csv
testing,1732589744886,16.70559756851126
testing,1732589744886,49.93214293713331
testing,1732589744886,54.485508690434905
```
{{< /tab >}}
{{< /tabs >}}

`$.db().query()` の結果から特定のカラムを選び、`$.yield()` で出力できます。
すべてのカラムをまとめて出力するには、`$.yieldArray()` を使用します {{< neo_since ver="8.0.39" />}}。

```js {{linenos=table,hl_lines=["4"]}}
SCRIPT({
    var sql = "SELECT name, time, value FROM example WHERE name = 'cpu.percent' LIMIT 3";
    $.db().query(sql).forEach( function(row){
        $.yieldArray(row);
    });
})
CSV()
```

または、`$.db().query().yield()` を使って自動的に出力できます {{< neo_since ver="8.0.39" />}}。

```js {{linenos=table,hl_lines=["9"]}}
SCRIPT({
    var tags = ["mem.total", "mem.used", "mem.free"];
    for( i = 0; i < tags.length; i++) {
        $.yield(tags[i]);
    }
})
SCRIPT({
    var sql = "SELECT * FROM example WHERE name = ? LIMIT 1";
    $.db().query(sql, $.values[0]).yield();
})
CSV( header(true) )
```


### `$.db().exec()`

SQLがSELECT文でない場合は、`$.db().exec()` を使用してINSERT、DELETE、CREATE TABLE文を実行します。

{{< tabs >}}
{{< tab name="MACHBASE" >}}
```js {{linenos=table,hl_lines=["10-14", "21-22"]}}
SCRIPT({
    for( i = 0; i < 3; i++) {
        ts = Date.now()*1000000; // ミリ秒をナノ秒に換算
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT({
    // このセクションは初期化コードです。
    // 最初のレコードを処理する前に1回だけ実行します。
    err = $.db().exec("CREATE TAG TABLE IF NOT EXISTS example ("+
        "NAME varchar(80) primary key,"+
        "TIME datetime basetime,"+
        "VALUE double"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // このセクションはメインコードです。
    // 各レコードに対して実行します。
    err = $.db().exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```
{{< /tab >}}
{{< tab name="BRIDGE-SQLITE" >}}
```js {{linenos=table,hl_lines=["10-14", "21-22"]}}
SCRIPT({
    for( i = 0; i < 3; i++) {
        ts = Date.now(); // ms
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT({
    // このセクションは初期化コードです。
    // 最初のレコードを処理する前に1回だけ実行します。
    err = $.db({bridge:"mem"}).exec("CREATE TABLE IF NOT EXISTS example ("+
        "NAME TEXT,"+
        "TIME INTEGER,"+
        "VALUE REAL"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // このセクションはメインコードです。
    // 各レコードに対して実行します。
    err = $.db({bridge:"mem"}).exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```

SQLエディターからブリッジ接続したデータベースを検索するには、クエリに `-- env: bridge=name` を指定します。

```sql
-- env: bridge=mem
SELECT
    name,
    datetime(time/1000, 'unixepoch', 'localtime') as time,
    value
FROM
    example;
-- env: reset
```

{{< figure src="/neo/tql/img/script_js_db_sqlite_exec.png" width="600px" >}}

{{< /tab >}}
{{< /tabs >}}

### `$.request().do()`

*構文*: `$.request(url [, option]).do(callback)`

**リクエストオプション**

```js
{
    method: "GET|POST|PUT|DELETE", // 既定値は "GET"
    headers: { "Authorization": "Bearer auth-token"}, // キーと値のマップ
    body: "body content if the method is POST or PUT"
}
```
レスポンスを処理するコールバック関数を指定して `.do()` を呼び出すと、実際のリクエストを送信します。コールバック関数は、各種プロパティとメソッドを持つResponseオブジェクトを引数として受け取ります。

**レスポンス**

| プロパティ         | 型    | 説明  |
|:-----------------|:-------:|:-------------|
| `.ok`            | Boolean | レスポンスのステータスコードが成功の場合に `true`（`200<= status < 300`） |
| `.status`        | Number  | HTTPレスポンスコード |
| `.statusText`    | String  | ステータスコードとメッセージ（例：`200 OK`） |
| `.url`           | String  | リクエストURL |
| `.headers`       | Map     | レスポンスヘッダー |

Responseオブジェクトには、レスポンス本文を取得するメソッドがあります。

| メソッド                 | 説明  |
|:-----------------------|:-------------|
| `.text(callback(txt))` | 本文を文字列としてコールバックに渡す |
| `.blob(callback(bin))` | 本文をバイナリ配列としてコールバックに渡す |
| `.csv(callback(row))`  | 本文をCSVとして解析し、各行（レコード）に対して `callback()` を呼び出す |
<!-- | .json(callback(obj)) | 本文をJSONオブジェクトまたは配列として解析し、各オブジェクトに対してcallback()を呼び出す。**未実装** | -->

**使用方法**

```js
$.request("https://server/path", {
    method: "GET",
    headers: { "Authorization": "Bearer auth-token" }
  }).do( function(rsp){
    console.log("ok:", rsp.ok);
    console.log("status:", rsp.status);
    console.log("statusText:", rsp.statusText);
    console.log("url:", rsp.url);
    console.log("Content-Type:", rsp.headers["Content-Type"]);
});
```

### finalize()

`SCRIPT()` 内のJavaScriptコードで `function finalize() {}` を定義すると、
すべてのレコードを処理した後に、システムがこの関数を自動的に呼び出します。

次の2つのコード例は同じ動作をし、どちらも最後のレコードとして `999` を出力します。

```js
FAKE( arrange(1, 3, 1) )
SCRIPT({
    function finalize() {
        $.yield(999);
    }
    $.yield($.values[0]);
})
CSV()
```

```js
FAKE( arrange(1, 3, 1) )
SCRIPT({
    // 初期化処理なし
},{
    // メイン処理
    $.yield($.values[0]);
}, {
    // 終了処理;
    $.yield(999);
})
CSV()
```

この例は、`1`、`2`、`3`、`999` の4レコードを出力します。

## 例 {#examples}

### Hello World {#hello-world}

```js
SCRIPT({
    console.log("Hello World?");
})
DISCARD()
```

**結果**

{{< figure src="/neo/tql/img/script_js_helloworld.png" width="550px" >}}

### 組み込みMathオブジェクト {#builtin-math-object}

{{< tabs >}}
{{< tab name="JS" >}}

JavaScriptの組み込み関数を使用できます。

```js {{linenos=table,hl_lines=["3-8"]}}
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SCRIPT({
  x = Math.cos($.values[0]) * Math.sin($.values[1]);
  y = Math.sin($.values[0]) * Math.sin($.values[1]);
  z = Math.cos($.values[1]);
  $.yield([x,y,z]);
})

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{}, xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{  min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[ { type:"scatter3D", data: column(0)} ]
  })
)
```
{{< /tab >}}
{{< tab name="SET-MAP" >}}

JavaScriptの代わりにSET-MAP関数で同じ結果を得る例です。

```js {{linenos=table,hl_lines=["3-8"]}}
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SET(x, cos(value(0))*sin(value(1)))
SET(y, sin(value(0))*sin(value(1)))
SET(z, cos(value(1)))

MAPVALUE(0, list($x, $y, $z))
POPVALUE(1)

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{}, xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{  min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[ { type:"scatter3D", data: column(0)} ]
  })
)
```
{{< /tab >}}
{{< /tabs >}}

**結果**
{{< figure src="/neo/tql/img/script_js_sphere.png" width="550px" >}}

### JSONの解析 {#json-parser}

```js {{linenos=table,hl_lines=["11"]}}
SCRIPT({
    $.result = {
        columns: ["NAME", "AGE", "IS_MEMBER", "HOBBY"],
        types: ["string", "int32", "bool", "string"],
    }
},{
    content = $.payload;
    if (content === undefined) {
        content = '{"name":"James", "age": 24, "isMember": true, "hobby": ["book", "game"]}';
    }
    obj = JSON.parse(content);
    $.yield(obj.name, obj.age, obj.isMember, obj.hobby.join(","));
})
JSON()
```

**結果**
```json
{
    "data": {
        "columns": [ "NAME", "AGE", "IS_MEMBER", "HOBBY" ],
        "types": [ "string", "int32", "bool", "string" ],
        "rows": [ [ "James", 24, true, "book,game" ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "627.958µs"
}
```

### CSVの取得 {#request-csv}

```js {{linenos=table,hl_lines=["17-19"]}}
SCRIPT({
    $.result = {
        columns: ["SepalLen", "SepalWidth", "PetalLen", "PetalWidth", "Species"],
        types: ["double", "double", "double", "double", "string"]
    };
},{
    $.request("https://docs.machbase.com/assets/example/iris.csv")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("url:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        var err = rsp.csv(function(fields){
            $.yield(fields[0], fields[1], fields[2], fields[3], fields[4]);
        })
        if (err !== undefined) {
            console.warn(err);
        }
    })
})
CSV(header(true))
```

### JSONテキストの取得 {#request-json-text}

この例は、リモートサーバーからJSONを取得し、JavaScriptで解析する方法を示します。

```js {{linenos=table,hl_lines=["17-23"]}}
SCRIPT({
    $.result = {
        columns: ["ID", "USER_ID", "TITLE", "COMPLETED"],
        types: ["int64", "int64", "string", "boolean"]
    };
},{
    $.request("https://jsonplaceholder.typicode.com/todos")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("URL:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        rsp.text( function(txt){
            list = JSON.parse(txt);
            for (i = 0; i < list.length; i++) {
                obj = list[i];
                $.yield(obj.id, obj.userId, obj.title, obj.completed);
            }
        })
    })
})
CSV(header(false))
```

