---
title: Go SQL 드라이버
type: docs
weight: 110
---

## 개요
`github.com/machbase/neo-client` 패키지는 Machbase Neo용 표준 Go `database/sql` 드라이버를 제공합니다.
이 드라이버는 네이티브 TCP 클라이언트를 기반으로 하며, 네이티브 포트(기본 `5656`)를 사용합니다.

애플리케이션이나 프레임워크가 Go의 `database/sql` 인터페이스를 요구한다면 이 드라이버를 사용하세요.
`database/sql` 호환이 필요 없는 신규 코드라면 일반적으로 `machgo`가 더 적합합니다.

### 사전 요구사항

- **Machbase Neo Server**: 네이티브 포트로 접근 가능한 실행 중인 서버
- **Go 1.22+**: `github.com/machbase/neo-client`에서 요구
- **계정 정보**: 유효한 Machbase 사용자 계정

## 시작하기

### 설치

```sh
go get github.com/machbase/neo-client@latest
```

### Import

드라이버 패키지는 blank identifier로 import합니다.
드라이버 이름 `machbase`로 자동 등록되므로 별도의 `sql.Register()` 호출은 필요하지 않습니다.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## 연결

### DSN 형식

가장 간단한 DSN은 `server` 키를 사용하는 방식입니다.

```text
server=tcp://sys:manager@127.0.0.1:5656
```

여기에 세미콜론으로 구분된 옵션을 추가할 수 있습니다.

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### 지원되는 DSN 키

| 키 | 설명 |
|----|------|
| `server`       | `tcp://user:password@127.0.0.1:5656` 형식의 서버 URL |
| `host`, `port` | 서버 호스트와 포트를 별도로 지정 |
| `user`         | 로그인 사용자 |
| `password`     | 로그인 비밀번호 |
| `fetch_rows`   | 한 번의 round trip에서 가져올 행 수 |
| `statement_cache` | statement cache 모드: `auto`, `on`, `off` |
| `io_metrics`   | I/O metrics 활성화 여부: `true`, `false` |
| `alternative_servers` | `127.0.0.2:5656` 형식의 대체 서버 주소 |
| `alternative_host`, `alternative_port` | 대체 서버 호스트와 포트를 별도로 지정 |

## 조회 예제

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
		"io_metrics=true",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()

	rows, err := db.QueryContext(ctx, `SELECT * FROM M$SYS_TABLES ORDER BY NAME`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		panic(err)
	}
	fmt.Println("Columns:", columns)

	var (
		name        string
		typ         int
		dbID        int64
		id          int64
		userID      int
		columnCount int
		flag        int
	)

	for rows.Next() {
		if err := rows.Scan(&name, &typ, &dbID, &id, &userID, &columnCount, &flag); err != nil {
			panic(err)
		}
		fmt.Println(name, typ, dbID, id, userID, columnCount, flag)
	}

	if err := rows.Err(); err != nil {
		panic(err)
	}
}
```

## 입력 예제

다음 예제는 `EXAMPLE`이라는 태그 테이블에 행을 삽입합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()
	ts := time.Now()

	for i := 0; i < 10; i++ {
		result, err := db.ExecContext(
			ctx,
			`INSERT INTO EXAMPLE VALUES (?, ?, ?)`,
			"example-client",
			ts.Add(time.Second*time.Duration(i)),
			3.14*float64(i),
		)
		if err != nil {
			panic(err)
		}

		affected, err := result.RowsAffected()
		if err != nil {
			panic(err)
		}
		fmt.Println("Rows affected:", affected)
	}
}
```

## 참고 사항 및 제한 사항

- 파라미터는 `?` 형태의 positional placeholder를 사용하며, named parameter는 지원하지 않습니다.
- `database/sql`의 connection pooling은 일반적인 `sql.DB` 방식대로 동작합니다.
- 명시적 트랜잭션은 지원하지 않으므로 `Begin`, `BeginTx`는 오류를 반환합니다.
- `LastInsertId()`는 지원하지 않습니다.
- 파라미터 타입은 드라이버 구현을 따릅니다. 일반적인 SQL 타입, `time.Time`, `[]byte`, `net.IP`는 지원하지만 `bool` 파라미터는 지원하지 않습니다.
