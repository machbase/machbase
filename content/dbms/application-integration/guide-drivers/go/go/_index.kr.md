---
type: docs
title: 'Go 클라이언트'
weight: 10
---

## 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하기 위한 순수 Go 클라이언트입니다. CGo 의존성이 없으며, `database/sql` 표준 인터페이스 없이 Machbase 고유 API를 직접 사용합니다. 고성능 Append API를 통한 대량 삽입에 최적화되어 있습니다.

### 주요 특징

- **CGo 의존성 없음**: 순수 Go 환경에서 빌드 및 배포 가능
- **네이티브 프로토콜**: Machbase 네이티브 포트(기본 `5656`)로 직접 연결
- **Append API**: 고속 대량 삽입을 위한 전용 인터페이스
- **세밀한 튜닝**: 연결별 FetchRows, StatementCache 설정 가능

## 설치 {#install}

```sh
go get github.com/machbase/neo-client@latest
```

### Import

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

## 데이터베이스 인스턴스 생성 {#database}

`machgo.Config`로 연결 풀 설정을 구성한 뒤 `NewDatabase()`로 인스턴스를 생성합니다.

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase 서버 호스트
    Port:         5656,         // 네이티브 포트
    MaxOpenConn:  0,            // 0: CPU 수 × 팩터(기본 1.5)
    MaxOpenQuery: 0,            // 0: CPU 수 × 팩터(기본 1.5)
}

mdb, err := machgo.NewDatabase(conf)
if err != nil {
    log.Fatal(err)
}
```

### 설정 매개변수

| 매개변수 | 설명 | 값 |
|----------|------|-----|
| `MaxOpenConn` | 최대 오픈 연결 수 | `< 0`: 무제한, `0`: CPU 수 × 팩터, `> 0`: 지정 제한 |
| `MaxOpenConnFactor` | `MaxOpenConn=0`일 때 승수 | 기본값: `1.5` |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한, `0`: CPU 수 × 팩터, `> 0`: 지정 제한 |
| `MaxOpenQueryFactor` | `MaxOpenQuery=0`일 때 승수 | 기본값: `1.5` |
| `FetchRows` | 기본 pre-fetch 레코드 수 | 기본값: `1000` |

## 연결 {#connect}

```go
ctx := context.Background()

conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    log.Fatal(err)
}
defer conn.Close()
```

{{< callout type="warning" >}}
리소스 해제를 위해 연결에는 항상 `Close()`를 호출하세요. `defer conn.Close()` 패턴을 권장합니다.
{{< /callout >}}

### 연결별 튜닝 옵션

`Connect()` 호출 시 전역 설정을 연결별로 재정의할 수 있습니다.

```go
// Statement 캐시 활성화 (동일 SQL 반복 실행 시 성능 향상)
connA, err := mdb.Connect(ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)

// 대량 스캔을 위한 큰 pre-fetch 크기
connB, err := mdb.Connect(ctx,
    api.WithPassword("sys", "manager"),
    api.WithFetchRows(5000),
)
```

## 데이터 조회 {#query}

### 단일 행 조회 (`QueryRow`)

정확히 한 행을 기대할 때 사용합니다.

```go
var name = "sensor-1"
var tm time.Time
var val float64

row := conn.QueryRow(ctx,
    `SELECT time, value FROM sensor_data WHERE name = ? ORDER BY time DESC LIMIT 1`,
    name,
)
if err := row.Err(); err != nil {
    log.Fatal(err)
}
if err := row.Scan(&tm, &val); err != nil {
    log.Fatal(err)
}

fmt.Printf("name=%s, time=%s, value=%.4f\n", name, tm.Local(), val)
```

### 다중 행 조회 (`Query`)

여러 행 결과를 순차적으로 읽을 때 사용합니다.

```go
rows, err := conn.Query(ctx,
    `SELECT name, time, value FROM sensor_data
      WHERE name = ?
      ORDER BY time DESC LIMIT 100`,
    "sensor-1",
)
if err != nil {
    log.Fatal(err)
}
defer rows.Close()

for rows.Next() {
    var name string
    var tm   time.Time
    var val  float64

    if err := rows.Scan(&name, &tm, &val); err != nil {
        log.Fatal(err)
    }
    fmt.Printf("name=%s, time=%s, value=%.4f\n", name, tm.Local(), val)
}
```

## 데이터 수정 (`Exec`) {#exec}

INSERT, DELETE, DDL 실행에는 `Exec`를 사용합니다.

```go
result := conn.Exec(ctx,
    `INSERT INTO sensor_data VALUES (?, ?, ?)`,
    "sensor-1", time.Now(), 3.14,
)
if err := result.Err(); err != nil {
    log.Fatal(err)
}

fmt.Println("RowsAffected:", result.RowsAffected())
```

## 고속 대량 삽입 (Append API) {#appender}

`Appender`는 대용량 시계열 데이터를 고처리량으로 적재하기 위한 전용 인터페이스입니다. 데이터를 버퍼에 쌓아 두었다가 임계값에 도달하면 서버로 일괄 전송합니다.

{{< callout type="warning" >}}
Appender를 사용하는 연결에서는 일반 쿼리를 함께 실행하지 마세요. Append 워크로드에는 반드시 별도 연결을 사용하세요.
{{< /callout >}}

### 기본 사용법

```go
apd, err := conn.Appender(ctx, "sensor_data")
if err != nil {
    log.Fatal(err)
}
defer apd.Close()

for i := range 10_000 {
    if err := apd.Append("sensor-1", time.Now(), float64(i)*0.1); err != nil {
        log.Fatal(err)
    }
}
```

### 버퍼 임계값 설정

임계값 중 하나라도 초과하면 버퍼를 서버로 전송합니다.

```go
apd, err := conn.Appender(ctx, "sensor_data")
if err != nil {
    log.Fatal(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).          // 1 MB 임계값
    WithBatchMaxRows(2000).                   // 2000 행 임계값
    WithBatchMaxDelay(500 * time.Millisecond) // 500ms 시간 임계값
```

| 옵션 | 기본값 | 최소값 | 설명 |
|------|--------|--------|------|
| `WithBatchMaxRows(rows)` | 512 | 1 | 버퍼 내 최대 행 수 |
| `WithBatchMaxBytes(bytes)` | 512KB | 4KB | 버퍼 최대 크기 |
| `WithBatchMaxDelay(duration)` | 5ms | 1ms | 버퍼 내 최장 대기 시간 (`0` 설정 시 시간 조건 비활성화) |

### 수동 Flush

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

## 전체 예제 {#full-example}

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
    // 1. 데이터베이스 인스턴스 생성
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

    // 2. 연결
    conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // 3. 테이블 생성
    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sensor_data (
            name  VARCHAR(100) PRIMARY KEY,
            time  DATETIME BASETIME,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    // 4. 단건 INSERT
    for i := 0; i < 5; i++ {
        r := conn.Exec(ctx,
            `INSERT INTO sensor_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor-%d", i),
            time.Now(),
            float64(i)*1.5,
        )
        if err := r.Err(); err != nil {
            log.Fatal(err)
        }
    }

    // 5. TABLE_FLUSH (태그 테이블 데이터 가시성 확보)
    conn.Exec(ctx, `EXEC TABLE_FLUSH(sensor_data)`)

    // 6. SELECT 조회
    rows, err := conn.Query(ctx,
        `SELECT name, time, value FROM sensor_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var name  string
        var tm    time.Time
        var value float64

        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Name: %-12s  Time: %s  Value: %.2f\n",
            name, tm.Local().Format(time.RFC3339), value)
    }

    // 7. Appender로 대량 삽입
    appendConn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer appendConn.Close()

    apd, err := appendConn.Appender(ctx, "sensor_data")
    if err != nil {
        log.Fatal(err)
    }

    baseTime := time.Now()
    for i := range 10_000 {
        if err := apd.Append(
            fmt.Sprintf("bulk-%d", i%10),
            baseTime.Add(time.Duration(i)*time.Millisecond),
            float64(i)*0.01,
        ); err != nil {
            log.Fatal(err)
        }
    }

    if err := apd.Close(); err != nil {
        log.Fatal(err)
    }
    fmt.Println("Append 완료")
}
```
