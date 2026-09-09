---
type: docs
title: '11.8 .NET Connector'
weight: 80
toc: true
aliases:
  - /dbms/reference/sdk-api/net-connector/
---

## Contents {#index}

* [Overview](#overview)
* [Installation](#install)
* [NuGet (Unified 8.0.55)](#nuget-unified-connector)
* [Connection String Reference](#connection-string-reference)
* [API Reference](#api-reference)
* [Usage and Examples](#usage-and-examples)
* [Protocol 4.0-full APIs](#full-provider-apis-protocol-40-full)

## Overview {#overview}

Machbase provides **UniMachNetConnector**, a universal ADO.NET provider supporting wire
protocols 2.1–4.0. The current unified package is `UniMachNetConnector` 8.0.55, with
`net452`, `net5.0`, `net6.0`, `net7.0`, and `net8.0` builds. Automatic negotiation runs
only when the connection string specifies `PROTOCOL=auto` or `auto-full`.

## Installation {#install}

Machbase server/client installations distribute the universal .NET provider under
`$MACHBASE_HOME/lib/`. A standard Linux package may include protocol-specific assemblies
such as `UniMachNetConnector-net50-8.0.55.dll` and
`machNetConnector-40-net50-3.2.2.dll`. The source project can build additional target
framework variants when the required .NET SDK is available.

- **UniMachNetConnector:** Framework-independent entry point. Source builds use
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll`; choose the file matching the
  deployment framework.
- **Legacy protocol connectors:** Protocol-specific assemblies such as
  `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`, loaded by UniMachNetConnector as needed.

Reference the DLL matching the application target framework, or deploy it beside the executable.

## Multiple Databases

MachConnector 4.0 can select the initial database with `DATABASE` or `DB_NAME` in the connection string.

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_A;PWD=secret;DATABASE=FACTORY_A
```

The standard `Database` property and `ChangeDatabase()` are not guaranteed current
catalog switching APIs; use SQL `USE` and `CURRENT_DATABASE()`. Do not assume automatic
catalog reset on return to a connection pool. See the
[Multi-Database Operations Guide](/dbms/operations-configuration-recovery/multi-database/#97-net)
for limitations.

## Install with NuGet (Unified Connector, 8.0.55) {#nuget-unified-connector}

The unified connector package ID is `UniMachNetConnector`. Prefer a NuGet package
reference over copying DLLs for new projects.

- Supported TFMs: net452, net5.0, net6.0, net7.0, net8.0
- net5.0 and later builds are self-contained. The net452 source build restores
  `System.ValueTuple` 4.5.0.

### Command-Line Quick Start

```bash
# Run in the project directory
dotnet add package UniMachNetConnector --version 8.0.55
dotnet build
```

To control the source feed explicitly, add the reference first and restore separately.

```bash
dotnet add package UniMachNetConnector --version 8.0.55 --no-restore

# Force a refresh of nuget.org metadata
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- Right-click the project → Manage NuGet Packages → Browse → search for
  “UniMachNetConnector” → select 8.0.55 → Install.

### Project File Example

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.55" />
  <!-- No additional Machbase packages required -->
  <!-- Target frameworks: net452|net5.0|net6.0|net7.0|net8.0 -->
</ItemGroup>
```

### Use a Local or Internal Feed (Optional)

For an internal registry or folder feed, add the source and restore as follows. For a
folder feed, place `UniMachNetConnector.8.0.55.nupkg` in that directory.

```bash
# One-time setup
dotnet nuget add source /path/to/local-nuget -n mach-local

# Restore using both the local feed and nuget.org
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

In environments with restricted permissions, set an absolute package cache path.

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> Tip: Immediately after publication, NU1102 (version not found) or “incompatible with
> 'all' frameworks” usually indicates indexing or cache issues. Run
> `dotnet nuget locals http-cache --clear`, then restore with `--no-cache`. The package
> supports net452 and net5.0–net8.0.

### Minimal Example

```csharp
using System;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var cs = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = Convert.ToInt64(cmd.ExecuteScalar());
Console.WriteLine($"Tables: {count}");
```

## Connection String Reference {#connection-string-reference}

Separate entries with semicolons (`;`). Keywords listed in the same table row are equivalent.

| Keywords | Description | Example | Default |
|---|---|---|---|
| `DSN`, `SERVER`, `HOST` | Host name or IP address | `SERVER=127.0.0.1` | None |
| `PORT`, `PORT_NO` | Listener port | `PORT=5656` | `5656` |
| `USERID`, `USERNAME`, `USER`, `UID` | User name | `UID=SYS` | `SYS` |
| `PASSWORD`, `PWD` | Password | `PWD=manager` | None |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout` | Connection timeout (ms) | `CONNECT_TIMEOUT=10000` | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout` | Per-command timeout (ms) | `COMMAND_TIMEOUT=50000` | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol` | Preferred wire protocol (`2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full`, etc.); omitted values use `4.0` | `PROTOCOL=auto` | `4.0` |

Example:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### Automatic Protocol Detection (`PROTOCOL=auto`)

With mixed server versions, set `PROTOCOL=auto` to let UniMachNetConnector negotiate
a suitable legacy protocol at runtime:

- `PROTOCOL=auto` attempts handshakes in order: 4.0 → 3.0 → 2.2 → 2.1. It uses the host,
  port, user, password, database, and `CONNECT_TIMEOUT` from the connection string.
- `PROTOCOL=auto-full` selects the registered `4.0-full` descriptor when the server
  major version is 4. Only builds without that descriptor select limited 4.0. A failed
  full connection does not automatically retry with limited.
- Multiple hosts, such as `SERVER=hostA:5700,hostB:6000`, are tried sequentially. Failure
  messages include each host/protocol combination to aid diagnosis.
- Credentials are uppercased as in legacy drivers. Specify `DATABASE=` when not using
  the default database (`data`).
- `CONNECT_TIMEOUT` applies to each detection round trip. If the exception says
  `Protocol probe received an invalid response`, check the port, firewall, and TLS configuration.

If the server version is known, specify `PROTOCOL=2.1`, `3.0`, `4.0`, or `4.0-full`
to skip automatic detection.

## API Reference {#api-reference}

{{< callout type="warning" >}}
Features not listed below may be unimplemented or may not work correctly.<br>
Even declared APIs may throw `NotImplementedException` or `NotSupportedException` for
unimplemented or unsupported features. Check that the installed provider supports the
APIs you require.
{{< /callout >}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

Manages Machbase connections. Like `DbConnection`, it implements `IDisposable`;
release it safely with `Dispose()` or a `using` statement.

#### Constructor

```
MachConnection(string aConnectionString)
```

Creates a `MachConnection` from a connection string.

#### Open

```cs
void Open()
```

Establishes the connection using the connection string.

#### Close

```cs
void Close()
```

Closes the open connection.

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Sets whether Append flushes automatically.

#### Fields

| Name | Description |
|--|--|
| `State` | `System.Data.ConnectionState` value |
| `StatusString` | State string of the `MachCommand` used by this connection; intended for internal logging, not query status checks |

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

Executes SQL or Append operations through a `MachConnection`. Like `DbCommand`,
it implements `IDisposable`.

#### Constructors

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

Creates an instance with the SQL to execute and a connection.

```cs
MachCommand(MachConnection aConn)
```

Creates an Append-only command without a query.

#### CreateParameter

```cs
MachParameter CreateParameter()
```

Creates a new `MachParameter`.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

Opens an Append session and returns a `MachAppendWriter`.

* `aTableName`: Target table name
* `aErrorCheckCount`: Sends data and checks failures after the specified record count;
  sets an automatic `APPEND-FLUSH` point.
* `option`: `None` or `MicroSecTruncated`.

#### AppendData

```cs
void AppendData(MachAppendWriter writer, List<object> dataList)
```

Loads list values into the Append buffer in order. Types must match the table columns;
too few or too many values raise an exception.

> **Note:** When specifying `_arrival_time` as `ulong`, use nanoseconds since
> 1970-01-01 UTC, as required by Machbase.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    DateTime arrivalTime)
```

Specifies `_arrival_time` explicitly as `DateTime`.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    ulong arrivalTime)
```

Specifies `_arrival_time` as `ulong` nanoseconds.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter writer)
```

Sends buffered data to the server. More frequent calls reduce client-buffered data and
transmission delay but may increase communication overhead. A successful call alone
does not establish disk durability; also check server processing results and the
target table durability policy.

#### AppendClose

```cs
void AppendClose(MachAppendWriter writer)
```

Closes the Append session. Internally calls `AppendFlush()` before completing the protocol.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

Executes a query and returns the affected-record count. Mainly used for `INSERT`,
`UPDATE`, `DELETE`, and DDL.

#### RowId

```cs
UInt64? RowId
```

After a successful single `INSERT ... VALUES` in Standard Edition, retrieve the
inserted row's ROWID after `ExecuteNonQuery()` in MachConnector 4.0/4.0-full and Universal .NET.

```cs
using (var command = new MachCommand(
    "INSERT INTO orders(item) VALUES('pump')", connection))
{
    command.ExecuteNonQuery();
    ulong? rowId = command.RowId;
}
```

Returns `null` if no ROWID is available. Read the 64-bit `RowId`, not the legacy
32-bit `LastInsertedId`. See [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/)
for differences in batches and Append.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

Executes a query and returns the first column value.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior behavior)
```

Executes a query and returns a `DbDataReader` for sequential result access.

#### Fields

| Name | Description |
|--|--|
| `Connection` / `DbConnection` | Current `MachConnection` |
| `ParameterCollection` / `DbParameterCollection` | Parameter collection for binding |
| `CommandText` | SQL string to execute |
| `CommandTimeout` | Maximum server response wait (ms); inherited from `MachConnection` and read-only here |
| `FetchSize` | Records fetched per server request; default 3000 |
| `IsAppendOpened` | Whether an Append session is open |
| `RowId` | 64-bit ROWID of a successful single INSERT; `null` when absent |

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

Reads fetched results sequentially. Use only objects obtained from
`MachCommand.ExecuteDbDataReader()`.

#### GetName

```cs
string GetName(int ordinal)
```

Returns the column name at the specified index.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Returns the Machbase column type name.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

Returns the mapped .NET type.

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

Returns the index for a column name.

#### GetValue

```cs
object GetValue(int ordinal)
```

Returns the current record value as `object`.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

Checks whether the column value is `NULL`.

#### GetValues

```cs
int GetValues(object[] values)
```

Fills an array with current record values and returns the number of entries written.

#### GetSchemaTable

```cs
DataTable GetSchemaTable()
```

Returns schema metadata for SELECT result columns. Check `AllowDBNull` for nullability.
This behavior applies to both MachConnector40 and MachConnector40-full-API.

```csharp
using var reader = command.ExecuteReader();
DataTable schema = reader.GetSchemaTable();

foreach (DataRow row in schema.Rows)
{
    string columnName = Convert.ToString(row["ColumnName"]);
    object allowDBNull = row["AllowDBNull"];

    if (allowDBNull is bool value && !value)
    {
        Console.WriteLine($"{columnName}: NO_NULLS");
    }
    else
    {
        // true or DBNull.Value: NULL handling required
        Console.WriteLine($"{columnName}: NULL handling required");
    }
}
```

| `AllowDBNull` | Meaning |
|---------------|------|
| `false` | Cannot be NULL |
| `true` | Can be NULL |
| `DBNull.Value` | Unknown |

`DBNull.Value` does not mean `NOT NULL`; handle it as potentially nullable. See
[Nullable Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)
for SQL result rules.

In Machbase SQL, `''` is SQL `NULL`: `AllowDBNull` in `GetSchemaTable()` is `true`,
and `IsDBNull()` is `true` for the row. The literal `''''` is one single quote character,
a non-NULL string result with `AllowDBNull=false`.

`GetSchemaTable()` provides `ColumnName`, `ColumnOrdinal`, `ColumnSize`,
`NumericPrecision`, `NumericScale`, `DataType`, `ProviderType`, `IsLong`, `AllowDBNull`,
and `IsKey`. `IsKey=true` identifies a direct SELECT result column that is a PRIMARY
KEY. Expressions and aggregates report `false`.

Older servers or SDKs may return `false` for `IsKey`.

Nullable metadata does not change DECIMAL precision `1–65`, scale `0–30`, or actual
values. .NET returns DECIMAL as `System.Decimal` when precision is at most 29 and scale
is at most 28. Values beyond that range return `System.String` to prevent precision
loss. In that case, `GetSchemaTable().DataType`, `GetFieldType()`, and the actual row
value CLR type are all `System.String`.

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

Returns the column value as the specified type.

#### Read

```cs
bool Read()
```

Reads the next record. Returns `false` when there are no more results.

#### Fields

| Name | Description |
|--|--|
| `FetchSize` | Records fetched per request; default 3000 and read-only here |
| `FieldCount` | Number of result columns |
| `this[int ordinal]` | Equivalent to `GetValue(int ordinal)` |
| `this[string name]` | Equivalent to `GetValue(GetOrdinal(name))` |
| `HasRows` | Whether results exist |
| `RecordsAffected` | Number of fetched records |

### MachParameterCollection

```cs
public sealed class MachParameterCollection :
    DbParameterCollection,
    IEnumerable<MachParameter>
```

Manages parameters bound to a `MachCommand`.

Set parameters before execution to send their values with the command.

> `MachParameter` binding does not provide a Prepared Statement execution-plan cache.
> Measure repeated execution with actual queries and server cache conditions.
>
> The current provider renders parameters as typed SQL literals and executes through
> ExecDirect. `MachParameterCollection` therefore does not use the server Prepared
> Named Bind protocol or parameter metadata.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

Adds a `MachParameter` with the specified name and type, and returns it.

```cs
int Add(object value)
```

Adds a value and returns its index.

```cs
void AddRange(Array values)
```

Adds an array of plain values in one call.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

Adds a parameter name and value, and returns the created `MachParameter`.

#### Contains

```cs
bool Contains(object value)
```

Checks whether the value has already been added.

```cs
bool Contains(string parameterName)
```

Checks whether the specified parameter name exists.

#### Clear

```cs
void Clear()
```

Removes all parameters.

#### IndexOf

```cs
int IndexOf(object value)
```

Returns the index of the value.

```cs
int IndexOf(string parameterName)
```

Returns the index of the parameter name.

#### Insert

```cs
void Insert(int index, object value)
```

Inserts a value at the specified position.

#### Remove

```cs
void Remove(object value)
```

Removes the parameter containing the value.

```cs
void RemoveAt(int index)
```

Removes the parameter at the index.

```cs
void RemoveAt(string parameterName)
```

Removes the parameter with the specified name.

#### Fields

| Name | Description |
|--|--|
| `Count` | Parameter count |
| `this[int index]` | `MachParameter` at the index |
| `this[string name]` | `MachParameter` matching the name |

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

Stores binding information for one parameter.

#### Fields

| Name | Description |
|--|--|
| `ParameterName` | Parameter name |
| `Value` | Value to send |
| `Size` | Value length |
| `Direction` | `ParameterDirection`; default `Input` |
| `DbType` | .NET database type |
| `MachDbType` | Machbase-specific type |
| `IsNullable` | Whether `NULL` is allowed |
| `HasSetDbType` | Whether `DbType` is set |

### MachException

```cs
public class MachException : DbException
```

Exception class for Machbase errors.

#### Fields

| Name | Description |
|--|--|
| `MachErrorCode` | Machbase error code when available; may be `0` when the Universal provider translates legacy exceptions |

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

Helper class for the Append protocol. Obtain an instance by calling `MachCommand.AppendOpen()`.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType callback)

void ErrorDelegateFuncType(MachAppendException e);
```

Registers a delegate called on Append errors.

#### Fields

| Name | Description |
|--|--|
| `SuccessCount` | Successfully stored record count; available after `AppendClose()` |
| `FailureCount` | Failed record count; set after `AppendClose()` |
| `Option` | `MachAppendOption` supplied to `AppendOpen()` |

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Exception with additional Append error information. Preserves the server error message
and exposes the failed record as a string.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

Returns the original failed record as a string.

## Usage and Examples {#usage-and-examples}

### Connect

This example connects with an environment-variable password, creates a LOG table,
inserts and queries data, then drops the table.

```csharp
using System;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
const string tableName = "NET_QUERY_DEMO";

using (var create = new MachCommand(
    $"CREATE LOG TABLE {tableName} (id INTEGER, name VARCHAR(40))", connection))
{
    create.ExecuteNonQuery();
}
try
{
    using (var insert = new MachCommand(
        $"INSERT INTO {tableName} VALUES (1, 'pump')", connection))
    {
        insert.ExecuteNonQuery();
    }
    using var query = new MachCommand($"SELECT id, name FROM {tableName}", connection);
    using var reader = query.ExecuteReader();
    while (reader.Read())
    {
        for (var column = 0; column < reader.FieldCount; column++)
        {
            Console.WriteLine($"{reader.GetName(column)} : {reader.GetValue(column)}");
        }
    }
}
finally
{
    using var drop = new MachCommand($"DROP TABLE {tableName}", connection);
    drop.ExecuteNonQuery();
}
```

### Parameter Binding

`MachParameterCollection` supports `:name`, `@name`, and `?name` placeholders. Prefer
`:name`, which matches common SQL syntax. Name lookup is case-insensitive; a repeated
name applies one value to all matching positions.

Use `:name` with Machbase 8.7.0 servers. Older servers raise `MachException`.
`@name` and `?name` are legacy provider compatibility formats.

```csharp
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

const string sql = @"
    SELECT NAME
      FROM V$TABLES
     WHERE NAME = :table_name OR NAME = :table_name";

using var command = new MachCommand(sql, connection);

command.Parameters.AddWithValue(":table_name", "V$TABLES");

using var reader = command.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetName(0)} : {reader.GetValue(0)}");
}
```

Pass NULL as `DBNull.Value`. See
[Named Bind Parameter Syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)
for shared name syntax.

### Append

Use the Append protocol to load large volumes of time-series data quickly.

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

const string tableName = "NET_APPEND_DEMO";
using (var create = new MachCommand(
    $"CREATE LOG TABLE {tableName} (ID INTEGER, NAME VARCHAR(40))", connection))
{
    create.ExecuteNonQuery();
}

try
{
using var appendCommand = new MachCommand(connection);
var writer = appendCommand.AppendOpen(tableName);
writer.SetErrorDelegator(error =>
    Console.Error.WriteLine($"Append row error: {error.Message}\n{error.GetRowBuffer()}"));

try
{
    for (var i = 1; i <= 100000; i++)
    {
        appendCommand.AppendData(writer, new List<object> { i, $"NAME_{i % 100}" });
        if (i % 1000 == 0) appendCommand.AppendFlush(writer);
    }
}
finally
{
    if (appendCommand.IsAppendOpened) appendCommand.AppendClose(writer);
}

Console.WriteLine($"Success Count : {writer.SuccessCount}");
Console.WriteLine($"Failure Count : {writer.FailureCount}");
if (writer.FailureCount != 0)
    throw new InvalidOperationException($"Append failed rows: {writer.FailureCount}");
}
finally
{
    if (connection.State == System.Data.ConnectionState.Open)
    {
        try
        {
            using var drop = new MachCommand($"DROP TABLE {tableName}", connection);
            drop.ExecuteNonQuery();
        }
        catch (Exception cleanupError)
        {
            Console.Error.WriteLine($"cleanup failed: {cleanupError.Message}");
        }
    }
}
```

### ARRAY and Selected-Column Append

Machbase DBMS 8.7.0 full/legacy providers return ARRAY as `object[]`. Element NULL is
`null` within the array; use `IsDBNull()` to identify whole-array NULL.

Standard `AppendOpen(table)` can also accept `MachSparseArray` as an ARRAY column value.

```csharp
var writer = append.AppendOpen("ARRAY_APPEND_FULL_EXAMPLE");
```

Input rows follow table column order. The
[standard Open example](../data-input-load-export/array-append/#dotnet-full-open) inserts
sparse values, empty sparse arrays, and whole NULL into `ID LONG, A INT32[4]`, covering
`AppendData()`, Close, and result checks.

The `IList<string>` overload of `AppendOpen()` accepts ordinary columns or
`ARRAY_COLUMN[position]`. To vary positions by row, pass `MachSparseArray` to a
whole-array target. Element targets and `MachSparseArray.Set()` positions are 0-based.

```csharp
using var append = new MachCommand(connection);
var writer = append.AppendOpen(
    "ARRAY_APPEND_EXAMPLE",
    new List<string> { "ID", "A" });
var sparse = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
    .Set(1, 200)
    .Set(3, 400);

try
{
    append.AppendData(writer, new List<object> { 2L, sparse });
}
finally
{
    if (append.IsAppendOpened)
        append.AppendClose(writer);
}
```

An empty `MachSparseArray` means an ARRAY with all NULL elements; `DBNull.Value` means
whole-array NULL. See [Sparse ARRAY and Selected-Column Append API](../data-input-load-export/array-append/)
for overloads and complete validation examples.

### Configure the Error Delegate

Register the delegate immediately after opening the writer to receive row errors as
in the example above. Check success/failure counts after close.

### Configure Automatic AppendFlush

AppendOpen starts an automatic flush thread. To disable it, call
`connection.SetConnectAppendFlush(false)` on an already open writer. Automatic thread
errors may not immediately surface as public exceptions; retain explicit flush/close
and callback/count checks.

## Protocol 4.0-full APIs {#full-provider-apis-protocol-40-full}

`PROTOCOL=4.0-full` enables expanded ADO.NET APIs. In the 8.0.55 source package, the
4.0 limited connector is 3.1.3 and 4.0-full is 3.2.2. Linux installations may include
only the net50 variant under `$MACHBASE_HOME/lib/`; use source builds or NuGet restore
artifacts for other target frameworks.

- `UniMachNetConnector-net50-8.0.55.dll` – Universal entry point commonly installed
  with the DBMS Standard Linux package
- `machNetConnector-40-net50-3.1.3.dll` – Protocol 4.0 limited connector
- `machNetConnector-40-net50-3.2.2.dll` – Protocol 4.0-full connector

### Main Types Added in 4.0-full

- `MachDbProviderFactory`: Registers/creates the provider with invariant name `Mach.Data`.
- `MachConnectionStringBuilder`: Constructs connection strings without keyword typos.
- `MachDataAdapter`, `MachRowUpdating`, `MachRowUpdated`: Support `DataTable`/`DataSet` workflows.
- `MachCommandBuilder`: Generates INSERT/DELETE (and UPDATE under certain conditions)
  from SELECT. Before execution, check that generated SQL complies with the target
  table DML restrictions.

### Enable the Full API

```csharp
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

For UPDATE/DELETE, check both table-specific requirements and driver SQL generation
capabilities. LOG does not support UPDATE. TAG UPDATE in Machbase DBMS 8.7.0 Standard
Edition requires NAME and BASETIME predicates. Use commands and bindings that follow
[TAG UPDATE Syntax](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/)
instead of relying on generic CommandBuilder output.

### Use the Connection String Builder

```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
        ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required")
};

builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### Example: SQL INSERT with MachDataAdapter

Load a LOOKUP table into a `DataTable` and add a row; the command builder executes an
ordinary SQL INSERT. This path does not use the Append protocol.

```csharp
using Mach.Data.MachClient;
using System;
using System.Data;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

using (var create = new MachCommand(
    "CREATE LOOKUP TABLE dotnet_lookup_demo (id INTEGER PRIMARY KEY, name VARCHAR(80))",
    connection))
{
    create.ExecuteNonQuery();
}

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

adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine(
        $"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};

adapter.Update(table);

using var drop = new MachCommand("DROP TABLE dotnet_lookup_demo", connection);
drop.ExecuteNonQuery();
```

> **Tip:** To inspect SQL before transmission, subscribe to events before `Update()`, as above.

### Example: Use DbProviderFactory

`MachDbProviderFactory.Instance` connects Machbase to provider-neutral configurations
such as `DbProviderFactories` and Dapper.

```csharp
using System;
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
connection.ConnectionString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM V$TABLES";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Visible tables: {count}");
```

For automatic factory discovery in configuration-based applications, call
`MachDbProviderFactory.Register()` once at startup so that
`DbProviderFactories.GetFactory("Mach.Data")` returns the same instance.

Protocol `4.0-full` requires Machbase 7.x or later. For older servers, use
`PROTOCOL=4.0` (limited features) or protocols 2.x/3.x.
