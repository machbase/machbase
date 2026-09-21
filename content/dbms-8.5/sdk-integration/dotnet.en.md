---
title: '.NET Connector'
type: docs
weight: 20
---

## Index

* [Overview](#overview)
* [Install](#install)
* [NuGet (Unified 8.0.54)](#install-via-nuget-unified-connector-8054)
* [NuGet (Legacy 5.x)](#install-via-nuget-legacy-5x)
* [Connection String Reference](#connection-string-reference)
* [API Reference](#api-reference)
* [Usage and Examples](#usage-and-examples)
* [Full Provider APIs (Protocol 4.0-full)](#full-provider-apis-protocol-40-full)

## Overview

Machbase ships a universal ADO.NET provider, **UniMachNetConnector**, that wraps every supported Machbase wire protocol (2.1 through 4.0). The DBMS standard source currently identifies the unified package as `UniMachNetConnector` version 8.0.54 and builds the target frameworks `net452`, `net5.0`, `net6.0`, `net7.0`, and `net8.0`. The connector automatically negotiates the correct protocol at runtime based on the connection string, so time-series ingestion and query workloads get a suitable protocol without extra configuration.

## Install

The Machbase server and client installers include the universal .NET provider under `$MACHBASE_HOME/lib/`.
A standard Linux install can include the .NET 5.0 build, for example
`UniMachNetConnector-net50-8.0.54.dll`, together with protocol-specific assemblies such as
`machNetConnector-40-net50-3.2.1.dll`. The source project can build additional target-framework
flavors when the matching .NET SDK is available.

- **UniMachNetConnector**: The framework-neutral entry point. Source builds are named
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll`, so choose the build that matches
  the target framework you deploy.
- **Legacy protocol connectors**: Optional protocol-specific assemblies that the universal
  loader activates on demand, such as `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`.

Reference the DLL that matches your application's target framework, or copy it next to your binaries when you deploy.

## Install via NuGet (Unified Connector, 8.0.54)

The unified provider package ID is `UniMachNetConnector`. This is the recommended way for new apps because it keeps your project self-contained without shipping loose DLLs.

- Supported target frameworks: net452, net5.0, net6.0, net7.0, net8.0.
- The net5.0 and newer builds are self-contained. The net452 build restores `System.ValueTuple`
  4.5.0, as reflected in the source project.

### Quick start (CLI)

```bash
# From your project folder
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

If you need to control the package sources (CI, offline, or a corporate feed), add the reference first and then restore explicitly:

```bash
dotnet add package UniMachNetConnector --version 8.0.54 --no-restore

# Restore from nuget.org only (force fresh metadata)
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- Right-click your project → Manage NuGet Packages → Browse tab → search “UniMachNetConnector” → select version 8.0.54 → Install.

### Project file example

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
  <!-- no other Machbase packages required -->
  <!-- targets: net452|net5.0|net6.0|net7.0|net8.0 -->
  <!-- keep AnyCPU/x64 per your app; Machbase server side is unaffected -->
</ItemGroup>
```

### Using a local or private feed (optional)

If your environment uses a local folder feed or an internal registry, point restore to those sources. For a folder feed, place `UniMachNetConnector.8.0.54.nupkg` in a directory and add it as a source:

```bash
# one-time setup
dotnet nuget add source /path/to/local-nuget -n mach-local

# restore using both nuget.org and the local feed
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

In CI or restricted accounts, specify the package cache directory with an absolute path:

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> Tip: If `NU1102` (unable to find the specified version) appears right after 8.0.54 is published, or `dotnet add package` still reports an older version, the cause is usually indexing or caching. Clear the HTTP cache with `dotnet nuget locals http-cache --clear` and restore with `--no-cache` as shown above. A transient “incompatible with 'all' frameworks” message is usually a side effect of a failed restore, not a real TFM mismatch; the package supports net452 and net5.0–net8.0.

### Minimal usage sample

```csharp
using Mach.Data.MachClient;

var cs = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = (long)cmd.ExecuteScalar();
Console.WriteLine($"Tables: {count}");
```

## Install via NuGet (Legacy 5.x)

> **Note**: Machbase .NET Connector 5.0 is also registered on NuGet. This 5.0 package is the legacy standalone distribution that predates the unified UniMachNetConnector.

If you use Visual Studio, you can still obtain the pre-unified connector from NuGet. The steps below install the legacy `machNetConnector5.0` package. Use it only when you must target older code that predates the unified provider; for new projects, `UniMachNetConnector` 8.0.54 is recommended.

1. In Visual Studio, create a new C# .NET project.
2. In Solution Explorer, right-click the project name and select **Manage NuGet Packages**.
3. When the NuGet Package Manager window opens, select the **Browse** tab at the upper left and search for `machNet`.
4. In the search results, select **machNetConnector5.0** and click **Install**.
5. If the **Preview Changes** window appears, click **OK** to continue the installation.
6. When the installation is complete, you can find the package under **Dependencies → Packages** in Solution Explorer.
7. Add `using Mach.Data.MachClient;` to `Program.cs` to use the machNetConnector API.

> Which NuGet should I use?
> - Prefer `UniMachNetConnector` 8.0.54 for new or upgraded apps. It supports net452 and net5.0–net8.0 and bundles all protocols, including the full provider surface (4.0-full).
> - Use `machNetConnector5.0` only for legacy scenarios where migrating to the unified package is not yet possible.

## Connection String Reference

Connection-string segments are separated by semicolons (`;`). Keywords listed in the same row are aliases.

| Keyword                                                         | Description                                                                                              | Example                                         | Default |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST`                                         | Hostname or IP address                                                                                    | `SERVER=127.0.0.1`                              | _(none)_|
| `PORT`, `PORT_NO`                                               | Listener port                                                                                             | `PORT=5656`                                    | `5656`  |
| `USERID`, `USERNAME`, `USER`, `UID`                             | Username                                                                                                  | `UID=SYS`                                       | `SYS`   |
| `PASSWORD`, `PWD`                                               | Password                                                                                                  | `PWD=manager`                                   | _(none)_|
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout`        | Connection timeout in milliseconds                                                                        | `CONNECT_TIMEOUT=10000`                        | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout`           | Per-command timeout in milliseconds                                                                       | `COMMAND_TIMEOUT=50000`                        | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol`                   | Preferred wire protocol (for example `2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full`). UniMachNetConnector defaults to `4.0` when omitted. | `PROTOCOL=auto`                                | `4.0`   |

Example:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### Protocol auto-detection (`PROTOCOL=auto`)

When your application connects to a mix of Machbase releases, set `PROTOCOL=auto` to let UniMachNetConnector negotiate the correct legacy handshake at runtime. The resolver works as follows:

- `PROTOCOL=auto` tries versions 4.0, 3.0, 2.2, and then 2.1 in that order, using the host, port, user, password, database, and `CONNECT_TIMEOUT` supplied in the connection string.
- `PROTOCOL=auto-full` behaves the same, but when the server reports protocol 4.0, the connector tries the full-provider descriptor (`4.0-full`) first and falls back to the limited version (4.0) if needed.
- Multiple hosts in `SERVER=hostA:5700,hostB:6000` are tried sequentially; each failure message records the per-host/per-protocol attempt so you can pinpoint unreachable versions.
- Credentials are upper-cased the same way as the legacy native drivers, so existing SYS/MANAGER test deployments work without change. Provide an explicit `DATABASE=` value when you do not use the default `data` catalog.
- `CONNECT_TIMEOUT` applies to each probe round trip. If you see `Protocol probe received an invalid response (missing result)` in the exception text, the handshake did not complete; verify the port, TLS/SSL settings, or firewall.

If you already know the exact server version, you can skip auto-detection by specifying `PROTOCOL=2.1`, `3.0`, `4.0`, or `4.0-full` explicitly.

## API Reference

{{<callout type="warning">}}
Features not listed below may not be implemented yet or may not work correctly.<br>
Calling a method or field that does not exist throws `NotImplementedException` or `NotSupportedException`.
{{</callout>}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

This class handles the connection to Machbase.

Like DbConnection, it implements IDisposable, so it can be released with Dispose() or automatically with a using statement.

#### Constructor

```
MachConnection(string aConnectionString)
```

Creates a MachConnection instance from a connection string.

#### Open

```cs
void Open()
```

Establishes the actual connection using the connection string.

#### Close

```cs
void Close()
```

Closes the open connection.

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Sets whether flush is performed automatically during append.

#### Field

| Name | Description |
|--|--|
|State|Represents a System.Data.ConnectionState value.|
|StatusString|The status string of the MachCommand that the connection currently depends on.<br>It is used internally to build error messages and indicates the state in which the operation started, so do not use it to check the status of a query.|

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

A class that executes **SQL commands or APPEND** through MachConnection.

Like DbCommand, it implements IDisposable, so it can be released with Dispose() or automatically with a using statement.

#### Constructor

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

Creates an instance with the query to execute and the MachConnection object to use.

```cs
MachCommand(MachConnection aConn)
```

Creates an instance with only the MachConnection object to use. Use it when there is no query to execute (for example, APPEND).

#### CreateParameter

```cs
MachParameter CreateParameter()
```

Creates a new MachParameter.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

Starts APPEND and returns a MachAppendWriter object.

* aTableName: Target table name.
* aErrorCheckCount: Each time the cumulative number of records entered with AppendData reaches this value, the records are sent to the server and checked for failure. In other words, it sets the automatic APPEND-FLUSH point.
* option: One of the following MachAppendOption values.
    * MachAppendOption.None: No option.
    * MachAppendOption.MicroSecTruncated: DateTime values are entered only up to microseconds. (The Ticks value of a DateTime object is expressed in units of 100 nanoseconds.)

#### AppendData

```cs
void AppendData(MachAppendWriter aWriter, List<object> aDataList)
```

Takes a list containing the data and enters it into the database through the MachAppendWriter object.

- The values in the list are loaded into the Append buffer in order, and the type of each value must match the type of the corresponding table column.
- If the list has too few or too many values, an exception occurs.

> **Note**: When you specify `_arrival_time` as a `ulong`, pass the number of nanoseconds since 1970-01-01 UTC, as Machbase expects. Do not pass the Tick value of a DateTime object as is: because `DateTime.Ticks` is in units of 100 nanoseconds, subtract the Ticks of the epoch (1970-01-01) from the UTC Ticks and multiply the result by 100.

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)
```

Same as AppendData(), but explicitly specifies the `_arrival_time` value as a DateTime object.

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong)
```

Same as AppendData(), but explicitly specifies the `_arrival_time` value as a `ulong` in nanoseconds. For the points to check when you pass a `ulong` value as `_arrival_time`, see AppendData() above.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter aWriter)
```

Immediately sends the data entered with AppendData() to the server to force the insert.<br>
The more often it is called, the less data is lost on a system failure and the sooner errors are detected, but performance goes down.<br>
The less often it is called, the more likely data loss becomes and the later errors are detected, but performance goes up significantly.

#### AppendClose

```cs
void AppendClose(MachAppendWriter aWriter)
```

Closes APPEND. Internally, it calls AppendFlush() and then finishes the protocol.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

Executes the query and returns the number of records affected by it. It is usually used for queries other than SELECT, such as INSERT, UPDATE, DELETE, and DDL.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

Executes the query and returns the first value of the query's target list as an object. It is usually used to get the result of a SELECT query that returns only one value (a scalar query) without a DbDataReader.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)
```

Executes the query and returns a DbDataReader that reads the query result sequentially.

#### Field

| Name | Description|
|--|--|
| Connection / DbConnection                   | The connected MachConnection.|
| ParameterCollection / DbParameterCollection | The MachParameterCollection used for binding.|
| CommandText                                 | The SQL string to execute.|
| CommandTimeout                              | The maximum time (in milliseconds) to wait for a response from the server.<br>It follows the value set in MachConnection and can only be read here.|
| FetchSize                                   | The number of records to fetch from the server at one time. The default value is 3000.|
| IsAppendOpened                              | Whether an Append session is open.|

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

A class that reads fetched results sequentially. It cannot be created directly; use only the object obtained from MachCommand.ExecuteDbDataReader().

#### GetName

```cs
string GetName(int ordinal)
```

Returns the name of the column at the ordinal position.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Returns the Machbase data type name of the column at the ordinal position.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

Returns the .NET type mapped to the column at the ordinal position.

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

Returns the index at which the column name is located.

#### GetValue

```cs
object GetValue(int ordinal)
```

Returns the value at the ordinal position of the current record as an `object`.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

Returns whether the value at the ordinal position of the current record is NULL.

#### GetValues

```cs
int GetValues(object[] values)
```

Fills the array with the values of the current record and returns the number of values filled.

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

Returns the value of the column at the ordinal position as the specified data type.

#### Read

```cs
bool Read()
```

Reads the next record. Returns false if there are no more results.

#### Field

| Name | Description|
|--|--|
| FetchSize         |The number of records to fetch from the server at one time. The default is 3000, and it cannot be modified here.|
| FieldCount        |Number of result columns.|
| this[int ordinal] |Equivalent to GetValue(int ordinal).|
| this[string name] |Equivalent to GetValue(GetOrdinal(name)).|
| HasRows           |Whether the result exists.|
| RecordsAffected   |Unlike in MachCommand, it represents the number of fetched records here.|

### MachParameterCollection

```cs
public sealed class MachParameterCollection : DbParameterCollection, IEnumerable<MachParameter>
```

A class that manages the set of parameters bound to a MachCommand.

If you execute the command after binding, the values are sent together.

> Since the execution plan cache of a prepared statement is not implemented in the current version, executing the same query repeatedly performs the same as the first execution.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

Adds a MachParameter with the specified parameter name and type, and returns the added MachParameter object.

```cs
int Add(object value)
```

Adds a value and returns the index where it was added.

```cs
void AddRange(Array values)
```

Adds an array of simple values at once.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

Adds a parameter name and its value together, and returns the added MachParameter object.

#### Contains

```cs
bool Contains(object value)
```

Determines whether the value has already been added.

```cs
bool Contains(string value)
```

Determines whether a parameter with the specified name exists.

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

Inserts the value at the specified index.

#### Remove

```cs
void Remove(object value)
```

Removes the parameter that contains the value.

```cs
void RemoveAt(int index)
```

Removes the parameter at the index.

```cs
void RemoveAt(string parameterName)
```

Removes the parameter with the specified name.

#### Field

| Name                 | Description                 |
| ----------------- | --------------------------------------- |
|Count              | Number of parameters.|
|this[int index]    | The MachParameter at the index.|
|this[string name]  | The MachParameter whose name matches.|

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

A class that stores the binding information of an individual parameter for a MachCommand.

No special methods are supported.

#### Field

| Name            | Description                                                                          |
| ------------- | --------------------------------------------------------------------------------- |
|ParameterName|Parameter name|
|Value|Value to send|
|Size|Value size|
|Direction|ParameterDirection (Input / Output / InputOutput / ReturnValue)<br>The default value is Input.|
|DbType|.NET-side DB type|
|MachDbType|Machbase DB type<br>It may differ from DbType.|
|IsNullable|Whether NULL is allowed|
|HasSetDbType|Whether DbType has been set|

### MachException

```cs
public class MachException : DbException
```

A class that represents errors that occur in Machbase.

An error message is set, and all error messages can be found in MachErrorMsg.

#### Field

| Name| Description|
|--|--|
|int MachErrorCode|Error code returned by Machbase|

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

A helper class that supports APPEND separately, used together with MachCommand.
It supports the Machbase Append protocol, not the ADO.NET standard.

It has no separate constructor; you obtain an instance by calling MachCommand.AppendOpen().

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType aFunc)

void ErrorDelegateFuncType(MachAppendException e);
```

Registers the ErrorDelegateFunc to call when an error occurs during Append.

#### Field

| Name | Description |
|--|--|
|SuccessCount|The number of records stored successfully. It is set after AppendClose().|
|FailureCount|The number of records that failed to be entered. It is set after AppendClose().|
|Option|The MachAppendOption value passed to AppendOpen().|

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Same as MachException, except for the following:

* The error message is received from the server as is.
* The data buffer of the record that caused the error can be obtained (comma-separated), so you can process it and append it again or record it.

This exception is available only inside the ErrorDelegateFunc.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

Returns the data buffer of the record that caused the error as a string.

## Usage and Examples

### Connection

You can create a MachConnection and control the connection with Open() and Close().

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//... do something
sConn.Close();
```

If you use the using statement, resources are released without calling Close() yourself.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=SYS;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //... do something
} // you don't need to call sConn.Close();
```

### Executing Queries

You can create a MachCommand and execute SQL statements.

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

With the using statement, the MachCommand can also be released immediately.

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

### Executing SELECT

Executing a MachCommand with a SELECT query through ExecuteReader() gives you a MachDataReader.

You can fetch the records one by one through the MachDataReader.

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

### Parameter Binding

You can fill the MachParameterCollection of a MachCommand with parameters. This lets you pass conditions, such as a time-series query range, safely as parameters.

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

### APPEND

With the Append protocol, you can load a large amount of time-series data quickly.

When you run AppendOpen() on a MachCommand, you get a MachAppendWriter object.

With this object and the MachCommand, pass a list holding one input record to AppendData().
AppendFlush() applies the input of all records, and AppendClose() ends the entire Append process.

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

### Set Error Delegator

In MachAppendWriter, you can specify a function that is called when an error occurs on the Machbase server side during APPEND.

In .NET, this function is specified as a delegate function.

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

### Set Auto AppendFlush

If you call `SetConnectAppendFlush(true)` on the connection, flush is performed automatically at regular intervals during append.

```cs
private static string connString = $"SERVER={HOST};PORT_NO={port};USER={USER};PWD={PWD}";

public static void Main(string[] args)
{
    MachConnection conn = new MachConnection(connString);
    conn.Open();
    conn.SetConnectAppendFlush(true);
}
```

If set to false, automatic flush is disabled.

```cs
conn.SetConnectAppendFlush(false);
```

## Full Provider APIs (Protocol 4.0-full)

The `4.0-full` handshake unlocks the full ADO.NET surface. In the 8.0.54 source package,
the 4.0 limited connector is version 3.1.2 and the 4.0-full connector is version 3.2.1.
Installed Linux packages may include only the net50 flavor under `$MACHBASE_HOME/lib/`; build
or restore additional target frameworks when your application needs them.

- `UniMachNetConnector-net50-8.0.54.dll` – universal entry point commonly installed with DBMS Standard Linux packages.
- `machNetConnector-40-net50-3.1.2.dll` – protocol 4.0 limited connector.
- `machNetConnector-40-net50-3.2.1.dll` – protocol 4.0-full connector.

### Key types introduced by 4.0-full

- `MachDbProviderFactory` (`Instance`, `Register()`, and the standard `Create*` methods) so frameworks can resolve the connector by the invariant name `Mach.Data`.
- `MachConnectionStringBuilder` for strongly typed connection-string edits without remembering every keyword.
- `MachDataAdapter` plus the `MachRowUpdating`/`MachRowUpdated` events for DataTable/DataSet workflows.
- `MachCommandBuilder` to auto-generate INSERT/DELETE (and UPDATE for tables that support it—never for log/tag tables) commands from a SELECT statement.

### Enable the full provider stack

```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

Use lookup or volatile tables when you need INSERT/DELETE/UPDATE semantics. Log and tag tables do not accept UPDATE statements, so keep those workloads append-only.

### Build connection strings fluently

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

### Sample: append rows with MachDataAdapter

This example loads a lookup table into a `DataTable`, adds a new row, and pushes the change back with `MachDataAdapter`. The `MachCommandBuilder` auto-generates the INSERT statement. (If the table does not exist yet, create it once: `CREATE LOOKUP TABLE dotnet_lookup_demo(id LONG PRIMARY KEY, name VARCHAR(64));`)

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

> **Tip**: When you need to inspect or veto outgoing commands before they are sent, subscribe to `MachDataAdapter.MachRowUpdating` / `MachRowUpdated`.

```csharp
adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine($"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};
```

### Sample: work through DbProviderFactory

`MachDbProviderFactory.Instance` lets you plug Machbase into provider-agnostic infrastructure such as `DbProviderFactories`, Dapper, or your own DI container.

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

To expose the factory to configuration-driven apps, call `MachDbProviderFactory.Register()` once during startup so that `DbProviderFactories.GetFactory("Mach.Data")` returns the same instance.

Remember that `4.0-full` is available only when you connect to Machbase 7.x or later servers; for older servers, fall back to `PROTOCOL=4.0` (limited surface) or the 2.x/3.x protocols.
