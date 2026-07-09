---
type: docs
title: '17.10.12 llms.txt'
weight: 120
---

`llms.txt`는 LLM이 이 문서 사이트의 구조를 빠르게 파악하기 위한 간략한 목차 파일입니다. [llms.txt 표준](https://llmstxt.org/)을 따릅니다.

## 목적

- LLM이 Machbase 문서의 전체 구조를 한 번에 파악
- 각 섹션의 목적과 주요 URL을 제공
- RAG 시스템이 인덱싱할 문서 목록을 제공

## 주요 URL 맵

Machbase 공식 문서 기준 (`/dbms/` 경로 아래):

### 시작하기

| 섹션 | URL |
|------|-----|
| 빠른 시작 | `/dbms/getting-started/` |
| 설치/준비 | `/dbms/getting-started/quick-start/` |
| 개요 | `/dbms/getting-started/overview/` |

### 핵심 개념

| 섹션 | URL |
|------|-----|
| 데이터 모델 개요 | `/dbms/core-concepts/` |
| TAG 테이블 | `/dbms/tag-table-usage/` |
| LOG 테이블 | `/dbms/log-table-usage/` |
| LOOKUP 테이블 | `/dbms/lookup-table-usage/` |
| RDB 테이블 | `/dbms/rdb-table-usage/` |
| ROLLUP | `/dbms/core-concepts/features-concepts/role-statistics-rollup/` |

### 애플리케이션 연동

| 섹션 | URL |
|------|-----|
| Append API 개념 | `/dbms/application-integration/concepts-common/append-api-batch/` |
| SDK 지원 범위 | `/dbms/application-integration/support-scope-sdk/` |
| JDBC | `/dbms/application-integration/guide-drivers/jdbc/` |
| Python | `/dbms/application-integration/guide-drivers/python/` |
| Go | `/dbms/application-integration/guide-drivers/go/` |
| .NET | `/dbms/application-integration/guide-drivers/net-connector/` |
| Node.js | `/dbms/application-integration/guide-drivers/node-js-typescript/` |
| ODBC/CLI | `/dbms/application-integration/guide-drivers/cli-odbc/` |

### 보안

| 섹션 | URL |
|------|-----|
| 인증 및 AUTH KEY | `/dbms/security-access-control/authentication-auth-key/` |
| 권한 관리 | `/dbms/security-access-control/privileges/` |

### 운영 및 복구

| 섹션 | URL |
|------|-----|
| 백업/복구/마운트 | `/dbms/operations-configuration-recovery/backup-restore-mount/` |

### 레퍼런스

| 섹션 | URL |
|------|-----|
| SQL 레퍼런스 | `/dbms/reference/sql/` |
| 설정 레퍼런스 | `/dbms/reference/configuration/` |
| 에러 코드 | `/dbms/reference/error-dictionary-codes/` |
| 지원 범위와 제약 | `/dbms/reference/support-scope-constraints/` |
| AI Agent Reference | `/dbms/reference/ai-agent-reference/` |

## 문서 업데이트 정책

- 이 문서는 Machbase 8.6 버전 기준입니다.
- 각 섹션의 정규 URL은 [canonical-url-map](../canonical-url-map/)을 참고하세요.
- 버전별 변경 사항은 릴리스 노트를 확인하세요.
- llms-full.txt (RAG용 전체 청크 인덱스)는 [llms-full.txt / chunk index](../llms-full-txt-chunk-index/)를 참고하세요.
