---
layout : post
title : '.NET CONNECTOR'
type : docs
weight: 40
---


ADO.NET 드라이버 일부 기능을 지원하는 .NET (C#) Connector 라이브러리를 제공하고 있다. 

라이브러리 위치는 $MACHBASE_HOME/lib/ 에서 DLL 형태로 제공하고 있으며, .NET 버전에 따라 다른 DLL 을 제공한다.

* .NET Framework 4.0: machNetConnector40.dll
* .NET Framework 5.0: machNetConnector50.dll

## NuGet 패키지 관리자를 이용한 설치

Machbase의 .NET Connector 5.0는 NuGet package에 등록되어 있다!
Visual Studio를 이용하면 .NET Connector을 쉽게 원격에서 가져와 사용할 수 있다.   
NuGet에서 machNetConnector5.0을 가져오는 방법은 다음과 같다.   

1. Visual Studio에서 새로운 C# .NET 프로젝트를 생성해준다.
2. 프로젝트가 생성되었으면 솔루션 탐색기에서 프로젝트 이름을 마우스 우클릭해 "NuGet 패키지 관리"를 눌러준다.
3. NuGet 패키지 관리자 창이 활성화되면 상단의 "찾아보기" 탭을 누르고, machNet을 검색한다.
4. 검색 결과가 목록에 나오는데, "machNetConnector5.0"을 선택하고, "설치"를 누른다.
5. 변경 내용 미리 보기 창이 떠도 "OK"를 눌러 설치를 계속 진행시킨다.
6. 정상적으로 설치가 완료되면 솔루션 탐색기의 "종속성 - 패키지"에서 설치된 패키지를 확인할 수 있다.
7. Program.cs에서 using Mach.Data.MachClient 구문을 입력하여 machNetConnector을 사용하면 된다.


## API Reference

> 아래 소개된 기능 외의 것은 아직 구현되어 있지 않거나, 올바르게 작동되지 않을 수 있다.<br>
미구현으로 명시된 메서드나 필드를 부르는 경우, NotImplementedException 또는 NotSupportedException 을 발생시킨다.

### MachConnection

```
public sealed class MachConnection : DbConnection
```

마크베이스와의 연결을 담당하는 클래스이다. 

DbConnection 과 같이 IDisposable 을 상속받기 때문에, Dispose() 를 통한 객체 해제나 using() 문을 이용한 객체의 자동 Dispose를 지원한다.MachConnection : DbConnection

#### 생성자

```
MachConnection(string aConnectionString)
```

Connection String 을 입력으로, MachConnection 을 생성한다.

#### 메서드

##### Open

```
void Open()
```

입력받은 Connection String 으로 실제 연결을 시도한다. 

##### Close

```
void Close()
```

연결중인 경우, 해당 연결을 종료한다.

#### 필드

| 이름 | 설명                                                                                                                        |
|--|--|
| State         | System.Data.ConnectionState 값을 나타낸다.                                                                                      |
| StatusString  | 연결된 MachCommand 로 수행하는 상태를 나타낸다.<br>Error Message 를 꾸미는 용도로 내부에서 사용되며, 작업이 시작된 상태를 나타내기 때문에 이 값으로 쿼리 상태를 체크하는 것은 적절하지 않다. |


#### Connection String
각 항목은 semicolon (;) 으로 구분되며, 다음을 사용할 수 있다.
동일 항목에 있는 여러 Keyword 는, 모두 같은 의미이다.

| Keyword                                                | 설명            | 예제                 | 기본값  |
| ------------------------------------------------------ | ------------- | ------------------ | ---- |
| SERVER                                                 | Hostname      | SERVER=192.168.0.1 |      |
| PORT<br>PORT_NO                                        | Port No.      | PORT=5656          | 5656 |
| USERID<br>USERNAME<br>USER<br>UID                      | 사용자 ID        | USER=SYS           | SYS  |
| PASSWORD<br>PWD                                        | 사용자 패스워드      | PWD=manager        |      |
| CONNECT_TIMEOUT<br>ConnectionTimeout<br>connectTimeout | 연결 최대 시간      | CONNECT_TIMEOUT    | 60초  |
| COMMAND_TIMEOUT<br>commandTimeout                      | 각 명령 수행 최대 시간 | COMMAND_TIMEOUT    | 60초  |

예제로, 아래와 같은 문자열을 준비해 둘 수 있다.
```
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;CONNECT_TIMEOUT=10000;COMMAND_TIMEOUT=50000", SERVER_HOST, SERVER_PORT);
```

### MachCommand : DbCommand
MachConnection 을 이용해 SQL 명령 또는 APPEND 를 수행하는 클래스이다.
DbCommand 와 같이 IDisposable 을 상속받기 때문에, Dispose() 를 통한 객체 해제나 using() 문을 이용한 객체의 자동 Dispose를 지원한다.

| 생성자                                              | 설명                                                                     |
| ------------------------------------------------ | ---------------------------------------------------------------------- |
| MachCommand(string aQueryString, MachConnection) | 연결할 MachConnection 객체와 함께, 수행할 쿼리를 입력해서 생성한다.                          |
| MachCommand(MachConnection)                      | 연결할 MachConnection 객체를 입력해서 생성한다. 수행할 쿼리가 없는 경우 (e.g. APPEND) 에만 사용한다. |


| 메서드                                                                                                  | 설명                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| void CreateParameter() /<br>void CreateDbParameter()                                                 | 새로운 MachParameter 를 생성한다.                                                                                                                                                                                                                                                                                                                                                                                                 |
| void Cancel()                                                                                        | (미구현)                                                                                                                                                                                                                                                                                                                                                                                                                     |
| void Prepare()                                                                                       | (미구현)                                                                                                                                                                                                                                                                                                                                                                                                                     |
| MachAppendWriter<br>AppendOpen(aTableName, aErrorCheckCount = 0, MachAppendOption = None)            | APPEND 를 시작한다. MachAppendWriter 객체를 반환한다.<br>aTableName : 대상 테이블 이름<br>aErrorCheckCount : APPEND-DATA 로 입력한 레코드 누적 개수가 일치할 때 마다, 서버로 보내 실패 여부를 확인한다.<br>말하자면, 자동 APPEND-FLUSH 지점을 정하는 셈이다.<br>MachAppendOption : 현재는 하나의 옵션만 제공하고 있다.MachAppendOption.None : 아무런 옵션도 붙지 않는다.<br>MachAppendOption.MicroSecTruncated : DateTime 객체의 값 입력 시, microsecond 까지만 표현된 값을 입력한다.<br>(DateTime 객체의 Ticks 값은 100 nanosecond 까지 표현된다.) |
| void<br>AppendData(MachAppendWriter aWriter, List<object> aDataList)                                 | MachAppendWriter 객체를 통해, 데이터가 들어있는 리스트를 받아 데이터베이스에 입력한다.<br>List 에 들어간 데이터 순서대로, 각각의 자료형은 테이블에 표현된 컬럼의 자료형과 일치해야 한다.<br>List 에 들어있는 데이터가 모자라거나 넘치면, 에러를 발생시킨다.                                                                                                                                                                                                                                                            |
| void<br>AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, DateTime aArrivalTime)  | AppendData() 에서, \_arrival_time 값을 DateTime 객체로 명시적으로 넣을 수 있는 메서드이다.                                                                                                                                                                                                                                                                                                                                                      |
| void<br>AppendDataWithTime(MachAppendWriter aWriter, List<object> aDataList, ulong aArrivalTimeLong) | AppendData() 에서, \_arrival_time 값을 ulong 객체로 명시적으로 넣을 수 있는 메서드이다.<br>ulong 값을 \_arrival_time 값으로 입력할 때 발생할 수 있는 문제는 위의 AppendData() 를 참고한다.                                                                                                                                                                                                                                                                               |
| void AppendFlush(MachAppendWriter aWriter)                                                           | AppendData() 로 입력한 데이터들을 즉시 서버로 보내, 데이터 입력을 강제한다.<br>호출 빈도가 잦을 수록, 성능은 떨어지지만 시스템 오류로 인한 데이터 유실율을 낮출 수 있고 에러 검사를 빠르게 할 수 있다.<br>호출 빈도가 뜸할 수록, 데이터 유실이 발생할 가능성이 크고 에러 검사가 지연되지만 성능은 크게 올라간다.                                                                                                                                                                                                                                |
| void AppendClose(MachAppendWriter aWriter)                                                           | APPEND 를 마친다. 내부적으로 AppendFlush() 를 호출한 뒤에 실제 프로토콜을 마친다.                                                                                                                                                                                                                                                                                                                                                                  |
| int ExecuteNonQuery()                                                                                | 입력받았던 쿼리를 수행한다. 쿼리가 영향을 미친 레코드 개수를 반환한다.<br>보통 SELECT 를 제외한 쿼리를 수행할 때 사용한다.                                                                                                                                                                                                                                                                                                                                               |
| object ExecuteScalar()                                                                               | 입력받았던 쿼리를 수행한다. 쿼리 Targetlist 의 첫 번째 값을 객체로 반환한다.<br>보통 SELECT 쿼리, 그 중에서도 결과가 1건만 나오는 SELECT (Scalar Query) 를 수행해 DbDataReader 없이 결과를 받고자 하는 경우 사용한다.                                                                                                                                                                                                                                                                     |
| DbDataReader ExecuteDbDataReader(CommandBehavior aBehavior)                                          | 입력받았던 쿼리를 수행해, 해당 쿼리의 결과를 읽어 올 수 있는 DbDataReader 를 생성해 반환한다.                                                                                                                                                                                                                                                                                                                                                              |


| 필드                                             | 설명                                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| Connection /<br>DbConnection                   | 연결된 MachConnection.                                                                  |
| ParameterCollection /<br>DbParameterCollection | Binding 목적으로 사용할 MachParameterCollection.                                            |
| CommandText                                    | 쿼리 문자열.                                                                              |
| CommandTimeout                                 | 특정 작업 수행 중, 서버로부터 응답을 기다리기까지의 시간.<br>MachConnection 에 설정된 값을 따르며, 여기서는 값 참조만 할 수 있다. |
| FetchSize                                      | 한번에 서버로부터 Fetch 할 레코드 개수. 기본값은 3000 이다.                                              |
| IsAppendOpened                                 | APPEND 작업 중인 경우, Append 가 이미 열려있는지 아닌지를 판단한다.                                        |
| CommandType                                    | (미구현)                                                                                |
| DesignTimeVisible                              | (미구현)                                                                                |
| UpdatedRowSource                               | (미구현)                                                                                |


### MachDataReader : DbDataReader
Fetch 한 결과를 읽어들이는 클래스이다. 명시적으로 생성이 불가능하고 MachCommand.ExecuteDbDataReader() 로 생성된 객체만 사용이 가능하다.

| 메서드                                 | 설명                                                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| string GetName(int ordinal)         | ordinal 번째 컬럼 이름을 반환한다.                                                                                                               |
| string GetDataTypeName(int ordinal) | ordinal 번째 컬럼의 자료형 이름을 반환한다.                                                                                                          |
| Type GetFieldType(int ordinal)      | ordinal 번째 컬럼의 자료형을 반환한다.                                                                                                             |
| int GetOrdinal(string name)         | 컬럼 이름이 위치한 인덱스를 반환한다.                                                                                                                 |
| object GetValue(int ordinal)        | 현재 위치한 레코드의 ordinal 번째 값을 반환한다.                                                                                                       |
| bool IsDBNull(int ordinal)          | 현재 위치한 레코드의 ordinal 번째 값이 NULL 인지 여부를 반환한다.                                                                                           |
| int GetValues(object[] values)      | 현재 위치한 레코드의 모든 값들을 전부 설정하고, 그 개수를 반환한다.                                                                                               |
| xxxx GetXXXX(int ordinal)           | ordinal 번째 컬럼 값을, 자료형 (XXXX) 에 맞춰 반환한다.<br>Boolean<br>Byte<br>Char<br>Int16/32/64<br>DateTime<br>String<br>Decimal<br>Double<br>Float |
| bool Read()                         | 다음 레코드를 읽는다. 결과가 존재하지 않으면 False 를 반환한다.                                                                                               |
| DataTable GetSchemaTable()          | (미지원)                                                                                                                                 |
| bool NextResult()                   | (미지원)                                                                                                                                 |


| 필드                | 설명                                                    |
| ----------------- | ----------------------------------------------------- |
| FetchSize         | 한번에 서버로부터 Fetch 할 레코드 개수. 기본값은 3000 이며 여기서는 수정할 수 없다. |
| FieldCount        | 결과 컬럼 개수.                                             |
| this[int ordinal] | object GetValue(int ordinal) 와 동일하다.                  |
| this[string name] | object GetValue(GetOrdinal(name)) 와 동일하다.             |
| HasRows           | 결과가 존재하는지 여부를 나타낸다.                                   |
| RecordsAffected   | MachCommand 의 것과 달리, 여기서는 Fetch Count 를 나타낸다.         |

### MachParameterCollection : DbParameterCollection
MachCommand 에 필요한 파라메터를 바인딩하는 클래스이다.

바인딩한 이후에 수행하게 되면, 해당 값이 같이 수행된다. 
```
Prepared Statement 개념이 구현되어 있지 않아, Binding 이후 Execute 를 해도 수행 성능은 최초 수행한 것과 같다.
```

| 메서드                                                               | 설명                                                                     |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| MachParameter<br>Add(string parameterName, DbType dbType)         | 파라메터 이름과 타입을 지정해, MachParameter 를 추가한다.<br>추가된 MachParameter 객체를 반환한다. |
| int Add(object value)                                             | 값을 추가한다. 추가된 인덱스를 반환한다.                                                |
| void AddRange(Array values)                                       | 단순 값의 배열을 모두 추가한다.                                                     |
| MachParameter<br>AddWithValue(string parameterName, object value) | 파라메터 이름과 그 값을 추가한다.<br>추가된 MachParameter 객체를 반환한다.                     |
| bool Contains(object value)                                       | 해당 값이 추가되었는지 여부를 판단한다.                                                 |
| bool Contains(string value)                                       | 해당 파라메터 이름이 추가되었는지 여부를 판단한다.                                           |
| void Clear()                                                      | 파라메터들을 모두 삭제한다.                                                        |
| int IndexOf(object value)                                         | 해당 값의 인덱스를 반환한다.                                                       |
| int IndexOf(string parameterName)                                 | 해당 파라메터 이름의 인덱스를 반환한다.                                                 |
| void Insert(int index, object value)                              | 특정 인덱스에, 해당 값을 추가한다.                                                   |
| void Remove(object value)                                         | 해당 값을 포함한 파라메터를 삭제한다.                                                  |
| void RemoveAt(int index)                                          | 인덱스에 위치한 파라메터를 삭제한다.                                                   |
| void RemoveAt(string parameterName)                               | 해당 이름을 가진 파라메터를 삭제한다.                                                  |


| 필드                | 설명                                      |
| ----------------- | --------------------------------------- |
| Count             | 파라메터 개수                                 |
| this[int index]   | index 번째의 MachParameter 를 나타낸다.         |
| this[string name] | 파라메터 이름과 일치하는 순서의 MachParameter 를 나타낸다. |


### MachParameter : DbParameter
MachCommand 에 필요한 파라메터를 각각 바인딩한 정보를 담는 클래스이다.

특별히 메서드는 지원하지 않는다.

| 필드            | 설명                                                                                |
| ------------- | --------------------------------------------------------------------------------- |
| ParameterName | 파라메터 이름                                                                           |
| Value         | 값                                                                                 |
| Size          | 값의 크기                                                                             |
| Direction     | ParameterDirection (Input / Output / InputOutput / ReturnValue)<br>기본값은 Input 이다. |
| DbType        | DB Type                                                                           |
| MachDbType    | MACHBASE DB Type<br>DB Type 과 다를 수 있다.                                            |
| IsNullable    | NULL 가능 여부                                                                        |
| HasSetDbType  | DB Type 이 지정되었는지 여부                                                               |


### MachException : DbException
마크베이스에서 나타나는 에러를 표시하는 클래스이다.

에러 메시지가 설정되어 있는데, 모든 에러 메시지는 MachErrorMsg 에서 확인할 수 있다.

| 필드                | 설명                     |
| ----------------- | ---------------------- |
| int MachErrorCode | MACHBASE 에서 제공하는 에러 코드 |


### MachAppendWriter
MachCommand 를 사용하는 별도의 클래스로 APPEND 를 지원한다.
ADO.NET 표준이 아닌, MACHBASE 의 Append Protocol 을 지원하기 위한 클래스이다.

별도의 생성자 없이 MachCommand 의 AppendOpen() 으로 생성된다.

| 메서드                                                 | 설명                                       |
| --------------------------------------------------- | ---------------------------------------- |
| void SetErrorDelegator(ErrorDelegateFuncType aFunc) | 에러가 발생했을 때 호출할 ErrorDelegateFunc 을 지정한다. |


| 필드           | 설명                                    |
| ------------ | ------------------------------------- |
| SuccessCount | 입력 성공한 레코드 개수. AppendClose() 이후 설정된다. |
| FailureCount | 입력 실패한 레코드 개수. AppendClose() 이후 설정된다. |
| Option       | AppendOpen() 때 입력받은 MachAppendOption  |


#### ErrorDelegateFuncType
```c#
public delegate void ErrorDelegateFuncType(MachAppendException e);
```
MachAppendWriter 에서, APPEND 도중 MACHBASE 서버 측에서 발생하는 Error 를 감지하기 위한 함수를 지정할 수 있다.

.NET 에서는 이 함수형을 Delegator Function 으로 지정한다.
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
MachException 과 동일하지만, 다음 점이 다르다.

* 에러 메시지가 서버 측으로부터 수신된다.
* 에러가 발생한 데이터 버퍼를 획득할 수 있다. (comma-separated) 이 데이터를 가공해 다시 APPEND 하거나 기록하는 용도로 사용할 수 있다.

해당 예외는 ErrorDelegateFunc 내부에서만 획득이 가능하다.

| 메서드            | 설명                        |
| -------------- | ------------------------- |
| GetRowBuffer() | 에러가 발생한 데이터 버퍼를 획득할 수 있다. |


### MachTransaction
지원하지 않는다.

## 샘플 코드
### 연결
MachConnection 을 만들어 Open() - Close() 하면 된다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
MachConnection sConn = new MachConnection(sConnString);
sConn.Open();
//... do something
sConn.Close();
```

using 구문을 사용하면, Connection 종료 작업인 Close() 를 호출하지 않아도 된다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
using (MachConnection sConn = new MachConnection(sConnString))
{
    sConn.Open();
    //... do something
} // you don't need to call sConn.Close();
```

### 쿼리 수행
MachCommand 를 만들어 쿼리를 수행하면 된다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
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

이 역시 using 구문을 사용하면, MachCommand 해제 작업을 곧바로 진행할 수 있다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
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

### SELECT 수행
SELECT 쿼리를 가진 MachCommand 를 실행해 MachDataReader 를 얻을 수 있다.

MachDataReader 를 통해 레코드를 하나씩 Fetch 할 수 있다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
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

### 파라메터 바인딩
MachParameterCollection 을 생성한 다음, MachCommand 에 연결해서 수행할 수 있다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
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
MachCommand 에서 AppendOpen() 을 수행하면, MachAppendWriter 객체를 얻을 수 있다.

이 객체와 MachCommand 를 이용해, 입력 레코드 1건을 리스트로 준비해 AppendData() 를 수행하면 입력이 이뤄진다.
AppendFlush() 를 하면 모든 레코드의 입력이 반영되며, AppendClose() 를 통해 Append 전체 과정을 종료할 수 있다.
```c#
String sConnString = String.Format("SERVER={0};PORT_NO={1};UID=;PWD=MANAGER;", SERVER_HOST, SERVER_PORT);
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
