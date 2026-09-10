---
toc: true
title: MQTTとRDBMSのブリッジ
type: docs
weight: 250
---

このチュートリアルは、外部のMQTTブローカーからJSONデータを受信し、ブリッジ先のデータベースに保存する手順を説明します。

**前提条件**

外部のMQTTブローカーには、`mosquitto`を使用します。
インストールが必要な場合は、[公式サイト](https://mosquitto.org)を参照してください。

この例では、`mosquitto`サーバーが`127.0.0.1:1883`で実行中であることを前提とします。

## TQLファイルの作成 {#tql-파일-생성}

外部のMQTTブローカーから届くメッセージを処理するTQLファイルを作成します。
この段階のスクリプトは、メッセージペイロードを受け取り、破棄する処理だけを行います。

machbase-neoのWeb UIのファイルエクスプローラーで`/mqtt-bridge.tql`を作成し、以下の内容を入力します。

```js
STRING(payload())
DISCARD()
```

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-tql-1.png" width="600" >}}

## MQTTブリッジの定義 {#mqtt-브리지-정의}

machbase-neoに、MQTTブリッジ「mosquitto」を登録します。

- Name: `mosquitto`
- Type: `MQTT`
- Connection String: `broker=127.0.0.1:1883 cleansession=true`

接続文字列のオプションの詳細は、[ドキュメント](/neo/bridges/mqtt/)を参照してください。

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-mqtt.png" width="600" >}}

「Test」ボタンで接続を確認します。エラーが発生した場合は、接続文字列を修正して再試行します。

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-mqtt-test.png" width="600" >}}


## MQTTブリッジへのTQLの関連付け {#mqtt-브리지에-tql-연결}

ブリッジの定義とテスト後、`mosquitto`ブローカーの特定のトピックに`mqtt-bridge.tql`を関連付けられます。

「Test」ボタンの下の「New subscriber」をクリックし、以下のように設定します。

- Name: `mosquitto-sub`
- Topic: `demo/#`
- Destination: 「TQL Script」を選択し、作成したTQLファイルを指定します。

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-sub1.png" width="600" >}}

サブスクライバーを作成し、状態を「RUNNING」に設定します。

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-sub2.png" width="600" >}}

## 接続先DBブリッジの定義 {#대상-db-브리지-정의}

外部データベースに接続するブリッジを追加します。この例ではSQLiteを使用しますが、他のデータベースでも、接続文字列以外の手順は同様です。

- Name: `destdb`
- Type: `SQLite`
- Connection String `file:///tmp/mqtt.db`

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-sqlite.png" width="600" >}}

> 受信データをmachbase-neo内部だけに保存する場合は、外部データベースのブリッジは不要です。

## TQL {#tql}

mosquittoブリッジが`demo/#`トピックでメッセージを受信するたびに実行するTQLコードを作成します。

- 2〜11行目：このJSON文字列はテスト実行に使用します。実際のメッセージがなく、`payload()`がNULLを返す場合、`??`演算子が指定したJSON文字列を代わりに使用します。
- 13行目：`SCRIPT({}, {})`は、JavaScriptを実行するTQL MAP関数です。詳細は、[ドキュメント](/neo/tql/script/)を参照してください。
- 44行目：この例では、SCRIPT MAP関数がすべての処理を行うため、SINKでの追加処理は不要です。TQLはSINK関数で終わる必要があるため、`DISCARD()`を使用します。

```js {linenos=table,hl_lines=["17-22","33-40"],linenostart=1}
STRING( payload() ?? `
    {
    "timestamp": 1732653071807,
        "message": {
            "totalCar": "1",
            "reason": "test",
            "total": "1",
            "resetTime": "2024-01-01T23:00:00Z",
            "scenario": "Scenario 0"
        }
    }
`)
SCRIPT({
    // 初期化コードブロック：
    // このブロックは、新しいメッセージの到着ごとに、
    // 最初のレコードがメインブロックに渡る前に1回実行します。
    err = $.db({bridge:"destdb"}).exec("CREATE TABLE IF NOT EXISTS DATA ("+
        "TS INTEGER,"+
        "TOTAL_CAR INTEGER,"+
        "REASON TEXT,"+
        "TOTAL INTEGER,"+
        "RESET_TIME DATETIME)");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // メインコードブロック：
    // このブロックは、レコードごとに実行します。
    // この例では、メッセージに1件のレコードだけが含まれます。
    //
    // JSONを解析
    obj = JSON.parse($.values[0]);    
    err = $.db({bridge:"destdb"}).exec("INSERT INTO DATA VALUES(?, ?, ?, ?, ?)",
        obj.timestamp,
        parseInt(obj.message.totalCar),
        obj.message.reason,
        parseInt(obj.message.total),
        obj.message.resetTime,
        obj.message.scenario);
    if (err instanceof Error) {
        console.error("Fail to insert into table", err.message);
    }
})
DISCARD()
```


## データの発行 {#데이터-발행}

まず、テスト用のJSONファイルを用意します。

**mqtt-test.json**

```json
{
  "timestamp": 1732653071807,
  "message": {
     "totalCar": "3683",
     "reason": "car",
     "total": "3956",
     "resetTime": "2024-11-25T23:00:00Z",
     "scenario": "Scenario 1"
  }
}
```

`demo/sensor_1`トピックにメッセージを発行します。ペイロードには、作成したファイルの内容を使用します。

```sh
mosquitto_pub -h 127.0.0.1 -p 1883 \
  -t demo/sensor_1 \
  -f ./mqtt-test.json
```

## ブリッジ先DBの検索 {#브리지-db-조회}

接続先データベースにデータが保存されたことを確認します。machbase-neoのSQLエディターで`-- env: bridge=destdb`コメントを使用すると、ブリッジ先DBに直接クエリを実行できます。

```sql
-- env: bridge=destdb
SELECT * FROM DATA;
-- env: reset
```

{{< figure src="/neo/tutorials/img/mqtt-sqlite-bridge-select.png" width="600" >}}
