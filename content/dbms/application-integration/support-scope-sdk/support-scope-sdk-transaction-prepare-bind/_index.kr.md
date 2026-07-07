---
type: docs
title: 'SDK별 transaction / prepare / bind 지원 범위 안내'
weight: 30
---

각 SDK가 지원하는 트랜잭션, Prepared Statement, Parameter Binding 기능을 정리합니다.

> TAG 및 LOG 테이블은 append-only 구조로 트랜잭션이 필요하지 않습니다. 트랜잭션은 **RDB 테이블**에서만 의미가 있습니다.

## 지원 범위 표

| SDK | Transaction (RDB) | Prepared Statement | Parameter Binding | 비고 |
|-----|:---:|:---:|:---:|------|
| **ODBC/CLI** | O | O | O | SQLEndTran, SQLPrepare, SQLBindParameter |
| **JDBC** | O | O | O | conn.setAutoCommit(false), PreparedStatement |
| **Python** | O | O | O | conn.commit(), cursor.execute(sql, params) |
| **.NET Connector** | O | O | O | MachTransaction, MachCommand.Parameters |
| **Go (database/sql)** | O | O | O | db.Begin(), db.Prepare(), Named/Positional |
| **Go (native client)** | X | △ | O | Append 중심, SELECT에 파라미터 제한적 |
| **Node.js** | X | O | O | transaction 미지원, prepare/bind는 지원 |
| **REST API** | X | X | X | 단일 요청 단위, 서버사이드 파라미터 없음 |

- O: 지원
- △: 부분 지원 (제한 있음)
- X: 미지원

## 트랜잭션 (Transaction)

RDB 테이블에서만 COMMIT/ROLLBACK이 유효합니다. 나머지 테이블 유형은 삽입 즉시 영구 저장됩니다.

```java
// JDBC
conn.setAutoCommit(false);
try {
    stmt.executeUpdate("INSERT INTO orders VALUES (1, 50000)");
    stmt.executeUpdate("INSERT INTO orders VALUES (2, 30000)");
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
}
```

```csharp
// .NET
using var tx = conn.BeginTransaction();
try {
    var cmd = conn.CreateCommand();
    cmd.Transaction = tx;
    cmd.CommandText = "INSERT INTO orders VALUES (1, 50000)";
    cmd.ExecuteNonQuery();
    tx.Commit();
} catch {
    tx.Rollback();
    throw;
}
```

## Prepared Statement

반복 실행할 쿼리를 미리 파싱·컴파일하여 성능을 향상시킵니다. SQL 인젝션 방지 효과도 있습니다.

```python
# Python
cursor = conn.cursor()
cursor.prepare("INSERT INTO sensor_log (name, time, value) VALUES (?, ?, ?)")
for name, ts, val in data_list:
    cursor.execute(None, (name, ts, val))  # 파라미터만 변경하여 재실행
```

```go
// Go database/sql
stmt, _ := db.Prepare("INSERT INTO sensor_log (name, time, value) VALUES (?, ?, ?)")
defer stmt.Close()
for _, row := range dataList {
    stmt.Exec(row.Name, row.Time, row.Value)
}
```

## Parameter Binding

파라미터 바인딩 사용 시 DATETIME 타입은 **나노초 정수**로 전달하는 것을 권장합니다.

```java
// JDBC - DATETIME 나노초 바인딩
PreparedStatement ps = conn.prepareStatement(
    "INSERT INTO sensor_log (name, time, value) VALUES (?, ?, ?)");
ps.setString(1, "sensor-01");
ps.setLong(2, System.currentTimeMillis() * 1_000_000L); // ms → ns
ps.setDouble(3, 23.5);
ps.executeUpdate();
```

```c
/* ODBC/CLI - SQLBindParameter */
SQLLEN nameLen = SQL_NTS;
SQLLEN timeInd = 0;
SQLLEN valueInd = 0;
char name[64] = "sensor-01";
SQLBIGINT time_ns = current_time_ns();
double value = 23.5;

SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR,
                 64, 0, name, 0, &nameLen);
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_SBIGINT, SQL_BIGINT,
                 0, 0, &time_ns, 0, &timeInd);
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE,
                 0, 0, &value, 0, &valueInd);
SQLExecute(stmt);
```

## NULL 처리

각 SDK에서 NULL 값을 바인딩하는 방법:

| SDK | NULL 바인딩 방법 |
|-----|----------------|
| JDBC | `ps.setNull(idx, java.sql.Types.INTEGER)` |
| Python | 파라미터 값에 `None` 전달 |
| .NET | `DBNull.Value` |
| Go | `sql.NullString{Valid: false}` 등 Null 타입 |
| ODBC/CLI | indicator를 `SQL_NULL_DATA`로 설정 |

상세 내용은 각 [드라이버별 가이드](../../guide-drivers/)를 참고하세요.
