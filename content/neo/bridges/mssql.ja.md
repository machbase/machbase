---
toc: true
title: ブリッジ - MSSQL
type: docs
weight: 15
---

## MSSQLブリッジの登録 {#mssql-브리지-등록}

MSSQLデータベースに接続するブリッジを登録します。

接続文字列はMSSQLの仕様に従います。

```
bridge add -t mssql  ms server=127.0.0.1:1433 user=sa pass=changeme database=master encrypt=disable
```

**接続オプション**

| オプション               | 別名                    | 説明                                              | 例                 |
| :-----------         | :-----------            | :-------------------------------------------------| :-------------          |
| `server`             |                          | MSSQLサーバーのアドレス                                   | `server=127.0.0.1:1433` |
| `database`           |                          | データベース名                                 | `database=master`       |
| `user id`            | `user`, `user-id`        | ユーザー名                                       | `user=sa`               |
| `password`           | `pass`                   | ユーザーのパスワード                                   | `password=changeme`     |
| `connection timeout` | `connection-timeout`     | DB接続の待機時間（秒）                              | `connection-timeout=5`  |
| `dial timeout`       | `dial-timeout`           | TCPハンドシェイクのタイムアウト（秒）                        | `dial-timeout=3`        |
| `app name`           | `app-name`               | アプリケーション名（既定値`neo-bridge`）             |                         |
| `encrypt`            |                          | 暗号化モード（`disable`、`true`、`false`）           | （以下を参照）             |

- `encrypt`
  - `disable` : クライアントとサーバー間のデータを暗号化しません。
  - `false` : ログインパケット以外のデータを暗号化しません。
  - `true` : クライアントとサーバー間のすべてのデータを暗号化します。

```
machbase-neo» bridge list;
╭────────┬──────────┬───────────────────────────────────────────────────────────╮
│ NAME   │ TYPE     │ CONNECTION                                                │
├────────┼──────────┼───────────────────────────────────────────────────────────┤
│ ms     │ mssql    │ server=127.0.0.1:1433 user=SA pass=secret database=master │
╰────────┴──────────┴───────────────────────────────────────────────────────────╯
```

接続テスト

```
machbase-neo» bridge test ms;
Test bridge ms connectivity... success 3.042458ms
```

## テーブルの作成 {#테이블-생성}

machbase-neoシェルで以下のコマンドを実行し、`ms`ブリッジを介して`ms_example`テーブルを作成します。

```sh
bridge exec ms CREATE TABLE ms_example(
    id         INT NOT NULL PRIMARY KEY,
    company    VARCHAR(50) UNIQUE NOT NULL,
    employee   INT,
    discount   REAL,
    pricePlan  NUMERIC(7,2),
    code       BINARY,
    valid      SMALLINT,
    memo       TEXT,
    created_on DATETIME NOT NULL,
    UNIQUE(company)
);
```

```
machbase-neo» bridge query ms select * from ms_example;
╭────┬─────────┬──────────┬──────────┬───────────┬──────┬───────┬──────┬────────────╮
│ ID │ COMPANY │ EMPLOYEE │ DISCOUNT │ PRICEPLAN │ CODE │ VALID │ MEMO │ CREATED_ON │
├────┼─────────┼──────────┼──────────┼───────────┼──────┼───────┼──────┼────────────┤
╰────┴─────────┴──────────┴──────────┴───────────┴──────┴───────┴──────┴────────────╯
```


## TQLによるMSSQLへの書き込み {#mssql에-tql로-쓰기}

現在のJavaScriptランタイムでは、次の例を使用してください。

```js
STRING(payload() ?? `{
  "id":1,
  "company": "acme",
  "employee": 10
}`)
SCRIPT({
  // JSONの入力文字列を解析し、現在時刻とともに出力
  const msg = JSON.parse($.values[0]);
  $.yield(msg.company, msg.employee, new Date());
})
INSERT(bridge("ms"), table("ms_example"), "id", "company", "employee", "created_on")
```

<details>
<summary>旧Tengoの例（現在のランタイムでは実行できません）</summary>

```js
BYTES(payload() ?? `{
  "id":1,
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
  ctx.yield(msg.id, msg.company, msg.employee, ts)
})
INSERT(bridge("ms"), table("ms_example"), "id", "company", "employee", "created_on")
```

</details>

```
machbase-neo» bridge query ms select id, company, employee, created_on from ms_example;
╭────┬─────────┬──────────┬───────────────────────────────────╮
│ ID │ COMPANY │ EMPLOYEE │ CREATED_ON                        │
├────┼─────────┼──────────┼───────────────────────────────────┤
│  1 │ acme    │       10 │ 2023-08-11 20:55:49.527 +0900 KST │
╰────┴─────────┴──────────┴───────────────────────────────────╯
```

## TQLによるMSSQLからの読み取り {#mssql에서-tql로-읽기}

```js
SQL(bridge('ms'), "select * from ms_example")
CSV()
```
