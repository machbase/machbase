---
title: Query
type: docs
weight: 13
---

일반적으로 애플리케이션은 쿼리를 실행한 뒤 반복문을 통해 여러 레코드를 가져옵니다.

`Query`는 실행 결과로 행 핸들을 반환하며, 애플리케이션은 이 핸들을 사용해 반복적으로 레코드를 읽어 들입니다.

- 요청 `QueryRequest`

| Field  | Type         | Desc                   |
|:-------|:-------------|:-----------------------|
| sql    | string       | SQL 쿼리 텍스트            |
| params | array of any | 쿼리 바인드 변수            |


- 응답 `QueryResponse`

| Field      | Type         | Desc                                   |
|:-----------|:-------------|:----------------------------------------|
| succes     | bool         | 성공 시 `true`, 오류 시 `false`              |
| reason     | string       | 응답 메시지                                 |
| elapse     | string       | 경과 시간을 나타내는 문자열                   |
| rowsHandle | RowsHandle   | 행 핸들                                    |

## 예시

### Go

#### 다중 레코드 조회

```go
sqlText := `select name, time, value from example limit ?`
rows, _ := cli.Query(sqlText, 3)
defer rows.Close()

for rows.Next() {
    var name string
    var ts time.Time
    var value float64
    rows.Scan(&name, &ts, &value)
    fmt.Println(name, ts, value)
}
```

{{< callout type="warning" >}}
행 핸들은 서버 측 자원을 사용하므로, 사용 직후 반드시 해제해야 합니다. 이 예제에서는 `defer rows.Close()`를 사용해 핸들을 해제합니다.
{{< /callout >}}

- [grpc_query.go]({{< neo_examples_url >}}/go/grpc_query/grpc_query.go)
