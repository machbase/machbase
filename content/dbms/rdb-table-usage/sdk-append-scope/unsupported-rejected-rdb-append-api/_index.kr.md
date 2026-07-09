---
type: docs
title: 'Append API'
weight: 110
---

RDB 테이블은 Append API를 지원합니다. 단, TAG·LOG 테이블의 Append API와 내부 동작 방식이 다릅니다.

## 지원 현황

| 입력 방식 | RDB 테이블 지원 여부 |
|---------|-----------------|
| `INSERT` SQL 문 | O |
| SDK INSERT (Go/Python/C) | O |
| **Append API** | **O (트랜잭션 기반)** |
| machloader CSV 가져오기 | O |

## TAG·LOG Append API와의 차이

| 항목 | TAG·LOG Append | RDB Append |
|------|---------------|-----------|
| 내부 구현 | 대용량 최적화 버퍼 | 트랜잭션 기반 |
| 처리량 | 매우 높음 | 일반 INSERT 수준 |
| 적합한 용도 | 초고빈도 계측값 | 배치 데이터 로드 |

RDB 테이블의 Append API는 내부적으로 트랜잭션(`qrdBeginStmtTx` / `qrdCommitStmtTx`)으로 처리됩니다. 따라서 TAG·LOG 테이블의 초고속 버퍼 Append와 달리 일반 INSERT와 유사한 성능을 제공합니다.

## SDK Append 예시

```go
// Go SDK - Append API 사용
appender, err := conn.Appender(ctx, "orders")
if err != nil { ... }

appender.Append(1001, "CUST-001", 5, 49.99, "PENDING")
appender.Append(1002, "CUST-002", 2, 19.99, "PENDING")
appender.Close()
```

## 대량 입력 권장 방법

RDB 테이블에 대량 데이터를 삽입할 때는 **배치 INSERT(트랜잭션 활용)**가 더 직관적입니다.

```go
tx, _ := db.Begin()
stmt, _ := tx.Prepare("INSERT INTO orders VALUES (?, ?, ?, ?, ?)")
for _, row := range rows {
    stmt.Exec(row.OrderID, row.Customer, row.Qty, row.Amount, row.Status)
}
tx.Commit()
```

## machloader 사용

```bash
# CSV 파일로 대량 삽입
machloader -i -d orders -f orders.csv
```
