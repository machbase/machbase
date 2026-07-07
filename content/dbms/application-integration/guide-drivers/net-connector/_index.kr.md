---
type: docs
title: '.NET Connector'
weight: 50
---

## 개요 {#overview}

Machbase는 모든 지원 와이어 프로토콜(2.1~4.0)을 포괄하는 범용 ADO.NET 프로바이더 **UniMachNetConnector**를 제공합니다. 커넥터는 실행 시 커넥션 문자열을 참고해 올바른 프로토콜을 자동으로 협상하므로, 시계열 데이터 수집·질의 워크로드에도 별도 설정 없이 적합한 프로토콜을 선택합니다.

- 현재 통합 패키지: `UniMachNetConnector` 8.0.54
- 지원 타깃 프레임워크: `net452`, `net5.0`, `net6.0`, `net7.0`, `net8.0`
- 네임스페이스: `Mach.Data.MachClient`

## 설치 {#install}

### NuGet 패키지 설치 (권장) {#nuget}

새 프로젝트에는 NuGet 패키지 참조 방식을 권장합니다.

```bash
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

**Visual Studio**를 사용하는 경우:

1. 프로젝트 마우스 오른쪽 클릭 → **NuGet 패키지 관리**
2. **찾아보기** 탭에서 `UniMachNetConnector` 검색
3. 버전 8.0.54 선택 → **설치**

**프로젝트 파일(`.csproj`) 직접 편집:**

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
</ItemGroup>
```

### 로컬 DLL 참조

설치된 Machbase 서버·클라이언트에는 `$MACHBASE_HOME/lib/` 경로에 범용 .NET 프로바이더가 함께 배포됩니다.

- `UniMachNetConnector-net50-8.0.54.dll` – universal entry point
- `machNetConnector-40-net50-3.2.1.dll` – protocol 4.0-full connector

응용 프로그램에서는 대상 프레임워크에 맞는 DLL을 참조하거나, 배포 시 실행 파일과 같은 위치에 함께 배치하면 됩니다.

## 커넥션 문자열 {#connection-string}

커넥션 문자열의 각 항목은 세미콜론(`;`)으로 구분합니다.

| 키워드 | 설명 | 예시 | 기본값 |
|--------|------|------|--------|
| `SERVER`, `HOST`, `DSN` | 호스트명 또는 IP 주소 | `SERVER=127.0.0.1` | 없음 |
| `PORT`, `PORT_NO` | 수신 포트 | `PORT_NO=5656` | `5656` |
| `UID`, `USER`, `USERNAME`, `USERID` | 사용자 이름 | `UID=SYS` | `SYS` |
| `PWD`, `PASSWORD` | 비밀번호 | `PWD=MANAGER` | 없음 |
| `CONNECT_TIMEOUT`, `ConnectionTimeout` | 커넥션 타임아웃(밀리초) | `CONNECT_TIMEOUT=10000` | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout` | 명령별 타임아웃(밀리초) | `COMMAND_TIMEOUT=50000` | `60000` |
| `PROTOCOL`, `ProtocolVersion` | 와이어 프로토콜 (`2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full`) | `PROTOCOL=4.0-full` | `4.0` |

**예시:**

```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
```

### 프로토콜 자동 감지

서버 버전이 혼재된 환경이라면 `PROTOCOL=auto`를 지정해 커넥터가 실행 시 적절한 프로토콜을 협상하도록 설정할 수 있습니다.

- `PROTOCOL=auto`: 4.0 → 3.0 → 2.2 → 2.1 순서로 핸드셰이크 시도
- `PROTOCOL=auto-full`: 위와 같지만 4.0-full을 먼저 시도하고 필요 시 4.0으로 폴백

이미 서버 버전을 알고 있다면 명시적으로 지정해 자동 감지를 건너뛰는 것이 좋습니다.

## API 레퍼런스 {#api-reference}

{{< callout type="warning" >}}
아래에 명시되지 않은 기능은 아직 구현되지 않았거나 정상적으로 동작하지 않을 수 있습니다. 존재하지 않는 메서드나 필드를 호출하면 `NotImplementedException` 또는 `NotSupportedException`이 발생합니다.
{{< /callout >}}

### MachConnection

```csharp
public sealed class MachConnection : DbConnection
```

Machbase와의 연결을 담당하는 클래스입니다. `IDisposable`을 구현하므로 `using` 문으로 안전하게 해제할 수 있습니다.

| 멤버 | 설명 |
|------|------|
| `MachConnection(string connString)` | 커넥션 문자열로 인스턴스 생성 |
| `Open()` | 실제 연결 수립 |
| `Close()` | 연결 종료 |
| `SetConnectAppendFlush(bool)` | Append 중 자동 flush 활성화 여부 설정 |
| `State` | `System.Data.ConnectionState` 현재 상태 |

### MachCommand

```csharp
public sealed class MachCommand : DbCommand
```

SQL 명령이나 Append 작업을 실행하는 클래스입니다.

| 멤버 | 설명 |
|------|------|
| `MachCommand(string sql, MachConnection conn)` | 쿼리와 연결 객체로 생성 |
| `MachCommand(MachConnection conn)` | Append 전용 커맨드 생성 |
| `ExecuteNonQuery()` | INSERT/UPDATE/DELETE/DDL 실행, 영향받은 레코드 수 반환 |
| `ExecuteScalar()` | 첫 번째 컬럼 값 반환 |
| `ExecuteReader()` | `MachDataReader` 반환 |
| `AppendOpen(tableName, errorCheckCount, option)` | Append 세션 열기, `MachAppendWriter` 반환 |
| `AppendData(writer, dataList)` | 리스트의 값을 Append 버퍼에 적재 |
| `AppendDataWithTime(writer, dataList, DateTime)` | `_arrival_time`을 `DateTime`으로 지정 |
| `AppendDataWithTime(writer, dataList, ulong)` | `_arrival_time`을 나노초 `ulong`으로 지정 |
| `AppendFlush(writer)` | 버퍼를 즉시 서버로 전송 |
| `AppendClose(writer)` | Append 세션 종료 |
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수 (기본값: 3000) |

### MachDataReader

```csharp
public sealed class MachDataReader : DbDataReader
```

`MachCommand.ExecuteReader()`로 획득하는 순차 결과 리더입니다.

| 멤버 | 설명 |
|------|------|
| `Read()` | 다음 레코드 읽기. 결과가 없으면 `false` 반환 |
| `GetName(int ordinal)` | 컬럼 이름 반환 |
| `GetValue(int ordinal)` | 현재 레코드 값을 `object`로 반환 |
| `GetInt32/GetInt64/GetDouble/GetString/GetDateTime(int)` | 타입별 값 반환 |
| `IsDBNull(int ordinal)` | NULL 여부 확인 |
| `FieldCount` | 결과 컬럼 수 |
| `HasRows` | 결과 존재 여부 |

### MachAppendWriter

`MachCommand.AppendOpen()` 호출 시 반환되는 보조 클래스입니다.

| 멤버 | 설명 |
|------|------|
| `SetErrorDelegator(callback)` | Append 오류 발생 시 호출할 델리게이트 등록 |
| `SuccessCount` | 성공적으로 저장된 레코드 수 (`AppendClose()` 이후 확인) |
| `FailureCount` | 실패한 레코드 수 (`AppendClose()` 이후 확인) |

### MachParameterCollection

파라미터 바인딩을 위한 컬렉션입니다. `MachCommand.ParameterCollection`으로 접근합니다.

| 멤버 | 설명 |
|------|------|
| `Add(name, DbType)` | 파라미터 이름과 타입으로 추가 |
| `AddWithValue(name, value)` | 이름과 값으로 추가 |
| `Clear()` | 모든 파라미터 제거 |

## 사용 예제 {#examples}

### 연결

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using (var conn = new MachConnection(connString))
{
    conn.Open();
    // 작업 수행
} // using 블록 종료 시 자동으로 Close()
```

### 테이블 생성 및 INSERT

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

// 테이블 생성
using (var cmd = new MachCommand(
    "CREATE TAG TABLE IF NOT EXISTS sensor_data (" +
    "  name VARCHAR(100) PRIMARY KEY," +
    "  time DATETIME BASETIME," +
    "  value DOUBLE" +
    ")", conn))
{
    cmd.ExecuteNonQuery();
}

// 단건 INSERT
using (var cmd = new MachCommand(
    "INSERT INTO sensor_data VALUES (?, ?, ?)", conn))
{
    cmd.ParameterCollection.AddWithValue("@name", "sensor-1");
    cmd.ParameterCollection.AddWithValue("@time", DateTime.UtcNow);
    cmd.ParameterCollection.AddWithValue("@value", 3.14);
    cmd.ExecuteNonQuery();
}
```

### SELECT 조회

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

using var cmd = new MachCommand(
    "SELECT name, time, value FROM sensor_data ORDER BY time DESC LIMIT 10",
    conn);
using var reader = cmd.ExecuteReader();

while (reader.Read())
{
    Console.WriteLine($"name={reader.GetString(0)}, " +
                      $"time={reader.GetDateTime(1)}, " +
                      $"value={reader.GetDouble(2)}");
}
```

### 파라미터 바인딩

시계열 범위 조회 등에 파라미터를 사용해 SQL 인젝션을 방지할 수 있습니다.

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

const string sql = @"
    SELECT name, time, value
      FROM sensor_data
     WHERE time >= @StartTime
       AND time <  @EndTime
     ORDER BY time";

using var cmd = new MachCommand(sql, conn);

var now  = DateTime.UtcNow;
var past = now.AddMinutes(-10);

cmd.ParameterCollection.Add(new MachParameter { ParameterName = "@StartTime", Value = past });
cmd.ParameterCollection.Add(new MachParameter { ParameterName = "@EndTime",   Value = now  });

using var reader = cmd.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetString(0)}: {reader.GetDouble(2)}");
}
```

### Append API (고속 대량 삽입)

Append 프로토콜을 사용하면 표준 INSERT보다 훨씬 빠르게 대량의 시계열 데이터를 적재할 수 있습니다.

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

using var appendCmd = new MachCommand(conn);
var writer = appendCmd.AppendOpen("sensor_data");

// 오류 발생 시 처리할 델리게이트 등록
writer.SetErrorDelegator(e =>
{
    Console.Error.WriteLine($"Append 오류: {e.Message}");
    Console.Error.WriteLine($"실패 레코드: {e.GetRowBuffer()}");
});

var row = new List<object>();
var baseTime = DateTime.UtcNow;

for (var i = 0; i < 100_000; i++)
{
    row.Add($"sensor-{i % 10}");
    row.Add(baseTime.AddMilliseconds(i));
    row.Add((double)i * 0.01);

    appendCmd.AppendData(writer, row);
    row.Clear();

    // 1000건마다 중간 flush
    if (i % 1000 == 0)
    {
        appendCmd.AppendFlush(writer);
    }
}

appendCmd.AppendClose(writer);
Console.WriteLine($"성공: {writer.SuccessCount}, 실패: {writer.FailureCount}");
```

### Append - _arrival_time 직접 지정

```csharp
// DateTime으로 arrival time 지정
appendCmd.AppendDataWithTime(writer, row, DateTime.UtcNow);

// 나노초(ulong)로 arrival time 지정 (1970-01-01 UTC 기준)
ulong nanoTs = (ulong)(DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() * 1_000_000L);
appendCmd.AppendDataWithTime(writer, row, nanoTs);
```

## 프로토콜 4.0-full 확장 API {#protocol-40-full}

`PROTOCOL=4.0-full`을 사용하면 추가적인 ADO.NET 기능을 활용할 수 있습니다. Machbase 7.x 이상 서버에서만 사용 가능합니다.

### 추가 제공 타입

| 타입 | 설명 |
|------|------|
| `MachDbProviderFactory` | `DbProviderFactories` 등록/생성 지원 |
| `MachConnectionStringBuilder` | 키워드 오타 없이 커넥션 문자열 구성 |
| `MachDataAdapter` | `DataTable`/`DataSet` 기반 워크플로 지원 |
| `MachCommandBuilder` | SELECT 문으로부터 INSERT 구문 자동 생성 |

### MachConnectionStringBuilder 사용

```csharp
using Mach.Data.MachClient;

var builder = new MachConnectionStringBuilder
{
    Server   = "127.0.0.1",
    Port     = 5656,
    UserID   = "SYS",
    Password = "MANAGER"
};
builder["PROTOCOL"] = "4.0-full";

using var conn = new MachConnection(builder.ConnectionString);
conn.Open();
```

### MachDbProviderFactory 활용

Dapper 등 프로바이더 중립 라이브러리와 연동 시 활용합니다.

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

// 시작 시 한 번만 등록
MachDbProviderFactory.Register();

DbProviderFactory factory = MachDbProviderFactory.Instance;
using DbConnection conn = factory.CreateConnection()!;
conn.ConnectionString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
conn.Open();

using DbCommand cmd = conn.CreateCommand();
cmd.CommandText = "SELECT COUNT(*) FROM M$SYS_TABLES";
var count = (long)cmd.ExecuteScalar()!;
Console.WriteLine($"테이블 수: {count}");
```

### MachDataAdapter로 Lookup 테이블 조작

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";

using var conn = new MachConnection(connString);
conn.Open();

var adapter = new MachDataAdapter("SELECT id, name FROM lookup_table ORDER BY id", conn);
var cmdBuilder = new MachCommandBuilder(adapter);

var table = new DataTable();
adapter.Fill(table);

var newRow = table.NewRow();
newRow["id"]   = 1001;
newRow["name"] = "새 항목";
table.Rows.Add(newRow);

adapter.Update(table);
```

{{< callout type="info" >}}
로그 테이블과 태그 테이블은 UPDATE를 지원하지 않습니다. UPDATE/DELETE가 필요한 경우에는 Lookup 또는 Volatile 테이블을 사용하세요.
{{< /callout >}}

## Entity Framework / LINQ {#ef-linq}

현재 UniMachNetConnector는 Entity Framework Core의 공식 프로바이더를 제공하지 않습니다. ADO.NET 직접 사용(`MachConnection`, `MachCommand`, `MachDataReader`) 또는 Dapper 같은 마이크로 ORM과 함께 사용하는 것을 권장합니다.

`4.0-full` 프로토콜의 `MachDbProviderFactory`를 통해 Dapper와 연동하면 LINQ 스타일의 편의성을 일부 활용할 수 있습니다.
