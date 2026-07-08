---
type: docs
title: 'canonical-url-map'
weight: 20
---

이 페이지는 Machbase의 주요 기능과 개념별 정규 URL 맵입니다. AI 에이전트가 문서 링크를 생성하거나 RAG 시스템이 문서를 참조할 때 사용합니다.

## 핵심 개념

| 개념 | 정규 URL |
|------|----------|
| 데이터 모델 개요 | `/dbms/core-concepts/` |
| TAG 테이블 | `/dbms/core-concepts/tag-table/` |
| LOG 테이블 | `/dbms/core-concepts/log-table/` |
| LOOKUP 테이블 | `/dbms/core-concepts/lookup-table/` |
| VOLATILE 테이블 | `/dbms/core-concepts/volatile-table/` |
| RDB 테이블 | `/dbms/core-concepts/rdb-table/` |
| ROLLUP | `/dbms/core-concepts/rollup/` |
| STREAM | `/dbms/core-concepts/stream/` |
| Append (개념) | `/dbms/application-integration/concepts-common/append/` |
| AUTH KEY | `/dbms/security-access-control/authentication-auth-key/` |

## 데이터 입력

| 방법 | 정규 URL |
|------|----------|
| Append API (공통 개념) | `/dbms/application-integration/concepts-common/append/` |
| machloader (CSV/파일 입력) | `/dbms/application-integration/tools/machloader/` |
| Collector | `/dbms/application-integration/tools/collector/` |
| Fluentd 플러그인 | `/dbms/application-integration/tools/fluentd/` |

## 드라이버 가이드

| SDK | 정규 URL |
|-----|----------|
| JDBC | `/dbms/application-integration/guide-drivers/jdbc/` |
| Python (machbaseAPI) | `/dbms/application-integration/guide-drivers/python/` |
| Go (native / machcli) | `/dbms/application-integration/guide-drivers/go/` |
| Go (database/sql) | `/dbms/application-integration/guide-drivers/go-sql/` |
| .NET (MachConnector) | `/dbms/application-integration/guide-drivers/.net/` |
| Node.js | `/dbms/application-integration/guide-drivers/node/` |
| ODBC/CLI | `/dbms/application-integration/guide-drivers/odbc-cli/` |
| REST API | `/dbms/application-integration/guide-drivers/rest-api/` |
| SDK 지원 범위 전체 | `/dbms/application-integration/support-scope-sdk/` |

## 운영

| 항목 | 정규 URL |
|------|----------|
| 서버 시작/중지 | `/dbms/operations-configuration-recovery/startup-configuration/` |
| BACKUP / RESTORE | `/dbms/operations-configuration-recovery/backup-restore-mount/` |
| MOUNT / UNMOUNT | `/dbms/operations-configuration-recovery/backup-restore-mount/mount/` |
| ALTER SYSTEM | `/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/` |
| 설정 레퍼런스 | `/dbms/reference/configuration/` |
| ROLLUP 운영 | `/dbms/core-concepts/rollup/` |
| STREAM 운영 | `/dbms/core-concepts/stream/` |

## 보안

| 항목 | 정규 URL |
|------|----------|
| 계정 관리 (CREATE/ALTER/DROP USER) | `/dbms/security-access-control/user-management/` |
| 권한 관리 (GRANT/REVOKE) | `/dbms/security-access-control/privileges/grant-revoke/` |
| AUTH KEY 설정 | `/dbms/security-access-control/authentication-auth-key/` |
| 원격 접속 설정 | `/dbms/security-access-control/remote-access/` |

## SQL 레퍼런스

| 항목 | 정규 URL |
|------|----------|
| SQL 레퍼런스 전체 | `/dbms/reference/sql/` |
| DDL (CREATE/ALTER/DROP) | `/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/` |
| DML (INSERT/UPDATE/DELETE) | `/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/` |
| SELECT | `/dbms/reference/sql/syntax-dictionary-sql/select-syntax/` |
| 내장 함수 | `/dbms/reference/sql/builtin-functions/` |
| 데이터 타입 | `/dbms/reference/sql/data-types/` |
| 에러 코드 | `/dbms/reference/error-dictionary-codes/` |
| 지원 범위와 제약 | `/dbms/reference/support-scope-constraints/` |

## 문제 해결

| 항목 | 정규 URL |
|------|----------|
| 문제 해결 전체 | `/dbms/troubleshooting/` |
| 서버 접속 문제 | `/dbms/troubleshooting/server-connection/` |
| 성능 문제 | `/dbms/troubleshooting/performance/` |
| 자동화 문제 (ROLLUP/STREAM) | `/dbms/troubleshooting/automation/` |
| Cluster 문제 | `/dbms/troubleshooting/cluster/` |
