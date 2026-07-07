---
type: docs
title: 'Go SQL 드라이버'
weight: 20
---

## 개요

`github.com/machbase/neo-client` 패키지는 Go 표준 `database/sql` 인터페이스를 통해 Machbase에 연결하는 드라이버를 제공합니다. 네이티브 TCP 클라이언트를 기반으로 하며, 네이티브 포트(기본 `5656`)를 사용합니다.

기존 코드가 `database/sql` 인터페이스를 사용하거나, GORM·sqlx 같은 `database/sql` 기반 라이브러리와 함께 사용할 때 적합합니다. Machbase 고유 기능(Append API 등)이 필요하다면 [Go 클라이언트](../go/)를 검토하세요.

## 설치 {#install}

```sh
go get github.com/machbase/neo-client@latest
```

### Import

드라이버 패키지를 blank identifier(`_`)로 import합니다. 드라이버 이름 `"machbase"`로 자동 등록되므로 별도의 `sql.Register()` 호출은 필요하지 않습니다.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## 연결 {#connect}

### DSN 형식

세미콜론(`;`)으로 구분된 키=값 쌍을 DSN으로 사용합니다.

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=1000
```

Statement 캐시를 추가하는 경우:

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=1000;statement_cache=auto
```

### 지원되는 DSN 키

| 키 | 설명 | 예시 |
|----|------|------|
| `server` | 서버 URL (`tcp://user:password@host:port` 형식) | `server=tcp://sys:manager@127.0.0.1:5656` |
| `host`, `port` | 호스트와 포트를 별도로 지정 | `host=127.0.0.1;port=5656` |
| `user` | 로그인 사용자 | `user=sys` |
| `password` | 로그인 비밀번호 | `password=manager` |
| `fetch_rows` | 한 번의 round trip에서 가져올 행 수. 현재 드라이버에서는 명시 필요 | `fetch_rows=2000` |
| `statement_cache` | Statement 캐시 모드: `auto`, `on`, `off` | `statement_cache=auto` |
| `io_metrics` | I/O metrics 활성화: `true`, `false` | `io_metrics=true` |
| `alternative_servers` | 대체 서버 주소 | `alternative_servers=127.0.0.2:5656` |

### sql.Open

```go
fields := []string{
    "server=tcp://sys:manager@127.0.0.1:5656",
    "fetch_rows=1000",
    "statement_cache=auto",
}

db, err := sql.Open("machbase", strings.Join(fields, ";"))
if err != nil {
    log.Fatal(err)
}
defer db.Close()
```

## 데이터 조회 예제 {#query-example}

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "strings"

    _ "github.com/machbase/neo-client"
)

func main() {
    dsn := strings.Join([]string{
        "server=tcp://sys:manager@127.0.0.1:5656",
        "fetch_rows=1000",
        "statement_cache=auto",
    }, ";")

    db, err := sql.Open("machbase", dsn)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    ctx := context.Background()

    // 시스템 테이블 목록 조회
    rows, err := db.QueryContext(ctx, `SELECT NAME, TYPE FROM M$SYS_TABLES ORDER BY NAME`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    columns, err := rows.Columns()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Columns:", columns)

    for rows.Next() {
        var name string
        var typ  int
        if err := rows.Scan(&name, &typ); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("  name=%-30s type=%d\n", name, typ)
    }

    if err := rows.Err(); err != nil {
        log.Fatal(err)
    }
}
```

## 데이터 삽입 예제 {#insert-example}

다음 예제는 태그 테이블에 행을 삽입합니다. 먼저 테이블을 생성합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name  VARCHAR(100) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);
```

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "strings"
    "time"

    _ "github.com/machbase/neo-client"
)

func main() {
    dsn := strings.Join([]string{
        "server=tcp://sys:manager@127.0.0.1:5656",
        "fetch_rows=1000",
    }, ";")

    db, err := sql.Open("machbase", dsn)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    ctx := context.Background()
    baseTime := time.Now()

    for i := 0; i < 10; i++ {
        result, err := db.ExecContext(ctx,
            `INSERT INTO example VALUES (?, ?, ?)`,
            "sensor-1",
            baseTime.Add(time.Second*time.Duration(i)),
            3.14*float64(i),
        )
        if err != nil {
            log.Fatal(err)
        }

        affected, err := result.RowsAffected()
        if err != nil {
            log.Fatal(err)
        }
        fmt.Println("RowsAffected:", affected)
    }
}
```

## Prepared Statement {#prepared-statement}

`database/sql`의 표준 Prepared Statement를 사용할 수 있습니다. 동일한 쿼리를 반복 실행할 때 `statement_cache=auto` DSN 옵션과 함께 사용하면 성능이 향상됩니다.

```go
ctx := context.Background()

stmt, err := db.PrepareContext(ctx, `INSERT INTO example VALUES (?, ?, ?)`)
if err != nil {
    log.Fatal(err)
}
defer stmt.Close()

for i := 0; i < 100; i++ {
    _, err := stmt.ExecContext(ctx,
        fmt.Sprintf("sensor-%d", i%5),
        time.Now().Add(time.Duration(i)*time.Millisecond),
        float64(i)*0.1,
    )
    if err != nil {
        log.Fatal(err)
    }
}
```

## 단일 행 조회 (`QueryRow`) {#queryrow}

```go
if _, err := db.ExecContext(ctx, `EXEC TABLE_FLUSH(example)`); err != nil {
    log.Fatal(err)
}

var name  string
var tm    time.Time
var value float64

err = db.QueryRowContext(ctx,
    `SELECT name, time, value FROM example WHERE name = ? ORDER BY time DESC LIMIT 1`,
    "sensor-1",
).Scan(&name, &tm, &value)

if err == sql.ErrNoRows {
    fmt.Println("결과 없음")
} else if err != nil {
    log.Fatal(err)
} else {
    fmt.Printf("name=%s, time=%s, value=%.4f\n", name, tm.Local(), value)
}
```

## 제한 사항 {#limitations}

| 항목 | 내용 |
|------|------|
| 파라미터 형식 | `?` 형태의 positional placeholder만 지원. named parameter 미지원 |
| 트랜잭션 | 명시적 트랜잭션 미지원 (`Begin`, `BeginTx`는 오류 반환) |
| LastInsertId | 미지원 |
| bool 파라미터 | 미지원. 정수(`0`/`1`)로 대체 |
| 지원 타입 | 일반 SQL 타입, `time.Time`, `[]byte`, `net.IP` |
| Append API | `database/sql` 인터페이스를 통해서는 Append 사용 불가. 필요 시 [Go 클라이언트](../go/) 사용 |
