---
type: docs
title: 'SDK 지원 범위'
weight: 120
---

RDB 테이블은 Machbase SDK를 통해 다양한 언어에서 접근할 수 있습니다.

## 지원 SDK

| SDK | SELECT | INSERT | DELETE | 트랜잭션 |
|-----|--------|--------|--------|---------|
| Go SDK | O | O | O | O |
| Python SDK | O | O | O | O |
| C/C++ SDK | O | O | O | O |
| JDBC | O | O | O | O |
| ODBC | O | O | O | O |
| REST API | O | O | O | 제한적 |

## Go SDK 예시

```go
package main

import (
    "database/sql"
    _ "github.com/machbase/neo-client/driver"
)

func main() {
    db, _ := sql.Open("machbase", "machbase://SYS:MANAGER@127.0.0.1:5656")
    defer db.Close()

    // INSERT
    db.Exec(`INSERT INTO order_history VALUES (1001, 'CUST-001', 5, 49.99, NOW, 'PENDING')`)

    // SELECT
    rows, _ := db.Query(`SELECT order_id, customer, amount FROM order_history WHERE customer = ?`, "CUST-001")
    defer rows.Close()

    // DELETE
    db.Exec(`DELETE FROM order_history WHERE order_id = ?`, 1001)
}
```

## Python SDK 예시

```python
import machbase_neo

conn = machbase_neo.connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cursor = conn.cursor()

# INSERT
cursor.execute("INSERT INTO order_history VALUES (?, ?, ?, ?, NOW, ?)",
               (1001, 'CUST-001', 5, 49.99, 'PENDING'))
conn.commit()

# SELECT
cursor.execute("SELECT order_id, customer, amount FROM order_history WHERE customer = ?",
               ('CUST-001',))
rows = cursor.fetchall()

# DELETE
cursor.execute("DELETE FROM order_history WHERE order_id = ?", (1001,))
conn.commit()
cursor.close()
conn.close()
```

## REST API 예시

```bash
# INSERT via REST
curl -X POST http://127.0.0.1:5657/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"q": "INSERT INTO order_history VALUES (1001, '\''CUST-001'\'', 5, 49.99, NOW, '\''PENDING'\'')"}'

# SELECT via REST
curl "http://127.0.0.1:5657/api/v1/query?q=SELECT+order_id,customer+FROM+order_history+WHERE+customer='\''CUST-001'\''"
```
