---
title: '.NET Connector'
type: docs
weight: 20
---

## 목차 {#index}

* [개요](#overview)
* [설치](#install)
* [NuGet(통합 8.0.51+)](#nuget-unified-connector)
* [레거시 NuGet(5.x) 설치](#install-connector-via-nuget-package-manager)
* [커넥션 문자열 참고](#connection-string-reference)
* [API 레퍼런스](#api-reference)
* [사용 예시](#usage-and-examples)
* [프로토콜 4.0-full 전체 API](#full-provider-apis-protocol-40-full)

## 개요 {#overview}

Machbase는 모든 지원 Machbase 와이어 프로토콜(2.1~4.0)을 포괄하는 범용 ADO.NET 프로바이더 **UniMachNetConnector**를 제공합니다. Machbase 8.0.51부터 이 커넥터가 서버 패키지에 기본 포함되며, DLL 파일명에 붙는 버전 번호는 빌드 또는 설치한 Machbase 버전과 동일합니다. 커넥터는 실행 시 커넥션 문자열을 참고해 올바른 프로토콜을 자동으로 협상하므로, 시계열 데이터 수집·질의 워크로드에도 별도 설정 없이 적합한 프로토콜을 선택합니다.

## 설치 {#install}

설치된 Machbase 서버·클라이언트에는 `$MACHBASE_HOME/lib/` 경로에 범용 .NET 프로바이더가 함께 배포됩니다. 설치 후 다음과 같은 파일을 볼 수 있습니다.

- **UniMachNetConnector**: 프레임워크에 구애받지 않는 진입점입니다. `UniMachNetConnector-net{50|60|70|80}-<version>.dll` 형식으로 제공되며, 대상 프레임워크에 맞는 파일을 선택하면 됩니다.
- **레거시 프로토콜 커넥터**: `machNetConnector-XX-net{50|60|70|80}-<version>.dll`과 같이 프로토콜별로 나뉜 어셈블리입니다. UniMachNetConnector가 필요 시 로드합니다.

응용 프로그램에서는 대상 프레임워크에 맞는 DLL(예: `UniMachNetConnector-net80-8.0.51.dll`)을 참조하거나, 배포 시 실행 파일과 같은 위치에 함께 배치하면 됩니다.

## NuGet로 설치 (통합 커넥터, 8.0.51+) {#nuget-unified-connector}

Machbase 8.0.51부터 통합 커넥터는 NuGet에도 `UniMachNetConnector` 패키지로 게시됩니다. 새 프로젝트에서는 DLL 복사 대신 NuGet 패키지 참조 방식을 권장합니다.

- 지원 TFM: net5.0, net6.0, net7.0, net8.0
- 외부 NuGet 의존성 없음(자급자족 패키지)

### 빠른 시작(명령줄)

```bash
# 프로젝트 폴더에서 실행
dotnet add package UniMachNetConnector --version 8.0.51
dotnet build
```

소스(피드)를 명시적으로 제어해야 하면 참조 추가만 하고, 별도로 복원하세요.

```bash
dotnet add package UniMachNetConnector --version 8.0.51 --no-restore

# nuget.org 메타데이터를 강제로 갱신
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- 프로젝트 마우스 오른쪽 클릭 → NuGet 패키지 관리 → 찾아보기 → “UniMachNetConnector” 검색 → 8.0.51 선택 → 설치.

### 프로젝트 파일 예시

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.51" />
  <!-- 추가 Machbase 패키지 불필요 -->
  <!-- 대상 프레임워크: net5.0|net6.0|net7.0|net8.0 -->
</ItemGroup>
```

### 로컬/사내 피드 사용(선택)

사내 레지스트리 또는 폴더 피드를 사용할 경우 다음과 같이 소스를 추가하고 복원합니다. 폴더 피드는 `UniMachNetConnector.8.0.51.nupkg`를 해당 디렉터리에 배치하면 됩니다.

```bash
# 1회 설정
dotnet nuget add source /path/to/local-nuget -n mach-local

# nuget.org와 병행 복원
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

권한 제약이 있는 환경에서는 패키지 캐시 경로를 절대 경로로 지정하세요.

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> 팁: 게시 직후 NU1102(지정 버전을 찾지 못함)나 “incompatible with 'all' frameworks”가 보이면 보통 인덱싱/캐시 이슈입니다. `dotnet nuget locals http-cache --clear` 후 `--no-cache`로 복원하면 해결됩니다. 패키지는 net5.0~net8.0을 지원합니다.

### 최소 사용 예시

```csharp
using Mach.Data.MachClient;

var cs = "SERVER=127.0.0.1;PORT_NO=55656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = (long)cmd.ExecuteScalar();
Console.WriteLine($"Tables: {count}");
```

## 레거시 NuGet(5.x) 설치 {#install-connector-via-nuget-package-manager}

> **참고**: Machbase .NET Connector 5.0 패키지는 NuGet에 등록되어 있으며, 통합형 UniMachNetConnector가 도입되기 이전의 독립 배포본입니다.

Visual Studio를 사용하면 기존(통합 이전) .NET Connector도 NuGet에서 받을 수 있습니다. 아래 절차는 `machNetConnector5.0` 패키지를 설치하는 방법입니다. (새 프로젝트에는 통합형 `UniMachNetConnector` 8.0.51+ 사용을 권장합니다.)

1. Visual Studio에서 새 C# .NET 프로젝트를 생성합니다.
2. 솔루션 탐색기에서 프로젝트 이름을 마우스 오른쪽 클릭하고 **NuGet 패키지 관리**를 선택합니다.
3. NuGet 패키지 관리자 창이 열리면 상단의 **찾아보기** 탭을 선택하고 `machNet`을 검색합니다.
4. 검색 결과 목록에서 **machNetConnector5.0**을 선택하고 **설치**를 클릭합니다.
5. **변경 내용 미리 보기** 창이 나타나면 **확인**을 눌러 설치를 계속합니다.
6. 설치가 완료되면 솔루션 탐색기 > **종속성 → 패키지**에서 설치된 패키지를 확인할 수 있습니다.
7. `Program.cs`에 `using Mach.Data.MachClient;`를 추가하면 machNetConnector API를 사용할 수 있습니다.

> 어떤 NuGet을 써야 하나요?
> - 신규/업그레이드 앱: `UniMachNetConnector` 8.0.51+ 권장(net5.0~net8.0 지원, 모든 프로토콜 및 4.0-full 포함).
> - 레거시 유지: 통합 패키지로 전환이 어려울 때만 `machNetConnector5.0`을 사용하세요.

## 커넥션 문자열 참고 {#connection-string-reference}

커넥션 문자열의 각 항목은 세미콜론(`;`)으로 구분합니다. 표의 한 행에 표시된 키워드는 서로 동일한 의미를 갖습니다.

| 키워드                                                         | 설명                                                                                                  | 예시                                             | 기본값  |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST`                                        | 호스트명 또는 IP 주소                                                                                 | `SERVER=127.0.0.1`                               | 없음    |
| `PORT`, `PORT_NO`                                              | 수신 포트                                                                                             | `PORT=55656`                                     | `5656`  |
| `USERID`, `USERNAME`, `USER`, `UID`                            | 사용자 이름                                                                                            | `UID=SYS`                                        | `SYS`   |
| `PASSWORD`, `PWD`                                              | 비밀번호                                                                                               | `PWD=manager`                                    | 없음    |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout`       | 커넥션 타임아웃(밀리초)                                                                                | `CONNECT_TIMEOUT=10000`                          | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout`          | 명령별 타임아웃(밀리초)                                                                               | `COMMAND_TIMEOUT=50000`                          | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol`                  | 선호하는 와이어 프로토콜 (`2.1`, `3.0`, `4.0`, `4.0-full` 등). 값을 지정하지 않으면 `4.0`을 사용합니다. | `PROTOCOL=4.0-full`                              | `4.0`   |

예시:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

## API 레퍼런스 {#api-reference}

{{< callout type="warning" >}}
아래에 명시되지 않은 기능은 아직 구현되지 않았거나 정상적으로 동작하지 않을 수 있습니다.<br>
존재하지 않는 메서드나 필드를 호출하면 `NotImplementedException` 또는 `NotSupportedException`이 발생합니다.
{{< /callout >}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

Machbase와의 연결을 담당하는 클래스입니다. `DbConnection`과 동일하게 `IDisposable`을 구현하므로 `Dispose()` 호출이나 `using` 문으로 안전하게 해제할 수 있습니다.

#### 생성자

```
MachConnection(string aConnectionString)
```

커넥션 문자열을 입력 받아 `MachConnection` 인스턴스를 생성합니다.

#### Open

```cs
void Open()
```

커넥션 문자열을 사용해 실제 연결을 수립합니다.

#### Close

```cs
void Close()
```

열려 있는 연결을 종료합니다.

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Append 작업 중 자동으로 flush를 수행할지 여부를 설정합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `State` | `System.Data.ConnectionState` 값을 나타냅니다. |
| `StatusString` | 현재 연결이 의존하는 `MachCommand`의 상태 문자열입니다. 내부 로깅용이므로 쿼리 상태 판단 용도로 사용하지 않는 것이 좋습니다. |

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

`MachConnection`을 통해 SQL 명령이나 Append 작업을 실행하는 클래스입니다. `DbCommand`와 마찬가지로 `IDisposable`을 구현합니다.

#### 생성자

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

실행할 쿼리와 연결 객체를 지정해 인스턴스를 생성합니다.

```cs
MachCommand(MachConnection aConn)
```

쿼리가 필요 없는 Append 전용 커맨드를 생성합니다.

#### CreateParameter

```cs
MachParameter CreateParameter()
```

새로운 `MachParameter`를 생성합니다.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

Append 세션을 열고 `MachAppendWriter`를 반환합니다.

* `aTableName`: 대상 테이블 이름
* `aErrorCheckCount`: 지정한 레코드 수마다 서버에 전송해 실패 여부를 확인합니다. 즉, 자동 `APPEND-FLUSH` 지점을 설정합니다.
* `option`: `None` 또는 `MicroSecTruncated` 옵션을 지정할 수 있습니다.

#### AppendData

```cs
void AppendData(MachAppendWriter writer, List<object> dataList)
```

리스트에 있는 값을 순서대로 Append 버퍼에 적재합니다. 각 값의 타입은 테이블 컬럼 타입과 일치해야 하며, 값이 부족하거나 초과하면 예외가 발생합니다.

> **참고**: `_arrival_time`을 `ulong`으로 직접 지정할 때는 Machbase가 기대하는 1970-01-01 UTC 기준 나노초 값을 입력해야 합니다.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    DateTime arrivalTime)
```

`_arrival_time`을 `DateTime`으로 명시적으로 지정합니다.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    ulong arrivalTime)
```

`_arrival_time`을 나노초 단위 `ulong`으로 지정합니다.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter writer)
```

버퍼에 쌓인 데이터를 즉시 서버로 전송합니다. 호출 주기가 짧을수록 장애 시 데이터 유실이 줄어들지만 처리량은 낮아집니다.

#### AppendClose

```cs
void AppendClose(MachAppendWriter writer)
```

Append 세션을 종료합니다. 내부적으로 `AppendFlush()` 호출 후 프로토콜을 마무리합니다.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

쿼리를 실행하고 영향을 받은 레코드 수를 반환합니다. 주로 `INSERT`, `UPDATE`, `DELETE`, DDL에서 사용합니다.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

쿼리를 실행하고 첫 번째 컬럼 값을 반환합니다.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior behavior)
```

쿼리를 실행하고 결과를 순차적으로 읽을 수 있는 `DbDataReader`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Connection` / `DbConnection` | 현재 연결된 `MachConnection`입니다. |
| `ParameterCollection` / `DbParameterCollection` | 바인딩에 사용할 파라미터 컬렉션입니다. |
| `CommandText` | 실행할 SQL 문자열입니다. |
| `CommandTimeout` | 서버 응답을 기다리는 최대 시간(밀리초)입니다. 값은 `MachConnection` 설정을 따르며 여기서는 조회만 가능합니다. |
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000입니다. |
| `IsAppendOpened` | Append 세션이 열려 있는지 여부입니다. |

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

Fetch된 결과를 순차적으로 읽는 리더입니다. `MachCommand.ExecuteDbDataReader()`로 획득한 객체만 사용할 수 있습니다.

#### GetName

```cs
string GetName(int ordinal)
```

지정한 인덱스의 컬럼 이름을 반환합니다.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Machbase 컬럼 타입 이름을 반환합니다.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

.NET 측 매핑 타입을 반환합니다.

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

컬럼 이름에 해당하는 인덱스를 반환합니다.

#### GetValue

```cs
object GetValue(int ordinal)
```

현재 레코드의 값을 `object`로 반환합니다.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

해당 컬럼 값이 `NULL`인지 확인합니다.

#### GetValues

```cs
int GetValues(object[] values)
```

현재 레코드의 값을 배열에 채워 넣고 채워진 항목 수를 반환합니다.

#### Get*XXXX*

```cs
bool GetBoolean(int ordinal)
byte GetByte(int ordinal)
char GetChar(int ordinal)
short GetInt16(int ordinal)
int GetInt32(int ordinal)
long GetInt64(int ordinal)
DateTime GetDateTime(int ordinal)
string GetString(int ordinal)
decimal GetDecimal(int ordinal)
double GetDouble(int ordinal)
float GetFloat(int ordinal)
```

컬럼 값을 지정한 타입으로 반환합니다.

#### Read

```cs
bool Read()
```

다음 레코드를 읽습니다. 결과가 더 이상 없으면 `false`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000이며 여기에서는 수정할 수 없습니다. |
| `FieldCount` | 결과 컬럼 수입니다. |
| `this[int ordinal]` | `GetValue(int ordinal)`과 동일합니다. |
| `this[string name]` | `GetValue(GetOrdinal(name))`과 동일합니다. |
| `HasRows` | 결과가 존재하는지 여부입니다. |
| `RecordsAffected` | Fetch된 레코드 수를 나타냅니다. |

### MachParameterCollection

```cs
public sealed class MachParameterCollection :
    DbParameterCollection,
    IEnumerable<MachParameter>
```

`MachCommand`에 바인딩할 파라미터 집합을 관리하는 클래스입니다.

파라미터를 설정한 뒤 실행하면 해당 값이 함께 전송됩니다.

> 현재 버전에는 Prepared Statement 의미에서의 실행 계획 캐시가 구현되어 있지 않으므로, 동일한 쿼리를 반복 실행하더라도 성능은 첫 실행과 동일합니다.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

파라미터 이름과 타입을 지정해 `MachParameter`를 추가하고, 생성된 객체를 반환합니다.

```cs
int Add(object value)
```

값을 추가하고 추가된 인덱스를 반환합니다.

```cs
void AddRange(Array values)
```

단순 값 배열을 한 번에 추가합니다.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

파라미터 이름과 값을 동시에 추가하고, 생성된 `MachParameter`를 반환합니다.

#### Contains

```cs
bool Contains(object value)
```

해당 값이 이미 추가되어 있는지 확인합니다.

```cs
bool Contains(string parameterName)
```

지정한 파라미터 이름이 존재하는지 확인합니다.

#### Clear

```cs
void Clear()
```

모든 파라미터를 제거합니다.

#### IndexOf

```cs
int IndexOf(object value)
```

해당 값이 있는 인덱스를 반환합니다.

```cs
int IndexOf(string parameterName)
```

파라미터 이름이 위치한 인덱스를 반환합니다.

#### Insert

```cs
void Insert(int index, object value)
```

지정한 위치에 값을 삽입합니다.

#### Remove

```cs
void Remove(object value)
```

해당 값을 포함한 파라미터를 제거합니다.

```cs
void RemoveAt(int index)
```

인덱스에 위치한 파라미터를 제거합니다.

```cs
void RemoveAt(string parameterName)
```

지정한 이름의 파라미터를 제거합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Count` | 파라미터 개수입니다. |
| `this[int index]` | 해당 인덱스의 `MachParameter`입니다. |
| `this[string name]` | 이름과 일치하는 `MachParameter`입니다. |

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

개별 파라미터의 바인딩 정보를 저장하는 클래스입니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `ParameterName` | 파라미터 이름입니다. |
| `Value` | 전송할 값입니다. |
| `Size` | 값의 길이입니다. |
| `Direction` | `ParameterDirection` 값입니다. 기본값은 `Input`입니다. |
| `DbType` | .NET 측 DB 타입입니다. |
| `MachDbType` | Machbase 고유 타입입니다. |
| `IsNullable` | `NULL` 허용 여부입니다. |
| `HasSetDbType` | `DbType`이 설정되었는지 여부입니다. |

### MachException

```cs
public class MachException : DbException
```

Machbase에서 발생한 오류를 표현하는 예외 클래스입니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `MachErrorCode` | Machbase가 반환한 오류 코드입니다. |

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

Append 프로토콜을 다루기 위한 보조 클래스입니다. `MachCommand.AppendOpen()` 호출 시 인스턴스를 획득합니다.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType callback)

void ErrorDelegateFuncType(MachAppendException e);
```

Append 중 오류가 발생했을 때 호출할 델리게이트를 등록합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `SuccessCount` | 성공적으로 저장된 레코드 수입니다. `AppendClose()` 이후에 확인할 수 있습니다. |
| `FailureCount` | 실패한 레코드 수입니다. `AppendClose()` 이후에 설정됩니다. |
| `Option` | `AppendOpen()` 호출 시 사용한 `MachAppendOption` 값입니다. |

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Append 과정에서 발생한 오류 정보를 추가로 제공하는 예외입니다. 서버가 반환한 오류 메시지를 그대로 전달하며, 실패한 레코드를 문자열로 확인할 수 있습니다.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

오류가 발생한 원본 레코드를 문자열 형태로 반환합니다.

## 사용 예시 {#usage-and-examples}

### 연결

`MachConnection`을 생성해 `Open()`/`Close()`로 연결을 제어할 수 있습니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

var connection = new MachConnection(connString);
connection.Open();
// ... 작업 ...
connection.Close();
```

`using` 문을 사용하면 `Close()`를 직접 호출하지 않아도 자원이 정리됩니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

using (var connection = new MachConnection(connString))
{
    connection.Open();
    // ... 작업 ...
}
```

### 쿼리 실행

`MachCommand`로 SQL 구문을 실행할 수 있습니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

using (var connection = new MachConnection(connString))
{
    connection.Open();

    const string sql = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    using var command = new MachCommand(sql, connection);
    command.ExecuteNonQuery();
}
```

### SELECT 실행

`MachCommand.ExecuteReader()`를 사용하면 `MachDataReader`로 결과를 순차적으로 읽을 수 있습니다.

```csharp
var connString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;",
    SERVER_HOST,
    SERVER_PORT);

using (var connection = new MachConnection(connString))
{
    connection.Open();

    using var command = new MachCommand("SELECT * FROM tab1", connection);
    using var reader = command.ExecuteReader();

    while (reader.Read())
    {
        for (var i = 0; i < reader.FieldCount; i++)
        {
            Console.WriteLine($"{reader.GetName(i)} : {reader.GetValue(i)}");
        }
    }
}
```

### 파라미터 바인딩

`MachParameterCollection`을 이용하면 시계열 조회 조건 등을 파라미터로 안전하게 전달할 수 있습니다.

```csharp
using var connection = new MachConnection(connString);
connection.Open();

const string sql = @"
    SELECT *
      FROM tab2
     WHERE CreatedDateTime < @CurrentTime
       AND CreatedDateTime >= @PastTime";

using var command = new MachCommand(sql, connection);

var now = DateTime.UtcNow;
var past = now.AddMinutes(-1);

command.ParameterCollection.Add(
    new MachParameter { ParameterName = "@CurrentTime", Value = now });
command.ParameterCollection.Add(
    new MachParameter { ParameterName = "@PastTime", Value = past });

using var reader = command.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetName(0)} : {reader.GetValue(0)}");
}
```

### Append

Append 프로토콜을 사용하면 대량의 시계열 데이터를 빠르게 적재할 수 있습니다.

```csharp
using var connection = new MachConnection(connString);
connection.Open();

using var appendCommand = new MachCommand(connection);
var writer = appendCommand.AppendOpen("tab2");

var row = new List<object>();
for (var i = 1; i <= 100000; i++)
{
    row.Add(i);
    row.Add($"NAME_{i % 100}");

    appendCommand.AppendData(writer, row);
    row.Clear();

    if (i % 1000 == 0)
    {
        appendCommand.AppendFlush(writer);
    }
}

appendCommand.AppendClose(writer);
Console.WriteLine($"Success Count : {writer.SuccessCount}");
Console.WriteLine($"Failure Count : {writer.FailureCount}");
```

### Error Delegator 설정

Append 중 서버에서 오류가 발생하면 지정한 델리게이트가 호출됩니다.

```csharp
void AppendErrorDelegator(MachAppendException e)
{
    Console.WriteLine("====================");
    Console.WriteLine("Append error");
    Console.WriteLine(e.Message);
    Console.WriteLine(e.GetRowBuffer());
    Console.WriteLine("====================");
}

// 등록
writer.SetErrorDelegator(AppendErrorDelegator);
```

### 자동 AppendFlush 설정

`MachConnection.SetConnectAppendFlush(true)`로 설정하면 Append 중 일정 주기로 자동 flush가 실행됩니다.

```csharp
var connection = new MachConnection(connString);
connection.Open();
connection.SetConnectAppendFlush(true);
```

`false`로 설정하면 자동 flush가 비활성화됩니다.

## 프로토콜 4.0-full 전체 API {#full-provider-apis-protocol-40-full}

`PROTOCOL=4.0-full`을 사용하면 Machbase 8.0.51 이상에서 확장된 ADO.NET 표면을 사용할 수 있습니다. 다음 어셈블리 중 하나를 로드해 기능을 활성화합니다.

- `UniMachNetConnector-net80-8.0.51.dll` – Machbase 8.0.51 이상에 포함된 기본 커넥터
- `machNetConnector-40-net80-3.2.0.dll` – 동일한 기능을 제공하는 독립 배포본

### 4.0-full에서 추가된 주요 타입

- `MachDbProviderFactory`: `Mach.Data` invariant 이름으로 프로바이더를 등록/생성할 수 있습니다.
- `MachConnectionStringBuilder`: 키워드 오타 없이 커넥션 문자열을 구성할 수 있습니다.
- `MachDataAdapter`, `MachRowUpdating`, `MachRowUpdated`: `DataTable`/`DataSet` 기반 워크플로를 지원합니다.
- `MachCommandBuilder`: SELECT 문으로부터 INSERT/DELETE(조건에 따라 UPDATE) 구문을 자동 생성합니다. 로그·태그 테이블은 UPDATE를 허용하지 않는다는 점에 유의하십시오.

### 전체 API 협상 확인

```csharp
var connString =
    "SERVER=127.0.0.1;PORT_NO=55656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

if (!connection.SupportsFullApi)
{
    throw new InvalidOperationException(
        "Full provider API negotiation failed.");
}
```

UPDATE/DELETE가 필요한 경우에는 Lookup/Volatile 테이블을 사용하고, 로그·태그 테이블은 Append 전용으로 유지하십시오.

### 커넥션 문자열 빌더 사용

```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 55656,
    UserID = "SYS",
    Password = "MANAGER"
};

builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### 예시: MachDataAdapter로 append

Lookup 테이블을 `DataTable`로 가져온 뒤 새 레코드를 추가하고 `MachDataAdapter`로 다시 반영할 수 있습니다.

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString =
    "SERVER=127.0.0.1;PORT_NO=55656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

var adapter = new MachDataAdapter(
    "SELECT id, name FROM dotnet_lookup_demo ORDER BY id",
    connection);
var builder = new MachCommandBuilder(adapter);

var table = new DataTable();
adapter.Fill(table);

var newRow = table.NewRow();
newRow["id"] = 2001;
newRow["name"] = "Inserted from MachDataAdapter";
table.Rows.Add(newRow);

adapter.Update(table);
```

> **Tip**: 전송 전 SQL을 확인하려면 `MachDataAdapter.MachRowUpdating` / `MachRowUpdated` 이벤트를 구독하십시오.

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine(
        $"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### 예시: DbProviderFactory 활용

`MachDbProviderFactory.Instance`를 사용하면 `DbProviderFactories`, Dapper 등 프로바이더 중립 구성에 Machbase를 연결할 수 있습니다.

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
connection.ConnectionString =
    "SERVER=127.0.0.1;PORT_NO=55656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM dotnet_lookup_demo";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Lookup rows: {count}");
```

설정 기반 애플리케이션에서 팩터리를 자동으로 노출하려면 시작 시 `MachDbProviderFactory.Register()`를 한 번 호출해 `DbProviderFactories.GetFactory("Mach.Data")`가 동일한 인스턴스를 반환하도록 구성하십시오.

`4.0-full` 프로토콜은 Machbase 7.x 이상 서버에서만 사용 가능합니다. 더 낮은 버전에서는 `PROTOCOL=4.0`(제한된 기능) 또는 2.x/3.x 프로토콜을 사용해야 합니다.
