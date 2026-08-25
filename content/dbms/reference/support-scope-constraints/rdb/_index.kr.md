---
type: docs
title: '17.6.3 TRANSACTION 기능 지원표'
weight: 30
toc: true
---

Machbase TRANSACTION 테이블은 트랜잭션이 필요한 일반 관계형 데이터를 저장합니다. Machbase SQL과
JDBC/ODBC 등 지원 드라이버를 통해 접근합니다.

> **주의**: TRANSACTION 테이블은 **Standard Edition에서만 지원**됩니다. Cluster Edition에서는 TRANSACTION 테이블을 생성하거나 사용할 수 없습니다.

무수식 `CREATE TABLE`, `CREATE TRANSACTION TABLE`, `CREATE TXN TABLE`은 모두 TRANSACTION
테이블을 생성합니다. 따라서 Cluster Edition에서는 세 문법이 모두 거부됩니다. Cluster
Edition에서 LOG 테이블을 만들 때는 `CREATE LOG TABLE`을 사용합니다.

## SQL 기능 지원 여부

| 기능 | 지원 여부 | 비고 |
|------|:---------:|------|
| **기본 DML** | | |
| SELECT | O | |
| INSERT | O | |
| UPDATE | O | |
| DELETE | O | |
| INSERT ... ON DUPLICATE KEY UPDATE | O | PRIMARY KEY·UNIQUE INDEX 충돌 시 기존 row 갱신 |
| Append API | O | Machbase SQLCLI·ODBC batch·stream 경로 지원 |
| **트랜잭션** | | |
| Transaction (COMMIT/ROLLBACK) | O | plain `BEGIN`, `COMMIT`, `ROLLBACK` |
| Savepoint | X | 미지원 |
| **쿼리 기능** | | |
| Prepared Statement | O | |
| 파라미터 바인딩 | O | |
| JOIN | O | 다른 테이블 유형과 조인 가능 |
| Subquery | O | |
| VIEW | O | |
| **객체** | | |
| SEQUENCE | O | `CREATE SEQUENCE` |
| PRIMARY KEY / UNIQUE INDEX | O | 단일 PRIMARY KEY와 단일·복합 UNIQUE INDEX |
| 보조 INDEX | O | 단일·복합 BTREE 인덱스 |
| JSON path INDEX | O | `json_column->'$.path'` |
| AUTO_INCREMENT | O | `LONG`/`INT64` 컬럼 단위 PRIMARY KEY |
| ALTER ADD/DROP COLUMN | O | 컬럼 정의에 괄호 사용 |
| ALTER RENAME COLUMN / RENAME TO | O | 컬럼명·테이블명 변경 |
| ALTER MODIFY COLUMN | X | 미지원 |
| Trigger | X | 미지원 |
| Stored Procedure | X | 미지원 |
| Foreign Key | X | 미지원 |

`AUTO_INCREMENT` 사용법은 [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/), upsert는
[INSERT ON DUPLICATE KEY UPDATE](/dbms/rdb-table-usage/insert-on-duplicate-key-update/), Append
동작은 [Append API 지원 범위](/dbms/rdb-table-usage/sdk-append-scope/)를 참고하십시오.

## TRANSACTION 테이블 생성 예시

```sql
CREATE TRANSACTION TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    customer   VARCHAR(100),
    amount     DOUBLE,
    order_date DATETIME
);
```

## 트랜잭션 사용 예시 (JDBC)

```java
Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
try {
    Statement stmt = conn.createStatement();
    stmt.execute("BEGIN");
    stmt.executeUpdate("INSERT INTO orders VALUES (1, 'customer_a', 50000, SYSDATE)");
    stmt.executeUpdate("INSERT INTO orders VALUES (2, 'customer_b', 30000, SYSDATE)");
    stmt.execute("COMMIT");
} catch (SQLException e) {
    conn.createStatement().execute("ROLLBACK");
}
```

## Cluster Edition 제약

Cluster Edition에서 TRANSACTION 테이블 생성 시 오류가 발생합니다.

```
[Error] TRANSACTION table is not supported in Cluster Edition.
```

TRANSACTION 테이블이 필요한 경우 Standard Edition을 사용하거나, 트랜잭션 데이터를 외부 RDBMS(PostgreSQL, MySQL 등)에 저장하고 애플리케이션 계층에서 함께 처리하는 방식을 검토하십시오.

## 다른 테이블 유형과 JOIN

TRANSACTION 테이블은 TAG, LOG, LOOKUP 테이블과 JOIN이 가능합니다.

```sql
-- TAG 테이블과 TRANSACTION 테이블 JOIN
SELECT s.name, s.time, s.value, o.customer
FROM sensor_data s
JOIN orders o ON s.name = o.sensor_name
WHERE s.time >= now - 1h;
```
