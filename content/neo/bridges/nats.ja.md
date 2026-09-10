---
toc: true
title: ブリッジ - NATS
type: docs
weight: 31
draft: false
---

NATSブリッジ{{< neo_since ver="8.0.20" />}}を使うと、machbase-neoとNATSサーバー（https://nats.io）の間でメッセージを送受信できます。

## NATSサーバーブリッジの登録 {#nats-서버-브리지-등록}

ブリッジを登録します。

```
bridge add -t nats my_nats server=nats://127.0.0.1:3000 name=client-name;
```

NATSブリッジは、machbase-neoから外部NATSサーバーへの接続方法を定義します。
メッセージの受信については、後述のサブスクライバーを参照してください。

使用できる接続オプションは以下のとおりです。詳細は、NATSの公式ドキュメントを参照してください。

| オプション           | 説明                          |
| :-----------     | :---------------------------------   |
| `Server`         | サーバーアドレス。接続先が冗長化されている場合は、複数の「server」オプションを指定します |
| `Name`           | CONNECT時に、クライアントを識別するためサーバーに送る、省略可能な名前ラベルです。 |
| `NoRandomize`    | サーバープールのランダム化を無効にするかどうかを指定します。 |
| `NoEcho`         | 同じ接続から送信したメッセージに一致する購読がある場合、サーバーからのエコーバックを無効にするかどうかを設定します。サーバーバージョン1.2以降、Proto 1以降で対応します。 |
| `Verbose`        | サーバーが正常に処理したコマンドに、OK ACKを返すように指定します。 |
| `Pedantic`       | サブジェクトを追加検証するかどうかをサーバーに指定します。 |
| `AllowReconnect` | 現在のサーバーから切断された場合の再接続処理を有効にします。 |
| `MaxReconnect`   | 再接続を中止するまでの最大試行回数を設定します。 |
| `ReconnectWait`  | 以前接続していたサーバーへの再接続を試みた後の、待機時間を設定します。 |
| `Timeout`        | 接続のDial操作のタイムアウトを設定します。 |
| `PingInterval`   | クライアントからサーバーへのping送信間隔です。0以下で無効になります（例：`PingInterval=2m`）。 |
| `User`           | サーバーへの接続時に使用するユーザー名を設定します。 |
| `Password`       | サーバーへの接続時に使用するパスワードを設定します。 |
| `Token`          | サーバーへの接続時に使用するトークンを設定します。 |
| `RetryOnFailedConnect` | 初期候補のサーバーに接続できない場合、直ちに再接続状態にします。 |
| `SkipHostLookup` | サーバーホスト名のDNS検索をスキップします（例：`SkipHostLookup=true`）。 |

## メッセージ受信とサブスクライバー {#메시지-수신---구독자}

NATSサーバーからメッセージを受信し、ブリッジとサブスクライバーを介してデータベースに保存する例を示します。

### 1. NATSサーバーの起動 {#1-run-nats-server}

NATSサーバーのインストールは、https://nats.io を参照してください。単独実行モードは簡単にインストールできます。

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

### 2. NATSブリッジの登録 {#2-nats-브리지-등록}

machbase-neoシェルで、以下のコマンドを実行します。

```
bridge add -t nats my_nats server=nats://127.0.0.1:4222 name=demo;
```

このコマンドは、machbase-neoからNATSサーバーへの接続方法を定義します。

```
┌──────────┬──────────┬──────────────────────────────────────────┐
│ NAME     │ TYPE     │ CONNECTION                               │
├──────────┼──────────┼──────────────────────────────────────────┤
│ my_nats  │ nats     │ server=nats://127.0.0.1:4222 name=demo   │
└──────────┴──────────┴──────────────────────────────────────────┘
```

### 3-A. 書き込み記述子を使用するサブスクライバー {#3-a-쓰기-디스크립터를-사용하는-구독자}

ブリッジとデータベーステーブルを関連付けるサブスクライバーを追加します。

```
subscriber add --autostart nats_subr my_nats iot.sensor db/append/EXAMPLE:csv;
```

`subscriber list`で確認します。

```
┌───────────┬─────────┬────────────┬───────────────────────┬───────────┬─────────┐
│ NAME      │ BRIDGE  │ TOPIC      │ DESTINATION           │ AUTOSTART │ STATE   │
├───────────┼─────────┼────────────┼───────────────────────┼───────────┼─────────┤
│ NATS_SUBR │ my_nats │ iot.sensor │ db/append/EXAMPLE:csv │ true      │ RUNNING │
└───────────┴─────────┴────────────┴───────────────────────┴───────────┴─────────┘
```

各項目の意味は以下のとおりです。
- `--autostart`: machbase-neoの起動時に自動起動します。省略すると、手動で開始・停止できます。
- `nats_subr`: サブスクライバー名です。
- `my_nats`: 使用するブリッジ名です。
- `iot.sensor`: 購読するNATSサブジェクト名です。
- `db/append/EXAMPLE:csv`: 書き込み記述子で、CSVデータを`EXAMPLE`テーブルにappendモードで書き込むことを示します。

書き込み記述子の代わりに、*TQL*スクリプトのパスも指定できます。後半で例を示します。

書き込み記述子の形式は以下のとおりです。

```
db/{method}/{table_name}:{format}:{compress}?{options}
```

**method**

方式は`append`と`write`の2つです。NATSなどのストリーミング環境では、`append`を推奨します。
- `append`: appendモードで書き込み
- `write`: INSERT SQLで書き込み

**table_name**

対象テーブル名を指定します。大文字と小文字は区別しません。

**format**

- `json`（既定）
- `csv`

**compress**

現在は`gzip`に対応しています。`:{compress}`を省略すると、データを圧縮しません。

**options**

`?`の後に、URLエンコードした追加オプションを指定できます。

| 名前          | 既定値      | 説明                                                    |
| :------------ | :----------- | :------------------------------------------------------------- |
| `timeformat`  | `ns`         | 時刻の形式：s、ms、us、ns                                     |
| `tz`          | `UTC`        | タイムゾーン：UTC、Local、地域指定                        |
| `delimiter`   | `,`          | CSV区切り文字。CSV以外の場合は無視                   |
| `heading`     | `false`      | CSVにヘッダーがある場合、`true`で先頭行をスキップ |

> サブスクライバーの保留メッセージの上限は、[nats.ioのドキュメント](https://docs.nats.io/running-a-nats-service/nats_admin/slow_consumers#client-configuration)を参照してください。

例：

- `db/append/EXAMPLE:csv?timeformat=s&heading=true`
- `db/write/EXAMPLE:csv:gzip?timeformat=s`
- `db/append/EXAMPLE:json?timeformat=s&pendingMsgLimit=1048576`


#### NATSクライアントアプリケーション {#nats-클라이언트-애플리케이션}

NATSサーバーの`iot.sensor`サブジェクトにCSVデータを送信する、簡単なGoアプリケーションを作成します。

```go {linenos=table,hl_lines=[33,39],linenostart=1}
package main

import (
	"fmt"
	"strings"
	"time"

	"github.com/nats-io/nats.go"
)

func main() {
    // NATSサーバーに接続
	opts := nats.GetDefaultOptions()
	opts.Servers = []string{"nats://127.0.0.1:4222"}
	conn, err := opts.Connect()
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	tick := time.Now()

    // CSVデータを作成
    lines := []string{}
	for i := 0; i < 10; i++ {
        // NAME,TIME,VALUE
		line := fmt.Sprintf("hello-nats,%d,3.1415", tick.Add(time.Duration(i)).UnixNano())
		lines = append(lines, line)
	}
	reqData := []byte(strings.Join(lines, "\n"))

	// A) 要求・応答方式
	if rsp, err := conn.Request("iot.sensor", reqData, 100*time.Millisecond); err != nil {
		panic(err)
	} else {
		fmt.Println("RESP:", string(rsp.Data))
	}
	// B) 応答を待たない送信方式
	// if err := conn.Publish("iot.sensor", reqData); err != nil {
	// 	panic(err)
	// }
}
```

実行すると、`iot.sensor`サブジェクトに10件のCSVレコードが送信され、
`nats_subr`サブスクライバーが受信して、`EXAMPLE`テーブルに保存します。

```sh
$ go run nats_pub.go ↵
RESP: {"success":true,"reason":"10 records appended","elapse":"2.186209ms"}
```

### 3-B. TQLを使用するサブスクライバー {#3-b-tql을-사용하는-구독자}

#### データ書き込み用TQLスクリプト {#데이터-작성용-tql-스크립트}

CSVデータを受信して`example`テーブルに書き込むTQLを作成し、`test.tql`として保存します。

```js {linenos=table,hl_lines=[1,4],linenostart=1}
CSV(payload())
MAPVALUE(1, parseTime(value(1), "ns"))
MAPVALUE(2, parseFloat(value(2)))
APPEND( table("example") )
```

machbase-neoシェルで、ブリッジとTQLスクリプトを関連付けるサブスクライバーを追加します。

```
subscriber add --autostart nats_subr my_nats iot.sensor /test.tql;
```

各項目の意味は以下のとおりです。
- `--autostart`: machbase-neoの起動時に自動起動
- `nats_subr`: サブスクライバー名
- `my_nats`: 使用するブリッジ名
- `iot.sensor`: 購読するサブジェクト（NATS構文に対応）
- `/test.tql`: 受信データを処理するTQLファイルのパス

`subscriber list`で確認します。

```
┌───────────┬─────────┬────────────┬─────────────┬───────────┬─────────┐
│ NAME      │ BRIDGE  │ TOPIC      │ DESTINATION │ AUTOSTART │ STATE   │
├───────────┼─────────┼────────────┼─────────────┼───────────┼─────────┤
│ NATS_SUBR │ my_nats │ test.topic │ /test.tql   │ true      │ RUNNING │
└───────────┴─────────┴────────────┴─────────────┴───────────┴─────────┘
```

#### NATSクライアントアプリケーション {#nats-클라이언트-애플리케이션-1}

前述のNATSクライアントアプリケーションを、そのまま実行します。

```go
package main

import (
	"flag"
	"fmt"
	"strings"
	"time"

	"github.com/nats-io/nats.go"
)

// このプログラムを実行する前に、
//  1. machbase-neoサーバーにブリッジを追加
//     bridge add -t nats my_nats server=127.0.0.1:4222 name=hello
//  2. サブスクライバーを追加
//     subscriber add hello-nats my_nats test.topic db/write/EXAMPLE:csv;
//  3. サブスクライバーを開始
//     subscriber start hello-nats
//  4. Run
//     go run nats_pub.go -server nats://<ip>:<port> -subject hello
func main() {
	optServer := flag.String("server", "nats://127.0.0.1:4222", "nats server address")
	optSubject := flag.String("subject", "hello", "subject to subscribe")
	optRequest := flag.Bool("request", false, "request-response model")
	flag.Parse()

	opts := nats.GetDefaultOptions()
	opts.Servers = []string{*optServer}
	conn, err := opts.Connect()
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	tick := time.Now()
	lines := []string{}
	linesPerMsg := 1
	msgCount := 1000000
	serial := 0

	for n := 0; n < msgCount; n++ {
		for i := 0; i < linesPerMsg; i++ {
			line := fmt.Sprintf("hello-nats,%d,1.2345", tick.Add(time.Duration(serial)*time.Microsecond).UnixNano())
			lines = append(lines, line)
			serial++
		}
		reqData := []byte(strings.Join(lines, "\n"))
		lines = lines[0:0]

		if *optRequest {
			// A) 要求・応答方式
			if rsp, err := conn.Request(*optSubject, reqData, 100*time.Millisecond); err != nil {
				panic(err)
			} else {
				fmt.Println("RESP:", string(rsp.Data))
			}
		} else {
			// B) 応答を待たない送信方式
			if err := conn.Publish(*optSubject, reqData); err != nil {
				panic(err)
			}
		}
	}

	fmt.Println("msg sent: ", conn.OutMsgs)
}
```
