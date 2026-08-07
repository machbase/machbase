---
type: docs
title: '11.6 Go'
weight: 60
toc: true
aliases:
  - /dbms/reference/sdk-api/go/
---


## machgo


## machgo 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하기 위한 순수 Go 클라이언트입니다.
Go 표준 도구 체인으로 빌드할 수 있으며 CGo 의존성이 없습니다.
완전한 Go 툴체인으로 네이티브 포트 성능이 필요하다면 `machgo`가 좋은 선택입니다.

## 다중 데이터베이스 <small>Machbase 8.7.0 부터 지원되는 기능</small>

native `machgo`는 `api.WithDatabase("DATABASE_A")`로 연결 직후의 초기 database를
선택할 수 있습니다. 연결 후 SQL `USE`로 current database를 변경할 수도 있으며,
다른 database의 table은 `database.owner.table` 세 부분 이름으로 지정합니다.

`Conn.Appender()`는 세 부분 이름의 대상 database를 조회하고 append-open 전후에
연결의 current database를 보존합니다. 다른 database에 접근하려면 해당 database의
`CONNECT`와 대상 table의 `INSERT` 권한이 필요합니다.

서버가 CMI 4.0.3 database metadata를 제공하는지는 `*machgo.Conn`의
`SupportsDatabaseMetadata()`로 확인할 수 있습니다. 구형 protocol에서는 logical
database ID와 PRIMARY KEY metadata가 제공되지 않을 수 있습니다. 자세한 예제는
[다중 데이터베이스 운영 가이드](/dbms/operations-configuration-recovery/multi-database/#96-go)를
참조하십시오.

### machgo를 사용하는 이유

- **CGo 의존성 없음**: 순수 Go 환경으로 빌드 및 배포 가능
- **네이티브 프로토콜 접근**: Machbase 네이티브 포트(기본 `5656`)로 연결
- **일관된 API**: 연결, 쿼리, 어펜더를 하나의 Go API로 사용
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
conn, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithDatabase("FACTORY_A"),
)
if err != nil {
    panic(err)
}
defer conn.Close()
```

인증 옵션:

- `api.WithPassword(user, password)`
- `api.WithDatabase(database)`: 연결 직후 초기 database 선택

`api.WithDatabase()`는 식별자를 인용한 `USE` 문으로 적용됩니다. database가 없거나
접근 권한이 없으면 연결이 실패합니다. 이후 `USE`로 database를 바꿀 수 있지만,
prepared statement와 cursor는 database를 바꾼 뒤 새로 준비하거나 열어야 합니다.

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

for i := range 10_000 {
    if err := apd.Append("tag1", time.Now(), float64(i)); err != nil {
        panic(err)
    }
}
success, failed, err := apd.Close()
if err != nil {
    panic(err)
}
fmt.Println("appended:", success, "failed:", failed)
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

`machgo`의 연결, 쿼리, 어펜더는 같은 클라이언트 안에서 일관된 방식으로 사용합니다.

## 네이티브 API <small>Machbase 8.7.0 부터 지원되는 기능</small>

### DECIMAL

`api.Decimal`은 부동 소수점 오차 없이 DECIMAL 값을 표현하는 fixed-point 타입입니다.
`api.ParseDecimal`은 지정한 scale보다 많은 소수 자리를 반올림하며, 반올림 방식은 0에서 멀어지는
half-away-from-zero입니다.

- precision 범위: `1`~`65` (`api.DecimalMaxPrecision`)
- scale 범위: `0`~`30`이며 precision보다 클 수 없음
- precision을 초과하는 값, 잘못된 문자열, 범위를 벗어난 precision/scale은 오류
- `String`, `Precision`, `Scale`, `Unscaled`로 값을 확인할 수 있음

```go
price, err := api.ParseDecimal("12.3456", 10, 2)
if err != nil {
    panic(err)
}
fmt.Println(price.String()) // 12.35

result := conn.Exec(ctx,
    `INSERT INTO decimal_table VALUES (?, ?)`,
    "item-1", price,
)
if err := result.Err(); err != nil {
    panic(err)
}
```

### Named bind parameter

네이티브 API에서는 `api.Named(name, value)`로 이름 기반 매개변수를 전달할 수 있습니다.
이름은 대소문자를 구분하고 SQL의 marker 순서와 인자 순서는 달라도 됩니다. 같은 이름을 여러 번
사용한 marker에는 한 번 전달한 값이 적용됩니다.

```go
rows, err := conn.Query(ctx,
    `SELECT name, value FROM example_table
       WHERE name = :name OR value > :threshold`,
    api.Named("threshold", 10.0),
    api.Named("name", "tag1"),
)
if err != nil {
    panic(err)
}
defer rows.Close()
```

이름이 없거나, SQL에 없는 이름을 전달하거나, 같은 이름을 중복 전달하거나, named와 positional
인자를 섞으면 오류가 발생합니다. 한 문장의 매개변수는 최대 256개이며, 구형 protocol에서는
서버 버전에 따라 제한이 더 낮을 수 있습니다.

### NULL과 컬럼 메타데이터

조회 결과의 `api.Column`은 `Nullable`과 `Nullability`를 제공합니다. `Nullability`는
`NullabilityNoNulls`, `NullabilityNullable`, `NullabilityUnknown` 중 하나이며, 서버가
정보를 제공하지 않는 경우 `Unknown`입니다.

NULL을 일반 Go 값으로 scan하면 오류가 발생할 수 있으므로 nullable 대상 타입을 사용합니다.
neo-client는 다음과 같은 표준 nullable 타입을 지원합니다.

| 값 유형 | 지원 대상 타입 |
|---------|----------------|
| 정수 | `sql.Null[int]`, `sql.Null[int16]`, `sql.Null[int32]`, `sql.Null[int64]`, `sql.NullInt16`, `sql.NullInt32`, `sql.NullInt64` |
| 실수 | `sql.Null[float32]`, `sql.Null[float64]`, `sql.NullFloat64` |
| 문자열·시간 | `sql.Null[string]`, `sql.NullString`, `sql.Null[time.Time]`, `sql.NullTime` |
| 바이너리·IP | `sql.Null[[]byte]`, `sql.Null[net.IP]` |
| Machbase 타입 | `sql.Null[api.Decimal]`, `sql.Null[api.JSONString]` |

`Valid=false`인 대상은 NULL을 받으면 값을 zero value로 초기화하고 그대로 invalid 상태로
유지합니다. `sql.Null[bool]`과 unsigned 정수의 generic nullable 대상은 이 경로의 NULL
처리 대상이 아니므로 사용하지 마십시오. `sql.RawBytes`와 `*sql.RawBytes` 입력은
`[]byte` 기반 scan 대상으로 변환할 수 있습니다.

### PRIMARY KEY 메타데이터

`api.Column.PrimaryKey`는 SELECT 결과의 직접 컬럼이 테이블의 PRIMARY KEY인지 나타냅니다.
`Rows.Columns()` 또는 `Row.Columns()`를 호출한 뒤 컬럼별 값을 확인합니다.

```go
rows, err := conn.Query(ctx, `
    SELECT id, amount, id + 1 AS id_expr
      FROM account
     ORDER BY id`)
if err != nil {
    panic(err)
}
defer rows.Close()

columns, err := rows.Columns()
if err != nil {
    panic(err)
}
for _, column := range columns {
    fmt.Printf("%s: primary_key=%t\n", column.Name, column.PrimaryKey)
}
```

위 예제에서 `id`가 PRIMARY KEY인 경우 `id`만 `true`이고 `id_expr`는 `false`입니다. 컬럼
별 메타데이터는 일반 조회, `QueryRow`, prepared statement, statement cache 재사용 경로에서
같은 의미로 전달됩니다. `Appender.Columns()`도 대상 테이블 컬럼의 `PrimaryKey` 상태를
반환합니다. `api.Column.PrimaryKey`는 `Nullability`와 별개의 값이므로 NULL 허용 여부를
사용해 PRIMARY KEY를 추론하지 않습니다.

| 테이블 또는 결과 컬럼 | `PrimaryKey` |
|----------------------|:------------:|
| TRANSACTION·LOOKUP·VOLATILE의 선언된 PK 직접 컬럼 | `true` |
| TAG 테이블의 `NAME` 직접 컬럼 | `true` |
| LOG 테이블의 컬럼 | `false` |
| 별칭을 사용한 직접 컬럼 | 원본 컬럼의 PK 상태 유지 |
| 산술식·함수·집계식·바인드 값·외부 조인 NULL 공급 측 컬럼 | `false` |

Machbase 8.7.0에서 CMI 4.0.3 메타데이터를 협상한 경우 이 값을 사용할 수 있습니다. CMI
4.0.2 이하의 구형 프로토콜에서는 기존 호환성을 위해 PRIMARY KEY 플래그를 전달하지 않습니다.

### TRANSACTION 테이블

`api.TableTypeTransaction`(값 `8`)은 Standard Edition에서 사용하는 TRANSACTION 테이블 타입입니다.
네이티브 API의 `Appender`는 LOG, TAG, TRANSACTION 테이블을 대상으로 사용할 수 있습니다. 네이티브
클라이언트에는 `Begin` 편의 메서드가 없으므로 트랜잭션 제어가 필요하면 연결에서 `BEGIN`,
`COMMIT`, `ROLLBACK` SQL을 직접 실행합니다.

```go
if err := conn.Exec(ctx, "BEGIN").Err(); err != nil {
    panic(err)
}
if err := conn.Exec(ctx,
    `INSERT INTO transaction_table VALUES (?, ?)`, "id-1", 10,
).Err(); err != nil {
    _ = conn.Exec(ctx, "ROLLBACK")
    panic(err)
}
if err := conn.Exec(ctx, "COMMIT").Err(); err != nil {
    panic(err)
}
```

Appender의 batch는 SQL 트랜잭션에 포함되지 않으며 batch 단위로 독립 커밋됩니다. 입력 성공/실패
건수는 `Close()` 결과로 확인하고, 필요한 경우 `Flush()`를 호출합니다.


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
    "time"
    "strings"

    "github.com/machbase/neo-client/api"
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

URL path 또는 query로 초기 database를 지정할 수도 있습니다.

```text
tcp://sys:manager@127.0.0.1:5656/FACTORY_A
tcp://sys:manager@127.0.0.1:5656?database=FACTORY_A
```

#### 지원되는 DSN 키

| 키 | 설명 |
|----|------|
| `server`       | `tcp://user:password@127.0.0.1:5656` 형식의 서버 URL |
| `host`, `port` | 서버 호스트와 포트를 별도로 지정 |
| `user`         | 로그인 사용자 |
| `password`     | 로그인 비밀번호 |
| `database`, `db` | 모든 physical connection에서 사용할 초기 database |
| `fetch_rows`   | 한 번의 round trip에서 가져올 행 수 |
| `statement_cache` | statement cache 모드: `auto`, `on`, `off` |
| `io_metrics`   | I/O metrics 활성화 여부: `true`, `false` |
| `alternative_servers` | `127.0.0.2:5656` 형식의 대체 서버 주소 |
| `alternative_host`, `alternative_port` | 대체 서버 호스트와 포트를 별도로 지정 |

`database`와 `db`는 동의어입니다. URL path, URL query, key-value DSN 모두 같은 초기
database 설정으로 처리되며, 이 설정은 `sql.DB`가 새 physical connection을 만들 때마다
적용됩니다. 연결 후 `USE`로 다른 database를 선택할 수 있지만, pool에 반환할 때 설정된
초기 database로 복원됩니다.

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

## database/sql <small>Machbase 8.7.0 부터 지원되는 기능</small>

### Named bind parameter

`database/sql`에서는 표준 `sql.Named(name, value)`를 사용합니다. 이름은 대소문자를 구분하며,
SQL marker의 순서와 인자 순서는 달라도 됩니다. 같은 이름을 반복해서 사용한 marker에는 한 번
전달한 값이 적용됩니다.

```go
rows, err := db.QueryContext(ctx,
    `SELECT name, value FROM example
       WHERE name = :name OR value > :threshold`,
    sql.Named("threshold", 10.0),
    sql.Named("name", "example-client"),
)
if err != nil {
    panic(err)
}
defer rows.Close()
```

드라이버는 `:name` 형태의 이름 marker를 처리합니다. 이름이 없거나, SQL에
없는 이름을 전달하거나, 같은 이름을 중복 전달하거나, named와 positional 인자를 섞으면 오류가
발생합니다. 한 문장의 named/positional 매개변수는 최대 256개이며, protocol 4.0.3 미만 서버는
최대 255개 제한을 사용할 수 있습니다.

### DECIMAL과 NULL

`api.Decimal`은 `database/sql`의 `driver.Valuer`와 `sql.Scanner`를 구현하므로 DECIMAL 입력과
출력에 사용할 수 있습니다. 정밀도가 필요한 경우 `api.ParseDecimal`로 precision과 scale을
명시해 값을 만듭니다.

```go
amount, err := api.ParseDecimal("123.456", 18, 3)
if err != nil {
    panic(err)
}
if _, err := db.ExecContext(ctx,
    `INSERT INTO decimal_table VALUES (?, ?)`, "item-1", amount,
); err != nil {
    panic(err)
}
```

`Rows.ColumnTypeNullable`로 결과 컬럼의 NULL 허용 여부를 확인할 수 있습니다. 두 번째 반환값이
`false`이면 드라이버가 해당 정보를 알 수 없다는 뜻입니다. 실제 값은 일반 Go 값 대신
`sql.Null[T]`, `sql.NullString`, `sql.NullTime`, `sql.Null[api.Decimal]` 같은 nullable 대상에
scan하십시오.

```go
rows, err := db.QueryContext(ctx, `SELECT value, note FROM decimal_table`)
if err != nil {
    panic(err)
}
defer rows.Close()

for rows.Next() {
    var value sql.Null[api.Decimal]
    var note sql.NullString
    if err := rows.Scan(&value, &note); err != nil {
        panic(err)
    }
}
```

어댑터나 사용자 정의 결과 변환이 필요한 경우 `api.NormalizeType()`은 nullable 포인터를
해제하고 `driver.Value`로 변환합니다. 변환할 수 없는 값은 원래 값을 유지하며, NULL은
`nil`을 반환합니다. `api.NormalizeTypes()`는 같은 규칙을 값 slice 전체에 적용하고 입력
slice를 직접 수정합니다.

```go
values := []any{
    &sql.NullString{String: "ok", Valid: true},
    &sql.NullInt64{Valid: false},
    sql.RawBytes("payload"),
}
values = api.NormalizeTypes(values, time.UTC)
// []any{"ok", nil, []byte("payload")}
```

`database/sql`의 표준 `ColumnType`를 native API의 컬럼 표현으로 변환해야 하면
`api.NewColumnWithType(columnType)`를 사용합니다. 이 함수는 `Name`과 `DataType`을
추론하지만 `Nullable`, `Nullability`, `PrimaryKey` 제약 메타데이터는 복사하거나
추론하지 않습니다.

### PRIMARY KEY 메타데이터

Go 표준 `database/sql.ColumnType`에는 PRIMARY KEY를 반환하는 메서드가 없습니다.
`Rows.ColumnTypeNullable()`은 NULL 허용 여부만 반환하므로 이 값으로 PRIMARY KEY를 추론할 수
없습니다. 결과 컬럼의 PK 상태가 필요하면 네이티브 `machgo`의 `api.Column.PrimaryKey`를
사용하거나 테이블 카탈로그를 별도로 조회합니다.

`database/sql` 드라이버도 CMI 4.0.3 협상과 구형 프로토콜 호환 규칙을 따릅니다. 따라서
구형 프로토콜에서는 결과 컬럼에 PRIMARY KEY 플래그가 노출되지 않습니다.

### 트랜잭션

Standard Edition의 TRANSACTION 테이블을 사용할 때 `database/sql`의 `Begin` 또는 `BeginTx`로
트랜잭션을 시작할 수 있습니다. 기본 isolation level만 지원하며, 사용자 지정 isolation level과 `ReadOnly` 옵션은
지원하지 않습니다.

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
    panic(err)
}

if _, err := tx.ExecContext(ctx,
    `INSERT INTO transaction_table VALUES (?, ?)`, "id-1", 10,
); err != nil {
    _ = tx.Rollback()
    panic(err)
}
if err := tx.Commit(); err != nil {
    panic(err)
}
```

`Commit` 또는 `Rollback`이 완료된 뒤 같은 트랜잭션을 다시 사용하면 `sql.ErrTxDone`이 반환됩니다.
커밋 또는 롤백 전에 모든 `Rows`를 닫아야 합니다. connection pool이 세션을 재사용할 때 미완료
트랜잭션은 자동으로 rollback됩니다. context 취소로 커밋이 실패한 경우 같은 트랜잭션을 다시
커밋하려고 시도하지 마십시오.

표준 `database/sql`의 `sql.DB`와 `sql.Tx`에는 Machbase Append 메서드가 없습니다. 다만
neo-client의 `machbase.Conn`은 선택적 `Appender()` 확장을 제공하므로, `sql.Conn.Raw()`로
physical connection을 고정한 뒤 사용할 수 있습니다. Appender를 닫기 전에 `sql.Conn`을
반납하지 말고, 일반 SQL과 Append에는 별도 연결을 사용하십시오.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machbase"
)

sqlConn, err := db.Conn(context.Background())
if err != nil {
    panic(err)
}
defer sqlConn.Close()

var appender api.Appender
err = sqlConn.Raw(func(raw any) error {
    conn, ok := raw.(*machbase.Conn)
    if !ok {
        return fmt.Errorf("unexpected driver connection type %T", raw)
    }
    appender, err = conn.Appender(context.Background(), "FACTORY_A.SYS.SENSOR_LOG")
    return err
})
if err != nil {
    panic(err)
}

if err := appender.Append("pump-1", time.Now(), 12.5); err != nil {
    panic(err)
}
success, failed, err := appender.Close()
if err != nil {
    panic(err)
}
if failed != 0 {
    panic(fmt.Errorf("append result: success=%d failed=%d", success, failed))
}
```

이 확장은 `database/sql`의 표준 Append 호환성을 추가하는 것이 아니므로, 신규 대량 입력
코드는 native `machgo.Conn.Appender()`를 우선 사용하십시오.

### Prepared statement와 statement cache

`db.PrepareContext`로 만든 statement는 여러 번 실행할 수 있습니다. 드라이버의 statement cache는
연결별로 동작하며, `statement_cache=auto|on|off` DSN 키로 설정합니다. 테이블을 삭제 후 다시
만들었거나 결과 컬럼 타입이 변경된 경우 캐시된 metadata가 갱신되도록 statement를 다시 준비합니다.
`USE`로 session database를 변경한 뒤에도 기존 prepared statement나 cursor를 다른 database의
작업에 재사용하지 말고 새로 준비하거나 열어야 합니다.
`ALTER SESSION SET` 또는 사용자 컨텍스트를 바꾸는 `CONNECT USER`가 실행된 뒤에도 이전
session metadata에 의존하는 statement를 재사용하지 말고 다시 준비하십시오.

## 참고 사항 및 제한 사항

- positional placeholder와 named placeholder를 모두 사용할 수 있지만, 한 문장 안에서 두 방식을
  섞을 수 없습니다. 이름 기반 API는 `sql.Named()`을 사용합니다. 공통 SQL 기능과 SDK별 차이는
  [Named Bind Parameter syntax](../../reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
  참고하십시오.
- `database/sql`의 connection pooling은 일반적인 `sql.DB` 방식대로 동작합니다. DSN에
  `database`/`db`를 지정하면 `USE`로 변경된 session을 pool에 반환할 때 설정된 database로
  복원합니다.
- `LastInsertId()`는 지원하지 않습니다.
- 파라미터 타입은 드라이버 구현을 따릅니다. 일반적인 SQL 타입, `time.Time`, `[]byte`, `net.IP`,
  `api.Decimal`을 지원하지만 `bool` 파라미터는 지원하지 않습니다.
- `BeginTx`에서는 기본 isolation level과 읽기/쓰기 트랜잭션만 지원합니다.
