---
toc: true
title: ブリッジ - SQLite
type: docs
weight: 11
---

## SQLiteブリッジの登録 {#sqlite-브리지-등록}

SQLiteに接続するブリッジを登録します。

```
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
```

SQLiteは、以下のメモリ専用モードにも対応しています。

```
bridge add -t sqlite mem file::memory:?cache=shared
```

以下のコマンドは、図のWeb UIで行う設定と同じです。

{{< figure src="/neo/bridges/img/sqlite-add.png" width="500" >}}


## ブリッジの接続テスト {#브리지-연결-테스트}

```
machbase-neo» bridge test mem;
Test bridge mem connectivity... success 11.917µs
```

{{< figure src="/neo/bridges/img/sqlite-test.png" width="600" >}}

## テーブルの作成 {#테이블-생성}

machbase-neoシェルで、`mem`ブリッジを介して`mem_example`テーブルを作成します。

```sh
bridge exec mem CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
```
標準のSQLエディターでは、`-- env: bridge=<name>`コメントを指定すると、対応するブリッジでSQLを実行できます。
このコメントの設定は、`-- env: reset`でリセットするまで有効です。

```sql
-- env: bridge=mem
CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
-- env: reset
```

{{< figure src="/neo/bridges/img/sqlite-sql-create-table.png" width="600" >}}

## SQLエディターでのDMLの実行 {#sql-에디터에서-dml-수행}

```sql
-- env: bridge=mem
INSERT INTO mem_example(company, employee, created_on) 
    values('Fedel-Gaylord', 12, datetime('now'));

INSERT INTO mem_example(company, employee, created_on) 
    values('Simoni', 23, datetime('now'));

SELECT company, employee, datetime(created_on, 'localtime') from mem_example;

DELETE from mem_example;
-- env: reset
```

{{< figure src="/neo/bridges/img/sqlite-sql-dml.png" width="600" >}}

## TQLによるSQLiteへの書き込み {#sqlite에-tql로-쓰기}

```js {linenos=table,hl_lines=["8-10"],linenostart=1}
FAKE( json({
    ["COMPANY", "EMPLOYEE"],
    ["NovaWave", 10],
    ["Sunflower", 20]
}))

DROP(1) // ヘッダーをスキップ
SQL(bridge("mem"), 
    `insert into mem_example (company, employee, created_on) values(?, ?, ?)`,
    value(0), value(1), time('now'))
```

```
machbase-neo» bridge query mem select * from mem_example;
╭────┬─────────┬──────────┬──────────┬───────┬───────┬──────┬──────────────────────────────────────╮
│ ID │ COMPANY │ EMPLOYEE │ DISCOUNT │ CODE  │ VALID │ MEMO │ CREATED_ON                           │
├────┼─────────┼──────────┼──────────┼───────┼───────┼──────┼──────────────────────────────────────┤
│  1 │ acme    │       10 │ <nil>    │ <nil> │ <nil> │ []   │ 2023-08-10 14:33:08.667491 +0900 KST │
╰────┴─────────┴──────────┴──────────┴───────┴───────┴──────┴──────────────────────────────────────╯
```

## TQLによるSQLiteからの読み取り {#sqlite에서-tql로-읽기}

以下のコードを`sqlite.tql`として保存します。

```js
SQL(bridge('mem'), "select company, employee, created_on from mem_example")
CSV()
```

次に、`curl`コマンドまたはブラウザーでエンドポイントを呼び出します。

```sh
curl -o - http://127.0.0.1:5654/db/tql/sqlite.tql
```

```csv
NovaWave,10,1704866777160399000
Sunflower,20,1704866777160407000
```

## SQLiteとのデータコピー {#sqlite-간-데이터-복사}

次の例は、MachbaseのデータをSQLiteブリッジにコピーする方法を示しています。

**ブリッジ**

以下の設定で`sqlite`ブリッジを定義します。

- 種類： `SQLite`
- 接続文字列： `file:///tmp/sqlite.db`

**SQL**

`/tmp/sqlite.db`にあるSQLiteデータベースに、`example`テーブルを作成します。

```sql
--env: bridge=sqlite
CREATE TABLE IF NOT EXISTS example (
    NAME TEXT,
    TIME DATETIME,
    VALUE REAL
);
-- env: reset
```

**TQL**

以下のTQLスクリプトは、`SQL()`でデータを検索した後、`SQL()`に`bridge("sqlite")`を指定してSQLiteに取り込みます。

```js
SQL(`select name, time, value from example where name = 'my-car'`)
SQL(bridge("sqlite"), 
    `insert into example values(?,?,?)`,
    value(0), value(1), value(2))
```

**SQL**

```sql
--env: bridge=sqlite
SELECT * FROM example order by TIME;
-- env: reset
```
