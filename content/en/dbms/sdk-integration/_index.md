---
title: 'SDK & Integration'
weight: 120
---

Integrate Machbase with your applications using various programming languages and protocols. This section covers all available SDKs, APIs, and integration methods.

## Available SDKs and APIs

### ODBC/CLI (C/C++)

Native C/C++ API for maximum performance:
- Direct database access
- APPEND protocol for bulk loading
- Lowest latency
- Full feature support

**Use when**: Building C/C++ applications, need maximum performance

[Complete Reference](../../dbms/sdk/cli-odbc/)

### JDBC (Java)

Standard JDBC driver for Java applications:
- Standard JDBC interface
- Connection pooling support
- Spring/Hibernate compatible
- APPEND API support

**Use when**: Building Java applications, need standard JDBC

[Complete Reference](../../dbms/sdk/jdbc/)

### Python

Python client library:
- Pythonic API
- Pandas integration
- Simple connection management
- Easy data import/export

**Use when**: Data science, scripting, Python applications

[Complete Reference](../../dbms/sdk/python/)

### .NET (C#)

.NET provider for C# applications:
- ADO.NET compatible
- Connection pooling
- LINQ support
- Entity Framework compatible

**Use when**: Building .NET/C# applications

[Complete Reference](../../dbms/sdk/dotnet/)

### REST API

HTTP-based API for web applications:
- Language-agnostic
- JSON responses
- Easy integration
- Web-friendly

**Use when**: Web applications, microservices, HTTP-only environments

[Complete Reference](../../dbms/sdk/restful_api/)

## Quick Start Examples

### C/C++ (ODBC/CLI)

```c
#include "machbase_cli.h"

SQLHENV env;
SQLHDBC conn;
SQLHSTMT stmt;

// Connect
SQLAllocEnv(&env);
SQLAllocConnect(env, &conn);
SQLConnect(conn, "127.0.0.1", SQL_NTS, "SYS", SQL_NTS, "MANAGER", SQL_NTS);

// Query
SQLAllocStmt(conn, &stmt);
SQLExecDirect(stmt, "SELECT * FROM sensors DURATION 1 HOUR", SQL_NTS);

// Cleanup
SQLFreeStmt(stmt, SQL_DROP);
SQLDisconnect(conn);
```

### Java (JDBC)

```java
Class.forName("com.machbase.jdbc.driver");
Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/MACHBASE",
    "SYS", "MANAGER"
);

Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM sensors DURATION 1 HOUR");

while (rs.next()) {
    System.out.println(rs.getString("sensor_id"));
}
```

### Python

```python
import machbase

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')
cur = conn.cursor()

cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
for row in cur.fetchall():
    print(row)

conn.close()
```

### C# (.NET)

```csharp
using Machbase.Data.MachbaseClient;

string connString = "Server=127.0.0.1;Port=5656;User Id=SYS;Password=MANAGER;";
MachConnection conn = new MachConnection(connString);
conn.Open();

MachCommand cmd = new MachCommand("SELECT * FROM sensors DURATION 1 HOUR", conn);
MachDataReader reader = cmd.ExecuteReader();

while (reader.Read()) {
    Console.WriteLine(reader.GetString(0));
}
```

### REST API (JavaScript)

```javascript
const response = await fetch('http://localhost:5654/machbase', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        sql: 'SELECT * FROM sensors DURATION 1 HOUR',
        format: 'json'
    })
});

const data = await response.json();
console.log(data);
```

## Integration Patterns

### Pattern 1: Real-Time Data Collection

```python
# Sensor data collector
import machbase
import time

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

while True:
    appender = conn.create_appender('sensors')

    for i in range(1000):
        sensor_id = f'sensor{i % 100:03d}'
        value = read_sensor(sensor_id)
        appender.append(sensor_id, time.time(), value)

    appender.close()
    time.sleep(10)
```

### Pattern 2: Dashboard Application

```java
// Real-time dashboard backend
@RestController
public class DashboardController {
    @Autowired
    private DataSource dataSource;

    @GetMapping("/api/sensors/current")
    public List<SensorData> getCurrentData() {
        String sql = "SELECT * FROM sensors DURATION 5 MINUTE";
        return jdbcTemplate.query(sql, new SensorDataMapper());
    }
}
```

### Pattern 3: Batch Processing

```csharp
// Nightly batch job
public class BatchProcessor {
    public void ProcessDailyData() {
        using (var conn = new MachConnection(connString)) {
            conn.Open();

            var sql = @"
                SELECT sensor_id, AVG(value), MAX(value), MIN(value)
                FROM sensors
                WHERE _arrival_time >= SYSDATE - 1
                GROUP BY sensor_id
            ";

            var cmd = new MachCommand(sql, conn);
            var reader = cmd.ExecuteReader();

            while (reader.Read()) {
                ProcessSensorStats(reader);
            }
        }
    }
}
```

## Connection Management

### Connection Pooling (Java)

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/MACHBASE");
config.setUsername("SYS");
config.setPassword("MANAGER");
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);

HikariDataSource pool = new HikariDataSource(config);
```

### Connection Retry (Python)

```python
def connect_with_retry(max_retries=3):
    for i in range(max_retries):
        try:
            return machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(1)
```

## Performance Tips

1. **Use APPEND API for bulk inserts**
2. **Enable connection pooling**
3. **Batch operations** (1000-10000 rows)
4. **Reuse prepared statements**
5. **Close resources properly**

## Framework Integration

### Spring Boot (Java)

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:machbase://127.0.0.1:5656/MACHBASE
    username: SYS
    password: MANAGER
    driver-class-name: com.machbase.jdbc.driver
```

### Django (Python)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'machbase_django',
        'NAME': 'MACHBASE',
        'USER': 'SYS',
        'PASSWORD': 'MANAGER',
        'HOST': '127.0.0.1',
        'PORT': '5656',
    }
}
```

## Security Best Practices

1. **Use environment variables** for credentials
2. **Enable SSL/TLS** for connections
3. **Use read-only users** for reporting
4. **Implement connection timeouts**
5. **Validate and sanitize input**

## Troubleshooting

### Connection Fails

```python
# Check server status
import socket

try:
    sock = socket.socket()
    sock.connect(('127.0.0.1', 5656))
    print("Server is reachable")
except:
    print("Cannot connect to server")
```

### Performance Issues

- Use APPEND API for bulk inserts
- Enable connection pooling
- Batch operations
- Check network latency

### Memory Issues

- Limit result set size
- Use server-side cursors
- Process data in chunks
- Close resources promptly

## Example Applications

### Complete Python Application

```python
#!/usr/bin/env python3
import machbase
import time
from datetime import datetime

class SensorMonitor:
    def __init__(self):
        self.conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

    def collect_data(self, sensor_id, value):
        appender = self.conn.create_appender('sensors')
        appender.append(sensor_id, datetime.now(), value)
        appender.close()

    def get_recent_data(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
        return cur.fetchall()

    def close(self):
        self.conn.close()

# Usage
monitor = SensorMonitor()
monitor.collect_data('sensor01', 25.3)
data = monitor.get_recent_data()
monitor.close()
```

## Next Steps

Choose the SDK that matches your development environment:

- **C/C++**: [CLI/ODBC Reference](../../dbms/sdk/cli-odbc/)
- **Java**: [JDBC Reference](../../dbms/sdk/jdbc/)
- **Python**: [Python SDK Reference](../../dbms/sdk/python/)
- **.NET**: [.NET Reference](../../dbms/sdk/dotnet/)
- **Web/REST**: [REST API Reference](../../dbms/sdk/restful_api/)

## Related Documentation

- [Common Tasks: Connecting](../common-tasks/connecting/) - Connection examples
- [Common Tasks: Importing Data](../common-tasks/importing-data/) - Bulk loading
- [Tutorials](../tutorials/) - Hands-on examples
