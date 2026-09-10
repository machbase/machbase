---
toc: true
title: MQTT v5のデータ書き込み
type: docs
weight: 31
---

## MQTT v5のトピック {#mqtt-v5-토픽}

{{< neo_since ver="8.0.33" />}}

MQTT v5では、各メッセージにユーザー定義のプロパティを付加できます。以前のバージョン（MQTT v3.1/v3.1.1）より柔軟で、メッセージに追加のメタデータを含められます。

{{< callout emoji="📌" >}}
注意：ユーザー定義のプロパティを使用せず、MQTT v3.1のトピック構文をMQTT v5でそのまま使用することもできます。
{{< /callout >}}

MQTT v5では、トピックを`db/write/{table}`のように簡単に指定し、以下のユーザープロパティを送信できます。

| ユーザープロパティ  | 既定値  | 値                  |
|:---------------|:--------:|:------------------------|
| format         | `json`   | `csv`, `json`, `ndjson` |
| timeformat     | `ns`     | 時刻の形式：`s`、`ms`、`us`、`ns` |
| tz             | `UTC`    | タイムゾーン：`UTC`、`Local`、地域指定 |
| compress       |          | `gzip`                  |
| method         | `insert` | `insert`, `append`      |
| reply          |          | サーバーが結果メッセージを送信するトピック |
| db             | `MACHBASEDB` | 複数データベース環境で対象データベース名を指定します。 {{< neo_since ver="8.7.0" />}} |


**format=csvの場合の追加プロパティ** 

| ユーザープロパティ  | 既定値  | 値                  |
|:---------------|:--------:|:------------------------|
| delimiter      |`,`       |                         |
| header         |          | `skip`, `columns`       |


{{< callout emoji="📌" >}}
append方式の特性上、`header=columns`は`method=append`と併用できません。
{{< /callout >}}

**複数データベース**

サーバーが複数の名前付きデータベースをホストする場合、`db`ユーザープロパティで対象を指定できます。`method=insert`と`method=append`の両方に適用されます。`db`を省略するか空にすると、既定のデータベース`MACHBASEDB`が対象になります。

トピックの`{table}`部分に、`db.user.table`または`user.table`形式の修飾名を含めることもできます（[MQTT v3.1のデータ書き込み](../write)を参照）。トピックに修飾名がある場合は、常に`db`ユーザープロパティより優先されます。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property db OTHERDB \
    -s << 'EOF'
[ "my-car", 1670380342000000000, 32.1 ]
EOF
```

## APPEND方式 {#append-방식}

MQTTは接続指向のプロトコルであるため、同じセッションを維持してデータを繰り返し送信できます。
これは、HTTPの代わりにMQTTを使用する大きな利点です。

以下は、`mosquitto_pub`を使用したデモです。
このツールは1件のメッセージを発行すると接続を切るため、HTTPの`write` APIより性能が向上しない場合や、遅くなる場合があります。<br/>
この方式は、接続を比較的長く維持し、複数のメッセージを送信できるクライアントで使用してください。

### JSON {#json}

**複数レコードの発行**

以下の例のペイロードは、タプルの配列（JSONでは配列の配列）です。
1つのMQTTメッセージで、複数のレコードをappendします。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property method append \
    -s << 'EOF'
[
    [ "my-car", 1670380342000000000, 32.1 ],
    [ "my-car", 1670380343000000000, 65.4 ],
    [ "my-car", 1670380344000000000, 76.5 ]
]
EOF
```

- JSHアプリ

次のJSHアプリは、JavaScriptからMQTTでMachbase Neoのテーブルに複数のレコードを書き込む方法を示します。
このコードは、独立したJSHスクリプト、またはTQLスクリプトの`SCRIPT()`関数で実行できます。

append方式と配列ペイロードにより、IoTやリアルタイムのデータ収集に適した高いスループットを確保できます。

コードの主要な部分を、以下で順に示します。

```js {linenos=table,linenostart=1,hl_lines=["9-13",25,30]}
// 必要なモジュールをインポートし、
// ポート5653のローカルMQTTブローカーに接続するクライアントを作成します。
const mqtt = require('mqtt');
var conf = { servers: ['tcp://127.0.0.1:5653'] };
var client = new mqtt.Client(conf);
// 送信するレコードの配列を用意します。
// 各レコードは、名前、ミリ秒単位のタイムスタンプ、値を含みます。
const ts = (new Date()).getTime();
var pubPayload = [
    [ "my-car", ts, 32.1 ],
    [ "my-car", (ts+1000), 65.4 ],
    [ "my-car", (ts+2000), 76.5 ],
];
var pubOption = {
    qos:1,
    properties: {
        user:{
            method: 'append',  // appendモードで書き込み
            timeformat: 'ms'   // 時刻の単位はnsではなくms
        }
    }
}
client.on('open', () => {
    // クライアントがブローカーに接続したら、指定したオプションでペイロードを発行します。
    client.publish('db/write/EXAMPLE', pubPayload, pubOption)
});
client.on('published', ()=>{
    // すべてのメッセージの送信完了から500ms後に切断します。
    setTimeout(() => {
        client.close();
    }, 500);
})
```

**単一レコードの発行**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property method append \
    -s << 'EOF'
[ "my-car", 1670380345000000000, 87.6 ]
EOF
```

**gzip圧縮したJSONの発行**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property compress gzip \
    -f mqtt-data.json.gz
```

### NDJSON {#ndjson}

{{< neo_since ver="8.0.33" />}}

NDJSON（Newline Delimited JSON）は、各行が完全なJSONオブジェクトとなるストリーミング形式です。大規模なデータやストリーミングデータの処理に便利です。
各行には、テーブルの列名と一致するフィールドを含める必要があります。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property format ndjson \
    -s << 'EOF'
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
EOF
```

### CSV {#csv}

```sh {hl_lines=[4]}
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property header skip \
    -D PUBLISH user-property timeformat s \
    -s << 'EOF'
NAME,TIME,VALUE
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
EOF
```

強調した`header=skip`オプションは、最初の行がヘッダーであることを示します。

**gzip圧縮したCSVの発行**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method append \
    -D PUBLISH user-property header skip \
    -D PUBLISH user-property timeformat s \
    -D PUBLISH user-property compress gzip \
    -f mqtt-data.csv.gz
```

## INSERT方式 {#insert-방식}

MQTTで性能を最適化するには、append方式を推奨します。
データのフィールド順がテーブルの列順と異なる場合や、一部の列だけを含む場合に、`insert`方式を使用してください。

フィールド数または順序がテーブルと異なる場合は、appendではなく`insert`を使用する必要があります。

### JSON {#json-1}

`db/write`は、SQLの`INSERT INTO table(...) VALUES(...)`と同じように動作します。テーブルの列順と異なる場合や一部の列だけを書き込む場合は、JSONペイロードに列情報を含めてください。

`method`プロパティの既定値は`insert`のため、省略できます。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property method insert \
    -s << 'EOF'
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

`method`プロパティの既定値は`insert`のため、省略できます。

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property method insert \
    -D PUBLISH user-property format ndjson \
    -D PUBLISH user-property timeformat s \
    -s << 'EOF'
{"NAME":"ndjson-data", "TIME":1670380342, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343, "VALUE":2.002}
EOF
```

### CSV {#csv-1}

テーブルの列とフィールド数または順序が異なるCSVデータをINSERT方式で送信するには、MQTT v5のユーザー定義プロパティを使用する必要があります。

```sh {hl_lines=[4]}
mosquitto_pub -h 127.0.0.1 -p 5653 -V 5 -t db/write/EXAMPLE \
    -D PUBLISH user-property format csv \
    -D PUBLISH user-property method insert \
    -D PUBLISH user-property header columns \
    -D PUBLISH user-property timeformat ms \
    -s << 'EOF'
VALUE,NAME,TIME
87.7,my-car,1670380346000
98.6,my-car,1670380347000
99.9,my-car,1670380348000
EOF
```

## TQL {#tql}

`db/tql/{file.tql}`トピックは、TQLファイルの実行に使用します。

データを変換して保存するには、適切な*TQL*スクリプトを用意し、`db/tql/{file.tql}`トピックにデータを発行します。

MQTTと*TQL*でのデータ書き込みについては、[書き込みAPIとしての使用](../../tql/writing)を参照してください。


## メッセージの最大サイズ {#최대-메시지-크기}

MQTT仕様では、PUBLISHメッセージの最大ペイロードサイズは256MBです。悪意のあるクライアントや誤動作したクライアントが大きなメッセージを送り続けると、サーバーのネットワークとリソースを消費し、サービス障害を引き起こす可能性があります。最大メッセージサイズは、クライアントの必要量より少し大きく設定することを推奨します。MQTTの既定の最大メッセージサイズは1MB（`1048576`）です。以下のように、コマンドラインフラグまたは設定ファイルの`MaxMessageSizeLimit`で調整できます。

```sh
machbase-neo serve --mqtt-max-message 1048576
```
