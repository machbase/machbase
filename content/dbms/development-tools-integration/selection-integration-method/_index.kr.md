---
type: docs
title: '11.1 연동 방식 선택'
weight: 10
toc: true
aliases:
  - /dbms/application-integration/selection-integration-method/
  - /dbms/application-integration/guide-drivers/
  - /dbms/scenario-guides/examples/
  - /dbms/reference/ai-agent-reference/sdk-api-selection-rules/
---

프로젝트의 언어, 입력 특성, 배포 환경에 맞는 연동 방식을 선택합니다.

<a id="selection-guide-integration-method"></a>

## 선택 기준

| 요구사항 | 우선 검토할 방식 |
|----------|------------------|
| C/C++ native 수집기 | SQLCLI |
| ODBC 관리자·DSN 기반 애플리케이션 | ODBC |
| Java·Spring | JDBC |
| Python 분석·자동화 | `machbaseapi` |
| C#·VB.NET | .NET Connector |
| Go 수집기·서비스 | native `machgo` 또는 `database/sql` |
| Node.js·TypeScript 백엔드 | `@machbase/ts-client` |
| R 분석 환경 | Machbase ODBC 드라이버와 RODBC |
| 큰 파일의 일괄 입력·반출 | machloader, csvimport, csvexport |
| 지속적인 TAG·LOG 대량 입력 | 선택한 SDK의 Append API |

브라우저에서 5656 포트로 직접 연결하지 않습니다. backend에서 query를 실행하고 필요한
결과만 전달합니다.

## 결정 순서

1. 애플리케이션 언어에서 유지보수 가능한 공식 드라이버를 고릅니다.
2. 5656 포트 연결, 운영체제와 runtime 호환성을 확인합니다.
3. SQL, prepared statement, Append, transaction 중 필요한 기능을 정합니다.
4. [SDK 기능 지원표](../sdk-support-scope/)에서 실제 지원 여부를
   확인합니다.
5. 표본 데이터로 timestamp, NULL, 숫자, 문자열을 왕복 검증합니다.
6. 목표 row 크기·동시 연결·batch 크기로 부하 테스트합니다.

Append 지원만으로 드라이버를 결정하지 않습니다. flush 지연, 오류 ack, 재연결, 실패 row
처리까지 실제 SDK에서 확인합니다. TRANSACTION DML에는 명시적 transaction 지원 범위를
확인하고, TAG·LOG Append를 같은 rollback 단위로 가정하지 않습니다.

<a id="distinction-sdk-api-canonical-owner"></a>

## 정본 구분

| 내용 | 정본 |
|------|------|
| SDK 설치·연결·API·완전한 코드 | 이 장의 SDK별 페이지 |
| 공통 인증·binding·transaction·retry | [공통 연동 개념](../concepts-common/) |
| SDK별 기능 지원 여부 | [SDK 기능 지원 범위](../sdk-support-scope/) |
| SQL·설정·명령줄 상세 | [17장 레퍼런스](/dbms/reference/) |
| 입력·반출 방식 선택 | [데이터 입력과 반출](../data-input-load-export/) |
| 외부 도구 연결 검증 | [외부 도구 연동](../external-tools/) |

SDK 함수 목록과 설치 절차는 선택 가이드에 복제하지 않습니다. 지원 여부가 바뀌는 기능은
해당 SDK 페이지와 배포 artifact를 함께 확인합니다.
