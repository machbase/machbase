---
title: Go 클라이언트 튜토리얼
type: docs
weight: 300
---

## 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하는 순수 Go 클라이언트로,
CGo 의존성 없이 고성능 데이터 처리 애플리케이션을 구현할 수 있도록 설계되었습니다.
연결 관리, 쿼리, 어펜더를 포함한 친숙한 API 스타일을 제공합니다.

### machgo를 사용하는 이유는?

- **CGo 의존성 없음**: 순수 Go 툴체인으로 빌드/배포 가능
- **네이티브 프로토콜 접근**: Machbase 네이티브 포트(기본 `5656`)로 연결
- **Go 친화적 API**: Go의 표준 database/sql과 유사한 개발 경험
- **운영 친화적**: 컨테이너 및 크로스 플랫폼 배포에 적합

### 사전 요구사항

- **Machbase Neo Server**: 실행 중인 Machbase Neo 서버 인스턴스
- **Go 1.24+**: 최적의 호환성을 위한 최신 Go 버전

### 설치

```sh
go get github.com/machbase/neo-server/v8
```

## 시작하기

### Import

먼저 필요한 패키지들을 import합니다. `machgo` 패키지는 Machbase용 Go 네이티브 클라이언트를 제공합니다:

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

`Config` 구조체를 사용하여 데이터베이스 연결 매개변수를 설정합니다. 이를 통해 연결 동작과 성능 특성을 사용자 정의할 수 있습니다:

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",    // Machbase 서버 호스트
    Port:         5656,           // Machbase 서버 포트
    MaxOpenConn:  0,              // 최대 연결 임계값
    MaxOpenQuery: 0,              // 최대 쿼리 동시성 제한
}

// 설정으로 데이터베이스 인스턴스 생성
db, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 설정 매개변수

| 매개변수 | 설명 | 값 |
|---------|------|---|
| `MaxOpenConn` | 최대 오픈 연결 수 | `< 0`: 무제한<br>`0`: CPU 수 × 팩터<br>`> 0`: 지정된 제한 |
| `MaxOpenConnFactor` | MaxOpenConn이 0일 때의 승수 | 기본값: 1.5 |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한<br>`0`: CPU 수 × 팩터<br>`> 0`: 지정된 제한 |
| `MaxOpenQueryFactor` | MaxOpenQuery가 0일 때의 승수 | 기본값: 1.5 |

{{< callout type="tip" >}}
**성능 팁**: 고처리량 애플리케이션의 경우 시스템 리소스와 예상 로드 패턴을 기반으로 명시적 제한을 설정하는 것을 고려하세요.
{{< /callout >}}

추가로 연결별 옵션인 `api.WithStatementCache(...)`, `api.WithFetchRows(...)`를 사용해
워크로드 특성에 맞게 튜닝할 수 있습니다.

#### Statement cache와 성능 개선 포인트

`StatementCache`는 동일 connection에서 반복 실행되는 SQL의 prepared statement를 재사용합니다.
반복 SQL 비중이 높은 워크로드에서는 prepare 오버헤드를 줄여 처리량(throughput)과 지연시간(latency)을
함께 개선할 수 있습니다.

대표 사용 패턴:

- **`api.StatementCacheAuto`**: 반복 쿼리/반복 INSERT가 많은 일반적인 서비스에 권장
- **`api.StatementCacheOff`**: SQL 텍스트가 자주 바뀌어 재사용률이 낮은 경우

```go
// 반복 SQL이 많은 연결: statement cache 활성화
connA, err := db.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// 동적 SQL이 많은 연결: 이 연결에서만 cache 비활성화
connB, err := db.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheOff),
)
if err != nil {
    panic(err)
}
defer connB.Close()
```

{{< callout type="tip" >}}
**성능 팁**: 워커가 동일 SQL을 고빈도로 반복 호출하는 구조에서는
`StatementCacheAuto`만으로도 CPU 사용량과 응답 지연이 눈에 띄게 개선될 수 있습니다.
{{< /callout >}}

### 연결 설정

설정된 데이터베이스 인스턴스를 사용하여 Machbase 서버에 연결을 생성합니다:

```go
ctx := context.Background()
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close() // 작업 완료 시 항상 연결을 닫습니다
```

연결은 비밀번호 기반 인증 방법을 지원합니다:
- `api.WithPassword(user, password)`

{{< callout type="warning" >}}
**연결 관리**: 연결이 적절히 해제되도록 항상 `defer conn.Close()`를 사용하세요.
{{< /callout >}}

## 데이터베이스 작업

### 단일 행 쿼리 (QueryRow)

정확히 하나의 결과 행을 예상할 때 `QueryRow`를 사용합니다. 이 메서드는 단일 행 쿼리에 최적화되어 있으며 자동 리소스 정리를 제공합니다:

```go
var name = "tag1"
var tm time.Time
var val float64

// 단일 행을 예상하는 쿼리 실행
row := conn.QueryRow(ctx, 
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY TIME DESC LIMIT 1`, 
    name)

// 쿼리 실행 오류 확인
if err := row.Err(); err != nil {
    panic(err)
}

// 결과를 변수로 스캔
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

// 표시를 위해 로컬 시간대로 변환
tm = tm.In(time.Local)
fmt.Println("name:", name, "time:", tm, "value:", val)
```

**주요 포인트:**
- SQL 인젝션을 방지하기 위해 `?` 플레이스홀더를 사용한 매개변수화된 쿼리 사용
- 스캔하기 전에 항상 `row.Err()` 확인
- `Scan()`은 데이터베이스와 Go 타입 간의 타입 변환을 자동으로 처리

### 다중 행 쿼리 (Query)

여러 행을 검색하려면 `Query`를 사용합니다. 이 메서드는 반복할 수 있는 `Rows` 객체를 반환합니다:

```go
var name = "tag1"
var tm time.Time
var val float64

// 여러 행을 반환할 수 있는 쿼리 실행
rows, err := conn.Query(ctx, 
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY TIME DESC LIMIT 10`, 
    name)
if err != nil {
    panic(err)
}
defer rows.Close() // 중요: 리소스를 해제하기 위해 항상 rows를 닫습니다

// 반환된 모든 행을 반복
for rows.Next() {
    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    tm = tm.In(time.Local)
    fmt.Println("name:", name, "time:", tm, "value:", val)
}
```

**중요 사항:**
- 리소스 누수를 방지하기 위해 항상 `defer rows.Close()` 사용
- `rows.Next()`를 사용한 반복자 패턴은 Go 개발자에게 친숙

### 데이터 수정 (Exec)

INSERT, DELETE, DDL 문에 `Exec`을 사용합니다. 이 메서드는 실행 정보가 포함된 결과 객체를 반환합니다:

```go
var name = "tag1"
var tm = time.Now()
var val = 3.14

// INSERT 문 실행
result := conn.Exec(ctx, 
    `INSERT INTO example_table VALUES(?, ?, ?)`, 
    name, tm, val)

// 실행 오류 확인
if err := result.Err(); err != nil {
    panic(err)
}

// 실행 결과 가져오기
fmt.Println("RowsAffected:", result.RowsAffected()) 
fmt.Println("Message:", result.Message())
```

**사용 사례:**
- **INSERT**: 테이블에 새 레코드 추가
- **DELETE**: 레코드 제거
- **DDL**: 테이블 및 인덱스 생성/변경

### 고성능 대량 삽입 (Appender)

고처리량 데이터 삽입의 경우 `Appender` 인터페이스를 사용합니다. 이는 시계열 데이터 수집에 최적의 성능을 제공합니다:

```go
// 중요: Appender를 위한 별도의 연결을 전용으로 사용
// 활성 Appender가 있는 연결은 다른 작업에 사용해서는 안 됩니다
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close()

// 대상 테이블에 대한 어펜더 생성
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close() // 남은 데이터를 플러시하기 위해 항상 어펜더를 닫습니다

// 고속 대량 삽입
for i := range 10_000 {
    err := apd.Append("tag1", time.Now(), 1.23*float64(i))
    if err != nil {
        panic(err)
    }
}
```

**Appender 모범 사례:**

{{< callout type="warning" >}}
**연결 격리**: 활성 Appender가 있는 연결을 다른 데이터베이스 작업에 절대 사용하지 마세요. 어펜딩을 위한 전용 연결을 생성하세요.
{{< /callout >}}

{{< callout type="tip" >}}
**성능**: Appender는 시계열 워크로드용으로 설계되었으며 적절한 배치 처리로 초당 수백만 건의 삽입을 달성할 수 있습니다.
{{< /callout >}}

- **배치 크기**: Appender는 내부적으로 배치 처리를 자동으로 처리
- **오류 처리**: 중요한 애플리케이션에서는 각 `Append()` 호출의 오류를 확인
- **리소스 정리**: 데이터가 플러시되도록 항상 어펜더를 `Close()`

#### Appender batch 옵션과 튜닝

Appender는 데이터를 메모리 버퍼에 모았다가 임계값에 도달하면 서버로 전송합니다.
임계값은 다음 옵션으로 제어할 수 있습니다.

- `WithBatchMaxRows(rows)`
- `WithBatchMaxBytes(bytes)`
- `WithBatchMaxDelay(duration)`

기본값과 최소값:

- `WithBatchMaxBytes`: 기본 `512KB`, 최소 `4KB`
- `WithBatchMaxRows`: 기본 `512`, 최소 `1`
- `WithBatchMaxDelay`: 기본 `5ms`, 최소 `1ms`
- `WithBatchMaxDelay(0)`: 시간 기반 임계조건 비활성화

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).          // 1MB
    WithBatchMaxRows(2000).                  // row 임계값
    WithBatchMaxDelay(500 * time.Millisecond) // 지연 임계값
```

이 옵션은 성능 튜닝의 핵심입니다.

- 임계값을 키우면 네트워크 왕복이 줄어 처리량 개선에 유리
- 임계값을 줄이면 레코드당 지연시간과 메모리 사용량 제어에 유리

## 완전한 예제

모든 개념을 보여주는 완전한 예제입니다:

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
    // 데이터베이스 연결 설정
    conf := &machgo.Config{
        Host: "127.0.0.1",
        Port: 5656,
        MaxOpenConn: 10,
        MaxOpenQuery: 5,
    }
    
    db, err := machgo.NewDatabase(conf)
    if err != nil {
        panic(err)
    }
    ctx := context.Background()
    
    // 데이터베이스에 연결
    conn, err := db.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()
    
    // 샘플 테이블 생성
    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) primary key,
            time DATETIME basetime,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }
    
    // 샘플 데이터 삽입
    for i := 0; i < 5; i++ {
        result := conn.Exec(ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i), time.Now(), float64(i)*1.5)
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }
    
    // 데이터 쿼리
    rows, err := conn.Query(ctx, `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()
    
    fmt.Println("Retrieved data:")
    for rows.Next() {
        var name string
        var tm time.Time
        var value float64
        
        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        tm = tm.Local()
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n", 
            name, tm.Format(time.RFC3339), value)
    }
}
```

이 예제는 연결 설정부터 데이터 조작까지의 완전한 워크플로우를 보여주며, Machbase와 함께 작업하는 Go 개발자를 위한 권장 패키지 `machgo`의 사용 방법을 보여줍니다.