---
type: docs
title: '12.3 드라이버별 가이드'
weight: 30
toc: true
---
Machbase에 연결하기 위한 각 드라이버 및 SDK의 사용 방법을 다룹니다. C/C++ 네이티브 환경부터 Java, Python, Go 등 다양한 언어별 연결 방식을 제공합니다.

Machbase 8.6.0 Standard Edition에서는 하나의 인스턴스에 여러 logical database를 둘 수
있습니다. 초기 database 옵션과 `USE`, 3-part table 이름, pool/handle binding 규칙은
[다중 데이터베이스 운영 가이드](/dbms/operations-configuration-recovery/multi-database/)를
먼저 확인하십시오. 연결 직후 `CURRENT_DATABASE()`를 실행해 server catalog를 검증합니다.

## 지원 드라이버 목록

| 드라이버 / SDK | 언어 | 연결 방식 | Append 지원 | 특징 |
|----------------|------|-----------|:-----------:|------|
| [CLI/ODBC](/dbms/application-integration/guide-drivers/#cli-odbc) | C / C++ | 네이티브 라이브러리 | 지원 | 직접 연결과 Append API 제공 |
| JDBC | Java | TCP/IP | 지원 | 표준 JDBC 인터페이스. `MachStatement` Append API 제공 |
| Python | Python | TCP/IP | 지원 | `machbaseAPI` 패키지 제공. 데이터 분석 환경에 적합 |
| Go | Go | TCP/IP | native 기본, SQL driver 확장 가능 | `machgo` Appender 제공. `database/sql`은 표준 SQL과 `sql.Conn.Raw()` Appender 확장 제공 |
| Node.js | JavaScript / TypeScript | TCP/IP | 지원 | `@machbase/ts-client` 패키지 제공 |
| REST API | 모든 언어 | HTTP | 지원 | `/machbase` POST Append 지원. 별도 드라이버 불필요 |

## 드라이버 선택 가이드

### 고성능 시계열 데이터 수집이 목적인 경우

지속적인 대량 시계열 데이터를 입력하고 버퍼와 flush 시점을 직접 제어해야 한다면
**CLI/ODBC의 Append API**를 검토합니다. Append 프로토콜은 여러 행을 버퍼링하여 반복 INSERT의
네트워크 왕복과 SQL 파싱 횟수를 줄입니다.

### 기존 Java 애플리케이션과 통합하는 경우

**JDBC 드라이버**를 사용하면 표준 `java.sql` 인터페이스를 그대로 활용할 수 있습니다. Spring, MyBatis 등 Java 생태계와의 통합이 용이합니다.

### 데이터 분석 및 빠른 개발이 목적인 경우

**Python 패키지** 또는 **REST API**를 사용하면 별도의 컴파일 없이 빠르게 프로토타입을 작성하고 분석 결과를 확인할 수 있습니다.

## 공통 연결 정보

모든 드라이버는 다음 정보를 사용하여 Machbase 서버에 연결합니다.

| 항목 | 기본값 | 설명 |
|------|--------|------|
| HOST | 127.0.0.1 | Machbase 서버의 호스트명 또는 IP 주소 |
| PORT | 5656 | Machbase 서버 포트 번호 (machbase.conf의 PORT_NO) |
| USER | SYS | 사용자 아이디 |
| PASSWORD | MANAGER | 사용자 패스워드 |


<a id="cli-odbc"></a>

## CLI/ODBC

CLI(Call Level Interface)는 [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003에 정의된 데이터베이스 접속 표준입니다. 이 표준을 구현한 네이티브 C 라이브러리를 통해 C/C++ 애플리케이션에서 직접 Machbase에 연결하고 데이터를 처리할 수 있습니다.

### 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [CLI/ODBC 개요](/dbms/application-integration/guide-drivers/#cli-odbc) | 헤더 파일, 라이브러리, 주요 API 함수, 연결 파라미터, Append API 상세 설명 |
| [CLI/ODBC 예제](/dbms/application-integration/guide-drivers/#examples-cli-odbc) | 접속/해제, INSERT/SELECT, Append 고속 삽입 등 실용적인 예제 코드 |

### CLI/ODBC의 특징

- **네이티브 성능**: 별도의 미들웨어 없이 Machbase 서버와 직접 통신
- **Append API**: 여러 시계열 행을 버퍼링하여 전송하는 전용 입력 프로토콜
- **표준 호환**: ODBC 3.52 표준을 기반으로 설계되어 익숙한 SQL CLI 패턴 적용 가능
- **C/C++ 지원**: `machbase_sqlcli.h` 헤더와 `libmachbasecli.a` 또는
  `libmachbasecli_dll.so` 라이브러리 제공

### 빠른 시작

Machbase가 설치된 환경에서는 다음 경로에 CLI 개발에 필요한 파일이 포함되어 있습니다.

```bash
$MACHBASE_HOME/include/machbase_sqlcli.h   # 헤더 파일
$MACHBASE_HOME/lib/libmachbasecli.a        # 정적 라이브러리
$MACHBASE_HOME/lib/libmachbasecli_dll.so   # 공유 라이브러리 (Linux)
```

컴파일 시 다음과 같이 라이브러리를 링크합니다.

```bash
gcc -o myapp myapp.c \
    -I$MACHBASE_HOME/include \
    -L$MACHBASE_HOME/lib \
    -lmachbasecli -lm -lpthread -ldl -lrt -rdynamic
```

공유 라이브러리로 링크할 때는 `-lmachbasecli_dll`을 사용합니다.

<a id="cli-odbc-cli-odbc"></a>

### CLI/ODBC 개요

#### CLI/ODBC란

CLI(Call Level Interface)는 ISO/IEC 9075-3:2003에 정의된 소프트웨어 개발 표준으로, 데이터베이스에 SQL을 전달하고 결과를 받는 방법을 함수 및 명세로 정의합니다. 가장 널리 알려진 구현체가 ODBC(Open Database Connectivity)이며, 현재 최신 ODBC API 버전은 3.52입니다.

이 표준을 구현한 네이티브 C 라이브러리를 제공합니다. C/C++ 애플리케이션은 이 라이브러리를 통해 직접 연결하여 SQL을 실행하고, Append API를 통해 초고속 데이터 삽입을 수행할 수 있습니다.

#### 헤더 파일 및 라이브러리

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

##### Makefile 예제

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

#### 핸들(HANDLE) 종류

CLI는 세 가지 핸들을 사용합니다. 핸들은 각 자원에 대한 참조로, 사용 후 반드시 해제해야 합니다.

| 핸들 타입 | 설명 | 할당 함수 | 해제 함수 |
|-----------|------|-----------|-----------|
| `SQLHENV` (환경 핸들) | CLI 환경 초기화, 최상위 핸들 | `SQLAllocEnv()` | `SQLFreeEnv()` |
| `SQLHDBC` (연결 핸들) | 서버와의 개별 연결 표현 | `SQLAllocConnect()` | `SQLFreeConnect()` |
| `SQLHSTMT` (문장 핸들) | SQL 문장 실행 단위 | `SQLAllocStmt()` | `SQLFreeStmt()` |

핸들의 생명주기는 항상 `HENV → HDBC → HSTMT` 순으로 생성하고, 해제는 반대 순서(`HSTMT → HDBC → HENV`)로 수행합니다.

#### 연결 파라미터

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

#### 주요 표준 CLI 함수

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

##### 핵심 함수 상세

###### SQLAllocEnv

```c
SQLRETURN SQLAllocEnv(SQLHENV *EnvironmentHandle);
```

CLI 환경 핸들을 할당합니다. 모든 CLI 작업의 시작점으로 가장 먼저 호출해야 합니다.

###### SQLAllocConnect

```c
SQLRETURN SQLAllocConnect(SQLHENV EnvironmentHandle, SQLHDBC *ConnectionHandle);
```

연결 핸들을 할당합니다. `SQLAllocEnv()` 성공 후 호출합니다.

###### SQLDriverConnect

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

###### SQLAllocStmt

```c
SQLRETURN SQLAllocStmt(SQLHDBC ConnectionHandle, SQLHSTMT *StatementHandle);
```

SQL 문장 실행을 위한 Statement 핸들을 할당합니다.

###### SQLExecDirect

```c
SQLRETURN SQLExecDirect(SQLHSTMT StatementHandle,
                        SQLCHAR *StatementText,
                        SQLINTEGER TextLength);
```

SQL 문자열을 즉시 실행합니다. 한 번만 실행할 SQL에 적합합니다.

###### SQLPrepare / SQLExecute

```c
SQLRETURN SQLPrepare(SQLHSTMT StatementHandle,
                     SQLCHAR *StatementText,
                     SQLINTEGER TextLength);

SQLRETURN SQLExecute(SQLHSTMT StatementHandle);
```

SQL을 미리 파싱(Prepare)한 후 반복 실행(Execute)할 때 사용합니다. 동일한 SQL을 파라미터만 바꾸며 여러 번 실행할 때 효율적입니다.

###### SQLBindCol

```c
SQLRETURN SQLBindCol(SQLHSTMT StatementHandle,
                     SQLUSMALLINT ColumnNumber,
                     SQLSMALLINT TargetType,
                     SQLPOINTER TargetValuePtr,
                     SQLLEN BufferLength,
                     SQLLEN *StrLen_or_IndPtr);
```

SELECT 결과의 컬럼을 C 변수에 바인딩합니다. `SQLFetch()` 호출 시 해당 변수에 값이 채워집니다.

###### SQLFetch

```c
SQLRETURN SQLFetch(SQLHSTMT StatementHandle);
```

쿼리 결과에서 다음 행을 가져옵니다. `SQL_SUCCESS`가 반환되는 동안 루프를 반복합니다.

###### SQLFreeStmt

```c
SQLRETURN SQLFreeStmt(SQLHSTMT StatementHandle, SQLUSMALLINT Option);
```

Statement 핸들을 해제합니다. `Option`에 `SQL_DROP`을 사용하면 핸들이 완전히 해제됩니다.

###### SQLDisconnect

```c
SQLRETURN SQLDisconnect(SQLHDBC ConnectionHandle);
```

서버와의 연결을 끊습니다. 이후 `SQLFreeConnect()`, `SQLFreeEnv()`를 순서대로 호출합니다.

#### 에러 처리

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

#### 확장 CLI 함수 (Append API)

Append API는 Machbase 전용 데이터 입력 프로토콜입니다. 여러 행을 통신 버퍼에 모아 전송하여
반복 INSERT의 네트워크 왕복과 SQL 파싱 횟수를 줄입니다.

##### Append 프로토콜의 동작 방식

Append 프로토콜은 **비동기(Asynchronous)** 방식으로 동작합니다.

- 클라이언트가 `SQLAppendDataV2()`를 호출해도 즉시 서버로 전송되지 않습니다.
- 내부 통신 버퍼가 가득 찰 때까지 데이터를 누적하다가 한꺼번에 전송합니다.
- 처리량과 flush 지연은 행 크기, 버퍼 크기, 네트워크와 서버 자원으로 측정합니다.

에러는 다음 세 시점에만 검출됩니다.

1. 통신 버퍼가 가득 차서 데이터를 서버로 전송한 직후
2. `SQLAppendFlush()` 호출 후 명시적 전송 직후
3. `SQLAppendClose()` 호출 시 채널 종료 직전

에러가 발생하면 `SQLAppendSetErrorCallback()`으로 등록한 콜백 함수가 호출됩니다.

##### SQLAppendOpen

```c
SQLRETURN SQLAppendOpen(SQLHSTMT   aStatementHandle,
                        SQLCHAR   *aTableName,
                        SQLINTEGER aErrorCheckCount);
```

대상 테이블에 대한 Append 채널을 엽니다.

- `aStatementHandle`: Append를 수행할 Statement 핸들
- `aTableName`: Append 대상 테이블 이름
- `aErrorCheckCount`: N번 Append마다 서버 에러를 검사. `0`이면 기본 동작(버퍼 전송 시에만 검사)

##### SQLAppendDataV2

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

###### 고정 길이 숫자형 타입

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

###### DATETIME 타입

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

###### IP 주소 타입

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

###### 가변 길이 타입 (VARCHAR, TEXT, BINARY 등)

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

##### SQLAppendDataByTimeV2

```c
SQLRETURN SQLAppendDataByTimeV2(SQLHSTMT StatementHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData);
```

`_arrival_time` 컬럼의 값을 현재 시간이 아닌 특정 시간으로 지정하여 데이터를 입력합니다. 과거 로그 파일을 당시 시각 기준으로 재입력할 때 유용합니다.

- `aTime`: 1970-01-01 기준 나노초 단위 시간. 입력 데이터는 시간 순으로 정렬되어 있어야 합니다.

##### SQLAppendFlush

```c
SQLRETURN SQLAppendFlush(SQLHSTMT StatementHandle);
```

현재 채널의 버퍼에 쌓인 데이터를 즉시 서버로 전송합니다. 버퍼가 가득 차지 않은 상태에서 강제로 데이터를 보내야 할 때 사용합니다.

##### SQLAppendClose

```c
SQLRETURN SQLAppendClose(SQLHSTMT   aStmtHandle,
                         SQLBIGINT *aSuccessCount,
                         SQLBIGINT *aFailureCount);
```

Append 채널을 닫습니다.

- `aSuccessCount`: 성공한 레코드 수
- `aFailureCount`: 실패한 레코드 수

##### SQLAppendSetErrorCallback

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

##### SQLSetConnectAppendFlush

```c
SQLRETURN SQLSetConnectAppendFlush(SQLHDBC hdbc, SQLINTEGER option);
```

100ms 주기로 마지막 전송 시간을 확인하여 일정 시간(기본 1초)이 지나면 자동으로 버퍼를 서버에 전송하는 기능을 켜거나 끕니다.

- `option`: 0이면 자동 플러시 off, 0이 아닌 값이면 on

##### SQLSetStmtAppendInterval

```c
SQLRETURN SQLSetStmtAppendInterval(SQLHSTMT hstmt, SQLINTEGER fValue);
```

특정 Statement에 대한 자동 플러시 주기를 밀리초 단위로 설정합니다. 0이면 자동 플러시 비활성화, 100의 배수로 설정을 권장하며 기본값은 1000ms입니다.

##### Append 에러 메시지 참조

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

#### 열 형식 파라미터 바인딩

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

#### 문자열 인코딩

Machbase는 기본적으로 UTF-8 방식으로 문자열을 저장합니다.

| OS | Unicode 방식 | 변환 |
|:---:|:---:|:---:|
| Windows | Unicode (UTF-16) | UTF-16 ↔ UTF-8 |
| Windows | Non-Unicode (MBCS) | MBCS ↔ UTF-8 |
| Linux | UTF-8 | 변환 없음 |

<a id="examples-cli-odbc"></a>
<a id="cli-odbc-examples-cli-odbc"></a>

### CLI/ODBC 예제

Machbase CLI를 사용하는 C 프로그램의 대표적인 예제입니다. 모든 예제는 `machbase_sqlcli.h`를 포함하고 정적 라이브러리는 `libmachbasecli`, 공유 라이브러리는 `libmachbasecli_dll`과 링크하여 컴파일합니다.

#### 개발 환경 준비

##### 설치 확인

Machbase가 설치된 디렉터리의 `include`와 `lib`에 다음 파일이 있으면 개발 환경이 준비된 것입니다.

```bash
$ ls $MACHBASE_HOME/include $MACHBASE_HOME/lib

include:
  machbase_sqlcli.h

lib:
  libmachbasecli.a
  libmachbasecli_dll.so
```

##### Makefile 작성

`$MACHBASE_HOME/sample/cli/` 경로에 기본 샘플과 Makefile이 포함되어 있습니다. 아래는 Makefile의 기본 형식입니다.

```makefile
include $(MACHBASE_HOME)/install/machbase_env.mk
INCLUDES += $(LIBDIR_OPT)/$(MACHBASE_HOME)/include

all : sample1_connect sample2_insert sample4_append1

sample1_connect : sample1_connect.o
    $(LD_CC) $(LD_FLAGS) $(LD_OUT_OPT)$@ $< $(LIB_OPT)machbasecli$(LIB_AFT) $(LIBDIR_OPT)$(MACHBASE_HOME)/lib $(LD_LIBS)

sample1_connect.o : sample1_connect.c
    $(COMPILE.cc) $(CC_FLAGS) $(INCLUDES) $(CC_OUT_OPT)$@ $<

clean :
    rm -f sample1_connect sample2_insert sample4_append1
```

##### 컴파일

```bash
$ cd $MACHBASE_HOME/sample/cli
$ make
```

---

#### 예제 1: 접속 및 해제 (sample1_connect.c)

가장 기본적인 패턴으로, Machbase 서버에 접속하고 해제하는 과정을 보여줍니다.

핸들 생성 순서는 반드시 `HENV → HDBC → HSTMT`이며, 해제는 반대 순서입니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;

void connectDB()
{
    char        connStr[1024];
    SQLINTEGER  errNo;
    SQLSMALLINT msgLength;
    SQLCHAR     errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(connStr,
            "SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d",
            MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect(gCon, NULL,
                                      (SQLCHAR *)connStr, SQL_NTS,
                                      NULL, 0, NULL,
                                      SQL_DRIVER_NOPROMPT))
    {
        printf("connection error\n");
        if (SQL_SUCCESS == SQLError(gEnv, gCon, NULL, NULL, &errNo,
                                    errMsg, sizeof(errMsg), &msgLength))
        {
            printf("mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    printf("connected ...\n");
}

void disconnectDB()
{
    SQLINTEGER  errNo;
    SQLSMALLINT msgLength;
    SQLCHAR     errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");
        if (SQL_SUCCESS == SQLError(gEnv, gCon, NULL, NULL, &errNo,
                                    errMsg, sizeof(errMsg), &msgLength))
        {
            printf("mach-%d : %s\n", errNo, errMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

int main()
{
    connectDB();
    disconnectDB();
    return 0;
}
```

실행 결과:

```
connected ...
```

---

#### 예제 2: 테이블 생성, INSERT, SELECT (sample2_insert.c)

테이블을 생성하고 문자열 포맷으로 데이터를 삽입한 뒤 SELECT로 조회합니다. 에러 처리 유틸리티 함수(`outError`, `executeDirectSQL`)를 함께 보여줍니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;

/* 에러 출력 후 프로그램 종료 */
void outError(const char *aMsg, SQLHSTMT aStmt)
{
    SQLINTEGER  errNo;
    SQLSMALLINT msgLength;
    SQLCHAR     errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);
    if (SQL_SUCCESS == SQLError(gEnv, gCon, aStmt, NULL, &errNo,
                                errMsg, sizeof(errMsg), &msgLength))
    {
        printf("mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

/* SQL을 즉시 실행 (에러 무시 옵션 포함) */
void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR) {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", sStmt);
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR) {
        if (aErrIgnore != 0) { SQLFreeStmt(sStmt, SQL_DROP); return; }
        outError("ExecDirect error", sStmt);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP)) {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", sStmt);
    }
}

void createTable()
{
    /* 이미 존재하면 삭제 후 재생성 */
    executeDirectSQL("DROP TABLE CLI_SAMPLE1", 1);
    executeDirectSQL(
        "CREATE LOG TABLE CLI_SAMPLE1("
        "  seq       SHORT,"
        "  score     INTEGER,"
        "  total     LONG,"
        "  ratio     DOUBLE,"
        "  id        VARCHAR(10),"
        "  srcip     IPV4,"
        "  reg_date  DATETIME,"
        "  textlog   TEXT"
        ")", 0);
}

void directInsert()
{
    int  i;
    char query[2048];

    for (i = 1; i <= 5; i++) {
        sprintf(query,
            "INSERT INTO CLI_SAMPLE1 VALUES("
            "  %d, %d, %ld, %.6f, 'id-%d',"
            "  '192.168.0.%d',"
            "  TO_DATE('2024-07-0%d 10:00:00','YYYY-MM-DD HH24:MI:SS'),"
            "  'log entry %d'"
            ")",
            i, i * 2, (long)(i * 10000), (double)i / (i * 10000),
            i, i, i, i);

        executeDirectSQL(query, 0);
        printf("%d record inserted\n", i);
    }
}

void selectTable()
{
    SQLHSTMT sStmt;
    const char *aSQL =
        "SELECT seq, score, total, ratio, id, srcip, reg_date, textlog"
        "  FROM CLI_SAMPLE1";

    short    sSeq;
    int      sScore;
    long     sTotal;
    double   sRatio;
    char     sId[11];
    char     sSrcIp[16];
    SQL_TIMESTAMP_STRUCT sRegDate;
    char     sLog[1024];
    SQLLEN   sLen = 0;
    int      i = 0;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
        outError("AllocStmt Error", sStmt);

    if (SQLPrepare(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
        outError("Prepare error", sStmt);

    if (SQLExecute(sStmt) == SQL_ERROR)
        outError("Execute error", sStmt);

    /* 결과 컬럼을 C 변수에 바인딩 */
    SQLBindCol(sStmt, 1, SQL_C_SHORT,          &sSeq,    0,           &sLen);
    SQLBindCol(sStmt, 2, SQL_C_LONG,           &sScore,  0,           &sLen);
    SQLBindCol(sStmt, 3, SQL_C_BIGINT,         &sTotal,  0,           &sLen);
    SQLBindCol(sStmt, 4, SQL_C_DOUBLE,         &sRatio,  0,           &sLen);
    SQLBindCol(sStmt, 5, SQL_C_CHAR,           sId,      sizeof(sId), &sLen);
    SQLBindCol(sStmt, 6, SQL_C_CHAR,           sSrcIp,   sizeof(sSrcIp), &sLen);
    SQLBindCol(sStmt, 7, SQL_C_TYPE_TIMESTAMP, &sRegDate, 0,          &sLen);
    SQLBindCol(sStmt, 8, SQL_C_CHAR,           sLog,     sizeof(sLog), &sLen);

    /* Fetch 루프 */
    while (SQLFetch(sStmt) == SQL_SUCCESS) {
        printf("=== row %d ===\n", i++);
        printf("  seq=%d, score=%d, total=%ld, ratio=%.6g\n",
               sSeq, sScore, sTotal, sRatio);
        printf("  id=%s, srcip=%s\n", sId, sSrcIp);
        printf("  reg_date=%d-%02d-%02d %02d:%02d:%02d\n",
               sRegDate.year, sRegDate.month, sRegDate.day,
               sRegDate.hour, sRegDate.minute, sRegDate.second);
        printf("  log=%s\n", sLog);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
        outError("FreeStmt error", sStmt);
}

int main()
{
    /* connectDB / disconnectDB 함수는 예제 1 참고 */
    connectDB();
    createTable();
    directInsert();
    selectTable();
    disconnectDB();
    return 0;
}
```

실행 결과:

```
connected ...
1 record inserted
2 record inserted
3 record inserted
4 record inserted
5 record inserted
=== row 0 ===
  seq=5, score=10, total=50000, ratio=2e-05
  id=id-5, srcip=192.168.0.5
  reg_date=2024-07-05 10:00:00
  log=log entry 5
...
```

---

#### 예제 3: Prepare/Execute + SQLBindParameter (sample3_prepare.c)

파라미터 바인딩(`?` 플레이스홀더)을 사용하여 타입 안전하게 데이터를 삽입합니다. 동일한 SQL을 반복 실행할 때 효율적입니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;

/* outError, connectDB, disconnectDB, executeDirectSQL 함수는 예제 2 참고 */

void prepareInsert()
{
    SQLHSTMT sStmt;
    int      i;
    short    sSeq;
    int      sScore;
    long     sTotal;
    char     sId[20];
    char     sSrcIp[20];
    int      sIdLen, sIpLen;

    const char *sSQL =
        "INSERT INTO CLI_SAMPLE VALUES(?, ?, ?, ?)";

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
        outError("AllocStmt error", sStmt);

    if (SQLPrepare(sStmt, (SQLCHAR *)sSQL, SQL_NTS) == SQL_ERROR)
        outError("Prepare error", sStmt);

    for (i = 1; i <= 5; i++) {
        sSeq   = (short)i;
        sScore = i * 2;
        sTotal = (long)(i * 10000);
        sprintf(sId, "id-%d", i);
        sprintf(sSrcIp, "192.168.0.%d", i);
        sIdLen = strlen(sId);
        sIpLen = strlen(sSrcIp);

        SQLBindParameter(sStmt, 1, SQL_PARAM_INPUT,
                         SQL_C_SSHORT, SQL_SMALLINT,
                         0, 0, &sSeq, 0, NULL);

        SQLBindParameter(sStmt, 2, SQL_PARAM_INPUT,
                         SQL_C_SLONG, SQL_INTEGER,
                         0, 0, &sScore, 0, NULL);

        SQLBindParameter(sStmt, 3, SQL_PARAM_INPUT,
                         SQL_C_SBIGINT, SQL_BIGINT,
                         0, 0, &sTotal, 0, NULL);

        SQLBindParameter(sStmt, 4, SQL_PARAM_INPUT,
                         SQL_C_CHAR, SQL_VARCHAR,
                         0, 0, sId, 0, (SQLLEN *)&sIdLen);

        if (SQLExecute(sStmt) == SQL_ERROR)
            outError("Execute error", sStmt);

        printf("%d prepared record inserted\n", i);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
        outError("FreeStmt error", sStmt);
}
```

---

#### 예제 4: Append API 고속 삽입 (sample4_append1.c)

Append API를 사용하여 시계열 데이터를 고속으로 삽입하는 전체 예제입니다. 에러 콜백을 등록하고 다양한 데이터 타입을 입력하는 방법을 보여줍니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <arpa/inet.h>

#if __linux__
#include <sys/time.h>
#endif

#define MACHBASE_PORT_NO  5656
#define ERROR_CHECK_COUNT 100

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;

/* 에러 콜백 함수 */
void dumpError(SQLHSTMT   aStmtHandle,
               SQLINTEGER  aErrorCode,
               SQLPOINTER  aErrorMessage,
               SQLLEN      aErrorBufLen,
               SQLPOINTER  aRowBuf,
               SQLLEN      aRowBufLen)
{
    char sErrMsg[1024]      = {0};
    char sRowMsg[32 * 1024] = {0};

    if (aErrorMessage != NULL)
        strncpy(sErrMsg, (char *)aErrorMessage, aErrorBufLen);

    if (aRowBuf != NULL)
        strncpy(sRowMsg, (char *)aRowBuf, aRowBufLen);

    fprintf(stderr, "Append Error: [%d][%s]\n[%s]\n\n",
            aErrorCode, sErrMsg, sRowMsg);
}

void outError(const char *aMsg)
{
    SQLINTEGER  errNo;
    SQLSMALLINT msgLength;
    SQLCHAR     errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);
    if (SQL_SUCCESS == SQLError(gEnv, gCon, gStmt, NULL, &errNo,
                                errMsg, sizeof(errMsg), &msgLength))
    {
        printf("mach-%d : %s\n", errNo, errMsg);
    }

    if (gStmt) SQLFreeStmt(gStmt, SQL_DROP);
    if (gCon)  SQLFreeConnect(gCon);
    if (gEnv)  SQLFreeEnv(gEnv);
    exit(-1);
}

void connectDB()
{
    char sConnStr[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv))
        outError("SQLAllocEnv error");

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon))
        outError("SQLAllocConnect error");

    sprintf(sConnStr,
            "SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d",
            MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect(gCon, NULL,
                                      (SQLCHAR *)sConnStr, SQL_NTS,
                                      NULL, 0, NULL,
                                      SQL_DRIVER_NOPROMPT))
        outError("connection error");

    if (SQL_ERROR == SQLAllocStmt(gCon, &gStmt))
        outError("AllocStmt error");

    printf("connected ...\n");
}

void disconnectDB()
{
    if (SQL_ERROR == SQLFreeStmt(gStmt, SQL_DROP))
        outError("FreeStmt error");

    if (SQL_ERROR == SQLDisconnect(gCon))
        outError("disconnect error");

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR) {
        if (aErrIgnore) return;
        outError("AllocStmt error");
    }
    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR) {
        if (aErrIgnore) { SQLFreeStmt(sStmt, SQL_DROP); return; }
        outError("ExecDirect error");
    }
    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP)) {
        if (aErrIgnore) return;
        outError("FreeStmt Error");
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL(
        "CREATE LOG TABLE CLI_SAMPLE("
        "  short1    SHORT,"
        "  integer1  INTEGER,"
        "  long1     LONG,"
        "  float1    FLOAT,"
        "  double1   DOUBLE,"
        "  datetime1 DATETIME,"
        "  varchar1  VARCHAR(10),"
        "  ip        IPV4,"
        "  text1     TEXT,"
        "  bin1      BINARY"
        ")", 0);
}

void appendOpen()
{
    const char *sTableName = "CLI_SAMPLE";

    if (SQLAppendOpen(gStmt, (SQLCHAR *)sTableName, ERROR_CHECK_COUNT)
            != SQL_SUCCESS)
        outError("SQLAppendOpen error");

    /* 에러 콜백 등록 */
    if (SQLAppendSetErrorCallback(gStmt, dumpError) != SQL_SUCCESS)
        outError("SQLAppendSetErrorCallback error");

    printf("append open ok\n");
}

void appendData()
{
    SQL_APPEND_PARAM sParam[10];
    char sVarchar[10] = {0};
    char sText[64]    = {0};
    char sBinary[64]  = {0};

    memset(sParam, 0, sizeof(sParam));

    /* --- 1. NULL 값으로 행 입력 --- */
    sParam[0].mShort               = SQL_APPEND_SHORT_NULL;
    sParam[1].mInteger             = SQL_APPEND_INTEGER_NULL;
    sParam[2].mLong                = SQL_APPEND_LONG_NULL;
    sParam[3].mFloat               = SQL_APPEND_FLOAT_NULL;
    sParam[4].mDouble              = SQL_APPEND_DOUBLE_NULL;
    sParam[5].mDateTime.mTime      = SQL_APPEND_DATETIME_NULL;
    sParam[6].mVarchar.mLength     = SQL_APPEND_VARCHAR_NULL;
    sParam[7].mIP.mLength          = SQL_APPEND_IP_NULL;
    sParam[8].mText.mLength        = SQL_APPEND_TEXT_NULL;
    sParam[9].mBinary.mLength      = SQL_APPEND_BINARY_NULL;
    SQLAppendDataV2(gStmt, sParam);

    /* --- 2. 실제 숫자 값 입력 --- */
    sParam[0].mShort   = 10;
    sParam[1].mInteger = 200;
    sParam[2].mLong    = 300000LL;
    sParam[3].mFloat   = 1.5f;
    sParam[4].mDouble  = 3.14;
    SQLAppendDataV2(gStmt, sParam);

    /* --- 3. DATETIME: 현재 시간 --- */
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(gStmt, sParam);

    /* --- 4. DATETIME: 문자열 파싱 --- */
    sParam[5].mDateTime.mTime      = SQL_APPEND_DATETIME_STRING;
    sParam[5].mDateTime.mDateStr   = "2024-07-01 12:00:00";
    sParam[5].mDateTime.mFormatStr = "YYYY-MM-DD HH24:MI:SS";
    SQLAppendDataV2(gStmt, sParam);

    /* --- 5. VARCHAR 입력 --- */
    strcpy(sVarchar, "MY DATA");
    sParam[6].mVarchar.mLength = strlen(sVarchar);
    sParam[6].mVarchar.mData   = sVarchar;
    SQLAppendDataV2(gStmt, sParam);

    /* --- 6. IPv4 문자열 입력 --- */
    sParam[7].mIP.mLength     = SQL_APPEND_IP_STRING;
    sParam[7].mIP.mAddrString = "192.168.0.1";
    SQLAppendDataV2(gStmt, sParam);

    /* --- 7. TEXT 입력 --- */
    memset(sText, 'A', sizeof(sText) - 1);
    sParam[8].mText.mLength = strlen(sText);
    sParam[8].mText.mData   = sText;
    SQLAppendDataV2(gStmt, sParam);

    /* --- 8. BINARY 입력 --- */
    memset(sBinary, 0xFA, sizeof(sBinary) - 1);
    sParam[9].mBinary.mLength = sizeof(sBinary) - 1;
    sParam[9].mBinary.mData   = sBinary;
    SQLAppendDataV2(gStmt, sParam);
}

int appendClose()
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if (SQLAppendClose(gStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS)
        outError("SQLAppendClose error");

    printf("append close ok\n");
    printf("success: %lld, failure: %lld\n",
           (long long)sSuccessCount, (long long)sFailureCount);

    return (int)sSuccessCount;
}

int main()
{
    connectDB();
    createTable();

    appendOpen();
    appendData();
    appendClose();

    disconnectDB();
    return 0;
}
```

실행 결과:

```
connected ...
append open ok
append close ok
success: 8, failure: 0
```

---

#### 예제 5: 대량 데이터 고속 삽입 (루프 패턴)

지속적인 시계열 데이터 수집에서 행을 반복 Append하는 패턴입니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <sys/time.h>

#define MACHBASE_PORT_NO  5656
#define TOTAL_RECORDS     100000
#define ERROR_CHECK_COUNT 1000

SQLHENV  gEnv;
SQLHDBC  gCon;
SQLHSTMT gStmt;

/* dumpError, outError, connectDB, disconnectDB,
   executeDirectSQL 함수는 예제 4 참고 */

static long long getCurrentTimeUs()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (long long)tv.tv_sec * 1000000LL + tv.tv_usec;
}

void bulkAppend(int aTotalCount)
{
    SQL_APPEND_PARAM sParam[3]; /* (datetime, integer, double) */
    int i;

    memset(sParam, 0, sizeof(sParam));

    if (SQLAppendOpen(gStmt, (SQLCHAR *)"SENSOR_DATA", ERROR_CHECK_COUNT)
            != SQL_SUCCESS)
        outError("SQLAppendOpen error");

    SQLAppendSetErrorCallback(gStmt, dumpError);

    for (i = 0; i < aTotalCount; i++) {
        /* _arrival_time은 자동 설정되므로 컬럼 데이터만 입력 */
        sParam[0].mDateTime.mTime = SQL_APPEND_DATETIME_NOW;
        sParam[1].mInteger        = i;
        sParam[2].mDouble         = i * 0.001;

        if (SQLAppendDataV2(gStmt, sParam) == SQL_ERROR) {
            outError("SQLAppendDataV2 error");
        }
    }

    /* 남은 버퍼 강제 전송 */
    SQLAppendFlush(gStmt);

    SQLBIGINT sSucc = 0, sFail = 0;
    SQLAppendClose(gStmt, &sSucc, &sFail);
    printf("bulk append done: success=%lld, failure=%lld\n",
           (long long)sSucc, (long long)sFail);
}

int main()
{
    long long sStart, sEnd;

    connectDB();

    /* 테이블 생성 */
    executeDirectSQL("DROP TABLE SENSOR_DATA", 1);
    executeDirectSQL(
        "CREATE LOG TABLE SENSOR_DATA("
        "  ts    DATETIME,"
        "  seq   INTEGER,"
        "  value DOUBLE"
        ")", 0);

    sStart = getCurrentTimeUs();
    bulkAppend(TOTAL_RECORDS);
    sEnd = getCurrentTimeUs();

    printf("elapsed: %lld us for %d records\n",
           sEnd - sStart, TOTAL_RECORDS);
    printf("throughput: %.2f records/sec\n",
           (double)TOTAL_RECORDS / ((sEnd - sStart) / 1000000.0));

    disconnectDB();
    return 0;
}
```

실행 결과 예시 (환경에 따라 다를 수 있습니다):

```
connected ...
bulk append done: success=100000, failure=0
elapsed: 312450 us for 100000 records
throughput: 320,052.38 records/sec
```

---

#### 에러 처리 요약

CLI 함수에서 `SQL_ERROR`가 반환되면 반드시 `SQLError()`로 상세 정보를 확인합니다.

```c
void checkError(SQLRETURN aRet, const char *aContext,
                SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt)
{
    SQLINTEGER  errNo;
    SQLSMALLINT msgLength;
    SQLCHAR     errMsg[1024];

    if (aRet == SQL_ERROR || aRet == SQL_SUCCESS_WITH_INFO) {
        if (SQL_SUCCESS == SQLError(aEnv, aCon, aStmt, NULL, &errNo,
                                    errMsg, sizeof(errMsg), &msgLength))
        {
            printf("[%s] mach-%05d: %s\n", aContext, errNo, errMsg);
        }
        if (aRet == SQL_ERROR) exit(-1);
    }
}

/* 사용 예 */
SQLRETURN ret = SQLExecDirect(sStmt, (SQLCHAR *)"SELECT ...", SQL_NTS);
checkError(ret, "SQLExecDirect", gEnv, gCon, sStmt);
```

> **참고**: `SQL_SUCCESS_WITH_INFO`는 경고(예: VARCHAR 값 잘림)를 나타냅니다. 에러는 아니지만 `SQLError()`로 확인하는 것을 권장합니다.

<a id="jdbc"></a>

## JDBC

### JDBC 개요

JDBC(Java Database Connectivity)는 Java 애플리케이션에서 데이터베이스에 접근하는 표준
API입니다. Machbase JDBC 드라이버는 Java 8을 기준으로 JDBC 4.2 핵심 API를 제공합니다.

- Java/JDBC 기준: Java 8, JDBC 4.2
- 드라이버 버전: 3.0.0
- 드라이버 클래스: `com.machbase.jdbc.MachDriver`
- Connection URL 형식: `jdbc:machbase://HOST:PORT/machbasedb`

`Driver.jdbcCompliant()`은 SQL-92 Entry Level 전체 지원 여부를 기준으로 `false`를
반환합니다. 이 값은 JDBC 4.2 API 지원 여부를 의미하지 않습니다.

### 드라이버 설치

#### JAR 파일 직접 사용

`$MACHBASE_HOME/lib` 디렉터리에서 `machbase.jar` 파일을 확인합니다.

```bash
ls -l $MACHBASE_HOME/lib/machbase.jar
```

클래스패스에 해당 JAR를 추가해 컴파일하고 실행합니다.

```bash
javac -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp.java
java  -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp
```

JAR에는 JDBC service provider가 포함되어 있으므로 JDBC 4.0 이후 환경에서는
`Class.forName()`을 호출하지 않아도 드라이버가 자동 등록됩니다.

#### Maven

`pom.xml`의 `<dependencies>` 블록에 다음을 추가합니다.

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```

최신 버전은 [Maven Central](https://mvnrepository.com/artifact/com.machbase/machjdbc)에서 확인하십시오.

#### Gradle

```groovy
dependencies {
    implementation 'com.machbase:machjdbc:{{< jdbc_version >}}'
}
```

### 연결 방법

#### 기본 연결

```java
import java.sql.*;
import java.util.Properties;
import com.machbase.jdbc.*;

public class ConnectSample {
    public static Connection connect() throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");

        return DriverManager.getConnection(url, props);
    }

    public static void main(String[] args) throws Exception {
        try (Connection conn = connect()) {
            System.out.println("Machbase JDBC connected.");
        }
    }
}
```

#### 연결 옵션

드라이버는 `Properties` 객체 또는 URL 쿼리 문자열로 옵션을 받습니다.

| 옵션 | 설명 |
|------|------|
| `user` / `password` | 비밀번호 인증 계정 정보 |
| `TIMEZONE` | 세션 타임존 (`+0900` 형식). 잘못된 값은 연결 오류로 처리됩니다. |
| `randomHost` | `true`이면 호스트 목록에서 무작위로 연결 대상을 선택합니다. |
| `maxStatements` | 풀링 연결에서 사용할 최대 캐시 Statement 수 |
| `CONNECTION_TIMEOUT` | 소켓 연결 타임아웃(초). `0`은 무제한 |
| `SOCKET_TIMEOUT` | 소켓 읽기 타임아웃(초). `0`은 무제한 |
| `characterEncoding` | 클라이언트 문자 인코딩 이름 |
| `AUTH_MODE` | `PASSWORD` 또는 `CHALLENGE` (AUTH KEY 인증) |
| `AUTH_SIG_SCHEME` | `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` 중 선택 |
| `AUTH_KEY_FILE` | 로컬 PEM 개인키 파일 경로 |

##### 타임존 설정 예제

```java
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
```

또는 `Properties`로 지정:

```java
props.put("TIMEZONE", "+0900");
```

### AUTH KEY 인증

Machbase 8.5 이상에서 공개키 기반 Challenge 인증을 사용할 수 있습니다.

```java
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties props = new Properties();
props.put("user", "app_user");
props.put("AUTH_MODE", "CHALLENGE");
props.put("AUTH_SIG_SCHEME", "ECDSA");
props.put("AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Connection conn = DriverManager.getConnection(url, props);
```

- `AUTH_KEY_FILE`만 지정하고 `AUTH_MODE`를 생략하면 내부적으로 `CHALLENGE`로 처리합니다.
- EC 키는 `ECDSA`, RSA 키는 `RSA_PKCS1_V15`가 기본 스킴으로 자동 선택됩니다.
- 지원 키: ECDSA (`P-256`, `P-384`, `P-521`), RSA (`2048`, `3072`, `4096` bits)
- POSIX 환경에서는 개인키 파일 권한을 `600`으로 설정하는 것을 권장합니다.

### PreparedStatement

```java
import java.sql.*;
import java.util.Properties;
import com.machbase.jdbc.*;

public class PreparedStmtSample {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");

        try (Connection conn = DriverManager.getConnection(url, props)) {
            // 테이블 생성
            try (Statement stmt = conn.createStatement()) {
                stmt.execute(
                    "CREATE LOG TABLE IF NOT EXISTS sensor_data (" +
                    "  ts DATETIME, device VARCHAR(40), value DOUBLE)"
                );
            }

            // PreparedStatement로 INSERT
            String insertSql = "INSERT INTO sensor_data VALUES (?, ?, ?)";
            try (MachPreparedStatement pstmt =
                     (MachPreparedStatement) conn.prepareStatement(insertSql)) {
                for (int i = 0; i < 5; i++) {
                    pstmt.setLong(1, System.currentTimeMillis() * 1_000_000L); // nanoseconds
                    pstmt.setString(2, "sensor-" + i);
                    pstmt.setDouble(3, 20.0 + i * 0.5);
                    pstmt.executeUpdate();
                }
                System.out.println("5 rows inserted.");
            }

            // SELECT
            String selectSql = "SELECT to_char(ts,'YYYY-MM-DD HH24:MI:SS') as ts, device, value" +
                               " FROM sensor_data ORDER BY ts";
            try (Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(selectSql)) {
                while (rs.next()) {
                    System.out.printf("ts=%s device=%s value=%.1f%n",
                        rs.getString("ts"),
                        rs.getString("device"),
                        rs.getDouble("value"));
                }
            }
        }
    }
}
```

#### IPv4/IPv6 바인딩

`MachPreparedStatement`는 IP 주소 타입을 위한 확장 메서드를 제공합니다.

```java
MachPreparedStatement pstmt =
    (MachPreparedStatement) conn.prepareStatement(
        "INSERT INTO net_log(ts, src_ip, dst_ip) VALUES (?, ?, ?)");
pstmt.setLong(1, System.currentTimeMillis() * 1_000_000L);
pstmt.setIpv4(2, "192.168.1.100");
pstmt.setIpv6(3, "::1");
pstmt.executeUpdate();
```

### 트랜잭션

Standard Edition의 TRANSACTION 테이블에서는 표준 JDBC 트랜잭션 API를 사용합니다.
`setAutoCommit(false)`는 즉시 SQL `BEGIN`을 보내지 않고 첫 Statement를 실행할 때
트랜잭션을 시작합니다.

```java
conn.setAutoCommit(false);

try (PreparedStatement pstmt = conn.prepareStatement(
         "INSERT INTO orders (order_id, amount) VALUES (?, ?)")) {
    pstmt.setInt(1, 1001);
    pstmt.setBigDecimal(2, new java.math.BigDecimal("50000.00"));
    pstmt.executeUpdate();

    pstmt.setInt(1, 1002);
    pstmt.setBigDecimal(2, new java.math.BigDecimal("30000.00"));
    pstmt.executeUpdate();

    conn.commit();
} catch (SQLException exception) {
    conn.rollback();
    throw exception;
}
```

commit과 rollback 후에도 auto-commit은 `false`로 유지됩니다. commit은 열린 ResultSet을
닫지만 Statement와 PreparedStatement는 재사용할 수 있습니다. 테이블 종류별 동작과
커넥션 풀 초기화 규칙은
[JDBC 트랜잭션과 커넥션 풀](/dbms/development-tools-integration/jdbc/transaction-pooling/)을
참고합니다.

### Append API

Machbase Append 프로토콜은 대량 데이터를 고속으로 적재할 때 사용합니다. `MachStatement`를 통해 접근합니다.

#### Append API 메서드

| 메서드 | 설명 |
|--------|------|
| `executeAppendOpen(tableName, errorCheckCount)` | Append 프로토콜 시작. errorCheckCount마다 오류 확인 |
| `executeAppendData(rsmd, data)` | 행 데이터 전송. 성공 시 1 또는 2 반환 |
| `executeAppendDataByTime(rsmd, time, data)` | 특정 나노초 시간을 지정해 행 전송 |
| `executeAppendFlush()` | Pending 응답 동기화. 성공 시 1 반환 |
| `executeAppendClose()` | Append 세션 종료. 성공 시 1 반환 |
| `executeSetAppendErrorCallback(callback)` | 오류 발생 시 호출할 콜백 등록 |
| `getAppendSuccessCount()` | 성공한 Append 건수 반환 |
| `getAppendFailureCount()` | 실패한 Append 건수 반환 |

#### Append 예제

```java
import java.util.*;
import java.sql.*;
import com.machbase.jdbc.*;

public class AppendSample {
    private static final String TABLE = "sensor_data";
    private static final int ERROR_CHECK_COUNT = 100;

    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");

        try (Connection conn = DriverManager.getConnection(url, props)) {
            MachStatement stmt = (MachStatement) conn.createStatement();

            // Append 시작
            ResultSet rs = stmt.executeAppendOpen(TABLE, ERROR_CHECK_COUNT);
            ResultSetMetaData rsmd = rs.getMetaData();

            // 오류 콜백 등록
            stmt.executeSetAppendErrorCallback(
                (errNo, errMsg, rowMsg) ->
                    System.err.printf("Append Error [%05d]: %s%n%s%n", errNo, errMsg, rowMsg)
            );

            long startTime = System.nanoTime();
            int count = 10_000;

            for (int i = 0; i < count; i++) {
                ArrayList<Object> row = new ArrayList<>();
                row.add(System.currentTimeMillis() * 1_000_000L + i); // ts (nanoseconds)
                row.add("sensor-" + (i % 10));                         // device
                row.add(20.0 + Math.random() * 10.0);                  // value

                int rc = stmt.executeAppendData(rsmd, row);
                if (rc != 1 && rc != 2) {
                    System.err.println("AppendData error at row " + i);
                    break;
                }
            }

            stmt.executeAppendFlush();
            stmt.executeAppendClose();

            long elapsed = (System.nanoTime() - startTime) / 1_000_000;
            System.out.printf("Appended %d rows in %d ms%n", count, elapsed);
            System.out.printf("Success: %d, Failure: %d%n",
                stmt.getAppendSuccessCount(),
                stmt.getAppendFailureCount());

            rs.close();
            stmt.close();
        }
    }
}
```

> **중요**: Append에서 DATETIME 컬럼 값은 반드시 `long` 타입의 나노초(nanosecond) 단위로 전달해야 합니다.
> `System.currentTimeMillis() * 1_000_000L`로 밀리초를 나노초로 변환합니다.

### 커넥션 풀 (HikariCP)

운영 환경에서는 커넥션 풀을 사용하는 것을 권장합니다. [HikariCP](https://github.com/brettwooldridge/HikariCP)와 연동하는 예시입니다.

#### Maven 의존성 추가

```xml
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>5.1.0</version>
</dependency>
```

#### HikariCP 설정 예제

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
config.setUsername("SYS");
config.setPassword("MANAGER");
config.setDriverClassName("com.machbase.jdbc.MachDriver");

// 풀 크기 설정
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);   // 30초
config.setIdleTimeout(600_000);        // 10분
config.setMaxLifetime(1_800_000);      // 30분

// 연결 검증 쿼리
config.setConnectionTestQuery("SELECT 1 FROM V$TABLES LIMIT 1");

// 타임존 설정
config.addDataSourceProperty("TIMEZONE", "+0900");

HikariDataSource dataSource = new HikariDataSource(config);

// 사용 예
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM sensor_data")) {
    if (rs.next()) {
        System.out.println("Row count: " + rs.getLong(1));
    }
}
```

### 전체 예제: INSERT / SELECT

아래 예제는 테이블 생성, 데이터 삽입, 조회까지 한 번에 확인할 수 있는 독립 실행 가능한 코드입니다.

```java
import java.sql.*;
import java.util.Properties;
import com.machbase.jdbc.*;

public class FullExample {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");
        props.put("TIMEZONE", "+0900");

        try (Connection conn = DriverManager.getConnection(url, props)) {
            System.out.println("Connected to Machbase.");

            // 테이블 생성
            try (Statement stmt = conn.createStatement()) {
                try {
                    stmt.execute("DROP TABLE ex_sensor");
                } catch (SQLException ignored) {
                    // 테이블이 없으면 무시하고 생성합니다.
                }
                stmt.execute(
                    "CREATE LOG TABLE ex_sensor (" +
                    "  ts DATETIME, tag VARCHAR(40), value DOUBLE)");
            }

            // PreparedStatement로 데이터 삽입
            String insertSql = "INSERT INTO ex_sensor VALUES (?, ?, ?)";
            try (MachPreparedStatement pstmt =
                     (MachPreparedStatement) conn.prepareStatement(insertSql)) {
                long baseTime = System.currentTimeMillis() * 1_000_000L;
                for (int i = 0; i < 10; i++) {
                    pstmt.setLong(1, baseTime + i * 1_000_000_000L);
                    pstmt.setString(2, "tag-" + (i % 3));
                    pstmt.setDouble(3, 20.0 + i);
                    pstmt.executeUpdate();
                }
                System.out.println("Inserted 10 rows.");
            }

            // SELECT
            String selectSql =
                "SELECT to_char(ts,'YYYY-MM-DD HH24:MI:SS') as ts, tag, value" +
                " FROM ex_sensor ORDER BY ts";
            try (Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(selectSql)) {
                System.out.println("--- Query Results ---");
                while (rs.next()) {
                    System.out.printf("  ts=%-22s tag=%-6s value=%.1f%n",
                        rs.getString("ts"),
                        rs.getString("tag"),
                        rs.getDouble("value"));
                }
            }
        }
    }
}
```

### 주의 사항

- Standard Edition의 TRANSACTION 테이블은 JDBC 표준 트랜잭션 API를 사용합니다.
- LOG/TAG Append 입력은 rollback 대상이 아닙니다. manual transaction의 테이블 종류별
  DML 동작은 JDBC 트랜잭션 레퍼런스를 확인합니다.
- LOG 테이블에는 `UPDATE`를 사용할 수 없습니다. TAG data UPDATE는 태그 선택자와 시간축
  조건을 만족하는 제한된 보정 작업에만 사용합니다.
- `_arrival_time` 컬럼은 기본적으로 숨겨져 있습니다. 표시하려면 URL에 `show_hidden_cols=1`을 추가합니다.
- Append에서 DATETIME 값은 반드시 나노초 단위 `long`으로 전달해야 합니다.

JDBC 4.2의 전체 타입, metadata, pool과 문제 해결 정보는
[JDBC 레퍼런스](/dbms/development-tools-integration/jdbc/)를 참고합니다.

<a id="python"></a>

## Python

### 개요

`machbaseapi` 패키지는 Machbase 서버에 연결하기 위한 순수 Python 구현 드라이버입니다. 네이티브 `.so`/`.dll` 파일이 필요 없으며, DB-API 2.0 스타일과 레거시 스타일 두 가지 인터페이스를 모두 제공합니다.

- PyPI 패키지명: `machbaseapi`
- Python 3.6 이상 필요
- 네이티브 라이브러리 의존성 없음
- DB-API 2.0 방식: `connect()`, `cursor()` 지원
- Python API 2.4부터 재사용 가능한 `cursor(prepared=True)` 지원
- Append 프로토콜 지원 (대량 고속 적재)

### 설치

```bash
pip3 install machbaseapi
```

`pip3`가 PATH에 없다면 다음 명령을 사용합니다.

```bash
python3 -m pip install machbaseapi
```

#### 설치 확인

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase 클래스 import:', bool(machbase))
print('connect 함수 존재:', callable(connect))
PY
```

### 빠른 시작

#### DB-API 방식 (권장)

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

# 테이블 생성
cur.execute('''
    CREATE LOG TABLE IF NOT EXISTS py_sensor (
        ts DATETIME,
        device VARCHAR(40),
        value DOUBLE
    )
''')

# 데이터 삽입
cur.execute("INSERT INTO py_sensor VALUES (NOW, 'sensor-1', 23.5)")
cur.execute("INSERT INTO py_sensor VALUES (NOW, 'sensor-2', 24.1)")

# 데이터 조회
cur.execute("SELECT to_char(ts,'YYYY-MM-DD HH24:MI:SS') as ts, device, value FROM py_sensor ORDER BY ts")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()
```

#### 레거시 방식 (machbase 클래스)

```python
#!/usr/bin/env python3
import json
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    # 테이블 생성
    db.execute('DROP TABLE py_quick')
    db.result()  # 테이블이 없어도 다음 CREATE를 계속 진행
    db.execute('CREATE LOG TABLE py_quick(ts DATETIME, device VARCHAR(40), value DOUBLE)')

    # 데이터 삽입
    for i in range(3):
        sql = (
            f"INSERT INTO py_quick VALUES ("
            f"to_date('2024-01-0{i+1}', 'YYYY-MM-DD'),"
            f"'sensor-{i}',"
            f"{20.5 + i})"
        )
        if db.execute(sql) == 0:
            raise SystemExit(db.result())

    # 데이터 조회 (스트리밍 방식)
    if db.select('SELECT * FROM py_quick ORDER BY ts') == 0:
        raise SystemExit(db.result())

    while True:
        rc, payload = db.fetch()
        if rc == 0:
            break
        print(json.loads(payload))

    db.selectClose()
finally:
    db.close()
```

### 연결 관리

#### DB-API connect()

```python
from machbaseAPI import connect

# 기본 연결
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# 추가 연결 문자열 속성 지정
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER',
               conn_str='APP_NAME=my-python-app')
```

#### machbase 클래스 open() / openEx()

```python
from machbaseAPI import machbase

db = machbase()

# 기본 연결
rc = db.open('127.0.0.1', 'SYS', 'MANAGER', 5656)

# 확장 연결 (추가 속성 지정)
rc = db.openEx('127.0.0.1', 'SYS', 'MANAGER', 5656, 'APP_NAME=my-app')

# 연결 상태 확인
print('isOpened:', db.isOpened())
print('isConnected:', db.isConnected())

db.close()
```

### 지원 API

#### DB-API 스타일

| API | 설명 |
|-----|------|
| `connect(**kwargs)` | 연결 생성. `host`, `port`, `user`, `password` 키워드 인자 사용 |
| `cursor(dictionary=True, raw=False, prepared=False)` | 일반 또는 prepared cursor 생성 |
| `cursor.execute(sql, params=None)` | SQL 실행 |
| `cursor.executemany(sql, seq_of_params)` | 같은 SQL을 여러 parameter 묶음으로 실행 |
| `cursor.fetchone()` | 결과 한 행 조회 |
| `cursor.fetchmany(size)` | 최대 `size`건 조회 |
| `cursor.fetchall()` | 전체 결과 조회 |
| `cursor.rowcount` | 영향받은 행 수 |
| `cursor.close()` | 커서 닫기 |
| `connection.append(table, rows, types=None, times=None)` | Append 프로토콜로 행 추가 |

#### machbase 클래스 스타일

| API | 반환 | 설명 |
|-----|------|------|
| `open(host, user, password, port)` | `1`/`0` | 서버 연결 |
| `openEx(host, user, password, port, conn_str)` | `1`/`0` | 확장 연결 |
| `close()` | `1`/`0` | 세션 종료 |
| `isOpened()` | `1`/`0` | 핸들 열림 여부 확인 |
| `isConnected()` | `1`/`0` | 연결 상태 확인 |
| `execute(sql)` | `1`/`0` | SQL 직접 실행 |
| `select(sql)` | `1`/`0` | 스트리밍 SELECT 실행 |
| `fetch()` | `(rc, json_str)` | 다음 행 조회 |
| `selectClose()` | `1`/`0` | 결과 커서 닫기 |
| `result()` | JSON 문자열 | 최신 결과 페이로드 반환 |
| `tables()` | `1`/`0` | 모든 테이블 메타데이터 조회 |
| `columns(table_name)` | `1`/`0` | 테이블 컬럼 메타데이터 조회 |
| `appendOpen(table_name)` | `1`/`0` | Append 세션 시작 |
| `appendData(table_name, rows)` | `1`/`0` | Append 행 전송 |
| `appendFlush()` | `1`/`0` | Pending 응답 동기화 |
| `appendClose()` | `1`/`0` | Append 세션 종료 |
| `append(table_name, rows)` | `1`/`0` | 열기·추가·닫기 한 번에 처리 |

### cursor 사용법

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# 딕셔너리 커서 (기본)
cur = conn.cursor()
cur.execute('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT 5')
for row in cur.fetchall():
    print(row['NAME'])

# 튜플 커서
cur_tuple = conn.cursor(dictionary=False)
cur_tuple.execute('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT 5')
for row in cur_tuple.fetchall():
    print(row[0])

# fetchone / fetchmany
cur.execute('SELECT NAME FROM V$TABLES ORDER BY NAME')
first = cur.fetchone()
print('first:', first)
batch = cur.fetchmany(3)
print('batch:', batch)

cur.close()
conn.close()
```

### Prepared cursor (2.4)

같은 SQL을 여러 번 실행할 때는 `prepared=True`로 cursor를 생성합니다. prepared cursor는
동일한 원본 SQL 문자열을 사용하는 동안 하나의 server statement를 유지합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor(dictionary=False, prepared=True)

sql = 'INSERT INTO PY_SENSOR(ts, device, value) VALUES(%s, %s, %s)'
cur.execute(sql, [1720000000000000000, 'sensor-1', 23.5])
cur.execute(sql, [1720000001000000000, 'sensor-2', 24.1])
cur.executemany(
    sql,
    [
        [1720000002000000000, 'sensor-3', 24.3],
        [1720000003000000000, 'sensor-4', None],
    ],
)

cur.close()
conn.close()
```

prepared cursor는 positional `%s`와 `?`, named `%(name)s`와 `:name`을 지원합니다.
positional marker에는 sequence를, named marker에는 mapping을 전달합니다. cursor 하나는
server statement 하나를 보유하므로 SQL 문자열이 달라지면 이전 statement를 해제합니다.
여러 SQL을 각각 유지하려면 SQL별 cursor를 생성하고, 사용 후 `close()`로 닫습니다.

marker 변환, 재사용, 오류와 종료 동작은
[Python Prepared Cursor](../../development-tools-integration/python/#prepared-cursor-24)를 참고하십시오.

### 에러 처리

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('SELECT * FROM non_existent_table')
except Exception as e:
    print('Query error:', e)
finally:
    cur.close()
    conn.close()
```

레거시 방식에서는 반환 코드로 성공 여부를 판별합니다.

```python
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    print('Connection failed:', db.result())
    raise SystemExit(1)

if db.execute('SELECT * FROM non_existent_table') == 0:
    print('Execute failed:', db.result())

db.close()
```

### Append 프로토콜

Append는 대량 데이터를 고속으로 적재할 때 사용합니다. `INSERT`보다 훨씬 빠른 성능을 제공합니다.

#### DB-API append()

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('DROP TABLE py_append_demo')
except Exception:
    pass
cur.execute('CREATE LOG TABLE py_append_demo(ts DATETIME, device VARCHAR(32), value DOUBLE)')

rows = [
    ['2024-01-01 09:00:00', 'sensor-a', 21.5],
    ['2024-01-01 09:01:00', 'sensor-b', 22.1],
    ['2024-01-01 09:02:00', 'sensor-a', 21.8],
]

appended = conn.append('PY_APPEND_DEMO', rows)
print(f'Appended {appended} rows.')

cur.execute('SELECT COUNT(*) as cnt FROM py_append_demo')
print('Count:', cur.fetchone())

cur.close()
conn.close()
```

#### Append 행 길이와 기본값

Append 입력 행은 테이블 컬럼 수와 같은 개수의 값을 가져야 합니다. 마지막 컬럼도
생략하지 말고 명시적으로 값을 전달합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('DROP TABLE py_append_defaults')
except Exception:
    pass
cur.execute(
    'CREATE LOG TABLE py_append_defaults('
    '  ts DATETIME, name VARCHAR(20), value DOUBLE, note VARCHAR(40))'
)

# 모든 행은 4개 컬럼 값을 전달합니다.
conn.append('PY_APPEND_DEFAULTS', [
    ['2024-01-01 10:00:00', 'sensor-1', 12.3, 'auto'],
    ['2024-01-01 10:00:01', 'sensor-2', 13.4, 'manual'],
])

cur.execute('SELECT ts, name, value, note FROM py_append_defaults ORDER BY ts')
print(cur.fetchall())

cur.close()
conn.close()
```

Append에서 컬럼을 생략하면 `Append row length does not match append metadata` 오류가
발생합니다. NULL 입력이 필요한 경우에는 `INSERT`와 파라미터 바인딩을 사용하고,
컬럼 타입별 조회 표현을 확인합니다.

#### 레거시 방식 Append

```python
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    db.execute('DROP TABLE py_legacy_append')
    db.result()
    db.execute('CREATE LOG TABLE py_legacy_append(ts DATETIME, tag VARCHAR(16), reading DOUBLE)')

    # appendOpen → appendData → appendFlush → appendClose
    if db.appendOpen('PY_LEGACY_APPEND') == 0:
        raise SystemExit(db.result())

    rows = [
        ['2024-01-01 09:00:00', 'node-1', 30.0],
        ['2024-01-01 09:05:00', 'node-1', 30.5],
    ]
    if db.appendData('PY_LEGACY_APPEND', rows) == 0:
        raise SystemExit(db.result())

    db.appendFlush()
    db.appendClose()

    # 편의 함수: append() - 열기/추가/닫기 한 번에 처리
    more_rows = [
        ['2024-01-01 10:00:00', 'node-2', 40.1],
        ['2024-01-01 10:05:00', 'node-2', 40.7],
    ]
    if db.append('PY_LEGACY_APPEND', more_rows) == 0:
        raise SystemExit(db.result())

    print('Append done.')
finally:
    db.close()
```

#### appendByTime() - LOG 테이블 arrival time 지정

```python
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    db.execute('DROP TABLE py_append_time')
    db.result()
    db.execute('CREATE LOG TABLE py_append_time(tag VARCHAR(16), reading DOUBLE)')

    rows = [
        ['node-2', 40.1],
        ['node-2', 40.7],
    ]
    epoch_times = [
        1704106800_000_000_000,
        1704106860_000_000_000,
    ]  # Unix epoch (나노초 단위)

    if db.appendByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
        raise SystemExit(db.result())
    print('appendByTime result:', db.result())
finally:
    db.close()
```

`aTimes`는 LOG 테이블의 `_ARRIVAL_TIME` 값으로 사용됩니다. 일반 컬럼에 저장할
시각 값은 행 데이터에 직접 포함합니다.

### TAG 테이블 Append

TAG 테이블 Append도 테이블 정의의 컬럼 순서에 맞춰 값을 전달해야 합니다. 추가 컬럼과
메타데이터 컬럼을 정의했다면 해당 값도 행 배열에 포함합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('DROP TABLE py_tag_demo')
except Exception:
    pass
cur.execute('''
    CREATE TAG TABLE py_tag_demo (
        name VARCHAR(40) PRIMARY KEY,
        time DATETIME BASETIME,
        value DOUBLE SUMMARIZED,
        status VARCHAR(20)
    ) METADATA (
        site VARCHAR(20),
        line INTEGER
    )
''')

# name, time, value, status, site, line 순서로 값을 전달
conn.append('PY_TAG_DEMO', [
    ['tag-1', '2024-01-01 10:00:00', 12.3, 'ok', 'seoul', 1],
    ['tag-2', '2024-01-01 10:01:00', 13.7, 'ok', 'busan', 2],
])

cur.execute('SELECT name, time, value, status FROM py_tag_demo ORDER BY time')
print(cur.fetchall())

cur.close()
conn.close()
```

### 스트리밍 SELECT (레거시)

대용량 결과를 처리할 때 `select()` + `fetch()` 방식으로 행을 스트리밍합니다.

```python
import json
from machbaseAPI import machbase

db = machbase()
if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

try:
    if db.select('SELECT NAME FROM V$TABLES ORDER BY NAME') == 0:
        raise SystemExit(db.result())

    count = 0
    while True:
        rc, payload = db.fetch()
        if rc == 0:
            break
        row = json.loads(payload)
        print(row)
        count += 1

    db.selectClose()
    print(f'Total: {count} rows')
finally:
    db.close()
```

### 주의 사항

- `machbase` 클래스 메서드는 성공 시 `1`, 실패 시 `0`을 반환합니다. 반드시 반환 코드를 확인하십시오.
- 트랜잭션은 TRANSACTION 테이블 작업에서 사용합니다. LOG/TAG 테이블 Append성 입력은 롤백 대상이 아니므로 테이블 타입별 지원 범위를 확인합니다.
- Append 행은 테이블 컬럼 수와 순서를 맞춰야 합니다. 컬럼 생략은 지원하지 않습니다.
- 커넥션 풀 옵션(`pool_name`, `pool_size`)은 현재 미지원입니다.
- `getSessionId()`, `count()`, `checkBit()` 등 기존 네이티브 기반 API는 2.3 이상 순수 Python 패키지에서 제공되지 않습니다.

<a id="node-js-typescript"></a>

## Node.js / TypeScript

### 개요

`@machbase/ts-client`는 Machbase CMI 프로토콜을 순수 TypeScript로 구현한 라이브러리입니다. Node.js 애플리케이션이 네이티브 바인딩 없이도 Machbase 서버에 연결해 SQL 실행, Prepared Statement, Append 프로토콜을 사용할 수 있습니다.

- 패키지: `@machbase/ts-client`
- Node.js 18 이상 (LTS 권장)
- 네이티브 바인딩 불필요 (순수 TypeScript)
- CommonJS / ESM / TypeScript 모두 지원
- TCP 소켓 사용 (브라우저 미지원)

### 설치

#### npm / yarn / pnpm

```bash
npm install @machbase/ts-client
# 또는
yarn add @machbase/ts-client
# 또는
pnpm add @machbase/ts-client
```

#### 오프라인 설치

`.tgz` 파일을 전달받은 경우:

```bash
npm install ./machbase-ts-client-1.0.0.tgz
```

#### 설치 확인

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'OK' : 'FAIL')"
```

### 빠른 시작

#### TypeScript

```typescript
// src/example.ts
import { createConnection } from '@machbase/ts-client';

const conn = createConnection({
    host: process.env.MACH_HOST ?? '127.0.0.1',
    port: +(process.env.MACH_PORT ?? 5656),
    user: process.env.MACH_USER ?? 'SYS',
    password: process.env.MACH_PASS ?? 'MANAGER',
});

await conn.connect();

const [rows, fields] = await conn.query(
    'SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]
);
console.log(rows);

await conn.end();
```

#### CommonJS (JavaScript)

```javascript
// quickstart.js
const { createConnection } = require('@machbase/ts-client');

async function main() {
    const conn = createConnection({
        host: '127.0.0.1',
        port: 5656,
        user: 'SYS',
        password: 'MANAGER',
    });
    await conn.connect();

    const [rows] = await conn.query(
        'SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [10]
    );
    console.table(rows);

    await conn.end();
}

main().catch(err => console.error('Error:', err));
```

### 연결 설정

#### createConnection(config)

| 매개변수 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `host` | string | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| `port` | number | `5656` | 리스너 포트 |
| `user` | string | – | 데이터베이스 사용자 |
| `password` | string | – | 비밀번호 |
| `database` | string | `MACHBASEDB` | 초기 logical database 이름 |
| `clientId` | string | `NPM` | 서버 로그에 표시될 클라이언트 ID |
| `showHiddenColumns` | boolean | `false` | 숨김 컬럼 포함 여부 |
| `timezone` | string | 빈 값 | 타임존 식별자 |
| `connectTimeout` | number | `5000` | 소켓 연결 타임아웃(ms) |
| `queryTimeout` | number | `60000` | 명령별 타임아웃(ms) |

```javascript
const conn = createConnection({
    host: '192.168.1.10',
    port: 5656,
    user: 'SYS',
    password: 'MANAGER',
    timezone: '+09:00',
    connectTimeout: 10_000,
    queryTimeout: 30_000,
});
await conn.connect();
```

#### 연결 종료

```javascript
// try...finally 패턴으로 항상 연결 종료를 보장합니다.
await conn.connect();
try {
    // ... 작업 수행 ...
} finally {
    await conn.end();
}
```

### SQL 실행

#### execute() - DDL / DML

결과 집합을 반환하지 않는 명령(DDL, INSERT, DELETE)에 사용합니다.

```javascript
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        // 테이블 생성
        const [create] = await conn.execute(
            'CREATE LOG TABLE demo (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)'
        );
        console.log('Affected rows:', create.affectedRows); // DDL은 0

        // 데이터 삽입
        const [insert] = await conn.execute(
            "INSERT INTO demo VALUES (1, 'alpha', 0.5)"
        );
        console.log('Inserted rows:', insert.affectedRows); // 1
    } finally {
        await conn.execute('DROP TABLE demo').catch(() => {});
        await conn.end();
    }
})();
```

#### query() - SELECT

행을 반환하는 쿼리에 사용합니다. `[rows, fields]` 형태의 2요소 배열을 반환합니다.

```javascript
const [rows, fields] = await conn.query(
    'SELECT ID, NAME, VALUE FROM demo ORDER BY ID'
);
console.table(rows);
console.log('Columns:', fields?.map(f => f.name));
```

### Prepared Statement

반복 실행 쿼리에는 Prepared Statement를 사용하면 성능이 향상됩니다.

```javascript
// prepared-reuse.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE VOLATILE TABLE vt_demo (ID INTEGER PRIMARY KEY, NAME VARCHAR(64))'
        );
        for (let i = 1; i <= 5; i++) {
            await conn.execute(`INSERT INTO vt_demo VALUES (${i}, 'name-${i}')`);
        }

        // Prepared Statement 준비
        const stmt = await conn.prepare('SELECT NAME FROM vt_demo WHERE ID = ?');
        try {
            for (const id of [1, 3, 5]) {
                const [rows] = await stmt.execute([id]);
                console.log(`ID ${id}:`, rows[0]?.NAME);
            }
        } finally {
            await stmt.close(); // 서버 리소스 해제
        }
    } finally {
        await conn.execute('DROP TABLE vt_demo').catch(() => {});
        await conn.end();
    }
})();
```

#### Prepared Statement 메서드

| 메서드 | 설명 |
|--------|------|
| `execute(params?)` | 실행 후 `[rows, fields]` 반환 |
| `getColumns()` | 컬럼 메타데이터 캐시 반환 |
| `getLastMessage()` | 최근 서버 메시지 확인 |
| `getStatementId()` | 내부 Statement ID 조회 |
| `close()` | 서버 리소스 정리 (여러 번 호출해도 안전) |

#### NULL 및 타입 지정 바인딩

```javascript
// null을 전달할 때는 타입을 명시합니다.
await stmt.execute([
    { value: null, type: 'varchar' },
    { value: new Date(), type: 'varchar' },
    { value: 42, type: 'int32' },
]);
```

### Append 프로토콜

Append는 대량 데이터를 고속으로 적재할 때 사용합니다. 단건 `INSERT`보다 훨씬 빠른 성능을 제공합니다.

지원 컬럼 타입: `int32`, `int64`, `float64`, `varchar`

#### appendBatch() - 로그 테이블 배치 Append

```javascript
// append-batch.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE LOG TABLE log_demo (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)'
        );

        const result = await conn.appendBatch(
            'log_demo',
            [
                { name: 'ID',    type: 'int32'   },
                { name: 'NAME',  type: 'varchar' },
                { name: 'VALUE', type: 'float64' },
            ],
            [
                [1, 'alpha', 0.5],
                [2, 'bravo', 1.25],
                { values: [3, 'charlie', 2.5], arrivalTime: Date.now() * 1_000_000 },
            ],
        );
        console.log('Appended:', result.rowsAppended);
        console.log('Failed:',   result.rowsFailed);
    } finally {
        await conn.execute('DROP TABLE log_demo').catch(() => {});
        await conn.end();
    }
})();
```

`appendBatch()` 반환값: `{ table, rowsAppended, rowsFailed, message }`

#### appendOpen() - 스트리밍 Append

점진적으로 데이터를 유입할 때 사용합니다.

```javascript
// append-stream.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE LOG TABLE stream_demo (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)'
        );

        const stream = await conn.appendOpen('stream_demo', [
            { name: 'ID',    type: 'int32'   },
            { name: 'NAME',  type: 'varchar' },
            { name: 'VALUE', type: 'float64' },
        ]);

        // 배열 또는 객체 형태로 행 전송
        await stream.append([
            [1, 'alpha', 0.5],
            [2, 'bravo', 1.25],
        ]);
        await stream.append({ values: [3, 'charlie', 2.5] });

        await stream.close();

        const [rows] = await conn.query('SELECT COUNT(*) AS CNT FROM stream_demo');
        console.log('Count:', rows[0]?.CNT);
    } finally {
        await conn.execute('DROP TABLE stream_demo').catch(() => {});
        await conn.end();
    }
})();
```

#### TAG 테이블 스트리밍 Append

```javascript
// append-tag.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE TAG TABLE tag_demo (' +
            '  name VARCHAR(20) PRIMARY KEY,' +
            '  time DATETIME BASETIME,' +
            '  value DOUBLE SUMMARIZED' +
            ')'
        );

        const stream = await conn.appendOpen('tag_demo', [
            { name: 'NAME',  type: 'varchar' },
            { name: 'TIME',  type: 'int64'   },
            { name: 'VALUE', type: 'float64' },
        ]);

        const now = Date.now();
        await stream.append([
            ['T-0001', new Date(now),     1.0],
            ['T-0002', new Date(now + 1), 2.0],
            ['T-0003', new Date(now + 2), 3.0],
        ]);
        await stream.close();

        const [rows] = await conn.query('SELECT COUNT(*) AS CNT FROM tag_demo');
        console.log('TAG count:', rows[0]?.CNT);
    } finally {
        await conn.execute('DROP TABLE tag_demo').catch(() => {});
        await conn.end();
    }
})();
```

> **팁**: 로그 테이블 Append에는 `appendBatch()`를, TAG 테이블이나 점진적 유입에는 `appendOpen()`을 사용하십시오.
> `MACHBASE_NATIVE_APPEND=0` 환경 변수를 설정하면 네이티브 Append를 비활성화하고 Prepared Statement 방식으로 전환합니다.

### 전체 예제: INSERT / SELECT / Append

```javascript
// full-example.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({
        host: '127.0.0.1',
        port: 5656,
        user: 'SYS',
        password: 'MANAGER',
    });
    await conn.connect();
    console.log('Connected to Machbase.');

    try {
        // 1. 테이블 생성
        await conn.execute('DROP TABLE ex_sensor').catch(() => {});
        await conn.execute(
            'CREATE LOG TABLE ex_sensor (ID INTEGER, DEVICE VARCHAR(40), VALUE DOUBLE)'
        );
        console.log('Table created.');

        // 2. 단건 INSERT
        for (let i = 1; i <= 5; i++) {
            await conn.execute(
                `INSERT INTO ex_sensor VALUES (${i}, 'device-${i}', ${20.0 + i * 0.5})`
            );
        }
        console.log('Inserted 5 rows via INSERT.');

        // 3. SELECT
        const [rows] = await conn.query(
            'SELECT ID, DEVICE, VALUE FROM ex_sensor ORDER BY ID'
        );
        console.table(rows);

        // 4. Append로 추가 적재
        const result = await conn.appendBatch(
            'ex_sensor',
            [
                { name: 'ID',     type: 'int32'   },
                { name: 'DEVICE', type: 'varchar' },
                { name: 'VALUE',  type: 'float64' },
            ],
            [[6, 'device-6', 23.0], [7, 'device-7', 23.5], [8, 'device-8', 24.0]],
        );
        console.log(`Appended ${result.rowsAppended} rows.`);

        // 5. 최종 건수 확인
        const [countRows] = await conn.query('SELECT COUNT(*) AS CNT FROM ex_sensor');
        console.log('Total rows:', countRows[0]?.CNT);
    } finally {
        await conn.execute('DROP TABLE ex_sensor').catch(() => {});
        await conn.end();
        console.log('Connection closed.');
    }
})();
```

### Promise 래퍼와 ping()

```javascript
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        // 연결 상태 확인
        await conn.ping();
        console.log('Ping OK');

        // promise() 래퍼 사용
        const p = conn.promise();
        const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
        console.log(rows.map(r => r.NAME));
    } finally {
        await conn.end();
    }
})();
```

### 오류 처리

```javascript
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        // 존재하지 않는 테이블 조회
        const [rows] = await conn.query('SELECT * FROM non_existent_table');
    } catch (err) {
        console.error('Query error:', err.message);
        // QueryError의 경우 err.code, err.sql 필드도 확인 가능
    } finally {
        await conn.end();
    }
})();
```

#### 자주 발생하는 오류

| 오류 | 원인 | 해결 방법 |
|------|------|-----------|
| `ECONNREFUSED` | 서버 미실행 또는 포트 불일치 | `machadmin -u`로 서버 상태 확인, 포트 및 방화벽 점검 |
| `Authentication failed` | 사용자/비밀번호 오류 | 계정 정보 확인, `machadmin -c`로 DB 생성 여부 확인 |
| `column count does not match` | Append 컬럼 수 불일치 | 대상 테이블 스키마와 컬럼 정의 확인 |

### 동작 특성과 한계

#### 트랜잭션 편의 메서드 미지원

서버는 TRANSACTION 테이블에 plain `BEGIN`, `COMMIT`, `ROLLBACK` SQL을 지원합니다. Node.js
클라이언트의 `beginTransaction`, `commit`, `rollback` 편의 메서드는 구현되어 있지 않으므로
동일한 연결에서 `execute()`로 SQL을 직접 실행합니다.

```javascript
await conn.execute('BEGIN');
await conn.execute(
    'UPDATE orders SET status = ? WHERE order_id = ?',
    ['DONE', 1001]
);
await conn.execute('COMMIT');
```

#### 테이블 타입별 SQL 제약

| 테이블 타입 | SELECT | INSERT | UPDATE | DELETE |
|-------------|--------|--------|--------|--------|
| LOG | 지원 | 지원 | 미지원 | 지원 |
| TAG | 지원 | 지원 | 지원 (태그/시간 조건 필요) | 지원 |
| VOLATILE | 지원 | 지원 | 지원 | 지원 |
| LOOKUP | 지원 | 지원 | 지원 | 지원 |

#### 결과 버퍼링

`query()` 메서드는 전체 결과를 메모리에 버퍼링합니다. 대용량 테이블에서는 `LIMIT`나 키 범위를 이용해 페이지를 나누십시오.

```javascript
// 페이지 단위로 조회
const pageSize = 1000;
let offset = 0;
while (true) {
    const [rows] = await conn.query(
        `SELECT * FROM big_table ORDER BY ID LIMIT ? OFFSET ?`,
        [pageSize, offset]
    );
    if (rows.length === 0) break;
    // 처리...
    offset += pageSize;
}
```

### 모범 사례

1. **항상 연결 닫기**: `try...finally` 블록으로 `conn.end()`가 반드시 호출되도록 합니다.
2. **Prepared Statement 재사용**: 동일 쿼리를 반복 실행할 때는 `prepare()`로 한 번 준비하고 재사용합니다.
3. **배치 입력 활용**: 단건 `INSERT` 대신 `appendBatch()`나 `appendOpen()`으로 대량 적재를 수행합니다.
4. **파라미터 바인딩 사용**: 문자열 결합 대신 `?`와 배열 또는 `:name`과 객체를
   사용합니다. 자세한 규칙은
   [Named Bind Parameter](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
   참고하십시오.
5. **오류 처리**: 모든 DB 작업을 `try...catch`로 감쌉니다.
6. **rowsFailed 확인**: Append 후에는 `rowsFailed`를 확인해 오류 여부를 점검합니다.

<a id="net-connector"></a>

## .NET Connector

### 개요 {#overview}

모든 지원 와이어 프로토콜(2.1~4.0)을 포괄하는 범용 ADO.NET 프로바이더 **UniMachNetConnector**를 제공합니다. 커넥터는 실행 시 커넥션 문자열을 참고해 올바른 프로토콜을 자동으로 협상하므로, 시계열 데이터 수집·질의 워크로드에도 별도 설정 없이 적합한 프로토콜을 선택합니다.

- 현재 통합 패키지: `UniMachNetConnector` 8.0.54
- 지원 타깃 프레임워크: `net452`, `net5.0`, `net6.0`, `net7.0`, `net8.0`
- 네임스페이스: `Mach.Data.MachClient`

### 설치 {#install}

#### NuGet 패키지 설치 (권장) {#nuget}

새 프로젝트에는 NuGet 패키지 참조 방식을 권장합니다.

```bash
dotnet add package UniMachNetConnector --version 8.0.54
dotnet build
```

**Visual Studio**를 사용하는 경우:

1. 프로젝트 마우스 오른쪽 클릭 → **NuGet 패키지 관리**
2. **찾아보기** 탭에서 `UniMachNetConnector` 검색
3. 버전 8.0.54 선택 → **설치**

**프로젝트 파일(`.csproj`) 직접 편집:**

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.54" />
</ItemGroup>
```

#### 로컬 DLL 참조

설치된 Machbase 서버·클라이언트에는 `$MACHBASE_HOME/lib/` 경로에 범용 .NET 프로바이더가 함께 배포됩니다.

- `UniMachNetConnector-net50-8.0.54.dll` – universal entry point
- `machNetConnector-40-net50-3.2.1.dll` – protocol 4.0-full connector

응용 프로그램에서는 대상 프레임워크에 맞는 DLL을 참조하거나, 배포 시 실행 파일과 같은 위치에 함께 배치하면 됩니다.

### 커넥션 문자열 {#connection-string}

커넥션 문자열의 각 항목은 세미콜론(`;`)으로 구분합니다.

| 키워드 | 설명 | 예시 | 기본값 |
|--------|------|------|--------|
| `SERVER`, `HOST`, `DSN` | 호스트명 또는 IP 주소 | `SERVER=127.0.0.1` | 없음 |
| `PORT`, `PORT_NO` | 수신 포트 | `PORT_NO=5656` | `5656` |
| `UID`, `USER`, `USERNAME`, `USERID` | 사용자 이름 | `UID=SYS` | `SYS` |
| `PWD`, `PASSWORD` | 비밀번호 | `PWD=MANAGER` | 없음 |
| `CONNECT_TIMEOUT`, `ConnectionTimeout` | 커넥션 타임아웃(밀리초) | `CONNECT_TIMEOUT=10000` | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout` | 명령별 타임아웃(밀리초) | `COMMAND_TIMEOUT=50000` | `60000` |
| `PROTOCOL`, `ProtocolVersion` | 와이어 프로토콜 (`2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full`) | `PROTOCOL=4.0-full` | `4.0` |

**예시:**

```csharp
var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
```

#### 프로토콜 자동 감지

서버 버전이 혼재된 환경이라면 `PROTOCOL=auto`를 지정해 커넥터가 실행 시 적절한 프로토콜을 협상하도록 설정할 수 있습니다.

- `PROTOCOL=auto`: 4.0 → 3.0 → 2.2 → 2.1 순서로 핸드셰이크 시도
- `PROTOCOL=auto-full`: 위와 같지만 4.0-full을 먼저 시도하고 필요 시 4.0으로 폴백

이미 서버 버전을 알고 있다면 명시적으로 지정해 자동 감지를 건너뛰는 것이 좋습니다.

### API 레퍼런스 {#api-reference}

{{< callout type="warning" >}}
아래에 명시되지 않은 기능은 아직 구현되지 않았거나 정상적으로 동작하지 않을 수 있습니다. 존재하지 않는 메서드나 필드를 호출하면 `NotImplementedException` 또는 `NotSupportedException`이 발생합니다.
{{< /callout >}}

#### MachConnection

```csharp
public sealed class MachConnection : DbConnection
```

Machbase와의 연결을 담당하는 클래스입니다. `IDisposable`을 구현하므로 `using` 문으로 안전하게 해제할 수 있습니다.

| 멤버 | 설명 |
|------|------|
| `MachConnection(string connString)` | 커넥션 문자열로 인스턴스 생성 |
| `Open()` | 실제 연결 수립 |
| `Close()` | 연결 종료 |
| `SetConnectAppendFlush(bool)` | Append 중 자동 flush 활성화 여부 설정 |
| `State` | `System.Data.ConnectionState` 현재 상태 |

#### MachCommand

```csharp
public sealed class MachCommand : DbCommand
```

SQL 명령이나 Append 작업을 실행하는 클래스입니다.

| 멤버 | 설명 |
|------|------|
| `MachCommand(string sql, MachConnection conn)` | 쿼리와 연결 객체로 생성 |
| `MachCommand(MachConnection conn)` | Append 전용 커맨드 생성 |
| `ExecuteNonQuery()` | INSERT/UPDATE/DELETE/DDL 실행, 영향받은 레코드 수 반환 |
| `ExecuteScalar()` | 첫 번째 컬럼 값 반환 |
| `ExecuteReader()` | `MachDataReader` 반환 |
| `AppendOpen(tableName, errorCheckCount, option)` | Append 세션 열기, `MachAppendWriter` 반환 |
| `AppendData(writer, dataList)` | 리스트의 값을 Append 버퍼에 적재 |
| `AppendDataWithTime(writer, dataList, DateTime)` | `_arrival_time`을 `DateTime`으로 지정 |
| `AppendDataWithTime(writer, dataList, ulong)` | `_arrival_time`을 나노초 `ulong`으로 지정 |
| `AppendFlush(writer)` | 버퍼를 즉시 서버로 전송 |
| `AppendClose(writer)` | Append 세션 종료 |
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수 (기본값: 3000) |

#### MachDataReader

```csharp
public sealed class MachDataReader : DbDataReader
```

`MachCommand.ExecuteReader()`로 획득하는 순차 결과 리더입니다.

| 멤버 | 설명 |
|------|------|
| `Read()` | 다음 레코드 읽기. 결과가 없으면 `false` 반환 |
| `GetName(int ordinal)` | 컬럼 이름 반환 |
| `GetValue(int ordinal)` | 현재 레코드 값을 `object`로 반환 |
| `GetInt32/GetInt64/GetDouble/GetString/GetDateTime(int)` | 타입별 값 반환 |
| `IsDBNull(int ordinal)` | NULL 여부 확인 |
| `FieldCount` | 결과 컬럼 수 |
| `HasRows` | 결과 존재 여부 |

#### MachAppendWriter

`MachCommand.AppendOpen()` 호출 시 반환되는 보조 클래스입니다.

| 멤버 | 설명 |
|------|------|
| `SetErrorDelegator(callback)` | Append 오류 발생 시 호출할 델리게이트 등록 |
| `SuccessCount` | 성공적으로 저장된 레코드 수 (`AppendClose()` 이후 확인) |
| `FailureCount` | 실패한 레코드 수 (`AppendClose()` 이후 확인) |

#### MachParameterCollection

파라미터 바인딩을 위한 컬렉션입니다. `MachCommand.ParameterCollection`으로 접근합니다.

| 멤버 | 설명 |
|------|------|
| `Add(name, DbType)` | 파라미터 이름과 타입으로 추가 |
| `AddWithValue(name, value)` | 이름과 값으로 추가 |
| `Clear()` | 모든 파라미터 제거 |

### 사용 예제 {#examples}

#### 연결

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using (var conn = new MachConnection(connString))
{
    conn.Open();
    // 작업 수행
} // using 블록 종료 시 자동으로 Close()
```

#### 테이블 생성 및 INSERT

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

// 테이블 생성
using (var cmd = new MachCommand(
    "CREATE TAG TABLE IF NOT EXISTS sensor_data (" +
    "  name VARCHAR(100) PRIMARY KEY," +
    "  time DATETIME BASETIME," +
    "  value DOUBLE" +
    ")", conn))
{
    cmd.ExecuteNonQuery();
}

// 단건 INSERT
using (var cmd = new MachCommand(
    "INSERT INTO sensor_data VALUES (?, ?, ?)", conn))
{
    cmd.ParameterCollection.AddWithValue("@name", "sensor-1");
    cmd.ParameterCollection.AddWithValue("@time", DateTime.UtcNow);
    cmd.ParameterCollection.AddWithValue("@value", 3.14);
    cmd.ExecuteNonQuery();
}
```

#### SELECT 조회

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

using var cmd = new MachCommand(
    "SELECT name, time, value FROM sensor_data ORDER BY time DESC LIMIT 10",
    conn);
using var reader = cmd.ExecuteReader();

while (reader.Read())
{
    Console.WriteLine($"name={reader.GetString(0)}, " +
                      $"time={reader.GetDateTime(1)}, " +
                      $"value={reader.GetDouble(2)}");
}
```

#### 파라미터 바인딩

시계열 범위 조회 등에 파라미터를 사용해 SQL 인젝션을 방지할 수 있습니다.

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

const string sql = @"
    SELECT name, time, value
      FROM sensor_data
     WHERE time >= @StartTime
       AND time <  @EndTime
     ORDER BY time";

using var cmd = new MachCommand(sql, conn);

var now  = DateTime.UtcNow;
var past = now.AddMinutes(-10);

cmd.ParameterCollection.Add(new MachParameter { ParameterName = "@StartTime", Value = past });
cmd.ParameterCollection.Add(new MachParameter { ParameterName = "@EndTime",   Value = now  });

using var reader = cmd.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetString(0)}: {reader.GetDouble(2)}");
}
```

#### Append API (고속 대량 삽입)

Append 프로토콜을 사용하면 표준 INSERT보다 훨씬 빠르게 대량의 시계열 데이터를 적재할 수 있습니다.

```csharp
using Mach.Data.MachClient;

var connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;";

using var conn = new MachConnection(connString);
conn.Open();

using var appendCmd = new MachCommand(conn);
var writer = appendCmd.AppendOpen("sensor_data");

// 오류 발생 시 처리할 델리게이트 등록
writer.SetErrorDelegator(e =>
{
    Console.Error.WriteLine($"Append 오류: {e.Message}");
    Console.Error.WriteLine($"실패 레코드: {e.GetRowBuffer()}");
});

var row = new List<object>();
var baseTime = DateTime.UtcNow;

for (var i = 0; i < 100_000; i++)
{
    row.Add($"sensor-{i % 10}");
    row.Add(baseTime.AddMilliseconds(i));
    row.Add((double)i * 0.01);

    appendCmd.AppendData(writer, row);
    row.Clear();

    // 1000건마다 중간 flush
    if (i % 1000 == 0)
    {
        appendCmd.AppendFlush(writer);
    }
}

appendCmd.AppendClose(writer);
Console.WriteLine($"성공: {writer.SuccessCount}, 실패: {writer.FailureCount}");
```

#### Append - _arrival_time 직접 지정

```csharp
// DateTime으로 arrival time 지정
appendCmd.AppendDataWithTime(writer, row, DateTime.UtcNow);

// 나노초(ulong)로 arrival time 지정 (1970-01-01 UTC 기준)
ulong nanoTs = (ulong)(DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() * 1_000_000L);
appendCmd.AppendDataWithTime(writer, row, nanoTs);
```

### 프로토콜 4.0-full 확장 API {#protocol-40-full}

`PROTOCOL=4.0-full`을 사용하면 추가적인 ADO.NET 기능을 활용할 수 있습니다. Machbase 7.x 이상 서버에서만 사용 가능합니다.

#### 추가 제공 타입

| 타입 | 설명 |
|------|------|
| `MachDbProviderFactory` | `DbProviderFactories` 등록/생성 지원 |
| `MachConnectionStringBuilder` | 키워드 오타 없이 커넥션 문자열 구성 |
| `MachDataAdapter` | `DataTable`/`DataSet` 기반 워크플로 지원 |
| `MachCommandBuilder` | SELECT 문으로부터 INSERT 구문 자동 생성 |

#### MachConnectionStringBuilder 사용

```csharp
using Mach.Data.MachClient;

var builder = new MachConnectionStringBuilder
{
    Server   = "127.0.0.1",
    Port     = 5656,
    UserID   = "SYS",
    Password = "MANAGER"
};
builder["PROTOCOL"] = "4.0-full";

using var conn = new MachConnection(builder.ConnectionString);
conn.Open();
```

#### MachDbProviderFactory 활용

Dapper 등 프로바이더 중립 라이브러리와 연동 시 활용합니다.

```csharp
using System.Data.Common;
using Mach.Data.MachClient;

// 시작 시 한 번만 등록
MachDbProviderFactory.Register();

DbProviderFactory factory = MachDbProviderFactory.Instance;
using DbConnection conn = factory.CreateConnection()!;
conn.ConnectionString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
conn.Open();

using DbCommand cmd = conn.CreateCommand();
cmd.CommandText = "SELECT COUNT(*) FROM M$SYS_TABLES";
var count = (long)cmd.ExecuteScalar()!;
Console.WriteLine($"테이블 수: {count}");
```

#### MachDataAdapter로 Lookup 테이블 조작

```csharp
using Mach.Data.MachClient;
using System.Data;

var connString =
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";

using var conn = new MachConnection(connString);
conn.Open();

var adapter = new MachDataAdapter("SELECT id, name FROM lookup_table ORDER BY id", conn);
var cmdBuilder = new MachCommandBuilder(adapter);

var table = new DataTable();
adapter.Fill(table);

var newRow = table.NewRow();
newRow["id"]   = 1001;
newRow["name"] = "새 항목";
table.Rows.Add(newRow);

adapter.Update(table);
```

{{< callout type="info" >}}
로그 테이블과 태그 테이블은 UPDATE를 지원하지 않습니다. UPDATE/DELETE가 필요한 경우에는 Lookup 또는 Volatile 테이블을 사용하십시오.
{{< /callout >}}

### Entity Framework / LINQ {#ef-linq}

현재 UniMachNetConnector는 Entity Framework Core의 공식 프로바이더를 제공하지 않습니다. ADO.NET 직접 사용(`MachConnection`, `MachCommand`, `MachDataReader`) 또는 Dapper 같은 마이크로 ORM과 함께 사용하는 것을 권장합니다.

`4.0-full` 프로토콜의 `MachDbProviderFactory`를 통해 Dapper와 연동하면 LINQ 스타일의 편의성을 일부 활용할 수 있습니다.

<a id="go"></a>

## Go

### 개요

Go 애플리케이션을 위해 두 가지 연결 방식을 제공합니다.

| 방식 | 패키지 | 특징 |
|------|--------|------|
| [Go 클라이언트](/dbms/application-integration/guide-drivers/#go) | `github.com/machbase/neo-client/machgo` | Machbase 네이티브 API, Append 고속 삽입 지원 |
| [Go SQL 드라이버](/dbms/application-integration/guide-drivers/#go-sql) | `github.com/machbase/neo-client` | Go 표준 `database/sql` 인터페이스 |

### 어느 방식을 선택해야 하나요?

**Go 클라이언트 (`machgo`)를 선택하십시오:**
- 최대 성능이 필요한 경우 (Append API로 고속 대량 삽입)
- Machbase 고유 기능(세밀한 연결 튜닝, FetchRows 제어 등)을 활용하고 싶은 경우
- 신규 프로젝트에서 Machbase 전용 코드로 작성하는 경우

**Go SQL 드라이버를 선택하십시오:**
- 기존 코드가 `database/sql` 인터페이스를 사용하는 경우
- GORM, sqlx 등 `database/sql` 기반 라이브러리와 함께 사용하는 경우
- 여러 데이터베이스를 추상화된 인터페이스로 다루는 경우

### 공통 사전 요구사항

- Machbase 서버가 네이티브 포트(기본 `5656`)로 접근 가능해야 합니다.
- Go 1.22 이상이 설치되어 있어야 합니다.

### 패키지 설치

두 방식 모두 동일한 패키지를 사용합니다.

```sh
go get github.com/machbase/neo-client@latest
```

<a id="go-go"></a>

### Go 클라이언트

#### 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜에 접근하기 위한 순수 Go 클라이언트입니다. CGo 의존성이 없으며, `database/sql` 표준 인터페이스 없이 Machbase 고유 API를 직접 사용합니다. 고성능 Append API를 통한 대량 삽입에 최적화되어 있습니다.

##### 주요 특징

- **CGo 의존성 없음**: 순수 Go 환경에서 빌드 및 배포 가능
- **네이티브 프로토콜**: Machbase 네이티브 포트(기본 `5656`)로 직접 연결
- **Append API**: 고속 대량 삽입을 위한 전용 인터페이스
- **세밀한 튜닝**: 연결별 FetchRows, StatementCache 설정 가능
- **PRIMARY KEY 메타데이터**: `Rows.Columns()`와 `Row.Columns()`에서 직접 컬럼의 PK 상태 확인

#### 설치 {#install}

```sh
go get github.com/machbase/neo-client@latest
```

##### Import

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

#### 데이터베이스 인스턴스 생성 {#database}

`machgo.Config`로 연결 풀 설정을 구성한 뒤 `NewDatabase()`로 인스턴스를 생성합니다.

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase 서버 호스트
    Port:         5656,         // 네이티브 포트
    MaxOpenConn:  0,            // 0: CPU 수 × 팩터(기본 1.5)
    MaxOpenQuery: 0,            // 0: CPU 수 × 팩터(기본 1.5)
}

mdb, err := machgo.NewDatabase(conf)
if err != nil {
    log.Fatal(err)
}
```

##### 설정 매개변수

| 매개변수 | 설명 | 값 |
|----------|------|-----|
| `MaxOpenConn` | 최대 오픈 연결 수 | `< 0`: 무제한, `0`: CPU 수 × 팩터, `> 0`: 지정 제한 |
| `MaxOpenConnFactor` | `MaxOpenConn=0`일 때 승수 | 기본값: `1.5` |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한, `0`: CPU 수 × 팩터, `> 0`: 지정 제한 |
| `MaxOpenQueryFactor` | `MaxOpenQuery=0`일 때 승수 | 기본값: `1.5` |
| `FetchRows` | 기본 pre-fetch 레코드 수 | 기본값: `1000` |

#### 연결 {#connect}

```go
ctx := context.Background()

conn, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithDatabase("FACTORY_A"),
)
if err != nil {
    log.Fatal(err)
}
defer conn.Close()
```

`api.WithDatabase(database)`는 연결 직후 초기 database를 선택합니다. 연결 후 `USE`로
database를 바꿀 수 있으며, 다른 database의 Append 대상은 `database.owner.table` 세 부분
이름으로 지정합니다. 세부 동작과 CMI 4.0.3 호환 조건은
[Go SDK 문서](/dbms/development-tools-integration/go/)를 참조하십시오.

{{< callout type="warning" >}}
리소스 해제를 위해 연결에는 항상 `Close()`를 호출하십시오. `defer conn.Close()` 패턴을 권장합니다.
{{< /callout >}}

##### 연결별 튜닝 옵션

`Connect()` 호출 시 전역 설정을 연결별로 재정의할 수 있습니다.

```go
// Statement 캐시 활성화 (동일 SQL 반복 실행 시 성능 향상)
connA, err := mdb.Connect(ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)

// 대량 스캔을 위한 큰 pre-fetch 크기
connB, err := mdb.Connect(ctx,
    api.WithPassword("sys", "manager"),
    api.WithFetchRows(5000),
)
```

#### 데이터 조회 {#query}

##### 단일 행 조회 (`QueryRow`)

정확히 한 행을 기대할 때 사용합니다.

```go
var name = "sensor-1"
var tm time.Time
var val float64

row := conn.QueryRow(ctx,
    `SELECT time, value FROM sensor_data WHERE name = ? ORDER BY time DESC LIMIT 1`,
    name,
)
if err := row.Err(); err != nil {
    log.Fatal(err)
}
if err := row.Scan(&tm, &val); err != nil {
    log.Fatal(err)
}

fmt.Printf("name=%s, time=%s, value=%.4f\n", name, tm.Local(), val)
```

##### 다중 행 조회 (`Query`)

여러 행 결과를 순차적으로 읽을 때 사용합니다.

```go
rows, err := conn.Query(ctx,
    `SELECT name, time, value FROM sensor_data
      WHERE name = ?
      ORDER BY time DESC LIMIT 100`,
    "sensor-1",
)
if err != nil {
    log.Fatal(err)
}
defer rows.Close()

for rows.Next() {
    var name string
    var tm   time.Time
    var val  float64

    if err := rows.Scan(&name, &tm, &val); err != nil {
        log.Fatal(err)
    }
    fmt.Printf("name=%s, time=%s, value=%.4f\n", name, tm.Local(), val)
}
```

#### 데이터 수정 (`Exec`) {#exec}

INSERT, DELETE, DDL 실행에는 `Exec`를 사용합니다.

```go
result := conn.Exec(ctx,
    `INSERT INTO sensor_data VALUES (?, ?, ?)`,
    "sensor-1", time.Now(), 3.14,
)
if err := result.Err(); err != nil {
    log.Fatal(err)
}

fmt.Println("RowsAffected:", result.RowsAffected())
```

#### 고속 대량 삽입 (Append API) {#appender}

`Appender`는 대용량 시계열 데이터를 고처리량으로 적재하기 위한 전용 인터페이스입니다. 데이터를 버퍼에 쌓아 두었다가 임계값에 도달하면 서버로 일괄 전송합니다.

{{< callout type="warning" >}}
Appender를 사용하는 연결에서는 일반 쿼리를 함께 실행하지 마십시오. Append 워크로드에는 반드시 별도 연결을 사용하십시오.
{{< /callout >}}

##### 기본 사용법

```go
apd, err := conn.Appender(ctx, "sensor_data")
if err != nil {
    log.Fatal(err)
}
defer apd.Close()

for i := range 10_000 {
    if err := apd.Append("sensor-1", time.Now(), float64(i)*0.1); err != nil {
        log.Fatal(err)
    }
}
```

##### 버퍼 임계값 설정

임계값 중 하나라도 초과하면 버퍼를 서버로 전송합니다.

```go
apd, err := conn.Appender(ctx, "sensor_data")
if err != nil {
    log.Fatal(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).          // 1 MB 임계값
    WithBatchMaxRows(2000).                   // 2000 행 임계값
    WithBatchMaxDelay(500 * time.Millisecond) // 500ms 시간 임계값
```

| 옵션 | 기본값 | 최소값 | 설명 |
|------|--------|--------|------|
| `WithBatchMaxRows(rows)` | 512 | 1 | 버퍼 내 최대 행 수 |
| `WithBatchMaxBytes(bytes)` | 512KB | 4KB | 버퍼 최대 크기 |
| `WithBatchMaxDelay(duration)` | 5ms | 1ms | 버퍼 내 최장 대기 시간 (`0` 설정 시 시간 조건 비활성화) |

##### 수동 Flush

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

#### 전체 예제 {#full-example}

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    // 1. 데이터베이스 인스턴스 생성
    conf := &machgo.Config{
        Host:         "127.0.0.1",
        Port:         5656,
        MaxOpenConn:  -1,
        MaxOpenQuery: -1,
    }

    mdb, err := machgo.NewDatabase(conf)
    if err != nil {
        log.Fatal(err)
    }

    ctx := context.Background()

    // 2. 연결
    conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // 3. 테이블 생성
    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sensor_data (
            name  VARCHAR(100) PRIMARY KEY,
            time  DATETIME BASETIME,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    // 4. 단건 INSERT
    for i := 0; i < 5; i++ {
        r := conn.Exec(ctx,
            `INSERT INTO sensor_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor-%d", i),
            time.Now(),
            float64(i)*1.5,
        )
        if err := r.Err(); err != nil {
            log.Fatal(err)
        }
    }

    // 5. TABLE_FLUSH (태그 테이블 데이터 가시성 확보)
    conn.Exec(ctx, `EXEC TABLE_FLUSH(sensor_data)`)

    // 6. SELECT 조회
    rows, err := conn.Query(ctx,
        `SELECT name, time, value FROM sensor_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var name  string
        var tm    time.Time
        var value float64

        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Name: %-12s  Time: %s  Value: %.2f\n",
            name, tm.Local().Format(time.RFC3339), value)
    }

    // 7. Appender로 대량 삽입
    appendConn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer appendConn.Close()

    apd, err := appendConn.Appender(ctx, "sensor_data")
    if err != nil {
        log.Fatal(err)
    }

    baseTime := time.Now()
    for i := range 10_000 {
        if err := apd.Append(
            fmt.Sprintf("bulk-%d", i%10),
            baseTime.Add(time.Duration(i)*time.Millisecond),
            float64(i)*0.01,
        ); err != nil {
            log.Fatal(err)
        }
    }

    if err := apd.Close(); err != nil {
        log.Fatal(err)
    }
    fmt.Println("Append 완료")
}
```

<a id="go-sql"></a>
<a id="go-go-sql"></a>

### Go SQL 드라이버

#### 개요

`github.com/machbase/neo-client` 패키지는 Go 표준 `database/sql` 인터페이스를 통해 Machbase에 연결하는 드라이버를 제공합니다. 네이티브 TCP 클라이언트를 기반으로 하며, 네이티브 포트(기본 `5656`)를 사용합니다.

기존 코드가 `database/sql` 인터페이스를 사용하거나, GORM·sqlx 같은 `database/sql` 기반 라이브러리와 함께 사용할 때 적합합니다. Machbase 고유 기능(Append API 등)이 필요하다면 [Go 클라이언트](#go)를 검토하십시오.

#### 설치 {#install}

```sh
go get github.com/machbase/neo-client@latest
```

##### Import

드라이버 패키지를 blank identifier(`_`)로 import합니다. 드라이버 이름 `"machbase"`로 자동 등록되므로 별도의 `sql.Register()` 호출은 필요하지 않습니다.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

#### 연결 {#connect}

##### DSN 형식

세미콜론(`;`)으로 구분된 키=값 쌍을 DSN으로 사용합니다.

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=1000
```

Statement 캐시를 추가하는 경우:

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=1000;statement_cache=auto
```

초기 database는 key-value의 `database`/`db`, URL path 또는 URL query로 지정할 수 있습니다.

```text
server=tcp://sys:manager@127.0.0.1:5656;database=FACTORY_A
tcp://sys:manager@127.0.0.1:5656/FACTORY_A
tcp://sys:manager@127.0.0.1:5656?database=FACTORY_A
```

##### 지원되는 DSN 키

| 키 | 설명 | 예시 |
|----|------|------|
| `server` | 서버 URL (`tcp://user:password@host:port` 형식) | `server=tcp://sys:manager@127.0.0.1:5656` |
| `host`, `port` | 호스트와 포트를 별도로 지정 | `host=127.0.0.1;port=5656` |
| `user` | 로그인 사용자 | `user=sys` |
| `password` | 로그인 비밀번호 | `password=manager` |
| `database`, `db` | 새 physical connection의 초기 database | `database=FACTORY_A` |
| `fetch_rows` | 한 번의 round trip에서 가져올 행 수. 현재 드라이버에서는 명시 필요 | `fetch_rows=2000` |
| `statement_cache` | Statement 캐시 모드: `auto`, `on`, `off` | `statement_cache=auto` |
| `io_metrics` | I/O metrics 활성화: `true`, `false` | `io_metrics=true` |
| `alternative_servers` | 대체 서버 주소 | `alternative_servers=127.0.0.2:5656` |

##### sql.Open

```go
fields := []string{
    "server=tcp://sys:manager@127.0.0.1:5656",
    "fetch_rows=1000",
    "statement_cache=auto",
}

db, err := sql.Open("machbase", strings.Join(fields, ";"))
if err != nil {
    log.Fatal(err)
}
defer db.Close()
```

#### 데이터 조회 예제 {#query-example}

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "strings"

    _ "github.com/machbase/neo-client"
)

func main() {
    dsn := strings.Join([]string{
        "server=tcp://sys:manager@127.0.0.1:5656",
        "fetch_rows=1000",
        "statement_cache=auto",
    }, ";")

    db, err := sql.Open("machbase", dsn)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    ctx := context.Background()

    // 시스템 테이블 목록 조회
    rows, err := db.QueryContext(ctx, `SELECT NAME, TYPE FROM M$SYS_TABLES ORDER BY NAME`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    columns, err := rows.Columns()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Columns:", columns)

    for rows.Next() {
        var name string
        var typ  int
        if err := rows.Scan(&name, &typ); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("  name=%-30s type=%d\n", name, typ)
    }

    if err := rows.Err(); err != nil {
        log.Fatal(err)
    }
}
```

#### 데이터 삽입 예제 {#insert-example}

다음 예제는 태그 테이블에 행을 삽입합니다. 먼저 테이블을 생성합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name  VARCHAR(100) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);
```

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "strings"
    "time"

    _ "github.com/machbase/neo-client"
)

func main() {
    dsn := strings.Join([]string{
        "server=tcp://sys:manager@127.0.0.1:5656",
        "fetch_rows=1000",
    }, ";")

    db, err := sql.Open("machbase", dsn)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    ctx := context.Background()
    baseTime := time.Now()

    for i := 0; i < 10; i++ {
        result, err := db.ExecContext(ctx,
            `INSERT INTO example VALUES (?, ?, ?)`,
            "sensor-1",
            baseTime.Add(time.Second*time.Duration(i)),
            3.14*float64(i),
        )
        if err != nil {
            log.Fatal(err)
        }

        affected, err := result.RowsAffected()
        if err != nil {
            log.Fatal(err)
        }
        fmt.Println("RowsAffected:", affected)
    }
}
```

#### Prepared Statement {#prepared-statement}

`database/sql`의 표준 Prepared Statement를 사용할 수 있습니다. 동일한 쿼리를 반복 실행할 때 `statement_cache=auto` DSN 옵션과 함께 사용하면 성능이 향상됩니다.

```go
ctx := context.Background()

stmt, err := db.PrepareContext(ctx, `INSERT INTO example VALUES (?, ?, ?)`)
if err != nil {
    log.Fatal(err)
}
defer stmt.Close()

for i := 0; i < 100; i++ {
    _, err := stmt.ExecContext(ctx,
        fmt.Sprintf("sensor-%d", i%5),
        time.Now().Add(time.Duration(i)*time.Millisecond),
        float64(i)*0.1,
    )
    if err != nil {
        log.Fatal(err)
    }
}
```

#### 단일 행 조회 (`QueryRow`) {#queryrow}

```go
if _, err := db.ExecContext(ctx, `EXEC TABLE_FLUSH(example)`); err != nil {
    log.Fatal(err)
}

var name  string
var tm    time.Time
var value float64

err = db.QueryRowContext(ctx,
    `SELECT name, time, value FROM example WHERE name = ? ORDER BY time DESC LIMIT 1`,
    "sensor-1",
).Scan(&name, &tm, &value)

if err == sql.ErrNoRows {
    fmt.Println("결과 없음")
} else if err != nil {
    log.Fatal(err)
} else {
    fmt.Printf("name=%s, time=%s, value=%.4f\n", name, tm.Local(), value)
}
```

#### 제한 사항 {#limitations}

| 항목 | 내용 |
|------|------|
| 파라미터 형식 | positional `?`와 named marker를 지원. 값은 `sql.Named()`으로 전달하며 한 문장에서 두 방식을 혼용할 수 없음 |
| 트랜잭션 | 기본 isolation level의 `Begin`, `BeginTx`, `Commit`, `Rollback` 지원. 사용자 지정 isolation과 ReadOnly는 미지원 |
| LastInsertId | 미지원 |
| bool 파라미터 | 미지원. 정수(`0`/`1`)로 대체 |
| 지원 타입 | 일반 SQL 타입, `time.Time`, `[]byte`, `net.IP`, `api.Decimal` |
| Nullable 메타데이터 | `Rows.ColumnTypeNullable()` 지원. 알 수 없는 경우 `ok=false` 반환 |
| PRIMARY KEY 메타데이터 | 표준 `database/sql.ColumnType`에는 PK API가 없음. 필요하면 Go native `api.Column.PrimaryKey` 또는 카탈로그 조회 사용 |
| Append API | 표준 `sql.DB`/`sql.Tx`에는 없음. `sql.Conn.Raw()`의 `machbase.Conn.Appender()` 확장 또는 [Go 클라이언트](#go) 사용 |

<a id="r-rodbc"></a>

## R / RODBC

### 개요

R 언어에서 ODBC 인터페이스를 통해 Machbase에 연결할 수 있습니다. `RODBC` 패키지를 사용하면 Machbase를 일반 ODBC 데이터 소스로 취급하여 SQL 쿼리를 실행하고 결과를 `data.frame`으로 받아볼 수 있습니다.

#### 구성 요소

| 구성 요소 | 설명 |
|-----------|------|
| Machbase ODBC 드라이버 | `libmachbaseodbc.so` (Linux) / `machbaseodbc.dll` (Windows) |
| ODBC 관리자 | unixODBC (Linux) 또는 Windows ODBC 데이터 원본 관리자 |
| R 패키지 | `RODBC` |

### 사전 요구사항 {#prerequisites}

#### 1. Machbase ODBC 드라이버 확인

Machbase 설치 경로의 `lib` 디렉터리에 ODBC 드라이버 파일이 있는지 확인합니다.

```sh
ls $MACHBASE_HOME/lib/libmachbaseodbc.so   # Linux
```

Windows의 경우 `%MACHBASE_HOME%\lib\machbaseodbc.dll`을 사용합니다.

#### 2. unixODBC 설치 (Linux)

```sh
# Ubuntu / Debian
sudo apt-get install unixodbc unixodbc-dev

# RHEL / CentOS
sudo yum install unixODBC unixODBC-devel
```

#### 3. R 및 RODBC 패키지 설치

```r
install.packages("RODBC")
```

### ODBC 드라이버 등록 {#odbc-config}

#### Linux: `/etc/odbcinst.ini` 또는 `~/.odbcinst.ini`

Machbase ODBC 드라이버를 시스템에 등록합니다.

```ini
[MachbaseODBC]
Description = Machbase ODBC Driver
Driver      = /path/to/machbase/lib/libmachbaseodbc.so
Setup       = /path/to/machbase/lib/libmachbaseodbc.so
FileUsage   = 1
```

#### DSN 설정 {#dsn-config}

##### Linux: `/etc/odbc.ini` (시스템 DSN) 또는 `~/.odbc.ini` (사용자 DSN)

```ini
[machbase_dsn]
Description = Machbase Database
Driver      = MachbaseODBC
SERVER      = 127.0.0.1
PORT_NO     = 5656
UID         = SYS
PWD         = MANAGER
```

##### Windows: 시스템 DSN

1. **시작** → **ODBC 데이터 원본 관리자** (64비트) 실행
2. **시스템 DSN** 탭 → **추가**
3. 목록에서 `MachbaseODBC` 드라이버 선택
4. DSN 이름(`machbase_dsn`), 서버 주소, 포트, 사용자 정보 입력
5. **확인** 클릭

#### DSN 설정 확인 (Linux)

```sh
isql -v machbase_dsn SYS MANAGER
```

접속에 성공하면 `SQL>` 프롬프트가 나타납니다.

### R에서 연결 {#r-connect}

```r
library(RODBC)

# DSN으로 연결
ch <- odbcConnect("machbase_dsn")

# 연결 성공 여부 확인
if (ch < 0) {
  stop("Machbase 연결 실패: ", odbcGetErrMsg(ch))
}

cat("Machbase에 연결되었습니다.\n")
```

#### DSN 없이 직접 연결 (연결 문자열)

```r
library(RODBC)

ch <- odbcDriverConnect(
  "DRIVER=MachbaseODBC;SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER"
)
```

### 데이터 조회 {#query}

#### 테이블 조회

```r
library(RODBC)

ch <- odbcConnect("machbase_dsn")

# SQL 쿼리 실행 → data.frame 반환
result <- sqlQuery(ch, "SELECT name, time, value FROM sensor_data ORDER BY time DESC")

# 결과 확인
print(head(result, 10))
str(result)
summary(result)
```

#### 조건부 조회

```r
# 특정 센서의 최근 1시간 데이터 조회
query <- "
  SELECT name, time, value
    FROM sensor_data
   WHERE name = 'sensor-1'
     AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   ORDER BY time DESC
   LIMIT 1000
"

df <- sqlQuery(ch, query)
cat("조회된 행 수:", nrow(df), "\n")
```

#### 집계 쿼리

```r
# 센서별 평균값 집계
agg <- sqlQuery(ch, "
  SELECT name,
         COUNT(*)  AS cnt,
         AVG(value) AS avg_value,
         MIN(value) AS min_value,
         MAX(value) AS max_value
    FROM sensor_data
   GROUP BY name
   ORDER BY name
")

print(agg)
```

### 데이터 삽입 {#insert}

#### sqlQuery로 INSERT

```r
# 단건 삽입
sqlQuery(ch, "INSERT INTO sensor_data VALUES ('sensor-r', NOW, 3.14)")

# R 변수를 사용한 삽입 (sprintf로 SQL 조합)
name  <- "sensor-r"
value <- 2.71

sql <- sprintf(
  "INSERT INTO sensor_data VALUES ('%s', NOW, %f)",
  name, value
)
sqlQuery(ch, sql)
```

{{< callout type="warning" >}}
문자열 값을 직접 SQL에 삽입할 때는 SQL 인젝션에 주의하십시오. 신뢰할 수 없는 입력값은 반드시 이스케이프 처리 후 사용하십시오.
{{< /callout >}}

#### sqlSave로 data.frame 일괄 삽입

`sqlSave()`를 사용하면 `data.frame`을 테이블에 일괄 삽입할 수 있습니다.

```r
# 삽입할 데이터 준비
new_data <- data.frame(
  name  = c("sensor-r", "sensor-r", "sensor-r"),
  time  = as.POSIXct(c("2024-01-01 00:00:00",
                        "2024-01-01 00:01:00",
                        "2024-01-01 00:02:00")),
  value = c(1.1, 2.2, 3.3)
)

# 테이블에 삽입 (append = TRUE: 기존 데이터 유지)
sqlSave(ch, new_data, tablename = "sensor_data", append = TRUE, rownames = FALSE)
```

### 시각화 예제 {#visualization}

Machbase에서 조회한 시계열 데이터를 R로 바로 시각화할 수 있습니다.

```r
library(RODBC)

ch <- odbcConnect("machbase_dsn")

# 데이터 조회
df <- sqlQuery(ch, "
  SELECT time, value
    FROM sensor_data
   WHERE name = 'sensor-1'
   ORDER BY time
   LIMIT 500
")

# time 컬럼을 POSIXct로 변환
df$time <- as.POSIXct(df$time)

# 시계열 플롯
plot(df$time, df$value,
     type  = "l",
     col   = "steelblue",
     xlab  = "시간",
     ylab  = "측정값",
     main  = "sensor-1 시계열 데이터")

odbcClose(ch)
```

### 연결 해제 {#disconnect}

```r
# 단일 연결 해제
odbcClose(ch)

# 열린 모든 ODBC 연결 해제
odbcCloseAll()
```

### 오류 처리 {#error-handling}

```r
library(RODBC)

ch <- odbcConnect("machbase_dsn")

tryCatch({
  result <- sqlQuery(ch, "SELECT * FROM sensor_data LIMIT 10", errors = TRUE)

  if (is.character(result)) {
    # sqlQuery는 오류 시 오류 메시지 문자열을 반환
    cat("오류 발생:", result, "\n")
  } else {
    print(result)
  }
}, finally = {
  odbcClose(ch)
})
```

### 주요 RODBC 함수 참고 {#rodbc-functions}

| 함수 | 설명 |
|------|------|
| `odbcConnect(dsn)` | DSN으로 연결 |
| `odbcDriverConnect(connStr)` | 연결 문자열로 연결 |
| `sqlQuery(ch, sql)` | SQL 실행 후 `data.frame` 반환 |
| `sqlFetch(ch, tableName)` | 테이블 전체를 `data.frame`으로 읽기 |
| `sqlSave(ch, df, tablename)` | `data.frame`을 테이블에 저장 |
| `sqlTables(ch)` | 사용 가능한 테이블 목록 조회 |
| `sqlColumns(ch, tableName)` | 테이블 컬럼 정보 조회 |
| `odbcGetErrMsg(ch)` | 오류 메시지 조회 |
| `odbcClose(ch)` | 연결 해제 |
| `odbcCloseAll()` | 모든 연결 해제 |

### 문제 해결 {#troubleshooting}

**드라이버를 찾을 수 없는 경우**

```sh
# 등록된 드라이버 목록 확인
odbcinst -q -d

# DSN 목록 확인
odbcinst -q -s
```

**연결 오류가 발생하는 경우**

- Machbase 서버가 실행 중인지 확인
- 방화벽에서 포트 5656이 열려 있는지 확인
- `isql -v machbase_dsn SYS MANAGER`로 ODBC 레벨에서 먼저 연결 테스트
- `LD_LIBRARY_PATH`에 `$MACHBASE_HOME/lib`가 포함되어 있는지 확인 (Linux)

```sh
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```
