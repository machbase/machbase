---
type: docs
title: '11.2.5 트랜잭션 처리 (RDB 및 SDK별 지원 범위 분리)'
weight: 50
---

Machbase는 테이블 유형에 따라 트랜잭션 지원 범위가 다릅니다. 애플리케이션 설계 시 반드시 확인해야 합니다.

## 테이블 유형별 트랜잭션 지원

| 테이블 유형 | 트랜잭션 | COMMIT/ROLLBACK | 이유 |
|-----------|:---:|:---:|------|
| **RDB** | O | O | 완전한 ACID 지원 |
| **VOLATILE** | O | O | 메모리 기반, 트랜잭션 지원 |
| **LOOKUP** | △ | △ | PK 기반 DML에 한해 지원 |
| **TAG** | X | X | Append-only, 트랜잭션 불필요 |
| **LOG** | X | X | Append-only, 트랜잭션 불필요 |

> TAG와 LOG 테이블은 고속 삽입을 위해 트랜잭션 없이 동작합니다. 삽입된 데이터는 즉시 저장되며 rollback이 불가능합니다.

## Autocommit 동작

Machbase JDBC 드라이버는 기본적으로 **autocommit이 활성화**되어 있습니다. RDB 테이블에서 트랜잭션을 명시적으로 제어하려면 autocommit을 비활성화합니다.

```java
// JDBC: 트랜잭션 제어
Connection conn = DriverManager.getConnection(url, props);
conn.setAutoCommit(false);  // autocommit 비활성화

try {
    PreparedStatement ps = conn.prepareStatement(
        "INSERT INTO orders (order_id, amount) VALUES (?, ?)");
    ps.setInt(1, 1001);
    ps.setDouble(2, 50000.0);
    ps.executeUpdate();

    ps.setInt(1, 1002);
    ps.setDouble(2, 30000.0);
    ps.executeUpdate();

    conn.commit();  // 두 행 모두 커밋
} catch (SQLException e) {
    conn.rollback();  // 오류 시 전체 롤백
    throw e;
} finally {
    conn.setAutoCommit(true);
}
```

```c
/* C/CLI: 트랜잭션 제어 */
SQLSetConnectAttr(conn, SQL_ATTR_AUTOCOMMIT,
                  (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0);

/* INSERT 작업 */
SQLExecDirect(stmt, "INSERT INTO orders VALUES (1001, 50000)", SQL_NTS);
SQLExecDirect(stmt, "INSERT INTO orders VALUES (1002, 30000)", SQL_NTS);

/* 커밋 또는 롤백 */
SQLEndTran(SQL_HANDLE_DBC, conn, SQL_COMMIT);
/* 오류 시: SQLEndTran(SQL_HANDLE_DBC, conn, SQL_ROLLBACK); */
```

```python
# Python: 트랜잭션 제어
conn = machbaseapi.connect(host, port, user, password)
# Python DB-API는 기본적으로 autocommit=False

cursor = conn.cursor()
try:
    cursor.execute("INSERT INTO orders (order_id, amount) VALUES (%s, %s)", [1001, 50000])
    cursor.execute("INSERT INTO orders (order_id, amount) VALUES (%s, %s)", [1002, 30000])
    conn.commit()
except Exception as e:
    conn.rollback()
    raise
finally:
    cursor.close()
```

## TAG/LOG 테이블에 대한 트랜잭션 시도

TAG와 LOG 테이블에 대해 COMMIT/ROLLBACK을 호출해도 무시되거나 오류가 반환됩니다. **삽입 즉시 영구 저장**됩니다.

```text
-- 이 패턴은 TAG 테이블에서 동작하지 않습니다
BEGIN;
INSERT INTO sensor_tag (name, time, value) VALUES ('s01', NOW, 25.0);
ROLLBACK;  -- 효과 없음: 데이터가 이미 저장됨
```

TAG/LOG 테이블에서 잘못 삽입된 데이터를 제거하려면 [DELETE 정책](../../../schema-data-lifecycle/alter-data-mutation-policy/policy-delete/)을 참고하세요.

## SDK별 트랜잭션 지원 요약

| SDK | RDB 트랜잭션 | 비고 |
|-----|:---:|------|
| ODBC/CLI | O | SQLEndTran(SQL_COMMIT / SQL_ROLLBACK) |
| JDBC | O | conn.commit() / conn.rollback() |
| Python | O | conn.commit() / conn.rollback() |
| .NET | O | MachTransaction 클래스 |
| Go (database/sql) | X | 현재 Go SQL 드라이버는 `Begin` / `BeginTx` 미지원 |
| Go (native client) | X | Append-only API 중심 |
| Node.js | X | 현재 미지원 |
| REST API | X | 단일 요청 단위 처리 |

상세 SDK별 지원 범위는 [SDK별 transaction/prepare/bind 지원 범위](../../support-scope-sdk/support-scope-sdk-transaction-prepare-bind/)를 참고하세요.
