---
title: Go 클라이언트
type: docs
weight: 69
---

## 준비

### Go용 paho-mqtt 임포트

```go
import paho "github.com/eclipse/paho.mqtt.golang"
```

### 프로젝트 디렉터리 생성

```sh
mkdir mqtt_client && cd mqtt_client
```

## 퍼블리셔

### 클라이언트

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

### 연결 (비 TLS)

MQTT 평문 소켓으로 machbase-neo에 연결합니다.

```go {linenos=table}
	connectToken := client.Connect()
	connectToken.WaitTimeout(1 * time.Second)
	if connectToken.Error() != nil {
		panic(connectToken.Error())
	}
```

### 연결 종료

```go {linenos=table}
client.Disconnect(100)
```

### 발행

```go {linenos=table}
	client.Publish("db/append/TAGDATA", 1, false, []byte(jsonStr))
```

## 전체 소스 코드

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

    // paho mqtt 클라이언트 옵션 설정
	opts := paho.NewClientOptions()
	opts.SetCleanSession(true)
	opts.SetConnectRetry(false)
	opts.SetAutoReconnect(false)
	opts.SetProtocolVersion(4)
	opts.SetClientID("machbase-mqtt-cli")
	opts.AddBroker("127.0.0.1:5653")
	opts.SetKeepAlive(30 * time.Second)

    // paho mqtt 클라이언트로 서버에 연결합니다.
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

    // 테이블 존재 여부 확인
	jsonStr := `{ "q": "select count(*) from M$SYS_TABLES where name = 'TAGDATA'" }`
	wg.Add(1)
	client.Publish("db/query", 1, false, []byte(jsonStr))
	wg.Wait()

    // 테이블 생성
	jsonStr = `{
			"q": "create tag table if not exists TAGDATA (name varchar(200) primary key, time datetime basetime, value double summarized, jstr varchar(80))"
		}`
	wg.Add(1)
	client.Publish("db/query", 1, false, []byte(jsonStr))
	wg.Wait()

    // insert 실행
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
    // `db/write/TAGDATA`처럼 토픽에 테이블명을 지정할 수도 있습니다.
    // 토픽과 페이로드 모두에 테이블명을 지정하면 페이로드의 테이블명이 우선합니다.
	wg.Add(1)
	client.Publish("db/write/TAGDATA", 1, false, []byte(jsonStr))
	wg.Wait()

    // append 실행
	for i := 0; i < 100; i++ {
        // 두 가지 형식을 모두 지원합니다.
        // 1) 단일 레코드: `[ columns... ]`
        // 2) 다중 레코드: `[ [columns...], [columns...] ]`
		jsonStr = fmt.Sprintf(`[ "my-car", %d, %.1f, "{\"speed\":\"%.1fkmh\",\"lat\":37.38906,\"lon\":127.12182}" ]`,
			time.Now().UnixNano(),
			float32(80+i),
			float32(80+i))
		client.Publish("db/append/TAGDATA", 1, false, []byte(jsonStr))
	}

    // select 실행
	jsonStr = `{ "q":"select count(*) from TAGDATA" }`
	wg.Add(1)
	client.Publish("db/query", 1, false, []byte(jsonStr))
	wg.Wait()

	client.Unsubscribe("db/reply/#")
    // MQTT 연결 종료
	client.Disconnect(100)
}
```
