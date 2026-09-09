---
type: docs
title: '16.8.9 sdk-api-selection-rules'
weight: 90
toc: true
---

SDK 이름만으로 기능을 가정하지 않고 요구사항과 실제 지원 범위를 함께 확인합니다.

## 선택 순서

1. 언어와 표준 인터페이스 요구사항을 [연동 방식 선택](/dbms/development-tools-integration/selection-integration-method/)에서 확인합니다.
2. Append, transaction, prepared statement, named bind, metadata와 AUTH KEY 요구사항을 정리합니다.
3. [SDK 지원 범위](/dbms/development-tools-integration/sdk-support-scope/)에서 지원 여부와 provenance를 확인합니다.
4. 선택한 SDK 페이지에서 설치, 연결 option, 타입 mapping과 오류 처리를 확인합니다.

| 환경 | 정본 |
|------|------|
| C/C++ SQLCLI·ODBC | [SQLCLI와 ODBC](/dbms/development-tools-integration/cli-odbc/) |
| Java | [JDBC](/dbms/development-tools-integration/jdbc/) |
| Python | [Python](/dbms/development-tools-integration/python/) |
| Node.js·TypeScript | [Node.js / TypeScript](/dbms/development-tools-integration/node-js-typescript/) |
| .NET | [.NET Connector](/dbms/development-tools-integration/net-connector/) |
| Go | [Go](/dbms/development-tools-integration/go/) |

서버와 SDK version 조합은 [호환성](/dbms/reference/support-scope-constraints/compatibility-xma-protocol/)을
함께 확인합니다.
