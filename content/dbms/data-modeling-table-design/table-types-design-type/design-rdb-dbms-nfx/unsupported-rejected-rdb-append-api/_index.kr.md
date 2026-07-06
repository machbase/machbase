---
type: docs
title: 'Append API 미지원'
weight: 110
---

RDB 테이블은 Machbase의 고속 Append API를 지원하지 않습니다.

## 지원 현황

| 입력 방식 | RDB 테이블 지원 여부 |
|---------|-----------------|
| `INSERT` SQL 문 | O |
| SDK INSERT (Go/Python/C) | O |
| **Append API** | **X (미지원)** |
| machloader CSV 가져오기 | O |

## Append API란

Append API는 Machbase의 고속 대량 입력 인터페이스입니다. TAG 테이블과 LOG 테이블에서 사용 가능하며, 일반 INSERT 대비 수십 배 빠른 처리량을 제공합니다.

## 대안

RDB 테이블에 대량 데이터를 삽입할 때는 다음 방법을 사용합니다.

### 배치 INSERT (트랜잭션 활용)

```go
// Go SDK 예시
tx, _ := db.Begin()
stmt, _ := tx.Prepare("INSERT INTO order_history VALUES (?, ?, ?, ?, ?, ?)")
for _, row := range rows {
    stmt.Exec(row.OrderID, row.Customer, row.ItemID, row.Amount, row.OrderTime, row.Status)
}
tx.Commit()
```

### machloader 사용

```bash
# CSV 파일로 대량 삽입
machloader -i -d order_history -f orders.csv -t rdb
```

## 주의사항

- Append API를 RDB 테이블에 사용하려 하면 오류가 반환됩니다.
- 고속 입력이 필요한 계측 데이터는 TAG 또는 LOG 테이블을 사용합니다.
- RDB 테이블은 트랜잭션 기반 INSERT가 주요 입력 방법입니다.
