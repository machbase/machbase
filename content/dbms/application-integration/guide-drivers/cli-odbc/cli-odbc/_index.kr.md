---
type: docs
title: '11.3.1.1 CLI/ODBC 개요'
weight: 10
---

## CLI/ODBC란

CLI(Call Level Interface)는 ISO/IEC 9075-3:2003에 정의된 소프트웨어 개발 표준으로, 데이터베이스에 SQL을 전달하고 결과를 받는 방법을 함수 및 명세로 정의합니다. 가장 널리 알려진 구현체가 ODBC(Open Database Connectivity)이며, 현재 최신 ODBC API 버전은 3.52입니다.

Machbase는 이 표준을 구현한 네이티브 C 라이브러리를 제공합니다. C/C++ 애플리케이션은 이 라이브러리를 통해 Machbase에 직접 연결하여 SQL을 실행하고, 특히 Append API를 통해 초고속 데이터 삽입을 수행할 수 있습니다.

## 헤더 파일 및 라이브러리

Machbase CLI 개발에 필요한 파일은 설치 디렉터리 내에 다음과 같이 위치합니다.

```bash
$MACHBASE_HOME/
├── include/
│   └── machbase_sqlcli.h    # CLI API 헤더 파일
├── lib/
│   ├── libmachbasecli.a     # 정적 라이브러리
│   └── libmachbasecli_dll.so # 공유 라이브러리 (Linux)
└── install/
    └── machbase_env.mk      # Makefile 환경 변수
```

설치 확인:

```bash
$ ls -l $MACHBASE_HOME/include $MACHBASE_HOME/lib
include:
-rwxrwxr-x  machbase_sqlcli.h

lib:
-rw-rw-r--  libmachbasecli.a
-rwxrwxr-x  libmachbasecli_dll.so
```

### Makefile 예제

`$MACHBASE_HOME/install/machbase_env.mk`를 활용하면 컴파일 환경을 간편하게 구성할 수 있습니다.

```makefile
include $(MACHBASE_HOME)/install/machbase_env.mk
INCLUDES += $(LIBDIR_OPT)/$(MACHBASE_HOME)/include

all : myapp

myapp : myapp.o
    $(LD_CC) $(LD_FLAGS) $(LD_OUT_OPT)$@ $< $(LIB_OPT)machbasecli$(LIB_AFT) $(LIBDIR_OPT)$(MACHBASE_HOME)/lib $(LD_LIBS)

myapp.o : myapp.c
    $(COMPILE.cc) $(CC_FLAGS) $(INCLUDES) $(CC_OUT_OPT)$@ $<

clean :
    rm -f myapp
```

공유 라이브러리로 링크해야 하는 경우에는 `$(LIB_OPT)machbasecli_dll$(LIB_AFT)`를
사용합니다.

## 핸들(HANDLE) 종류

CLI는 세 가지 핸들을 사용합니다. 핸들은 각 자원에 대한 참조로, 사용 후 반드시 해제해야 합니다.

| 핸들 타입 | 설명 | 할당 함수 | 해제 함수 |
|-----------|------|-----------|-----------|
| `SQLHENV` (환경 핸들) | CLI 환경 초기화, 최상위 핸들 | `SQLAllocEnv()` | `SQLFreeEnv()` |
| `SQLHDBC` (연결 핸들) | 서버와의 개별 연결 표현 | `SQLAllocConnect()` | `SQLFreeConnect()` |
| `SQLHSTMT` (문장 핸들) | SQL 문장 실행 단위 | `SQLAllocStmt()` | `SQLFreeStmt()` |

핸들의 생명주기는 항상 `HENV → HDBC → HSTMT` 순으로 생성하고, 해제는 반대 순서(`HSTMT → HDBC → HENV`)로 수행합니다.

## 연결 파라미터

`SQLDriverConnect()` 함수에 연결 문자열(Connection String)을 전달하여 서버에 접속합니다.

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| `SERVER` | 서버 호스트명 또는 IP 주소 | `SERVER=127.0.0.1` |
| `PORT_NO` | 접속 포트 번호 | `PORT_NO=5656` |
| `UID` | 사용자 아이디 | `UID=SYS` |
| `PWD` | 사용자 패스워드 | `PWD=MANAGER` |
| `CONNTYPE` | 접속 방식 (1: TCP/IP, 2: Unix Domain) | `CONNTYPE=1` |
| `DBNAME` | DB명 | `DBNAME=machbase` |
| `COMPRESS` | Append 프로토콜 압축 임계값(바이트). 0이면 압축 안 함 | `COMPRESS=512` |
| `CONNECTION_TIMEOUT` | 최초 연결 대기 시간(초). 기본값 30 | `CONNECTION_TIMEOUT=30` |
| `SOCKET_TIMEOUT` | 프로토콜 I/O 타임아웃(초). 기본값 1800 | `SOCKET_TIMEOUT=1800` |
| `SHOW_HIDDEN_COLS` | `SELECT *` 시 `_arrival_time` 컬럼 표시 여부 (0/1) | `SHOW_HIDDEN_COLS=0` |
| `ALTERNATIVE_SERVERS` | 클러스터 환경의 대체 브로커 목록 | `ALTERNATIVE_SERVERS=192.168.0.10:20320` |
| `AUTH_MODE` | 인증 방식 (`PASSWORD` 또는 `CHALLENGE`) | `AUTH_MODE=PASSWORD` |
| `AUTH_KEY_FILE` | Challenge 인증에 사용할 PEM 개인키 파일 경로 | `AUTH_KEY_FILE=/path/to/key.pem` |

연결 문자열 예제:

```c
char connStr[1024];
sprintf(connStr,
    "SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=5656;COMPRESS=512");

if (SQL_ERROR == SQLDriverConnect(gCon, NULL,
                                  (SQLCHAR *)connStr, SQL_NTS,
                                  NULL, 0, NULL,
                                  SQL_DRIVER_NOPROMPT)) {
    /* 에러 처리 */
}
```

## 주요 표준 CLI 함수

Machbase CLI는 다음 표준 함수를 지원합니다.

| | | | |
|--|--|--|--|
| SQLAllocConnect   | SQLDisconnect     | SQLGetDescField  | SQLPrepare        |
| SQLAllocEnv       | SQLDriverConnect  | SQLGetDescRec    | SQLPrimaryKeys    |
| SQLAllocHandle    | SQLExecDirect     | SQLGetDiagRec    | SQLStatistics     |
| SQLAllocStmt      | SQLExecute        | SQLGetEnvAttr    | SQLRowCount       |
| SQLBindCol        | SQLFetch          | SQLGetFunctions  | SQLSetConnectAttr |
| SQLBindParameter  | SQLFreeConnect    | SQLGetInfo       | SQLSetDescField   |
| SQLColAttribute   | SQLFreeEnv        | SQLGetStmtAttr   | SQLSetDescRec     |
| SQLColumns        | SQLFreeHandle     | SQLGetTypeInfo   | SQLSetEnvAttr     |
| SQLConnect        | SQLFreeStmt       | SQLNativeSQL     | SQLSetStmtAttr    |
| SQLCopyDesc       | SQLGetConnectAttr | SQLNumParams     | SQLTables         |
| SQLDescribeCol    | SQLGetData        | SQLNumResultCols | SQLError          |

### 핵심 함수 상세

#### SQLAllocEnv

```c
SQLRETURN SQLAllocEnv(SQLHENV *EnvironmentHandle);
```

CLI 환경 핸들을 할당합니다. 모든 CLI 작업의 시작점으로 가장 먼저 호출해야 합니다.

#### SQLAllocConnect

```c
SQLRETURN SQLAllocConnect(SQLHENV EnvironmentHandle, SQLHDBC *ConnectionHandle);
```

연결 핸들을 할당합니다. `SQLAllocEnv()` 성공 후 호출합니다.

#### SQLDriverConnect

```c
SQLRETURN SQLDriverConnect(SQLHDBC ConnectionHandle,
                           SQLHWND WindowHandle,
                           SQLCHAR *InConnectionString,
                           SQLSMALLINT StringLength1,
                           SQLCHAR *OutConnectionString,
                           SQLSMALLINT BufferLength,
                           SQLSMALLINT *StringLength2Ptr,
                           SQLUSMALLINT DriverCompletion);
```

연결 문자열을 사용하여 Machbase 서버에 접속합니다. `DriverCompletion`에는 `SQL_DRIVER_NOPROMPT`를 사용합니다.

#### SQLAllocStmt

```c
SQLRETURN SQLAllocStmt(SQLHDBC ConnectionHandle, SQLHSTMT *StatementHandle);
```

SQL 문장 실행을 위한 Statement 핸들을 할당합니다.

#### SQLExecDirect

```c
SQLRETURN SQLExecDirect(SQLHSTMT StatementHandle,
                        SQLCHAR *StatementText,
                        SQLINTEGER TextLength);
```

SQL 문자열을 즉시 실행합니다. 한 번만 실행할 SQL에 적합합니다.

#### SQLPrepare / SQLExecute

```c
SQLRETURN SQLPrepare(SQLHSTMT StatementHandle,
                     SQLCHAR *StatementText,
                     SQLINTEGER TextLength);

SQLRETURN SQLExecute(SQLHSTMT StatementHandle);
```

SQL을 미리 파싱(Prepare)한 후 반복 실행(Execute)할 때 사용합니다. 동일한 SQL을 파라미터만 바꾸며 여러 번 실행할 때 효율적입니다.

#### SQLBindCol

```c
SQLRETURN SQLBindCol(SQLHSTMT StatementHandle,
                     SQLUSMALLINT ColumnNumber,
                     SQLSMALLINT TargetType,
                     SQLPOINTER TargetValuePtr,
                     SQLLEN BufferLength,
                     SQLLEN *StrLen_or_IndPtr);
```

SELECT 결과의 컬럼을 C 변수에 바인딩합니다. `SQLFetch()` 호출 시 해당 변수에 값이 채워집니다.

#### SQLFetch

```c
SQLRETURN SQLFetch(SQLHSTMT StatementHandle);
```

쿼리 결과에서 다음 행을 가져옵니다. `SQL_SUCCESS`가 반환되는 동안 루프를 반복합니다.

#### SQLFreeStmt

```c
SQLRETURN SQLFreeStmt(SQLHSTMT StatementHandle, SQLUSMALLINT Option);
```

Statement 핸들을 해제합니다. `Option`에 `SQL_DROP`을 사용하면 핸들이 완전히 해제됩니다.

#### SQLDisconnect

```c
SQLRETURN SQLDisconnect(SQLHDBC ConnectionHandle);
```

서버와의 연결을 끊습니다. 이후 `SQLFreeConnect()`, `SQLFreeEnv()`를 순서대로 호출합니다.

## 에러 처리

CLI 함수가 `SQL_ERROR`를 반환하면 `SQLError()` 함수로 상세 에러 정보를 확인합니다.

```c
SQLRETURN SQLError(SQLHENV EnvironmentHandle,
                   SQLHDBC ConnectionHandle,
                   SQLHSTMT StatementHandle,
                   SQLCHAR *Sqlstate,
                   SQLINTEGER *NativeError,
                   SQLCHAR *MessageText,
                   SQLSMALLINT BufferLength,
                   SQLSMALLINT *TextLength);
```

사용 예:

```c
SQLINTEGER  errNo;
SQLSMALLINT msgLength;
SQLCHAR     sqlState[6];
SQLCHAR     errMsg[1024];

if (SQL_SUCCESS == SQLError(gEnv, gCon, gStmt,
                            sqlState, &errNo,
                            errMsg, sizeof(errMsg), &msgLength))
{
    printf("ERROR-%05d: %s\n", errNo, errMsg);
}
```

에러 처리를 포함한 유틸리티 함수 패턴:

```c
void outError(const char *aMsg, SQLHSTMT aStmt)
{
    SQLINTEGER  errNo;
    SQLSMALLINT msgLength;
    SQLCHAR     errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError(gEnv, gCon, aStmt, NULL,
                                &errNo, errMsg, sizeof(errMsg), &msgLength))
    {
        printf("mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}
```

## 확장 CLI 함수 (Append API)

Append API는 Machbase 전용 고속 데이터 입력 프로토콜입니다. 비동기 버퍼링 방식으로 동작하여 일반 INSERT보다 수십 배 이상 높은 처리량을 제공합니다.

### Append 프로토콜의 동작 방식

Append 프로토콜은 **비동기(Asynchronous)** 방식으로 동작합니다.

- 클라이언트가 `SQLAppendDataV2()`를 호출해도 즉시 서버로 전송되지 않습니다.
- 내부 통신 버퍼가 가득 찰 때까지 데이터를 누적하다가 한꺼번에 전송합니다.
- 이 방식은 초당 수만~수십만 건의 레코드 입력을 가정하여 설계되었습니다.

에러는 다음 세 시점에만 검출됩니다.

1. 통신 버퍼가 가득 차서 데이터를 서버로 전송한 직후
2. `SQLAppendFlush()` 호출 후 명시적 전송 직후
3. `SQLAppendClose()` 호출 시 채널 종료 직전

에러가 발생하면 `SQLAppendSetErrorCallback()`으로 등록한 콜백 함수가 호출됩니다.

### SQLAppendOpen

```c
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount);
```

대상 테이블에 대한 Append 채널을 엽니다.

- `aStatementHandle`: Append를 수행할 Statement 핸들
- `aTableName`: Append 대상 테이블 이름
- `aErrorCheckCount`: N번 Append마다 서버 에러를 검사. `0`이면 기본 동작(버퍼 전송 시에만 검사)

### SQLAppendDataV2

```c
SQLRETURN SQLAppendDataV2(SQLHSTMT StatementHandle, SQL_APPEND_PARAM *aData);
```

Append 채널에 데이터를 입력합니다. `aData`는 테이블의 컬럼 수와 동일한 크기의 `SQL_APPEND_PARAM` 배열입니다.

`SQL_APPEND_PARAM`은 모든 데이터 타입을 담을 수 있는 공용 구조체(union)입니다.

```c
typedef union machbaseAppendParam {
    short                        mShort;
    unsigned short               mUShort;
    int                          mInteger;
    unsigned int                 mUInteger;
    long long                    mLong;
    unsigned long long           mULong;
    float                        mFloat;
    double                       mDouble;
    machbaseAppendIPStruct       mIP;
    machbaseAppendVarStruct      mVar;
    machbaseAppendVarStruct      mVarchar;
    machbaseAppendVarStruct      mText;
    machbaseAppendVarStruct      mJson;
    machbaseAppendVarStruct      mBinary;
    machbaseAppendDateTimeStruct mDateTime;
} machbaseAppendParam;

#define SQL_APPEND_PARAM machbaseAppendParam
```

#### 고정 길이 숫자형 타입

| DB 타입 | NULL 매크로 | SQL_APPEND_PARAM 멤버 |
|---------|------------|----------------------|
| SHORT | `SQL_APPEND_SHORT_NULL` | `mShort` |
| USHORT | `SQL_APPEND_USHORT_NULL` | `mUShort` |
| INTEGER | `SQL_APPEND_INTEGER_NULL` | `mInteger` |
| UINTEGER | `SQL_APPEND_UINTEGER_NULL` | `mUInteger` |
| LONG | `SQL_APPEND_LONG_NULL` | `mLong` |
| ULONG | `SQL_APPEND_ULONG_NULL` | `mULong` |
| FLOAT | `SQL_APPEND_FLOAT_NULL` | `mFloat` |
| DOUBLE | `SQL_APPEND_DOUBLE_NULL` | `mDouble` |

```c
SQL_APPEND_PARAM sParam[8];

/* NULL 입력 */
sParam[0].mShort   = SQL_APPEND_SHORT_NULL;
sParam[1].mInteger = SQL_APPEND_INTEGER_NULL;
sParam[2].mLong    = SQL_APPEND_LONG_NULL;
sParam[3].mFloat   = SQL_APPEND_FLOAT_NULL;
sParam[4].mDouble  = SQL_APPEND_DOUBLE_NULL;

/* 실제 값 입력 */
sParam[0].mShort   = 10;
sParam[1].mInteger = 200;
sParam[2].mLong    = 3000LL;
sParam[3].mFloat   = 1.5f;
sParam[4].mDouble  = 3.14;

SQLAppendDataV2(gStmt, sParam);
```

#### DATETIME 타입

`mDateTime.mTime` 멤버에 다음 매크로 또는 나노초 값을 설정합니다.

| 매크로 | 설명 |
|--------|------|
| `SQL_APPEND_DATETIME_NOW` | 현재 클라이언트 시간 |
| `SQL_APPEND_DATETIME_STRING` | `mDateStr`, `mFormatStr`을 이용한 문자열 파싱 |
| `SQL_APPEND_DATETIME_STRUCT_TM` | `mTM` (struct tm) 값을 변환하여 입력 |
| `SQL_APPEND_DATETIME_NULL` | NULL 입력 |
| 임의의 64비트 정수 | 1970-01-01 기준 나노초 단위 절대 시간 |

```c
SQL_APPEND_PARAM sParam[1];

/* 현재 시간 */
sParam[0].mDateTime.mTime = SQL_APPEND_DATETIME_NOW;
SQLAppendDataV2(gStmt, sParam);

/* 문자열 파싱 */
sParam[0].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
sParam[0].mDateTime.mDateStr   = "2024-07-01 12:00:00";
sParam[0].mDateTime.mFormatStr = "YYYY-MM-DD HH24:MI:SS";
SQLAppendDataV2(gStmt, sParam);

/* 나노초 절대값 */
sParam[0].mDateTime.mTime = 1719835200000000000LL; /* 2024-07-01 00:00:00 UTC */
SQLAppendDataV2(gStmt, sParam);
```

> **참고**: Machbase 시간 = (Unix 타임스탬프 초) × 1,000,000,000 + 나노초

#### IP 주소 타입

`mIP.mLength` 에 다음 매크로를 설정합니다.

| 매크로 | 설명 |
|--------|------|
| `SQL_APPEND_IP_NULL` | NULL 입력 |
| `SQL_APPEND_IP_IPV4` | `mAddr`에 IPv4 바이너리 주소 (4바이트) |
| `SQL_APPEND_IP_IPV6` | `mAddr`에 IPv6 바이너리 주소 (16바이트) |
| `SQL_APPEND_IP_STRING` | `mAddrString`에 IP 문자열 |

```c
SQL_APPEND_PARAM sParam[1];

/* 문자열로 IPv4 입력 */
sParam[0].mIP.mLength     = SQL_APPEND_IP_STRING;
sParam[0].mIP.mAddrString = "192.168.0.1";
SQLAppendDataV2(gStmt, sParam);

/* 바이너리로 IPv4 입력 */
sParam[0].mIP.mLength  = SQL_APPEND_IP_IPV4;
*(in_addr_t *)(sParam[0].mIP.mAddr) = inet_addr("10.0.0.1");
SQLAppendDataV2(gStmt, sParam);
```

> **주의**: 문자열(`SQL_APPEND_IP_STRING`)로 입력하면 `SQLAppendDataV2()` 호출 후 `mLength`가 4 또는 6으로 변경됩니다. 루프 내에서 사용할 경우 매번 `mLength`를 `SQL_APPEND_IP_STRING`으로 재설정해야 합니다.

#### 가변 길이 타입 (VARCHAR, TEXT, BINARY 등)

`mVar.mLength`에 데이터 길이, `mVar.mData`에 데이터 포인터를 설정합니다.

| DB 타입 | NULL 매크로 | SQL_APPEND_PARAM 멤버 |
|---------|------------|----------------------|
| VARCHAR | `SQL_APPEND_VARCHAR_NULL` | `mVarchar` |
| TEXT | `SQL_APPEND_TEXT_NULL` | `mText` |
| JSON | `SQL_APPEND_JSON_NULL` | `mJson` |
| BINARY | `SQL_APPEND_BINARY_NULL` | `mBinary` |

```c
SQL_APPEND_PARAM sParam[1];
char sVarchar[20] = "hello machbase";

sParam[0].mVarchar.mLength = strlen(sVarchar);
sParam[0].mVarchar.mData   = sVarchar;
SQLAppendDataV2(gStmt, sParam);
```

### SQLAppendDataByTimeV2

```c
SQLRETURN SQLAppendDataByTimeV2(SQLHSTMT StatementHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData);
```

`_arrival_time` 컬럼의 값을 현재 시간이 아닌 특정 시간으로 지정하여 데이터를 입력합니다. 과거 로그 파일을 당시 시각 기준으로 재입력할 때 유용합니다.

- `aTime`: 1970-01-01 기준 나노초 단위 시간. 입력 데이터는 시간 순으로 정렬되어 있어야 합니다.

### SQLAppendFlush

```c
SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
```

현재 채널의 버퍼에 쌓인 데이터를 즉시 서버로 전송합니다. 버퍼가 가득 차지 않은 상태에서 강제로 데이터를 보내야 할 때 사용합니다.

### SQLAppendClose

```c
SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT *aSuccessCount,
                         SQLBIGINT *aFailureCount);
```

Append 채널을 닫습니다.

- `aSuccessCount`: 성공한 레코드 수
- `aFailureCount`: 실패한 레코드 수

### SQLAppendSetErrorCallback

```c
SQLRETURN SQLAppendSetErrorCallback(SQLHSTMT aStmtHandle,
                                    SQLAppendErrorCallback aFunc);
```

Append 에러 발생 시 호출할 콜백 함수를 등록합니다. 이 함수를 설정하지 않으면 서버에서 에러가 발생해도 클라이언트에서 무시됩니다.

콜백 함수 프로토타입:

```c
typedef void (*SQLAppendErrorCallback)(SQLHSTMT   aStmtHandle,
                                       SQLINTEGER  aErrorCode,
                                       SQLPOINTER  aErrorMessage,
                                       SQLLEN      aErrorBufLen,
                                       SQLPOINTER  aRowBuf,
                                       SQLLEN      aRowBufLen);
```

- `aErrorCode`: 에러 코드 (32비트 정수)
- `aErrorMessage`: 에러 메시지 문자열
- `aRowBuf`: 에러를 유발한 레코드 명세 문자열

에러 콜백 등록 예제:

```c
void dumpError(SQLHSTMT   aStmtHandle,
               SQLINTEGER  aErrorCode,
               SQLPOINTER  aErrorMessage,
               SQLLEN      aErrorBufLen,
               SQLPOINTER  aRowBuf,
               SQLLEN      aRowBufLen)
{
    char sErrMsg[1024] = {0};
    char sRowMsg[32 * 1024] = {0};

    if (aErrorMessage != NULL)
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);

    if (aRowBuf != NULL)
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);

    fprintf(stderr, "Append Error: [%d][%s]\n[%s]\n", aErrorCode, sErrMsg, sRowMsg);
}

/* 사용 예 */
SQLAppendOpen(gStmt, (SQLCHAR *)"MY_TABLE", 100);
SQLAppendSetErrorCallback(gStmt, dumpError);
```

### SQLSetConnectAppendFlush

```c
SQLRETURN SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option);
```

100ms 주기로 마지막 전송 시간을 확인하여 일정 시간(기본 1초)이 지나면 자동으로 버퍼를 서버에 전송하는 기능을 켜거나 끕니다.

- `option`: 0이면 자동 플러시 off, 0이 아닌 값이면 on

### SQLSetStmtAppendInterval

```c
SQLRETURN SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue);
```

특정 Statement에 대한 자동 플러시 주기를 밀리초 단위로 설정합니다. 0이면 자동 플러시 비활성화, 100의 배수로 설정을 권장하며 기본값은 1000ms입니다.

### Append 에러 메시지 참조

| 함수 | 에러 메시지 | 설명 |
|------|------------|------|
| SQLAppendOpen | `statement is already opened.` | 중복 SQLAppendOpen 호출 |
| SQLAppendOpen | `Failed to read protocol.` | 네트워크 읽기 오류 |
| SQLAppendOpen | `cannot allocate memory.` | 내부 버퍼 메모리 할당 실패 |
| SQLAppendData | `statement is not opened.` | SQLAppendOpen 없이 호출 |
| SQLAppendData | `column() truncated :` | VARCHAR 컬럼 길이 초과 |
| SQLAppendClose | `statement is not opened.` | AppendOpen 상태가 아님 |
| SQLAppendClose | `Failed to close stream protocol.` | 스트림 프로토콜 종료 실패 |
| SQLAppendFlush | `statement is not opened.` | AppendOpen 상태가 아님 |
| SQLAppendDataV2 | `Invalid date format or date string.` | 날짜/시간 형식 오류 |
| SQLAppendDataV2 | `IP address length is invalid.` | IP 타입 mLength 값 오류 |
| SQLAppendDataV2 | `IP string is invalid.` | 유효하지 않은 IP 문자열 |

## 열 형식 파라미터 바인딩

Machbase 5.5 이후 버전에서는 열 형식(column-wise) 파라미터 바인딩을 지원합니다. 이를 이용하면 배열 단위로 대량 INSERT를 수행할 수 있습니다.

```c
#define ARRAY_SIZE 10
#define DESC_LEN   51

SQLCHAR * sSQL = "INSERT INTO Parts (PartID, Description, Price) VALUES (?, ?, ?)";

SQLUINTEGER  PartIDArray[ARRAY_SIZE];
SQLCHAR      DescArray[ARRAY_SIZE][DESC_LEN];
SQLREAL      PriceArray[ARRAY_SIZE];
SQLINTEGER   PartIDIndArray[ARRAY_SIZE];
SQLINTEGER   DescLenOrIndArray[ARRAY_SIZE];
SQLINTEGER   PriceIndArray[ARRAY_SIZE];
SQLUSMALLINT ParamStatusArray[ARRAY_SIZE];
SQLUINTEGER  ParamsProcessed;

/* 열 형식 바인딩 설정 */
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE,
               SQL_PARAM_BIND_BY_COLUMN, 0);
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE,
               ARRAY_SIZE, 0);
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR,
               ParamStatusArray, 0);
SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR,
               &ParamsProcessed, 0);

/* 각 컬럼 배열을 파라미터로 바인딩 */
SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER,
                 5, 0, PartIDArray, 0, PartIDIndArray);
SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR,
                 DESC_LEN - 1, 0, DescArray, DESC_LEN, DescLenOrIndArray);
SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL,
                 7, 0, PriceArray, 0, PriceIndArray);
```

## 문자열 인코딩

Machbase는 기본적으로 UTF-8 방식으로 문자열을 저장합니다.

| OS | Unicode 방식 | 변환 |
|:---:|:---:|:---:|
| Windows | Unicode (UTF-16) | UTF-16 ↔ UTF-8 |
| Windows | Non-Unicode (MBCS) | MBCS ↔ UTF-8 |
| Linux | UTF-8 | 변환 없음 |
