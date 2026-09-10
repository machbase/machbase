---
toc: true
title: Go クライアント
type: docs
weight: 69
---

## 準備 {#준비}

### Go用paho-mqttのインポート {#go용-paho-mqtt-임포트}

```go
import paho "github.com/eclipse/paho.mqtt.golang"
```

### プロジェクトディレクトリの作成 {#프로젝트-디렉터리-생성}

```sh
mkdir mqtt_client && cd mqtt_client
```

## パブリッシャー {#퍼블리셔}

### クライアント {#클라이언트}

```go {linenos=table,hl_lines=[5]}
	opts := paho.NewClientOptions()
	opts.SetCleanSession(true)
	opts.SetConnectRetry(false)
	opts.SetAutoReconnect(false)
	opts.SetProtocolVersion(4)
	opts.SetClientID("machbase-mqtt-cli")
	opts.AddBroker("127.0.0.1:5653")
	opts.SetKeepAlive(30 * time.Second)

	client := paho.NewClient(opts)
```

### 接続（TLSなし） {#연결-비-tls}

MQTTの平文ソケットでmachbase-neoに接続します。

```go {linenos=table}
	connectToken := client.Connect()
	connectToken.WaitTimeout(1 * time.Second)
	if connectToken.Error() != nil {
		panic(connectToken.Error())
	}
```

### 切断 {#연결-종료}

```go {linenos=table}
client.Disconnect(100)
```

### 発行 {#발행}

```go {linenos=table}
	client.Publish("db/append/TAGDATA", 1, false, []byte(jsonStr))
```

## ソースコード全体 {#전체-소스-코드}

```go
package main

import (
	"fmt"
	"sync"
	"time"

	paho "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	wg := sync.WaitGroup{}

    // paho mqttクライアントのオプション設定
	opts := paho.NewClientOptions()
	opts.SetCleanSession(true)
	opts.SetConnectRetry(false)
	opts.SetAutoReconnect(false)
	opts.SetProtocolVersion(4)
	opts.SetClientID("machbase-mqtt-cli")
	opts.AddBroker("127.0.0.1:5653")
	opts.SetKeepAlive(30 * time.Second)

    // paho mqttクライアントでサーバーに接続します。
	client := paho.NewClient(opts)
	connectToken := client.Connect()
	connectToken.WaitTimeout(1 * time.Second)
	if connectToken.Error() != nil {
		panic(connectToken.Error())
	}

	client.Subscribe("db/reply/#", 1, func(_ paho.Client, msg paho.Message) {
		defer wg.Done()

		buff := msg.Payload()
		str := string(buff)
		fmt.Println("RECV", msg.Topic(), " :", str)
	})

    // テーブルの存在確認
	jsonStr := `{ "q": "select count(*) from M$SYS_TABLES where name = 'TAGDATA'" }`
	wg.Add(1)
	client.Publish("db/query", 1, false, []byte(jsonStr))
	wg.Wait()

    // テーブルの作成
	jsonStr = `{
			"q": "create tag table if not exists TAGDATA (name varchar(200) primary key, time datetime basetime, value double summarized, jstr varchar(80))"
		}`
	wg.Add(1)
	client.Publish("db/query", 1, false, []byte(jsonStr))
	wg.Wait()

    // insertの実行
	jsonStr = `{
			"reply": "db/reply",
			"data": {
				"columns":["name", "time", "value"],
				"rows": [
					[ "my-car", 1670380342000000000, 32.1 ],
					[ "my-car", 1670380343000000000, 65.4 ],
					[ "my-car", 1670380344000000000, 76.5 ]
				]
			}
		}`
    // `db/write/TAGDATA`のように、トピックにテーブル名を指定することもできます。
    // トピックとペイロードの両方にテーブル名を指定すると、ペイロードのテーブル名が優先されます。
	wg.Add(1)
	client.Publish("db/write/TAGDATA", 1, false, []byte(jsonStr))
	wg.Wait()

    // appendの実行
	for i := 0; i < 100; i++ {
        // 次の2つの形式に対応しています。
        // 1) 単一レコード: `[ columns... ]`
        // 2) 複数レコード: `[ [columns...], [columns...] ]`
		jsonStr = fmt.Sprintf(`[ "my-car", %d, %.1f, "{\"speed\":\"%.1fkmh\",\"lat\":37.38906,\"lon\":127.12182}" ]`,
			time.Now().UnixNano(),
			float32(80+i),
			float32(80+i))
		client.Publish("db/append/TAGDATA", 1, false, []byte(jsonStr))
	}

    // selectの実行
	jsonStr = `{ "q":"select count(*) from TAGDATA" }`
	wg.Add(1)
	client.Publish("db/query", 1, false, []byte(jsonStr))
	wg.Wait()

	client.Unsubscribe("db/reply/#")
    // MQTT 切断
	client.Disconnect(100)
}
```
