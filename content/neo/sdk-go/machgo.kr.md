---
title: 순수 Go 네이티브 클라이언트
type: docs
weight: 100
---

## 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하기 위한 순수 Go 클라이언트입니다.
`machcli`와 동일한 API 스타일을 제공하면서 CGo 의존성이 없습니다.
완전한 Go 툴체인으로 네이티브 포트 성능이 필요하다면 `machgo`가 좋은 선택입니다.

### machgo를 사용하는 이유

- **CGo 의존성 없음**: 순수 Go 환경으로 빌드 및 배포 가능
- **네이티브 프로토콜 접근**: Machbase 네이티브 포트(기본 `5656`)로 연결
- **machcli와의 API 호환성**: 동일한 연결/쿼리/어펜더 패턴 재사용 가능
- **운영 친화적**: 컨테이너 환경 및 크로스 플랫폼 Go 배포에 적합

### 사전 요구사항

- **Machbase Neo Server**: 실행 중인 Machbase Neo 서버 인스턴스
- **Go 1.24+**: 최신 Go 버전 권장
- **네트워크 접근**: 네이티브 포트(기본 `5656`) 접근 가능

## 시작하기

### 설치

```sh
go get github.com/machbase/neo-server/v8
```

### Import

API 패키지와 `machgo` 클라이언트 패키지를 import합니다.

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machgo"
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

```go
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

```go
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
리소스 해제를 위해 연결에는 항상 `Close()`를 호출하세요.
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

- `WithBatchMaxRows(rows)`
- `WithBatchMaxBytes(bytes)`
- `WithBatchMaxDelay(duration)`

기본값과 최소값은 다음과 같습니다.

- `WithBatchMaxBytes`: 기본값 `512KB`, 최소값 `4KB`
- `WithBatchMaxRows`: 기본값 `512`, 최소값 `1`
- `WithBatchMaxDelay`: 기본값 `5ms`, 최소값 `1ms`
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
활성 appender를 사용하는 연결에서 일반 쿼리를 함께 실행하지 마세요.
append 워크로드에는 별도 연결을 사용하세요.
{{< /callout >}}

## 전체 예제

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machgo"
)

func main() {
    conf := &machgo.Config{
        Host:         "127.0.0.1",
        Port:         5656,
        MaxOpenConn:  10,
        MaxOpenQuery: 5,
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
