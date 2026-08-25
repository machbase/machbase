---
type: docs
title: '12.3 드라이버별 가이드'
weight: 30
toc: true
---

이 페이지는 애플리케이션 요구사항에 맞는 드라이버를 고르는 진입점입니다. 설치, API,
지원 범위와 전체 코드는 [11장 개발 도구 연동](/dbms/development-tools-integration/)을
정본으로 사용하십시오.

## 드라이버 선택

| 환경 | 권장 드라이버 | 상세 레퍼런스 |
|------|---------------|---------------|
| C/C++ 네이티브 | Machbase SQLCLI | [SQLCLI/ODBC](/dbms/development-tools-integration/cli-odbc/) |
| ODBC·DSN 기반 도구 | ODBC | [SQLCLI/ODBC](/dbms/development-tools-integration/cli-odbc/) |
| Java·Spring | JDBC | [JDBC](/dbms/development-tools-integration/jdbc/) |
| Python 분석·자동화 | `machbaseapi` | [Python](/dbms/development-tools-integration/python/) |
| JavaScript·TypeScript | `@machbase/ts-client` | [Node.js/TypeScript](/dbms/development-tools-integration/node-js-typescript/) |
| C#·VB.NET | .NET Connector | [.NET Connector](/dbms/development-tools-integration/net-connector/) |
| Go native·`database/sql` | Go | [Go](/dbms/development-tools-integration/go/) |
| R 분석 환경 | RODBC | [SQLCLI/ODBC](/dbms/development-tools-integration/cli-odbc/) |

지속적인 TAG/LOG 대량 입력에는 Append API를 지원하는 드라이버를 우선 검토합니다.
TRANSACTION 테이블의 원자적 변경이 필요하면 드라이버별 트랜잭션 지원 범위를 확인하십시오.

## 공통 준비

드라이버를 선택한 뒤 다음 순서로 확인합니다.

1. [연결 문자열과 인증](/dbms/application-integration/concepts-common/#connection-string-authentication)
2. [Prepared statement와 parameter binding](/dbms/application-integration/concepts-common/#prepared-statement)
3. [Append API와 Batch INSERT](/dbms/application-integration/concepts-common/#append-api-batch)
4. [오류 처리와 재시도](/dbms/application-integration/concepts-common/#error-handling-retry)
5. [SDK별 기능 지원표](/dbms/development-tools-integration/#sdk)

<a id="cli-odbc"></a>
<a id="machbase-sqlcli"></a>
<a id="examples-cli-odbc"></a>
<a id="cli-odbc-cli-odbc"></a>
<a id="cli-odbc-examples-cli-odbc"></a>

## Machbase SQLCLI

C/C++에서 Machbase native API와 Append를 직접 사용할 때 선택합니다. 헤더, 링크 옵션,
연결, statement, bind, Append 예제는
[Machbase SQLCLI 레퍼런스](/dbms/development-tools-integration/cli-odbc/#machbase-sqlcli)를
참고하십시오.

<a id="odbc"></a>

## ODBC

ODBC 관리자와 DSN을 사용하는 C/C++ 또는 외부 도구에 적합합니다. 설치, DSN, 표준 API와
Append 범위는 [ODBC 레퍼런스](/dbms/development-tools-integration/cli-odbc/#odbc)를
참고하십시오.

<a id="jdbc"></a>

## JDBC

Java와 Spring 환경에서는 JDBC를 사용합니다. 설치, 연결, PreparedStatement, 트랜잭션,
Append와 pool 설정은 [JDBC 레퍼런스](/dbms/development-tools-integration/jdbc/)를
참고하십시오.

<a id="python"></a>

## Python

분석 스크립트와 수집 자동화에는 `machbaseapi`를 사용합니다. DB-API 사용법, bind,
Append와 메타데이터는 [Python 레퍼런스](/dbms/development-tools-integration/python/)를
참고하십시오.

<a id="node-js-typescript"></a>

## Node.js / TypeScript

웹 서비스와 IoT 게이트웨이에는 `@machbase/ts-client`를 사용합니다. Promise API,
prepared statement, Append와 타입 메타데이터는
[Node.js/TypeScript 레퍼런스](/dbms/development-tools-integration/node-js-typescript/)를
참고하십시오.

<a id="net-connector"></a>

## .NET Connector

C#과 VB.NET 환경에서는 ADO.NET 호환 Connector를 사용합니다. connection string,
command, reader, Append와 `GetSchemaTable()`은
[.NET Connector 레퍼런스](/dbms/development-tools-integration/net-connector/)를
참고하십시오.

<a id="go"></a>
<a id="go-go"></a>
<a id="go-sql"></a>
<a id="go-go-sql"></a>

## Go

고성능 수집에는 native `machgo`, 표준 SQL 호환이 필요하면 `database/sql` 드라이버를
선택합니다. 설치, 연결, Appender와 두 인터페이스의 차이는
[Go 레퍼런스](/dbms/development-tools-integration/go/)를 참고하십시오.

<a id="r-rodbc"></a>

## R / RODBC

R에서는 시스템 ODBC 드라이버와 DSN을 구성한 뒤 RODBC 같은 호환 패키지에서 연결합니다.
드라이버 등록과 접속 속성은
[ODBC 레퍼런스](/dbms/development-tools-integration/cli-odbc/#odbc)를 기준으로 확인하십시오.
