---
type: docs
title: '17.7.1 CLI/ODBC'
weight: 10
toc: true
---


## CLI/ODBC API


CLI(Call Level Interface)는 [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003에 정의된 소프트웨어 개발 표준으로, SQL 전달과 결과 수신에 관한 함수 명세를 규정합니다. 1990년대 초 C와 COBOL 용으로 개발되었으며 현재까지 스펙이 유지되고 있습니다.

ODBC(Open Database Connectivity)는 CLI 기반의 대표적 표준 인터페이스로, 데이터베이스 종류와 무관하게 접속할 수 있는 방법을 제공합니다. 현재 최신 ODBC API 버전은 3.52이며 ISO와 X/Open 표준에 정의되어 있습니다.


## 표준 CLI 함수
표준 함수 사용법은 아래 링크를 참고하십시오.

* [위키피디아](https://en.wikipedia.org/wiki/Call_Level_Interface)
* [오픈그룹 문서](https://www2.opengroup.org/ogsys/catalog/c451)

지원하는 표준 함수 목록:

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

## Nullable 메타데이터 조회

SELECT 결과 컬럼과 Prepared Parameter의 NULL 가능 여부는 다음 세 값으로 반환됩니다.

| 상태 | Native MachCLI | SQLCLI/ODBC |
|------|:--------------:|:-----------:|
| NULL이 될 수 없음 | `0` | `SQL_NO_NULLS` |
| NULL이 될 수 있음 | `1` | `SQL_NULLABLE` |
| 판정할 수 없음 | `2` | `SQL_NULLABLE_UNKNOWN` |

판정할 수 없는 값은 `NOT NULL`이 아닙니다. `SQL_NULLABLE`과
`SQL_NULLABLE_UNKNOWN`을 모두 NULL 처리 대상으로 가정합니다. SQL 식별 규칙은
[Nullable 메타데이터 지원 범위](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-nullable-metadata)를
참고합니다.

### Native MachCLI

Native MachCLI에서는 `<machcli.h>`를 포함하고 `MachCLIDescribeCol()` 또는
`MachCLIDescribeParam()`의 마지막 인자로 Nullable 상태를 받습니다.

```c
int nullable;
int type;
int precision;
int scale;

MachCLIDescribeCol(stmt, column_no,
                   name, sizeof(name), &name_length,
                   &type, &precision, &scale, &nullable);

MachCLIDescribeParam(stmt, parameter_no,
                     &type, &precision, &scale, &nullable);
```

### SQLCLI와 ODBC

SQLCLI와 ODBC에서는 `SQLDescribeCol()`과 `SQLDescribeParam()`의 `NullablePtr`로
Nullable 상태를 받습니다.

```c
SQLSMALLINT nullable;

SQLDescribeCol(stmt, column_no,
               name, sizeof(name), &name_length,
               &type, &precision, &scale, &nullable);

SQLDescribeParam(stmt, parameter_no,
                 &type, &precision, &scale, &nullable);
```

컬럼 속성과 IRD(Implementation Row Descriptor)에서도 같은 값을 조회할 수 있습니다.

```c
SQLLEN nullable_attr;
SQLColAttribute(stmt, column_no, SQL_DESC_NULLABLE,
                NULL, 0, NULL, &nullable_attr);

SQLHDESC ird;
SQLSMALLINT nullable_desc;
SQLGetStmtAttr(stmt, SQL_ATTR_IMP_ROW_DESC, &ird, 0, NULL);
SQLGetDescField(ird, column_no, SQL_DESC_NULLABLE,
                &nullable_desc, 0, NULL);
```

테이블 컬럼의 NULL 제약은 `SQLColumns()` 결과의 `NULLABLE`과 `IS_NULLABLE`로
확인합니다. `PRIMARY KEY`는 Nullable 값으로 판단하지 않고 `SQLPrimaryKeys()`로 별도
조회합니다.

## Named Bind Parameter

ODBC 표준은 이름으로 Prepared Parameter를 바인딩하는 함수를 제공하지 않습니다.
이식성이 필요한 애플리케이션은 `?`와 `SQLBindParameter()`를 사용합니다.

Machbase ODBC 드라이버는 SQL의 `:name` marker를 해석할 수 있지만 값은 SQL에 나타난
순서대로 `SQLBindParameter()`의 ordinal에 바인딩합니다. 같은 이름이 반복되어도 각
위치는 독립된 ordinal이므로 서로 다른 값을 전달할 수 있습니다.

Native MachCLI도 별도의 이름 setter를 제공하지 않습니다. `:name` SQL을 prepare한 뒤
`MachCLIBindParam()`으로 각 발생 위치의 ordinal을 바인딩합니다.

```c
SQLPrepare(stmt,
    (SQLCHAR *)"SELECT ID, NAME FROM SENSOR_DATA "
               "WHERE ID = :id OR PARENT_ID = :id",
    SQL_NTS);

SQLBindParameter(stmt, 1, SQL_PARAM_INPUT,
    SQL_C_SLONG, SQL_INTEGER, 0, 0,
    &first_id, 0, &first_ind);
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT,
    SQL_C_SLONG, SQL_INTEGER, 0, 0,
    &parent_id, 0, &parent_ind);
```

Machbase SQLCLI는 외부 C/C++용 `<machbase_sqlcli.h>`에 다음 비표준 확장을 제공합니다.
이 함수는 ODBC 표준 함수나 Native MachCLI API가 아닙니다.

```c
SQLRETURN SQLBindParameterByName(
    SQLHSTMT stmt,
    SQLCHAR *parameter_name,
    SQLSMALLINT name_length,
    SQLSMALLINT input_output_type,
    SQLSMALLINT value_type,
    SQLSMALLINT parameter_type,
    SQLULEN column_size,
    SQLSMALLINT decimal_digits,
    SQLPOINTER value,
    SQLLEN buffer_length,
    SQLLEN *indicator);

SQLRETURN SQLBindParameterByNameW(
    SQLHSTMT stmt,
    SQLWCHAR *parameter_name,
    SQLSMALLINT name_length,
    SQLSMALLINT input_output_type,
    SQLSMALLINT value_type,
    SQLSMALLINT parameter_type,
    SQLULEN column_size,
    SQLSMALLINT decimal_digits,
    SQLPOINTER value,
    SQLLEN buffer_length,
    SQLLEN *indicator);
```

이름은 선행 콜론 없이 전달합니다. 한 번의 호출로 같은 이름의 모든 발생 위치를
바인딩하며, 이름 기반 API와 ordinal bind를 한 statement에서 혼용할 수 없습니다.
`SQLBindParameterByNameW()`의 이름은 ASCII 문자로 지정합니다.

```c
SQLPrepare(stmt,
    (SQLCHAR *)"INSERT INTO SENSOR_DATA (ID, VALUE) "
               "VALUES (:id, :value)",
    SQL_NTS);

SQLBindParameterByName(stmt, (SQLCHAR *)"id", SQL_NTS,
    SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER,
    0, 0, &id, 0, &id_ind);
SQLBindParameterByName(stmt, (SQLCHAR *)"value", SQL_NTS,
    SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DECIMAL,
    20, 6, decimal_text, sizeof(decimal_text), &value_ind);

SQLExecute(stmt);
```

NULL은 indicator에 `SQL_NULL_DATA`를 지정합니다. 대표 SQLSTATE는 다음과 같습니다.

| SQLSTATE | 상황 |
|---|---|
| `07002` | 이름 기반 바인딩 대상 SQL에 anonymous marker가 있음 |
| `07006` | 필요한 값이 누락되었거나 타입이 맞지 않음 |
| `07009` | 파라미터 이름을 찾을 수 없음 |
| `HY010` | 이름 기반과 ordinal 바인딩을 혼용했거나 호출 순서가 잘못됨 |
| `HY090` | 이름이 유효하지 않음 |
| `HYC00` | 연결된 서버가 이름 기반 API를 지원하지 않음 |

공통 이름 문법과 반복 이름 규칙은
[Named Bind Parameter syntax](../../sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
참고하십시오.

## 접속을 위한 연결 스트링
CLI 접속 시 사용하는 연결 스트링 항목은 다음과 같습니다.

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
|      AUTH_MODE      | 인증 방식입니다. 비밀번호 인증은 `PASSWORD`, 개인키 challenge 인증은 `CHALLENGE`를 사용합니다. `AUTH_KEY_FILE`만 지정하고 `AUTH_MODE`를 생략하면 CLI는 `CHALLENGE`로 처리합니다. |
|   AUTH_SIG_SCHEME   | `AUTH_MODE=CHALLENGE`에서 사용할 서명 스킴입니다. `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`를 지정할 수 있습니다. 생략하면 키 파일에서 기본 스킴을 추론합니다. |
|    AUTH_KEY_FILE    | `AUTH_MODE=CHALLENGE`에서 사용할 로컬 PEM 개인키 파일 경로입니다. challenge 인증에는 필수입니다. |

CLI 접속 예제:

```cpp
sprintf(connStr,"SERVER=127.0.0.1;COMPRESS=512;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

if (SQL_ERROR == SQLDriverConnect( gCon, NULL, (SQLCHAR *)connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT )) {
   ...
}
```

## 확장 CLI 함수 (APPEND)
Machbase 서버에 초고속 데이터를 입력하기 위한 Append 프로토콜 함수입니다. 채널 오픈, 데이터 입력, 플러시, 클로징의 4가지 함수로 구성됩니다.

### Append 프로토콜의 이해
Append 프로토콜은 비동기 방식으로 동작합니다. 클라이언트가 Append를 수행해도 그 결과를 즉시 받을 수 없고, 서버 측에서 처리가 완료되는 시점에 확인할 수 있습니다. 따라서 Append 기반 애플리케이션을 개발할 때는 아래에 설명하는 비동기 에러 검출 동작을 이해해야 합니다.

### Append 데이터의 전송
SQLExecute나 SQLExecDirect()는 결과를 즉시 반환하는 동기 방식이지만, SQLAppendDataV2()는
데이터를 클라이언트 통신 버퍼에 모았다가 버퍼가 가득 차면 서버로 전송합니다. 처리량과 flush
지연은 행 크기, 버퍼 크기와 네트워크 환경에 따라 측정합니다. 버퍼 내용을 즉시 전송하려면
SQLAppendFlush()를 호출하십시오.

### Append 데이터의 에러 확인
Append 프로토콜은 비동기 버퍼링 방식이므로, 서버에서 에러가 없으면 응답이 없고 에러 발생 시에만 검출됩니다. 에러 검출 비용이 크기 때문에 매 레코드마다 검사하지 않고, 다음 세 가지 경우에만 에러를 확인합니다. 에러가 검출되면 사용자가 설정한 에러 콜백 함수를 호출합니다.

1. 전송 버퍼가 모두 차고, 서버에게 명시적으로 데이터를 전송한 이후 검사
2. SQLAppendFlush() 내부에서 서버에게 명시적으로 데이터를 전송한 이후 검사
3. SQLAppendClose() 내부에서 종료 직전에 검사

즉, 기본적으로 위의 3가지 경우에만 에러를 검출하도록 되어 있어, I/O의 발생을 최소화하도록 설계되었습니다.

### 서버 에러 검사를 위한 부가 옵션
SQLAppendOpen() 함수의 마지막 인자인 aErrorCheckCount로 에러 검사 빈도를 조절할 수 있습니다. `0`이면 기본 동작(위 세 가지 경우에만 검출)이고, `0`보다 큰 값을 지정하면 해당 횟수의 SQLAppendData() 호출마다 에러를 검사합니다. 예를 들어 `10`이면 10번마다 검사합니다. 값이 작을수록 시스템 리소스 사용량이 늘어나므로 적절히 조절하십시오.

### 서버 에러 발생시 Trace 로그 남기기
에러가 발생한 Append 데이터의 Trace 로그를 남기려면 서버 프로퍼티 DUMP_APPEND_ERROR를 1로 설정합니다. mach.trc 파일에 에러를 일으킨 레코드 상세가 기록됩니다. 다만 에러가 빈번하면 시스템 리소스 사용량이 급격히 증가하여 전체 성능이 저하될 수 있으므로 주의하십시오.

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

Machbase 2.0에서 도입된 Append 함수로, 기존 함수의 입력 방식을 개선했습니다. TEXT와 BINARY 타입은 이 함수에서만 입력 가능합니다.

* 각 타입에 맞는 NULL 입력 가능
* VARCHAR 입력시 스트링 길이 입력 가능
* IPv4, IPv6 입력시 바이너리 및 스트링 형태의 데이터 입력 가능
* TEXT, BINARY 타입에 대한 데이터 길이 지정 가능

함수 인자는 다음과 같이 구성됩니다.

* aData는 SQL_APPEND_PARAM 이라는 인자배열을 가리키는 포인터입니다. 이 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.
* 리턴값은 SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, SQL_ERROR 가 가능합니다. 특히, SQL_SUCCESS_WITH_INFO가 반환되었을 경우에는 입력된 특정 컬럼의 길이가 길어 잘리는 등의 오류가 있을 수 있으므로 결과를 다시 확인하여야 합니다.

아래는 실제로 V2에서 사용될 SQL_APPEND_PARAM 의 정의이며, 이 내용은 machbase_sqlcli.h 에 포함되어 있습니다.

```cpp
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
    SQL_APPEND_PARAM sParam[1];
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

가변 데이터형에는 VARCHAR, TEXT, BLOB, CLOB이 포함됩니다. 기존 함수에서는 VARCHAR만 지원하며 strlen()으로 길이를 구해야 했지만, V2부터는 길이를 직접 지정할 수 있어 성능이 향상됩니다. 내부적으로는 하나의 구조체이지만, 개발 편의를 위해 데이터 타입별로 멤버를 분리했습니다.

```cpp
typedef struct machbaseAppendVarStruct
{
    unsigned int mLength;
    void *mData;
} machbaseAppendVarStruct;
```

가변 데이터형의 입력시에는 데이터의 길이를 mLength에 설정하고, 원시 데이터 포인터를 mData로 설정하면 됩니다. 만일 mLength의 길이가 정의된 스키마보다 클 경우에는 자동으로 잘려서 입력됩니다. 이때 SQLAppendDataV2() 함수는 SQL_SUCCESS_WITH_INFO을 리턴하게 되고, 더불어 관련 경고 메시지를 내부 구조체에 채웁니다. 이 경고 메시지를 확인하기 위해서는 SQLError() 함수를 이용하면 됩니다.

| 데이터베이스 타입 | NULL 매크로             | SQL_APPEND_PARAM 멤버 (mVar를 사용해도 무방함) |
|-------------------|-------------------------|:----------------------------------------------:|
|      VARCHAR      | SQL_APPEND_VARCHAR_NULL |                    mVarchar                    |
|        TEXT       |   SQL_APPEND_TEXT_NULL  |                      mText                     |
|        JSON       |   SQL_APPEND_JSON_NULL  |                      mJson                     |
|       BINARY      |  SQL_APPEND_BINARY_NULL |                     mBinary                    |
|        BLOB       |   SQL_APPEND_BLOB_NULL  |                      mBlob                     |
|        CLOB       |   SQL_APPEND_CLOB_NULL  |                      mClob                     |

다음은 각각의 환경에 대해 실제 값을 입력하는 예제입니다. 하나의 VARCHAR 컬럼이 존재한다고 가정합니다.

```sql
CREATE LOG TABLE ttt (name VARCHAR(10));
```

```cpp

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

다음은 Text 타입에 대한 입력 예제입니다.

```sql
CREATE LOG TABLE ttt (doc TEXT);
```

```cpp
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

```cpp
SQLRETURN  SQLAppendDataByTimeV2(SQLHSTMT StatementHandle, SQLBIGINT aTime, SQL_APPEND_PARAM  *aData);
```

이 함수는 해당 채널에 대해 데이터를 입력하는 함수이며, DB에 저장되는 _arrival_time 값을 현재 시간이 아닌 특정 시간의 값으로 설정할 수 있습니다. 예를 들면, 1개월전 로그 파일에 있는 날짜를 그 당시의 날짜로 입력하고자 할때 사용됩니다.

* aTime은 _arrival_time으로 설정될 time값입니다. 1970년 1월 1일 이후로부터의 현재까지 nano second 값을 입력해야 합니다. 또한 입력되는 값이 과거부터 현재순으로 순차적으로 정렬되어 있어야 합니다.
* aData는 입력될 데이터의 포인터를 담고 있는 배열입니다. 배열의 개수는 Open시에 지정한 테이블이 보유하고 있는 컬럼의 개수와 일치해야 합니다.

 나머지 사항은 SQLAppendDataV2()함수를 참고하여 작성하면 됩니다.

#### SQLAppendDataV3 및 SQLAppendDataByTimeV3

```cpp
SQLRETURN SQLAppendDataV3(SQLHSTMT aStmtHandle,
                          SQL_APPEND_PARAM *aData,
                          SQLINTEGER aColCount);

SQLRETURN SQLAppendDataByTimeV3(SQLHSTMT aStmtHandle,
                                SQLBIGINT aTime,
                                SQL_APPEND_PARAM *aData,
                                SQLINTEGER aColCount);
```

V3는 V2와 동일한 `SQL_APPEND_PARAM` 값을 사용하며 `aColCount`를 추가로 받습니다.
클라이언트가 전달하는 값 개수를 `SQLAppendOpen`으로 연 테이블 메타데이터에만 의존하지 않고 명시해야 할 때 사용합니다.

#### SQLAppendBatch 및 SQLAppendBatchByTime

```cpp
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

Batch append는 직사각형 row set을 한 번의 호출로 전송합니다. `aTypes`는 `SQL_APPEND_TYPE_*` 값 배열이고, `aData`는 row 순서로 배치한 `aRowCount * aColCount`개의 값입니다. JSON 컬럼에는 `SQL_APPEND_TYPE_JSON`을 사용할 수 있으며, 가변 이진/문자 payload용 BLOB/CLOB 타입 항목도 유지됩니다.

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

Append 데이터는 통신 버퍼에 기록되어, SQLAppendFlush 호출이나 버퍼가 가득 찰 때 서버로 전송됩니다. 이 함수를 사용하면 버퍼가 가득 차지 않아도 주기적으로 전송합니다. 100ms 간격으로 마지막 전송 시간을 확인하여, 지정 시간(기본 1초)이 경과하면 버퍼 내용을 서버에 전달합니다.

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

Machbase 5.5 이후 버전에서 열 형식 매개변수 바인딩을 지원합니다 (행 형식은 미지원).

SQLSetStmtAttr()에 SQL_ATTR_PARAM_BIND_TYPE / SQL_PARAM_BIND_BY_COLUMN을 설정하고, 각 컬럼의 매개변수와 지시자 변수를 배열로 준비한 뒤 SQLBindParameter()를 호출합니다.

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


## CLI/ODBC 예제


## 응용 프로그램 개발

### CLI 설치 확인

마크베이스가 설치된 디렉터리의 include 및 lib에 다음과 같은 파일이 있으면 응용 프로그램을 개발할 수 있는 환경이 완비된 것입니다.


```bash
Mach@localhost:~/machbase_home$ ls -l include lib install/
include:
total 176
-rwxrwxr-x 1 mach mach 31449 Jun 18 19:26 machbase_sqlcli.h

install/:
total 12
-rw-rw-r-- 1 mach mach 1667 Jun 18 19:26 machbase_env.mk

lib:
total 16196
-rw-rw-r-- 1 mach mach  78603 Jun 18 19:26 machbase.jar
-rw-rw-r-- 1 mach mach 964290 Jun 18 19:26 libmachbasecli.a
```

### Makefile 작성 가이드

```bash
mach@localhost:~/machbase_home$ cd sample/
mach@localhost:~/machbase_home/sample$ cd cli/
mach@localhost:~/machbase_home/sample/cli$ ls
Makefile sample1_connect.c
```
마크베이스 패키지를 설치했다면, 다음 경로에 샘플 프로그램이 설치되어 있을 것입니다.

```makefile
include $(MACHBASE_HOME)/install/machbase_env.mk
INCLUDES += $(LIBDIR_OPT)/$(MACHBASE_HOME)/include

all : sample1_connect

sample1_connect : sample1_connect.o
    $(LD_CC) $(LD_FLAGS) $(LD_OUT_OPT)$@ $< $(LIB_OPT)machbasecli$(LIB_AFT) $(LIBDIR_OPT)$(MACHBASE_HOME)/lib $(LD_LIBS)

sample1_connect.o : sample1_connect.c
    $(COMPILE.cc) $(CC_FLAGS) $(INCLUDES) $(CC_OUT_OPT)$@ $<

clean :
    rm -f sample1_connect
```

### 컴파일 및 링크

주어진 샘플에 대해 다음과 같이 수행하면 실행 파일이 만들어집니다.

```bash
mach@localhost:~/machbase_home/sample/cli$ make
gcc -c -g -W -Wall -rdynamic -O3 -finline-functions -fno-omit-frame-pointer -fno-strict-aliasing -m64 -mtune=k8 -g -W -Wall -rdynamic -O3 -finline-functions -fno-omit-frame-pointer -fno-strict-aliasing -m64 -mtune=k8 -I/home/machbase/machbase_home/include -I. -L//home/machbase/machbase_home/include -osample1_connect.o sample1_connect.c
gcc -m64 -mtune=k8 -L/home/machbase/machbase_home/lib -osample1_connect sample1_connect.o -lmachbasecli -L/home/machbase/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
mach@localhost:~/machbase_home/sample/cli$ ls -al
total 1196
drwxrwxr-x 2 mach mach 4096 Jun 18 20:15 .
drwxrwxr-x 4 mach mach 4096 Jun 18 19:26 ..
-rw-rw-r-- 1 mach mach 483 Jun 18 19:26 Makefile
-rwxrwxr-x 1 mach mach 1196943 Jun 18 20:15 sample1_connect
-rw-rw-r-- 1 mach mach 549 Jun 18 19:26 sample1_connect.c
-rw-rw-r-- 1 mach mach 8168 Jun 18 20:15 sample1_connect.o
```
위의 샘플 Makefile을 수정하여 응용 프로그램을 작성할 수 있습니다.

## 샘플 프로그램

### 접속 예제

CLI 접속 예제입니다. 파일명은 sample1_connect.c입니다.

MACHBASE_PORT_NO는 $MACHBASE_HOME/conf/machbase.conf 파일에 있는 PORT_NO 값과 같아야 합니다.

<details>
<summary>sample1_connect.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;

void connectDB()
{
    char connStr[1024];
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }
    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }
    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");
        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf("mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }
    printf("connected ... \n");
}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon))
    {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
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

</div>
</details>

컴파일 후 실행 결과입니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample1_connect
connected ...
```

### 데이터 입력 및 출력 예제

CREATE TABLE로 테이블을 생성하고, INSERT로 데이터를 입력한 뒤 SELECT로 조회하는 예제입니다. 각 타입별 설정 방법을 확인할 수 있습니다. 파일명은 sample2_insert.c입니다.

<details>
<summary>sample2_insert.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char connStr[1024];
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];
    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }
    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }
    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);
    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");
        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }
    printf("connected ... \n");
}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];
    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");
        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
    }
    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT stmt)
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];
    printf("ERROR : (%s)\n", aMsg);
    if (SQL_SUCCESS == SQLError( gEnv, gCon, stmt, NULL, &errNo,
                                 errMsg, 1024, &msgLength ))
    {
        printf(" mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT stmt;
    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", stmt);
    }
    if (SQLExecDirect(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", stmt);
    }
    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", stmt);
    }
}

void prepareExecuteSQL(const char *aSQL)
{
    SQLHSTMT stmt;
    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        outError("AllocStmt error", stmt);
    }
    if (SQLPrepare(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        printf("Prepare error[%s]\n", aSQL);
        outError("Prepare error", stmt);
    }
    if (SQLExecute(stmt) == SQL_ERROR)
    {
        outError("prepared execute error", stmt);
    }
    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        outError("FreeStmt Error", stmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE1", 1);
    executeDirectSQL("CREATE LOG TABLE CLI_SAMPLE1(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, textlog text, image binary)", 0);
}

void selectTable()
{
    SQLHSTMT stmt;
    const char *aSQL = "SELECT seq, score, total, percentage, ratio, id, srcip, dstip, reg_date, textlog, image FROM CLI_SAMPLE1";
    int i=0;
    SQLLEN Len = 0;
    short seq;
    int score;
    long total;
    float percentage;
    double ratio;
    char id [11];
    char srcip[16];
    char dstip[40];
    SQL_TIMESTAMP_STRUCT regdate;
    char log [1024];
    char image[1024];
    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR) {
        outError("AllocStmt Error", stmt);
    }
    if (SQLPrepare(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR) {
        printf("Prepare error[%s] \n", aSQL);
        outError("Prepare error", stmt);
    }
    if (SQLExecute(stmt) == SQL_ERROR) {
        outError("prepared execute error", stmt);
    }
    SQLBindCol(stmt, 1, SQL_C_SHORT, &seq, 0, &Len);
    SQLBindCol(stmt, 2, SQL_C_LONG, &score, 0, &Len);
    SQLBindCol(stmt, 3, SQL_C_BIGINT, &total, 0, &Len);
    SQLBindCol(stmt, 4, SQL_C_FLOAT, &percentage, 0, &Len);
    SQLBindCol(stmt, 5, SQL_C_DOUBLE, &ratio, 0, &Len);
    SQLBindCol(stmt, 6, SQL_C_CHAR, id, sizeof(id), &Len);
    SQLBindCol(stmt, 7, SQL_C_CHAR, srcip, sizeof(srcip), &Len);
    SQLBindCol(stmt, 8, SQL_C_CHAR, dstip, sizeof(dstip), &Len);
    SQLBindCol(stmt, 9, SQL_C_TYPE_TIMESTAMP, &regdate, 0, &Len);
    SQLBindCol(stmt, 10, SQL_C_CHAR, log, sizeof(log), &Len);
    SQLBindCol(stmt, 11, SQL_C_CHAR, image, sizeof(image), &Len);
    while (SQLFetch(stmt) == SQL_SUCCESS)
    {
        printf("===== %d ========\n", i++);
        printf("seq = %d", seq);
        printf(", score = %d", score);
        printf(", total = %ld", total);
        printf(", percentage = %.2f", percentage);
        printf(", ratio = %g", ratio);
        printf(", id = %s", id);
        printf(", srcip = %s", srcip);
        printf(", dstip = %s", dstip);
        printf(", regdate = %d-%02d-%02d %02d:%02d:%02d",
               regdate.year, regdate.month, regdate.day,
               regdate.hour, regdate.minute, regdate.second);
        printf(", log = %s", log);
        printf(", image = %s\n", image);
    }
    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        outError("FreeStmt eror", stmt);
    }
}

void directInsert()
{
    int i;
    char query[2 * 1024];
    short seq;
    int score;
    long total;
    float percentage;
    double ratio;
    char id [11];
    char srcip [16];
    char dstip [40];
    char reg_date [40];
    char log [1024];
    char image [1024];
    for(i=1; i<10; i++)
    {
        seq = i;
        score = i+i;
        total = (seq + score) * 10000;
        percentage = (float)score/total;
        ratio = (double)seq/total;
        sprintf(id, "id-%d", i);
        sprintf(srcip, "192.168.0.%d", i);
        sprintf(dstip, "2001:0DB8:0000:0000:0000:0000:1428:%04d", i);
        sprintf(reg_date, "2015-03-31 15:26:%02d", i);
        sprintf(log, "text log-%d", i);
        sprintf(image, "binary image-%d", i);
        memset(query, 0x00, sizeof(query));
        sprintf(query, "INSERT INTO CLI_SAMPLE1 VALUES(%d, %d, %ld, %f, %f, '%s', '%s', '%s',TO_DATE('%s','YYYY-MM-DD HH24:MI:SS'),'%s','%s')",
                seq, score, total, percentage, ratio, id, srcip, dstip, reg_date, log, image);
        prepareExecuteSQL(query);
        printf("%d record inserted\n", i);
    }
}

int main()
{
    connectDB();
    createTable();
    directInsert();
    selectTable();
    disconnectDB();
    return 0;
}
```
</div>
</details>


컴파일 후 실행 결과입니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample2_insert

connected ...
1 record inserted
2 record inserted
3 record inserted
4 record inserted
5 record inserted
6 record inserted
7 record inserted
8 record inserted
9 record inserted
===== 0 ========
seq = 9, score = 18, total = 270000, percentage = 0.00, ratio = 3.3e-05, id = id-9, srcip = 192.168.0.9, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0009, regdate = 2015-03-31 15:26:09, log = text log-9, image = 62696E61727920696D6167652D39
===== 1 ========
seq = 8, score = 16, total = 240000, percentage = 0.00, ratio = 3.3e-05, id = id-8, srcip = 192.168.0.8, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0008, regdate = 2015-03-31 15:26:08, log = text log-8, image = 62696E61727920696D6167652D38
===== 2 ========
seq = 7, score = 14, total = 210000, percentage = 0.00, ratio = 3.3e-05, id = id-7, srcip = 192.168.0.7, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0007, regdate = 2015-03-31 15:26:07, log = text log-7, image = 62696E61727920696D6167652D37
===== 3 ========
seq = 6, score = 12, total = 180000, percentage = 0.00, ratio = 3.3e-05, id = id-6, srcip = 192.168.0.6, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0006, regdate = 2015-03-31 15:26:06, log = text log-6, image = 62696E61727920696D6167652D36
===== 4 ========
seq = 5, score = 10, total = 150000, percentage = 0.00, ratio = 3.3e-05, id = id-5, srcip = 192.168.0.5, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0005, regdate = 2015-03-31 15:26:05, log = text log-5, image = 62696E61727920696D6167652D35
===== 5 ========
seq = 4, score = 8, total = 120000, percentage = 0.00, ratio = 3.3e-05, id = id-4, srcip = 192.168.0.4, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0004, regdate = 2015-03-31 15:26:04, log = text log-4, image = 62696E61727920696D6167652D34
===== 6 ========
seq = 3, score = 6, total = 90000, percentage = 0.00, ratio = 3.3e-05, id = id-3, srcip = 192.168.0.3, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0003, regdate = 2015-03-31 15:26:03, log = text log-3, image = 62696E61727920696D6167652D33
===== 7 ========
seq = 2, score = 4, total = 60000, percentage = 0.00, ratio = 3.3e-05, id = id-2, srcip = 192.168.0.2, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0002, regdate = 2015-03-31 15:26:02, log = text log-2, image = 62696E61727920696D6167652D32
===== 8 ========
seq = 1, score = 2, total = 30000, percentage = 0.00, ratio = 3.3e-05, id = id-1, srcip = 192.168.0.1, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0001, regdate = 2015-03-31 15:26:01, log = text log-1, image = 62696E61727920696D6167652D31
```

### Prepare Execute 예제

파라미터 바인딩으로 INSERT하는 예제입니다. 각 타입의 바인딩 시 데이터 타입을 명확히 지정하고, 문자열 타입은 길이 값을 반드시 설정해야 합니다. 파일명은 sample3_prepare.c입니다.

<details>
<summary>sample3_prepare.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <time.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char sConnStr[1024];

    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)sConnStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");

        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &sErrorNo,
                                      sErrorMsg, 1024, &sMsgLength ))
        {
            printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    printf("connected ... \n");

}

void disconnectDB()
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &sErrorNo,
                                     sErrorMsg, 1024, &sMsgLength ))
        {
            printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT aStmt)
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, aStmt, NULL, &sErrorNo,
                                 sErrorMsg, 1024, &sMsgLength ))
    {
        printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", sStmt);
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", sStmt);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", sStmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE LOG TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);
}

void selectTable()
{
    SQLHSTMT sStmt;
    const char *aSQL = "SELECT seq, score, total, percentage, ratio, id, srcip, dstip, reg_date, tlog, image FROM CLI_SAMPLE";

    int i=0;
    short sSeq;
    int sScore;
    long sTotal;
    float sPercentage;
    double sRatio;
    char sId [20];
    char sSrcIp[20];
    char sDstIp[50];
    SQL_TIMESTAMP_STRUCT sRegDate;
    char sLog [1024];
    char sImage[1024];
    SQL_LEN sLen;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR) {
        outError("AllocStmt Error", sStmt);
    }

    if (SQLPrepare(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR) {
        printf("Prepare error[%s] \n", aSQL);
        outError("Prepare error", sStmt);
    }

    if (SQLExecute(sStmt) == SQL_ERROR) {
        outError("prepared execute error", sStmt);
    }

    SQLBindCol(sStmt, 1, SQL_C_SSHORT, &sSeq, 0, &sLen);
    SQLBindCol(sStmt, 2, SQL_C_SLONG, &sScore, 0, &sLen);
    SQLBindCol(sStmt, 3, SQL_C_SBIGINT, &sTotal, 0, &sLen);
    SQLBindCol(sStmt, 4, SQL_C_FLOAT, &sPercentage, 0, &sLen);
    SQLBindCol(sStmt, 5, SQL_C_DOUBLE, &sRatio, 0, &sLen);
    SQLBindCol(sStmt, 6, SQL_C_CHAR, sId, sizeof(sId), &sLen);
    SQLBindCol(sStmt, 7, SQL_C_CHAR, sSrcIp, sizeof(sSrcIp), &sLen);
    SQLBindCol(sStmt, 8, SQL_C_CHAR, sDstIp, sizeof(sDstIp), &sLen);
    SQLBindCol(sStmt, 9, SQL_C_TYPE_TIMESTAMP, &sRegDate, 0, &sLen);
    SQLBindCol(sStmt, 10, SQL_C_CHAR, sLog, sizeof(sLog), &sLen);
    SQLBindCol(sStmt, 11, SQL_C_CHAR, sImage, sizeof(sImage), &sLen);

    while (SQLFetch(sStmt) == SQL_SUCCESS)
    {
        printf("===== %d ========\n", i++);
        printf("seq = %d", sSeq);
        printf(", score = %d", sScore);
        printf(", total = %ld", sTotal);
        printf(", percentage = %.2f", sPercentage);
        printf(", ratio = %g", sRatio);
        printf(", id = %s", sId);
        printf(", srcip = %s", sSrcIp);
        printf(", dstip = %s", sDstIp);
        printf(", regdate = %d-%02d-%02d %02d:%02d:%02d",
               sRegDate.year, sRegDate.month, sRegDate.day,
               sRegDate.hour, sRegDate.minute, sRegDate.second);
        printf(", log = %s", sLog);
        printf(", image = %s\n", sImage);
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        outError("FreeStmt eror", sStmt);
    }
}

void prepareInsert()
{
    SQLHSTMT sStmt;
    int i;
    short sSeq;
    int sScore;
    long sTotal;
    float sPercentage;
    double sRatio;
    char sId [20];
    char sSrcIp [20];
    char sDstIp [50];
    long reg_date;
    char sLog [100];
    char sImage [100];
    int sLength[5];

    const char *sSQL = "INSERT INTO CLI_SAMPLE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )";

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        outError("AllocStmt error", sStmt);
    }

    if (SQLPrepare(sStmt, (SQLCHAR *)sSQL, SQL_NTS) == SQL_ERROR)
    {
        printf("Prepare error[%s]\n", sSQL);
        outError("Prepare error", sStmt);
    }

    for(i=1; i<10; i++)
    {
        sSeq = i;
        sScore = i+i;
        sTotal = (sSeq + sScore) * 10000;
        sPercentage = (float)(sScore+2)/sScore;
        sRatio = (double)(sSeq+1)/sTotal;
        sprintf(sId, "id-%d", i);
        sprintf(sSrcIp, "192.168.0.%d", i);
        sprintf(sDstIp, "2001:0DB8:0000:0000:0000:0000:1428:%04x", i);
        reg_date = i*10000;
        sprintf(sLog, "log-%d", i);
        sprintf(sImage, "image-%d", i);

        if (SQLBindParameter(sStmt,
                             1,
                             SQL_PARAM_INPUT,
                             SQL_C_SSHORT,
                             SQL_SMALLINT,
                             0,
                             0,
                             &sSeq,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 1", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             2,
                             SQL_PARAM_INPUT,
                             SQL_C_SLONG,
                             SQL_INTEGER,
                             0,
                             0,
                             &sScore,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 2", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             3,
                             SQL_PARAM_INPUT,
                             SQL_C_SBIGINT,
                             SQL_BIGINT,
                             0,
                             0,
                             &sTotal,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 3", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             4,
                             SQL_PARAM_INPUT,
                             SQL_C_FLOAT,
                             SQL_FLOAT,
                             0,
                             0,
                             &sPercentage,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 4", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             5,
                             SQL_PARAM_INPUT,
                             SQL_C_DOUBLE,
                             SQL_DOUBLE,
                             0,
                             0,
                             &sRatio,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 5", sStmt);
        }

        sLength[0] = strlen(sId);
        if (SQLBindParameter(sStmt,
                             6,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_VARCHAR,
                             0,
                             0,
                             sId,
                             0,
                             (SQLLEN *)&sLength[0]) == SQL_ERROR)
        {
            outError("BindParameter error 6", sStmt);
        }

        sLength[1] = strlen(sSrcIp);
        if (SQLBindParameter(sStmt,
                             7,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_IPV4,
                             0,
                             0,
                             sSrcIp,
                             0,
                             (SQLLEN *)&sLength[1]) == SQL_ERROR)
        {
            outError("BindParameter error 7", sStmt);
        }

        sLength[2] = strlen(sDstIp);
        if (SQLBindParameter(sStmt,
                             8,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_IPV6,
                             0,
                             0,
                             sDstIp,
                             0,
                             (SQLLEN *)&sLength[2]) == SQL_ERROR)
        {
            outError("BindParameter error 8", sStmt);
        }

        if (SQLBindParameter(sStmt,
                             9,
                             SQL_PARAM_INPUT,
                             SQL_C_SBIGINT,
                             SQL_DATE,
                             0,
                             0,
                             &reg_date,
                             0,
                             NULL) == SQL_ERROR)
        {
            outError("BindParameter error 9", sStmt);
        }

        sLength[3] = strlen(sLog);
        if (SQLBindParameter(sStmt,
                             10,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_VARCHAR,
                             0,
                             0,
                             sLog,
                             0,
                             (SQLLEN *)&sLength[3]) == SQL_ERROR)
        {
            outError("BindParameter error 10", sStmt);
        }

        sLength[4] = strlen(sImage);
        if (SQLBindParameter(sStmt,
                             11,
                             SQL_PARAM_INPUT,
                             SQL_C_CHAR,
                             SQL_BINARY,
                             0,
                             0,
                             sImage,
                             0,
                             (SQLLEN *)&sLength[4]) == SQL_ERROR)
        {
            outError("BindParameter error 11", sStmt);
        }

        if( SQLExecute(sStmt) == SQL_ERROR) {
            outError("prepare execute error", sStmt);
        }

        printf("%d prepared record inserted\n", i);

    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP)) {
        outError("FreeStmt", sStmt);
    }
}

int main()
{
    connectDB();
    createTable();
    prepareInsert();
    selectTable();
    disconnectDB();

    return 0;
}
```

</div>
</details>

컴파일 후 실행 결과입니다.

``` bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample3_prepare

connected ...
1 prepared record inserted
2 prepared record inserted
3 prepared record inserted
4 prepared record inserted
5 prepared record inserted
6 prepared record inserted
7 prepared record inserted
8 prepared record inserted
9 prepared record inserted
===== 0 ========
seq = 9, score = 18, total = 270000, percentage = 1.11, ratio = 3.7037e-05, id = id-9, srcip = 192.168.0.9, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0009, regdate = 1970-01-01 09:00:00, log = log-9, image = 696D6167652D39
===== 1 ========
seq = 8, score = 16, total = 240000, percentage = 1.12, ratio = 3.75e-05, id = id-8, srcip = 192.168.0.8, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0008, regdate = 1970-01-01 09:00:00, log = log-8, image = 696D6167652D38
===== 2 ========
seq = 7, score = 14, total = 210000, percentage = 1.14, ratio = 3.80952e-05, id = id-7, srcip = 192.168.0.7, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0007, regdate = 1970-01-01 09:00:00, log = log-7, image = 696D6167652D37
===== 3 ========
seq = 6, score = 12, total = 180000, percentage = 1.17, ratio = 3.88889e-05, id = id-6, srcip = 192.168.0.6, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0006, regdate = 1970-01-01 09:00:00, log = log-6, image = 696D6167652D36
===== 4 ========
seq = 5, score = 10, total = 150000, percentage = 1.20, ratio = 4e-05, id = id-5, srcip = 192.168.0.5, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0005, regdate = 1970-01-01 09:00:00, log = log-5, image = 696D6167652D35
===== 5 ========
seq = 4, score = 8, total = 120000, percentage = 1.25, ratio = 4.16667e-05, id = id-4, srcip = 192.168.0.4, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0004, regdate = 1970-01-01 09:00:00, log = log-4, image = 696D6167652D34
===== 6 ========
seq = 3, score = 6, total = 90000, percentage = 1.33, ratio = 4.44444e-05, id = id-3, srcip = 192.168.0.3, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0003, regdate = 1970-01-01 09:00:00, log = log-3, image = 696D6167652D33
===== 7 ========
seq = 2, score = 4, total = 60000, percentage = 1.50, ratio = 5e-05, id = id-2, srcip = 192.168.0.2, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0002, regdate = 1970-01-01 09:00:00, log = log-2, image = 696D6167652D32
===== 8 ========
seq = 1, score = 2, total = 30000, percentage = 2.00, ratio = 6.66667e-05, id = id-1, srcip = 192.168.0.1, dstip = 2001:0DB8:0000:0000:0000:0000:1428:0001, regdate = 1970-01-01 09:00:00, log = log-1, image = 696D6167652D31
```

### 확장 함수 Append 예제

Append 프로토콜을 사용한 고속 데이터 입력 예제입니다. 다양한 타입별 Append 설정 방법을 포함합니다. 파일명은 sample4_append1.c입니다.


<details>
<summary>sample4_append1.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <arpa/inet.h>

#if __linux__
#include <sys/time.h>
#endif

#if defined(SUPPORT_STRUCT_TM)
## include <time.h>
#endif

#define MACHBASE_PORT_NO 5656
#define MAX_APPEND_COUNT 0xFFFFFFFF
#define ERROR_CHECK_COUNT 100

#define ERROR -1
#define SUCCESS 0

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB();
void disconnectDB();
void outError(const char *aMsg);
void executeDirectSQL(const char *aSQL, int aErrIgnore);
void createTable();
void appendOpen();
void appendData();
int appendClose();
time_t getTimeStamp();

int main()
{
    unsigned int sCount=0;
    time_t sStartTime, sEndTime;

    connectDB();
    createTable();

    appendOpen();
    sStartTime = getTimeStamp();
    appendData();
    sEndTime = getTimeStamp();
    appendClose();

    printf("timegap = %ld microseconds for %d records\n", sEndTime - sStartTime, sCount);
    printf("%.2f records/second\n", ((double)sCount/(double)(sEndTime - sStartTime))*1000000);

    disconnectDB();
    return SUCCESS;
}

void connectDB()
{
    char sConnStr[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        outError("SQLAllocEnv error!!");
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        outError("SQLAllocConnect error!!");
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)sConnStr, SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        outError("connection error\n");
    }

    if (SQL_ERROR == SQLAllocStmt(gCon, &gStmt) )
    {
        outError("AllocStmt error");
    }

    printf("connected ... \n");
}

void disconnectDB()
{
    if( SQL_ERROR == SQLFreeStmt(gStmt, SQL_DROP) )
    {
        outError("SQLFreeStmt error");
    }

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        outError("disconnect error");
    }
    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg)
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    printf("ERROR : (%s)\n", aMsg);
    if (SQL_SUCCESS == SQLError( gEnv, gCon, gStmt, NULL, &sErrorNo,
                                 sErrorMsg, 1024, &sMsgLength ))
    {
        printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
    }

    if( gStmt )
    {
        SQLFreeStmt(gStmt, SQL_DROP);
    }

    if( gCon )
    {
        SQLFreeConnect( gCon );
    }

    if( gEnv )
    {
        SQLFreeEnv( gEnv );
    }
    exit(ERROR);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error");
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error");
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error");
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE LOG TABLE CLI_SAMPLE(short1 short, integer1 integer, long1 long, float1 float, double1 double, datetime1 datetime, varchar1 varchar(10), ip ipv4, ip2 ipv6, text1 text, bin1 binary)", 0);
}

void appendOpen()
{
    const char *sTableName = "CLI_SAMPLE";

    if( SQLAppendOpen(gStmt, (SQLCHAR *)sTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        outError("SQLAppendOpen error");
    }

    printf("append open ok\n");
}

void appendData()
{
    SQL_APPEND_PARAM sParam[11];
    char sVarchar[10] = {0, };
    char sText[100] = {0, };
    char sBinary[100] = {0, };

    memset(sParam, 0, sizeof(sParam));

    /* NULL FOR ALL*/
    /* fixed column */
    sParam[0].mShort = SQL_APPEND_SHORT_NULL;
    sParam[1].mInteger = SQL_APPEND_INTEGER_NULL;
    sParam[2].mLong = SQL_APPEND_LONG_NULL;
    sParam[3].mFloat = SQL_APPEND_FLOAT_NULL;
    sParam[4].mDouble = SQL_APPEND_DOUBLE_NULL;
    /* datetime */
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_NULL;
    /* varchar */
    sParam[6].mVarchar.mLength = SQL_APPEND_VARCHAR_NULL;
    /* ipv4 */
    sParam[7].mIP.mLength = SQL_APPEND_IP_NULL;
    /* ipv6 */
    sParam[8].mIP.mLength = SQL_APPEND_IP_NULL;
    /* text */
    sParam[9].mText.mLength = SQL_APPEND_TEXT_NULL;
    /* binary */
    sParam[10].mBinary.mLength = SQL_APPEND_BINARY_NULL;
    SQLAppendDataV2(gStmt, sParam);

    /* FIXED COLUMN Value */
    sParam[0].mShort = 2;
    sParam[1].mInteger = 4;
    sParam[2].mLong = 6;
    sParam[3].mFloat = 8.4;
    sParam[4].mDouble = 10.9;
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : absolute value */
    sParam[5].mDateTime.mTime = MACHBASE_UINT64_LITERAL(1000000000);
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : current */
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_NOW;
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : string format*/
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_STRING;
    sParam[5].mDateTime.mDateStr = "23/May/2014:17:41:28";
    sParam[5].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
    SQLAppendDataV2(gStmt, sParam);

    /* DATETIME : struct tm format*/
    sParam[5].mDateTime.mTime = SQL_APPEND_DATETIME_STRUCT_TM;
    sParam[5].mDateTime.mTM.tm_year = 2000 - 1900;
    sParam[5].mDateTime.mTM.tm_mon = 11;
    sParam[5].mDateTime.mTM.tm_mday = 31;
    SQLAppendDataV2(gStmt, sParam);

    /* VARCHAR : string */
    strcpy(sVarchar, "MY VARCHAR");
    sParam[6].mVar.mLength = strlen(sVarchar);
    sParam[6].mVar.mData = sVarchar;
    SQLAppendDataV2(gStmt, sParam);

    /* IPv4 : ipv4 from binary bytes */
    sParam[7].mIP.mLength = SQL_APPEND_IP_IPV4;
    sParam[7].mIP.mAddr[0] = 127;
    sParam[7].mIP.mAddr[1] = 0;
    sParam[7].mIP.mAddr[2] = 0;
    sParam[7].mIP.mAddr[3] = 1;
    SQLAppendDataV2(gStmt, sParam);

    /* IPv4 : ipv4 from binary */
    sParam[7].mIP.mLength = SQL_APPEND_IP_IPV4;
    *(in_addr_t *)(sParam[7].mIP.mAddr) = inet_addr("192.168.0.1");
    SQLAppendDataV2(gStmt, sParam);

    /* IPv4 : ipv4 from string */
    sParam[7].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[7].mIP.mAddrString = "203.212.222.111";
    SQLAppendDataV2(gStmt, sParam);

    /* IPv6 : ipv6 from binary bytes */
    sParam[8].mIP.mLength = SQL_APPEND_IP_IPV6;
    sParam[8].mIP.mAddr[0] = 127;
    sParam[8].mIP.mAddr[1] = 127;
    sParam[8].mIP.mAddr[2] = 127;
    sParam[8].mIP.mAddr[3] = 127;
    sParam[8].mIP.mAddr[4] = 127;
    sParam[8].mIP.mAddr[5] = 127;
    sParam[8].mIP.mAddr[6] = 127;
    sParam[8].mIP.mAddr[7] = 127;
    sParam[8].mIP.mAddr[8] = 127;
    sParam[8].mIP.mAddr[9] = 127;
    sParam[8].mIP.mAddr[10] = 127;
    sParam[8].mIP.mAddr[11] = 127;
    sParam[8].mIP.mAddr[12] = 127;
    sParam[8].mIP.mAddr[13] = 127;
    sParam[8].mIP.mAddr[14] = 127;
    sParam[8].mIP.mAddr[15] = 127;
    SQLAppendDataV2(gStmt, sParam);
    sParam[8].mIP.mLength = SQL_APPEND_IP_NULL; /* recover */

    /* TEXT : string */
    memset(sText, 'X', sizeof(sText));
    sParam[9].mVar.mLength = 100;
    sParam[9].mVar.mData = sText;
    SQLAppendDataV2(gStmt, sParam);

    /* BINARY : datas */
    memset(sBinary, 0xFA, sizeof(sBinary));
    sParam[10].mVar.mLength = 100;
    sParam[10].mVar.mData = sBinary;
    SQLAppendDataV2(gStmt, sParam);
}

int appendClose()
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if( SQLAppendClose(gStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        outError("SQLAppendClose error");
    }

    printf("append close ok\n");
    printf("success : %ld, failure : %ld\n", sSuccessCount, sFailureCount);
    return sSuccessCount;
}

time_t getTimeStamp()
{
#if _WIN32 || _WIN64

#if defined(_MSC_VER) || defined(_MSC_EXTENSIONS)
#define DELTA_EPOCH_IN_MICROSECS 11644473600000000Ui64
#else
#define DELTA_EPOCH_IN_MICROSECS 11644473600000000ULL
#endif
    FILETIME sFT;
    unsigned __int64 sTempResult = 0;

    GetSystemTimeAsFileTime(&sFT);

    sTempResult |= sFT.dwHighDateTime;
    sTempResult <<= 32;
    sTempResult |= sFT.dwLowDateTime;

    sTempResult -= DELTA_EPOCH_IN_MICROSECS;
    sTempResult /= 10;

    return sTempResult;
#else
    struct timeval sTimeVal;
    int sRet;

    sRet = gettimeofday(&sTimeVal, NULL);

    if (sRet == 0)
    {
        return (time_t)(sTimeVal.tv_sec * 1000000 + sTimeVal.tv_usec);
    }
    else
    {
        return 0;
    }
#endif
}
```

</div>
</details>

컴파일 후 실행 결과입니다.

```bash
[mach@localhost cli]$ make sample4_append1
gcc -c -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -I/home/mach/machbase_home/include -I. -L//home/mach/machbase_home/include -osample4_append1.o sample4_append1.c
gcc -m64 -mtune=k8 -L/home/mach/machbase_home/lib -osample4_append1 sample4_append1.o -lmachbasecli -L/home/mach/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
[mach@localhost cli]$ ./sample4_append1
connected ...
append open ok
append close ok
success : 13, failure : 0
timegap = 48 microseconds for 13 records
270833.33 records/second
[mach@localhost cli]$

You can check what is inserted after MACH_SQL.

Mach> select * from CLI_SAMPLE;
SHORT1 INTEGER1 LONG1 FLOAT1 DOUBLE1
-----------------------------------------------------------------------------------------------------------
DATETIME1 VARCHAR1 IP IP2
------------------------------------------------------------------------------------------------------------------------------
TEXT1
------------------------------------------------------------------------------------
BIN1
------------------------------------------------------------------------------------
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 NULL
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXX
FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 NULL
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXX
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 7F7F:7F7F:7F7F:7F7F:7F7F:7F7F:7F7F:7F7F
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 203.212.222.111 NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 192.168.0.1 NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR 127.0.0.1 NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 MY VARCHAR NULL NULL
NULL
NULL
2 4 6 8.4 10.9
2000-12-31 00:00:00 000:000:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
2014-05-23 17:41:28 000:000:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
2015-04-09 16:44:11 134:256:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
1970-01-01 09:00:01 000:000:000 NULL NULL NULL
NULL
NULL
2 4 6 8.4 10.9
1970-01-01 09:00:00 000:000:000 NULL NULL NULL
NULL
NULL
[12] row(s) selected.
```

파일에서 대량의 로그/패킷 데이터를 읽어 고속으로 Append하는 예제입니다. 파일명은 sample4_append2.c입니다.

미리 입력할 데이터를 data.txt에 저장해 두어야 합니다.

```bash
./make_data
```

미리 주어진 make_data.c 를 수정하면 상황에 맞게 data.txt 파일을 생성할 수 있습니다.


<details>
<summary>make_data.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO 5656
#define MAX_APPEND_COUNT 0xFFFFFFFF
#define ERROR_CHECK_COUNT 100

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB();
void disconnectDB();
void outError(const char *aMsg);
void executeDirectSQL(const char *aSQL, int aErrIgnore);
void createTable();
void appendOpen();
int appendData();
void appendClose();
time_t getTimeStamp();

int main()
{
    unsigned int sCount=0;
    time_t sStartTime, sEndTime;

    connectDB();
    createTable();

    appendOpen();
    sStartTime = getTimeStamp();
    sCount = appendData();
    sEndTime = getTimeStamp();

    appendClose();

    printf("timegap = %ld microseconds for %d records\n", sEndTime - sStartTime, sCount);
    printf("%.2f records/second\n", ((double)sCount/(double)(sEndTime - sStartTime))*1000000);

    disconnectDB();

    return 0;
}

void connectDB()
{
    char sConnStr[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        outError("SQLAllocEnv error!!");
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        outError("SQLAllocConnect error!!");
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)sConnStr, SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        outError("connection error!!");
    }

    if( SQL_ERROR == SQLAllocStmt(gCon, &gStmt) )
    {
        outError("SQLAllocStmt error!!");
    }

    printf("connected ... \n");
}

void disconnectDB()
{
    if( SQL_ERROR == SQLFreeStmt(gStmt, SQL_DROP) )
    {
        outError("SQLFreeStmt error");
    }

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        outError("disconnect error");
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg)
{
    SQLINTEGER sErrorNo;
    SQLSMALLINT sMsgLength;
    SQLCHAR sErrorMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, gStmt, NULL, &sErrorNo,
                                 sErrorMsg, 1024, &sMsgLength ))
    {
        printf(" mach-%d : %s\n", sErrorNo, sErrorMsg);
    }

    if( gStmt )
    {
        SQLFreeStmt( gStmt, SQL_DROP );
    }
    if( gCon )
    {
        SQLFreeConnect( gCon );
    }
    if( gEnv )
    {
        SQLFreeEnv( gEnv );
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt;

    if (SQLAllocStmt(gCon, &sStmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error");
    }

    if (SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("sql_exec_direct error");
    }

    if (SQL_ERROR == SQLFreeStmt(sStmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error");
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE LOG TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);

    printf("table created\n");
}

void appendOpen()
{
    const char *sTableName = "CLI_SAMPLE";

    if( SQLAppendOpen(gStmt, (SQLCHAR *)sTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        outError("SQLAppendOpen error!!");
    }

    printf("append open ok\n");
}

int appendData()
{
    FILE *sFp;
    char sBuf[1024];
    int j;
    char *sToken;
    unsigned int sCount=0;
    SQL_APPEND_PARAM sParam[11];

    sFp = fopen("data.txt", "r");
    if( !sFp )
    {
        printf("file open error\n");
        exit(-1);
    }

    printf("append data start\n");

    memset(sBuf, 0, sizeof(sBuf));

    while( fgets(sBuf, 1024, sFp ) != NULL )
    {
        if( strlen(sBuf) < 1)
        {
            break;
        }

        j=0;
        sToken = strtok(sBuf,",");

        while( sToken != NULL )
        {
            memset(sParam+j, 0, sizeof(sParam));
            switch(j){
                case 0 : sParam[j].mShort = atoi(sToken); break; //short
                case 1 : sParam[j].mInteger = atoi(sToken); break; //int
                case 2 : sParam[j].mLong = atol(sToken); break; //long
                case 3 : sParam[j].mFloat = atof(sToken); break; //float
                case 4 : sParam[j].mDouble = atof(sToken); break; //double
                case 5 : //string
                case 9 : //text
                case 10 : //binary
                         sParam[j].mVar.mLength = strlen(sToken);
                         strcpy(sParam[j].mVar.mData, sToken);
                         break;
                case 6 : //ipv4
                case 7 : //ipv6
                         sParam[j].mIP.mLength = SQL_APPEND_IP_STRING;
                         strcpy(sParam[j].mIP.mAddrString, sToken);
                         break;
                case 8 : //datetime
                         sParam[j].mDateTime.mTime = SQL_APPEND_DATETIME_STRING;
                         strcpy(sParam[j].mDateTime.mDateStr, sToken);
                         sParam[j].mDateTime.mFormatStr = "DD/MON/YYYY:HH24:MI:SS";
                         break;
            }

            sToken = strtok(NULL, ",");

            j++;
        }
        if( SQLAppendDataV2(gStmt, sParam) != SQL_SUCCESS )
        {
            printf("SQLAppendData error\n");
            return 0;
        }
        if ( ((sCount++) % 10000) == 0)
        {
            printf(".");
        }

        if( ((sCount) % 100) == 0 )
        {
            if( SQLAppendFlush( gStmt ) != SQL_SUCCESS )
            {
                outError("SQLAppendFlush error");
            }
        }
        if (sCount == MAX_APPEND_COUNT)
        {
            break;
        }
    }

    printf("\nappend data end\n");

    fclose(sFp);

    return sCount;
}

void appendClose()
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if( SQLAppendClose(gStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        outError("SQLAppendClose error");
    }

    printf("append close ok\n");
    printf("success : %ld, failure : %ld\n", sSuccessCount, sFailureCount);
}

time_t getTimeStamp()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec*1000000+tv.tv_usec;
}
```

</div>
</details>

컴파일 후 실행 결과입니다.

```bash
[mach@localhost cli]$ make
gcc -c -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -I/home/mach/machbase_home/include -I. -L//home/mach/machbase_home/include -osample4_append2.o sample4_append2.c
gcc -m64 -mtune=k8 -L/home/mach/machbase_home/lib -osample4_append2 sample4_append2.o -lmachbasecli -L/home/mach/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
[mach@localhost cli]$ ./sample4_append2
connected ...
table created
append open ok
append data start
....................................................................................................
append data end
append close ok
success : 1000000, failure : 0
timegap = 1641503 microseconds for 1000000 records
609197.79 records/second
```

### 테이블 열 정보 획득 예제

테이블 열 정보를 획득하는 방법은 다양하지만 그중에 SQLDescribeCol과 SQLColumns를 이용한 방법을 살펴봅니다.

#### SQLDescribeCol

SQLDescribeCol은 테이블 열의 번호, 이름, 버퍼 크기, 길이, 타입 등을 가져오는 함수로 이를 이용해서 데이터베이스 내부에서 원하는 내용을 손쉽게 가져올수 있습니다.

예제 파일명은 sample5_describe.c 라고 합니다.


<details>
<summary>sample5_describe.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>
#include <time.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char connStr[1024];

    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");

        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    if (SQLAllocStmt(gCon, &gStmt) == SQL_ERROR)
    {
        outError("AllocStmt error", gStmt);
    }

    printf("connected ... \n");

}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT stmt)
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, stmt, NULL, &errNo,
                                 errMsg, 1024, &msgLength ))
    {
        printf(" mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT stmt;

    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", stmt);
    }

    if (SQLExecDirect(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", stmt);
    }

    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", stmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE LOG TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);

}

int main()
{
    char sSqlStr[] = "select * from cli_sample";
    SQLCHAR sColName[32];
    SQLSMALLINT sColType;
    SQLSMALLINT sColNameLen;
    SQLSMALLINT sNullable;
    SQLULEN sColLen;
    SQLSMALLINT sDecimalDigits;
    SQLLEN sOutlen;
    SQLCHAR* sData;
    SQLLEN sDisplaySize;
    int i;

    SQLSMALLINT sColumns;

    connectDB();

    createTable();

    if(SQLPrepare(gStmt, (SQLCHAR*)sSqlStr, SQL_NTS))
    {
        outError("sql prepare fail", gStmt);
        return -1;
    }

    if(SQLNumResultCols(gStmt, &sColumns) != SQL_SUCCESS )
    {
        printf("get col length error \n");
        return -1;
    }

    printf("----------------------------------------------------------------\n");
    printf("%32s%16s%10s%10s\n","Name","Type","Length","Nullable");
    printf("----------------------------------------------------------------\n");

    for(i = 0; i < sColumns; i++)
    {
        SQLDescribeCol(gStmt,
                       (SQLUSMALLINT)(i + 1),
                       sColName,
                       sizeof(sColName),
                       &sColNameLen,
                       &sColType,
                       (SQLULEN *)&sColLen,
                       &sDecimalDigits,
                       (SQLSMALLINT *)&sNullable);

        printf("%32s%16d%10d%10d\n",
               sColName, sColType, sColLen, sNullable);
    }

    printf("----------------------------------------------------------------\n");

    disconnectDB();

    return 0;
}
```

</div>
</details>

make를 실행하면 열 정보가 출력됩니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample5_describe
connected ...
----------------------------------------------------------------
Name Type Length Nullable
----------------------------------------------------------------
SEQ 5 5 1
SCORE 4 10 1
TOTAL -5 19 1
PERCENTAGE 6 27 1
RATIO 8 27 1
ID 12 10 1
SRCIP 2104 15 1
DSTIP 2106 60 1
REG_DATE 9 31 1
TLOG 2100 67108864 1
IMAGE -2 67108864 1
----------------------------------------------------------------
[mach@localhost cli]$
```

#### SQLColumns

SQLColumns는 테이블의 컬럼 정보를 조회하는 함수입니다. 파일명은 sample6_columns.c입니다.


<details>
<summary>sample6_columns.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

#include <time.h>

#define MACHBASE_PORT_NO 5656

SQLHENV gEnv;
SQLHDBC gCon;
SQLHSTMT gStmt;
SQLCHAR gErrorState[6];

void connectDB()
{
    char connStr[1024];

    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLAllocEnv(&gEnv)) {
        printf("SQLAllocEnv error!!\n");
        exit(1);
    }

    if (SQL_ERROR == SQLAllocConnect(gEnv, &gCon)) {
        printf("SQLAllocConnect error!!\n");
        SQLFreeEnv(gEnv);
        exit(1);
    }

    sprintf(connStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if (SQL_ERROR == SQLDriverConnect( gCon, NULL,
                                       (SQLCHAR *)connStr,
                                       SQL_NTS,
                                       NULL, 0, NULL,
                                       SQL_DRIVER_NOPROMPT ))
    {
        printf("connection error\n");

        if (SQL_SUCCESS == SQLError ( gEnv, gCon, NULL, NULL, &errNo,
                                      errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
        SQLFreeEnv(gEnv);
        exit(1);
    }

    if (SQLAllocStmt(gCon, &gStmt) == SQL_ERROR)
    {
        outError("AllocStmt error", gStmt);
    }

    printf("connected ... \n");

}

void disconnectDB()
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    if (SQL_ERROR == SQLDisconnect(gCon)) {
        printf("disconnect error\n");

        if( SQL_SUCCESS == SQLError( gEnv, gCon, NULL, NULL, &errNo,
                                     errMsg, 1024, &msgLength ))
        {
            printf(" mach-%d : %s\n", errNo, errMsg);
        }
    }

    SQLFreeConnect(gCon);
    SQLFreeEnv(gEnv);
}

void outError(const char *aMsg, SQLHSTMT stmt)
{
    SQLINTEGER errNo;
    SQLSMALLINT msgLength;
    SQLCHAR errMsg[1024];

    printf("ERROR : (%s)\n", aMsg);

    if (SQL_SUCCESS == SQLError( gEnv, gCon, stmt, NULL, &errNo,
                                 errMsg, 1024, &msgLength ))
    {
        printf(" mach-%d : %s\n", errNo, errMsg);
    }
    exit(-1);
}

void executeDirectSQL(const char *aSQL, int aErrIgnore)
{
    SQLHSTMT stmt;

    if (SQLAllocStmt(gCon, &stmt) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        outError("AllocStmt error", stmt);
    }

    if (SQLExecDirect(stmt, (SQLCHAR *)aSQL, SQL_NTS) == SQL_ERROR)
    {
        if (aErrIgnore != 0) return;
        printf("sql_exec_direct error[%s] \n", aSQL);
        outError("sql_exec_direct error", stmt);
    }

    if (SQL_ERROR == SQLFreeStmt(stmt, SQL_DROP))
    {
        if (aErrIgnore != 0) return;
        outError("FreeStmt Error", stmt);
    }
}

void createTable()
{
    executeDirectSQL("DROP TABLE CLI_SAMPLE", 1);
    executeDirectSQL("CREATE LOG TABLE CLI_SAMPLE(seq short, score integer, total long, percentage float, ratio double, id varchar(10), srcip ipv4, dstip ipv6, reg_date datetime, tlog text, image binary)", 0);
}

int main()
{
    SQLCHAR sColName[32];
    SQLSMALLINT sColType;
    SQLCHAR sColTypeName[16];
    SQLSMALLINT sColNameLen;
    SQLSMALLINT sColTypeLen;
    SQLSMALLINT sNullable;
    SQLULEN sColLen;
    SQLSMALLINT sDecimalDigits;
    SQLLEN sOutlen;
    SQLCHAR* sData;
    SQLLEN sDisplaySize;
    int i;

    SQLSMALLINT sColumns;

    connectDB();

    createTable();

    if(SQLColumns(gStmt, NULL, 0, NULL, 0, "cli_sample", SQL_NTS, NULL, 0) != SQL_SUCCESS)
    {
        printf("sql columns error!\n");
        return -1;
    }

    SQLBindCol(gStmt, 4, SQL_C_CHAR, sColName, sizeof(sColName), &sColNameLen);
    SQLBindCol(gStmt, 5, SQL_C_SSHORT, &sColType, 0, &sColTypeLen);
    SQLBindCol(gStmt, 6, SQL_C_CHAR, sColTypeName, sizeof(sColTypeName), NULL);
    SQLBindCol(gStmt, 7, SQL_C_SLONG, &sColLen, 0, NULL);

    printf("--------------------------------------------------------------------------------\n");
    printf("%32s%16s%16s%10s\n","Name","Type","TypeName","Length");
    printf("--------------------------------------------------------------------------------\n");

    while( SQLFetch(gStmt) != SQL_NO_DATA )
    {
        printf("%32s%16d%16s%10d\n",sColName, sColType, sColTypeName, sColLen);
    }
    printf("--------------------------------------------------------------------------------\n");

    disconnectDB();

    return 0;
}
```

</div>
</details>

make를 실행한 결과입니다.

```bash
[mach@localhost cli]$ make

[mach@localhost cli]$ ./sample6_columns
connected ...
--------------------------------------------------------------------------------
Name Type TypeName Length
--------------------------------------------------------------------------------
_ARRIVAL_TIME 93 DATE 31
SEQ 5 SMALLINT 5
SCORE 4 INTEGER 10
TOTAL -5 BIGINT 19
PERCENTAGE 6 FLOAT 27
RATIO 8 DOUBLE 27
ID 12 VARCHAR 10
SRCIP 2104 IPV4 15
DSTIP 2106 IPV6 60
REG_DATE 93 DATE 31
TLOG 2100 TEXT 67108864
IMAGE -2 BINARY 67108864
--------------------------------------------------------------------------------
```


## 멀티 쓰레드 append 예제

여러 스레드에서 여러 테이블에 동시에 Append하는 예제입니다. 파일명은 sample8_multi_session_multi_table.c입니다.


<details>
<summary>sample8_multi_session_multi_table.c</summary>
<div markdown="1">

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <machbase_sqlcli.h>

#define MACHBASE_PORT_NO       5656
#define ERROR_CHECK_COUNT   100

#define LOG_FILE_CNT        3
#define MAX_THREAD_NUM      LOG_FILE_CNT

#define RC_FAILURE          -1
#define RC_SUCCESS          0

#define UNUSED(aVar) do { (void)(aVar); } while(0)

char *gTableName[LOG_FILE_CNT] = {"table_f1", "table_f2", "table_event"};
char *gFileName[LOG_FILE_CNT] =  {"suffle_data1.txt","suffle_data2.txt","suffle_data3.txt"};

void printError(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char *aMsg);
int connectDB(SQLHENV *aEnv, SQLHDBC *aCon);
void disconnectDB(SQLHENV aEnv, SQLHDBC aCon);
int executeDirectSQL(SQLHENV aEnv, SQLHDBC aCon, const char *aSQL, int aErrIgnore);
int appendOpen(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char* aTableName);
int appendClose(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt);
int createTables(SQLHENV aEnv, SQLHDBC aCon);

/*
 * error code returned from CLI lib
 */
void printError(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char *aMsg)
{
    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    if( aMsg != NULL )
    {
        printf("%s\n", aMsg);
    }

    if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                 sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) == SQL_SUCCESS )
    {
        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);
    }
}

/*
 * error code returned from Machbase server
 */

void appendDumpError(SQLHSTMT    aStmt,
                     SQLINTEGER  aErrorCode,
                     SQLPOINTER  aErrorMessage,
                     SQLLEN      aErrorBufLen,
                     SQLPOINTER  aRowBuf,
                     SQLLEN      aRowBufLen)
{
    char       sErrMsg[1024] = {0, };
    char       sRowMsg[32 * 1024] = {0, };

    UNUSED(aStmt);

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


int connectDB(SQLHENV *aEnv, SQLHDBC *aCon)
{
    char sConnStr[1024];

    if( SQLAllocEnv(aEnv) != SQL_SUCCESS )
    {
        printf("SQLAllocEnv error\n");
        return RC_FAILURE;
    }

    if( SQLAllocConnect(*aEnv, aCon) != SQL_SUCCESS )
    {
        printf("SQLAllocConnect error\n");

        SQLFreeEnv(*aEnv);
        *aEnv = SQL_NULL_HENV;

        return RC_FAILURE;
    }

    sprintf(sConnStr,"SERVER=127.0.0.1;UID=SYS;PWD=MANAGER;CONNTYPE=1;PORT_NO=%d", MACHBASE_PORT_NO);

    if( SQLDriverConnect( *aCon, NULL,
                          (SQLCHAR *)sConnStr,
                          SQL_NTS,
                          NULL, 0, NULL,
                          SQL_DRIVER_NOPROMPT ) != SQL_SUCCESS
      )
    {

        printError(*aEnv, *aCon, NULL, "SQLDriverConnect error");

        SQLFreeConnect(*aCon);
        *aCon = SQL_NULL_HDBC;

        SQLFreeEnv(*aEnv);
        *aEnv = SQL_NULL_HENV;

        return RC_FAILURE;
    }

    return RC_SUCCESS;
}


void disconnectDB(SQLHENV aEnv, SQLHDBC aCon)
{
    if( SQLDisconnect(aCon) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, NULL, "SQLDisconnect error");
    }

    SQLFreeConnect(aCon);
    aCon = SQL_NULL_HDBC;

    SQLFreeEnv(aEnv);
    aEnv = SQL_NULL_HENV;
}


int executeDirectSQL(SQLHENV aEnv, SQLHDBC aCon, const char *aSQL, int aErrIgnore)
{
    SQLHSTMT sStmt = SQL_NULL_HSTMT;

    if( SQLAllocStmt(aCon, &sStmt) != SQL_SUCCESS )
    {
        if( aErrIgnore == 0 )
        {
            printError(aEnv, aCon, sStmt, "SQLAllocStmt Error");
            return RC_FAILURE;
        }
    }

    if( SQLExecDirect(sStmt, (SQLCHAR *)aSQL, SQL_NTS) != SQL_SUCCESS )
    {

        if( aErrIgnore == 0 )
        {
            printError(aEnv, aCon, sStmt, "SQLExecDirect Error");

            SQLFreeStmt(sStmt,SQL_DROP);
            sStmt = SQL_NULL_HSTMT;
            return RC_FAILURE;
        }
    }

    if( SQLFreeStmt(sStmt, SQL_DROP) != SQL_SUCCESS )
    {
        if (aErrIgnore == 0)
        {
            printError(aEnv, aCon, sStmt, "SQLFreeStmt Error");
            sStmt = SQL_NULL_HSTMT;
            return RC_FAILURE;
        }
    }
    sStmt = SQL_NULL_HSTMT;

    return RC_SUCCESS;
}


int appendOpen(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, char* aTableName)
{
    if( aTableName == NULL )
    {
        printf("append open wrong table name");
        return RC_FAILURE;
    }

    if( SQLAppendOpen(aStmt, (SQLCHAR *)aTableName, ERROR_CHECK_COUNT) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, aStmt, "SQLAppendOpen error");
        return RC_FAILURE;
    }
    return RC_SUCCESS;
}


int appendClose(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt)
{
    SQLBIGINT sSuccessCount = 0;
    SQLBIGINT sFailureCount = 0;

    if( SQLAppendClose(aStmt, &sSuccessCount, &sFailureCount) != SQL_SUCCESS )
    {
        printError(aEnv, aCon, aStmt, "SQLAppendClose error");
        return RC_FAILURE;
    }

    printf("append result success : %ld, failure : %ld\n", sSuccessCount, sFailureCount);

    return RC_SUCCESS;
}


int createTables(SQLHENV aEnv, SQLHDBC aCon)
{
    int      i;
    char    *sSchema[] = { "srcip1 ipv4, srcip2 ipv6, srcport short, dstip1 ipv4, dstip2 ipv6, dstport short, data1 long, data2 long",
        "srcip1 ipv4, srcip2 ipv6, srcport short, dstip1 ipv4, dstip2 ipv6, dstport short, data1 long, data2 long",
        "machine ipv4, err integer, msg varchar(30)"
    };

    char sDropQuery[256];
    char sCreateQuery[256];

    for(i = 0; i < LOG_FILE_CNT; i++)
    {
        snprintf(sDropQuery, 256, "DROP TABLE %s", gTableName[i]);
        snprintf(sCreateQuery, 256, "CREATE LOG TABLE %s ( %s )", gTableName[i], sSchema[i]);

        executeDirectSQL(aEnv, aCon, sDropQuery, 1);
        executeDirectSQL(aEnv, aCon, sCreateQuery, 0);
    }

    return RC_SUCCESS;
}


int appendF1(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE *aFp)
{
    SQL_APPEND_PARAM sParam[8];
    SQLRETURN        sRC;

    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    char             sData[4][64];

    memset(sParam, 0, sizeof(sParam));

    fscanf(aFp, "%s %s %hd %s %s %hd %lld %lld\n",
           sData[0], sData[1], &sParam[2].mShort,
           sData[2], sData[3], &sParam[5].mShort,
           &sParam[6].mLong, &sParam[7].mLong);

    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];

    sParam[1].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[1].mIP.mAddrString = sData[1];

    sParam[3].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[3].mIP.mAddrString = sData[2];

    sParam[4].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[4].mIP.mAddrString = sData[3];

    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }

        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);

        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}


int appendF2(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE* aFp)
{
    SQL_APPEND_PARAM sParam[8];
    SQLRETURN        sRC;

    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    char             sData[4][64];

    memset(sParam, 0, sizeof(sParam));

    fscanf(aFp, "%s %s %hd %s %s %hd %lld %lld\n",
           sData[0], sData[1], &sParam[2].mShort,
           sData[2], sData[3], &sParam[5].mShort,
           &sParam[6].mLong, &sParam[7].mLong);

    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];

    sParam[1].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[1].mIP.mAddrString = sData[1];

    sParam[3].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[3].mIP.mAddrString = sData[2];

    sParam[4].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[4].mIP.mAddrString = sData[3];

    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }

        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);

        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}


int appendEvent(SQLHENV aEnv, SQLHDBC aCon, SQLHSTMT aStmt, FILE* aFp)
{
    SQL_APPEND_PARAM sParam[3];
    SQLRETURN        sRC;

    SQLINTEGER      sNativeError;
    SQLCHAR         sErrorMsg[SQL_MAX_MESSAGE_LENGTH + 1];
    SQLCHAR         sSqlState[SQL_SQLSTATE_SIZE + 1];
    SQLSMALLINT     sMsgLength;

    char             sData[2][20];

    memset(sParam, 0, sizeof(sParam));

    fscanf(aFp, "%s %d %s\n",sData[0], &sParam[1].mInteger, sData[1]);

    sParam[0].mIP.mLength = SQL_APPEND_IP_STRING;
    sParam[0].mIP.mAddrString = sData[0];

    sParam[2].mVarchar.mLength = strlen(sData[1]);
    sParam[2].mVarchar.mData = sData[1];

    sRC = SQLAppendDataV2(aStmt, sParam);
    if( !SQL_SUCCEEDED(sRC) )
    {
        if( SQLError(aEnv, aCon, aStmt, sSqlState, &sNativeError,
                     sErrorMsg, SQL_MAX_MESSAGE_LENGTH, &sMsgLength) != SQL_SUCCESS )
        {
            return RC_FAILURE;
        }

        printf("SQLSTATE-[%s], Machbase-[%d][%s]\n", sSqlState, sNativeError, sErrorMsg);

        if( sNativeError != 9604 &&
            sNativeError != 9605 &&
            sNativeError != 9606 )
        {
            return RC_FAILURE;
        }
        else
        {
            //data value error in one record, so return success to keep attending
        }
    }
    return RC_SUCCESS;
}


void *eachThread(void *aIdx)
{
    SQLHENV    sEnv = SQL_NULL_HENV;
    SQLHDBC    sCon = SQL_NULL_HDBC;
    SQLHSTMT   sStmt[LOG_FILE_CNT] = {SQL_NULL_HSTMT,};

    FILE*      sFp;
    int        i;
    int        sLogType;

    int        sThrNo = *(int *)aIdx;

    // Alloc ENV and DBC
    if( connectDB(&sEnv, &sCon) == RC_SUCCESS )
    {
        printf("[%d]connectDB success.\n", sThrNo);
    }
    else
    {
        printf("[%d]connectDB failure.\n", sThrNo);
        goto error;
    }

    // set timed flush true
    if( SQLSetConnectAppendFlush(sCon, 1) != SQL_SUCCESS )
    {
        printError(sEnv, sCon, NULL, "SQLSetConnectAppendFlush Error");
        goto error;
    }

    for( i = 0; i < LOG_FILE_CNT; i++ )
    {
        // Alloc stmt
        if( SQLAllocStmt(sCon,&sStmt[i]) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAllocStmt Error");
            goto error;
        }

        if( appendOpen(sEnv, sCon, sStmt[i], gTableName[i]) == RC_FAILURE )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAppendOpen Error");
            goto error;
        }
        else
        {
            printf("[%d-%d]appendOpen success.\n", sThrNo, i);
        }

        if( SQLAppendSetErrorCallback(sStmt[i], appendDumpError) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLAppendSetErrorCallback Error");
            goto error;
        }

        // set timed flush interval as 2 seconds
        if( SQLSetStmtAppendInterval(sStmt[i], 2000) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLSetStmtAppendInterval Error");
            goto error;
        }
    }

    sFp = fopen((char*)gFileName[sThrNo], "rt");
    if( sFp == NULL )
    {
        printf("file open error - [%d][%s]\n", sThrNo, gFileName[sThrNo]);
    }
    else
    {
        printf("file open success - [%d][%s]\n", sThrNo, gFileName[sThrNo]);

        for( i = 0; !feof(sFp); i++ )
        {
            fscanf(sFp, "%d ", &sLogType);
            switch(sLogType)
            {
                case 1://f1
                    if( appendF1(sEnv, sCon, sStmt[0], sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                case 2://f2
                    if( appendF2(sEnv, sCon, sStmt[1],sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                case 3://event
                    if(appendEvent(sEnv, sCon, sStmt[2], sFp) == RC_FAILURE )
                    {
                        goto error;
                    }
                    break;
                default:
                    printf("unknown type error\n");
                    break;
            }

            if( (i%10000) == 0 )
            {
                fprintf(stdout, ".");
                fflush(stdout);
            }
        }
        printf("\n");

        fclose(sFp);
    }

    for( i = 0; i < LOG_FILE_CNT; i++)
    {
        printf("[%d-%d]appendClose start...\n", sThrNo, i);
        if( appendClose(sEnv, sCon, sStmt[i]) == RC_FAILURE )
        {
            printf("[%d-%d]appendClose failure\n", sThrNo, i);
        }
        else
        {
            printf("[%d-%d]appendClose success\n", sThrNo, i);
        }

        if( SQLFreeStmt(sStmt[i], SQL_DROP) != SQL_SUCCESS )
        {
            printError(sEnv, sCon, sStmt[i], "SQLFreeStmt Error");
        }
        sStmt[i] = SQL_NULL_HSTMT;
    }

    disconnectDB(sEnv, sCon);

    printf("[%d]disconnected.\n", sThrNo);

    pthread_exit(NULL);

error:
    for( i = 0; i < LOG_FILE_CNT; i++)
    {
        if( sStmt[i] != SQL_NULL_HSTMT )
        {
            appendClose(sEnv, sCon, sStmt[i]);

            if( SQLFreeStmt(sStmt[i], SQL_DROP) != SQL_SUCCESS )
            {
                printError(sEnv, sCon, sStmt[i], "SQLFreeStmt Error");
            }
            sStmt[i] = SQL_NULL_HSTMT;
        }
    }

    if( sCon != SQL_NULL_HDBC )
    {
        disconnectDB(sEnv, sCon);
    }

    pthread_exit(NULL);
}


int initTables()
{
    SQLHENV     sEnv  = SQL_NULL_HENV;
    SQLHDBC     sCon  = SQL_NULL_HDBC;

    if( connectDB(&sEnv, &sCon) == RC_SUCCESS )
    {
        printf("connectDB success.\n");
    }
    else
    {
        printf("connectDB failure.\n");
        goto error;
    }

    if( createTables(sEnv, sCon) == RC_SUCCESS )
    {
        printf("createTables success.\n");
    }
    else
    {
        printf("createTables failure.\n");
        goto error;
    }

    disconnectDB(sEnv, sCon);

    return RC_SUCCESS;

error:

    if( sCon != SQL_NULL_HDBC )
    {
        disconnectDB(sEnv, sCon);
    }

    return RC_FAILURE;
}


int main()
{
    pthread_t sThread[MAX_THREAD_NUM];
    int       sNum[MAX_THREAD_NUM];
    int       sRC;
    int       i;

    initTables();

    //
    //eachThread has own ENV,DBC and STMT
    //
    for(i = 0; i < MAX_THREAD_NUM; i++)
    {
        sNum[i] = i;

        sRC = pthread_create(&sThread[i], NULL, (void *)eachThread, (void*)&sNum[i]);
        if ( sRC != RC_SUCCESS )
        {
            printf("Error in Thread create[%d] : %d\n", i, sRC);
            return RC_FAILURE;
        }
    }

    for(i = 0; i < MAX_THREAD_NUM; i++)
    {
        sRC = pthread_join(sThread[i], NULL);
        if( sRC != RC_SUCCESS )
        {
            printf("Error in Thread[%d] : %d\n", i, sRC);
            return RC_FAILURE;
        }
        printf("%d thread join\n", i+1);
    }

    return RC_SUCCESS;
}
```

</div>
</details>

멀티 스레드이므로 출력 순서가 다를 수 있습니다. 실행 결과 예시입니다.

```bash
[mach@localhost cli]$ make sample8_multi_session_multi_table
gcc -c -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -g -W -Wall -rdynamic -fno-inline -m64 -mtune=k8 -I/home/mach/machbase_home/include -I. -L//home/mach/machbase_home/include -osample8_multi_session_multi_table.o sample8_multi_session_multi_table.c
gcc -m64 -mtune=k8 -L/home/mach/machbase_home/lib -osample8_multi_session_multi_table sample8_multi_session_multi_table.o -lmachbasecli  -L/home/mach/machbase_home/lib -lm -lpthread -ldl -lrt -rdynamic
[mach@localhost cli]$ ./sample8_multi_session_multi_table
connectDB success.
createTables success.
[0]connectDB success.
[1]connectDB success.
[2]connectDB success.
[1-0]appendOpen success.
[0-0]appendOpen success.
[2-0]appendOpen success.
[1-1]appendOpen success.
[2-1]appendOpen success.
[0-1]appendOpen success.
[1-2]appendOpen success.
[2-2]appendOpen success.
file open success - [1][suffle_data2.txt]
file open success - [2][suffle_data3.txt]
[0-2]appendOpen success.
file open success - [0][suffle_data1.txt]
.......................................................................................

[1-0]appendClose start...
..
[0-0]appendClose start...
append result success : 100000, failure : 0
[1-0]appendClose success
[1-1]appendClose start...
append result success : 100000, failure : 0
[1-1]appendClose success
[1-2]appendClose start...
append result success : 100000, failure : 0
[1-2]appendClose success
append result success : 100000, failure : 0
[0-0]appendClose success
[0-1]appendClose start...
.append result success : 100000, failure : 0
[0-1]appendClose success
[0-2]appendClose start...
append result success : 100000, failure : 0
[0-2]appendClose success

[2-0]appendClose start...
append result success : 100000, failure : 0
[2-0]appendClose success
[2-1]appendClose start...
append result success : 100000, failure : 0
[2-1]appendClose success
[2-2]appendClose start...
append result success : 100000, failure : 0
[2-2]appendClose success
[1]disconnected.
[2]disconnected.
[0]disconnected.
1 thread join
2 thread join
3 thread join
```

machsql을 통해 아래와 같이 결과를 확인할 수 있습니다.

```bash
[mach@localhost cli]$ machsql


=================================================================
     Machbase Client Query Utility
     Release Version 8.5.4.develop
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase Server Addr (Default:127.0.0.1) :
Machbase User ID  (Default:SYS)
Machbase User Password : manager
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
Mach> select count(*) from table_f1;
count(*)
-----------------------
300000
[1] Row Selected.
Mach> select count(*) from table_f2;
count(*)
-----------------------
300000
[1] row(s) selected.
Mach> select count(*) from table_event;
count(*)
-----------------------
300000
[1] row(s) selected.
```
