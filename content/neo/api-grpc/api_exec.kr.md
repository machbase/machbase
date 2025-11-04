---
title: Exec
type: docs
weight: 11
---

`Exec`는 결과 집합이 필요하지 않은 쿼리를 실행합니다.
`create table...`, `drop table...`, `insert into...`처럼 레코드를 반환하지 않고 성공/실패만 확인하면 되는 쿼리에 적합합니다.

- 요청 `ExecRequest`

| Field  | Type         | Desc                   |
|:-------|:-------------|:-----------------------|
| sql    | string       | SQL 쿼리 텍스트            |
| params | array of any | 쿼리 바인드 변수            |

- 응답 `ExecResponse`

| Field  | Type         | Desc                                   |
|:-------|:-------------|:----------------------------------------|
| succes | bool         | 성공 시 `true`, 오류 시 `false`              |
| reason | string       | 응답 메시지                                 |
| elapse | string       | 경과 시간을 나타내는 문자열                   |

## 예시

### Go

#### 테이블 생성

```go
sqlText := `
    create tag table example (
        name varchar(100) primary key, 
        time datetime basetime, 
        value double
    )`

cli.Exec(sqlText)
```

- [grpc_cretable.go]({{< neo_examples_url >}}/go/grpc_cretable/grpc_cretable.go)

#### 테이블 삭제

```go
sqlText := `drop table example`
cli.Exec(sqlText)
```

- [grpc_droptable.go]({{< neo_examples_url >}}/go/grpc_droptable/grpc_droptable.go)

#### 삽입

```go
sqlText := `insert into example (name, time, value) values (?, ?, ?)`
cli.Exec(sqlText, "tag-name-1", time.Now(), 1.234)
```

- [grpc_insert.go]({{< neo_examples_url >}}/go/grpc_insert/grpc_insert.go)
