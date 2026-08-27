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

SDK를 처음 고를 때는 [연동 방식 선택](../selection-integration-method/)을 먼저 읽고, 이
페이지에서는 필요한 capability와 정확한 API 경로를 대조합니다.

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
| Node.js | 실행 결과 `rowId` | `undefined` |

batch, `executemany()`, Append, loader, `INSERT ... SELECT`와 UPSERT에서는 단일 ROWID를
반환하지 않습니다. SQL 의미와 테이블별 제약은 [ROWID](/dbms/reference/sql/rowid/)를
참고하십시오.

<a id="support-scope-sdk-append"></a>
<a id="append-table-type-matrix"></a>

## Append API와 table type

| API path | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION | 기준 |
|---|:---:|:---:|:---:|:---:|:---:|---|
| SQLCLI `SQLAppend*` extension | O | O | O | O | O | TRANSACTION은 Standard |
| JDBC `MachStatement.executeAppend*` | O | O | O | O | O | NFX cce422d source/test |
| Python 2.4 `append*` | O | O | O | O | O | NFX cce422d source/test |
| .NET `MachAppendWriter` | O | O | O | O | O | NFX cce422d provider |
| Go v1.8.4 native `Appender` | O | O | X | X | O | TRANSACTION은 Standard |
| Go `database/sql` 표준 API | X | X | X | X | X | `sql.Conn.Raw()` 확장은 native 계약 |
| Node source `appendBatch()` | O | △ | △ | △ | O | NFX cce422d source build |
| Node source `appendOpen()` | O | O | △ | △ | △ | generic native/fallback, table별 검증 필요 |

표준 query connection과 Append handle의 lifecycle을 구분하고 close·flush 결과를
확인합니다. `O`는 해당 source/test에서 확인된 범위이고 `△`는 generic path만 있어 table별
회귀 검증이 더 필요한 범위입니다. Append extension은 표준 ODBC나 `database/sql` 기능이
아닙니다.

<a id="support-scope-sdk-auth-key"></a>

## AUTH KEY

| SDK·도구 | 지원 |
|---|:---:|
| machsql, Machbase SQLCLI, ODBC, JDBC | O |
| Go native, Go `database/sql` | O (neo-client v1.5.0+) |
| Python, Node.js, .NET | X |

키 생성·등록·교체는 [AUTH KEY 인증](/dbms/security-access-control/authentication-auth-key/)을,
연결 option은 지원 SDK 페이지를 정본으로 사용합니다.

<a id="support-scope-sdk-transaction-prepare-bind"></a>

## Transaction, prepare와 bind

| SDK | Transaction API | Server prepared | Named bind API |
|---|:---:|:---:|:---:|
| JDBC | O | O | △ (Machbase extension) |
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

Machbase 8.7.0 Standard Edition의 TAG data UPDATE는 각 SDK의 기존 positional/named API로
NAME과 BASETIME 조건 값을 바인딩할 수 있습니다. NFX #4127 회귀 테스트는 C/C++ SQLCLI,
Go `database/sql`, JDBC, Node.js, Python과 .NET 경로를 검증합니다. ODBC는 별도 SDK 회귀
매트릭스에 포함되지 않으며 `?` 또는 named SQL의 marker를 표준 `SQLBindParameter()` ordinal로
바인딩합니다. TAG UPDATE 조건 계약은
[TAG data UPDATE bind](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)를
정본으로 사용합니다.

Transaction 열의 `△`는 전용 객체 대신 같은 connection에서 transaction SQL을 직접 실행하는
경로입니다. Named bind 열의 `△`는 standard capability가 아닌 vendor/client rendering
extension입니다.

## 최소 확인 version과 provenance

| SDK | 이 문서의 확인 기준 |
|---|---|
| SQLCLI·JDBC·Python | NFX `cce422d2972`; Python package 2.4 |
| Node.js | NFX `cce422d2972` source build (`package.json` 1.0.1) |
| .NET | Uni 8.0.55, limited 3.1.3, full 3.2.2 |
| Go | released neo-client v1.8.4; AUTH KEY는 v1.5.0+, database 선택은 v1.8.3+ |

NFX cce422d의 Node 기능 일부는 public npm 1.0.1 publish 이후 추가되었습니다. registry package의
version 문자열만으로 동일 기능을 가정하지 말고 배포 artifact의 commit provenance를
확인하거나 NFX source build를 사용합니다.

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
