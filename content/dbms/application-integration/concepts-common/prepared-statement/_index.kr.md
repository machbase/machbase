---
type: docs
title: 'Prepared statement'
weight: 30
---

Prepared statement는 SQL 문을 먼저 파싱·컴파일한 뒤, 파라미터만 바꿔가며 반복 실행하는 방식입니다. SQL 인젝션 방지와 반복 실행 성능 향상이라는 두 가지 이점이 있습니다.

## 왜 Prepared statement를 사용하는가

### SQL 인젝션 방지

문자열을 직접 SQL에 연결(concatenate)하면 악의적인 입력값이 SQL 구조를 변경할 수 있습니다.

```python
# 위험한 코드: 문자열 직접 연결
sensor_id = "'; DROP TABLE tag_table; --"
sql = f"SELECT * FROM tag_table WHERE name = '{sensor_id}'"
# 실행되는 SQL: SELECT * FROM tag_table WHERE name = ''; DROP TABLE tag_table; --'
```

Prepared statement를 사용하면 파라미터 값은 항상 데이터로만 처리됩니다.

```python
# Python machbaseAPI: %s 파라미터 렌더링 사용
sql = "SELECT * FROM tag_table WHERE name = %s"
cur.execute(sql, ['sensor_id_value'])
```

### 반복 실행 성능

같은 SQL을 반복 실행할 때 매번 파싱하는 비용을 줄입니다. 수집 루프에서 동일한 INSERT 문을 반복 실행하는 경우에 특히 효과적입니다.

```
일반 execute() × 1000번:
  SQL 파싱 × 1000 + 네트워크 × 1000

Prepared statement × 1000번:
  SQL 파싱 × 1 + 파라미터 전송 × 1000
```

## Machbase에서의 지원 범위

Machbase는 LOG, TAG, RDB 테이블 모두에서 Prepared statement를 지원합니다.

| 테이블 타입 | INSERT | SELECT |
|------------|--------|--------|
| LOG 테이블 | O | O |
| TAG 테이블 | O | O |
| RDB 테이블 | O | O |

단, Append API와 Prepared statement는 별개입니다. Append API는 Prepared statement 형태가 아니라 전용 API 호출로 동작합니다. 대용량 입력은 Append API를, 단건 또는 소량 반복 입력은 Prepared statement를 사용합니다.

## 예제

### INSERT (Python)

Python `machbaseAPI`의 DB-API 스타일 커서는 서버 prepared statement가 아니라 `%s`
자리 표시자를 클라이언트에서 렌더링하는 방식입니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

sql = "INSERT INTO tag_table (name, time, value) VALUES (%s, %s, %s)"

sensor_data = [
    ('sensor_01', 1720000000000000000, 23.5),
    ('sensor_01', 1720000001000000000, 23.7),
    ('sensor_02', 1720000000000000000, 18.2),
]

for row in sensor_data:
    cur.execute(sql, row)

cur.close()
conn.close()
```

### SELECT (Python)

```python
cur.execute(
    "SELECT name, time, value FROM tag_table WHERE name = %s AND time >= %s",
    ['sensor_01', 1720000000000000000],
)

for row in cur.fetchall():
    print(row)
```

### INSERT (Java)

```java
String sql = "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)";
PreparedStatement pstmt = conn.prepareStatement(sql);

List<SensorData> dataList = getSensorData();

for (SensorData data : dataList) {
    pstmt.setString(1, data.getName());
    pstmt.setLong(2, data.getTimestampNano());
    pstmt.setDouble(3, data.getValue());
    pstmt.executeUpdate();
}

pstmt.close();
```

### SELECT (Java)

```java
String sql = "SELECT name, time, value FROM tag_table WHERE name = ? AND time >= ?";
PreparedStatement pstmt = conn.prepareStatement(sql);

pstmt.setString(1, "sensor_01");
pstmt.setLong(2, 1720000000000000000L);

ResultSet rs = pstmt.executeQuery();
while (rs.next()) {
    String name  = rs.getString("name");
    long   ts    = rs.getLong("time");
    double value = rs.getDouble("value");
    System.out.printf("%s: %d -> %.2f%n", name, ts, value);
}

rs.close();
pstmt.close();
```

### INSERT (ODBC/C)

```c
#include <machbase_sqlcli.h>

SQLHSTMT stmt;
SQLAllocStmt(conn, &stmt);

char* sql = "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)";
SQLPrepare(stmt, (SQLCHAR*)sql, SQL_NTS);

// 파라미터 바인딩
char   name[64] = "sensor_01";
long   ts       = 1720000000000000000LL;
double value    = 23.5;

SQLLEN nameLen  = SQL_NTS;
SQLLEN tsLen    = 0;
SQLLEN valueLen = 0;

SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR,   SQL_VARCHAR,  63, 0, name,  0, &nameLen);
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_SBIGINT, SQL_BIGINT,  0,  0, &ts,   0, &tsLen);
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE,   0,  0, &value, 0, &valueLen);

SQLExecute(stmt);
SQLFreeStmt(stmt, SQL_DROP);
```

## Prepared statement 재사용 시 주의사항

- `close()`를 너무 빨리 호출하지 마세요. 반복 실행이 끝난 후 닫습니다.
- connection pool 환경에서는 connection이 반환될 때 statement도 함께 닫히는지 확인하세요. statement leak은 서버 리소스를 소진시킵니다.
- TAG 테이블에 많은 양의 데이터를 입력할 때는 Prepared statement보다 [Append API](../append-api-batch/)가 훨씬 효율적입니다.

파라미터 바인딩의 상세 방법(DATETIME 타입, NULL 처리 등)은 [Parameter binding](../parameter-binding/)을 참조하세요.
