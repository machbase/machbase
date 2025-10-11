---
title: QueryRow
type: docs
weight: 12
---

`QueryRow`는 단일 행을 반환하는 쿼리를 실행합니다.
`select count(*) from ...`, `select col1,col2 from table where id=?`처럼 단일 레코드를 조회하는 쿼리에 적합합니다.
쿼리가 여러 행을 반환하면 첫 번째 행만 가져옵니다.

- 요청 `QueryRowRequest`

| Field  | Type         | Desc                   |
|:-------|:-------------|:-----------------------|
| sql    | string       | SQL 쿼리 텍스트            |
| params | array of any | 쿼리 바인드 변수            |

- 응답 `QueryRowResponse`

| Field  | Type         | Desc                                   |
|:-------|:-------------|:----------------------------------------|
| succes | bool         | 성공 시 `true`, 오류 시 `false`              |
| reason | string       | 응답 메시지                                 |
| elapse | string       | 경과 시간을 나타내는 문자열                   |
| values | array of any | 첫 번째 행의 컬럼 값                         |

## 예시

### Go

#### count(*) 조회

```go
sqlText := `select count(*) from example`
row := cli.QueryRow(sqlText)

var count int
row.Scan(&count)

fmt.Println("count=", count)
```

- [grpc_queryrow.go]({{< neo_examples_url >}}/go/grpc_queryrow/grpc_queryrow.go)
