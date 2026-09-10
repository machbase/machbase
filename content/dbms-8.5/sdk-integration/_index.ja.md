---
type: docs
title: 'SDK と連携'
weight: 120
toc: true
---

さまざまな言語とプロトコルから Machbase に接続するための SDK、API、連携方法を説明します。

## SDK と API {#available-sdks-and-apis}

### ODBC/CLI (C/C++) {#odbccli-cc}

高い性能を得るためのネイティブ C/C++ API：
- DB への直接アクセス
- 一括入力用 APPEND プロトコル
- 低遅延
- 全機能のサポート

**用途**：C/C++ 開発、最大限の性能が必要な場合

[詳細](cli-odbc/)

### JDBC (Java) {#jdbc-java}

Java 用の標準 JDBC ドライバー：
- 標準 JDBC インターフェース
- コネクションプール
- Spring/Hibernate との互換性
- AUTH KEY チャレンジ認証（Machbase 8.5 以降）
- APPEND API

**用途**：Java 開発、標準 JDBC が必要な場合

[詳細](jdbc/)

### Python {#python}

Python クライアントライブラリー：
- Python に適した API
- Pandas 連携
- 簡単な接続管理
- データのインポートとエクスポート

**用途**：データサイエンス、スクリプト、Python アプリケーション

[詳細](python/)

### .NET (C#) {#net-c}

C# 用の .NET プロバイダー：
- ADO.NET 互換
- コネクションプール
- LINQ サポート
- Entity Framework 互換

**用途**：.NET/C# 開発

[詳細](dotnet/)

### REST API {#rest-api}

Web アプリケーション用の HTTP API：
- 言語に依存しない
- JSON 応答
- 簡単な連携
- Web に適した構成

**用途**：Web、マイクロサービス、HTTP のみ使用可能な環境

この DBMS セクションに REST API リファレンスは含まれません。

## クイックスタートの例 {#quick-start-examples}

### C/C++ (ODBC/CLI) {#cc-odbccli}

```c
#include <machbase_sqlcli.h>

SQLHENV env;
SQLHDBC conn;
SQLHSTMT stmt;

// 接続
SQLAllocEnv(&env);
SQLAllocConnect(env, &conn);
SQLConnect(conn, "127.0.0.1", SQL_NTS, "SYS", SQL_NTS, "MANAGER", SQL_NTS);

// 検索
SQLAllocStmt(conn, &stmt);
SQLExecDirect(stmt, "SELECT * FROM sensors DURATION 1 HOUR", SQL_NTS);

// 後処理
SQLFreeStmt(stmt, SQL_DROP);
SQLDisconnect(conn);
```

### Java (JDBC) {#java-jdbc}

```java
Class.forName("com.machbase.jdbc.MachDriver");
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

### Python {#python-1}

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
for row in cur.fetchall():
    print(row)

conn.close()
```

### C# (.NET) {#c-net}

```csharp
using Mach.Data.MachClient;

string connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
MachConnection conn = new MachConnection(connString);
conn.Open();

MachCommand cmd = new MachCommand("SELECT * FROM sensors DURATION 1 HOUR", conn);
MachDataReader reader = cmd.ExecuteReader();

while (reader.Read()) {
    Console.WriteLine(reader.GetString(0));
}
```

### REST API (JavaScript) {#rest-api-javascript}

```javascript
const params = new URLSearchParams({
    q: 'SELECT * FROM sensors DURATION 1 HOUR'
});

const response = await fetch(`http://localhost:5657/machbase?${params}`);

const data = await response.json();
console.log(data);
```

## 連携パターン {#integration-patterns}

### パターン 1：リアルタイムのデータ収集 {#pattern-1-real-time-data-collection}

```python
# センサーデータの収集
from machbaseAPI import connect
import time

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

while True:
    rows = []
    for i in range(1000):
        sensor_id = f'sensor{i % 100:03d}'
        value = read_sensor(sensor_id)
        rows.append([sensor_id, time.time(), value])

    conn.append('sensors', rows)
    time.sleep(10)
```

### パターン 2：ダッシュボード {#pattern-2-dashboard-application}

```java
// リアルタイムダッシュボードのバックエンド
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

### パターン 3：バッチ処理 {#pattern-3-batch-processing}

```csharp
// 夜間バッチジョブ
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

## 接続管理 {#connection-management}

### コネクションプール（Java） {#connection-pooling-java}

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

### 接続の再試行（Python） {#connection-retry-python}

```python
import time
from machbaseAPI import connect

def connect_with_retry(max_retries=3):
    for i in range(max_retries):
        try:
            return connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(1)
```

## 性能向上のヒント {#performance-tips}

1. **一括入力には APPEND API を使用**
2. **コネクションプールを有効化**
3. **操作をまとめる**（1000 ～ 10000 行）
4. **プリペアードステートメントを再利用**
5. **リソースを正しく解放**

## フレームワーク連携 {#framework-integration}

### Spring Boot (Java) {#spring-boot-java}

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:machbase://127.0.0.1:5656/MACHBASE
    username: SYS
    password: MANAGER
    driver-class-name: com.machbase.jdbc.MachDriver
```

### 汎用 DB-API（Python） {#generic-db-api-python}

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()
cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
rows = cur.fetchall()
conn.close()
```

## セキュリティの推奨事項 {#security-best-practices}

1. 認証情報には**環境変数を使用**
2. 接続に **SSL/TLS を有効化**
3. レポートには**読み取り専用ユーザーを使用**
4. **接続タイムアウトを設定**
5. **入力値を検証し、無害化**

## トラブルシューティング {#troubleshooting}

### 接続の失敗 {#connection-fails}

```python
# 状態を確認
import socket

try:
    sock = socket.socket()
    sock.connect(('127.0.0.1', 5656))
    print("Server is reachable")
except:
    print("Cannot connect to server")
```

### 性能の問題 {#performance-issues}

- 一括入力には APPEND API を使用
- コネクションプールを有効化
- 操作をバッチ化
- ネットワーク遅延を確認

### メモリの問題 {#memory-issues}

- 結果セットのサイズを制限
- サーバー側カーソルを使用
- データを分割して処理
- リソースを速やかに解放

## アプリケーションの例 {#example-applications}

### Python アプリケーションの全体例 {#complete-python-application}

```python
#!/usr/bin/env python3
from machbaseAPI import connect
import time
from datetime import datetime

class SensorMonitor:
    def __init__(self):
        self.conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

    def collect_data(self, sensor_id, value):
        self.conn.append('sensors', [[sensor_id, datetime.now(), value]])

    def get_recent_data(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
        return cur.fetchall()

    def close(self):
        self.conn.close()

# 使用方法
monitor = SensorMonitor()
monitor.collect_data('sensor01', 25.3)
data = monitor.get_recent_data()
monitor.close()
```

## 次のステップ {#next-steps}

開発環境に合う SDK を選択してください。

- **C/C++**：[CLI/ODBC リファレンス](cli-odbc/)
- **Java**：[JDBC リファレンス](jdbc/)
- **Python**：[Python SDK リファレンス](python/)
- **.NET**：[.NET リファレンス](dotnet/)
- **Web/REST**：配置環境でエンドポイントを利用できる場合は HTTP 連携を使用。

## 関連ドキュメント {#related-documentation}

- [最初の操作](../getting-started/first-steps/)：接続の例
- [データのインポート](../table-types/log-tables/insert/import-data/)：一括読み込み
- [テーブルの種類](../table-types/)：実践例
