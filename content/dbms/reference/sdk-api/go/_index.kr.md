---
type: docs
title: '17.7.6 Go'
weight: 60
toc: true
---


## machgo


## machgo 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하기 위한 순수 Go 클라이언트입니다.
`machcli`와 동일한 API 스타일을 제공하면서 CGo 의존성이 없습니다.
완전한 Go 툴체인으로 네이티브 포트 성능이 필요하다면 `machgo`가 좋은 선택입니다.

### machgo를 사용하는 이유

- **CGo 의존성 없음**: 순수 Go 환경으로 빌드 및 배포 가능
- **네이티브 프로토콜 접근**: Machbase 네이티브 포트(기본 `5656`)로 연결
- **machcli와의 API 호환성**: 동일한 연결/쿼리/어펜더 패턴 재사용 가능
- **운영 친화적**: 컨테이너 환경 및 크로스 플랫폼 Go 배포에 적합

### 사전 요구사항

- **Machbase server**: native port로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22+**: 최신 Go 버전 권장
- **네트워크 접근**: 네이티브 포트(기본 `5656`) 접근 가능

## machgo 시작하기

### 설치

```sh
go get github.com/machbase/neo-client@latest
```

### Import

API 패키지와 `machgo` 클라이언트 패키지를 import합니다.

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### 설정

`machgo.Config`를 사용해 호스트/포트 및 동시성 옵션을 설정합니다.

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase 서버 호스트
    Port:         5656,          // Machbase 네이티브 포트
    MaxOpenConn:  0,             // 최대 연결 임계값
    MaxOpenQuery: 0,             // 최대 쿼리 동시성 제한
}

// 데이터베이스 인스턴스 생성
// API 사용 방식은 machcli와 동일
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 설정 매개변수

| 매개변수 | 설명 | 값 |
|-----------|-------------|--------|
| `MaxOpenConn` | 최대 오픈 연결 수 | `< 0`: 무제한<br>`0`: CPU 수 × 팩터<br>`> 0`: 지정된 제한 |
| `MaxOpenConnFactor` | MaxOpenConn이 0일 때의 승수 | 기본값: 1.5 |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한<br>`0`: CPU 수 × 팩터<br>`> 0`: 지정된 제한 |
| `MaxOpenQueryFactor` | MaxOpenQuery가 0일 때의 승수 | 기본값: 1.5 |

#### FlowControl 동작

`MaxOpenConn`과 `MaxOpenQuery`는 FlowControl 제한값입니다.
둘 중 하나라도 `-1`로 설정하면 해당 제한이 비활성화됩니다(해당 축의 FlowControl 없음).

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // connection FlowControl 비활성화
    MaxOpenQuery: -1, // query FlowControl 비활성화
}
```

### 연결 설정

```go
ctx := context.Background()
conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    panic(err)
}
defer conn.Close()
```

인증 옵션:

- `api.WithPassword(user, password)`

### 연결 단위 튜닝 옵션

`machgo`는 `Connect()` 호출 시 연결별 오버라이드를 지원합니다.
즉, `machgo.Config`의 전역 기본값은 유지하면서 연결마다 다른 튜닝이 가능합니다.

#### 반복 SQL을 위한 StatementCache

하나의 connection lifetime 동안 동일 SQL을 반복 실행하는 경우,
준비된 statement를 재사용해 성능을 향상할 수 있습니다.

기본 모드는 `machgo.Config.StatementCache`에 설정하고,
연결별로 `api.WithStatementCache(...)`로 재정의할 수 있습니다.

```go  {linenos=table,linenostart=1,hl_lines=[5,16]}
// Connection A: statement 재사용을 적극적으로 사용
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// Connection B: 이 연결에서만 statement 재사용 비활성화
connB, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheOff),
)
if err != nil {
    panic(err)
}
defer connB.Close()
```

#### FetchRows pre-fetch 크기

`FetchRows`는 서버에서 한 번의 fetch 라운드에 미리 받아올 레코드 최대 개수를 제어합니다.
기본값은 `machgo.Config.FetchRows`에 설정하고,
연결별로 `api.WithFetchRows(...)`로 재정의할 수 있습니다.
기본값은 `1000`입니다.

{{< callout type="warning" >}}
워크로드 검증 없이 `FetchRows` 값을 과도하게 크게 또는 작게 설정하지 마십시오.
네트워크 레이턴시와 쿼리 특성에 따라 부적절한 값은 급격한 성능 저하와 메모리 소비 증가를 유발할 수 있습니다.
{{< /callout >}}

```go  {linenos=table,linenostart=1,hl_lines=[5]}
// Connection C: 대량 스캔 워크로드를 위한 큰 pre-fetch
connC, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithFetchRows(5000),
)
if err != nil {
    panic(err)
}
defer connC.Close()
```

{{< callout type="warning" >}}
리소스 해제를 위해 연결에는 항상 `Close()`를 호출하십시오.
{{< /callout >}}

## 데이터베이스 작업

### 단일 행 쿼리 (`QueryRow`)

정확히 한 행을 기대할 때 `QueryRow`를 사용합니다.

```go
var name = "tag1"
var tm time.Time
var val float64

row := conn.QueryRow(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 1`,
    name,
)
if err := row.Err(); err != nil {
    panic(err)
}
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

fmt.Println("name:", name, "time:", tm.Local(), "value:", val)
```

### 다중 행 쿼리 (`Query`)

여러 행 결과를 가져올 때 `Query`를 사용합니다.

```go
rows, err := conn.Query(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 10`,
    "tag1",
)
if err != nil {
    panic(err)
}
defer rows.Close()

for rows.Next() {
    var tm time.Time
    var val float64

    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    fmt.Println("time:", tm.Local(), "value:", val)
}
```

### 데이터 수정 (`Exec`)

INSERT, DELETE, DDL 문 실행에는 `Exec`를 사용합니다.

```go
result := conn.Exec(
    ctx,
    `INSERT INTO example_table VALUES(?, ?, ?)`,
    "tag1", time.Now(), 3.14,
)
if err := result.Err(); err != nil {
    panic(err)
}

fmt.Println("RowsAffected:", result.RowsAffected())
fmt.Println("Message:", result.Message())
```

## 고성능 대량 입력 (`Appender`)

고처리량 입력에는 전용 연결과 함께 `Appender`를 사용합니다.

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

for i := range 10_000 {
    if err := apd.Append("tag1", time.Now(), float64(i)); err != nil {
        panic(err)
    }
}
```

appender는 애플리케이션이 `Append()` 요청한 데이터를 버퍼에 쌓아두다가 지정된 임계값에 도달해야만 서버로 전송합니다.
임계값은 bytes 크기, rows 수, 버퍼에서 가장 오래된 레코드의 인입 시간과 가장 최근 레코드간의 시간 차이를 설정할 수 있으며,
이 중 한 가지라도 임계값을 초과할 경우 버퍼를 서버로 전송합니다.

서버 전송 버퍼 임계값은 아래 옵션으로 조정할 수 있습니다.

- `WithBatchMaxRows(rows)` : 기본값 `512`, 최소값 `1`
- `WithBatchMaxBytes(bytes)` : 기본값 `512KB`, 최소값 `4KB`
- `WithBatchMaxDelay(duration)` : 기본값 `5ms`, 최소값 `1ms`
- `WithBatchMaxDelay(0)`을 설정하면 시간 기반 임계조건을 사용하지 않습니다.

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MB 임계값
    WithBatchMaxRows(2000).            // row 수 임계값
    WithBatchMaxDelay(500 * time.Millisecond) // 최대 지연 임계값
```

Appender flush 예시:

`Flush()`는 프로그래밍 방식으로 flush를 수행하는 메서드입니다.
임계값 기반 자동 flush 동작과 달리, bytes/rows/delay 임계값 설정과 무관하게 현재 버퍼의 레코드를 즉시 서버로 전송합니다.

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

{{< callout type="warning" >}}
활성 appender를 사용하는 연결에서 일반 쿼리를 함께 실행하지 마십시오.
append 워크로드에는 별도 연결을 사용하십시오.
{{< /callout >}}

## 전체 예제

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    conf := &machgo.Config{
        Host:         "127.0.0.1",
        Port:         5656,
        MaxOpenConn:  -1,
        MaxOpenQuery: -1,
    }

    mdb, err := machgo.NewDatabase(conf)
    if err != nil {
        log.Fatal(err)
    }

    ctx := context.Background()
    conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) PRIMARY KEY,
            time DATETIME BASETIME,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    for i := 0; i < 5; i++ {
        result := conn.Exec(
            ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i),
            time.Now(),
            float64(i)*1.5,
        )
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }

    result = conn.Exec(ctx, `EXEC TABLE_FLUSH(sample_data)`)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    rows, err := conn.Query(ctx,
        `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var name string
        var tm time.Time
        var value float64

        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n",
            name, tm.Local().Format(time.RFC3339), value)
    }
}
```

이 워크플로우는 `machcli`와 의도적으로 동일하게 만들어졌으며, 기존 코드를 최소 변경으로 마이그레이션할 수 있습니다.


## Go database/sql 드라이버


## database/sql 개요
`github.com/machbase/neo-client` 패키지는 Machbase용 표준 Go `database/sql` 드라이버를 제공합니다.
이 드라이버는 네이티브 TCP 클라이언트를 기반으로 하며, 네이티브 포트(기본 `5656`)를 사용합니다.

애플리케이션이나 프레임워크가 Go의 `database/sql` 인터페이스를 요구한다면 이 드라이버를 사용하십시오.
`database/sql` 호환이 필요 없는 신규 코드라면 일반적으로 `machgo`가 더 적합합니다.

### 사전 요구사항

- **Machbase server**: native port로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22+**: `github.com/machbase/neo-client`에서 요구
- **계정 정보**: 유효한 Machbase 사용자 계정

## database/sql 시작하기

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
