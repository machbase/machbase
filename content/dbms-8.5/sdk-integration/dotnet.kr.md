---
title: '.NET Connector'
type: docs
weight: 20
---

## 목차

* [개요](#개요)
* [설치](#설치)
* [NuGet(통합 8.0.54)](#nuget으로-설치-통합-커넥터-8054)
* [NuGet(레거시 5.x)](#nuget으로-설치-레거시-5x)
* [커넥션 문자열 참고](#커넥션-문자열-참고)
* [API 레퍼런스](#api-레퍼런스)
* [사용 예시](#사용-예시)
* [프로토콜 4.0-full 전체 API](#프로토콜-40-full-전체-api)

## 개요

Machbase는 모든 지원 Machbase 와이어 프로토콜(2.1~4.0)을 포괄하는 범용 ADO.NET 프로바이더 **UniMachNetConnector**를 제공합니다. DBMS standard 소스의 현재 통합 패키지는 `UniMachNetConnector` 8.0.54이며 `net452`, `net5.0`, `net6.0`, `net7.0`, `net8.0` 타깃을 빌드합니다. 커넥터는 실행 시 커넥션 문자열을 참고해 올바른 프로토콜을 자동으로 협상하므로, 시계열 데이터 수집·질의 워크로드에도 별도 설정 없이 적합한 프로토콜을 선택합니다.

## 설치

설치된 Machbase 서버·클라이언트에는 `$MACHBASE_HOME/lib/` 경로에 범용 .NET 프로바이더가
함께 배포됩니다. 표준 Linux 설치에는 예를 들어 .NET 5.0 빌드인 `UniMachNetConnector-net50-8.0.54.dll`과
`machNetConnector-40-net50-3.2.1.dll` 같은 프로토콜별 어셈블리가 포함될 수 있습니다.
소스 프로젝트는 필요한 .NET SDK가 있을 때 추가 target-framework flavor도 빌드할 수 있습니다.

- **UniMachNetConnector**: 프레임워크에 구애받지 않는 진입점입니다. 소스 빌드 파일 이름은
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll` 형식이며, 배포 대상
  프레임워크에 맞는 파일을 선택합니다.
- **레거시 프로토콜 커넥터**: `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`과 같이
  프로토콜별로 나뉜 선택적 어셈블리입니다. UniMachNetConnector가 필요할 때 로드합니다.

응용 프로그램에서는 대상 프레임워크에 맞는 DLL을 참조하거나, 배포 시 실행 파일과 같은 위치에 함께 배치하면 됩니다.

## NuGet으로 설치 (통합 커넥터, 8.0.54)

통합 커넥터의 패키지 ID는 `UniMachNetConnector`입니다. DLL을 따로 배포하지 않고 프로젝트에서 패키지로 관리할 수 있으므로, 새 프로젝트에서는 DLL 복사 대신 NuGet 패키지 참조 방식을 권장합니다.

- 지원 TFM: net452, net5.0, net6.0, net7.0, net8.0
- net5.0 이상 빌드는 self-contained입니다. net452 빌드는 소스 프로젝트 기준
  `System.ValueTuple` 4.5.0을 restore합니다.

### 빠른 시작(명령줄)

```bash
# From your project folder
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

CI, 오프라인, 사내 피드처럼 패키지 소스(피드)를 명시적으로 제어해야 하면 참조만 먼저 추가하고, 별도로 복원하세요.

```bash
dotnet add package UniMachNetConnector --version 8.0.54 --no-restore

# Restore from nuget.org only (force fresh metadata)
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- 프로젝트 마우스 오른쪽 클릭 → NuGet 패키지 관리 → 찾아보기 → “UniMachNetConnector” 검색 → 8.0.54 선택 → 설치.

### 프로젝트 파일 예시

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
  <!-- no other Machbase packages required -->
  <!-- targets: net452|net5.0|net6.0|net7.0|net8.0 -->
  <!-- keep AnyCPU/x64 per your app; Machbase server side is unaffected -->
</ItemGroup>
```

### 로컬/사내 피드 사용(선택)

로컬 폴더 피드나 사내 레지스트리를 사용할 경우 다음과 같이 소스를 추가하고 복원합니다. 폴더 피드는 `UniMachNetConnector.8.0.54.nupkg`를 해당 디렉터리에 배치한 뒤 소스로 추가하면 됩니다.

```bash
# one-time setup
dotnet nuget add source /path/to/local-nuget -n mach-local

# restore using both nuget.org and the local feed
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

CI나 권한 제약이 있는 계정에서는 패키지 캐시 경로를 절대 경로로 지정하세요.

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> 팁: 8.0.54 게시 직후 `NU1102`(지정 버전을 찾지 못함)가 발생하거나 `dotnet add package`가 여전히 이전 버전을 보고하면 보통 인덱싱/캐시 문제입니다. `dotnet nuget locals http-cache --clear`로 HTTP 캐시를 지운 뒤 위와 같이 `--no-cache`로 복원하면 해결됩니다. 일시적으로 보이는 “incompatible with 'all' frameworks” 메시지는 실제 TFM 불일치가 아니라 복원 실패의 부작용인 경우가 많습니다. 패키지는 net452 및 net5.0~net8.0을 지원합니다.

### 최소 사용 예시

```csharp
using Mach.Data.MachClient;

var cs = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = (long)cmd.ExecuteScalar();
Console.WriteLine($"Tables: {count}");
```

## NuGet으로 설치 (레거시 5.x)

> **참고**: Machbase .NET Connector 5.0 패키지도 NuGet에 등록되어 있으며, 통합형 UniMachNetConnector가 도입되기 이전의 독립 배포본입니다.

Visual Studio를 사용하면 기존(통합 이전) .NET Connector도 NuGet에서 받을 수 있습니다. 아래 절차는 레거시 `machNetConnector5.0` 패키지를 설치하는 방법입니다. 통합 이전의 코드를 대상으로 해야 할 때만 사용하고, 새 프로젝트에는 통합형 `UniMachNetConnector` 8.0.54 사용을 권장합니다.

1. Visual Studio에서 새 C# .NET 프로젝트를 생성합니다.
2. 솔루션 탐색기에서 프로젝트 이름을 마우스 오른쪽 클릭하고 **NuGet 패키지 관리**를 선택합니다.
3. NuGet 패키지 관리자 창이 열리면 왼쪽 위의 **찾아보기** 탭을 선택하고 `machNet`을 검색합니다.
4. 검색 결과 목록에서 **machNetConnector5.0**을 선택하고 **설치**를 클릭합니다.
5. **변경 내용 미리 보기** 창이 나타나면 **확인**을 눌러 설치를 계속합니다.
6. 설치가 완료되면 솔루션 탐색기의 **종속성 → 패키지**에서 설치된 패키지를 확인할 수 있습니다.
7. `Program.cs`에 `using Mach.Data.MachClient;`를 추가하면 machNetConnector API를 사용할 수 있습니다.

> 어떤 NuGet을 써야 하나요?
> - 신규/업그레이드 앱: `UniMachNetConnector` 8.0.54 권장(net452 및 net5.0~net8.0 지원, 모든 프로토콜 및 4.0-full 포함).
> - 레거시 유지: 통합 패키지로 전환이 어려울 때만 `machNetConnector5.0`을 사용하세요.

## 커넥션 문자열 참고

커넥션 문자열의 각 항목은 세미콜론(`;`)으로 구분합니다. 표의 한 행에 표시된 키워드는 서로 동일한 의미를 갖습니다.

| 키워드                                                         | 설명                                                                                                  | 예시                                             | 기본값  |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST`                                        | 호스트명 또는 IP 주소                                                                                 | `SERVER=127.0.0.1`                               | 없음    |
| `PORT`, `PORT_NO`                                              | 수신 포트                                                                                             | `PORT=5656`                                     | `5656`  |
| `USERID`, `USERNAME`, `USER`, `UID`                            | 사용자 이름                                                                                            | `UID=SYS`                                        | `SYS`   |
| `PASSWORD`, `PWD`                                              | 비밀번호                                                                                               | `PWD=manager`                                    | 없음    |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout`       | 커넥션 타임아웃(밀리초)                                                                                | `CONNECT_TIMEOUT=10000`                          | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout`          | 명령별 타임아웃(밀리초)                                                                               | `COMMAND_TIMEOUT=50000`                          | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol`                  | 선호하는 와이어 프로토콜 (`2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full` 등). 입력하지 않으면 UniMachNetConnector는 `4.0`을 사용합니다. | `PROTOCOL=auto`                                  | `4.0`   |

예시:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### 프로토콜 자동 감지 (`PROTOCOL=auto`)

서버 버전이 혼재된 환경이라면 `PROTOCOL=auto`를 지정해 UniMachNetConnector가 실행 시 적절한 레거시 프로토콜을 협상하도록 설정할 수 있습니다. 동작 방식은 다음과 같습니다.

- `PROTOCOL=auto`는 4.0 → 3.0 → 2.2 → 2.1 순서로 핸드셰이크를 시도하며, 커넥션 문자열에 전달한 호스트·포트·사용자·비밀번호·데이터베이스·`CONNECT_TIMEOUT` 값을 그대로 사용합니다.
- `PROTOCOL=auto-full`은 위와 같지만 서버가 4.0을 리턴하면 먼저 `4.0-full` 디스크립터를 시도하고, 필요 시 제한 버전(4.0)으로 폴백합니다.
- `SERVER=hostA:5700,hostB:6000`처럼 여러 호스트를 지정하면 순차적으로 시도하며, 실패 메시지에는 각 호스트/프로토콜 조합이 기록되어 문제 지점을 파악할 수 있습니다.
- 자격 증명은 기존 레거시 네이티브 드라이버와 동일하게 대문자로 변환되므로, 기존 SYS/MANAGER 테스트 환경을 그대로 사용할 수 있습니다. 기본 데이터베이스(`data`)를 사용하지 않는다면 `DATABASE=` 값을 명시하세요.
- `CONNECT_TIMEOUT` 값은 각 감지 라운드 트립에 적용됩니다. 예외 메시지에 `Protocol probe received an invalid response (missing result)`가 보이면 핸드셰이크가 완료되지 않은 것이므로 포트·방화벽·TLS/SSL 설정을 다시 확인하십시오.

이미 서버 버전을 알고 있다면 `PROTOCOL=2.1`, `3.0`, `4.0`, `4.0-full`처럼 명시적으로 지정해 자동 감지를 건너뛸 수도 있습니다.

## API 레퍼런스

{{< callout type="warning" >}}
아래에 명시되지 않은 기능은 아직 구현되지 않았거나 정상적으로 동작하지 않을 수 있습니다.<br>
존재하지 않는 메서드나 필드를 호출하면 `NotImplementedException` 또는 `NotSupportedException`이 발생합니다.
{{< /callout >}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

Machbase와의 연결을 담당하는 클래스입니다.

`DbConnection`과 마찬가지로 `IDisposable`을 구현하므로 `Dispose()` 호출이나 `using` 문으로 해제할 수 있습니다.

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
| `StatusString` | 현재 연결이 의존하는 `MachCommand`의 상태 문자열입니다.<br>내부에서 오류 메시지를 구성하는 데 사용하며, 작업이 시작된 시점의 상태를 나타내므로 쿼리 상태를 판단하는 용도로 사용하지 않는 것이 좋습니다. |

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

`MachConnection`을 통해 **SQL 명령이나 Append 작업**을 실행하는 클래스입니다.

`DbCommand`와 마찬가지로 `IDisposable`을 구현하므로 `Dispose()` 호출이나 `using` 문으로 해제할 수 있습니다.

#### 생성자

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

실행할 쿼리와 사용할 `MachConnection` 객체를 지정해 인스턴스를 생성합니다.

```cs
MachCommand(MachConnection aConn)
```

사용할 `MachConnection` 객체만 지정해 인스턴스를 생성합니다. Append처럼 실행할 쿼리가 없을 때 사용합니다.

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

* `aTableName`: 대상 테이블 이름입니다.
* `aErrorCheckCount`: AppendData로 입력한 레코드의 누적 개수가 이 값에 도달할 때마다 서버에 전송해 실패 여부를 확인합니다. 즉, 자동 `APPEND-FLUSH` 지점을 설정합니다.
* `option`: 다음 `MachAppendOption` 값 중 하나를 지정합니다.
    * `MachAppendOption.None`: 옵션을 지정하지 않습니다.
    * `MachAppendOption.MicroSecTruncated`: `DateTime` 값을 마이크로초까지만 입력합니다. (`DateTime` 객체의 Ticks 값은 100나노초 단위로 표현됩니다.)

#### AppendData

```cs
void AppendData(MachAppendWriter aWriter, List<object> aDataList)
```

`MachAppendWriter` 객체를 통해, 데이터를 담은 리스트를 받아 데이터베이스에 입력합니다.

- 리스트에 있는 값은 순서대로 Append 버퍼에 적재되며, 각 값의 타입은 해당 테이블 컬럼의 타입과 일치해야 합니다.
- 값이 부족하거나 초과하면 예외가 발생합니다.

> **참고**: `_arrival_time`을 `ulong`으로 직접 지정할 때는 Machbase가 기대하는 1970-01-01 UTC 기준 나노초 값을 입력해야 합니다. `DateTime` 객체의 Tick 값을 그대로 넣으면 안 됩니다. `DateTime.Ticks`는 100나노초 단위이므로, UTC Ticks에서 기준 시각(1970-01-01)의 Ticks를 뺀 뒤 100을 곱합니다.

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)
```

`AppendData()`와 같지만, `_arrival_time`을 `DateTime`으로 명시적으로 지정합니다.

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong)
```

`AppendData()`와 같지만, `_arrival_time`을 나노초 단위 `ulong`으로 명시적으로 지정합니다. `ulong` 값을 `_arrival_time`으로 입력할 때 주의할 점은 위의 `AppendData()`를 참고하세요.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter aWriter)
```

`AppendData()`로 입력한 데이터를 즉시 서버로 전송해 입력을 반영합니다.<br>
호출 주기가 짧을수록 장애 시 데이터 유실이 줄어들고 오류를 빨리 확인할 수 있지만, 처리 성능은 낮아집니다.<br>
호출 주기가 길수록 데이터 유실 가능성이 커지고 오류 확인이 늦어지지만, 처리 성능은 크게 높아집니다.

#### AppendClose

```cs
void AppendClose(MachAppendWriter aWriter)
```

Append 세션을 종료합니다. 내부적으로 `AppendFlush()` 호출 후 프로토콜을 마무리합니다.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

쿼리를 실행하고 영향을 받은 레코드 수를 반환합니다. 주로 `INSERT`, `UPDATE`, `DELETE`, DDL 등 SELECT 이외의 쿼리에서 사용합니다.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

쿼리를 실행하고 결과 대상 목록의 첫 번째 값을 `object`로 반환합니다. 주로 결과가 하나뿐인 SELECT 쿼리(Scalar Query)의 결과를 `DbDataReader` 없이 얻을 때 사용합니다.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)
```

쿼리를 실행하고 결과를 순차적으로 읽을 수 있는 `DbDataReader`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Connection` / `DbConnection` | 현재 연결된 `MachConnection`입니다. |
| `ParameterCollection` / `DbParameterCollection` | 바인딩에 사용할 `MachParameterCollection`입니다. |
| `CommandText` | 실행할 SQL 문자열입니다. |
| `CommandTimeout` | 서버 응답을 기다리는 최대 시간(밀리초)입니다.<br>값은 `MachConnection` 설정을 따르며 여기서는 조회만 가능합니다. |
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000입니다. |
| `IsAppendOpened` | Append 세션이 열려 있는지 여부입니다. |

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

Fetch된 결과를 순차적으로 읽는 클래스입니다. 직접 생성할 수 없으며, `MachCommand.ExecuteDbDataReader()`로 획득한 객체만 사용할 수 있습니다.

#### GetName

```cs
string GetName(int ordinal)
```

지정한 인덱스의 컬럼 이름을 반환합니다.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

지정한 인덱스 컬럼의 Machbase 데이터 타입 이름을 반환합니다.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

지정한 인덱스 컬럼에 매핑된 .NET 타입을 반환합니다.

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

컬럼 이름에 해당하는 인덱스를 반환합니다.

#### GetValue

```cs
object GetValue(int ordinal)
```

현재 레코드에서 지정한 인덱스의 값을 `object`로 반환합니다.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

현재 레코드에서 지정한 인덱스의 값이 `NULL`인지 확인합니다.

#### GetValues

```cs
int GetValues(object[] values)
```

현재 레코드의 값을 배열에 채워 넣고 채워진 항목 수를 반환합니다.

#### Get*xxxx*

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

지정한 인덱스의 컬럼 값을 해당 데이터 타입으로 반환합니다.

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
| `RecordsAffected` | `MachCommand`와 달리, 여기서는 Fetch된 레코드 수를 나타냅니다. |

### MachParameterCollection

```cs
public sealed class MachParameterCollection : DbParameterCollection, IEnumerable<MachParameter>
```

`MachCommand`에 바인딩할 파라미터 집합을 관리하는 클래스입니다.

파라미터를 바인딩한 뒤 실행하면 해당 값이 함께 전송됩니다.

> 현재 버전에는 Prepared Statement의 실행 계획 캐시가 구현되어 있지 않으므로, 바인딩 후 동일한 쿼리를 반복 실행해도 성능은 첫 실행과 동일합니다.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

파라미터 이름과 타입을 지정해 `MachParameter`를 추가하고, 추가된 객체를 반환합니다.

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

파라미터 이름과 값을 함께 추가하고, 추가된 `MachParameter`를 반환합니다.

#### Contains

```cs
bool Contains(object value)
```

해당 값이 이미 추가되어 있는지 확인합니다.

```cs
bool Contains(string value)
```

지정한 이름의 파라미터가 존재하는지 확인합니다.

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

`MachCommand`에 바인딩할 개별 파라미터의 정보를 저장하는 클래스입니다.

별도로 지원하는 메서드는 없습니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `ParameterName` | 파라미터 이름입니다. |
| `Value` | 전송할 값입니다. |
| `Size` | 값의 길이입니다. |
| `Direction` | `ParameterDirection` 값(Input / Output / InputOutput / ReturnValue)입니다.<br>기본값은 `Input`입니다. |
| `DbType` | .NET 측 DB 타입입니다. |
| `MachDbType` | Machbase 고유 타입입니다.<br>`DbType`과 다를 수 있습니다. |
| `IsNullable` | `NULL` 허용 여부입니다. |
| `HasSetDbType` | `DbType`이 설정되었는지 여부입니다. |

### MachException

```cs
public class MachException : DbException
```

Machbase에서 발생한 오류를 표현하는 예외 클래스입니다.

오류 메시지가 설정되며, 모든 오류 메시지는 `MachErrorMsg`에서 확인할 수 있습니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `int MachErrorCode` | Machbase가 반환한 오류 코드입니다. |

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

`MachCommand`와 함께 Append를 별도로 지원하는 보조 클래스입니다.
ADO.NET 표준이 아니라 Machbase Append 프로토콜을 지원하기 위한 클래스입니다.

별도의 생성자 없이 `MachCommand.AppendOpen()`을 호출해 인스턴스를 획득합니다.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType aFunc)

void ErrorDelegateFuncType(MachAppendException e);
```

Append 중 오류가 발생했을 때 호출할 `ErrorDelegateFunc`를 등록합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `SuccessCount` | 성공적으로 저장된 레코드 수입니다. `AppendClose()` 이후에 설정됩니다. |
| `FailureCount` | 입력에 실패한 레코드 수입니다. `AppendClose()` 이후에 설정됩니다. |
| `Option` | `AppendOpen()` 호출 시 사용한 `MachAppendOption` 값입니다. |

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

다음 사항을 제외하면 `MachException`과 같습니다.

* 서버가 반환한 오류 메시지를 그대로 전달합니다.
* 오류가 발생한 레코드의 데이터 버퍼(쉼표로 구분)를 얻을 수 있어, 이를 가공해 다시 Append하거나 기록할 수 있습니다.

이 예외는 `ErrorDelegateFunc` 안에서만 사용할 수 있습니다.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

오류가 발생한 레코드의 데이터 버퍼를 문자열 형태로 반환합니다.

## 사용 예시

### 연결

`MachConnection`을 생성해 `Open()`/`Close()`로 연결을 제어할 수 있습니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//... do something
sConn.Close();
```

`using` 문을 사용하면 `Close()`를 직접 호출하지 않아도 자원이 정리됩니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //... do something
} // you don't need to call sConn.Close();
```

### 쿼리 실행

`MachCommand`를 생성해 SQL 구문을 실행할 수 있습니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    MachCommand sCommand = new MachCommand(sQueryString , sConn);
    try
    {
        sCommand.ExecuteNonQuery();
    }
    catch (MachException me)
    {
        throw me;
    }
}
```

`using` 문을 사용하면 `MachCommand`도 바로 해제할 수 있습니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    using(MachCommand sCommand = new MachCommand(sQueryString , sConn))
    {
        try
        {
            sCommand.ExecuteNonQuery();
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### SELECT 실행

SELECT 쿼리를 담은 `MachCommand`를 `ExecuteReader()`로 실행하면 `MachDataReader`를 얻을 수 있습니다.

`MachDataReader`로 레코드를 하나씩 순차적으로 읽을 수 있습니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    String sQueryString = "SELECT * FROM tab1;";
    using(MachCommand sCommand = new MachCommand(sQueryString , sConn))
    {
        try
        {
            MachDataReader sDataReader = sCommand.ExecuteReader();
            while (sDataReader.Read())
            {
                for (int i = 0; i < sDataReader.FieldCount; i++)
                {
                    Console.WriteLine(String.Format("{0} : {1}",
                                                    sDataReader.GetName(i),
                                                    sDataReader.GetValue(i)));
                }
            }
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### 파라미터 바인딩

`MachCommand`의 `MachParameterCollection`에 파라미터를 채워 연결할 수 있습니다. 이를 이용하면 시계열 조회 조건 등을 파라미터로 안전하게 전달할 수 있습니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    string sSelectQuery = @"SELECT *
        FROM tab2
        WHERE CreatedDateTime < @CurrentTime
        AND CreatedDateTime >= @PastTime";

    using (MachCommand sCommand = new MachCommand(sSelectQuery, sConn))
    {
        DateTime sCurrtime = DateTime.Now;
        DateTime sPastTime = sCurrtime.AddMinutes(-1);

        try
        {
            sCommand.ParameterCollection.Add(new MachParameter { ParameterName = "@CurrentTime", Value = sCurrtime });
            sCommand.ParameterCollection.Add(new MachParameter { ParameterName = "@PastTime", Value = sPastTime });

            MachDataReader sDataReader = sCommand.ExecuteReader();

            while (sDataReader.Read())
            {
                for (int i = 0; i < sDataReader.FieldCount; i++)
                {
                    Console.WriteLine(String.Format("{0} : {1}",
                                                    sDataReader.GetName(i),
                                                    sDataReader.GetValue(i)));
                }
            }
        }
        catch (MachException me)
        {
            throw me;
        }
    }
}
```

### Append

Append 프로토콜을 사용하면 대량의 시계열 데이터를 빠르게 적재할 수 있습니다.

`MachCommand`에서 `AppendOpen()`을 실행하면 `MachAppendWriter` 객체를 얻습니다.

이 객체와 `MachCommand`를 사용해 입력 레코드 하나를 담은 리스트를 `AppendData()`에 전달합니다.
`AppendFlush()`는 입력된 모든 레코드를 반영하고, `AppendClose()`는 전체 Append 과정을 종료합니다.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();

    using (MachCommand sAppendCommand = new MachCommand(sConn))
    {
        MachAppendWriter sWriter = sAppendCommand.AppendOpen("tab2");
        sWriter.SetErrorDelegator(AppendErrorDelegator);

        var sList = new List<object>();
        for (int i = 1; i <= 100000; i++)
        {
            sList.Add(i);
            sList.Add(String.Format("NAME_{0}", i % 100));

            sAppendCommand.AppendData(sWriter, sList);

            sList.Clear();

            if (i % 1000 == 0)
            {
                sAppendCommand.AppendFlush(sWriter);
            }
        }

        sAppendCommand.AppendClose(sWriter);
        Console.WriteLine(String.Format("Success Count : {0}", sWriter.SuccessCount));
        Console.WriteLine(String.Format("Failure Count : {0}", sWriter.FailureCount));
    }
}
```

```c#
private static void AppendErrorDelegator(MachAppendException e)
{
    Console.WriteLine("{0}", e.Message);
    Console.WriteLine("{0}", e.GetRowBuffer());
}
```

### Error Delegator 설정

`MachAppendWriter`에는 Append 중 Machbase 서버 측에서 발생한 오류를 감지할 함수를 지정할 수 있습니다. Append 중 서버에서 오류가 발생하면 지정한 델리게이트가 호출됩니다.

.NET에서는 이 함수를 델리게이트 함수로 지정합니다.

```c#
public static void ErrorCallbackFunc(MachAppendException e)
{
    Console.WriteLine("====================");
    Console.WriteLine("Error occured");
    Console.WriteLine(e.Message);
    Console.WriteLine(e.StackTrace);
    Console.WriteLine("====================");
}

public static void DoAppend()
{
    MachCommand com = new MachCommand(conn);
    MachAppendWriter writer = com.AppendOpen("tag", errorCheckCount);
    writer.SetErrorDelegator(ErrorCallbackFunc);
    //... do append
}
```

### 자동 AppendFlush 설정

커넥션에서 `SetConnectAppendFlush(true)`를 호출하면 Append 중 일정 주기로 자동 flush가 실행됩니다.

```cs
private static string connString = $"SERVER={HOST};PORT_NO={port};USER={USER};PWD={PWD}";

public static void Main(string[] args)
{
    MachConnection conn = new MachConnection(connString);
    conn.Open();
    conn.SetConnectAppendFlush(true);
}
```

`false`로 설정하면 자동 flush가 비활성화됩니다.

```cs
conn.SetConnectAppendFlush(false);
```

## 프로토콜 4.0-full 전체 API

`PROTOCOL=4.0-full`을 사용하면 확장된 ADO.NET 표면을 사용할 수 있습니다. 8.0.54 소스
패키지에서 4.0 limited connector는 3.1.2, 4.0-full connector는 3.2.1입니다.
설치된 Linux 패키지는 `$MACHBASE_HOME/lib/` 아래에 net50 flavor만 포함할 수 있으므로,
다른 target framework가 필요하면 소스 빌드 또는 NuGet restore 산출물을 사용하십시오.

- `UniMachNetConnector-net50-8.0.54.dll` – DBMS Standard Linux 패키지에서 흔히 설치되는 universal entry point
- `machNetConnector-40-net50-3.1.2.dll` – protocol 4.0 limited connector
- `machNetConnector-40-net50-3.2.1.dll` – protocol 4.0-full connector

### 4.0-full에서 추가된 주요 타입

- `MachDbProviderFactory`: `Instance`, `Register()`, 표준 `Create*` 메서드를 제공하므로, 프레임워크가 `Mach.Data` invariant 이름으로 프로바이더를 찾아 생성할 수 있습니다.
- `MachConnectionStringBuilder`: 키워드를 모두 외우지 않아도 오타 없이 커넥션 문자열을 구성할 수 있습니다.
- `MachDataAdapter`, `MachRowUpdating`, `MachRowUpdated`: `DataTable`/`DataSet` 기반 워크플로를 지원합니다.
- `MachCommandBuilder`: SELECT 문으로부터 INSERT/DELETE(조건에 따라 UPDATE) 구문을 자동 생성합니다. 로그·태그 테이블은 UPDATE를 허용하지 않는다는 점에 유의하십시오.

### 전체 API 활성화

```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

UPDATE/DELETE가 필요한 경우에는 Lookup/Volatile 테이블을 사용하고, 로그·태그 테이블은 UPDATE를 허용하지 않으므로 Append 전용으로 유지하십시오.

### 커넥션 문자열 빌더 사용

```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = "MANAGER"
};

// Protocol stays a string key so older connectors understand the value.
builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### 예시: MachDataAdapter로 append

Lookup 테이블을 `DataTable`로 가져온 뒤 새 레코드를 추가하고 `MachDataAdapter`로 다시 반영할 수 있습니다. INSERT 구문은 `MachCommandBuilder`가 자동으로 생성합니다. (테이블이 아직 없다면 먼저 한 번 생성하십시오: `CREATE LOOKUP TABLE dotnet_lookup_demo(id LONG PRIMARY KEY, name VARCHAR(64));`)

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
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

> **Tip**: 전송 전에 SQL을 확인하거나 실행을 거부하려면 `MachDataAdapter.MachRowUpdating` / `MachRowUpdated` 이벤트를 구독하십시오.

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine($"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### 예시: DbProviderFactory 활용

`MachDbProviderFactory.Instance`를 사용하면 `DbProviderFactories`, Dapper, 자체 DI 컨테이너 등 프로바이더 중립 구성에 Machbase를 연결할 수 있습니다.

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
connection.ConnectionString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM dotnet_lookup_demo";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Lookup rows: {count}");
```

설정 기반 애플리케이션에서 팩터리를 자동으로 노출하려면 시작 시 `MachDbProviderFactory.Register()`를 한 번 호출해 `DbProviderFactories.GetFactory("Mach.Data")`가 동일한 인스턴스를 반환하도록 구성하십시오.

`4.0-full` 프로토콜은 Machbase 7.x 이상 서버에서만 사용 가능합니다. 더 낮은 버전에서는 `PROTOCOL=4.0`(제한된 기능) 또는 2.x/3.x 프로토콜을 사용해야 합니다.
