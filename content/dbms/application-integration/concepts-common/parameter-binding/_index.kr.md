---
type: docs
title: 'Parameter binding'
weight: 40
---

Parameter binding은 SQL 문의 `?` 자리에 값을 채워 넣는 메커니즘입니다. Machbase는 위치 기반(positional) 바인딩을 사용합니다.

## 위치 기반 바인딩 (Positional Binding)

Machbase의 모든 드라이버는 `?`를 파라미터 자리 표시자로 사용합니다.

```sql
INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)
--                                                 1  2  3 (위치 순서)
```

파라미터는 왼쪽부터 순서대로 1번이며, 각 드라이버에서 이 위치 순서에 따라 값을 바인딩합니다.

> Machbase는 `:name` 형식의 named binding을 지원하지 않습니다. 항상 `?`와 위치 순서를 사용합니다.

## DATETIME 타입 바인딩

Machbase의 시간 값은 내부적으로 **UTC 기준 nanosecond 정수**로 저장됩니다. 드라이버마다 바인딩 방식이 다릅니다.

### 주의: nanosecond vs millisecond

Java의 `System.currentTimeMillis()`는 millisecond 단위입니다. Machbase에 nanosecond로 저장하려면 1,000,000을 곱해야 합니다.

```java
long nowNano = System.currentTimeMillis() * 1_000_000L;
pstmt.setLong(2, nowNano);
```

Python의 `time.time()`은 초(float) 단위입니다.

```python
import time
now_nano = int(time.time() * 1_000_000_000)
cur.execute(sql, ('sensor_01', now_nano, 23.5))
```

### ODBC (C/C++)

ODBC에서는 `SQL_C_SBIGINT` 타입으로 nanosecond 정수를 바인딩하거나, `SQL_C_TYPE_TIMESTAMP` 구조체를 사용할 수 있습니다.

```c
// nanosecond 정수로 바인딩
long long ts_nano = 1720000000000000000LL;
SQLLEN indicator = 0;
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT,
                 SQL_C_SBIGINT, SQL_BIGINT,
                 0, 0, &ts_nano, 0, &indicator);
```

### JDBC

JDBC에서는 `setLong()`으로 nanosecond 정수를 직접 바인딩하거나, `setTimestamp()`로 `java.sql.Timestamp`를 사용할 수 있습니다. `setTimestamp()`는 millisecond 해상도이므로 nanosecond 정밀도가 필요하면 `setLong()`을 사용하세요.

```java
// nanosecond 정수로 바인딩 (권장: 정밀도 손실 없음)
pstmt.setLong(2, 1720000000123456789L);

// Timestamp로 바인딩 (millisecond 해상도)
pstmt.setTimestamp(2, new java.sql.Timestamp(1720000000123L));
```

### Python

```python
import time

# nanosecond 정수 (권장)
now_ns = int(time.time_ns())  # Python 3.7+
cur.execute("INSERT INTO tag_table VALUES (?, ?, ?)", ('sensor_01', now_ns, 23.5))

# datetime 객체 사용 (microsecond 해상도)
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
cur.execute("INSERT INTO tag_table VALUES (?, ?, ?)", ('sensor_01', now, 23.5))
```

## NULL 값 처리

### Python

Python에서는 `None`으로 NULL을 표현합니다.

```python
# value 컬럼에 NULL 삽입
cur.execute("INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)",
            ('sensor_01', now_ns, None))
```

### Java

Java에서는 `setNull()` 메서드를 사용합니다.

```java
pstmt.setNull(3, java.sql.Types.DOUBLE);
```

또는 `setObject()`에 `null`을 전달합니다.

```java
pstmt.setObject(3, null);
```

### ODBC (C/C++)

ODBC에서는 indicator 변수를 `SQL_NULL_DATA`로 설정합니다.

```c
SQLLEN indicator = SQL_NULL_DATA;
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT,
                 SQL_C_DOUBLE, SQL_DOUBLE,
                 0, 0, NULL, 0, &indicator);
```

### .NET (C#)

```csharp
// DBNull.Value로 NULL 표현
cmd.Parameters.AddWithValue("@value", DBNull.Value);
```

## SDK별 바인딩 메서드 요약

### ODBC (SQLBindParameter)

```c
// 문자열
SQLBindParameter(stmt, 1, SQL_PARAM_INPUT,
                 SQL_C_CHAR, SQL_VARCHAR, 63, 0,
                 name_buf, 0, &name_len);

// 정수
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT,
                 SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
                 &int_val, 0, &indicator);

// 실수
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT,
                 SQL_C_DOUBLE, SQL_DOUBLE, 0, 0,
                 &double_val, 0, &indicator);
```

### JDBC (setXxx 메서드)

```java
pstmt.setString(1, "sensor_01");     // VARCHAR, CHAR
pstmt.setLong(2, tsNano);            // DATETIME (nanosecond), BIGINT
pstmt.setInt(3, 42);                 // INTEGER
pstmt.setDouble(4, 23.5);           // DOUBLE
pstmt.setFloat(5, 23.5f);           // FLOAT
pstmt.setShort(6, (short)10);       // SMALLINT
```

### Python (튜플로 전달)

```python
# 파라미터는 execute()의 두 번째 인자로 튜플 또는 리스트
cur.execute(
    "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)",
    ('sensor_01', now_ns, 23.5)
)

# executemany(): 리스트 of 튜플
cur.executemany(
    "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)",
    [
        ('sensor_01', now_ns,           23.5),
        ('sensor_02', now_ns + 1000000, 18.2),
    ]
)
```

### .NET (MachCommand.Parameters)

```csharp
MachCommand cmd = new MachCommand(
    "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)", conn);

cmd.Parameters.Add(new MachParameter { Value = "sensor_01" });
cmd.Parameters.Add(new MachParameter { Value = 1720000000000000000L });
cmd.Parameters.Add(new MachParameter { Value = 23.5 });

cmd.ExecuteNonQuery();
```

## 타입 변환 주의사항

Machbase는 타입 불일치 시 암묵적 변환을 시도하지만, 정밀도 손실이 발생할 수 있습니다. 특히 다음 경우에 주의하세요.

| 상황 | 권장 처리 |
|------|-----------|
| DATETIME 바인딩 | nanosecond 정수(`BIGINT`)로 바인딩 |
| VARCHAR → BIGINT 자동 변환 | 명시적으로 올바른 타입을 사용할 것 |
| DOUBLE → FLOAT 바인딩 | 정밀도 손실 가능, DOUBLE로 바인딩 권장 |

타임존 관련 처리는 [타임존 연결 옵션](../timezone-connection/)을 참조하세요.
