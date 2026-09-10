---
toc: true
title: ブリッジ - PostgreSQL
type: docs
weight: 12
---

## PostgreSQLブリッジの登録 {#postgresql-브리지-등록}

PostgreSQLデータベースに接続するブリッジを登録します。

```
bridge add -t postgres pg host=127.0.0.1 port=5432 user=dbuser dbname=postgres sslmode=disable;
```

接続オプションは以下のとおりです。

| オプション            | 説明                                                         | 例         |
| :-----------      | :------------------------------------------------------------ | :-------------  |
| `dbname`          | 接続先のデータベース名                                      |                 |
| `user`            | 接続に使用するユーザー名                                     |                 |
| `password`        | ユーザーのパスワード                                               |                 |
| `host`            | 接続先のホスト。`/`で始まる場合はUnixドメインソケットを表します。既定値はlocalhost | `host=127.0.0.1` |
| `port`            | ポート番号。既定値は`5432`                                    |                 |
| `sslmode`         | SSLの使用（既定値`require`）。下表を参照                 | （以下を参照）     |
| `connect_timeout` | 接続の待機時間（秒）。0または省略した場合は無期限に待機               |                 |
| `sslcert`         | PEM形式の証明書ファイルのパス                                     |                 |
| `sslkey`          | PEM形式の秘密鍵ファイルのパス                                    |                 |
| `sslrootcert`     | PEM形式のルート証明書ファイルのパス                                |                 |

<!-- | `fallback_application_name` | application_name が指定されていない場合の代替名。 | -->

`sslmode`には、以下の値を指定できます。

| sslmode       | 説明                                                                                     |
|:------------  | :----------------------------------------------------------------------------------------|
| `disable`     | SSLを使用しない                                                                           |
| `require`     | 常にSSLを使用する（証明書の検証は省略）                                                          |
| `verify-ca`   | 常にSSLを使用する（サーバー証明書が信頼できるCAによって署名されていることを検証）                 |
| `verify-full` | 常にSSLを使用する（サーバー証明書を検証し、証明書のホスト名と実際のホスト名が一致することを確認） |


## テーブルの作成 {#테이블-생성}

machbase-neoシェルで以下のコマンドを実行し、`pg`ブリッジを介して`pg_example`テーブルを作成します。

```sh
bridge exec pg CREATE TABLE IF NOT EXISTS pg_example(
    id         SERIAL PRIMARY KEY,
    company    VARCHAR(50) UNIQUE NOT NULL,
    employee   INT,
    discount   REAL,
    plan       FLOAT(8),
    code       UUID,
    valid      BOOL,
    memo       TEXT,
    created_on TIMESTAMP NOT NULL
);
```

`psql`コマンドラインツールで、テーブルが作成されたことを確認できます。

```
postgres=# \d pg_example;
                                        Table "public.pg_example"
   Column   |            Type             | Collation | Nullable |                Default                 
------------+-----------------------------+-----------+----------+----------------------------------------
 id         | integer                     |           | not null | nextval('pg_example_id_seq'::regclass)
 company    | character varying(50)       |           | not null | 
 employee   | integer                     |           |          | 
 discount   | real                        |           |          | 
 plan       | real                        |           |          | 
 code       | uuid                        |           |          | 
 valid      | boolean                     |           |          | 
 memo       | text                        |           |          | 
 created_on | timestamp without time zone |           | not null | 
Indexes:
    "pg_example_pkey" PRIMARY KEY, btree (id)
    "pg_example_company_key" UNIQUE CONSTRAINT, btree (company)

```

## TQLによるPostgreSQLへの書き込み {#postgresql에-tql로-쓰기}

現在のJavaScriptランタイムでは、次の例を使用してください。

```js
STRING(payload() ?? `{
  "company": "acme",
  "employee": 10
}`)
SCRIPT({
  // JSONの入力文字列を解析し、現在時刻とともに出力
  const msg = JSON.parse($.values[0]);
  $.yield(msg.company, msg.employee, new Date());
})
INSERT(bridge("pg"), table("pg_example"), "company", "employee", "created_on")
```

<details>
<summary>旧Tengoの例（現在のランタイムでは実行できません）</summary>

```js
BYTES(payload() ?? `{
  "company": "acme",
  "employee": 10
}`)
SCRIPT("tengo", {
  // 現在時刻を取得
  times := import("times")
  ts := times.now()
  // TQLコンテキストを取得
  ctx := import("context")
  val := ctx.value()
  // JSONを解析
  json := import("json")
  msg := json.decode(val[0])
  ctx.yield(msg.company, msg.employee, ts)
})
INSERT(bridge("pg"), table("pg_example"), "company", "employee", "created_on")
```

</details>

```
postgres=# select * from pg_example;
 id | company | employee | discount | plan | code | valid | memo |         created_on         
----+---------+----------+----------+------+------+-------+------+----------------------------
  1 | acme    |       10 |          |      |      |       |      | 2023-08-09 11:05:30.039961
(1 row)
```

## TQLによるPostgreSQLからの読み取り {#postgresql에서-tql로-읽기}

```js
SQL(bridge('pg'), "select * from pg_example")
CSV()
```
