---
type: docs
title : 'CLI/ODBC'
type : docs
weight: 10
---

CLI란 [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003에 정의된 소프트웨어 개발 표준입니다.

CLI는 데이터베이스에 어떻게 SQL을 전달하고, 결과 값을 어떻게 받고 분석해야 하는지에 대한 함수 및 명세를 정의하고 있습니다. 이 CLI는 1990년 초창기에 개발되었고, C 와 COBOL 언어 만을 위해 개발되었고, 현재까지 그 스펙이 유지되고 있습니다.

현재까지 가장 널리 알려진 표준 인터페이스는 ODBC(Open Database Connectivity)로서 클라이언트 프로그램이 데이터베이스의 종류와 무관하게 데이터베이스 접속할 수 있는 방법을 제시해 주고 있습니다. 현재 최신 ODBC API 버전은 3.52 로서 ISO와 X/Open 표준에 정의되어 있습니다.


## 표준 CLI 함수
표준 함수의 사용법에 대해서는 다음과 같은 링크를 참조합니다.

* [위키피디아](https://en.wikipedia.org/wiki/Call_Level_Interface)
* [오픈그룹 문서](https://www2.opengroup.org/ogsys/catalog/c451)

다음의 함수를 참고하면 됩니다.

| | | | |
|--|--|--|--|
| SQLAllocConnect   | SQLDisconnect     | SQLGetDescField  | SQLPrepare        |
| SQLAllocEnv       | SQLDriverConnect  | SQLGetDescRec    | SQLPrimaryKeys    |
| SQLAllocHandle    | SQLExecDirect     | SQLGetDiagRec    | SQLStatistics     |
| SQLAllocStmt      | SQLExecute        | SQLGetEnvAttr    | SQLRowCount       |
| SQLBindCol        | SQLFetch          | SQLGetFunctions  | SQLSetConnectAttr |
| SQLBindParameter+ | SQLFreeConnect    | SQLGetInfo       | SQLSetDescField   |
| SQLColAttribute   | SQLFreeEnv        | SQLGetStmtAttr   | SQLSetDescRec     |
| SQLColumns        | SQLFreeHandle     | SQLGetTypeInfo   | SQLSetEnvAttr     |
| SQLConnect        | SQLFreeStmt       | SQLNativeSQL     | SQLSetStmtAttr    |
| SQLCopyDesc       | SQLGetConnectAttr | SQLNumParams     | SQLStatistics     |
| SQLDescribeCol    | SQLGetData        | SQLNumResultCols | SQLTables         |

## 접속을 위한 연결 스트링
CLI를 통해 접속을 하기 위해서는 연결 스트링을 만들어야 하며, 각각의 내용은 다음과 같습니다.

| 연결 스트링 항목명  | 항목 설명 |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         DSN         | 데이터 소스 명을 지정합니다.<br> ODBC에서는 리소스가 담긴 파일의 섹션 명을 기술하고, CLI에서는 서버명 혹은 IP 주소를 지정합니다.  |
|        DBNAME       | Machbase의 DB명을 기술합니다.  |
|        SERVER       | Machbase가 위치하는 서버의 호스트 명 혹은 IP 주소를 가리킵니다.  |
|       NLS_USE       | 서로 사용할 언어 종류를 설정합니다.(현재 사용되지 않으며, 차후 확장을 위해 유지합니다.)  |
|         UID         | 사용자 아이디  |
|         PWD         | 사용자 패스워드  |
|       PORT_NO       | 접속할 포트 번호  |
|       PORT_DIR      | 유닉스에서 Unix domain으로 접속할 경우 사용되는 파일 경로를 지정합니다.<br> (서버에서 수정했을 경우에 지정하며, 디폴트로는 지정하지 않아도 동작합니다.)  |
|       CONNTYPE      | 클라이언트와 서버의 접속 방법을 지정합니다.<br> 1: TCP/IP INET 으로 접속<br> 2: Unix Domain 으로 접속  |
|       COMPRESS      | Append 프로토콜을 압축할 것인지 나타냅니다.<br> 이 값이 0일 경우에는 압축하지 않고 전송합니다.<br> 이 값이 0보다 큰 임의의 값일 경우에는 그 값보다 Append 레코드가 클 경우에만 압축합니다.<br> 예) COMPRESS=512<br> 레코드 사이즈가 512보다 클 경우에만 압축하여 동작합니다.<br> 원격 접속일 경우 압축하면 전송 성능이 향상됩니다.  |
|   SHOW_HIDDEN_COLS  | 숨겨진 컬럼(_arrival_time)을 select * 로 수행시 보여줄 것인지 결정합니다.<br> 0일 경우에는 보이지 않으며, 1일 경우에 해당 컬럼의 정보가 출력됩니다.  |
|  CONNECTION_TIMEOUT | 최초 연결시에 얼마나 대기할 것이지 설정합니다.<br> 디폴트로는 30초가 설정되어 있습니다.<br> 만일 최초 연결시 서버의 응답이 30초 보다 더 느려지는 경우를 고려하면, 이 값을 더 크게 설정해야 합니다.<br> CONNECTION_TIMEOUT에서 0 값은 Timeout에 제한이 없음을 의미하며 연결이 실패할 때에도 무한정으로 대기하므로 되도록이면 사용하지 않는 편이 좋습니다.  |
|    SOCKET_TIMEOUT   | Protocol I/O에 시간이 걸리면 발생하는 timeout입니다.<br> Client에서 검사하여 대기 후 Disconnect를 수행합니다.<br> ORACLE의 Read Timeout과 같습니다. (MYSQL, MSSQL에서는 동일하게 SOCKET_TIMEOUT이라는 이름으로 사용합니다.)<br> Connection String에서 SOCKET_TIMEOUT=NN(초)로 설정하며 기본값은 30분(1800)으로 설정됩니다.  |
| ALTERNATIVE_SERVERS | cluster 버전을 사용 시, 여러 대의 브로커의 정보를 추가적으로 가지게 되는 설정입니다.<br> 다중의 브로커를 등록해두었을 시, 접속되어있던 브로커가 혹시 내려가게 된 경우에도 다른 브로커에 접속한 뒤, 입력하던 데이터를 계속해서 입력하게 됩니다.<br> 여러개의 브로커를 등록할 수 있으며, <서버 주소>:<서버 포트>의 값을 ',' 단위로 이어서 작성합니다.<br>  ex) ALTERNATIVE_SERVERS=192.168.0.10:20320,192.168.0.11:20320; |

CLI 접속 예제는 다음과 같습니다.

```cpp
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
 
if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```

## 확장 CLI 함수 (APPEND)
CLI 확장 함수는 Machbase 서버에 데이터를 초고속으로 입력하기 위해 제공되는 Append 프로토콜을 구현하기 위한 함수입니다.

이 함수는 크게 4가지의 함수로 구성되어 있는데, 채널의 오픈, 채널에 대한 데이터 입력, 채널의 플러쉬, 채널 클로징입니다.

### Append 프로토콜의 이해
Machbase에서 제공하는 Append 프로토콜은 비동기 방식으로 동작합니다. 비동기라 함은 클라이언트가 서버에게 요청한 특정 작업에 대한 응답이 서로 완전히 동기화되지 않고, 임의의 이벤트가 발생하는 순간에 발생하는 것을 의미합니다. 즉, 클라이언트가 Append를 수행했다고 하더라도, 그 수행에 대한 결과를 바로 얻거나 확인할 수 없으며, 서버에서 준비가 되는 임의의 시점에 그것을 확인할 수 있다는 것입니다. 이런 이유로 Append 프로토콜을 활용해서 응용 프로그램을 개발하는 개발자는 다음과 같은 내부 동작에 대한 이해를 가져야 합니다. 이후의 설명은 클라이언트가 언제 어떻게 서버에서 발생하는 비동기 에러를 검출하고 사용자에게 되돌여주는지에 대한 것입니다.

### Append 데이터의 전송
SQLExecute 혹은 SQLExecDirect()와 같은 일반적인 호출에서 Machbase는 즉시 그 결과를 클라이언트에게 되돌려주는 동기화 방식을 사용합니다. 그러나, SQLAppendDataV2()는 사용자 데이터가 입력된 이후 즉시 요청을 보내지 않습니다. 대신, 클라이언트 통신 버퍼가 모두 찰 때 까지 대기하고 있다가 모두 차면 그 이후에 한꺼번에 데이터를 클라이언트로 전송하게 됩니다. 이렇게 설계된 이유는 Append를 사용하는 클라이언트의 입력 데이터가 초당 수만에서 수십만 레코드를 가정하였기 때문에 고속의 데이터 전송을 위한 버퍼링 방식을 활용한 것입니다. 이런 이유로 만일 사용자가 임의로 해당 버퍼의 내용을 전송하고자 할 경우에는 SQLAppendFlush() 함수를 호출하여, 명시적으로 데이터를 입력할 수 있습니다.

### Append 데이터의 에러 확인
앞에서 언급한 바와 같이 Append 프로토콜은 버퍼링되어 비동기로 동작합니다. 특히, 서버에서 에러가 발생하지 않았을 경우에는 아무런 응답을 받지 않고, 에러가 발생했을 경우에만 에러를 검출하는 방식을 취하기 때문에 에러가 언제 어떻게 검출되는지 이해하는 것이 매우 중요합니다. 또한, 에러를 검출하는 비용이 상대적으로 매우 크기 때문에 레코드 입력시마다 매번 검사하는 것이 매우 비효율적으로 판단되어, 현재 Machbase에서는 명시적으로 다음과 같은 경우에만 에러를 검출하도록 되어 있습니다. 에러가 검출될 경우에는 사용자가 설정한 에러 콜백 함수를 매번 호출하게 됩니다.

1. 전송 버퍼가 모두 차고, 서버에게 명시적으로 데이터를 전송한 이후 검사
2. SQLAppendFlush() 내부에서 서버에게 명시적으로 데이터를 전송한 이후 검사
3. SQLAppendClose() 내부에서 종료 직전에 검사

즉, 기본적으로 위의 3가지 경우에만 에러를 검출하도록 되어 있어, I/O의 발생을 최소화하도록 설계되었습니다.

### 서버 에러 검사를 위한 부가 옵션
성능을 최대한으로 달성하기 위해 기본적으로 설정된 에러 검출 기법은 사용자가 원하는 경우 좀 더 빈번하게 검사하고, 이를 활용할 수 있습니다. 즉, SQLAppendOpen() 함수의 마지막 인자인 aErrorCheckCount를 조절함으로서 가능합니다. 이 값이 0일 경우에는 별도의 확인 동작을 하지 않고, 기본으로 동작합니다. 그러나, 만일 이 값이 0보다 클 경우에는 SQLAppendData()의 호출 횟수마다 명시적으로 에러를 검사하도록 되어 있습니다. 다시 말해 이 값이 10일 경우에는 10번의 Append 동작마다 에러를 검사하는 비용을 지불합니다. 따라서, 이 값이 작을 경우에는 에러 검출을 위한 시스템 리소스를 많이 사용하기 때문에 적절한 숫자로 조절하여 사용해야 합니다.

### 서버 에러 발생시 Trace 로그 남기기
만일 에러가 발생한 Append 데이터에 대해서 별도로 Trace 로그를 남기고자 할 경우에는 서버에 준비된 프로퍼티 DUMP_APPEND_ERROR 를 1로 설정합니다. 이렇게 설정하면, mach.trc 파일에 해당 에러를 발생시킨 레코드에 대한 명세가 파일로 기록됩니다. 단, 에러의 횟수가 과도할 경우 시스템 리소스의 사용량이 급격히 늘어나, Machbase의 전체 성능을 떨어뜨릴 수 있으므로 주의하여 사용해야 합니다.

### APPEND 함수 설명
#### SQLAppendOpen
```cpp
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount );
```
이 함수는 대상 테이블에 대한 채널을 오픈합니다. 이후 이 채널을 닫아 주지 않으면 지속적으로 열린 상태가 유지됩니다.

하나의 연결에 대해 최대 1024개의 Statement 설정이 가능합니다. 각 Statement마다 SQLAppendOpen을 사용하면 됩니다.

1. aStatementHandle : Append를 수행할 Statement의 핸들을 나타냅니다.
2. aTableName : Append를 수행할 대상 테이블의 이름을 나타냅니다.
3. aErrorCheckCount : 몇 건의 데이터가 입력될 때 마다 서버의 에러를 검사할 것인지 결정합니다. 이 값이 0일 경우에는 임의로 에러를 검사하지 않습니다.

#### SQLAppendData (deprecated)
```cpp
SQLRETURN  SQLAppendData(SQLHSTMT StatementHandle, void *aData[]);
```
이 함수는 해당 채널에 대해 데이터를 입력하는 함수입니다.

* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다. 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.
* 리턴값은 SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, SQL_ERROR가 가능합니다. 특히, SQL_SUCCESS_WITH_INFO가 반환되었을 경우에는 입력된 특정 컬럼의 길이가 길어 잘리는 등의 오류가 있을 수 있으므로 결과를 다시 확인하여야 합니다.

**데이터 타입에 따른 설정**

숫자형 및 문자형
* float, double, short, int, long long, char * 과 같은 타입은 해당 값에 대한 포인터 설정 만으로 잘 동작합니다.

주소형
* ipv4 의 경우에는 5 바이트 무부호 문자(unsigned char)의 배열로 넘깁니다.
* 첫 번째 바이트는 4로 설정하고, 이후의 4바이트는 연속되는 주소값으로 설정합니다. 
* 예를 들어, 127.0.0.1의 경우에는 5바이트 배열 0x04, 0x7f, 0x00, 0x00, 0x01 의 순으로 들어가게 됩니다.

```cpp
// 4개의 컬럼 정보를 가지는 테이블의 경우 (short(16), int(32), long(64), varchar)
 
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

**데이터 타입에 따른 설정**

datetime 형 

* Machbase 는 내부적으로 나노 단위 시간 해상도 값을 가지기 때문에 클라이언트에서 시간을 설정할 때는 변환과정을 거쳐야 하며, 64비트 부호없는 정수형 값으로 표현됩니다. 따라서 적절한 변환을 위해서는 유닉스 라이브러리인 mktime을 이용하여 초로 변환한 이후에 나노 값을 더해주어야 합니다.
* ※ Machbase의 시간 = (1970년 1월 1일 이후로부터의 총 시간 (초)) * 1,000,000,000 + mili-second * 1,000,000 + micro-second * 1000 + nano-second;

```cpp
// Date String이 "연도-월-일 시:분:초 밀리:마이크로:나노" 형태로 입력될 경우 코드
 
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

```cpp
SQLRETURN  SQLAppendDataByTime(SQLHSTMT StatementHandle, SQLBIGINT aTime, void *aData[]);
```
이 함수는 해당 채널에 대해 데이터를 입력하는 함수이며, DB에 저장되는 _arrival_time 값을 현재 시간이 아닌 특정 시간의 값으로 설정할 수 있습니다.

예를 들면, 1개월전 로그 파일에 있는 날짜를 그 당시의 날짜로 입력하고자 할때 사용됩니다.

* aTime은 _arrival_time으로 설정된 time 값입니다. 
* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다. 
* 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.

나머지 사항은 SQLAppendData()함수를 참고하여 작성하면 됩니다.

```cpp
// 4개의 컬럼 정보를 가지는 테이블의 경우  (short(16), int(32), long(64), varchar)
 
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

```cpp
SQLRETURN  SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

이 함수는 Machbase 2.0 부터 새로 도입된 Append 함수로서, 기존의 함수에서 불편했던 입력 방식을 편리하게 대폭 개선한 함수입니다. 

특히, 2.0에서 도입된 TEXT와 BINARY 타입의 경우는 SQLAppendDataV2() 함수에서만 입력이 가능합니다.

* 각 타입에 맞는 NULL 입력 가능
* VARCHAR 입력시 스트링 길이 입력 가능
* IPv4, IPv6 입력시 바이너리 및 스트링 형태의 데이터 입력 가능
* TEXT, BINARY 타입에 대한 데이터 길이 지정 가능

함수 인자는 다음과 같이 구성됩니다.

* aData는 SQL_APPEND_PARAM 이라는 인자배열을 가리키는 포인터입니다. 이 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다. 
* 리턴값은 SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, SQL_ERROR 가 가능합니다. 특히, SQL_SUCCESS_WITH_INFO가 반환되었을 경우에는 입력된 특정 컬럼의 길이가 길어 잘리는 등의 오류가 있을 수 있으므로 결과를 다시 확인하여야 합니다.

아래는 실제로 V2에서 사용될 SQL_APPEND_PARAM 의 정의이며, 이 내용은 machbase_sqlcli.h 에 포함되어 있습니다.

```cpp
typedef struct machAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machAppendVarStruct;
 
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
    machbaseAppendVarStruct      mBinary;  /* binary */
    machbaseAppendVarStruct      mBlob;    /* reserved alias */
    machbaseAppendVarStruct      mClob;    /* reserved alias */
    machbaseAppendDateTimeStruct mDateTime;
} machbaseAppendParam;
 
#define SQL_APPEND_PARAM machbaseAppendParam
```
위에서 볼 수 있듯이 내부적으로 machbaseAppendParam 이라는 공용 구조체가 하나의 인자를 담고 있는 구조입니다. 각 데이터 타입에 대해 데이터 및 스트링에 대한 길이 및 값을 명시적으로 입력할 수 있도록 되어 있습니다. 실제 사용 예는 다음과 같습니다.

**고정 길이 숫자형 타입의 입력**

고정 길이 숫자형 타입이라 함은 short, ushort, integer, uinteger, long, ulong, float, double 을 말합니다. 이 타입의 경우 SQL_APPEND_PARAM의 구조체 멤버에 직접 값을 대입함으로써 입력 가능합니다.

| 데이터베이스 타입 | NULL 매크로              | SQL_APPEND_PARAM 멤버 |
|-------------------|--------------------------|-----------------------|
|       SHORT       |   SQL_APPEND_SHORT_NULL  |         mShort        |
|       USHORT      |  SQL_APPEND_USHORT_NULL  |        mUShort        |
|      INTEGER      |  SQL_APPEND_INTEGER_NULL |        mInteger       |
|      UINTEGER     | SQL_APPEND_UINTEGER_NULL |       mUInteger       |
|        LONG       |   SQL_APPEND_LONG_NULL   |         mLong         |
|       ULONG       |   SQL_APPEND_ULONG_NULL  |         mULong        |
|       FLOAT       |   SQL_APPEND_FLOAT_NULL  |         mFloat        |
|       DOUBLE      |  SQL_APPEND_DOUBLE_NULL  |        mDouble        |

다음은 실제 값을 입력하는 예제입니다.

```cpp
// Table Schema가 8개의 컬럼이고, 각각 SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, DOUBLE로 이루어진 것으로 가정합니다.
 
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

**날짜형 타입의 입력**

아래는 DATETIME형의 데이터를 입력하는 예입니다. 편의를 위해 몇가지의 매크로가 준비되어 있습니다.

SQL_APPEND_PARAM에서 mDateTime 멤버에 대한 조작을 수행합니다. 아래의 매크로는 mDateTime 구조체에서 mTime이라는 64비트 정수값에 대해 설정함으로써 날짜를 지정할 수 있습니다.

```cpp
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

| 매크로 | 설명 |
|-------------------------------|------------------------------------------------------------|
|    SQL_APPEND_DATETIME_NOW    | 현재의 클라이언트 시간을 입력합니다.                                                                                                                                                                                      |
| SQL_APPEND_DATETIME_STRUCT_TM | mDateTime의 struct tm 구조체인 mTM에 값을 설정하고, 그 값을 데이터베이스로 입력합니다.                                                                                                                                    |
|   SQL_APPEND_DATETIME_STRING  | mDateTime의 스트링형에 대한 값을 설정하고, 이를 데이터베이스로 입력합니다.<br> mDateStr : 실제 날짜 스트링 값이 할당<br> mFormatStr : 날짜 스트링에 대한 포맷 스트링 할당                                                         |
|    SQL_APPEND_DATETIME_NULL   | 날짜 컬럼의 값을 NULL로 입력합니다.                                                                                                                                                                                       |
|        임의의 64비트 값       | 이 값이 실제 datetime으로 입력됩니다.<br> 이 값을 1970년 1월 1일 이후로부터 나노세컨드 단위의 시간이 흐른 정수값을 나타냅니다. <br>예를 들어, 만일 이 값이 10억 (1,000,000,000) 이라면, 1970년 1월 1일 0시 0분 1초를 나타냅니다.(GMT) |

```cpp
// 다음은 각각의 경우에 대해 실제 값을 입력하는 예제입니다. 하나의 DATETIME 컬럼이 존재한다고 가정합니다.
void testAppendDateTimeFunc()
{
    SQL_mach_PARAM sParam[1];
    /* NULL 입력 */
    sParam[0].mDateTime.mTime   = SQL_APPEND_DATETIME_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* 현재 시간 입력 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(Stmt, sParam);
 
    /* 임의의 값 입력 :1970.1.1일 이후로부터의 현재까지 나노세컨드의 값 */
    sParam[0].mDateTime.mTime      = 1234;
    SQLAppendDataV2(Stmt, sParam);
 
    /*  스트링 포맷 기준 입력 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[0].mDateTime.mDateStr   = "23/May/2014:17:41:28";
    sParam[0].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(Stmt, sParam);
 
    /*  struct tm의 값을 변경하여 입력 */
    sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[0].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[0].mDateTime.mTM.tm_mon  =  11;
    sParam[0].mDateTime.mTM.tm_mday  = 31;
    SQLAppendDataV2(Stmt, sParam);
}
```

**인터넷 주소형 타입의 입력**

아래는 IPv4와 IPv6 형의 데이터를 입력하는 예입니다. 이 역시 편의를 위해 몇가지의 매크로가 준비되어 있습니다. SQL_APPEND_PARAM에서 mLength 멤버에 대한 조작을 수행합니다.

```cpp
/* for IPv4, IPv6 as bin or string representation */
typedef struct machbaseAppendIPStruct
{
    unsigned char   mLength; /* 0:null, 4:ipv4, 6:ipv6, 255:string representation */
    unsigned char   mAddr[16];
    char           *mAddrString;
} machbaseAppendIPStruct;
```

| 매크로 (mLength 에 설정) | 설명                                     |
|--------------------------|------------------------------------------|
|    SQL_APPEND_IP_NULL    |        해당 컬럼에 NULL 값을 입력        |
|    SQL_APPEND_IP_IPV4    |        mAddr이 IPv4를 가지고 있음        |
|    SQL_APPEND_IP_IPV6    |        mAddr이 IPv6를 가지고 있음        |
|   SQL_APPEND_IP_STRING   | mAddrString이 주소 문자열을 가지고 있습니다. |

다음은 각각의 경우에 대해 실제 값을 입력하는 예제입니다.

```cpp
void testAppendIPFunc()
{
    SQL_APPEND_PARAM sParam[1];
    /* NULL */
    sParam[0].mIP.mLength  = SQL_APPEND_IP_NULL;
    SQLAppendDataV2(Stmt, sParam);
 
    /* 배열을 직접 수정 */
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

IP 타입을 문자열 (STRING) 로 입력할경우 SQLAppendDataV2 이후에 각각 자료형에 맞게 mLength가 4 또는 6으로 바뀌게 됩니다.
따라서 반복문에서 코딩할 경우 매번 SQLAppendDataV2() 전에, mLength 를 SQL_APPEND_IP_STRING 으로 지정해 주어야 합니다.

**가변 데이터형(문자 및 이진 데이터) 입력**

가변 데이터 형에는 VARCHAR 및 TEXT 그리고, BLOB과 CLOB이 포함됩니다. 기존함수에서는 VARCHAR 만이 지원되었고, 또한 스트링의 길이를 사용자가 입력할 수 있는 방법이 없었습니다. 그런 이유로 매번 strlen() 함수를 통해 길이를 얻어야 했지만, 함수 V2 부터는 사용자가 직접 가변 데이터형에 대한 길이를 지정할 수 있게 되었습니다. 따라서, 만일 사용자가 그 길이를 미리 알고 있다면, 더 빠르게 데이터를 입력할 수 있습니다. 내부적으로는 가변 데이터형이 하나의 구조체로 되어 있지만, 개발 편의를 위해 각 데이터타입에 따라 멤버를 별도로 만들어 놓았습니다.

```cpp
typedef struct machAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machAppendVarStruct;
```

가변 데이터형의 입력시에는 데이터의 길이를 mLength에 설정하고, 원시 데이터 포인터를 mData로 설정하면 됩니다. 만일 mLength의 길이가 정의된 스키마보다 클 경우에는 자동으로 잘려서 입력됩니다. 이때 SQLAppendDataV2() 함수는 SQL_SUCCESS_WITH_INFO을 리턴하게 되고, 더불어 관련 경고 메시지를 내부 구조체에 채웁니다. 이 경고 메시지를 확인하기 위해서는 SQLError() 함수를 이용하면 됩니다.

| 데이터베이스 타입 | NULL 매크로             | SQL_APPEND_PARAM 멤버 (mVar를 사용해도 무방함) |
|-------------------|-------------------------|:----------------------------------------------:|
|      VARCHAR      | SQL_APPEND_VARCHAR_NULL |                    mVarchar                    |
|        TEXT       |   SQL_APPEND_TEXT_NULL  |                      mText                     |
|       BINARY      |  SQL_APPEND_BINARY_NULL |                     mBinary                    |
|        BLOB       |   SQL_APPEND_BLOB_NULL  |                      mBlob                     |
|        CLOB       |   SQL_APPEND_CLOB_NULL  |                      mClob                     |

다음은 각각의 환경에 대해 실제 값을 입력하는 예제입니다. 하나의 VARCHAR 컬럼이 존재한다고 가정합니다.

```sql
CREATE TABLE ttt (name VARCHAR(10));
```

```cpp

void testAppendVarcharFunc()
{
    SQL_mach_PARAM sParam[1];
 
    /*  VARCHAR : NULL */
    sParam[0].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL
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

다음은 Text 타입에 대한 입력 예제입니다.

```sql
CREATE TABLE ttt (doc TEXT);
```

```cpp
void testAppendFunc()
{
    SQL_mach_PARAM sParam[1];
 
    /*  VARCHAR : NULL */
    sParam[0].mText.mLength = SQL_APPEND_TEXT_NULL
    SQLAppendDataV2(Stmt, sParam); /* OK */
 
    /*  VARCHAR : string */
    strcpy(sText, "This is the sample document for tutorial.");
    sParam[0].mVar.mLength = strlen(sText);
    sParam[0].mVar.mData   = sText;
    SQLAppendDataV2(Stmt, sParam); /* OK */
}
```

#### SQLAppendDataByTimeV2

```cpp
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

이 함수는 해당 채널에 대해 데이터를 입력하는 함수이며, DB에 저장되는 _arrival_time 값을 현재 시간이 아닌 특정 시간의 값으로 설정할 수 있습니다. 예를 들면, 1개월전 로그 파일에 있는 날짜를 그 당시의 날짜로 입력하고자 할때 사용됩니다.

* aTime은 _arrival_time으로 설정될 time값입니다. 1970년 1월 1일 이후로부터의 현재까지 nano second 값을 입력해야 합니다. 또한 입력되는 값이 과거부터 현재순으로 순차적으로 정렬되어 있어야 합니다.
* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다. 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다. 

 나머지 사항은 SQLAppendDataV2()함수를 참고하여 작성하면 됩니다.

#### SQLAppendFlush

 ```cpp
 SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
 ```

 이 함수는 현재 채널 버퍼에 쌓여있는 데이터를 Machbase 서버로 즉시 전송합니다.

#### SQLAppendClose

 ```cpp
 SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT* aSuccessCount,
                         SQLBIGINT* aFailureCount);
 ```

 이 함수는 현재 열린 채널을 닫습니다. 만일 열려지지 않은 채널이 존재할 경우 에러가 발생합니다.

* aSuccessCount : Append를 성공한 레코드 개수 값을 가집니다.
* aFailureCount : Append를 실패한 레코드 개수 값을 가집니다.

#### SQLAppendSetErrorCallback

```cpp
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle, SQLAppendErrorCallback aFunc);
```

이 함수는 SQLAppendOpen()이 성공한 다음 Append시 에러가 발생했을 때 호출되는 콜백 함수를 설정합니다. 만일 이 함수를 설정하지 않을 경우에는 서버에 에러가 발생하더라도, 클라이언트에서는 무시하게 됩니다.

* aStmtHandle : 에러를 확인할 Statement를 지정합니다.
* aFunc : Append 실패시 호출할 함수 포인터를 지정합니다.

SQLAppendErrorCallback의 프로토타입은 다음과 같습니다.

```cpp
typedef void (*SQLAppendErrorCallback)(SQLHSTMT aStmtHandle,
                                     SQLINTEGER aErrorCode,
                                     SQLPOINTER aErrorMessage,
                                         SQLLEN aErrorBufLen,
                                     SQLPOINTER aRowBuf,
                                         SQLLEN aRowBufLen);
```

* aStatementHandle : 에러를 발생한 Statement 핸들
* aErrorCode : 에러의 원인이 된 32비트 에러 코드
* aErrorMessage : 해당 에러코드에 대한 문자열
* aErrorBufLen : aErrorMessage의 길이
* aRowBuf : 에러를 발생시킨 레코드의 상세 명세가 담긴 문자열
* aRowBufLen : aRowBuf의 길이

**에러 콜백(dumpError)의 사용 예**

```cpp
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
    // 콜백을 설정합니다.
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

```cpp
SQLRETURN SQL_API SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option)
```

Append에 의해서 입력된 데이터는 통신 버퍼에 기록되어 전송대기 상태에서 사용자가 SQLAppendFlush 함수를 호출하거나 통신 버퍼가 가득 차게 되면 서버로 전송됩니다. 사용자가 버퍼가 가득 차 있지 않아도 일정 주기로 서버에게 Append에 의한 데이터를 전송하게 하려면 이 함수를 이용하면 됩니다. 이 함수는 매 100ms 주기로 마지막으로 전송한 시간과 현재 시간의 차이를 계산하여 지정된 시간(설정하지 않은 경우에는 1초)가 지난 경우 통신 버퍼의 내용을 서버에 전달합니다.

매개변수는 다음과 같습니다.

* hdbc : DB의 connection handle입니다.
* option : 0이면 auto flush를 off, 0이 아닌 값이면 auto flush를 on으로 합니다.

연결되지 않은 hdbc에 대해서 실행하면 오류로 처리됩니다.

#### SQLSetStmtAppendInterval

```cpp
SQLRETURN SQL_API SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue)
```

SQLSetConnectAppendFlush를 이용해서 시간 단위 flush기능을 켰을 경우, 특정 statement에 대해서는 자동 flush를 끄거나 flush 주기를 조정하고 싶을 경우 이 함수를 사용합니다.

매개변수는 다음과 같습니다.

* hstmt : flush주기를 조정하고자 하는 statement handle입니다.
* fValue : flush주기를 조정하고자 하는 값입니다. 0이면 flush를 하지 않으며 단위는 ms입니다. 100ms마다 flush할지를 결정하는 스레드가 실행되므로 100의 배수로 설정합니다. 정확히 원하는 시점에 자동 flush가 실행되지는 않습니다. 1000이 기본 값입니다.

시간 기반 flush가 실행중이지 않은 경우라도 이 함수의 실행은 성공합니다.

**Error 확인 및 설명**

Append 관련 함수를 사용할때 에러를 확인하는 방법과 코드에 대한 설명입니다. CLI 함수에서 return 값이 SQL_SUCCESS가 아닌 경우 아래 코드를 이용하여 에러 메시지를 확인할 수 있습니다.

```cpp
SQLINTEGER errNo;
int msgLength;
char sqlState[6];
char errMsg[1024];
 
if (SQL_SUCCESS == SQLError ( env, con, stmt, (SQLCHAR *)sqlState, &errNo,
                              (SQLCHAR *)errMsg, 1024, &msgLength ))
{
    //error code값을 5자리 숫자로 지정합니다.
    printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

Append관련 함수에서 리턴되는 에러 메시지는 아래와 같습니다.

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
      <td>중복으로 SQLAppendOpen을 하는 경우 발생합니다.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>스트림 프로토콜 종료에 실패했습니다.</td>
    </tr>
    <tr>
      <td>Failed to read protocol.</td>
      <td>네트워크 읽기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>column meta 정보 구조가 잘못됨</td>
    </tr>
    <tr>
      <td>cannot allocate memory.</td>
      <td>내부 버퍼 메모리 할당 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>cannot allocate compress memory.</td>
      <td>압축 버퍼 메모리 할당 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>return값에 오류가 있습니다.</td>
    </tr>
    <tr>
      <td rowspan="3">SQLAppendData</td>
      <td>statement is not opened.</td>
      <td>AppendOpen을 하지 않고 AppendData를 call합니다.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>varchar 타입 컬럼에 지정된 사이즈 보다 큰 데이터를 입력하는 경우 발생합니다.</td>
    </tr>
    <tr>
      <td>Failed to add binary.</td>
      <td>통신버퍼에 쓰기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td rowspan="5">SQLAppendClose</td>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님.</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>스트림 프로토콜 종료에 실패했습니다.</td>
    </tr>
    <tr>
      <td>Failed to close buffer protocol.</td>
      <td>버퍼 프로토콜 종료에 실패했습니다.</td>
    </tr>
    <tr>
      <td>cannot read column meta.</td>
      <td>column meta정보 구조가 잘못됩니다.</td>
    </tr>
    <tr>
      <td>invalid return after reading column meta.</td>
      <td>return값에 오류가 있습니다.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLAppendFlush</td>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님</td>
    </tr>
    <tr>
      <td>Failed to close stream protocol.</td>
      <td>네트워크 쓰기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td rowspan="2">SQLSetErrorCallback</td>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님.</td>
    </tr>
    <tr>
      <td>Protocol Error (not APPEND_DATA_PROTOCOL)</td>
      <td>통신 버퍼 읽기 결과가 APPEND_DATA_PROTOCOL 값이 아님.</td>
    </tr>
    <tr>
      <td rowspan="8">SQLAppendDataV2</td>
      <td>Invalid date format or date string.</td>
      <td>날짜/시간 유형이 잘못된 경우 발생.</td>
    </tr>
    <tr>
      <td>statement is not opened.</td>
      <td>AppendOpen상태가 아님.</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>바이너리 유형 열에 지정된 크기보다 큰 데이터를 입력하는 경우 발생</td>
    </tr>
    <tr>
      <td>column() truncated :</td>
      <td>varchar 타입 컬럼에 지정된 사이즈 보다 큰 데이터를 입력하는 경우 발생합니다.</td>
    </tr>
    <tr>
      <td>Failed to add stream.</td>
      <td>통신버퍼에 쓰기 오류가 발생합니다.</td>
    </tr>
    <tr>
      <td>IP address length is invalid.</td>
      <td>IPv4, IPv6 유형 구조의 mLength 값이 잘못 지정됩니다.</td>
    </tr>
    <tr>
      <td>IP string is invalid.</td>
      <td>IPv4 또는 IPv6 형식이 아님.</td>
    </tr>
    <tr>
      <td>Unknown data type has been specified.</td>
      <td>Machbase에서 사용하는 데이터 유형이 아님.</td>
    </tr>
  </tbody>
</table>

## 열 형식 매개변수 바인딩

이를 위해서 Machbase 5.5 이후 버전에서는 열 형색 매개변수 바인딩을 지원합니다. (행 형식 매개변수 바인딩은 아직 지원되지 않습니다.)

함수 SQLSetStmtAttr()의 인자 Attribute에 SQL_ATTR_PARAM_BIND_TYPE을 설정하고 인자 param에 SQL_PARAM_BIND_BY_COLUMN을 설정합니다. 바인드할 각  칼럼에 대해서 매개변수를 배열로 설정하고, 지시자 변수 또한 배열로 설정합니다. 이후 SQLBindParameter()를 이 매개변수를 전달하여 호출합니다.

아래 그림은 각 매개변수 배열에 대해 열 형식 바인딩이 동작하는 방식을 보여줍니다.

| Column A<br>(parameter A)             | Column B<br>(parameter B)             | Column C<br>(parameter C)             |
| ------------------------------------- | ------------------------------------- | ------------------------------------- |
| Value_Array<br>Indicator/length array | Value_Array<br>Indicator/length array | Value_Array<br>Indicator/length array |

아래 예제는 열 형식 매개변수 바인딩을 이용하여 대량의 데이터를 삽입하는 예제입니다.

```cpp
#define DESC_LEN 51
#define ARRAY_SIZE 10
SQLCHAR * Statement = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";
 
/* 바인드할 매개변수 배열 */
SQLUINTEGER PartIDArray[ARRAY_SIZE];
SQLCHAR DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL PriceArray[ARRAY_SIZE];
/* 바인드할 지사자 변수 배열 */
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

## 지원되는 문자열

마크베이스는 기본적으로 UTF-8 방식을 사용하여 문자열 데이터를 저장합니다.

UTF-8 이외의 방식으로 문자열을 입/출력하는 Windows의 경우 ODBC에서 아래와 같이 변환합니다.

|    OS   | Unicode/Non-Unicode |   문자열 변환  |                              Note                              |
|:-------:|:-------------------:|:--------------:|:--------------------------------------------------------------:|
| Windows | Unicode (UTF-16)    | UTF-16 ⟷ UTF-8 | N/A                                                            |
| Windows | Non-Unicode (MBCS)  | MBCS ⟷ UTF-8   | Windows 설정의 Non-Unicode 어플리케이션의 기본 문자열을 사용함 |
| Linux   | UTF-8               | N/A            | UTF-8 만 지원됨                                                |
