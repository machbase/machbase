---
toc: true
title: "@jsh/db"
type: docs
weight: 10
draft: true
---

{{< neo_since ver="8.0.75" />}}


## Client {#client}

データベースクライアントオブジェクトです。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const db = require("@jsh/db");
const client = new db.Client();
try {    
    conn = client.connect();
    rows = conn.query("select * from example limit 10")
    cols = rows.columns()
    console.log("cols.names:", JSON.stringify(cols.columns));
    console.log("cols.types:", JSON.stringify(cols.types));
    
    count = 0;
    for (const rec of rows) {
        console.log(...rec);
        count++;
    }
    console.log("rows:", count, "selected" );
} catch(e) {
    console.log("Error:", e);
} finally {
    if (rows) rows.close();
    if (conn) conn.close();
}
```

<h6>作成</h6>

| コンストラクター               | 説明                                      |
|:---------------------|:------------------------------------------|
| new Client(*options*) | オプションを指定してデータベースクライアントを作成します。 |

`bridge`も`driver`も指定しない場合は、既定で内部のMachbase DBMSに接続します。

<h6>オプション</h6>

| オプション                | 型        | 既定値    | 説明                                              |
|:--------------------|:------------|:----------|:--------------------------------------------------|
| lowerCaseColumns    | Boolean     | `false`   | 結果オブジェクトに、列名を小文字で割り当てます。      |

ドライバーオプション

定義済みのブリッジがなくても、`driver`と`dataSource`で`sqlite`、`mysql`、`mssql`、`postgresql`、`machbase`に直接接続できます。

| オプション                | 型        | 既定値    | 説明                       |
|:--------------------|:------------|:----------|:---------------------------|
| driver              | String      |           | 使用するドライバー名       |
| dataSource          | String      |           | データベースの接続文字列   |

ブリッジオプション

定義済みのブリッジを使ってClientを作成することもできます。

| オプション                | 型        | 既定値    | 説明                       |
|:--------------------|:------------|:----------|:---------------------------|
| bridge              | String      |           | 使用するブリッジ名        |

<h6>プロパティ</h6>

| プロパティ           | 型       | 説明                                         |
|:-------------------|:-----------|:---------------------------------------------|
| supportAppend      | Boolean    | 「Append」モードに対応する場合は`true`です。       |

### connect() {#connect}

データベースに接続します。

<h6>戻り値</h6>

- `Object` [Conn](#Conn)


<a id="Conn"></a>
## Conn {#conn}

### close() {#close}

接続を閉じ、リソースを解放します。

<h6>構文</h6>

```js
close()
```

### query() {#query}

<h6>構文</h6>

```js
query(String *sqlText*, any ...*args*)
```

<h6>戻り値</h6>

- `Object` [Rows](#rows)

### queryRow() {#queryrow}

<h6>構文</h6>

```js
queryRow(String *sqlText*, any ...*args*)
```

<h6>戻り値</h6>

- `Object` [Row](#Row)


### exec() {#exec}

<h6>構文</h6>

```js
exec(sqlText, ...args)
```

<h6>パラメーター</h6>

- `sqlText` `String` 実行するSQL文字列です。
- `args` `any` SQLにバインドする可変長引数です。

<h6>戻り値</h6>

- `Object` [Result](#result)

### appender() {#appender}

新しい「appender」を作成します。

<h6>構文</h6>

```js
appender(table_name, ...columns)
```

<h6>パラメーター</h6>

- `table_name` `String` データを追加するテーブルの名前です。
- `columns` `String` 可変長の列名リストです。省略すると、テーブルのすべての列を順に使用します。

<h6>戻り値</h6>

- `Object` [Appender](#appender-1)

## Rows {#rows}

Rowsオブジェクトは、クエリの実行結果セットをカプセル化します。

`Symbol.iterator`を実装しており、以下の2つの方式に対応しています。

```js
for(rec := rows.next(); rec != null; rec = rows.next()) {
    console.log(...rec);
}

for (rec of rows) {
    console.log(...rec);
}
```

### close() {#close-1}

データベースステートメントを解放します。

<h6>構文</h6>

```js
close()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

なし（成功時は`undefined`）。

### next() {#next}

次のレコードを読み取ります。レコードがない場合は`null`を返します。

<h6>構文</h6>

```js
next()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `any[]`

### columns() {#columns}

<h6>構文</h6>

```js
columns()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `Object` [Columns](#columns-2)

### columnNames() {#columnnames}

<h6>構文</h6>

```js
columnNames()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `String[]`

### columnTypes() {#columntypes}

<h6>構文</h6>

```js
columnTypes()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `String[]`


<a id="Row"></a>
## Row {#row}

Rowオブジェクトは、単一レコードを返す`queryRow`の結果を扱います。

### columns() {#columns-1}

<h6>構文</h6>

```js
columns()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `Object` [Columns](#columns-2)


### columnNames() {#columnnames-1}

結果の列名を返します。

<h6>構文</h6>

```js
columnNames()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `String[]`

### columnTypes() {#columntypes-1}

結果の列の型を返します。

<h6>構文</h6>

```js
columnTypes()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `String[]`

### values() {#values}

列の値を配列で返します。

<h6>構文</h6>

```js
values()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `any[]`

## Result {#result}

Resultオブジェクトは、`exec()`の実行結果と付加情報を提供します。

<h6>プロパティ</h6>

| プロパティ           | 型       | 説明               |
|:-------------------|:-----------|:-------------------|
| message            | String     | 結果メッセージ        |
| rowsAffected       | Number     | 影響を受けた行数  |

## Columns {#columns-2}

<h6>プロパティ</h6>

| プロパティ           | 型       | 説明                 |
|:-------------------|:-----------|:---------------------|
| columns            | String[]   | 結果の列名一覧  |
| types              | String[]   | 結果の列の型一覧  |

## Appender {#appender-1}

### append() {#append}

列の順序に合わせて値を指定し、行を追加します。

<h6>構文</h6>

```js
append(...values)
```

<h6>パラメーター</h6>

- `values` `any` 指定した列の順序に合わせた、挿入する値のリストです。

<h6>戻り値</h6>

なし。

### close() {#close-2}

Appenderを閉じます。

<h6>構文</h6>

```js
close()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

なし。

### result() {#result-1}

Appenderを閉じた後、最後のappend結果を返します。

<h6>構文</h6>

```js
result()
```

<h6>パラメーター</h6>

なし。

<h6>戻り値</h6>

- `Object`

| プロパティ           | 型       | 説明        |
|:-------------------|:-----------|:-------------------|
| success            | Number     |                    |
| fail               | Number     |                    |
