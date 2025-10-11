---
title: Go 클라이언트
type: docs
weight: 63
---

## 조회

### GET

URL 인코딩을 적용해 SQL 쿼리를 만듭니다.

```go
q := url.QueryEscape("select count(*) from M$SYS_TABLES where name = 'TAGDATA'")
```

HTTP GET 메서드를 호출합니다.

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

### POST JSON

클라이언트는 SQL 쿼리를 포함한 JSON 메시지를 전송할 수 있습니다.

SQL 쿼리를 담은 JSON 본문을 준비합니다.

```go {linenos=table,linenostart=12}
queryJson := `{"q":"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}`
```

`Content-Type`을 지정하고 HTTP POST 메서드를 호출합니다.

```go {linenos=table,linenostart=14}
rsp, err := client.Post(addr, "application/json", bytes.NewBufferString(queryJson))
```

**전체 소스 코드**

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

### POST FormData

HTML 폼 데이터로 SQL 쿼리를 전송할 수도 있습니다.

```go
data := url.Values{"q": {"select count(*) from M$SYS_TABLES where name = 'TAGDATA'"}}
rsp, err := client.Post(addr, "application/x-www-form-urlencoded", bytes.NewBufferString(data.Encode()))
```

**전체 소스 코드**

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

## 쓰기

### POST JSON

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

### POST CSV

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

## 예시

{{< callout emoji="📌" >}}
아래 테이블이 존재한다고 가정합니다.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

Go 언어로 RESTful API 클라이언트를 작성하고 싶다면 이 방식을 참고하십시오.

### 코드 설명

쓰기 API의 페이로드를 나타내는 데이터 구조를 정의합니다.

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

HTTP로 데이터를 쓰는 API는 [여기](/neo/api-http/write)에 설명되어 있으며 JSON 페이로드를 기대합니다.

아래 코드처럼 페이로드를 구성하면 한 번의 요청으로 여러 레코드를 저장할 수 있습니다.
`sin`, `cos` 변수는 적절한 `float64` 값으로 초기화되어 있다고 가정합니다.

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

이는 아래와 같은 JSON으로 인코딩되어 쓰기 API에 전달됩니다.


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

HTTP POST 요청으로 서버에 전송합니다.

```go
client := http.Client{}
rsp, err := client.Post("http://127.0.0.1:5654/db/write/EXAMPLE", 
    "application/json", bytes.NewBuffer(content))
```

데이터를 성공적으로 저장하면 서버는 `HTTP 200 OK`를 응답합니다.

### 전체 소스 코드

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
