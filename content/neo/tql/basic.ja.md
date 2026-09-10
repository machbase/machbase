---
title: 基礎
type: docs
weight: 02
toc: true
---

## 基本型 {#기본-타입}

TQLは、文字列（`string`）、数値（`number`）、ブール値（`boolean`）、時刻（`time`）型をサポートします。

### 文字列（string） {#문자열string}

文字列は、単一引用符（'）、二重引用符（"）、バッククォート、中括弧で囲めます。バッククォートは、複数行の文字列や引用符を含む長いSQL文に便利です。

複数行のテキストにバッククォートや中括弧（`{`、`}`）が含まれ、区切り文字と衝突する場合は、タグ付きリテラルを使用できます。

- タグ付きバッククォート：`` `<<TAG ... TAG` ``
- タグ付き中括弧：`({<<TAG ... TAG})`

どちらも内容をrawテキストとして扱い、終了行のタグで閉じます。

```js
SQL( 'select * from example where name=\'temperature\' limit 10' )
CSV()
```

```js
SQL( "select * from example where name='temperature' limit 10" )
CSV()
```

```js
SQL( `select *
      from example
      where name='temperature'
      limit 10` )
CSV()
```

```js
SCRIPT(`<<JS
// '{' を返す関数
function a () { return '{' }
JS`)
CSV()
```

~~~js
MARKDOWN({<<MD
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER :places
```
MD})
~~~

二重中括弧（`{{ }}`）を使うと、引用符をエスケープせずにJSON文字列を記述できます。

```js
STRING({{
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}})
CSV()
```

バッククォートでJSONを記述する例です。

```js {linenos=table}
STRING(`{ 
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}`)
CSV()

```

### 数値（number） {#숫자number}

すべての数値リテラルは64ビット浮動小数点数として処理されます。

```js
SQL_SELECT('time', 'value', from('example', 'temperature'), limit(10))
CSV()
```

```js
FAKE( oscillator( freq(12.34, 20), range("now", "1s", "100ms")) )
CSV()
```

### ブール値（boolean） {#불리언boolean}

ブール定数は `true` と `false` です。

```js
FAKE( linspace(0, 1, 1))
CSV( heading(false) )
```

### 時刻（time） {#시간time}

`time()`、`parseTime()` 関数で生成するか、SQLの結果の `DATETIME` カラムから取得できます。

### タイムゾーン（timeZone） {#타임존timezone}

`tz()` 関数でタイムゾーンを指定できます。例：`tz('UTC')`、`tz('Local')`、`tz('Asia/Seoul')`

### リスト（list） {#리스트list}

`list()` 関数で値の配列を生成します。例：`list(1, 2, 3)`

### 辞書（dictionary） {#딕셔너리dictionary}

`dict()` 関数は、文字列のキーと値のペアからなる辞書を生成します。例：`dict("name", "pi", "value", 3.14)`

## 文の記述規則 {#문장-작성-규칙}

文字列、数値、ブール値のリテラルを除き、すべての文は関数呼び出しの形式で記述します。

```js
// コメントは '//' で記述します。
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
CSV()
```

## SRCとSINK {#src와-sink}

`.tql` スクリプトは、データを生成する**ソース（SRC）**関数で始める必要があります。`SQL()`、`SQL_SELECT()`、`SCRIPT()` などが該当します。最後の文は、結果を出力または保存する**シンク（SINK）**関数である必要があります。代表例は `CSV()`、`JSON()`、`APPEND()`、`CHART()` です。

## MAP関数 {#map-함수}

ソースとシンクの間には、0個以上のMAP関数を配置できます。MAP関数名は大文字で始まり、内部のオプションは小文字で始まるキャメルケースの関数で指定します。

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
DROP(5)
TAKE(5)
CSV()
```

## パラメーター（param） {#파라미터param}

HTTPで `.tql` スクリプトを呼び出す際にクエリパラメーターを渡し、`param()` 関数で値を読み取れます。

```js
SQL_SELECT(
    'time', 'value',
    from('example', param('name')),
    limit( param('count') )
)
CSV()
```

たとえば、ファイルを `hello2.tql` として保存し、`http://127.0.0.1:5654/db/tql/hello2.tql?name=temperature&count=10` で呼び出すと、`param('name')` は `"temperature"`、`param('count')` は文字列 `"10"` を返します。

{{% steps %}}

### `param()` の使用 {#param-사용}

次のコードを `example.tql` ファイルに保存します。

```js
SQL( `select * from example where name = ?`, param('name'))
CSV()
```

### クライアントからのGETリクエスト {#클라이언트-get-요청}

`curl` コマンドでTQLを呼び出します。

```
curl "http://127.0.0.1:5654/db/tql/param.tql?name=TAG0"
```

{{% /steps %}}

## 演算子 {#연산자}

### 算術演算子 {#산술-연산자}

`+`、`-`、`*`、`/` の4つの算術演算をサポートします。

```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 10, 5))
MAPVALUE( 1, value(0) * 100 )
CSV()
```

```csv
1,100
3.25,325
5.5,550
7.75,775
10,1000
```

### 剰余演算子 {#modulo-operator}

`%` で表す剰余演算子（モジュロ演算子）は、算術演算子です。
整数除算の余りを返します。

```js {linenos=table,hl_lines=[2]}
FAKE(arrange(1, 10, 1))
FILTER(value(0) % 3 == 0)
CSV()
```

```csv
3
6
9
```

### 文字列の連結 {#concatenation}

`+` 演算子のオペランドが文字列の場合、連結した文字列を返します。

```js {linenos=table,hl_lines=[4]}
FAKE(json({
    ["hello", "world"]
}))
MAPVALUE(2, value(0) + " " + value(1) + "?")
CSV()
```

```csv
hello,world,hello world?
```

### 比較演算子 {#relational-operator}

| 比較         | 演算子 | 説明 |
| :--------------------- | :--  | :-- |
| 等しい               | `==` | オペランドが等しい場合にTRUEを返す |
| 等しくない             | `!=` | オペランドが等しくない場合にTRUEを返す |
| より大きい           | `>`  | 左辺の値が右辺の値より大きいかを判定する |
| 以上  | `>=` | 左辺の値が右辺の値以上かを判定する |
| より小さい              | `<`  | 左辺の値が右辺の値より小さいかを判定する |
| 以下     | `<=` | 左辺の値が右辺の値以下かを判定する |


```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 5, 5))
FILTER( value(0) >= 4 )
CSV()
```

```csv
4
5
```

### 論理演算子 {#logical-operators}

論理演算子は、論理積、論理和、否定を実行します。

| 論理演算 | 演算子 | 説明 |
| :-- | :--  | :-- |
| AND | `&&` | 両方のオペランドがTRUEの場合にTRUEを返す |
| OR  | `\|\|` | いずれかのオペランドがTRUEの場合にTRUEを返す |
| NOT | `!`  | 1つのオペランドを受け取る |

```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 5, 5))
FILTER( value(0) > 0  && mod(value(0), 2) == 0 )
CSV()
```

```csv
2
4
```

### IN演算子 {#in-operator}

`A in (args...)` は、argsに `A` が含まれる場合にtrue、それ以外の場合にfalseを返します。

```js {linenos=table,hl_lines=[7]}
FAKE(json({
    ["A", 1.0],
    ["B", 1.5],
    ["C", 2.0],
    ["D", 2.5]
}))
FILTER( value(0) in ("A", "C") )
CSV()
```

```js {linenos=table,hl_lines=[7]}
FAKE(json({
    ["A", 1.0],
    ["B", 1.5],
    ["C", 2.0],
    ["D", 2.5]
}))
FILTER( value(1) in (1.5, 2.5) )
CSV()
```

### 三項演算子 {#ternary-operator}

三項演算子 `? :` は、他のプログラミング言語のif-else文に似ています。
if-else文と同じ手順で条件に応じた値を選択します。

- param('name') が定義されているかどうか

```js {linenos=table,hl_lines=[4]}
SQL_SELECT(
    'time', 'value',
    from('example',
        param('name') == NULL ? 'temperature' : param('name')
    ),
    limit( param('count') ?? 10 )
)
CSV()
```

- 条件に応じた値の変更

```js {linenos=table,hl_lines=[2]}
FAKE(linspace(1, 5, 5))
MAPVALUE(0, mod(value(0), 2) == 0 ? value(0)*10 : value(0))
CSV()
```

```
1
20
3
40
5
```

### Nil合体演算子 {#nil-coalescing}

`??` 演算子は左右のオペランドを受け取ります。左辺が定義されている場合はその値を返し、未定義の場合は右辺の値を返します。
以下は `??` 演算子の一般的な使用例です。呼び出し元がクエリパラメーターを指定しなかった場合、右辺の値を既定値として使用します。

```js {linenos=table,hl_lines=[3]}
SQL_SELECT(
    'time', 'value',
    from('example', param('name') ?? 'temperature'),
    limit( param('count') ?? 10 )
)
CSV()
```

> {{< figure src="/images/copy_addr_icon.jpg" width="24px" >}}
> TQLスクリプトを保存すると、エディターの右上にリンクアイコンが表示されます。クリックすると、スクリプトファイルのアドレスをコピーできます。

**例**

{{% steps %}}

#### `??` の使用 {#use-}

以下のコードを `param-default.tql` として保存します。

```js
SQL( `select * from example limit ?`, param('limit') ?? 1)
CSV()
```

#### HTTP GET

クエリパラメーターなしのGETリクエスト

```sh
curl http://127.0.0.1:5654/db/tql/param-default.tql
```

```csv
TAG0,1628694000000000000,10
```

#### パラメーター付きHTTP GET {#http-get-with-param}

クエリパラメーター付きのGETリクエスト

```sh
curl http://127.0.0.1:5654/db/tql/param-default.tql?limit=2
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

{{% /steps %}}

## プラグマ {#pragma}

`//+ name=value` ディレクティブは、Machbase NeoによるTQLスクリプトの実行方法を指定します。

### log-level

{{< neo_since ver="8.0.47" />}}

ログレベルを `[TRACE | DEBUG | INFO | WARN | ERROR]` のいずれかに設定します。
既定値は `ERROR` です。HTTPおよびMQTT APIから呼び出した場合、ほとんどのログメッセージを抑制します。

```js {linenos=table,hl_lines=["1"]}
//+ log-level=TRACE
SQL(`select * from my_table where name = ?`, param("name"))
WHEN(true, doLog('hello world'))
CSV()
```

### sql-thread-lock

{{< neo_since ver="8.0.47" />}}

このプラグマは、指定した `SQL()` を専用のネイティブスレッドで実行します。
スレッドはTQLスクリプトの終了時に終了します。
SRCの `SQL()` でのみ動作します。

100個のHTTPクライアントが同時にTQLファイルを実行する内部性能テストでは、
このオプションを有効にするとレスポンスのレイテンシーが35%増加しますが、メモリ解放の遅延が大幅に減少しました。

```js {linenos=table,hl_lines=["1"]}
//+ sql-thread-lock
SQL(`select * from my_table where name = ?`, param("name"))
WHEN(true, doLog('hello world'))
CSV()
```
