---
title: '8.14 Append API 지원과 SDK 사용 범위'
weight: 150
toc: true
---

TRANSACTION 테이블의 Append API 동작 방식과 SDK별 지원 범위를 정리합니다.


<a id="unsupported-rejected-rdb-append-api"></a>

## Append API

TRANSACTION 테이블도 Append API를 지원합니다. 단, TAG·LOG 테이블의 Append와 내부 동작 방식이 다릅니다.

## 지원 현황

| 입력 방식 | TRANSACTION 테이블 지원 여부 |
|---------|-----------------|
| `INSERT` SQL 문 | O |
| SDK INSERT (Go/Python/C) | O |
| **Append API** | **O (트랜잭션 기반)** |
| machloader CSV 가져오기 | O |

## TAG·LOG Append API와의 차이

| 항목 | TAG·LOG Append | TRANSACTION Append |
|------|---------------|-----------|
| 내부 구현 | 대용량 최적화 버퍼 | 트랜잭션 기반 |
| 처리량 | 매우 높음 | 일반 INSERT 수준 |
| 적합한 용도 | 초고빈도 계측값 | 배치 데이터 로드 |

TRANSACTION 테이블의 Append API는 트랜잭션 기반으로 처리됩니다. TAG·LOG 테이블의 초고속
버퍼 Append와 달리 일반 INSERT와 유사한 성능 특성을 가집니다.

`AUTO_INCREMENT` 컬럼이 있는 TRANSACTION 테이블에 `SQLAppendBatch`를 사용할 때는 auto 컬럼을 생략할 수 없습니다. auto 컬럼을 포함하고 `SQL_APPEND_TYPE_INT64`와 `SQL_APPEND_LONG_NULL` 조합으로 자동값 생성을 요청합니다. 자세한 예시는 [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/#sqlappendbatch-사용-시-주의-사항)를 참고합니다.

## C SQLCLI DECIMAL Append

`SQLAppendDataV2()`와 `SQLAppendBatch()`로 `DECIMAL` 또는 `NUMERIC` 값을 입력할 때는
32바이트 opaque 타입인 `SQL_APPEND_NUMERIC`과 전용 생성 함수를 사용합니다. 구조체의 내부
바이트를 애플리케이션에서 직접 만들거나 수정하지 않습니다.

| 함수 | 입력 값 |
|------|---------|
| `SQLAppendNumericFromString()` | UTF-8 숫자 문자열 |
| `SQLAppendNumericFromStringW()` | wide-character 숫자 문자열 |
| `SQLAppendNumericFromInt64()` | signed 64비트 정수 |
| `SQLAppendNumericFromUInt64()` | unsigned 64비트 정수 |
| `SQLAppendNumericFromDouble()` | 유한한 `double` 값 |
| `SQLAppendNumericFromSQLNumeric()` | ODBC `SQL_NUMERIC_STRUCT` |
| `SQLAppendNumericSetNull()` | SQL NULL |

정확한 10진수 값을 보존하려면 문자열 또는 `SQL_NUMERIC_STRUCT` 입력을 권장합니다.
`SQLAppendNumericFromDouble()`은 이진 부동소수점 값을 변환하므로 NaN과 양·음의 무한대는
거부됩니다. NULL은 구조체를 0으로 초기화하지 말고 `SQLAppendNumericSetNull()`로 만듭니다.

```c
SQL_APPEND_NUMERIC amount;

if (SQLAppendNumericFromString(stmt,
                               &amount,
                               (const SQLCHAR *)"123.456",
                               SQL_NTS) != SQL_SUCCESS) {
    /* SQLError() 또는 ODBC diagnostic API로 오류를 확인합니다. */
}
```

`SQLAppendBatch()`의 타입 배열에는 `SQL_APPEND_TYPE_NUMERIC` 또는 같은 코드의 별칭인
`SQL_APPEND_TYPE_DECIMAL`을 지정합니다. 대상 컬럼의 precision과 scale은 append 시 적용되며,
scale을 넘는 소수는 DECIMAL 반올림 규칙으로 정규화되고 precision 초과 값은 저장하지 않고
오류를 반환합니다.

| 오류 | SQLSTATE |
|------|----------|
| 잘못된 숫자 문자열 | `22018` |
| precision/scale 범위 초과 또는 대상 컬럼 overflow | `22003` |
| NULL 포인터 | `HY009` |
| 잘못된 문자열 길이 | `HY090` |

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

대량 데이터를 삽입할 때는 **배치 INSERT(트랜잭션 활용)**가 더 직관적입니다.

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
# TRANSACTION 사용자 컬럼의 스키마 파일 생성
machloader -c -t orders -f orders.fmt

# 스키마 파일로 CSV 컬럼을 매핑하여 입력
machloader -i -f orders.fmt -d orders.csv
```

TRANSACTION 테이블에는 사용자 컬럼을 명시적으로 매핑할 수 있도록 `-t`와 `-d`만 지정한 자동 매핑
대신 `-f` 스키마 파일을 사용합니다. `csvimport`도 같은 스키마 파일 옵션으로 입력할 수 있습니다.

<a id="support-scope-rdb-sdk"></a>

## SDK 지원 범위

TRANSACTION 테이블은 다양한 언어의 Machbase SDK를 통해 접근할 수 있습니다.

## 지원 SDK

| SDK | SELECT | INSERT | UPDATE | DELETE | 트랜잭션 |
|-----|--------|--------|--------|--------|---------|
| Go `database/sql` | O | O | O | O | O |
| Go native | O | O | O | O | △ (같은 연결에서 트랜잭션 SQL 실행) |
| Python SDK | O | O | O | O | X |
| Machbase SQLCLI | O | O | O | O | △ (같은 연결에서 트랜잭션 SQL 실행) |
| JDBC | O | O | O | O | O |
| ODBC | O | O | O | O | △ (같은 연결에서 트랜잭션 SQL 실행) |

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
    db.Exec(`INSERT INTO orders VALUES (1001, 'CUST-001', 5, 49.99, 'PENDING')`)

    // UPDATE
    db.Exec(`UPDATE orders SET status = 'SHIPPED' WHERE order_id = ?`, 1001)

    // SELECT
    rows, _ := db.Query(`SELECT order_id, customer, amount FROM orders WHERE customer = ?`, "CUST-001")
    defer rows.Close()

    // DELETE
    db.Exec(`DELETE FROM orders WHERE order_id = ?`, 1001)
}
```

## Python SDK 예시

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cursor = conn.cursor(prepared=True)

# INSERT
cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
               (1001, 'CUST-001', 5, 49.99, 'PENDING'))

# UPDATE
cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", ('SHIPPED', 1001))

# SELECT
cursor.execute("SELECT order_id, customer, amount FROM orders WHERE customer = ?", ('CUST-001',))
rows = cursor.fetchall()

# DELETE
cursor.execute("DELETE FROM orders WHERE order_id = ?", (1001,))

cursor.close()
conn.close()
```
