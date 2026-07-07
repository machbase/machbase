---
type: docs
title: 'SDK별 APPEND 지원 범위 안내'
weight: 10
---

Machbase Neo의 **Append API**는 대량 데이터를 고속으로 삽입하기 위한 전용 프로토콜입니다. 일반 `INSERT` SQL 대비 수십 배 이상의 처리량을 제공하며, 시계열 데이터 수집 시나리오에서 핵심적으로 사용됩니다.

## SDK별 Append API 지원 현황

| SDK | Append 지원 | API / 메서드 | 비고 |
|-----|:-----------:|--------------|------|
| **ODBC / CLI** | O | `SQLAppendOpen` / `SQLAppendData` / `SQLAppendClose` | 전체 지원, 최고 성능 |
| **JDBC** | O | `MachStatement` Append 메서드 | `executeAppendOpen` / `executeAppendData` / `executeAppendFlush` |
| **Python** | O | `conn.append(table, rows)` | `machbaseAPI` 패키지 |
| **.NET** | O | `MachCommand` + `MachAppendWriter` | `MachCommand.AppendOpen(tableName)` |
| **Go (native)** | O | `AppendWriter` | `conn.Appender(ctx, tableName)` |
| **Go (database/sql)** | X | 없음 | Append는 `machgo` 네이티브 클라이언트 사용 |
| **Node.js** | O | `appendBatch` / `appendOpen` | LOG/TAG Append 지원 |
| **REST API** | O | `POST /machbase` | HTTP JSON Append |

- **O**: 완전 지원
- **X**: 미지원

## ODBC / CLI: Append 사용 예시

```c
#include <machbase_sqlcli.h>

SQLHSTMT stmt;
SQLAllocStmt(conn, &stmt);

// Append 세션 시작
SQLAppendOpen(stmt, "sensor_data", 0);

// 데이터 행 추가
SQL_APPEND_PARAM param[3];
// name, time(나노초), value 순으로 바인딩
param[0].mVarchar.mLength = strlen("sensor01");
strcpy(param[0].mVarchar.mData, "sensor01");
param[1].mDateTime.mTime = 1720000000000000000LL; // 나노초 타임스탬프
param[2].mDouble          = 25.3;

SQLAppendDataV2(stmt, param);

// Append 세션 종료 및 커밋
SQLAppendClose(stmt, NULL, NULL);
SQLFreeStmt(stmt, SQL_DROP);
```

## JDBC: MachStatement Append 사용 예시

```java
import java.sql.*;
import java.util.*;
import com.machbase.jdbc.MachStatement;

Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER"
);
MachStatement stmt = (MachStatement) conn.createStatement();

// Append 세션 시작
ResultSet rs = stmt.executeAppendOpen("sensor_data", 100);
ResultSetMetaData rsmd = rs.getMetaData();

// 행 추가 (컬럼 순서대로 값 추가)
ArrayList<Object> row = new ArrayList<>();
row.add("sensor01");
row.add(System.currentTimeMillis() * 1_000_000L);
row.add(25.3);
stmt.executeAppendData(rsmd, row);

// pending 응답 확인 및 종료
stmt.executeAppendFlush();
stmt.executeAppendClose();
conn.close();
```

## Python: conn.append() 사용 예시

```python
from machbaseAPI import connect
from datetime import datetime

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# 여러 행을 한 번에 Append
rows = [
    ['sensor01', datetime.now(), 25.3],
    ['sensor02', datetime.now(), 30.1],
    ['sensor03', datetime.now(), 18.7],
]
conn.append('sensor_data', rows)

conn.close()
```

## .NET: MachAppendWriter 사용 예시

```csharp
using System.Collections.Generic;
using Mach.Data.MachClient;

string connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(connString);
conn.Open();

using var appendCmd = new MachCommand(conn);
var writer = appendCmd.AppendOpen("sensor_data");

// 행 추가
var row = new List<object> { "sensor01", DateTime.UtcNow, 25.3 };
appendCmd.AppendData(writer, row);

// 완료
appendCmd.AppendFlush(writer);
appendCmd.AppendClose(writer);
```

## Go (native): Appender 사용 예시

```go
package main

import (
    "context"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    ctx := context.Background()
    mdb, err := machgo.NewDatabase(&machgo.Config{
        Host: "127.0.0.1",
        Port: 5656,
    })
    if err != nil {
        log.Fatal(err)
    }

    conn, err := mdb.Connect(ctx, api.WithPassword("SYS", "MANAGER"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    appender, err := conn.Appender(ctx, "sensor_data")
    if err != nil {
        log.Fatal(err)
    }
    defer appender.Close()

    if err := appender.Append("sensor01", time.Now(), 25.3); err != nil {
        log.Fatal(err)
    }
}
```

## REST API: POST /machbase

REST API를 통한 Append는 JSON 본문에 테이블 이름과 행 배열을 전달합니다.

```bash
curl -X POST "http://localhost:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_data","values":[["sensor01",1720000000000000000,25.3],["sensor02",1720000000000000001,30.1]]}'
```

성공 시 Append 결과 건수를 반환합니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "append_success": 2,
  "append_failure": 0
}
```

## Append API 성능 특성

| 특성 | 설명 |
|------|------|
| **원자성** | Append는 트랜잭션 없이 동작 (즉시 커밋) |
| **대상 테이블** | TAG 테이블, LOG 테이블 지원 |
| **배치 크기** | 1,000 ~ 10,000행 단위로 플러시하는 것을 권장 |
| **병렬 처리** | 여러 스레드에서 각각 독립적인 Appender 사용 가능 |
| **롤백 불가** | Append 완료된 데이터는 롤백할 수 없음 |

> **참고**: RDB(Lookup) 테이블에 대한 Append API 사용은 지원되지 않습니다. RDB 테이블에는 일반 `INSERT` SQL을 사용하세요.
