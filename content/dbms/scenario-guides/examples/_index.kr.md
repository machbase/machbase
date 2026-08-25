---
type: docs
title: '15.8 SDK 선택'
weight: 80
toc: true
---

언어별 연결, 바인드, Append API의 정본은 11장에서 관리합니다. 이 페이지는 같은 코드를
복제하지 않고 시나리오에 맞는 시작점을 안내합니다.

| 환경 | 권장 시작점 | 주요 용도 |
|---|---|---|
| Python | [Python 연동](/dbms/development-tools-integration/python/) | 자동화, 분석, 배치 적재 |
| Java | [JDBC](/dbms/development-tools-integration/jdbc/) | JVM 애플리케이션, JDBC 도구 |
| Go | [Go 연동](/dbms/development-tools-integration/go/) | 서비스, 동시 처리 |
| Node.js / TypeScript | [Node.js / TypeScript](/dbms/development-tools-integration/node-js-typescript/) | 웹 백엔드, 대시보드 API |
| .NET | [.NET Connector](/dbms/development-tools-integration/net-connector/) | .NET 서비스와 도구 |
| C/C++ | [SQLCLI / ODBC](/dbms/development-tools-integration/cli-odbc/) | 네이티브 애플리케이션 |

구현 전에 다음을 결정합니다.

1. 일반 SQL DML과 Append 중 어떤 입력 경로가 필요한가
2. database, 사용자, 비밀번호 또는 개인키를 어떻게 주입할 것인가
3. 시간대를 연결 속성에서 고정할 것인가
4. 재시도 가능한 오류와 재시도해서는 안 되는 오류를 어떻게 구분할 것인가
5. 적재 뒤 어느 쿼리로 행 수와 시간 범위를 검증할 것인가

포트, 비밀번호, SDK 버전을 소스 코드에 고정하지 마십시오. 각 언어 페이지의 현재 설치 방법과
검증된 quickstart를 기준으로 작은 연결 테스트부터 실행합니다.
