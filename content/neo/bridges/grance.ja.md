---
toc: true
title: ブリッジとサブスクライバー
type: docs
weight: 1
---

## ブリッジ {#브리지}

### ブリッジの登録 {#브리지-등록}

SQLite接続を登録します。

~~~
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
~~~

### 登録済みブリッジの一覧 {#등록된-브리지-조회}

~~~
bridge list
┌──────────┬────────┬────────────────────────┐
│ NAME     │ TYPE   │ CONNECTION             │
├──────────┼────────┼────────────────────────┤
│ sqlitedb │ sqlite │ file:/data/sqlite.db   │
└──────────┴────────┴────────────────────────┘
~~~

### ブリッジでのコマンド実行 {#브리지에서-명령-실행}

~~~
bridge exec sqlitedb CREATE TABLE IF NOT EXISTS example(id INTEGER NOT NULL PRIMARY KEY, name TEXT, age TEXT, address TEXT, UNIQUE(name));
~~~


### ブリッジでのクエリ実行 {#브리지에서-조회-실행}

> `bridge query`コマンドは、「SQL」タイプのブリッジでのみ使用できます。

~~~
bridge query sqlitedb select * from example;

┌────┬────────┬─────┬───────────────┐
│ ID │ NAME   │ AGE │ ADDRESS       │
├────┼────────┼─────┼───────────────┤
│  1 │ hong_1 │ 20  │ address for 1 │
│  2 │ hong_2 │ 20  │ address for 2 │
│  3 │ hong_3 │ 20  │ address for 3 │
└────┴────────┴─────┴───────────────┘
~~~


### TQLの`SQL()`でのブリッジの使用 {#tql-sql에서-브리지-사용}

`SQL()`関数は、`bridge()`オプションで「SQL」タイプのブリッジを指定し、SQL文を実行します。

~~~js
SQL(bridge("sqlitedb"), `select * from example`)
CSV()
~~~

### TQLの`SCRIPT()`でのブリッジの使用 {#tql-script에서-브리지-사용}

以下の例のように、`SCRIPT()`内で`$.db({bridge:"name"})`を呼び出すと、データベースタイプのブリッジにアクセスできます。
この機能はバージョン8.0.27以降で利用できます。

~~~js
SCRIPT({
    err = $.db({bridge:"mem"})
     .query("select company, employee, created_on from mem_example")
     .forEach( function(fields){
        $.yield(fields[0], fields[1], fields[2]);
     })
    if (err !== undefined) {
        console.error("result", ret);
    }
})
CSV()
~~~

### 他のデータベースへのデータコピー {#다른-데이터베이스로-데이터-복사}

次の例は、MachbaseのデータをSQLiteブリッジにコピーする方法を示しています。

**ブリッジ**

以下の設定で`sqlite`ブリッジを定義します。

- 種類： `SQLite`
- 接続文字列： `file:///tmp/sqlite.db`

**SQL**

`/tmp/sqlite.db`にあるSQLiteデータベースに、`example`テーブルを作成します。

~~~sql
--env: bridge=sqlite
CREATE TABLE IF NOT EXISTS example (
    NAME TEXT,
    TIME DATETIME,
    VALUE REAL
);
-- env: reset
~~~

**TQL**

以下のTQLスクリプトは、`SQL()`でデータを検索した後、`bridge("sqlite")`を指定してSQLiteデータベースに取り込みます。

~~~js
SQL(`select name, time, value from example where name = 'my-car'`)
SQL(bridge('sqlite'), `insert into example values(?,?,?)`, value(0), value(1), value(2))
~~~

## サブスクライバー {#구독자}

*サブスクライバー*は、外部のメッセージブローカーに接続してストリーミングメッセージを受信し、TQLスクリプトでデータを取り込みます。

machbase-neoは外部のMQTTブローカーとNATSへの接続に対応しています。Kafkaへの対応は今後の予定です。

最も簡単な使用例は、外部のMQTTブローカーへのブリッジを作成し、①そのブリッジ、②購読するトピック、③メッセージを処理するTQLスクリプトのパスを指定してサブスクライバーを登録する方法です。
その後、machbase-neoはMQTTクライアントとして動作し、メッセージを受信するたびに、指定したTQLスクリプトに渡します。


~~~mermaid
flowchart RL
    external-system --PUBLISH--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        bridge --> subscriber
        subscriber["Subscriber
                    TQL"] --Write--> machbase
        machbase[("machbase
                    engine")]
    end
    subgraph external-system
        direction RL
        client["Client"] --PUBLISH--> mqtt[["MQTT
                                            Broker"]]
    end
~~~

### サブスクライバーの登録 {#구독자-등록}

サブスクライバーを登録します。

**構文：** `subscriber add [options] <name> <bridge> <topic> <tql-path>`

- オプション
    - `--autostart`：machbase-neoの起動時にサブスクライバーを自動的に起動します。自動起動しないモードでは、`subscriber start <name>`と`subscriber stop <name>`で手動操作します。
    - `--qos <int>`：MQTTタイプのブリッジで、トピック購読のQoSレベルを指定します。`0`と`1`に対応し、既定値は`0`です。
    - `--queue <string>`：NATSタイプのブリッジで使用するキューグループを指定します。

- `<name>`      サブスクライバー名
- `<bridge>`    定義済みのブリッジ名（ブローカーのタイプと一致する必要があります）
- `<topic>`     購読するトピック
- `<tql-path>`  受信メッセージを処理するTQLスクリプトのパス


### サブスクライバーの状態確認 {#구독자-상태-확인}

**構文：** `subscriber list`

- `STOP`
- `RUNNING`

### サブスクライバーの開始・停止 {#구독자-시작중지}

**構文：** `subscriber [start | stop] <name>`

### サブスクライバーの削除 {#구독자-삭제}

**構文：** `subscriber del <name>`
