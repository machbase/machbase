---
type: docs
title: '17.8.3 RDB 기능 지원표'
weight: 30
---

Machbase RDB 테이블은 트랜잭션이 필요한 일반 관계형 데이터를 저장합니다. SQL 표준을 준수하며, JDBC/ODBC 등 표준 드라이버를 통해 접근합니다.

> **주의**: RDB 테이블은 **Standard Edition에서만 지원**됩니다. Cluster Edition에서는 RDB 테이블을 생성하거나 사용할 수 없습니다.

## SQL 기능 지원 여부

| 기능 | 지원 여부 | 비고 |
|------|:---------:|------|
| **기본 DML** | | |
| SELECT | O | |
| INSERT | O | |
| UPDATE | O | |
| DELETE | O | |
| **트랜잭션** | | |
| Transaction (COMMIT/ROLLBACK) | O | `conn.setAutoCommit(false)` |
| Savepoint | X | 미지원 |
| **쿼리 기능** | | |
| Prepared Statement | O | |
| 파라미터 바인딩 | O | |
| JOIN | O | 다른 테이블 유형과 조인 가능 |
| Subquery | O | |
| VIEW | O | |
| **객체** | | |
| SEQUENCE | O | `CREATE SEQUENCE` |
| INDEX | O | |
| Trigger | X | 미지원 |
| Stored Procedure | X | 미지원 |
| Foreign Key | X | 미지원 |

## RDB 테이블 생성 예시

```sql
CREATE TABLE orders (
    order_id   INTEGER,
    customer   VARCHAR(100),
    amount     DOUBLE,
    order_date DATETIME,
    PRIMARY KEY (order_id)
) ENGINE=RDB;
```

## 트랜잭션 사용 예시 (JDBC)

```java
Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
conn.setAutoCommit(false);

try {
    Statement stmt = conn.createStatement();
    stmt.executeUpdate("INSERT INTO orders VALUES (1, 'customer_a', 50000, NOW())");
    stmt.executeUpdate("INSERT INTO orders VALUES (2, 'customer_b', 30000, NOW())");
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
}
```

## Cluster Edition 제약

Cluster Edition에서 RDB 테이블 생성 시 오류가 발생합니다.

```
[Error] RDB table is not supported in Cluster Edition.
```

RDB 테이블이 필요한 경우 Standard Edition을 사용하거나, 트랜잭션 데이터를 외부 RDBMS(PostgreSQL, MySQL 등)에 저장하고 Machbase에서 JOIN 또는 REST API로 연동하는 방식을 검토하세요.

## 다른 테이블 유형과 JOIN

RDB 테이블은 TAG, LOG, LOOKUP 테이블과 JOIN이 가능합니다.

```sql
-- TAG 테이블과 RDB 테이블 JOIN
SELECT s.name, s.time, s.value, o.customer
FROM sensor_data s
JOIN orders o ON s.name = o.sensor_name
WHERE s.time >= now - 1h;
```
