---
title: 브리지 - NATS
type: docs
weight: 31
draft: false
---

NATS 브리지 {{< neo_since ver="8.0.20" />}}를 사용하면 machbase-neo가 NATS 서버(https://nats.io)와 메시지를 주고받을 수 있습니다.

## NATS 서버 브리지 등록

브리지를 등록합니다.

```
bridge add -t nats my_nats server=nats://127.0.0.1:3000 name=client-name;
```

A NATS 브리지는 machbase-neo가 외부 NATS 서버에 연결하는 방법을 정의합니다.
메시지를 수신하려면 아래 구독자 섹션을 참고하십시오.

사용 가능한 연결 옵션은 다음과 같습니다. 자세한 내용은 NATS 공식 문서를 참고하십시오.

| Option           | Description                          |
| :-----------     | :---------------------------------   |
| `Server`         | server address, If the broker has redundant access points, use multiple "broker" options |
| `Name`           | Name is an optional name label which will be sent to the server on CONNECT to identify the client. |
| `NoRandomize`    | NoRandomize configures whether we will randomize the server pool. |
| `NoEcho`         | NoEcho configures whether the server will echo back messages that are sent on this connection if we also have matching subscriptions. Note this is supported on servers >= version 1.2. Proto 1 or greater. |
| `Verbose`        | Verbose signals the server to send an OK ack for commands successfully processed by the server. |
| `Pedantic`       | Pedantic signals the server whether it should be doing further validation of subjects. |
| `AllowReconnect` | AllowReconnect enables reconnection logic to be used when we encounter a disconnect from the current server. |
| `MaxReconnect`   | MaxReconnect sets the number of reconnect attempts that will be tried before giving up. |
| `ReconnectWait`  | ReconnectWait sets the time to backoff after attempting a reconnect to a server that we were already connected to previously. |
| `Timeout`        | Timeout sets the timeout for a Dial operation on a connection. |
| `PingInterval`   | PingInterval is the period at which the client will be sending ping commands to the server, disabled if 0 or negative. (ex: `PingInterval=2m`) |
| `User`           | User sets the username to be used when connecting to the server. |
| `Password`       | Password sets the password to be used when connecting to a server. |
| `Token`          | Token sets the token to be used when connecting to a server. |
| `RetryOnFailedConnect` | sets the connection in reconnecting state right away if it can't connect to a server in the initial set. |
| `SkipHostLookup` | SkipHostLookup skips the DNS lookup for the server hostname. (ex: `SkipHostLookup=true`) |

## 메시지 수신 - 구독자

이제 NATS 서버에서 메시지를 받아 브리지와 구독자를 통해 데이터베이스에 저장하는 예제를 살펴봅니다.

### 1. Run NATS server

NATS 서버 설치가 필요하다면 https://nats.io 를 참고하십시오. 단독 실행 모드 설치는 간단합니다.

```sh
$ nats-server
[61052] 2021/10/28 16:53:38.003205 [INF] Starting nats-server
[61052] 2021/10/28 16:53:38.003329 [INF]   Version:  2.6.1
[61052] 2021/10/28 16:53:38.003333 [INF]   Git:      [not set]
[61052] 2021/10/28 16:53:38.003339 [INF]   Name:     NDUP6JO4T5LRUEXZUHWXMJYMG4IZAJDNWETTA4GPJ7DKXLJUXBN3UP3M
[61052] 2021/10/28 16:53:38.003342 [INF]   ID:       NDUP6JO4T5LRUEXZUHWXMJYMG4IZAJDNWETTA4GPJ7DKXLJUXBN3UP3M
[61052] 2021/10/28 16:53:38.004046 [INF] Listening for client connections on 0.0.0.0:4222
[61052] 2021/10/28 16:53:38.004683 [INF] Server is ready
...
```

### 2. NATS 브리지 등록

machbase-neo 셸에서 아래 명령을 실행합니다.

```
bridge add -t nats my_nats server=nats://127.0.0.1:4222 name=demo;
```

이 명령은 machbase-neo가 NATS 서버에 접속하는 방법을 정의합니다.

```
┌──────────┬──────────┬──────────────────────────────────────────┐
│ NAME     │ TYPE     │ CONNECTION                               │
├──────────┼──────────┼──────────────────────────────────────────┤
│ my_nats  │ nats     │ server=nats://127.0.0.1:4222 name=demo   │
└──────────┴──────────┴──────────────────────────────────────────┘
```

### 3-A. 쓰기 디스크립터를 사용하는 구독자

브리지와 데이터베이스 테이블을 연결할 구독자를 추가합니다.

```
subscriber add --autostart nats_subr my_nats iot.sensor db/append/EXAMPLE:csv;
```

Execute `subscriber list` to confirm.

```
┌───────────┬─────────┬────────────┬───────────────────────┬───────────┬─────────┐
│ NAME      │ BRIDGE  │ TOPIC      │ DESTINATION           │ AUTOSTART │ STATE   │
├───────────┼─────────┼────────────┼───────────────────────┼───────────┼─────────┤
│ NATS_SUBR │ my_nats │ iot.sensor │ db/append/EXAMPLE:csv │ true      │ RUNNING │
└───────────┴─────────┴────────────┴───────────────────────┴───────────┴─────────┘
```

각 항목의 의미는 다음과 같습니다.
- `--autostart`: machbase-neo 시작과 함께 자동 실행합니다. 생략하면 수동 시작/중지가 가능합니다.
- `nats_subr`: 구독자 이름입니다.
- `my_nats`: 사용할 브리지 이름입니다.
- `iot.sensor`: 구독할 NATS subject 이름입니다.
- `db/append/EXAMPLE:csv`: 쓰기 디스크립터로, CSV 데이터를 `EXAMPLE` 테이블에 append 모드로 기록함을 의미합니다.

쓰기 디스크립터 대신 *TQL* 스크립트 경로를 지정할 수도 있습니다. 관련 예시는 뒤에서 다룹니다.

쓰기 디스크립터 형식은 다음과 같습니다.

```
db/{method}/{table_name}:{format}:{compress}?{options}
```

**method**

방법(method)은 `append`, `write` 두 가지이며, NATS와 같이 스트림 환경에서는 `append`를 권장합니다.
- `append`: append 모드로 기록
- `write`: INSERT SQL로 기록

**table_name**

Specify the destination table name, case insensitive.

**format**

- `json` (default)
- `csv`

**compress**

현재는 `gzip`을 지원하며, `:{compress}`를 생략하면 데이터를 압축하지 않습니다.

**options**

추가로 `?` 뒤에 URL 인코딩된 옵션을 지정할 수 있습니다.

| Name          | Default      | Description                                                    |
| :------------ | :----------- | :------------------------------------------------------------- |
| `timeformat`  | `ns`         | Time format: s, ms, us, ns                                     |
| `tz`          | `UTC`        | Time Zone: UTC, Local and location spec                        |
| `delimiter`   | `,`          | CSV delimiter, ignored if content is not csv                   |
| `heading`     | `false`      | If CSV contains header line, set `true` to skip the first line |

> 구독자의 보류 메시지 한도에 대해서는 [nats.io 문서](https://docs.nats.io/running-a-nats-service/nats_admin/slow_consumers#client-configuration)를 참고하십시오.

Examples)

- `db/append/EXAMPLE:csv?timeformat=s&heading=true`
- `db/write/EXAMPLE:csv:gzip?timeformat=s`
- `db/append/EXAMPLE:json?timeformat=2&pendingMsgLimit=1048576`


#### NATS 클라이언트 애플리케이션

이제 NATS 서버의 `iot.sensor` subject로 CSV 데이터를 전송하는 간단한 Go 애플리케이션을 작성해 봅니다.

```go {linenos=table,hl_lines=[33,39],linenostart=1}
package main

import (
	"fmt"
	"strings"
	"time"

	"github.com/nats-io/nats.go"
)

func main() {
    // connect to the NATS server
	opts := nats.GetDefaultOptions()
	opts.Servers = []string{"nats://127.0.0.1:4222"}
	conn, err := opts.Connect()
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	tick := time.Now()

    // make CSV data
    lines := []string{}
	for i := 0; i < 10; i++ {
        // NAME,TIME,VALUE
		line := fmt.Sprintf("hello-nats,%d,3.1415", tick.Add(time.Duration(i)).UnixNano())
		lines = append(lines, line)
	}
	reqData := []byte(strings.Join(lines, "\n"))

	// A) request-respond model
	if rsp, err := conn.Request("iot.sensor", reqData, 100*time.Millisecond); err != nil {
		panic(err)
	} else {
		fmt.Println("RESP:", string(rsp.Data))
	}
	// B) fire-and-forget model
	// if err := conn.Publish("iot.sensor", reqData); err != nil {
	// 	panic(err)
	// }
}
```

이 프로그램을 실행하면 `iot.sensor` subject에 10개의 CSV 레코드가 전송되고,
구독자 `nats_subr`가 이를 받아 `EXAMPLE` 테이블에 저장합니다.

```sh
$ go run nats_pub.go ↵
RESP: {"success":true,"reason":"10 records appended","elapse":"2.186209ms"}
```

### 3-B. TQL을 사용하는 구독자

#### 데이터 작성용 TQL 스크립트

CSV 데이터를 받아 `example` 테이블에 기록하는 TQL을 작성해 `test.tql`로 저장합니다.

```js {linenos=table,hl_lines=[1,4],linenostart=1}
CSV(payload())
MAPVALUE(1, parseTime(value(1), "ns"))
MAPVALUE(2, parseFloat(value(2)))
APPEND( table("example") )
```

machbase-neo 셸에서 브리지와 TQL 스크립트를 연결하는 구독자를 추가합니다.

```
subscriber add --autostart nats_subr my_nats iot.sensor /test.tql;
```

각 항목의 의미는 다음과 같습니다.
- `--autostart`: machbase-neo 시작 시 자동 실행
- `nats_subr`: 구독자 이름
- `my_nats`: 사용할 브리지 이름
- `iot.sensor`: 구독할 subject (NATS 문법 지원)
- `/test.tql`: 수신 데이터를 처리할 TQL 파일 경로

Execute `subscriber list` to confirm.

```
┌───────────┬─────────┬────────────┬─────────────┬───────────┬─────────┐
│ NAME      │ BRIDGE  │ TOPIC      │ DESTINATION │ AUTOSTART │ STATE   │
├───────────┼─────────┼────────────┼─────────────┼───────────┼─────────┤
│ NATS_SUBR │ my_nats │ test.topic │ /test.tql   │ true      │ RUNNING │
└───────────┴─────────┴────────────┴─────────────┴───────────┴─────────┘
```

#### NATS 클라이언트 애플리케이션

앞서 작성한 NATS 클라이언트 애플리케이션을 그대로 실행하면 됩니다.

예제 소스 코드는 [Github](https://github.com/machbase/neo-server/tree/main/examples/go/nats_pub)에서 확인할 수 있습니다.
