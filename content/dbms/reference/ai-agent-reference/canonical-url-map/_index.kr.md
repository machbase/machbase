---
type: docs
title: '18.10.2 canonical-url-map'
weight: 20
toc: true
---

이 페이지는 Machbase의 주요 기능과 개념별 정규 URL 맵입니다. AI 에이전트가 문서 링크를 생성하거나 RAG 시스템이 문서를 참조할 때 사용합니다.

## 핵심 개념

| 개념 | 정규 URL |
|------|----------|
| 데이터 모델 개요 | `/dbms/core-concepts/` |
| TAG 테이블 | `/dbms/tag-table-usage/` |
| LOG 테이블 | `/dbms/log-table-usage/` |
| LOOKUP 테이블 | `/dbms/lookup-table-usage/` |
| VOLATILE 테이블 | `/dbms/volatile-table-usage/` |
| TRANSACTION 테이블 | `/dbms/rdb-table-usage/` |
| ROLLUP | `/dbms/core-concepts/features-concepts/#role-statistics-rollup` |
| STREAM | `/dbms/core-concepts/features-concepts/#processing-model-stream` |
| Append (개념) | `/dbms/application-integration/concepts-common/#append-api-batch` |
| AUTH KEY | `/dbms/security-access-control/authentication-auth-key/` |
| 다중 데이터베이스 | `/dbms/operations-configuration-recovery/multi-database/` |

## 데이터 입력

| 방법 | 정규 URL |
|------|----------|
| Append API (공통 개념) | `/dbms/application-integration/concepts-common/#append-api-batch` |
| machloader (CSV/파일 입력) | `/dbms/application-integration/data-input-load-export/#file-import-machloader` |
| Collector | `/dbms/operations-configuration-recovery/collector/` |
| Fluentd 플러그인 | `/dbms/application-integration/external-tools/#fluentd-plugin` |

## 개발 도구 API와 실무 가이드

| SDK | 정규 URL |
|-----|----------|
| JDBC API | `/dbms/development-tools-integration/jdbc/` |
| Python API | `/dbms/development-tools-integration/python/` |
| Go API (native / machgo) | `/dbms/development-tools-integration/go/` |
| .NET API (MachConnector) | `/dbms/development-tools-integration/net-connector/` |
| Node.js API | `/dbms/development-tools-integration/node-js-typescript/` |
| ODBC/CLI API | `/dbms/development-tools-integration/cli-odbc/` |
| 실무 드라이버 가이드 | `/dbms/application-integration/guide-drivers/` |
| REST API 레퍼런스 | `/dbms/reference/rest-api/` |
| REST API 실무 가이드 | `/dbms/application-integration/rest-api/` |
| SDK 지원 범위 전체 | `/dbms/development-tools-integration/#sdk` |
| Nullable 메타데이터 지원 | `/dbms/development-tools-integration/#support-scope-sdk-nullable-metadata` |
| Named Bind Parameter | `/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/` |

## 운영

| 항목 | 정규 URL |
|------|----------|
| 서버 시작/중지 | `/dbms/operations-configuration-recovery/server-database/` |
| BACKUP / RESTORE | `/dbms/operations-configuration-recovery/backup-restore-mount/` |
| MOUNT / UMOUNT | `/dbms/operations-configuration-recovery/backup-restore-mount/#database-mount` |
| ALTER SYSTEM | `/dbms/reference/sql/syntax-dictionary-sql/system-session-alter-syntax/` |
| 설정 레퍼런스 | `/dbms/reference/configuration/` |
| ROLLUP 운영 | `/dbms/tag-rollup-usage/` |
| STREAM 운영 | `/dbms/operations-configuration-recovery/automation-stream/#stream` |
| 논리 database 문법 | `/dbms/reference/sql/syntax-dictionary-sql/database-syntax/` |

## 보안

| 항목 | 정규 URL |
|------|----------|
| 계정 관리 (CREATE/ALTER/DROP USER) | `/dbms/security-access-control/account/#create-delete-user` |
| 권한 관리 (GRANT/REVOKE) | `/dbms/security-access-control/privileges/#grant-revoke` |
| AUTH KEY 설정 | `/dbms/security-access-control/authentication-auth-key/` |
| 원격 접속 설정 | `/dbms/security-access-control/access-control/#remote-access-configuration` |

## SQL 레퍼런스

| 항목 | 정규 URL |
|------|----------|
| SQL 레퍼런스 전체 | `/dbms/reference/sql/` |
| DDL (CREATE/ALTER/DROP) | `/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/` |
| DML (INSERT/UPDATE/DELETE) | `/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/` |
| SELECT | `/dbms/reference/sql/syntax-dictionary-sql/select-syntax/` |
| WITH / CTE (Standard Edition) | `/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/` |
| Named Bind Parameter | `/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/` |
| DATABASE lifecycle / USE | `/dbms/reference/sql/syntax-dictionary-sql/database-syntax/` |
| 내장 함수 | `/dbms/reference/sql/dictionary/` |
| 데이터 타입 | `/dbms/reference/sql/type-data-types-dictionary/` |
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
