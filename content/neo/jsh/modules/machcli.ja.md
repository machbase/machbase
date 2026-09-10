---
toc: true
title: "machcli"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`machcli`モジュールは、JSHアプリケーションからMachbaseデータベースを使用するクライアントAPIを提供します。

## Client {#client}

データベースクライアントを作成します。

<h6>構文</h6>

```js
new Client(config)
```

<h6>設定フィールド</h6>

- `host` (既定値： `127.0.0.1`)
- `port` (既定値： `5656`)
- `user` (既定値： `sys`)
- `password` (既定値： `manager`)
- `alternativeHost` (省略可能)
- `alternativePort` (省略可能)
- `database` (省略可能): 複数データベース環境で接続する対象データベース（別名：`db`） {{< neo_since ver="8.7.0" />}}

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
```

<h6>複数データベースの例</h6>

クライアントの作成時に`database`を指定すると、接続する対象データベースを選択できます。`db`は`database`の別名です。 {{< neo_since ver="8.7.0" />}}

```js {linenos=table,linenostart=1}
const { Client } = require('machcli');
const db = new Client({
    host: '127.0.0.1',
    port: 5656,
    user: 'sys',
    password: 'manager',
    db: 'MACHBASEDB',
});
const conn = db.connect();
```

**Client.connect()**

接続を開き、`Connection`オブジェクトを返します。

<h6>構文</h6>

```js
connect()
```

**Client.close()**

内部のデータベースクライアントを閉じます。

<h6>構文</h6>

```js
close()
```

**Client.user()**

設定したユーザー名を大文字で返します。

<h6>構文</h6>

```js
user()
```

**Client.normalizeTableName()**

テーブル名を`[database, user, table]`形式に正規化します。

<h6>構文</h6>

```js
normalizeTableName(tableName)
```

**Client.tx()**

{{< neo_since ver="8.7.0" />}}

プールから取得した接続でトランザクションを開始し、その中で`fn`を実行します。`fn`が正常に戻るとコミットし、例外をスローするとロールバックして例外を再スローします。`fn`にはそのトランザクションにバインドされた`Connection`が渡されるため、このオブジェクトの`query()`、`queryRow()`、`exec()`は同じトランザクション内で実行されます。

{{< callout emoji="⚠️" >}}
トランザクションは、`CREATE TABLE`で作成した通常のトランザクションテーブルでのみ動作します。ログテーブル（`CREATE LOG TABLE`）とタグテーブル（`CREATE TAG TABLE`）はトランザクションに対応していません。`tx()`内でこれらのテーブルに`exec()`や`query()`を実行すると、`MACHCLI-ERR-2362`などのエラーが発生します。
{{< /callout >}}

<h6>構文</h6>

```js
tx(fn)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
const conn = db.connect();
conn.exec('CREATE TABLE IF NOT EXISTS TX_SAMPLE (ID LONG, NAME VARCHAR(100))');

// fnが正常に戻ると、自動的にコミットします。
db.tx(function (tx) {
    tx.exec('INSERT INTO TX_SAMPLE VALUES(?, ?)', 1, 'committed');
});

// fnが例外をスローすると、ロールバックして例外を再スローします。
try {
    db.tx(function (tx) {
        tx.exec('INSERT INTO TX_SAMPLE VALUES(?, ?)', 2, 'rolledback');
        throw new Error('abort');
    });
} catch (e) {
    console.println('rolled back:', e.message);
}
conn.close();
db.close();
```

## Connection {#connection}

`Client.connect()`が返す接続オブジェクトです。

**Connection.query()**

検索SQLを実行し、`Rows`オブジェクトを返します。`params`には、`?`の位置パラメーター用の可変長引数を渡します。
または、`:key`の名前付きパラメーター用に`{ key: value, ... }`オブジェクトを渡せます {{< neo_since ver="8.7.0" />}}.

<h6>構文</h6>

```js
query(sql[, ...params])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { Client } = require('machcli');
var db, conn, rows;
const conf = {
    host: '127.0.0.1',
    port: 5656,
    user: 'sys',
    password: 'manager' 
};
try {
    db = new Client(conf);
    conn = db.connect();

    // 位置パラメーター
    rows = conn.query('SELECT NAME, TIME, VALUE FROM TAG LIMIT ?', 1);
    for (const row of rows) {
        console.println(row.NAME, row.TIME, row.VALUE);
    }
    rows.close();

    // 名前付きパラメーター
    rows = conn.query('SELECT NAME, TIME, VALUE FROM TAG WHERE NAME = :name ORDER BY TIME LIMIT :one', { name: 'jsh', one: 1 });
    for (const row of rows) {
        console.println(row.NAME, row.TIME, row.VALUE);
    }
    rows.close();
} catch( e ) {
    console.println("ERROR", e.message);
}
db && db.close();
```

**Connection.queryRow()**

検索SQLを実行し、単一行のオブジェクトを返します。

返されるオブジェクトには、`_ROWNUM`と各列名がプロパティとして含まれます。

<h6>構文</h6>

```js
queryRow(sql[, ...params])
```

**Connection.exec()**

DDL/DMLを実行し、結果オブジェクトを返します。

返されるフィールド：

- `rowsAffected`
- `message`

<h6>構文</h6>

```js
exec(sql[, ...params])
```

**Connection.explain()**

実行計画の文字列を返します。

<h6>構文</h6>

```js
explain(sql[, ...params])
```

**Connection.append()**

一括挿入用のAppenderオブジェクトを作成します。

返されるAppenderは、`append()`、`flush()`、`close()`などのメソッドに対応しています。

<h6>構文</h6>

```js
append(tableName)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
const conn = db.connect();
const appender = conn.append('TAG');
appender.append('sensor-1', new Date(), 12.34);
appender.flush();
const result = appender.close();
console.println(result);
conn.close();
db.close();
```

**Connection.tx()**

{{< neo_since ver="8.7.0" />}}

この接続でトランザクションを開始し、その中で`fn`を実行します。コミット・ロールバックの動作は`Client.tx()`と同じです。`Client.connect()`が返した接続など、確保済みの接続でトランザクションを実行する場合に使用します。

{{< callout emoji="⚠️" >}}
トランザクションは、`CREATE TABLE`で作成した通常のトランザクションテーブルでのみ動作します。ログテーブル（`CREATE LOG TABLE`）とタグテーブル（`CREATE TAG TABLE`）はトランザクションに対応していません。`tx()`内でこれらのテーブルに`exec()`や`query()`を実行すると、`MACHCLI-ERR-2362`などのエラーが発生します。
{{< /callout >}}

<h6>構文</h6>

```js
tx(fn)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
const conn = db.connect();
conn.exec('CREATE TABLE IF NOT EXISTS TX_SAMPLE (ID LONG, NAME VARCHAR(100))');

conn.tx(function (tx) {
    tx.exec('INSERT INTO TX_SAMPLE VALUES(?, ?)', 1, 'committed');
});

conn.close();
db.close();
```

**Connection.close()**

接続を閉じます。

<h6>構文</h6>

```js
close()
```

## Rows {#rows}

`Connection.query()`が返す結果セットオブジェクトです。

**Rows.message**

クエリの実行結果メッセージです。

**Rows.isFetchable()**

行を取得できる結果かどうかを返します。

<h6>構文</h6>

```js
isFetchable()
```

**Rows.next()**

イテレーターの結果オブジェクトを返します。

- 行がある場合は`{ value: Row, done: false }`
- 完了した場合は`{ done: true }`

<h6>構文</h6>

```js
next()
```

**Rows.close()**

結果セットを閉じます。

<h6>構文</h6>

```js
close()
```

## Row {#row}

取得した行を表すオブジェクトです。

- 各列には、`row.COLUMN_NAME`でアクセスできます。
- `for...of`による反復処理に対応しています。

## queryDatabaseId() {#querydatabaseid}

マウントしたデータベースのバックアップ表領域IDを返します。

- 既定のDB（`''`または`MACHBASEDB`）では`-1`を返す
- データベースが存在しない場合は、例外を発生させます。

<h6>構文</h6>

```js
queryDatabaseId(conn, dbName)
```

## queryTableType() {#querytabletype}

正規化したテーブル名のトークンから、テーブル型コードを返します。

<h6>構文</h6>

```js
queryTableType(conn, names)
```

## TableType {#tabletype}

**stringTableType()**

テーブル型の定数と文字列変換関数です。

<h6>TableTypeの値</h6>

- `Log`, `Fixed`, `Volatile`, `Lookup`, `KeyValue`, `Tag`

<h6>構文</h6>

```js
stringTableType(type)
```

## TableFlag {#tableflag}

**stringTableFlag()**

テーブルフラグの定数と文字列変換関数です。

<h6>TableFlagの値</h6>

- `None`, `Data`, `Rollup`, `Meta`, `Stat`

<h6>構文</h6>

```js
stringTableFlag(flag)
```

**stringTableDescription()**

テーブルの型とフラグを組み合わせた説明文字列を返します。

<h6>構文</h6>

```js
stringTableDescription(type, flag)
```

## ColumnType {#columntype}

**stringColumnType()**

列型の定数と文字列変換関数です。

<h6>主なColumnTypeの値</h6>

- `Short`, `UShort`, `Integer`, `UInteger`, `Long`, `ULong`
- `Float`, `Double`, `Varchar`, `Text`, `Clob`, `Blob`, `Binary`
- `Datetime`, `IPv4`, `IPv6`, `JSON`

<h6>構文</h6>

```js
stringColumnType(columnType)
```

**columnWidth()**

列型の既定の表示幅を返します。

<h6>構文</h6>

```js
columnWidth(columnType, length)
```

## ColumnFlag {#columnflag}

**stringColumnFlag()**

列フラグの定数と文字列変換関数です。

<h6>ColumnFlagの値</h6>

- `TagName`
- `Basetime`
- `Summarized`
- `MetaColumn`

<h6>構文</h6>

```js
stringColumnFlag(flag)
```
