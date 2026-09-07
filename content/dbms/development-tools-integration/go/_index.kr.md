---
type: docs
title: '11.9 Go'
weight: 90
toc: true
aliases:
  - /dbms/reference/sdk-api/go/
---


## machgo


## machgo 개요

`machgo` 패키지는 Machbase 서버에 직접 연결하는 순수 Go 클라이언트입니다.
Go 표준 도구 체인으로 빌드할 수 있으며 CGo 의존성이 없습니다.
Go 도구 체인으로 빌드하면서 Machbase 전용 API로 연결·조회·대량 입력을 구현할 때
사용합니다. 표준 `database/sql` 인터페이스가 필요한 경우에는 이 페이지 후반의 드라이버
사용법을 참고하십시오.

## 다중 데이터베이스

neo-client v1.8.3 이상은 `api.WithDatabase()`로 연결의 초기 데이터베이스를 선택합니다. 이미
열린 연결에서 전환할 때는 `conn.Exec(ctx, "USE DATABASE_A")`를 실행합니다. 문장,
커서와 Appender는 데이터베이스 선택 후 생성하고, 사용 중인 서버·SDK 조합에서 지원 범위를
검증하십시오.

### machgo를 사용하는 이유

- **CGo 의존성 없음**: 순수 Go 환경으로 빌드 및 배포 가능
- **직접 연결**: Machbase 서버 포트(기본 `5656`)로 연결
- **일관된 API**: 연결, 쿼리, 어펜더를 하나의 Go API로 사용
- **운영 친화적**: 컨테이너 환경 및 크로스 플랫폼 Go 배포에 적합

### 사전 요구사항

- **Machbase 서버**: 네이티브 포트로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22+**: 최신 Go 버전 권장
- **네트워크 접근**: 네이티브 포트(기본 `5656`) 접근 가능

## machgo 시작하기

### 설치

```sh
go get github.com/machbase/neo-client@v1.8.4
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

`machgo.Config`를 사용해 호스트와 포트를 설정합니다.

```go
conf := &machgo.Config{
    Host: "127.0.0.1",
    Port: 5656,
}

// 데이터베이스 인스턴스 생성
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
mdb.SetMaxOpenConns(32)
```

v1.8.4의 `Config.MaxOpenConn`, `MaxOpenQuery`와 factor 필드는 deprecated이며
`NewDatabase()`가 사용하지 않습니다. 연결 수는 생성 뒤 `SetMaxOpenConns()`로 제한하고,
쿼리 동시성은 애플리케이션에서 제어합니다.

### 연결 설정

```go
ctx := context.Background()
conn, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithDatabase("MACHBASEDB"),
)
if err != nil {
    panic(err)
}
defer conn.Close()
```

인증 옵션:

- `api.WithPassword(user, password)`

초기 데이터베이스는 neo-client v1.8.3 이상의 `api.WithDatabase()`로 지정합니다. 이미 열린 같은
연결에서 다른 데이터베이스로 전환하려면 `conn.Exec(ctx, "USE FACTORY_A")`를 실행합니다.

### 연결 단위 튜닝 옵션

`machgo`는 `Connect()` 호출 시 연결별 오버라이드를 지원합니다.
즉, `machgo.Config`의 전역 기본값은 유지하면서 연결마다 다른 튜닝이 가능합니다.

#### 반복 SQL을 위한 StatementCache

하나의 연결 수명 동안 동일 SQL을 반복 실행하는 경우,
준비된 문장을 재사용해 성능을 향상할 수 있습니다.

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

## 공통 예제 schema

이후 네이티브 쿼리·INSERT·Appender 예제는 다음 TAG 테이블을 먼저 생성한 상태를 전제로 합니다.

```sql
CREATE TAG TABLE example_table (
    name VARCHAR(40) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

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
임계값은 바이트 크기, 행 수, 버퍼에서 가장 오래된 레코드의 인입 시간과 가장 최근 레코드간의 시간 차이를 설정할 수 있으며,
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
    if err := flusher.Flush(); err != nil {
        panic(err)
    }
}
```

{{< callout type="warning" >}}
활성 appender를 사용하는 연결에서 일반 쿼리를 함께 실행하지 마십시오.
append 워크로드에는 별도 연결을 사용하십시오.
{{< /callout >}}

### ARRAY와 선택 컬럼 Append

일반 `Appender.Connect(ctx, dsn, table)`에서 컬럼 인자를 생략하고 ARRAY 컬럼 값으로
`api.NewSparseArray()`가 만든 객체를 전달할 수 있습니다. 고정된 요소 선택과는 다릅니다.

```go
if err := appender.Connect(ctx, dsn, "ARRAY_APPEND_FULL_EXAMPLE"); err != nil {
    return err
}
```

`ID LONG, A INT32[4]` 테이블의 입력 순서, 희소 값 구성, 오류 시 Close와 조회 확인은
[일반 Connect 예제](../data-input-load-export/array-append/#go-full-open)를 참고하십시오.

Machbase DBMS 8.7.0의 ARRAY 기능이 포함된
[`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17) 이후의 v2 module
소스는 고정 길이 ARRAY와 선택 대상을 지원합니다. 공개 v2 릴리스가 지정되기 전에는 공개
모듈 버전에 같은 기능이 포함되었다고 가정하지 마십시오.

```go
func appendSelected(ctx context.Context, dsn string) error {
    appender := &client.Appender{}
    if err := appender.Connect(
        ctx,
        dsn,
        "ARRAY_APPEND_EXAMPLE",
        "ID",
        "A[0]",
        "A[3]",
    ); err != nil {
        return err
    }
    if err := appender.Append(int64(1), int32(10), int32(40)); err != nil {
        _, _, _ = appender.Close()
        return err
    }
    success, failed, err := appender.Close()
    if err != nil {
        return err
    }
    if failed != 0 {
        return fmt.Errorf(
            "append result: success=%d failed=%d",
            success,
            failed,
        )
    }
    return nil
}
```

위 예제는 `context`, `fmt`와
`client "github.com/machbase/neo-client/v2"`를 import한 상태를 전제로 합니다.

행마다 다른 위치를 입력할 때는 `api.NewSparseArray()`를 사용합니다. `Array.Set()`,
`Get()`, `Entries()`와 요소 위치를 지정한 Append 대상의 위치는 0부터 시작하는 인덱스입니다. API와 버전
제한은
[Sparse ARRAY와 선택 컬럼 Append API](../data-input-load-export/array-append/)를
참고하십시오.

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
        Host: "127.0.0.1",
        Port: 5656,
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
`api.ParseDecimal`은 지정한 소수 자릿수보다 많은 소수 자리를 반올림하며, 반올림 방식은 0에서 멀어지는
half-away-from-zero입니다.

- 전체 자릿수 범위: `1`~`65` (`api.DecimalMaxPrecision`)
- 소수 자릿수 범위: `0`~`30`이며 전체 자릿수보다 클 수 없음
- 전체 자릿수를 초과하는 값, 잘못된 문자열, 범위를 벗어난 precision/scale은 오류
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
이름은 대소문자를 구분하고 SQL의 자리표시자 순서와 인자 순서는 달라도 됩니다. 같은 이름을 여러 번
사용한 자리표시자에는 한 번 전달한 값이 적용됩니다.

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

이름이 없거나, SQL에 없는 이름을 전달하거나, 같은 이름을 중복 전달하거나, 이름 기반과 위치 기반
인자를 섞으면 오류가 발생합니다. 한 문장의 매개변수는 최대 256개이며, 구형 프로토콜에서는
서버 버전에 따라 제한이 더 낮을 수 있습니다.

### NULL과 컬럼 메타데이터

조회 결과의 `api.Column`은 `Nullable`과 `Nullability`를 제공합니다. `Nullability`는
`NullabilityNoNulls`, `NullabilityNullable`, `NullabilityUnknown` 중 하나이며, 서버가
정보를 제공하지 않는 경우 `Unknown`입니다.

NULL을 일반 Go 값으로 스캔하면 오류가 발생할 수 있으므로 nullable 대상 타입을 사용합니다.
neo-client는 다음과 같은 표준 nullable 타입을 지원합니다.

| 값 유형 | 지원 대상 타입 |
|---------|----------------|
| 정수 | `sql.Null[int]`, `sql.Null[int16]`, `sql.Null[int32]`, `sql.Null[int64]`, `sql.NullInt16`, `sql.NullInt32`, `sql.NullInt64` |
| 실수 | `sql.Null[float32]`, `sql.Null[float64]`, `sql.NullFloat64` |
| 문자열·시간 | `sql.Null[string]`, `sql.NullString`, `sql.Null[time.Time]`, `sql.NullTime` |
| 바이너리·IP | `sql.Null[[]byte]`, `sql.Null[net.IP]` |
| Machbase 타입 | `sql.Null[api.Decimal]`, `sql.Null[api.JSONString]` |

`Valid=false`인 대상은 NULL을 받으면 값을 zero value로 초기화하고 그대로 invalid 상태로
유지합니다. `sql.Null[bool]`과 unsigned 정수의 범용 nullable 대상은 이 경로의 NULL
처리 대상이 아니므로 사용하지 마십시오. `sql.RawBytes`와 `*sql.RawBytes` 입력은
`[]byte` 기반 스캔 대상으로 변환할 수 있습니다.

Machbase SQL의 빈 문자열 리터럴 `''`은 SQL `NULL`입니다. 따라서 이 값을 조회하면 네이티브
`api.Column.Nullability`는 `NullabilityNullable`로, `database/sql`의
`ColumnTypeNullable()`은 `(true, true)`로 보고됩니다. 실제 행은 `sql.NullString` 또는
동등한 nullable 대상에 스캔하십시오.

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
별 메타데이터는 일반 조회, `QueryRow`, 준비된 문장, 문장 캐시 재사용 경로에서
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

Machbase 8.7.0 서버와 해당 버전 SDK를 함께 사용하면 이 값을 사용할 수 있습니다. 이전
버전 서버 또는 SDK와 연결한 경우에는 PRIMARY KEY 플래그가 제공되지 않을 수 있습니다.

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

Appender의 배치는 SQL 트랜잭션에 포함되지 않으며 배치 단위로 독립 커밋됩니다. 입력 성공/실패
건수는 `Close()` 결과로 확인하고, 필요한 경우 `Flush()`를 호출합니다.


## Go database/sql 드라이버


## database/sql 개요
`github.com/machbase/neo-client` 패키지는 Machbase용 표준 Go `database/sql` 드라이버를 제공합니다.
이 드라이버는 네이티브 TCP 클라이언트를 기반으로 하며, 네이티브 포트(기본 `5656`)를 사용합니다.

애플리케이션이나 프레임워크가 Go의 `database/sql` 인터페이스를 요구한다면 이 드라이버를 사용하십시오.
`database/sql` 호환이 필요 없는 신규 코드라면 일반적으로 `machgo`가 더 적합합니다.

### 사전 요구사항

- **Machbase 서버**: 네이티브 포트로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22+**: `github.com/machbase/neo-client`에서 요구
- **계정 정보**: 유효한 Machbase 사용자 계정

## database/sql 시작하기

### 설치

```sh
go get github.com/machbase/neo-client@v1.8.4
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

#### 지원되는 DSN 키

| 키 | 설명 |
|----|------|
| `server`       | `tcp://user:password@127.0.0.1:5656` 형식의 서버 URL |
| `host`, `port` | 서버 호스트와 포트를 별도로 지정 |
| `user`, `uid` | 로그인 사용자 |
| `password`, `pwd` | 로그인 비밀번호 |
| `database`, `db` | 초기 데이터베이스 |
| `auth_mode` | `password` 또는 `challenge` |
| `auth_key_file`, `auth_key_pem` | challenge 인증 개인키 |
| `fetch_rows`   | 한 번의 왕복 통신에서 가져올 행 수 |
| `statement_cache`, `statementcache` | 문장 캐시 모드: `auto`, `on`, `off` |
| `io_metrics`   | I/O 지표 활성화 여부: `true`, `false` |
| `alternative_servers` | `127.0.0.2:5656` 형식의 대체 서버 주소 |

목록에 없는 키는 파싱 오류를 반환합니다. AUTH KEY는 neo-client v1.5.0 이상에서 사용할 수
있으며 개인키를 로그에 기록하지 않습니다.

`database/sql`의 연결 풀에서는 요청마다 다른 물리 연결이 선택될 수 있습니다.
현재 데이터베이스가 유지된다고 가정하지 말고, 다중 데이터베이스가 필요한 애플리케이션은
연결 고정과 `USE` 실행 순서를 실제 SDK 버전에서 검증합니다.

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

단일 `INSERT ... VALUES`가 성공하면 `Result.LastInsertId()`로 입력된 행의 ROWID를 확인할
수 있습니다. 반환 타입이 `int64`이므로 `uint64`로 변환해 ROWID의 64비트 값을 보존합니다.

```go
result, err := db.ExecContext(ctx,
	"INSERT INTO EXAMPLE VALUES (?, ?, ?)",
	"example-client", time.Now(), 3.14)
if err != nil {
	panic(err)
}

value, err := result.LastInsertId()
if err != nil {
	panic(err)
}
rowID := uint64(value)
fmt.Println("ROWID:", rowID)
```

이 기능은 ROWID를 지원하는 Standard Edition에서 사용할 수 있습니다. 배치, Append,
`INSERT ... SELECT`, UPSERT에서는 ROWID를 반환하지 않습니다. 자세한 조건은
[ROWID와 INSERT 결과 ID](/dbms/reference/sql/rowid/)를 참고하십시오.

## database/sql <small>Machbase 8.7.0 부터 지원되는 기능</small>

### Named bind parameter

`database/sql`에서는 표준 `sql.Named(name, value)`를 사용합니다. 이름은 대소문자를 구분하며,
SQL 자리표시자의 순서와 인자 순서는 달라도 됩니다. 같은 이름을 반복해서 사용한 자리표시자에는 한 번
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

드라이버는 `:name` 형태의 이름 자리표시자를 처리합니다. 이름이 없거나, SQL에
없는 이름을 전달하거나, 같은 이름을 중복 전달하거나, 이름 기반과 위치 기반 인자를 섞으면 오류가
발생합니다. Machbase 8.7.0에서 한 문장의 named/positional 매개변수는 최대 256개입니다.
이전 버전 서버에서는 최대 255개로 제한될 수 있습니다.

### DECIMAL과 NULL

`api.Decimal`은 `database/sql`의 `driver.Valuer`와 `sql.Scanner`를 구현하므로 DECIMAL 입력과
출력에 사용할 수 있습니다. 정밀도가 필요한 경우 `api.ParseDecimal`로 전체 자릿수와 소수 자릿수를
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
스캔하십시오.

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

`database/sql`의 표준 `ColumnType`를 네이티브 API의 컬럼 표현으로 변환해야 하면
`api.NewColumnWithType(columnType)`를 사용합니다. 이 함수는 `Name`과 `DataType`을
추론하지만 `Nullable`, `Nullability`, `PrimaryKey` 제약 메타데이터는 복사하거나
추론하지 않습니다.

### PRIMARY KEY 메타데이터

Go 표준 `database/sql.ColumnType`에는 PRIMARY KEY를 반환하는 메서드가 없습니다.
`Rows.ColumnTypeNullable()`은 NULL 허용 여부만 반환하므로 이 값으로 PRIMARY KEY를 추론할 수
없습니다. 결과 컬럼의 PK 상태가 필요하면 네이티브 `machgo`의 `api.Column.PrimaryKey`를
사용하거나 테이블 카탈로그를 별도로 조회합니다.

`database/sql` 드라이버도 서버와 SDK의 버전 호환 규칙을 따릅니다. 이전 버전 서버 또는
SDK와 연결한 경우에는 결과 컬럼에 PRIMARY KEY 플래그가 노출되지 않을 수 있습니다.

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
커밋 또는 롤백 전에 모든 `Rows`를 닫아야 합니다. 연결 풀이 세션을 재사용할 때 미완료
트랜잭션은 자동으로 롤백됩니다. context 취소로 커밋이 실패한 경우 같은 트랜잭션을 다시
커밋하려고 시도하지 마십시오.

표준 `database/sql`의 `sql.DB`와 `sql.Tx`에는 Machbase Append 메서드가 없습니다. 다만
neo-client의 `machbase.Conn`은 선택적 `Appender()` 확장을 제공하므로, `sql.Conn.Raw()`로
물리 연결을 고정한 뒤 사용할 수 있습니다. Appender를 닫기 전에 `sql.Conn`을
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
코드는 네이티브 `machgo.Conn.Appender()`를 우선 사용하십시오.

### Prepared statement와 statement cache

`db.PrepareContext`로 만든 문장은 여러 번 실행할 수 있습니다. 드라이버의 문장 캐시는
연결별로 동작하며, `statement_cache=auto|on|off` DSN 키로 설정합니다. 테이블을 삭제 후 다시
만들었거나 결과 컬럼 타입이 변경된 경우 캐시된 메타데이터가 갱신되도록 문장을 다시 준비합니다.
`USE`로 세션 데이터베이스를 변경한 뒤에도 기존 준비된 문장이나 커서를 다른 데이터베이스의
작업에 재사용하지 말고 새로 준비하거나 열어야 합니다.
`ALTER SESSION SET` 또는 사용자 컨텍스트를 바꾸는 `CONNECT USER`가 실행된 뒤에도 이전
세션 메타데이터에 의존하는 문장을 재사용하지 말고 다시 준비하십시오.

## 참고 사항 및 제한 사항

- 위치 기반 placeholder와 이름 기반 placeholder를 모두 사용할 수 있지만, 한 문장 안에서 두 방식을
  섞을 수 없습니다. 이름 기반 API는 `sql.Named()`을 사용합니다. 공통 SQL 기능과 SDK별 차이는
  [Named Bind Parameter syntax](../../reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
  참고하십시오.
- `database/sql`의 연결 풀은 일반적인 `sql.DB` 방식대로 동작합니다. DSN에
  `database`/`db`를 지정하면 `USE`로 변경된 세션을 연결 풀에 반환할 때 설정된 데이터베이스로
  복원합니다.
- ROWID를 지원하는 Standard Edition과 `neo-client`를 사용하면 단일 INSERT 결과에서
  `Result.LastInsertId()`를 호출할 수 있습니다. 반환된 `int64`는 `uint64`로 변환해 ROWID의
  bit pattern을 보존합니다. 자세한 내용은 [ROWID와 INSERT 결과 ID](/dbms/reference/sql/rowid/)를
  참고하십시오.
- 파라미터 타입은 드라이버 구현을 따릅니다. 일반적인 SQL 타입, `time.Time`, `[]byte`, `net.IP`,
  `api.Decimal`을 지원하지만 `bool` 파라미터는 지원하지 않습니다.
- `BeginTx`에서는 기본 isolation level과 읽기/쓰기 트랜잭션만 지원합니다.
