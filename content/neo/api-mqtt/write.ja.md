---
toc: true
title: MQTT v3.1のデータ書き込み
type: docs
weight: 30
---

## MQTT v3.1/v3.1.1のトピック {#mqtt-v31v311-토픽}

データの書き込みには、対象テーブル名を含むトピックを使用します。

JSON以外のペイロード形式を使用する場合は、テーブル名、ペイロード形式、圧縮方式をコロン（`:`）で連結したトピックを使用します。

トピックの完全な形式は以下のとおりです。

```
db/{method}/{table}:{format}:{compress}
```

**method**: 書き込み方式は、`append`と`write`の2種類です。MQTT環境では、通常は`append`を推奨します。
- `append`: appendモードでデータを保存します。
- `write`: SQLの`INSERT`文でデータを保存します。

**format**: 現在、machbase-neoは`json`、`csv`、`ndjson`に対応しており、既定値は`json`です。

**compress**: 現在は`gzip`に対応しています。

**例**

- `db/append/EXAMPLE`は、`EXAMPLE`テーブルにappend方式でJSONペイロードを保存します。

- `db/append/EXAMPLE:json`は上記と同じです。`json`が既定値のため、末尾の`:json`は省略できます。

- `db/append/EXAMPLE:json:gzip`は、`EXAMPLE`テーブルにappend方式でgzip圧縮したJSONを保存します。

- `db/append/EXAMPLE:csv`は、`EXAMPLE`テーブルにappend方式でCSVペイロードを保存します。

- `db/write/EXAMPLE:csv`は、SQLの`INSERT INTO...`で`EXAMPLE`テーブルにCSVペイロードを保存します。

- `db/write/EXAMPLE:csv:gzip`は、SQLの`INSERT INTO...`でgzip圧縮したCSVを保存します。

**複数データベース**

{{< neo_since ver="8.7.0" />}}

MQTT v3.1/v3.1.1のトピック構文には、`db`を指定する専用フィールドはありません。ただし、トピックの`{table}`部分を`db.user.table`または`user.table`形式にすると、その修飾名に基づいて対象を指定できます。修飾名を省略すると、常に既定のデータベース`MACHBASEDB`に保存します。

```
db/append/OTHERDB.SYS.EXAMPLE
```

上記のトピックは、`OTHERDB`データベースの`SYS.EXAMPLE`テーブルにappend方式で保存します。

MQTT v5の`db`ユーザープロパティでも対象データベースを指定できます。ただし、トピックに`db.user.table`の修飾名がある場合は、その値が`db`ユーザープロパティより優先されます。詳細は、[MQTT v5のデータ書き込み](../writev5)を参照してください。


## APPEND方式 {#append-방식}

MQTTは接続指向のプロトコルであるため、同じMQTTセッションを維持してデータを繰り返し送信できます。
これは、HTTPの代わりにMQTTを使用する大きな利点です。

以下は、`mosquitto_pub`を使用したデモです。
このツールは1件のメッセージを発行すると接続を切るため、HTTPの`write` APIより性能が向上しない場合や、遅くなる場合があります。<br/>
この方式は、MQTT接続を比較的長く維持し、複数のメッセージを送信できるクライアントで使用してください。

### JSON {#json}

**複数レコードの発行**

以下の例のペイロードは、タプルの配列（JSONでは配列の配列）です。
1つのMQTTメッセージで、複数のレコードをテーブルにappendします。
以下のように単一のタプルも送信でき、Machbase Neoは両方の形式に対応しています。

```bash
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/append/EXAMPLE -s << 'EOF'
[
    [ "my-car", 1670380342000000000, 32.1 ],
    [ "my-car", 1670380343000000000, 65.4 ],
    [ "my-car", 1670380344000000000, 76.5 ]
]
EOF
```

- JSHアプリ

次のJSHアプリは、JavaScriptからMQTTでMachbase Neoのテーブルに複数のレコードを送信する方法を示します。
このコードは、独立したJSHスクリプト、またはTQLスクリプトの`SCRIPT()`関数で実行できます。

append方式と配列ペイロードにより、大量データを効率的に収集でき、IoTやリアルタイムのデータ収集に適しています。

コードの主要な部分を、以下で順に示します。

```js {linenos=table,linenostart=1,hl_lines=["9-13",17,22]}
// 必要なモジュールをインポートし、
// ポート5653のローカルMQTTブローカーに接続するクライアントを作成します。
const mqtt = require('mqtt');
var conf = { servers: ['tcp://127.0.0.1:5653'] };
var client = new mqtt.Client(conf);
// 送信するレコードの配列を用意します。
// 各レコードは、名前、ナノ秒単位のタイムスタンプ、値を含みます。
const ts = (new Date()).getTime() * 1000000; // ミリ秒をナノ秒に変換
var pubPayload = [
    [ "my-car", ts, 32.1 ],
    [ "my-car", (ts+1000000000), 65.4 ],
    [ "my-car", (ts+2000000000), 76.5 ],
];

client.on('open', () => {
    // クライアントがブローカーに接続したら、指定したオプションで用意したペイロードを発行します。
    client.publish('db/append/EXAMPLE', JSON.stringify(pubPayload))
});
client.on('published', ()=>{
    // すべてのメッセージの送信を確認したら、500ms後に切断します。
    setTimeout(() => {
        client.close();
    }, 500);
})
```

**単一レコードの発行**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/append/EXAMPLE -s << 'EOF'
  [ "my-car", 1670380345000000000, 87.6 ]
EOF
```

**gzip圧縮したJSONの発行**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:json:gzip \
    -f mqtt-data.json.gz
```

### NDJSON {#ndjson}

{{< neo_since ver="8.0.33" />}}

NDJSON（Newline Delimited JSON）は、各行が完全なJSONオブジェクトとなるストリーミング形式です。大規模なデータやストリーミングデータの処理に便利です。
各行は、テーブルの列名と同じフィールド名を含むJSONオブジェクトである必要があります。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/append/EXAMPLE:ndjson -s << 'EOF'
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
EOF
```

### CSV {#csv}

MQTT v3.1には、最初の行がヘッダーかデータかを指定する方法がありません。
そのため、ペイロードにヘッダーを含めず、すべてのフィールドをテーブルの列順に合わせてください。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/append/EXAMPLE:csv -s << 'EOF'
my-car,1670380346000000000,87.7
my-car,1670380347000000000,98.6
my-car,1670380348000000000,99.9
EOF
```

**gzip圧縮したCSVの発行**

Topic = Table + `:csv:gzip`

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:csv:gzip \
    -f mqtt-data.csv.gz
```

## INSERT方式 {#insert-방식}

MQTTで性能を最適化するには、append方式を推奨します。
データのフィールド順がテーブルの列順と異なる場合や、一部の列だけを含む場合に、`insert`方式を使用してください。

フィールド数または順序がテーブルと異なる場合は、既定のappendではなく`insert`方式を使用する必要があります。

### JSON {#json-1}

`db/write/{table}`トピックは、`INSERT`用です。
`db/write`は、SQLの`INSERT INTO table(...) VALUES(...)`と同じように動作します。テーブルの列順と異なる場合や一部の列だけを書き込む場合は、JSONペイロードに列情報を含めてください。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/write/EXAMPLE -s << 'EOF'
{
  "data": {
    "columns": ["name", "time", "value"],
    "rows": [
      [ "wave.pi", 1687481466000000000, 1.2345],
      [ "wave.pi", 1687481467000000000, 3.1415]
    ]
  }
}
EOF
```

### NDJSON {#ndjson-1}

{{< neo_since ver="8.0.33" />}}

このリクエストメッセージは、`INSERT INTO {table} (columns...) VALUES (values...)`文と同じ構造です。

`db/write/{table}:ndjson`トピックは、`INSERT`用です。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/write/EXAMPLE:ndjson -s << 'EOF'
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
EOF
```

### CSV {#csv-1}

テーブルの列とフィールド数や順序が異なるCSVデータをINSERT方式で送信するには、MQTT v5のユーザープロパティを使用する必要があります。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/write/EXAMPLE:csv -s << 'EOF'
my-car,1670380346000000000,87.7
my-car,1670380347000000000,98.6
my-car,1670380348000000000,99.9
EOF
```

## TQL {#tql}

`db/tql/{file.tql}`トピックは、TQLファイルの実行に使用します。

データを変換して保存するには、適切な*TQL*スクリプトを用意し、`db/tql/{file.tql}`トピックにデータを発行します。

MQTTと*TQL*での書き込みについては、[書き込みAPIとしての使用](../../tql/writing)を参照してください。


## メッセージの最大サイズ {#최대-메시지-크기}

MQTT仕様では、PUBLISHメッセージの最大ペイロードサイズは256MBです。悪意のあるクライアントや誤動作したクライアントが大きなメッセージを送り続けると、サーバーのネットワーク帯域とリソースを消費し、サービス障害を引き起こす可能性があります。最大メッセージサイズは、クライアントの必要量より少し大きく設定することを推奨します。MQTTの既定の最大メッセージサイズは1MB（`1048576`）です。以下のように、コマンドラインフラグまたは設定ファイルの`MaxMessageSizeLimit`で調整できます。

```sh
machbase-neo serve --mqtt-max-message 1048576
```
