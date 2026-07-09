---
type: docs
title: '15.8 애플리케이션 연동 예제'
weight: 130
---

주요 언어별 Machbase 연동 최소 예제를 모아 제공합니다. 각 예제는 연결 → 데이터 삽입(Append) → 조회의 3단계로 구성됩니다.

## Python

`machbaseAPI` 패키지의 `machbase()` 클래스를 사용하는 방법입니다.

```python
import json, re
from machbaseAPI.machbaseAPI import machbase

# 연결
db = machbase()
db.open('127.0.0.1', 'SYS', 'MANAGER', 5656)

# 테이블 컬럼 정보 조회 (Append에 필요)
table_name = 'sensor_tag'
db.columns(table_name)
import re, json
columns_raw = db.result()
types = [json.loads(item).get('type')
         for item in re.findall(r'\{[^}]+\}', columns_raw)]

# Append (대량 삽입)
import time
values = [
    ['sensor-01', int(time.time() * 1_000_000_000), 23.5],
    ['sensor-02', int(time.time() * 1_000_000_000), 45.1],
]
db.append(table_name, types, values, 'YYYY-MM-DD HH24:MI:SS')

# 조회
db.execute('SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 5')
print(db.result())

db.close()
```

상세 내용: [Python 드라이버 가이드](../application-integration/guide-drivers/python/)

## Java (JDBC + Append API)

JDBC Append API(`MachStatement`)를 사용해 고속 삽입합니다.

```java
import java.sql.*;
import java.util.ArrayList;
import com.machbase.jdbc.MachStatement;

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
Properties props = new Properties();
props.setProperty("user", "SYS");
props.setProperty("password", "MANAGER");

Connection conn = DriverManager.getConnection(url, props);
MachStatement stmt = (MachStatement) conn.createStatement();

// Append 시작
ResultSet rs = stmt.executeAppendOpen("sensor_tag", 100);
ResultSetMetaData rsmd = rs.getMetaData();

// 데이터 삽입
ArrayList<Object> row = new ArrayList<>();
row.add("sensor-01");                            // name
row.add(System.currentTimeMillis() * 1_000_000L); // time (ns)
row.add(23.5);                                    // value
stmt.executeAppendData(rsmd, row);

// 완료
stmt.executeAppendClose();
conn.close();
```

상세 내용: [JDBC 드라이버 가이드](../application-integration/guide-drivers/jdbc/)

## Go (native client)

`github.com/machbase/neo-client/machcli` 패키지를 사용합니다.

```go
package main

import (
    "context"
    "fmt"
    "time"
    "github.com/machbase/neo-client/machcli"
)

func main() {
    db, err := machcli.New("tcp://127.0.0.1:5656",
        machcli.WithUser("SYS"),
        machcli.WithPassword("MANAGER"),
    )
    if err != nil {
        panic(err)
    }
    defer db.Close()

    ctx := context.Background()

    // INSERT
    _, err = db.Exec(ctx,
        "INSERT INTO sensor_tag (name, time, value) VALUES (?, ?, ?)",
        "sensor-01", time.Now().UnixNano(), 23.5,
    )
    if err != nil {
        panic(err)
    }

    // 조회
    rows, err := db.Query(ctx,
        "SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 5")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    for rows.Next() {
        var name string
        var ts int64
        var val float64
        rows.Scan(&name, &ts, &val)
        fmt.Printf("%s %d %.2f\n", name, ts, val)
    }
}
```

상세 내용: [Go native client 가이드](../application-integration/guide-drivers/go/go/)

## REST API (curl)

별도 드라이버 없이 HTTP로 직접 조회합니다.

```bash
# 조회
curl -s -G 'http://localhost:5657/machbase' \
  --data-urlencode "q=SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 5" \
  -u SYS:MANAGER

# INSERT도 SQL endpoint로 실행할 수 있습니다.
curl -s -G 'http://localhost:5657/machbase' \
  --data-urlencode "q=INSERT INTO sensor_tag VALUES ('sensor-01', TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 23.5)" \
  -u SYS:MANAGER
```

상세 내용: [REST API 가이드](../application-integration/rest-api/)

## Node.js / TypeScript

`@machbase/ts-client` 패키지를 사용합니다.

```typescript
import { Client } from '@machbase/ts-client';

const client = new Client({
    host: '127.0.0.1',
    port: 5654,
    user: 'SYS',
    password: 'MANAGER',
});

await client.connect();

// 조회
const result = await client.query(
    'SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 5'
);
console.log(result.data.rows);

await client.disconnect();
```

상세 내용: [Node.js/TypeScript 드라이버 가이드](../application-integration/guide-drivers/node-js-typescript/)

## .NET

`MachConnector` NuGet 패키지를 사용합니다.

```csharp
using Mach.Data.MachClient;

var conn = new MachConnection("DSN=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;");
conn.Open();

// INSERT
var cmd = conn.CreateCommand();
cmd.CommandText = "INSERT INTO sensor_tag (name, time, value) VALUES (?, ?, ?)";
cmd.Parameters.Add(new MachParameter { Value = "sensor-01" });
cmd.Parameters.Add(new MachParameter { Value = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() * 1_000_000L });
cmd.Parameters.Add(new MachParameter { Value = 23.5 });
cmd.ExecuteNonQuery();

// 조회
cmd.CommandText = "SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 5";
using var reader = cmd.ExecuteReader();
while (reader.Read())
    Console.WriteLine($"{reader[0]} {reader[1]} {reader[2]}");

conn.Close();
```

상세 내용: [.NET Connector 드라이버 가이드](../application-integration/guide-drivers/net-connector/)

## 언어별 드라이버 선택 가이드

| 언어 | 패키지 | Append API | 트랜잭션(RDB) |
|------|--------|:---:|:---:|
| Python | `machbaseAPI` | O | O |
| Java | JDBC (`machbase-jdbc`) | O | O |
| Go | `machcli` (native) | O | X |
| Go | `database/sql` | X | X |
| Node.js | `@machbase/ts-client` | O | X |
| .NET | `MachConnector` | O | O |
| REST API | HTTP | O | X |

전체 SDK 지원 범위: [SDK별 Append/AUTH KEY/Transaction/Prepare 지원 범위](../application-integration/support-scope-sdk/)
