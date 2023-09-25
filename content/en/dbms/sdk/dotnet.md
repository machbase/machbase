---
title : '.NET Connector'
type : docs
weight: 40
---


The .NET (C #) Connector library that supports some features of the ADO.NET driver is provided.

The library location is  $MACHBASE_HOME/lib/ provided as a DLL type. It provides different DLLs depending on the .NET version.

* .NET Framework 4.0: machNetConnector.dll
* .NET 5.0: machNetConnector5.0.dll

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


## Class

> Features not listed below may not be implemented yet or may not work correctly.<br>
If you call a method or field that is not a named instance, it generates NotImplementedException or a NotSupportedException.

### MachConnection : DbConnection
This class is responsible for linking with Machbase. 

Because it inherits IDisposable like DbConnection, it supports disassociation through Dispose () or automatic disposition of object using using () statement.

|Constructor|Description|
|--|--|
|MachConnection(string aConnectionString)|Creates a MachConnection with a Connection String as input.|

|Method|Description|
|--|--|
|Open()|Attempts to connect to the connection string.|
|Close()|Closes the connection when connecting.|
|BeginDbTransaction(IsolationLevel isolationLevel)|<span style="color: #4f0111;">(Not yet implemented) MACHBASE does not support this object because there is no special transaction.</span>|
|CreateDbCommand()|<span style="color: #4f0111;">(Not yet implemented) Explicitly induces MachCommands to be created</span>|
|ChangeDatabase(string databaseName)|<span style="color: #4f0111;">(Not yet implemented) MACHBASE has no DATABASE classification.</span>|

|Field|Description|
|--|--|
|State|Represents a System.Data.ConnectionState value.|
|StatusString|Indicates the state to be performed by the connected MachCommand.<br><br>This is used internally to decorate the Error Message and it is not appropriate to check the status of the query with this value because it indicates the state in which the operation started.|
|Database|<span style="color: #4f0111;">(Not yet implemented)<span>|
|DataSource|<span style="color: #4f0111;">(Not yet implemented)<span>|
|ServerVersion|<span style="color: #4f0111;">(Not yet implemented)<span>|

#### Connection String
Each item is separated by a semicolon (;). <br>
Many of the keywords in the same section have the same meaning.<br>
<table>
 <thead>
   <tr>
     <th>Keyword</th>
     <th>Description</th>
     <th>Example</th>
     <th>Default value</th>
   </tr>
 </thead>
 <tbody>
   <tr>
     <td>DSN<br>SERVER<br>HOST</td>
     <td>Hostname</td>
     <td>DSN=localhost<br>SERVER=192.168.0.1</td>
     <td></td>
   </tr>
   <tr>
     <td>PORT<br>PORT_NO</td>
     <td>Port No.</td>
     <td>PORT=5656</td>
     <td>5656</td>
   </tr>
   <tr>
     <td>USERID<br>USERNAME<br>USER<br>UID</td>
     <td>User ID</td>
     <td>USER=SYS</td>
     <td>SYS</td>
   </tr>
   <tr>
     <td>PASSWORD<br>PWD</td>
     <td>User password</td>
     <td>PWD=manager</td>
     <td></td>
   </tr>
   <tr>
     <td>CONNECT_TIMEOUT<br>ConnectionTimeout<br>connectTimeout</td>
     <td>Maximum connection time</td>
     <td>CONNECT_TIMEOUT</td>
     <td>60 second</td>
   </tr>
   <tr>
     <td>COMMAND_TIMEOUT<br>commandTimeout</td>
     <td>Maximum time to perform each command</td>
     <td>COMMAND_TIMEOUT</td>
     <td>60 second</td>
   </tr>
 </tbody>
</table>

As an example, we can prepare the following string.
```
String sConnString = String.Format("DSN={0};PORT_NO={1};UID=;PWD=MANAGER;CONNECT_TIMEOUT=10000;COMMAND_TIMEOUT=50000", SERVER_HOST, SERVER_PORT);
```

### MachCommand : DbCommand
A class that performs **SQL commands or APPEND** using MachConnection. 
Since it inherits IDisposable like DbCommand, it supports object disposal through Dispose () or automatic disposal of object using using () statement

<table>
  <thead>
    <tr>
      <th>Constructor</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MachCommand(string aQueryString, MachConnection)</td>
      <td>Creates by typing the query to be executed along with the MachConnection object to be connected.</td>
    </tr>
    <tr>
      <td>MachCommand(MachConnection)</td>
      <td>Creates a MachConnection object to connect to. Use only if there is no query to perform (eg APPEND).</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>void CreateParameter() /<br>void CreateDbParameter()</td>
      <td>Creates a new MachParameter.</td>
    </tr>
    <tr>
      <td>void Cancel()</td>
      <td><span style="color: #4f0111;">(Not yet implemented)</span></td>
    </tr>
    <tr>
      <td>void Prepare()</td>
      <td><span style="color: #4f0111;">(Not yet implemented)</span></td>
    </tr>
    <tr>
      <td>MachAppendWriter<br>AppendOpen(aTableName, aErrorCheckCount = 0, MachAppendOption = None)</td>
      <td>
        Starts APPEND. Returns a MachAppendWriter object.<br><br>
        - aTableName: Target table name<br>
        - aErrorCheckCount: Each time the cumulative number of records entered by APPEND-DATA matches, it is checked whether it is sent to the server or not.<br>
          In other words, you are setting the automatic APPEND-FLUSH point.<br>
        - MachAppendOption: Currently only one option is provided.<br>
          - MachAppendOption.None: No options are attached.<br>
          - MachAppendOption.MicroSecTruncated: When inputting the value of a DateTime object, enter the value expressed only up to microsecond.<br>
          (The Ticks value of a DateTime object is expressed up to 100 nanoseconds.)
      </td>
    </tr>
    <tr>
      <td>void<br>AppendData(MachAppendWriter aWriter, List&lt;object&gt; aDataList)</td>
      <td>
        Through the MachAppendWriter object, it takes a list containing the data and enters it into the database.<br>
        - In the order of the data in the List, each datatype must match the datatype of the column represented in the table.<br>
        - If the data in the List is insufficient or overflows, an error occurs.<br><br>
        <blockquote> 
          <p>When representing a time value with a ulong object, simply do not enter the Tick value of the DateTime object. <br><br>In that value, you must enter a <u>value that excludes the DateTime Tick value that represents 1970-01-01</u>.</p>
        </blockquote>
      </td>
    </tr>
    <tr>
      <td>void<br>AppendDataWithTime(MachAppendWriter aWriter, List&lt;object&gt; aDataList, DateTime aArrivalTime)</td>
      <td>Method that explicitly puts an _arrival_time value into a DateTime object in AppendData().</td>
    </tr>
    <tr>
      <td>void<br>AppendDataWithTime(MachAppendWriter aWriter, List&lt;object&gt; aDataList, ulong aArrivalTimeLong)</td>
      <td>Method that can explicitly put _arrival_time value into a ulong object in AppendData().<br><br>Refer to AppendData() above for problems that may occur when typing a ulong value as an _arrival_time value.</td>
    </tr>
    <tr>
      <td>void AppendFlush(MachAppendWriter aWriter)</td>
      <td>
        The data entered by AppendData() is immediately sent to the server to force data insert.<br><br>
        The more frequently the call is made, the lower the data loss rate due to the system error and the faster the error check, although the performance is lowered.<br>
        The less frequently the call is made, the more likely the data loss will occur and the error checking will be delayed, but the performance will increase significantly.
      </td>
    </tr>
    <tr>
      <td>void AppendClose(MachAppendWriter aWriter)</td>
      <td>Closes APPEND. Internally, after calling AppendFlush(), the actual protocol is internally finished.</td>
    </tr>
    <tr>
      <td>int ExecuteNonQuery()</td>
      <td>Performs the input query. Returns the number of records affected by the query.<br><br>
        It is usually used when performing queries except SELECT.
      </td>
    </tr>
    <tr>
      <td>object ExecuteScalar()</td>
      <td>Performs the input query. Returns the first value of the query targetlist as an object.<br><br>
        It is usually used when you want to perform a SELECT query, especially a SELECT (Scalar Query) with only one result, and get the result without a DbDataReader.
      </td>
    </tr>
    <tr>
      <td>DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)</td>
      <td>Executes the input query, generates a DbDataReader that can read the result of the query, and returns it.</td>
    </tr>
  </tbody>
</table>

|Field|Description|
|--|--|
|Connection / DbConnection|Connected MachConnection.|
|ParameterCollection / DbParameterCollection|The MachParameterCollection to use for the Binding purpose.|
|CommandText|Query string.|
|CommandTimeout|The amount of time it takes to perform a particular task, waiting for a response from the server.<br>It follows the values ​​set in MachConnection, where you can only reference values.|
|FetchSize|The number of records to fetch from the server at one time . The default value is 3000.|
|IsAppendOpened|Determines if Append is already open when APPEND is at work|
|CommandType|<span style="color: #4f0111;">(Not yet implemented)</span>|
|DesignTimeVisible|<span style="color: #4f0111;">(Not yet implemented)</span>|
|UpdatedRowSource|<span style="color: #4f0111;">(Not yet implemented)</span>|

### MachDataReader : DbDataReader

This is a class that reads fetch results. Only objects created with MachCommand.ExecuteDbDataReader () that can not be explicitly created are available.

|Method|Description|
|--|--|
|string GetName(int ordinal)|Returns the ordinal column name.|
|string GetDataTypeName(int ordinal)|Returns the datatype name of the ordinal column.|
|Type GetFieldType(int ordinal)|Returns the datatype of the ordinal column.|
|int GetOrdinal(string name)|Returns the index at which the column name is located.|
|object GetValue(int ordinal)|Returns the ordinal value of the current record.|
|bool IsDBNull(int ordinal)|Returns whether the ordinal value of the current record is NULL.|
|int GetValues(object[] values)|Sets all the values ​​of the current record and returns the number.|
|xxxx GetXXXX(int ordinal)|Returns the ordinal column value according to the datatype (XXXX).<br> - Boolean<br> - Byte<br> - Char<br> - Int16 / 32/64<br> - DateTime<br> - String<br> - Decimal<br> - Double<br> - Float|
|bool Read()|Reads the next record. Returns False if the result does not exist.|
|DataTable GetSchemaTable()|<span style="color: #4f0111;">(Not supported)</span>|
|bool NextResult()|<span style="color: #4f0111;">(Not supported)</span>|

|Field|Description|
|--|--|
|FetchSize|The number of records to fetch from the server at one time. The default is 3000, which can not be modified here.|
|FieldCount|Number of result columns.|
|this[int ordinal]|Equivalent to object GetValue (int ordinal).|
|this[string name]|Equivalent to object GetValue(GetOrdinal(name).|
|HasRows|Indicates whether the result is present.|
|RecordsAffected|Unlike MachCommand, here, it represents Fetch Count.|

### MachParameterCollection : DbParameterCollection

This is a class that binds parameters needed by MachCommand.

If you do this after binding, the values ​​are done together. 
```
Since the concept of Prepared Statement is not implemented, execution performance after Binding is the same as the performance performed first.
```

|Method|Description|
|--|--|
|MachParameter<br>Add(string parameterName, DbType dbType)|Adds the MachParameter, specifying the parameter name and type. <br><br>Returns the added MachParameter object.|
|int Add(object value)|Adds a value. Returns the index added.|
|void AddRange(Array values)|Adds an array of simple values.|
|MachParameter<br>AddWithValue(string parameterName, object value)|Adds the parameter name and its value. <br><br>Returns the added MachParameter object.|
|bool Contains(object value)|Determines whether or not the corresponding value is added.|
|bool Contains(string value)|Determines whether or not the corresponding parameter name is added.|
|void Clear()|Deletes all parameters.|
|int IndexOf(object value)|Returns the index of the corresponding value.|
|int IndexOf(string parameterName)|Returns the index of the corresponding parameter name.|
|void Insert(int index, object value)|Adds the value to a specific index.|
|void Remove(object value)|Deletes the parameter including the value.|
|void RemoveAt(int index)|Deletes the parameter located at the index.|
|void RemoveAt(string parameterName)|Deletes the parameter with that name.|

|Field|Description|
|--|--|
|Count|Number of parameters|
|this[int index]|Indicates the MachParameter at index.|
|this[string name]|Indicates the MachParameter of the order in which the parameter names match.|

### MachParameter : DbParameter

This is a class that contains the information that binds the necessary parameters to each MachCommand.

No special methods are supported.

|Field|Description|
|--|--|
|ParameterName|Parameter name|
|Value|Value|
|Size|Value size|
|Direction|ParameterDirection (Input / Output / InputOutput / ReturnValue)<br><br>The default value is Input.|
|DbType|DB Type|
|MachDbType|MACHBASE DB Type<br><br>May differ from DB Type.|
|IsNullable|Whether nullable|
|HasSetDbType|Whether DB Type is specified|

### MachException : DbException

This is a class that displays errors that appear in Machbase.

An error message is set, and all error messages  can be found in  MachErrorMsg .

|Field|Description|
|--|--|
|int MachErrorCode|Error code provided by MACHBASE|

### MachAppendWriter
APPEND is supported as a separate class using MachCommand.
This is a class to support MACHBASE Append Protocol, not ADO.NET standard.

It is created with MachCommand's AppendOpen () without a separate constructor.

|Method|Description|
|--|--|
|void SetErrorDelegator(ErrorDelegateFuncType aFunc)|Specifies the ErrorDelegateFunc to call when an error occurs.|

|Field|Description|
|--|--|
|SuccessCount|Number of successful records. Is set after AppendClose().|
|FailureCount|The number of records that failed input. Set after AppendClose ().|
|Option|MachAppendOption received input during AppendOpen()|

### ErrorDelegateFuncType
```c#
public delegate void ErrorDelegateFuncType(MachAppendException e);
```
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

### MachAppendException : MachException
Same as MachException, except that:

* An error message is received from the server side.
* A data buffer in which an error has occurred can be obtained. (comma-separated) can be used to process and re-append or record data.

The exception is only available within the ErrorDelegateFunc.

|Method|Description|
|--|--|
|GetRowBuffer()|A data buffer in which an error has occurred can be obtained.|

### MachTransaction
Not supported.


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
