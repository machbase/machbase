---
layout : post
title : '.NET Connector'
type : docs
weight: 40
---

## Index

* [Install](#install)
* [Install Connector via NuGet Package Manager](#install-connector-via-nuget-package-manager)
* [API Reference](#api-reference)
* [Sample Code](#sample-code)

## Install

The .NET (C #) Connector library that supports some features of the ADO.NET driver is provided.

The library location is  $MACHBASE_HOME/lib/ provided as a DLL type. It provides different DLLs depending on the .NET version.

* .NET Framework 4.0: machNetConnector40.dll
* .NET Framework 5.0: machNetConnector50.dll

## Install Connector via NuGet Package Manager

<u>.NET Connector 5.0 of Machbase has already enrolled to NuGet package!</u>   
If you use Visual Studio, you'll easily get and use .NET Connector from NuGet repository.   
Below procedure is about how to get machNetConnector5.0 from NuGet.   

1. In Visual Studio, create a new C# .NET project.
2. When the project is created, activate context menu above project name at Solution Explorer and select "Manage NuGet Packages".
3. When NuGet Package Manager window is activated, select "Browse" tab on the upper left and search "machNet".
4. When the result is displayed on the left pane, select "machNetConnector5.0" and select "Install".
5. If Preview Changes window is activated, just select "OK" to continue to install.
6. When the package was installed successfully, you can confirm it at "Dependencies - Packages" on Solution Explorer.
7. Now, you can use machNetConnector by "using Mach.Data.MachClient" at Program.cs.


## API Reference

{{<callout type="warning">}}
Features not listed below may not be implemented yet or may not work correctly.<br>
If you call a method or field that is not a named instance, it generates NotImplementedException or a NotSupportedException.
{{</callout>}}

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

This class is responsible for linking with Machbase. 

Because it inherits IDisposable like DbConnection, it supports disassociation through Dispose () or automatic disposition of object using using () statement.

#### Constructor
```
MachConnection(string aConnectionString)
```

Creates a MachConnection with a Connection String as input.


#### Open

```cs
void Open()
```

Attempts to connect to the connection string.

#### Close

```cs
void Close()
```

Closes the connection when connecting.

#### Field

| Name | Description |
|--|--|
|State|Represents a System.Data.ConnectionState value.|
|StatusString|Indicates the state to be performed by the connected MachCommand.<br>This is used internally to decorate the Error Message and it is not appropriate to check the status of the query with this value because it indicates the state in which the operation started.|


### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

A class that performs **SQL commands or APPEND** using MachConnection. 

Since it inherits IDisposable like DbCommand, it supports object disposal through Dispose () or automatic disposal of object using using () statement

#### Constructor

```cs
MachCommand(string aQueryString, MachConnection)
```

Creates by typing the query to be executed along with the MachConnection object to be connected.

```cs
MachCommand(MachConnection)
```

Creates a MachConnection object to connect to. Use only if there is no query to perform (eg APPEND).


#### CreateParameter

```cs
MachParameter CreateParameter()
```

Creates a new MachParameter.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(aTableName, aErrorCheckCount = 0, MachAppendOption = None)
```

Starts APPEND. Returns a MachAppendWriter object.

* aTableName: Target table name
* aErrorCheckCount: Each time the cumulative number of records entered by APPEND-DATA matches, it is checked whether it is sent to the server or not.<br>
  In other words, you are setting the automatic APPEND-FLUSH point.<br>
* MachAppendOption: Currently only one option is provided.
  * MachAppendOption.None: No options are attached.
  * MachAppendOption.MicroSecTruncated: When inputting the value of a DateTime object, enter the value expressed only up to microsecond.
  (The Ticks value of a DateTime object is expressed up to 100 nanoseconds.)

#### AppendData

```cs
void AppendData(MachAppendWriter aWriter, List<object> aDataList)
```

Through the MachAppendWriter object, it takes a list containing the data and enters it into the database.
- In the order of the data in the List, each datatype must match the datatype of the column represented in the table.
- If the data in the List is insufficient or overflows, an error occurs.
<blockquote> 
  <p>When representing a time value with a ulong object, simply do not enter the Tick value of the DateTime object. <br><br>In that value, you must enter a <u>value that excludes the DateTime Tick value that represents 1970-01-01</u>.</p>
</blockquote>


```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)
```

Method that explicitly puts an _arrival_time value into a DateTime object in AppendData().

```cs
void AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong)
```

Method that can explicitly put _arrival_time value into a ulong object in AppendData(). Refer to AppendData() above for problems that may occur when typing a ulong value as an _arrival_time value.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter aWriter)
```

The data entered by AppendData() is immediately sent to the server to force data insert.<br>
The more frequently the call is made, the lower the data loss rate due to the system error and the faster the error check, although the performance is lowered.<br>
The less frequently the call is made, the more likely the data loss will occur and the error checking will be delayed, but the performance will increase significantly.

#### AppendClose

```cs
void AppendClose(MachAppendWriter aWriter)
```

Closes APPEND. Internally, after calling AppendFlush(), the actual protocol is internally finished.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

Performs the input query. Returns the number of records affected by the query. It is usually used when performing queries except SELECT.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

Performs the input query. Returns the first value of the query targetlist as an object. It is usually used when you want to perform a SELECT query, especially a SELECT (Scalar Query) with only one result, and get the result without a DbDataReader.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)
```

Executes the input query, generates a DbDataReader that can read the result of the query, and returns it.

#### Field

| Name | Description|
|--|--|
| Connection / DbConnection                   | Connected MachConnection.|
| ParameterCollection / DbParameterCollection | The MachParameterCollection to use for the Binding purpose.|
| CommandText                                 | Query string.|
| CommandTimeout                              | The amount of time it takes to perform a particular task, waiting for a response from the server.<br>It follows the values ​​set in MachConnection, where you can only reference values.|
| FetchSize                                   | The number of records to fetch from the server at one time . The default value is 3000.|
| IsAppendOpened                              | Determines if Append is already open when APPEND is at work|


### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

This is a class that reads fetch results. Only objects created with MachCommand.ExecuteDbDataReader () that can not be explicitly created are available.

#### GetName

```cs
string GetName(int ordinal)
```

Returns the ordinal column name.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Returns the datatype name of the ordinal column.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

Returns the datatype of the ordinal column.


#### GetOrdinal

```cs
int GetOrdinal(string name)
```

Returns the index at which the column name is located.


#### GetValue

```cs
object GetValue(int ordinal)
```

Returns the ordinal value of the current record.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

Returns whether the ordinal value of the current record is NULL.

#### GetValues

```cs
int GetValues(object[] values)
```

Sets all the values ​​of the current record and returns the number.

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

Returns the ordinal column value according to the datatype.

#### Read

```cs
bool Read()
```

Reads the next record. Returns False if the result does not exist.

#### Field

| Name | Description|
|--|--|
| FetchSize         |The number of records to fetch from the server at one time. The default is 3000, which can not be modified here.|
| FieldCount        |Number of result columns.|
| this[int ordinal] |Equivalent to object GetValue (int ordinal).|
| this[string name] |Equivalent to object GetValue(GetOrdinal(name).|
| HasRows           |Indicates whether the result is present.|
| RecordsAffected   |Unlike MachCommand, here, it represents Fetch Count.|

### MachParameterCollection

```cs
public sealed class MachParameterCollection : DbParameterCollection, IEnumerable<MachParameter>
```

This is a class that binds parameters needed by MachCommand.

If you do this after binding, the values ​​are done together. 

> Since the concept of Prepared Statement is not implemented, execution performance after Binding is the same as the performance performed first.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

Adds the MachParameter, specifying the parameter name and type. Returns the added MachParameter object.

```cs
int Add(object value)
```

Adds a value. Returns the index added.


```cs
void AddRange(Array values)
```

Adds an array of simple values.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

Adds the parameter name and its value. Returns the added MachParameter object.|

#### Contains

```cs
bool Contains(object value)                                        
```

Determines whether or not the corresponding value is added.

```cs
bool Contains(string value)
```

Determines whether or not the corresponding parameter name is added.

#### Clear

```cs
void Clear()
```

Deletes all parameters.

#### IndexOf

```cs
int IndexOf(object value)
```

Returns the index of the corresponding value.

```cs
int IndexOf(string parameterName)
```

Returns the index of the corresponding parameter name.

#### Insert

```cs
void Insert(int index, object value)
```

Adds the value to a specific index.

#### Remove

```cs
void Remove(object value)
```

Deletes the parameter including the value.

```cs
void RemoveAt(int index)
```

Deletes the parameter located at the index.

```cs
void RemoveAt(string parameterName)
```

Deletes the parameter with that name.

#### Field

| Name                 | Description                 |
| ----------------- | --------------------------------------- |
|Count              | Number of parameters|
|this[int index]    | Indicates the MachParameter at index.|
|this[string name]  | Indicates the MachParameter of the order in which the parameter names match.|

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

This is a class that contains the information that binds the necessary parameters to each MachCommand.

No special methods are supported.

#### Field

| Name            | Description                                                                          |
| ------------- | --------------------------------------------------------------------------------- |
|ParameterName|Parameter name|
|Value|Value|
|Size|Value size|
|Direction|ParameterDirection (Input / Output / InputOutput / ReturnValue)<br>The default value is Input.|
|DbType|DB Type|
|MachDbType|MACHBASE DB Type<br>May differ from DB Type.|
|IsNullable|Whether nullable|
|HasSetDbType|Whether DB Type is specified|


### MachException

```cs
public class MachException : DbException
```

This is a class that displays errors that appear in Machbase.

An error message is set, and all error messages  can be found in  MachErrorMsg .

#### Field

| Name| Description|
|--|--|
|int MachErrorCode|Error code provided by MACHBASE|

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

APPEND is supported as a separate class using MachCommand.
This is a class to support MACHBASE Append Protocol, not ADO.NET standard.

It is created with MachCommand's AppendOpen () without a separate constructor.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType aFunc)

void ErrorDelegateFuncType(MachAppendException e);
```

Specifies the ErrorDelegateFunc to call when an error occurs.

#### Field

| Name | Description |
|--|--|
|SuccessCount|Number of successful records. Is set after AppendClose().|
|FailureCount|The number of records that failed input. Set after AppendClose ().|
|Option|MachAppendOption received input during AppendOpen()|


### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Same as MachException, except that:

* An error message is received from the server side.
* A data buffer in which an error has occurred can be obtained. (comma-separated) can be used to process and re-append or record data.

The exception is only available within the ErrorDelegateFunc.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

A data buffer in which an error has occurred can be obtained.

## Sample Code

### Connection

You can create a MachConnection and use Open () - Close ().
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//... do something
sConn.Close();
```

If you use the using statement, you do not need to call Close (), which is a connection closing task.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //... do something
} // you don't need to call sConn.Close();
```

### Executing Queries

Create a MachCommand and perform the query.

```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    String sQueryString = "CREATE TABLE tab1 ( col1 INTEGER, col2 VARCHAR(20) )";
    MachCommand sCommand = new MachCommand(sQueryString , sConn)
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

Again, using the using statement, MachCommand release can be done immediately.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
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
You can get a MachDataReader by executing a MachCommand with a SELECT query. 

You can fetch the records one by one through the MachDataReader.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
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
You can create a MachParameterCollection and then link it to a MachCommand.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
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
When you run AppendOpen () on a MachCommand, you get a MachAppendWriter object.

Using this object and MachCommand, you can get a list of one input record and perform an AppendData().
AppendFlush() will reflect the input of all records, and AppendClose () will end the entire Append process.
```c#
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
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
                sAppendCommand.AppendFlush();
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

#### Connection String

Each item is separated by a semicolon (;).
Many of the keywords in the same section have the same meaning.

| Keyword                                                | Description   | Example            | Default value |
| ------------------------------------------------------ | ------------- | ------------------ | ---- |
| DSN<br>SERVER<br>HOST                                  | Hostname      | DSN=localhost<br>SERVER=192.168.0.1 |      |
| PORT<br>PORT_NO                                        | Port No.      | PORT=5656          | 5656 |
| USERID<br>USERNAME<br>USER<br>UID                      | User ID        | USER=SYS           | SYS  |
| PASSWORD<br>PWD                                        | User password      | PWD=manager        |      |
| CONNECT_TIMEOUT<br>ConnectionTimeout<br>connectTimeout | Maximum connection time     | CONNECT_TIMEOUT    | 60 second  |
| COMMAND_TIMEOUT<br>commandTimeout                      | Maximum time to perform each command | COMMAND_TIMEOUT    | 60 second  |

As an example, we can prepare the following string.
```
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;CONNECT_TIMEOUT=10000;COMMAND_TIMEOUT=50000", SERVER_HOST, SERVER_PORT);
```

### Set Error Delegator

In MachAppendWriter, you can specify a function to detect errors occurring on the MACHBASE server side during APPEND.

In .NET, this function type is specified as a Delegator Function.
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

