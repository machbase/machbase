---
type: docs
title: '11.3 SDK 기능 지원 범위'
weight: 30
toc: true
aliases:
  - /dbms/development-tools-integration/support-scope-sdk/
  - /dbms/application-integration/support-scope-sdk/
  - /dbms/reference/support-scope-constraints/sdk/
---

애플리케이션 요구사항에 맞는 SDK를 선택할 수 있도록 기능별 지원 여부와 API 진입점을
비교합니다. 설치, 연결, 함수와 실행 코드는 각 SDK 페이지를 정본으로 사용합니다.

## SDK 선택

| 요구사항 | 먼저 확인할 SDK |
|---|---|
| 지속적인 TAG·LOG 대량 입력 | Append를 지원하는 SDK |
| 표준 SQL 인터페이스 | JDBC, Python DB-API, Go `database/sql`, ODBC |
| TRANSACTION table transaction | JDBC, Go `database/sql`, SQLCLI·ODBC 지원 경로 |
| AUTH KEY | JDBC, Machbase SQLCLI, ODBC |
| 결과 컬럼 메타데이터 | 해당 metadata API를 제공하는 SDK |

Append 지원만으로 SDK를 결정하지 않습니다. ack, flush, 오류 row, 재연결과 중복 처리까지
해당 언어 페이지에서 확인하십시오.

<a id="support-scope-sdk-nullable-metadata"></a>

## Nullable 메타데이터

Machbase는 SELECT 결과 컬럼의 NULL 가능성을 `NO_NULLS`, `NULLABLE`, `UNKNOWN`으로
구분합니다. 애플리케이션은 `NULLABLE`과 `UNKNOWN`을 모두 NULL 처리 대상으로 가정합니다.

| SDK | 조회 방법 |
|---|---|
| JDBC | `ResultSetMetaData.isNullable()` |
| Python | `cursor.description[i][6]` |
| Go native | `api.Column.Nullability` |
| Go `database/sql` | `Rows.ColumnTypeNullable()` |
| Node.js | `ColumnMeta.nullable` |
| .NET | `GetSchemaTable()`의 `AllowDBNull` |
| SQLCLI·ODBC | descriptor의 nullable 속성 |

표현식, 집계, VIEW와 JOIN 결과는 `UNKNOWN`이 될 수 있습니다. 직접 컬럼의 스키마 제약과
조회 결과 metadata를 같은 것으로 가정하지 마십시오.

<a id="support-scope-sdk-primary-key-metadata"></a>

## PRIMARY KEY 메타데이터

| SDK | 결과 컬럼 | table catalog |
|---|:---:|:---:|
| JDBC | O | `DatabaseMetaData.getPrimaryKeys()` |
| Python | O | catalog SQL |
| Go native | O | catalog SQL |
| Go `database/sql` | 표준 API 없음 | catalog SQL |
| Node.js | O | catalog SQL |
| .NET | O | catalog SQL |
| ODBC | 별도 결과 API 없음 | `SQLPrimaryKeys()` |

표현식·집계·외부 JOIN의 NULL 공급 측은 원본 컬럼의 PK 속성을 그대로 전달하지 않을 수
있습니다.

<a id="support-scope-sdk-generated-rowid"></a>

## INSERT 결과 ROWID

Machbase 8.7.0 Standard Edition에서 성공한 단일 `INSERT ... VALUES`는 지원 SDK에 ROWID를
제공할 수 있습니다.

| SDK·도구 | 확인 방법 | 값이 없을 때 |
|---|---|---|
| machsql | `SHOW LAST ROWID` | `NULL` |
| Machbase SQLCLI | `SQLGetGeneratedRowID()` | `SQL_NO_DATA` |
| 표준 ODBC | 전용 표준 API 없음 | - |
| JDBC | `Statement.getGeneratedKeys()` | 빈 `ResultSet` |
| Python | `cursor.lastrowid` | `None` |
| .NET | `MachCommand.RowId` | `null` |
| Go `database/sql` | `Result.LastInsertId()` | 오류 |
| Go native | 미지원 | - |
| Node.js | 실행 결과 `rowId` | 속성 없음 |

batch, `executemany()`, Append, loader, `INSERT ... SELECT`와 UPSERT에서는 단일 ROWID를
반환하지 않습니다. SQL 의미와 테이블별 제약은 [ROWID](/dbms/reference/sql/rowid/)를
참고하십시오.

<a id="support-scope-sdk-append"></a>

## Append API

| SDK | 지원 | API 진입점 |
|---|:---:|---|
| Machbase SQLCLI·ODBC | O | `SQLAppendOpen` 계열 |
| JDBC | O | `MachStatement` Append 계열 |
| Python | O | connection `append()` |
| .NET | O | `MachAppendWriter` |
| Go native | O | `Appender` |
| Go `database/sql` | △ | `sql.Conn.Raw()`의 client 확장 |
| Node.js | O | `appendBatch`·`appendOpen` |

표준 query connection과 Append handle의 lifecycle을 구분하고 close·flush 결과를
확인합니다. 테이블 타입별 입력 의미는 해당 테이블의 데이터 입력 페이지를 참고하십시오.

<a id="support-scope-sdk-auth-key"></a>

## AUTH KEY

| SDK·도구 | 지원 |
|---|:---:|
| machsql, Machbase SQLCLI, ODBC, JDBC | O |
| Python, Go, Node.js, .NET | X |

키 생성·등록·교체는 [AUTH KEY 인증](/dbms/security-access-control/authentication-auth-key/)을,
연결 option은 지원 SDK 페이지를 정본으로 사용합니다.

<a id="support-scope-sdk-transaction-prepare-bind"></a>

## Transaction, prepare와 bind

| SDK | Transaction API | Server prepared | Named bind API |
|---|:---:|:---:|:---:|
| JDBC | O | O | O |
| Python | X | O | O |
| Go native | △ | O | O |
| Go `database/sql` | O | O | O |
| .NET | X | X | △ |
| Node.js | X | O | O |
| SQLCLI | △ | O | O |
| ODBC | △ | O | ordinal bind |

Prepared statement와 parameter binding은 transaction 지원과 별개입니다. marker 문법은
[Named Bind Parameter](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
참고하십시오.

`△`는 전용 transaction 객체 대신 같은 connection에서 `BEGIN`, `COMMIT`, `ROLLBACK` SQL을
실행하는 경로를 의미합니다. TRANSACTION 테이블과 Standard Edition에서 검증하십시오.

<a id="sdk"></a>

## SDK 레퍼런스

| SDK | 정본 |
|---|---|
| Machbase SQLCLI·ODBC | [SQLCLI와 ODBC](../cli-odbc/) |
| JDBC | [JDBC](../jdbc/) |
| Python | [Python](../python/) |
| Node.js / TypeScript | [Node.js / TypeScript](../node-js-typescript/) |
| .NET Connector | [.NET Connector](../net-connector/) |
| Go | [Go](../go/) |
