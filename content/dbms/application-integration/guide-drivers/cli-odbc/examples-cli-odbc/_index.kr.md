---
type: docs
title: 'CLI/ODBC 예제'
weight: 20
---

이 페이지는 Machbase CLI를 사용하는 C 프로그램의 대표적인 예제를 제공합니다. 모든 예제는 `machbase_sqlcli.h`를 포함하고 `libmachbasecli` 라이브러리와 링크하여 컴파일합니다.

## 개발 환경 준비

### 설치 확인

Machbase가 설치된 디렉터리의 `include`와 `lib`에 다음 파일이 있으면 개발 환경이 준비된 것입니다.

```bash
$ ls $MACHBASE_HOME/include $MACHBASE_HOME/lib

include:
  machbase_sqlcli.h

lib:
  libmachbasecli.a
  libmachbasecli.so
```

### Makefile 작성

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

### 컴파일

```bash
$ cd $MACHBASE_HOME/sample/cli
$ make
```

---

## 예제 1: 접속 및 해제 (sample1_connect.c)

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

## 예제 2: 테이블 생성, INSERT, SELECT (sample2_insert.c)

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
        "CREATE TABLE CLI_SAMPLE1("
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

## 예제 3: Prepare/Execute + SQLBindParameter (sample3_prepare.c)

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

## 예제 4: Append API 고속 삽입 (sample4_append1.c)

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
        "CREATE TABLE CLI_SAMPLE("
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

## 예제 5: 대량 데이터 고속 삽입 (루프 패턴)

실제 시계열 데이터 수집 시나리오에서 초당 수만 건을 입력하는 패턴입니다.

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
        "CREATE TABLE SENSOR_DATA("
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

## 에러 처리 요약

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
