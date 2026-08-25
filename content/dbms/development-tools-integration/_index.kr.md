---
type: docs
title: '11. 개발 및 애플리케이션 연동'
weight: 110
toc: true
aliases:
  - /dbms/reference/sdk-api/
  - /dbms/application-integration/
---

애플리케이션 요구사항에 맞는 연동 방식을 선택하고, SDK별 설치·API와 공통 운영 원칙을
확인합니다. 언어별 구현은 SDK 페이지를, 여러 SDK에 공통인 판단 기준은 선택·개념·지원 범위
페이지를 정본으로 사용합니다.

## 읽는 순서

1. [연동 방식 선택](selection-integration-method/)에서 언어와 입력 방식에 맞는 인터페이스를
   고릅니다.
2. [공통 연동 개념](concepts-common/)에서 인증, 시간값, binding, transaction과 retry를
   확인합니다.
3. [SDK 기능 지원 범위](sdk-support-scope/)에서 필요한 기능의 실제 지원 여부를 비교합니다.
4. 해당 언어의 SDK 페이지에서 설치, 연결과 실행 코드를 확인합니다.
5. [데이터 입력과 반출](data-input-load-export/), [ROWID와 INSERT 결과 ID](rowid-generated-id/),
   [외부 도구 연동](external-tools/)에서 작업별 절차를 적용합니다.

## SDK별 레퍼런스

| 환경 | 문서 |
|---|---|
| C/C++ native 또는 ODBC | [Machbase SQLCLI와 ODBC](cli-odbc/) |
| Java·Spring | [JDBC](jdbc/) |
| Python | [Python](python/) |
| Node.js·TypeScript | [Node.js / TypeScript](node-js-typescript/) |
| C#·VB.NET | [.NET Connector](net-connector/) |
| Go native·`database/sql` | [Go](go/) |

## 공통 연결 정보

| 항목 | 기본값 | 설명 |
|---|---|---|
| HOST | `127.0.0.1` | Machbase 서버 호스트명 또는 IP |
| PORT | `5656` | Machbase 서버 포트 (`machbase.conf`의 `PORT_NO`) |
| USER | `SYS` | 사용자 ID |
| PASSWORD | `MANAGER` | 사용자 비밀번호 |

운영 환경에서는 별도 사용자와 필요한 최소 권한을 사용합니다. 계정과 인증 설정은
[계정, 권한, 접속 제어](../security-access-control/)를 참고하십시오.

## 기존 지원 범위 링크

다음 anchor는 기존 북마크와 외부 링크의 호환성을 위해 유지합니다. 최신 내용은
[SDK 기능 지원 범위](sdk-support-scope/)에서 확인하십시오.

<a id="support-scope-sdk-nullable-metadata"></a>
<a id="support-scope-sdk-primary-key-metadata"></a>
<a id="support-scope-sdk-generated-rowid"></a>
<a id="support-scope-sdk-append"></a>
<a id="support-scope-sdk-auth-key"></a>
<a id="support-scope-sdk-transaction-prepare-bind"></a>
<a id="sdk"></a>
