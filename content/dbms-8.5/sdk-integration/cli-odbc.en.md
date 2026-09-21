---
title : 'CLI/ODBC'
type : docs
weight: 10
---

CLI is a software development standard defined in [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003.

The CLI defines functions and specifications for how to pass SQL to the database and how to receive and analyze the results. The CLI was developed in the early 1990s exclusively for the C and COBOL languages, and its specification has been maintained to date.

The most widely known standard interface to date is ODBC (Open Database Connectivity), which provides a way for a client program to access a database regardless of the type of database. The current ODBC API version is 3.52 and is defined in the ISO and X/Open standards.


## Standard CLI Functions

See the following links for usage of the standard functions.

* [Wikipedia](https://en.wikipedia.org/wiki/Call_Level_Interface)
* [Open Group Document](https://www2.opengroup.org/ogsys/catalog/c451)

You can refer to the following functions.

| | | | |
|--|--|--|--|
|SQLAllocConnect|SQLDisconnect|SQLGetDescField|SQLPrepare|
|SQLAllocEnv|SQLDriverConnect|SQLGetDescRec|SQLPrimaryKeys|
|SQLAllocHandle|SQLExecDirect|SQLGetDiagRec|SQLStatistics|
|SQLAllocStmt|SQLExecute|SQLGetEnvAttr|SQLRowCount|
|SQLBindCol|SQLFetch|SQLGetFunctions|SQLSetConnectAttr|
|SQLBindParameter+|SQLFreeConnect|SQLGetInfo|SQLSetDescField|
|SQLColAttribute|SQLFreeEnv|SQLGetStmtAttr|SQLSetDescRec|
|SQLColumns|SQLFreeHandle|SQLGetTypeInfo|SQLSetEnvAttr|
|SQLConnect|SQLFreeStmt|SQLNativeSQL|SQLSetStmtAttr|
|SQLCopyDesc|SQLGetConnectAttr|SQLNumParams|SQLStatistics|
|SQLDescribeCol|SQLGetData|SQLNumResultCols|SQLTables|


## Connection String for Connecting

To connect through the CLI, you need to create a connection string. The items are as follows.

|Connection String Item Name|Item Description|
|--|--|
|DSN|Specifies the data source name.<br>ODBC specifies the section name of the file containing the resource, and CLI specifies the server name or IP address.|
|DBNAME|Specifies the Machbase DB name.|
|SERVER|Indicates the host name or IP address of the server where Machbase is located.|
|NLS_USE|Sets the language type used by both sides (currently unused, kept for future expansion).|
|UID|User ID|
|PWD|User password|
|PORT_NO|Port number to connect to|
|PORT_DIR|Specifies the file path used when connecting through a Unix domain socket on Unix.<br>(Specify it only when it was changed on the server; by default, it works without it.)|
|CONNTYPE|Specifies the connection method between the client and the server.<br><br>1: Connect with TCP/IP INET<br>2: Connect with Unix Domain|
|COMPRESS|Indicates whether to compress the Append protocol.<br><br>If this value is 0, data is transmitted without compression.<br>If this value is greater than 0, an Append record is compressed only when it is larger than this value.<br><br>Ex) COMPRESS=512<br>Only records larger than 512 are compressed.<br><br>For remote connections, compression improves transmission performance.|
|SHOW_HIDDEN_COLS|Decides whether to show the hidden column (`_arrival_time`) when running `select *`.<br><br>If it is 0, the column is not shown. If it is 1, the column is output.|
|CONNECTION_TIMEOUT|Sets how long to wait on the first connection.<br><br>The default is 30 seconds.<br>Set this value higher if the server may take longer than 30 seconds to respond to the first connection.<br><br>A CONNECTION_TIMEOUT of 0 means no timeout limit; the client waits indefinitely even when the connection fails, so avoid it where possible.|
|SOCKET_TIMEOUT|The timeout that occurs when protocol I/O takes too long.<br><br>The client checks it, waits, and then disconnects.<br><br>Same as the Read Timeout of ORACLE. (MYSQL and MSSQL use the same name, SOCKET_TIMEOUT.)<br><br>Set SOCKET_TIMEOUT=NN (seconds) in the connection string. The default is 30 minutes (1800).|
|ALTERNATIVE_SERVERS|When using the cluster version, this setting holds the information of additional brokers.<br><br>When multiple brokers are registered, even if the connected broker goes down, the client connects to another broker and continues inputting data.<br><br>Multiple brokers can be registered; write the values of <server address>:<server port> separated by commas.<br><br>ex) ALTERNATIVE_SERVERS=192.168.0.10:20320,192.168.0.11:20320;|
|AUTH_MODE|Authentication mode. Use `PASSWORD` for password authentication or `CHALLENGE` for private-key challenge authentication. If `AUTH_KEY_FILE` is set and `AUTH_MODE` is omitted, the CLI treats the connection as `CHALLENGE`.|
|AUTH_SIG_SCHEME|Signature scheme for `AUTH_MODE=CHALLENGE`: `ECDSA`, `RSA_PKCS1_V15`, or `RSA_PSS`. If omitted, the client attempts to infer the default scheme from the key file.|
|AUTH_KEY_FILE|Local PEM private key file path for `AUTH_MODE=CHALLENGE`. The key file is required for challenge authentication.|

An example of a CLI connection is as follows.

```c
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
 
if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```


## Extension CLI Function (APPEND)

The CLI extension functions implement the Append protocol, which is provided to input data into the Machbase server at high speed.

They consist of four kinds of functions: channel open, data input to the channel, channel flush, and channel close.

### Understanding Append Protocol

The Append protocol provided by Machbase works asynchronously. Asynchronous means that the response to a job the client requested from the server is not fully synchronized with the request, but arrives when an arbitrary event occurs. That is, even if a client has performed an append, it cannot immediately get or verify the result of that execution; it can check the result at the point when the server is ready. For this reason, developers who build applications with the Append protocol should understand the following internal behavior. The following sections describe when and how a client detects asynchronous errors that occur in the server and returns them to the user.

### Append Data Transfer

In a typical call such as SQLExecute() or SQLExecDirect(), Machbase uses a synchronous scheme that returns the result to the client immediately. However, SQLAppendDataV2() does not send a request immediately after user data is entered. Instead, it waits until the client communication buffer is full and then sends the data to the server all at once. This design assumes that a client using Append inputs tens to hundreds of thousands of records per second, so it uses buffering for high-speed data transmission. For this reason, if the user wants to send the contents of the buffer at an arbitrary time, the user can call SQLAppendFlush() to input the data explicitly.

### Append Data Error Check

As mentioned earlier, the Append protocol is buffered and operates asynchronously. In particular, the server sends no response when no error occurs and the client detects an error only when one occurs, so it is very important to understand when and how an error is detected. In addition, because detecting an error is relatively expensive, checking on every record input would be very inefficient, so Machbase currently detects errors explicitly only in the following cases. When an error is detected, the error callback function set by the user is called every time.

1. After the transmit buffer is full and the data has been explicitly sent to the server
2. After SQLAppendFlush() explicitly sends data to the server
3. Just before closing, inside SQLAppendClose()

In other words, errors are basically detected only in the above three cases, which is designed to minimize I/O.

### Additional Options for Checking Server Errors

The default error detection, set up for maximum performance, can be made more frequent if the user wants. This is done by adjusting aErrorCheckCount, the last argument of the SQLAppendOpen() function. When this value is 0, no additional check is performed and the default behavior applies. If this value is greater than 0, errors are explicitly checked every time SQLAppendData() has been called that many times. For example, if this value is 10, you pay the cost of an error check every 10 appends. Therefore, a small value uses a lot of system resources for error detection, so adjust it to an appropriate number.

### Leaving Trace Log When Server Error Occurs

If you want to leave a trace log for the append data that caused an error, set the server property DUMP_APPEND_ERROR to 1. With this setting, the description of the record that caused the error is written to the mach.trc file. However, if errors are excessive, system resource usage increases sharply and can degrade the overall performance of Machbase, so use it with care.

### APPEND Function Description

#### SQLAppendOpen

```c
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount );
```

This function opens a channel for the target table. The channel stays open until you close it.

A maximum of 1024 statements can be set for one connection. You can use SQLAppendOpen for each statement.

1. aStatementHandle: The handle of the statement on which Append is performed.
2. aTableName: The name of the table to which Append is performed.
3. aErrorCheckCount: Decides after how many input records the server is checked for errors. If this value is 0, no extra error check is performed.

#### SQLAppendData (deprecated)

```c
SQLRETURN  SQLAppendData(SQLHSTMT StatementHandle, void *aData[]);
```

This function inputs data into the channel.

* aData is an array containing pointers to the data to be input. The number of array elements must match the number of columns of the table specified at open.
* The return value can be SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, or SQL_ERROR. In particular, if SQL_SUCCESS_WITH_INFO is returned, an input column may have been truncated because it was too long, so check the result again.

**Configuration According to Data Type**

Numeric and character types

* Types such as float, double, short, int, long long, and char * work with a pointer to their value.

Address type

* IPv4 is passed as a 5-byte unsigned char array.
* The first byte is set to 4, and the next 4 bytes are set to the consecutive address values.
* For example, 127.0.0.1 is entered as the 5-byte array **0x04, 0x7f, 0x00, 0x00, 0x01** in this order.

```c
// For tables with four column information (short (16), int (32), long (64), varchar)
 
testAppendIPFunc()
{
   short val1 = 0;
   int   val2 = 1;
   long long  val3 = 2;  
   char *val4 = "my string";
   void *valueArray[4];
 
   valueArray[0] = (void *)&val1;
   valueArray[1] = (void *)&val2;
   valueArray[2] = (void *)&val3;
   valueArray[3] = (void *)val4;
 
   SQLAppendData(aStmt, valueArray);
}
```

**Configuration According to Data Type**

datetime type

* Machbase internally keeps time with nanosecond resolution, so a time set on the client must be converted, and it is expressed as a 64-bit unsigned integer. For proper conversion, convert the time to seconds with the UNIX library function mktime and then add the sub-second values.
* ※ Machbase time = (total time (seconds) since January 1, 1970) * 1,000,000,000 + milli-second * 1,000,000 + micro-second * 1000 + nano-second;

```c
// Code for a date string in the form "Year-Month-Day Hour:Minute:Second Milli:Micro:Nano"
 
testAppendDateStrFunc(char *aDateString)
{
    int yy, int mm, int dd, int hh, int mi, int ss;
    unsigned long t1;
    void *valueArray[5];
    sscanf(aDateString, "%d-%d-%d %d:%d:%d %d:%d:%d",
        &yy, &mm, &dd, &hh, &mi, &ss, &mmm, &uuu, &nnn);
    sTm.tm_year = yy - 1900;
    sTm.tm_mon = mm - 1;
    sTm.tm_mday = dd;
    sTm.tm_hour = hh;
    sTm.tm_min = mi;
    sTm.tm_sec = ss;
    t1 = mktime(&sTm);
    t1 = t1 * 1000000000L;
    t1 = t1 + (mmm*1000000L) + (uuu*1000) + nnn;
 
    valueArray[4] = &t1;
    SQLAppendData(aStmt, valueArray);
}
```

#### SQLAppendDataByTime(deprecated)

```c
SQLRETURN  SQLAppendDataByTime(SQLHSTMT StatementHandle, SQLBIGINT aTime, void *aData[]);
```

This function inputs data into the channel, and it lets you set the `_arrival_time` value stored in the DB to a specific time instead of the current time.

For example, use it when you want to enter the dates in a log file from a month ago as they were at that time.

* aTime is the time value set to `_arrival_time`.
* aData is an array containing pointers to the data to be input.
* The number of array elements must match the number of columns of the table specified at open.

For the rest, refer to the SQLAppendData() function.

```c
// For tables with four column information (short (16), int (32), long (64), varchar)
 
testAppendFuncWithTime()
{
   long long sTime = 1;
   short val1 = 0;
   int   val2 = 1;
   long long  val3 = 2;  
   char *val4 = "my string";
   void *valueArray[4];
 
   valueArray[0] = (void *)&val1;
   valueArray[1] = (void *)&val2;
   valueArray[2] = (void *)&val3;
   valueArray[3] = (void *)val4;
 
   SQLAppendDataByTime(aStmt, sTime, valueArray);
}
```

#### SQLAppendDataV2

```c
SQLRETURN  SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

This Append function was introduced in Machbase 2.0 and greatly improves the input method that was inconvenient in the earlier function.

In particular, the TEXT and BINARY types introduced in 2.0 can be input only with SQLAppendDataV2().

* NULL can be input for each type
* The string length can be specified when inputting VARCHAR
* IPv4 and IPv6 can be input as binary or string data
* The data length can be specified for the TEXT and BINARY types

The function arguments are as follows.

* aData is a pointer to an array of SQL_APPEND_PARAM arguments. The number of array elements must match the number of columns of the table specified at open.
* The return value can be SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, or SQL_ERROR. In particular, if SQL_SUCCESS_WITH_INFO is returned, an input column may have been truncated because it was too long, so check the result again.

Below is the definition of SQL_APPEND_PARAM used in V2, which is included in machbase_sqlcli.h.

```c
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
 
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
 
/* Date time*/
typedef struct machbaseAppendDateTimeStruct
{
    long long       mTime;
#if defined(SUPPORT_STRUCT_TM)
    struct tm       mTM;
#endif
    char           *mDateStr;
    char           *mFormatStr;
} machbaseAppendDateTimeStruct;
 
typedef union machbaseAppendParam
{
    short                        mShort;
    unsigned short               mUShort;
    int                          mInteger;
    unsigned int                 mUInteger;
    long long                    mLong;
    unsigned long long           mULong;
    float                        mFloat;
    double                       mDouble;
    machbaseAppendIPStruct       mIP;
    machbaseAppendVarStruct      mVar;     /* for all varying type */
    machbaseAppendVarStruct      mVarchar; /* alias */
    machbaseAppendVarStruct      mText;    /* alias */
    machbaseAppendVarStruct      mJson;    /* alias */
    machbaseAppendVarStruct      mBinary;  /* binary */
    machbaseAppendVarStruct      mBlob;    /* reserved alias */
    machbaseAppendVarStruct      mClob;    /* reserved alias */
    machbaseAppendDateTimeStruct mDateTime;
} machbaseAppendParam;
 
#define SQL_APPEND_PARAM machbaseAppendParam
```

As shown above, one argument is held internally in the union machbaseAppendParam. For each data type, the length and value of the data or string can be entered explicitly. Examples of actual use are as follows.

**Fixed-Length Numeric Type Input**

Fixed-length numeric types are short, ushort, integer, uinteger, long, ulong, float, and double. These types can be entered by directly assigning a value to the corresponding member of SQL_APPEND_PARAM.

|Database Type|NULL Macro|SQL_APPEND_PARAM Member|
|--|--|--|
|SHORT|SQL_APPEND_SHORT_NULL|mShort|
|USHORT|SQL_APPEND_USHORT_NULL|mUShort|
|INTEGER|SQL_APPEND_INTEGER_NULL|mInteger|
|UINTEGER|SQL_APPEND_UINTEGER_NULL|mUInteger|
|LONG|SQL_APPEND_LONG_NULL|mLong|
|ULONG|SQL_APPEND_ULONG_NULL|mULong|
|FLOAT|SQL_APPEND_FLOAT_NULL|mFloat|
|DOUBLE|SQL_APPEND_DOUBLE_NULL|mDouble|

The following is an example of entering actual values.

```c
// Assume that the Table Schema consists of eight columns, SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, and DOUBLE, respectively.
 
void testAppendExampleFunc()
{
    SQL_APPEND_PARAM sParam[8];
 
    /* fixed column */
    sParam[0].mShort = SQL_APPEND_SHORT_NULL;
    sParam[1].mUShort = SQL_APPEND_USHORT_NULL;
    sParam[2].mInteger = SQL_APPEND_INTEGER_NULL;
    sParam[3].mUInteger = SQL_APPEND_UINTEGER_NULL;
    sParam[4].mLong = SQL_APPEND_LONG_NULL;
    sParam[5].mULong = SQL_APPEND_ULONG_NULL;
    sParam[6].mFloat = SQL_APPEND_FLOAT_NULL;
    sParam[7].mDouble = SQL_APPEND_DOUBLE_NULL;
 
    SQLAppendDataV2(Stmt, sParam);
 
    /* FIXED COLUMN Value */
    sParam[0].mShort = 2;
    sParam[1].mUShort = 3;
    sParam[2].mInteger = 4;
    sParam[3].mUInteger = 5;
    sParam[4].mLong = 6;
    sParam[5].mULong = 7;
    sParam[6].mFloat = 8.4;
    sParam[7].mDouble = 10.9;
 
    SQLAppendDataV2(Stmt, sParam);
}
```

**Date Type Input**

Below is an example of inputting DATETIME data. Several macros are available for convenience.

These operate on the mDateTime member of SQL_APPEND_PARAM. The following macros specify a date by setting mTime, a 64-bit integer in the mDateTime structure.

```c
typedef struct machbaseAppendDateTimeStruct
{
    long long       mTime;
#if defined(SUPPORT_STRUCT_TM)
    struct tm       mTM;
#endif
    char           *mDateStr;
    char           *mFormatStr;
} machbaseAppendDateTimeStruct;
```

|Macro|Description|
|--|--|
|SQL_APPEND_DATETIME_NOW|Enters the current client time.|
|SQL_APPEND_DATETIME_STRUCT_TM|Sets a value in mTM, the struct tm structure of mDateTime, and enters that value into the database.|
|SQL_APPEND_DATETIME_STRING|Sets a string value in mDateTime and enters it into the database.<br><br>mDateStr: the actual date string value<br>mFormatStr: the format string for the date string|
|SQL_APPEND_DATETIME_NULL|Enters NULL into the date column.|
|Any 64-bit Value|This value is entered as the actual datetime.<br><br>It is an integer representing the time elapsed in nanoseconds since January 1, 1970.<br>For example, if this value is 1 billion (1,000,000,000), it represents 00:00:01 on January 1, 1970 (GMT).|

The following example enters an actual value for each case, assuming that there is one DATETIME column.

```c
void testAppendDateTimeFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL Insert */
    sParam[0].mDateTime.mTime   = SQL_APPEND_DATETIME_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* Current Time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(Stmt, sParam);
 
    /* nano second since 1970/01/01 */
    sParam[0].mDateTime.mTime      = 1234;
    SQLAppendDataV2(Stmt, sParam);
 
    /* String format time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[0].mDateTime.mDateStr   = "23/May/2014:17:41:28";
    sParam[0].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(Stmt, sParam);
 
    /* struct tm based time */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[0].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[0].mDateTime.mTM.tm_mon  =  11;
    sParam[0].mDateTime.mTM.tm_mday  = 31;
    SQLAppendDataV2(Stmt, sParam);
}
```

**Internet Address Type Input**

The following is an example of inputting IPv4 and IPv6 data. Several macros are also available for convenience. They operate on the mLength member of SQL_APPEND_PARAM.

```c
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
```

|Macro (set on mLength)|Description|
|--|--|
|SQL_APPEND_IP_NULL|Enters a NULL value in the corresponding column|
|SQL_APPEND_IP_IPV4|mAddr has IPv4|
|SQL_APPEND_IP_IPV6|mAddr has IPv6|
|SQL_APPEND_IP_STRING|mAddrString has an address string.|

The following is an example of entering actual values for each case.

```c
void testAppendIPFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* Direct array access */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    sParam[0].mIP.mAddr[0] = 127;
    sParam[0].mIP.mAddr[1] = 0;
    sParam[0].mIP.mAddr[2] = 0;
    sParam[0].mIP.mAddr[3] = 1;
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4 from binary */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
    *(in_addr_t *)(sParam[0].mIP.mAddr) = inet_addr("192.168.0.1");
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4 : ipv4 from string */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "203.212.222.111";
    SQLAppendDataV2(Stmt, sParam);
 
    /* IPv4 : ipv4 from invalid string */
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "ip address is not valid";
    SQLAppendDataV2(Stmt, sParam);                           // invalid IP value
 
    /* IPv6 : ipv6 from binary bytes */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV6;
    sParam[0].mIP.mAddr[0]  = 127;
    sParam[0].mIP.mAddr[1]  = 127;
    sParam[0].mIP.mAddr[2]  = 127;
    sParam[0].mIP.mAddr[3]  = 127;
    sParam[0].mIP.mAddr[4]  = 127;
    sParam[0].mIP.mAddr[5]  = 127;
    sParam[0].mIP.mAddr[6]  = 127;
    sParam[0].mIP.mAddr[7]  = 127;
    sParam[0].mIP.mAddr[8]  = 127;
    sParam[0].mIP.mAddr[9]  = 127;
    sParam[0].mIP.mAddr[10] = 127;
    sParam[0].mIP.mAddr[11] = 127;
    sParam[0].mIP.mAddr[12] = 127;
    sParam[0].mIP.mAddr[13] = 127;
    sParam[0].mIP.mAddr[14] = 127;
    sParam[0].mIP.mAddr[15] = 127;
    SQLAppendDataV2(Stmt, sParam);
 
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "::127.0.0.1";
    SQLAppendDataV2(Stmt, sParam);
 
    sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = "FFFF:FFFF:1111:2222:3333:4444:7733:2123";
    SQLAppendDataV2(Stmt, sParam);
}
```

When an IP value is entered as a string, SQLAppendDataV2() changes mLength to 4 or 6 according to the address type. Therefore, when you input values in a loop, set mLength to SQL_APPEND_IP_STRING before every SQLAppendDataV2() call.

**Variable Data Types (Character and Binary Data) Input**

Variable data types include VARCHAR, TEXT, BLOB, and CLOB. The earlier function supported only VARCHAR and gave the user no way to enter the string length, so the length had to be obtained with strlen() each time. Since V2, the user can specify the length of variable data directly, so if the length is known in advance, data can be input faster. Internally, variable data types share one structure, but for convenience separate members are provided for each data type.

```c
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
```

When inputting variable data, set the data length in mLength and the raw data pointer in mData. If mLength is larger than the length defined in the schema, the data is truncated automatically. In that case, SQLAppendDataV2() returns SQL_SUCCESS_WITH_INFO and also fills the internal structure with a related warning message. To see this warning message, use the SQLError() function.

|Database Type|NULL Macro|SQL_APPEND_PARAM Member<br>(mVar is acceptable)|
|--|--|--|
|VARCHAR|SQL_APPEND_VARCHAR_NULL|mVarchar|
|TEXT|SQL_APPEND_TEXT_NULL|mText|
|JSON|SQL_APPEND_JSON_NULL|mJson|
|BINARY|SQL_APPEND_BINARY_NULL|mBinary|
|BLOB|SQL_APPEND_BLOB_NULL|mBlob|
|CLOB|SQL_APPEND_CLOB_NULL|mClob|

The following is an example of entering actual values for each case. Assume that there is one VARCHAR column.

```sql
CREATE TABLE ttt (name VARCHAR(10));
```

```c
void testAppendVarcharFunc()
{
    SQL_APPEND_PARAM sParam[1];
 
    /*  VARCHAR : NULL */
    sParam[0].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL;
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  VARCHAR : string */
    strcpy(sVarchar, "MY VARCHAR");
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  VARCHAR : Truncation! */
    strcpy(sVarchar, "MY VARCHAR9"); /* Truncation! */
    sParam[0].mVarchar.mLength = strlen(sVarchar);
    sParam[0].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(Stmt, sParam);  /* SQL_SUCCESS_WITH_INFO */
}
```

The following is an example of inputting TEXT data.

```sql
CREATE TABLE ttt (doc TEXT);
```

```c
void testAppendFunc()
{
    SQL_APPEND_PARAM sParam[1];
 
    /*  TEXT : NULL */
    sParam[0].mText.mLength = SQL_APPEND_TEXT_NULL;
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  TEXT : string */
    strcpy(sText, "This is the sample document for tutorial.");
    sParam[0].mVar.mLength = strlen(sText);
    sParam[0].mVar.mData   = sText;
    SQLAppendDataV2(Stmt, sParam); /* OK */
}
```

#### SQLAppendDataByTimeV2

```c
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

This function inputs data into the channel, and it lets you set the `_arrival_time` value stored in the DB to a specific time instead of the current time. For example, use it when you want to enter the dates in a log file from a month ago as they were at that time.

* aTime is the time value to be set to `_arrival_time`. Enter the value in nanoseconds since January 1, 1970. The input values must also be sorted in order from the past to the present.
* aData is an array containing pointers to the data to be input. The number of array elements must match the number of columns of the table specified at open.

For the rest, refer to the SQLAppendDataV2() function.

#### SQLAppendDataV3 and SQLAppendDataByTimeV3

```c
SQLRETURN SQLAppendDataV3(SQLHSTMT aStmtHandle,
                          SQL_APPEND_PARAM *aData,
                          SQLINTEGER aColCount);

SQLRETURN SQLAppendDataByTimeV3(SQLHSTMT aStmtHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData,
                                SQLINTEGER aColCount);
```

V3 uses the same `SQL_APPEND_PARAM` values as V2 and adds `aColCount`.
Use it when the number of values supplied by the client must be explicit instead of inferred only from the table metadata opened by `SQLAppendOpen`.

#### SQLAppendBatch and SQLAppendBatchByTime

```c
SQLRETURN SQLAppendBatch(SQLHSTMT aStmtHandle,
                         SQLCHAR *aTableName,
                         SQLINTEGER aRowCount,
                         SQLINTEGER aColCount,
                         SQL_APPEND_TYPES *aTypes,
                         SQL_APPEND_PARAM *aData);

SQLRETURN SQLAppendBatchByTime(SQLHSTMT aStmtHandle,
                               SQLCHAR *aTableName,
                               SQLBIGINT aTime,
                               SQLINTEGER aRowCount,
                               SQLINTEGER aColCount,
                               SQL_APPEND_TYPES *aTypes,
                               SQL_APPEND_PARAM *aData);
```

Batch append sends a rectangular row set in one call. `aTypes` is an array of `SQL_APPEND_TYPE_*` values, and `aData` contains `aRowCount * aColCount` values in row order. `SQL_APPEND_TYPE_JSON` is available for JSON columns; BLOB and CLOB type entries are retained for variable binary/text payloads.

#### SQLAppendFlush

```c
SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
```

This function immediately sends the data accumulated in the current channel buffer to the Machbase server.

#### SQLAppendClose

```c
SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT* aSuccessCount,
                         SQLBIGINT* aFailureCount);
```

This function closes the currently open channel. If the channel is not open, an error occurs.

* aSuccessCount: The number of records appended successfully.
* aFailureCount: The number of records that failed to be appended.

#### SQLAppendSetErrorCallback

```c
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle, SQLAppendErrorCallback aFunc);
```

This function sets the callback function that is called when an error occurs during Append after SQLAppendOpen() has succeeded. If you do not set it, the client ignores errors even when they occur in the server.

* aStmtHandle: Specifies the statement to check for errors.
* aFunc: Specifies the function pointer to call on Append failure.

The prototype of SQLAppendErrorCallback is as follows.

```c
typedef void (*SQLAppendErrorCallback)(SQLHSTMT aStmtHandle,
                                     SQLINTEGER aErrorCode,
                                     SQLPOINTER aErrorMessage,
                                         SQLLEN aErrorBufLen,
                                     SQLPOINTER aRowBuf,
                                         SQLLEN aRowBufLen);
```

* aStatementHandle: The statement handle that caused the error
* aErrorCode: The 32-bit error code that caused the error
* aErrorMessage: The string for the error code
* aErrorBufLen: The length of aErrorMessage
* aRowBuf: A string containing the detailed description of the record that caused the error
* aRowBufLen: The length of aRowBuf

**Example of Using Error Callback (dumpError)**

```c
void dumpError(SQLHSTMT    aStmtHandle,
               SQLINTEGER  aErrorCode,
               SQLPOINTER  aErrorMessage,
               SQLLEN      aErrorBufLen,
               SQLPOINTER  aRowBuf,
               SQLLEN      aRowBufLen)
{
    char       sErrMsg[1024] = {0, };
    char       sRowMsg[32 * 1024] = {0, };
 
    if (aErrorMessage != NULL)
    {
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);
    }
 
    if (aRowBuf != NULL)
    {
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);
    }
 
    fprintf(stdout, "Append Error : [%d][%s]\n[%s]\n\n", aErrorCode, sErrMsg, sRowMsg);
}
 
 
......
 
    if( SQLAppendOpen(m_IStmt, TableName, aErrorCheckCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendOpen error\n");
        exit(-1);
    }
    // Setting Callback.
    assert(SQLAppendSetErrorCallback(m_IStmt, dumpError) == SQL_SUCCESS);
 
    doAppend(sMaxAppend);
 
    if( SQLAppendClose(m_IStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        fprintf(stdout, "SQLAppendClose error\n");
        exit(-1);
    }
}
```

#### SQLSetConnectAppendFlush

```c
SQLRETURN SQL_API SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option)
```

Data input by Append is written to the communication buffer and waits there until the user calls SQLAppendFlush or the buffer becomes full, and then it is sent to the server. Use this function if you want the Append data to be sent to the server at regular intervals even when the buffer is not full. Every 100 ms, this function computes the difference between the last transmission time and the current time, and sends the contents of the communication buffer to the server when the specified time (1 second if not set) has passed.

The parameters are as follows.

* hdbc: The DB connection handle.
* option: If 0, auto flush is turned off; any other value turns auto flush on.

Executing it on an unconnected hdbc results in an error.

#### SQLSetStmtAppendInterval

```c
SQLRETURN SQL_API SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue)
```

When time-based flushing is turned on with SQLSetConnectAppendFlush, use this function to turn off automatic flushing or adjust the flush interval for a particular statement.

The parameters are as follows.

* hstmt: The statement handle whose flush interval you want to adjust.
* fValue: The flush interval to set. **If 0, flush is not performed, and the unit is ms**. Because the thread that decides whether to flush runs every 100 ms, set it to a multiple of 100. Automatic flush does not run at exactly the specified time. **1000 is the default value**.

This function succeeds even if time-based flush is not running.

**Error Check and Description**

This section describes how to check for errors when using the Append-related functions, and the error codes. If a CLI function does not return SQL_SUCCESS, you can check the error message with the following code.

```c
SQLINTEGER errNo;
int msgLength;
char sqlState[6];
char errMsg[1024];
 
if (SQL_SUCCESS == SQLError ( env, con, stmt, (SQLCHAR *)sqlState, &errNo,
                              (SQLCHAR *)errMsg, 1024, &msgLength ))
{
    //set five length error code
    printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

The error messages returned by the Append-related functions are as follows.

<table>
  <thead>
    <tr>
      <th>function</th>
      <th>message</th>
      <th>description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="7">SQLAppendOpen</td>
      <td>statement is already opened.</td>
      <td>Occurs when SQLAppendOpen is executed in duplicate.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>Stream protocol termination failed.</td>
    </tr>
    <tr>
      <td>Failed to read protocol.</td>
      <td>A network read error occurred.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>Invalid column meta information structure</td>
    </tr>
    <tr>
      <td>cannot allocate memory.</td>
      <td>An internal buffer memory allocation error occurred.</td>
    </tr>
    <tr>
      <td>cannot allocate compress memory.</td>
      <td>A compression buffer memory allocation error occurred.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>The return value has an error.</td>
    </tr>
    <tr>
      <td rowspan="3">SQLAppendData</td>
      <td>statement is not opened.</td>
      <td>AppendData was called without AppendOpen.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>Occurs when you enter data larger than the size specified for a varchar type column.</td>
    </tr>
    <tr>
      <td>Failed to add binary.</td>
      <td>A write error occurred in the communication buffer.</td>
    </tr>
    <tr>
      <td rowspan="5">SQLAppendClose</td>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>Stream protocol termination failed.</td>
    </tr>
    <tr>
      <td>Failed to close buffer protocol.</td>
      <td>Buffer protocol termination failed.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>The column meta information structure is incorrect.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>The return value has an error.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLAppendFlush</td>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>A network write error occurred.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLSetErrorCallback</td>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state.</td>
    </tr>
    <tr>
      <td>Protocol Error (not APPEND_DATA_PROTOCOL)</td>
      <td>The value read from the communication buffer is not APPEND_DATA_PROTOCOL.</td>
    </tr>
    <tr>
      <td rowspan="8">SQLAppendDataV2</td>
      <td>Invalid date format or date string.</td>
      <td>Occurs when the datetime format is wrong.</td>
    </tr>
    <tr>
      <td>statement is not opened.</td>
      <td>Not in AppendOpen state.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>Occurs when you enter data larger than the size specified for a binary type column.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>Occurs when you enter data larger than the size specified for a varchar or text type column.</td>
    </tr>
    <tr>
      <td>Failed to add stream.</td>
      <td>A write error occurred in the communication buffer.</td>
    </tr>
    <tr>
      <td>IP address length is invalid.</td>
      <td>The mLength value of the IPv4/IPv6 type structure is specified incorrectly.</td>
    </tr>
    <tr>
      <td>IP string is invalid.</td>
      <td>Not in IPv4 or IPv6 format.</td>
    </tr>
    <tr>
      <td>Unknown data type has been specified.</td>
      <td>Not a data type used by Machbase.</td>
    </tr>
  </tbody>
</table>

## Column wise parameter binding

The SQLAppend functions, which input a large amount of data into Machbase quickly, can be used only for log and tag tables; they cannot be used to perform a bulk update on a lookup or volatile table.

For this purpose, Machbase 5.5 and later versions support column-wise parameter binding. (Row-wise parameter binding is not supported yet.)

Set SQL_ATTR_PARAM_BIND_TYPE in the Attribute argument of SQLSetStmtAttr() and SQL_PARAM_BIND_BY_COLUMN in the param argument. For each column to bind, set the parameter as an array and the indicator variable as an array as well. Then call SQLBindParameter() with these parameters.

The figure below shows how column-wise binding works for each parameter array.

<table>
  <thead>
    <tr>
      <th colspan="2">Column A<br>(parameter A)</th>
      <th colspan="2">Column B<br>(parameter B)</th>
      <th colspan="2">Column C<br>(parameter C)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Value_Array</td>
      <td>Indicator/<br>length array</td>
      <td>Value_Array</td>
      <td>Indicator/<br>length array</td>
      <td>Value_Array</td>
      <td>Indicator/<br>length array</td>
    </tr>
  </tbody>
</table>

The following example inserts a large amount of data with column-wise parameter binding.

```c
#define DESC_LEN 51
#define ARRAY_SIZE 10
SQLCHAR * Statement = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";
 
/* Array of parameters to bind */
SQLUINTEGER PartIDArray[ARRAY_SIZE];
SQLCHAR DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL PriceArray[ARRAY_SIZE];
/* Array of indicator variables to bind */
SQLINTEGER PartIDIndArray[ARRAY_SIZE], DescLenOrIndArray[ARRAY_SIZE], PriceIndArray[ARRAY_SIZE];
SQLUSMALLINT i, ParamStatusArray[ARRAY_SIZE];
SQLUINTEGER ParamsProcessed;
 
// Set the SQL_ATTR_PARAM_BIND_TYPE statement attribute to use
// column-wise binding.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE, SQL_PARAM_BIND_BY_COLUMN, 0);
// Specify the number of elements in each parameter array.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, ARRAY_SIZE, 0);
// Specify an array in which to return the status of each set of
// parameters.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR, ParamStatusArray, 0);
// Specify an SQLUINTEGER value in which to return the number of sets of
// parameters processed.
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR, &ParamsProcessed, 0);
// Bind the parameters in column-wise fashion.
SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER, 5, 0,
    PartIDArray, 0, PartIDIndArray);
SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, DESC_LEN - 1, 0,
    DescArray, DESC_LEN, DescLenOrIndArray);
SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 7, 0,
    PriceArray, 0, PriceIndArray);
```

## Supported Strings

Machbase stores string data in UTF-8 by default.

On Windows, where strings are input and output in encodings other than UTF-8, ODBC converts them as follows.

|OS|Unicode/Non-Unicode|String Conversion|Note|
|--|--|--|--|
|Windows|Unicode (UTF-16)|UTF-16 ⟷ UTF-8|N/A|
|Windows|Non-Unicode (MBCS)|MBCS ⟷ UTF-8|Uses the default string encoding for non-Unicode applications in the Windows settings|
|Linux|UTF-8|N/A|Only UTF-8 is supported|
