---
toc: true
title: Go クライアント
type: docs
weight: 63
---

## 検索 {#조회}

### GET {#get}

URLエンコードしたSQLクエリを作成します。

```go
q := url.QueryEscape("select count(*) from M$SYS_TABLES where name = 'TAGDATA'")
```

HTTP GETメソッドを呼び出します。

```go {linenos=table,hl_lines=[10,11],linenostart=1}
import (
	"fmt"
	"io"
	"net/http"
	"net/url"
)

func main() {
	client := http.Client{}
	q := url.QueryEscape("select count(*) from M$SYS_TABLES where name = 'TAGDATA'")
	rsp, err := client.Get("http://127.0.0.1:5654/db/query?q=" + q)
	if err != nil {
		panic(err)
	}

	body, err := io.ReadAll(rsp.Body)
	if err != nil {
		panic(err)
	}

	content := string(body)

	if rsp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("ERR %s %s", rsp.Status, content))
	}

	fmt.Println(content)
}
```

### POST JSON {#post-json}

クライアントは、SQLクエリを含むJSONメッセージを送信できます。

SQLクエリを含むJSONボディを用意します。

```go {linenos=table,linenostart=12}
queryJson := `{"q":"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}`
```

`Content-Type`を指定して、HTTP POSTメソッドを呼び出します。

```go {linenos=table,linenostart=14}
rsp, err := client.Post(addr, "application/json", bytes.NewBufferString(queryJson))
```

**ソースコード全体**

```go {linenos=table,hl_lines=[12,14],linenostart=1}
package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
)

func main() {
	addr := "http://127.0.0.1:5654/db/query"
	queryJson := `{"q":"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}`
	client := http.Client{}
	rsp, err := client.Post(addr, "application/json", bytes.NewBufferString(queryJson))
	if err != nil {
		panic(err)
	}

	body, err := io.ReadAll(rsp.Body)
	if err != nil {
		panic(err)
	}

	content := string(body)

	if rsp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("ERR %s %s", rsp.Status, content))
	}

	fmt.Println(content)
}
```

### POST FormData {#post-formdata}

HTMLフォームデータでSQLクエリを送信することもできます。

```go
data := url.Values{"q": {"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}}
rsp, err := client.Post(addr, "application/x-www-form-urlencoded", bytes.NewBufferString(data.Encode()))
```

**ソースコード全体**

```go {linenos=table,hl_lines=[13,15],linenostart=1}
package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/url"
)

func main() {
	addr := "http://127.0.0.1:5654/db/query"
	data := url.Values{"q": {"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}}
	client := http.Client{}
	rsp, err := client.Post(addr, "application/x-www-form-urlencoded", bytes.NewBufferString(data.Encode()))
	if err != nil {
		panic(err)
	}

	body, err := io.ReadAll(rsp.Body)
	if err != nil {
		panic(err)
	}

	content := string(body)

	if rsp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("ERR %s %s", rsp.Status, content))
	}

	fmt.Println(content)
}
```

## 書き込み {#쓰기}

### POST JSON {#post-json-1}

```go {linenos=table,hl_lines=["12-17","31-37",39,41],linenostart=1}
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

type WriteRsp struct {
	Success bool         `json:"success"`
	Reason  string       `json:"reason"`
	Elapse  string       `json:"elapse"`
	Data    WriteRspData `json:"data"`
}

type WriteRspData struct {
	AffectedRows uint64 `json:"affectedRows"`
}

func main() {
	addr := "http://127.0.0.1:5654/db/write/TAGDATA"

	rows := [][]any{
		{"my-car", time.Now().UnixNano(), 32.1},
		{"my-car", time.Now().UnixNano(), 65.4},
		{"my-car", time.Now().UnixNano(), 76.5},
	}
	columns := []string{"name", "time", "value", "jsondata"}
	writeReq := map[string]any{
		"data": map[string]any{
			"columns": columns,
			"rows":    rows,
		},
	}

	queryJson, _ := json.Marshal(&writeReq)
	client := http.Client{}
	rsp, err := client.Post(addr, "application/json", bytes.NewBuffer(queryJson))
	if err != nil {
		panic(err)
	}

	body, err := io.ReadAll(rsp.Body)
	if err != nil {
		panic(err)
	}

	content := string(body)

	if rsp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("ERR %s %s", rsp.Status, content))
	}

	fmt.Println(content)
}
```

### POST CSV {#post-csv}

```go {linenos=table,hl_lines=["26-30",33],linenostart=1}
package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

type WriteRsp struct {
	Success bool         `json:"success"`
	Reason  string       `json:"reason"`
	Elapse  string       `json:"elapse"`
	Data    WriteRspData `json:"data"`
}

type WriteRspData struct {
	AffectedRows uint64 `json:"affectedRows"`
}

func main() {
	addr := "http://127.0.0.1:5654/db/write/TAGDATA"

	rows := []string{
		fmt.Sprintf("my-car,%d,32.1", time.Now().UnixNano()),
		fmt.Sprintf("my-car,%d,65.4", time.Now().UnixNano()),
		fmt.Sprintf("my-car,%d,76.5", time.Now().UnixNano()),
	}

	client := http.Client{}
	rsp, err := client.Post(addr, "text/csv", bytes.NewBuffer([]byte(strings.Join(rows, "\n"))))
	if err != nil {
		panic(err)
	}

	body, err := io.ReadAll(rsp.Body)
	if err != nil {
		panic(err)
	}

	content := string(body)

	if rsp.StatusCode != http.StatusOK {
		panic(fmt.Errorf("ERR %s %s", rsp.Status, content))
	}

	fmt.Println(content)
}
```

## 例 {#예시}

{{< callout emoji="📌" >}}
以下のテーブルが存在することを前提とします。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

GoでRESTful APIクライアントを作成する場合は、この方法を参考にしてください。

### コードの説明 {#코드-설명}

書き込みAPIのペイロードを表すデータ構造を定義します。

```go
type WriteReq struct {
    Table string       `json:"table"`
    Data  WriteReqData `json:"data"`
}

type WriteReqData struct {
    Columns []string `json:"columns"`
    Rows    [][]any  `json:"rows"`
}
```

HTTPでデータを書き込むAPIは、[こちら](/neo/api-http/write)で説明しています。JSONペイロードを受け取ります。

以下のようにペイロードを構成すると、1回のリクエストで複数のレコードを保存できます。
`sin`と`cos`は、適切な`float64`値で初期化済みとします。

```go
content, _ := json.Marshal(&WriteReq{
    Data: WriteReqData{
        Columns: []string{"name", "time", "value"},
        Rows: [][]any{
            {"wave.sin", ts.UTC().UnixNano(), sin},
            {"wave.cos", ts.UTC().UnixNano(), cos},
        },
    },
})
```

これは以下のJSONにエンコードされ、書き込みAPIに渡されます。


```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "wave.sin", 1670380342000000000, 1.1 ],
            [ "wave.cos", 1670380343000000000, 2.2 ]
        ]
    }
}
```

HTTP POSTリクエストでサーバーに送信します。

```go
client := http.Client{}
rsp, err := client.Post("http://127.0.0.1:5654/db/write/EXAMPLE", 
    "application/json", bytes.NewBuffer(content))
```

データの保存に成功すると、サーバーは`HTTP 200 OK`を返します。

### ソースコード全体 {#전체-소스-코드}

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"math"
	"net/http"
	"time"
)

type WriteReq struct {
	Table string       `json:"table"`
	Data  WriteReqData `json:"data"`
}

type WriteReqData struct {
	Columns []string `json:"columns"`
	Rows    [][]any  `json:"rows"`
}

func main() {
	client := http.Client{}
	for ts := range time.Tick(500 * time.Millisecond) {
		delta := float64(ts.UnixMilli()%15000) / 15000
		theta := 2 * math.Pi * delta
		sin, cos := math.Sin(theta), math.Cos(theta)

		content, _ := json.Marshal(&WriteReq{
			Table: "EXAMPLE",
			Data: WriteReqData{
				Columns: []string{"name", "time", "value"},
				Rows: [][]any{
					{"wave.sin", ts.UTC().UnixNano(), sin},
					{"wave.cos", ts.UTC().UnixNano(), cos},
				},
			},
		})
		rsp, err := client.Post(
			"http://127.0.0.1:5654/db/write/example",
			"application/json",
			bytes.NewBuffer(content))
		if err != nil {
			panic(err)
		}
		if rsp.StatusCode != http.StatusOK {
			panic(fmt.Errorf("response %d", rsp.StatusCode))
		}
	}
}
```
